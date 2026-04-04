---
name: mayor-coordinator
description: Northbridge coordination pattern for multi-agent orchestration. Creates convoys, dispatches work via sling, monitors progress, and handles escalations. Never executes work directly.
---

# Mayor Coordinator

Cross-rig coordinator for multi-agent orchestration topologies. The Mayor owns the convoy (batch of work items), dispatches work to polecats via the sling mechanism, monitors progress through agent status queries, and handles escalations from the witness. The Mayor is the Northbridge of the Gastown chipset -- it routes work between high-bandwidth components without performing computation itself.

## Activation Triggers

This skill activates when the task involves:

- Breaking work into parallel units for multiple agents
- Coordinating execution across two or more polecats
- Creating a convoy (batch of related work items)
- Monitoring aggregate progress across agents
- Handling escalations from a witness observer
- Deciding how to respond to stalled or failed agents

## Core Capabilities

### Convoy Management

A convoy groups related work items for batch tracking and dispatch. The mayor creates convoys, adds beads, and monitors aggregate completion.

**Creating a convoy:**

```typescript
import { StateManager } from '../../src/chipset/gastown/state-manager';

const state = new StateManager({ stateDir: '.chipset/state/' });

// Create individual work items
const item1 = await state.createWorkItem('Fix auth flow', 'JWT refresh broken', 'P1');
const item2 = await state.createWorkItem('Add rate limiting', 'API needs throttling', 'P2');
const item3 = await state.createWorkItem('Update docs', 'Auth docs stale', 'P3');

// Bundle into a convoy
const convoy = await state.createConvoy('Auth Sprint', [
  item1.beadId,
  item2.beadId,
  item3.beadId,
]);
```

**Monitoring convoy progress:**

```typescript
await state.updateConvoyProgress(convoy.id);
const updated = await state.getConvoy(convoy.id);
// updated.progress is 0.0 to 1.0 based on member bead statuses
```

### Agent Spawning and Dispatch

The mayor requests polecat allocation and assigns work via hooks. Each polecat gets exactly one hook (one work item at a time).

**Dispatch flow:**

1. Identify idle polecats: `state.listAgents({ role: 'polecat', status: 'idle' })`
2. If no idle polecats, request spawn: `state.createAgent('polecat', rigName)`
3. Assign work via hook: `state.setHook(agent.id, workItem.beadId)`
4. The polecat detects the hook and enters GUPP autonomous execution

**Work assignment example:**

```typescript
// Find available polecats
const idle = (await state.listAgents({ role: 'polecat' }))
  .filter(a => a.status === 'idle');

// Spawn more if needed
while (idle.length < convoy.beadIds.length) {
  const newAgent = await state.createAgent('polecat', 'my-rig');
  idle.push(newAgent);
}

// Dispatch: one bead per polecat
for (let i = 0; i < convoy.beadIds.length; i++) {
  const item = await state.getWorkItem(convoy.beadIds[i]);
  if (item && item.status === 'open') {
    await state.setHook(idle[i].id, item.beadId);
    await state.updateWorkStatus(item.beadId, 'hooked');
  }
}
```

### Progress Monitoring

The mayor periodically queries agent and convoy status to track overall execution.

**Status query pattern:**

```typescript
// Check all active agents
const active = await state.listAgents({ status: 'active' });
const stalled = await state.listAgents({ status: 'stalled' });

// Check convoy completion
const convoy = await state.getConvoy(convoyId);
if (convoy && convoy.progress === 1.0) {
  // All work complete -- convoy finished
}
```

### Escalation Handling

When the witness detects a stalled polecat or the refinery encounters a merge conflict, the mayor receives an escalation via mail and decides on action.

**Escalation response options:**

| Escalation Type | Source | Mayor Response |
|----------------|--------|----------------|
| Stalled agent | Witness | Nudge agent, or terminate and reassign work |
| Merge conflict | Refinery | Block queue, assess conflict, reassign or request human review |
| Agent terminated unexpectedly | Witness | Spawn replacement polecat, re-hook the work item |
| All polecats busy | Dispatch | Queue work or increase polecat pool |

**Handling a stalled agent:**

