---
name: cre-underwriting
description: "CRE Underwriting analysis suite — 3 specialist skills for building pro formas, running sensitivity scenarios, and writing investment committee memos for multifamily acquisitions."
argument-hint: "[task-description]"
---

# CRE Underwriting Suite

You have access to 3 specialist underwriting skills for commercial real estate multifamily acquisitions.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Financial Model Builder | `skills/financial-model-builder.md` | User needs a 5-year pro forma with NOI, debt service, cash flow, reversion, and return metrics (IRR, equity multiple, CoC) |
| Scenario Analyst | `skills/scenario-analyst.md` | User wants to stress-test a deal across 27 scenarios varying rent growth, vacancy, and exit cap rate |
| IC Memo Writer | `skills/ic-memo-writer.md` | User needs to synthesize all analysis into a structured investment committee memorandum with go/no-go recommendation |

## How to Use

1. Read the user's request to determine which skill is needed
2. Load the full skill file — e.g., `Read skills/financial-model-builder.md`
3. Follow the Strategy steps exactly
4. Produce output in the specified format
5. Run Quality Checks before delivering results

For deeper analysis, load knowledge bases:
- `knowledge/underwriting-calc.md` — every CRE financial formula
- `knowledge/multifamily-benchmarks.md` — industry benchmarks by property class and region

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Financial Model Builder** — Builds: 5-year pro forma (GPI → Vacancy → EGI → OpEx → NOI → Debt Service → Cash Flow → Reversion). Calculates: IRR, equity multiple, cash-on-cash, cap rate, debt yield, DSCR. Models: stabilization, renovation impact, refinancing.

**Scenario Analyst** — Runs: 27 scenarios (3×3×3 matrix) across rent growth (low/base/high), vacancy (low/base/high), and exit cap rate (low/base/high). Outputs: sensitivity tables, break-even analysis, probability-weighted returns, downside risk quantification.

**IC Memo Writer** — Produces: 11-section investment committee memo with executive summary, market overview, property description, financial analysis, risk assessment, and go/no-go recommendation. Includes: 3 appendices (pro forma, scenario matrix, comparable sales).
