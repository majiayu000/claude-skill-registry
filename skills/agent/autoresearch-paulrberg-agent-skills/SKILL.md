---
argument-hint: '<goal>'
name: autoresearch
user-invocable: true
description: This skill should be used when the user asks to "run autoresearch", "optimize X in a loop", "set up autonomous experiments", "start autoresearch", "optimize X overnight", or "experiment loop". Sets up and runs an autonomous experiment loop for any optimization target.
---

# Autoresearch

Autonomous experiment loop: try ideas, measure results, keep what works, discard what doesn't, never stop.

Works for any optimization target: test speed, bundle size, LLM training, build times, Lighthouse scores, binary size, latency, memory usage.

## Setup

If `autoresearch.md` already exists in the working directory, **skip setup and resume the loop** — read `autoresearch.md`, `autoresearch.jsonl`, and `git log`, then continue experimenting.

Otherwise:

1. **Gather context**: Ask (or infer from `$ARGUMENTS` and conversation) the **Goal**, **Command** to benchmark, **Primary metric** (name + direction), **Files in scope**, and **Constraints**.
2. **Create branch**: `git checkout -b autoresearch/<goal>-<date>` (e.g. `autoresearch/test-speed-2026-03-21`).
3. **Read source files**: Understand the workload deeply before writing anything. Read every file in scope.
4. **Write session files**: Create `autoresearch.md` and `autoresearch.sh` (see templates below). If constraints require correctness validation (tests must pass, types must check), also create `autoresearch.checks.sh`. Commit all.
5. **Run baseline**: Execute the first experiment with no changes to establish the baseline metric.
6. **Start looping**: Begin the experiment loop immediately after the baseline is logged.

### `autoresearch.md`

The heart of the session. A fresh agent with no context should be able to read this file alone and run the loop effectively. Invest time making it excellent.

```markdown
# Autoresearch: <goal>

## Objective
<Specific description of what we're optimizing and the workload.>

## Metrics
- **Primary**: <name> (<unit>, lower/higher is better)
- **Secondary**: <name>, <name>, ...

## How to Run
`./autoresearch.sh` — outputs `METRIC name=value` lines.

## Files in Scope
<Every file the agent may modify, with a brief note on what it does.>

## Off Limits
<What must NOT be touched — evaluation harness, data prep, etc.>

## Constraints
<Hard rules: tests must pass, no new deps, fixed time budget, etc.>

## What's Been Tried
<Update this section as experiments accumulate. Note key wins, dead ends,
and architectural insights so the agent doesn't repeat failed approaches.>
```

Update `autoresearch.md` periodically — especially "What's Been Tried" — so resuming agents have full context.

### `autoresearch.sh`

Bash script that runs the benchmark and outputs structured metrics.

```bash
#!/bin/bash
set -euo pipefail

# Pre-checks (fast, <1s — catch syntax errors early)
python3 -c "import ast; ast.parse(open('train.py').read())"

# Run benchmark
uv run train.py > /tmp/autoresearch-output.log 2>&1

# Extract and output metrics as METRIC lines
val_bpb=$(grep "^val_bpb:" /tmp/autoresearch-output.log | awk '{print $2}')
echo "METRIC val_bpb=$val_bpb"
```

Rules:
- Use `set -euo pipefail`.
- Output `METRIC name=value` lines to stdout (one per metric). The primary metric name must match what's documented in `autoresearch.md`.
- Metric names: word chars, dots, or `µ` (e.g. `val_bpb`, `total_µs`, `bundle.size_kb`).
- Keep the script fast — every second is multiplied by hundreds of runs.
- For fast/noisy benchmarks (<5s), run multiple times inside the script and report the median.
- Update the script during the loop as needed.

### `autoresearch.checks.sh` (optional)

Backpressure checks: tests, types, lint. **Only create when constraints require correctness validation.**

```bash
#!/bin/bash
set -euo pipefail
pnpm test --run --reporter=dot 2>&1 | tail -50
pnpm typecheck 2>&1 | grep -i error || true
```

When this file exists:
- Run it after every **passing** benchmark (exit 0).
- If checks fail, log the experiment as `checks_failed` and revert.
- Check execution time does NOT affect the primary metric.
- Keep output minimal — suppress verbose progress, only show errors.

When this file does not exist, skip checks entirely.

## The Experiment Loop

**LOOP FOREVER.** Never ask "should I continue?" — the user expects autonomous work.

Each iteration:

