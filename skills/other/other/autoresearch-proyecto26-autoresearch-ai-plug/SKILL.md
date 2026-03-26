---
name: autoresearch
description: >-
  Autonomous experiment loop: edit code, commit, run benchmark, extract metrics,
  keep improvements or revert, repeat forever. Use this skill when the user asks
  to "run autoresearch", "start an experiment loop", "optimize a metric autonomously",
  "autonomous experiments", "autoresearch setup", "benchmark loop",
  "keep/discard experiments", "optimize test speed", "optimize bundle size",
  "optimize build time", "run experiments overnight", "speed up my tests",
  "make my build faster", "reduce compile time", "optimize this automatically",
  "keep trying until it's faster", "run experiments while I sleep",
  "overnight optimization", "edit-measure-keep loop", "cancel autoresearch",
  "stop autoresearch", "autoresearch status", "how many experiments", or mentions
  "autoresearch", "experiment loop", "autonomous optimization".
  Always use this skill when the user wants to iteratively and autonomously
  improve any measurable metric — even if they don't use the word "autoresearch".
  Also use when the user asks about the status of a running autoresearch session
  or wants to cancel/stop one.
version: 0.2.0
argument-hint: "[GOAL] [--max-iterations N]"
---

# Autoresearch: Autonomous Experiment Loop

