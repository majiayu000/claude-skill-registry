---
name: experiment-loop
description: Autonomous experiment loop - modify code, measure, keep/discard, iterate until target met
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
keywords: [experiment, optimize, iterate, measure, benchmark, performance, loop, autonomous]
---

# Experiment Loop

Autonomous optimization loop: modify code, run measurement, evaluate results, keep improvements, discard regressions. Inspired by the 3-file principle: fixed measurement + mutable code + human instructions.

## Concept

```
┌─────────────────────────────────────────┐
│  INSTRUCTIONS (fixed)                    │
│  "Optimize X to achieve Y metric"        │
└──────────────┬──────────────────────────┘
               │
               v
┌──────────────────────────────┐
│  MEASURE (fixed)              │ ◄── Never changes during loop
│  benchmark.sh / test suite    │
└──────────────┬───────────────┘
               │
               v
┌──────────────────────────────┐
│  CODE (mutable)               │ ◄── Agent modifies this
│  src/target-module.ts         │
└──────────────┬───────────────┘
               │
               v
┌──────────────────────────────┐
│  EVALUATE                     │
│  Better? → KEEP + next iter   │
│  Worse?  → REVERT + try alt   │
│  Target met? → DONE           │
└──────────────────────────────┘
```

## Usage

```
/experiment-loop --target "response time < 100ms" --measure "npm run benchmark" --file src/api/handler.ts
```

## Parameters

| Param | Required | Description |
|-------|----------|-------------|
| `--target` | Yes | Success criteria (quantitative) |
| `--measure` | Yes | Command to run measurement |
| `--file` | Yes | File(s) to optimize |
| `--max-iterations` | No | Max attempts (default: 10) |
| `--baseline` | No | Run baseline measurement first (default: true) |

## Workflow

### Step 1: Baseline
```
1. Run measurement command
2. Record baseline metrics
3. Save current code state (git stash or copy)
```

### Step 2: Hypothesize
```
1. Analyze current code
2. Identify optimization opportunity
3. Predict expected improvement
```

### Step 3: Modify
```
1. Make ONE focused change
2. Keep change small and reversible
3. Document what was changed and why
```

### Step 4: Measure
```
1. Run same measurement command
2. Record new metrics
3. Compare against baseline AND previous best
```

### Step 5: Evaluate
```
IF metrics improved:
  → KEEP change
  → Update "current best" baseline
  → Log: "Iteration N: +X% improvement from [change description]"

IF metrics worsened or unchanged:
  → REVERT change
  → Log: "Iteration N: [change description] did not improve, reverted"
  → Try different approach

IF target met:
  → DONE
  → Generate summary report
```

### Step 6: Iterate or Stop
```
IF target met → Report success
IF max_iterations reached → Report best achieved
IF no improvement for 3 consecutive iterations → Report plateau
```

## Output

```markdown
# Experiment Report: [Target]
Date: [timestamp]
Iterations: [N]
Status: TARGET MET / PLATEAU / MAX ITERATIONS

## Baseline
[Initial measurement results]

## Best Result
[Best measurement achieved]
Improvement: [X% over baseline]

## Iteration Log
| # | Change | Result | Delta | Keep? |
|---|--------|--------|-------|-------|
| 1 | [desc] | [metric] | +X% | Yes |
| 2 | [desc] | [metric] | -Y% | No |

## Final Code State
[What changes were kept]

## Learnings
- [What worked]
- [What didn't work]
- [Suggestions for further optimization]
```

## Best For

| Agent | Use Case |
|-------|----------|
| nitro | Performance optimization loops |
| profiler | Memory/CPU optimization |
| backend-dev | API response time optimization |
| frontend-dev | Bundle size / render time optimization |
| ai-engineer | Prompt optimization loops |

## Rules

- ONE change per iteration (isolate variables)
- ALWAYS measure before and after
- ALWAYS revert failed changes
- Max 10 iterations default (prevent infinite loops)
- Report progress every 3 iterations
- Stop if 3 consecutive non-improvements (plateau detection)
