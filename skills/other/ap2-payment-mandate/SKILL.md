---
name: ap2-payment-mandate
description: Implement the AP2 Payment Mandate — the VDC shared with payment networks and issuers to signal AI involvement and user authorization. Use when building payment authorization flows, tokenization, and network integration.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Payment Mandate

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for the Payment Mandate schema
2. Web-search `site:github.com google-agentic-commerce AP2 payment mandate` for type definitions
3. Web-search `site:github.com google-agentic-commerce AP2 src/ap2/types payment` for Python types
4. Fetch `https://ap2-protocol.org/topics/core-concepts/` for Payment Mandate conceptual details

## Conceptual Architecture

### What the Payment Mandate Is

The Payment Mandate is a **separate VDC specifically for the payment ecosystem** — shared with payment networks (Visa, Mastercard) and issuers (banks). Unlike the Cart/Intent Mandates that focus on purchase authorization, the Payment Mandate provides **visibility into the agentic nature of the transaction**.

### Purpose

The Payment Mandate serves three functions:
1. **Signals AI involvement** — Tells the network/issuer that an AI agent initiated this transaction
2. **Signals user presence** — Indicates whether the user was present (human-present vs human-not-present)
3. **Provides authorization proof** — Includes user-signed authorization for the payment

### Who Creates It

The **Merchant Payment Processor (MPP)** constructs the Payment Mandate from the transaction information after the user has authorized the purchase. The Shopping Agent does not create the Payment Mandate — it is assembled on the MPP side from the payment context.

### Payment Mandate Contents

```json
{
  "payment_mandate_contents": {
    "payment_mandate_id": "pm_unique_id",
    "payment_details_id": "order_id",
    "payment_details_total": {
      "amount": {
        "currency": "USD",
        "value": "29.99"
      },
      "refund_period": 30
    },
    "payment_response": {
      "request_id": "order_id",
      "method_name": "CARD",
      "details": {
        "token": "dpan_token_xyz"
      },
      "shipping_address": null
    },
    "merchant_agent": "MerchantAgentName",
    "timestamp": "2025-09-01T12:00:00Z"
  },
  "user_authorization": "eyJhbGc..."
}
```

### Key Fields

- **payment_mandate_id** — Unique identifier for this payment mandate
- **payment_details_id** — Links back to the order/cart
- **payment_details_total** — Transaction amount, currency, and refund period
- **payment_response** — Selected payment method, tokenized credentials, shipping
- **merchant_agent** — Identity of the merchant's agent
- **user_authorization** — User's cryptographic signature
- **timestamp** — When the mandate was created

### How It Flows Through the System

```
1. User authorizes purchase on trusted device surface
2. Shopping Agent sends Cart Mandate + user attestation to Merchant
3. Merchant submits payment to Merchant Payment Processor (MPP)
4. MPP constructs the Payment Mandate from the transaction context
5. MPP requests payment credentials from Credentials Provider (CP)
6. CP verifies and performs tokenization (if needed)
7. CP returns credentials to MPP
8. Network/Issuer evaluates the mandate for risk assessment
9. Payment authorized (or challenged)
```

### Payment Method Tokenization

The Payment Mandate includes a tokenized payment method (DPAN — Digitized Primary Account Number):
- The actual card number is never exposed to the Shopping Agent
- Credentials Provider handles tokenization
- The token is bound to the specific transaction
- Network/Issuer can resolve the token to the real credentials

### Relationship to Cart/Intent Mandates

- **Cart Mandate** → authorizes what's being purchased (user → merchant)
- **Intent Mandate** → authorizes the shopping scope (user → agent)
- **Payment Mandate** → authorizes the payment (user → payment ecosystem)

All three work together: the Cart/Intent Mandate proves the purchase is authorized; the Payment Mandate proves the payment is authorized and provides network visibility.

### Refund Period

The `refund_period` field in the mandate specifies the refund window (in days). This is important for:
- Dispute resolution timelines
- Chargeback eligibility
- Merchant liability assessment

### Best Practices

- Always include a valid user_authorization signature
- Link the Payment Mandate to the corresponding Cart/Intent Mandate via IDs
- Include accurate merchant_agent identification
- Set realistic refund periods aligned with merchant policy
- Store Payment Mandates for the full refund period for dispute resolution
- Never expose raw payment credentials to Shopping Agents
- Validate the payment method token before processing

Fetch the specification for exact Payment Mandate fields, token formats, and network integration requirements before implementing.
