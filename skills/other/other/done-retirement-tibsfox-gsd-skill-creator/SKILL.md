---
name: done-retirement
description: Pipeline retirement protocol for completed work items. Implements a 7-stage validate-commit-push-submit-notify-cleanup-terminate pipeline with irreversibility after push. Done means gone.
format: 2025-10-02
version: 1.0.0
status: active
updated: 2026-04-15
---

# Done Retirement

Pipeline retirement processor for the Gastown chipset. When a polecat finishes its work, this pipeline validates, commits, pushes, submits an MR, notifies, cleans up, and terminates. In hardware terms, it is the **instruction retirement unit** — writing results to the register file (shared repository), updating the reorder buffer (merge queue), and freeing execution resources.

## Activation Triggers

This skill activates when:

- A polecat has completed execution and is ready to retire its work
- An agent's hook status transitions to `completed`
- A work item's status transitions to `done`
- A convoy needs to track individual bead completion

## The 7-Stage Retirement Pipeline

Every retirement flows through seven stages in strict order. The pipeline has an **irreversibility boundary at Stage 3 (Push)**. Before push, the retirement can be aborted and the bead returned to `in_progress`. After push, the process is irreversible — the branch is in the shared repository and the workspace will be destroyed.

| # | Stage | Purpose |
|---|-------|---------|
| 1 | Validate | Verify work meets acceptance criteria; reject premature retirement. |
| 2 | Commit | Ensure all changes are committed to the working branch. |
| 3 | **Push** | **Push branch to shared repository. IRREVERSIBLE AFTER THIS.** Work item status → `done`. |
| 4 | Submit | Create merge request record in the refinery's merge queue. |
| 5 | Notify | Send completion mail to mayor, witness, and convoy. |
| 6 | Cleanup | Destroy worktree, clear hook, remove dispatch record. |
| 7 | Terminate | Mark agent as terminated; release resources back to the pool. |

Stages: `VALIDATE → COMMIT → PUSH → SUBMIT → NOTIFY → CLEANUP → TERMINATE`.

Full TypeScript implementations live in [`references/retirement-implementation.md`](references/retirement-implementation.md).

## "Done Means Gone" — Irreversibility Rules

The irreversibility contract is the core design principle of this pipeline and **MUST remain active at all times**:

1. **Before push (Stages 1-2):** The retirement can be aborted. The bead returns to `in_progress` and the polecat continues working. No permanent side effects.
2. **At push (Stage 3):** The point of no return. The branch reaches the shared repository. The work item status transitions to `done`.
3. **After push (Stages 4-7):** Consequences unfold. The merge request is created, notifications sent, workspace destroyed, agent terminated. Each of these stages can fail individually without compromising the work — the branch is already safe in the remote.

```
Stages 1-2:  REVERSIBLE    (abort returns to in_progress)
Stage 3:     COMMITMENT    (push to remote, status = done)
Stages 4-7:  CONSEQUENCES  (submit, notify, cleanup, terminate)
```

If any consequence stage fails (e.g., mail delivery failure in Stage 5), the work is still done. The failure is logged and the mayor can retry the notification manually. The push is the only stage that truly matters for durability.

**Cleanup is destructive by design.** The polecat's local state — worktree, context files, dispatch records — is deleted. There is no going back to inspect local state after cleanup. If the work needs revision, a new polecat is spawned with a fresh workspace.

**Termination is the final lifecycle transition.** The polecat goes from `active` to `terminated`. There is no re-activation.

## Convoy Progress Tracking

When a bead belongs to a convoy (batch dispatch), its completion updates the convoy's aggregate progress. The mayor monitors convoy progress to determine when all beads in a batch are done. A convoy is complete when all beads reach `done` or `merged` status.

## Communication Protocol

Done retirement is invoked by the polecat itself when work is complete — there is no external trigger message. On the outbound side, it sends durable `mail` to the mayor (completion report with MR details) and the witness (retirement notification), and a `handoff` record to the refinery via the merge queue.

## Boundary: What Done Retirement Does NOT Do

Done retirement does not merge code (the refinery does), decide when work is complete (the polecat does), re-assign work (the mayor handles reassignment), preserve local state ("done means gone"), or reverse after push (the irreversibility contract is absolute). It is the exit ramp — and there is no U-turn after the push.

## Integration with Other Gastown Skills

Invoked by `polecat-worker` when work is complete. Feeds `refinery-merge` via the merge queue (Stage 4). Uses `hook-persistence` to clear the polecat's hook (Stage 6) and `mail-async` for notifications (Stage 5). Reads and writes `beads-state` for work items and convoy progress. `sling-dispatch` is the other end of the lifecycle — dispatch feeds into retirement.

## References

Implementation detail moved to:

- [`references/retirement-implementation.md`](references/retirement-implementation.md) — full TypeScript code for all 7 stages, convoy tracking, refinery integration, and error handling.
- [`references/gastown-origin.md`](references/gastown-origin.md) — how this pattern derives from Gastown's `done.go` completion pipeline.
