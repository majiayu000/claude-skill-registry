---
name: a2a-server
description: Build an A2A server — the agent-side endpoint that receives JSON-RPC requests, processes tasks, manages state, and returns results. Use when implementing the server side of an A2A agent.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Server Implementation

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the server-side protocol requirements
2. Web-search `site:github.com a2aproject a2a-python server` or `a2aproject a2a-js server` for SDK server classes
3. Web-search `site:github.com a2aproject a2a-samples server` for reference server implementations
4. Fetch the target SDK README for server setup patterns

## Conceptual Architecture

### What an A2A Server Does

An A2A server is the **agent's network endpoint** that:
1. Serves the Agent Card at `/.well-known/agent-card.json`
2. Accepts JSON-RPC 2.0 requests at the agent's URL
3. Routes requests to the appropriate method handler
4. Manages task state (creation, updates, terminal states)
5. Executes the agent's logic (the "brain" — typically an LLM or deterministic logic)
6. Returns responses in the correct JSON-RPC format

### Request Processing Flow

```
HTTP POST → JSON-RPC parse → Method routing → Handler execution → Task state update → JSON-RPC response
```

### Methods to Implement

Every A2A server must handle:

| Method | Required | Description |
|--------|----------|-------------|
| `message/send` | Yes | Receive a message, create/update task, return result |
| `message/stream` | If streaming | Same as send but returns SSE stream |
| `tasks/get` | Yes | Return task by ID |
| `tasks/cancel` | Yes | Cancel a task |
| `tasks/resubscribe` | If streaming | Re-subscribe to task's SSE stream |
| Push notification methods | If supported | Configure/manage push notification callbacks |

### Task State Management

The server is responsible for task state transitions:
- Create tasks in `submitted` state when receiving new messages
- Transition to `working` when processing begins
- Transition to `input-required` when more input is needed
- Transition to terminal state (`completed`, `failed`, `canceled`, `rejected`) when done
- Never transition from a terminal state to a non-terminal state

### Handler Pattern

The SDK typically provides a handler interface you implement:

```
class MyAgentHandler:
    async def handle_message(task_id, message) -> TaskResult:
        # Your agent logic here
        # 1. Parse the input message parts
        # 2. Process with LLM or business logic
        # 3. Return result with updated task state
```

### Server Components

1. **HTTP Server** — Handles HTTP requests (FastAPI, Express, built-in SDK server)
2. **JSON-RPC Router** — Parses JSON-RPC and routes to method handlers
3. **Task Store** — Persists task state (in-memory for dev, database for production)
4. **Agent Handler** — Your custom logic that processes tasks
5. **Agent Card Endpoint** — Serves the discovery document

### Task Storage

- **In-memory** — Dict/Map of task IDs to task objects (development only)
- **Redis** — Fast key-value storage for task state (good for single-region)
- **Database** — PostgreSQL, MongoDB, etc. (production, multi-region)
- **SDK built-in** — Some SDKs provide task store abstractions

### Concurrency

A2A servers must handle concurrent requests:
- Multiple tasks running simultaneously
- Same task receiving updates while processing
- Streaming responses held open while processing continues
- Proper locking/synchronization for task state updates

### Best Practices

- Use the SDK's built-in server utilities rather than implementing raw JSON-RPC
- Implement proper task state validation — reject invalid transitions
- Add request logging with task IDs for debugging
- Set reasonable timeouts for long-running tasks
- Handle graceful shutdown — complete or cancel in-flight tasks
- Return proper JSON-RPC errors for invalid requests
- Validate incoming messages against expected input modes
- Use async/await for I/O-bound operations (LLM calls, external APIs)

Fetch the SDK documentation for exact server class names, constructor parameters, middleware patterns, and handler interfaces before implementing.
