---
name: eval-runner
description: "Run eval scenarios to benchmark Mycelium effectiveness. Execute tasks using reflexion loop, validate against success criteria, record metrics."
---

# Eval Runner

Benchmark the agent's performance against defined scenarios. Adapted from n-trax eval system.

## Commands

### `run <category/name>`
1. Read YAML from `.claude/evals/scenarios/<category>/<name>.yml`
2. Parse fields (name, category, task_prompt, success_criteria, budget)
3. Execute setup steps if defined
4. Record start time
5. Execute task via reflexion workflow (read corrections first)
6. Record end time and iteration count
7. Validate ALL success criteria
8. Write result JSON to `.claude/evals/results/<timestamp>-<name>.json`
9. Report summary

### `run-all [category]`
1. Glob `.claude/evals/scenarios/**/*.yml`
2. For each: run in isolation (git stash), record result, restore
3. Aggregate and report

### `report`
1. Read all results from `.claude/evals/results/`
2. Generate summary table:
```
| Category    | Pass Rate | Avg Iterations | Avg Time | Notes |
|-------------|-----------|----------------|----------|-------|
| discovery   | ...       | ...            | ...      |       |
| delivery    | ...       | ...            | ...      |       |
| integration | ...       | ...            | ...      |       |
| **Overall** | ...       | ...            | ...      |       |
```
3. List failure patterns and recommendations

## Result Format
See `.claude/evals/schema.md` for YAML scenario and JSON result formats.

## Creating Scenarios
Place YAML files in `.claude/evals/scenarios/<category>/`. Define task_prompt, success_criteria, and budget.
