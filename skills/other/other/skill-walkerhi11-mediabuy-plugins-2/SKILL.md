---
name: ecom-ai-image-ads
description: "Generate a daily ecom image-ad plan + prompt packs from foundation docs and competitor ad examples; includes a winner→variants loop and creative registry tagging."
---

# Ecom AI Image Ads (Plan → Prompts → Variants)

This skill produces a **daily creative plan** and prompt packs you can run in your image tool of choice (Gemini/MJ/SDXL), built from your angle matrix.

## Required inputs

- Workspace with foundation docs + `ads/ads.csv` (from `ecom-foundation-docs`)
- Competitor ad examples (URLs, screenshots, or notes on what’s working)

## Required outputs (create these files)

In `outputs/ecom/<brand_slug>/<run_id>/creative/`:
- `plan.yaml` (what to make; format/aspect/angle mapping)
- `prompts.md` (copy/paste prompt pack with variants)
- `winner_variations.md` (prompt pack for “20 variants of winner”)

## Daily creative plan rules (DTC)

For each angle, generate a balanced set:
- **UGC look** (authentic, imperfect, believable)
- **Product hero** (clean, DTC aesthetic, benefits visible)
- **Proof-first** (reviews, demo frames, ingredient/mechanism visual)
- **Comparison/how-to** (simple “why it works” visuals; avoid policy landmines)

Aspect ratios to cover:
- 1:1, 4:5, 9:16

## Prompt structure (recommended)

Each prompt should include:
- subject + setting (UGC/home, bathroom, gym, kitchen, etc.)
- mechanism/proof (what’s visually different)
- shot type (selfie, handheld, product close-up, before/after only if true/allowed)
- lighting + lens (phone look vs studio)
- negative constraints (no text overlay, no logos, no medical claims)

## Winner → variants loop

When you identify a winner, generate 10–30 variants that preserve the “why it worked”:
- change background, wardrobe, framing, angle, props
- keep mechanism + core visual cue consistent
- keep “UGC authenticity” (avoid over-polish)

Output these as `winner_variations.md` with explicit instructions for subtle vs moderate changes.

## Registry tagging (for learning loop)

Tag each creative with:
- `brand:<slug>`
- `product:<slug>`
- `angle:<angle_id>`
- `format:<ugclook|product|proof|comparison|howto>`
- `aspect:<1:1|4:5|9:16>`

Use `ecom-learning-loop` to store prompt → performance so you can generate variants from data.

