---
name: executor-architecture
description: Executor package architecture for ChainGraph flow execution engine. Use
  when working on packages/chaingraph-executor, execution services, DBOS workflows,
  event bus, task queues, tRPC routes, or execut
---

---
name: executor-architecture
description: Executor package architecture for ChainGraph flow execution engine. Use when working on packages/chaingraph-executor, execution services, DBOS workflows, event bus, task queues, tRPC routes, or execution-related database operations. Triggers: executor, execution, service, worker, queue, event bus, dbos, workflow, tRPC execution, execution-api, execution-worker.
---

# ChainGraph Executor Architecture

This skill provides architectural guidance for the `@badaitech/chaingraph-executor` package - the execution engine that runs ChainGraph flows with durable execution via DBOS.

## Package Overview

**Location**: `packages/chaingraph-executor/`
**Purpose**: Flow execution engine with DBOS durable execution
**Key Feature**: Exactly-once execution semantics with automatic recovery

## Directory Structure

```
packages/chaingraph-executor/
├── server/
│   ├── index.ts                    # Main exports
│   │
│   ├── dbos/                       # DBOS durable execution ⭐
│   │   ├── config.ts               # DBOS initialization
│   │   ├── DBOSExecutionWorker.ts  # Worker lifecycle
│   │   ├── queue.ts                # Queue management
│   │   ├── workflows/
│   │   │   └── ExecutionWorkflows.ts  # Main orchestration
│   │   └── steps/
│   │       ├── ExecuteFlowAtomicStep.ts  # Core execution
│   │       └── UpdateStatusStep.ts  # Status updates
│   │
│   ├── services/                   # Business logic layer
│   │   ├── ExecutionService.ts     # Execution instance management
│   │   ├── RecoveryService.ts      # Failure recovery
│   │   └── ServiceFactory.ts       # Service initialization
│   │
│   ├── implementations/            # Interface implementations
│   │   ├── dbos/
│   │   │   ├── DBOSEventBus.ts     # DBOS event streaming
│   │   │   └── DBOSTaskQueue.ts    # DBOS task queue
│   │   └── local/
│   │       ├── InMemoryEventBus.ts # Dev/test event bus
│   │       └── InMemoryTaskQueue.ts
│   │
│   ├── interfaces/                 # Abstract interfaces
│   │   ├── IEventBus.ts            # Event streaming contract
│   │   └── ITaskQueue.ts           # Task queue contract
│   │
│   ├── stores/                     # Data access layer
│   │   ├── execution-store.ts      # Execution CRUD
│   │   ├── flow-store.ts           # Flow loading
│   │   └── postgres/
│   │       ├── schema.ts           # Drizzle schema
│   │       └── postgres-execution-store.ts
│   │
│   ├── trpc/                       # API layer
│   │   ├── router.ts               # tRPC procedures
│   │   └── context.ts              # Request context
│   │
│   └── utils/                      # Utilities
│       ├── config.ts               # Environment config
│       ├── db.ts                   # Database connection
│       └── logger.ts               # Logging
│
├── client/                         # tRPC client exports
└── types/                          # TypeScript types
```

## Architecture Layers

```
┌────────────────────────────────────────────────────────────┐
│ Layer 1: API (tRPC)                                         │
│ ├─ create()    → Start execution workflow                   │
│ ├─ start()     → Send START_SIGNAL                          │
│ ├─ stop()      → Cancel workflow                            │
│ ├─ pause()     → Send PAUSE command                         │
│ └─ subscribeToExecutionEvents() → Stream events             │
├────────────────────────────────────────────────────────────┤
│ Layer 2: Services                                           │
│ ├─ ExecutionService   → Instance management                 │
│ ├─ RecoveryService    → Failure recovery                    │
│ └─ ServiceFactory     → Dependency injection                │
├────────────────────────────────────────────────────────────┤
│ Layer 3: DBOS (Durable Execution)                           │
│ ├─ ExecutionWorkflow  → Orchestration + child spawning      │
│ └─ ExecuteFlowAtomicStep → Core flow execution              │
├────────────────────────────────────────────────────────────┤
│ Layer 4: Implementations                                    │
│ ├─ DBOSEventBus       → PostgreSQL event streaming          │
│ └─ DBOSTaskQueue      → PostgreSQL task queue               │
├────────────────────────────────────────────────────────────┤
│ Layer 5: Stores                                             │
│ ├─ ExecutionStore     → Execution row CRUD                  │
│ └─ FlowStore          → Flow definition loading             │
└────────────────────────────────────────────────────────────┘
```

