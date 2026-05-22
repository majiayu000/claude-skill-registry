---
name: ecom-learning-loop
description: "Persist creatives + prompts + angles + performance tags so you can generate new variants from data (e.g., “make 20 new variants of our best angle”)."
---

# Ecom Learning Loop (Creative Memory → Next Tests)

Goal: turn ad testing into a compounding system:
1) store what you made (angle, prompt, format, creator)
2) store what happened (spend, CTR, CPA, purchases)
3) generate the next tests from data, not vibes

## Required output (create this file)

Maintain a registry file (recommended):
- `outputs/meta-creative-registry.json`

Each item should store:
- `id`, `type` (image/video/copy), `source_path` or URL
- `tags`: `brand:*`, `product:*`, `angle:*`, `format:*`, `hook:*`, `stage:*`
- `performance`: spend, impressions, ctr, cpa/cpp, roas, purchases, notes

## Minimal tagging taxonomy

- `brand:<slug>`
- `product:<slug>`
- `angle:<angle_id>`
- `format:<ugclook|product|proof|comparison|howto|video>`
- `hook:<hook_type>`
- `stage:<unaware|problem|solution|product|most>`

## Winner → 20 variants workflow

1) Pick the best creative for an angle (by CPA/ROAS) and document why it worked.
2) Generate a “subtle change” prompt pack: 10–30 variants preserving the core mechanism.
3) Launch and tag the variants with the same `angle:<angle_id>` so you can attribute learnings.

## Operating rhythm

- Daily: log every launched creative + copy variant
- Daily: write back results (wins and losses)
- Weekly: export top angles + mechanisms and plan a new creative sprint

