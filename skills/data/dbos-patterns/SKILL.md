---
name: dbos-patterns
description: DBOS durable execution patterns and CRITICAL constraints for ChainGraph
  executor. Use when working on workflows, steps, execution, or any DBOS-related code.
  Contains MUST-FOLLOW constraints about what
---

---
name: dbos-patterns
description: DBOS durable execution patterns and CRITICAL constraints for ChainGraph executor. Use when working on workflows, steps, execution, or any DBOS-related code. Contains MUST-FOLLOW constraints about what can be called from workflows vs steps. Triggers: dbos, workflow, step, durable, execution, startWorkflow, writeStream, recv, send, runStep, atomic, checkpoint, WorkflowQueue, queue, cancelWorkflow, Promise.allSettled. (project)
---

# DBOS Patterns for ChainGraph

This skill covers DBOS (Database-Oriented Operating System) patterns used in the ChainGraph executor. **CRITICAL**: Contains constraints that agents MUST follow to avoid runtime errors.

## CRITICAL Constraints

### The Most Important Rule

**DBOS context methods have strict calling restrictions based on WHERE you are:**

```typescript
// ============================================================
// WORKFLOW FUNCTIONS: All DBOS methods allowed
// ============================================================
async function myWorkflow(task: Task): Promise<Result> {
  await DBOS.send(...)           // ✅ Allowed
  await DBOS.recv(...)           // ✅ Allowed
  await DBOS.startWorkflow(...)  // ✅ Allowed
  await DBOS.writeStream(...)    // ✅ Allowed
  await DBOS.setEvent(...)       // ✅ Allowed
  await DBOS.sleep(...)          // ✅ Allowed

  const result = await DBOS.runStep(() => myStep(task))  // ✅ Allowed
  return result
}

// ============================================================
// STEP FUNCTIONS: ONLY writeStream() allowed!
// ============================================================
async function myStep(task: Task): Promise<StepResult> {
  await DBOS.writeStream(...)    // ✅ ONLY THIS ONE!

  // ❌ NOT ALLOWED - Will throw runtime error:
  // await DBOS.send(...)        // ❌ Error!
  // await DBOS.recv(...)        // ❌ Error!
  // await DBOS.startWorkflow(...) // ❌ Error!
  // await DBOS.setEvent(...)    // ❌ Error!
  // await DBOS.sleep(...)       // ❌ Error!

  return { data: ... }
}
```

### Constraint Reference Table

| DBOS Method | From Workflow | From Step |
|-------------|---------------|-----------|
| `DBOS.send()` | ✅ | ❌ |
| `DBOS.recv()` | ✅ | ❌ |
| `DBOS.startWorkflow()` | ✅ | ❌ |
| `DBOS.setEvent()` / `getEvent()` | ✅ | ❌ |
| `DBOS.sleep()` | ✅ | ❌ |
| `DBOS.cancelWorkflow()` | ✅ | ❌ |
| `DBOS.runStep()` | ✅ | ❌ |
| **`DBOS.writeStream()`** | ✅ | **✅** |
| `DBOS.readStream()` | ✅ | ❌ |

### Promise Handling

**NEVER use `Promise.all()`** - it fails fast and leaves promises unresolved, risking unhandled rejections.

```typescript
// ❌ BAD: Promise.all() fails fast, other promises left dangling
const results = await Promise.all([step1(), step2(), step3()])

// ✅ GOOD: Promise.allSettled() waits for all, reports outcomes
const results = await Promise.allSettled([step1(), step2(), step3()])
```

### Memory Isolation

Workflows and steps should **NOT** have side effects outside their own scope:
- ✅ Can READ global variables
- ❌ Must NOT create or update global variables
- ❌ Must NOT modify shared state outside return values

### Queue Initialization Order

**CRITICAL**: WorkflowQueue MUST be created **before** `DBOS.launch()` is called!

