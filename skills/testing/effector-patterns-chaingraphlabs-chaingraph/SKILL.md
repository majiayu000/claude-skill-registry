---
name: effector-patterns
description: Effector state management patterns and CRITICAL anti-patterns for ChainGraph
  frontend. Use when writing Effector stores, events, effects, samples, or any reactive
  state code. Contains anti-patterns to
---

---
name: effector-patterns
description: Effector state management patterns and CRITICAL anti-patterns for ChainGraph frontend. Use when writing Effector stores, events, effects, samples, or any reactive state code. Contains anti-patterns to AVOID like $store.getState(). Covers domains, patronum utilities, global reset. Triggers: effector, store, createStore, createEvent, createEffect, sample, combine, attach, domain, $, useUnit, getState, anti-pattern, patronum.
---

# Effector Patterns for ChainGraph

This skill covers Effector state management patterns used in the ChainGraph frontend, including **CRITICAL anti-patterns** that agents MUST avoid.

## Domain Organization

ChainGraph uses domain-based store organization. All domains are defined in:

**File**: `apps/chaingraph-frontend/src/store/domains.ts`

### All Domains

| Domain | Line | Purpose |
|--------|------|---------|
| `flowDomain` | 17 | Flow list, active flow, metadata |
| `nodesDomain` | 20 | Node CRUD, positions, dimensions |
| `edgesDomain` | 23 | Edge connections, anchors, selection |
| `executionDomain` | 26 | Execution state, events, control |
| `categoriesDomain` | 29 | Node categories, filtering |
| `portsDomain` | 32 | Legacy port management |
| `trpcDomain` | 35 | tRPC client instances |
| `archaiDomain` | 38 | ArchAI integration |
| `focusedEditorsDomain` | 41 | Port editor focus state |
| `dragDropDomain` | 44 | Drag & drop state |
| `mcpDomain` | 47 | MCP server management |
| `initializationDomain` | 50 | App initialization |
| `walletDomain` | 53 | Wallet integration |
| `hotkeysDomain` | hotkeys/stores.ts | Keyboard shortcuts (not in domains.ts) |
| `xyflowDomain` | xyflow/domain.ts | XYFlow render (not in domains.ts) |
| `perfTraceDomain` | perf-trace/domain.ts | Performance (not in domains.ts) |
| `portsV2Domain` | ports-v2/domain.ts:23 | Granular ports (not in domains.ts) |

### Creating a Domain

```typescript
import { createDomain } from 'effector'

// Naming: {feature}Domain with kebab-case internal name
export const myFeatureDomain = createDomain('my-feature')
```

---

## CRITICAL Anti-Patterns

### Anti-Pattern #1: Using `.getState()` in Store Reducers

**This is the most common mistake.** Found in 13+ files in the codebase.

```typescript
// ❌ BAD: .getState() in reducer breaks reactivity
const $compatiblePorts = portsDomain.createStore<string[] | null>(null)
  .on($draggingEdgePort, (state, draggingEdgePort) => {
    // This ONLY reads $nodes at call time, NOT reactively
    const nodes = Object.values($nodes.getState())  // ← ANTI-PATTERN
    // ...
    return compatiblePorts
  })
```

**Why it's wrong:**
- `.getState()` bypasses Effector's dependency tracking
- Updates to `$nodes` won't trigger updates to `$compatiblePorts`
- No subscription established - reads value once at call time
- Breaks the reactive data flow model

```typescript
// ✅ GOOD: Use sample() for reactive derivation
const $compatiblePorts = sample({
  source: { nodes: $nodes, draggingPort: $draggingEdgePort },
  clock: $draggingEdgePort,
  fn: ({ nodes, draggingPort }) => {
    if (!draggingPort) return null
    const nodeList = Object.values(nodes)
    // ... compute compatible ports
    return compatiblePorts
  },
})
```

### Where `.getState()` IS Acceptable

Only use `.getState()` in these specific cases:

1. **Inside effect handlers** (when you truly need a snapshot):
   ```typescript
   const myEffectFx = createEffect(async (params) => {
     // OK: Effect runs once, needs current value
     const client = $trpcClient.getState()
     return client.mutation(params)
   })
   ```

2. **Better: Use `attach()` instead**:
   ```typescript
   // ✅ BEST: Explicit dependency via attach()
   const myEffectFx = attach({
     source: $trpcClient,
     effect: async (client, params) => {
       return client.mutation(params)
     },
   })
   ```

