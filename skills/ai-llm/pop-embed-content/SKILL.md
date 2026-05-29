---
name: embed-content
description: "Use when you need to manage project embeddings - embed skills, agents, commands, and MCP tools for semantic discovery. Handles rate limiting, incremental updates, and status reporting. Do NOT use if you just want to search for content - use the semantic router directly instead."
context: fork
---

# Embed Content

## Overview

Manage embeddings for project-local content including skills, agents, commands, and MCP tools. Enables semantic search and discovery of project-specific items.

**Core principle:** Make project content discoverable via semantic search.

**Trigger:** `/popkit:project embed` command or auto-invoked by generators

## Arguments

| Flag            | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| `--status`      | Show embedding status without embedding                       |
| `--force`       | Re-embed all content (ignore cache)                           |
| `--export`      | Export embeddings to .claude/tool_embeddings.json             |
| `--type <type>` | Only embed specific type: `skill`, `agent`, `command`, `tool` |

## Process

### Step 1: Discover Content

Scan project for embeddable items:

```python
import sys
from pathlib import Path

# No longer needed - install popkit-shared instead
from embedding_project import scan_project_items

# Scan locations:
# - .claude/skills/*/SKILL.md      → project-skill
# - .claude/agents/*/AGENT.md      → project-agent
# - .claude/commands/*.md          → project-command
# - .generated/skills/*/SKILL.md   → generated-skill
# - .generated/agents/*/AGENT.md   → generated-agent
# - MCP tool definitions            → mcp-tool

items = scan_project_items(Path.cwd())
print(f"Found {len(items)} embeddable items")
```

### Step 2: Check Status

Compare against embedding store:

```python
from embedding_project import get_project_embedding_status

status = get_project_embedding_status()

# Returns:
# - total_items: Number of items found
# - embedded_items: Number already embedded
# - stale_items: Number with changed content
# - missing_items: Number not yet embedded
# - by_type: Breakdown by source type
```

### Step 3: Compute Embeddings

Via Voyage AI with rate limiting:

```python
from embedding_project import embed_project_items

# Respects rate limits:
# - 3 requests per minute (21s delay between batches)
# - Up to 50 items per batch
# - Progress reporting

result = embed_project_items(
    project_root=Path.cwd(),
    force=False  # Set True to re-embed unchanged items
)

print(f"Embedded: {result['embedded']}")
print(f"Skipped: {result['skipped']}")
print(f"Errors: {result['errors']}")
```

### Step 4: Export for MCP

Optionally export embeddings for MCP server:

```python
import json
from datetime import datetime
from pathlib import Path

def export_tool_embeddings(tools: list, output_path: str):
    """Export embeddings for MCP semantic search."""
    output = {
        "generated_at": datetime.now().isoformat(),
        "model": "voyage-3.5",
        "dimension": len(tools[0]["embedding"]) if tools else 0,
        "tools": tools
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(output, indent=2))
```

## Output Formats

### Status Mode (`--status`)

```
Project Embedding Status
═══════════════════════

Location: /path/to/project
API Available: Yes (VOYAGE_API_KEY set)

Content Found:
  Skills:   4 (2 embedded, 2 new)
  Agents:   1 (1 embedded)
  Commands: 3 (3 embedded)
  Tools:    8 (8 embedded)
  ─────────────────────────
  Total:   16 items

Needs Embedding: 2 items
  - .claude/skills/new-skill/SKILL.md
  - .claude/skills/updated-skill/SKILL.md (content changed)

Run `/popkit:project embed` to update.
```

### Embed Mode (default)

```
Embedding Project Content
═════════════════════════

Discovering content...
  Found 16 items (14 current, 2 need update)

Embedding 2 items...
  ████████████████████ 100%

  ✓ project-skill:new-skill
  ✓ project-skill:updated-skill

Summary:
  Embedded:  2
  Skipped:  14 (already current)
  Errors:    0

Embeddings stored in global database.
```

### Export Mode (`--export`)

```
Exporting Tool Embeddings
═════════════════════════

Collecting MCP tool embeddings...
  Found 8 tools with embeddings

Exporting to .claude/tool_embeddings.json...
✓ Exported 8 tool embeddings

File: .claude/tool_embeddings.json
Size: 245 KB
Model: voyage-3.5
Dimension: 1024
```

## Rate Limiting

The skill respects Voyage AI rate limits:

| Limit               | Value   | Handling                        |
| ------------------- | ------- | ------------------------------- |
| Requests per minute | 3       | 21-second delay between batches |
| Items per request   | 50      | Batch items automatically       |
| Tokens per request  | 120,000 | Descriptions typically small    |

**Typical Times:**

- 10 items: ~5 seconds (1 batch)
- 30 items: ~25 seconds (1 batch + delay)
- 100 items: ~1 minute (2 batches + delays)

## Error Handling

| Error           | Handling                                                  |
| --------------- | --------------------------------------------------------- |
| No API key      | Report and skip embedding, suggest setting VOYAGE_API_KEY |
| Rate limit hit  | Wait and retry automatically                              |
| Network error   | Report item, continue with others                         |
| Invalid content | Skip item, report in summary                              |

## Integration

**Uses:**

- `hooks/utils/embedding_project.py` - Core embedding logic
- `hooks/utils/voyage_client.py` - Voyage API client
- `hooks/utils/embedding_store.py` - SQLite storage

**Called by:**

- `/popkit:project embed` - Manual invocation
- `/popkit:project generate` - Final pipeline step
- `pop-skill-generator` - After creating skills
- `pop-mcp-generator` - After creating MCP server

**Enables:**

- Semantic search for project content
- Natural language tool discovery
- Cross-project skill discovery
- Priority boost for project items in routing

## Examples

```bash
# Check what needs embedding
/popkit:project embed --status

# Embed all new/changed items
/popkit:project embed

# Force re-embed everything
/popkit:project embed --force

# Embed only skills
/popkit:project embed --type skill

# Export for MCP server
/popkit:project embed --export

# Combine: embed and export
/popkit:project embed --export
```
