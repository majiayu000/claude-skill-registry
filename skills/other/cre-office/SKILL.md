---
name: cre-office
description: "CRE Office analysis suite - 8 specialist skills for U.S. office acquisitions, refinancings, lease-up, tenant credit, TI/LC underwriting, financing fit, and investment committee memo writing."
argument-hint: "[task-description]"
---

# CRE Office Suite

You have access to 8 specialist office skills for U.S. commercial real estate analysis.

## Available Skills

| Skill | File | Use When |
|---|---|---|
| Office Market and Flight-to-Quality Study | `skills/office-market-and-flight-to-quality-study.md` | User needs submarket, competitive set, flight-to-quality, or tenant-demand analysis |
| Office Rent Roll and Stacking Plan Analyst | `skills/office-rent-roll-and-stacking-plan-analyst.md` | User needs WALT, rollover, occupancy reconciliation, stacking plan, or floor-level exposure analysis |
| Office Lease Abstract Reviewer | `skills/office-lease-abstract-reviewer.md` | User needs office lease economics, recoveries, options, work letter, or assignment/sublease issue spotting |
| Office Rollover and Occupancy Cost Analyst | `skills/office-rollover-and-occupancy-cost-analyst.md` | User needs renewal probability, occupancy-cost pressure, or renewal-vs-relet economics |
| Office TI / LC Underwriting Model Builder | `skills/office-ti-lc-underwriting-model-builder.md` | User needs cash-flow underwriting with downtime, TI, LC, free rent, and net effective rent |
| Office Tenant Credit and Exposure Analyst | `skills/office-tenant-credit-and-exposure-analyst.md` | User needs tenant credit, industry concentration, guaranty, or downside vacancy analysis |
| Office Financing Fit | `skills/office-financing-fit.md` | User needs lender-lane fit, office debt sizing, reserves, or financing-risk analysis |
| Office IC Memo Writer | `skills/office-ic-memo-writer.md` | User needs a decision memo synthesizing office diligence findings |

## How to Use

1. Read the user's request to determine which office skill is needed.
2. Load the full skill file, for example: `Read skills/office-ti-lc-underwriting-model-builder.md`.
3. Load relevant knowledge files when the skill asks for them.
4. Follow the Strategy steps exactly.
5. Produce output in the specified format.
6. Run Quality Checks before delivering results.

For deeper analysis, load knowledge bases:

- `knowledge/office-benchmarks.md` - office market, quality-tier, vacancy, leasing, and operating guardrails
- `knowledge/office-lease-structures.md` - full-service, modified gross, base-year, expense-stop, NNN, BOMA, work letter, and option issue spotting
- `knowledge/office-ti-lc-economics.md` - TI, LC, free rent, downtime, net effective rent, and leasing-cost modeling
- `knowledge/office-lender-criteria.md` - office lender lanes, sizing tests, reserves, and financing red flags
- `knowledge/underwriting-calc.md` - canonical CRE formulas
- `knowledge/risk-scoring.md` - risk categorization for IC memo synthesis

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Office Market and Flight-to-Quality Study** - Market regime, prime vs commodity, competitive set, tenant demand, sublease pressure, conversion risk.

**Office Rent Roll and Stacking Plan Analyst** - Occupancy reconciliation, WALT, rollover schedule, tenant concentration, floor-by-floor vacancy.

**Office Lease Abstract Reviewer** - Lease economics, recovery structure, BOMA area, work letter, options, assignment/sublease, termination/contraction rights.

**Office Rollover and Occupancy Cost Analyst** - Tenant renewal probability, occupancy-cost pressure, renewal vs re-let economics, action plan.

**Office TI / LC Underwriting Model Builder** - Cash flow after leasing costs, net effective rent, downtime, TI, LC, free rent, debt stress.

**Office Tenant Credit and Exposure Analyst** - Tenant durability, parent/guarantor exposure, industry concentration, watchlist, downside vacancy.

**Office Financing Fit** - Bank, life company, CMBS, debt fund, SBA owner-user, private credit, reserve, and structure fit.

**Office IC Memo Writer** - Full decision memo for office acquisition, refinance, recap, or hold/sell decision.
