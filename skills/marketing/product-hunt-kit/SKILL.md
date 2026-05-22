---
name: product-hunt-kit
description: |
  Complete Product Hunt launch preparation. Generates tagline, description,
  maker comment, gallery checklist, topics, hunter outreach, launch timeline.
  Use when: preparing PH launch, writing PH copy, creating launch checklist.
  Zero external deps - pure content generation. Keywords: product hunt, launch,
  tagline, maker comment, PH, producthunt.
argument-hint: "[product name]"
---

# /product-hunt-kit

Product Hunt launch kit. Copy, checklist, timeline. One pass.

## What This Generates

- Tagline (<=60 chars) with 3 variants
- Description (<=260 chars) with 3 variants
- First comment / maker intro
- Gallery image specs + asset checklist
- Topic recommendations
- Hunter outreach email template
- Hour-by-hour launch timeline
- Social amplification posts

## Usage

```bash
/product-hunt-kit heartbeat
/product-hunt-kit caesar for hunter@example.com
```

## Process

1. Read `brand-profile.yaml` (suggest `/brand-builder` if missing)
2. Analyze product: README, landing, core features, differentiators
3. Research similar successful launches (voice, topics, gallery patterns)
4. Generate all copy with variants, tuned to PH norms and constraints
5. Create asset checklist with exact specs and submission guardrails

## Output

Produces `product-hunt-kit.md` with copy, checklist, timeline, social posts.

## Integration

Reads `brand-profile.yaml` via `/brand-builder`.
