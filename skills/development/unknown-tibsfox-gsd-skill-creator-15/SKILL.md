---
name: sling-dispatch
description: Instruction dispatch pipeline for routing work items to available agents. Implements a 7-stage fetch-allocate-prepare-hook-store-launch-confirm pipeline with batch convoy mode, formula expansion, idempotent dispatch, and crash recovery.
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-25
triggers:
  - mayor needs to assign work items to available polecats
  - convoy of beads is ready for dispatch to a rig
  - formula template needs expansion into ordered dispatch steps
  - partial dispatch needs recovery after a crash or session restart
references_subdir: true
word_budget: 800
---

# Sling Dispatch

Instruction dispatch unit for the Gastown chipset. The sling routes a work item (bead) to an available polecat through a 7-stage pipeline. In hardware terms, the sling is the **instruction fetch-decode-dispatch unit** — it sets up the conditions for execution and confirms the dispatch was recorded, but does not execute work itself.

## Activation Triggers

This skill activates when:

- The mayor needs to assign work items to available polecats
- A convoy of beads is ready for dispatch to a rig
- A formula template needs expansion into ordered dispatch steps
- A partial dispatch needs recovery after a crash or session restart

## The 7-Stage Dispatch Pipeline

Every dispatch flows through seven stages in strict order. Each stage completes before the next begins. If any stage fails, the pipeline halts at that stage and the partial state is recoverable.

| # | Stage | Purpose |
|---|-------|---------|
| 1 | Fetch | Resolve bead ID to a work item; reject anything not in `open` status (idempotency). |
| 2 | Allocate | Select an idle polecat from the pool, or spawn a new one if the pool has capacity. |
| 3 | Prepare | Set up the polecat's isolated workspace (worktree + execution context). |
| 4 | Hook | Set work item status to `hooked` and bind it to the polecat. Idempotency boundary. |
| 5 | Store | Write dispatch arguments to durable state so a crash after this point is recoverable. |
| 6 | Launch | Start the polecat's agent session and send assignment mail. GUPP activates immediately. |
| 7 | Confirm | Record the bead-to-agent assignment in convoy tracking and notify the witness. |

Full TypeScript implementations live in [`references/pipeline-implementation.md`](references/pipeline-implementation.md).

## Batch Mode

When more than `batch_threshold` beads (default: 3, configurable in chipset YAML at `dispatch.batch_threshold`) target the same rig, the sling automatically batches them into a convoy and dispatches in parallel. The batch detection groups beads by target rig; groups exceeding the threshold become convoys. Dispatches within a batch run in parallel up to `max_parallel`. Convoy progress updates after each individual dispatch confirms.

## Formula Mode

When a formula (TOML template) is specified, the sling expands it into step-ordered beads before dispatching. Formulas define multi-step workflows as declarative sequences. Beads respect dependency ordering — steps with `depends_on` wait for their dependencies to reach `done` status before being dispatched. Steps without dependencies dispatch immediately.

## Idempotency

The sling is idempotent. Re-dispatching an already-hooked bead is a no-op:

- Stage 1 (Fetch) rejects any bead not in `open` status
- A bead transitions to `hooked` in Stage 4 and never returns to `open`
- Calling `dispatchSingle(beadId)` multiple times for the same bead has the same effect as calling it once
- No side effects on repeated calls — the second call returns immediately at Stage 1

This makes the dispatch pipeline safe to retry after crashes, timeouts, or duplicate requests.

## Crash Recovery

If the sling crashes mid-pipeline, the dispatch can be resumed from the durable state written in Stage 5 (Store). Records in the `stored` stage resume from Launch; records in the `launched` stage resume from Confirm; `confirmed` records are complete. All state updates use the write-then-rename pattern so partial writes are impossible.

## Communication Protocol

The sling is invoked by the mayor, not by external events. The mayor decides what to dispatch and when; the sling handles how. On the outbound side, the sling sends durable `mail` to the polecat (work assignment) and the witness (dispatch confirmation), and writes the polecat's `hook` record in Stage 4. Inbound, it only receives dispatch and batch-dispatch mail from the mayor.

## Boundary: What the Sling Does NOT Do

The sling dispatches; it does not execute work (the polecat does), decide what to dispatch (the mayor does), monitor agent progress (the witness does), resolve merge conflicts (the refinery does), or modify bead content. It fetches instructions, decodes them, assigns them to polecats, and confirms delivery.

## Integration with Other Gastown Skills

Invoked by `mayor-coordinator`; targets `polecat-worker` via `hook-persistence` (Stage 4) and `mail-async` (Stages 6-7). Uses `beads-state` (StateManager) for work items and dispatch records. Emits confirmations to `witness-observer`. `done-retirement` processes the other end of the lifecycle.

## References

Implementation detail moved to:

- [`references/pipeline-implementation.md`](references/pipeline-implementation.md) — full TypeScript code for all 7 stages, batch mode, formula expansion, crash recovery, and error handling.
- [`references/gastown-origin.md`](references/gastown-origin.md) — how this pattern derives from Gastown's `sling.go` dispatch system.
