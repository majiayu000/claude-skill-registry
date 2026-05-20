---
name: draft-marketing
description: Create channel-specific marketing asset drafts with clear positioning, CTA, and measurable campaign intent.
---

# Draft Marketing Asset

Create practical marketing artifacts that are usable in execution, with explicit positioning and measurement intent.

## When to Use

Use this skill when a plan task outputs campaign-ready content (email campaign copy, ad copy, landing copy, promo announcement, etc.).

## Operating Mode

**MARKETING ARTIFACT AUTHORING**

**Allowed:** craft copy variants, define CTA, map message to audience and channel constraints.

**Not allowed:** fabricate proof points, ignore channel limits, produce generic copy without positioning, or ignore the active message ledger when one already exists.

## Inputs

- Mode (`--mode brief|final`, default: `final`)
- Channel (`email`, `ads`, `landing`, `landing-page-copy`, `social`, etc.)
- Audience segment
- Offer/value proposition
- Evidence/proof points available
- CTA and conversion event
- Tone/brand constraints
- Existing message-testing context from `docs/business-os/strategy/<BIZ>/message-variants.user.md`, when the business already has a CAP-02 ledger

### Mode Behavior

**brief** - Produces a creative brief (strategy + messaging hierarchy + key visuals + CTA variants) before final assets are drafted. Output: `docs/marketing/<slug>-creative-brief.md`

**final** (default) - Produces campaign-ready copy with variants. Output: `docs/marketing/<slug>-asset-pack.md`

## Output

### Brief Mode

Create/update:

`docs/marketing/<slug>-creative-brief.md`

Required sections:

```markdown
# <Campaign Name> - Creative Brief

## Objective
- What this campaign must achieve
- Success metric

## Target Audience
- Primary segment
- Pain points/motivations
- Language/tone expectations

## Core Message
- Positioning statement
- Key benefit hierarchy (1-3 bullets)
- Proof points available

## Visual Direction
- Mood/style references
- Key visual concepts
- Brand constraints

## CTA Strategy
- Primary CTA
- Secondary CTA (if applicable)
- Conversion path

## Channel Considerations
- Format constraints
- Platform-specific requirements
- Distribution plan

## Next Steps
- [ ] Stakeholder approval
- [ ] Final asset drafting
- [ ] Asset testing plan
```

### Final Mode (Default)

Create/update:

`docs/marketing/<slug>-asset-pack.md`

Required sections:

```markdown
# <Campaign/Asset Name>

## Strategy Snapshot
- Channel:
- Audience:
- Hypothesis:
- Positioning:
- CTA:
- Source tag(s):

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

### Brief Mode

1. Lock objective, audience, and channel.
2. Define core message and positioning.
3. Map visual direction and CTA strategy.
4. Document channel considerations.
5. Save brief with clear next steps.

### Final Mode

1. Lock channel + audience + objective.
2. If a CAP-02 ledger already exists, choose the hypothesis/frame the asset belongs to before drafting fresh copy.
3. Draft primary asset with one clear CTA.
4. Add one to two variants only when strategically justified, and keep them traceable back to the selected hypothesis.
5. Attach measurement plan, source tags, and QA checklist.
6. Save artifact and list recommended next action.

## Completion Message

**Brief mode:**
> "Creative brief ready: `docs/marketing/<slug>-creative-brief.md` with strategy, messaging hierarchy, visual direction, and CTA variants."

**Final mode:**
> "Marketing asset pack ready: `docs/marketing/<slug>-asset-pack.md` with primary draft, variants, and measurement plan."
