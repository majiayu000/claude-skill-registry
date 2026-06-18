---
name: icp-research
version: '1.0'
last_updated: 2026-05-19
author: genesys-growth
description: Build structured ICP documentation by scraping case studies, testimonials, and solutions pages from your website. Produces firmographics, champion + economic buyer personas, pain points, decision criteria, anti-ICP, customer proof points, and voice-of-customer synthesis. Writes to marketing/icp/ICP.md as the canonical ICP every downstream skill reads. Triggers - "icp research", "ideal customer profile", "persona research", "customer segments", "who are our customers", "build ICP"
goal: Build a structured ICP from website signals + win-loss data so every downstream skill works from the same definition of the customer.
outcome: marketing/icp/ICP.md with firmographics, champion + economic buyer personas, pain points, anti-ICP, voice-of-customer.
primitive: research
ontology_type: icp-profile
review_gate: 2
inputs:
  required: []
  recommended:
    - competitor-research
outputs:
  - type: icp-profile
    feeds_into:
      - positioning
      - product-messaging
      - funnel-strategy
      - content-strategy
owned_by_agent: researcher
mcps_used:
  - exa
triggers:
  slash_commands:
    - /icp-research
status: draft
---

# icp-research — Stage 1 + 2 research skill

The article's Example 1 Day 5 skill. Reads your website + win-loss patterns (if available) + competitor outputs (if locked) and writes a structured ICP to `marketing/icp/ICP.md`. This file is canonical from creation — every downstream skill reads it.

---

## When to use

- Day 5 of Example 1: after competitor research + win-loss data exist, build the ICP synthesis
- Quarterly refresh of ICP (markets shift)
- New segment exploration ("we're adding a healthcare vertical — re-run ICP for that segment")
- After major win-loss shift (5+ recent losses in a segment → re-run ICP)

## When NOT to use

- For behavioural simulation of an ICP buyer (use `/icp-behavioural` — not in V2 quickstart)
- For interview prep against a single account (use `/customer-interviews` — not in V2 quickstart)
- For competitor research (use `/competitor-research`)
- For positioning strategy (use `/positioning` after ICP locks)

## How it works

1. Inputs: your website URL (required). Optional: list of representative customer URLs, win-loss patterns from prior cycle, competitor aggregate.
2. Reads (Exa MCP for fresh data): website case studies, customer pages, testimonials, blog posts, About / Solutions pages.
3. Optionally reads: `marketing/competitors/aggregate.md` (if locked) to inform "anti-ICP" framing; recent win-loss data from `marketing/win-loss/win-loss.md` (if `/win-loss-analysis` has run).
4. Produces a structured ICP with these sections (matches the PulseAnalytics example at `marketing/icp/ICP.md`):
   - **Firmographics** — company type, revenue stage, team size, funding, geography, industry
   - **Champion persona** — title, tenure, reporting, owns, their week, JTBD, job-context triggers, pain points (priority order), decision criteria
   - **Economic buyer persona** — title, motivation, decision criteria
   - **Anti-ICP** — who NOT to sell to + why
   - **Where they hang out** — acquisition channels with rationale
   - **Customer proof points** — populate as real customers ship (start empty with `[UNAVAILABLE]` notation)
   - **Voice of customer** — verbatim quotes by theme (populate from `/win-loss-analysis` over time)
5. Every claim tagged with confidence per `.claude/rules/ontology.md`. Invented metrics forbidden — use `[UNAVAILABLE]` instead.
6. Writes to `marketing/icp/ICP.md` (overwrites prior canonical; git history preserves prior versions).

## Invoke

```
/icp-research https://yourdomain.com
```

Or with optional inputs:
```
/icp-research https://yourdomain.com + read these 3 case studies: [URLs]
```

## Example output

See [`marketing/icp/ICP.md`](../../../marketing/icp/ICP.md) for the PulseAnalytics example seed. Notice the structure repeats per persona (champion + economic buyer); pain points are priority-ordered; anti-ICP is explicit; VoC + proof points start `[UNAVAILABLE]` and fill as data lands.

## Dependencies

- **Reads from:** your website URL (required); `marketing/competitors/aggregate.md` (optional, recommended); `marketing/win-loss/win-loss.md` (optional, recommended — produced by `/win-loss-analysis`)
- **Reads via Exa MCP (optional):** website + recent customer-facing pages
- **Writes to:** `marketing/icp/ICP.md` (canonical, every downstream skill reads here)

## Customization

Add a custom segment (e.g., "Enterprise tier") by extending the firmographics section with a segment-table — different revenue/team-size cuts get different champion personas. The Genesys-internal version supports segment-by-segment ICPs; the quickstart simplifies to one ICP and one champion.

Edit pain-point priority order based on real customer conversations as they happen. Pain priority drives messaging hierarchy downstream.

## Where this fits in the Example 1 chain

```
Day 1-3: /competitor-research × N → per-competitor files
Day 3:   /competitor-aggregate → competitor canonical
Day 4:   /win-loss-analysis → win-loss canonical (marketing/win-loss/win-loss.md)
Day 5:   /icp-research (THIS SKILL) → canonical ICP
Week 2:  /positioning reads ICP.md + competitor aggregate
```

## Refresh cadence

Quarterly. Trigger sooner on major win-loss shift, new segment entry, or major change in champion-persona vocabulary.
