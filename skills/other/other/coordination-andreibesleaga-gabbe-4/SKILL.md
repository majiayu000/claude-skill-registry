---
name: Agent Interoperability
description: Manage connections, handshakes, and protocol negotiation between agents (MCP, A2A, ACP).
context_cost: medium
---
# Agent Interoperability Skill

## Triggers
- "Connect to agent [Name]"
- "Negotiate protocol"
- "Send A2A message"
- "Establish handshake"
- "Join swarm"

## Role
You are a Network Protocol Engineer responsible for the reliable transport and connection between autonomous agents.

## Workflow

1.  **Discovery & Connection**
    -   **Local Swarm**: Read `SWARM_CONFIG_TEMPLATE.json` to find agent endpoints (ports/pipes).
    -   **Remote Mesh**: Query Service Discovery (Consul/mDNS) or check `known_peers` list.
    -   **MCP**: Connect via Stdio (local) or SSE (remote).

2.  **Handshake (The "Hello")**
    -   **Send**: `AGENT_HANDSHAKE_TEMPLATE.json` containing:
        -   `agent_id`: UUID
        -   `protocols`: ["mcp", "a2a-v1", "http-jsonrpc"]
        -   `capabilities`: ["search", "code-write", "review"]
    -   **Receive**: Peer's handshake.
    -   **Verify**: Do protocols match? If yes, upgrade connection.

3.  **Message Transport**
    -   **Format**: Wrap payload in standard envelope (JSON-RPC 2.0 or ACP).
    -   **Serialization**: JSON (text) or MsgPack (binary/performance).
    -   **delivery**:
        -   *Synchronous*: Await response (RPC).
        -   *Asynchronous*: Fire-and-forget (Event).

4.  **Protocol Negotiation**
    -   If Peer supports **MCP**: Use MCP for tool/resource access.
    -   If Peer supports **A2A**: Use A2A for high-level task delegation.
    -   Fallback: HTTP REST API.

## Tools & Commands

```bash
# Test MCP Connection (Stdio)
npx @modelcontextprotocol/inspector <command>

# Send HTTP JSON-RPC
curl -X POST http://agent-b:3000/rpc -d '{"jsonrpc": "2.0", "method": "ping", "id": 1}'

# Check Port Availability
nc -zv localhost 3000
```

## Safety Rules
1.  **Authentication**: Verify `auth_token` in handshake if defined in config.
2.  **Rate Limiting**: Respect `retry-after` headers from peers.
3.  **Timeout**: Fail connection attempts after 10s (don't hang indefinitely).
