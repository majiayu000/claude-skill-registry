---
name: done-retirement
description: Pipeline retirement protocol for completed work items. Implements a 7-stage validate-commit-push-submit-notify-cleanup-terminate pipeline with irreversibility after push. Done means gone.
---

# Done Retirement

Pipeline retirement processor for the Gastown chipset. When a polecat finishes its work, the done retirement pipeline takes over -- it validates the work, commits and pushes the branch, creates a merge request, notifies the convoy and mayor, cleans up the workspace, and terminates the agent. In hardware terms, done retirement is the **instruction retirement unit** -- it takes completed instructions from the execution unit (polecat), writes results to the register file (shared repository), updates the reorder buffer (merge queue), and frees execution resources (workspace and agent slot).

## Activation Triggers

This skill activates when:

- A polecat has completed execution and is ready to retire its work
- An agent's hook status transitions to `completed`
- A work item's status transitions to `done`
- A convoy needs to track individual bead completion

## Core Capabilities

### The 7-Stage Retirement Pipeline

Every retirement flows through seven stages in strict order. The pipeline has an irreversibility boundary at Stage 3 (Push). Before push, the retirement can be aborted and the bead returned to `in_progress`. After push, the process is irreversible -- the branch is in the shared repository and the workspace will be destroyed.

```
VALIDATE      COMMIT        PUSH          SUBMIT        NOTIFY        CLEANUP      TERMINATE
   |             |            |              |             |             |             |
   v             v            v              v             v             v             v
verify work   ensure all   push branch   create merge  send mail to  remove work   mark agent
is actually   changes are  to shared     request       convoy/mayor  directory     as idle or
complete      committed    repository    record in     and witness   and context   terminated,
(criteria     to working   (IRREVERSIBLE state                                    release
met)          branch       AFTER THIS)                                            resources
```

**Stage 1 -- Validate:**

Verify that the work is actually complete. The bead's acceptance criteria must be met before the retirement pipeline begins. Validation checks the work item's done criteria against the actual state of the working branch.

```typescript
const state = new StateManager({ stateDir: '.chipset/state/' });

async function validateCompletion(
  agentId: string,
  beadId: string
): Promise<ValidationResult> {
  const workItem = await state.getWorkItem(beadId);
  const hook = await state.getHook(agentId);

  // Work item must exist and be in progress
  if (!workItem || workItem.status !== 'in_progress') {
    return { valid: false, reason: `Work item ${beadId} is not in_progress` };
  }

  // Hook must be active for this agent
  if (!hook || hook.status !== 'active') {
    return { valid: false, reason: `No active hook for agent ${agentId}` };
  }

  // Check that the agent is the assigned worker
  if (workItem.assignee !== agentId) {
    return { valid: false, reason: `Agent ${agentId} is not assigned to ${beadId}` };
  }

  return { valid: true };
}
```

Validation failures are non-destructive. The bead stays `in_progress` and the polecat continues working. The polecat should not call done until its acceptance criteria are met.

**Stage 2 -- Commit:**

Ensure all changes are committed to the working branch. If there are uncommitted changes, commit them with a summary message. If the working tree is clean, this stage is a no-op.

```typescript
async function ensureCommitted(
  context: WorkspaceContext
): Promise<void> {
  // Check for uncommitted changes
  // git status --porcelain
  // If output is non-empty, commit with a summary message

  // Verify the branch has at least one commit
  // git log --oneline -1 polecat/{beadId}
  // If no commits, validation should have caught this (Stage 1)
}
```

The commit stage ensures no work is lost. Even partial work gets committed before the branch is pushed. The commit message follows the project's conventional commit format.

**Stage 3 -- Push:**

Push the working branch to the shared repository. This is the point of no return.

```typescript
async function pushBranch(context: WorkspaceContext): Promise<void> {
  // Push the polecat's branch to remote
  // git push origin polecat/{beadId}

  // Update work item status to 'done'
  await state.updateWorkStatus(context.beadId, 'done');
}
```

**IRREVERSIBILITY BOUNDARY:** After the push completes, the retirement process cannot be undone. The branch exists in the shared repository and serves as the durable artifact of the polecat's work. All subsequent stages (submit, notify, cleanup, terminate) are consequences of this push. Even if they fail, the work is preserved in the remote branch.

The push uses the write-then-rename pattern for the state update: the work item status file is written to a temporary location, fsynced, and renamed atomically. A crash during push leaves either the old status (`in_progress`) or the new status (`done`), never a partial state.

**Stage 4 -- Submit:**

Create a merge request record in the state for the refinery to process. The merge request links the polecat's branch to the target branch and queues it for sequential merge processing.

