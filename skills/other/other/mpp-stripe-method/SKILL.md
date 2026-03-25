---
name: mpp-stripe-method
description: Configure Stripe as an MPP payment method — card and wallet payments via Shared Payment Tokens (SPTs), integrating MPP's HTTP 402 flow with Stripe's payment infrastructure. Use when enabling fiat/card payments for machine-to-machine transactions.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Stripe Payment Method (Cards via SPTs)

## Before writing code

**Fetch live docs**:
1. Fetch `https://docs.stripe.com/agentic-commerce/concepts/shared-payment-tokens` for the latest SPT API
2. Fetch `https://docs.stripe.com/payments/machine/mpp` for MPP + Stripe integration
3. Web-search `site:docs.stripe.com shared_payment granted_token` for SPT creation and usage API
4. Web-search `mppx stripe payment method server configuration` for mppx Stripe adapter setup

## Conceptual Architecture

### What Stripe Method Does in MPP

The Stripe payment method enables fiat/card payments within the MPP protocol. Instead of on-chain crypto transactions, the payment proof is a Shared Payment Token (SPT) — a one-time, merchant-scoped, amount-limited token that Stripe processes as a standard charge.

### Flow: MPP + Stripe SPT

```
1. Agent → Server:        GET /resource
2. Server → Agent:        402 with Stripe payment challenge
3. Agent → Stripe:        Create SPT (or use pre-provisioned SPT)
4. Agent → Server:        GET /resource with SPT credential
5. Server → Stripe:       PaymentIntent.create with shared_payment_granted_token
6. Stripe → Server:       Payment confirmed
7. Server → Agent:        200 OK with Payment-Receipt
```

### SPT Structure

```json
{
  "id": "spt_...",
  "usage_limits": {
    "currency": "usd",
    "max_amount": 1000,
    "expires_at": 1711234567
  },
  "deactivated_at": null,
  "deactivated_reason": null
}
```

### SPT Creation (Agent-Side)

```
POST https://api.stripe.com/v1/test_helpers/shared_payment/granted_tokens

Parameters:
  payment_method: pm_card_visa
  usage_limits[currency]: usd
  usage_limits[max_amount]: 1000
  usage_limits[expires_at]: <unix_timestamp>
  seller_details[network_id]: <seller_network_id>
  seller_details[external_id]: <optional_external_id>
```

### SPT Consumption (Server-Side)

```
POST https://api.stripe.com/v1/payment_intents

Parameters:
  amount: 500
  currency: usd
  shared_payment_granted_token: spt_...
  confirm: true
```

### Server-Side mppx Configuration

```typescript
import { Mppx, stripe } from 'mppx/server';

const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY,
  methods: [
    stripe.charge({
      // Stripe configuration for MPP
      // Automatically creates PaymentIntents when valid SPT credentials arrive
    }),
  ],
});
```

### SPT Properties

- **Single-use** — Can only be charged once
- **Time-bound** — Agent-defined expiration window
- **Amount-limited** — Cannot exceed max_amount
- **Currency-restricted** — Only functions in specified currency
- **Seller-scoped** — `network_id` isolates tokens to specific merchants

### SPT Webhook Events

| Event | Recipient | Trigger |
|-------|-----------|---------|
| `shared_payment.granted_token.used` | Seller | SPT successfully consumed |
| `shared_payment.granted_token.deactivated` | Seller | SPT revoked or expired |
| `shared_payment.issued_token.used` | Agent | Seller consumed the SPT |
| `shared_payment.issued_token.deactivated` | Agent | SPT no longer valid |

### Multi-Method Support

Combine Stripe with Tempo for maximum flexibility:

```typescript
const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY,
  methods: [
    tempo.charge({ /* Tempo config */ }),
    stripe.charge({ /* Stripe config */ }),
  ],
});
```

Clients choose their preferred method when fulfilling the challenge.

### Best Practices

- Set SPT `max_amount` to the exact payment amount (not higher)
- Set short expiration times — just enough for the payment to complete
- Implement SPT webhook listeners for lifecycle tracking
- Log SPT creation and usage for reconciliation (without sensitive data)
- Handle SPT expiration gracefully — re-provision if needed
- Never log full card numbers or CVCs (SPTs abstract away PCI data)

Fetch the latest Stripe SPT API documentation and mppx Stripe adapter docs for exact endpoint paths, request schemas, and configuration options before implementing.
