---
name: sse-streaming-patterns
description: Server-Sent Events streaming patterns for this project. Covers TransformStream-based SSE (mobile API), ReadableStream-based SSE (legacy tier 2), heartbeat keep-alive, polling loops, event formatting, cleanup on disconnect. Triggers on "sse", "server-sent events", "streaming", "heartbeat", "polling", "transform stream".
---

# SSE Streaming Patterns

Two SSE implementations: TransformStream-based (mobile API tier) and ReadableStream-based (legacy tier 2). Both use 2min heartbeat to prevent carrier timeout, proper headers, AbortSignal cleanup.

## TransformStream Pattern (Mobile API)

Primary pattern for mobile API. Uses `createSSEResponse()` utility from `src/lib/api/sse/utils.ts`.

```typescript
// From apps/web/src/app/api/v1/conversations/stream/route.ts
import {
  createSSEResponse,
  createHeartbeatLoop,
  createPollingLoop,
  setupSSECleanup,
} from "@/lib/api/sse/utils";

async function handler(req: NextRequest, { userId }: { userId: string }) {
  const { response, send, sendError, close, isClosed } = createSSEResponse();

  try {
    // 1. Send initial snapshot
    const initialData = await convex.query(api.conversations.list, {...});
    await send("snapshot", { conversations: initialData });

    // 2. Setup polling loop (5s interval)
    const pollInterval = createPollingLoop(
      async () => {
        if (isClosed()) return null;
        const conversations = await convex.query(api.conversations.list, {...});
        return { conversations };
      },
      send,
      5000,
      "update"
    );

    // 3. Setup heartbeat (2min interval)
    const heartbeat = createHeartbeatLoop(send, 120_000);

    // 4. Cleanup on disconnect
    setupSSECleanup(req.signal, close, [pollInterval, heartbeat]);

    return response;
  } catch (error) {
    await sendError(error instanceof Error ? error : new Error(String(error)));
    await close();
    return new Response("Internal server error", { status: 500 });
  }
}
```

**SSEConnection interface**:
```typescript
interface SSEConnection {
  response: Response;
  send: (event: string, data: unknown) => Promise<void>;
  sendError: (error: Error | string) => Promise<void>;
  close: () => Promise<void>;
  isClosed: () => boolean;
}
```

**Key features**:
- TransformStream with WritableStreamDefaultWriter
- `send()` checks `closed` flag before writing
- Client disconnect caught via try/catch on `writer.write()`
- `close()` idempotent (safe to call multiple times)

## ReadableStream Pattern (Legacy Tier 2)

Legacy pattern from `src/app/api/_lib/sse-helpers.ts`. Used for medium-duration operations (5-30s).

```typescript
import { createSSEResponse, SSEStream } from "@/app/api/_lib/sse-helpers";

export function POST(req: Request) {
  return createSSEResponse(async (stream) => {
    // Send progress updates
    stream.sendProgress(jobId, { current: 50, message: "Half done" });

    // Do work
    const result = await doWork();

    // Send completion
    stream.sendComplete(jobId, result);
  });
}
```

**SSEStream class methods**:
```typescript
class SSEStream {
  send(data: any, event?: string) // Generic event
  sendProgress(jobId: string, progress: ProgressUpdate) // Progress
  sendComplete(jobId: string, result: any) // Completion
  sendError(jobId: string, error: string | { message: string }) // Error
  sendHeartbeat() // Keep-alive
  close() // Close stream
}
```

**Key differences from TransformStream**:
- ReadableStream with controller
- Handler passed to `createSSEResponse()`
- Auto-closes in finally block
- No explicit `isClosed()` check (stream handles it)

## Heartbeat Keep-Alive

**CRITICAL**: Mobile carriers disconnect idle SSE connections after 5-10 minutes. Heartbeat every 2 minutes prevents disconnection.

```typescript
// TransformStream pattern (120s = 2min)
const heartbeat = createHeartbeatLoop(send, 120_000);

// ReadableStream pattern (30s default, configurable)
const cleanup = createHeartbeat(stream, 30000);
```

