---
name: research
description: Autonomous goal-directed iteration loop. Define goal + metric + guard, iterate with specialist agents (perf-optimizer, sw-engineer, ai-researcher) until metric improves or limit reached. Supports GPU workloads via Colab MCP and team mode for parallel strategy exploration.
argument-hint: '[plan|resume] <goal description> [--team] [--colab]'
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent, TaskCreate, TaskUpdate, WebFetch
---

<objective>

Autonomously improve a measurable metric through iterative, atomic code changes. Each iteration follows a fixed loop: Review → Ideate (specialist agent) → Modify (ONE change) → Commit (before verify) → Verify (metric) → Guard (regression check) → Decide (keep/revert) → Log (JSONL).

Unlike `/optimize` (single-pass profiling) or `/develop` (feature/fix/refactor), `/research` runs sustained improvement campaigns with automatic rollback and logged experiment history. It is the right tool when you want the system to autonomously explore many code changes toward a measurable goal — coverage targets, accuracy improvements, latency reductions — over many iterations.

</objective>

<inputs>

- `plan <goal>` — interactive wizard: scan codebase, present proposed config, write to state file
- `<goal>` — run the iteration loop directly (uses existing config or auto-detects)
- `resume [run-id]` — resume a previous run from saved state
- `--team` flag — parallel strategy exploration: 2-3 teammates each own a different optimization axis
- `--colab` flag — route metric verification through a Colab MCP GPU runtime

</inputs>

<constants>

```
MAX_ITERATIONS:             20 (ceiling: 50 — never exceed without explicit user override)
STUCK_THRESHOLD:            5 consecutive discards → escalation
GUARD_REWORK_MAX:           2 attempts before revert
VERIFY_TIMEOUT_SEC:         120 (local), 300 (--colab)
SUMMARY_INTERVAL:           10 iterations
DIMINISHING_RETURNS_WINDOW: 5 iterations < 0.5% each → warn user and suggest stopping
STATE_DIR:                  .claude/state/research/
```

**Agent strategy mapping** (`agent_strategy` in config → ideation agent to spawn):

| `agent_strategy` | Specialist agent     | When to use                                  |
| ---------------- | -------------------- | -------------------------------------------- |
| `auto`           | heuristic            | Default — infer from metric_cmd keywords     |
| `perf`           | `perf-optimizer`     | latency, throughput, memory, GPU utilization |
| `code`           | `sw-engineer`        | coverage, complexity, lines, coupling        |
| `ml`             | `ai-researcher`      | accuracy, loss, F1, AUC, BLEU                |
| `arch`           | `solution-architect` | coupling, cohesion, modularity metrics       |

**Auto-inference keyword heuristics** (applied when `agent_strategy: auto`):

- metric_cmd contains `pytest`, `coverage`, `complexity` → `code` → `sw-engineer`
- metric_cmd contains `time`, `latency`, `bench`, `throughput`, `memory` → `perf` → `perf-optimizer`
- metric_cmd contains `accuracy`, `loss`, `f1`, `auc`, `train`, `val`, `eval` → `ml` → `ai-researcher`

**Stuck escalation sequence** (at STUCK_THRESHOLD consecutive discards):

1. Switch to a different agent type (rotate through: `code` → `ml` → `perf`)
2. Spawn 2 agents in parallel with competing strategies; keep whichever improves metric
3. Stop, report progress, surface to user — do not continue looping blindly

</constants>

<workflow>

**Task tracking**: per CLAUDE.md, create TaskCreate entries for all known steps immediately at skill start. In plan mode, create P1/P2/P3. In default/resume mode, create steps 1-7. Mark in_progress when starting each step, completed when done. Keep statuses current — the task list is the user's live feed.

## Plan Mode (Steps P1–P3)

Triggered by `plan <goal>`. Interactive wizard to configure a research run.

### Step P1: Parse and scan

Parse `<goal>` from arguments. Scan the codebase to detect:

- Language and framework (Python, PyTorch, pytest, etc.)
- Available test runners or benchmark scripts
- Candidate metric commands (pytest coverage, benchmark scripts, eval scripts)
- Candidate guard commands (test suite, lint, type check)
- Files relevant to the goal (scope files)

### Step P2: Present proposed config

Present the proposed config as a code block for user review. Include:

```
metric_cmd:      [command that prints a single numeric result]
metric_direction: higher | lower
guard_cmd:       [command that must pass (exit 0) on every kept commit]
max_iterations:  [default 20]
agent_strategy:  [auto | perf | code | ml | arch]
scope_files:     [files the ideation agent may modify]
compute:         local | colab
```

Dry-run both commands before presenting. If either fails, flag the error and propose corrections. Do not proceed to P3 until the user confirms or edits the config.

