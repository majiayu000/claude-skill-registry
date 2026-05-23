---
name: sling-dispatch
description: Instruction dispatch pipeline for routing work items to available agents. Implements a 7-stage fetch-allocate-prepare-hook-store-launch-confirm pipeline with batch convoy mode, formula expansion, idempotent dispatch, and crash recovery.
---

# Sling Dispatch

Instruction dispatch unit for the Gastown chipset. The sling takes a work item (bead) and routes it to an available polecat through a 7-stage pipeline. In hardware terms, the sling is the **instruction fetch-decode-dispatch unit** -- it resolves work items from state, selects an execution unit (polecat), prepares the execution context, and launches the agent. The sling does not execute work; it sets up the conditions for execution and confirms the dispatch was recorded.

## Activation Triggers

This skill activates when:

- The mayor needs to assign work items to available polecats
- A convoy of beads is ready for dispatch to a rig
- A formula template needs expansion into ordered dispatch steps
- A partial dispatch needs recovery after a crash or session restart

## Core Capabilities

### The 7-Stage Dispatch Pipeline

Every dispatch flows through seven stages in strict order. Each stage completes before the next begins. If any stage fails, the pipeline halts at that stage and the partial state is recoverable.

```
FETCH       ALLOCATE      PREPARE       HOOK         STORE        LAUNCH       CONFIRM
  |            |             |            |             |            |            |
  v            v             v            v             v            v            v
resolve    select or     create       update work   write args   start agent   record
bead ID    spawn idle    isolated     item status   to durable   session       dispatch
to work    polecat       workspace    to 'hooked',  state file   with GUPP     in convoy
item                     (dir+ctx)    set assignee  (crash-safe)  context      tracking
```

**Stage 1 -- Fetch:**

Resolve the bead ID to a concrete work item from state. The bead must exist and must be in `open` status. If the bead is already `hooked`, `in_progress`, or `done`, the dispatch is a no-op (idempotency guarantee).

```typescript
const state = new StateManager({ stateDir: '.chipset/state/' });

async function fetchBead(beadId: string): Promise<WorkItem | null> {
  const workItem = await state.getWorkItem(beadId);

  if (!workItem) {
    // Bead does not exist -- dispatch fails
    return null;
  }

  if (workItem.status !== 'open') {
    // Already dispatched or completed -- idempotent no-op
    return null;
  }

  return workItem;
}
```

**Stage 2 -- Allocate:**

Select an available polecat from the agent pool, or spawn a new one if the pool has capacity. The allocator prefers idle polecats over spawning new ones to minimize resource usage.

```typescript
async function allocatePolecat(rig: string): Promise<AgentIdentity | null> {
  // List all polecats for this rig
  const polecats = await state.listAgents({ role: 'polecat', rig });

  // Prefer idle polecats (already spawned, ready for work)
  const idle = polecats.filter(p => p.status === 'idle');
  if (idle.length > 0) {
    return idle[0];
  }

  // Check if we can spawn a new polecat (within max_parallel limit)
  const active = polecats.filter(p => p.status === 'active');
  const config = await state.getChipsetConfig();

  if (active.length >= config.dispatch.max_parallel) {
    // Pool is full -- cannot dispatch right now
    return null;
  }

  // Spawn a new polecat
  return state.createAgent({
    role: 'polecat',
    rig,
    status: 'idle',
  });
}
```

**Stage 3 -- Prepare:**

Create the isolated workspace for the polecat. This includes setting up the working directory (git worktree or clean checkout) and assembling the execution context (bead details, convoy membership, relevant file paths).

```typescript
async function prepareWorkspace(
  polecat: AgentIdentity,
  workItem: WorkItem
): Promise<WorkspaceContext> {
  // Create a working branch for the polecat
  const branchName = `polecat/${workItem.beadId}`;

  // Assemble the execution context
  const context: WorkspaceContext = {
    agentId: polecat.id,
    beadId: workItem.beadId,
    branch: branchName,
    title: workItem.title,
    description: workItem.description,
    priority: workItem.priority,
  };

  return context;
}
```

**Stage 4 -- Hook:**

