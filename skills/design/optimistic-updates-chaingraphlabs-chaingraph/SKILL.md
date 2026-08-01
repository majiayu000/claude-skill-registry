---
name: optimistic-updates
description: Optimistic UI patterns for ChainGraph frontend. Use when working on real-time
  collaboration, port value updates, node position syncing, debouncing, echo detection,
  or any client-server state synchroni
---

---
name: optimistic-updates
description: Optimistic UI patterns for ChainGraph frontend. Use when working on real-time collaboration, port value updates, node position syncing, debouncing, echo detection, or any client-server state synchronization. Covers 3-step echo detection, pending mutations, position interpolation. Triggers: optimistic, echo detection, pending mutation, debounce, throttle, position interpolation, staleness, real-time, collaboration.
---

# Optimistic Updates Patterns

This skill covers the optimistic update patterns used in ChainGraph frontend for responsive UI during client-server synchronization.

## Pattern Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    OPTIMISTIC UPDATE FLOW                     │
│                                                               │
│  User Input → Local Update → Server Request → Echo Detection │
│      │            │                │                 │        │
│      │            ▼                │                 ▼        │
│      │      Immediate UI           │         Filter Own Echo  │
│      │                             ▼                          │
│      │                      Server Confirms                   │
│      │                             │                          │
│      └─────────────────────────────┴──────────────────────────│
│                         Final State Consistent                │
└──────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Immediate Local Update
Update UI immediately when user acts, don't wait for server.

### 2. Debounced Server Sync
Batch rapid changes before sending to server.

### 3. Echo Detection
When server broadcasts the change back, filter out "echoes" of our own changes.

### 4. Pending Mutation Tracking
Track what we've sent to detect and match echoes correctly.

---

## Echo Detection (3-Step)

**File**: `apps/chaingraph-frontend/src/store/ports-v2/echo-detection.ts`

When a port update arrives from the server, it could be:
1. **Our own echo** - Confirmation of our optimistic update
2. **Stale update** - Older than our pending changes
3. **Other user's change** - Genuine new data to apply

### 3-Step Detection Algorithm

```typescript
// STEP 1: Mutation Match (own echo confirmation)
// Check if incoming update matches a pending mutation
const matchedMutation = pendingMutations.find(m =>
  m.version === event.version &&
  isDeepEqual(m.value, event.changes.value)
)

if (matchedMutation) {
  // This is our own echo - already applied optimistically
  confirmPendingMutation({ portKey, mutationId: matchedMutation.mutationId })
  return  // Don't re-apply
}

// STEP 2: Staleness Check
// Drop echoes older than our latest pending version
const latestPending = pendingMutations
  .sort((a, b) => b.version - a.version)[0]

if (latestPending && event.version < latestPending.version) {
  return  // Stale, drop it
}

// STEP 3: Duplicate Check
// Filter out unchanged data
const currentValue = $portValues.get(portKey)
if (isDeepEqual(currentValue, event.changes.value)) {
  return  // No change needed
}

// Apply the update
applyPortUpdate(event)
```

---

## Pending Mutations

**File**: `apps/chaingraph-frontend/src/store/ports-v2/pending-mutations.ts`

### PendingMutation Interface

```typescript
interface PendingMutation {
  portKey: string           // Port being mutated
  value: unknown            // Value sent to server
  version: number           // Expected version after mutation
  timestamp: number         // When mutation was sent
  mutationId: string        // Unique ID for echo matching
  clientId: string          // For multi-tab/multi-user support
}
```

### Store Structure

```typescript
// Store of pending mutations by portKey
// Multiple mutations can be pending during fast typing
export const $pendingPortMutations = portsV2Domain
  .createStore<Map<PortKey, PendingMutation[]>>(new Map())
  .reset(globalReset)

// Events
export const addPendingMutation = portsV2Domain.createEvent<PendingMutation>()
export const confirmPendingMutation = portsV2Domain.createEvent<{
  portKey: PortKey
  mutationId: string
}>()
export const rejectPendingMutation = portsV2Domain.createEvent<{
  portKey: PortKey
  mutationId: string
  reason: string
}>()
```

