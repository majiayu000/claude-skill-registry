---
name: ln-814-optimization-executor
description: "Executes optimization hypotheses with keep/discard testing loop. Use when applying validated performance improvements."
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-line__outline, mcp__hex-line__read_file, mcp__hex-line__edit_file, mcp__hex-line__write_file, mcp__hex-line__verify, mcp__hex-line__changes
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-814-optimization-executor

**Type:** L3 Worker
**Category:** 8XX Optimization

Executes optimization hypotheses from the researcher using keep/discard autoresearch loop. Supports multi-file changes, compound baselines, and any optimization type (algorithm, architecture, query, caching, batching).

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | `.hex-skills/optimization/{slug}/context.md` OR conversation context (standalone invocation) |
| **Output** | Optimized code on isolated branch, per-hypothesis results, experiment log |
| **Pattern** | Strike-first: apply all → test → measure. Bisect only on failure. A/B only for contested alternatives |

---

## Workflow

**Phases:** Pre-flight → Baseline → Strike-First Execution → Report → Gap Analysis

---

## Phase 0: Pre-flight Checks

### Slug Resolution

- If invoked via Agent with contextStore containing `slug` — use directly.
- If invoked standalone — derive slug from context_file path or ask user.

### Step 1: Load Context

Read `.hex-skills/optimization/{slug}/context.md` from project root. Contains problem statement, profiling results, research hypotheses, and target metric.

If file not found: check conversation context for the same data (standalone invocation).

### Step 2: Pre-flight Validation

| Check | Required | Action if Missing |
|-------|----------|-------------------|
| Hypotheses provided (H1..H7) | Yes | Block — nothing to execute |
| Test infrastructure | Yes | Block (see ci_tool_detection.md) |
| Git clean state | Yes | Block (need clean baseline for revert) |
| Worktree isolation | Yes | Create per git_worktree_fallback.md |
| E2E safety test | No (recommended) | Read from context; WARN if null — full test suite as fallback gate |

**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md` — use optimization rows.
**MANDATORY READ:** Load `shared/references/ci_tool_detection.md` — use Test Frameworks + Benchmarks sections.

**MANDATORY READ:** Load `shared/references/mcp_tool_preferences.md` and `shared/references/mcp_integration_patterns.md`.

Use `hex-line` as the primary path for code/config/script edits in this worker. Profilers and benchmarks stay the source of truth; do not treat `hex-graph` as runtime evidence here.

### E2E Safety Test

Read `e2e_test_command` from context file (discovered by profiler during test discovery phase).

| Source | Action |
|--------|--------|
| Context has `e2e_test_command` | Use as functional safety gate in Phase 2 |
| Context has `e2e_test_command = null` | WARN: full test suite is the fallback gate |
| Standalone (no context) | User must provide test command; block if missing |

---

## Phase 1: Establish Baseline

Reuse baseline from performance map (already measured with real metrics).

### From Context File

Read `performance_map.baseline` and `performance_map.test_command` from `.hex-skills/optimization/{slug}/context.md`.

| Field | Source |
|-------|--------|
| `test_command` | Discovered/created test command |
| `baseline` | Multi-metric snapshot: wall time, CPU, memory, I/O |

### Verification Run

Run `test_command` once to confirm baseline is still valid (code unchanged since profiling):

| Step | Action |
|------|--------|
| 1 | Run `test_command` |
| 2 | IF result within 10% of `baseline.wall_time_ms` → baseline confirmed |
| 3 | IF result diverges > 10% → re-measure (3 runs, median) as new baseline |
| 4 | IF test FAILS → BLOCK: "test fails on unmodified code" |

---

## Phase 2: Strike-First Execution

**MANDATORY READ:** Load [optimization_categories.md](references/optimization_categories.md) for pattern reference during implementation.

Apply maximum changes at once. Only fall back to A/B testing where sources genuinely disagree on approach.

### Step 1: Triage Hypotheses

Split hypotheses from researcher into two groups:

| Group | Criteria | Action |
|-------|----------|--------|
| **Uncontested** | Clear best approach, no conflicting alternatives | Apply directly in the strike |
| **Contested** | Multiple approaches exist (e.g., source A says cache, source B says batch) OR `conflicts_with` another hypothesis | A/B test each alternative on top of full implementation |

Most hypotheses should be uncontested — the researcher already ranked them by evidence.

### Step 2: Strike (Apply All Uncontested)

```
1. APPLY all uncontested hypotheses at once (all file edits)
2. VERIFY: Run full test suite
   IF tests FAIL:
     - IF fixable (typo, missing import) → fix & re-run ONCE
     - IF fundamental → BISECT (see Step 4)
