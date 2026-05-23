---
name: execution-lifecycle-manager
description: Manage DAG execution lifecycles including start, stop, pause, resume, and cleanup. Activate on 'execution lifecycle', 'stop execution', 'abort DAG', 'graceful shutdown', 'kill process'. NOT for cost estimation, DAG building, or skill selection.
allowed-tools: Read,Write,Edit,Bash
---

# Execution Lifecycle Manager

Centralized state management for running DAG executions with graceful shutdown patterns.

## When to Use

✅ **Use for**:
- Implementing execution start/stop/pause/resume controls
- Graceful process termination (SIGTERM → SIGKILL)
- Tracking active executions across the system
- Cleaning up orphaned processes
- Implementing abort handlers with cost tracking

❌ **NOT for**:
- Cost estimation or pricing calculations (use cost-accrual-tracker)
- Building or modifying DAG structures
- Skill matching or selection
- Process spawning (use the executor directly)

## Core Patterns

### 1. Graceful Shutdown Pattern

Always use SIGTERM first, then escalate to SIGKILL:

```typescript
// CORRECT: Two-phase shutdown
const GRACEFUL_TIMEOUT_MS = 2000;

async function terminateProcess(proc: ChildProcess): Promise<void> {
  proc.kill('SIGTERM');

  const forceKillTimer = setTimeout(() => {
    if (!proc.killed) {
      proc.kill('SIGKILL');
    }
  }, GRACEFUL_TIMEOUT_MS);

  await waitForExit(proc);
  clearTimeout(forceKillTimer);
}
```

### 2. AbortController Pattern

Use `AbortController` for cancellation propagation:

```typescript
// Parent (DAGExecutor)
const abortController = new AbortController();

// Pass signal to child executors
await executor.execute({
  ...request,
  abortSignal: abortController.signal,
});

// To abort all children:
abortController.abort();
```

### 3. Execution Registry Pattern

Track active executions for monitoring and cleanup:

```typescript
interface ActiveExecution {
  executionId: string;
  abortController: AbortController;
  status: 'running' | 'stopping' | 'stopped' | 'completed' | 'failed';
  startedAt: number;
  stoppedAt?: number;
}

class ExecutionManager {
  private executions: Map<string, ActiveExecution> = new Map();

  create(id: string): ActiveExecution { /* ... */ }
  stop(id: string, reason: string): Promise<StopResult> { /* ... */ }
  listActive(): ActiveExecution[] { /* ... */ }
}
```

## Anti-Patterns

### SIGKILL Without SIGTERM

**Novice thinking**: "Just kill it immediately"

**Reality**: SIGKILL doesn't allow cleanup. Processes can't:
- Flush buffers to disk
- Close network connections gracefully
- Release locks
- Save partial progress

**Timeline**:
- Always: SIGTERM allows graceful shutdown
- If stuck after 2-5s: Then use SIGKILL

**Correct approach**: Always SIGTERM first, SIGKILL as fallback.

### Missing Abort Signal Propagation

**Novice thinking**: "Just track the top-level execution"

**Reality**: Without signal propagation, child processes become orphans:
- Parent dies, children keep running
- Resources leak
- Costs continue accruing

**Correct approach**: Pass `AbortSignal` through entire execution tree.

### Synchronous Stop Handler

**Novice thinking**: "Stop should return immediately"

**Reality**: Stopping is async - processes need time to terminate:
- Network requests need to timeout
- File handles need to close
- Costs need final calculation

**Correct approach**: Return `Promise` with final state after cleanup completes.

## State Machine

```
         ┌──────────┐
         │  idle    │
         └────┬─────┘
              │ start()
              ▼
         ┌──────────┐
    ┌───►│ running  │◄───┐
    │    └────┬─────┘    │
    │         │          │ resume()
    │         │ pause()  │
    │         ▼          │
    │    ┌──────────┐    │
    │    │ paused   │────┘
    │    └────┬─────┘
    │         │ stop()
    │         ▼
    │    ┌──────────┐
    └────│ stopping │ (transitional - 2-10s)
         └────┬─────┘
              │
     ┌────────┴────────┐
     ▼                 ▼
┌──────────┐     ┌──────────┐
│ stopped  │     │  failed  │
└──────────┘     └──────────┘
```

## API Design

### Stop Endpoint Response

```typescript
interface StopResponse {
  status: 'stopped';
  executionId: string;
  reason: string;  // 'user_abort' | 'timeout' | 'error'
  finalCostUsd: number;
  stoppedAt: number;
  summary: {
    nodesCompleted: number;
    nodesFailed: number;
    nodesTotal: number;
    durationMs: number;
  };
}
```

### Cleanup on Server Shutdown

```typescript
// In server.ts
process.on('SIGINT', async () => {
  console.log('Shutting down...');

  // Stop all active executions gracefully
  const active = executionManager.listActive();
  await Promise.all(
    active.map(e => executionManager.stop(e.executionId, 'server_shutdown'))
  );

  server.close();
});
```

## Integration Points

| Component | Responsibility |
|-----------|----------------|
| `ExecutionManager` | Tracks executions, coordinates stop |
| `DAGExecutor` | Owns AbortController, orchestrates waves |
| `ProcessExecutor` | Spawns processes, handles SIGTERM/SIGKILL |
| `/api/execute/stop` | HTTP interface for stop requests |

## References

See `/references/process-signals.md` for Unix signal handling details.
