---
name: elasticity-lab
description: Use to run pricing elasticity experiments with consistent assumptions
  and guardrails.
---

# Elasticity Lab Skill

## When to Use
- Modeling price increases/decreases across segments.
- Evaluating new pricing metrics (consumption, seats, feature gates).
- Stress testing monetization experiments before council reviews.

## Framework
1. **Data Inputs** – define baseline metrics (ASP, win rate, churn, attach rate) with data sources.
2. **Elasticity Curves** – map expected response bands (conservative/moderate/aggressive).
3. **Scenario Builder** – plug in price/metric changes and auto-calc ARR, margin, churn impact.
4. **Risk Flags** – highlight cohorts sensitive to change (industry, tenure, product mix).
5. **Experiment Plan** – propose pilot cohorts, measurement windows, and success criteria.

## Templates
- Elasticity workbook (inputs, assumptions, scenarios, summary).
- Pilot plan checklist with KPI thresholds.
- Risk matrix by cohort.

## Tips
- Keep historical data windows consistent to avoid noisy comparisons.
- Document assumptions + version history for auditability.
- Pair with `pricing-governance` to log council approvals.

---
