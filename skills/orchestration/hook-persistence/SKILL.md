---
name: hook-persistence
description: Pull-based work assignment channel implementing GUPP (Get Up and Push Protocol). Manages single-active-work-item hooks per agent with filesystem persistence and atomic state transitions.
---

# Hook Persistence

Filesystem-backed work assignment for multi-agent orchestration. Each agent has exactly one hook file that tracks its current work item. The hook enforces GUPP -- Get Up and Push Protocol -- meaning an agent with hooked work must execute it before accepting new assignments.

## Purpose

Hook is the work assignment channel in the Gastown chipset -- the MMIO (Memory-Mapped I/O) equivalent. It is the mechanism by which the mayor dispatches work to agents and tracks assignment state. Unlike mail (which sends notifications about work) or nudge (which checks on work), the hook is the work itself -- the binding between an agent and a bead.

The hook is pull-based: the agent polls its hook file on startup and periodically thereafter. If the hook has a work item, the agent picks it up and begins execution. This pull model means agents self-schedule -- the mayor sets the hook, and the agent activates when ready.

## Filesystem Contract

```
.chipset/state/hooks/{agent-id}.json
```

Each agent has exactly one hook file. The file contains the agent's current assignment state: empty (no work), pending (work assigned but not started), active (work in progress), or completed (work finished, awaiting retirement).

**Example paths:**

```
.chipset/state/hooks/polecat-alpha.json
.chipset/state/hooks/polecat-bravo.json
.chipset/state/hooks/refinery-f5g6h.json
```

## Hook Format

