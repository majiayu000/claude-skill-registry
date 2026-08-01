---
name: trpc-execution
description: ChainGraph execution tRPC layer for flow execution management. Use when
  working on packages/chaingraph-executor or apps/chaingraph-execution-api. Covers
  execution lifecycle (create/start/pause/resume/
---

---
name: trpc-execution
description: ChainGraph execution tRPC layer for flow execution management. Use when working on packages/chaingraph-executor or apps/chaingraph-execution-api. Covers execution lifecycle (create/start/pause/resume/stop), event streaming, DBOS workflow integration, signal pattern, API vs Worker modes. Triggers: execution procedure, subscribeToExecutionEvents, ExecutionService, chaingraph-executor, execution-api, execution workflow, DBOS signal, taskQueue, eventBus.
---

# tRPC Execution Layer

This skill covers the tRPC procedures for execution management in ChainGraph - the API for controlling flow execution with real-time event streaming.

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                 Frontend (React + XYFlow)                       │
│                        │                                        │
│              tRPC Client (WebSocket)                            │
│                   (Port 4021)                                   │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│         chaingraph-execution-api OR execution-worker            │
│                        │                                        │
│   ┌────────────────────▼────────────────────────────────────┐  │
│   │               executionRouter                            │  │
│   │  ├─ create         (starts workflow, waits for signal)  │  │
│   │  ├─ start          (sends START_SIGNAL)                 │  │
│   │  ├─ stop           (cancels workflow)                   │  │
│   │  ├─ pause          (sends PAUSE command)                │  │
│   │  ├─ resume         (sends RESUME command)               │  │
│   │  └─ subscribeToExecutionEvents (event streaming)        │  │
│   └─────────────────────────────────────────────────────────┘  │
│                        │                                        │
│   ┌────────────────────▼────────────────────────────────────┐  │
│   │              ServiceFactory                              │  │
│   │  ├─ API Mode: DBOSClient (enqueue only)                 │  │
│   │  └─ Worker Mode: Full DBOS runtime                      │  │
│   └─────────────────────────────────────────────────────────┘  │
│                        │                                        │
│   ┌────────────────────▼────────────────────────────────────┐  │
│   │              DBOS Workflows                              │  │
│   │  ├─ ExecutionWorkflow (orchestration)                   │  │
│   │  ├─ executeFlowAtomic (step - runs ExecutionEngine)     │  │
│   │  └─ PostgreSQL (state + event streams)                  │  │
│   └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
packages/chaingraph-executor/server/
├── trpc/
│   ├── router.ts          # Main execution router
│   └── context.ts         # tRPC context with services
│
├── services/
│   ├── ExecutionService.ts    # Core execution logic
│   ├── IExecutionService.ts   # Service interface
│   └── ServiceFactory.ts      # API vs Worker mode setup
│
├── implementations/
│   ├── dbos/
│   │   ├── DBOSEventBus.ts    # DBOS event streaming
│   │   ├── DBOSTaskQueue.ts   # Worker queue (DBOS.startWorkflow)
│   │   ├── APITaskQueue.ts    # API queue (DBOSClient.enqueue)
│   │   └── streaming/
│   │       └── StreamBridge.ts # PostgreSQL LISTEN/NOTIFY
│   └── local/
│       ├── InMemoryEventBus.ts
│       └── InMemoryTaskQueue.ts
│
├── dbos/
│   ├── workflows/
│   │   └── ExecutionWorkflows.ts  # Main DBOS workflow
│   ├── steps/
│   │   ├── ExecuteFlowAtomicStep.ts  # Core execution step
│   │   └── UpdateStatusStep.ts
│   └── queue.ts                      # DBOS queue config
│
├── interfaces/
│   ├── IEventBus.ts
│   └── ITaskQueue.ts
│
└── ws-server.ts           # WebSocket server

apps/chaingraph-execution-api/
└── src/
    ├── index.ts           # Entry point
    └── server/index.ts    # Uses createServicesForAPI()
```

---

## Execution Procedures

**File**: `packages/chaingraph-executor/server/trpc/router.ts`

### Create Execution

**Lines**: 148-271

```typescript
create: authedProcedure
  .input(z.object({
    flowId: z.string(),
    options: ExecutionOptionsSchema.optional(),
    integration: IntegrationContextSchema.optional(),
    events: z.array(ExecutionExternalEventSchema).optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    const { executionStore, taskQueue, flowStore } = ctx
    const userId = ctx.session?.user?.id

    // 1. Validate user owns the flow
    const flow = await flowStore.getFlow(input.flowId)
    if (!flow) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `Flow ${input.flowId} not found`,
      })
    }

    if (flow.metadata.ownerID !== userId) {
      throw new TRPCError({
        code: 'FORBIDDEN',
        message: 'User does not own this flow',
      })
    }

    // 2. Create execution row in database
    const executionId = `EX${generateShortId(16)}`
    const execution = await executionStore.create({
      id: executionId,
      flowId: input.flowId,
      userId,
      status: ExecutionStatus.Created,
      createdAt: new Date(),
      options: input.options,
      integration: input.integration,
    })

    if (!execution) {
      throw new TRPCError({
        code: 'INTERNAL_SERVER_ERROR',
        message: 'Failed to create execution record',
      })
    }

    // 3. Start DBOS workflow (SIGNAL PATTERN)
    // Workflow writes EXECUTION_CREATED and waits for START_SIGNAL
    await taskQueue.publishTask({
      executionId,
      flowId: input.flowId,
      userId,
      options: input.options,
      integration: input.integration,
      externalEvents: input.events,
    })

    return { executionId }
  })
