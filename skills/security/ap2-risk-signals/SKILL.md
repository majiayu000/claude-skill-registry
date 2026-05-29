---
name: ap2-risk-signals
description: Implement the AP2 risk signals framework — novel risk considerations for agentic payments, risk payload construction, trust establishment, and fraud assessment. Use when building risk evaluation, fraud detection, or trust scoring for AP2 transactions.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Risk Signals Framework

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for risk payload specification
2. Fetch `https://ap2-protocol.org/topics/privacy-and-security/` for risk considerations
3. Web-search `ap2 protocol risk signals fraud agentic payments` for risk framework details
4. Web-search `site:github.com google-agentic-commerce AP2 risk` for implementation references

## Conceptual Architecture

### Why Risk Signals Matter

Agentic commerce introduces **novel risk dimensions** that traditional payment systems weren't designed for. AP2's risk signals framework provides a common language for all ecosystem participants to assess transaction risk.

### Novel Agentic Risk Factors (from the official AP2 risk factor table)

| Risk Factor | Description |
|------------|-------------|
| **User asynchronicity** | User may not be present during the entire transaction journey |
| **Delegated trust** | Agents initiate transactions on behalf of users |
| **Mandate-merchant matching** | Verifying the purchase matches the authorized intent |
| **Temporal gaps** | Time between token generation and payment execution |
| **Indirect trust establishment** | CP and Merchant may not have a direct trust relationship |
| **Agent identity verification** | Verifying the agent is who it claims to be |

### Additional AI-Specific Risks (not from the official AP2 risk factor table)

The following are additional AI-specific risk considerations relevant to agentic commerce implementations, but they are **not part of the official AP2 specification's novel risk factor table**:

| Risk Factor | Description |
|------------|-------------|
| **Agent hallucination** | AI agent may misinterpret user intent |
| **Prompt injection** | Malicious inputs that manipulate agent behavior |

### Risk Payload

The risk payload is an **open-ended field structure** in V0.1:
- Intentionally flexible for industry-specific risk signals
- Allows Credentials Providers, Merchants, and Networks to pass custom risk data
- Each actor contributes their own risk assessment signals
- The payload travels with the mandate through the transaction flow

### Risk Assessment by Role

#### Shopping Agent
- Quality of intent capture (how clearly the user expressed their intent)
- Session authentication strength
- User behavioral signals

#### Credentials Provider
- Payment method risk level
- User account history
- Device trust score
- Previous transaction patterns

#### Merchant
- Order anomaly detection
- Intent-to-cart matching confidence
- Fulfillment risk assessment

#### Network/Issuer
- Card risk signals (fraud patterns, velocity checks)
- 3DS challenge decisions
- Authorization risk scoring
- AI involvement context (from Payment Mandate)

### Trust Establishment

AP2 defines trust establishment phases:

**Short-term (V0.1)**:
- Manually curated allowlists per entity
- Known partner relationships
- Pre-configured trust

**Long-term (future)**:
- Real-time trust via HTTPS certificate validation
- DNS ownership verification
- mTLS (mutual TLS) for strong identity
- API key exchange
- Identity assertions in A2A/MCP protocols
- Agent reputation systems

### Dispute Risk Assessment

For dispute resolution, risk signals help determine accountability:
- Strong user authentication → lower risk of ATO (account takeover)
- Clear Intent Mandate → lower risk of agent mispick
- Valid merchant signature → merchant committed to terms
- Matching mandate vs delivery → no fulfillment fraud

### Best Practices

- Include as many risk signals as available — more data helps better assessment
- Don't rely solely on LLM output for risk signals — use deterministic checks
- Validate agent identity cryptographically, not just by self-declaration
- Monitor for prompt injection in shopping intent
- Track temporal gaps between intent capture and payment
- Build risk scoring models specific to agentic transactions
- Log all risk signals for post-transaction analysis
- Implement anomaly detection for unusual agent behavior patterns
- Update risk models as agentic commerce patterns emerge

Fetch the specification for exact risk payload structure, supported signal types, and risk assessment requirements before implementing.
