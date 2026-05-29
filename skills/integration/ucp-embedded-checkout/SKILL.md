---
name: ucp-embedded-checkout
description: Implement UCP Embedded Checkout Protocol — iframe/webview-based checkout UI for human escalation using JSON-RPC 2.0 over postMessage. Use when the checkout status is requires_escalation and the buyer needs a merchant-hosted UI.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Embedded Checkout Protocol (EP)

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification checkout-embedded` or fetch https://developers.google.com/merchant/ucp/guides/checkout/embedded for the exact JSON-RPC method definitions, handshake flow, and security requirements.

## Conceptual Architecture

### When Embedded Checkout Is Used

When a checkout reaches `requires_escalation` status, the agent cannot resolve the issue via API alone. The checkout response includes a `continue_url` — the Platform opens this URL in an iframe or webview so the buyer can interact with the merchant's checkout UI directly.

### Communication Protocol

The iframe communicates with the host (Platform) using **JSON-RPC 2.0 over `postMessage`**. Both sides send and receive structured messages.

### Key JSON-RPC Methods

| Method | Direction | Purpose |
|--------|-----------|---------|
| `ec.ready` | Merchant → Host | Handshake; merchant declares which capabilities it delegates to the host |
| `ec.start` | Merchant → Host | Checkout UI is visible and ready |
| `ec.payment.credential_request` | Merchant → Host | Merchant asks host to acquire a payment credential |
| `ec.line_items.change` | Merchant → Host | Cart was modified in the UI |
| `ec.buyer.change` | Merchant → Host | Buyer details were updated |
| `ec.complete` | Merchant → Host | Order was placed successfully |
| `ec.messages.change` | Merchant → Host | Errors or warnings updated |
| `ec.payment.instruments_change_request` | Merchant → Host | Merchant requests updated payment instruments |
| `ec.payment.change` | Merchant → Host | Payment state was updated |
| `ec.fulfillment.address_change_request` | Merchant → Host | Merchant requests updated fulfillment address |

### Handshake Flow

1. Host loads `continue_url` in a sandboxed iframe
2. Merchant sends `ec.ready` with a `delegate` array listing capabilities it wants the host to handle (e.g., `["payment.credential", "fulfillment.address_change"]`)
3. Host acknowledges and provides delegated capabilities
4. Merchant sends `ec.start` when UI is fully rendered

### URL Parameters

The `continue_url` may include:
- `ec_version`: Protocol version
- `ec_auth`: Session validation token
- `ec_delegate`: Comma-separated delegated actions

### Security Requirements

- CSP with `frame-ancestors <host_origin>` — merchant page must allow being framed only by the Platform
- Strict `postMessage` origin validation on both sides
- iframe `sandbox` attribute: `allow-scripts allow-forms allow-same-origin` with `credentialless`
- HTTPS required for all URLs
- **Silent tokenization is strictly PROHIBITED when the trigger originates from the Embedded Checkout**

### W3C DOMException Error Codes

Embedded Checkout methods may reject with W3C DOMException error codes:
- `abort_error` — The operation was aborted
- `security_error` — The operation violates security constraints
- `not_supported_error` — The requested capability is not supported
- `invalid_state_error` — The object is in an invalid state for this operation
- `not_allowed_error` — The operation is not allowed in the current context

### Implementation Guidance

**Business (iframe content):**
- Render checkout UI at the `continue_url`
- Implement the JSON-RPC sender/receiver over postMessage
- Send `ec.ready` on load, `ec.start` when visible
- Delegate payment credential acquisition to the host when possible
- Send `ec.complete` with order details when checkout finishes

**Platform (host):**
- Open `continue_url` in a sandboxed iframe
- Listen for postMessage events, parse JSON-RPC
- Handle `ec.payment.credential_request` by invoking the payment provider
- Handle `ec.complete` to update the agent's checkout state
- Validate message origins strictly

Fetch the exact current method signatures from the live spec before implementing.
