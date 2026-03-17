---
name: pql-framework
description: Methodology for defining product-qualified lead (PQL) signals, scoring,
  and routing.
---

# PQL Framework Skill

## When to Use
- Standing up or recalibrating PQL/PQA programs.
- Aligning product, growth, and sales on what constitutes a high-intent product user.
- Auditing the health of existing PQL scoring + routing logic.

## Framework
1. **Signal Library** – catalog feature usage, plan limits, collaboration signals, intent, firmographics.
2. **Scoring Model** – weight signals, set decay rules, and define negative indicators.
3. **Tiering** – map PQL tiers (A/B/C) to follow-up motions and SLAs.
4. **Routing Rules** – specify owners, cues, channels (CRM tasks, Slack alerts, CS queue).
5. **Measurement Loop** – track conversion, ARR impact, and feedback for model tuning.

## Templates
- Signal inventory worksheet with data source + freshness.
- Scoring matrix with weights, thresholds, and decay logic.
- Routing decision tree linking tiers to plays.

## Tips
- Start with simple tiering, iterate once telemetry + feedback improve.
- Include “disqualifier” signals (expired trials, churn risk) to avoid noise.
- Pair with `operationalize-pql-routing` to push models into automation.

---
