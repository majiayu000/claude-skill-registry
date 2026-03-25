---
name: a2a-error-handling
description: Implement A2A error handling — JSON-RPC errors, A2A-specific error codes, task failure states, retry strategies, and graceful degradation. Use when building robust error handling in A2A agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Error Handling

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the error handling section
2. Web-search `site:github.com a2aproject A2A error codes` for error code definitions
3. Web-search `site:github.com a2aproject a2a-samples error` for error handling examples
4. Fetch SDK docs for error classes and exception types

## Conceptual Architecture

### Error Categories

A2A has three categories of errors:

1. **JSON-RPC Protocol Errors** — Malformed requests, invalid methods, parse failures
2. **A2A-Specific Errors** — Protocol-level issues specific to A2A operations
3. **Task-Level Failures** — The task itself fails during processing (task state → `failed`)

### JSON-RPC 2.0 Error Format

All errors follow the JSON-RPC 2.0 error response format:
```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": { "details": "..." }
  }
}
```

### Standard JSON-RPC Error Codes

| Code | Name | Meaning |
|------|------|---------|
| `-32700` | Parse error | Invalid JSON |
| `-32600` | Invalid request | Not a valid JSON-RPC request |
| `-32601` | Method not found | Method doesn't exist or isn't supported |
| `-32602` | Invalid params | Method parameters are invalid |
| `-32603` | Internal error | Server internal error |

### A2A-Specific Error Codes

| Code | Name | Meaning |
|------|------|---------|
| `-32001` | TaskNotFoundError | The referenced `taskId` doesn't exist |
| `-32002` | TaskNotCancelableError | Task is in a state that can't be canceled (terminal state) |
| `-32003` | PushNotificationNotSupportedError | Agent doesn't support push notifications |
| `-32004` | UnsupportedOperationError | The requested operation is not supported |
| `-32005` | ContentTypeNotSupportedError | Client's accepted output modes don't match agent's capabilities |
| `-32006` | InvalidAgentResponseError | The agent returned an invalid or malformed response |
| `-32007` | ExtendedAgentCardNotConfiguredError | Extended Agent Card is not configured |
| `-32008` | ExtensionSupportRequiredError | A required extension is not supported |
| `-32009` | VersionNotSupportedError | The requested protocol version is not supported |

### Task Failure vs Protocol Error

Important distinction:
- **Protocol errors** return a JSON-RPC error response — the request itself was invalid or couldn't be processed
- **Task failures** return a normal response with the task in `failed` state — the request was valid but the task's processing failed

Example: If a client sends `message/send` with invalid JSON → `-32700` (protocol error). If a client sends a valid message but the agent's LLM call fails → task state becomes `failed` with an error message.

### Server-Side Error Handling

The server should:
1. **Validate JSON-RPC structure** — Return `-32600/-32700` for malformed requests
2. **Validate method** — Return `-32601` for unsupported methods
3. **Validate parameters** — Return `-32602` for invalid params
4. **Check task existence** — Return `-32001` for unknown task IDs
5. **Check capabilities** — Return `-32003/-32005` for unsupported features
6. **Handle extended card** — Return `-32007` if extended Agent Card is not configured
7. **Handle internal errors** — Return `-32603` for unexpected server errors
8. **Set task state** — Transition to `failed` for task-level processing errors

### Client-Side Error Handling

The client should:
1. **Parse the response** — Check for `error` field vs `result` field
2. **Handle by error code** — Different codes need different responses
3. **Retry transient errors** — `-32603` (internal error) may be retryable
4. **Don't retry permanent errors** — `-32601` (method not found) won't succeed on retry
5. **Handle task failures** — Check task state for `failed` and read the error message
6. **Fallback** — Try alternative agents if one fails

### Retry Strategy

| Error Code | Retryable? | Strategy |
|-----------|------------|----------|
| `-32700` | No | Fix the request |
| `-32600` | No | Fix the request |
| `-32601` | No | Method not available on this agent |
| `-32602` | No | Fix the parameters |
| `-32603` | Yes | Exponential backoff, max 3 retries |
| `-32001` | No | Task doesn't exist |
| `-32002` | No | Task can't be canceled |
| `-32005` | No | Content type mismatch |
| `-32007` | No | Extended Agent Card not configured |

### Best Practices

- Always include meaningful error messages, not just codes
- Use the `data` field in JSON-RPC errors for additional debugging context
- Log errors with request IDs and task IDs for traceability
- Implement circuit breakers for agents that are consistently failing
- Set task state to `failed` with a descriptive message when processing fails
- Don't expose internal implementation details in error messages to external clients
- Implement graceful degradation — if one agent in a pipeline fails, handle it upstream
- Test error paths explicitly — they're as important as the happy path

Fetch the specification for the complete list of error codes, their semantics, and any error handling requirements before implementing.
