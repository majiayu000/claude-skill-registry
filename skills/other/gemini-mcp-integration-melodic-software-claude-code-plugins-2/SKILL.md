---
name: gemini-mcp-integration
description: Expert guide for Model Context Protocol (MCP) integration with Gemini CLI. Covers MCP server configuration (HTTP, SSE, Stdio), connection management, and tool permissions. Use when adding MCP servers to Gemini, configuring transports, troubleshooting MCP connections, or managing tool permissions. Delegates to gemini-cli-docs.
allowed-tools: Read, Glob, Grep, Skill
---

# Gemini MCP Integration

## 🚨 MANDATORY: Invoke gemini-cli-docs First

> **STOP - Before providing ANY response about Gemini MCP:**
>
> 1. **INVOKE** `gemini-cli-docs` skill
> 2. **QUERY** for the specific MCP topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded

## Overview

Expert skill for connecting and managing Model Context Protocol (MCP) servers within the Gemini CLI ecosystem.

## When to Use This Skill

**Keywords:** MCP, model context protocol, mcp servers, mcp config, gemini mcp, stdio transport, sse transport, mcp tool permissions, mcp debugging

**Use this skill when:**

- Adding new MCP servers via `settings.json` or CLI (`gemini mcp add`)
- Configuring transports: `httpUrl`, `url` (SSE), or `command` (Stdio)
- Troubleshooting MCP connection states (`CONNECTING`, `DISCONNECTED`)
- Managing MCP tool permissions (Trust vs Ask)
- Integrating local scripts as MCP servers

## MCP Server Configuration

MCP servers are defined in the `mcpServers` object in `settings.json`.

### Transport Types

1. **Stdio (`command`):** Runs a local executable. Best for local scripts/tools.

    ```json
    "local-server": { "command": "node", "args": ["server.js"] }
    ```

2. **HTTP (`httpUrl`):** Connects via standard HTTP.
3. **SSE (`url`):** Server-Sent Events for streaming updates.

## Keyword Registry (Delegates to gemini-cli-docs)

| Topic | Query Keywords |
| :--- | :--- |
| **Adding Servers** | `gemini mcp add command`, `mcpServers settings` |
| **Transports** | `mcp transport types`, `stdio vs sse mcp` |
| **Permissions** | `mcp tool permissions`, `trust mcp server` |
| **Troubleshooting** | `mcp connection error`, `debug mcp server` |

## Quick Decision Tree

**What do you want to do?**

1. **Connect a Local Tool** -> Query `gemini-cli-docs`: "configure stdio mcp server"
2. **Connect a Remote API** -> Query `gemini-cli-docs`: "configure http mcp server"
3. **Trust a Server** -> Query `gemini-cli-docs`: "mcp server trust settings"
4. **List Tools** -> Query `gemini-cli-docs`: "list mcp tools command"
5. **Debug Connection** -> Query `gemini-cli-docs`: "troubleshoot mcp connection"

## Common Commands

- `gemini mcp add` - Interactive wizard to add a server.
- `/mcp` - List connected servers and their status.
- `gemini --debug` - View raw MCP connection logs (essential for troubleshooting connection issues).

## Test Scenarios

### Scenario 1: Add MCP Server

**Query**: "How do I add an MCP server to Gemini CLI?"
**Expected Behavior**:

- Skill activates on "MCP" or "mcp servers"
- Delegates to gemini-cli-docs for configuration
**Success Criteria**: User receives mcpServers settings.json structure

### Scenario 2: Configure Transport

**Query**: "What transport should I use for my MCP server?"
**Expected Behavior**:

- Skill activates on "mcp transport"
- Provides comparison of stdio, HTTP, SSE
**Success Criteria**: User receives transport selection guidance

### Scenario 3: Debug Connection

**Query**: "My MCP server isn't connecting to Gemini"
**Expected Behavior**:

- Skill activates on "mcp connection error"
- Provides debugging steps with --debug flag
**Success Criteria**: User receives troubleshooting workflow

## References

**Official Documentation:**
Query `gemini-cli-docs` for:

- "mcp servers"
- "mcp configuration"

## Version History

- v1.1.0 (2025-12-01): Added Test Scenarios section
- v1.0.0 (2025-11-25): Initial release
