---
name: ucp-checkout-rest
description: Implement UCP Checkout over the REST binding — create, get, update, complete, and cancel checkout sessions with proper headers, idempotency, status transitions, and error handling. Use when building REST-based UCP checkout endpoints or clients.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Checkout — REST Binding

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification checkout-rest` and fetch the page for the exact current endpoint shapes, required headers, request/response schemas, and status codes.

Also fetch https://ucp.dev/specification/reference/ for all data type definitions (Buyer, LineItem, Total, Message, etc.).

## Conceptual Architecture

### Five REST Operations

| Operation | HTTP | Path | Idempotent? |
|-----------|------|------|-------------|
| Create Checkout | POST | `/checkout-sessions` | Yes (via Idempotency-Key) |
| Get Checkout | GET | `/checkout-sessions/{id}` | Naturally |
| Update Checkout | PUT | `/checkout-sessions/{id}` | Yes (full replace) |
| Complete Checkout | POST | `/checkout-sessions/{id}/complete` | Yes (via Idempotency-Key) |
| Cancel Checkout | POST | `/checkout-sessions/{id}/cancel` | Yes (via Idempotency-Key) |

### Required Headers (every request)

- `UCP-Agent`: Platform's profile URI in RFC 8941 structured field format — `profile="https://..."`
- `Idempotency-Key`: UUID for mutating operations; Business caches 24+ hours
- `Request-Id`: UUID for distributed tracing
- `Request-Signature`: Cryptographic signature for request integrity verification
- `Content-Type`: `application/json`

### Status State Machine

```
incomplete → requires_escalation → ready_for_complete → complete_in_progress → completed
     |               |                    |                      |
     +---------------+--------------------+----------------------+--------→ canceled
```

The `canceled` state is reachable from any non-terminal state (incomplete, requires_escalation, ready_for_complete, complete_in_progress).

The agent's job is to drive the session from `incomplete` to `ready_for_complete` by resolving messages, then call complete.

### Negotiation in Every Response

Every response includes a `ucp` object with the negotiated version and capabilities. The Business computes the intersection of its own capabilities with the Platform's profile, prunes orphaned extensions, and returns only what both sides support.

### Error Handling Pattern

Responses include a `messages` array. Each message has:
- `type`: error / warning / info
- `code`: Machine-readable error code
- `content`: Human-readable description
- `severity`: recoverable / requires_buyer_input / requires_buyer_review (these are the 3 formal enum values; note: `escalation` appears in some spec sections but is NOT part of the formal severity enum — this is a spec inconsistency)
- `path`: JSONPath pointing to the problematic field

**Agent behavior by severity:**
- `recoverable` → Agent fixes automatically (e.g., update with missing address)
- `requires_buyer_input` → Ask the human user
- `requires_buyer_review` → Show totals/terms for human confirmation
- `escalation` → Redirect to `continue_url`

### Implementation Checklist

**Business (merchant server):**
1. Parse `UCP-Agent` header and fetch platform profile for negotiation
2. Validate `Idempotency-Key` — return cached response if duplicate
3. Create checkout session with line items, compute totals
4. Return negotiated `ucp` object + full session state + messages
5. Handle Update by recalculating totals, re-validating, updating messages
6. Handle Complete by processing payment credential, creating order
7. Handle Cancel by cleaning up session
8. Return proper HTTP status codes (201 Created, 200 OK, 400/409/429, etc.)

**Platform (agent client):**
1. Discover Business profile at `/.well-known/ucp`
2. Send `UCP-Agent` header with own profile URI
3. Create checkout, inspect `status` and `messages`
4. Loop: resolve messages → update checkout → re-check status
5. When `ready_for_complete`: acquire payment credential, call complete
6. Handle `requires_escalation` by surfacing `continue_url` to user

### Monetary Values

All amounts are **integers in minor currency units** (e.g., $29.99 = `2999`). Never use floating point.

### TLS Requirement

All UCP REST endpoints MUST be served over HTTPS with minimum TLS 1.3.