Update the work item status to `hooked` and set the assignee. This is the binding step -- after this, the bead is claimed by the polecat and cannot be dispatched to another agent.

```typescript
async function hookBead(
  workItem: WorkItem,
  polecat: AgentIdentity
): Promise<void> {
  // Update work item status atomically
  workItem.status = 'hooked';
  workItem.assignee = polecat.id;
  workItem.hookStatus = 'pending';
  await state.updateWorkItem(workItem);

  // Set the polecat's hook
  await state.setHook(polecat.id, workItem.beadId, workItem.title);
}
```

This is the idempotency boundary. Re-dispatching a bead that is already `hooked` returns a no-op at Stage 1 (the fetch rejects non-`open` beads). The hook stage itself is atomic -- the work item status and hook file are written using the write-then-rename pattern.

**Stage 5 -- Store:**

Write the dispatch arguments to durable state. This creates a dispatch record that survives process crashes. If the sling crashes after Store but before Launch, the dispatch can be resumed from this record.

```typescript
interface DispatchRecord {
  beadId: string;
  agentId: string;
  branch: string;
  context: WorkspaceContext;
  stage: 'stored' | 'launched' | 'confirmed';
  createdAt: string;
}

async function storeDispatch(
  context: WorkspaceContext,
  polecat: AgentIdentity
): Promise<void> {
  const record: DispatchRecord = {
    beadId: context.beadId,
    agentId: polecat.id,
    branch: context.branch,
    context,
    stage: 'stored',
    createdAt: new Date().toISOString(),
  };

  // Write atomically to dispatch state
  const recordPath = join(stateDir, 'dispatch', `${context.beadId}.json`);
  await atomicWrite(recordPath, serializeSorted(record));
}
```

**Stage 6 -- Launch:**

Start the polecat's agent session with the GUPP execution context. The polecat receives its hook (set in Stage 4) and the dispatch context (stored in Stage 5). GUPP activates immediately -- the polecat begins work without waiting for confirmation.

```typescript
async function launchPolecat(
  polecat: AgentIdentity,
  context: WorkspaceContext
): Promise<void> {
  // Update agent status to active
  await state.updateAgentStatus(polecat.id, 'active');

  // Update dispatch record to 'launched'
  const recordPath = join(stateDir, 'dispatch', `${context.beadId}.json`);
  const record = await readJson<DispatchRecord>(recordPath);
  record.stage = 'launched';
  await atomicWrite(recordPath, serializeSorted(record));

  // Send work assignment mail to polecat
  const assignmentMail: AgentMessage = {
    from: 'mayor',
    to: polecat.id,
    channel: 'mail',
    payload: `ASSIGNED: ${context.beadId} - ${context.title}`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  await sendMail(assignmentMail);

  // The polecat detects the hook via polling and enters GUPP mode
}
```

**Stage 7 -- Confirm:**

Write the dispatch confirmation to convoy tracking. This closes the dispatch pipeline and records the bead-to-agent assignment in the convoy's progress state.

```typescript
async function confirmDispatch(
  context: WorkspaceContext,
  polecat: AgentIdentity,
  convoyId?: string
): Promise<void> {
  // Update dispatch record to 'confirmed'
  const recordPath = join(stateDir, 'dispatch', `${context.beadId}.json`);
  const record = await readJson<DispatchRecord>(recordPath);
  record.stage = 'confirmed';
  await atomicWrite(recordPath, serializeSorted(record));

  // If part of a convoy, update convoy progress
  if (convoyId) {
    await state.updateConvoyProgress(convoyId);
  }

  // Notify the witness of the new dispatch
  const witnessMail: AgentMessage = {
    from: 'mayor',
    to: 'witness',
    channel: 'mail',
    payload: `DISPATCH: ${context.beadId} -> ${polecat.id} on branch ${context.branch}`,
    timestamp: new Date().toISOString(),
    durable: true,
  };
  await sendMail(witnessMail);
}
```

### Batch Mode

When more than `batch_threshold` beads (default: 3, configurable in chipset YAML) target the same rig, the sling automatically batches them into a convoy and dispatches in parallel.

