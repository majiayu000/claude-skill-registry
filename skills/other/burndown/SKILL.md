---
name: burndown
description: Drive a finite epic set to all-merged, then stop.
practices:
- continuous-delivery
- xp
- agile-manifesto
hexagonal_role: domain
consumes:
- beads
- rpi
- implement
- post-mortem
produces:
- .agents/burndown/*.json
- git-changes
context_rel:
- kind: shared-kernel
  with: standards
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: execution
  dependencies:
  - beads
  - rpi
  - implement
  - post-mortem
output_contract: merged PRs for every in-scope bead + a completion report; the loop STOPS at the finite end (target merged, max-cycles, or surfaced blocker)
---

# /burndown — Bounded Epic-Completion Loop

> Pick a finite target. Drive every bead in it to merged. Stop when it's done.

`/burndown` is the **terminating** counterpart to [`/evolve`](../evolve/SKILL.md).
Where `/evolve` is open-ended (a goal-driven compounding loop that goes *dormant*
but never *completes*), `/burndown` takes a **finite target** — one epic, a set of
epics, or an explicit bead list — and drives every in-scope bead to **merged on
main**, then **STOPS**. It is the orchestrator-merge loop with a finish line.

**You must execute this workflow. Do not just describe it.**

## When to use which

| You want… | Command |
|---|---|
| Drive *this specific* epic/set to completion, then stop | **`/burndown`** |
| Always-on, whole-repo improvement against GOALS.md (no finish line) | `/evolve` |
| One-shot **parallel** fan-out of an epic's ready beads into swarm waves | `/crank` |
| Define/validate the PROGRAM.md contract the loops read | `/autodev` |
| One bead, full lifecycle, once | `/rpi` |

`/burndown` is **serial and resumable** (one PR in flight, idempotent across
firings) where `/crank` is **parallel and one-shot**. `/burndown` may *call*
`/crank` for a single wave-able bead, and calls `/rpi` per bead by default.

## Invocation

```bash
/burndown <epic-id>                      # drive every bead under the epic to merged, then stop
/burndown <epic-id> --max-cycles=20      # cap the number of bead-cycles
/burndown <epic-a> <epic-b> ...          # a finite set of epics (frontier order = arg order)
/burndown --beads ag-x.1,ag-x.2,ag-x.3   # an explicit finite bead list
/burndown <epic-id> --dry-run            # show the in-scope frontier + plan, don't execute
/burndown <epic-id> --hold-merges        # open PRs but leave green ones for operator review
```

The **target set** = the transitive in-scope beads of the arguments (epic
children, recursively) that are not already closed. This set is fixed at start
and is the loop's definition of "done."

## Per-cycle algorithm (idempotent — safe to fire from cron, `ScheduleWakeup`, or in-session)

Each firing does **one** of: merge an outstanding PR, finish, or advance one bead.

1. **Reconcile in-flight work (idempotency).**
   `git worktree list` + `git status`. If a prior cycle / agent is still
   mid-edit → **SKIP** this firing.
   If a target tick-PR is **OPEN**, check `gh pr checks`:
   - **all required green** → bring the branch up to date, `gh pr merge <N>
     --squash --admin`, record cited provenance on its bead (close it only if its
     acceptance is fully met — partial slices stay open), remove the worktree,
     then **STOP this firing** (one merge per cycle).
   - **pending** → SKIP. **red** → fix-and-repush or revert; never merge red.
   - `--hold-merges` → leave the green PR for the operator; log and STOP.
   Never pick new work while a target PR is outstanding.

2. **Completion check (the finite end `/evolve` lacks).**
   Re-resolve the target set. If **every in-scope bead is closed/merged** →
   write the completion report, run teardown, and **STOP — DONE**.
   If `--max-cycles=N` reached → STOP with a handoff (remaining beads listed).

3. **Select ONE ready bead within target scope only.**
   `bd ready` filtered to the target set, in frontier order (arg/priority/dep
   order). **No open-ended ladder** — do not pull goals, coverage, or bug-hunt
   work from outside the target. If no in-scope bead is ready but the target is
   incomplete, **surface the blocker** (the remaining beads are blocked on a
   dependency or an operator decision) and STOP — do not spin or widen scope.
   Claim it: `bd update <id> --status in_progress`.

4. **Drive that one bead to a PR.**
   In a fresh worktree off `origin/main`
   (`bd worktree create <slug> --branch <type>/<bead>-<slug>`): prefer
   `/rpi "Land <id>: <title>" --auto --max-cycles=1` (full lifecycle) when scope
   is fuzzy; a direct TDD slice (first failing test → smallest green change) when
   the bead is execution-ready. Run the repo gates (`cd cli && make test && go
   vet ./...`; `env -u AGENTOPS_RPI_RUNTIME scripts/pre-push-gate.sh --fast`).
   Open a PR citing the bead (trailers `Closes-scenario` / `Bounded-context` /
   `Evidence`). **Landing happens on a later cycle via step 1** — do not block on
   CI within this firing.

5. **Log the cycle** to `.agents/burndown/cycle-history.jsonl` and loop.

## Finite stop conditions

`/burndown` STOPS (it does not go dormant) on the first of:

1. **Target merged** — every in-scope bead closed/merged. Primary success.
2. **`--max-cycles=N`** cap reached — STOP with a handoff listing remaining beads.
3. **Operator override** — `~/.config/burndown/STOP` / `.agents/burndown/STOP`,
   or `--hold-merges` for the merge step only.
4. **Genuine blocker** — all remaining in-scope beads are blocked on a dependency
   or an operator decision. Surface it; do not spin.

## Self-perpetuation

For unattended completion, fire the same `/burndown <target>` prompt on a cadence
— a `CronCreate` session loop (idle-tick) or an end-of-turn `ScheduleWakeup`.
Because every firing is idempotent (step 1 reconciles the single outstanding PR),
repeated firings drive the target to completion without stacking PRs or
double-work. Tune the cadence to CI latency: a tick that mostly waits on CI
should fire no faster than the gate takes to go green.

## Hard constraints (inherited from PROGRAM.md + AGENTS.md)

- No bead, no PR — `bd create` discovered work before editing.
- One bead-backed vertical slice per PR; first failing test before the change.
- Worktree-mandatory; never edit the shared checkout directly.
- Green CI is the only merge gate; never merge red.
- New skills need the dual-runtime triad (`skills/`, `skills-codex/`,
  `skills-codex-overrides/` when it must differ) + `scripts/audit-codex-parity.sh`.
- Capture through the promotion ratchet; record deferred follow-ups in bd.

## Example

```bash
/burndown ag-a81zu --max-cycles=20
```

Drives the AgentOps × Claude Managed Agents epic: each cycle merges the prior
green PR or advances the next in-scope bead through `/rpi` → PR; STOPS when every
child bead of `ag-a81zu` is merged or 20 cycles elapse, emitting a completion
report (merged beads, remaining beads, blockers).

## See Also

- [`/evolve`](../evolve/SKILL.md) — open-ended compounding sibling (no finish line)
- [`/crank`](../crank/SKILL.md) — parallel-wave one-shot epic execution
- [`/rpi`](../rpi/SKILL.md) — per-bead full lifecycle (the default per-cycle engine)
- [`/autodev`](../autodev/SKILL.md) — the PROGRAM.md contract the loop reads