```typescript
// File: server/dbos/queue.ts:17-35
// Queue is created at module level BEFORE DBOS.launch()
export const executionQueue = new WorkflowQueue(QUEUE_NAME, {
  workerConcurrency: config.dbos.workerConcurrency ?? 5,
  concurrency: config.dbos.queueConcurrency ?? 100,
})

// If created AFTER DBOS.launch(), queue will NOT dequeue tasks!
```

---

## Design Patterns

### Pattern 1: Signal Pattern (Race Condition Fix)

**Problem**: Client subscribes to events before the stream exists.

**Solution**: Workflow writes initialization event BEFORE waiting for start signal.

**File**: `packages/chaingraph-executor/server/dbos/workflows/ExecutionWorkflows.ts`

```
Timeline:
1. create execution (tRPC)
   └─ Workflow starts → writes EXECUTION_CREATED → stream exists! ✅
   └─ Workflow waits for START_SIGNAL... ⏸️

2. subscribe events (tRPC)
   └─ Stream already exists → immediately receives EXECUTION_CREATED ✅

3. start execution (tRPC)
   └─ Sends START_SIGNAL → workflow continues ▶️
```

**Implementation Pattern**:
```typescript
async function executionWorkflow(task: ExecutionTask): Promise<ExecutionResult> {
  // Write event BEFORE waiting - stream now exists!
  await DBOS.writeStream('events', {
    executionId: task.executionId,
    event: 'EXECUTION_CREATED',
    timestamp: Date.now(),
  })

  // Now safe to wait - clients can subscribe
  const signal = await DBOS.recv<string>('START_SIGNAL', 300)
  if (!signal) {
    throw new Error('Execution start timeout')
  }

  // Continue with execution...
}
```

---

### Pattern 2: Shared State Pattern (Command System)

**Problem**: Cannot call `DBOS.recv()` from steps, but need to check for commands.

**Solution**: Workflow polls messages, updates shared state object that step reads.

**Files**:
- Workflow: `server/dbos/workflows/ExecutionWorkflows.ts`
- Step: `server/dbos/steps/ExecuteFlowAtomicStep.ts`

```typescript
// Shared state object (passed from workflow to step)
interface CommandController {
  currentCommand: 'PAUSE' | 'RESUME' | 'STEP' | null
}

// WORKFLOW LEVEL: Poll DBOS.recv() every 500ms
async function executionWorkflow(task: ExecutionTask) {
  const commandController: CommandController = { currentCommand: null }
  const abortController = new AbortController()

  // Start polling loop (runs concurrently with step)
  const pollCommands = async () => {
    while (!abortController.signal.aborted) {
      const cmd = await DBOS.recv<{ command: string }>('COMMAND', 0.5)
      if (cmd) {
        if (cmd.command === 'STOP') {
          abortController.abort()
        } else {
          commandController.currentCommand = cmd.command
        }
      }
    }
  }

  // Run step with shared state
  const result = await DBOS.runStep(() =>
    executeFlowAtomic(task, abortController, commandController)
  )

  return result
}

// STEP LEVEL: Check shared state every 100ms (no DBOS calls!)
async function executeFlowAtomic(
  task: ExecutionTask,
  abortController: AbortController,
  commandController: CommandController
) {
  const checkCommands = setInterval(() => {
    if (commandController.currentCommand === 'PAUSE') {
      debugger.pause()
    } else if (commandController.currentCommand === 'RESUME') {
      debugger.continue()
    }
    commandController.currentCommand = null
  }, 100)

  // Execute flow...
  // Step reads shared state, never calls DBOS.recv()
}
```

---

### Pattern 3: Collect & Spawn Pattern (Child Executions)

**Problem**: Cannot call `DBOS.startWorkflow()` from steps, but Event Emitter nodes need to spawn children.

**Solution**: Step collects child tasks and returns them, workflow spawns them.

**Files**:
- Step: `server/dbos/steps/ExecuteFlowAtomicStep.ts:346-401`
- Workflow: `server/dbos/workflows/ExecutionWorkflows.ts`

