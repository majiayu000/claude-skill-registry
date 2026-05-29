---
name: ucp-dev-patterns
description: UCP development patterns — capability negotiation algorithms, idempotency implementation, error resolution loops, multi-binding servers, and production architecture. Use when designing the internal architecture of a UCP implementation or solving cross-cutting concerns.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Development Patterns

## Before writing code

**Fetch live reference**: Web-search `site:ucp.dev specification reference` for the latest data model definitions and enum values. Also check https://ucp.dev/2026-01-23/documentation/core-concepts/ for architectural guidance.

## Pattern: Capability Negotiation

Every request/response pair involves negotiation:

1. Platform sends `UCP-Agent` header with its profile URI
2. Business fetches the platform profile (cache it — don't fetch on every request)
3. Business computes the intersection: capabilities both support
4. Orphaned extensions are pruned (extensions whose parent capability is not in the intersection)
5. Business returns the negotiated `ucp` object

**Caching**: Cache the platform profile with a TTL (e.g., 5 minutes). Don't re-fetch on every request.

**Version compatibility**: If platform version > business version, return `version_unsupported`. If platform version <= business version, process using the platform's version semantics.

## Pattern: Idempotency

Every mutating operation uses `Idempotency-Key` (UUID):

1. Hash the key and check your cache/store
2. If found: return the cached response (same status code, same body)
3. If not found: process the request, cache the response keyed by the idempotency key
4. Cache duration: 24+ hours minimum

**Storage**: Use Redis, database table, or in-memory store depending on scale. Key = idempotency_key, Value = serialized response + status code.

**Race condition**: If two identical requests arrive simultaneously, use locking (database row lock, Redis SETNX) to ensure only one processes.

## Pattern: Agent Error Resolution Loop

The core Platform pattern for driving checkout to completion:

```
1. Create checkout
2. LOOP:
   a. Inspect status
   b. If "incomplete": read messages, resolve recoverable errors, update checkout, goto 2
   c. If "requires_escalation": surface continue_url to user, wait, goto 2
   d. If "ready_for_complete": acquire payment credential, call complete
   e. If "complete_in_progress": payment is being processed, poll/wait, goto 2
   f. If "completed": done — extract order
   g. If "canceled": done — report to user
3. Timeout after N iterations or session expiry
```

**Error resolution heuristics**:
- `missing_shipping_address` → prompt user for address, update checkout
- `missing_email` → prompt user for email, update checkout
- `invalid_cart_items` → item unavailable, suggest alternatives or remove
- `discount_code_invalid` → inform user, remove code

## Pattern: Multi-Binding Server

A single Business server can support REST + MCP + A2A simultaneously:

```
app/
├── core/
│   ├── checkout_service.py    # Shared business logic (binding-agnostic)
│   ├── negotiation.py         # Capability negotiation
│   └── models.py              # UCP data models (from SDK)
├── bindings/
│   ├── rest/
│   │   └── routes.py          # REST endpoints
│   ├── mcp/
│   │   └── tools.py           # MCP tool handlers
│   └── a2a/
│       └── agent.py           # A2A agent message handler
└── discovery.py               # /.well-known/ucp serving all bindings
```

The key: **all bindings share the same core business logic**. The binding layer only handles transport-specific concerns (HTTP headers vs JSON-RPC envelope vs A2A message parts).

## Pattern: Monetary Calculations

- All amounts are **integers in minor currency units** (cents). $29.99 = `2999`.
- Never use floating point for money.
- Totals include typed entries: `items_discount`, `subtotal`, `discount`, `fulfillment`, `tax`, `fee`, `total`.
- Recalculate all totals on every update (don't trust client-submitted totals).

## Pattern: Webhook Reliability

**Business (sender):**
- Implement exponential backoff: 1s, 2s, 4s, 8s, 16s... up to a max
- Set a max retry count (e.g., 10 attempts over 24 hours)
- Log failed deliveries for manual retry
- Always send the **full order entity**, not deltas

**Platform (receiver):**
- Respond 2xx immediately, process async
- Deduplicate using `event_id`
- Verify `Request-Signature` before processing
- Handle out-of-order deliveries gracefully (use `created_time` to determine freshness)

## Pattern: Testing Strategy

1. **Unit tests**: Test negotiation logic, total calculations, error message generation
2. **Integration tests**: Test each binding independently against your core logic
3. **Conformance tests**: Run the official suite from https://github.com/Universal-Commerce-Protocol/conformance
4. **Playground validation**: Use https://ucp.dev/playground/ for interactive flow testing
5. **End-to-end**: Test full flows including payment handler integration

## Ecosystem References

Always check these for the latest developments before major implementation decisions:

- **Official spec repo**: https://github.com/Universal-Commerce-Protocol/ucp
- **Meeting minutes**: https://github.com/Universal-Commerce-Protocol/meeting-minutes (governance decisions)
- **Awesome UCP**: https://github.com/Upsonic/awesome-ucp (community resources)
- **OpenAI ACP comparison**: https://github.com/agentic-commerce-protocol/agentic-commerce-protocol (competing protocol — merchants may want to support both)
