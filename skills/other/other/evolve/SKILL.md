---
name: evolve
description: Goal-driven fitness-scored improvement loop. Measures goals, picks worst gap, runs /rpi (or parallel /swarm of /rpi cycles), compounds via knowledge flywheel.
context: fork
disable-model-invocation: true
metadata:
  tier: execution
  dependencies:
    - rpi         # required - executes each improvement cycle
    - post-mortem # required - auto-runs at teardown to harvest learnings
  triggers:
    - evolve
    - improve everything
    - autonomous improvement
    - run until done
---

# /evolve — Goal-Driven Compounding Loop

> **Purpose:** Measure what's wrong. Fix the worst thing. Measure again. Compound.

Thin fitness-scored loop over `/rpi`. The knowledge flywheel provides compounding — each cycle loads learnings from all prior cycles.

## Compaction Resilience

The evolve loop MUST survive context compaction. On session restart, read `cycle-history.jsonl` to determine cycle number and resume from Step 1. See `references/cycle-history.md` for recovery protocol details.

## Known Good Properties

- Severity-based selection naturally orders: code health → architecture →
  testing → documentation → cleanup. This is the correct ordering.
  Do not add special-case logic to front-load doc fixes.

**Dormancy is success.** When all goals pass and no harvested work remains, the system enters dormancy — a valid, healthy state. The system does not manufacture work to justify its existence. Nothing to do means everything is working.

## Quick Start

```bash
/evolve                      # Run forever until kill switch or stagnation
/evolve --max-cycles=5       # Cap at 5 improvement cycles
/evolve --dry-run            # Measure fitness, show what would be worked on, don't execute
```

## Execution Steps

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

### Step 0: Setup

```bash
mkdir -p .agents/evolve
```

Load accumulated learnings (COMPOUNDING):
```bash
ao inject 2>/dev/null || true
```

Parse flags:
- `--max-cycles=N` (default: **unlimited**) — optional hard cap. Without this flag, the loop runs **forever** until kill switch or stagnation.
- `--dry-run` — measure and report only, no execution
- `--skip-baseline` — skip the Step 0.5 baseline sweep
- `--parallel` — enable parallel goal execution via /swarm per cycle (default: off, sequential)
- `--max-parallel=N` (default: **3**, cap: **5**) — max goals to improve in parallel per cycle. Only meaningful with `--parallel`.

**Capture session-start SHA** (for multi-commit revert):
```bash
SESSION_START_SHA=$(git rev-parse HEAD)
```

Initialize state:
```
evolve_state = {
  cycle: 0,
  max_cycles: <from flag, or Infinity if not set>,
  dry_run: <from flag, default false>,
  test_first: <from flag, default false>,
  parallel: <from --parallel flag, default false>,
  max_parallel: <from --max-parallel flag, default 3, cap 5>,
  session_start_sha: $SESSION_START_SHA,
  idle_streak: 0,         # consecutive cycles with nothing to do
  max_idle_streak: 3,     # stop after this many consecutive idle cycles
  history: []
}
```

### Step 0.5: Cycle-0 Baseline Sweep

Capture a baseline fitness snapshot before the first cycle so every later cycle
has a comparison anchor.  Skipped on resume (idempotent).

