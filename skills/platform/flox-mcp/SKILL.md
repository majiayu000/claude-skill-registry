---
name: flox-mcp
description: MCP server wrapper for flox CLI operations - environment management via JSON-RPC
version: 1.0.0
trit: 0
role: ERGODIC
color: "#26D826"
---

# flox-mcp

MCP server exposing flox CLI operations over JSON-RPC stdio transport.

**Trit**: 0 (ERGODIC) - Coordinator role for environment orchestration

---

## Overview

This skill wraps the flox CLI as an MCP server, enabling AI agents to manage reproducible development environments programmatically. The server communicates via JSON-RPC 2.0 over stdio.

---

## MCP Tools

### flox_activate

Activate a flox environment.

```json
{
  "name": "flox_activate",
  "description": "Activate a flox environment",
  "inputSchema": {
    "type": "object",
    "properties": {
      "directory": { "type": "string", "description": "Path to environment directory" },
      "remote": { "type": "string", "description": "Remote environment (user/env)" }
    }
  }
}
```

### flox_search

Search for packages in the flox catalog.

```json
{
  "name": "flox_search",
  "description": "Search for packages",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Package search query" }
    },
    "required": ["query"]
  }
}
```

### flox_install

Install a package into the current environment.

```json
{
  "name": "flox_install",
  "description": "Install a package",
  "inputSchema": {
    "type": "object",
    "properties": {
      "package": { "type": "string", "description": "Package name or pkg-path" }
    },
    "required": ["package"]
  }
}
```

### flox_list

List installed packages in the environment.

```json
{
  "name": "flox_list",
  "description": "List installed packages",
  "inputSchema": {
    "type": "object",
    "properties": {
      "directory": { "type": "string", "description": "Environment directory" }
    }
  }
}
```

### flox_services

Manage flox services (start/stop/status/restart).

```json
{
  "name": "flox_services",
  "description": "Manage flox services",
  "inputSchema": {
    "type": "object",
    "properties": {
      "action": { 
        "type": "string", 
        "enum": ["start", "stop", "restart", "status", "logs"],
        "description": "Service action"
      },
      "service": { "type": "string", "description": "Specific service name (optional)" }
    },
    "required": ["action"]
  }
}
```

### flox_envs

List available flox environments.

```json
{
  "name": "flox_envs",
  "description": "List flox environments",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

### flox_push

Push environment to FloxHub.

```json
{
  "name": "flox_push",
  "description": "Push environment to FloxHub",
  "inputSchema": {
    "type": "object",
    "properties": {
      "force": { "type": "boolean", "description": "Force overwrite remote" }
    }
  }
}
```

### flox_pull

Pull environment from FloxHub.

```json
{
  "name": "flox_pull",
  "description": "Pull environment from FloxHub",
  "inputSchema": {
    "type": "object",
    "properties": {
      "remote": { "type": "string", "description": "Remote environment (user/env)" },
      "force": { "type": "boolean", "description": "Force overwrite local" },
      "copy": { "type": "boolean", "description": "Copy without remote link" }
    }
  }
}
```

---

## Usage

### Start the MCP Server

```bash
bb flox-mcp-server.bb
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "flox": {
      "command": "bb",
      "args": ["<path-to-skills>/flox-mcp/flox-mcp-server.bb"]
    }
  }
}
```

---

## GF(3) Integration

```
Trit: 0 (ERGODIC)
Role: Coordinator
Color: #26D826

Triad Formation:
  flox-mcp (0) + generator (+1) + validator (-1) ≡ 0 (mod 3)
```

The ERGODIC trit reflects flox's role as an infrastructure coordinator - it neither generates nor validates, but orchestrates the environment lifecycle.

---

## Dependencies

- `bb` (Babashka) - Clojure scripting runtime
- `flox` - Flox CLI installed and in PATH
- `cheshire` - JSON parsing (bundled with Babashka)

---

## References

- [flox skill](../flox/SKILL.md) - CLI command reference
- [MCP Specification](https://modelcontextprotocol.io)
- [FloxHub](https://hub.flox.dev)