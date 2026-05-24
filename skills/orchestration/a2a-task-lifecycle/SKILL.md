---
name: a2a-task-lifecycle
description: Implement A2A task lifecycle management — task creation, state transitions, terminal states, history, and artifacts. Use when building task state machines, handling state transitions, or managing task persistence.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Task Lifecycle

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the Task object schema and state machine
2. Web-search `site:github.com a2aproject A2A task lifecycle states` for state transition rules
3. Web-search `site:github.com a2aproject a2a-samples task` for task handling examples
4. Fetch SDK docs for task-related classes and state management utilities

## Conceptual Architecture

### What a Task Is

A Task is the **central unit of work** in A2A. It represents a request from a client agent to a server agent, tracks progress through well-defined states, accumulates messages and artifacts, and reaches a terminal state when complete.

### Task Structure

Key fields of a Task object:
- **id** — Unique task identifier (set by client or server)
- **status** — Current state object containing `state` enum and optional `message`
- **messages** — Array of messages exchanged (if `stateTransitionHistory` enabled)
- **artifacts** — Array of output artifacts produced by the agent
- **metadata** — Optional key-value pairs for custom data

### The 9 States

| State | Terminal? | Description |
|-------|-----------|-------------|
| `submitted` | No | Task received, queued for processing |
| `working` | No | Agent actively processing |
| `input-required` | No | Agent needs more input (multi-turn) |
| `auth-required` | No | Authentication needed |
| `completed` | Yes | Task finished successfully |
| `failed` | Yes | Task encountered an unrecoverable error |
| `canceled` | Yes | Task was canceled |
| `rejected` | Yes | Server refused the task |
| `unknown` | — | Default/unknown state |

### Valid State Transitions

```
submitted → working
submitted → rejected
submitted → canceled

working → completed
working → failed
working → canceled
working → input-required

input-required → working (when client provides more input)
input-required → canceled

auth-required → working (when auth is provided)
auth-required → canceled
```

**Rules:**
- Terminal states (`completed`, `failed`, `canceled`, `rejected`) are final — no transitions out
- Only the server transitions the task state (except `canceled` which client can request)
- `input-required` → `working` happens when the client sends a follow-up message

### Task Creation

Tasks are created implicitly when a client sends a message without a `taskId`:
1. Client sends `message/send` or `message/stream` without `taskId`
2. Server creates a new task, assigns an ID
3. Task starts in `submitted` state
4. Server may immediately transition to `working` or return `submitted`

### Task Continuation

When a client sends a message with an existing `taskId`:
1. The message is appended to the task's history
2. The server resumes processing
3. State typically transitions from `input-required` back to `working`

### Artifacts

Artifacts are the **outputs** of a task:
- Produced during `working` state
- Each artifact has `id`, `name`, optional `description`, and `parts`
- Parts can be TextPart, FilePart, or DataPart
- In streaming mode, artifacts are delivered incrementally via `TaskArtifactUpdateEvent`
- Multiple artifacts can be produced per task

### State Transition History

If the agent declares `stateTransitionHistory: true` in its Agent Card:
- The task object includes a complete history of all state transitions
- Each transition records the state, timestamp, and optional message
- Useful for auditing and debugging

### Best Practices

- Always validate state transitions — reject invalid ones with appropriate errors
- Use task IDs that are globally unique (UUIDs recommended)
- Store task state durably for production (not just in-memory)
- Set timeouts for tasks stuck in non-terminal states
- Clean up old tasks to prevent unbounded storage growth
- Include meaningful messages in status updates (not just the state enum)
- Use artifacts for structured outputs, messages for conversational exchanges
- Implement idempotency — handle duplicate messages for the same task gracefully

Fetch the specification for the exact Task object schema, state enum values, and transition validation rules before implementing.
