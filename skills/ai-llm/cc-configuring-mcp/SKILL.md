---
name: cc-configuring-mcp
description: Use when optimizing MCP token usage, understanding Tool Search thresholds, or deciding MCP vs skills for token efficiency. For plugin MCP bundling, use plugin-dev:mcp-integration.
---

# Configuring MCP

## Scope

This skill covers **MCP token optimization and Tool Search**. For different purposes, use:

- **Bundling MCP in plugins:** `plugin-dev:mcp-integration`
- **This skill:** Token efficiency, Tool Search thresholds, skill wrappers for infrequent MCP

## Overview

MCP (Model Context Protocol) connects Claude Code to external tools. **Core trade-off:** MCP tools load at session start (consuming tokens) while skills load on-demand.

## Tool Search: Progressive Disclosure for MCP

### How It Works

When MCP tool definitions exceed a threshold, Claude Code defers them and uses MCPSearch to discover tools on-demand.

```
Without Tool Search: 77K tokens consumed before any work
With Tool Search:    8.7K tokens (85% reduction)
```

### Configuration

| Value    | Behavior                                |
| -------- | --------------------------------------- |
| `auto`   | Activates at 10% of context (default)   |
| `auto:N` | Activates at N% (e.g., `auto:5` for 5%) |
| `true`   | Always use Tool Search                  |
| `false`  | Never use Tool Search                   |

**Set via environment:**

```bash
export ENABLE_TOOL_SEARCH=true
```

**Or in settings.json:**

```json
{
  "env": {
    "ENABLE_TOOL_SEARCH": "true"
  }
}
```

### When to Use Each Setting

| Scenario                             | Recommended                     |
| ------------------------------------ | ------------------------------- |
| Use MCP tools every session          | `auto` (default)                |
| Use MCP tools occasionally           | `true` or `auto:1`              |
| Many MCP servers (50+ tools)         | `auto` (triggers automatically) |
| Few MCP servers, want to save tokens | `true`                          |

## Per-Tool Control: Not Available

**Claude API** supports per-tool `defer_loading`:

```typescript
// API only - NOT in Claude Code
{
  default_config: { defer_loading: true },
  configs: { "frequently_used_tool": { defer_loading: false } }
}
```

**Claude Code** only has global threshold control. Workaround: use rules/instructions to encourage specific MCP tool usage.

**Tracking:** [#12836](https://github.com/anthropics/claude-code/issues/12836) (102 upvotes, open)

## MCP vs Skills: Token Comparison

| Aspect      | MCP (under threshold) | MCP (Tool Search)       | Skill                |
| ----------- | --------------------- | ----------------------- | -------------------- |
| Load timing | Session start         | On-demand via search    | On-demand via invoke |
| Base cost   | Full tool definitions | ~500 tokens (MCPSearch) | 0 tokens             |
| Use cost    | 0 (already loaded)    | Tool definitions loaded | Skill content loaded |
| Best for    | Frequent use          | Occasional use          | Rare use             |

**Rule of thumb:** If you don't use an MCP tool most sessions, either enable Tool Search or use a skill wrapper.

## Configuration Files

### .mcp.json (Tool Definitions)

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_TOKEN": "${API_TOKEN}"
      }
    }
  }
}
```

### settings.json (Enabling Servers)

```json
{
  "enableAllProjectMcpServers": true,
  "enabledMcpjsonServers": ["server-name"]
}
```

**Note:** Servers in `.mcp.json` but not in `enabledMcpjsonServers` won't load (0 tokens).

## Token-Efficient MCP Design

### Action Dispatch Pattern

Instead of many tools, use one tool with actions:

```json
// Bad: 23 tools × ~700 tokens each = 16,100 tokens
"linear_create_issue", "linear_update_issue", "linear_search"...

// Good: 1 tool × ~500 tokens
{"action": "create", ...}, {"action": "update", ...}, {"action": "search", ...}
```

Example: [streamlinear](https://github.com/obra/streamlinear) (500 tokens vs 17K for official Linear MCP)

### Skill Wrappers for Infrequent MCP

For rarely-used MCP servers:

1. Define in `.mcp.json` but don't enable by default
2. Create skill documenting setup + usage
3. First use: skill instructs to enable + restart

## Troubleshooting

### MCP Server Not Loading

1. Check `enabledMcpjsonServers` includes server name
2. Verify env vars are set (use `${VAR}` syntax)
3. Test command manually: `npx -y package-name`

### Tool Search Not Activating

Check total MCP token usage vs threshold:

- Default 10% of 200K context = 20K tokens
- If under threshold, set `ENABLE_TOOL_SEARCH=true` to force

### Model Compatibility

| Model     | Tool Search Support |
| --------- | ------------------- |
| Opus 4+   | Yes                 |
| Sonnet 4+ | Yes                 |
| Haiku     | No (use `false`)    |

## Reference

- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
- [Tool Search Announcement](https://www.atcyrus.com/stories/mcp-tool-search-claude-code-context-pollution-guide)
- [GitHub #12836](https://github.com/anthropics/claude-code/issues/12836) - Per-tool defer_loading request
- [GitHub #18303](https://github.com/anthropics/claude-code/issues/18303) - Configurable threshold request
