---
name: ai
description: |
    Use when working with AI agent protocols, standards, and interoperability specifications. Covers MCP, A2A, ACP, Agent Skills, AGENTS.md, ADL, x402, AP2, MCP Apps, and cagent.
    USE FOR: agent protocol selection, comparing MCP vs A2A vs ACP, understanding agent standards ecosystem, choosing payment protocols
    DO NOT USE FOR: specific protocol implementation details (use the sub-skills: mcp, a2a, acp, x402, etc.)
license: MIT
metadata:
  displayName: "AI Agent Protocols & Standards"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Model Context Protocol Specification"
    url: "https://modelcontextprotocol.io"
  - title: "Google A2A Protocol GitHub Repository"
    url: "https://github.com/google/A2A"
---

# AI Agent Protocols & Standards

## Overview
This skill covers the emerging ecosystem of open standards and protocols for AI agents. These specifications define how agents discover capabilities, communicate with each other, make payments, render UI, and are described declaratively.

## Protocol Landscape

| Protocol | Purpose | Maintained By |
|----------|---------|---------------|
| **MCP** | Tool integration — how agents use tools and access context | Anthropic |
| **A2A** | Agent-to-agent communication and task delegation | Google |
| **ACP** | REST-based agent communication (merged into A2A) | IBM / BeeAI / Linux Foundation |
| **Agent Skills** | Skill packaging — how capabilities are discovered and loaded | Anthropic |
| **AGENTS.md** | Project-level guidance for coding agents | Community |
| **ADL** | Declarative agent definition (identity, tools, permissions) | Next Moca / Eclipse LMOS |
| **x402** | HTTP-native micropayments using stablecoins | Coinbase |
| **AP2** | Secure agent-driven commerce and purchases | Google |
| **MCP Apps** | Rich interactive UI served by MCP servers | Anthropic |
| **cagent** | Multi-agent runtime with YAML configuration | Docker |

## How They Relate
```
┌─────────────────────────────────────────────┐
│  Agent Definition (ADL, AGENTS.md)          │
│  "What the agent is and what it can do"     │
├─────────────────────────────────────────────┤
│  Capability Discovery (Agent Skills, MCP)   │
│  "How agents find and load tools/skills"    │
├─────────────────────────────────────────────┤
│  Agent Communication (A2A, ACP)             │
│  "How agents talk to each other"            │
├─────────────────────────────────────────────┤
│  Payments (x402, AP2)                       │
│  "How agents pay for services"              │
├─────────────────────────────────────────────┤
│  UI (MCP Apps)                              │
│  "How agents render interactive interfaces" │
├─────────────────────────────────────────────┤
│  Runtime (cagent)                           │
│  "How agents are orchestrated and executed" │
└─────────────────────────────────────────────┘
```

## Choosing the Right Protocol
- **Building tools for agents to call?** Use MCP to expose them as tool servers.
- **Packaging reusable knowledge/instructions?** Use Agent Skills (SKILL.md).
- **Orchestrating multiple agents?** Use A2A for inter-agent communication (ACP's REST approach merged into A2A).
- **Monetizing an API for agent consumption?** Use x402 for micropayments.
- **Enabling agent-driven purchases?** Use AP2 for secure commerce flows.
- **Defining agent configurations declaratively?** Use ADL for portable blueprints.
- **Guiding coding agents in a repo?** Add an AGENTS.md file.
- **Serving rich UI from an MCP server?** Use MCP Apps.
- **Running multi-agent systems locally?** Use Docker cagent.
