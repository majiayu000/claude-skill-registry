---
name: ucp-payment-handlers
description: Implement UCP payment handlers — configure Google Pay, Shop Pay, or custom payment methods with tokenization, credential flow, and instrument schemas. Use when integrating payment processing into a UCP checkout.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Payment Handlers

## Before writing code

**Fetch live docs**:
- Google Pay handler: https://developers.google.com/merchant/ucp/guides/google-pay-payment-handler
- Shop Pay handler: Web-search `site:shopify.dev UCP Shop Pay payment handler`
- Payment architecture: https://ucp.dev/specification/overview/ (payment section)
- Reference types: https://ucp.dev/specification/reference/ (credential and instrument schemas)

## Conceptual Architecture

### Trust Triangle

```
Business <——> PSP <——> Credential Provider
```

- **Credential Provider** (Google Pay, Shop Pay): Issues encrypted payment tokens to the Platform
- **PSP** (Stripe, Adyen, etc.): Decrypts tokens, authorizes with card networks, settles funds
- **Business**: Configures which handlers/PSPs it accepts; receives credentials from Platform, forwards to PSP

**Critical security rule**: Credentials flow Platform → Business ONLY. Business MUST NEVER echo credentials back to the Platform.

### Payment Handler Concept

A payment handler is a **specification**, not an entity. It defines:
- `id`: Unique identifier for this payment handler instance
- `name`: Reverse-domain identifier (e.g., `com.google.pay`, `com.shopify.shop_pay`)
- `version`: Date-based version
- `spec`: URI to the handler specification
- `config`: Handler-specific configuration (merchant ID, accepted card networks, tokenization params)
- `config_schema`: JSON Schema defining the structure of the `config` object for this handler
- `instrument_schemas`: Schemas defining the shape of payment instruments this handler produces

Handlers are declared in the Business's discovery profile and echoed in checkout responses.

### Three Payment Processing Scenarios

1. **Digital Wallet** (Google Pay, Shop Pay): Platform acquires encrypted tokens from the wallet provider's API, sends to Business in `complete_checkout`.
2. **Direct Tokenization**: Platform calls PSP endpoint directly with Business's public key, gets network tokens.
3. **Autonomous Agent (AP2)**: Agent generates cryptographically-signed mandates proving user authorization — no human interaction needed. See the `ucp-ap2-mandates` skill.

### Credential Flow in Complete Checkout

When calling complete:
- `payment_data.instrument`: Describes the payment method (type, brand, last digits, billing address)
- `payment_data.credential`: The actual token/cryptogram (encrypted, handler-specific)

### Implementation Guidance

**Business side:**
1. Configure your PSP (Stripe, Adyen, etc.) and get merchant credentials
2. Build payment handler config for your discovery profile — fetch the exact format from the live handler spec
3. On `complete_checkout`, extract the credential and forward it to your PSP for authorization
4. Map PSP responses back to UCP checkout status (completed, or error with messages)

**Platform side:**
1. Read `payment.handlers` from the checkout response
2. Use the handler's `config` to initialize the payment provider SDK (e.g., Google Pay JS API)
3. Acquire a payment credential from the user
4. Send it in the `complete_checkout` call

Always verify the exact handler config schema from the live spec — payment handler configurations change frequently.
