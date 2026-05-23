---
name: refinery-merge
description: DMA merge queue pattern for sequential, deterministic merge request processing. Checks out branches, rebases onto main, runs tests, merges, and pushes. Never auto-resolves conflicts.
type: skill
category: workflow
status: stable
origin: tibsfox
modified: false
first_seen: 2026-03-06
first_path: .claude/skills/refinery-merge/SKILL.md
superseded_by: null
---
# Refinery Merge

Sequential merge queue processor for completed polecat branches. The refinery is the DMA controller of the Gastown chipset -- it moves data (code changes) from producer (polecat branches) to consumer (main branch) without CPU (mayor) intervention during normal operations. The pipeline is deterministic: checkout, rebase, test, merge, push. Merge conflicts block the queue and escalate; they are never auto-resolved.

## Activation Triggers

This skill activates when:

- The merge queue has pending merge requests from completed polecats
- A polecat calls done and its branch needs to be merged into main
- The refinery is assigned to process a rig's merge queue
- Merge queue depth exceeds a threshold and processing is needed

## Core Capabilities

### Sequential MR Processing

The refinery processes merge requests one at a time in strict FIFO order. No parallel merges. No priority reordering. The queue is a pipeline, not a pool.

**Queue processing loop:**

```typescript
const state = new StateManager({ stateDir: '.chipset/state/' });

async function processQueue(): Promise<void> {
  // Get pending MRs in FIFO order
  const pending = await listMergeRequests('pending');

  if (pending.length === 0) {
    // Queue empty -- nothing to process
    return;
  }

  // Process the oldest MR first (strict FIFO)
  const mr = pending[0];
  await processMergeRequest(mr);
}
```

### Rebase-Test-Merge Pipeline

Each merge request flows through a five-stage pipeline. Every stage must succeed before advancing to the next.

```
CHECKOUT        REBASE          TEST            MERGE           PUSH
   |               |              |               |               |
   v               v              v               v               v
get branch -> rebase onto  -> run tests  -> merge to main -> push remote
              current main    (if configured)                close bead
```

**Stage 1 -- Checkout:**

```typescript
async function processMergeRequest(mr: MergeRequest): Promise<void> {
  // Update MR status to 'merging'
  // Checkout the source branch
  // git checkout {mr.sourceBranch}
```

**Stage 2 -- Rebase:**

```typescript
  // Rebase onto current main
  // git rebase {mr.targetBranch}
  //
  // If rebase fails (conflicts):
  //   git rebase --abort
  //   Mark MR as 'conflicted'
  //   Block queue
  //   Escalate to mayor/witness
  //   RETURN (do not proceed)
```

**Stage 3 -- Test:**

```typescript
  // Run configured test suite
  // npm test (or project-specific command)
  //
  // If tests fail:
  //   Mark MR as 'conflicted' (test failure = logical conflict)
  //   Block queue
  //   Escalate to mayor
  //   RETURN
```

**Stage 4 -- Merge:**

```typescript
  // Fast-forward merge onto main (after successful rebase, this is always FF)
  // git checkout {mr.targetBranch}
  // git merge {mr.sourceBranch}
```

**Stage 5 -- Push and close:**

```typescript
  // Push main to remote
  // git push origin {mr.targetBranch}

  // Close the MR bead
  // Update MR status to 'merged'

  // Update the source work item
  await state.updateWorkStatus(mr.beadId, 'merged');

  // Notify mayor of successful merge
  const successMail: AgentMessage = {
    from: refineryId,
    to: 'mayor',
    channel: 'mail',
    payload: `MERGED: ${mr.beadId} - ${mr.sourceBranch} into ${mr.targetBranch}`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
}
```

### Conflict Handling

When a rebase produces conflicts or tests fail, the refinery does NOT attempt resolution. It blocks the queue and escalates.

**Conflict protocol:**

