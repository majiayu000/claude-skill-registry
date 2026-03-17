---
name: ml-model-eval-benchmark
description: Compare model candidates using weighted metrics and deterministic ranking outputs. Use for benchmark leaderboards and model promotion decisions.
---

# ML Model Eval Benchmark

## Overview

Produce consistent model ranking outputs from metric-weighted evaluation inputs.

## Workflow

1. Define metric weights and accepted metric ranges.
2. Ingest model metrics for each candidate.
3. Compute weighted score and ranking.
4. Export leaderboard and promotion recommendation.

## Use Bundled Resources

- Run `scripts/benchmark_models.py` to generate benchmark outputs.
- Read `references/benchmarking-guide.md` for weighting and tie-break guidance.

## Guardrails

- Keep metric names and scales consistent across candidates.
- Record weighting assumptions in the output.