---

## Correct Patterns

### Pattern 1: `sample()` - Reactive Derivation

Use `sample()` when you need to combine multiple sources reactively:

**File**: `apps/chaingraph-frontend/src/store/edges/stores.ts:126-151`

```typescript
// Derive dragging port data from nodes and dragging edge
const $draggingEdgePortUpdated = sample({
  source: $nodes,                    // Reactive source
  clock: $draggingEdge,              // When to sample
  fn: (nodes, draggingEdge) => {     // Transform function
    if (!draggingEdge?.nodeId || !draggingEdge?.handleId) {
      return null
    }
    const node = nodes[draggingEdge.nodeId]
    if (!node) return null

    const draggingPort = node.getPort(draggingEdge.handleId)
    return draggingPort ? { draggingEdge, draggingPort } : null
  },
})
```

### Pattern 2: `attach()` - Effect with Source

Use `attach()` when effects need store values:

**File**: `apps/chaingraph-frontend/src/store/edges/stores.ts:46-74`

```typescript
// Effect that needs tRPC client
const addEdgeFx = attach({
  source: $trpcClient,
  effect: async (client, event: AddEdgeEventData) => {
    if (!client) {
      throw new Error('TRPC client is not initialized')
    }
    return client.flow.connectPorts.mutate({
      flowId: event.flowId,
      sourceNodeId: event.sourceNodeId,
      sourcePortId: event.sourcePortId,
      targetNodeId: event.targetNodeId,
      targetPortId: event.targetPortId,
    })
  },
})
```

### Pattern 3: `combine()` - Merge Stores

Use `combine()` to create derived stores from multiple sources:

**File**: `apps/chaingraph-frontend/src/store/flow/stores.ts:300-308`

```typescript
// Combine multiple error states
export const $allFlowsErrors = combine(
  $flowsError,
  $createFlowError,
  $updateFlowError,
  $deleteFlowError,
  $forkFlowError,
  (loadError, createError, updateError, deleteError, forkError) =>
    loadError || createError || updateError || deleteError || forkError,
)

// Object syntax (creates named object)
export const $flowSubscriptionState = combine({
  status: $flowSubscriptionStatus,
  error: $flowSubscriptionError,
  isSubscribed: $isFlowSubscribed,
})
```

### Pattern 4: Advanced `sample()` with Multiple Clocks

**File**: `apps/chaingraph-frontend/src/store/edges/stores.ts:335-393`

```typescript
// React to multiple events with named source object
sample({
  clock: [$portConfigs, $portUI, setEdges, setEdge, $xyflowNodesList],
  source: {
    edgeMap: $edgeRenderMap,
    portConfigs: $portConfigs,
    portUI: $portUI,
    xyflowNodes: $xyflowNodesList,
  },
  fn: ({ edgeMap, portConfigs, portUI, xyflowNodes }) => {
    const changes: Array<{ edgeId: string, changes: Partial<EdgeRenderData> }> = []

    for (const [edgeId, edge] of edgeMap) {
      const sourceKey = toPortKey(edge.source, edge.sourceHandle)
      const sourceConfig = portConfigs.get(sourceKey)
      // ... compute changes
    }

    return { changes }
  },
  target: edgeDataChanged,
})
```

---

## Global Reset Pattern

All stores should support global reset for clean state transitions:

**File**: `apps/chaingraph-frontend/src/store/common.ts`

```typescript
import { createEvent } from 'effector'

export const globalReset = createEvent()
```

**Usage in stores:**

```typescript
export const $edges = edgesDomain.createStore<EdgeData[]>([])
  .on(setEdges, (source, edges) => [...source, ...edges])
  .on(removeEdge, (edges, event) => edges.filter(e => e.edgeId !== event.edgeId))
  .reset(resetEdges)      // Domain-specific reset
  .reset(globalReset)     // Global reset (ALWAYS add this)
```

---

## Patronum Utilities

