---
name: ap2-dev-patterns
description: Apply AP2 cross-cutting development patterns — multi-agent payment architecture, UCP integration, x402 crypto payments, testing with mock providers, and production deployment. Use when architecting agentic payment systems or solving cross-cutting payment concerns.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Development Patterns

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for the latest protocol details
2. Fetch `https://ap2-protocol.org/topics/ap2-and-ucp/` for UCP integration patterns
3. Fetch `https://ap2-protocol.org/topics/ap2-and-x402/` for x402 crypto integration
4. Web-search `site:github.com google-agentic-commerce AP2 samples` for reference architectures

## Conceptual Architecture

### Multi-Agent Payment Architecture

The standard AP2 architecture involves four agents communicating via A2A:

```
┌──────────────────────────────────────────────────┐
│                    User                           │
│          (trusted device surface)                 │
└──────────┬───────────────────────────────────────┘
           │ intent + signatures
┌──────────▼───────────────────────────────────────┐
│            Shopping Agent (SA)                     │
│    Orchestrator — coordinates the full flow        │
└──┬──────────────┬────────────────────────────────┘
   │              │
   │ A2A          │ A2A
   │              │
┌──▼──────┐  ┌───▼──────────┐
│ Merchant │  │ Credentials  │
│ Agent    │  │ Provider     │
│          │  │              │
│ catalog  │  │ payment      │
│ cart     │  │ methods      │
│ signing  │  │ tokenization │
└────┬─────┘  └──────────────┘
     │
     │ (Merchant → MPP)
     │
┌────▼─────────────┐
│ Merchant Payment  │
│ Processor (MPP)   │
│                   │
│ authorization     │
│ settlement        │
│ Payment Mandate   │
│ challenges        │
└────────┬──────────┘
         │
    ┌────▼──────────┐
    │ Network/Issuer │
    │ (Visa, MC,     │
    │  banks)        │
    └────────────────┘
```

**Important**: The SA communicates with the Merchant and the CP via A2A. The Merchant communicates with the MPP. The SA does **not** directly communicate with the MPP.

### UCP Integration Pattern

UCP (Universal Commerce Protocol) operationalizes AP2:
- UCP's **Checkout object** maps to a commerce-level checkout flow
- UCP's `checkout_mandate` is distinct from (but related to) AP2's **Cart Mandate** — `checkout_mandate` is a UCP-specific concept that wraps the commerce checkout authorization, while AP2's Cart Mandate is the cryptographically signed VDC binding user consent to specific transaction terms
- UCP's `/complete_checkout` API = AP2's payment authorization step
- **PaymentMandate** (constructed by the MPP) proves payment authorization for the network/issuer

Use UCP when you need the full commerce checkout flow (catalog, cart, checkout, orders) with AP2's payment security.

### x402 Crypto Payment Pattern

AP2 supports emerging digital payment methods via x402:
- AP2 is **payment-method agnostic** — supports cards and crypto
- x402 represents a specific crypto payment standard
- AP2's VDC framework provides trust infrastructure for any payment method
- Reference: `github.com/google-agentic-commerce/a2a-x402`

### Testing with Mock Providers

Development testing without real money:
- Set up internal environments with mock payment methods
- Use the official samples as test harnesses (no real payment dependencies)
- Mock Credentials Provider returns fake DPANs
- Mock Payment Processor approves without real authorization
- OTP test value: "123" (from samples)
- Use "verbose" mode for full mandate payload visibility

### Framework Flexibility

AP2 agents can be built with any framework:
- **Google ADK** — Reference implementation framework
- **LangGraph** — LangChain-based agent graphs
- **CrewAI** — Crew-based multi-agent orchestration
- **AG2** — Microsoft's agent framework
- **Custom** — Any Python/JS framework with A2A support

The protocol doesn't mandate a specific framework — only A2A compliance.

### Multi-Merchant Comparison

Shopping Agents can query multiple merchants:
1. Send Intent Mandate to Merchant A, B, C in parallel
2. Receive Cart Mandates from each
3. Compare offers (price, shipping, availability)
4. Present best options to user
5. User selects preferred offer
6. Proceed with selected merchant

### Subscription and Recurring Payments

On the V1.x roadmap:
- Standardized recurring payment flows
- Subscription management
- Recurring Intent Mandates with TTL-based reauthorization

### Production Deployment Considerations

- **Key management** — HSMs for merchant signing keys, secure hardware for user keys
- **PCI compliance** — Credentials Provider must meet PCI DSS requirements
- **Logging** — Complete audit trail for all mandates and transactions
- **Monitoring** — Track mandate creation, signing, and payment success rates
- **Scaling** — Each agent role scales independently
- **Trust establishment** — Start with allowlists, evolve to certificate-based trust

### Security Checklist

- [ ] Shopping Agent cannot access raw payment credentials
- [ ] User signatures are hardware-backed
- [ ] Merchant signatures are entity-level (not agent-level)
- [ ] All mandates are stored with signatures for audit
- [ ] Challenge flows redirect to trusted surfaces
- [ ] Risk signals are captured at transaction time
- [ ] PCI data stays within Credentials Provider boundary
- [ ] Agent-to-agent communication is encrypted (HTTPS)

### Best Practices

- Start with the official samples as a foundation
- Use mocked payment providers for development
- Test the full multi-agent flow end-to-end
- Implement proper role separation from the beginning
- Build with the UCP integration pattern for full commerce flows
- Monitor the AP2 roadmap for new capabilities (push payments, subscriptions)
- Follow Google ADK patterns for the reference implementation approach
- Engage with the AP2 community on GitHub for updates

Fetch the latest specification, roadmap, and sample implementations for current capabilities and patterns before implementing.
