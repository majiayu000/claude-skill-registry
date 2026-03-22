---
name: ucp-orders-webhooks
description: Implement UCP Order capability and webhook delivery — post-purchase order management with fulfillment tracking, adjustments (refunds/returns), and cryptographically signed webhook notifications. Use when building order management or webhook infrastructure.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Orders & Webhooks

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification order` and fetch the page for the exact order data model, webhook envelope, and signature format.

Also fetch https://ucp.dev/specification/reference/ for adjustment types, fulfillment event types, and line item status derivation rules.

## Conceptual Architecture

### Order Capability (`dev.ucp.shopping.order`)

Orders represent the post-purchase lifecycle. An order is created when a checkout completes successfully. The order contains:

- **Line items** with quantity tracking (total, fulfilled)
- **Fulfillment expectations** (estimated delivery) and **fulfillment events** (shipped, delivered, etc.)
- **Adjustments** (refunds, returns, credits, disputes, cancellations)
- **Totals** (subtotal, tax, discount, fulfillment, fee, total)

### Line Item Status Derivation

Status is derived from quantities, not stored:
- `fulfilled == total` → `"fulfilled"`
- `fulfilled > 0` → `"partial"`
- `fulfilled == 0` → `"processing"`

### Fulfillment Event Types (open string enum)

Common values: `processing`, `shipped`, `in_transit`, `delivered`, `failed_attempt`, `canceled`, `undeliverable`, `returned_to_sender`. The set is extensible — new values may appear.

### Adjustment Types (open string enum)

Common values: `refund`, `return`, `credit`, `price_adjustment`, `dispute`, `cancellation`. Also extensible.

### Webhook Delivery

- Business POSTs the **full order entity** (not incremental deltas) to the Platform's webhook URL.
- Each delivery includes an `event_id` (unique) and `created_time` (RFC 3339).
- Platform MUST respond with 2xx immediately and process asynchronously.
- Business should implement retry with exponential backoff on non-2xx responses.

### Webhook Signature (Detached JWT)

This is critical for security:

1. **Signing (Business side):**
   - Select an EC P-256 key from `signing_keys` in the Business's `/.well-known/ucp` profile
   - Create a Detached JWT (RFC 7797) over the request body
   - Set `kid` in the JWT header to match the key ID
   - Include the signature in the `Request-Signature` HTTP header

2. **Verification (Platform side):**
   - Extract `Request-Signature` header
   - Parse JWT header for `kid`
   - Fetch Business's `/.well-known/ucp` profile, find the matching key
   - Verify the JWT signature against the request body
   - Reject if verification fails

### Implementation Guidance

**Business:**
- Generate EC P-256 key pair; publish public key in discovery profile
- After checkout completion, create order entity
- On every fulfillment event or adjustment, POST the full updated order to the platform webhook URL with a fresh signature
- Implement retry logic (exponential backoff, max attempts)

**Platform:**
- Expose a webhook endpoint URL (declared in order capability config)
- Verify `Request-Signature` on every incoming webhook
- Process order updates asynchronously (respond 2xx first)
- Handle idempotency using `event_id`

Fetch the conformance test suite at https://github.com/Universal-Commerce-Protocol/conformance for webhook test cases.
