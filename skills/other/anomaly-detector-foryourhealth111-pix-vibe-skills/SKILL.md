---
name: anomaly-detector
description: |
  Detect outliers, spikes, rare events, and abnormal records in tabular or time-series data.
  Use when the task is anomaly detection or suspicious-pattern review, not generic data-quality linting or full ML pipeline ownership.
allowed-tools: Read, Write, Edit, Bash, Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Anomaly Detector

## Purpose

Use this skill when the user needs to identify abnormal rows, drift, spikes, or rare-event behavior in data.

## When to Use

Use this skill when:
- Investigating outlier transactions, sensor spikes, fraud candidates, or rare failures
- Comparing statistical, distance-based, or density-based anomaly detection approaches
- Setting anomaly thresholds and reviewing false positives or false negatives

## Not For / Boundaries

- Generic schema/null/range validation: use `data-quality-checker`
- Publication-grade figure polishing: use `scientific-visualization`
- End-to-end supervised model training: use `training-machine-learning-models`

## Typical Outputs

- Candidate anomaly rules or model choices
- Thresholding and review workflow
- Follow-up plots or tables showing suspicious records

## Related Skills

- `data-quality-checker` for dataset sanity checks before anomaly review
- `creating-data-visualizations` for general charts after anomalies are identified
