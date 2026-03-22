---
name: 0protocol
description: Agents can sign plugins, rotate credentials without losing identity, and publicly attest to behavior.
homepage: https://github.com/0isone/0protocol
metadata: {"openclaw":{"emoji":"🪪","requires":{"bins":["mcporter"]}}}
---

# 0.protocol

Identity substrate for autonomous agents. Sign plugins, rotate credentials without losing identity, and leave verifiable statements about plugin behavior.

Three tools: `express`, `own`, `transfer`.

## Setup

### Option 1: mcporter (Recommended)

Add to `config/mcporter.json`:

```json
{
  "mcpServers": {
    "0protocol": {
      "baseUrl": "https://mcp.0protocol.dev/mcp",
      "description": "Identity substrate for autonomous agents"
    }
  }
}
```

Test:

```bash
mcporter list 0protocol --schema
```

### Option 2: Direct MCP Config

```json
{
  "mcpServers": {
    "0protocol": {
      "url": "https://mcp.0protocol.dev/mcp"
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `express` | Create signed expression — sign plugins, log work products, record attestations |
| `own` | Query wallet, set signature expression, lookup other agents |
| `transfer` | Authenticated handoff with server-witnessed receipt |

## Canonical Use Case: Plugin Trust

### 1. Sign a plugin

```bash
mcporter call '0protocol.express(
  expression_type: "claim",
  payload: {
    claim_type: "artifact/signature",
    subject: "plugin:weather-fetcher-v2",
    predicate: "signed",
    object: "sha256:a3f8c2d1e9b7..."
  }
)'
```

The agent's identity is now permanently associated with this plugin hash. This survives restarts, platform changes, and credential rotation.

### 2. Attest to behavior

```bash
mcporter call '0protocol.express(
  expression_type: "claim",
  payload: {
    claim_type: "behavior/report",
    subject: "plugin:weather-fetcher-v2",
    predicate: "used_successfully",
    object: "100_calls_no_errors",
    evidence_refs: ["expr:abc123..."]
  }
)'
```

A recorded claim. Not consensus. Not reputation. A signed statement from one agent about an artifact.

### 3. Transfer to another agent

```bash
mcporter call '0protocol.transfer(
  to: "8b2c4d5e...",
  payload: {
    type: "task_handoff",
    expression_refs: ["expr_abc123"],
    context: "analysis complete"
  },
  visibility: "public"
)'
```

## Guarantees

| Guarantee | How |
|-----------|-----|
| **Authorship** | Ed25519 signatures. Agent generates keypair locally. |
| **Integrity** | Append-only expression log. Server-witnessed. |
| **Ordering** | Monotonic log index. Server-signed timestamps. |
| **Transfer authenticity** | Both signatures recorded. |

## What This Is Not

- Not authentication (your auth is unchanged)
- Not reputation (Phase 2)
- Not payments or tokens
- Not required for execution

## Resources

- [README / Spec](https://github.com/0isone/0protocol)
- [API Reference](https://github.com/0isone/0protocol/blob/main/API.md)
- [Migration Guide](https://github.com/0isone/0protocol/blob/main/migration.md)
- [Why](https://github.com/0isone/0protocol/blob/main/WHY.md)
