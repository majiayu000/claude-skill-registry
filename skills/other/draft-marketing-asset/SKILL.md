---
name: draft-marketing-asset
description: Create channel-specific marketing asset drafts with clear positioning, CTA, and measurable campaign intent.
---

# Draft Marketing Asset

Create practical marketing artifacts that are usable in execution, with explicit positioning and measurement intent.

## When to Use

Use this skill when a plan task outputs campaign-ready content (email campaign copy, ad copy, landing copy, promo announcement, etc.).

## Operating Mode

**MARKETING ARTIFACT AUTHORING**

**Allowed:** craft copy variants, define CTA, map message to audience and channel constraints.

**Not allowed:** fabricate proof points, ignore channel limits, produce generic copy without positioning.

## Inputs

- Channel (`email`, `ads`, `landing`, `social`, etc.)
- Audience segment
- Offer/value proposition
- Evidence/proof points available
- CTA and conversion event
- Tone/brand constraints

## Output

Create/update:

`docs/marketing/<slug>-asset-pack.md`

Required sections:

```markdown
# <Campaign/Asset Name>

## Strategy Snapshot
- Channel:
- Audience:
- Positioning:
- CTA:

## Primary Asset Draft
...

## Variant(s)
...

## Measurement Plan
- Primary metric:
- Secondary metric:
- Decision threshold:

## QA Checklist
- [ ] Positioning is explicit
- [ ] CTA is singular and clear
- [ ] Claims are evidence-backed
- [ ] Channel constraints satisfied
```

## Workflow

1. Lock channel + audience + objective.
2. Draft primary asset with one clear CTA.
3. Add one to two variants only when strategically justified.
4. Attach measurement plan and QA checklist.
5. Save artifact and list recommended next action.

## Completion Message

> "Marketing asset pack ready: `docs/marketing/<slug>-asset-pack.md` with primary draft, variants, and measurement plan."
