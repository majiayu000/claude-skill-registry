---
name: burndown
description: 'Drive a finite epic set to all-merged, then stop.'
---
# $burndown - Bounded Epic-Completion Loop (Codex Native)

> **Quick Ref:** Drive a finite target (epic / set of epics / explicit bead list) to every in-scope bead merged on `main`, one bead per cycle, then STOP. The terminating counterpart to `$evolve` (open-ended). Output: merged PRs + a completion report.

**You must execute this workflow. Do not just describe it.**

## When to use which

| You want… | Command |
|---|---|
| Drive *this specific* epic/set to completion, then stop | **`$burndown`** |
| Always-on, whole-repo improvement (no finish line) | `$evolve` |
| One-shot **parallel** fan-out of an epic into worker waves | `$crank` |
| Define/validate the PROGRAM.md contract | `$autodev` |
| One bead, full lifecycle, once | `$rpi` |

`$burndown` is **serial and resumable** (one PR in flight); `$crank` is
**parallel and one-shot**.

## Invocation

```bash
$burndown <epic-id>                    # drive the epic to merged, then stop
$burndown <epic-id> --max-cycles=20    # cap bead-cycles
$burndown <epic-a> <epic-b>            # finite set of epics
$burndown --beads ag-x.1,ag-x.2        # explicit bead list
$burndown <epic-id> --hold-merges      # open PRs, leave green for operator
```

The **target set** = transitive in-scope (non-closed) beads of the arguments,
fixed at start. It is the loop's definition of "done."

## Per-cycle algorithm (idempotent)

Each firing does ONE of: merge an outstanding PR, finish, or advance one bead.

1. **Reconcile in-flight.** `git worktree list` + `git status`; if mid-edit → SKIP.
   If a target PR is OPEN, check CI (`gh pr checks`):
   - all required green → update branch, `gh pr merge <N> --squash --admin`,
     record cited provenance, close the bead only if its acceptance is fully met,
     remove the worktree, STOP this firing.
   - pending → SKIP. red → fix-and-repush or revert; never merge red.
   - `--hold-merges` → leave green PR for operator; STOP.
   Never pick new work while a target PR is outstanding.
2. **Completion check.** Re-resolve the target set. All in-scope beads merged →
   write completion report and STOP (DONE). `--max-cycles=N` reached → STOP with
   handoff.
3. **Select ONE in-scope ready bead.** `bd ready` filtered to the target set, in
   frontier order. NO open-ended ladder. No ready in-scope bead but target
   incomplete → surface the blocker and STOP. Claim: `bd update <id> --status in_progress`.
4. **Drive to a PR.** Fresh worktree off `origin/main`. Codex runtime: drive the
   bead with an `ao rpi` cycle or a direct TDD slice; for a wave-able bead fan
   workers via NTM (`spawn_agent` / `wait_agent` / `close_agent`). First failing
   test before the change. Gates: `cd cli && make test && go vet ./...`;
   `env -u AGENTOPS_RPI_RUNTIME scripts/pre-push-gate.sh --fast`. Open a PR citing
   the bead (trailers `Closes-scenario` / `Bounded-context` / `Evidence`).
   Landing happens on a later cycle via step 1 — do not block on CI here.
5. **Log** to `.agents/burndown/cycle-history.jsonl` and loop.

## Finite stop conditions

STOPS (never dormant) on first of: target merged · `--max-cycles=N` · operator
STOP marker / `--hold-merges` · genuine blocker (remaining beads blocked on a
dependency or operator decision — surface, don't spin).

## Self-perpetuation

Fire the same `$burndown <target>` on a cadence (NTM pipeline tick, cron, or
ssh-to-bushido loop). Idempotency (step 1) makes repeated firings safe — no
stacked PRs, no double-work. Match cadence to CI latency.

## Hard constraints

No bead no PR; one vertical slice per PR; first failing test first;
worktree-mandatory; green CI is the only merge gate; dual-runtime triad for new
skills; capture via the promotion ratchet; record deferred follow-ups in bd.

## Backend Rules

- `bd` is the tracker; `bd ready --json` for in-scope selection; `bd worktree
  create` per bead.
- `gh` drives PR + merge; `--admin` only overrides the up-to-date (BEHIND)
  requirement when all required checks are green.
- Never send holdout `target`/`ground_truth`/PII to any cloud surface.
