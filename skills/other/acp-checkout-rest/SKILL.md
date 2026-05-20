---
name: acp-checkout-rest
description: Implement the ACP REST checkout API — create, update, retrieve, complete, and cancel checkout sessions. Use when building merchant-side checkout endpoints, handling the checkout session state machine, or integrating with AI agent checkout flows.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Checkout — REST Binding

## Before writing code

**Fetch live docs**:
1. Fetch `https://developers.openai.com/commerce/specs/checkout/` for the canonical checkout specification
2. Web-search `site:github.com agentic-commerce-protocol spec openapi checkout` for the latest OpenAPI YAML
3. Fetch `https://developers.openai.com/commerce/guides/key-concepts/` for data model details
4. Web-search `site:docs.stripe.com agentic-commerce protocol specification` for Stripe's merchant-side reference

## Conceptual Architecture

### Five Checkout Operations

| Operation | Method | Path | Success |
|-----------|--------|------|---------|
| Create | POST | `/checkout_sessions` | 201 |
| Update | POST | `/checkout_sessions/{id}` | 200 |
| Retrieve | GET | `/checkout_sessions/{id}` | 200 |
| Complete | POST | `/checkout_sessions/{id}/complete` | 200 |
| Cancel | POST | `/checkout_sessions/{id}/cancel` | 200 |

### Session State Machine

```
not_ready_for_payment → ready_for_payment → completed
         |                      |                |
         +──────────────────────+→ canceled ←────+
                                |
                           in_progress
                                |
                      authentication_required
```

The five core status enum values are: `not_ready_for_payment`, `ready_for_payment`, `completed`, `canceled`, `in_progress`. Note that `authentication_required` is a transitional/conditional state (returned during 3DS flows), not one of the five core status values.

The merchant controls status transitions. The agent reads the status and reacts.

### Required Headers (Every Request)

- `Authorization: Bearer <token>` — REQUIRED
- `API-Version: YYYY-MM-DD` — REQUIRED
- `Idempotency-Key: <UUID>` — REQUIRED on all POST
- `Content-Type: application/json`

### Core Data Objects

- **CheckoutSession** — The central primitive: ID, status, currency, line items, fulfillment options, totals, messages, links, payment provider
- **Item** — `id` + `quantity` (sent by agent in create/update)
- **LineItem** — Merchant's expanded view: base amount, discount, subtotal, tax, total, name, description, images
- **Total** — Typed breakdown: `items_base_amount`, `items_discount`, `subtotal`, `discount`, `fulfillment`, `tax`, `fee`, `total`
- **FulfillmentOption** — Shipping/digital/pickup/local delivery with pricing and windows
- **Address** — Buyer's fulfillment address
- **Buyer** — First name, last name, email, optional phone

### Monetary Values

All amounts are **integers in minor currency units** (cents). `$19.99` = `1999`. Floating-point is prohibited.

### Messages

The `messages[]` array allows merchant-to-agent communication:
- Inform the agent about restrictions, policies, or required actions
- Messages have types (info, warning, error) that influence agent behavior

### Links

The `links[]` array provides actionable URLs with spec-defined link types:
- `terms_of_use` — Merchant terms of use page
- `privacy_policy` — Merchant privacy policy page
- `seller_shop_policies` — Merchant shop policies page

### Create Flow

1. Agent sends items + optional buyer info + optional address
2. Merchant validates items against inventory
3. Merchant computes line items, fulfillment options, totals
4. Returns session with `not_ready_for_payment` or `ready_for_payment`

### Update Flow

1. Agent sends modified items, address, fulfillment choice, or buyer info
2. Merchant revalidates and recomputes everything
3. Returns updated session with new status

### Complete Flow

1. Agent sends payment data (SPT from delegated payment)
2. Merchant processes payment via PSP
3. On success: returns session with `completed` status + order details
4. On 3DS required: returns `authentication_required` + authentication challenge
5. Agent must handle 3DS and retry complete with authentication result

### Error Handling

- All errors return flat objects: `type`, `code`, `message`, `param`
- Use `param` (JSONPath) to indicate which field caused the error
- Handle idempotency conflicts (422) and in-flight duplicates (409)

Fetch the OpenAPI spec for exact request/response schemas, field types, and all possible error codes before implementing.
