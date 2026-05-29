---
name: embed-project
description: "Embed project-local skills, agents, and commands for semantic search. Use after creating items manually or to update embeddings. Works with both keyword and semantic search modes."
---

# Embed Project Items

Compute vector embeddings for project-local items to enable semantic discovery and routing.

## Enhancement Available

This skill works in two modes:

- **Without API key**: Keyword-based file search (fully functional)
- **With API key**: Semantic embeddings for intelligent discovery (enhanced)

### Keyword Search Mode (Always Available)

All users can search projects using built-in file search:

````markdown
## Keyword Search Mode

Project search works great with built-in tools!

### Available Search Methods

**Find skills:**

```bash
ls .claude/skills/*/SKILL.md 2>/dev/null
```
````

**Find agents:**

```bash
ls .claude/agents/*/AGENT.md 2>/dev/null
```

**Find commands:**

```bash
ls .claude/commands/*.md 2>/dev/null
```

**Search by keyword:**

```bash
grep -r "keyword" .claude/
```

### What Semantic Embeddings Add

With an API key, you get semantic intelligence:

- ✨ **Semantic search** - Find by meaning, not just keywords
- 🔍 **Smart routing** - Auto-select best agent for task
- ⚡ **Cross-project discovery** - Find patterns across codebases
- 📊 **Relevance ranking** - Results sorted by semantic similarity

Get a free API key: `/popkit:cloud signup`

````

### Enhancement Detection

```python
import sys
# No longer needed - install popkit-shared instead
from enhancement_detector import check_enhancement

result = check_enhancement("project-embeddings")
if not result.has_api_key:
    # Provide keyword search alternatives (fully functional)
    print("## Keyword Search Mode")
    print("\nProject search works great with built-in tools!")
    print("Use file search: `grep -r 'keyword' .claude/`")
    print("\nFor semantic enhancements: `/popkit:cloud signup` (free)")
    return
````

## When to Use

- After creating skills/agents/commands manually (not via generators)
- To check embedding status for the project
- To force re-embedding after content changes
- Before using semantic search features

## Process

### Step 1: Parse Arguments

Check for flags in the user's command:

- `--status`: Show status only, don't embed
- `--force` or `-f`: Re-embed all items even if unchanged
- `--type <type>`: Filter to specific type (skill, agent, command)

### Step 2: Execute Based on Mode

**If --status flag:**

```python
# Use the embedding_project module
import sys
# No longer needed - install popkit-shared instead
from embedding_project import get_project_embedding_status

status = get_project_embedding_status()

# Display results
print(f"Project: {status['project_path']}")
print(f"API Available: {status['api_available']}")
print()
print(f"Items Found:    {status['items_found']}")
print(f"Items Embedded: {status['items_embedded']}")
print(f"Items Stale:    {status['items_stale']}")
print(f"Items Missing:  {status['items_missing']}")

if status['by_type']:
    print("\nBy Type:")
    for stype, counts in status['by_type'].items():
        print(f"  {stype}: {counts['embedded']}/{counts['found']}")
```

**If embedding (default):**

```python
import sys
# No longer needed - install popkit-shared instead
from embedding_project import embed_project_items, scan_project_items

# Map --type flag to source types
type_map = {
    "skill": ["project-skill", "generated-skill"],
    "agent": ["project-agent", "generated-agent"],
    "command": ["project-command"],
}

source_types = None
if args.type:
    source_types = type_map.get(args.type, [f"project-{args.type}"])

# First scan to show what we found
items = scan_project_items()
print(f"Found {len(items)} items")

# Embed items
result = embed_project_items(
    force=args.force,
    source_types=source_types,
    verbose=True
)

# Report results
if result["status"] == "success":
    print(f"\nEmbedding complete!")
    print(f"  Embedded: {result['embedded']}")
    print(f"  Skipped: {result['skipped']}")
    if result['errors']:
        print(f"  Errors: {result['errors']}")
elif result["status"] == "no_items":
    print("No embeddable items found in project.")
elif result["status"] == "error":
    print(f"Error: {result.get('error', 'Unknown error')}")
```

### Step 3: Handle Rate Limiting

The embedding module automatically handles rate limiting:

- Batches up to 50 items per API call
- Waits 21 seconds between batches (Voyage 3 RPM limit)
- Displays progress during wait

## Project Locations Scanned

| Location                       | Source Type     |
| ------------------------------ | --------------- |
| `.claude/skills/*/SKILL.md`    | project-skill   |
| `.claude/agents/*/AGENT.md`    | project-agent   |
| `.claude/commands/*.md`        | project-command |
| `.generated/skills/*/SKILL.md` | generated-skill |
| `.generated/agents/*/AGENT.md` | generated-agent |

## Requirements

- `VOYAGE_API_KEY` environment variable set
- Items must have `description` in YAML frontmatter

## Example Usage

```
# Check current status
/popkit:project embed --status

# Embed all items (skips unchanged)
/popkit:project embed

# Force re-embed everything
/popkit:project embed --force

# Embed only skills
/popkit:project embed --type skill
```

## Output Format

### Embedding Progress

```
Scanning project: /path/to/project
Found 8 items

Embedding 5 new/changed items...
Waiting 21s for rate limit...

Embedding complete!
  Embedded: 5
  Skipped: 3 (unchanged)
  Errors: 0
```

### Status Report

```
Project: /path/to/project
API Available: Yes

Items Found:    8
Items Embedded: 8
Items Stale:    0
Items Missing:  0

By Type:
  project-skill: 3/3
  project-agent: 2/2
  project-command: 3/3
```

## Integration

This skill integrates with:

- `hooks/utils/embedding_project.py` - Core embedding logic
- `hooks/utils/embedding_store.py` - Database storage
- `hooks/utils/voyage_client.py` - Voyage API client
- `hooks/utils/semantic_router.py` - Routing using embeddings

## Related

- `/popkit:project skills generate` - Creates skills then auto-embeds
- `/popkit:project mcp` - Creates MCP server with semantic search
