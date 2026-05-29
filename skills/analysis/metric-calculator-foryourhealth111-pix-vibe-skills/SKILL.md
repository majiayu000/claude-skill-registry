---
name: metric-calculator
description: |
  Compute well-defined metrics from existing formulas, datasets, or test outputs.
  Use as an explicit/manual helper when the metric definition is already known, not for choosing the overall analysis owner or dashboard strategy.
allowed-tools: Read, Write, Edit, Bash, Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Metric Calculator

## Positioning

Treat this skill as an explicit/manual helper for narrow metric-computation work.

## When to Use

Use this skill when:
- Calculating a named business, statistical, or QA metric from available data
- Converting raw counts into rates, ratios, deltas, or scorecards
- Verifying that a metric formula is implemented consistently across outputs

## Not For / Boundaries

- Model evaluation strategy selection: use `evaluating-machine-learning-models`
- Full regression or causal analysis ownership: use `performing-regression-analysis`
- Chart design or presentation decisions: use `creating-data-visualizations`

## Typical Outputs

- Metric definitions and formulas
- Reproducible calculation steps
- Sanity checks for units, denominators, and aggregation scope

## Related Skills

- `evaluating-machine-learning-models` for ML benchmark metrics
- `creating-data-visualizations` after the numbers are finalized