3. E2E GATE (if e2e_test_command not null):
   IF FAIL → BISECT
4. MEASURE: 5 runs, median
5. COMPARE: improvement vs baseline
   IF improvement meets target → DONE. Commit all:
     git add {all_files}
     git commit -m "perf: apply optimizations H1,H2,H3,... (+{improvement}%)"
   IF no improvement → BISECT
```

### Step 3: Contested Alternatives (A/B on top of strike)

For each contested pair/group, with ALL uncontested changes already applied:

```
FOR each contested hypothesis group:
  1. Apply alternative A → test → measure (5 runs, median)
  2. Revert alternative A, apply alternative B → test → measure
  3. KEEP the winner. Commit.
  4. Winner becomes part of the baseline for next contested group.
```

### Step 4: Bisect (only on strike failure)

If strike fails tests or shows no improvement:

```
1. Revert all changes: git checkout -- . && git clean -fd
2. Binary search: apply first half of hypotheses → test
   - IF passes → problem in second half
   - IF fails → problem in first half
3. Narrow down to the breaking hypothesis
4. Remove it from strike, re-apply remaining → test → measure
5. Log removed hypothesis with reason
```

### Scope Rules

| Rule | Description |
|------|-------------|
| File scope | Multiple files allowed (not limited to single function) |
| Signature changes | Allowed if tests still pass |
| New files | Allowed (cache wrapper, batch adapter, utility) |
| New dependencies | Allowed if already in project ecosystem (e.g., using configured Redis) |
| Time budget | 45 minutes total |

### Revert Protocol

| Scope | Command |
|-------|---------|
| Full revert | `git checkout -- . && git clean -fd` (safe in worktree) |
| Single hypothesis | `git checkout -- {files}` (only during bisect) |

### Safety Rules

| Rule | Description |
|------|-------------|
| Traceability | Commit message lists all applied hypothesis IDs |
| Isolation | All work in isolated worktree; never modify main worktree |
| Bisect only on failure | Do NOT test hypotheses individually unless strike fails or alternatives genuinely conflict |
| Crash triage | Runtime crash → fix once if trivial (typo, import), else bisect to find cause |

### Stop Conditions (Execution Loop)

| Condition | Action |
|-----------|--------|
| Strike passes + improvement meets target | STOP — commit, proceed to Report |
| All contested alternatives tested | STOP — commit winner, proceed to Report |
| Bisect removes all hypotheses | STOP — report "all hypotheses failed" with profiling data |
| Time budget exceeded (45 min) | STOP — report partial results with remaining hypotheses |
| All tests fail after strike + bisect | STOP — full revert, report diagnostic value only |

---

## Phase 3: Report Results

### Report Schema

| Field | Description |
|-------|-------------|
| baseline | Original measurement (metric + value) |
| final | Final measurement after optimizations |
| total_improvement_pct | Overall percentage improvement |
| target_met | Boolean — did we reach the target metric? |
| strike_result | `clean` (all applied) / `bisected` (some removed) / `failed` |
| hypotheses_applied | List of hypothesis IDs applied in strike |
| hypotheses_removed | List removed during bisect (with reasons) |
| contested_results | Per-contested group: alternatives tested, winner, measurement |
| branch | Worktree branch name |
| files_modified | All changed files |
| e2e_test | `{ command, source, baseline_passed, final_passed }` or null |

### Results Comparison (mandatory)

Show baseline vs final for EVERY metric from `performance_map.baseline`. Include both percentage and multiplier.

```
| Metric | Baseline | After Strike | Improvement |
|--------|----------|-------------|-------------|
| Wall time | 7280ms | 3800ms | 47.8% (1.9x) |
| CPU time | 850ms | 720ms | 15.3% (1.2x) |
| Memory peak | 256MB | 245MB | 4.3% |
| HTTP round-trips | 13 | 2 | 84.6% (6.5x) |

