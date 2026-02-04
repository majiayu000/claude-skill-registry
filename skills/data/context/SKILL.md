---
name: Context
description: |
  Personal knowledge base integration via Obsidian vault. Provides semantic search,
  note retrieval, and context loading for Claude Code sessions.

  USE WHEN user says 'load context', 'search my notes', 'find in obsidian',
  'what do I have on', 'check my vault', 'incoming notes', 'recent captures',
  'semantic search', 'load project context'

  CAPABILITIES:
  - Search notes by tags, text, or semantic similarity
  - Load project-specific context into sessions
  - View incoming/unprocessed captures from Telegram
  - Read and create notes in Obsidian vault
  - Process captured content (images, documents, URLs)

  TOOLS:
  - `obs` CLI: ~/.claude/bin/obs/obs.ts
  - `ingest` CLI: ~/.claude/bin/ingest/ingest.ts
---

# Context Management Skill

**Purpose:** Seamless integration between your Obsidian knowledge base and Claude Code sessions. Find relevant notes, load project context, and manage captures from Telegram.

## Quick Reference

### obs CLI Commands
```bash
# Search
obs search "query"              # Full-text search
obs search --tag "project/pai"  # Tag-based search
obs semantic "concept"          # Semantic similarity search

# Read/Write
obs read "Note Title"           # Read a specific note
obs write "Title" --tag inbox   # Create a new note

# Browse
obs tags                        # List all tags
obs tags --counts               # Tags with usage counts
obs recent                      # Recently modified notes
obs incoming                    # Unprocessed inbox items

# Context
obs context project-name        # Load project context

# Embeddings
obs embed                       # Build/update embeddings
obs stats                       # Embedding statistics
```

### ingest CLI Commands
```bash
# Telegram capture
ingest poll                     # Fetch new messages
ingest process                  # Process pending → notes
ingest status                   # View message states

# Maintenance
ingest retry                    # Retry failed messages
ingest clear                    # Clear all (testing)
```

## Workflows

### 1. load-context.md
**Purpose:** Load project-specific context into current session
**Trigger:** "load context for X", "get project context", "what do I know about X"

### 2. search-notes.md
**Purpose:** Search personal notes using text, tags, or semantic similarity
**Trigger:** "search my notes for", "find notes about", "semantic search"

### 3. process-incoming.md
**Purpose:** Review and process captured content from Telegram
**Trigger:** "check incoming", "process captures", "what's in my inbox"

### 4. capture-content.md
**Purpose:** Capture new content to Obsidian via direct write
**Trigger:** "save this to obsidian", "capture this", "add to my notes"

## Routing Logic

```
User Intent → Workflow Selection

"Load context for PAI project"     → load-context.md
"Search notes about embeddings"    → search-notes.md
"What's in my inbox?"              → process-incoming.md
"Save this to my notes"            → capture-content.md
```

## Integration with Claude Code

This skill enables context-aware coding sessions:

1. **Start of session:** Load relevant project context
2. **During coding:** Search notes for reference material
3. **After research:** Capture findings to Obsidian
4. **End of session:** Auto-saved via hooks

### Example Session Flow
```
User: "Load context for the API redesign project"
→ obs context api-redesign
→ Returns: Related notes, decisions, meeting notes

User: "What did we decide about authentication?"
→ obs semantic "authentication decision"
→ Returns: Relevant note excerpts

User: "Save this architecture decision to my notes"
→ obs write "API Auth Decision" --tag "project/api" --tag "decision"
→ Creates note in vault
```

## Vault Structure

Expected Obsidian vault organization:
```
~/Documents/personal/
├── Inbox/                  # New captures land here
├── Projects/               # Project-specific notes
│   └── project-name/
├── Reference/              # Technical references
├── Archive/                # Completed/old items
└── attachments/            # Images, PDFs, etc.
```

## Tag Conventions

| Tag Pattern | Purpose |
|-------------|---------|
| `project/<name>` | Project association |
| `incoming` | Unprocessed captures |
| `decision` | Architectural decisions |
| `meeting` | Meeting notes |
| `reference` | Reference material |
| `todo` | Action items |

## Configuration

Environment variables (in `~/.claude/.env`):
```bash
OBSIDIAN_VAULT_PATH=~/Documents/personal
OPENAI_API_KEY=sk-...  # For embeddings & vision
```

State databases:
- Embeddings: `~/.claude/embeddings.db`
- Ingest state: `~/.claude/ingest-state.db`

## Troubleshooting

### Semantic search not working
```bash
obs stats  # Check if embeddings exist
obs embed  # Rebuild embeddings
```

### Telegram captures not appearing
```bash
ingest test    # Verify bot connection
ingest poll    # Fetch new messages
ingest status  # Check message states
```

### Note not found
```bash
obs tags --counts  # See what tags exist
obs recent         # Check recent files
```

## Related Skills

- **research** - Multi-source web research
- **fabric** - Pattern-based content processing

## References

- Obsidian: https://obsidian.md
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