```typescript
// STEP: Collect child tasks (don't spawn!)
async function executeFlowAtomic(task: ExecutionTask): Promise<ExecutionResult> {
  const collectedChildTasks: ExecutionTask[] = []

  // Execute flow, capture emitted events
  await engine.execute()

  // After execution, collect child tasks from emitted events
  for (const event of context.emittedEvents.filter(e => !e.processed)) {
    event.processed = true

    // Create child execution row in DB (allowed in step)
    const childTask = await createChildTask(instance, event, store)
    collectedChildTasks.push(childTask)
  }

  // Return child tasks for workflow-level spawning
  return {
    status: 'completed',
    childTasks: collectedChildTasks,  // ← Workflow will spawn these
  }
}

// WORKFLOW: Spawn collected children (DBOS.startWorkflow allowed here!)
async function executionWorkflow(task: ExecutionTask) {
  const result = await DBOS.runStep(() => executeFlowAtomic(task))

  // Spawn children at workflow level
  if (result.childTasks?.length > 0) {
    for (const childTask of result.childTasks) {
      await DBOS.startWorkflow(executionWorkflow, {
        workflowID: childTask.executionId
      })(childTask)
    }
  }

  return result
}
```

---

### Pattern 4: Auto-Start Pattern (Child Execution Lifecycle)

**Problem**: Children need manual start call, slowing down execution tree.

**Solution**: Children skip the signal wait entirely and start immediately.

**File**: `server/dbos/workflows/ExecutionWorkflows.ts:192-214`

```typescript
async function executionWorkflow(task: ExecutionTask) {
  const executionRow = await store.get(task.executionId)
  const isChildExecution = !!executionRow.parentExecutionId

  // Write EXECUTION_CREATED first (Signal Pattern)
  await DBOS.writeStream('events', { event: 'EXECUTION_CREATED', ... })

  // Auto-start for children!
  if (!isChildExecution) {
    // Parents: wait for signal from tRPC (timeout: 5 minutes)
    const startSignal = await DBOS.recv<string>('START_SIGNAL', 300)
    if (!startSignal) {
      throw new Error('Execution start timeout')
    }
  } else {
    // Children: skip waiting, start immediately
    DBOS.logger.info(`Child execution auto-start, beginning execution`)
  }

  // Continue execution...
}
```

**Child Execution Lifecycle**:

```text
Parent spawns child via DBOS.startWorkflow()
  └─ Child workflow starts
      ├─ Writes EXECUTION_CREATED event
      ├─ Detects parentExecutionId
      ├─ Skips signal wait (auto-start)
      └─ Executes flow immediately
```

---

### Pattern 5: WorkflowQueue Pattern (Managed Concurrency)

**Problem**: Need to manage concurrency and ensure idempotent workflow spawning.

**Solution**: Use WorkflowQueue with concurrency limits and deduplication.

**File**: `server/dbos/queue.ts`

```typescript
import { WorkflowQueue } from '@dbos-inc/dbos-sdk'

// Create at module level BEFORE DBOS.launch()
export const executionQueue = new WorkflowQueue('chaingraph-executions', {
  workerConcurrency: 5,   // Max concurrent per worker process
  concurrency: 100,       // Max concurrent globally
})

// Use with deduplication to prevent duplicate workflows
await DBOS.startWorkflow(ExecutionWorkflows, {
  queueName: executionQueue.name,
  workflowID: childTask.executionId,  // Unique ID
  enqueueOptions: {
    deduplicationID: childTask.executionId,  // Idempotency key
  },
}).executeChainGraph(childTask)
```

---

### Pattern 6: Parent Monitoring Pattern (Child Stops if Parent Dies)

**Problem**: Child executions should stop if their parent completes or fails.

**Solution**: Background checker monitors parent workflow status.

**File**: `server/dbos/workflows/ExecutionWorkflows.ts`

```typescript
async function monitorParentWorkflow(
  parentExecutionId: string,
  abortController: AbortController
) {
  while (!abortController.signal.aborted) {
    const parentStatus = await DBOS.getWorkflowStatus(parentExecutionId)

    if (parentStatus?.status === 'COMPLETED' ||
        parentStatus?.status === 'ERROR' ||
        parentStatus?.status === 'CANCELLED') {
      abortController.abort('Parent workflow has ended')
      break
    }

    await DBOS.sleep(5)  // Check every 5 seconds
  }
}
```

