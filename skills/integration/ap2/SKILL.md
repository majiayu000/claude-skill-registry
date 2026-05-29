---
name: ap2
description: |
    Use when implementing the Agent Payments Protocol (AP2) for secure, compliant AI-driven commerce. Covers intent mandates, cart mandates, payment flows, and merchant integration.
    USE FOR: agent-driven purchases, secure commerce mandates, user-authorized shopping flows, payment credential verification
    DO NOT USE FOR: API micropayments (use x402), agent communication (use a2a), tool integration (use mcp)
license: Apache-2.0
metadata:
  displayName: "AP2 (Agent Payments Protocol)"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "AP2 (Agent Payments Protocol) GitHub Repository"
    url: "https://github.com/google/anthropic-agent-payments-protocol"
  - title: "Google A2A Protocol (AP2 Extension)"
    url: "https://github.com/google/A2A"
---

# AP2 — Agent Payments Protocol

## Overview
AP2 is an open protocol from Google for secure, interoperable AI-driven commerce. It provides a common language for transactions between agents and merchants, preventing a fragmented payments ecosystem. AP2 is designed as an extension for A2A and MCP, adding a secure commerce layer on top of agent communication.

## Core Concepts

### Intent Mandate
Captures the conditions under which an AI agent can make a purchase on behalf of the user:
- Budget limits (per-transaction, daily, monthly)
- Allowed merchant categories
- Product type restrictions
- Time-based constraints

### Cart Mandate
Captures the user's final, explicit authorization for a specific cart:
- Itemized list of products/services
- Total price and currency
- User's cryptographic signature (non-repudiable proof of intent)
- Payment method reference

## Payment Flow
```
User            Agent           Merchant        Payment Provider
  │               │                │                  │
  │── "Buy X" ───►│                │                  │
  │               │── browse ─────►│                  │
  │               │◄── product ────│                  │
  │               │                │                  │
  │◄── confirm? ──│                │                  │
  │── approve ───►│  (Cart Mandate signed)            │
  │               │── purchase ───►│                  │
  │               │                │── charge ───────►│
  │               │                │◄── receipt ──────│
  │               │◄── receipt ────│                  │
  │◄── done ──────│                │                  │
```

## Key Design Principles
| Principle | Description |
|-----------|-------------|
| **User control** | Users set spending limits and approve purchases via signed mandates |
| **Verifiable credentials** | Cryptographic signatures provide non-repudiable proof of authorization |
| **Protocol-agnostic payments** | Supports pull methods (credit/debit cards) initially, with push methods (bank transfers, wallets) planned |
| **Compliant by design** | Built-in support for regulatory requirements (PCI, PSD2) |

## Phased Rollout
| Version | Scope |
|---------|-------|
| v0.1 | Core architecture, pull payment methods (credit/debit cards) |
| Future | Push payments, real-time bank transfers, e-wallets, multi-currency |

## AP2 vs x402
| Aspect | AP2 | x402 |
|--------|-----|------|
| Focus | Full commerce flow (browse → buy → receipt) | Per-request API micropayments |
| Payment methods | Cards, bank transfers, wallets | Stablecoins (USDC on Base/Solana) |
| Authorization | Intent + Cart Mandates with user signatures | Wallet-signed HTTP headers |
| Use case | Agent-driven shopping and purchases | Monetizing APIs and content |
| Relationship | Extension for A2A/MCP | Standalone HTTP protocol |

## Integration with A2A and MCP
AP2 extends existing protocols:
- **A2A**: Agent discovers a merchant agent via Agent Card, negotiates purchase via A2A tasks, uses AP2 for the payment step
- **MCP**: Agent calls a shopping tool via MCP, the tool uses AP2 internally to process the transaction

## Best Practices
- Always require user confirmation (Cart Mandate) before processing payments — agents should never make unauthorized purchases.
- Set conservative Intent Mandate limits initially and let users expand them as trust is established.
- Use the verifiable credential model for audit trails — every purchase has a cryptographic proof chain.
- Implement AP2 as a payment layer on top of A2A or MCP rather than as a standalone protocol.
- Handle partial failures gracefully — if payment succeeds but delivery fails, the protocol should support refund flows.
