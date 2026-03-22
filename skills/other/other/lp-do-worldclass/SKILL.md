---
name: lp-do-worldclass
description: World-class benchmark skill for startup loop. Validates a business goal artifact, generates or refreshes a deep-research prompt, and (when a benchmark result is present) scans business strategy artifacts against world-class standards, presents improvement ideas to the operator for selection, and invokes /lp-do-ideas for each selected idea.
---

# World-Class Benchmark Orchestrator

`/lp-do-worldclass` is the goal-validation, benchmarking, and ideas-emission layer for startup loop world-class analysis.

This skill does three things:
1. Validate the operator-authored goal artifact at `<artifact_dir>/worldclass-goal.md` and generate or refresh a deep-research prompt
2. When a benchmark result exists and is current, scan strategy artifacts against world-class standards via `modules/scan-phase.md`
3. Present improvement ideas to the operator for selection via `modules/ideas-phase.md`, then invoke `/lp-do-ideas` for each selected idea

Keep this file thin. Do not embed scan rules, benchmark rubrics, or ideas templates here.

## Invocation

```
/lp-do-worldclass (--biz <BIZ> | --app <APP>) [--as-of-date <YYYY-MM-DD>] [--dry-run]
```

`--biz` and `--app` are mutually exclusive; exactly one is required.

### Parameters

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `--biz` | Required (if no `--app`) | — | Business identifier (e.g. `BRIK`, `PWRB`). Must match a directory under `docs/business-os/strategy/`. Mutually exclusive with `--app`. |
| `--app` | Required (if no `--biz`) | — | App identifier from the `apps` array in `docs/business-os/strategy/businesses.json` (e.g. `reception`). Resolves the parent BIZ automatically. Artifacts are stored under `docs/business-os/strategy/<resolved-BIZ>/apps/<APP>/`. Mutually exclusive with `--biz`. |
| `--as-of-date` | Optional | Today (YYYY-MM-DD) | Date used for scan output filename (`worldclass-scan-<YYYY-MM-DD>.md`) and the `scan_date` field in dispatch key formulas. Does not trigger time-based staleness — staleness is determined solely by `goal_version` mismatch. |
| `--dry-run` | Optional | — | When present: scan runs and scan output is written, but all queue-state.json writes are skipped. Safe mode for verifying scan behavior. |

## Global Invariants

### Operating mode

**SCAN + BENCHMARK**

### Allowed actions

- Read strategy artifact files, frontmatter, and goal/benchmark artifacts (read-only scan)
- Read `<artifact_dir>/worldclass-goal.md` and `worldclass-benchmark.md`
- **Edit** `<artifact_dir>/worldclass-goal.md` — `benchmark-status` field only (goal-phase Step 4 updates this after writing the research prompt)
- Write research prompt to `<artifact_dir>/worldclass-research-prompt.md`
- Write scan output to `<artifact_dir>/worldclass-scan-<YYYY-MM-DD>.md`
- **Append** to the scan output file — ideas-phase appends the `## Dispatches (Dry Run)` block and `## Ideas Summary` section
- Read `docs/business-os/startup-loop/ideas/trial/queue-state.json` (read-only; used for already-queued pre-filter in ideas-phase)
- Invoke `/lp-do-ideas` for each operator-selected idea (ideas-phase delegates all queue writes to `/lp-do-ideas`)
- **Create** `<artifact_dir>` if it does not exist — goal-phase may create the directory when `--app` mode resolves to a new app-level path

### Prohibited actions

- Code changes, refactors, or production data modifications
- Destructive shell or git commands
- Writing directly to queue-state.json — all queue writes are delegated to `/lp-do-ideas`
- Running scan-phase or ideas-phase in any state other than State 3 (goal-phase runs in States 2, 3, and 4)
- Skipping the dry-run flag when the operator passes it — must respect `--dry-run` and never write to queue-state.json in dry-run mode
- **Reusing a pre-existing scan file.** If `worldclass-scan-<YYYY-MM-DD>.md` already exists for the current `--as-of-date`, it must be overwritten by a fresh scan — never read and reused as the output of this invocation. Scan-phase Steps 1–7 execute from scratch on every invocation without exception.

