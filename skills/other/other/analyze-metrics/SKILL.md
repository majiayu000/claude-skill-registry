---
name: analyze-metrics
description: Analyze product metrics and identify trends when the user asks to review metrics, analyze KPIs, or assess product health
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[metric name, period, or metrics file]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: analysis, metrics, data
---

# Analyze Metrics

## Overview

Review product metrics against targets, identify trends across cohorts, distinguish leading from lagging indicators, and generate hypotheses for unexpected changes. Turns raw numbers into actionable insight.

## Workflow

1. **Read metrics context** — Scan `.chalk/docs/product/` for any metrics framework, KPI definitions, or previous metrics reviews. Identify which metrics have defined targets and baselines.

2. **Gather metrics data** — Parse `$ARGUMENTS` for the specific metrics or period to analyze. If the user provides data inline or references a file, read it. If no data is provided, ask the user to supply current metric values.

3. **Classify each metric** — For each metric, determine:
   - Type: leading (predictive) vs. lagging (outcome)
   - Category: acquisition, activation, engagement, retention, revenue, referral
   - Comparison basis: target value, previous period, cohort benchmark

4. **Assess current vs. target** — Compare each metric's current value against its target. Classify as: on-track (within 10%), at-risk (10-25% off), or off-track (>25% off). If no target exists, note the gap.

5. **Identify trends** — For each metric with historical data, classify the trend: improving, stable, or declining. Note acceleration or deceleration (is improvement slowing down?). Flag inflection points.

6. **Cohort comparison** — Where cohort data is available, compare across user segments (new vs. returning, plan tiers, acquisition channels). Identify cohorts that outperform or underperform the average.

7. **Generate hypotheses** — For any metric that is off-track or shows unexpected changes, propose 2-3 hypotheses for the cause. Each hypothesis should be testable. Connect to recent product changes, market events, or seasonal patterns.

8. **Identify metric relationships** — Flag leading indicators that predict lagging indicator changes. Note correlations and potential causal chains.

9. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. Use `highest + 1`.

10. **Write the review** — Save to `.chalk/docs/product/<n>_metrics_review_<period>.md`.

## Output

- **File**: `.chalk/docs/product/<n>_metrics_review_<period>.md`
- **Format**: Markdown with a health dashboard table and detailed metric sections
- **Key sections**: Health Summary Table (metric / current / target / status / trend), Detailed Analysis per metric, Cohort Insights, Hypotheses for Off-Track Metrics, Recommended Actions

## Anti-patterns

- **Vanity metrics without context** — Reporting "10K signups" without conversion rate, activation rate, or retention is misleading. Always pair volume metrics with quality metrics.
- **Confusing correlation with causation** — "We launched feature X and signups went up" is a correlation, not a causal claim. Always note confounders and suggest experiments to validate.
- **Ignoring leading indicators** — Only reviewing lagging indicators (revenue, churn) means you are looking in the rearview mirror. Prioritize leading indicators that let you act before outcomes materialize.
- **Reporting without hypotheses** — Stating "retention dropped 5%" without proposing why is not analysis. Every unexpected change needs at least one testable hypothesis.
- **Missing cohort breakdowns** — Aggregate metrics hide important variation. A stable overall retention rate can mask declining retention in new cohorts offset by strong retention in old cohorts.
