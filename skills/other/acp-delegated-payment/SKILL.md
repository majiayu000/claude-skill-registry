---
name: acp-delegated-payment
description: Implement the ACP delegated payment flow and SharedPaymentToken (SPT) provisioning. Use when integrating with Stripe for payment tokenization, handling SPT lifecycle, or building the payment completion flow.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Delegated Payment & SharedPaymentToken

## Before writing code

**Fetch live docs**:
1. Fetch `https://developers.openai.com/commerce/specs/payment/` for the delegated payment specification
2. Fetch `https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens` for SPT implementation details
3. Web-search `site:docs.stripe.com agentic-commerce delegate payment` for Stripe integration guide
4. Web-search `site:github.com agentic-commerce-protocol spec openapi delegate` for the delegate payment OpenAPI spec

## Conceptual Architecture

### What Delegated Payment Solves

The agent facilitates purchases but must **never see raw card data**. Delegated payment creates a secure intermediary:
- Buyer's payment credentials go to the PSP (Stripe), not the agent or merchant
- PSP returns a single-use, scoped token (SPT)
- Agent passes the SPT to the merchant in the `complete` call
- Merchant charges via PSP using the SPT

### End-to-End Flow

```
Buyer → Agent: "Buy this"
Agent → PSP: POST /agentic_commerce/delegate_payment (credentials + constraints)
PSP → Agent: SharedPaymentToken (single-use, scoped)
Agent → Merchant: POST /checkout_sessions/{id}/complete (with SPT)
Merchant → PSP: Charge using SPT
PSP → Merchant: Payment confirmation
Merchant → Agent: Session status = completed + order
```

### SPT Constraints (Allowance)

Each SharedPaymentToken is scoped with:
- **max_amount** — Maximum chargeable amount (integer, minor units)
- **currency** — Currency code
- **checkout_session_id** — Tied to a specific session
- **merchant_id** — Only usable by the specified merchant
- **expires_at** — Expiration timestamp
- **reason** — Purpose of the allowance (value: `"one_time"` for single-use checkout tokens)

If any constraint is violated, the charge fails.

### SPT Properties

- **Single-use** — Can only be charged once
- **Time-bound** — Expires after a configured duration
- **Amount-scoped** — Cannot exceed the max amount
- **Merchant-scoped** — Only the designated merchant can use it
- **Session-scoped** — Tied to a specific checkout session

### 3D Secure Flow

When the merchant returns `authentication_required`:
1. Agent receives a 3DS challenge
2. Agent performs 3DS authentication with the buyer
3. Agent calls `complete` again with `authentication_result` containing:
   - `three_ds_cryptogram`
   - `electronic_commerce_indicator`
   - `transaction_id`
   - `version`

### SPT Webhook Events

| Event | Recipient | Purpose |
|-------|-----------|---------|
| `shared_payment.granted_token.used` | Merchant | Confirms SPT was consumed |
| `shared_payment.granted_token.deactivated` | Merchant | SPT revoked or expired |
| `shared_payment.issued_token.used` | Agent | Payment was processed |
| `shared_payment.issued_token.deactivated` | Agent | SPT invalidated |

### PCI Considerations

- Direct `/delegate_payment` integration may affect PCI DSS scope
- Network tokens preferred over full PAN (FPAN) where possible
- Never log full card numbers or CVCs
- SPT itself is not PCI-sensitive — it's a vault reference

### Best Practices

- Always set `max_amount` to the session total (not higher)
- Set short expiration times — just enough for the checkout completion
- Handle SPT expiration gracefully — re-provision if needed
- Implement SPT webhook listeners for lifecycle tracking
- Log SPT creation and usage for reconciliation (without sensitive data)

Fetch the delegated payment OpenAPI spec and Stripe SPT docs for exact endpoint, request/response schemas, and error codes before implementing.
