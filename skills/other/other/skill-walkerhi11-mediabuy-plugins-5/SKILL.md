---
name: ecom-foundation-docs
description: "Automate Research → Avatar → Offer Brief → Necessary Beliefs → Angle Matrix → ads.csv for DTC ecom creative. Use when starting a new product or when you need structured inputs for creative/copy/testing."
---

# Ecom Foundation Docs (Research → Angles → Production Sheet)

This skill turns raw product info + competitor context into **structured artifacts** you can feed into:
- image ad prompt generation (UGC look + product-focused + proof-focused)
- copy packs (branded/trust + hard sell + long-form “chapter text”)
- Meta testing workflows (creative matrix, spend-gated guardrails, learning loop)

## Required outputs (create these files)

Create a workspace folder (recommended): `outputs/ecom/<brand_slug>/<run_id>/` containing:
- `foundation/research.md`
- `foundation/avatar.md`
- `foundation/offer_brief.md`
- `foundation/beliefs.md` (3–6 “I believe…” statements)
- `foundation/angles.md`
- `ads/ads.csv` (angle → copy → image prompt build sheet)

## Inputs to request (minimum viable)

- Brand + product name, price, AOV target
- Offer URL (PDP) + any advertorial/VSL URLs
- Margin + COGS + fulfillment constraints (inventory, ship times)
- Competitor list + 3–10 competitor URLs
- Existing creative winners (if any): images + copy + KPIs

## Workflow (how to fill the docs)

Use voice-of-customer and competitor patterns instead of guessing:

1) **Research** (`foundation/research.md`)
   - Pull customer language, objections, alternatives, and proof sources.
   - If you don’t have VOC, write a “VOC needed” section instead of inventing quotes.

2) **Avatar** (`foundation/avatar.md`)
   - Who buys, why now, what they tried, what they fear, what they want.
   - Capture “phrases they actually use” (from reviews/comments/messages).

3) **Offer Brief** (`foundation/offer_brief.md`)
   - Awareness + sophistication level
   - Big idea + mechanism + proof points
   - Objections + belief chain + funnel notes

4) **Necessary Beliefs** (`foundation/beliefs.md`)
   - 3–6 max; each starts with `I believe…`
   - Add 1–3 bullets of evidence/logic for each belief

5) **Angle Matrix** (`foundation/angles.md`)
   - For each belief: generate multiple angles across:
     - branded/trust (education, empathy, credibility)
     - hard sell (direct response, urgency, payoff)
     - proof-first (UGC/reviews, demo, before/after only if truthful/allowed)
   - Each angle should specify: hook, mechanism/proof, CTA, and competing alternative.

6) **Production Sheet** (`ads/ads.csv`)
   - Convert angles into testable rows with IDs for:
     - `angle_id`, `angle_name`, `hook`, `mechanism`, `proof`, `cta`
     - `primary_text` variants and `headline` variants (or pointers to copy packs)
     - `image_concept` + `image_prompt_base`

## Subagent pattern (recommended)

Assign in parallel:
- **Researcher** → `foundation/research.md`
- **Angle strategist** → `foundation/beliefs.md` + `foundation/angles.md`
- **Copywriter** → populate copy columns for each angle + long-text variants
- **Creative director** → populate image concepts + prompt bases

## Guardrails

- Don’t fabricate proof or quotes; cite sources or mark as hypothesis.
- Avoid sensitive personal attribute inference (“you have X condition”).
- Keep belief count tight (≤6) and angles diverse (don’t spam the same hook).