```json
{
  "agent_id": "polecat-alpha",
  "status": "active",
  "work_item": {
    "bead_id": "gt-abc12",
    "title": "Add README section",
    "assigned_at": "2026-03-05T10:30:00Z"
  },
  "last_activity": "2026-03-05T10:32:00Z"
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | yes | Agent this hook belongs to |
| `status` | string | yes | Hook lifecycle status (see Status Lifecycle) |
| `work_item` | object or null | yes | Current work assignment (null when empty) |
| `last_activity` | string | yes | ISO 8601 timestamp of last state change |

### Work Item Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `bead_id` | string | yes | Work item bead identifier |
| `title` | string | yes | Short description of the work |
| `assigned_at` | string | yes | ISO 8601 timestamp of assignment |

## Status Lifecycle

```
empty --> pending --> active --> completed --> empty
```

| Status | Meaning | Transitions To |
|--------|---------|---------------|
| `empty` | No work assigned. Agent is idle. | `pending` (mayor assigns work) |
| `pending` | Work assigned, agent not yet started. | `active` (agent picks up work) |
| `active` | Agent is executing the work item. | `completed` (agent finishes work) |
| `completed` | Work finished, awaiting retirement. | `empty` (hook cleared after done) |

### Transition Rules

- **empty to pending:** Only the mayor (or sling dispatcher) can set a hook
- **pending to active:** Only the owning agent can activate its own hook
- **active to completed:** Only the owning agent can complete its own hook
- **completed to empty:** Mayor clears the hook after verifying completion
- **No skipping:** Transitions must follow the lifecycle order
- **No parallel hooks:** An agent can hold at most one hook at a time

## Setting a Hook

The mayor (or sling dispatcher) assigns work by writing to the agent's hook file.

### Protocol

1. **Read** the agent's current hook state
2. **Verify** the hook is empty (reject if active or pending)
3. **Construct** the new hook with status `pending` and work item details
4. **Write** atomically using write-then-rename

### Pseudocode

```typescript
async function setHook(
  agentId: string,
  beadId: string,
  title: string
): Promise<void> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);
  const existing = await readJson<HookFile>(hookPath);

  if (existing && (existing.status === 'active' || existing.status === 'pending')) {
    throw new Error(
      `Agent ${agentId} already has a ${existing.status} hook. ` +
      `Clear it before assigning new work.`
    );
  }

  const hook: HookFile = {
    agent_id: agentId,
    status: 'pending',
    work_item: {
      bead_id: beadId,
      title,
      assigned_at: new Date().toISOString(),
    },
    last_activity: new Date().toISOString(),
  };

  await atomicWrite(hookPath, serializeSorted(hook));
}
```

## Polling a Hook

Agents check their hook on startup and periodically during execution.

### Startup Poll

```typescript
async function checkHook(agentId: string): Promise<HookFile | null> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);
  return readJson<HookFile>(hookPath);
}
```

### GUPP Enforcement

When an agent polls and finds a pending hook, GUPP activates:

```typescript
async function enforceGupp(agentId: string): Promise<void> {
  const hook = await checkHook(agentId);
  if (!hook) return;

  if (hook.status === 'pending') {
    // GUPP: agent MUST execute this work
    await activateHook(agentId);
    await executeWork(hook.work_item);
    await completeHook(agentId);
  }
}
```

GUPP means the agent has no choice -- if the hook has work, the agent executes it. This prevents agents from cherry-picking work or ignoring assignments.

## Activating a Hook

When an agent begins work, it transitions the hook from `pending` to `active`.

```typescript
async function activateHook(agentId: string): Promise<void> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);
  const hook = await readJson<HookFile>(hookPath);
  if (!hook || hook.status !== 'pending') {
    throw new Error(`Cannot activate: hook is ${hook?.status ?? 'missing'}`);
  }

  hook.status = 'active';
  hook.last_activity = new Date().toISOString();
  await atomicWrite(hookPath, serializeSorted(hook));
}
```

## Completing a Hook

When an agent finishes work, it transitions the hook from `active` to `completed`.

```typescript
async function completeHook(agentId: string): Promise<void> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);
  const hook = await readJson<HookFile>(hookPath);
  if (!hook || hook.status !== 'active') {
    throw new Error(`Cannot complete: hook is ${hook?.status ?? 'missing'}`);
  }

  hook.status = 'completed';
  hook.last_activity = new Date().toISOString();
  await atomicWrite(hookPath, serializeSorted(hook));
}
```

## Clearing a Hook

After the mayor verifies completion (or decides to reassign), the hook is cleared by resetting to empty.

```typescript
async function clearHook(agentId: string): Promise<void> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);

  const hook: HookFile = {
    agent_id: agentId,
    status: 'empty',
    work_item: null,
    last_activity: new Date().toISOString(),
  };

  await atomicWrite(hookPath, serializeSorted(hook));
}
```

Note: Clearing writes an empty hook rather than deleting the file. This preserves the agent's hook presence in the filesystem for monitoring purposes.

## Updating Activity

Agents update `last_activity` periodically while working to signal liveness. The witness monitors this timestamp to detect stalls.

```typescript
async function touchHook(agentId: string): Promise<void> {
  const hookPath = join(stateDir, 'hooks', `${agentId}.json`);
  const hook = await readJson<HookFile>(hookPath);
  if (!hook || hook.status !== 'active') return;

  hook.last_activity = new Date().toISOString();
  await atomicWrite(hookPath, serializeSorted(hook));
}
```

## GUPP Integration

GUPP (Get Up and Push Protocol) is the enforcement mechanism that ensures agents execute hooked work. The hook file is the GUPP contract:

1. **Mayor sets hook** with status `pending`
2. **Agent polls** and finds pending work
3. **GUPP activates:** Agent MUST begin execution (no deferral, no rejection)
4. **Agent activates hook** (status becomes `active`)
5. **Agent executes work** and updates `last_activity` periodically
6. **Agent completes hook** (status becomes `completed`)
7. **Agent sends completion mail** to mayor
8. **Mayor clears hook** after verification

If the agent fails to activate within the expected window, the witness detects via `last_activity` staleness and nudges the agent. If the nudge goes unanswered, the witness escalates to the mayor.

## Cross-Channel Integration

Hook is the assignment layer in the three-channel system:

| Channel | Role | Data Flow |
|---------|------|-----------|
| **Hook** (this skill) | Assignment | Mayor sets work; agent polls and executes |
| **Mail** (mail-async) | Context | Mayor sends details; agent sends completion report |
| **Nudge** (nudge-sync) | Monitoring | Witness checks agent liveness via heartbeat |

### Full Dispatch Flow

```
1. Mayor creates work item (beads-state)
2. Sling selects agent (dispatch logic)
3. Mayor sets hook on agent (hook-persistence)
4. Mayor sends work_assignment mail (mail-async)
5. Agent polls hook, finds pending work
6. Agent activates hook, reads mail for context
7. Agent executes work, touches hook periodically
8. Agent completes hook
9. Agent sends completion_report mail to mayor
10. Mayor verifies, clears hook
11. Agent returns to idle
```

## Error Handling

| Condition | Behavior |
|-----------|----------|
| Hook file doesn't exist | Returns null (agent has no assignment) |
| Hook already active | Reject new assignment with error |
| Corrupt hook JSON | Returns null, treated as no hook |
| Agent crashes mid-work | Hook stays `active`; witness detects via stale `last_activity` |
| Mayor clears active hook | Allowed (reassignment scenario) |
| Concurrent hook writes | Last writer wins (atomic rename) |

## Constraints

- **Filesystem only:** No sockets, no tmux, no network
- **Single assignment:** One hook per agent, one work item per hook
- **Pull-based:** Agent polls for work; mayor does not push execution
- **GUPP enforced:** Agent cannot reject or defer hooked work
- **Ordered transitions:** Status must follow the lifecycle order
- **Activity tracking:** `last_activity` must be updated during active work
- **Cleared, not deleted:** Empty hooks write a reset file rather than removing the file