```

### Start Execution

**Lines**: 273-318

```typescript
start: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
  }))
  .mutation(async ({ input, ctx }) => {
    const { executionStore, dbosClient } = ctx

    // 1. Validate status
    const execution = await executionStore.get(input.executionId)
    if (!execution) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `Execution ${input.executionId} not found`,
      })
    }

    if (execution.status !== ExecutionStatus.Created) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot start execution in status ${execution.status}`,
      })
    }

    // 2. Send START_SIGNAL to waiting workflow
    // Uses DBOSClient in API mode, DBOS.send() in Worker mode
    if (dbosClient) {
      // API Mode: Use DBOSClient
      await dbosClient.send(input.executionId, START_SIGNAL, 'START_SIGNAL')
    } else {
      // Worker Mode: Use DBOS directly
      await DBOS.send(input.executionId, START_SIGNAL, 'START_SIGNAL')
    }

    return { success: true }
  })
```

### Stop Execution

**Lines**: 320-378

```typescript
stop: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
    reason: z.string().optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    const { executionStore, dbosClient } = ctx

    const execution = await executionStore.get(input.executionId)
    if (!execution) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `Execution ${input.executionId} not found`,
      })
    }

    // Can't stop if already terminal
    const terminalStatuses = [
      ExecutionStatus.Completed,
      ExecutionStatus.Failed,
      ExecutionStatus.Stopped,
    ]
    if (terminalStatuses.includes(execution.status)) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: `Cannot stop execution in status ${execution.status}`,
      })
    }

    // Cancel DBOS workflow (built-in feature)
    if (dbosClient) {
      await dbosClient.cancelWorkflow(input.executionId)
    } else {
      await DBOS.cancelWorkflow(input.executionId)
    }

    // Update database status
    await executionStore.updateStatus(input.executionId, ExecutionStatus.Stopped)

    return { success: true }
  })
```

### Pause Execution

**Lines**: 380-437

```typescript
pause: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
    reason: z.string().optional(),
  }))
  .mutation(async ({ input, ctx }) => {
    const { executionStore, dbosClient } = ctx

    const execution = await executionStore.get(input.executionId)
    if (!execution || execution.status !== ExecutionStatus.Running) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: 'Can only pause running executions',
      })
    }

    // Send PAUSE command via DBOS messaging
    const command = { command: 'PAUSE', reason: input.reason }

    if (dbosClient) {
      await dbosClient.send(input.executionId, command, 'COMMAND')
    } else {
      await DBOS.send(input.executionId, command, 'COMMAND')
    }

    return { success: true }
  })
```

### Resume Execution

**Lines**: 439-494

