---
name: confusion-matrix-generator
description: |
  Inspect classifier errors with confusion matrices after predictions already exist.
  Use for per-class error analysis, threshold tradeoffs, and label-confusion diagnosis; not for regression metrics or full model training ownership.
allowed-tools: Read, Write, Edit, Bash(python:*), Bash(pip:*)
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Confusion Matrix Generator

## Purpose

Use this skill when the user already has classification outputs and needs to understand where the model is getting confused.

## When to Use

Use this skill when:
- Breaking down false positives and false negatives by class
- Comparing thresholds or class weights for a classification model
- Explaining which classes are systematically confused with one another

## Not For / Boundaries

- Regression evaluation: use `evaluating-machine-learning-models`
- Leakage audits: use `ml-data-leakage-guard`
- End-to-end training runs: use `training-machine-learning-models`

## Typical Outputs

- Confusion matrix tables or heatmaps
- Per-class precision/recall breakdowns
- Actionable notes on thresholding, relabeling, or class balancing

## Related Skills

- `evaluating-machine-learning-models` for the broader metric suite
- `feature-importance-analyzer` when the next question is why a class fails
