---
name: a2a-jsonrpc-transport
description: Implement the A2A JSON-RPC 2.0 transport layer — request/response format, method routing, batch requests, and HTTP details. Use when building custom A2A transport handling or debugging protocol-level issues.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A JSON-RPC 2.0 Transport

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the transport layer section
2. Web-search `site:github.com a2aproject A2A JSON-RPC transport` for transport protocol details
3. Fetch `https://www.jsonrpc.org/specification` for the JSON-RPC 2.0 base specification
4. Fetch SDK docs for transport-level classes and middleware

## Conceptual Architecture

### Why JSON-RPC 2.0

A2A uses JSON-RPC 2.0 as its transport protocol because:
- **Simple** — Lightweight request/response format
- **Standard** — Well-established protocol with broad tooling support
- **Language-agnostic** — Works with any language that handles JSON over HTTP
- **Extensible** — Custom methods without changing the protocol

### Request Format

Every A2A request is a JSON-RPC 2.0 request:
```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "id": "unique-request-id",
  "params": { ... }
}
```

- **jsonrpc** — Always `"2.0"`
- **method** — The A2A method name (e.g., `message/send`, `tasks/get`)
- **id** — Client-generated unique ID for matching responses
- **params** — Method-specific parameters (object)

### Response Format

Success:
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "result": { ... }
}
```

Error:
```json
{
  "jsonrpc": "2.0",
  "id": "unique-request-id",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": { ... }
  }
}
```

### HTTP Details

- **Method**: All A2A requests use HTTP POST
- **URL**: The agent's endpoint URL (from the Agent Card)
- **Content-Type**: `application/json` for regular requests
- **Response Content-Type**: `application/json` for `message/send`, `text/event-stream` for `message/stream`
- **HTTP Status**: Typically `200 OK` — errors are in the JSON-RPC response body, not HTTP status codes

### A2A Methods

| Method | Direction | Purpose |
|--------|-----------|---------|
| `message/send` | Client → Server | Send message, get synchronous response |
| `message/stream` | Client → Server | Send message, get SSE stream |
| `tasks/get` | Client → Server | Retrieve task by ID |
| `tasks/cancel` | Client → Server | Cancel a task |
| `tasks/resubscribe` | Client → Server | Re-subscribe to task's SSE stream |
| `tasks/pushNotificationConfig/set` | Client → Server | Register push notification |
| `tasks/pushNotificationConfig/get` | Client → Server | Get notification config |
| `tasks/pushNotificationConfig/list` | Client → Server | List notification configs |
| `tasks/pushNotificationConfig/delete` | Client → Server | Delete notification config |
| `agent/authenticatedExtendedCard` | Client → Server | Get extended Agent Card |

### Method Routing

The server must route incoming requests by the `method` field:
1. Parse the JSON body
2. Validate JSON-RPC 2.0 structure
3. Extract the `method` field
4. Route to the appropriate handler
5. Return the handler's result wrapped in a JSON-RPC response

### Request IDs

- Client generates unique IDs for each request
- Server echoes the same ID in the response
- Use UUIDs or monotonically increasing integers
- IDs enable matching responses to requests in async scenarios

### Idempotency

A2A doesn't mandate built-in idempotency, but best practice is:
- Use unique request IDs for deduplication
- Design handlers to be idempotent where possible
- For `message/send`, sending the same message twice should be handled gracefully

### Best Practices

- Use the SDK's built-in JSON-RPC handling rather than implementing from scratch
- Validate the `jsonrpc` field is exactly `"2.0"`
- Return proper JSON-RPC errors for malformed requests (not HTTP error codes)
- Log request/response pairs with IDs for debugging
- Set appropriate HTTP timeouts (longer for `message/stream`)
- Use `Content-Type: application/json` for all non-streaming requests
- Handle unknown methods gracefully with `-32601`
- Don't rely on HTTP status codes for error handling — always check the JSON-RPC response body

Fetch the specification for any additional transport requirements, header conventions, and method parameter schemas before implementing.
