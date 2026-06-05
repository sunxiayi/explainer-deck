---
name: explainer-deck
description: Build a beginner-friendly "陪读 PPT" / explainer deck (single-HTML teaching deck) that walks the user through a dense technical article paragraph by paragraph. Output language is set by the `--language` flag (english default, or chinese). Use when the user shares a hard-to-read article and asks for help understanding it ("帮我读懂这篇", "做个 PPT 讲", "陪读 PPT", "图文并茂讲讲", "我看不懂", "拆解一下让我理解", "给我做个教学 deck", "explain this article", "make me a teaching deck", "walk me through this paper"). The deck has two parts: foundation slides (basic terms explained from scratch — token, GPU, wafer, etc.) + article walkthrough slides (paragraph-by-paragraph with analogies, math, diagrams, and real photos). Flags: `--language <english|chinese>`, `--image <neo|gemini|gpt> [--api-key …]`. Output is one self-contained `index.html` with sticky TOC, keyboard navigation, dark theme, and embedded images.
---

# Explainer Deck — Single-HTML 陪读 PPT Generator

Take a dense technical article and produce a single-HTML teaching deck that explains it from scratch, **in the language set by `--language` (default `english`; or `chinese`)**. Audience is a smart college sophomore/junior who doesn't have the specific domain background (hardware, finance, biology, etc.).

The output is a **single `index.html`** file in the article's folder, with:

- Dark theme + yellow accent
- Sticky left-side TOC
- Keyboard navigation (← / → / space)
- Embedded real photos (downloaded from the article source or related sites)
- ~60 slides typical (15 foundation + 45 walkthrough)

## When to invoke

Triggers — the user has shared a long technical article (could be SemiAnalysis, a paper, a textbook chapter, a Cerebras/Nvidia whitepaper, a financial S-1, etc.) and asks any of:

- "帮我读懂这篇"
- "做个 PPT 给我讲讲"
- "陪读 PPT"
- "图文并茂讲讲"
- "我看不懂这个"
- "给我做个教学 deck"
- "explain this article to me"
- "我应该当作小白来看，给我从头讲"

The trigger is **comprehension help**, not summarization or republishing. If the user wants a short summary or xhs card, use a different skill.

## Input

### Required

One of:

- A URL — Substack, IEEE Spectrum, arxiv, blog post, anything web-accessible
- A local path to an already-fetched `article.txt` and `article_meta.json`

### Optional

- Reader level — default "CS sophomore-level, no domain background." User can specify ("我已经懂 GPU 架构" / "I already know GPU architecture") to skip relevant foundation slides.
- Target slide count — default ~60 (15 foundation + ~45 walkthrough). Long articles → more walkthrough slides.

### Flags

Parse these from the user's invocation (e.g. `/explainer-deck <url> --language chinese --image neo`):

- **`--language <english|chinese>`** — output language of the whole deck. **Default: `english`.**
  - `english` (default): write every slide + TOC + boxes in English. Deepdive resources are **English-only** — do NOT hunt for Chinese (知乎/B站) supplementary links (skip the bilingual mandate in Step 7.5). Set `<html lang="en">`. Voice: apply the general anti-AI-voice rules (no hype, no false-dichotomy, no absolutes) but the Chinese-specific banlist in `references/anti-ai-voice.md` does not apply.
  - `chinese`: write the deck in Chinese (the original behavior). Deepdive boxes MUST be bilingual EN+CN (Step 7.5). `<html lang="zh-CN">`. Apply the full Chinese anti-AI-voice banlist.
  - When spawning walkthrough agents (Step 4), pass the chosen language into every agent prompt so they write in it.

- **`--image <neo|gemini|gpt>` [`--api-key <KEY>`]** — which backend to use for **③ AI image-gen** in Step 5.5. If this flag is absent, do NOT drive any AI image backend — use only ① download + ② SVG for visuals.
  - `--image neo` — drive ChatGPT via neo (Path B). **Activate it yourself** (`neo start` → open chatgpt.com → probe login). If it stalls or hits a login wall / DOM drift you can't get past, **stop and ask the user for help** (don't silently fall back). No `--api-key` needed.
  - `--image gemini --api-key XXX` — use the **Gemini / Imagen** image API with the supplied key (Path A). Read the current official docs before coding the call.
  - `--image gpt --api-key XXX` — use the **OpenAI gpt-image** API with the supplied key (Path A). Read the current official docs before coding the call.
  - Still apply the ①/②/③ decision rule (Step 5.5): even with `--image` set, only route *illustrative/analogy* or genuinely-better-as-raster concepts to ③; keep precise structural diagrams as ② SVG. The flag chooses the AI backend; it doesn't force every visual through AI.

## Output structure