Target: 5000ms → Achieved: 3800ms ✓ TARGET MET
```

### Per-Function Delta (if instrumentation available)

If `instrumented_files` from context is non-empty, run `test_command` once more AFTER strike to capture per-function timing with the same instrumentation the profiler placed:

```
| Function | Before (ms) | After (ms) | Delta |
|----------|------------|------------|-------|
| mt_translate | 3500 | 450 | -87% (7.8x) |
| tikal_extract | 2800 | 2800 | 0% (unchanged) |
```

Then clean up: `git checkout -- {instrumented_files}` — remove all profiling instrumentation before final commit.

Present both tables to user. This is the primary deliverable — numbers the user sees first.

### Experiment Log

Write to `{project_root}/.hex-skills/optimization/{slug}/ln-814-log.tsv`:

| Column | Description |
|--------|-------------|
| timestamp | ISO 8601 |
| phase | `strike` / `bisect` / `contested` |
| hypotheses | Comma-separated IDs applied in this round |
| baseline_ms | Baseline before this round |
| result_ms | Measurement after changes |
| improvement_pct | Percentage change |
| status | `applied` / `removed` / `alternative_a` / `alternative_b` |
| commit | Git commit hash |
| files | Comma-separated modified files |
| e2e_status | pass / fail / skipped |

Append to existing file if present (enables tracking across multiple runs).

---

## Phase 4: Gap Analysis (If Target Not Met)

If target metric not reached after all hypotheses:

| Section | Content |
|---------|---------|
| Achievement | What was achieved (original → final, improvement %) |
| Remaining bottlenecks | From time map: which steps still dominate |
| Remaining cycles | If coordinator runs multi-cycle: "{remaining} optimization cycles available for remaining bottlenecks" |
| Infrastructure recommendations | If bottleneck requires infra changes (scaling, caching layer, CDN) |
| Further research | Optimization directions not explored in this run |

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Strike fails all tests | Bisect to find breaking hypothesis, remove it, retry |
| Strike shows no improvement | Bisect to identify ineffective hypotheses |
| Measurement inconsistent (high variance) | Increase runs to 10, use median |
| Worktree creation fails | Fall back to branch per git_worktree_fallback.md |
| Time budget exceeded | Stop loop, report partial results with hypotheses remaining |
| Multi-file revert fails | `git checkout -- .` in worktree (safe — worktree is isolated) |

---

## References

- [optimization_categories.md](references/optimization_categories.md) — optimization pattern checklist
- `shared/references/ci_tool_detection.md` (test + benchmark detection)
- `shared/references/git_worktree_fallback.md` (worktree isolation)

---

## Runtime Summary Artifact

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`

Emit an `optimization-worker` summary envelope.

Managed mode:
- `ln-810` passes deterministic `runId` and exact `summaryArtifactPath`
- write the summary to the provided `summaryArtifactPath`

Standalone mode:
- omit `runId` and `summaryArtifactPath`
- write `.hex-skills/runtime-artifacts/runs/{run_id}/optimization-worker/ln-814--{identifier}.json`

## Definition of Done

- [ ] Baseline established using same metric type as observed problem
- [ ] Hypotheses triaged: uncontested vs contested
- [ ] Strike applied: all uncontested hypotheses implemented at once
- [ ] Tests pass after strike
- [ ] Contested alternatives A/B tested on top of full implementation
- [ ] Bisect performed only if strike fails (not preemptively)
- [ ] E2E safety test passes (or documented as unavailable)
- [ ] Experiment log written to `.hex-skills/optimization/{slug}/ln-814-log.tsv`
- [ ] Report returned with baseline, final, improvement%, strike result
- [ ] All changes on isolated branch, pushed to remote
- [ ] Gap analysis provided if target metric not met
- [ ] Optimization execution artifact written to the shared location

---

**Version:** 2.0.0
**Last Updated:** 2026-03-14