```typescript
// Witness reports agent-id is stalled
const hook = await state.getHook(stalledAgentId);
if (hook && hook.status === 'active') {
  // Option 1: Send nudge message
  const nudge: AgentMessage = {
    from: mayorId,
    to: stalledAgentId,
    channel: 'nudge',
    payload: 'Progress check: are you blocked?',
    timestamp: new Date().toISOString(),
    durable: false,
  };
  // Write nudge to filesystem
  // Option 2: If unresponsive, terminate and reassign
  await state.updateAgentStatus(stalledAgentId, 'terminated');
  await state.clearHook(stalledAgentId);
  // Re-dispatch the work item to a new polecat
}
```

## Communication Protocol

The mayor communicates exclusively through filesystem-based messaging. No tmux session injection, no direct process signals.

### Messages the Mayor SENDS

| Channel | Target | Purpose | Durability |
|---------|--------|---------|------------|
| `mail` | Any agent | Work assignments, instructions, status requests | Durable (filesystem) |
| `nudge` | Stuck agents | "Do your job" reminders | Non-durable |
| `hook` | Polecats | Work item assignment via hook state files | Durable (filesystem) |

### Messages the Mayor RECEIVES

| Channel | Source | Content |
|---------|--------|---------|
| `mail` | Polecats | Completion reports, status updates |
| `mail` | Witness | Stall alerts, health reports |
| `mail` | Refinery | Merge success/failure notifications |
| `nudge` | Witness | Urgent escalations |

### Message Format

All messages follow the `AgentMessage` interface from the shared type system:

```typescript
interface AgentMessage {
  from: string;       // Sender agent ID
  to: string;         // Recipient agent ID
  channel: MessageChannel;  // 'mail' | 'nudge' | 'hook' | 'handoff'
  payload: string;    // Message content
  timestamp: string;  // ISO 8601
  durable: boolean;   // Whether to persist to filesystem
}
```

Durable messages are written to `.chipset/state/mail/{to}/{timestamp}-{from}.json`.

## Convoy Lifecycle

```
CREATE          DISPATCH         MONITOR         COMPLETE
  |                |                |                |
  v                v                v                v
convoy.create -> sling beads -> query status -> all done?
                 to polecats    check stalls     -> yes: close convoy
                                handle alerts    -> no: continue monitoring
```

1. **Create:** Mayor bundles related beads into a convoy
2. **Dispatch:** Mayor assigns beads to polecats via hooks
3. **Monitor:** Mayor checks progress, handles escalations
4. **Complete:** When all beads reach `done` or `merged`, convoy is finished

## Error Handling

### Stuck Convoy Resolution

If a convoy stalls (progress unchanged for extended period):

1. Identify which beads are incomplete
2. Check assigned agents for stall status
3. For stalled agents: nudge, then terminate and reassign if unresponsive
4. For failed beads: assess whether to retry or escalate to human

### Partial Completion

If some beads in a convoy complete but others fail:

1. Record partial progress in convoy status
2. Report completed work to the human operator
3. Create a new convoy for remaining work if appropriate
4. Never silently drop failed beads

### Agent Pool Exhaustion

If all polecats are busy and work remains:

1. Queue remaining beads (do not over-allocate)
2. Monitor for polecat completion and dispatch queued work
3. Report queue depth to the operator if threshold exceeded

## Boundary: What the Mayor Does NOT Do

The mayor NEVER:

- **Executes work directly** -- no file editing, no code writing, no test running
- **Modifies source code** -- the mayor coordinates, polecats execute
- **Resolves merge conflicts** -- the refinery handles merges; conflicts escalate to human
- **Monitors agent health directly** -- the witness handles observation; mayor responds to witness reports
- **Makes architectural decisions** -- the mayor dispatches work per the plan; design decisions come from the human operator

The mayor is a coordinator. If it finds itself writing code, running tests, or editing files, something has gone wrong. Delegate to a polecat.

## Integration with Other Gastown Skills

| Skill | Relationship |
|-------|-------------|
| `polecat-worker` | Mayor dispatches work TO polecats via hooks |
| `witness-observer` | Witness reports TO mayor via mail/nudge |
| `refinery-merge` | Refinery reports merge results TO mayor via mail |
| `beads-state` | Mayor uses StateManager for all state operations |

## References

- `references/gastown-origin.md` -- How this pattern derives from Gastown's mayor.go
- `references/examples.md` -- Convoy creation, dispatch, and escalation examples
- `references/boundaries.md` -- Detailed boundary constraints and anti-patterns