```
${PROJECT_ROOT}/<article-source-dir>/explainer/
├── index.html                  # The deck — single self-contained file
└── img/
    ├── <several real photos>.{png,jpeg}
    └── ...
```

`<article-source-dir>` defaults to the article fetcher's output directory. For example, if the fetcher wrote `articles/<slug>/article.txt`, the deck goes in `articles/<slug>/explainer/`.

## Pipeline (10 steps)

### Step 1 — Fetch the article (skip if already fetched)

If the user gives a URL and we don't already have `article.txt`, fetch via:

```bash
python3 .claude/skills/explainer-deck/references/fetch_article.py "<url>" "<output_dir>"
```

(This works for Substack, Medium, blog, IEEE Spectrum, most paywalled-but-readable pages — uses curl with neo fallback.)

For other sources, use WebFetch or curl directly.

### Step 2 — Read the article + plan slide structure

Read `article.txt` in full. Then plan two lists:

**A. Foundation slide list** — every jargon term that a CS sophomore wouldn't know cold. Examples from prior decks:

- LLM inference, token, KV cache, transformer
- GPU, Tensor Core, FLOPs, bandwidth, arithmetic intensity, roofline
- SRAM / HBM / DDR memory hierarchy
- Wafer / die / chip, lithography, mask/reticle, reticle limit, scribe line
- Yield, yield harvesting
- Sharding (tensor / data / pipeline parallel)
- Data center: rack, PSU, CDU, LPM/kW, free cooling
- (For financial articles: warrant, dilution, MRA, contra-revenue, etc.)
- (For bio articles: different list entirely)

Cap at **~15 foundation slides**. If more terms exist, group related ones onto one slide.

**B. Walkthrough slide list** — paragraph by paragraph, what to cover. Each section of the article gets 4-15 slides depending on density. Target **~45 walkthrough slides** for a 4000-word article; scale up for longer.

### Step 3 — Write the deck shell + foundation slides yourself

The deck shell is a copy of `references/deck-template.html` (full file, ready to use). Just clone it into the output dir as `index.html` and customize the `<title>` + the TOC part-1 entries.

**Match the template chrome to `--language`:** the template ships with Chinese chrome — `<html lang="zh-CN">` and the TOC part headers `第一部分 · 基础知识` / `第二部分 · 文章逐段`. For an `--language english` deck, set `<html lang="en">` and translate those headers (`Part 1 · Foundations` / `Part 2 · Article walkthrough`), plus the `SLIDE NN` label stays as-is. Keep them Chinese only for a `--language chinese` deck.

Then **write all foundation slides yourself** (not via agent). These are the vocabulary that every later slide will reference — they must be consistent and high-quality. Use the templates in `references/slide-patterns.md` as building blocks.

Save the result. Verify it opens cleanly in a browser before continuing.

### Step 4 — Spawn parallel agents for the walkthrough sections

Divide the article's sections into 3-5 chunks (typical: 3). Spawn one agent per chunk **in parallel** (single message, multiple `Agent` tool calls).

Each agent receives:

- The article path
- The deck `index.html` path (so they see the existing CSS classes)
- Their assigned slide ID range (e.g. s16–s30)
- Which article sections to cover
- A foundation slide map ("slide N already explains X, just say 'see slide N'")
- Voice rules (Chinese, no emoji, no AI-flavored patterns)
- Format rules (full `<section class="slide" id="sN">…</section>` blocks)
- Output file path (e.g. `part2-A.html`)

Each agent writes its slides to its own file plus a `<!-- TOC … TOC -->` comment block at the end with the TOC entries it wants.

See `references/workflow.md` for the exact agent prompt template.

### Step 5 — Get the article's OWN figures first, then other real images

**RULE: if the source article contains a figure, you MUST attach the original figure.** The article's own diagrams are authoritative — they can't be subtly wrong the way an AI-generated image or hand-drawn ASCII can. Always prefer the original over a substitute. (AI-generated diagrams in Step 5.5 are only for concepts the article did NOT illustrate.)

**Extracting the article's own figures (do this FIRST):**
Many blogs (Cerebras, Substack, Medium) **lazy-load** their figures — they're absent from a static `curl` of the HTML (you'll see `<img>` count ≈ 0 or only the logo/OG image). To get them:
1. Open the article in the real browser: `neo open "<url>"`, then `neo tab --url <slug>`.
2. Let it render / scroll to trigger lazy-load. Pull figure URLs from the **live DOM**:
   `neo eval '[].slice.call(document.querySelectorAll("img")).filter(i=>i.naturalWidth>=400).map(i=>({src:i.src,alt:i.alt,w:i.naturalWidth}))' --tab <slug>`