**Heartbeat event format**:
```typescript
// TransformStream
event: heartbeat
data: {"ts":1705939200000}

// ReadableStream
event: ping
data: {"timestamp":1705939200000}
```

## Polling Loop

Used to poll Convex queries for updates. Error handling built-in.

```typescript
const pollInterval = createPollingLoop(
  async () => {
    if (isClosed()) return null; // Check before polling

    const data = await convex.query(api.some.query, { args });
    return { data };
  },
  send,
  5000, // 5s interval
  "update" // Event name (optional, defaults to "update")
);
```

**Error handling**: Catches errors, sends as SSE error event, continues polling.

```typescript
// Inside createPollingLoop
try {
  const data = await pollFn();
  await send(eventName, data);
} catch (error) {
  const errorMessage = error instanceof Error ? error.message : "Poll failed";
  await send("error", { error: errorMessage }).catch(() => {
    // Client disconnected
  });
}
```

## Event Formatting

SSE events use `event: name\ndata: json\n\n` format.

```typescript
// TransformStream pattern
await send("snapshot", { conversations: [...] });
// Output:
// event: snapshot
// data: {"conversations":[...]}
//

// ReadableStream pattern
stream.send({ conversations: [...] }, "snapshot");
// Same output

// Generic event (no name)
stream.send({ data: "value" });
// Output:
// data: {"data":"value"}
//
```

**Manual formatting** (if needed):
```typescript
import { formatSSEEvent } from "@/lib/api/sse/utils";

const eventString = formatSSEEvent("update", { data: "value" });
// Returns: 'event: update\ndata: {"data":"value"}\n\n'
```

## Cleanup on Disconnect

Use `setupSSECleanup()` to handle AbortSignal, clear intervals, close connection.

```typescript
setupSSECleanup(req.signal, close, [pollInterval, heartbeat]);
```

**What it does**:
- Listens to `req.signal` abort event
- Clears all intervals (polling, heartbeat)
- Calls `close()` to close SSE connection
- Swallows errors (already closed)

**AbortSignal triggered by**:
- Client closes tab/browser
- Client navigates away
- Network disconnection
- Request timeout

## Required Headers

Both patterns use identical headers:

```typescript
{
  "Content-Type": "text/event-stream",
  "Cache-Control": "no-cache, no-transform",
  "Connection": "keep-alive",
  "X-Accel-Buffering": "no" // CRITICAL for nginx
}
```

**X-Accel-Buffering: no**: Disables nginx buffering. Without this, nginx buffers SSE events and sends them in batches, breaking real-time streaming.

## Pattern Selection

**Use TransformStream** (mobile API tier):
- Long-running connections (>30s)
- Polling for updates
- Mobile clients
- Need explicit `isClosed()` checks

**Use ReadableStream** (legacy tier 2):
- Medium-duration operations (5-30s)
- Progress updates with completion
- Handler function pattern preferred
- No polling needed

## Key Files

- `apps/web/src/lib/api/sse/utils.ts` - TransformStream utilities
- `apps/web/src/app/api/_lib/sse-helpers.ts` - ReadableStream utilities
- `apps/web/src/app/api/v1/conversations/stream/route.ts` - TransformStream example

## Common Mistakes

**Don't**: Send events after close
```typescript
await send("data", { ... });
await close();
await send("more", { ... }); // ERROR: closed
```

**Do**: Check isClosed() before sending
```typescript
if (!isClosed()) {
  await send("data", { ... });
}
```

**Don't**: Forget X-Accel-Buffering header
```typescript
// nginx will buffer events
headers: { "Content-Type": "text/event-stream" }
```

**Do**: Always include X-Accel-Buffering: no
```typescript
headers: {
  "Content-Type": "text/event-stream",
  "X-Accel-Buffering": "no"
}
```

**Don't**: Skip heartbeat for long connections
```typescript
// Connection dies after 5-10min on mobile
const { response, send } = createSSEResponse();
return response;
```

**Do**: Always setup heartbeat
```typescript
const heartbeat = createHeartbeatLoop(send, 120_000);
setupSSECleanup(req.signal, close, [heartbeat]);
```
