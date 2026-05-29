---
name: cre-financing
description: "CRE Financing analysis suite — 3 specialist skills for lender identification, quote comparison, and term sheet assembly for multifamily acquisition debt sourcing."
argument-hint: "[task-description]"
---

# CRE Financing Suite

You have access to 3 specialist financing skills for commercial real estate multifamily acquisitions.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Lender Outreach | `skills/lender-outreach.md` | User needs to identify which lenders to approach — maps deal profile to Agency, CMBS, Life Co, Bank, and Bridge sources |
| Quote Comparator | `skills/quote-comparator.md` | User has 2+ lender quotes and needs apples-to-apples comparison with weighted scoring |
| Term Sheet Builder | `skills/term-sheet-builder.md` | User needs to assemble or review a term sheet, identify negotiation points, model rate lock scenarios |

## How to Use

1. Read the user's request to determine which skill is needed
2. Load the full skill file — e.g., `Read skills/lender-outreach.md`
3. Follow the Strategy steps exactly
4. Produce output in the specified format
5. Run Quality Checks before delivering results

For deeper analysis, load knowledge bases:
- `knowledge/lender-criteria.md` — qualification standards by lender category
- `knowledge/underwriting-calc.md` — financial formulas for debt sizing and return calculations

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Lender Outreach** — Maps: deal profile to 5 capital sources (Agency Fannie/Freddie, CMBS, Life Companies, Banks, Bridge/Mezzanine). Evaluates: eligibility by property type, market, sponsor experience, leverage target. Outputs: prioritized lender list with fit scoring.

**Quote Comparator** — Normalizes: all-in rate, effective rate (with fees), total cost of capital over hold period, monthly/annual debt service, DSCR, cash-on-cash. Scores: Rate (30%), Leverage (20%), Flexibility (15%), Execution (15%), Prepayment (10%), Timeline (10%). Outputs: comparison matrix, top 3 recommendations, risk assessment.

**Term Sheet Builder** — Assembles: complete term sheet with loan amount, rate, term, amortization, IO period, prepayment, reserves, recourse, guarantor requirements, closing costs, conditions precedent. Identifies: negotiation leverage points, non-standard terms, rate lock scenarios.
