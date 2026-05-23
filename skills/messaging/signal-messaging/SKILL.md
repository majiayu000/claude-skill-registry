---
name: signal-messaging
description: Send and receive Signal messages via MCP. Use this skill when you need to interact with Signal messenger - sending messages, reading conversations, or automating Signal-based workflows.
version: 1.0.0
---


# Signal Messaging via MCP

Interact with Signal messenger through the local MCP server.

## Setup

The Signal MCP server is configured in `~/.mcp.json`:

```json
{
  "signal": {
    "command": "cargo",
    "args": ["run", "--release", "--example", "signal-server-stdio"],
    "cwd": "/Users/alice/signal-mcp",
    "env": {
      "RUST_LOG": "signal_mcp=info"
    }
  }
}
```

## Prerequisites

1. Clone and build the signal-mcp server:
   ```bash
   cd /Users/alice/signal-mcp
   cargo build --release --example signal-server-stdio
   ```

2. Register/link your Signal account with the server

## Usage

Use `read_mcp_resource` to interact with Signal:

```json
{"server": "signal", "uri": "signal://..."}
```

## Capabilities

- Send messages to contacts or groups
- Read incoming messages
- List conversations
- Handle attachments

## Troubleshooting

- Ensure the server starts: `cargo run --release --example signal-server-stdio`
- Check logs: `RUST_LOG=signal_mcp=debug`
- Verify Signal account is registered/linked
- Restart Amp after config changes



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Scientific Computing
- **scipy** [○] via bicomodule
  - Hub for numerical/scientific computation

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.