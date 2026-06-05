# Example: Consistent Hashing

A complete deck produced by the **explainer-deck** skill, end to end.

- [`article.txt`](article.txt) — the input: an original, copyright-free (CC0) dense article on consistent hashing, written deliberately in a terse systems-paper voice so the deck has something hard to unpack.
- [`explainer/index.html`](explainer/index.html) — the output deck: 22 slides (7 foundation + 15 walkthrough), 3 hand-authored SVG figures (hash ring, add-node monotonicity, modulo remap), per-slide takeaways, analogies/examples, tables, ASCII diagrams, English-only deepdive links, and the built-in Q&A layer.

This deck was built with the English defaults (`--language english`) and `--image` left off, so its figures are hand-authored SVGs (the accurate choice for structural diagrams) rather than AI-generated images.

## Run it

```bash
cd explainer
python3 qa/qa-server.py
# open the printed http://127.0.0.1:<port>/index.html
```

Opening `index.html` directly via `file://` works too, but the select-text-to-ask Q&A only functions when served through `qa-server.py`.

## Preview

See [`../../media/`](../../media/) for a hero screenshot, an animated GIF, and an MP4 walk-through of this deck.
