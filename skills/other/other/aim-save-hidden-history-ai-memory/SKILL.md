---
name: aim-save
description: 'Manually save current session to memory'
allowed-tools: Bash
---

# Save Memory - Manual Session Summary Storage

Save the current session context to the AI Memory system's `discussions`
collection. This creates a `type=session` entry that can be retrieved by
SessionStart on future session resume or by `/aim-search`.

## When to Use

- Before ending a session to preserve important context
- After making significant decisions you want remembered
- When you want to bookmark a particular conversation state
- As a manual complement to the automatic PreCompact session save

## Usage

The save-memory command runs the manual_save_memory.py script using the
project's configured AI Memory installation.

```bash
# Save with a description (recommended)
"$AI_MEMORY_INSTALL_DIR/.venv/bin/python" "$AI_MEMORY_INSTALL_DIR/.claude/hooks/scripts/manual_save_memory.py" \
"Completed authentication refactor, decided on JWT approach"

# Save without description
"$AI_MEMORY_INSTALL_DIR/.venv/bin/python" "$AI_MEMORY_INSTALL_DIR/.claude/hooks/scripts/manual_save_memory.py"
```

## What Gets Stored

The script stores to the discussions collection with:
- type: session (default); agent_memory or agent_insight (when --type is used)
- source_hook: ManualSave
- group_id: Auto-detected from current project directory
- session_id: Current Claude session ID (from CLAUDE_SESSION_ID env var)
- content: Structured summary with timestamp and user description
- embedding: 768-dim Jina v2 vector for semantic retrieval
- content_hash: SHA-256 for deduplication

## Agent Memory Support

When `--type agent_memory` or `--type agent_insight` is used, the memory is stored
via `store_agent_memory()` to the Parzival namespace with `agent_id=parzival`.

This requires Parzival to be enabled (`parzival_enabled=true` in config).
If Parzival is not enabled, the command returns an error.

### Usage

```bash
# Default behavior (unchanged)
/aim-save "Completed authentication refactor"

# Save as agent memory (general project knowledge)
/aim-save "The decay formula uses 0.7/0.3 weighting" --type agent_memory

# Save as agent insight (key learning or pattern)
/aim-save "PyYAML not in test deps caused CI failures" --type agent_insight
```

## Environment Variables (Auto-Configured)

These are set automatically in settings.json by the installer:
- AI_MEMORY_INSTALL_DIR — Path to ~/.ai-memory installation
- AI_MEMORY_PROJECT_ID — Current project name
- QDRANT_HOST / QDRANT_PORT — Qdrant connection (localhost:26350)
- QDRANT_API_KEY — Qdrant authentication
- EMBEDDING_HOST / EMBEDDING_PORT — Embedding service (localhost:28080)

## Error Handling

- If Qdrant is unavailable: queues to ~/.ai-memory/queue/ for background processing
- If embedding fails: stores with zero vector (backfilled later)
- Exit code 0 on success OR successful queue fallback
- Exit code 1 only on hard errors (missing installation)

## Prerequisites

- AI Memory services running (docker compose up -d from ~/.ai-memory/docker/)
- Installation directory exists at $AI_MEMORY_INSTALL_DIR
- Python venv at $AI_MEMORY_INSTALL_DIR/.venv/

## Examples

```bash
# Save decision context
/aim-save "Decided to use Qdrant for vector storage over Pinecone due to self-hosting requirement"

# Save progress checkpoint
/aim-save "Completed 3 of 5 API endpoints, auth middleware working"

# Quick save without description
/aim-save

# Save as agent memory (general project knowledge)
/aim-save "The decay formula uses 0.7/0.3 weighting" --type agent_memory

# Save as agent insight (key learning or pattern)
/aim-save "PyYAML not in test deps caused CI failures" --type agent_insight
```

## Technical Details

- Script: .claude/hooks/scripts/manual_save_memory.py
- Collection: discussions (COLLECTION_DISCUSSIONS)
- Type: session (same as PreCompact auto-saves)
- Embedding: jina-embeddings-v2-base-en (768 dimensions)
- Fallback: File queue at ~/.ai-memory/queue/ via queue_operation()
- Logging: Activity logged via log_manual_save() to ~/.ai-memory/logs/activity.log
