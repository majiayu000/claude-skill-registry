---
name: ucp-buyer-consent
description: Implement the UCP Buyer Consent extension — GDPR/CCPA consent collection, consent fields in checkout sessions, and privacy-compliant consent management. Use when adding consent flows, privacy compliance, or data processing agreements to UCP checkout.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Buyer Consent Extension

## Before writing code

**Fetch live docs**:
1. Fetch `https://ucp.dev/specification/buyer-consent/` for the canonical Buyer Consent extension spec
2. Web-search `site:ucp.dev buyer consent` for related pages and examples
3. Web-search `site:github.com Universal-Commerce-Protocol buyer consent` for SDK support and samples
4. Fetch `https://ucp.dev/specification/overview/` for how extensions integrate with the core spec

## Conceptual Architecture

### What Buyer Consent Does

The Buyer Consent extension adds **privacy-compliant consent collection** to UCP checkout sessions. It enables merchants to collect and record buyer consent for data processing, marketing, and terms acceptance — satisfying GDPR, CCPA, and other privacy regulations.

### Why It Exists

Agentic commerce introduces a new challenge: an AI agent acts on behalf of the buyer. Regulations require explicit, informed consent for data processing. This extension standardizes how consent is requested, granted, and recorded across the UCP protocol.

### Extension Identity

- **Layer**: Extension (composable add-on to the Checkout capability)
- **Parent capability**: Checkout
- **Discovery**: Negotiated via `capabilities.extensions[]` like all UCP extensions

### Key Concepts

- **Consent fields** — The spec defines exactly four boolean consent fields:
  - `analytics` — consent for analytics/measurement data collection
  - `preferences` — consent for personalization and preference storage
  - `marketing` — consent for marketing communications
  - `sale_of_data` — consent for sale/sharing of personal data
- **Consent values** — Each field is a simple **boolean** (`true`/`false`). There is no status enum.
- **All fields are optional** — The protocol communicates consent declaratively; it does not enforce compliance

### How It Works in Checkout

1. **Merchant declares consent fields** — In the checkout session response, the merchant includes consent fields it wants to collect
2. **Agent presents consent to buyer** — The agent shows consent requests to the human buyer (this is a human-in-the-loop step)
3. **Buyer sets consent values** — The buyer decides true/false for each consent field
4. **Agent submits consent** — In the next session update, the agent includes the buyer's consent boolean values
5. **Consent communicated** — The protocol communicates consent declaratively; it does not enforce compliance. Merchants are responsible for their own compliance logic

### Interaction with Checkout Status

All consent fields are optional booleans. The protocol does not define consent as blocking checkout. Merchants may choose to enforce consent requirements in their own business logic, but the UCP spec itself does not mandate that missing consent prevents checkout completion.

### Privacy Regulations Addressed

| Regulation | Requirement | How Buyer Consent Helps |
|-----------|-------------|------------------------|
| **GDPR** (EU) | Explicit consent for data processing | Structured consent collection with audit trail |
| **CCPA** (California) | Right to know, right to opt-out | Consent types for data collection and sale |
| **LGPD** (Brazil) | Legal basis for processing | Consent as legal basis documentation |
| **PIPEDA** (Canada) | Meaningful consent | Human-readable consent text |

### Extension Negotiation

Like all UCP extensions:
1. Platform includes `buyer_consent` in `capabilities.extensions[]`
2. Business confirms support in the response
3. If not negotiated, consent fields are absent from the session

### Use Cases

- E-commerce checkout with GDPR-required consent (analytics, marketing, sale_of_data)
- Marketing opt-in collection during purchase (marketing field)
- Personalization preferences during checkout (preferences field)
- Data sharing consent for third-party fulfillment (sale_of_data field)

### Best Practices

- Always collect consent from the human buyer, never auto-grant via the agent
- Store consent records with timestamps for audit compliance (your application should track this; the protocol does not include a consent_timestamp field)
- Make consent context clear, specific, and in the buyer's language
- The protocol communicates consent declaratively; it does not enforce compliance. Your application is responsible for enforcement logic.
- Support consent withdrawal post-purchase (per GDPR Article 7)
- Test with different regulation scenarios (EU buyer, US buyer, etc.)

Fetch the Buyer Consent extension specification for exact field names, consent type enumerations, and schema structure before implementing.
