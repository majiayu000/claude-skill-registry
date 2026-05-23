---
name: benchmark-models
description: Standardized compliance QRA benchmarks against candidate LLMs
triggers:
  - "benchmark models"
  - "model comparison"
  - "llm benchmark"
allowed-tools:
  - Bash
provides:
  - benchmark-models
composes:
  - scillm
  - create-figure
  - task-monitor
---

# benchmark-models

Run standardized compliance QRA tests against candidate LLMs to evaluate accuracy, latency, and cost before deploying to the inference pipeline.

## Usage

### Run a single-model benchmark

```bash
./run.sh run --model deepseek-v3 --suite compliance-basic
```

Runs 20 gold-set compliance QRA questions against the specified model via `/scillm`. Outputs a results table with TEST_CASE, EXPECTED, ACTUAL, MATCH, and LATENCY_MS columns, plus summary metrics (accuracy%, latency_p50, latency_p95, estimated_token_cost).

### Compare multiple models

```bash
./run.sh compare --models "deepseek-v3,llama-3.1-70b" --suite compliance-basic
```

Runs the benchmark for each model and outputs a side-by-side comparison table.

### View last report

```bash
./run.sh report
```

Reads the most recent benchmark results from `~/.embry/benchmark_results.json` and renders a summary.

### Dry run (no LLM calls)

```bash
./run.sh run --model deepseek-v3 --suite compliance-basic --dry-run
./run.sh compare --models "deepseek-v3,llama-3.1-70b" --dry-run
```

Outputs the full benchmark scaffold with 20 test cases and mock results. No LLM calls are made.

## Suites

- **compliance-basic**: 20 gold-set QRA questions covering NIST 800-171, AS9100D, CMMC, ITAR, DFARS, DO-178C, MIL-STD, and cross-program compliance drift detection.

## Output

Results are saved to `~/.embry/benchmark_results.json` and printed to stdout. The report includes per-question accuracy and aggregate metrics for model selection decisions.