3. Download each. If the URL needs the site's cookies (e.g. `backend-api/.../content?id=`), fetch it **in-page** as base64 (same trick as the ChatGPT image grab in Step 5.5) rather than curl.
4. **Read each downloaded PNG** to confirm it's the actual figure (not a logo/banner/OG card) before keeping it. Caption as `来源：<publication> 原文 Figure N`.

Then ALSO use `WebSearch` + `WebFetch` for canonical product photos / diagrams / screenshots to supplement. Good sources:

- The article itself (paywalled articles usually have images visible via the public CDN URL — substack uses `substack-post-media.s3.amazonaws.com/public/images/<UUID>_<W>x<H>.<ext>` direct S3 URLs which are usually unprotected even when the article is paywalled)
- The company's own press kit (Cerebras: `cdn.sanity.io/images/...`)
- IEEE Spectrum, Tom's Hardware, AnandTech archives, Wikipedia Commons
- For diagrams in the article: try to extract via WebFetch on the source

Download via curl into `<output_dir>/explainer/img/`. **Verify each file is real** (not 9-byte error pages, not duplicates with same MD5):

```bash
md5 img/*.{png,jpeg}  # check for duplicates
ls -lh img/           # check sizes (real images >50KB usually)
```

If a CDN URL with `$` in it fails, try the same image from the source S3 URL directly (often unsigned and works).

Aim for **5-10 real images**. Embed them in the most relevant slides using:

```html
<div class="figure">
  <img src="img/<file>.png" alt="...">
  <div class="figure-caption">… <span class="src">来源：…</span></div>
</div>
```

Or side-by-side:

```html
<div class="figure-row">
  <div class="figure">…</div>
  <div class="figure">…</div>
</div>
```

### Step 5.5 — Generate concept diagrams (AI image-gen)

Real photos (Step 5) cover the physical stuff (the chip, the system). For the **abstract concepts** that are hard to grasp from text alone, add a visual.

**HARD RULE — every technically-complex / abstract / hard-to-grasp concept MUST get a figure (a real photo ①, an SVG ②, or an AI image ③). No "it's just text" excuse.** Text + a table is NOT enough for a genuinely hard idea. Walk every slide and ask "would a beginner struggle to picture this?" — if yes, it needs a figure. This is ON by default; don't wait for the user to ask for 配图. A typical 60-slide deck ends up with **8-12 figures**, not 2-3. Concretely, these almost always need one: layered/nested structures, before/after topology, "who connects to what" fabrics, anything scaling as N vs N² (geometry), a protocol stack collapsing into one, dataflow, a physical stack (TSV/HBM/bonding). When in doubt, add the figure.

**Three ways to get a visual — judge PER CONCEPT by context. All three belong in the toolbox; a good deck usually mixes all three.**

| Approach | Best for | Cost |
|---|---|---|
| **① Download a real figure/photo** (Step 5) | physical objects + already-existing authoritative diagrams — the chip, wafer, package, server rack, an official labeled cross-section | fast, authoritative |
| **② Hand-authored SVG** | *structural / spatial schematics* needing exact labels & boxes — layer stacks, who-connects-to-what, before/after topology, the τ nest. Labels never garble, structure is exact (accuracy-first). | fast, precise |
| **③ AI image-gen** (image model, below) | *illustrative / organic / analogy* art where a hand-drawn-feeling picture helps and exact label precision matters less — "a city of cores", textured scenes, metaphor art | slow / needs a path |

Decision rule: real thing exists → **①**. Precise structure/labels → **②**. Loose conceptual/analogy art → **③**. Don't force one approach onto every concept.

