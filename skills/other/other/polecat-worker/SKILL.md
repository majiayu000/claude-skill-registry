---
name: polecat-worker
description: ALU execution pattern for ephemeral autonomous work. Detects hooked work, enters GUPP autonomous mode, executes the assigned bead, commits and pushes results, then self-terminates. Never coordinates other agents.
---

# Polecat Worker

Ephemeral execution unit for single-bead autonomous work. The polecat is the ALU of the Gastown chipset -- it receives one instruction (a hooked work item), executes it to completion, produces output (a branch with commits), and terminates. Polecats do not persist between tasks. Identity lives in the bead (git-backed state); the session is disposable.

## Activation Triggers

This skill activates when:

- A bead has been placed on this agent's hook (work assignment detected)
- The agent is operating in an isolated workspace (worktree or clean context)
- A single, well-defined work item needs autonomous execution
- The agent needs to follow the GUPP protocol (Get Up and Push)

## Core Capabilities

### GUPP Execution Flow

The Gas Town Universal Propulsion Principle defines the polecat's entire lifecycle. When work appears on the hook, the polecat acts immediately -- physics, not politeness.

**The four-step cycle:**

```
1. CHECK HOOK    Is there a bead on my hook?
       |              |
       no             yes
       |              |
    [idle]     2. ANNOUNCE
                      |
               3. EXECUTE
                      |
               4. DONE (terminate)
```

**Step 1 -- Check Hook:**

```typescript
const state = new StateManager({ stateDir: '.chipset/state/' });
const hook = await state.getHook(myAgentId);

if (!hook || hook.status === 'empty') {
  // No work assigned -- remain idle
  return;
}

// Work found -- enter GUPP mode
const workItem = hook.workItem;
```

**Step 2 -- Announce:**

```typescript
// Notify the mayor/convoy that work has started
await state.updateAgentStatus(myAgentId, 'active');
await state.updateWorkStatus(workItem.beadId, 'in_progress');

// Send mail to convoy
const announcement: AgentMessage = {
  from: myAgentId,
  to: 'mayor',
  channel: 'mail',
  payload: `STARTED: ${workItem.beadId} - ${workItem.title}`,
  timestamp: new Date().toISOString(),
  durable: true,
};
```

**Step 3 -- Execute:**

This is where the actual work happens. The polecat:

1. Creates a working branch: `git checkout -b polecat/{beadId}`
2. Performs the assigned work (code, tests, docs -- whatever the bead specifies)
3. Commits incrementally with conventional commit messages
4. Keeps working until the bead's acceptance criteria are met

The polecat works autonomously. It does not wait for approval between steps. It does not ask for permission. GUPP means: if the work is on your hook, you execute it.

**Step 4 -- Done:**

```typescript
// Push branch to remote
// git push origin polecat/{beadId}

// Update state
await state.updateWorkStatus(workItem.beadId, 'done');
await state.clearHook(myAgentId);
await state.updateAgentStatus(myAgentId, 'terminated');

// Send completion mail
const completion: AgentMessage = {
  from: myAgentId,
  to: 'mayor',
  channel: 'mail',
  payload: `DONE: ${workItem.beadId} - branch pushed, ready for merge`,
  timestamp: new Date().toISOString(),
  durable: true,
};
```

### Branch Management

Each polecat creates a dedicated branch for its work, commits incrementally, and pushes to remote on completion.

**Branch naming:** `polecat/{bead-id}` (e.g., `polecat/bead-a1b2c`)

**Commit strategy:**

- Commit early and often with meaningful messages
- Each commit should be atomic (one logical change)
- Follow the project's conventional commit format
- Never squash -- the refinery handles merge strategy

**Push timing:** Push only on completion (Step 4). Intermediate work stays local until the polecat calls done.

### Self-Termination

When work completes, the polecat terminates its own session. "Done means gone" -- there is no re-activation. The polecat's lifecycle is one-way:

```
spawned -> active -> done -> terminated
```

There is no "paused" state. There is no "reassigned" state. If a polecat's work needs to be reassigned, the mayor terminates the polecat and spawns a new one.