```typescript
async function submitMergeRequest(
  context: WorkspaceContext
): Promise<MergeRequest> {
  const mr: MergeRequest = {
    id: `mr-${context.beadId}`,
    sourceBranch: `polecat/${context.beadId}`,
    targetBranch: 'main',
    status: 'pending',
    beadId: context.beadId,
  };

  // Write MR record atomically
  const mrPath = join(stateDir, 'merge-queue', `${mr.id}.json`);
  await atomicWrite(mrPath, serializeSorted(mr));

  return mr;
}
```

The merge request is a state record, not a Git platform PR. The refinery reads these records from the `state/merge-queue/` directory and processes them in FIFO order. The refinery skill handles the actual rebase-test-merge pipeline.

**Stage 5 -- Notify:**

Send completion notifications to the convoy, mayor, and witness. These messages provide the audit trail for the work item's completion.

```typescript
async function notifyCompletion(
  context: WorkspaceContext,
  mr: MergeRequest,
  convoyId?: string
): Promise<void> {
  // Notify mayor of completion
  const mayorMail: AgentMessage = {
    from: context.agentId,
    to: 'mayor',
    channel: 'mail',
    payload: `DONE: ${context.beadId} - branch ${mr.sourceBranch} pushed, MR ${mr.id} submitted`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  await sendMail(mayorMail);

  // Notify witness for monitoring records
  const witnessMail: AgentMessage = {
    from: context.agentId,
    to: 'witness',
    channel: 'mail',
    payload: `RETIRED: ${context.beadId} - agent ${context.agentId} completing retirement`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  await sendMail(witnessMail);

  // Update convoy progress if part of a batch
  if (convoyId) {
    await state.updateConvoyProgress(convoyId);
  }
}
```

Notifications use the mail-async durable messaging channel. Messages persist on disk and survive agent termination -- the mayor and witness can read them even after the polecat is gone.

**Stage 6 -- Cleanup:**

Remove the working directory and execution context. After cleanup, the polecat's local workspace no longer exists. The branch in the shared repository is the only artifact.

```typescript
async function cleanupWorkspace(
  context: WorkspaceContext
): Promise<void> {
  // Clear the agent's hook (work is done)
  await state.clearHook(context.agentId);

  // Remove the dispatch record (dispatch lifecycle complete)
  const dispatchPath = join(stateDir, 'dispatch', `${context.beadId}.json`);
  await removeFile(dispatchPath);

  // Remove worktree or working directory
  // git worktree remove polecat/{beadId} --force
  // (or equivalent workspace teardown)
}
```

Cleanup is destructive by design. The polecat's local state -- worktree, context files, dispatch records -- is deleted. "Done means gone" applies to the workspace: there is no going back to inspect local state after cleanup. If the work needs revision, a new polecat is spawned with a fresh workspace.

**Stage 7 -- Terminate:**

Mark the agent as idle or terminated and release its resources back to the pool. After termination, the polecat's identity record reflects its completed lifecycle.

```typescript
async function terminateAgent(
  context: WorkspaceContext
): Promise<void> {
  // Mark agent as terminated
  await state.updateAgentStatus(context.agentId, 'terminated');

  // Update hook to completed -> empty transition
  // (already cleared in cleanup, but ensure consistency)
  const hookPath = join(stateDir, 'hooks', `${context.agentId}.json`);
  const hook = await readJson(hookPath);
  if (hook && hook.status !== 'empty') {
    await state.clearHook(context.agentId);
  }
}
```

Termination is the final lifecycle transition. The polecat goes from `active` to `terminated`. There is no re-activation. If more work needs to be done, the mayor spawns a new polecat through the sling dispatch pipeline.

### "Done Means Gone" Principle

The irreversibility contract is the core design principle of the done retirement pipeline:

1. **Before push (Stages 1-2):** The retirement can be aborted. The bead returns to `in_progress` and the polecat continues working. No permanent side effects.

2. **At push (Stage 3):** The point of no return. The branch reaches the shared repository. The work item status transitions to `done`.

3. **After push (Stages 4-7):** Consequences unfold. The merge request is created, notifications sent, workspace destroyed, agent terminated. Each of these stages can fail individually without compromising the work -- the branch is already safe in the remote.

```
Stages 1-2:  REVERSIBLE    (abort returns to in_progress)
Stage 3:     COMMITMENT    (push to remote, status = done)
Stages 4-7:  CONSEQUENCES  (submit, notify, cleanup, terminate)
```

If any consequence stage fails (e.g., mail delivery failure in Stage 5), the work is still done. The failure is logged and the mayor can retry the notification manually. The push is the only stage that truly matters for durability.

### Convoy Progress Tracking

When a bead belongs to a convoy (batch dispatch), its completion updates the convoy's aggregate progress.

