---
name: fnd.r-segmenting-customers
description: Generates strategic customer segment definitions with observable filters, segment sizing, and pain intensity scores. Use when defining target customers, building Canvas section 04, translating market research to segments, or when user mentions "segments", "ICP", "target market", or "who to sell to".
allowed-tools: Read Write WebSearch
license: Complete terms in LICENSE.txt
---

# Customer Segmenting

Generate strategic customer segment definitions for `strategy/canvas/04.segments.md`.

## Prerequisites

Before proceeding, verify:
- `strategy/canvas/03.opportunity.md` exists (TAM/SAM/SOM data required)

If missing, inform user:
```
Canvas 03.opportunity.md required before defining segments.
Use fnd-researcher agent to establish market sizing first.
```

Optional context (read if exists):
- `strategy/canvas/01.context.md` — KBOS framework
- `strategy/canvas/05.problem.md` — Problem severity data

## Core Principle

Segments must be **observable and strategic**:

| Criterion | Test |
|-----------|------|
| Observable | Can identify via searchable database query |
| Sizeable | Market size estimable from public data |
| Accessible | Reachable through known channels |
| Differentiable | Distinct needs from other segments |

## Process

### 1. Load Context

Read available canvas files:
```
strategy/canvas/03.opportunity.md  # Required: TAM/SAM/SOM
strategy/canvas/01.context.md      # Optional: strategic context
strategy/canvas/05.problem.md      # Optional: pain data
```

Extract: market size, trends, existing customer hypotheses.

### 2. List Segment Hypotheses

From market research, identify 3-5 potential customer groups.

For each, capture:
- Who they are (role, company type)
- Why they might buy (problem fit)
- How big the group is (rough estimate)

### 3. Define Observable Filters

For each segment, identify 2-4 **searchable** criteria.

**Valid filters** (can query in databases):
- Company size: "50-200 employees"
- Industry: "E-commerce, NAICS 454110"
- Technology: "Uses Shopify Plus"
- Geography: "US-based, tier-1 cities"
- Behavior: "Monthly GMV >$100K"

**Invalid filters** (not searchable):
- "Innovative companies"
- "Growth-minded founders"
- "Customer-centric organizations"

See [references/filters.md](references/filters.md) for comprehensive examples.

### 4. Score Pain Intensity

Rate each segment's pain 1-5:

| Score | Signal |
|-------|--------|
| 5 | Hair-on-fire, actively buying solutions |
| 4 | Significant pain, budget exists |
| 3 | Recognized problem, no urgency |
| 2 | Mild inconvenience |
| 1 | Unaware of problem |

**Require evidence for each score** — job postings, market reports, interview quotes.

See [references/scoring.md](references/scoring.md) for detailed rubric.

### 5. Estimate Segment Size

For each segment, calculate:
- Total matching filters (from industry data)
- Portion within SAM (addressable)
- Derivation source (cite report or calculation)

Use 03.opportunity.md TAM/SAM as ceiling.

### 6. Prioritize Segments

Rank by: `Pain Intensity × Willingness to Pay × Accessibility`

Select:
- **1 Primary (P0)** — Immediate focus, highest score
- **1-2 Secondary (P1)** — Expansion path

Document rationale for prioritization.

### 7. Write Output

Format per [references/template.md](references/template.md).

Write to: `strategy/canvas/04.segments.md`

## Quality Checklist

Before writing output, verify:

- [ ] Each segment has 2+ observable, searchable filters
- [ ] No psychographic traits in filters
- [ ] Segment sizes quantified with sources
- [ ] Pain scores have evidence justification
- [ ] 1-3 segments total (not 5+)
- [ ] Clear prioritization rationale
- [ ] Cross-references 05.problem.md if exists

## Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too many segments | 5+ with blurry boundaries | Consolidate to 1-3 focused segments |
| Vague sizing | "Large market" | "~12,000 US companies matching filters" |
| Missing pain evidence | "Pain: 4" | "Pain: 4 — 340 job postings for this role" |
| Psychographic filters | "Forward-thinking retailers" | "Retailers >$1M GMV on modern platforms" |
| No prioritization logic | "Both equally important" | "Primary: highest pain (5) + proven WTP" |

## Output Location

```
strategy/canvas/04.segments.md
```

## Boundaries

- Does NOT validate segment existence (requires outreach)
- Does NOT guarantee segment accessibility
- Does NOT interview customers (provides framework)
- Segment sizes are estimates from available data
- Pain scores require evidence — flag when assumed
- Does NOT handle persona creation (behavior, not demographics)
- Observable filters must be searchable in databases
- Psychographic traits are NOT valid filters

## Resources

- **Output template**: [references/template.md](references/template.md)
- **Filter examples**: [references/filters.md](references/filters.md)
- **Scoring rubric**: [references/scoring.md](references/scoring.md)