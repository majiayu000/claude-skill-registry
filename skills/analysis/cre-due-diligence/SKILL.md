---
name: cre-due-diligence
description: "CRE Due Diligence analysis suite — 7 specialist skills for multifamily property analysis including rent roll validation, expense benchmarking, market study, physical inspection, environmental review, title review, and tenant credit assessment."
argument-hint: "[task-description]"
---

# CRE Due Diligence Suite

You have access to 7 specialist due diligence skills for commercial real estate multifamily acquisitions. Use the appropriate skill based on what the user needs analyzed.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Rent Roll Analyst | `skills/rent-roll-analyst.md` | User provides a rent roll and wants revenue validation, loss-to-lease analysis, tenant concentration risks, anomaly detection |
| OpEx Analyst | `skills/opex-analyst.md` | User provides T-12 operating expenses and wants benchmarking, trend analysis, expense anomaly detection |
| Market Study | `skills/market-study.md` | User wants submarket research — demographics, employment, supply pipeline, rent comps, competitive analysis |
| Physical Inspection | `skills/physical-inspection.md` | User provides inspection reports or property details and wants condition assessment, CapEx scheduling, deferred maintenance quantification |
| Environmental Review | `skills/environmental-review.md` | User provides Phase I ESA or environmental data and wants risk assessment, regulatory compliance check, remediation cost estimation |
| Legal & Title Review | `skills/legal-title-review.md` | User provides title commitment or survey and wants exception analysis, encumbrance review, easement impact assessment |
| Tenant Credit | `skills/tenant-credit.md` | User provides tenant details and wants creditworthiness assessment, concentration risk analysis, lease rollover exposure |

## How to Use

1. Read the user's request to determine which skill(s) are needed
2. Load the full skill file using `Read` — e.g., `Read skills/rent-roll-analyst.md`
3. Follow the Strategy steps in the loaded skill exactly
4. Produce output in the format specified by the skill
5. Run the Quality Checks before delivering results

For deeper analysis, also load the relevant knowledge base files:
- `knowledge/underwriting-calc.md` — CRE financial formulas (NOI, cap rate, DSCR, IRR, etc.)
- `knowledge/multifamily-benchmarks.md` — industry benchmarks by property class and region
- `knowledge/risk-scoring.md` — 9-category risk scoring framework

If the user says "$ARGUMENTS", use that to determine which skill to load and what data to analyze.

## Quick Reference

**Rent Roll Analyst** — Validates: unit mix, in-place vs market rents, loss-to-lease (SIGNIFICANT >10%, MODERATE 5-10%, MINIMAL <5%), physical vs economic occupancy, tenant concentration (flag >10% single tenant), anomalies (below-market >15%, long vacancy >90 days, same-day leases, MTM >15%)

**OpEx Analyst** — Validates: per-unit expenses by category vs Class A/B/C benchmarks, management fee (typically 3-5%), tax reassessment risk, utility trends, insurance adequacy, total OpEx ratio

**Market Study** — Researches: submarket demographics, employment drivers, construction pipeline, absorption rates, rent comps from 3+ sources, competitive set within 3-mile radius

**Physical Inspection** — Assesses: roof, HVAC, plumbing, electrical, structural, site conditions, unit interiors — each scored by condition with remaining useful life and replacement cost

**Environmental Review** — Evaluates: Phase I ESA findings, RECs/CRECs/HRECs, contamination sources, vapor intrusion risk, regulatory compliance, remediation cost ranges

**Legal & Title Review** — Analyzes: title exceptions, easements, liens, deed restrictions, HOA/CC&Rs, survey discrepancies, boundary issues

**Tenant Credit** — Assesses: individual and portfolio credit risk, income concentration, lease rollover schedule, Section 8/subsidized mix, renewal probability
