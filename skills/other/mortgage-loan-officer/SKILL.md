---
name: mortgage-loan-officer
category: business-finance
description: Guides borrowers through mortgage refinance evaluation — collects loan data, extracts mortgage statement fields, evaluates qualification, and delivers recommendations with consumer-friendly communication.
---

# Mortgage Loan Officer

Knowledgeable mortgage loan officer assistant that guides borrowers through a refinance evaluation by collecting information, extracting data from mortgage statements, analyzing refinance scenarios, and delivering clear recommendations.

## When to Use This Skill

- Borrower wants to explore refinance options
- Need to collect and validate loan scenario data
- Extracting fields from uploaded mortgage statements
- Evaluating credit score tiers, DTI ratios, and LTV thresholds

## What This Skill Does

1. Collects borrower information through a structured conversational interview
2. Extracts mortgage data from uploaded statements (servicer, balance, rate, escrow, loan type)
3. Validates all inputs against underwriting guidelines
4. Detects FHA Streamline and VA IRRRL eligibility automatically
5. Maps collected data to a LoanScenario for the pricing engine

## Supported Loan Types

- Conventional (fixed and adjustable)
- FHA
- FHA Streamline (FHA-to-FHA, non-credit qualifying)
- VA IRRRL (Interest Rate Reduction Refinance Loan)
- VA Cash-Out

## Installation

This skill is part of the mortgage plugin. Install via:

```
/plugin marketplace add lendtrain/mortgage
/plugin install mortgage@mortgage
```

Full source: [github.com/lendtrain/mortgage](https://github.com/lendtrain/mortgage)
