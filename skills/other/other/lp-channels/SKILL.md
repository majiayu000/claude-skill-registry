---
name: lp-channels
description: Startup channel strategy + GTM skill (SELL-01). Analyzes channel-customer fit, selects 2-3 launch channels with rationale, and produces a 30-day GTM timeline. Consumes lp-offer output (ICP, positioning, objections) and feeds channel selection to draft-marketing and lp-seo.
---

# lp-channels — Startup Channel Strategy + GTM (SELL-01)

Produces a channel selection strategy and 30-day go-to-market (GTM) timeline for startups. Analyzes channel-customer fit, cost constraints, and cadence requirements to select 2-3 launch channels. Includes GTM execution plan with sequenced actions and resource allocation.

## Invocation

```
/lp-channels --business <BIZ>
```

Required: `--business <BIZ>` — business identifier (e.g., BRIK, SEG, INT)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

RESEARCH + ANALYSIS + STRATEGY + DOCUMENT

This skill researches channel landscape, analyzes channel-customer fit using lp-offer ICP/positioning, selects 2-3 launch channels, designs a 30-day GTM timeline, and documents the artifact. Does NOT execute campaigns or select channels without ICP validation.

## Inputs

Required:
- `lp-offer` output: ICP, positioning, objections from `docs/business-os/startup-baselines/<BIZ>/offer.md`
- `lp-readiness` output: distribution feasibility from RG-02 gate
- Business context from `docs/business-os/strategy/<BIZ>/`

**Demand Evidence Pack (DEP) — strategy eligibility gate (GATE-SELL-STRAT-01):**

Before SELL-01 starts, a valid DEP record must pass the floor defined in `docs/business-os/startup-loop/schemas/demand-evidence-pack-schema.md`. Full gate logic is in startup-loop advance gate docs. Summary:
- DEP passes → SELL-01 strategy design is eligible.
- DEP missing or fails → SELL-01 is blocked.

**Paid spend activation gate (GATE-SELL-ACT-01):**

Paid spend authorization is evaluated separately at SELL-08 after strategy output exists. This skill can produce a complete strategy artifact even when spend activation is still blocked.

SELL-08 now requires both:
- decision-grade measurement signal verification, and
- a recent rendered sales-funnel audit pass from `/lp-sell-funnel-audit --business <BIZ>` with no unresolved High/Critical blockers on the mobile + fullscreen core booking path.

Optional (enhances quality):
- Competitor channel analysis, budget/resource constraints, existing audiences, market research
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` — channel voice and tone alignment
- `docs/business-os/strategy/<BIZ>/messaging-hierarchy.user.md` — channel-specific messaging
- Existing GTM standing artifacts, when present:
  - `docs/business-os/strategy/<BIZ>/stockist-target-list.user.md` — pre-live retail/distribution targets and coverage gaps
  - `docs/business-os/strategy/<BIZ>/channel-health-log.user.md` — live channel actuals and partner performance
  - `docs/business-os/strategy/<BIZ>/weekly-demand-plan.user.md` — current GTM-1 operating sprint
  - `docs/business-os/strategy/<BIZ>/channel-policy.user.md` — channel governance, terms, and conflict rules
  - `docs/business-os/strategy/<BIZ>/message-variants.user.md` — canonical CAP-02 message-testing ledger; schema defined in `docs/business-os/startup-loop/schemas/message-variants-schema.md`

## Workflow

### Stages 1–2: Channel Research and Fit Analysis

Load `modules/channel-research.md`:
- Stage 1: Load Context — ICP, readiness, competitor channels, channel taxonomy
- Stage 2: Channel-Customer Fit Analysis — score ≥8 channels on 3 dimensions

### Stages 3–4: Strategy and Cost Analysis

Load `modules/channel-strategy.md`:
- Stage 3: Select 2-3 Launch Channels — rationale, stop conditions, success metrics
- Stage 4: Cost/Constraint Analysis — budget, resource, and risk tables

### Stages 5–6 + QC + Red Flags: GTM Output and Documentation

Load `modules/channel-gtm-output.md`:
- Stage 5: 30-Day GTM Timeline
- Stage 6: Document primary artifact and any required companion GTM artifacts
- Self-audit QC-01–QC-10 and Red Flags

## Output Contract

Produces required primary file: `docs/business-os/startup-baselines/<BIZ>/channels.md`

**Artifact registry**: Canonical path defined in `docs/business-os/startup-loop/artifact-registry.md` (artifact ID: `channels`).

**Structure**: metadata frontmatter; executive summary; channel landscape audit; selected channels; cost/constraint analysis; 30-day GTM timeline; month 2+ roadmap; evidence register.

**Conditional companion artifacts**:
- If selected channels include boutiques, retailers, distributors, wholesale accounts, hotel shops, or other physical-product distribution lanes, initialize or refresh `docs/business-os/strategy/<BIZ>/stockist-target-list.user.md`.
- If live physical placements or partner accounts already exist, read actuals from `docs/business-os/strategy/<BIZ>/channel-health-log.user.md` and do not restate those numbers as unsupported assumptions.
- If the strategy introduces real partner-term, allocation, or channel-conflict rules, initialize or refresh `docs/business-os/strategy/<BIZ>/channel-policy.user.md`.
- If the strategy is execution-ready for the next 7 days, initialize or refresh `docs/business-os/strategy/<BIZ>/weekly-demand-plan.user.md` with the first operating sprint.
- If the strategy depends on testing multiple frames, copy angles, or retailer pitches, initialize or refresh `docs/business-os/strategy/<BIZ>/message-variants.user.md` so CAP-02 starts as a standing ledger rather than chat-only context.

**Downstream compatibility**:
- `draft-marketing`: selected channels, positioning, success metrics
- `lp-seo`: organic channel context, keyword intent from ICP
- `lp-do-fact-find`: channel strategy to scope go-items
- `startup-loop`: SELL-01 strategy output for S4 join + SELL-08 activation gate for paid spend; companion GTM artifacts preserve GTM-1/GTM-2/OFF-4 continuity

## Integration

### Upstream (MARKET-06 + readiness context)
- `/lp-offer --business <BIZ>` (MARKET-06) — MUST consume ICP, positioning, and objections
- `/lp-readiness --business <BIZ>` (readiness context) — SHOULD pass RG-02 distribution feasibility gate
- May consume market research from `docs/business-os/market-research/`

### Downstream (DO)
- `/draft-marketing` — channel selection for asset targeting
- `/lp-seo` — organic channel context and ICP keyword intent
- `/lp-do-fact-find` — scopes go-items from GTM timeline
- `startup-loop` — SELL-01 validation before S4; SELL-08 activation gate before paid spend

### Parallel Skills
- Can run in parallel with `/lp-forecast` (S3) after MARKET-06 if both consume the same lp-offer input
- Does NOT depend on `/lp-measure` (Measure stage), but measurement feeds into success metrics tracking
