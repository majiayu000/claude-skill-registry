---
name: planning-gtm-launch
description: Use when preparing to launch a product or major feature - creates market analysis, positioning, launch plan, and enablement strategy.
---

# Planning GTM Launch

## Overview

Creates a comprehensive go-to-market (GTM) plan covering market context, positioning, launch phases, enablement, and success criteria. Ensures products land, not just launch.

## When to Use

- Approved charter ready for launch planning
- New product or major feature shipping
- Entering a new market segment
- Repositioning existing product
- Pre-sales kickoff planning

## Core Pattern

**Step 1: Understand the Launch**

Ask user:
- "What product/feature are we launching?"
- "What charter or PRD does this map to?"
- "Who is the target customer/segment?"
- "When is target launch date?"

Read related charter/PRD if exists.

**Step 2: Market Context**

Analyze:
- **TAM/SAM/SOM:** Total/Serviceable/Obtainable Addressable Market
  - If data unavailable, state "Unknown - need market research"
  - If available, cite source (e.g., analyst report, internal data)

- **Competitive landscape:**
  - Who are direct competitors?
  - How do we differentiate?
  - What's our unique advantage?

- **Customer segments/ICP:**
  - Who is the ideal customer?
  - What pain points do they have?
  - Why will they buy?

**Step 3: Positioning & Messaging**

Define:
- **Value proposition:** Core value in 1 sentence
- **Differentiation:** Why us vs competition (3 key differentiators)
- **Messaging framework:** Key messages per audience
  - For customers: [Message]
  - For sales: [Message]
  - For partners: [Message]
  - For press/analysts: [Message]

**Step 4: Launch Plan**

Create phased plan:

**Pre-launch (before launch date):**
- Activities: Beta, docs, training, collateral
- Channels: Internal comms, partner previews
- Owner: Who drives each workstream
- Success metric: Readiness criteria

**Launch (launch week):**
- Activities: Announcement, events, campaigns
- Channels: Email, social, PR, events
- Owner: Who executes
- Success metric: Launch day KPIs

**Post-launch (after launch):**
- Activities: Iterate based on feedback, scale adoption
- Channels: CS outreach, webinars, case studies
- Owner: Who owns follow-up
- Success metric: Adoption/revenue KPIs

**Step 5: Enablement Checklist**

Required deliverables:
- [ ] Sales training (what to pitch, objection handling)
- [ ] CS runbook (how to support, troubleshooting)
- [ ] Demo environment (working prototype/sandbox)
- [ ] Collateral (pitch deck, one-pager, video)
- [ ] Pricing/packaging (tiers, discounts, terms)
- [ ] Legal/compliance (contracts, terms, privacy)

**Step 6: Success Criteria**

Define metrics:
- **Leading indicators:** Early signals (signups, demos, trials)
- **Lagging indicators:** Business outcomes (revenue, retention, NPS)

**Step 7: Generate Output**

