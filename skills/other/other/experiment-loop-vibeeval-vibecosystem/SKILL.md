---
name: experiment-loop
description: "Autonomous experiment loop: hypothesize > modify > test > evaluate > keep/discard > repeat. Run N experiments automatically with measurable metrics. Works for performance optimization, A/B testing, prompt engineering, and any measurable improvement task."
---

# Experiment Loop

Autonomous, iterative improvement inspired by Karpathy's autoresearch methodology. Define a metric, set a target, and let the loop run until the target is met or the iteration limit is reached.

## The 5-Step Loop

```
1. HYPOTHESIZE  -> Form a specific, falsifiable improvement hypothesis
2. MODIFY       -> Apply the minimal code/config/prompt change
3. TEST         -> Run the measurement suite (benchmarks, tests, evals)
4. EVALUATE     -> Compare result against baseline and previous best
5. DECIDE       -> KEEP if better, DISCARD (git stash pop --index) if worse
      |
   Repeat until target met OR max_iterations reached
```

Each iteration is atomic: one hypothesis, one change, one measurement, one decision.

## Experiment Definition

Define an experiment in your task or in `thoughts/EXPERIMENTS.md`:

```yaml
experiment:
  name: "reduce-api-latency"
  metric: "p95 response time (ms)"
  baseline: 340
  target: 200
  direction: minimize          # minimize | maximize
  max_iterations: 10           # hard cap, never exceed
  measurement_cmd: "npm run bench:api"
  measurement_key: "p95"       # JSON key from bench output
  scope: "src/api/"            # files the loop is allowed to touch
```

### Key Fields

| Field | Description |
|-------|-------------|
| `metric` | Human-readable name of what you are measuring |
| `baseline` | Measured value before any changes (run this first) |
| `target` | Success condition -- loop exits when this is met |
| `direction` | `minimize` for latency/size, `maximize` for coverage/score |
| `max_iterations` | Safety cap, default 10, absolute maximum 10 |
| `measurement_cmd` | Shell command that produces JSON with the metric value |
| `scope` | Directories/files the loop is allowed to modify |

## Safety Protocol

Before every experiment iteration:

```bash
# Save current state
git stash push -u -m "experiment-loop: iteration N baseline"

# Run experiment
# ... apply hypothesis change ...
# ... run measurement ...

# Decision
if result is better:
    git stash drop          # keep changes, discard stash
else:
    git stash pop --index   # restore exactly: staged + unstaged
```

Never skip the stash. Never accumulate multiple iterations without a decision checkpoint. If the measurement command fails or times out, treat it as DISCARD.

## Agent Integration

The experiment loop coordinates three vibecosystem agents:

| Phase | Agent | Role |
|-------|-------|------|
| Hypothesize | `profiler` | Identify bottlenecks, suggest what to change |
| Modify | `spark` | Apply the focused code change |
| Test + Evaluate | `verifier` / `tdd-guide` | Run benchmarks, tests, evals and parse results |

Spawn `profiler` once at the start to get the initial hypothesis queue. Then run `spark` + `verifier` in tight loops per iteration.

## Example Experiments

### Bundle Size Reduction

```yaml
experiment:
  name: "optimize-bundle-size"
  metric: "gzipped bundle size (KB)"
  baseline: 420
  target: 300
  direction: minimize
  max_iterations: 10
  measurement_cmd: "npm run build && node scripts/measure-bundle.js"
  measurement_key: "gzipped_kb"
  scope: "src/"
```

Hypothesis queue to try in order:
1. Add tree-shaking for unused lodash imports (use named imports)
2. Replace `moment` with `date-fns` (smaller footprint)
3. Move large dependencies to dynamic `import()` at route boundaries
4. Enable `usedExports: true` in webpack/rollup config
5. Replace `axios` with native `fetch` wrapper

### API Latency

```yaml
experiment:
  name: "reduce-api-latency"
  metric: "p95 response time (ms)"
  baseline: 340
  target: 200
  direction: minimize
  max_iterations: 8
  measurement_cmd: "npm run bench:api"
  measurement_key: "p95"
  scope: "src/api/"
```

Hypothesis queue:
1. Add Redis cache for repeated DB reads (TTL 60s)
2. Replace N+1 queries with single JOIN query
3. Add connection pool sizing (`max: 20`)
4. Move synchronous validation to async parallel (`Promise.all`)
5. Add response compression (gzip middleware)

### Test Coverage

```yaml
experiment:
  name: "improve-test-coverage"
  metric: "line coverage (%)"
  baseline: 64
  target: 80
  direction: maximize
  max_iterations: 10
  measurement_cmd: "npm test -- --coverage --json > coverage.json"
  measurement_key: "coverageMap.total.lines.pct"
  scope: "src/"
```

### Prompt Engineering (LLM Eval)

```yaml
experiment:
  name: "improve-extraction-accuracy"
  metric: "extraction F1 score"
  baseline: 0.71
  target: 0.85
  direction: maximize
  max_iterations: 10
  measurement_cmd: "python eval/run_evals.py --output eval/results.json"
  measurement_key: "f1"
  scope: "prompts/"
```

## Results Log Format

Append each iteration result to `thoughts/EXPERIMENTS.md`:

```markdown
## Experiment: reduce-api-latency
Started: 2026-04-07T10:00:00Z
Baseline: 340ms | Target: 200ms | Direction: minimize

### Iteration 1
- Hypothesis: Add Redis cache for repeated DB reads
- Change: `src/api/users.ts` lines 45-67 -- wrap DB call with cache layer
- Result: 280ms (improvement: -60ms, -17.6%)
- Decision: KEEP
- Cumulative best: 280ms

### Iteration 2
- Hypothesis: Replace N+1 queries with JOIN
- Change: `src/api/users.ts` lines 89-102 -- rewrite fetchWithPosts()
- Result: 210ms (improvement: -70ms, -25%)
- Decision: KEEP
- Cumulative best: 210ms

### Iteration 3
- Hypothesis: Add connection pool sizing max:20
- Change: `src/db/pool.ts` line 12 -- max: 10 -> 20
- Result: 215ms (regression: +5ms)
- Decision: DISCARD (restored via git stash pop)
- Cumulative best: 210ms

### Final Result
- Target: 200ms | Achieved: 210ms | Status: NEAR_MISS (within 5%)
- Iterations: 3 of 10 used
- Total improvement: -38% from baseline
```

## Iteration Limits and Exit Conditions

| Condition | Action |
|-----------|--------|
| Target met | EXIT -- log SUCCESS, keep all accumulated changes |
| max_iterations reached | EXIT -- log PARTIAL, keep best achieved state |
| 3 consecutive DISCARDs | PAUSE -- re-run profiler for new hypothesis queue |
| Measurement command fails | DISCARD current iteration, continue loop |
| Git stash fails | STOP -- do not continue, report error |

## Running the Loop

Invoke this skill by describing the experiment:

```
Use experiment-loop to reduce the API p95 latency from 340ms to under 200ms.
Baseline measurement: npm run bench:api
Max iterations: 8
Scope: src/api/
```

The loop will:
1. Read any existing `thoughts/EXPERIMENTS.md` for prior runs on the same metric
2. Ask `profiler` for an ordered hypothesis queue
3. Execute iterations with safety stashing
4. Log each result immediately after measurement
5. Report final state with all changes that were kept

## Hard Limits

- Maximum 10 experiments per invocation (no exceptions)
- Scope must be specified -- loop will not touch files outside scope
- Measurement command must be deterministic (no unbounded network calls)
- Total wall-clock time cap: 30 minutes (prevents runaway loops)
- Never auto-merge to main -- changes stay on current branch
