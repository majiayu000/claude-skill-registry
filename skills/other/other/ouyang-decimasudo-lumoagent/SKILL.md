---
name: jasper-recall
description: Local RAG system for agent memory using ChromaDB and sentence-transformers. Provides semantic search over session logs, daily notes, and memory files. Use when you need persistent memory across sessions, want to search past conversations, or build agents that remember context. Commands: recall "query", index-digests, digest-sessions.
---

# Jasper Recall

Local RAG (Retrieval-Augmented Generation) system for AI agent memory. Gives your agent the ability to remember and search past conversations.

## When to Use

- **Memory recall**: Search past sessions for context before answering
- **Continuous learning**: Index daily notes and decisions for future reference
- **Session continuity**: Remember what happened across restarts
- **Knowledge base**: Build searchable documentation from your agent's experience

## Quick Start

### Setup

One command installs everything:

```bash
npx jasper-recall setup
```

This creates:
- Python venv at `~/.openclaw/rag-env`
- ChromaDB database at `~/.openclaw/chroma-db`
- CLI scripts in `~/.local/bin/`

### Basic Usage

**Search your memory:**
```bash
recall "what did we decide about the API design"
recall "hopeIDS patterns" --limit 10
recall "meeting notes" --json
```

**Index your files:**
```bash
index-digests  # Index memory files into ChromaDB
```

**Create session digests:**
```bash
digest-sessions          # Process new sessions
digest-sessions --dry-run  # Preview what would be processed
```

## How It Works

### Three Components

1. **digest-sessions** — Extracts key info from session logs (topics, tools used)
2. **index-digests** — Chunks and embeds markdown files into ChromaDB
3. **recall** — Semantic search across your indexed memory

### What Gets Indexed

By default, indexes files from `~/.openclaw/workspace/memory/`:

- `*.md` — Daily notes, MEMORY.md
- `session-digests/*.md` — Session summaries
- `repos/*.md` — Project documentation
- `founder-logs/*.md` — Development logs (if present)

### Embedding Model

Uses `sentence-transformers/all-MiniLM-L6-v2`:
- 384-dimensional embeddings
- ~80MB download on first run
- Runs locally, no API needed

## Agent Integration

### Memory-Augmented Responses

```python
# Before answering questions about past work
results = exec("recall 'project setup decisions' --json")
# Include relevant context in your response
```

### Automated Indexing (Heartbeat)

Add to HEARTBEAT.md:
```markdown
## Memory Maintenance
- [ ] New session logs? → `digest-sessions`
- [ ] Memory files updated? → `index-digests`
```

### Cron Job

Schedule regular indexing:
```json
{
  "schedule": { "kind": "cron", "expr": "0 */6 * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run index-digests to update the memory index"
  },
  "sessionTarget": "isolated"
}
```

## CLI Reference

### recall

```
recall "query" [OPTIONS]

Options:
  -n, --limit N     Number of results (default: 5)
  --json            Output as JSON
  -v, --verbose     Show similarity scores
```

### index-digests

```
index-digests

Indexes markdown files from:
  ~/.openclaw/workspace/memory/*.md
  ~/.openclaw/workspace/memory/session-digests/*.md
  ~/.openclaw/workspace/memory/repos/*.md
  ~/.openclaw/workspace/memory/founder-logs/*.md

Skips files that haven't changed (content hash check).
```

### digest-sessions

```
digest-sessions [OPTIONS]

Options:
  --dry-run    Preview without writing
  --all        Process all sessions (not just new)
  --recent N   Process only N most recent sessions
```

## Configuration

### Custom Paths

Set environment variables:

```bash
export RECALL_WORKSPACE=~/.openclaw/workspace
export RECALL_CHROMA_DB=~/.openclaw/chroma-db
export RECALL_SESSIONS_DIR=~/.openclaw/agents/main/sessions
```

### Chunking

Default settings in index-digests:
- Chunk size: 500 characters
- Overlap: 100 characters

## Troubleshooting

**"No index found"**
```bash
index-digests  # Create the index first
```

**"Collection not found"**
```bash
rm -rf ~/.openclaw/chroma-db  # Clear and rebuild
index-digests
```

**Model download slow**
First run downloads ~80MB model. Subsequent runs are instant.

## Links

- **GitHub**: https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall
- **npm**: https://www.npmjs.com/package/jasper-recall
- **ClawHub**: https://clawhub.ai/skills/jasper-recall
