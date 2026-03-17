---
name: codesearch-code-search
description: "MANDATORY: Query CodeSearch BEFORE using grep, glob, find, or search. Performs 400x faster semantic and structural code search via SQL on indexed codebase. Use for finding functions, classes, patterns, callers, and implementations. Agents MUST query CodeSearch first; grep is only allowed after CodeSearch returns zero results."
allowed-tools: Bash, Read, SlashCommand
---

# CodeSearch Local Semantic Code Search

## MANDATORY: QUERY CODESEARCH BEFORE GREP/GLOB

**This is a PROTOCOL REQUIREMENT, not a suggestion. Failure to query CodeSearch first is a violation.**

### WHY THIS IS MANDATORY
- CodeSearch SQL: 0.002s | grep: 0.8s (400x slower)
- Agents using grep first waste tokens and time
- Index already exists at `~/.local/share/codesearch/index_v2.db`

### ALWAYS USE CODESEARCH FIRST
```bash
# Exact name lookup - 0.002s
sqlite3 ~/.local/share/codesearch/index_v2.db "SELECT file_path, line_number FROM entities WHERE name = 'MyFunction';"

# Fuzzy search - 0.004s
sqlite3 ~/.local/share/codesearch/index_v2.db "SELECT file_path, line_number FROM entities WHERE name LIKE '%Store%' LIMIT 10;"

# Semantic search
/codebase-search "authentication middleware pattern"
```

### GREP IS ONLY ALLOWED WHEN:
- CodeSearch query returned zero results AND project confirmed not indexed
- Searching literal strings (error messages, comments, config values)
- Explicit user request for grep

### FOR CONCEPTUAL QUESTIONS:
- "Where is X implemented?" → CodeSearch semantic search
- "Find similar patterns" → CodeSearch embeddings
- "How is feature Y built?" → CodeSearch first, then read files

## Quick Commands

### Semantic Search (V1 - Embeddings)
```bash
# Natural language search
/codebase-search "authentication middleware pattern"
/cfn-codesearch-search "error handling in API routes"

# CLI direct (global install preferred)
local-codesearch query "user login flow" --max-results 5
```

### Structural Search (V2 - SQL on AST)
```bash
# Find all callers of a function
sqlite3 ~/.local/share/codesearch/index_v2.db \
  "SELECT * FROM refs WHERE target_name = 'MyFunction';"

# Find all functions in a file
sqlite3 ~/.local/share/codesearch/index_v2.db \
  "SELECT name, line_number FROM entities WHERE file_path LIKE '%myfile.rs' AND kind = 'function';"

# Find entities by project (multi-project isolation)
sqlite3 ~/.local/share/codesearch/index_v2.db \
  "SELECT COUNT(*) FROM entities WHERE project_root = '/path/to/project';"
```

## Installation

**Global install (recommended for multi-project use):**
```bash
# From claude-flow-novice project
./scripts/install-codesearch-global.sh

# Verify
local-codesearch --version
```

This installs to `~/.local/bin/local-codesearch` for access from any project.

## Prerequisites

**OPENAI_API_KEY is REQUIRED for indexing.** Indexing will fail without a valid key.

```bash
# Option 1: Export before running
export OPENAI_API_KEY="sk-..."

# Option 2: Add to shell profile (~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc

# Option 3: Inline with command
OPENAI_API_KEY="sk-..." ./local-codesearch index --path /project
```

**Verify key is set:**
```bash
echo $OPENAI_API_KEY  # Should show your key (not empty)
```

## Index Management

```bash
# Index a project (first time or full rebuild)
local-codesearch index --path /path/to/project --types rs,ts,py

# Incremental update (after code changes)
/codebase-reindex

# Check index stats
sqlite3 ~/.local/share/codesearch/index_v2.db "SELECT project_root, COUNT(*) FROM entities GROUP BY project_root;"
```

## Key Features

- **Multi-project isolation**: Index multiple projects in single database without data collision
- **Non-destructive**: Indexing one project never deletes data from other projects
- **Centralized storage**: `~/.local/share/codesearch/index_v2.db`
- **Dual search**: V1 semantic (embeddings) + V2 structural (SQL on AST)
- **Fast**: Rust binary with SQLite backend

## Database Location
```
~/.local/share/codesearch/index_v2.db
```

## For Agents (MANDATORY PROTOCOL)

**DO NOT use grep/glob until you have queried CodeSearch. This is enforced.**

```bash
# STEP 1: Query CodeSearch FIRST (required)
/codebase-search "relevant search terms" --top 5
# Or SQL:
sqlite3 ~/.local/share/codesearch/index_v2.db "SELECT file_path, line_number FROM entities WHERE name LIKE '%keyword%';"

# STEP 2: Query past errors/patterns
./.claude/skills/cfn-codesearch/query-agent-patterns.sh "description"

# STEP 3: Only if CodeSearch returns nothing, then use grep
```

**Violation of this protocol wastes tokens and time. CodeSearch exists to prevent duplicated work.**