```
if [ "$SKIP_BASELINE" = "true" ]; then
  log "Skipping baseline sweep (--skip-baseline flag set)"
  exit 0
fi

if ! [ -f .agents/evolve/fitness-0-baseline.json ]; then
  # **Preferred (when ao CLI available):**
  if command -v ao &>/dev/null; then
    ao goals measure --json > .agents/evolve/fitness-0-baseline.json
  fi

  # **Fallback (no ao CLI):**
  baseline = MEASURE_FITNESS()            # run every GOALS.yaml goal
  baseline.cycle = 0
  write ".agents/evolve/fitness-0-baseline.json" baseline

  # Baseline report
  failing = [g for g in baseline.goals if g.result == "fail"]
  failing.sort(by=weight, descending)
  cat > .agents/evolve/cycle-0-report.md << EOF
  # Cycle-0 Baseline
  **Total goals:** ${len(baseline.goals)}
  **Passing:** ${len(baseline.goals) - len(failing)}
  **Failing:** ${len(failing)}
  $(for g in failing: "- [weight ${g.weight}] ${g.id}: ${g.result}")
  EOF

  log "Baseline captured: ${len(failing)}/${len(baseline.goals)} goals failing"
fi

# Wiring closure check: every check-*.sh must appear in GOALS.yaml
unwired=$(comm -23 \
  <(ls scripts/check-*.sh 2>/dev/null | xargs -I{} basename {} | sort) \
  <(grep -oP 'scripts/check-\S+\.sh' GOALS.yaml | xargs -I{} basename {} | sort))
if [ -n "$unwired" ]; then
  for script in $unwired; do
    add_to_next_work("Unwired script: $script — wire to GOALS.yaml or delete",
                     severity="high", type="tech-debt")
  done
  log "Found $(echo "$unwired" | wc -l | tr -d ' ') unwired scripts — added to next-work"
fi
```

### Step 1: Kill Switch Check

Check at the TOP of every cycle iteration:

```bash
# External kill (outside repo — can't be accidentally deleted by agents)
if [ -f ~/.config/evolve/KILL ]; then
  echo "KILL SWITCH ACTIVE: $(cat ~/.config/evolve/KILL)"
  # Write acknowledgment
  echo "{\"killed_at\": \"$(date -Iseconds)\", \"cycle\": $CYCLE}" > .agents/evolve/KILLED.json
  exit 0
fi

# Local convenience stop
if [ -f .agents/evolve/STOP ]; then
  echo "STOP file detected: $(cat .agents/evolve/STOP 2>/dev/null)"
  exit 0
fi
```

If either file exists, log reason and **stop immediately**. Do not proceed to measurement.

### Step 2: Measure Fitness (MEASURE_FITNESS)

Read `GOALS.yaml` from repo root.

**Preferred (when ao CLI available):**
```bash
if command -v ao &>/dev/null; then
  ao goals measure --json > .agents/evolve/fitness-${CYCLE}-snapshot.json
fi
```

**Fallback (no ao CLI):**

For each goal:

```bash
# Run the check command
if eval "$goal_check" > /dev/null 2>&1; then
  # Exit code 0 = PASS
  result = "pass"
else
  # Non-zero = FAIL
  result = "fail"
fi
```

Record results with **continuous values** (not just pass/fail):
```bash
# Write fitness snapshot
cat > .agents/evolve/fitness-${CYCLE}.json << EOF
{
  "cycle": $CYCLE,
  "timestamp": "$(date -Iseconds)",
  "cycle_start_sha": "$(git rev-parse HEAD)",
  "goals": [
    {"id": "$goal_id", "result": "$result", "weight": $weight, "value": $metric_value, "threshold": $threshold},
    ...
  ]
}
EOF
```

For goals with measurable metrics, extract the continuous value:
- `go-coverage-floor`: parse `go test -cover` output → `"value": 85.7, "threshold": 80`
- `doc-coverage`: count skills with references/ → `"value": 20, "threshold": 16`
- `shellcheck-clean`: count of warnings → `"value": 0, "threshold": 0`
- Other goals: `"value": null` (binary pass/fail only)

**Snapshot enforcement (HARD GATE):** After writing the snapshot, validate it:
```bash
if ! jq empty ".agents/evolve/fitness-${CYCLE}.json" 2>/dev/null; then
  echo "ERROR: Fitness snapshot write failed or invalid JSON. Refusing to proceed."
  exit 1
fi
```
Do NOT proceed to Step 3 without a valid fitness snapshot.

**Bootstrap mode:** If a check command fails to execute (command not found, permission denied), mark that goal as `"result": "skip"` with a warning. Do NOT block the entire loop because one check is broken.

### Step 3: Select Work

