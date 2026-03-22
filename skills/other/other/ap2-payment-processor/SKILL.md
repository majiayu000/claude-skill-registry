---
name: ap2-payment-processor
description: Build an AP2 Merchant Payment Processor — the agent that constructs payment authorization messages, requests credentials from the Credentials Provider, processes payments, and returns receipts. Use when implementing the MPP role.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Merchant Payment Processor Implementation

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for Payment Processor responsibilities
2. Web-search `site:github.com google-agentic-commerce AP2 samples roles merchant_payment_processor` for reference implementation
3. Web-search `site:github.com google-agentic-commerce AP2 payment processor authorization` for authorization flow
4. Fetch `https://ap2-protocol.org/topics/core-concepts/` for MPP role details

## Conceptual Architecture

### What the Payment Processor Does

The Merchant Payment Processor (MPP) **handles the financial side** of the transaction on behalf of the merchant:

1. **Receives payment requests** from the Merchant Agent
2. **Requests credentials** from the Credentials Provider using the Payment Mandate
3. **Constructs authorization messages** for the payment network
4. **Processes the payment** through the network/issuer
5. **Handles challenges** (3DS2, OTP) when required
6. **Returns receipts** to the Merchant Agent

### Where It Sits in the Flow

```
Shopping Agent → Merchant Agent → MPP → Credentials Provider
                                  ↓
                            Payment Network / Issuer
                                  ↓
                            Authorization Result
                                  ↓
                     MPP → Merchant Agent → Shopping Agent → User
```

### Key Responsibilities

#### Payment Authorization
- Receive the Payment Mandate from the Merchant Agent
- Present the mandate to the Credentials Provider
- Receive tokenized/resolved credentials
- Construct network authorization message
- Submit to the payment network for authorization
- Handle authorization response (approved, declined, challenged)

#### Challenge Handling
When the network/issuer requires additional verification:
- **3DS2** — Strong customer authentication challenge
- **OTP** — One-time password verification
- The MPP triggers a redirect to a trusted user surface
- User completes the challenge
- MPP retries authorization with challenge response
- V0.1 supports redirect challenges

#### Receipt Generation
After successful authorization:
- Generate a payment receipt with transaction details
- Include authorization code, transaction ID
- Return receipt to Merchant Agent
- Receipt flows through to Shopping Agent and ultimately to user

### Payment Network Integration

The MPP interfaces with traditional payment infrastructure:
- **Card networks** — Visa, Mastercard, etc.
- **Payment gateways** — Stripe, Adyen, etc.
- **Issuing banks** — For authorization and settlement
- The Payment Mandate provides these entities visibility into the agentic nature of the transaction

### Risk Signals

The MPP may add risk signals to the authorization:
- Agent identity information
- Transaction context (human-present/not-present)
- Mandate verification results
- Risk payload from the Payment Mandate

### OTP Challenge Flow (Reference)

From the sample implementation:
1. MPP receives payment request from Merchant
2. MPP determines OTP is required
3. MPP sends challenge to Shopping Agent (via A2A)
4. Shopping Agent presents challenge to user
5. User enters OTP (test value: "123" in samples)
6. Shopping Agent returns OTP to MPP
7. MPP verifies OTP
8. MPP proceeds with payment authorization

### Best Practices

- Always validate the Payment Mandate before requesting credentials
- Handle all authorization responses (approved, declined, challenged)
- Implement proper retry logic for transient network failures
- Support multiple challenge types (3DS2, OTP)
- Generate detailed receipts for audit trail
- Log all payment attempts with outcomes
- Handle partial authorizations appropriately
- Implement idempotency for payment processing

Fetch the specification for exact MPP requirements, authorization message format, and challenge flow details before implementing.
