---
name: ucp-checkout-a2a
description: Implement UCP Checkout over the A2A (Agent-to-Agent) binding — enable autonomous agent-to-agent commerce using Agent Cards and structured message parts. Use when building agent-to-agent commerce flows.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# UCP Checkout — A2A Binding

## Before writing code

**Fetch live spec**: Web-search `site:ucp.dev specification checkout-a2a` and fetch the page for the exact message structure, DataPart keys, and Agent Card format.

Also review Google's A2A protocol spec for the underlying transport: https://google.github.io/A2A/

## Conceptual Architecture

### What is A2A?

A2A (Agent-to-Agent) is a protocol for autonomous inter-agent communication. UCP's A2A binding lets a Platform agent talk to a Business agent using structured messages rather than REST calls.

### How It Works

1. **Discovery**: Business publishes an Agent Card at the URL declared in their `/.well-known/ucp` profile under `services.dev.ucp.shopping.a2a.endpoint`.
2. **Communication**: Platform sends messages with checkout data in `DataPart` objects. Business agent responds with checkout state in `DataPart` objects.
3. **Identification**: Platform includes `UCP-Agent` header and `X-A2A-Extensions` header referencing the UCP spec version.

### Key Data Part Keys

| Key | Direction | Purpose |
|-----|-----------|---------|
| `a2a.ucp.checkout` | Both | Checkout session data |
| `a2a.ucp.checkout.payment_data` | Platform → Business | Payment credentials for completion |
| `a2a.ucp.checkout.risk_signals` | Platform → Business | Optional risk signals |
| `ap2.merchant_authorization` | Business → Platform | Merchant's JWS detached content signature for AP2 mandate flow |
| `ap2.checkout_mandate` | Platform → Business | SD-JWT+kb credential proving user-authorized agent checkout |

### Message Structure

Messages use A2A's standard format:
- `messageId`: Unique ID (used for idempotency)
- `contextId`: Session/conversation ID
- `kind`: `"message"`
- `role`: `"user"` (from platform) or `"agent"` (from business)
- `parts`: Array of TextPart and DataPart objects

Checkout data is carried in `DataPart` with the appropriate key.

### Idempotency

The Business agent uses `messageId` to detect duplicate requests. Task tracking uses `taskId` with `contextId`.

### When to Use A2A

- Fully autonomous agent-to-agent commerce (no human in the loop for most steps)
- Multi-agent architectures where commerce is one capability among many
- When you want the Business to maintain its own agent logic (not just expose tools)

### Implementation Guidance

Before implementing, fetch the latest sample A2A Business Agent from https://github.com/Universal-Commerce-Protocol/samples (look for the `a2a/` directory) to see the reference pattern.