### Step P3: Write config

Write the confirmed config to `.claude/state/research/config.json`. Print:

```
✓ Config saved to .claude/state/research/config.json
Run /research <goal> to start the iteration loop.
```

______________________________________________________________________

## Default Mode (Steps 1–7)

### Step 1: Load / build config

If `.claude/state/research/config.json` exists, read it. Otherwise, attempt auto-detection of `metric_cmd` and `guard_cmd` from the goal string and codebase scan (same logic as Plan P1, but non-interactive — infer reasonable defaults).

Generate a `run-id` = `$(date +%Y%m%d-%H%M%S)`. Create the run directory:

```
.claude/state/research/<run-id>/
  state.json      ← iteration count, best metric, status
  experiments.jsonl  ← one line per iteration
```

Write initial `state.json`:

```json
{
  "run_id": "<run-id>",
  "goal": "<goal>",
  "config": {},
  "iteration": 0,
  "best_metric": null,
  "best_commit": null,
  "status": "running",
  "started_at": "<ISO timestamp>"
}
```

### Step 2: Precondition checks

Run all checks before touching code. Fail fast with a clear message if any fail:

1. **Clean git**: `git status --porcelain` → must be empty. If dirty: print the dirty files and stop.
2. **Not detached HEAD**: `git rev-parse --abbrev-ref HEAD` → must not be `HEAD`.
3. **Metric command produces numeric output**: run `metric_cmd` once; parse stdout for a float. If no float found: show the output and stop.
4. **Guard command passes**: run `guard_cmd` once; must exit 0. If it fails: show the output and stop.
5. **`--colab` check** (if flag present): verify Colab MCP tools are available by checking for `mcp__colab-mcp__runtime_execute_code`. If unavailable, print setup instructions (see Colab MCP section) and stop.

### Step 3: Select ideation agent

Apply the `agent_strategy` mapping from `<constants>`. If `auto`, apply keyword heuristics to `metric_cmd`. Log selected agent to `state.json`.

### Step 4: Establish baseline (iteration 0)

Run `metric_cmd` and `guard_cmd`. Parse the metric value. Append to `experiments.jsonl`:

```json
{
  "iteration": 0,
  "commit": "<HEAD sha>",
  "metric": 0.0,
  "delta": 0.0,
  "guard": "pass",
  "status": "baseline",
  "description": "baseline",
  "agent": null,
  "confidence": null,
  "timestamp": "<ISO>",
  "files": []
}
```

Update `state.json`: `best_metric = <baseline>`, `best_commit = <HEAD sha>`.

Print: `Baseline: <metric_cmd key> = <value>`. Then proceed to Step 5.

### Step 5: Iteration loop

For each iteration `i` from 1 to `max_iterations`:

#### Phase 1 — Review

Build context for the ideation agent:

- `git log --oneline -10` (recent commits)
- Last 10 lines of `experiments.jsonl` (prior experiment results)
- `git diff --stat HEAD~5 HEAD` (scope of recent changes)

Summarize into a compact context block: goal, current metric vs baseline, delta trend, recently modified files, previous agent actions and outcomes.

#### Phase 2 — Ideate

Spawn the selected specialist agent with this prompt (adapt as needed):

```
Goal: <goal>
Current metric: <metric_cmd key> = <current value> (baseline: <baseline>, direction: <higher|lower>)
Experiment history (last 10):
<jsonl summary>
Scope files (read and modify only these): <scope_files>

Read the scope files. Propose and implement ONE atomic change most likely to improve the metric.
The change must not break <guard_cmd>.
Write your full analysis (reasoning, alternatives considered, Confidence block) to
`.claude/state/research/<run-id>/ideation-<i>.md` using the Write tool.
Return ONLY the JSON result line — nothing else after it:
{"description":"...","files_modified":[...],"confidence":0.N}
```

For `--colab` runs: the ideation agent (especially `ai-researcher`) may call `mcp__colab-mcp__runtime_execute_code` during this phase to prototype GPU code before committing.

If the Agent tool is unavailable (nested subagent context), implement the change inline and construct the JSON result manually.

#### Phase 3 — Verify files changed

`git diff --stat`. If no files changed (no-op): append to JSONL with `status: no-op`, skip to Phase 8 (log), continue loop.

#### Phase 4 — Commit

Stage only the modified files (never `git add -A`):

```bash
git add <files_modified from agent JSON>
git commit -m "experiment(research/i<N>): <description>"
```

If pre-commit hooks fail:

- Delegate to `linting-expert` agent: provide the failing hook output and the modified files; ask it to fix the issues. Max 2 attempts.
- If still failing after 2 attempts: `git restore --staged .` + `git checkout -- .` to clean up, append `status: hook-blocked`, continue loop.

