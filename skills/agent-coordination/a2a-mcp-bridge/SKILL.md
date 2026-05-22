---
name: a2a-mcp-bridge
description: Build bridges between A2A and MCP — wrap A2A agents as MCP tools, use MCP tools from A2A agents, and architect hybrid multi-agent systems. Use when integrating A2A agent-to-agent communication with MCP tool access.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A + MCP Bridge

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the A2A protocol details
2. Web-search `a2a mcp integration bridge agent tool` for patterns combining the two protocols
3. Web-search `site:github.com a2aproject A2A MCP` for any official A2A-MCP integration examples
4. Web-search `site:modelcontextprotocol.io specification` for the latest MCP specification

## Conceptual Architecture

### A2A vs MCP — Complementary Protocols

| Aspect | A2A | MCP |
|--------|-----|-----|
| **Purpose** | Agent-to-agent delegation | Agent-to-tool/data access |
| **Participants** | Agents (opaque, autonomous) | Agent + tool server (transparent) |
| **Communication** | Tasks with messages | Tool calls with structured I/O |
| **State** | Long-lived tasks with lifecycle | Stateless tool invocations |
| **Discovery** | Agent Cards | Server manifests |
| **Transport** | JSON-RPC over HTTP | JSON-RPC over stdio/HTTP+SSE |

### Why Bridge Them

Real-world multi-agent systems need both:
- **A2A** for delegating complex, open-ended work to other agents
- **MCP** for accessing specific tools, databases, APIs, and data sources

Bridging patterns enable agents to participate in both ecosystems.

### Bridge Patterns

#### Pattern 1: A2A Agent Wrapping MCP Tools
An A2A agent that internally uses MCP tools to fulfill tasks.

```
Client Agent → (A2A) → Bridge Agent → (MCP) → Tool Server
```

- Client sends a task via A2A
- Bridge agent interprets the task
- Bridge agent calls MCP tools to gather data/perform actions
- Bridge agent composes the result and returns via A2A

#### Pattern 2: MCP Tool Wrapping an A2A Agent
An MCP tool that delegates work to an A2A agent.

```
Agent → (MCP tool call) → MCP Server → (A2A) → Specialist Agent
```

- Agent calls an MCP tool
- MCP server sends a task to a specialist A2A agent
- A2A agent processes and returns
- MCP server returns the result as tool output

#### Pattern 3: Hybrid Orchestrator
A coordinator agent that uses both A2A and MCP:

```
Orchestrator Agent
  ├── (A2A) → Research Agent
  ├── (A2A) → Writing Agent
  ├── (MCP) → Database Tool
  └── (MCP) → Search Tool
```

### Implementation Considerations

**A2A agent using MCP tools:**
- The agent's handler connects to MCP servers as part of its processing
- MCP tool calls happen inside the `working` state
- Results from MCP tools inform the A2A task response
- The A2A client doesn't know or care that MCP is used internally

**MCP tool wrapping A2A agent:**
- MCP tool definition describes what the A2A agent can do
- Tool handler creates an A2A task, waits for completion
- Map A2A task failures to MCP tool errors
- Handle A2A multi-turn by either auto-responding or failing with a message

**State mapping:**
- A2A tasks are long-lived; MCP tool calls are short-lived
- For synchronous MCP tools wrapping A2A, block until the A2A task completes
- For async scenarios, consider returning a task ID and providing a status-check tool

### Architecture Guidelines

- Keep the bridge layer thin — don't add unnecessary abstraction
- Clearly document which protocol each component uses
- Handle timeout mismatches (MCP tools typically expect fast responses; A2A tasks can be long)
- Map error codes between protocols appropriately
- Log cross-protocol calls for debugging

### Best Practices

- Use A2A for delegation to autonomous agents, MCP for accessing deterministic tools
- Don't wrap simple tool calls as A2A agents — use MCP directly
- Don't use MCP for complex, multi-turn agent interactions — use A2A
- Consider the latency implications of cross-protocol bridges
- Test the bridge with realistic payloads and error scenarios
- Document the agent topology so developers understand the flow

Fetch the latest A2A specification and MCP specification for current schemas and integration guidance before implementing bridges.
