---
name: agentic-mcp
description: Agentic MCP - Three-layer progressive disclosure for MCP servers with Socket daemon. Use when the user needs to interact with MCP servers, query available tools, call MCP tools, or manage the MCP daemon process. Provides socket-based communication for efficient server interaction with three-layer progressive disclosure API.
---

# Agentic MCP

## Quick start

```bash
agentic-mcp daemon start --config <mcp-servers.json path>  # Start daemon
agentic-mcp metadata <server-name>                  # Get server info
agentic-mcp list <server-name>                      # List tools
agentic-mcp schema <server-name> <tool-name>        # Get tool schema
agentic-mcp call <server-name> <tool-name> --params '{"arg":"value"}'  # Call tool
agentic-mcp daemon stop                             # Stop daemon
```

## Core workflow

1. `agentic-mcp daemon start` - Start daemon
2. `agentic-mcp metadata <server>` - Layer 1: server info
3. `agentic-mcp list <server>` - Layer 2: available tools
4. `agentic-mcp schema <server> <tool>` - Layer 3: tool details
5. `agentic-mcp call <server> <tool> --params '{"arg":"value"}'` - Execute tool

## Daemon management

```bash
agentic-mcp daemon start                           # Start daemon
agentic-mcp daemon health                          # Check status
agentic-mcp daemon reload                          # Reload config
agentic-mcp daemon stop                            # Stop daemon
agentic-mcp daemon start --config <path>           # Custom config
```

**Sessions** (isolated instances):
```bash
MCP_DAEMON_SESSION=<name> agentic-mcp daemon start
```

## Query commands

```bash
agentic-mcp metadata <server>                      # Server info
agentic-mcp list <server>                          # List tools
agentic-mcp schema <server> <tool>                 # Tool schema
agentic-mcp daemon health                          # Check daemon status
```

## Tool calls

```bash
agentic-mcp call <server> <tool> --params '{"argName":"value"}'
```

**All parameters must be JSON object via `--params`**.

**JSON mode**:
```bash
agentic-mcp metadata <server> --json
agentic-mcp call <server> <tool> --params '{"arg":"value"}' --json
```

## Configuration

**mcp-servers.json**:
```json
{
  "servers": {
    "<server-name>": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-server"]
    }
  }
}
```

## Socket protocol

**Command** (newline-delimited JSON):
```json
{"id":"1","action":"metadata","server":"<server>"}
```

**Response**:
```json
{"id":"1","success":true,"data":{...}}
```

**Platform**: Windows (TCP) / Unix (domain socket)

## Examples

**Basic usage**:
```bash
agentic-mcp daemon start
agentic-mcp metadata <server>
agentic-mcp list <server>
agentic-mcp schema <server> <tool>
agentic-mcp call <server> <tool> --params '{"arg":"value"}'
```

**Multiple sessions**:
```bash
MCP_DAEMON_SESSION=proj1 agentic-mcp daemon start
MCP_DAEMON_SESSION=proj2 agentic-mcp daemon start
```

## Debugging

```bash
agentic-mcp daemon health                          # Check status
agentic-mcp daemon reload                          # Reload after config change
```

## Errors

```
✗ MCP daemon is not running
✗ Server '<name>' not found
✗ Tool '<name>' not found
✗ Required argument '<name>' not provided
```