ChainGraph uses [patronum](https://patronum.effector.dev/) for advanced patterns:

### `interval` - Time-based Events

**File**: `apps/chaingraph-frontend/src/store/flow/event-buffer.ts`

```typescript
import { interval } from 'patronum'

// Create periodic ticker for event batching
const ticker = interval({
  timeout: 50,           // 50ms interval
  start: tickerStart,    // Event to start ticker
  stop: tickerStop,      // Event to stop ticker
})

// Auto-start when buffer gets first event
sample({
  clock: flowEventReceived,
  source: $flowEventBuffer,
  filter: buffer => buffer.length === 1,  // First event
  target: tickerStart,
})

// Auto-stop when buffer is empty
sample({
  clock: $flowEventBuffer,
  filter: buffer => buffer.length === 0,
  target: tickerStop,
})
```

### `spread` - Distribute Events

**File**: `apps/chaingraph-frontend/src/store/ports-v2/buffer.ts`

```typescript
import { spread } from 'patronum'

// Spread port updates to multiple targets
sample({
  clock: portUpdatesReceived,
  fn: processPortUpdates,
  target: spread({
    valueUpdates: applyValueUpdates,
    uiUpdates: applyUIUpdates,
    configUpdates: applyConfigUpdates,
    connectionUpdates: applyConnectionUpdates,
  }),
})
```

### `debug` - Development Debugging

**File**: `apps/chaingraph-frontend/src/store/ports-v2/domain.ts`

```typescript
import { debug } from 'patronum'

// Enable in development (commented out in production)
// debug(portsV2Domain)
```

---

## React Integration

### Using `useUnit` (Recommended)

```typescript
import { useUnit } from 'effector-react'

function MyComponent() {
  // ✅ GOOD: Destructure stores and events together
  const [nodes, selectedIds, selectNode] = useUnit([
    $nodes,
    $selectedNodeIds,
    selectNode,
  ])

  // Or with object syntax
  const { nodes, addNode } = useUnit({
    nodes: $nodes,
    addNode: addNodeEvent,
  })

  return <div onClick={() => addNode(newNode)}>{/* ... */}</div>
}
```

### Avoid: `useStore` and `useEvent` separately

```typescript
// ❌ AVOID: Separate hooks (less efficient)
const nodes = useStore($nodes)
const addNode = useEvent(addNodeEvent)

// ✅ PREFER: Combined useUnit
const [nodes, addNode] = useUnit([$nodes, addNodeEvent])
```

---

## Store Organization Pattern

### Standard Store File Structure

```typescript
// stores.ts
import { sample, combine } from 'effector'
import { myDomain } from '../domains'
import { globalReset } from '../common'

// ============ EVENTS ============
export const doSomething = myDomain.createEvent<Payload>()
export const reset = myDomain.createEvent()

// ============ EFFECTS ============
export const doSomethingFx = myDomain.createEffect(async (payload: Payload) => {
  // async logic
})

// Or with attach for source dependency
export const doSomethingFx = attach({
  source: $dependency,
  effect: async (dep, payload) => {
    // async logic with dep
  },
})

// ============ STORES ============
export const $myStore = myDomain.createStore<State>(initialState)
  .on(doSomething, (state, payload) => newState)
  .on(doSomethingFx.doneData, (state, result) => newState)
  .reset(reset)
  .reset(globalReset)

// ============ DERIVED STORES ============
export const $derivedStore = combine($myStore, $otherStore, (my, other) => {
  // compute derived state
})

// ============ WIRING ============
sample({
  clock: someEvent,
  source: $myStore,
  filter: (state) => state.shouldTrigger,
  target: doSomethingFx,
})
```

---

## Quick Reference

| Need | Pattern | Example |
|------|---------|---------|
| Derive from multiple stores | `sample({ source, clock, fn })` | Reactive computation |
| Effect needs store value | `attach({ source, effect })` | tRPC calls |
| Merge stores | `combine(stores, fn)` | Error aggregation |
| Time-based batching | `interval({ timeout, start, stop })` | Event buffer |
| Distribute to multiple targets | `spread({ ... })` | Port updates |
| Reset on app state change | `.reset(globalReset)` | All stores |
| Read store in component | `useUnit([$store, event])` | React integration |

---

## Key Files

| File | Purpose |
|------|---------|
| `src/store/domains.ts` | All domain definitions |
| `src/store/common.ts` | globalReset event |
| `src/store/flow/event-buffer.ts` | Patronum interval example |
| `src/store/ports-v2/buffer.ts` | Patronum spread example |
| `src/store/edges/stores.ts` | sample/attach examples |

---

## Related Skills

- `frontend-architecture` - Overall frontend structure
- `subscription-sync` - How stores sync with backend
- `optimistic-updates` - Optimistic UI patterns with Effector
