---
name: a2a-streaming
description: Implement A2A SSE streaming — message/stream method, Server-Sent Events, TaskStatusUpdateEvent, TaskArtifactUpdateEvent, and re-subscription. Use when building real-time streaming responses in A2A agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Streaming (SSE)

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the streaming section
2. Web-search `site:github.com a2aproject A2A streaming SSE message/stream` for streaming protocol details
3. Web-search `site:github.com a2aproject a2a-samples streaming` for streaming implementation examples
4. Fetch SDK docs for streaming server/client classes and event types

## Conceptual Architecture

### What A2A Streaming Is

A2A streaming uses **Server-Sent Events (SSE)** to deliver real-time task updates from server to client. Instead of waiting for the entire task to complete (`message/send`), the client receives incremental updates as the agent works (`message/stream`).

### When to Use Streaming

- **Long-running tasks** — Keep the client informed of progress
- **Incremental results** — Deliver partial artifacts as they're generated
- **Interactive UX** — Show real-time agent activity to end users
- **Token streaming** — Stream LLM output tokens as they're generated

### How It Works

1. Client sends `message/stream` (same payload as `message/send`)
2. Server responds with `Content-Type: text/event-stream`
3. Server sends SSE events as the task progresses
4. Final event contains a terminal task state
5. Connection closes after the terminal event

### SSE Event Types

| Event Type | Purpose | When Sent |
|-----------|---------|-----------|
| **TaskStatusUpdateEvent** | Task state changed | On every state transition |
| **TaskArtifactUpdateEvent** | New artifact data | When agent produces output |

### Event Format

SSE events follow the standard format:
```
event: <event-type>
data: <JSON payload>

```

Each event's `data` field contains a JSON object with:
- **taskId** — Which task this event belongs to
- **type** — Event type discriminator
- Type-specific fields (status update, artifact data, message content)

### Re-subscription

If the SSE connection drops, the client can re-subscribe:
- Call `tasks/resubscribe` with the `taskId`
- Server resumes sending events from the current state
- Events that were sent before the reconnection are NOT replayed (unless the server implements replay)

### Server-Side Implementation

The server must:
1. Declare `streaming: true` in the Agent Card capabilities
2. Handle `message/stream` method
3. Keep the HTTP connection open
4. Send SSE events as the agent processes
5. Send a final event with a terminal state
6. Close the connection cleanly

### Client-Side Implementation

The client must:
1. Check Agent Card for `streaming` capability
2. Send `message/stream` instead of `message/send`
3. Parse SSE events (use an SSE client library)
4. Handle each event type appropriately
5. Handle connection drops and re-subscribe if needed

### Backpressure and Buffering

- Servers should buffer events if the client can't consume fast enough
- Set reasonable connection timeouts
- Send periodic keepalive comments (`:keepalive\n\n`) to prevent proxy timeouts
- Clients should process events asynchronously to avoid blocking the stream

### Best Practices

- Always send a terminal event before closing the stream
- Include the full task status in TaskStatusUpdateEvent (not just the state name)
- Use TaskArtifactUpdateEvent for incremental delivery of large results
- Implement heartbeat/keepalive to prevent connection timeouts
- Handle client disconnection gracefully on the server side
- Test with slow clients to verify backpressure handling
- Set appropriate timeouts on both client and server

Fetch the specification for exact SSE event schemas, event naming conventions, and re-subscription protocol before implementing.
