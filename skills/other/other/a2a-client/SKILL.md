---
name: a2a-client
description: Build an A2A client — the agent-side code that discovers other agents, sends tasks, handles responses, and manages multi-turn conversations. Use when implementing the client side that delegates work to A2A agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Client Implementation

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for client-side protocol requirements
2. Web-search `site:github.com a2aproject a2a-python client` or `a2aproject a2a-js client` for SDK client classes
3. Web-search `site:github.com a2aproject a2a-samples client` for reference client implementations
4. Fetch the target SDK README for client usage patterns

## Conceptual Architecture

### What an A2A Client Does

An A2A client is the **requesting side** that:
1. Discovers agents via Agent Cards (fetch `/.well-known/agent-card.json`)
2. Sends messages to create or continue tasks
3. Handles synchronous responses or SSE streams
4. Manages multi-turn conversations (handles `input-required` states)
5. Optionally configures push notifications for long-running tasks

### Client Workflow

```
1. Discover agent → Fetch Agent Card
2. Check capabilities → Verify the agent can handle the task
3. Authenticate → Satisfy the agent's auth requirements
4. Send message → POST JSON-RPC to agent URL
5. Handle response → Process task result or continue conversation
6. Monitor → Poll, stream, or receive push notifications
```

### Discovery

Before sending requests, the client must discover the target agent:
- **Direct URL** — Fetch `{base_url}/.well-known/agent-card.json`
- **Registry lookup** — Query an agent registry by skill tags or name
- **Referral** — Another agent provides the target agent's URL
- **Configuration** — Hard-coded agent URLs for known partners

### Sending Messages

Two modes:
- **Synchronous** (`message/send`) — Send a message, wait for the complete response
- **Streaming** (`message/stream`) — Send a message, receive SSE events as the agent processes

### Client Message Structure

```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "request-id",
  "params": {
    "message": {
      "role": "user",
      "parts": [
        { "kind": "text", "text": "Your task description" }
      ]
    },
    "configuration": {
      "acceptedOutputModes": ["text/plain", "application/json"]
    }
  }
}
```

For continuing a task, include `taskId` in params.

### Handling Responses

The client must handle different task states:
- **completed** — Extract artifacts and results
- **failed** — Handle the error, maybe retry
- **input-required** — Prompt user or generate follow-up message, send to same task
- **working** — Task still processing (poll via `tasks/get` or use streaming)
- **auth-required** — Authenticate and retry
- **rejected** — Agent refused the task, try a different agent

### Orchestration Patterns

**Sequential delegation**: Client sends tasks to agents one at a time, using results from one as input to the next.

**Parallel delegation**: Client sends tasks to multiple agents concurrently, aggregates results.

**Conditional routing**: Client reads Agent Cards to decide which agent handles each subtask based on skills.

**Fallback**: Client tries one agent, falls back to another if the first fails or rejects.

### Best Practices

- Cache Agent Cards with appropriate TTL — don't fetch on every request
- Implement retry logic with exponential backoff for transient failures
- Validate Agent Card capabilities before sending requests
- Handle all task states, not just `completed`
- Use streaming for interactive/long-running tasks
- Include meaningful request IDs for debugging and tracing
- Set appropriate timeouts for synchronous calls
- Respect the agent's declared input/output modes

Fetch the SDK documentation for exact client class names, constructor parameters, request builders, and response types before implementing.