An autonomous optimization loop where Claude edits code, runs a benchmark, measures a metric, and keeps improvements or reverts — repeating forever until stopped. Inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch) and [pi-autoresearch](https://github.com/davebcn87/pi-autoresearch).

## Core Concept

The loop is simple: **edit → commit → run → measure → keep or discard → repeat**.

- **Primary metric is king.** Lower (or higher, depending on direction) is better. Improved → keep the commit. Equal or worse → `git revert`.
- **State survives context resets** via `autoresearch.jsonl` (append-only log) and `autoresearch.md` (living session document).
- **Domain-agnostic.** Works for any measurable target: test speed, bundle size, LLM training loss, Lighthouse scores, build times, etc.
- **Be careful not to overfit to the benchmarks and do not cheat on the benchmarks.** Optimize the real workload, not the measurement harness.

## Setup Phase

When the user triggers autoresearch, gather the following (ask if not provided):

1. **Goal** — what to optimize (e.g., "reduce unit test runtime")
2. **Command** — the benchmark to run (e.g., `pnpm test`, `uv run train.py`)
3. **Primary metric** — name, unit, and direction (`lower` or `higher` is better)
4. **Secondary metrics** — optional additional metrics to track for tradeoff monitoring (e.g., memory, compile time)
5. **Files in scope** — which files can be modified
6. **Constraints** — time budget, off-limits files, correctness requirements

Optionally check for `.claude/autoresearch-ai-plugin.local.md` in the project root for persistent configuration:

```markdown
---
enabled: true
max_iterations: 50
working_dir: "/path/to/project"
benchmark_timeout: 600
checks_timeout: 300
---

# Autoresearch Configuration

Additional context or notes for this project's autoresearch setup.
```

- `enabled` — whether autoresearch is active (default: true)
- `max_iterations` — stop after N experiments (default: 0 = unlimited)
- `working_dir` — override directory for experiment files (default: current directory)
- `benchmark_timeout` — benchmark timeout in seconds (default: 600)
- `checks_timeout` — correctness checks timeout in seconds (default: 300)

If the file doesn't exist, use defaults. The file should be added to `.gitignore` (`.claude/*.local.md`).

Then execute these setup steps:

1. Create a branch: `git checkout -b autoresearch/<goal>-<date>`
2. Ensure session files are gitignored (critical — `git revert` will fail if `autoresearch.jsonl` is tracked):
   ```bash
   echo -e "autoresearch.jsonl\nrun.log" >> .gitignore
   git add .gitignore && git commit -m "autoresearch: add session files to gitignore"
   ```
3. Read all files in scope thoroughly to understand the codebase
4. Write `autoresearch.md` — the session document (see `examples/autoresearch.md`)
5. Write `autoresearch.sh` — the benchmark script (see `examples/autoresearch.sh`)
6. Optionally write `autoresearch.checks.sh` — correctness checks (tests, lint, types)
7. Commit session files
8. Run baseline: `bash autoresearch.sh`
9. Parse metrics from output (lines matching `METRIC name=value`)
10. Record baseline in `autoresearch.jsonl` (with `"type":"config"` header first, then baseline result)
11. Begin the experiment loop

## The Experiment Loop

**LOOP FOREVER. Never ask "should I continue?" — just keep going.**

The user might be asleep, away from the computer, or expects you to work indefinitely. If each experiment takes ~5 minutes, you can run ~12/hour, ~100 overnight. The loop runs until the user interrupts you, period.

Each iteration:

```
1. Read current git state and autoresearch.md
2. Choose an experimental change (informed by past results and ASI notes)
3. Edit files in scope
4. git add <files> && git commit -m "experiment: <description>"
5. Run: bash autoresearch.sh > run.log 2>&1
6. Parse METRIC lines from output
7. If autoresearch.checks.sh exists, run it (separate timeout, default 300s)
8. Decide: keep or discard
9. Log result to autoresearch.jsonl (include ASI annotations)
10. If discard/crash: git revert $(git rev-parse HEAD) --no-edit
11. Update autoresearch.md with learnings (every few experiments)
12. Repeat
```

### Decision Rules

- **Metric improved** → `keep` (commit stays, branch advances)
- **Metric equal or worse** → `discard` (run `git revert $(git rev-parse HEAD) --no-edit`)
- **Crash or checks failed** → `discard` (revert, note the failure in ASI)
- **Simpler code for equal perf** → `keep` (removing complexity is a win)
- **Catastrophic secondary metric regression** → consider `discard` even if primary improved (e.g., 1% speed gain but 10x memory usage)
- **If stuck** → think deeper, try a different approach. Consult `autoresearch.ideas.md` if it exists. Re-read source files for new angles. Try combining previous near-misses. Try more radical changes. Read any papers or docs referenced in the code.

### Simplicity Criterion

All else being equal, simpler is better. Weigh complexity cost against improvement magnitude:

- A 0.001 improvement that adds 20 lines of hacky code? Probably not worth it.
- A 0.001 improvement from deleting code? Definitely keep.
- Equal performance with much simpler code? Keep.

### Handling User Messages During Experiments

If the user sends a message while the loop is running:
1. Finish the current experiment cycle (don't abandon mid-run)
2. Address the user's feedback or question
3. Resume the loop immediately after — do not wait for permission

### Benchmark Timeout

- Default benchmark timeout: 600 seconds (10 minutes)
- If a run exceeds the timeout, kill it and treat as a crash
- Checks timeout: 300 seconds (5 minutes), separate from benchmark

### Don't Thrash

If 3 consecutive experiments fail or get discarded:
1. Stop and think about why
2. Re-read the source files for new angles
3. Try a fundamentally different approach
4. Consult `autoresearch.ideas.md` for untried ideas

## Metric Output Format

Benchmark scripts output metrics as structured lines:

```
METRIC total_time=4.23
METRIC memory_mb=512
METRIC val_bpb=1.042
```

Parse these with the helper script at `${CLAUDE_SKILL_DIR}/scripts/parse-metrics.sh`:

```bash
bash autoresearch.sh 2>&1 | bash ${CLAUDE_SKILL_DIR}/scripts/parse-metrics.sh
```

### Secondary Metrics

Beyond the primary metric, output additional `METRIC` lines for tradeoff monitoring:

```
METRIC total_ms=4230        # primary
METRIC compile_ms=1200      # secondary — helps identify bottlenecks
METRIC memory_mb=512        # secondary — monitors resource usage
METRIC cache_hit_rate=0.85  # secondary — instrumentation data
```

Secondary metrics are tracked in the JSONL log and help guide future experiments, but they rarely affect keep/discard decisions (only discard if a catastrophic secondary regression accompanies a marginal primary improvement).

**Output instrumentation data** — phase timings, error counts, cache rates, domain-specific signals. This data guides the next iteration and helps identify where optimization effort should focus.

## Actionable Side Information (ASI)

ASI is structured annotation per experiment that **survives reverts**. When code changes are discarded, only the description and ASI remain — making them the only structured memory of what happened.

Record ASI for every experiment:

```json
{
  "hypothesis": "Reducing loop iterations by breaking early",
  "result": "Marginal speedup but code readability suffered",
  "next_action_hint": "Try vectorization instead of loop unrolling",
  "bottleneck": "Memory bandwidth on L2 cache misses"
}
```

ASI fields are free-form — use whatever keys are useful:
- `hypothesis` — what you expected
- `result` — what actually happened
- `next_action_hint` — guidance for the next experiment
- `bottleneck` — identified performance bottleneck
- `error_details` — crash/failure diagnostics
- Any other domain-specific observations

## Logging to autoresearch.jsonl

### Config Header (written once at setup)

```json
{"type":"config","name":"Optimize unit test runtime","metricName":"total_ms","metricUnit":"ms","bestDirection":"lower"}
```

### Experiment Results (appended after each run)

Each experiment appends one JSON line:

```json
{"run":5,"commit":"abc1234","metric":4230,"metrics":{"compile_ms":1200,"memory_mb":512},"status":"keep","description":"parallelized test suites","timestamp":1700000000,"segment":0,"confidence":2.3,"asi":{"hypothesis":"parallel tests reduce wall time","next_action_hint":"try worker pool size tuning"}}
```

Fields:
- `run` — experiment number (1-indexed, sequential)
- `commit` — short git commit hash (7 chars)
- `metric` — primary metric value
- `metrics` — secondary metrics dict (optional)
- `status` — one of: `keep`, `discard`, `crash`, `checks_failed`
- `description` — brief description of what was tried
- `timestamp` — Unix timestamp (seconds)
- `segment` — session segment index (0-based, incremented when optimization target changes)
- `confidence` — MAD-based confidence score (null if < 3 experiments)
- `asi` — Actionable Side Information dict (optional, omit if empty)

Use `${CLAUDE_SKILL_DIR}/scripts/log-experiment.sh` to append entries:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/log-experiment.sh \
  --run 5 \
  --commit "$(git rev-parse --short HEAD)" \
  --metric 4230 \
  --status keep \
  --description "parallelized test suites" \
  --metrics '{"compile_ms":1200,"memory_mb":512}' \
  --segment 0 \
  --confidence 2.3 \
  --asi '{"hypothesis":"parallel tests reduce wall time"}'
```

Valid statuses: `keep`, `discard`, `crash`, `checks_failed`

## Segments (Multi-Phase Sessions)

When the optimization target changes mid-session (different benchmark, metric, or workload):

1. Write a new config header to `autoresearch.jsonl` with the updated target
2. Increment the segment counter
3. Old results stay in the JSONL but are filtered as previous phase
4. Establish a new baseline for the new segment

This allows a single session to evolve — e.g., first optimize compilation speed, then switch to runtime performance.

## Resuming After Context Reset

If `autoresearch.jsonl` and `autoresearch.md` exist in the working directory:

1. Read `autoresearch.md` for full context (goal, metrics, files, constraints, learnings)
2. Read `autoresearch.jsonl` to see all past experiments, current best, and ASI annotations
3. Check `autoresearch.ideas.md` if it exists — prune stale entries, experiment with remaining ideas
4. Check git log to verify current branch state matches expected state
5. Resume the loop from where it left off — no re-setup needed
6. **Resume immediately** — do not ask "should I continue?"

## Confidence Scoring

After 3+ experiments, assess whether improvements are real or noise:

- Compute the **Median Absolute Deviation (MAD)** of all metric values in the current segment as a noise floor
- **Confidence = |best improvement| / MAD**
- ≥2.0× → likely real improvement (green)
- 1.0–2.0× → marginal, could be noise (yellow)
- <1.0× → within noise floor (red) — consider re-running to confirm

Record confidence on each experiment result in the JSONL log. When confidence is low, consider:
- Running the benchmark multiple times inside `autoresearch.sh` and reporting the median
- Pinning CPU frequency or reducing system noise
- Making larger changes that produce clearer signal

See `references/confidence-scoring.md` for detailed methodology.

## Session Files

| File | Purpose | Created by |
|------|---------|------------|
| `autoresearch.md` | Living session document — goal, metrics, scope, learnings | Setup phase |
| `autoresearch.sh` | Benchmark script — outputs `METRIC name=value` lines | Setup phase |
| `autoresearch.checks.sh` | Optional correctness checks (tests, lint, types) | Setup phase |
| `autoresearch.jsonl` | Append-only experiment log (survives restarts) | First experiment |
| `autoresearch.ideas.md` | Optional backlog of ideas to try | Anytime |
| `.claude/autoresearch-ai-plugin.local.md` | Optional persistent configuration (max_iterations, working_dir, timeouts) | User-provided |

## Cancel and Status

### Cancelling an Autoresearch Session

When the user asks to cancel or stop autoresearch:

1. Finish the current experiment cycle if one is running
2. Read `autoresearch.jsonl` to count total experiments and results
3. Report a summary: goal, total runs, kept improvements, best metric
4. Remove `.claude/autoresearch-ai-plugin.local.md` if it exists
5. Do NOT delete `autoresearch.jsonl` or `autoresearch.md` — they contain valuable history
6. Do NOT revert any kept commits — the improvements are real
7. Inform the user they can resume later with `/autoresearch`

### Checking Session Status

When the user asks about autoresearch status or progress:

1. Check if `autoresearch.jsonl` exists — if not, report "No active session"
2. Read `autoresearch.md` for the goal and primary metric
3. Parse `autoresearch.jsonl` to compute: total runs, kept/discarded/crashed counts, baseline vs best, improvement percentage, confidence score
4. Display a formatted summary

## Additional Resources

### Reference Files

- **`references/confidence-scoring.md`** — Detailed MAD-based confidence methodology
- **`references/best-practices.md`** — Tips for writing good benchmarks, choosing experiments, ASI patterns, and avoiding pitfalls

### Example Files

- **`examples/autoresearch.md`** — Example session document template
- **`examples/autoresearch.sh`** — Example benchmark script with METRIC output
- **`examples/autoresearch.checks.sh`** — Example correctness checks script

### Utility Scripts

- **`scripts/parse-metrics.sh`** — Extract METRIC lines from benchmark output
- **`scripts/log-experiment.sh`** — Append an experiment result to autoresearch.jsonl
