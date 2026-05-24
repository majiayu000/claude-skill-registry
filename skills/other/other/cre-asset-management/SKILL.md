---
name: cre-asset-management
description: "CRE Asset Management analysis suite — 9 specialist skills for post-acquisition multifamily operations including annual budgeting, monthly variance analysis, rent collection, renewal decisions, lease-up tracking, capex execution, NOI improvement, hold/sell/refi scenario analysis, and quarterly asset review memos."
argument-hint: "[task-description]"
---

# CRE Asset Management Suite

You have access to 9 specialist asset management skills for commercial real estate multifamily post-acquisition operations. Use the appropriate skill based on what the user needs analyzed.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Annual Operating Budget Builder | `skills/annual-operating-budget-builder.md` | User needs to build a next-year operating budget from T-12 actuals and rent roll, line-by-line with every OpEx category traced to a benchmark |
| Monthly Variance Analyst | `skills/monthly-variance-analyst.md` | User provides monthly/YTD actuals vs budget and wants variance analysis classified as Timing / Permanent / One-Time with reforecast triggers |
| Rent Collection & Delinquency Manager | `skills/rent-collection-delinquency-manager.md` | User provides A/R aging and wants delinquency classification, bad-debt reserve sizing, tenant action list, and chronic-delinquent identification |
| Renewal Decision Analyst | `skills/renewal-decision-analyst.md` | User provides expiring-lease list and wants per-lease retain-vs-replace economics with rent-bump elasticity and turnover-cost comparison |
| Lease-Up & Concessions Analyst | `skills/lease-up-concessions-analyst.md` | User has a lease-up or stabilizing property and wants absorption velocity, concession burn-off tracking, and stabilization reforecast |
| CapEx / Value-Add Execution Tracker | `skills/capex-value-add-execution-tracker.md` | User provides value-add program data and wants capex execution tracking, rent-premium realization, yield-on-cost, and cost/schedule variance |
| NOI Improvement Analyst | `skills/noi-improvement-analyst.md` | User wants a prioritized list of NOI-lift levers scored on Impact × Difficulty with estimated annual lift and time-to-realize |
| Hold / Sell / Refi Analyst | `skills/hold-sell-refi-analyst.md` | User wants hold vs refi vs disposition scenario comparison with IRR, equity multiple, and recommended path |
| Quarterly Asset Review Writer | `skills/quarterly-asset-review-writer.md` | User wants the composite Quarterly Asset Review (QAR) memo integrating upstream skill outputs into the 10-section LP-facing narrative |

## How to Use

1. Read the user's request to determine which skill(s) are needed
2. Load the full skill file using `Read` — e.g., `Read skills/annual-operating-budget-builder.md`
3. Follow the Strategy steps in the loaded skill exactly
4. Produce output in the format specified by the skill
5. Run the Quality Checks before delivering results

For deeper analysis, also load the relevant knowledge base files:
- `knowledge/asset-management-benchmarks.md` — variance materiality thresholds, A/R aging reserves, turnover decomposition, ancillary lifts, OpEx-KPI thresholds for post-acquisition operations
- `knowledge/renewal-economics.md` — Retain-vs-Replace framework, rent-bump elasticity, tenant tier definitions, hold/sell/refi decision frameworks
- `knowledge/asset-management-reporting-standards.md` — QAR structure, KPI checklist, variance-classification-at-reporting-layer conventions, LP-facing commentary norms
- `knowledge/underwriting-calc.md` — canonical CRE formulas (NOI, EGI, GPI, cap rate, DSCR, IRR, equity multiple, effective rent)
- `knowledge/multifamily-benchmarks.md` — industry benchmarks by property class, region, vintage, COL tier; property tax by state; insurance cat-zone adjustments

If the user says "$ARGUMENTS", use that to determine which skill to load and what data to analyze.

## Quick Reference

**Annual Operating Budget Builder** — Builds: line-by-line next-year budget from T-12 + rent roll; contract-driven escalators for taxes/insurance/payroll; benchmark-calibrated run-rate for R&M/turnover/marketing; seasonality curve; NOI (AM convention, reserves below line) and NCF (Fannie/Freddie Form 4660)

**Monthly Variance Analyst** — Classifies: every GL line variance vs budget as Timing / Permanent / One-Time per taxonomy-seed §3; applies dual-threshold materiality (10% / $25K default, line-item and property-scale adjustments); surfaces reforecast triggers

**Rent Collection & Delinquency Manager** — Sizes: A/R aging buckets (current / 1-30 / 31-60 / 61-90 / 90+); bad-debt reserve by class; chronic delinquents; write-off recommendations; tenant action list

**Renewal Decision Analyst** — Computes: per-lease Retain-vs-Replace economics using rent-bump elasticity, tenant tier, turnover cost components, seasonality modifiers; outputs retain / replace / negotiate per expiring lease

**Lease-Up & Concessions Analyst** — Tracks: absorption velocity vs plan, effective rent vs face rent, concession burn-off phase (heavy / tapering / normal), stabilization reforecast trigger

**CapEx / Value-Add Execution Tracker** — Tracks: capex spent vs budget, units renovated vs planned, rent premium realization %, yield-on-cost, cost overrun %, schedule variance; flags failure modes

**NOI Improvement Analyst** — Prioritizes: NOI-lift levers on Impact × Difficulty score; estimates annual lift and time-to-realize; flags quick wins and regulatory-risk levers; bounds estimates to benchmark ranges

**Hold / Sell / Refi Analyst** — Scenarios: hold / refi-and-hold / sell-now / sell-at-stabilization with projected IRR, equity multiple, and net proceeds; outputs recommendation with rationale; includes disposition handoff package

**Quarterly Asset Review Writer** — Produces: 10-section QAR memo (Executive Summary, KPI Dashboard, Variance Drivers, Leasing & Occupancy, Capital Projects, Market Update, Risks & Watch Items, Financial Position, Forward Look, Consumed Upstream Outputs) consuming outputs from the other 8 AM skills