```typescript
async function updateConvoyProgress(convoyId: string): Promise<void> {
  const convoy = await state.getConvoy(convoyId);
  if (!convoy) return;

  // Count completed beads
  let completed = 0;
  for (const beadId of convoy.beadIds) {
    const workItem = await state.getWorkItem(beadId);
    if (workItem && (workItem.status === 'done' || workItem.status === 'merged')) {
      completed++;
    }
  }

  // Update progress (0.0 to 1.0)
  convoy.progress = completed / convoy.beadIds.length;
  await state.updateConvoy(convoy);
}
```

The mayor monitors convoy progress to determine when all beads in a batch are done. A convoy is complete when `progress === 1.0` (all beads are `done` or `merged`).

### Integration with Refinery Merge Queue

The done retirement pipeline feeds into the refinery's merge queue at Stage 4 (Submit). The merge request record created by done retirement is the input to the refinery's checkout-rebase-test-merge-push pipeline.

```
Done Retirement                    Refinery Merge

Stage 4: Submit MR ──────────────> Queue: pending
                                       |
                                   Checkout branch
                                       |
                                   Rebase onto main
                                       |
                                   Run tests
                                       |
                                   Merge to main
                                       |
                                   Push remote
                                       |
                                   Status: merged
```

The done retirement pipeline does not wait for the refinery to merge. It submits the MR and moves on to cleanup and termination. The refinery processes the queue asynchronously.

## Communication Protocol

### Messages Done Retirement SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `mail` | Mayor | Completion report with MR details | Durable |
| `mail` | Witness | Retirement notification for monitoring | Durable |
| `handoff` | Refinery | Merge request record in merge queue | Durable |

### Messages Done Retirement RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| (none) | | Done retirement is invoked by the polecat, not triggered by messages |

The polecat invokes the done retirement pipeline directly when its work is complete. There is no external message that triggers retirement -- the polecat decides when it is done.

## Retirement Lifecycle

```
POLECAT COMPLETES WORK:

  hook (active) --> [validate] --> [commit] --> [push] --> [submit MR] --> [notify] --> [cleanup] --> [terminate]
                                                 |
                                          IRREVERSIBLE
                                          AFTER THIS
                                                 |
                                          bead (done)
                                          branch (remote)
                                          workspace (destroyed)
                                          agent (terminated)
```

## Error Handling

### Validation Failure

If validation fails (Stage 1), the retirement is rejected. The bead stays `in_progress` and the polecat should continue working until acceptance criteria are met. This is not an error -- it is the expected response to premature retirement.

### Commit Failure

If the commit stage fails (Stage 2), likely due to filesystem issues, the retirement halts. The bead stays `in_progress`. The polecat should retry after resolving the filesystem issue.

### Push Failure

If the push fails (Stage 3), retry once. If the retry fails (network error, permission denied), halt the retirement and escalate to the mayor. The bead stays `in_progress` (push did not complete). This is the most critical failure point -- the work exists locally but has not reached the shared repository.

### Post-Push Failures

If any stage after push fails (Stages 4-7), the work is already safe in the remote. Log the failure and continue with subsequent stages. The mayor can manually create the MR, send notifications, or clean up the workspace. These failures are inconvenient but not dangerous.

### Partial Retirement Recovery

If the process crashes mid-retirement:

- **Before push:** No recovery needed. The bead is still `in_progress` and the polecat can retry the entire pipeline.
- **After push, before submit:** The branch exists in remote but no MR was created. The mayor can detect this by checking for branches without corresponding MRs and create the MR manually.
- **After submit:** The MR exists. Cleanup and termination can be retried by inspecting the work item status (`done`) and the agent's hook state.

## Boundary: What Done Retirement Does NOT Do

Done retirement NEVER:

- **Merges code** -- the refinery handles merging; done retirement submits the MR
- **Decides when work is complete** -- the polecat decides; done retirement validates
- **Re-assigns work** -- the mayor handles reassignment; done retirement terminates
- **Preserves local state** -- done means gone; the workspace is destroyed
- **Reverses after push** -- the irreversibility contract is absolute

Done retirement is the exit ramp. The polecat takes it when work is complete, and there is no U-turn after the push.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `polecat-worker` | Polecat invokes done retirement when work is complete |
| `refinery-merge` | Refinery processes the MR submitted by done retirement |
| `mayor-coordinator` | Mayor receives completion notification from done retirement |
| `witness-observer` | Witness receives retirement notification for monitoring |
| `hook-persistence` | Done retirement clears the polecat's hook (Stage 6) |
| `mail-async` | Done retirement uses mail for completion and retirement notifications |
| `beads-state` | Done retirement updates work item status and convoy progress |
| `sling-dispatch` | Sling dispatch is the other end of the lifecycle (dispatch feeds into retirement) |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's done.go completion pipeline