## Two Execution Modes

The executor supports two modes controlled by `ENABLE_DBOS_EXECUTION`:

### DBOS Mode (Production)

```
ENABLE_DBOS_EXECUTION=true

Features:
├─ Exactly-once execution via workflow IDs
├─ Automatic recovery from failures
├─ Real-time event streaming via PostgreSQL
├─ Durable task queue (no Kafka needed)
└─ DBOS Admin UI at localhost:3022
```

### Legacy/Local Mode (Development)

```
ENABLE_DBOS_EXECUTION=false

Features:
├─ In-memory event bus
├─ In-memory task queue
├─ Simpler debugging
└─ No durability guarantees
```

## Key Files

| File | Purpose | Critical? |
|------|---------|-----------|
| `server/dbos/workflows/ExecutionWorkflows.ts` | Main orchestration | ⭐⭐⭐ |
| `server/dbos/steps/ExecuteFlowAtomicStep.ts` | Core execution step | ⭐⭐⭐ |
| `server/services/ExecutionService.ts` | Instance management | ⭐⭐ |
| `server/services/ServiceFactory.ts` | Service initialization | ⭐⭐ |
| `server/implementations/dbos/DBOSEventBus.ts` | Event streaming | ⭐⭐ |
| `server/trpc/router.ts` | API procedures | ⭐⭐ |
| `server/stores/postgres/schema.ts` | Database schema | ⭐ |
| `server/utils/config.ts` | Environment config | ⭐ |

## Execution Lifecycle

```
1. CREATE (tRPC)
   └─ ExecutionRow inserted → Workflow started
   └─ Workflow writes EXECUTION_CREATED event
   └─ Workflow waits for START_SIGNAL

2. SUBSCRIBE (tRPC)
   └─ Client subscribes to DBOS stream
   └─ Immediately receives EXECUTION_CREATED

3. START (tRPC)
   └─ Sends START_SIGNAL via DBOS.send()
   └─ Workflow continues

4. EXECUTE (Workflow)
   └─ Step 1: updateToRunning()
   └─ Step 2: executeFlowAtomic()
   │   └─ Load flow from DB
   │   └─ Create execution instance
   │   └─ Execute flow (up to 30min)
   │   └─ Stream events in real-time
   │   └─ Collect child tasks
   └─ Step 3: Spawn children
   └─ Step 4: updateToCompleted()

5. COMPLETE
   └─ DBOS auto-closes event stream
   └─ Client receives all events
```

## Service Layer

### ExecutionService

Manages execution instances with event streaming setup:

```typescript
// server/services/ExecutionService.ts
class ExecutionService {
  // Create execution instance with event handling
  async createExecutionInstance(params: {
    task: ExecutionTask
    flow: Flow
    executionRow: ExecutionRow
    abortController: AbortController
  }): Promise<ExecutionInstance>

  // Get event bus (DBOS or InMemory based on config)
  getEventBus(): IEventBus

  // Setup event handling (connects engine events → event bus)
  setupEventHandling(instance: ExecutionInstance): () => Promise<void>
}
```

### ServiceFactory

Initializes all services with proper dependency injection:

```typescript
// server/services/ServiceFactory.ts
async function initializeServices(): Promise<Services> {
  // 1. Create event bus (DBOS or InMemory)
  const eventBus = config.dbos.enabled
    ? new DBOSEventBus()
    : new InMemoryEventBus()

  // 2. Create task queue
  const taskQueue = config.dbos.enabled
    ? new DBOSTaskQueue()
    : new InMemoryTaskQueue()

  // 3. Create execution service
  const executionService = new ExecutionService(eventBus, taskQueue)

  // 4. Initialize DBOS steps (dependency injection)
  initializeExecuteFlowStep(executionService, executionStore)

  return { eventBus, taskQueue, executionService }
}
```