```typescript
async function handleConflict(mr: MergeRequest, reason: string): Promise<void> {
  // 1. Abort the rebase
  // git rebase --abort

  // 2. Mark MR as conflicted
  // Update MR status to 'conflicted'

  // 3. Block the queue (subsequent MRs wait until this is resolved)

  // 4. Escalate to mayor and witness
  const conflictMail: AgentMessage = {
    from: refineryId,
    to: 'mayor',
    channel: 'mail',
    payload: `CONFLICT: ${mr.beadId} - ${mr.sourceBranch} conflicts with ${mr.targetBranch}: ${reason}`,
    timestamp: new Date().toISOString(),
    durable: true,
  };

  const witnessMail: AgentMessage = {
    from: refineryId,
    to: 'witness',
    channel: 'mail',
    payload: `QUEUE_BLOCKED: conflict on ${mr.beadId}, awaiting resolution`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
}
```

**Why no auto-resolution:** Merge conflicts represent disagreements between two code paths. Resolving them requires understanding the intent of both changes. The refinery is a deterministic pipeline -- it has no judgment about code semantics. Auto-resolution would introduce silent bugs.

### Bead Lifecycle Management

On successful merge, the refinery closes the merge request bead and updates the source work item.

```typescript
// After successful merge + push:

// 1. Update MR status
// mr.status = 'merged'

// 2. Update source work item
await state.updateWorkStatus(mr.beadId, 'merged');

// 3. Report to mayor
// (included in the push stage above)
```

### Queue Depth Monitoring

The refinery tracks queue depth and reports to the witness/mayor when the queue grows beyond expected bounds.

```typescript
async function checkQueueHealth(): Promise<void> {
  const pending = await listMergeRequests('pending');
  const conflicted = await listMergeRequests('conflicted');

  if (conflicted.length > 0) {
    // Queue is blocked -- already escalated
    return;
  }

  if (pending.length > 10) {
    // Queue depth warning
    const depthAlert: AgentMessage = {
      from: refineryId,
      to: 'mayor',
      channel: 'mail',
      payload: `QUEUE_DEPTH: ${pending.length} MRs pending, processing may be slow`,
      timestamp: new Date().toISOString(),
      durable: true,
    };
  }
}
```

## Communication Protocol

### Messages the Refinery SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `mail` | Mayor | Merge success notifications | Durable |
| `mail` | Mayor | Conflict escalations | Durable |
| `mail` | Witness | Queue blocked notifications | Durable |

### Messages the Refinery RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| `mail` | Polecats (via done) | MR notification (new branch ready for merge) |
| `mail` | Mayor | Queue management instructions (resume after conflict resolution) |

## Error Handling

### Rebase Conflicts

Abort the rebase, mark MR as conflicted, block queue, escalate. The queue remains blocked until the mayor resolves the conflict (manually or by reassigning a polecat to fix it).

### Test Failures

Same as rebase conflicts: mark as conflicted, block queue, escalate. The refinery does not diagnose test failures -- it reports them.

### Push Failures

If the push to remote fails (network error, permissions), retry once. If the retry fails, mark as conflicted and escalate. The merge was successful locally, so the branch state is preserved.

### Queue Resume

After a conflict is resolved (mayor or human fixes the conflict and signals the refinery), the refinery:

1. Retries the conflicted MR from the checkout stage
2. If successful, continues processing the remaining queue
3. If still conflicted, re-escalates

## Boundary: What the Refinery Does NOT Do

The refinery NEVER:

- **Auto-resolves merge conflicts** -- conflicts require human or mayor judgment
- **Reorders the queue** -- FIFO is strict; no priority bumping
- **Runs in parallel** -- one MR at a time; serialization prevents race conditions
- **Makes code changes** -- the refinery moves code between branches; it does not author code
- **Decides merge strategy** -- rebase-then-fast-forward is the only strategy; the refinery does not choose between squash, merge commit, or rebase
- **Skips tests** -- if tests are configured, they run; failures block the queue

The refinery is a pipeline. Data goes in one end and comes out the other in a predictable, deterministic sequence. If the pipeline encounters something it cannot handle, it stops and asks for help.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `mayor-coordinator` | Mayor receives merge results FROM refinery |
| `polecat-worker` | Polecat branches feed INTO refinery queue via done |
| `witness-observer` | Witness receives queue-blocked notifications FROM refinery |
| `beads-state` | Refinery uses StateManager for MR and work item status updates |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's refinery.go pipeline
- `references/boundaries.md` -- No auto-resolution, FIFO constraints, pipeline-only scope