1. **Formulate hypothesis**: Based on prior results, source code understanding, and any ideas in `autoresearch.ideas.md`, choose what to try next.
2. **Edit code**: Modify the in-scope files. Make a single, focused change per experiment.
3. **Commit**: `git add -A && git commit -m "<short description of what this experiment tries>"`
4. **Run benchmark**:
   ```bash
   timeout 600 ./autoresearch.sh > run.log 2>&1
   ```
   If the command times out or crashes, treat it as a failure.
5. **Parse metrics**: Extract `METRIC` lines from the output:
   ```bash
   grep '^METRIC ' run.log
   ```
   If no METRIC lines found, the run crashed — read `tail -50 run.log` for the error.
6. **Run checks** (if `autoresearch.checks.sh` exists and benchmark passed):
   ```bash
   timeout 300 ./autoresearch.checks.sh > checks.log 2>&1
   ```
7. **Evaluate and log**:
   - **Improved** (primary metric better than best so far) → status `keep`. The commit stays.
   - **Worse or equal** → status `discard`. Revert: stage autoresearch files first, then reset.
   - **Crash** (benchmark failed) → status `crash`. Fix if trivial, otherwise revert and move on.
   - **Checks failed** → status `checks_failed`. Revert.
8. **Log to JSONL**: Append one line to `autoresearch.jsonl`:
   ```json
   {"run":1,"commit":"a1b2c3d","metric":0.9979,"metrics":{"val_bpb":0.9979,"peak_vram_mb":45060.2},"status":"keep","description":"baseline","timestamp":1711036800000,"confidence":null}
   ```
9. **On discard/crash/checks_failed — revert code changes**:
   ```bash
   # Preserve autoresearch session files, revert everything else
   git add autoresearch.jsonl autoresearch.md autoresearch.sh autoresearch.ideas.md autoresearch.checks.sh 2>/dev/null || true
   git checkout -- .
   git clean -fd
   ```
10. **Check confidence**: After 3+ runs, run the confidence script from the skill's installation directory:
    ```bash
    bash "$(dirname "$(readlink -f "$0")")/scripts/confidence.sh"
    ```
    Or locate it via the skill path and run it directly. Interpret the score:
    - **>= 2.0x**: Improvement is likely real (green).
    - **1.0-2.0x**: Above noise but marginal (yellow).
    - **< 1.0x**: Within noise — consider re-running to confirm (red).
11. **Update session**: Periodically update `autoresearch.md` "What's Been Tried" section and run the summary script to review progress.

Repeat forever until interrupted.

## JSONL Schema

Each line in `autoresearch.jsonl` is a JSON object:

| Field | Type | Description |
|-------|------|-------------|
| `run` | number | 1-indexed experiment count |
| `commit` | string | Short git SHA (7 chars) |
| `metric` | number | Primary metric value |
| `metrics` | object | All metrics dict (primary + secondary) |
| `status` | string | `keep`, `discard`, `crash`, or `checks_failed` |
| `description` | string | What this experiment tried |
| `timestamp` | number | Unix timestamp (ms) |
| `confidence` | number or null | MAD-based confidence score (null if <3 runs) |

## Resuming

When `autoresearch.md` exists in the working directory:

1. Read `autoresearch.md` for full context (objective, what's been tried, constraints).
2. Read `autoresearch.jsonl` to reconstruct state (best metric, run count, last segment).
3. Read `git log --oneline -20` for recent commit history.
4. Check `autoresearch.ideas.md` if it exists — prune stale entries, experiment with promising ones.
5. Continue the loop from where it left off. Do not re-run the baseline.

## Ideas Backlog

When you discover complex but promising optimizations you won't pursue right now, append them as bullets to `autoresearch.ideas.md`. Don't let good ideas get lost.

On resume, check this file — prune stale/tried entries, experiment with the rest. When all paths are exhausted, delete the file and write a final summary to `autoresearch.md`.

## Loop Rules

See `references/loop-rules.md` for the full reference. Key rules:

- **Primary metric is king.** Improved → keep. Worse/equal → discard.
- **Simpler is better.** Remove code for equal perf = keep. Ugly complexity for tiny gain = discard.
- **Don't thrash.** Repeatedly reverting the same idea? Try something structurally different.
- **Think longer when stuck.** Re-read source files, reason about what the CPU/compiler/runtime is actually doing. Deep understanding beats random variation.
- **Crashes**: fix if trivial (typo, missing import), otherwise log and move on. Don't over-invest.
- **NEVER STOP.** The user may be away for hours. Keep going until interrupted.

## User Messages During Experiments

If the user sends a message while an experiment is running, finish the current run-evaluate-log cycle first, then incorporate their feedback in the next iteration.
