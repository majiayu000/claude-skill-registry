---
name: mcp-management
description: "[Tooling & Meta] Manage Model Context Protocol (MCP) servers - discover, analyze, and execute tools/prompts/resources from configured MCP servers. Use when working with MCP integrations, need to discover available MCP capabilities, filter MCP tools for specific tasks, execute MCP tools programmatically, access MCP prompts/resources, or implement MCP client functionality. Supports intelligent tool selection, multi-server management, and context-efficient capability discovery."
---

# MCP Management

Manage and interact with Model Context Protocol (MCP) servers.

## Overview

MCP enables AI agents to connect to external tools and data sources. This skill provides discovery, analysis, and execution of MCP capabilities.

**Key Benefits**: Progressive disclosure, intelligent tool selection, multi-server management, persistent tool catalog (`assets/tools.json`).

## When to Use

1. Discovering MCP capabilities (tools/prompts/resources)
2. Task-based tool selection
3. Executing MCP tools programmatically
4. Building/debugging MCP client implementations
5. Context management (delegate MCP ops to subagents)

## Configuration

MCP servers configured in `.claude/.mcp.json`.

**Gemini CLI Integration**: `mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json`

**GEMINI.md**: Auto-loaded by Gemini CLI, enforces structured JSON responses:
```json
{"server":"name","tool":"name","success":true,"result":<data>,"error":null}
```

See [references/configuration.md](references/configuration.md) and [references/gemini-cli-integration.md](references/gemini-cli-integration.md).

## Execution Priority

### 1. Gemini CLI (Primary)
```bash
# IMPORTANT: Use stdin piping, NOT -p flag (deprecated, skips MCP init)
echo "Take a screenshot of https://example.com. Return JSON only per GEMINI.md instructions." | gemini -y -m gemini-2.5-flash
```
Check availability: `command -v gemini`

### 2. Direct CLI Scripts (Secondary)
```bash
cd .claude/skills/mcp-management/scripts && npm install
npx tsx cli.ts list-tools       # Saves to assets/tools.json
npx tsx cli.ts list-prompts
npx tsx cli.ts list-resources
npx tsx cli.ts call-tool <server> <tool> <json>
```

### 3. mcp-manager Subagent (Fallback)
Use when Gemini CLI unavailable. Keeps main context clean.

## Implementation Patterns

| Pattern                    | When                      | How                                            |
| -------------------------- | ------------------------- | ---------------------------------------------- |
| Gemini CLI Auto-Execution  | Default (fastest)         | `echo "task" \| gemini -y -m gemini-2.5-flash` |
| LLM-Driven Tool Selection  | Need intelligent matching | LLM reads `assets/tools.json`                  |
| Multi-Server Orchestration | Cross-server coordination | Tools tagged with source server                |
| Subagent Delegation        | Context efficiency        | `mcp-manager` agent handles MCP ops            |

## Scripts Reference

| Script                  | Purpose                                                                     |
| ----------------------- | --------------------------------------------------------------------------- |
| `scripts/mcp-client.ts` | Core MCP client (config, connect, list, execute)                            |
| `scripts/cli.ts`        | CLI interface (`list-tools`, `list-prompts`, `list-resources`, `call-tool`) |

## Technical Details

See [references/mcp-protocol.md](references/mcp-protocol.md) for JSON-RPC protocol, message types, error codes, transports.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
