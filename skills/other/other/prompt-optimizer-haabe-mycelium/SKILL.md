---
name: prompt-optimizer
description: "A/B test CLAUDE.md instruction changes against eval benchmarks. Capture baselines, test variants, compare results."
---

# Prompt Optimizer

Systematically improve Mycelium instructions through measurement. Adapted from n-trax.

## Commands

### `baseline` -- Capture current performance
1. Run `/eval-runner run-all`
2. Record to `.claude/optimization/baseline.json`: timestamp, CLAUDE.md hash, overall and per-category metrics (pass_rate, avg_iterations, avg_time)

### `test <variant>` -- Test a variant
1. Read variant from `.claude/optimization/variants/<variant>.md`
2. Apply the CLAUDE.md changes described
3. Run `/eval-runner run-all`
4. Store results in `.claude/optimization/results/<variant>.json`
5. Compare against baseline
6. Do NOT auto-revert -- let user decide

### `report` -- Compare all variants
Generate comparison table: variant, pass rate, delta vs baseline, avg iterations, decision (keep/revert).

### `exemplar <eval-name>` -- Capture winning trajectory
After a clean eval win (1 iteration, fast), save the approach to `.claude/optimization/exemplars/`.

## Workflow
1. Capture baseline
2. Hypothesize an instruction improvement
3. Document in variants/ directory
4. Test the variant
5. Compare via report
6. Keep or revert based on data
7. Capture exemplars from clean wins
