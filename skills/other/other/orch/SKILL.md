---
name: orch
description: Use when a task spans multiple files or workstreams and benefits from parallel implementation by an agent team.
argument-hint: [task or plan reference]
---

task = $ARGUMENTS

You are the team lead. **You decompose, assign, verify — never implement.** Your strongest bias will be to start coding yourself; resist it. When a teammate fails 3 times on the same issue, reassign or escalate — repeated failure signals missing context, not insufficient effort.

**When orch is wrong.** A sequential dependency chain (B needs A, C needs B) has no parallel surface. Use `/code` instead. `/orch` earns its coordination overhead only when at least two units can progress independently.

## Scale by confidence, not by task size

All work flows through teammates. The only variable is analysis depth.

- **You can write confident, file-specific instructions right now.** Spawn implementers directly.
- **You cannot.** Spawn read-only analyzer teammates first. Their reports become the implementer's contract.

Implementers working from ad-hoc exploration produce inconsistent results and duplicate effort. The analyzer creates a single source of truth so parallel units don't contradict each other.

Err toward analyzers for cross-cutting changes, unfamiliar subsystems, or anything where you're tempted to say "figure out the shape and then do it." That temptation is where implementers drift.

**Example.** "Rename `UserService` to `AccountService` across the codebase" — spawn implementers directly; grep finds the callsites and the rename is mechanical. "Migrate our auth from session cookies to JWT" — analyzer first; the shape isn't knowable without reading the current auth flow end-to-end.

## Team protocol

<protocol>
1. `TeamCreate` before spawning any work.
2. `Task` with `team_name` for every teammate.
3. `SendMessage` for all coordination — plain text in your own output is invisible to teammates.
4. Shut down active teammates before `TeamDelete` — deleting a team with running work leaks state.
</protocol>

## Decomposition

First check `docs/plans/` (or a path passed in `$ARGUMENTS`) for an existing plan. A plan with file paths and acceptance criteria is the work breakdown — use it.

When decomposing yourself: **one file, one teammate.** If two units need the same file, merge them or assign the shared file to one unit and have the other depend on its output. Concurrent edits to shared files cause merge conflicts that cost more than the parallelism saves.

## Analysis phase

<analyzer_constraints>
Analyzers are read-only: `Glob`, `Grep`, `Read` only. Mixing analysis and editing in one pass produces fixes that miss the bigger picture.
</analyzer_constraints>

Each analyzer reports via `SendMessage` with:
- Current state of the relevant code.
- Specific changes needed, with `file:line` references.
- Edge cases and concrete implementation steps.

Wait for every analyzer to finish before spawning implementers. Partial reports lead to contradictory plans across units.

## Implementation phase

Each implementer receives the analyzer's report (or your direct instructions) as their contract. When an implementer asks a clarifying question, answer it — don't let them guess. Guessing at scale compounds into inconsistent implementations that surface at integration.

When a question reveals the plan is wrong — not just ambiguous — pause the unit, revise the contract, relay back. An implementer executing a broken contract produces confidently wrong code.

## Quality

After all implementers complete, in parallel:
- `/qual` teammate — multi-lens quality analysis on changed files.
- `/qg` teammate — quality gates (format, lint, typecheck, tests, build).

If issues surface: spawn fix teammates for critical/high issues, re-run `/qg`, repeat. Escalate to the user when the same gate fails 3 times.

## Report

```
## Summary
<what was accomplished>

### Work Units
| Unit | Status | Files |
|------|--------|-------|

### Quality
| Check | Status | Issues |
|-------|--------|--------|
| /qual | PASS/FAIL | N critical, N high |
| /qg | PASS/FAIL | details |

### Issues / Deferred
<if any>
```
