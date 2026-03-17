---
name: optimization.metric_review
phase: optimization
roles:
  - Product Manager
  - Analytics Lead
description: Conduct a metric review that contextualizes performance trends, flags anomalies, and recommends actions.
variables:
  required:
    - name: goal_metric
      description: Primary metric being evaluated.
    - name: period
      description: Time period (e.g., Q3 2024, last 14 days).
  optional:
    - name: comparison_period
      description: Baseline period for comparison.
    - name: segments
      description: Segments to slice the metric by.
outputs:
  - Trend analysis with visualizations and key drivers.
  - Anomaly detection summary with hypotheses.
  - Recommended actions and owners.
---

# Purpose
Support continuous optimization by providing a structured prompt for reviewing performance data and identifying next steps.

# Pre-run Checklist
- ✅ Export relevant metric data (CSV or dashboard snapshots).
- ✅ Align on segments and filters to analyze.
- ✅ Confirm data freshness and quality.

# Invocation Guidance
```bash
codex run --skill optimization.metric_review \
  --input data/{{goal_metric}}-{{period}}.csv \
  --vars "goal_metric={{goal_metric}}" \
         "period={{period}}" \
         "comparison_period={{comparison_period}}" \
         "segments={{segments}}"
```

# Recommended Input Attachments
- CSV exports or BI dashboard screenshots.
- Notes from recent experiments or launches impacting the metric.

# Claude Workflow Outline
1. Summarize the goal metric, period, and comparison baseline.
2. Provide visual or tabular trend analysis highlighting significant movements.
3. Identify anomalies or inflections, offering hypotheses tied to events or segments.
4. Recommend actions, owners, and expected impact.
5. List questions or data gaps to investigate further.

# Output Template
```
## Metric Review — {{goal_metric}} ({{period}})

### Performance Summary
- Trend Overview:
- % Change vs {{comparison_period}}:

### Segment Analysis
| Segment | Current Value | Δ vs Baseline | Notable Insight |
| --- | --- | --- | --- |

### Anomalies & Hypotheses
1. Observation — Hypothesis — Supporting Evidence

### Recommended Actions
| Action | Owner | Timeline | Expected Impact |
| --- | --- | --- | --- |

### Follow-up Questions
- ...
```

# Follow-up Actions
- Align on prioritized actions during weekly business reviews.
- File tickets or tasks for high-impact recommendations.
- Schedule the next review cadence.