**AI image-gen (③) runs only when the `--image` flag is set** (see Flags above). If `--image` is absent, do NOT drive any AI backend — use ① download + ② SVG only. When `--image` IS set, use the matching backend and wire it up YOURSELF — don't treat "not connected" as a blocker:
- **`--image gpt` / `--image gemini`** → Path A with the supplied `--api-key`.
- **`--image neo`** → Path B, **activate it yourself**:
   - `neo start` (launches Chrome with the neo extension + CDP on 9222 using the `~/.neo/chrome-profile`, which usually already holds the chatgpt.com login — check `neo status`: a high `chatgpt.com:` capture count means it's been used there).
   - `neo open https://chatgpt.com/` → wait → `neo tab --url chatgpt` → probe login with a composer check (`#prompt-textarea` exists, no "Log in" wall).
   - If `neo start` stalls, ChatGPT shows a login wall, or the DOM drifts so you can't retrieve the image — **stop and ask the user for help** (e.g. "log into chatgpt.com in the neo Chrome and tell me when ready"). Don't silently bail to SVG.

Caption ② and ③ honestly as `示意图`/`生成示意图` / `schematic (illustrative)` (no fake "original figure" / source claim).

**WHAT each approach is good at:**
- **Structural / spatial diagrams** — "who sits where, what connects to what": distributed memory (SRAM next to each core), dataflow, wafer/die/scribe-line, 2D mesh fabric, layer stacks, before/after topology. → **Prefer ② SVG** (exact labels, exact structure). Image-gen (③) can do these too but tends to mislabel — only use ③ here if you want a looser illustrative look and will Read-review hard.
- **Precise-scale / ordered diagrams** — roofline curves with a specific ridge point, exact GEMM reduction step-order, anything with meaningful numeric axes. Image models get these subtly WRONG. **Keep as ASCII `<pre>` or a ② SVG** — both are more accurate. Keeps the diagram accurate — accuracy over a prettier-but-wrong picture.
- **Illustrative / analogy art** — a metaphor scene, "imagine a city of cores", textured conceptual art where precise labels don't matter. → **③ AI image-gen** shines here.
- **Every visual you generate (② SVG or ③ AI) MUST be reviewed by you before injecting** — render the SVG to PNG (Chrome headless `--screenshot` or `qlmanage`) and Read it; Read the AI PNG directly. Garbled labels / wrong structure → fix the SVG, or regenerate / fall back to SVG for AI. Tell the user which approach you used per concept.

**Prompt recipe** (keeps it on-brand + maximizes label correctness):
> Generate an image: a clean flat technical diagram, 16:9, dark background #0f0f10, yellow (#f4d03f) and cyan (#8be3ff) accents, white SHORT English labels spelled correctly, minimal vector style, NO photorealism, no clutter. Title: '<concept>'. <describe left/right halves, what connects to what, the 2-3 short labels>. Legible.

Keep labels short and few — long text is where image models produce gibberish.

**Two generation paths — selected by the `--image` flag (see Flags above):**

**Path A — image API (FAST, ~10-30s/img, stable, concurrent). Used for `--image gemini --api-key …` or `--image gpt --api-key …`.**
- `--image gpt`: OpenAI `images/generations` (gpt-image-1 / dall-e-3). `--image gemini`: Gemini / Imagen. Use the supplied `--api-key`. Read the official docs before coding the call (your memorized API may be stale).
- Save the returned base64/URL straight to `<EXPLAINER_DIR>/img/<concept>.png`.

**Path B — neo drives ChatGPT web UI (SLOW, no key needed, fragile).** Requires Chrome running with the neo extension, logged into chatgpt.com — **you activate this yourself with `neo start` (see ③ above), don't wait for the user.** Mechanics that actually work (the naive `neo fill` fails on ChatGPT's contenteditable):

**Hard-won gotchas (verified against the ChatGPT web UI):**
- **Sidebar/history thumbnails are 512×512 and WILL false-match** your `estuary/content` filter — the real generated image is large (e.g. **1672×941** for a 16:9 ask). Filter `naturalWidth >= 1000` to skip thumbnails (a 512 hit = stale/wrong image, never download it).
- **If the selected model is a reasoning model (the composer shows "Thinking"), image-gen is SLOW — ~5 min, not 1.5-2 min** (it "Thought for 30s" then renders). Poll up to ~6 min. A non-thinking model (GPT-4o-class) is much faster for pictures; switch model first if you can.
- `[data-message-author-role=assistant]` selectors drift — when introspection returns `numAssistant:0`, don't trust it; **take a `neo screenshot` to see ground truth** (a gray box in the main panel = image still rendering).
- Even when it works, an image model labels in **English** and you can't force Chinese labels reliably — for a Chinese structural diagram, ② SVG (you control every label) usually beats ③ for the actual deck. Use ③ to prove capability / for analogy art.

- Fill the composer via JS injection, not `neo fill`:
  ```js
  // /tmp/_fill.js — set text on the ProseMirror editor
  (function(){var ed=document.querySelector('#prompt-textarea')||document.querySelector('div[contenteditable="true"]')||document.querySelector('textarea');if(!ed)return'NO_EDITOR';ed.focus();var msg=<JSON-encoded prompt>;if(ed.tagName==='TEXTAREA'){ed.value=msg;}else{ed.textContent=msg;}ed.dispatchEvent(new InputEvent('input',{bubbles:true}));return'filled';})()
  ```
  `neo eval "$(cat /tmp/_fill.js)" --tab chatgpt`
- Click send: `button[data-testid="send-button"]` → `.click()` via `neo eval`.
- Image gen takes 1.5-2 min (diffusion = iterative denoising, dozens of steps, server queue). You can't get a "done" event, so **poll the DOM** until a big image appears. Match on the `alt` text (e.g. contains the concept title), NOT just any `<img>` — UI icons and PREVIOUS images in the same thread will false-match:
  ```js
  // count big generated imgs + their alts
  [].slice.call(document.querySelectorAll('img')).filter(i=>/estuary\/content|oaiusercontent/.test(i.src)&&i.naturalWidth>=1000).map(i=>i.alt)
  ```
