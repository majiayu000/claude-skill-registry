---
name: skill-forge-benchmark
description: >
  Benchmark Claude Code skill performance with variance analysis, tracking pass
  rate, execution time, and token usage across iterations. Runs multiple trials
  per eval for statistical reliability, aggregates results into benchmark.json,
  and generates comparison reports between skill versions. Use when user says
  "benchmark skill", "measure skill performance", "skill metrics", "compare
  skill versions", "skill performance", "track skill improvement",
  "skill regression test", or "skill A/B test".
---

# Skill Benchmarking & Performance Tracking

Measure and compare skill performance across iterations with statistical
rigor using multiple trials, variance analysis, and trend tracking.

## Process

### Step 1: Define Benchmark Configuration

Accept configuration as:
- **Existing eval set**: Path to `evals/evals.json` (from `/skill-forge eval`)
- **Benchmark config**: Custom config with trial count and thresholds

**Benchmark config schema:**
```json
{
  "skill_name": "my-skill",
  "skill_path": "./my-skill",
  "eval_set_path": "./evals/evals.json",
  "trials_per_eval": 3,
  "baseline_type": "no_skill",
  "previous_benchmark": null,
  "thresholds": {
    "min_pass_rate": 0.8,
    "max_avg_tokens": 100000,
    "max_avg_duration_seconds": 120,
    "min_improvement_ratio": 1.0
  }
}
```

### Step 2: Execute Benchmark Runs

For each eval, run `trials_per_eval` times (default: 3) to get reliable metrics:

1. Execute with-skill runs (3x per eval)
2. Execute baseline runs (3x per eval)
3. Capture per-run: pass/fail, token count, duration
4. Save each run's `timing.json` and `grading.json`

Use `agents/skill-forge-executor.md` for parallel execution where possible.

### Step 3: Aggregate Results

Run `python scripts/aggregate_benchmark.py <workspace>/iteration-<N> --skill-name <name>`:

**Output `benchmark.json` schema:**
```json
{
  "skill_name": "my-skill",
  "iteration": 1,
  "timestamp": "2026-03-06T12:00:00Z",
  "summary": {
    "total_evals": 10,
    "with_skill": {
      "pass_rate": 0.87,
      "pass_rate_std": 0.05,
      "avg_tokens": 45000,
      "avg_duration_seconds": 34.2
    },
    "baseline": {
      "pass_rate": 0.60,
      "pass_rate_std": 0.08,
      "avg_tokens": 62000,
      "avg_duration_seconds": 52.1
    },
    "improvement_ratio": 1.45,
    "token_savings_ratio": 0.73,
    "time_savings_ratio": 0.66
  },
  "per_eval": [
    {
      "eval_id": 0,
      "eval_name": "basic-trigger",
      "with_skill": {"pass_rate": 1.0, "avg_tokens": 30000, "avg_duration_seconds": 20.1},
      "baseline": {"pass_rate": 0.67, "avg_tokens": 50000, "avg_duration_seconds": 45.0},
      "trials": 3
    }
  ],
  "thresholds_met": {
    "min_pass_rate": true,
    "max_avg_tokens": true,
    "max_avg_duration_seconds": true,
    "min_improvement_ratio": true
  }
}
```

### Step 4: Compare with Previous Iterations

If `previous_benchmark` is provided or prior `iteration-<N-1>` exists:

1. Load previous `benchmark.json`
2. Calculate delta per metric:
   - Pass rate change
   - Token usage change
   - Duration change
   - New regressions (evals that passed before but fail now)
   - New improvements (evals that failed before but pass now)

### Step 5: Generate Benchmark Report

```markdown
# Benchmark Report: [skill-name]

## Iteration [N] vs [N-1]

### Summary
| Metric | Current | Previous | Delta | Threshold | Status |
|--------|---------|----------|-------|-----------|--------|
| Pass Rate | 87% | 78% | +9% | >= 80% | PASS |
| Avg Tokens | 45K | 52K | -13% | <= 100K | PASS |
| Avg Time | 34s | 41s | -17% | <= 120s | PASS |
| Improvement | 1.45x | 1.30x | +0.15x | >= 1.0x | PASS |

### Regressions (Action Required)
| Eval | Previous | Current | Notes |
|------|----------|---------|-------|
| eval-5 | PASS | FAIL | Output missing required section |

### Improvements
| Eval | Previous | Current | Notes |
|------|----------|---------|-------|
| eval-3 | FAIL | PASS | Error handling now works |

### Per-Eval Detail
[Full breakdown table]

### Variance Analysis
| Eval | Pass Rate | Std Dev | Trials | Reliability |
|------|-----------|---------|--------|-------------|
| eval-0 | 100% | 0.00 | 3 | High |
| eval-1 | 67% | 0.47 | 3 | Low (investigate) |

### Recommendations
[Based on regressions, low-reliability evals, and threshold failures]
```

### Step 6: Threshold Gating

If any threshold fails:
1. Flag as **FAIL** with specific threshold details
2. List which evals caused the failure
3. Recommend running `/skill-forge evolve` to address issues
4. Do NOT approve for publish until thresholds pass

## Error Handling

- **Flaky trials**: If a trial times out or crashes, exclude it from variance calculation and note `"trials_completed"` vs `"trials_requested"` in per-eval results
- **Insufficient trials**: If fewer than 2 trials complete for an eval, flag variance as `"unreliable"` in the report
- **Missing baseline**: If baseline runs fail entirely, report with-skill results only and skip improvement_ratio
- **Threshold edge cases**: If pass_rate equals the threshold exactly, treat as PASS

## Integration with Other Sub-Skills

- **skill-forge-eval**: Provides the eval set and grading infrastructure
- **skill-forge-evolve**: Receives benchmark failures as improvement targets
- **skill-forge-publish**: Requires benchmark pass (score >= thresholds) before publish
- **skill-forge-review**: Can include benchmark summary in review report