```typescript
resume: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
  }))
  .mutation(async ({ input, ctx }) => {
    const { executionStore, dbosClient } = ctx

    const execution = await executionStore.get(input.executionId)
    if (!execution || execution.status !== ExecutionStatus.Paused) {
      throw new TRPCError({
        code: 'BAD_REQUEST',
        message: 'Can only resume paused executions',
      })
    }

    // Send RESUME command via DBOS messaging
    const command = { command: 'RESUME' }

    if (dbosClient) {
      await dbosClient.send(input.executionId, command, 'COMMAND')
    } else {
      await DBOS.send(input.executionId, command, 'COMMAND')
    }

    return { success: true }
  })
```

### Subscribe to Execution Events

**Lines**: 574-644

```typescript
subscribeToExecutionEvents: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
    fromIndex: z.number().optional().default(0),
    eventTypes: z.array(z.string()).optional().default([]),
    batchSize: z.number().min(1).max(1000).optional().default(100),
    batchTimeoutMs: z.number().min(0).max(1000).optional().default(25),
  }))
  .subscription(async function* ({ input, ctx, signal }) {
    const { executionStore, eventBus } = ctx

    // 1. Verify execution exists
    const instance = await executionStore.get(input.executionId)
    if (!instance) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `Execution with id ${input.executionId} not found`,
      })
    }

    // 2. Subscribe to event stream with batching
    const iterator = eventBus.subscribeToEvents(
      input.executionId,
      input.fromIndex,
      {
        maxSize: input.batchSize,
        timeoutMs: input.batchTimeoutMs,
      },
    )

    let eventCount = 0

    try {
      for await (const events of iterator) {
        // Check for client disconnect
        if (signal?.aborted) {
          logger.info({ executionId: input.executionId, eventsSent: eventCount },
            'Client disconnected')
          break
        }

        // Filter by event types
        const filtered = events.filter((event) => {
          if (input.eventTypes.length === 0) return true
          return input.eventTypes.includes(event.type)
        })

        // Only yield non-empty batches
        if (filtered.length > 0) {
          eventCount += filtered.length
          yield filtered
        }
      }
    } catch (error) {
      logger.error({ error, executionId: input.executionId },
        'Error in event subscription')
      throw error
    } finally {
      logger.info({ executionId: input.executionId, eventsSent: eventCount },
        'Subscription ended, cleaning up')
      await eventBus.unsubscribe(input.executionId)
    }
  })
```

---

## Signal Pattern (CRITICAL)

The signal pattern solves a race condition where clients might subscribe before the event stream exists.

```
WITHOUT SIGNAL PATTERN (BROKEN):
1. create() → Returns immediately
2. subscribe() → Stream doesn't exist yet! ❌
3. Workflow starts → EXECUTION_CREATED lost!

WITH SIGNAL PATTERN (CORRECT):
1. create() → Workflow starts → EXECUTION_CREATED → Stream exists! ✅
2. subscribe() → Stream exists → Receives EXECUTION_CREATED ✅
3. start() → Sends START_SIGNAL → Workflow continues
```

### Implementation

**In `create` procedure:**
```typescript
// Workflow starts but PAUSES after writing EXECUTION_CREATED
await taskQueue.publishTask({ executionId, ... })
```

**In ExecutionWorkflow:**
```typescript
// Phase 1: Write event BEFORE waiting
await DBOS.writeStream('events', {
  type: ExecutionEventEnum.EXECUTION_CREATED,
  executionId,
  index: -1,  // Special index
})

// Wait for START_SIGNAL
const signal = await DBOS.recv<string>('START_SIGNAL', 60)
if (signal !== START_SIGNAL) {
  throw new Error('Expected START_SIGNAL')
}
// Phase 2: Continue execution...
```

**In `start` procedure:**
```typescript
// Send signal to waiting workflow
await DBOS.send(executionId, START_SIGNAL, 'START_SIGNAL')
```

---

## Dual-Mode Architecture

ChainGraph execution supports two deployment modes:

### API Mode

**File**: `packages/chaingraph-executor/server/services/ServiceFactory.ts:202-298`

```typescript
export async function createServicesForAPI(): Promise<ServiceInstances> {
  // NO DBOS runtime initialization!
  // Uses external DBOSClient instead

  const dbosClient = new DBOSClient(config.dbos)

  return {
    executionService: new ExecutionService(flowStore, nodeRegistry),
    executionStore: new PostgresExecutionStore(db),
    eventBus: new DBOSEventBus(streamBridge),
    taskQueue: new APITaskQueue(dbosClient),  // Uses DBOSClient.enqueue()
    flowStore,
    ownershipResolver,
    dbosClient,  // Available in context
  }
}
```