- Download via an **authenticated in-page fetch** (the `backend-api/estuary/content?id=...` URL needs ChatGPT's cookies — a plain curl won't work):
  ```js
  (async()=>{var img=/*the matched big img*/;var b=await(await fetch(img.src)).blob();var buf=await b.arrayBuffer();var u=new Uint8Array(buf),s='';for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return img.naturalWidth+'x'+img.naturalHeight+'|'+btoa(s);})()
  ```
  Then base64-decode to `img/<concept>.png` in Python. **Verify dims** (should be the 16:9 you asked, e.g. 1672x941) — if you grab a 512x512 it's a stale/wrong image.
- Pacing reality: ~1.5-2 min each, serial. Tell the user the wall-clock up front (5 images ≈ 8-10 min) and offer Path A if they have a key.

**Caption** generated diagrams honestly with `来源：ChatGPT 生成示意图` (or the model used) — never imply it's an official figure.

### Step 6 — Assemble: splice agent outputs into the deck

Use a Python one-liner inside `Bash` to:

1. Read each `part2-X.html` file
2. Extract the slide bodies (everything before `<!-- TOC`)
3. Extract the TOC entries (lines between `<!-- TOC` and `TOC -->`)
4. Replace `<!-- INSERT_PART2_SLIDES -->` in `index.html` with the combined slide bodies
5. Replace `<!-- TOC_INSERT_PART2 -->` in `index.html` with the combined TOC entries

Example script:

```python
import re

parts = {n: open(f'part2-{n}.html').read() for n in ['A','B','C']}
slides, toc = [], []
for n in ['A','B','C']:
    c = parts[n]
    if '<!-- TOC' in c:
        body, t = c.split('<!-- TOC', 1)
        lines = t.split('TOC -->', 1)[0].strip().splitlines()
        toc.extend(l for l in lines if l.strip())
    else:
        body = c
    slides.append(body.rstrip())

html = open('index.html').read()
html = html.replace('  <!-- INSERT_PART2_SLIDES -->', '\n\n'.join(slides) + '\n')
html = html.replace('    <!-- TOC_INSERT_PART2 -->', '    ' + '\n    '.join(toc))
open('index.html', 'w').write(html)
```

### Step 7 — Inject images into walkthrough slides

The agents write text-only slides. After assembling, identify 4-6 walkthrough slides where a real image would help, and `Edit` each slide to inject a `<div class="figure">…</div>` block.

Pattern: image at the **end of the slide body**, before the `.takeaway` box.

### Step 7.5 — Inject "深入" deepdive boxes on key concept slides

For every foundation slide (and selectively for walkthrough slides covering a major concept), add a `.deepdive` box at the end of the slide pointing to 1-3 high-quality external resources — YouTube videos, established blogs, free courses, papers.

Pattern (insert BEFORE `</section>`, AFTER the `.takeaway` box):

```html
<div class="deepdive">
  <div class="deepdive-title">想深入这个概念</div>
  <ul>
    <li><a href="URL" target="_blank">Title</a><span class="meta"> · YouTube · 60 min</span> — 1 line description</li>
    <li><a href="URL" target="_blank">Another Resource</a><span class="meta"> · Blog</span> — 1 line description</li>
  </ul>
</div>
```

Add `· 强推` to the title for one-stop resources that cover the slide's concept end-to-end.

**Bilingual rule — applies ONLY when `--language chinese`.** For an **`--language english`** deck (the default), use **English resources only** — skip the Chinese-resource hunt entirely (no 知乎/B站 lookups) and the rest of this bilingual subsection does not apply.

**When `--language chinese`: every deepdive box must mix English AND Chinese resources.** The deck is Chinese, for Chinese readers — an all-English resource list is a usability failure. For each deepdive box:

- Keep the best 1-2 English resources (Karpathy, Horace He, Asianometry, official blogs, etc.).
- ALSO add 1-2 Chinese-internet resources for the same concept: a 知乎专栏 / 博客园 / CSDN article, and/or a **Bilibili (B站)** video.
- Aim for roughly half-and-half. Order doesn't matter, but never leave a box English-only.
- Find them with `WebSearch` queries like `bilibili <概念> 讲解 up主` and `知乎 <概念> 原理`. Prefer well-known up 主 (3Blue1Brown 中字, ZOMI酱, 老石谈芯, 影视飓风) and stable 知乎专栏 over random reposts.
- **Caveat to state when reporting to the user**: Bilibili reposts and 知乎 links are harder to verify as live/canonical than YouTube. Pick title+author matches you're confident in; tell the user these may occasionally be dead/removed and offer to swap. Do NOT fabricate a BV id — only use BV ids / `space.bilibili.com` URLs that actually appeared in search results.
- Format Chinese entries the same way, with a Chinese meta tag: `<span class="meta"> · B站</span>` or `<span class="meta"> · 知乎</span>` or `<span class="meta"> · 博客园</span>`.

