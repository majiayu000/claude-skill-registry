---
name: cre-development
description: "CRE Development and Construction suite - 8 specialist skills for U.S. site/entitlement screening, budget and yield-on-cost, construction loan sizing, GC contracts, draw review, schedule risk, lease-up pro forma, and IC memo writing."
argument-hint: "[task-description]"
license: Apache-2.0
metadata:
  author: "Avi Hacker, J.D."
  organization: "The AI Consulting Network"
  homepage: https://www.theaiconsultingnetwork.com
  source: https://github.com/ahacker-1/cre-agent-skills
  copyright: "Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network"
---

# CRE Development and Construction Suite

You have access to 8 specialist development and construction skills for U.S. ground-up development and heavy redevelopment.

## Available Skills

| Skill | File | Use When |
|---|---|---|
| Site and Entitlement Screen | `skills/site-and-entitlement-screen.md` | User needs zoning fit, entitlement path, fees and exactions, environmental and physical constraint, or political-risk screening for a development site |
| Development Budget and Yield on Cost Analyst | `skills/development-budget-and-yield-on-cost-analyst.md` | User needs a ground-up or heavy-redevelopment budget built or audited against untrended and trended yield on cost, development spread, residual land value, and overrun sensitivity |
| Construction Loan Sizing and Structure | `skills/construction-loan-sizing-and-structure.md` | User needs a construction loan sized against controlling tests, cash equity quantified, interest reserve and guaranty structure, draw controls, and takeout with lender-lane fit |
| GC Contract and Change Order Reviewer | `skills/gc-contract-and-change-order-reviewer.md` | User needs a GC or CM agreement and its exhibits reviewed for price, time, payment, and risk transfer, or individual change orders reviewed for entitlement, pricing, and schedule impact |
| Construction Draw and Cost-to-Complete Reviewer | `skills/construction-draw-and-cost-to-complete-reviewer.md` | User needs a monthly construction draw package reviewed end to end and a fund, partial-fund, or hold recommendation |
| Schedule and Delivery Risk Tracker | `skills/schedule-and-delivery-risk-tracker.md` | User needs a development schedule tracked from entitlement through certificate of occupancy, delay priced, and a recovery plan produced |
| Lease-Up and Stabilization Pro Forma | `skills/lease-up-and-stabilization-pro-forma.md` | User needs the interval between first delivery and stabilization modeled, including absorption, concessions, operating shortfall, interest carry, and takeout repayment |
| Development IC Memo Writer | `skills/development-ic-memo-writer.md` | User needs a decision memo synthesizing site, budget, capital stack, contract and schedule, and lease-up diligence findings |

## How to Use

1. Read the user's request to determine which development skill is needed.
2. Load the full skill file, for example: `Read skills/construction-loan-sizing-and-structure.md`.
3. Load relevant knowledge files when the skill asks for them.
4. Follow the Strategy steps exactly.
5. Produce output in the specified format.
6. Run Quality Checks before delivering results.

For deeper analysis, load knowledge bases:

- `knowledge/development-benchmarks.md` - development budget, contingency, escalation, yield-on-cost, and absorption guardrails
- `knowledge/construction-lending-criteria.md` - construction lender sizing tests, equity and HVCRE rules, interest reserve, guaranty, and takeout criteria
- `knowledge/construction-contracts-and-draw-controls.md` - owner-contractor contract structure, money mechanics, changes, completion, and monthly draw controls
- `knowledge/entitlement-and-site-risk.md` - zoning, entitlement timeline, impact fees, environmental review, and political and litigation risk
- `knowledge/underwriting-calc.md` - canonical CRE formulas
- `knowledge/risk-scoring.md` - risk categorization for IC memo synthesis

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Site and Entitlement Screen** - Zoning fit, entitlement path, fees and exactions, environmental and physical constraints, political risk, go/no-go on pursuit.

**Development Budget and Yield on Cost Analyst** - Sources and uses, untrended and trended yield on cost, development spread, residual land value, profit margin, overrun sensitivity.

**Construction Loan Sizing and Structure** - Controlling sizing tests, cash equity requirement, interest reserve, guaranty package, draw controls, takeout, lender-lane fit.

**GC Contract and Change Order Reviewer** - Contract price, time, payment, and risk-transfer review; change order entitlement, pricing, and schedule impact; negotiation positions.

**Construction Draw and Cost-to-Complete Reviewer** - Schedule of values, percent complete, retainage, stored materials, lien waivers, title date-down, cost to complete, in-balance test, fund/partial-fund/hold recommendation.

**Schedule and Delivery Risk Tracker** - Entitlement-through-CO milestone tracking, delivery date vs. loan and lease-up plan, delay pricing, recovery plan.

**Lease-Up and Stabilization Pro Forma** - Absorption pace, pre-leasing, concession burn-off, operating shortfall, interest carry, breakeven and stabilization dates, takeout repayment test.

**Development IC Memo Writer** - Full decision memo synthesizing site, budget, capital stack, contract and schedule, and lease-up diligence into a go/no-go recommendation.

---

## Attribution

Built and maintained by [The AI Consulting Network](https://www.theaiconsultingnetwork.com/?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills), the commercial real estate AI consulting practice of Avi Hacker, J.D., and part of [CRE Agent Skills](https://github.com/ahacker-1/cre-agent-skills), an open-source library of AI skills for commercial real estate.

If this skill saved you time and you want systems like it built inside your firm, [reach out](https://www.theaiconsultingnetwork.com/contact?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills). We would love to work with you.

Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network. Licensed under the [Apache License 2.0](https://github.com/ahacker-1/cre-agent-skills/blob/main/LICENSE). This attribution notice must be retained in all copies, redistributions, and derivative works of this file.