### Usage Pattern

```typescript
// When user changes a port value
function handlePortChange(portKey: string, newValue: unknown) {
  const mutationId = generateMutationId()
  const version = getCurrentVersion(portKey) + 1

  // 1. Track pending mutation
  addPendingMutation({
    portKey,
    value: newValue,
    version,
    timestamp: Date.now(),
    mutationId,
    clientId: getClientId(),
  })

  // 2. Apply optimistically
  updatePortValueLocal({ portKey, value: newValue })

  // 3. Send to server (debounced)
  debouncedServerUpdate({ portKey, value: newValue, version })
}
```

---

## Debounce/Throttle Constants

**File**: `apps/chaingraph-frontend/src/store/nodes/constants.ts`

```typescript
// Node position updates (drag)
export const NODE_POSITION_DEBOUNCE_MS = 500

// Node dimension updates (resize)
export const NODE_DIMENSIONS_DEBOUNCE_MS = 500

// Node UI metadata updates
export const NODE_UI_DEBOUNCE_MS = 250

// Local UI updates (very fast)
export const LOCAL_NODE_UI_DEBOUNCE_MS = 1000 / 90  // ~11ms

// Port value updates (throttle, not debounce)
export const PORT_VALUE_THROTTLE_MS = 500
```

### Debounce Pattern

```typescript
import { debounce } from 'patronum'

// Create debounced effect
const updateNodePositionFx = nodesDomain.createEffect(
  async (params: PositionUpdate) => {
    return trpcClient.flow.updateNodePosition.mutate(params)
  }
)

// Debounce the trigger
const debouncedPositionUpdate = debounce({
  source: nodePositionChanged,
  timeout: NODE_POSITION_DEBOUNCE_MS,
})

// Wire up
sample({
  clock: debouncedPositionUpdate,
  target: updateNodePositionFx,
})
```

---

## Position Interpolation

**File**: `apps/chaingraph-frontend/src/store/nodes/position-interpolation-advanced.ts`

Smooth animations for node positions during drag and server updates.

### Spring Physics Model

```typescript
class PositionInterpolator {
  // Spring configuration
  private tension = 180      // Spring stiffness
  private friction = 12      // Damping factor

  // State per node
  private positions: Map<string, { x: number, y: number }>
  private velocities: Map<string, { vx: number, vy: number }>
  private targets: Map<string, { x: number, y: number }>

  // Animate towards target
  update(nodeId: string, targetX: number, targetY: number) {
    this.targets.set(nodeId, { x: targetX, y: targetY })
    this.startAnimation()
  }

  private tick() {
    for (const [nodeId, target] of this.targets) {
      const pos = this.positions.get(nodeId)
      const vel = this.velocities.get(nodeId)

      // Spring force
      const dx = target.x - pos.x
      const dy = target.y - pos.y
      const ax = dx * this.tension - vel.vx * this.friction
      const ay = dy * this.tension - vel.vy * this.friction

      // Update velocity and position
      vel.vx += ax * dt
      vel.vy += ay * dt
      pos.x += vel.vx * dt
      pos.y += vel.vy * dt
    }
  }
}

export const positionInterpolator = new PositionInterpolator()
```

### Usage

```typescript
// When server sends position update
sample({
  clock: nodePositionReceived,
  fn: ({ nodeId, x, y }) => {
    // Interpolate to new position (smooth animation)
    positionInterpolator.update(nodeId, x, y)
  },
})

// When user drags node
sample({
  clock: nodeDragged,
  fn: ({ nodeId, x, y }) => {
    // Immediate update during drag (no interpolation)
    positionInterpolator.setImmediate(nodeId, x, y)
  },
})
```

---

## Optimistic Update Pattern (Complete)

### Port Value Update

