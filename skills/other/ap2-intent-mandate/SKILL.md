---
name: ap2-intent-mandate
description: Implement the AP2 Intent Mandate — the human-not-present VDC that pre-authorizes agent purchases within defined constraints. Use when building autonomous agent shopping with user-signed intent, TTL, and constraint enforcement.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Intent Mandate

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for the Intent Mandate schema
2. Web-search `site:github.com google-agentic-commerce AP2 intent mandate` for type definitions and samples
3. Fetch `https://ap2-protocol.org/topics/core-concepts/` for Intent Mandate conceptual details
4. Web-search `ap2 protocol intent mandate human-not-present autonomous` for implementation guides

## Conceptual Architecture

### What the Intent Mandate Is

The Intent Mandate is the **VDC for human-not-present transactions**. It captures the user's pre-authorized shopping intent with defined constraints, allowing the Shopping Agent to act autonomously within those bounds after the user has left the session.

### Who Creates It

The **Shopping Agent** creates the Intent Mandate based on the user's expressed intent. The agent captures the user's requirements and formalizes them into a structured mandate.

### Who Signs It

The **User** signs the Intent Mandate before going offline:
- Hardware-backed device key with in-session authentication
- Signature proves the user reviewed and authorized the intent
- Must be signed before the user leaves the session

### Intent Mandate Contents

The spec describes several conceptual properties for the Intent Mandate (payer/payee identities, authorized payment method categories, risk payload, shopping intent, etc.). The actual **V0.1 implementation** uses the following `IntentMandate` Python type fields:

- **`user_cart_confirmation_required`** (`bool`) — Whether the user must confirm the cart before purchase
- **`natural_language_description`** (`str`) — The user's actual words / shopping intent, captured for accountability
- **`merchants`** (`Optional[List[str]]`) — Optional list of preferred or allowed merchants
- **`skus`** (`Optional[List[str]]`) — Optional list of specific SKUs the agent may purchase
- **`requires_refundability`** (`Optional[bool]`) — Whether the user requires the purchase to be refundable
- **`intent_expiry`** (`str`, ISO 8601) — When this authorization expires (e.g., `"2025-09-02T12:00:00Z"`)

Note: Use `intent_expiry` (an ISO 8601 timestamp) rather than a generic "TTL" concept.

Additional conceptual fields described in the specification (but not necessarily present in V0.1 types) include:
- Payer/payee identities
- Authorized payment method categories
- Risk payload for fraud assessment
- Decision criteria (price range, brand preferences, quality requirements)
- User device signature (cryptographic proof of authorization)

### How It Differs from Cart Mandate

| Aspect | Cart Mandate | Intent Mandate |
|--------|-------------|----------------|
| **Scenario** | Human-present | Human-not-present |
| **Created by** | Merchant | Shopping Agent |
| **Specificity** | Exact items, prices, totals | Categories, constraints, intent |
| **Payment method** | Specific tokenized method | Authorized categories |
| **User presence** | User present at signing | User signs before leaving |
| **Expiration** | Transaction-scoped | `intent_expiry` (ISO 8601 timestamp) |

### Intent Mandate Flow

1. User expresses shopping intent to Shopping Agent
2. Shopping Agent interprets and structures the intent
3. Shopping Agent presents Intent Mandate summary to user
4. Agent repeats back understanding for confirmation
5. User confirms via in-session authentication and signs
6. User may go offline
7. Shopping Agent presents Intent Mandate to Merchant(s)
8. Merchant evaluates whether they can fulfill within constraints
9. If merchant is uncertain → may force user confirmation (escalate to human-present)
10. If merchant needs clarification → asks questions (updates Intent Mandate)
11. If merchant can fulfill → proceeds with purchase

### Constraint Enforcement

The Intent Mandate defines boundaries the agent must stay within:
- **Price limits** — Maximum amount authorized
- **Product categories** — Only buy items in specified categories
- **Brand preferences** — Preferred or required brands
- **Quality criteria** — Minimum quality or rating requirements
- **`intent_expiry`** — Authorization expires at the specified ISO 8601 timestamp

### Merchant Escalation

The merchant can escalate a human-not-present flow to human-present:
- Request user select from specific SKU options → becomes Cart Mandate flow
- Ask clarification questions → updates Intent Mandate
- Force user confirmation → full human-present authorization required

### Best Practices

- Capture the user's natural language intent verbatim for audit
- Set reasonable `intent_expiry` values — don't leave Intent Mandates valid indefinitely
- Include clear constraints that are machine-evaluable
- Handle the escalation to human-present gracefully
- Store signed Intent Mandates for dispute resolution
- Validate that the final purchase falls within the Intent Mandate constraints
- Log the constraint evaluation for audit trail

Fetch the specification for exact Intent Mandate fields, constraint formats, and TTL semantics before implementing.