## State Machine

The skill auto-routes to one of four states based on file presence and version alignment. Evaluate states in order; take the first match.

| State | Condition | Action | Outcome |
|---|---|---|---|
| **1** | `worldclass-goal.md` does not exist | Stop immediately | Emit guidance (see State 1 below) |
| **2** | Goal exists; `worldclass-benchmark.md` does not exist | Run goal-phase only | Stop; instruct operator (see State 2 below) |
| **3** | Goal + benchmark both exist AND `benchmark.goal_version == goal.goal_version` | Run goal-phase → scan-phase → ideas-phase | Emit summary |
| **4** | Goal + benchmark both exist AND `benchmark.goal_version != goal.goal_version` | Run goal-phase only, then stop | Refresh research prompt; instruct operator (see State 4 below) |

### State 1 — No goal artifact

Stop with:

```
No world-class goal found for <BIZ> (app: <APP> | biz mode).
Expected path: <artifact_dir>/worldclass-goal.md
Create a goal artifact from the template at docs/plans/lp-do-worldclass/worldclass-goal.template.md before running lp-do-worldclass.
```

### State 2 — Goal exists; no benchmark

Run goal-phase (validate goal artifact and generate research prompt). Then stop with:

```
Research prompt written to: <artifact_dir>/worldclass-research-prompt.md

Next step: run the prompt in your deep-research tool of choice and paste the result as:
  <artifact_dir>/worldclass-benchmark.md

Ensure the benchmark frontmatter includes:
  goal_version: <value from worldclass-goal.md>

Then re-run /lp-do-worldclass <original-invocation-form> to continue.
```

Where `<original-invocation-form>` is `--app <APP>` if invoked with `--app`, or `--biz <BIZ>` if invoked with `--biz`.

### State 3 — Goal + current benchmark

Run all three phases in sequence: goal-phase → scan-phase → ideas-phase. Emit a summary to the operator on completion.

### State 4 — Benchmark stale

Run goal-phase first (to refresh the research prompt if `goal_version` has changed), then stop with:

```
Benchmark is out of date for <BIZ> (app: <APP> | biz mode).
  goal_version in goal:      <goal.goal_version>
  goal_version in benchmark: <benchmark.goal_version>

The goal has changed since the benchmark was gathered. Rerun deep research using the refreshed prompt at:
  <artifact_dir>/worldclass-research-prompt.md

Paste the updated result as <artifact_dir>/worldclass-benchmark.md (replacing the existing file),
ensure frontmatter goal_version matches <goal.goal_version>, then re-run /lp-do-worldclass <original-invocation-form>.
```

## Module Routing

Execute phases in the order shown. Only run scan-phase and ideas-phase in State 3.

1. **Preflight** — resolve target (`--biz` or `--app`), validate strategy directory, set `BIZ`, `APP`, `artifact_dir`, `app_dir`; fail-closed if checks fail (see Preflight Gate below)
2. **State routing** — determine current state from file presence and version alignment (see State Machine above)
3. **`modules/goal-phase.md`** — validate goal artifact structure; generate or refresh the deep-research prompt; write `worldclass-research-prompt.md` *(runs in States 2, 3, and 4)*
4. **`modules/scan-phase.md`** — read benchmark; scan strategy artifacts; compare against world-class standards; produce gap table *(runs in State 3 only)*
5. **`modules/ideas-phase.md`** — derive improvement ideas from scan gaps; present selection list to operator; invoke `/lp-do-ideas` for each selected idea (dry-run: skip selection, write dry-run annotations to scan file) *(runs in State 3 only)*

## Preflight Gate

Run checks in this order; stop immediately on the first failure.