```typescript
// 1. User types in port input
const handleInputChange = (portKey: string, value: string) => {
  // Generate mutation ID for tracking
  const mutationId = nanoid()

  // Track pending mutation
  addPendingMutation({
    portKey,
    value,
    version: nextVersion,
    timestamp: Date.now(),
    mutationId,
    clientId,
  })

  // Apply optimistically (immediate UI update)
  setPortValueLocal({ portKey, value })
}

// 2. Debounced server sync
sample({
  clock: debounce({ source: setPortValueLocal, timeout: 300 }),
  target: updatePortValueFx,
})

// 3. Server broadcasts update to all clients
// (including us - this is the "echo")

// 4. Echo detection filters our own update
sample({
  clock: portUpdateReceived,
  source: {
    pending: $pendingPortMutations,
    values: $portValues,
  },
  fn: ({ pending, values }, event) => {
    // 3-step echo detection
    const matched = findMatchingMutation(pending, event)
    if (matched) {
      return { confirm: matched.mutationId }
    }
    if (isStale(pending, event)) {
      return { drop: true }
    }
    if (isDuplicate(values, event)) {
      return { drop: true }
    }
    return { apply: event }
  },
  target: spread({
    confirm: confirmPendingMutation,
    apply: applyPortUpdate,
  }),
})
```

---

## Key Files

| File | Purpose |
|------|---------|
| `store/ports-v2/echo-detection.ts` | 3-step echo filtering |
| `store/ports-v2/pending-mutations.ts` | Mutation tracking |
| `store/nodes/position-interpolation-advanced.ts` | Smooth animations |
| `store/nodes/stores.ts` | Debounce constants |
| `store/flow/event-buffer.ts` | Event batching |

---

## Anti-Patterns

### Anti-Pattern #1: Not tracking mutations

```typescript
// ❌ BAD: No mutation tracking
const handleChange = (value) => {
  setPortValueLocal(value)      // Optimistic
  updatePortValueFx(value)      // Server
  // Echo will re-apply the same value!
}

// ✅ GOOD: Track pending mutations
const handleChange = (value) => {
  const mutationId = nanoid()
  addPendingMutation({ portKey, value, mutationId, ... })
  setPortValueLocal(value)
  updatePortValueFx(value)
  // Echo will be filtered by mutation match
}
```

### Anti-Pattern #2: Not debouncing rapid updates

```typescript
// ❌ BAD: Every keystroke hits server
input.oninput = (e) => {
  updateServerFx(e.target.value)  // 100s of requests!
}

// ✅ GOOD: Debounce server updates
input.oninput = (e) => {
  setLocalValue(e.target.value)  // Immediate UI
}

sample({
  clock: debounce({ source: setLocalValue, timeout: 300 }),
  target: updateServerFx,  // Batched request
})
```

### Anti-Pattern #3: Ignoring staleness

```typescript
// ❌ BAD: Apply all server updates
portUpdateReceived.watch((event) => {
  setPortValue(event.value)  // Might overwrite newer local value!
})

// ✅ GOOD: Check staleness
sample({
  clock: portUpdateReceived,
  source: $pendingPortMutations,
  filter: (pending, event) => {
    const latest = getLatestPendingVersion(pending, event.portKey)
    return !latest || event.version >= latest  // Not stale
  },
  target: applyPortUpdate,
})
```

---

## Quick Reference

| Need | Pattern | File |
|------|---------|------|
| Track local changes | `addPendingMutation()` | `pending-mutations.ts` |
| Filter echoes | 3-step detection | `echo-detection.ts` |
| Debounce updates | `debounce({ timeout: X })` | patronum |
| Smooth animations | `positionInterpolator` | `position-interpolation-advanced.ts` |
| Batch events | Event buffer | `event-buffer.ts` |

---

## Related Skills

- `effector-patterns` - Effector patterns for state management
- `subscription-sync` - Server subscription handling
- `frontend-architecture` - Overall frontend structure
- `port-system` - Port value management