#### Phase 5 — Verify metric

Run `metric_cmd` with timeout:

```bash
timeout <VERIFY_TIMEOUT_SEC> <metric_cmd>
```

For `--colab`: route through `mcp__colab-mcp__runtime_execute_code` instead of local Bash. Parse numeric result from output.

If timeout expires: append `status: timeout`, revert via `git revert HEAD --no-edit`, continue loop.

#### Phase 6 — Guard

Run `guard_cmd` (exit-code check only). Record pass or fail.

#### Phase 7 — Decide

| Condition                                             | Action                                                                                                           |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| metric improved AND guard pass                        | Keep commit. Update `state.json`: `best_metric`, `best_commit`.                                                  |
| metric improved AND guard fail                        | Rework: re-spawn agent with guard failure output. Max `GUARD_REWORK_MAX` (2) attempts. If still failing: revert. |
| metric improved AND gain < 0.1% AND change > 50 lines | Discard (simplicity override): `git revert HEAD --no-edit`.                                                      |
| no improvement                                        | Revert: `git revert HEAD --no-edit`.                                                                             |

`git revert HEAD --no-edit` — never `git reset --hard` (preserves history, not in deny list).

#### Phase 8 — Log

Append one JSONL record to `experiments.jsonl`:

```json
{
  "iteration": 1,
  "commit": "<sha of experiment commit or revert>",
  "metric": 0.0,
  "delta": 0.0,
  "guard": "pass|fail",
  "status": "kept|reverted|rework|no-op|hook-blocked|timeout",
  "description": "<agent description>",
  "agent": "<agent type>",
  "confidence": 0.0,
  "timestamp": "<ISO>",
  "files": []
}
```

Update `state.json`: `iteration = i`, `status = running`.

#### Phase 9 — Progress checks

- **Summary every SUMMARY_INTERVAL iterations**: print compact table (iteration, metric, delta, status) for the last N iterations.
- **Stuck detection**: if last `STUCK_THRESHOLD` entries all have `status: reverted|no-op|hook-blocked`, trigger escalation (see `<constants>`). Log escalation action.
- **Diminishing returns**: if last `DIMINISHING_RETURNS_WINDOW` kept entries each improved < 0.5%, print a warning and suggest stopping. Do not auto-stop — let the user decide.
- **Early stop**: if the goal specifies a numeric target (e.g., "achieve 90% coverage") and the metric crosses it, stop and mark `state.json` `status: goal-achieved`.

### Step 6: Results report

Write full report to `tasks/output-research-<YYYY-MM-DD>.md` using the Write tool. Do not print the full report to terminal.

**Report structure:**

```markdown
## Research Run: <goal>

**Run ID**: <run-id>
**Date**: <date>
**Iterations**: <total> (<kept> kept, <reverted> reverted, <other> other)
**Baseline**: <metric> = <baseline value>
**Best**: <metric> = <best value> (<delta>% improvement)
**Best commit**: <sha>

### Experiment History
| # | Metric | Delta | Status | Description | Agent | Confidence |
|---|--------|-------|--------|-------------|-------|------------|
| ... |

### Summary
[2-3 sentences on what strategies worked, what didn't, what to try next]

### Recommended Follow-ups
- [next action]
```

Print compact terminal summary:

```
---
Research — <goal>
Iterations: <total>  Kept: <kept>  Reverted: <reverted>
Baseline:   <metric_key> = <baseline>
Best:       <metric_key> = <best> (<delta>% improvement, commit <sha>)
Agent:      <agent type used>
→ saved to tasks/output-research-<date>.md
---
```

Update `state.json`: `status = completed`.

### Step 7: Codex delegation (optional)

After confirming results, inspect applied changes (`git diff <baseline_commit>...<best_commit> --stat`) and identify tasks Codex can complete (inline comments on non-obvious changes, docstring updates for modified functions, test coverage for the modified path). Read `.claude/skills/_shared/codex-delegation.md` and apply the criteria defined there.

______________________________________________________________________

## Resume Mode

Triggered by `resume [run-id]`. If no `run-id` given, list available runs from `.claude/state/research/` and resume the most recent `status: running` one.

1. Read `state.json` from the run dir.
2. Validate git HEAD: if the current HEAD has diverged from `state.json.best_commit` in an unexpected direction, warn and ask before continuing.
3. Continue the iteration loop from `state.json.iteration + 1`.

______________________________________________________________________

## Team Mode (`--team`)

**When to trigger**: goal spans multiple optimization axes (e.g., "improve training speed" = model architecture + data pipeline + compute efficiency), OR user explicitly passes `--team`.

**Workflow:**

