---
name: ap2-human-present-flow
description: Implement the AP2 human-present transaction flow — the checkout process where the user is actively present to confirm cart details and payment method selection. The primary VDC in this flow is the Cart Mandate. Use when building interactive agentic checkout with user in the loop.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Human-Present Transaction Flow

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for the human-present flow specification
2. Web-search `site:github.com google-agentic-commerce AP2 samples human-present` for reference implementations
3. Fetch `https://github.com/google-agentic-commerce/AP2/blob/main/samples/python/scenarios/a2a/human-present/cards/README.md` for the card payment sample
4. Fetch `https://ap2-protocol.org/topics/core-concepts/` for flow overview

## Conceptual Architecture

### What Human-Present Means

In a human-present flow, the **user is actively engaged** throughout the transaction. They review products, select items, choose a payment method, and confirm the purchase — all while interacting with the Shopping Agent.

### The Human-Present Transaction Flow

The official AP2 specification describes approximately **11 high-level steps** for the human-present flow. The primary VDC in this flow is the **Cart Mandate**.

```
Phase 1: Shopping Intent
  1. User → Shopping Agent:    Provides shopping prompt ("I want to buy a coffee maker")
  2. SA → User:                Confirms intent and collects CP preference + shipping address

Phase 2: Product Discovery
  3. SA → CP:                  Queries Credentials Provider for available payment methods
  4. SA → Merchant:            Presents shopping intent
  5. Merchant → SA:            Creates and signs Cart Mandate(s) with product offers

Phase 3: User Confirmation
  6. SA → User:                Displays final cart + payment options
  7. User → SA:                Reviews cart, selects payment method, confirms on trusted device surface

Phase 4: Payment Processing
  8. SA → Merchant:            Sends confirmed Cart Mandate + user attestation
  9. Merchant → MPP:           Submits payment for processing
  10. MPP:                     Constructs Payment Mandate and requests credentials from CP

Phase 5: Completion
  11. MPP → Merchant → SA → User: Payment processed, receipt delivered
```

### Agent Interactions (A2A Messages)

Each step involves A2A protocol communication:
- Shopping Agent ↔ Merchant Agent: A2A tasks with mandate DataParts
- Shopping Agent ↔ Credentials Provider: A2A tasks for payment methods
- Shopping Agent ↔ Payment Processor: Indirect (via Merchant)

### User Touchpoints

The user is involved at these critical points:
- **Step 1**: Initiates the shopping request
- **Step 2**: Confirms intent and provides preferences
- **Step 6-7**: Reviews cart, selects payment, and confirms on trusted device surface (attestation)
- **Step 11**: Receives confirmation and receipt

### Trusted Device Surface

Step 7 is a **load-bearing security step**:
- User is redirected to a trusted device surface (not the agent)
- User reviews the final transaction details
- User provides attestation (biometric, PIN, etc.)
- This is hardware-backed confirmation, not just an LLM prompt
- Prevents agent manipulation of the final authorization

### Challenge Handling

During the flow, any participant may trigger a challenge:
- **3DS2** — Card network challenges for risk assessment
- **OTP** — One-time password verification
- User is redirected to a trusted surface for challenge resolution
- Flow resumes after successful challenge

### Implementation Considerations

- **Stateful flow** — The human-present transaction flow must maintain state across multiple agent interactions
- **Timeout handling** — Users may step away; implement reasonable timeouts
- **Error recovery** — Handle failures at any step with proper rollback
- **Concurrent agents** — Shopping Agent may query multiple merchants in parallel
- **Cart changes** — User may modify the cart between steps

### Best Practices

- Display clear product information at step 6 for user review
- Never skip the trusted device confirmation (step 7)
- Handle 3DS/OTP challenges gracefully
- Log every step for audit trail
- Implement timeouts for user response steps
- Support cart modification before final confirmation
- Show the user exactly what they're authorizing (items, prices, total)
- Test the full human-present transaction flow end-to-end

Fetch the specification and sample implementations for exact message formats, mandate structures at each step, and agent communication patterns before implementing.
