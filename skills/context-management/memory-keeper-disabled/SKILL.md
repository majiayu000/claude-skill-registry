---
name: memory-keeper
description: Persistent context/memory management MCP server. Stores and retrieves context across AI sessions.
metadata: {"clawdbot":{"emoji":"🧠","installed":"✅ Installed via npm","requires":{"env":["MEMORY_KEEPER_PATH"]}}}
---

# Memory Keeper - Persistent Context

Persistent context management that stores and retrieves information across AI sessions.

## Status

**✅ INSTALLED** via npm
```bash
npm install -g mcp-memory-keeper
which mcp-memory-keeper  # /home/opc/.nvm/versions/node/v22.20.0/bin/mcp-memory-keeper
```

## Setup

**Environment variables:**
```bash
# Path to store memory database
export MEMORY_KEEPER_PATH="/home/opc/.clawdbot/memory-keeper"

# Optional: encryption key
export MEMORY_KEEPER_KEY="your-encryption-key"
```

## Usage

### Run as MCP Server
```bash
# As MCP server (for integration with agents)
memory-keeper --transport stdio

# With custom storage path
memory-keeper --storage /path/to/memory.db
```

### Using the CLI
```bash
uv run {baseDir}/scripts/memory-keeper.py store "key" "value"
uv run {baseDir}/scripts/memory-keeper.py retrieve "key"
uv run {baseDir}/scripts/memory-keeper.py search "query"
uv run {baseDir}/scripts/memory-keeper.py list
uv run {baseDir}/scripts/memory-keeper.py delete "key"
```

## Commands

### Store Information
```bash
# Store a fact
uv run scripts/memory-keeper.py store "user_preference" "Bradley likes concise messages"

# Store context from a session
uv run scripts/memory-keeper.py store "session_2026_01_13" "Discussed MCP servers, installed context7 and memory-keeper"
```

### Retrieve Information
```bash
# Get stored information
uv run scripts/memory-keeper.py retrieve "user_preference"

# Search memories
uv run scripts/memory-keeper.py search "MCP"

# List all memories
uv run scripts/memory-keeper.py list
```

### Delete
```bash
uv run scripts/memory-keeper.py delete "old_memory"
```

## When to Use

| Task | Use This | Alternative |
|------|----------|-------------|
| Remember across sessions | Memory Keeper | Manual file updates |
| Store user preferences | Memory Keeper | `SECRETS.md` |
| Track context between sessions | Memory Keeper | Memory files |
| Quick lookup | Memory Keeper | `qmd search` |

## Architecture

```
Session → Store Context → Persistent DB → Retrieve → Next Session
```

## Comparison

| Feature | Memory Keeper | Current (Files) |
|---------|--------------|-----------------|
| Cross-session memory | ✅ Yes | ❌ Manual |
| Automatic storage | ✅ Yes | ❌ Manual |
| Searchable | ✅ Yes | ✅ qmd |
| Structured | ✅ Yes | ❌ Unstructured |
| Fast lookup | ✅ Yes | ⚠️ Slow |

## Notes

- Stores data locally (SQLite by default)
- Supports encryption for sensitive data
- Can export/import memories
- Works offline

## Files

- `scripts/memory-keeper.py` - CLI wrapper
- MCP server: `memory-keeper`
- Storage: `~/.clawdbot/memory-keeper/` (default)

## See Also

- **context7 skill** - Codebase Q&A (complementary)
- **Full research:** `memory/MCP-SERVERS-RESEARCH.md`
- **Memory Keeper GitHub:** https://github.com/mkreyman/mcp-memory-keeper
