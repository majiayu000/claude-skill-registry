---
name: ap2-cart-mandate
description: Implement the AP2 Cart Mandate — the human-present VDC that binds user authorization to a specific transaction with merchant-signed product offers and user-signed confirmation. Use when building cart creation, signing, and verification for human-present checkout flows.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Cart Mandate

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for the Cart Mandate schema
2. Web-search `site:github.com google-agentic-commerce AP2 src/ap2/types mandate` for the Python type definitions
3. Web-search `site:github.com google-agentic-commerce AP2 samples cart mandate` for sample implementations
4. Fetch `https://ap2-protocol.org/topics/core-concepts/` for Cart Mandate conceptual details

## Conceptual Architecture

### What the Cart Mandate Is

The Cart Mandate is the **primary VDC for human-present transactions**. It captures explicit user authorization for a specific set of items at specific prices, cryptographically binding the user's identity and consent to the exact transaction details.

### Who Creates It

The **Merchant Endpoint** creates and signs the Cart Mandate after receiving an Intent Mandate from the Shopping Agent. The merchant's signature guarantees fulfillment of the specified items at the specified prices.

### Who Signs It

Two signatures are required:
1. **Merchant signature** — Entity-level (not agent-level) guarantee of fulfillment
2. **User signature** — Hardware-backed device key with in-session authentication

### Cart Mandate Structure

A CartMandate has two parts: `contents` (CartContents) and `merchant_authorization` (a JWT).

**CartContents fields**: `id`, `user_cart_confirmation_required`, `payment_request` (W3C PaymentRequest), `cart_expiry`, `merchant_name`.

Based on the specification, key fields include:

```json
{
  "contents": {
    "id": "cart_identifier",
    "user_cart_confirmation_required": true,
    "payment_request": {
      "method_data": [
        {
          "supportedMethods": "https://processor.example.com/pay",
          "data": { ... }
        }
      ],
      "details": {
        "id": "order_id",
        "displayItems": [
          { "label": "Product Name", "amount": { "currency": "USD", "value": "29.99" } }
        ],
        "total": {
          "label": "Total",
          "amount": { "currency": "USD", "value": "29.99" }
        },
        "shipping_options": null
      },
      "options": {
        "requestPayerName": true,
        "requestShipping": true,
        "requestPayerEmail": false,
        "requestPayerPhone": false
      }
    },
    "cart_expiry": "2025-09-01T13:00:00Z",
    "merchant_name": "Example Merchant"
  },
  "merchant_authorization": "<base64url-header>..<base64url-signature>"
}
```

### Payment Request API Structure

Cart Mandates embed the W3C Payment Request API structure:
- **methodData** — Supported payment methods with processor endpoint URLs
- **details** — Order ID, line items with amounts, total, shipping options
- **options** — What payer information the merchant requests

### Cart Mandate Flow

1. Shopping Agent presents Intent Mandate to Merchant
2. Merchant searches catalog, finds matching products
3. Merchant creates Cart Mandate with product offers, prices, totals
4. Merchant signs the Cart Mandate (entity-level signature)
5. Cart Mandate returned to Shopping Agent
6. Shopping Agent displays cart to user
7. User reviews and confirms
8. User signs the Cart Mandate on trusted device surface

### Merchant Authorization

The `merchant_authorization` is a **Base64url-encoded JWT using detached JWS format**: `<base64url-header>..<base64url-signature>` (double dots — the payload is omitted because it is the canonicalized CartContents).

**Supported signing algorithms**: ES256, ES384, ES512 (ECDSA with P-256, P-384, P-521 curves).

**JCS (RFC 8785) canonicalization** is applied to the CartContents JSON before signing, ensuring deterministic serialization.

The JWT header MUST include `alg` and `kid` claims. The JWT payload includes: `iss`, `aud`, `iat`, `exp`, `jti`, `cart_hash`.

The merchant authorization guarantees:
- The listed products are available
- The prices are accurate
- The merchant commits to fulfilling the order at those terms
- This is an **entity** authorization, not an agent authorization — the merchant organization, not its AI agent

### User Signature

The user signature proves:
- The user reviewed the cart contents
- The user authorized the purchase
- The signature is hardware-backed (device key) and in-session authenticated
- This provides non-repudiation for dispute resolution

### Best Practices

- Always include all line items with individual prices — don't just show a total
- Include clear product descriptions the user can review
- Validate the Cart Mandate signature chain before processing payment
- Store signed Cart Mandates for dispute resolution
- Handle the case where the user rejects the cart (don't force signing)
- Include shipping options when physical fulfillment is involved
- Use the W3C Payment Request API structure consistently

Fetch the specification for exact Cart Mandate fields, signature format, and the payment_request schema before implementing.