---

## Three-Phase Workflow Structure

ChainGraph executions follow a three-phase structure:

```text
┌──────────────────────────────────────────────────────────────┐
│ PHASE 1: Stream Initialization (Lines 148-214)               │
│   ├─ Create CommandController                                │
│   ├─ Write EXECUTION_CREATED event (stream exists!)          │
│   ├─ Auto-start children (send START_SIGNAL to self)         │
│   └─ Wait for START_SIGNAL                                   │
├──────────────────────────────────────────────────────────────┤
│ PHASE 2: Execution (Lines 216-374)                           │
│   ├─ Step 1: updateToRunning()                               │
│   ├─ Step 2: executeFlowAtomic() ← Core execution            │
│   └─ Spawn children via DBOS.startWorkflow()                 │
├──────────────────────────────────────────────────────────────┤
│ PHASE 3: Cleanup (Lines 376-423)                             │
│   ├─ Step 3: updateToCompleted()                             │
│   ├─ Stop command polling                                    │
│   └─ DBOS auto-closes event stream                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Key Files

| File | Purpose | Critical? |
|------|---------|-----------|
| `server/dbos/workflows/ExecutionWorkflows.ts` | Main orchestration workflow | ⭐⭐⭐ |
| `server/dbos/steps/ExecuteFlowAtomicStep.ts` | Core execution step | ⭐⭐⭐ |
| `server/dbos/queue.ts:17-35` | Queue initialization (MUST be before DBOS.launch) | ⭐⭐⭐ |
| `server/dbos/config.ts` | DBOS initialization | ⭐⭐ |
| `server/dbos/DBOSExecutionWorker.ts` | Worker lifecycle | ⭐⭐ |
| `server/dbos/steps/UpdateStatusStep.ts` | Status updates | ⭐ |
| `server/implementations/dbos/DBOSEventBus.ts` | Event streaming via DBOS.writeStream() | ⭐⭐ |
| `server/utils/config.ts:70-139` | Environment config | ⭐⭐ |

---

## Environment Variables

```bash
# Enable DBOS mode (default: false)
ENABLE_DBOS_EXECUTION=true

# DBOS Admin UI
DBOS_ADMIN_ENABLED=true
DBOS_ADMIN_PORT=3022              # Access at http://localhost:3022

# Concurrency Limits
DBOS_QUEUE_CONCURRENCY=100        # Global across all workers
DBOS_WORKER_CONCURRENCY=5         # Per worker process

# DBOS Conductor (optional, for production monitoring)
DBOS_CONDUCTOR_URL=https://conductor.dbos.dev
DBOS_APPLICATION_NAME=chaingraph-executor
DBOS_CONDUCTOR_KEY=your-api-key-here
```

---

## Anti-Patterns

### Anti-Pattern #1: Calling DBOS methods from steps

```typescript
// ❌ BAD: Will throw runtime error
async function myStep(data: string) {
  await DBOS.send('other-workflow', 'message', 'TOPIC')  // ❌ Error!
}

// ✅ GOOD: Return data, let workflow send
async function myStep(data: string): Promise<{ toSend: Message }> {
  return { toSend: { target: 'other-workflow', message: 'hello' } }
}

async function myWorkflow() {
  const result = await DBOS.runStep(() => myStep(data))
  await DBOS.send(result.toSend.target, result.toSend.message, 'TOPIC')  // ✅
}
```

### Anti-Pattern #2: Splitting atomic execution

```typescript
// ❌ BAD: State lost between steps
await DBOS.runStep(() => loadFlow())
await DBOS.runStep(() => executeFlow())  // ❌ Flow state lost!

