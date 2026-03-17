---
name: ml-experiment-tracker
description: Plan reproducible ML experiment runs with explicit parameters, metrics, and artifacts. Use before model training to standardize tracking-ready experiment definitions.
---

# ML Experiment Tracker

## Overview

Generate structured experiment plans that can be logged consistently in experiment tracking systems.

## Workflow

1. Define dataset, target task, model family, and parameter search space.
2. Define metrics and acceptance thresholds before training.
3. Produce run plan with version and artifact expectations.
4. Export the run plan for execution in tracking tools.

## Use Bundled Resources

- Run `scripts/build_experiment_plan.py` to generate consistent run plans.
- Read `references/tracking-guide.md` for reproducibility checklist.

## Guardrails

- Keep inputs explicit and machine-readable.
- Always include metrics and baseline criteria.
