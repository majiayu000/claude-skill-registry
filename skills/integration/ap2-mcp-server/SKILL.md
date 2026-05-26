---
name: ap2-mcp-server
description: Implement AP2 MCP servers — payment tools exposed via Model Context Protocol for agent access to payment capabilities. Use when building MCP-based payment tool integrations for AP2.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# AP2 MCP Server Integration

## Before writing code

**Fetch live docs**:
1. Fetch `https://ap2-protocol.org/specification/` for MCP server references
2. Fetch `https://ap2-protocol.org/topics/ap2-a2a-and-mcp/` for MCP integration details
3. Fetch `https://ap2-protocol.org/roadmap/` to check MCP server availability status
4. Web-search `site:github.com google-agentic-commerce AP2 MCP server` for MCP implementations

## Conceptual Architecture

### AP2 + MCP

While AP2's primary integration is with A2A (agent-to-agent), it also integrates with **MCP (Model Context Protocol)** for tool-based access to payment capabilities:

- **A2A** — Agent-to-agent: Shopping Agent ↔ Merchant Agent communication
- **MCP** — Agent-to-tool: Agent accessing payment APIs as tools

### MCP's Role in the Stack

MCP provides the foundational layer for connecting agents to external resources:
```
Agent
  ├── A2A → Other Agents (Merchant, CP, MPP)
  └── MCP → Payment Tools (APIs, databases, services)
```

### AP2 MCP Server

The AP2 MCP server exposes payment-related tools that agents can call:
- Payment method management tools
- Mandate creation and signing tools
- Transaction status tools
- Receipt retrieval tools

### Roadmap Status

The AP2 roadmap includes:
- **V0.1**: A2A extension (primary), MCP server v0.1
- **V1.x**: MCP-based implementation sequence diagrams, expanded MCP support

Check the latest roadmap and GitHub for current MCP server availability.

### MCP Tool Patterns for Payments

> **Note**: The following tool names are entirely **speculative/hypothetical examples** illustrating what an AP2 MCP server might expose. They are **not from any published AP2 MCP server specification or implementation**. Always check the latest AP2 roadmap and GitHub repositories for actual MCP tool definitions.

Hypothetical AP2 MCP tools:

| Tool | Description |
|------|-------------|
| `list_payment_methods` | Get available payment methods for a user |
| `create_intent_mandate` | Build an Intent Mandate from shopping parameters |
| `create_cart_mandate` | Build a Cart Mandate from product/price details |
| `validate_mandate` | Verify mandate signatures and contents |
| `process_payment` | Submit a payment for processing |
| `get_transaction_status` | Check payment processing status |
| `get_receipt` | Retrieve a payment receipt |

### When to Use MCP vs A2A for Payments

| Scenario | Use |
|----------|-----|
| Agent calling another agent (Merchant, CP) | A2A |
| Agent calling a payment API/tool directly | MCP |
| Multi-step agent negotiation | A2A |
| Simple payment status check | MCP |
| Complex multi-party flow | A2A |
| Tool-based payment method query | MCP |

### Integration Architecture

```
Shopping Agent
  ├── A2A → Merchant Agent
  ├── A2A → Credentials Provider Agent
  ├── MCP → Payment Tools Server
  └── MCP → Product Catalog Server
```

### Best Practices

- Use A2A for multi-party payment flows (the primary AP2 pattern)
- Use MCP for single-call tool operations (status checks, receipts)
- Don't expose raw payment credentials through MCP tools
- Follow the same security model (VDCs, signing) regardless of transport
- Check the roadmap for MCP server maturity before relying on it
- Test MCP tools alongside A2A flows for consistency

Fetch the latest roadmap and any published MCP server implementations for exact tool schemas and availability before implementing.