### Context Recovery on Restart

If the polecat's session restarts unexpectedly (process crash, context reset), it recovers by checking its hook:

```typescript
// On startup, always check hook first
const hook = await state.getHook(myAgentId);

if (hook && hook.status === 'active') {
  // Work was in progress -- resume from last commit
  // Check git log on the working branch to determine progress
  // Continue execution from where it left off
}

if (hook && hook.status === 'pending') {
  // Work was assigned but not started -- begin GUPP from step 2
}
```

The hook state file is the polecat's durable memory. The session is ephemeral; the hook survives.

## Communication Protocol

Polecats have minimal communication needs. They receive work and report completion. That is all.

### Messages the Polecat RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| `hook` | Sling (via mayor) | Work item assignment placed on hook |
| `nudge` | Witness or Mayor | "Are you still working?" health check |

### Messages the Polecat SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `mail` | Mayor / Convoy | Work started announcement | Durable |
| `mail` | Mayor / Convoy | Work completion report | Durable |

### Responding to Nudges

If the polecat receives a nudge while actively working, it sends a brief status update:

```typescript
// Nudge received from witness
const response: AgentMessage = {
  from: myAgentId,
  to: nudge.from,
  channel: 'mail',
  payload: `ACTIVE: working on ${currentBead.beadId}, last commit ${lastCommitHash}`,
  timestamp: new Date().toISOString(),
  durable: true,
};
```

## Polecat Lifecycle

```
SPAWN           HOOK            EXECUTE         DONE
  |               |                |               |
  v               v                v               v
created ->   detect work ->   autonomous ->   push + terminate
(idle)       (GUPP step 1)    execution       (one-way exit)
                              (steps 2-3)     (step 4)
```

The entire lifecycle is forward-only. A polecat never goes backward in this sequence.

## Error Handling

### Execution Failure

If the polecat encounters an error during execution:

1. Commit current progress (even if incomplete)
2. Push the branch (preserve work in remote)
3. Send failure mail to mayor with error details
4. Update work status and terminate

```typescript
// On execution error
await state.updateWorkStatus(workItem.beadId, 'done'); // mark as done (failed)
const failureMail: AgentMessage = {
  from: myAgentId,
  to: 'mayor',
  channel: 'mail',
  payload: `FAILED: ${workItem.beadId} - ${errorDescription}`,
  timestamp: new Date().toISOString(),
  durable: true,
};
await state.clearHook(myAgentId);
await state.updateAgentStatus(myAgentId, 'terminated');
```

### Context Window Exhaustion

If the polecat's context window fills before work is complete:

1. Commit and push all current progress
2. Send a status mail with progress summary
3. Terminate -- the mayor can spawn a fresh polecat to continue

### Hook Conflict

If the polecat detects a hook that references a non-existent or already-completed work item:

1. Clear the hook
2. Send an alert mail to the mayor
3. Return to idle (or terminate if no further work expected)

## Boundary: What the Polecat Does NOT Do

The polecat NEVER:

- **Coordinates other agents** -- no dispatching, no assigning, no scheduling
- **Creates convoys** -- convoy management is the mayor's responsibility
- **Monitors other agents** -- the polecat is not aware of other polecats
- **Resolves merge conflicts** -- the polecat pushes its branch; the refinery merges
- **Makes project-level decisions** -- the polecat executes the work described in its bead
- **Re-activates after termination** -- done means gone; spawn a new polecat instead

The polecat is a worker. It takes one task, does it, and stops. If it finds itself managing other agents or making coordination decisions, something has gone wrong.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `mayor-coordinator` | Mayor dispatches work TO polecat via hooks |
| `witness-observer` | Witness monitors polecat health, sends nudges |
| `refinery-merge` | Refinery processes polecat's completed branch |
| `beads-state` | Polecat uses StateManager for hook checks and status updates |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's polecat.go
- `references/examples.md` -- Hook detection, autonomous execution, branch+push+done
- `references/boundaries.md` -- No coordination, single bead scope, lifecycle constraints