```
failing_goals = [g for g in goals if g.result == "fail"]

if not failing_goals:
  # Comprehensive sweep: if .agents/evolve/last-sweep-date is stale (>7 days) or missing,
  # run shellcheck, go vet, anti-pattern grep, and coverage floor scan.
  # Add all findings to next-work.jsonl via add_to_next_work().
  # Process ALL coverage floors in a single pass (never split across cycles).
  # Touch .agents/evolve/last-sweep-date when done.

  # All goals pass — check harvested work from prior /rpi cycles
  if [ -f .agents/rpi/next-work.jsonl ]; then
    # Detect current repo for filtering
    CURRENT_REPO=$(bd config --get prefix 2>/dev/null \
      || basename "$(git remote get-url origin 2>/dev/null)" .git 2>/dev/null \
      || basename "$(pwd)")

    all_items = read_unconsumed(next-work.jsonl)  # entries with consumed: false
    # Filter by target_repo: include items where target_repo matches
    # CURRENT_REPO, target_repo is "*" (cross-repo), or field is absent (backward compat).
    # Skip items whose target_repo names a different repo.
    items = [i for i in all_items
             if i.target_repo in (CURRENT_REPO, "*", None)]
    if items:
      evolve_state.idle_streak = 0  # reset — we found work
      selected_item = max(items, by=severity)  # highest severity first
      log "All goals met. Picking harvested work: {selected_item.title}"
      # Execute as an /rpi cycle (Step 4), then mark consumed
      /rpi "{selected_item.title}" --auto --max-cycles=1 --test-first   # if --test-first set
      /rpi "{selected_item.title}" --auto --max-cycles=1                 # otherwise
      mark_consumed(selected_item)  # set consumed: true, consumed_by, consumed_at
      # Skip Steps 4-5 (already executed above), go to Step 6 (log cycle)
      log_cycle(cycle, goal_id="next-work:{selected_item.title}", result="harvested")
      continue loop  # → Step 1 (kill switch check)

  # Nothing to do THIS cycle — but don't quit yet
  evolve_state.idle_streak += 1
  log "All goals met, no harvested work. Idle streak: {idle_streak}/{max_idle_streak}"

  if evolve_state.idle_streak >= evolve_state.max_idle_streak:
    log "Stagnation: {max_idle_streak} consecutive idle cycles. Nothing left to improve."
    STOP → go to Teardown

  # NOT stagnant yet — re-measure next cycle (external changes, new harvested work)
  log "Re-measuring next cycle in case conditions changed..."
  continue loop  # → Step 1 (kill switch check)

# Meta-goal guidance: after pruning any allowlist, add a meta-goal that
# prevents re-accumulation. The meta-goal should fail if allowlist entries
# have callers. Allowlists without meta-goals are technical debt magnets.
# See references/goals-schema.md for the meta-goal pattern.

# We have failing goals — reset idle streak
evolve_state.idle_streak = 0

# Sort by weight (highest priority first)
failing_goals.sort(by=weight, descending)

# Simple strike check: skip goals that failed the last 3 consecutive cycles
eligible_goals = []
for goal in failing_goals:
  recent = last_3_cycles_for(goal.id)
  if all(r.result == "regressed" for r in recent):
    log "Skipping {goal.id}: regressed 3 consecutive cycles. Needs human attention."
    continue
  eligible_goals.append(goal)

if not eligible_goals:
  log "All failing goals have regressed 3+ times. Human intervention needed."
  STOP → go to Teardown

if evolve_state.parallel and len(eligible_goals) > 1:
  # PARALLEL: Select top N independent goals (heuristic: non-overlapping check scripts)
  # True conflicts caught by regression gate (Step 5) which reverts entire wave.
  selected_goals = select_parallel_goals(eligible_goals, max=evolve_state.max_parallel)
else:
  # SEQUENTIAL MODE: Select single worst goal (existing behavior)
  selected = eligible_goals[0]
```

### Step 4: Execute

**If `--dry-run`:** Report the selected goal (or harvested item) and stop.

