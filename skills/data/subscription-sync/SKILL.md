---
name: subscription-sync
description: Real-time data synchronization patterns for ChainGraph frontend. Use
  when working on WebSocket subscriptions, event buffers, tRPC subscriptions, flow
  synchronization, or execution event streaming. Cov
---

---
name: subscription-sync
description: Real-time data synchronization patterns for ChainGraph frontend. Use when working on WebSocket subscriptions, event buffers, tRPC subscriptions, flow synchronization, or execution event streaming. Covers subscription lifecycle, event buffering, race condition solutions. Triggers: subscription, sync, real-time, websocket, event buffer, tRPC subscription, flow events, onData, patronum interval.
---

# Subscription Sync Patterns

This skill covers the real-time data synchronization system between ChainGraph backend and frontend via WebSocket subscriptions.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      BACKEND (tRPC)                           │
│                                                               │
│  Flow Subscription           Execution Subscription           │
│  ├─ FlowInitStart            ├─ EXECUTION_CREATED            │
│  ├─ NodesAdded               ├─ FLOW_STARTED                 │
│  ├─ EdgesAdded               ├─ NODE_STARTED                 │
│  ├─ FlowInitEnd              ├─ NODE_COMPLETED               │
│  ├─ NodeUpdated              ├─ EDGE_TRANSFER                │
│  ├─ PortUpdated              └─ FLOW_COMPLETED               │
│  └─ ...                                                       │
└──────────────────┬───────────────────────┬───────────────────┘
                   │ WebSocket             │ WebSocket
                   ▼                       ▼
┌──────────────────────────────────────────────────────────────┐
│                      FRONTEND                                  │
│                                                               │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │ $trpcClient         │    │ $trpcClientExecutor │          │
│  │ ws://localhost:3001 │    │ ws://localhost:4021 │          │
│  └──────────┬──────────┘    └──────────┬──────────┘          │
│             │                          │                      │
│             ▼                          ▼                      │
│  ┌─────────────────────┐    ┌─────────────────────┐          │
│  │ Flow Event Buffer   │    │ Execution Events    │          │
│  │ (50ms batching)     │    │ (direct processing) │          │
│  └──────────┬──────────┘    └──────────┬──────────┘          │
│             │                          │                      │
│             ▼                          ▼                      │
│  ┌────────────────────────────────────────────────┐          │
│  │              Effector Stores                    │          │
│  │  $nodes, $edges, $portValues, $execution        │          │
│  └────────────────────────────────────────────────┘          │
└──────────────────────────────────────────────────────────────┘
```

## Two tRPC Clients

ChainGraph frontend maintains TWO separate WebSocket connections:

**Files**:
- Main Server Client: `apps/chaingraph-frontend/src/store/trpc/store.ts`
- Executor Server Client: `apps/chaingraph-frontend/src/store/trpc/execution-client.ts`

```typescript
// Main Server - Flow editing operations (store.ts)
export const $trpcClient = trpcDomain.createStore<TRPCClient | null>(null)
// Connects to: ws://localhost:3001

// Executor Server - Execution events (execution-client.ts)
export const $trpcClientExecutor = trpcDomain.createStore<TRPCClient | null>(null)
// Connects to: ws://localhost:4021
```

### Why Two Clients?

1. **Separation of Concerns**: Flow editing and execution are independent
2. **Load Distribution**: Heavy execution traffic doesn't block editing
3. **Independent Scaling**: Executor can scale separately
4. **Failure Isolation**: Execution server crash doesn't break editing

## Flow Subscription Lifecycle

**Files**:
- Subscription: `apps/chaingraph-frontend/src/store/flow/subscription.ts`
- Event Buffer: `apps/chaingraph-frontend/src/store/flow/event-buffer.ts`

### Event Sequence

```
1. FlowInitStart
   └─ Clear existing nodes/edges
   └─ Set status: CONNECTING → SUBSCRIBED

2. NodesAdded (batch)
   └─ Buffer accumulates events

3. EdgesAdded (batch)
   └─ Buffer accumulates events

4. FlowInitEnd (COMMIT SIGNAL)
   └─ Buffer flushes immediately
   └─ All events processed atomically
   └─ Nodes render BEFORE edges (race condition solved)

5. Live Updates (ongoing)
   └─ Buffer with 50ms interval
   └─ NodeUpdated, PortUpdated, EdgeAdded, etc.
```

### Subscription Status

```typescript
enum FlowSubscriptionStatus {
  IDLE = 'idle',
  CONNECTING = 'connecting',
  SUBSCRIBED = 'subscribed',
  ERROR = 'error',
  DISCONNECTED = 'disconnected',
}
```

## Event Buffer Pattern

**Problem**: Race condition where edges render before nodes during flow initialization.

**Root Cause**:
```
1. addNodes triggers xyflowStructureChanged with 50ms debounce
2. setEdges updates $xyflowEdges immediately
3. $xyflowEdges filters out edges because $xyflowNodes is empty
```

**Solution**: Buffer ALL FlowEvents and flush atomically on FlowInitEnd.

**File**: `apps/chaingraph-frontend/src/store/flow/event-buffer.ts`

```typescript
import { interval } from 'patronum'

// Buffer accumulates events
export const $flowEventBuffer = flowDomain.createStore<FlowEvent[]>([])
  .on(flowEventReceived, (buffer, event) => [...buffer, event])

// Ticker runs every 50ms (configurable via VITE_FLOW_EVENT_BUFFER_INTERVAL)
const ticker = interval({
  timeout: 50,  // BUFFER_INTERVAL_MS
  start: tickerStart,
  stop: tickerStop,
})