**Batch detection:**

```typescript
async function detectBatch(
  beads: WorkItem[],
  config: ChipsetConfig
): Promise<Map<string, WorkItem[]>> {
  // Group beads by target rig
  const rigGroups = new Map<string, WorkItem[]>();

  for (const bead of beads) {
    const rig = bead.rig ?? 'default';
    const group = rigGroups.get(rig) ?? [];
    group.push(bead);
    rigGroups.set(rig, group);
  }

  // Filter to groups exceeding batch threshold
  const batches = new Map<string, WorkItem[]>();
  for (const [rig, group] of rigGroups) {
    if (group.length > config.dispatch.batch_threshold) {
      batches.set(rig, group);
    }
  }

  return batches;
}
```

**Batch dispatch flow:**

1. Detect rig groups exceeding the `batch_threshold` (from `dispatch.batch_threshold` in chipset YAML)
2. Create a convoy for each batch with a descriptive name
3. Dispatch each bead in the batch through the 7-stage pipeline
4. Dispatches within a batch run in parallel (up to `max_parallel`)
5. Convoy progress updates after each individual dispatch confirms

```typescript
async function dispatchBatch(
  rig: string,
  beads: WorkItem[],
  config: ChipsetConfig
): Promise<void> {
  // Create convoy for this batch
  const convoy = await state.createConvoy({
    name: `batch-${rig}-${Date.now()}`,
    beadIds: beads.map(b => b.beadId),
  });

  // Dispatch each bead (parallel within max_parallel limit)
  const dispatches = beads.map(bead =>
    dispatchSingle(bead, rig, convoy.id)
  );

  // Execute up to max_parallel at a time
  await parallelLimit(dispatches, config.dispatch.max_parallel);
}
```

The `batch_threshold` is configurable via the chipset YAML at `dispatch.batch_threshold`. The default value of 3 means any rig receiving 4 or more beads triggers automatic batch mode.

### Formula Mode

When a formula (TOML template) is specified, the sling expands it into step-ordered beads before dispatching. Formulas define multi-step workflows as declarative sequences.

**Formula expansion:**

```typescript
interface FormulaStep {
  name: string;
  description: string;
  depends_on?: string[];  // Step names this step waits for
}

interface Formula {
  name: string;
  steps: FormulaStep[];
}

async function expandFormula(formula: Formula): Promise<WorkItem[]> {
  const beads: WorkItem[] = [];

  for (let i = 0; i < formula.steps.length; i++) {
    const step = formula.steps[i];
    const bead: WorkItem = {
      beadId: `formula-${formula.name}-step-${i + 1}`,
      title: step.name,
      description: step.description,
      status: 'open',
      hookStatus: 'empty',
      priority: 'P2',
    };
    beads.push(bead);
  }

  return beads;
}
```

**Formula dispatch ordering:**

Formula beads respect dependency ordering. Steps with `depends_on` wait for their dependencies to reach `done` status before being dispatched. Steps without dependencies dispatch immediately.

```typescript
async function dispatchFormula(formula: Formula): Promise<void> {
  const beads = await expandFormula(formula);

  // Dispatch independent steps first
  const independent = beads.filter((_, i) => !formula.steps[i].depends_on);
  for (const bead of independent) {
    await state.createWorkItem(bead);
    await dispatchSingle(bead);
  }

  // Dependent steps are dispatched by the mayor when their
  // dependencies complete (event-driven, not polled here)
}
```

### Idempotency

The sling is idempotent. Re-dispatching an already-hooked bead is a no-op.

**Idempotency contract:**

- Stage 1 (Fetch) rejects any bead not in `open` status
- A bead transitions to `hooked` in Stage 4 and never returns to `open`
- Calling `dispatchSingle(beadId)` multiple times for the same bead has the same effect as calling it once
- No side effects on repeated calls -- the second call returns immediately at Stage 1

This makes the dispatch pipeline safe to retry after crashes, timeouts, or duplicate requests.

### Crash Recovery

If the sling crashes mid-pipeline, the dispatch can be resumed from the durable state written in Stage 5 (Store).

