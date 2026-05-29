---
name: gobby-mcp
description: Use this skill when discovering and using MCP tools through the Gobby proxy. This skill teaches the progressive disclosure workflow for efficient tool discovery and prevents common mistakes like querying live servers instead of using the local cache.
---

# Gobby MCP Tool Discovery

## Overview

The Gobby daemon provides an MCP proxy with progressive tool discovery for efficient access to downstream servers. This skill teaches the proper workflow for discovering and using MCP tools.

## Daemon Management: Use CLI

Daemon lifecycle (start/stop/restart/status) should be managed via CLI commands, not MCP tools:

```bash
# Start the daemon
uv run gobby start

# Stop the daemon
uv run gobby stop

# Check status
uv run gobby status

# Restart
uv run gobby restart
```

**Why CLI?** MCP tools require a running daemon. You can't start a daemon via MCP if it isn't running, and stopping/restarting via MCP severs your own connection.

---

## MCP Tool Discovery & Usage

### Progressive Disclosure System

The gobby implements progressive disclosure to reduce token usage:
- Tool metadata cached locally in `~/.gobby/.mcp.json` (lightweight)
- Full schemas stored in `~/.gobby/tools/` (loaded on-demand)

This enables a three-step workflow that's **96% more token-efficient** than loading all schemas upfront.

### Three-Step Workflow

#### Step 1: Discover Tools - `list_tools()`

**When**: At the start of a task when discovering what tools are available

**How**: Use the `list_tools` tool (exposed by gobby)

```python
# List all tools across all servers
mcp__gobby__list_tools()

# List tools for specific server
mcp__gobby__list_tools(server="context7")
```

**Returns**: Tool names + brief descriptions (not full schemas)

**Token cost**: ~1.5K tokens (vs. 40K for all schemas)

#### Step 2: Inspect Schema - `get_tool_schema()`

**When**: After discovering a tool, before calling it

**How**: Use the `get_tool_schema` tool (exposed by gobby)

**Important**: Reads from local cache, not live server

```python
# Get full schema for a specific tool
mcp__gobby__get_tool_schema(
    server_name="context7",
    tool_name="get-library-docs"
)
```

**Returns**: Complete inputSchema with all properties, types, required fields

**Token cost**: ~2KB per tool (only when needed)

#### Step 3: Execute Tool - `call_tool()`

**When**: After understanding the schema and preparing correct arguments

**How**: Use `mcp__gobby__call_tool` with the downstream server name

```python
# Call a tool on a downstream MCP server
mcp__gobby__call_tool(
    server_name="context7",
    tool_name="get-library-docs",
    arguments={
        "context7CompatibleLibraryID": "/react/react",
        "topic": "hooks"
    }
)
```

**Important**: Use the downstream server name (context7, supabase, etc.)

### Complete Example

```python
# Scenario: User asks "Find React hooks documentation"

# Step 1: Discover available tools
tools = mcp__gobby__list_tools(server="context7")
# Found: resolve-library-id, get-library-docs

# Step 2: Get schema for resolve-library-id
schema = mcp__gobby__get_tool_schema(
    server_name="context7",
    tool_name="resolve-library-id"
)
# Learned: Takes 'packageName' parameter

# Step 3: Resolve React library ID
library_id = mcp__gobby__call_tool(
    server_name="context7",
    tool_name="resolve-library-id",
    arguments={"packageName": "react"}
)
# Got: "/react/react"

# Step 4: Get React documentation on hooks
docs = mcp__gobby__call_tool(
    server_name="context7",
    tool_name="get-library-docs",
    arguments={
        "context7CompatibleLibraryID": "/react/react",
        "topic": "hooks"
    }
)
# Got: React hooks documentation
```

### Best Practices

#### DO:
- Always start with `list_tools()` to discover available tools
- Use `get_tool_schema()` before calling unfamiliar tools
- Use the three-step workflow for efficient token usage
- Remember tool schemas are cached locally (no live queries needed)

#### DON'T:
- Skip tool discovery - always know what's available first
- Call tools without checking their schema
- Try to query live MCP servers for tool schemas (use get_tool_schema instead)
- Load all tool schemas upfront (defeats progressive disclosure)

### Understanding server_name Context

The `server_name` parameter identifies the target server:

| Tool | server_name value | Meaning |
|------|------------------|---------|
| `list_tools` | `"context7"` | Filter to context7's tools |
| `get_tool_schema` | `"context7"` | Get schema from context7 |
| `call_tool` | `"context7"`, `"supabase"`, etc. | Execute on downstream server |

### Internal Tool Servers

Internal tools use a `gobby-*` prefix and are handled locally:

- **gobby-tasks** - Task CRUD, dependencies, ready work detection
- **gobby-memory** - Memory storage and recall
- **gobby-skills** - Skill management and learning

```python
# List internal task tools
mcp__gobby__list_tools(server="gobby-tasks")

# Call an internal tool
mcp__gobby__call_tool(
    server_name="gobby-tasks",
    tool_name="list_ready_tasks",
    arguments={}
)
```

### Token Efficiency Comparison

**Without progressive disclosure** (loading all schemas):
- 53 tool schemas = ~150KB = ~40,000 tokens

**With progressive disclosure** (this system):
- `list_tools()` = ~5KB = ~1,500 tokens (96% reduction)
- `get_tool_schema()` per tool = ~2KB = ~500 tokens (only when needed)

**Result**: Load only what you need, when you need it.

---

## Quick Reference

### Daemon (use CLI)
```bash
uv run gobby start    # Start daemon
uv run gobby stop     # Stop daemon
uv run gobby status   # Check status
```

### Tool Discovery (use MCP)
```python
# Discover → Inspect → Execute
mcp__gobby__list_tools(server="context7")
mcp__gobby__get_tool_schema(server_name="context7", tool_name="...")
mcp__gobby__call_tool(server_name="context7", tool_name="...", arguments={...})
```

### Remember
- Daemon lifecycle: Use CLI commands
- Tool discovery: Three-step MCP workflow (list → inspect → execute)
- Never query live servers for tool schemas (use local cache)