// Auto-start ticker when first event arrives
sample({
  clock: flowEventReceived,
  source: $flowEventBuffer,
  filter: buffer => buffer.length === 1,  // Buffer was empty
  target: tickerStart,
})

// Auto-stop ticker when buffer is empty
sample({
  clock: $flowEventBuffer,
  filter: buffer => buffer.length === 0,
  target: tickerStop,
})

// CRITICAL: Flush immediately on FlowInitEnd
sample({
  clock: flowEventReceived,
  filter: event => event.type === FlowEventType.FlowInitEnd,
  target: flushBuffer,
})
```

### Buffer Processing Flow

```
Subscription → flowEventReceived → $flowEventBuffer
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                          │
              [FlowInitEnd]                               [50ms tick]
                    │                                          │
                    ▼                                          ▼
             flushBuffer (immediate)              processBufferFx (batched)
                    │                                          │
                    └────────────────┬─────────────────────────┘
                                     │
                                     ▼
                              newFlowEvents (batch of FlowEvent[])
                                     │
                                     ▼
                              Event Handlers in stores.ts
```

## Execution Subscription

**File**: `apps/chaingraph-frontend/src/store/execution/subscription.ts`

Execution events are processed directly (no buffering needed):

```typescript
// Subscribe to execution events
// Note: No .execution namespace - procedures are at router root
const subscription = trpcClientExecutor.subscribeToExecutionEvents.subscribe(
  { executionId, fromIndex: 0 },
  {
    onData: (event) => {
      executionEventReceived(event)  // Direct dispatch
    },
    onError: (error) => {
      executionError(error)
    },
  }
)
```

### Execution Event Types

```typescript
enum ExecutionEventEnum {
  EXECUTION_CREATED = 'EXECUTION_CREATED',  // index -1
  FLOW_STARTED = 'FLOW_STARTED',
  NODE_STARTED = 'NODE_STARTED',
  NODE_COMPLETED = 'NODE_COMPLETED',
  NODE_FAILED = 'NODE_FAILED',
  EDGE_TRANSFER_COMPLETED = 'EDGE_TRANSFER_COMPLETED',
  FLOW_COMPLETED = 'FLOW_COMPLETED',
  FLOW_FAILED = 'FLOW_FAILED',
  CHILD_EXECUTION_SPAWNED = 'CHILD_EXECUTION_SPAWNED',
}
```

## Key Files

| File | Purpose |
|------|---------|
| `src/store/trpc/store.ts` | tRPC client stores |
| `src/store/flow/subscription.ts` | Flow subscription management |
| `src/store/flow/event-buffer.ts` | Event buffering with patronum |
| `src/store/execution/subscription.ts` | Execution event subscription |
| `src/store/flow/stores.ts` | Event handlers (newFlowEvents) |

## Common Patterns

### Subscribe to Flow

```typescript
import { subscribeToFlowFx, unsubscribeFromFlowFx } from '@/store/flow/subscription'

// Subscribe
subscribeToFlowFx(flowId)

// Unsubscribe (cleanup)
unsubscribeFromFlowFx()
```

### Handle Flow Events

```typescript
// In stores.ts
sample({
  clock: newFlowEvents,
  filter: events => events.some(e => e.type === FlowEventType.NodeUpdated),
  fn: events => events.filter(e => e.type === FlowEventType.NodeUpdated),
  target: processNodeUpdates,
})
```

### Subscribe to Execution

```typescript
import { subscribeToExecutionFx } from '@/store/execution/subscription'

// Subscribe and wait for EXECUTION_CREATED
await subscribeToExecutionFx({ executionId })

// Start execution after subscription is ready
startExecution({ executionId })
```

## Anti-Patterns

### Anti-Pattern #1: Processing events without buffering

```typescript
// ❌ BAD: Direct dispatch causes race conditions
onData: (event) => {
  newFlowEvents([event])  // Edges may render before nodes!
}

// ✅ GOOD: Use buffer
onData: (event) => {
  flowEventReceived(event)  // Buffer handles ordering
}
```

### Anti-Pattern #2: Not waiting for EXECUTION_CREATED

```typescript
// ❌ BAD: Start before subscription is ready
startExecution({ executionId })
subscribeToExecutionFx({ executionId })  // Might miss events!

// ✅ GOOD: Subscribe first, then start
await subscribeToExecutionFx({ executionId })
startExecution({ executionId })
```

### Anti-Pattern #3: Not cleaning up subscriptions

```typescript
// ❌ BAD: Memory leak
useEffect(() => {
  subscribeToFlowFx(flowId)
  // No cleanup!
}, [flowId])

// ✅ GOOD: Cleanup on unmount/change
useEffect(() => {
  subscribeToFlowFx(flowId)
  return () => {
    unsubscribeFromFlowFx()
  }
}, [flowId])
```

## Quick Reference

| Need | Pattern | File |
|------|---------|------|
| Subscribe to flow | `subscribeToFlowFx(flowId)` | `flow/subscription.ts` |
| Buffer events | `flowEventReceived(event)` | `flow/event-buffer.ts` |
| Process buffered events | `newFlowEvents` event | `flow/stores.ts` |
| Subscribe to execution | `subscribeToExecutionFx()` | `execution/subscription.ts` |
| Get subscription status | `$flowSubscriptionStatus` | `flow/stores.ts` |

---

## Related Skills

- `effector-patterns` - Effector patterns used in subscriptions
- `frontend-architecture` - Overall frontend structure
- `executor-architecture` - Backend event emission
- `dbos-patterns` - DBOS event streaming
- `trpc-patterns` - General tRPC framework patterns
- `trpc-flow-editing` - Flow editing tRPC procedures
- `trpc-execution` - Execution tRPC procedures
