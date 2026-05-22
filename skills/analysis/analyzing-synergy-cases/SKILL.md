---
name: analyzing-synergy-cases
description: Structures revenue and cost synergy analysis with build-up methodology and realization timing. Use when estimating synergies, modeling cost savings, or analyzing revenue enhancement opportunities.
tags:
  - analysis
  - investment-banking
metadata:
  author: casemark
  practice_areas:
    - Investment Banking
    - Mergers and Acquisitions
    - Corporate Finance
  document_types:
    - Analysis Report
  skill_modes:
    - Analysis
---
# Analyzing Synergy Cases

Structures revenue and cost synergy analysis with bottom-up build methodology, realization phasing, and risk-adjusted valuation for M&A transactions.

## When To Use

- Estimating cost synergies (headcount, facilities, procurement, IT) for a proposed acquisition or merger
- Modeling revenue synergies (cross-sell, pricing power, geographic expansion, product bundling)
- Building a synergy bridge for management presentations or board materials
- Stress-testing synergy assumptions for fairness opinions or buyer due diligence
- Comparing synergy potential across multiple acquisition targets

## Inputs To Gather

- **Combined P&L data**: Both acquirer and target income statements, broken out by segment/function
- **Organizational charts**: Headcount by function and geography for overlap analysis
- **Facility and lease schedules**: Locations, square footage, lease terms, and consolidation candidates
- **Vendor and procurement data**: Top suppliers, contract terms, and volume discount thresholds
- **Revenue detail**: Customer lists, product mix, channel breakdown, and geographic coverage for cross-sell sizing
- **Integration timeline constraints**: Regulatory approval timing, IT migration dependencies, retention commitments
- **Precedent transaction synergies**: Comparable deals with disclosed synergy figures and realization track records

## Workflow

1. **Categorize synergy types** — Separate into cost synergies (headcount reduction, facilities consolidation, procurement savings, IT rationalization, G&A elimination) and revenue synergies (cross-sell, upsell, pricing, new market access). Create a synergy taxonomy table with line-item granularity.

2. **Build bottom-up estimates for each line item**
   - Headcount: Identify overlapping roles by function; apply elimination percentages (typically 20–40% of overlapping G&A, 5–15% of revenue-facing roles) [VERIFY against industry benchmarks]
   - Facilities: Map redundant locations; estimate savings net of lease break costs and relocation expenses
   - Procurement: Calculate combined spend by category; apply volume discount curves from supplier proposals or precedent data
   - Revenue: Size addressable cross-sell TAM using customer overlap analysis; apply conservative conversion rates (typically 5–15% penetration over 3 years) [VERIFY conversion assumptions with commercial DD findings]

3. **Phase realization over time** — Map each synergy to a realization curve. Cost synergies typically begin in Year 1 and reach run-rate by Year 2–3. Revenue synergies lag, often starting Year 2 with full run-rate at Year 3–5. Assign each line item a specific quarter for initiation and full realization.

4. **Estimate one-time costs to achieve** — For each synergy, quantify implementation costs: severance (typically 6–12 months per eliminated role), lease termination penalties, IT integration spend, rebranding, and change management. Express as a ratio of costs-to-achieve vs. annual run-rate synergies (market range: 0.5x–1.5x for cost synergies).

5. **Risk-adjust and build scenario cases**
   - **Base case**: Management estimates with moderate haircuts (10–20% reduction on cost synergies, 30–50% on revenue synergies)
   - **Downside case**: Apply higher haircuts (25–40% cost, 50–75% revenue) and extend realization timelines by 6–12 months
   - **Upside case**: Full management case with accelerated timeline
   - Assign probability weights if building an expected-value framework

6. **Calculate NPV of net synergies** — Discount phased net synergies (gross synergies minus costs to achieve) at the acquirer's WACC or a synergy-specific discount rate reflecting execution risk. Present as total NPV, NPV per share of target, and as a percentage of transaction enterprise value.

7. **Benchmark against precedents** — Compare synergy estimates (as % of combined revenue, combined COGS, or target revenue) to announced and realized synergies in comparable transactions. Flag material deviations with explanations.

## Output

- **Synergy summary table**: Line-item detail showing gross annual run-rate synergies by category, phased realization schedule (quarterly or annual), one-time costs to achieve, and net synergy by period
- **Synergy bridge chart**: Waterfall visualization from combined standalone costs/revenues to pro forma with synergies
- **Scenario matrix**: Base / downside / upside cases with NPV, run-rate, and cost-to-achieve for each
- **Precedent comparison table**: Target synergies benchmarked against 3–5 comparable transactions
- **Key assumptions register**: Documented assumptions with source references and [VERIFY] flags for unconfirmed inputs

## Quality Checks

- Every synergy line item traces to a specific operational driver (no unsupported "management judgment" buckets exceeding 10% of total)
- Revenue synergies do not exceed cost synergies in the base case without explicit justification [VERIFY — revenue synergy dominance is atypical and warrants scrutiny]
- Costs to achieve are explicitly modeled — never omitted or assumed to be zero
- Realization timeline reflects actual integration constraints (regulatory approvals, system migrations, contractual obligations)
- NPV discount rate reflects execution risk, not just cost of capital
- Precedent benchmarking uses realized synergies where available, not just announced targets
- Double-counting check: confirm no synergy appears in more than one category
- Tax effects on synergies are addressed (cost savings generate taxable income; restructuring charges may be deductible) [VERIFY tax treatment by jurisdiction]
