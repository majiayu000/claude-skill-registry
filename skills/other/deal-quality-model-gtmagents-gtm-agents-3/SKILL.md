---
name: deal-quality-model
description: Scoring system for opportunity hygiene, win likelihood, and inspection
  prioritization.
---

# Deal Quality Model Skill

## When to Use
- Prioritizing inspection focus during forecast and pipeline reviews.
- Flagging opportunities with incomplete data or low win signals.
- Creating alerts when critical hygiene steps (MEDDIC, next steps) are missing.

## Framework
1. **Input Signals** – discovery notes, exec sponsor, mutual plan, activity recency, budget proof.
2. **Weighting** – assign weights per signal (required, strong, nice-to-have) per segment.
3. **Score Bands** – define thresholds for healthy, watch, and critical opportunities.
4. **Automation Hooks** – integrate with CRM validation rules, Slack alerts, and dashboards.
5. **Governance** – review scoring monthly, capture overrides, and document rationale.

## Templates
- Signal scoring matrix with thresholds + automation IDs.
- Inspection checklist for reps/managers.
- Alert message template for Slack/email.

## Tips
- Align scoring with enablement frameworks (MEDDIC, SPICED) to drive adoption.
- Expose scores in forecasts so execs can challenge risky commits.
- Pair with `guardrail-scorecard` or pipeline commands to operationalize.

---