Example bilingual box:
```html
<div class="deepdive">
  <div class="deepdive-title">想深入这个概念</div>
  <ul>
    <li><a href="https://horace.io/brrr_intro.html" target="_blank">Horace He: Making Deep Learning Go Brrrr</a><span class="meta"> · Blog · 20 min</span> — roofline 的英文经典</li>
    <li><a href="https://zhuanlan.zhihu.com/p/34204282" target="_blank">知乎：Roofline Model 与深度学习性能分析</a><span class="meta"> · 知乎</span> — 中文最经典的 roofline 入门</li>
  </ul>
</div>
```

Source quality bar:

- **Strong yes (English)**: Andrej Karpathy YouTube, Lilian Weng blog, Horace He blog, Asianometry YouTube, ChipsAndCheese, HuggingFace docs, official company tech blogs (Cerebras, Nvidia, Anthropic), Hot Chips PDFs, arxiv papers
- **Strong yes (Chinese)**: 3Blue1Brown 官方中字 (B站), ZOMI酱 AI系统系列 (B站/博客园), 老石谈芯 (B站, 半导体), 影视飓风 (科普), established 知乎专栏 with depth
- **Yes with caveats**: ServeTheHome, AnandTech, Tom's Hardware, Tim Dettmers, IEEE Spectrum, Wikipedia; 中文侧 CSDN / 博客园 / 智源社区 (quality varies — pick depth)
- **Avoid**: random Medium posts, Reddit comments, content farms, dead-link-prone YouTube videos by small channels, 营销号 / 搬运党 with no original explanation

**Always prefer specific video URLs over channel URLs.** The user has to actually click and watch — a channel URL like `youtube.com/@Asianometry` makes them hunt through hundreds of videos. Always do a `WebSearch` for the exact video title before inserting, and use the resulting `watch?v=<ID>` URL. Channel root URLs are a last-resort fallback only if a search returns nothing usable.

When you're recommending a video by title but not 100% sure which specific upload is canonical, do `WebSearch` like:
```
"<channel name>" "<video title keywords>" YouTube site:youtube.com
```

Verify URLs are still live before inserting.

See `references/resource-bank.md` for curated topic → specific video URLs I've already validated.

Insertion script (Python in Bash, batch insert into assembled deck):

```python
import re
DEEPDIVES = {'s3': '<div class="deepdive">…</div>', ...}
with open('index.html') as f: html = f.read()
for sid, html_block in DEEPDIVES.items():
    pat = re.compile(rf'(<section class="slide" id="{sid}">.*?)(\s*</section>)', re.DOTALL)
    m = pat.search(html)
    if m:
        html = html[:m.start()] + m.group(1) + '\n\n    ' + html_block + m.group(2) + html[m.end():]
with open('index.html', 'w') as f: f.write(html)
```

### Step 8 — Verify + cleanup

Verify:

```bash
grep -c '<section class="slide"' index.html              # should match expected count
grep -c 'href="#s'              index.html              # TOC link count should match
grep -n 'INSERT_PART2\|TOC_INSERT' index.html           # no leftover placeholders
ls img/                                                  # all referenced images exist
md5 img/*.{png,jpeg} 2>/dev/null                        # no duplicate MD5s
# --language chinese ONLY: Chinese resources present (should be > 0); every .deepdive box mixes EN+CN
grep -c 'bilibili.com\|zhihu.com\|cnblogs.com\|csdn.net' index.html
# --language english: SKIP the line above — deepdives are English-only by design
```

Cleanup:

```bash
rm part2-A.html part2-B.html part2-C.html  # remove intermediate files
rm img/<broken-or-tiny-files>                # remove anything <1KB that's not a valid placeholder
```

### Step 9 — Install the interactive Q&A layer (ALWAYS)

Every deck ships with a built-in "select-text-to-ask" Q&A system so the user can highlight any passage, type a question, and have **you (Claude) answer it in the same conversation** — with history persisted back into the deck folder. The user should never have to think about the backend.

**Bundle (copy verbatim from `references/qa/` into `<EXPLAINER_DIR>/qa/`):**

```bash
mkdir -p "$EXPLAINER_DIR/qa"
cp .claude/skills/explainer-deck/references/qa/{qa-server.py,qa-widget.js,qa-widget.css,answer.py,watch.py,pending.py} "$EXPLAINER_DIR/qa/"
```

Then wire the widget into `index.html` (idempotent):