## tRPC Router

**File**: `server/trpc/router.ts`

```typescript
export const executionRouter = router({
  // Create execution (starts workflow immediately)
  create: procedure
    .input(CreateExecutionInput)
    .mutation(async ({ input }) => {
      // 1. Create execution row in DB
      // 2. Start DBOS workflow (writes EXECUTION_CREATED)
      // 3. Return executionId
    }),

  // Start execution (sends START_SIGNAL)
  start: procedure
    .input(z.object({ executionId: z.string() }))
    .mutation(async ({ input }) => {
      await DBOS.send(input.executionId, 'API', 'START_SIGNAL')
    }),

  // Subscribe to execution events (real-time streaming)
  subscribeToExecutionEvents: procedure
    .input(z.object({ executionId: z.string(), fromIndex: z.number() }))
    .subscription(async function* ({ input }) {
      // Yields events from DBOS stream
      for await (const event of DBOS.readStream(input.executionId, 'events')) {
        yield event
      }
    }),

  // Control commands
  pause: procedure.mutation(...),
  resume: procedure.mutation(...),
  stop: procedure.mutation(...),
})
```

## Database Schema

**File**: `server/stores/postgres/schema.ts`

```typescript
export const executions = pgTable('executions', {
  id: text('id').primaryKey(),              // EX123...
  flowId: text('flow_id').notNull(),
  ownerId: text('owner_id').notNull(),
  status: executionStatusEnum('status').notNull(),

  // Hierarchy
  rootExecutionId: text('root_execution_id'),
  parentExecutionId: text('parent_execution_id'),
  executionDepth: integer('execution_depth').default(0),

  // Timestamps
  createdAt: timestamp('created_at').notNull(),
  startedAt: timestamp('started_at'),
  completedAt: timestamp('completed_at'),

  // Error tracking
  errorMessage: text('error_message'),
  errorNodeId: text('error_node_id'),

  // Recovery
  failureCount: integer('failure_count').default(0),
  lastFailureAt: timestamp('last_failure_at'),

  // Context
  options: jsonb('options'),
  integration: jsonb('integration'),        // archai context
  externalEvents: jsonb('external_events'), // events for children
})
```

## Environment Variables

```bash
# DBOS Mode
ENABLE_DBOS_EXECUTION=true

# Database
DATABASE_URL_EXECUTIONS=postgres://...

# DBOS Configuration
DBOS_ADMIN_ENABLED=true
DBOS_ADMIN_PORT=3022
DBOS_QUEUE_CONCURRENCY=100
DBOS_WORKER_CONCURRENCY=5

# Execution Limits
EXECUTION_MAX_DEPTH=100
EXECUTION_DEFAULT_TIMEOUT_MS=3600000  # 1 hour
```

## Quick Reference

| Need | Where | File |
|------|-------|------|
| Add new tRPC procedure | API layer | `server/trpc/router.ts` |
| Modify execution logic | DBOS step | `server/dbos/steps/ExecuteFlowAtomicStep.ts` |
| Add orchestration logic | DBOS workflow | `server/dbos/workflows/ExecutionWorkflows.ts` |
| Change event streaming | Implementation | `server/implementations/dbos/DBOSEventBus.ts` |
| Modify schema | Store | `server/stores/postgres/schema.ts` |
| Add service | Service layer | `server/services/` |

---

## Related Skills

- `dbos-patterns` - CRITICAL DBOS constraints and patterns
- `chaingraph-concepts` - Core domain concepts (Flow, Node, Port)
- `subscription-sync` - Event streaming architecture
- `types-architecture` - Execution types and events
- `trpc-execution` - Execution tRPC procedures (API layer)
- `trpc-patterns` - General tRPC framework patterns
