---
name: claude-plugin
description: "**Use MCP repo-map tools when:** - Searching for symbols by name pattern (faster than Grep) - Getting all symbols in a file (faster than Read + parsing)"
---

# Context Tools Plugin - Usage Guide

## Dynamic Directory Support (v0.8.0+)

**GOOD NEWS:** MCP tools automatically adapt to the current working directory!

**How it works:**
```bash
cd /home/user/project-a
# MCP tools query/index project-a/.claude/repo-map.db

cd /home/user/project-b
# MCP tools now query/index project-b/.claude/repo-map.db ✅
```

**Behavior:**
- Tools check current working directory on each call
- If `.claude/repo-map.db` exists: query it
- If not: trigger indexing for current directory
- Logs show which directory is being queried

**Benefits:**
- No need to restart session when changing projects
- Can work with multiple projects in one session
- Each project maintains its own index
- Tools "just work" wherever you are

## Plugin Installation and Updates

**CRITICAL: When the user runs `/plugin install` or `/plugin update`:**

The MCP server configuration changes immediately, but the MCP server itself **does not restart automatically**. The new plugin features (especially MCP tools like `search_symbols`) will NOT be available until the session restarts.

**YOU MUST tell the user:**

```
The plugin has been installed/updated successfully. To use the MCP tools (search_symbols, get_file_symbols, etc.), you need to restart the session:

1. Exit this session (Ctrl+C or type 'exit')
2. Start a new session with: claude continue

The MCP server will restart with the new plugin configuration.
```

**When to give this instruction:**
- Immediately after the user runs `/plugin install context-tools`
- Immediately after the user runs `/plugin update context-tools`
- When the user tries to use MCP tools but they're not available (and you suspect they just installed)

**Why this matters:**
- MCP servers are started when Claude Code starts
- Plugin installation modifies MCP server configuration
- Changes only take effect on next Claude Code startup
- Users will be confused if tools don't work after installation

## Available MCP Tools

Once the session has been restarted after installation, the following MCP tools are available:

### mcp__repo-map__search_symbols
Search for symbols (functions, classes, methods) by name pattern.

**Faster than Grep/Search** - uses pre-built SQLite index.

Parameters:
- `pattern` (required): Glob pattern like `get_*`, `*Handler`, `Config*`
- `kind` (optional): Filter by `"class"`, `"function"`, or `"method"`
- `limit` (optional): Max results (default: 20)

Example:
```json
{
  "pattern": "parse_*",
  "kind": "function",
  "limit": 10
}
```

### mcp__repo-map__get_file_symbols
Get all symbols defined in a specific file.

Parameters:
- `file` (required): Relative path from project root (e.g., `"src/models/user.py"`)

### mcp__repo-map__get_symbol_content
Get the source code content of a symbol by exact name.

**Faster than Grep/Search+Read** - directly retrieves function/class source code.

Parameters:
- `name` (required): Exact symbol name (e.g., `"MyClass"`, `"User.save"`)
- `kind` (optional): Filter by type if name is ambiguous

### mcp__repo-map__reindex_repo_map
Trigger a reindex of the repository symbols.

Parameters:
- `force` (optional): Force reindex even if cache is fresh (default: false)

### mcp__repo-map__repo_map_status
Get the current status of the repo map index.

Shows:
- Index status: `idle`, `indexing`, `completed`, or `failed`
- Symbol count
- Last indexed time
- Whether index is stale
- Indexing errors (if any)

### mcp__repo-map__wait_for_index
Wait for indexing to complete.

Parameters:
- `timeout_seconds` (optional): How long to wait (default: 60)

**Note:** Most tools automatically wait for indexing to complete, so this is rarely needed.

## Database Schema (.claude/repo-map.db)

**symbols table:**
- `name` (TEXT): Symbol name
- `kind` (TEXT): `class`, `function`, or `method`
- `file_path` (TEXT): Relative path from project root
- `line_number` (INTEGER): Start line (1-indexed)
- `end_line_number` (INTEGER): End line (nullable)
- `parent` (TEXT): Parent class/module (nullable)
- `docstring` (TEXT): First line of docstring (nullable)
- `signature` (TEXT): Function/method signature (nullable)
- `language` (TEXT): `python`, `cpp`, or `rust`

**metadata table (v0.7.0+):**
- `key` (TEXT PRIMARY KEY): Metadata key
- `value` (TEXT): Metadata value

Keys:
- `status`: `idle` | `indexing` | `completed` | `failed`
- `index_start_time`: ISO8601 timestamp when indexing started
- `last_indexed`: ISO8601 timestamp when last completed
- `symbol_count`: Total symbols indexed (string)
- `error_message`: Error message if status='failed'

## Indexing Status and Auto-Wait (v0.7.0+)

**First Use Behavior:**
- On first use, indexing starts automatically in background
- Tools automatically wait (up to 60s) if indexing is in progress
- If timeout, tools return helpful error asking user to retry

**Watchdog (v0.7.0+):**
- Detects hung indexing processes (>10 minutes)
- Automatically resets status to 'failed'
- Can be manually recovered with `reindex_repo_map`

**Multiprocess Architecture (v0.8.0+):**
- Indexing runs in separate subprocess
- MCP server remains responsive even if indexing hangs
- Watchdog can kill hung subprocess without affecting MCP server
- Resource limits (Unix/macOS): 4GB memory, 20 min CPU time

## When to Use MCP Tools vs Other Tools

**Use MCP repo-map tools when:**
- Searching for symbols by name pattern (faster than Grep)
- Getting all symbols in a file (faster than Read + parsing)
- Getting source code of a specific function/class (faster than Grep + Read)
- Need to search across multiple languages (Python, C++, Rust)

**Use other tools when:**
- Searching file contents (not symbol names) - use Grep
- Reading entire files - use Read
- Need to search files that aren't Python/C++/Rust
- Searching for non-code patterns (comments, strings, etc.)

## Project-Specific Files

**Automatically generated at session start:**
- `.claude/project-manifest.json` - Project structure and build commands
- `.claude/repo-map.md` - Human-readable code structure with duplicate detection
- `.claude/repo-map.db` - SQLite database for fast symbol queries (MCP server)

**Optional (created manually):**
- `.claude/learnings.md` - Project-specific learnings and discoveries

**Logs:**
- `.claude/logs/repo-map-server.log` - MCP server rotating log (1MB per file, 3 backups)
  - Tool calls and results
  - Indexing events and performance
  - Watchdog actions and resource limit violations
  - Server startup/shutdown
- Session start hook outputs are also logged for debugging
