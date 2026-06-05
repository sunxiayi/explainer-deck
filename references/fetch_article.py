#!/usr/bin/env python3
"""Fetch a Substack or Medium article URL and produce article.txt + article_meta.json.

Tries curl first; falls back to `neo` (Chrome CDP bridge) for paywalled or
JS-heavy pages. Logs errors RED, warnings YELLOW (no emoji).
"""

from __future__ import annotations

import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib import request as urlrequest
from urllib.parse import urlparse

RED = "\x1b[31m"
YELLOW = "\x1b[33m"
RESET = "\x1b[0m"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/16.6 Safari/605.1.15"
)

PAYWALL_SENTINELS = (
    "this post is for paid subscribers",
    "subscribe to read",
    "subscribers only",
    "post is for paying subscribers",
    "member-only story",
    "this story is for members",
    "this story is paywalled",
    "you've reached your free reading limit",
)

MIN_BODY_BYTES = 2048

DROP_TAGS = {
    "script",
    "style",
    "noscript",
    "nav",
    "footer",
    "header",
    "aside",
    "button",
    "form",
    "iframe",
    "svg",
}

KEEP_TAGS = {"h1", "h2", "h3", "h4", "p", "li", "blockquote", "pre", "code"}


class SubstackHtmlExtractor(HTMLParser):
    """Extract clean text from Substack HTML.

    Captures:
      - title (first <h1> inside main article body, or <title>)
      - byline (looks for substack-specific author markers)
      - body text from KEEP_TAGS, with one blank line between blocks
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._stack: list[str] = []
        self._drop_depth = 0
        self._buf: list[str] = []
        self._current_block: list[str] = []
        self._title_from_tag = ""
        self._first_h1 = ""
        self._page_title = ""
        self._byline = ""
        self._publication = ""
        self._capture_h1 = False
        self._capture_title = False
        self._meta_collected: dict[str, str] = {}
        self._images: list[dict[str, str]] = []
        self._seen_image_srcs: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: (v or "") for k, v in attrs}
        if tag == "meta":
            name = attrs_d.get("name", "").lower() or attrs_d.get("property", "").lower()
            content = attrs_d.get("content", "")
            if name == "og:title" and content:
                self._meta_collected.setdefault("og_title", content)
            elif name == "og:site_name" and content:
                self._meta_collected.setdefault("og_site_name", content)
            elif name == "author" and content:
                self._meta_collected.setdefault("meta_author", content)
            elif name == "article:author" and content:
                self._meta_collected.setdefault("article_author", content)
            elif name == "twitter:title" and content:
                self._meta_collected.setdefault("twitter_title", content)
            elif name in ("article:published_time", "datepublished", "og:article:published_time") and content:
                self._meta_collected.setdefault("published_at", content)
            return
        if tag == "time":
            dt = attrs_d.get("datetime", "")
            if dt and "published_at" not in self._meta_collected:
                self._meta_collected["published_at"] = dt
            return
        if tag == "title":
            self._capture_title = True
            return
        if tag in DROP_TAGS:
            self._drop_depth += 1
            return
        if tag == "img":
            src = attrs_d.get("src", "") or attrs_d.get("data-src", "")
            alt = attrs_d.get("alt", "").strip()
            if src and src not in self._seen_image_srcs and self._is_content_image(src, attrs_d):
                self._seen_image_srcs.add(src)
                placeholder = f"__IMG_{len(self._images)}__"
                self._images.append({"src": src, "alt": alt, "placeholder": placeholder})
                self._buf.append(placeholder)
            return
        self._stack.append(tag)
        if tag == "h1" and not self._first_h1:
            self._capture_h1 = True
            self._current_block = []
        elif tag in KEEP_TAGS:
            self._current_block = []
        elif tag == "br":
            if self._current_block:
                self._current_block.append("\n")

    @staticmethod
    def _is_content_image(src: str, attrs: dict[str, str]) -> bool:
        # Filter out tracking pixels, avatars, icons.
        lower = src.lower()
        if any(s in lower for s in ("avatar", "favicon", "logo", "tracking", "1x1.gif", "spacer.gif", "pixel.gif")):
            return False
        # Substack CDN encodes resize hints like ",w_40,h_40," — anything ≤ 200 is decorative.
        cdn_size = re.search(r"[,/]w_(\d+)(?:,h_(\d+))?", lower)
        if cdn_size:
            try:
                w = int(cdn_size.group(1))
                h = int(cdn_size.group(2)) if cdn_size.group(2) else w
                if w <= 200 and h <= 200:
                    return False
            except ValueError:
                pass
        # Medium CDN (miro.medium.com) uses `resize:fit:NNN` / `resize:fill:N:N` hints.
        medium_size = re.search(r"resize:(?:fit|fill):(\d+)(?::(\d+))?", lower)
        if medium_size:
            try:
                w = int(medium_size.group(1))
                h = int(medium_size.group(2)) if medium_size.group(2) else w
                if w <= 200 and h <= 200:
                    return False
            except ValueError:
                pass
        try:
            w = int(attrs.get("width", "0") or 0)
            h = int(attrs.get("height", "0") or 0)
            if 0 < w < 200 or 0 < h < 200:
                return False
        except ValueError:
            pass
        return True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
            return
        if tag in DROP_TAGS:
            if self._drop_depth > 0:
                self._drop_depth -= 1
            return
        if not self._stack:
            return
        if self._stack[-1] == tag:
            self._stack.pop()
        if tag == "h1" and self._capture_h1:
            self._capture_h1 = False
            text = " ".join("".join(self._current_block).split()).strip()
            if text and not self._first_h1:
                self._first_h1 = text
            if text:
                self._buf.append(f"# {text}")
            self._current_block = []
        elif tag in KEEP_TAGS:
            text = "".join(self._current_block).strip()
            if not text:
                self._current_block = []
                return
            if tag in ("h2", "h3", "h4"):
                level = "##" if tag == "h2" else ("###" if tag == "h3" else "####")
                self._buf.append(f"{level} {text}")
            elif tag == "li":
                self._buf.append(f"- {text}")
            elif tag == "pre" or tag == "code":
                # Only keep code blocks if inside <pre> or top-level code blocks.
                self._buf.append(f"```\n{text}\n```")
            elif tag == "blockquote":
                self._buf.append(f"> {text}")
            else:
                self._buf.append(text)
            self._current_block = []

    def handle_data(self, data: str) -> None:
        if self._drop_depth > 0:
            return
        if self._capture_title:
            self._title_from_tag += data
            return
        if self._capture_h1 or (self._stack and self._stack[-1] in KEEP_TAGS):
            self._current_block.append(data)

    def result(self) -> dict[str, str]:
        body = "\n\n".join(b for b in self._buf if b.strip())
        title = (
            self._meta_collected.get("og_title")
            or self._meta_collected.get("twitter_title")
            or self._first_h1
            or self._title_from_tag.strip()
        )
        # Substack <title>: "Article Title - Publication Name"
        # Medium  <title>: "Article Title | Publication" or "Article Title - Medium"
        publication = self._meta_collected.get("og_site_name", "")
        if not publication:
            for sep in (" | ", " - "):
                if sep in self._title_from_tag:
                    publication = self._title_from_tag.rsplit(sep, 1)[-1].strip()
                    break
        if title and publication:
            for sep in (" | ", " - "):
                suffix = f"{sep}{publication}"
                if title.endswith(suffix):
                    title = title[: -len(suffix)].strip()
                    break
        if title and not self._meta_collected.get("og_title"):
            for sep in (" | ", " - "):
                if sep in title:
                    title = title.rsplit(sep, 1)[0].strip()
                    break
        byline = (
            self._meta_collected.get("article_author")
            or self._meta_collected.get("meta_author")
            or ""
        )
        date = self._meta_collected.get("published_at", "").strip()
        if date:
            # Normalize ISO 8601 to YYYY-MM-DD.
            m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", date)
            if m:
                date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        return {
            "title": title.strip(),
            "publication": publication.strip(),
            "byline": byline.strip(),
            "body": body,
            "images": list(self._images),
            "date": date,
        }


def download_image(src: str, dest_dir: Path, index: int) -> str:
    if not src or src.startswith("data:"):
        return ""
    try:
        req = urlrequest.Request(src, headers={"User-Agent": USER_AGENT})
        with urlrequest.urlopen(req, timeout=20) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "").split(";")[0].strip()
        ext = mimetypes.guess_extension(content_type) or ""
        if not ext:
            url_path = urlparse(src).path
            ext = os.path.splitext(url_path)[1].lower() or ".jpg"
        if ext == ".jpe":
            ext = ".jpg"
        local_name = f"{str(index).zfill(2)}{ext}"
        (dest_dir / local_name).write_bytes(data)
        return local_name
    except Exception as exc:  # noqa: BLE001
        print(f"{YELLOW}WARNING: image download failed for {src}: {exc}{RESET}", file=sys.stderr)
        return ""


def slug_from_url(url: str) -> str:
    parts = [p for p in urlparse(url).path.split("/") if p]
    if not parts:
        return "substack-article"
    slug = parts[-1]
    # Medium appends a 12-char hex id to the slug (e.g. "title-abc123def456").
    # Strip it so output dir names stay readable.
    if is_medium_host(urlparse(url).netloc):
        slug = re.sub(r"-[0-9a-f]{8,}$", "", slug)
    return slug


def is_medium_host(host: str) -> bool:
    """True if the host is a Medium-hosted publication."""
    host = host.lower()
    if host == "medium.com" or host.endswith(".medium.com"):
        return True
    # Well-known Medium-hosted publications on custom domains.
    return host in {
        "towardsdatascience.com",
        "betterprogramming.pub",
        "uxdesign.cc",
        "uxplanet.org",
        "blog.devgenius.io",
        "javascript.plainenglish.io",
        "python.plainenglish.io",
        "levelup.gitconnected.com",
        "betterhumans.pub",
    }


def fetch_curl(url: str) -> tuple[int, bytes]:
    proc = subprocess.run(
        [
            "curl",
            "-sSL",
            "-A",
            USER_AGENT,
            "-H",
            "Accept-Language: en-US,en;q=0.9",
            "--max-time",
            "30",
            "-w",
            "\n__HTTP_CODE__:%{http_code}",
            url,
        ],
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return 0, b""
    out = proc.stdout
    match = re.search(rb"\n__HTTP_CODE__:(\d+)\s*$", out)
    if not match:
        return 0, out
    code = int(match.group(1))
    body = out[: match.start()]
    return code, body


def looks_paywalled(body_text: str) -> bool:
    lo = body_text.lower()
    return any(s in lo for s in PAYWALL_SENTINELS)


def extract_via_html(html_bytes: bytes) -> dict[str, str]:
    try:
        text = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = html_bytes.decode("utf-8", errors="replace")
    parser = SubstackHtmlExtractor()
    parser.feed(text)
    parser.close()
    return parser.result()


def fetch_neo(url: str) -> str:
    """Fall back to neo Chrome CDP bridge. Best effort — returns text."""
    if not shutil.which("neo"):
        raise RuntimeError("neo CLI not found in PATH; cannot fall back from curl")
    print(f"{YELLOW}WARNING: curl fetch insufficient, falling back to neo{RESET}", file=sys.stderr)
    # Open the URL in an existing/new neo Chrome session. `neo open` is non-blocking.
    subprocess.run(["neo", "open", url], check=False, capture_output=True)
    # Give the page a moment to settle. neo's `read` waits for tab content.
    proc = subprocess.run(
        ["neo", "read", url],
        capture_output=True,
        check=False,
        timeout=60,
    )
    text = proc.stdout.decode("utf-8", errors="replace").strip()
    if not text:
        # Some neo versions use `dom-text` instead
        proc = subprocess.run(
            ["neo", "dom-text"],
            capture_output=True,
            check=False,
            timeout=30,
        )
        text = proc.stdout.decode("utf-8", errors="replace").strip()
    return text


def fetch(url: str) -> dict[str, str]:
    code, body = fetch_curl(url)
    if code == 200 and len(body) >= MIN_BODY_BYTES:
        parsed = extract_via_html(body)
        if parsed["body"] and not looks_paywalled(parsed["body"]):
            parsed["source"] = url
            parsed["fetch_method"] = "curl"
            return parsed
        if looks_paywalled(parsed["body"]):
            print(f"{YELLOW}WARNING: paywall sentinel detected in curl response, falling back to neo{RESET}", file=sys.stderr)
    elif code != 200:
        print(f"{YELLOW}WARNING: curl returned HTTP {code}, falling back to neo{RESET}", file=sys.stderr)
    else:
        print(f"{YELLOW}WARNING: curl body too small ({len(body)} bytes), falling back to neo{RESET}", file=sys.stderr)

    text = fetch_neo(url)
    if not text:
        raise RuntimeError("neo fallback returned empty content")
    # neo gives plain text (no HTML), so we cannot reliably split title/body
    # from structure. Split on the first blank line as a heuristic.
    lines = [ln for ln in text.splitlines() if ln.strip()]
    title = lines[0] if lines else ""
    body_text = "\n\n".join(lines[1:]) if len(lines) > 1 else text
    return {
        "title": title,
        "publication": "",
        "byline": "",
        "body": body_text,
        "source": url,
        "fetch_method": "neo",
    }


def main() -> int:
    if len(sys.argv) < 3:
        print(
            f"{RED}Usage: fetch_substack.py <url> <output_dir>{RESET}",
            file=sys.stderr,
        )
        return 2
    url = sys.argv[1]
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        data = fetch(url)
    except Exception as exc:  # noqa: BLE001
        print(f"{RED}ERROR: fetch failed: {exc}{RESET}", file=sys.stderr)
        return 1

    if not data.get("body", "").strip():
        print(f"{RED}ERROR: no article body extracted{RESET}", file=sys.stderr)
        return 1

    body = data["body"]
    images = data.get("images", []) or []
    images_dir = out_dir / "images"
    downloaded: list[dict[str, str]] = []
    if images:
        images_dir.mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(images, 1):
            local_name = download_image(img["src"], images_dir, i)
            placeholder = img["placeholder"]
            if local_name:
                rel = f"images/{local_name}"
                body = body.replace(placeholder, f"\n\n![{img.get('alt','')}]({rel})\n\n")
                downloaded.append({"src": img["src"], "local": rel, "alt": img.get("alt", "")})
            else:
                body = body.replace(placeholder, "")
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    article_path = out_dir / "article.txt"
    meta_path = out_dir / "article_meta.json"
    article_path.write_text(body, encoding="utf-8")
    meta = {
        "title": data.get("title", ""),
        "publication": data.get("publication", ""),
        "byline": data.get("byline", ""),
        "date": data.get("date", ""),
        "source": data.get("source", url),
        "fetch_method": data.get("fetch_method", ""),
        "slug": slug_from_url(url),
        "images": downloaded,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"article: {article_path}")
    print(f"meta: {meta_path}")
    print(f"title: {meta['title']}")
    print(f"publication: {meta['publication']}")
    print(f"byline: {meta['byline']}")
    print(f"slug: {meta['slug']}")
    print(f"method: {meta['fetch_method']}")
    print(f"bytes: {len(data['body'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