**Characteristics:**
- **NO** local workflow execution
- Uses `DBOSClient` for remote enqueue
- Can send signals via `DBOSClient.send()`
- Can cancel workflows via `DBOSClient.cancelWorkflow()`
- Subscribes to events via `DBOSEventBus`

### Worker Mode

**File**: `packages/chaingraph-executor/server/services/ServiceFactory.ts:306-429`

```typescript
export async function createServicesForWorker(): Promise<ServiceInstances> {
  // Import workflow class (REQUIRED for DBOS registration)
  const { ExecutionWorkflows } = await import('../dbos/workflows/ExecutionWorkflows')

  // Create queue BEFORE DBOS.launch() for dequeue capability
  const executionQueue = new WorkflowQueue('executionQueue', {
    workerConcurrency: config.dbos.workerConcurrency,
  })

  // Initialize DBOS runtime
  await initializeDBOS()

  return {
    executionService: new ExecutionService(flowStore, nodeRegistry),
    executionStore: new PostgresExecutionStore(db),
    eventBus: new DBOSEventBus(streamBridge),
    taskQueue: new DBOSTaskQueue(executionQueue),  // Uses DBOS.startWorkflow()
    flowStore,
    ownershipResolver,
    // NO dbosClient - use DBOS directly
  }
}
```

**Characteristics:**
- **Full** DBOS runtime initialization
- Executes workflows locally
- Queue created BEFORE `DBOS.launch()` (critical!)
- Uses `DBOS.send()`, `DBOS.startWorkflow()` directly

---

## Event Streaming

### Event Bus Interface

**File**: `packages/chaingraph-executor/server/interfaces/IEventBus.ts`

```typescript
interface IEventBus {
  publishEvent(executionId: string, event: ExecutionEventImpl): Promise<void>

  subscribeToEvents(
    executionId: string,
    fromIndex: number,
    batchConfig?: EventBatchConfig,
  ): AsyncIterable<ExecutionEventImpl[]>

  unsubscribe(executionId: string): Promise<void>

  close(): Promise<void>
}

interface EventBatchConfig {
  maxSize: number      // Max events per batch (default: 100)
  timeoutMs: number    // Max wait before flush (default: 25ms)
}
```

### DBOS Event Bus

**File**: `packages/chaingraph-executor/server/implementations/dbos/DBOSEventBus.ts`

```typescript
export class DBOSEventBus implements IEventBus {
  private readonly streamBridge: StreamBridge

  async publishEvent(executionId: string, event: ExecutionEventImpl): Promise<void> {
    // Uses DBOS.writeStream() - allowed from STEP context!
    await DBOS.writeStream('events', {
      ...event,
      executionId,
    })
  }

  subscribeToEvents(
    executionId: string,
    fromIndex: number,
    batchConfig?: EventBatchConfig,
  ): AsyncIterable<ExecutionEventImpl[]> {
    return this.streamBridge.subscribe(executionId, fromIndex, batchConfig)
  }

  async unsubscribe(executionId: string): Promise<void> {
    await this.streamBridge.unsubscribe(executionId)
  }
}
```

### Stream Bridge (PostgreSQL LISTEN/NOTIFY)

**File**: `packages/chaingraph-executor/server/implementations/dbos/streaming/StreamBridge.ts`

```
Event Published (DBOS.writeStream)
        │
        ▼
PostgreSQL (dbos_workflow_event_queue table)
        │
        ▼
NOTIFY dbos_workflow_events (with executionId)
        │
        ▼
PGListenerPool (10 listeners, sharded)
        │
        ▼
DBOSStreamSubscriber
        │
        ▼
StreamBridge (batching accumulator)
        │
        ▼
DBOSEventBus
        │
        ▼
tRPC Subscription (WebSocket)
```

**Key Features:**
- Real-time via PostgreSQL LISTEN/NOTIFY
- Fallback polling if LISTEN unavailable
- Automatic listener sharding (10 listeners)
- Configurable batching for network efficiency

---

## Execution Context

**File**: `packages/chaingraph-executor/server/trpc/context.ts`

