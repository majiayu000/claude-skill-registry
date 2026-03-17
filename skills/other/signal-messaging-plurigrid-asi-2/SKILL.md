---
name: signal-messaging
description: Send and receive Signal messages via MCP. Use this skill when you need to interact with Signal messenger - sending messages, reading conversations, or automating Signal-based workflows.
compatibility: Requires signal-mcp server built with Cargo. Signal account must be registered.
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
