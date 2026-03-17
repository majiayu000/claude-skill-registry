---
name: Observability Patterns
description: Debugging and monitoring patterns for the distributed offline-first architecture
---

# Observability Patterns

In a system with Offline Clients, Edge Workers (Cloudflare), and AI Agents, "It works on my machine" means nothing.

## 1. The Request ID Chain

Every operation must have a traceable ID.

1. **Client Generation:** Client generates `x-request-id` (UUID).
2. **Worker Propagation:** Cloudflare Worker logs this ID and passes it to the DB middleware.
3. **Error Context:** If an `AppError` is thrown, it _must_ include this ID.

## 2. Structured AppError Logging

When logging errors, never log just the message. Log the _Context_.

```typescript
// ✅ Correct Logging Pattern
console.error(
  JSON.stringify({
    level: 'error',
    requestId: ctx.requestId,
    error: error.name,
    code: error.code,
    // Critical for debugging offline sync issues:
    metadata: {
      batchId: data.batchId,
      inputs: truncate(JSON.stringify(data), 1000),
    },
    stack: error.stack,
  }),
)
```

## 3. "Health Check" Endpoints for Agents

Agents need to know if the system is healthy before attempting complex actions.

- `/api/health`: Basic uptime.
- `/api/health/sync`: Status of the sync queues.
- `/api/health/ai`: Status of the LLM/Agent provider connections.

## 4. Distributed Tracing for Sync

The hardest bugs are "Sync Conflicts".
Log the **Sync Lifecycle**:

1. `SYNC_START`: Device X, 5 items.
2. `SYNC_ITEM`: Item A (Create Batch). Result: Success.
3. `SYNC_ITEM`: Item B (Log Feed). Result: Conflict (Version Mismatch).
4. `SYNC_END`: Success: 4, Fail: 1.

## 5. Client-Side Telemetry

Since much logic happens offline, the client must store a "Telemtry Buffer".
When online, flush this buffer to the server.
_Key Metric:_ "Time from Action to Sync" (How long are users offline?)

## Related Skills

- `error-handling` - The `AppError` class usage
- `cloudflare-workers` - The logging constraints (standard out)