```typescript
export interface ExecutorContext {
  session: Session
  executionService: IExecutionService
  executionStore: IExecutionStore
  eventBus: IEventBus
  taskQueue: ITaskQueue
  flowStore: IFlowStore
  ownershipResolver: IOwnershipResolver
  dbosClient?: DBOSClient  // Only in API mode
}

export async function createContext(opts: CreateHTTPContextOptions): Promise<ExecutorContext> {
  // Get services from ServiceFactory (singleton)
  const services = await getServices()

  // Extract auth token and validate session
  const token = getAuthToken(opts)
  const session = await authService.validateSession(token)

  return {
    session: {
      user: session?.user,
      isAuthenticated: !!session?.user,
    },
    ...services,
  }
}
```

---

## Query Procedures

### Get Execution Details

**Lines**: 496-513

```typescript
getExecutionDetails: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
  }))
  .query(async ({ input, ctx }) => {
    const execution = await ctx.executionStore.get(input.executionId)
    if (!execution) {
      throw new TRPCError({
        code: 'NOT_FOUND',
        message: `Execution ${input.executionId} not found`,
      })
    }
    return execution
  })
```

### Get Executions Tree

**Lines**: 515-532

```typescript
getExecutionsTree: executionContextProcedure
  .input(z.object({
    executionId: z.string(),
  }))
  .query(async ({ input, ctx }) => {
    return ctx.executionStore.getTree(input.executionId)
  })
```

### Get Root Executions

**Lines**: 534-572

```typescript
getRootExecutions: authedProcedure
  .input(z.object({
    flowId: z.string(),
    limit: z.number().min(1).max(100).default(50),
    after: z.date().optional(),
  }))
  .query(async ({ input, ctx }) => {
    // Returns paginated list of root executions for a flow
    return ctx.executionStore.listRootExecutions(
      input.flowId,
      ctx.session.user.id,
      input.limit,
      input.after,
    )
  })
```

---

## Comparison: Flow Editing vs Execution

| Aspect | Flow Editing | Execution |
|--------|--------------|-----------|
| **Port** | 3001 | 4021 |
| **Package** | chaingraph-trpc | chaingraph-executor |
| **App** | chaingraph-backend | chaingraph-execution-api |
| **Purpose** | CRUD flows, nodes, edges | Run flows, stream events |
| **Storage** | Flow definitions (JSONB) | Execution state + events |
| **Real-time** | `flow.onEvent()` → WebSocket | DBOS streams → WebSocket |
| **Orchestration** | None | DBOS workflows |
| **Modes** | Single mode | API + Worker modes |

---

## Key Files

| File | Purpose |
|------|---------|
| `packages/chaingraph-executor/server/trpc/router.ts:148-644` | All execution procedures |
| `packages/chaingraph-executor/server/trpc/context.ts` | Execution context |
| `packages/chaingraph-executor/server/services/ServiceFactory.ts` | API vs Worker setup |
| `packages/chaingraph-executor/server/implementations/dbos/DBOSEventBus.ts` | Event streaming |
| `packages/chaingraph-executor/server/implementations/dbos/streaming/StreamBridge.ts` | LISTEN/NOTIFY |
| `packages/chaingraph-executor/server/dbos/workflows/ExecutionWorkflows.ts` | DBOS workflow |
| `packages/chaingraph-executor/server/ws-server.ts` | WebSocket server |
| `apps/chaingraph-execution-api/src/index.ts` | API entry point |

---

## Quick Reference

| Operation | Procedure | Key Pattern |
|-----------|-----------|-------------|
| Create | `create` | Start workflow, wait for signal |
| Start | `start` | Send START_SIGNAL |
| Stop | `stop` | DBOS.cancelWorkflow() |
| Pause | `pause` | Send PAUSE command |
| Resume | `resume` | Send RESUME command |
| Subscribe | `subscribeToExecutionEvents` | Stream with batching |

| Mode | TaskQueue | Signal Method |
|------|-----------|---------------|
| API | `APITaskQueue` → `DBOSClient.enqueue()` | `dbosClient.send()` |
| Worker | `DBOSTaskQueue` → `DBOS.startWorkflow()` | `DBOS.send()` |

---

## Related Skills

- `trpc-patterns` - General tRPC framework patterns
- `trpc-flow-editing` - Flow editing procedures
- `dbos-patterns` - DBOS constraints and patterns
- `executor-architecture` - Package overview
