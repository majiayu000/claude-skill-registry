---
name: saas-metrics-diligence
description: "Analyze SaaS and usage-based metrics for diligence: NDR/NRR, gross margin, CAC payback, sales efficiency, cohorts, and unit economics by segment. Use when diligencing B2B SaaS or infra companies."
license: Proprietary
compatibility: Requires spreadsheet-style data; optional Python for calculation; optional Salesforce logging.
metadata:
  author: evalops
  version: "0.1"
---
# SaaS metrics diligence

## When to use
Use this skill when:
- Diligencing B2B SaaS, PLG, or usage-based businesses
- You need to translate raw metrics into an investment view
- You want to detect metric illusions (cohort mixing, accounting artifacts)

## Inputs you should request (only if missing)
- Revenue metrics: ARR/MRR by month (12–24 months)
- Customer counts and logos (by cohort if possible)
- Gross margin (and what’s included in COGS)
- Sales & marketing spend (and headcount)
- Churn/expansion data by cohort
- Pricing and ACV distribution

## Outputs you must produce
1) **Metrics readout** (1–2 pages)  
2) **Cohort/retention assessment** (what’s driving NDR)  
3) **Unit economics summary** (CAC payback, efficiency)  
4) **Questions/risks** (ranked) + recommended next data

Templates:
- assets/metrics-readout.md
- assets/metrics-worksheet.csv

## Procedure

### 1) Normalize definitions (do not assume)
Write down:
- What counts as “revenue” (bookings vs recognized)
- Whether NDR is logo-weighted or revenue-weighted
- Whether gross margin includes hosting, support, etc.

### 2) Retention: start with cohorts
Compute:
- Gross revenue retention (GRR) if possible
- Net dollar retention (NDR/NRR) by cohort and by segment

Look for:
- expansion vs churn drivers
- segment mix effects (beware Simpson’s paradox)
- “one whale” distorting NDR

### 3) Efficiency and payback
Compute:
- CAC payback (on a gross margin basis)
- Sales efficiency / magic number (if you use it)
- Contribution margin (if available)

Check:
- whether growth is cash-efficient at current payback
- whether payback is improving or worsening

### 4) Pricing and ACV distribution
- Identify ACV bands
- Evaluate whether the product supports expansion (seat-based, usage-based, tier upgrades)
- Check whether pricing matches perceived value

### 5) Produce an investment-grade interpretation
Translate metrics into:
- “Is this repeatable?” (cohorts + pipeline)
- “Is this durable?” (retention + switching costs)
- “Is this capital-efficient?” (payback + margins)
- “What breaks at scale?” (support costs, infra costs, sales cycle)

## References
- Tomasz Tunguz’s public writing is a useful mental model set for NDR, payback, and SaaS efficiency metrics.

## Salesforce logging (optional)
If your Opportunity has metric fields:
- Update NDR, GRR, GM, payback, etc.
Otherwise:
- Attach the metrics readout as a File/Note to the Opportunity.

## Edge cases
- If data is messy: request raw exports and define one source of truth.
- If NDR is high but churn is hidden: insist on cohort-level GRR and logo churn.
