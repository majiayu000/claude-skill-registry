---
name: acp-payment-handlers
description: Implement ACP payment handlers — pluggable payment method specifications including tokenized cards, seller-backed methods (gift cards, points, store credit), and handler negotiation. Use when adding payment methods or building custom payment handler support.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# ACP Payment Handlers

## Before writing code

**Fetch live docs**:
1. Web-search `site:github.com agentic-commerce-protocol rfcs payment_handlers` for the payment handlers RFC
2. Web-search `site:github.com agentic-commerce-protocol rfcs seller_backed` for seller-backed payment handler RFC
3. Fetch `https://developers.openai.com/commerce/specs/payment/` for payment data structures
4. Web-search `site:docs.stripe.com agentic-commerce payment handler` for Stripe's handler implementation

## Conceptual Architecture

### What Payment Handlers Are

Payment handlers are **pluggable specifications** that define how a particular payment method works within ACP. Each PSP or merchant publishes handler specs, and agents/merchants negotiate which handlers they mutually support.

This inverts the traditional integration model — instead of hardcoding payment methods into the protocol, handlers are discoverable and composable.

### Handler Identification

Each handler has a reverse-DNS name and version:
- `dev.acp.tokenized.card` — Tokenized credit/debit cards (Stripe SPT)
- `dev.acp.seller_backed.saved_card` — Pre-stored cards on merchant
- `dev.acp.seller_backed.gift_card` — Gift cards with number/PIN
- `dev.acp.seller_backed.points` — Loyalty/rewards points
- `dev.acp.seller_backed.store_credit` — Account balance/store credit

### Handler Structure

Each payment handler spec defines:
- **`id`** — Unique instance identifier within the session
- **`name`** — Specification name in reverse-DNS format (e.g., `dev.acp.tokenized.card`)
- **`version`** — Spec version
- **`spec`** — URL to the handler specification
- **`requires_delegate_payment`** — Whether the agent must call `/delegate_payment` (true for tokenized cards)
- **`requires_pci_compliance`** — Whether PCI DSS scope is affected
- **`psp`** — Which PSP processes this handler
- **`config_schema`** — JSON Schema for merchant configuration
- **`instrument_schemas`** — JSON Schema(s) for the payment instrument data the agent sends

### Tokenized Card Handler

The primary handler — uses Stripe's delegated payment:
1. Agent provisions SPT via Stripe
2. Agent sends SPT as the instrument credential in `complete`
3. Merchant charges via Stripe using the SPT
4. `requires_delegate_payment: true`

### Seller-Backed Handlers

These bypass the PSP — the merchant directly manages the payment:
- **Saved card** — Customer has a card on file with the merchant
- **Gift card** — Number + optional PIN
- **Points** — Loyalty program balance
- **Store credit** — Account balance
- `requires_delegate_payment: false`
- `requires_pci_compliance: false` (except saved cards)

### Handler Negotiation

During capability negotiation:
1. Agent advertises supported payment handlers in `capabilities.payment.handlers[]`
2. Merchant responds with handlers they accept
3. Intersection determines available payment methods for the session
4. Agent picks one and provides the appropriate instrument data

### Payment Data Structure

When completing a checkout, the agent provides:
- `handler_id` — Which handler is being used
- `instrument` — `type` + `credential` (shape defined by handler's instrument schema)
- Optional `billing_address`

### Best Practices

- Support multiple handlers to maximize conversion
- Advertise all accepted handlers in capability negotiation
- Validate instrument data against the handler's instrument schema
- Handle handler-specific errors (e.g., insufficient points, expired gift card)
- Log handler usage for payment method analytics

Fetch the payment handlers RFC and instrument schemas from the GitHub repo for exact field definitions before implementing.