```
log "Dry run: would work on '{selected.id}' (weight: {selected.weight})"
log "Description: {selected.description}"
log "Check command: {selected.check}"

# Also show queued harvested work (filtered to current repo)
if [ -f .agents/rpi/next-work.jsonl ]; then
  all_items = read_unconsumed(next-work.jsonl)
  items = [i for i in all_items
           if i.target_repo in (CURRENT_REPO, "*", None)]
  if items:
    log "Harvested work queue ({len(items)} items):"
    for item in items:
      log "  - [{item.severity}] {item.title} ({item.type})"

STOP → go to Teardown
```

**Otherwise:** Run improvement cycle(s) on the selected goal(s).

```
if evolve_state.parallel and len(selected_goals) > 1:
  # PARALLEL: Create isolated artifact dirs per goal, TaskCreate for each,
  # invoke /swarm --worktrees. Each worker runs /rpi independently.
  # Results written to .agents/evolve/parallel-results/{goal.id}.md
  # See references/parallel-execution.md for full task template and architecture.
  /swarm --worktrees
else:
  # SEQUENTIAL: Run a single /rpi cycle
  /rpi "Improve {selected.id}: {selected.description}" --auto --max-cycles=1
```

This internally runs the full lifecycle (per goal):
- `/research` — understand the problem
- `/plan` — decompose into issues
- `/pre-mortem` — validate the plan
- `/crank` — implement (spawns workers)
- `/vibe` — validate the code
- `/post-mortem` — extract learnings + `ao forge` (COMPOUNDING)

**Wait for all /rpi cycles to complete before proceeding to Step 5.**

In parallel mode, each worker runs a complete /rpi cycle independently. The regression gate (Step 5) runs once after ALL parallel goals complete — not per-goal. See `references/parallel-execution.md` for architecture details.

### Step 5: Full-Fitness Regression Gate

**CRITICAL: Re-run ALL goals, not just the target.**

After /rpi completes, re-run MEASURE_FITNESS on **every goal** (same as Step 2). Write result to `fitness-{CYCLE}-post.json`.

Compare the pre-cycle snapshot (`fitness-{CYCLE}.json`) against the post-cycle snapshot (`fitness-{CYCLE}-post.json`) for **ALL goals**:

```
pre_results = load("fitness-{CYCLE}.json")
post_results = MEASURE_FITNESS()  # writes fitness-{CYCLE}-post.json

# Determine outcome for target goal(s)
outcome = "improved" if target_now_passes else "unchanged"

# FULL REGRESSION CHECK: compare ALL goals (both parallel and sequential)
newly_failing = [g.id for g in post_results.goals
                 if pre_results.find(g.id).result == "pass" and g.result == "fail"]

if newly_failing:
  outcome = "regressed"
  log "REGRESSION: {newly_failing} started failing"
  # Revert all commits since cycle start
  cycle_start_sha = pre_results.cycle_start_sha
  commit_count = $(git rev-list --count ${cycle_start_sha}..HEAD)
  if commit_count == 1:
    git revert HEAD --no-edit
  elif commit_count > 1:
    git revert --no-commit ${cycle_start_sha}..HEAD
    git commit -m "revert: evolve cycle ${CYCLE} regression in {newly_failing}"
```

**Snapshot enforcement:** Validate `fitness-{CYCLE}-post.json` was written and is valid JSON before proceeding.

### Step 6: Log Cycle

Append to `.agents/evolve/cycle-history.jsonl` with mandatory fields: `cycle`, `goal_id`/`goal_ids`, `result`, `commit_sha`, `goals_passing`, `goals_total`, `goals_added`, `timestamp`. For cycle history JSONL format, mandatory fields, and telemetry details, read `references/cycle-history.md`.

**Compaction-proofing: commit after every cycle.** Uncommitted state does not survive context compaction.

```bash
bash scripts/log-telemetry.sh evolve cycle-complete cycle=${CYCLE} goal=${selected.id} outcome=${outcome} 2>/dev/null || true
git add .agents/evolve/cycle-history.jsonl .agents/evolve/fitness-*.json
git commit -m "evolve: cycle ${CYCLE} — ${selected.id} ${outcome}" --allow-empty
```