**Check 1 — Missing target:** if neither `--biz` nor `--app` is provided, stop with:

```
Error: one of --biz or --app is required.
Usage: /lp-do-worldclass (--biz <BIZ> | --app <APP>) [--as-of-date <YYYY-MM-DD>] [--dry-run]
```

**Check 2 — Mutual exclusivity:** if both `--biz` and `--app` are provided, stop with:

```
Error: --biz and --app are mutually exclusive. Provide one or the other.
```

**Check 3 — App resolution (`--app` mode only):** read `docs/business-os/strategy/businesses.json`. Find the entry whose `apps` array contains the `--app` value. Set `resolved_biz = entry.id`. If not found, stop with:

```
Error: App '<APP>' not found in businesses.json.
Verify the app identifier matches an entry in the apps array of a registered business.
Path: docs/business-os/strategy/businesses.json
```

**Check 4 — Strategy directory:** validate the parent business strategy directory exists:
- `--biz` mode: `docs/business-os/strategy/<BIZ>/` — if absent, stop with:
  ```
  Error: No strategy directory found for business <BIZ>.
  Expected path: docs/business-os/strategy/<BIZ>/
  Run from repo root and verify the business identifier is correct.
  ```
- `--app` mode: `docs/business-os/strategy/<resolved_biz>/` — if absent, stop with:
  ```
  Error: No strategy directory found for parent business <resolved_biz> (resolved from app '<APP>').
  Expected path: docs/business-os/strategy/<resolved_biz>/
  Run from repo root and verify the businesses.json entry for '<APP>' is correct.
  ```

**After all checks pass — set resolved variables** (passed to all modules):

```
BIZ          = --biz value  OR  resolved_biz from businesses.json lookup
APP          = --app value  OR  null (biz mode)
artifact_dir = docs/business-os/strategy/<BIZ>/                      (biz mode)
             = docs/business-os/strategy/<BIZ>/apps/<APP>/            (app mode)
app_dir      = apps/<first-app-in-BIZ-apps-array>/                    (biz mode — from businesses.json)
             = apps/<APP>/                                             (app mode — exact)
```

In biz mode, `app_dir` is resolved to the first entry in the business's `apps` array in `businesses.json` that maps to an existing directory under `apps/`. If no apps are listed or none exist, `app_dir` is `null` (scan-phase will skip app-directory probing).

## Inputs

| Input | Source | Notes |
|---|---|---|
| Goal artifact | `<artifact_dir>/worldclass-goal.md` | Required in States 2–4; preflight (state routing) fails to State 1 if missing |
| Benchmark artifact | `<artifact_dir>/worldclass-benchmark.md` | Required in States 3–4; absence routes to State 2 |
| Strategy directory | `docs/business-os/strategy/<BIZ>/` | Scanned by scan-phase in State 3 (always the parent business directory regardless of mode) |
| Business catalog | `docs/business-os/strategy/businesses.json` | Read by preflight in `--app` mode to resolve BIZ from app identifier |
| Queue state | `docs/business-os/startup-loop/ideas/trial/queue-state.json` | Read-only by ideas-phase (already-queued pre-filter); written by `/lp-do-ideas` for each operator-selected idea |

Where `<artifact_dir>` is resolved in the Preflight Gate:
- `--biz` mode: `docs/business-os/strategy/<BIZ>/`
- `--app` mode: `docs/business-os/strategy/<resolved-BIZ>/apps/<APP>/`

## Output Paths

- **Research prompt**: `<artifact_dir>/worldclass-research-prompt.md` — written by goal-phase (States 2, 3, and 4)
- **Scan output**: `<artifact_dir>/worldclass-scan-<YYYY-MM-DD>.md` — written by scan-phase (State 3 only; written on both live and dry-run)
- **Queue dispatches**: `docs/business-os/startup-loop/ideas/trial/queue-state.json` — written by `/lp-do-ideas` for each operator-selected idea (State 3 live runs only; ideas-phase never writes directly to this file)