// ✅ GOOD: Single atomic step
await DBOS.runStep(() => executeFlowAtomic(task))  // ✅ All in one step
```

### Anti-Pattern #3: Making children wait for START_SIGNAL

```typescript
// ❌ BAD: Children timeout waiting for signal that never comes
async function executionWorkflow(task: ExecutionTask) {
  const isChild = !!executionRow.parentExecutionId
  // Always waiting - children have no one to send them the signal!
  await DBOS.recv('START_SIGNAL', 300)  // ❌ Times out for children
}

// ✅ GOOD: Children skip signal wait
async function executionWorkflow(task: ExecutionTask) {
  const isChild = !!executionRow.parentExecutionId
  if (!isChild) {
    // Only parents wait for signal (from tRPC start() call)
    await DBOS.recv('START_SIGNAL', 300)
  }
  // Children start immediately - no signal wait!
}
```

### Anti-Pattern #4: Using Promise.all() for parallel steps

```typescript
// ❌ BAD: Promise.all() fails fast, leaving other promises dangling
const results = await Promise.all([
  DBOS.runStep(() => step1()),
  DBOS.runStep(() => step2()),
  DBOS.runStep(() => step3()),
])

// ✅ GOOD: Promise.allSettled() waits for all, handles all outcomes
const results = await Promise.allSettled([
  DBOS.runStep(() => step1()),
  DBOS.runStep(() => step2()),
  DBOS.runStep(() => step3()),
])
```

### Anti-Pattern #5: Memory side effects in workflows/steps

```typescript
// ❌ BAD: Modifying global state
let globalCounter = 0
async function myWorkflow() {
  globalCounter++  // ❌ Side effect outside scope!
}

// ✅ GOOD: Return values instead of mutating globals
async function myWorkflow(): Promise<{ count: number }> {
  const count = calculateCount()
  return { count }  // ✅ Pure function, no side effects
}
```

### Anti-Pattern #6: Creating queue after DBOS.launch()

```typescript
// ❌ BAD: Queue created after DBOS is initialized
await DBOS.launch()
const queue = new WorkflowQueue('my-queue')  // ❌ Won't dequeue!

// ✅ GOOD: Queue created at module level BEFORE DBOS.launch()
const queue = new WorkflowQueue('my-queue')  // ✅ Module level
// ... later in main()
await DBOS.launch()
```

---

## Quick Reference

| Need | Pattern | Where |
|------|---------|-------|
| Stream exists before subscribe | Signal Pattern | Write event before recv() |
| Commands during step execution | Shared State | Workflow polls, step reads object |
| Spawn child workflows | Collect & Spawn | Step collects, workflow spawns |
| Children start immediately | Auto-Start | Skip signal wait |
| Real-time events from step | `DBOS.writeStream()` | Only stream method allowed in steps |
| Managed concurrency | WorkflowQueue | Queue with workerConcurrency/concurrency |
| Child stops if parent dies | Parent Monitoring | Background status checker |
| Parallel steps safely | Promise.allSettled() | Never use Promise.all() |

---

## DBOS Workflow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW (can call ALL DBOS methods)                        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ DBOS.send() │  │ DBOS.recv() │  │startWorkflow│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ DBOS.runStep(() => ...)                              │   │
│  │                                                       │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │ STEP (ONLY writeStream allowed)               │    │   │
│  │  │                                                │    │   │
│  │  │  ✅ DBOS.writeStream()                         │    │   │
│  │  │  ❌ DBOS.send/recv/startWorkflow/sleep/...    │    │   │
│  │  │                                                │    │   │
│  │  │  return { childTasks: [...] }                  │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  // After step completes:                                   │
│  for (child of result.childTasks) {                        │
│    await DBOS.startWorkflow(...)(child)  // ✅ Allowed here│
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Advanced DBOS Features

For advanced DBOS features not currently used in ChainGraph (Debouncer, forkWorkflow, versioning, rate limiting, partitioned queues), see `dbos-advanced.md` in this skill directory.

---

## Related Skills

- `executor-architecture` - Package overview
- `chaingraph-concepts` - Core domain concepts
- `subscription-sync` - Event streaming patterns
- `trpc-execution` - Execution tRPC procedures
- `trpc-patterns` - General tRPC framework patterns
