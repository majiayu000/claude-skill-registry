---
name: ralph-memories
description: "Manage persistent memories. Use when: Storing or retrieving patterns, decisions, and fixes across sessions. Not for: Temporary scratchpad or session-specific state."
---

# Ralph Memories

Persistent learning system for accumulated wisdom across sessions. Storage: `.agent/memories.md`.

## Memory Injection Configuration

Configure how memories are automatically injected into Ralph's context in `ralph.yml`:

```yaml
memories:
  enabled: true                         # Enable/disable memory system
  inject: auto                          # How memories enter context
  budget: 2000                          # Max tokens to inject (0 = unlimited)
  filter:
    types: []                           # Filter by type: pattern, decision, fix, context
    tags: []                            # Filter by tag names
    recent: 0                           # Only memories from last N days (0 = no limit)
```

### Injection Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `auto` | Ralph prepends relevant memories at start of each iteration | Most workflows - automatic context |
| `manual` | Agent must explicitly run `ralph memory search` | When you want selective memory access |
| `none` | Memories disabled entirely | Testing or memory-free workflows |

### Token Budget

| Setting | Effect |
|---------|--------|
| `0` | Unlimited memories injected (risky for large memory bases) |
| `1500-3000` | Balanced context (recommended) |
| `500-1000` | Minimal memory injection for token-constrained workflows |

### Filter Configuration

```yaml
# Only inject pattern memories about API and auth
memories:
  inject: auto
  budget: 1500
  filter:
    types: [pattern]
    tags: [api, auth]
    recent: 30  # Only last 30 days
```

**Prime command equivalents:**
```bash
# Same filtering via CLI
ralph tools memory prime -t pattern --tags api,auth --recent 30 --budget 1500

# Multiple types (comma-separated)
ralph tools memory prime -t pattern,decision

# Show all memories (no budget limit)
ralph tools memory prime --budget 0
```

## When to Search Memories

**Search BEFORE starting work when:**
- Entering unfamiliar code area → `ralph tools memory search "area-name"`
- Encountering an error → `ralph tools memory search -t fix "error message"`
- Making architectural decisions → `ralph tools memory search -t decision "topic"`
- Something feels familiar → there might be a memory about it

**Search strategies:**
- Start broad, narrow with filters: `search "api"` → `search -t pattern --tags api`
- Check fixes first for errors: `search -t fix "ECONNREFUSED"`
- Review decisions before changing architecture: `search -t decision`
- Use `--all` flag to show unlimited results

**Working directory option:**
All `ralph tools memory` commands support `--root <ROOT>` to specify working directory (default: current directory).

## When to Create Memories

**Create a memory when:**
- You discover how this codebase does things (pattern)
- You make or learn why an architectural choice was made (decision)
- You solve a problem that might recur (fix)
- You learn project-specific knowledge others need (context)

**Do NOT create memories for:**
- Session-specific state (use tasks instead)
- Obvious/universal practices
- Temporary workarounds

## Memory Types

| Type | Flag | Use For |
|------|------|---------|
| pattern | `-t pattern` | "Uses barrel exports", "API routes use kebab-case" |
| decision | `-t decision` | "Chose Postgres over SQLite for concurrent writes" |
| fix | `-t fix` | "ECONNREFUSED on :5432 means run docker-compose up" |
| context | `-t context` | "ralph-core is shared lib, ralph-cli is binary" |

## Discover Available Tags

Before searching or adding, check what tags already exist:

```bash
# See all memories with their tags
ralph tools memory list

# Extract unique tags (grep the file directly)
grep -o 'tags: [^|]*' .agent/memories.md | sort -u
```

Reuse existing tags for consistency. Common tag patterns:
- Component names: `api`, `auth`, `database`, `cli`
- Concerns: `testing`, `performance`, `error-handling`
- Tools: `docker`, `postgres`, `redis`

## Quick Reference

```bash
# Add memory (creates file if needed)
ralph tools memory add "content" -t pattern --tags tag1,tag2

# Add with options
ralph tools memory add "content" -t pattern --tags tag1,tag2 --format quiet

# Search (start broad, narrow with filters)
ralph tools memory search "query"
ralph tools memory search -t fix "error message"
ralph tools memory search --tags api,auth
ralph tools memory search --tags api,auth --all  # Show all results

# List and show
ralph tools memory list
ralph tools memory list -t fix --last 10
ralph tools memory list --format json
ralph tools memory show mem-1737372000-a1b2

# Delete
ralph tools memory delete mem-1737372000-a1b2

# Prime for context injection
ralph tools memory prime --budget 2000
ralph tools memory prime --tags api,auth    # Prime specific tags only
ralph tools memory prime --recent 7         # Only last 7 days
ralph tools memory prime -t pattern         # Prime by type

# Initialize
ralph tools memory init --force             # Overwrite existing file
```

**Output formats:** `--format {table,json,markdown,quiet}`
- `table`: Human-readable table format (default)
- `json`: JSON format for programmatic access
- `markdown`: Markdown format (for prime command)
- `quiet`: ID-only output for scripting

## Best Practices

1. **Be specific**: "Uses barrel exports in each module" not "Has good patterns"
2. **Include why**: "Chose X because Y" not just "Uses X"
3. **One concept per memory**: Split complex learnings
4. **Tag consistently**: Reuse existing tags when possible

## Examples

```bash
# Pattern: discovered codebase convention
ralph tools memory add "All API handlers return Result<Json<T>, AppError>" -t pattern --tags api,error-handling

# Decision: learned why something was chosen
ralph tools memory add "Chose JSONL over SQLite: simpler, git-friendly, append-only" -t decision --tags storage,architecture

# Fix: solved a recurring problem
ralph tools memory add "cargo test hangs: kill orphan postgres from previous run" -t fix --tags testing,postgres

# Context: project-specific knowledge
ralph tools memory add "The /legacy folder is deprecated, use /v2 endpoints" -t context --tags api,migration
```
