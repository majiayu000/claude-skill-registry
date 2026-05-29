---
name: beads-state
description: Git-friendly, crash-recoverable state persistence for the Gastown orchestration chipset. Manages agent identities, work items, hooks, convoys, and merge requests as JSON files with atomic write operations.
---

# Beads State Persistence

Filesystem-backed state management for multi-agent orchestration. All state is stored as individual JSON files using atomic write operations. No database dependencies.

## State Entities

### Agent Identity

**Path:** `.chipset/state/agents/{id}.json`

Persistent record of an agent in the topology. Contains role, rig assignment, hook pointer, lifecycle status, and optional ephemeral session ID.

```typescript
interface AgentIdentity {
  id: string;           // Unique identifier (e.g., 'polecat-alpha')
  role: AgentRole;      // mayor | witness | refinery | polecat | crew
  rig: string;          // Parent rig name
  hookId: string;       // Pointer to hook bead in state/hooks/
  status: AgentStatus;  // idle | active | stalled | terminated
  sessionId?: string;   // Present only while agent is active
}
```

### Work Item

**Path:** `.chipset/state/work/{bead-id}.json`

A unit of work flowing through the dispatch pipeline. Created by the mayor, assigned via hooks, tracked through lifecycle.

```typescript
interface WorkItem {
  beadId: string;          // Bead-style ID (prefix-xxxxx)
  title: string;
  description: string;
  status: WorkStatus;      // open | hooked | in_progress | done | merged
  assignee?: string;       // Agent ID (undefined if unassigned)
  hookStatus: HookStatus;  // empty | pending | active | completed
  priority: 'P1' | 'P2' | 'P3';
}
```

### Hook

**Path:** `.chipset/state/hooks/{agent-id}.json`

Current work assignment for an agent. Enforces GUPP (Get Up and Push Protocol) -- one agent, one work item at a time.

```typescript
interface HookState {
  agentId: string;
  status: HookStatus;
  workItem?: WorkItem;     // Present when hook is pending/active
  lastActivity: string;    // ISO 8601 timestamp
}
```

**Constraint:** An agent can hold at most one hook at a time. Setting a new hook on an agent that already has an active hook is rejected. The caller must clear the existing hook first.

### Convoy

**Path:** `.chipset/state/convoys/{id}.json`

Groups related work items for batch tracking. The mayor creates convoys to organize beads and monitor aggregate progress.

```typescript
interface Convoy {
  id: string;
  name: string;
  beadIds: string[];
  progress: number;     // 0.0 to 1.0
  createdAt: string;    // ISO 8601
}
```

### Merge Request

**Path:** `.chipset/state/merge-queue/{id}.json`

Queued for the refinery. Processed strictly sequentially -- no parallel merges. Conflicts block the queue and escalate.

```typescript
interface MergeRequest {
  id: string;
  sourceBranch: string;
  targetBranch: string;
  status: 'pending' | 'merging' | 'merged' | 'conflicted';
  beadId: string;
}
```

## Filesystem Layout

```
.chipset/state/
  agents/          Agent identity JSON files
  hooks/           GUPP hook state per agent
  work/            Work item beads
  convoys/         Batch tracking
  merge-queue/     Refinery merge requests
```

Each entity is a single JSON file. The directory structure acts as the "table" -- listing files is the equivalent of a database scan.

## Durability Contract

### Atomic Writes

All mutations follow a three-step atomic write protocol:

1. **Write** content to a temporary file in the same directory (`.{name}.tmp`)
2. **Fsync** the temporary file to ensure data reaches disk
3. **Rename** the temporary file to the target path (atomic on POSIX filesystems)

This guarantees that a reader always sees either the complete old state or the complete new state, never a partial write. If the process crashes between steps 1-2, only the temp file is left (cleaned up on next startup). If it crashes between steps 2-3, the temp file contains the full new state and can be recovered.

### JSON Format

All JSON output uses `JSON.stringify` with sorted keys. This produces deterministic output that creates clean, minimal diffs when tracked by git. Sorted keys also make manual inspection easier -- fields appear in a predictable order.

```typescript
// Sorted-key serialization
function serialize(data: unknown): string {
  return JSON.stringify(data, Object.keys(data as object).sort(), 2);
}
```

### No Database Dependencies

State is filesystem-only. No SQLite, no LevelDB, no external services. This means:

- State is readable with `cat` and editable with any text editor
- State is trackable by git (JSON diffs show exactly what changed)
- State survives any process crash (atomic writes prevent corruption)
- State works across all platforms (POSIX rename semantics)
- State requires no setup beyond `mkdir -p`

## StateManager API

The StateManager class provides typed CRUD operations for all state entities.

### Construction

```typescript
const manager = new StateManager({ stateDir: '.chipset/state/' });
```

The `stateDir` parameter is configurable. The manager creates subdirectories on first use.

### Agent Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `createAgent` | `(role, rig) => AgentIdentity` | Generate unique ID, write agent JSON |
| `getAgent` | `(id) => AgentIdentity \| null` | Read agent by ID, null if not found |
| `updateAgentStatus` | `(id, status) => void` | Atomic status update |
| `listAgents` | `(filter?) => AgentIdentity[]` | List all agents, optional role/rig filter |

### Work Item Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `createWorkItem` | `(title, description, priority?) => WorkItem` | Generate bead ID, write work JSON |
| `getWorkItem` | `(beadId) => WorkItem \| null` | Read work item by bead ID |
| `updateWorkStatus` | `(beadId, status) => void` | Atomic status update |

### Hook Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `setHook` | `(agentId, beadId) => void` | Assign work to agent (single assignment enforced) |
| `getHook` | `(agentId) => HookState \| null` | Read hook state for agent |
| `clearHook` | `(agentId) => void` | Remove hook assignment |

### Convoy Operations

| Method | Signature | Description |
|--------|-----------|-------------|
| `createConvoy` | `(name, beadIds) => Convoy` | Create batch with member beads |
| `getConvoy` | `(id) => Convoy \| null` | Read convoy by ID |
| `updateConvoyProgress` | `(id) => void` | Recalculate progress from member bead statuses |

## Error Handling

- **File not found:** Returns `null` for get operations. Never throws on missing state.
- **Concurrent writes:** Last writer wins (rename is atomic). For coordination, use the convoy or hook layer.
- **Corrupt JSON:** Log warning, return `null`. Caller decides recovery strategy.
- **Disk full:** Propagates OS error. Temp file cleanup is best-effort.

## Usage Patterns

### Create and Assign Work

```typescript
const agent = await manager.createAgent('polecat', 'my-rig');
const item = await manager.createWorkItem('Fix auth bug', 'JWT expiry not handled', 'P1');
await manager.setHook(agent.id, item.beadId);
```

### Track Convoy Progress

```typescript
const convoy = await manager.createConvoy('Sprint 1', [item1.beadId, item2.beadId]);
// ... after some work completes ...
await manager.updateConvoyProgress(convoy.id);
const updated = await manager.getConvoy(convoy.id);
console.log(`Progress: ${(updated!.progress * 100).toFixed(0)}%`);
```

### Filter Agents by Role

```typescript
const polecats = await manager.listAgents({ role: 'polecat' });
const idle = polecats.filter(a => a.status === 'idle');
```
