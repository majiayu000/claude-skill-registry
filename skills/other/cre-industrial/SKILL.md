---
name: cre-industrial
description: "CRE Industrial analysis suite - 8 specialist skills for U.S. industrial acquisitions, covering market study, lease roster analysis, lease abstraction, tenant credit, physical inspection, underwriting, financing fit, and investment committee memo writing."
argument-hint: "[task-description]"
---

# CRE Industrial Suite

You have access to 8 specialist industrial skills for U.S. commercial real estate acquisitions.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Industrial Market Study | `skills/industrial-market-study.md` | User needs a submarket view, demand / supply analysis, or competitive positioning for an industrial asset |
| Industrial Lease Roster Analyst | `skills/industrial-lease-roster-analyst.md` | User needs WALT, rollover, concentration, and release-risk analysis from an industrial lease roster |
| Industrial Lease Abstract Reviewer | `skills/industrial-lease-abstract-reviewer.md` | User needs an industrial lease abstract with reimbursement, repair, option, and transfer analysis |
| Industrial Tenant Credit Analyst | `skills/industrial-tenant-credit-analyst.md` | User needs tenant-quality, concentration, and release-risk analysis |
| Industrial Physical Inspection | `skills/industrial-physical-inspection.md` | User needs building-condition and functional-competitiveness analysis |
| Industrial Underwriting Model Builder | `skills/industrial-underwriting-model-builder.md` | User needs a base-case industrial underwriting model |
| Industrial Financing Fit | `skills/industrial-financing-fit.md` | User needs lender-category fit and debt-structure guidance |
| Industrial IC Memo Writer | `skills/industrial-ic-memo-writer.md` | User needs a decision memo synthesizing industrial diligence findings |

## How to Use

1. Read the user's request to determine which skill is needed
2. Load the full skill file - e.g. `Read skills/industrial-underwriting-model-builder.md`
3. Follow the Strategy steps exactly
4. Produce output in the specified format
5. Run Quality Checks before delivering results

For deeper analysis, load knowledge bases:

- `knowledge/industrial-benchmarks.md` - subtype-aware U.S. industrial benchmarks
- `knowledge/industrial-lease-structures.md` - reimbursement, repair, and transfer structure guidance
- `knowledge/industrial-lender-criteria.md` - lender-type fit for industrial deals

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Industrial Market Study** - Market strength, subtype fit, competing inventory, logistics access, release depth.

**Industrial Lease Roster Analyst** - WALT, concentration, reimbursement structure, rollover schedule, release risk.

**Industrial Lease Abstract Reviewer** - Lease structure, reimbursements, repairs, options, transfer rights, estoppel, SNDA.

**Industrial Tenant Credit Analyst** - Tenant durability, concentration, building dependence, release risk.

**Industrial Physical Inspection** - Building condition, function, fire protection, power, capital needs.

**Industrial Underwriting Model Builder** - Contractual income, rollover, downtime, TI, LC, capital plan, returns.

**Industrial Financing Fit** - Bank, life company, CMBS, bridge, and SBA owner-user fit.

**Industrial IC Memo Writer** - Market, lease, physical, underwriting, financing, and risk synthesis into a go / no-go memo.
