---
name: ecom-meta-testing-os
description: "Ecom-specific Meta testing operating system: naming conventions, creative matrix presets, pausing/scaling guardrails, and daily reporting."
---

# Ecom Meta Testing OS (Launch → Learn → Iterate)

This skill standardizes how you run Meta tests so learnings compound.

## Inputs

- `ads/ads.csv` (angle IDs, copy, creative prompts)
- Baseline business truth: AOV, margin, shipping, inventory, target CPA/CAC

## Naming conventions (do this or you can’t learn fast)

- Campaign: `ECOM-{brand}-{product}-{YYYYMMDD}-{test_id}`
- Ad set: `AUD-{audience_name}`
- Ad: `ANG-{angle_id}__IMG-{img_id}__COPY-{copy_id}`

## UTM minimums

- `utm_source=meta`
- `utm_medium=paid_social`
- `utm_campaign=<campaign_name>`
- `utm_content=angle:{angle_id}|img:{img_id}|copy:{copy_id}`

## Default test presets

### Creative matrix (starter)
- 6–12 angles × 2–3 image variants × 3–5 primary text variants
- Broad audiences first; add 1–2 “intent proxy” audiences if needed

### Spend-gated guardrails (starter)
- Don’t kill too early: require a spend threshold before pausing.
- Scale only after stable conversions and clean tracking.

## Daily operator checklist

1) Verify tracking (Pixel/CAPI events) before “creative changes”
2) Identify winners by CPA/ROAS + volume
3) Generate 10–30 variants for the best angle(s)
4) Pause clear losers after spend threshold
5) Log learnings into your creative registry (angle → prompt → KPI)

## Measurement note (Pixel/CAPI)

If results are noisy, fix signal first:
- Event deduplication
- Purchase value accuracy
- Matching quality (CAPI / enhanced conversions)

