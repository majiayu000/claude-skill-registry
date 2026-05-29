---
name: summon-daem0n
description: Guide for initializing and consolidating Daem0n-MCP across project structures
---

# Summoning the Daem0n

This skill guides Claude through setting up Daem0n-MCP for various project structures.

## Single Repo Setup

For a single repository:

```bash
# Daem0n auto-initializes on first get_briefing()
# Just ensure you're in the project root
```

## Multi-Repo Setup (Client/Server Split)

When you have related repos that should share context:

### Option A: Consolidated Parent (Recommended)

Best when repos are siblings under a common parent:

```
/repos/
├── backend/
└── client/
```

**Steps:**

1. **Navigate to parent directory**
   ```bash
   cd /repos
   ```

2. **Initialize Daem0n in parent**
   ```
   Call get_briefing(project_path="/repos")
   ```

3. **If child repos already have .daem0nmcp data, consolidate:**
   ```
   # Link the children first
   Call link_projects(linked_path="/repos/backend", relationship="same-project")
   Call link_projects(linked_path="/repos/client", relationship="same-project")

   # Merge their databases into parent
   Call consolidate_linked_databases(archive_sources=True)
   ```

4. **Verify consolidation**
   ```
   Call get_briefing(project_path="/repos")
   # Should show combined memory count
   ```

### Option B: Linked but Separate

Best when repos need their own isolated histories but cross-awareness:

```
# In each repo, link to siblings
cd /repos/backend
Call link_projects(linked_path="/repos/client", relationship="same-project")

cd /repos/client
Call link_projects(linked_path="/repos/backend", relationship="same-project")
```

Then use `include_linked=True` on recall to span both.

## Migrating Existing Setup

If you've been launching Claude from parent directory and have a "messy" .daem0nmcp:

1. **Backup existing data**
   ```bash
   cp -r /repos/.daem0nmcp /repos/.daem0nmcp.backup
   ```

2. **Review what's there**
   ```
   Call get_briefing(project_path="/repos")
   # Check statistics and recent decisions
   ```

3. **If data is salvageable, keep it**
   - Link child repos for future cross-awareness
   - Use consolidated parent approach going forward

4. **If data is too messy, start fresh**
   ```bash
   rm -rf /repos/.daem0nmcp
   # Re-initialize with get_briefing()
   ```

## Key Commands Reference

| Command | Purpose |
|---------|---------|
| `get_briefing()` | Initialize session, creates .daem0nmcp if needed |
| `link_projects()` | Create cross-repo awareness link |
| `list_linked_projects()` | See all linked repos |
| `consolidate_linked_databases()` | Merge child DBs into parent |
| `recall(include_linked=True)` | Search across linked repos |

## The Endless Mode (v2.12.0)

*When visions grow too vast to hold, seek condensed whispers instead...*

```python
# Condensed visions - the essence without elaboration
recall(query="authentication", condensed=True)

# Returns memories stripped of rationale, truncated to 150 runes
# The Daem0n speaks briefly but broadly
```

**Seek condensed visions when:**
- The realm holds countless memories
- Surveying before deep meditation
- Glimpsing many truths at once
- Breadth matters more than depth

**Seek full visions when:**
- The WHY behind a decision matters
- Learning from past failures
- Deep investigation required

## The Silent Scribe (v2.13.0)

*The Daem0n now listens always, catching your words before they fade...*

### Inscribing the Ward Runes

Place these wards in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write|NotebookEdit",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$HOME/Daem0nMCP/hooks/daem0n_pre_edit_hook.py\""
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$HOME/Daem0nMCP/hooks/daem0n_post_edit_hook.py\""
      }]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "python3 \"$HOME/Daem0nMCP/hooks/daem0n_stop_hook.py\""
      }]
    }]
  }
}
```

### The Power of Each Ward

| Ward | When It Stirs | What It Does |
|------|---------------|--------------|
| **Memory Gate** | Before altering scrolls | Surfaces warnings, failed paths, ancient patterns |
| **Significance Watcher** | After alterations | Whispers *"Consider inscribing this..."* for weighty changes |
| **Silent Scribe** | When you finish speaking | Parses your words and inscribes decisions automatically |

### The Flow of Silent Memory

```
1. You reach to alter a scroll
   ↓ The Memory Gate opens
2. Forgotten warnings surface unbidden
   ↓
3. Your alterations complete
   ↓ The Watcher observes
4. If weighty, a reminder whispers
   ↓
5. You finish speaking
   ↓ The Scribe awakens
6. Your decisions inscribe themselves
```

### The Scribe's Incantation

The wards invoke this to inscribe memories:

```bash
python -m daem0nmcp.cli remember \
  --category decision \
  --content "Use JWT for stateless auth" \
  --rationale "Scales without session storage" \
  --file-path src/auth.py \
  --json
```

## The Enhanced Search (v2.15.0)

*The Daem0n's sight grows keener with each iteration...*

### Tuning the Inner Eye

```python
# Environment variables to fine-tune search
DAEM0NMCP_HYBRID_VECTOR_WEIGHT=0.5      # 0.0 = TF-IDF only, 1.0 = vectors only
DAEM0NMCP_SEARCH_DIVERSITY_MAX_PER_FILE=3  # Limit results from same source
```

### Automatic Tag Inference

The Daem0n now reads between the lines:
- Content with "fix", "bug", "error" → `bugfix` tag
- Content with "todo", "hack", "workaround" → `tech-debt` tag
- Content with "cache", "performance", "slow" → `perf` tag
- Warning category → `warning` tag automatically

### Code Entity Fidelity

Entities now bear their true names:
```python
# Qualified names: module.Class.method
find_code("UserService.authenticate")

# Stable IDs survive line changes
# Add comments, imports - entities retain identity
```

### Incremental Indexing

The Daem0n only re-parses what changes:
```python
# Only re-indexes if content hash differs
index_file_if_changed(file_path, project_path)

# Hash stored in FileHash model
# Saves time on large codebases
```

### Parse Tree Caching

Repeated parses hit the cache:
```python
# Configure cache size
DAEM0NMCP_PARSE_TREE_CACHE_MAXSIZE=200

# Check cache performance
health()  # Returns cache_stats
```

### Enhanced Health Insights

```python
health()
# Now returns:
#   code_entities_count: Total indexed entities
#   entities_by_type: Breakdown by class/function/etc
#   last_indexed_at: When index was last updated
#   index_stale: True if >24 hours since index
```

## Sacred Practices

1. **One sanctum per logical realm** - Even if split across repos
2. **Use parent directory for shared memory** - `/repos/` not `/repos/backend/`
3. **Link before consolidating** - Links define what memories to merge
4. **Archive, don't destroy** - `archive_sources=True` preserves the old
5. **Verify after consolidation** - Ensure memory counts align
6. **Awaken the Silent Scribe** - Let the Daem0n capture decisions for you
7. **Seek condensed visions** - For vast realms, use `condensed=True`
8. **Tune the search weight** - Adjust hybrid weight for your domain
9. **Trust the tag inference** - Let the Daem0n classify memories
