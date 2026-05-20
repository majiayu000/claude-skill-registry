---
name: splitting-datasets
description: |
  Split datasets into training, validation, and test partitions with the right stratification and temporal rules.
  Use as a narrow preprocessing helper once the broader ML workflow is already chosen, not as the main route owner for an end-to-end ML task.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(cmd:*)
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---
# Dataset Splitter

## Positioning

Treat this skill as a narrow helper for partition strategy.

## When to Use

Use this skill when:
- Prepare a dataset for machine learning model training.
- Create training, validation, and testing sets.
- Partition data to evaluate model performance.

## Not For / Boundaries

- Full preprocessing-pipeline ownership: use `preprocessing-data-with-automated-pipelines`
- Leakage audits and prediction-time checks: use `ml-data-leakage-guard`
- Model training and tuning after the split: use `training-machine-learning-models`

## Typical Outputs

- Partition strategy with ratios, random seeds, and stratification rules
- Notes on temporal or grouped split constraints
- Handoff guidance for leakage review and downstream training

## Related Skills

- `preprocessing-data-with-automated-pipelines` for the broader preprocessing sequence
- `ml-data-leakage-guard` to verify the split does not leak future or test information
