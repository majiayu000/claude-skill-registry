---
name: ucp-ap2-mandates
description: Implement UCP AP2 Mandates extension — cryptographic payment mandates for fully autonomous agent commerce using SD-JWT credentials, merchant authorization signatures, and the Agent Payments Protocol. Use when building autonomous agent payment flows without human-in-the-loop.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP AP2 Mandates Extension

## Before writing code

**Fetch live spec**:
- Web-search `site:ucp.dev specification ap2-mandates` for the extension schema
- Fetch https://ucp.dev/2026-01-23/documentation/ucp-and-ap2/ for the conceptual relationship
- Web-search `site:ap2-protocol.org` for the AP2 protocol specification

## Conceptual Architecture

### What AP2 Enables

AP2 (Agent Payments Protocol) enables **fully autonomous agent commerce** — the agent can authorize payments cryptographically without requiring real-time human approval for each transaction. The user pre-authorizes spending parameters, and the agent proves authorization via signed credentials.

### Two Mandate Artifacts

1. **Checkout Mandate** (`ap2.checkout_mandate`): An SD-JWT+kb (Selective Disclosure JWT with Key Binding) credential that proves the user authorized the agent to complete this specific checkout at these specific terms.

2. **Payment Mandate** (`payment_data.token`): A separate credential proving payment authorization, verified by the PSP (not the Business).

### Merchant Authorization

Before the Platform generates mandates, the Business must sign the checkout terms:
- Format: **JWS Detached Content** (RFC 7515 Appendix F) — `<header>..<signature>`
- Canonicalization: **JSON Canonicalization Scheme** (RFC 8785)
- Algorithms: ES256, ES384, ES512 (elliptic curve)

The Business returns this `merchant_authorization` in the checkout response.

### 7-Step Flow

1. **Discovery** — Business publishes AP2 support in capabilities
2. **Session Activation** — Platform signals AP2 intent
3. **Business Signing** — Business returns checkout + `merchant_authorization` (JWS detached content)
4. **Authorization Generation** — Platform creates CheckoutMandate (SD-JWT-VC) + PaymentMandate
5. **Submission** — Platform sends both mandates in the `complete_checkout` call
6. **Verification** — Business verifies checkout mandate; PSP verifies payment mandate
7. **Confirmation** — Order confirmed

### Security Lock

Once AP2 is negotiated for a checkout session, a **Security Lock** is activated: neither party may revert to a standard (non-AP2) checkout flow for that session. This prevents downgrade attacks where a malicious actor could bypass the cryptographic mandate requirements by falling back to a simpler payment flow.

### Error Codes

AP2-specific errors:
- `mandate_required` — AP2 mandates needed but not provided
- `agent_missing_key` — Agent's signing key not found
- `mandate_invalid_signature` — Signature verification failed
- `mandate_expired` — Mandate past validity window
- `mandate_scope_mismatch` — Mandate doesn't match checkout terms
- `merchant_authorization_invalid` — Business signature invalid
- `merchant_authorization_missing` — Business didn't sign terms

### Implementation Guidance

This is the most complex UCP extension. Before implementing:

1. Understand SD-JWT-VC (Selective Disclosure JWT Verifiable Credentials) — this is the credential format
2. Understand JWS Detached Content (RFC 7515 Appendix F) — this is the merchant signing format
3. Understand JSON Canonicalization (RFC 8785) — deterministic JSON serialization for signing
4. Fetch the latest AP2 protocol spec from https://ap2-protocol.org for the full mandate lifecycle
5. Check the conformance test suite: https://github.com/Universal-Commerce-Protocol/conformance (ap2_test.py)

This extension is intended for advanced autonomous agent scenarios. Most initial implementations should start with standard payment handlers (Google Pay, Shop Pay) before adding AP2.
