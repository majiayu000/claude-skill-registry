---
name: acp-orders-webhooks
description: Implement ACP order lifecycle management and webhook event delivery. Use when building order creation, status tracking, fulfillment updates, post-purchase adjustments, and HMAC-signed webhook emission.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Orders & Webhooks

## Before writing code

**Fetch live docs**:
1. Web-search `site:github.com agentic-commerce-protocol rfcs orders` for the orders RFC
2. Fetch `https://developers.openai.com/commerce/guides/key-concepts/` for order lifecycle details
3. Web-search `site:github.com agentic-commerce-protocol examples orders` for order webhook examples
4. Web-search `site:docs.stripe.com agentic-commerce webhook` for Stripe webhook guidance

## Conceptual Architecture

### Order Lifecycle

After checkout completion, the order moves through these statuses:

```
created → confirmed → manual_review → processing → shipped → delivered
    |         |            |              |            |          |
    +─────────+────────────+──────────────+────────────+──────────+→ canceled
```

**7 statuses**:
- `created` — Order placed, payment captured
- `confirmed` — Merchant acknowledged the order
- `manual_review` — Requires human review (fraud, compliance)
- `processing` — Being prepared for fulfillment
- `shipped` — Handed to carrier (physical) or access granted (digital)
- `delivered` — Buyer received the goods
- `canceled` — Order canceled at any stage

### Webhook Events

Merchants emit two event types to the agent platform:
- **`order_created`** — Fired after successful checkout completion
- **`order_updated`** — Fired on any order status change or update

### Webhook Payload

Each webhook event contains:
- Order ID
- Checkout session ID
- Current order status
- Order permalink URL (for buyer to view)
- Fulfillment details (tracking, carrier, delivery windows)
- Line items
- Totals
- Timestamps

### HMAC Webhook Signatures

All webhook events MUST be signed:
- **Algorithm**: HMAC-SHA256
- **Header**: `Merchant-Signature` (or as specified in the latest spec)
- **Key**: Shared secret obtained during onboarding
- **Payload**: Raw request body (canonical JSON)
- **Verification**: Timing-safe comparison to prevent timing attacks

### Post-Purchase Order Adjustments

ACP supports adjustments after order creation:

| Type | Description |
|------|-------------|
| `refund` | Full refund |
| `partial_refund` | Partial amount refund |
| `store_credit` | Refund as store credit |
| `return` | Buyer returns goods |
| `exchange` | Swap for different item |
| `cancellation` | Order cancellation |
| `dispute` | Buyer disputes charge |
| `chargeback` | PSP-initiated chargeback |

Each adjustment has its own status: `pending`, `completed`, `failed`.

### Order Object

The order contains:
- `id` — Unique order identifier
- `checkout_session_id` — Links back to the checkout session
- `permalink_url` — Buyer-facing order page

### Best Practices

- Emit `order_created` immediately after payment capture
- Emit `order_updated` for every status transition
- Include all current fulfillment details in each webhook
- Use idempotent webhook delivery (include event ID for deduplication)
- Implement retry logic for failed webhook deliveries (exponential backoff)
- Sign EVERY webhook — never send unsigned events
- Use timing-safe comparison when verifying signatures on the receiving end
- Store webhook delivery status for debugging

Fetch the orders RFC and webhook examples from the GitHub repo for exact event shapes, signature format, and field definitions before implementing.