**Recovery protocol:**

```typescript
async function recoverPartialDispatches(): Promise<void> {
  const dispatchDir = join(stateDir, 'dispatch');
  const records = await listJsonFiles(dispatchDir);

  for (const record of records) {
    if (record.stage === 'stored') {
      // Dispatch was stored but not launched -- resume from Stage 6
      const polecat = await state.getAgent(record.agentId);
      if (polecat) {
        await launchPolecat(polecat, record.context);
        await confirmDispatch(record.context, polecat);
      }
    }

    if (record.stage === 'launched') {
      // Dispatch was launched but not confirmed -- resume from Stage 7
      const polecat = await state.getAgent(record.agentId);
      if (polecat) {
        await confirmDispatch(record.context, polecat);
      }
    }

    // 'confirmed' records are complete -- no recovery needed
  }
}
```

**State file atomicity:** All state updates use the write-then-rename pattern. A crash during any write leaves either the old state (rename not yet called) or the new state (rename completed). Partial writes are impossible because the temporary file is written and fsynced before the atomic rename.

## Communication Protocol

### Messages the Sling SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `mail` | Polecat | Work assignment notification | Durable |
| `mail` | Witness | Dispatch confirmation for monitoring | Durable |
| `hook` | Polecat | Hook state set to pending (Stage 4) | Durable |

### Messages the Sling RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| `mail` | Mayor | Dispatch request with bead IDs |
| `mail` | Mayor | Batch dispatch request with convoy spec |

The sling is invoked by the mayor, not by external events. The mayor decides what to dispatch and when; the sling handles how.

## Dispatch Lifecycle

```
SINGLE DISPATCH:

  bead (open) --> [fetch] --> [allocate] --> [prepare] --> [hook] --> [store] --> [launch] --> [confirm]
                                                            |
                                                     bead (hooked)
                                                     hook (pending)

BATCH DISPATCH:

  N beads --> detect batch --> create convoy --> dispatch each (parallel) --> convoy progress updated

FORMULA DISPATCH:

  formula --> expand to beads --> order by dependency --> dispatch independent --> await deps --> dispatch dependent
```

## Error Handling

### No Available Polecat

If allocation fails (all polecats active, pool at max capacity), the dispatch halts at Stage 2. The bead remains `open` and can be retried when capacity frees up. The mayor receives a mail notification about the capacity constraint.

### Bead Not Found

If fetch fails (bead ID does not resolve to a work item), the dispatch is rejected immediately. No state changes occur.

### Hook Already Set

If the target polecat already has an active hook, allocation skips that polecat and selects another. If no polecat is available, the dispatch halts at Stage 2 (same as no available polecat).

### Partial Pipeline Failure

If any stage after Hook (stages 5-7) fails, the bead is already marked as `hooked`. The crash recovery protocol (above) handles resumption from the stored dispatch record. The bead does not return to `open` -- it stays `hooked` and the dispatch is retried from the failure point.

## Boundary: What the Sling Does NOT Do

The sling NEVER:

- **Executes work** -- the sling dispatches; the polecat executes
- **Decides what to dispatch** -- the mayor selects beads; the sling routes them
- **Monitors agent progress** -- the witness monitors; the sling dispatches
- **Resolves merge conflicts** -- the refinery merges; the sling dispatches
- **Modifies bead content** -- the sling reads bead details but never changes the work description

The sling is the instruction dispatch unit. It fetches instructions (beads), decodes them (resolves work items), dispatches them (assigns to polecats), and confirms delivery. It does not execute, monitor, or merge.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `mayor-coordinator` | Mayor invokes sling to dispatch work to polecats |
| `polecat-worker` | Polecat receives dispatched work via hook and mail |
| `witness-observer` | Witness receives dispatch confirmations for monitoring |
| `hook-persistence` | Sling uses hook-persistence to set agent hooks (Stage 4) |
| `mail-async` | Sling uses mail-async for assignment and confirmation messages |
| `beads-state` | Sling uses StateManager for work item and dispatch record persistence |
| `done-retirement` | Done retirement processes the other end of the lifecycle |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's sling.go dispatch system
