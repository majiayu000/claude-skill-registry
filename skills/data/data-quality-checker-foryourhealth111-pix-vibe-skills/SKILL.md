---
name: data-quality-checker
description: |
  Validate dataset completeness and basic correctness before downstream analysis.
  Use for nulls, duplicates, schema drift, range checks, and column-level sanity reviews; not for anomaly detection or ML evaluation.
allowed-tools: Read, Write, Edit, Bash, Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Data Quality Checker

## Purpose

Use this skill when the user needs to know whether the dataset is trustworthy enough to continue.

## When to Use

Use this skill when:
- Checking null rates, duplicates, invalid categories, or out-of-range values
- Verifying schemas after ETL or data ingestion
- Producing a pre-modeling data sanity checklist

## Not For / Boundaries

- Rare-event or fraud detection: use `anomaly-detector`
- Model metrics and benchmark comparisons: use `evaluating-machine-learning-models`
- Report authoring and presentation polish: use `scientific-reporting`

## Typical Outputs

- Data quality scorecards
- Column-level issue summaries
- Recommended cleaning priorities before modeling or reporting

## Related Skills

- `anomaly-detector` after the basic data checks pass
- `structured-content-storage` if the dataset and outputs need stricter organization
