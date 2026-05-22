---
name: ecom-copywriter-lab
description: "Produce ecom ad copy packs: branded/trust + hard sell, plus chapter-length primary text tests and Meta-friendly text-variation sets. Use when generating ad copy from an angle matrix."
---

# Ecom Copywriter Lab (Branded + Hard Sell + Long Text)

This skill generates copy packs aligned to Meta’s “text variations” approach: multiple primary texts + headlines per creative/angle.

## Required inputs

- `foundation/*` (research, avatar, beliefs, angles)
- `ads/ads.csv` with `angle_id` and angle summaries

## Required outputs (create these files)

In `outputs/ecom/<brand_slug>/<run_id>/ads/`:
- `copy_pack.md` (organized per angle)
- `copy_variations.csv` (angle_id, variant_id, primary_text, headline, description)

## Copy modes to generate (per angle)

### 1) Branded / trust (credibility first)
- Education + empathy + specificity
- Softer CTA (“learn more”, “see how it works”)
- Proof via believable details, not hype

### 2) Hard sell (direct response)
- Strong hook → payoff → proof → CTA
- Objection handling (shipping, price, “does this actually work?”)
- Concrete offers (bundles, guarantees, deadline only if real)

### 3) “Chapter-length” primary text tests
- 700–2,000+ words
- Structure: story → problem agitation → new mechanism → proof → offer → link
- Goal: let delivery find “readers” and send higher intent traffic

## Variant generation rules

For each angle:
- 8–12 primary texts (mix short/medium/long)
- 6–10 headlines (benefit + mechanism + proof)
- 0–5 descriptions (optional)

Keep variants “same idea, different expression” (don’t mix angles in one ad).

## Guardrails

- No sensitive personal attribute claims.
- No unverifiable claims (results, timelines, medical/financial).
- Don’t imply “you have X condition”; frame as “if you struggle with…”.