### Step 7: Loop or Stop

```
evolve_state.cycle += 1

# Only stop for max-cycles if the user explicitly set one
if evolve_state.max_cycles != Infinity and evolve_state.cycle >= evolve_state.max_cycles:
  log "Max cycles ({max_cycles}) reached."
  STOP → go to Teardown

# Otherwise: loop back to Step 1 (kill switch check) — run forever
```

### Teardown

1. Run `/post-mortem "evolve session: $CYCLE cycles, goals improved: X, harvested: Y"` to harvest learnings from the entire session.
2. Compute session fitness trajectory (compare baseline vs final snapshot). See `references/teardown.md` for the full trajectory computation and session summary template.
3. Write `session-summary.md` and report to user.

Report to user:
```
## /evolve Complete

Cycles: N of M
Goals improved: X
Goals regressed: Y (reverted)
Goals unchanged: Z
Post-mortem: <verdict> (see <report-path>)

Run `/evolve` again to continue improving.
```

---

## Examples

### Basic Improvement Loop

**User says:** `/evolve --max-cycles=5`

**What happens:**
1. Baseline sweep captures fitness snapshot (cycle 0)
2. Measures all GOALS.yaml goals, finds `shellcheck-clean` failing (weight 8)
3. Runs `/rpi "Improve shellcheck-clean"` — fixes 12 shellcheck warnings
4. Regression gate confirms no other goals broke
5. Repeats for up to 5 cycles, improving highest-weight failures first

**Result:** 3 goals improved over 5 cycles, session summary written to `.agents/evolve/session-summary.md`.

### Dry Run Assessment

**User says:** `/evolve --dry-run`

**What happens:**
1. Measures all goals, identifies `go-coverage-floor` failing (value: 72.3, threshold: 80)
2. Reports what would be worked on without executing
3. Shows harvested work queue from prior `/rpi` cycles

**Result:** Assessment report showing current fitness state and recommended next improvement.

### Parallel Goal Improvement

**User says:** `/evolve --parallel --max-parallel=3 --max-cycles=2`

**What happens:**
1. Measures fitness, finds 4 failing goals
2. Selects top 3 non-overlapping goals for parallel execution
3. Spawns `/swarm --worktrees` with one `/rpi` per goal
4. Regression gate checks ALL goals after parallel wave completes
5. Repeats for cycle 2

**Result:** Multiple goals improved simultaneously, with full regression protection.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| Loop exits immediately | Kill switch file exists (`~/.config/evolve/KILL` or `.agents/evolve/STOP`) | Remove the kill switch file |
| "Stagnation" after 3 idle cycles | All goals pass and no harvested work remains | This is success — dormancy is healthy. Run again when conditions change |
| Regression gate reverts cycle | Improvement broke a previously-passing goal | Review reverted changes, narrow the fix scope, re-run |
| Fitness snapshot invalid JSON | Goal check command produced unexpected output | Check individual goal commands manually, fix broken checks |
| Goal stuck (3 consecutive regressions) | Strike rule skips goal after 3 failures | Needs manual investigation — review `.agents/evolve/cycle-history.jsonl` |
| Baseline sweep hangs | A goal check command hangs or takes too long | Use `--skip-baseline` and investigate the slow check |

---

## References

- `references/cycle-history.md` — Cycle history format, recovery protocol, kill switch, flags, troubleshooting
- `references/compounding.md` — Knowledge flywheel and work harvesting
- `references/goals-schema.md` — GOALS.yaml format
- `references/artifacts.md` — Generated files and their purposes
- `references/examples.md` — Detailed usage examples
- `references/parallel-execution.md` — Parallel /swarm architecture
- `references/teardown.md` — Trajectory computation and session summary template

## See Also

- `skills/rpi/SKILL.md` — Full lifecycle orchestrator (called per cycle)
- `skills/vibe/SKILL.md` — Code validation (called by /rpi)
- `skills/council/SKILL.md` — Multi-model judgment (called by /rpi)
- `GOALS.yaml` — Fitness goals for this repo
