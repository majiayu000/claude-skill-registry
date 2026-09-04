---
name: cre-retail
description: "CRE Retail analysis suite - 8 specialist skills for U.S. retail trade-area studies, rent roll and tenant mix, lease abstraction, co-tenancy and anchor risk, CAM recovery, underwriting, financing fit, and investment committee memo writing."
argument-hint: "[task-description]"
license: Apache-2.0
metadata:
  author: "Avi Hacker, J.D."
  organization: "The AI Consulting Network"
  homepage: https://www.theaiconsultingnetwork.com
  source: https://github.com/ahacker-1/cre-agent-skills
  copyright: "Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network"
---

# CRE Retail Suite

You have access to 8 specialist retail skills for U.S. commercial real estate analysis.

## Available Skills

| Skill | File | Use When |
|---|---|---|
| Retail Market and Trade Area Study | `skills/retail-market-and-trade-area-study.md` | User needs trade-area demand, void and leakage, competitive supply, anchor draw, or category-resilience analysis |
| Retail Rent Roll and Tenant Mix Analyst | `skills/retail-rent-roll-and-tenant-mix-analyst.md` | User needs space mix, tenant productivity, rollover, concentration, credit, or mark-to-market analysis from a retail rent roll |
| Retail Lease Abstract Reviewer | `skills/retail-lease-abstract-reviewer.md` | User needs retail lease economics, recovery structure, work letter, options, or assignment/sublease issue spotting |
| Retail Co-Tenancy and Anchor Risk Analyst | `skills/retail-co-tenancy-and-anchor-risk-analyst.md` | User needs anchor mapping, co-tenancy clause review, dark-anchor cascade modeling, or REA re-tenanting analysis |
| Retail CAM Reconciliation and Recovery Analyst | `skills/retail-cam-reconciliation-and-recovery-analyst.md` | User needs recoverable expense pool rebuild, CAM reconciliation testing, or recovery-income reconciliation to underwriting |
| Retail Underwriting Model Builder | `skills/retail-underwriting-model-builder.md` | User needs a lease-by-lease cash flow model with percentage rent, capped recoveries, sales-driven renewal probability, or a co-tenancy downside case |
| Retail Financing Fit | `skills/retail-financing-fit.md` | User needs lender-lane fit, retail debt sizing, reserves, or financing-risk analysis |
| Retail IC Memo Writer | `skills/retail-ic-memo-writer.md` | User needs a decision memo synthesizing retail diligence findings |

## How to Use

1. Read the user's request to determine which retail skill is needed.
2. Load the full skill file, for example: `Read skills/retail-underwriting-model-builder.md`.
3. Load relevant knowledge files when the skill asks for them.
4. Follow the Strategy steps exactly.
5. Produce output in the specified format.
6. Run Quality Checks before delivering results.

For deeper analysis, load knowledge bases:

- `knowledge/retail-benchmarks.md` - retail market, format, occupancy, rent, and leasing-capital guardrails
- `knowledge/retail-lease-structures.md` - percentage rent, CAM/recovery structure, co-tenancy, go-dark, REA, and option issue spotting
- `knowledge/retail-tenant-sales-and-occupancy-cost.md` - tenant sales reporting, occupancy cost ratio, and category-level productivity benchmarks
- `knowledge/retail-lender-criteria.md` - retail lender lanes, sizing tests, reserves, and financing red flags
- `knowledge/underwriting-calc.md` - canonical CRE formulas
- `knowledge/risk-scoring.md` - risk categorization for IC memo synthesis

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Retail Market and Trade Area Study** - Trade-area demand, void and leakage, competitive supply, anchor draw, access, category resilience, trade-area durability verdict.

**Retail Rent Roll and Tenant Mix Analyst** - Space mix, tenant productivity, rollover, concentration, credit, mark-to-market.

**Retail Lease Abstract Reviewer** - Lease economics, recovery structure, options, work letter, assignment/sublease, investor/lender/rent-roll conflicts.

**Retail Co-Tenancy and Anchor Risk Analyst** - Anchor mapping, co-tenancy clause testing, dark-anchor cascade, REA re-tenanting restrictions, mitigation plan.

**Retail CAM Reconciliation and Recovery Analyst** - Recoverable expense pool rebuild, prior reconciliation testing, recovery income reconciled to underwriting.

**Retail Underwriting Model Builder** - Lease-by-lease cash flow, percentage rent, capped recoveries, sales-driven renewal probability, tenant-type leasing capital, anchor reserve, co-tenancy downside case, lender sizing view.

**Retail Financing Fit** - Lender-lane fit, proceeds-controlling test, structure requirements before close.

**Retail IC Memo Writer** - Full decision memo synthesizing trade-area, rent roll, lease, co-tenancy, recovery, underwriting, and financing work.

---

## Attribution

Built and maintained by [The AI Consulting Network](https://www.theaiconsultingnetwork.com/?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills), the commercial real estate AI consulting practice of Avi Hacker, J.D., and part of [CRE Agent Skills](https://github.com/ahacker-1/cre-agent-skills), an open-source library of AI skills for commercial real estate.

If this skill saved you time and you want systems like it built inside your firm, [reach out](https://www.theaiconsultingnetwork.com/contact?utm_source=github&utm_medium=skill-file&utm_campaign=cre-agent-skills). We would love to work with you.

Copyright 2026 Avi Hacker, J.D. / The AI Consulting Network. Licensed under the [Apache License 2.0](https://github.com/ahacker-1/cre-agent-skills/blob/main/LICENSE). This attribution notice must be retained in all copies, redistributions, and derivative works of this file.
