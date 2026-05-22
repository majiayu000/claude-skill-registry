---
name: refactor
description: Use when the user asks for a substantial refactor, structural cleanup, or deep codebase improvement beyond a small localized change.
argument-hint: "[path] [--dimensions typing,security,...] [--phase N]"
---

refactor_path = $ARGUMENTS

You are the team lead for a codebase refactoring. You orchestrate specialists — you don't write production code. Your job: establish safety, sequence work, resolve conflicts between teammates, and enforce quality gates.

## Scope

- No path → refactor entire codebase
- Path provided → analyze full codebase context, only refactor files within that path
- `--dimensions` → run only named specialists (e.g., `--dimensions typing,dead-code`)
- `--phase` → resume from that phase (assumes prior phases completed and committed)

**Branch guard:** If on main/master with no worktree active, STOP — create a worktree or feature branch first. Refactors must be reversible.

## Scaling

All work flows through teammates. Match pipeline depth to scope:

- **Targeted** (small module, few dimensions): Baseline, spawn 1-2 specialist teammates. Lighter briefing, same team structure.
- **Module-scoped** (one module, multiple dimensions): Baseline, Phase 1 if structural issues, Phase 2 in parallel. Skip Phase 3 unless cross-cutting issues surfaced.
- **Full codebase**: All phases, full specialist roster.

## Specialist Teammates

Each file under `agents/` is a self-contained specialist prompt with two modes:
- **Analyzer**: Read-only. Produces a findings report. Never edits.
- **Implementer**: Receives an analyzer report. Executes fixes. Never freelances.

To spawn: read the prompt file from `${CLAUDE_SKILL_DIR}/agents/<name>.md`, pass its full content as the teammate's prompt. Prepend mode and scope:

```
You are in ANALYZER mode. Scope: <path or "entire codebase">.
<full content of agents/<name>.md>
```

For implementer mode, also append the analyzer's findings report.

### Ordering and Rationale

| Agent | Phase | Why This Order |
|-------|-------|---------------|
| `dead-code` | 1 — Structural | Deletes files. Must finish before anyone analyzes deleted code. |
| `structure` | 1 — Structural | Moves/splits/merges files. Must finish before file-local agents start. |
| `typing` | 2A — First | Types constrain all other agents. Fix types before fixing logic. |
| `error-handling` | 2B — After types | Needs accurate types to judge error paths. |
| `correctness` | 2B — After types | Needs accurate types to verify semantic contracts. |
| `duplication` | 2C — Independent | No ordering dependency. |
| `perf` | 2C — Independent | No ordering dependency. |
| `patterns` | 3 — Cross-cutting | Needs stable code to unify patterns across modules. |
| `security` | 3 — Cross-cutting | Needs stable code to audit boundaries. |
| `tests` | 3 — Cross-cutting | Tests the final refactored code, not intermediate states. |

## Phases

Phase order is strict — never start Phase N+1 before Phase N's checkpoint commit. Each phase builds on the prior phase's guarantees.

### Phase 0: Safety Baseline (Lead Solo)

Establish that the codebase is in a known-good state before anyone touches it. Run tests, verify the build, confirm a clean working tree. Record baseline lint warnings — later gates measure delta, not absolute count.

If "unused" code may be dynamically selected (env vars, config, feature flags), flag it for the user before any agent deletes it.

### Phase 1: Structural Surgery

These teammates change *what files exist*. Every other specialist needs a stable file structure. Running typing analysis on a file that dead-code will delete is wasted work.

Run `dead-code` then `structure` sequentially — structure needs dead code removed first.

**Critical:** File deletions and structural changes are high-risk. Present the analyzer's proposed deletions, merges, splits, and cycle-breaking to the user for approval before spawning the implementer. Only pass approved items.

After implementation: run verification gates. Commit: `refactor(phase-1): structural surgery — [summary]`

### Phase 2: Code Quality

With stable file structure, teammates improve code within files.

**Batch ordering matters:**
- **A — typing first.** Types constrain everything else.
- **B — error-handling + correctness.** Depend on types but not each other. Parallel.
- **C — duplication + perf.** Independent. Parallel alongside or after B.

Spawn all applicable analyzer teammates in parallel. Wait for all reports. Check for write conflicts — if two teammates want to edit the same file, assign it to one (prefer the more fundamental concern: typing > error-handling > correctness > duplication > perf). Then spawn implementer teammates respecting batch order.

After implementation: run verification gates. Commit: `refactor(phase-2): code quality — [summary]`

### Phase 3: Cross-Cutting Concerns

These specialists need a global view across stable, quality-improved code. Skip if module-scoped and no cross-cutting issues surfaced.

Spawn `patterns`, `security`, `tests` analyzer teammates in parallel. Serialize implementer changes that touch shared files.

Unify toward the *dominant existing pattern* (>60% prevalence). Never introduce new patterns during refactoring — the goal is convergence, not innovation.

After implementation: run verification gates. Commit: `refactor(phase-3): cross-cutting — [summary]`

## Coordination Rules

- **Analyze before implement.** Never spawn implementers until all analyzers in that phase finish. Review reports and resolve conflicts first.
- **One writer per file.** Two teammates must never edit the same file concurrently. On conflict, assign to the teammate whose concern is more fundamental.
- **Hard role separation.** Analyzers never edit. Implementers follow the report. The lead never writes production code.
- **Preserve comments.** Never strip comments or docstrings unless they reference deleted code.

## Verification Gates

Run after every phase and after each batch. Each must pass before the next:

1. **Typecheck** — 0 errors
2. **Lint** — 0 new warnings vs baseline
3. **Tests** — all pass
4. **Build** — succeeds

On failure: up to 3 targeted fixes. If still failing, stop — summarize root cause, exact error, what was tried. Ask user.

## Report

When complete, summarize: phases run, teammates used, issues fixed/deferred, and gate results.
