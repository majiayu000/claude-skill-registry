---
name: funnel-strategy
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Maps your company's GTM motion (PLG, SLG, or Hybrid) to concrete funnel stages with inputs, outputs, and qualification criteria per stage. Detects motion type from website + Exa research, then produces pre-close + post-close stage definitions, the FETE mapping (Fit / Engagement / Tier / Eligibility), and closed-lost re-entry paths. Triggers - "funnel strategy", "funnel stages", "pipeline stages", "sales process", "lead qualification", "GTM motion mapping", or any work defining how leads flow through the business. Upstream - recommended company-context, icp-research. Downstream - feeds lifecycle-marketing, outreach-emails, content-strategy. NOT for lead scoring logic (use /lead-scoring) or lifecycle email campaigns (use /lifecycle-marketing).
goal: Map a company's GTM motion to concrete funnel stages with qualification criteria per stage.
outcome: A funnel-strategy.md file in `marketing/funnel/` that downstream skills (lifecycle, outbound, content) consume to align their work to the same funnel definition.
primitive: research
ontology_type: funnel-strategy
review_gate: 2
inputs:
  required: []
  recommended:
    - icp-research
    - positioning
outputs:
  - type: funnel-strategy
    feeds_into:
      - lifecycle-marketing
      - outreach-emails
      - content-strategy
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /funnel-strategy
status: draft
---

# funnel-strategy — research skill

Infer and structure your sales funnel based on your GTM motion. Reads ICP + positioning (if locked) and your website signals to produce pre-close + post-close stages with qualification criteria per stage. Output: `marketing/funnel/funnel-strategy.md`.

## When to use

- Early in the engagement, after ICP research is in place — defines the stages every downstream skill assumes
- When the GTM motion is shifting (e.g., PLG → Hybrid as enterprise deals start landing)
- Quarterly refresh if win/loss data suggests stages are misaligned with reality

## When NOT to use

- For lead scoring logic per account — use `/lead-scoring` after this is locked
- For lifecycle email campaign design — use `/lifecycle-marketing` after this is locked
- If you already have a documented funnel that the team trusts — skip this; it's already done

## Inputs

- **Recommended:** `marketing/icp/ICP.md` (the champion + economic buyer help identify stage transitions)
- **Recommended:** `marketing/positioning/positioning.md` (status-quo alternatives often map to closed-lost re-entry signals)
- Your company website URL (Exa fetches + reads it)

## What it produces

`marketing/funnel/funnel-strategy.md` with these sections:

- **GTM motion classification** — PLG / SLG / Hybrid, with evidence from website + ICP signals
- **Pre-close stages** — typically 4–6 stages (Aware → Engaged → Qualified → Discovery → Evaluation → Closed-Won)
- **Post-close stages** — Onboarding → Activated → Habitual → Expansion (or Churn-Risk → Recovered)
- **Per-stage definitions** — what triggers entry, what defines progression, what qualification criteria gate the next stage
- **FETE mapping** — Fit / Engagement / Tier / Eligibility signals per stage
- **Closed-lost re-entry paths** — how leads that dropped out get back in

## Example run

In your terminal: `/funnel-strategy`

Claude reads your ICP + positioning files + fetches your website, then walks you through the GTM motion classification. Edits the draft with you, then writes the final to `marketing/funnel/funnel-strategy.md`.

**For the format:** see [`../../../pulse-analytics-example/funnel/funnel-strategy.md`](../../../pulse-analytics-example/funnel/funnel-strategy.md) — fully populated example for the fictional PulseAnalytics B2B SaaS analytics company.
