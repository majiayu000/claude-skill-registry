---
name: ap2-challenge-stepup
description: Implement AP2 challenge and step-up flows — 3DS2, OTP verification, redirect challenges, and trusted surface interactions. Use when building additional authentication steps during agentic payment processing.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 Challenge and Step-Up Flows

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for challenge flow specification
2. Web-search `site:github.com google-agentic-commerce AP2 challenge OTP 3DS step-up` for implementation examples
3. Fetch `https://ap2-protocol.org/topics/privacy-and-security/` for security context
4. Web-search `ap2 protocol 3DS2 OTP challenge redirect` for integration details

## Conceptual Architecture

### What Challenges Are

Challenges are **additional authentication steps** that any participant in the payment ecosystem can require during an AP2 transaction. They provide an extra layer of security beyond the mandate signatures.

### When Challenges Occur

Any ecosystem participant may trigger a challenge:
- **Payment Network** — Requires 3DS2 for high-risk transactions
- **Issuer/Bank** — Requires OTP or biometric for verification
- **Merchant** — Requires confirmation for unusual orders
- **Credentials Provider** — Requires step-up for new payment methods

### V0.1 Supported Challenge Types

AP2 V0.1 supports **redirect challenges**:
- **3DS2 (3D Secure 2.0)** — Card network strong customer authentication
- **OTP (One-Time Password)** — SMS/email/app verification codes
- User is redirected to a trusted surface (not the agent) for resolution

### Challenge Flow

```
1. Payment processing initiated
2. Network/Issuer determines challenge required
3. Challenge request returned to MPP
4. MPP sends challenge to Merchant Agent
5. Merchant Agent forwards to Shopping Agent (via A2A)
6. Shopping Agent redirects user to trusted surface
7. User completes challenge (enters OTP, completes 3DS)
8. Trusted surface confirms completion
9. Shopping Agent receives confirmation
10. Flow resumes from where the challenge was triggered
```

### Redirect Pattern

The redirect challenge follows this pattern:
- Shopping Agent can't handle the challenge itself (security)
- User is redirected to the challenger's trusted surface
- This is a separate UI/page, not an agent conversation
- User interacts directly with the challenger's system
- Completion triggers a callback/redirect back to the flow

### Key Design Decisions

**Why redirect?** Agent conversations are not trusted surfaces for authentication. The challenge must happen on a system controlled by the challenging entity.

**Why A2A messaging?** The challenge request and completion notification flow through the A2A protocol, keeping the multi-agent orchestration consistent.

**Duplicate prevention**: The protocol ensures that if one entity has already challenged the user, others are informed to avoid duplicate challenges.

### OTP Implementation (from samples)

The reference sample implements OTP:
1. MPP determines OTP required
2. Sends OTP challenge via A2A to Shopping Agent
3. Shopping Agent presents to user
4. User enters code (test value: "123")
5. Code returned to MPP for verification
6. Payment proceeds if code is valid

### 3DS2 Integration

For 3DS2 (Strong Customer Authentication):
1. Card network requires 3DS2 during authorization
2. MPP receives 3DS challenge data
3. Challenge forwarded to Shopping Agent
4. User redirected to issuer's 3DS2 page
5. User authenticates (biometric, SMS, etc.)
6. Authentication result returned
7. MPP retries authorization with 3DS result

### Backward Compatibility

AP2 challenges are backward compatible with existing systems:
- Works with existing 3DS2 infrastructure
- Compatible with existing OTP systems
- Doesn't require payment networks to change their risk systems
- Adds agentic context without breaking existing flows

### Best Practices

- Always redirect challenges to trusted surfaces — never handle auth in agent conversation
- Implement timeout handling for challenges (user may not respond)
- Support multiple challenge types (3DS, OTP, biometric)
- Handle challenge failure gracefully (retry or abort)
- Avoid duplicate challenges — check if user has already been challenged
- Log all challenges for audit and fraud analysis
- Test with various challenge scenarios in staging
- Implement fallback flows when challenges can't be completed

Fetch the specification for exact challenge message formats, redirect protocols, and completion callback schemas before implementing.