```python
t=open('index.html',encoding='utf-8').read()
if 'qa/qa-widget.css' not in t: t=t.replace('</head>','<link rel="stylesheet" href="qa/qa-widget.css">\n</head>',1)
if 'qa/qa-widget.js'  not in t: t=t.replace('</body>','<script src="qa/qa-widget.js"></script>\n</body>',1)
open('index.html','w',encoding='utf-8').write(t)
```

**How it works (architecture):**
- `qa-server.py` is a tiny local HTTP server that ALSO serves the deck. The page must be opened **through it** (`http://127.0.0.1:<port>/index.html`), not `file://` — a `file://` page falls back to read-only (history visible, can't ask).
- **Port is auto-derived from the deck's absolute path** (`8800 + md5(path)%200`), so every deck gets a **different, stable port and they never collide**; if taken, it probes the next free one and writes the chosen port to `qa/qa-port.txt`. The widget uses same-origin `fetch`, so it always hits whatever port served the page — no hardcoding.
- Question → `POST /ask` → appended to `qa/qa-inbox.jsonl`. Answer → you run `python3 qa/answer.py <qid>` → written to `qa/qa-answers.json` → page polls every **1s** and renders it. History persists in `qa-answers.json` (committable) + localStorage. Slides with Q&A get a cyan ◦ marker; clicking it reopens that thread's full history.
- UI: select text → yellow "问" bubble → right drawer. **Enter does NOT send** (it newlines; only the 发送 button sends — Cmd/Ctrl+Enter is a shortcut). Each thread has a 删除此条 button. Keyboard nav (space/arrows) is suppressed while typing in the drawer.

**Start it + open for the user:**
```bash
cd "$EXPLAINER_DIR" && python3 qa/qa-server.py &   # prints the URL + shutdown hint
# wait ~1s, then read qa/qa-port.txt and: open "http://127.0.0.1:$(cat qa/qa-port.txt)/index.html"
```

**Answering loop — THIS IS THE RELIABILITY-CRITICAL PART. Get it right or questions silently hang.**

The widget is NOT a live AI — answers come from YOU (Claude), and you only "see" a question when something wakes you. So you must keep a watcher armed in a LOOP, and answer ALL pending questions each time, not just the latest.

1. **Arm the watcher** (state-based, not line-baseline): `python3 qa/watch.py` with `run_in_background: true`. It blocks until there's at least one *unanswered* question and then returns the full pending list. It uses `pending.py`, which compares inbox-per-qid against answers-per-qid — so it correctly catches **follow-ups in an already-answered thread** (the classic miss) and **never re-fires on already-answered ones**.
2. When it fires, run `python3 qa/pending.py` to get the authoritative list of everything still unanswered (JSON: qid, slideId, anchorText, question, qIndex). Answer **every** item.
3. Push each reply: `python3 qa/answer.py <qid> <<'EOF' … EOF`. For a follow-up, use the SAME qid — answers append in order, and the widget shows the Nth answer against the Nth question.
4. **Immediately re-arm** the watcher (back to step 1). This loop is what makes follow-ups fast. If you ever stop looping, the next question waits until the user speaks to you again.
- Sanity check anytime with `python3 qa/pending.py` — `[]` means everything's answered.

**Shutdown is user-controlled (REQUIRED):**
- The deck shows a reminder banner at BOTH the **top and bottom**: "问答服务运行中 · 用完请告诉 Claude「关闭问答」来停止服务". (Built into `qa-widget.js` → `installBanners()`; do not remove.)
- Do NOT auto-kill anything. Leave the server + watcher running until the user explicitly says to stop (e.g. "关闭问答" / "关掉服务"). Only then: `pkill -f "qa/qa-server.py"` AND `pkill -f "qa/watch.py"`.

### Step 10 — Report

Tell the user:

- Number of slides (foundation count + walkthrough count = total)
- Number of real images embedded + which slides they're on
- The Q&A system is live: the `http://127.0.0.1:<port>/index.html` URL (Q&A only works via this URL, not `file://`)
- How to use Q&A: 选中文字 → 点"问"气泡 → 抽屉里提问；提过问的段落留 ◦ 标记可回看
- **Remind them they control shutdown**: 用完告诉你"关闭问答"，你才会停服务
- Suggestion to use keyboard arrows + ask for refinements

## Voice rules

The deck is for a beginner. **`--language chinese`**: apply ALL the rules from `.claude/skills/explainer-deck/references/anti-ai-voice.md` (no insight-frame openers, no false-dichotomy reframing, no absolutes, no performative reading reactions, no 狠/猛 dramatic descriptors, etc.). **`--language english`** (default): the Chinese-specific banlist doesn't apply, but keep the language-agnostic spirit — no hype/event-inflation ("a thing the internet waited 30 years for"), no false-dichotomy reframing ("it's not X, it's Y"), no absolutes, no performative reading reactions, name specific mechanisms instead of gesturing at depth.

Additional explainer-specific rules:

- **Always explain a term from scratch the FIRST time it appears** in a slide. The reader is opening this deck without prior context.
- **Use analogies aggressively** — every abstract concept gets a real-world parallel (microwave = 1 kW; capillary force = paper towel; CDU = HVAC fridge; warrant = "free stock that vests with conditions").
- **Do the math explicitly** when numbers are involved. Don't say "the difference is significant"; compute "21.5cm × 60°C × (15e-6 − 2.6e-6) = 160 μm = a hair's width".
- **Reference earlier slides** by ID when reusing concepts: "see slide 12 reticle limit" / "见 slide 12".
- **Write in the chosen `--language`** — Chinese deck: Chinese prose, English in `<code>` for product names + English term in parens after first Chinese mention. English deck: English prose throughout.
- **NO emoji anywhere** — use Unicode shapes (▸ ◂ ▲) and existing CSS box classes

## Design system (already in `references/deck-template.html`)

CSS classes provided:

| Class | Purpose | Visual |
|---|---|---|
| `.slide` | Each slide section | Vertical full-screen-ish block |
| `.slide-num` | "SLIDE NN" header label | Small gray uppercase |
| `<h2>` inside `.slide` | Slide title | Yellow with left bar |
| `.takeaway` | Key insight box | Yellow tinted bg + ▸ prefix |
| `.analogy` | Analogy box | Cyan tinted bg + "类比" prefix |
| `.example` | Concrete example | Green tinted bg + "例子" prefix |
| `.warning` | Caveat / important note | Orange tinted bg + "注意" prefix |
| `<pre>` | ASCII diagrams / code | Monospace dark bg with yellow border |
| `<table>` | Comparisons | Borderless dark with yellow th |
| `<code>` | Inline tech terms | Yellow on dark bg |
| `.figure` | Single image with caption | Centered with caption below |
| `.figure-row` | Side-by-side images | Flex row, captions below each |
| `.deepdive` | "想深入这个概念" — external YouTube / blog links | Purple-tinted box with ▼ marker, link list |

Color scheme:

- Background: `#0f0f10` (deep dark)
- Text: `#e4e4e6` (off-white)
- Accent: `#f4d03f` (yellow) — for titles, takeaways, code, divider bars
- Secondary accents: `#8be3ff` (cyan, analogy), `#96dc96` (green, example), `#ff8c5a` (orange, warning)

JS provides: keyboard navigation, scroll-spy active TOC item, slide counter in bottom right.

## File templates

- `references/deck-template.html` — full HTML shell with all CSS/JS and placeholders for foundation + part2 slides + TOC
- `references/slide-patterns.md` — example slides showing each CSS class in use, copy-paste building blocks
- `references/workflow.md` — exact agent prompt template + parallelization strategy

## Common pitfalls

1. **Agents repeat themselves explaining foundation concepts.** Fix: in each agent prompt, include "Foundation slide map" with what's already explained.
2. **Duplicate images via CDN URLs.** Substack `substackcdn.com/image/fetch/$...` URLs sometimes return wrong content. Always check MD5 after downloading multiple images. Prefer direct `substack-post-media.s3.amazonaws.com/public/images/<UUID>_WxH.<ext>` URLs.
3. **Slide ID conflicts.** Each agent gets a disjoint ID range (s16–s30, s31–s46, s47–s62). Check the final assembled file has no duplicate IDs.
4. **Bash $ interpolation in URLs.** Always use single quotes around URLs containing `$` (e.g. `curl 'https://substackcdn.com/image/fetch/$s_!...'`). Double quotes will eat the `$` and produce 9-byte error responses.
5. **AI-flavored Chinese.** Run the grep self-check from `.claude/skills/explainer-deck/references/anti-ai-voice.md` against `index.html` before reporting done. Zero hits is the bar.

## Reference: what good output looks like

A finished deck is a single `index.html` with:

- ~60 slides (≈15 foundation + ≈45 walkthrough), sticky TOC, dark theme + yellow accent, keyboard nav.
- **8–12 figures** mixing real photos, hand-authored SVG schematics, and (optionally) AI-generated diagrams — every hard/abstract concept gets one (see Step 5.5).
- Per-slide `.takeaway` boxes, `.analogy` / `.example` / `.warning` callouts, ASCII diagrams for precise/numeric figures, comparison tables.
- Bilingual `.deepdive` resource boxes (Chinese decks) or English-only (English decks).
- A built-in select-text-to-ask Q&A layer served by `qa/qa-server.py`.

Build one against any dense article and use it as your own reference going forward.