1. Lead completes Steps 1–4 (config, preconditions, baseline) solo.
2. Lead identifies 2–3 distinct optimization axes from the goal + codebase analysis.
3. Lead spawns 2–3 teammates (reasoning agents at `opus` per CLAUDE.md §Agent Teams), each assigned a different axis and a matching ideation agent type. Each teammate runs in an isolated worktree (`isolation: worktree`).

Example axis assignment for "reduce training time":

- teammate-A = `ai-researcher` axis: model architecture changes
- teammate-B = `perf-optimizer` axis: data pipeline and GPU utilization
- teammate-C = `sw-engineer` axis: code-level optimizations (batching, caching)

Each teammate's spawn prompt must include:

```
Read .claude/TEAM_PROTOCOL.md and use AgentSpeak v2.
You are a research teammate. Your axis: <axis description>.
Ideation agent: <agent type>.
Run 3–5 independent iterations of the Review→Ideate→Modify→Commit→Verify→Guard→Log loop.
Baseline metric: <metric_cmd key> = <baseline>. Direction: <higher|lower>.
Scope files: <scope_files>.
Report: {axis, iterations_run, kept, best_metric, best_commit, description}
Call TaskUpdate(in_progress) when starting; TaskUpdate(completed) when done.
```

4. Each teammate runs their iterations independently and reports results.
5. Lead cherry-picks the winning commits from each axis into the main branch, tests for compatibility, runs `guard_cmd`.
6. Lead measures combined metric, resolves conflicts if needed, writes the Step 6 report with per-axis breakdown and combined result.
7. Shutdown teammates.

**Note on CLAUDE.md §8**: team mode uses in-process teammates that send `TeammateIdle` notifications on completion — the file-activity polling protocol does not apply; `TeammateIdle` is the liveness signal.

______________________________________________________________________

## Colab MCP Integration (`--colab`)

**Purpose**: route metric verification and GPU code testing to a Colab notebook runtime instead of local execution. Essential for ML training metrics, CUDA benchmarks, and any workload requiring a GPU.

**Setup** (user must complete before running `--colab`):

1. Add `"colab-mcp"` to `enabledMcpjsonServers` in `settings.local.json`:
   ```json
   {
     "enabledMcpjsonServers": [
       "colab-mcp"
     ]
   }
   ```
2. Ensure `colab-mcp` server is defined in `.mcp.json` under `mcpServers` (see project `.mcp.json`).
3. Open a Colab notebook with the runtime connected and execute the MCP connection cell.

**How it works during a run:**

- Step 2 (preconditions): checks for `mcp__colab-mcp__runtime_execute_code` availability.
- Phase 5 (verify metric): calls `mcp__colab-mcp__runtime_execute_code` with `metric_cmd` instead of local `timeout <cmd>`.
- Phase 2 (ideate): `ai-researcher` agent can call `mcp__colab-mcp__runtime_execute_code` to prototype GPU code before committing.
- `VERIFY_TIMEOUT_SEC` = 300 (vs 120 local) to account for network + GPU startup latency.

If Colab MCP is unavailable at Step 2, print:

```
⚠ Colab MCP not available. To enable:
  1. Add "colab-mcp" to enabledMcpjsonServers in settings.local.json
  2. Open a Colab notebook and connect the runtime
  3. Execute the MCP connection cell in the notebook
Then re-run with --colab.
```

</workflow>

<notes>

- **Commit before verify** is the foundational pattern — it enables a clean `git revert HEAD` if the metric does not improve. Never verify before committing.
- **`git revert` over `git reset --hard`** — preserves experiment history, is not in the deny list.
- **Never `git add -A`** — always stage specific files returned by the agent JSON.
- **Never `--no-verify`** — if a pre-commit hook blocks, delegate to `linting-expert` and fix.
- **Guard ≠ Verify** — guard checks for regressions (tests, lint); verify checks the target metric. Both must pass to keep a commit.
- **Scope files are read-only for guard/test files** — the ideation agent must not modify test files or the metric/guard scripts themselves.
- **JSONL over TSV** — richer structured fields, `jq`-parseable, no delimiter ambiguity; query with `jq -c 'select(.status == "kept")' experiments.jsonl`.
- **State persistence enables resume** — if the loop crashes or times out, `resume` picks up exactly where it stopped.
- **Safety break**: max iterations default is 20; the skill never exceeds MAX_ITERATIONS without a user override in config.
- **Follow-up chains:**
  - Run improves metric → `/review` for quality validation of kept commits
  - Run finds the metric is plateauing → `/survey` for SOTA comparison — maybe a fundamentally different approach is needed
  - Kept commits accumulate technical debt → `/develop refactor` for structural cleanup with test safety net
  - Run exposes performance ceiling → `/optimize` for a deeper profiling pass on the bottleneck

</notes>