Write to `outputs/gtm/gtm-[initiative]-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: planning-gtm-launch
initiative: [Product/Feature name]
sources:
  - outputs/roadmap/Q1-2026-charters.md (modified: YYYY-MM-DD)
  - (market data provided by user or "Unknown")
downstream:
  - (launch execution tracked separately)
---

# GTM Plan: [Initiative]

## Initiative Context
**What:** [Product/feature name]
**Target launch:** [Date]
**Charter/PRD:** [Link to source document]

## Market Context

### TAM/SAM/SOM
- **TAM (Total Addressable Market):** [Size] - [Source or "Unknown"]
- **SAM (Serviceable Addressable Market):** [Size] - [Source or "Unknown"]
- **SOM (Obtainable Market):** [Target in Year 1] - [Source or "Estimate"]

### Competitive Landscape
| Competitor | Strength | Our Differentiation |
|------------|----------|---------------------|
| [Competitor 1] | [What they do well] | [How we're better/different] |
| [Competitor 2] | [What they do well] | [How we're better/different] |

### Customer Segments (ICP)

**Primary segment:**
- **Who:** [Description]
- **Pain points:** [Top 3 problems they have]
- **Why they'll buy:** [Value they get]
- **Evidence:** [VOC, customer interviews, or "Assumption"]

**Secondary segment:**
- **Who:** [Description]
- **Pain points:** [Top 3 problems]
- **Why they'll buy:** [Value]

## Positioning

### Value Proposition
[One sentence: What we do, for whom, that delivers what value]

### Differentiation (Why Us)
1. **[Differentiator 1]:** [Why this matters to customers]
2. **[Differentiator 2]:** [Why this matters to customers]
3. **[Differentiator 3]:** [Why this matters to customers]

### Messaging Framework

| Audience | Key Message | Supporting Points |
|----------|-------------|-------------------|
| **Customers** | [What they need to hear] | [3 supporting points] |
| **Sales** | [How to pitch] | [3 supporting points] |
| **Partners** | [Partnership value] | [3 supporting points] |
| **Press/Analysts** | [Industry narrative] | [3 supporting points] |

## Launch Plan

### Pre-Launch Phase
**Timeline:** [Start date] - [Launch date]

| Activity | Owner | Deliverable | Success Criterion | Status |
|----------|-------|-------------|-------------------|--------|
| Beta program | [Name] | 10 beta customers | Feedback collected | Pending |
| Sales training | [Name] | Training deck + session | Team certified | Pending |
| Collateral | [Name] | Deck, one-pager, video | Approved by leadership | Pending |
| Docs | [Name] | User guides, API docs | Published | Pending |

**Channels:** Internal comms, partner previews, beta customer access

### Launch Phase
**Timeline:** [Launch week dates]

| Activity | Owner | Channel | Success Metric | Status |
|----------|-------|---------|----------------|--------|
| Announcement | [Name] | Email, blog, social | 10K impressions | Pending |
| Launch event | [Name] | Webinar | 500 attendees | Pending |
| Press release | [Name] | PR wire | 5 media pickups | Pending |

**Channels:** Email blast, social media, PR, customer events

### Post-Launch Phase
**Timeline:** [First 30/60/90 days]

| Activity | Owner | Channel | Success Metric | Status |
|----------|-------|---------|----------------|--------|
| Customer feedback | [Name] | CS outreach | 20 interviews | Pending |
| Case studies | [Name] | Marketing | 3 published | Pending |
| Iteration sprint | [Name] | Product team | Ship fixes | Pending |

**Channels:** CS outreach, webinars, case studies, community

## Enablement Checklist

- [ ] **Sales training completed** - [Date or TBD]
- [ ] **CS runbook created** - [Date or TBD]
- [ ] **Demo environment ready** - [Date or TBD]
- [ ] **Collateral available** - Deck: [Y/N], One-pager: [Y/N], Video: [Y/N]
- [ ] **Pricing/packaging finalized** - [Y/N]
- [ ] **Legal/compliance approved** - [Y/N]

## Success Criteria

### Leading Indicators (Early Signals)
| Metric | Target | Timeframe | Source |
|--------|--------|-----------|--------|
| [Signups] | [N] | Week 1 | [Analytics tool] |
| [Demos booked] | [N] | Month 1 | [CRM] |
| [Trials started] | [N] | Month 1 | [Product analytics] |

### Lagging Indicators (Business Outcomes)
| Metric | Target | Timeframe | Source |
|--------|--------|-----------|--------|
| [Revenue] | $[N] | Quarter 1 | [Finance dashboard] |
| [Customers] | [N] | Quarter 1 | [CRM] |
| [Retention] | [%] | Quarter 2 | [Product analytics] |

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| [Competitive response] | High/Med/Low | High/Med/Low | [How to counter] |
| [Enablement delays] | High/Med/Low | High/Med/Low | [Backup plan] |
| [Low adoption] | High/Med/Low | High/Med/Low | [Demand gen plan] |

## Unknowns / Open Questions

- [What market data is missing?]
- [What enablement needs are unclear?]
- [What success metrics need definition?]

## Sources Used
- [file paths or "Market data from [source]"]
- [customer research source]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Market size $X] | Evidence/Unknown | [Analyst report or "Need research"] |
| [Customers have pain Y] | Evidence | [VOC:line or customer interviews] |
| [Competitor weakness Z] | Evidence/Assumption | [Competitive analysis or "Observed in market"] |
| [Revenue target $A] | Evidence | [Charter:line or OKRs] |
```

**Step 8: Copy to History & Update Tracker**

- Copy to `history/planning-gtm-launch/gtm-[initiative]-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

### GTM Phases Timeline

| Phase | Duration | Key Activities | Success Gate |
|-------|----------|----------------|--------------|
| **Pre-launch** | 4-8 weeks before | Beta, training, collateral | Enablement complete |
| **Launch** | Launch week | Announce, events, campaigns | Launch metrics hit |
| **Post-launch** | First 90 days | Feedback, iterate, scale | Adoption targets met |

### Common GTM Mistakes

- **Skipping pre-launch:** Launching before sales/CS ready
- **No differentiation:** Generic "better, faster" positioning
- **Ignoring competition:** Assuming we have no competitors
- **Metrics missing:** No way to know if launch succeeded
- **One-and-done:** Launching then moving on (no follow-up)

## Verification Checklist

- [ ] Market context documented (TAM/SAM/SOM)
- [ ] Competitive differentiation clear
- [ ] ICP defined with evidence
- [ ] Value prop crisp (1 sentence)
- [ ] Messaging per audience defined
- [ ] Launch phases mapped (pre/during/post)
- [ ] Enablement checklist complete
- [ ] Success metrics defined (leading + lagging)
- [ ] Risks identified with mitigation
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Market size] | Evidence/Unknown | [Source or "Need research"] |
| [Customer pain] | Evidence | [VOC or interviews] |
| [Competitive position] | Evidence/Assumption | [Analysis or assessment] |
| [Success target] | Evidence | [Charter or OKRs] |
