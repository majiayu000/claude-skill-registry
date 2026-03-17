---
name: closing-costs
category: business-finance
description: Calculates itemized state-specific closing costs for mortgage refinance transactions across 10 licensed states, with product-specific fees for Conventional, FHA, FHA Streamline, VA IRRRL, and VA Cash-Out.
---

# Closing Costs

Provides itemized estimated closing costs for refinance transactions with state-specific fee schedules, product-specific calculations, and compliance-required disclosures.

## When to Use This Skill

- Calculating closing costs for a refinance quote
- Presenting fee breakdowns to borrowers
- Determining FHA UFMIP refund netting for Streamline refinances
- Calculating VA funding fees with disability exemption handling

## What This Skill Does

1. Calculates Section A (lender fees), Section B (third-party fees), Section C (title/settlement), and Section E (recording/taxes)
2. Applies state-specific title insurance rate formulas for all 10 licensed states
3. Handles FHA UFMIP with refund netting for Streamline refinances
4. Handles VA funding fee with disability exemption detection
5. Presents full itemized breakdown with compliance disclosures

## Supported States

| State | Key Taxes/Fees |
|-------|---------------|
| Georgia (GA) | Intangible tax $3.00/$1,000 |
| Alabama (AL) | Mortgage recordation tax $1.50/$1,000 |
| Florida (FL) | Doc stamp $3.50/$1,000 + intangible $2.00/$1,000 |
| Kentucky (KY) | No transfer tax on refinance |
| North Carolina (NC) | Attorney-closing state, no excise tax on refi |
| Oregon (OR) | No mortgage recording tax |
| South Carolina (SC) | Attorney-closing state |
| Tennessee (TN) | Indebtedness tax $1.15/$1,000 |
| Texas (TX) | No mortgage recording tax |
| Utah (UT) | No mortgage tax |

## Installation

This skill is part of the mortgage plugin. Install via:

```
/plugin marketplace add lendtrain/mortgage
/plugin install mortgage@mortgage
```

Full source: [github.com/lendtrain/mortgage](https://github.com/lendtrain/mortgage)
