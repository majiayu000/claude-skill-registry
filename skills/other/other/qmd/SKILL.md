---
name: qmd
description: Local hybrid search for markdown notes and docs. Use BEFORE reading files to save tokens - search first, read only what's relevant. Provides 90% token savings on exploration tasks.
---

# qmd - Quick Markdown Search

Local search engine for Markdown notes, docs, and knowledge bases. **Use this to find relevant files BEFORE reading them** to dramatically reduce token usage.

## When to Use (IMPORTANT)

**ALWAYS prefer qmd search over reading files directly when:**
- Exploring a codebase or documentation
- Looking for specific functionality or concepts
- Finding related files to a topic
- Answering questions about the codebase

**Token savings:** Instead of reading 5 files (5000+ tokens), search first (50 tokens) and read only the relevant sections (200 tokens).

## Search Priority (follow this order)

1. **`qmd search "query"`** - Fast BM25 keyword search. Use this first, it's instant.
2. **`qmd vsearch "query"`** - Semantic similarity. Use only if keyword search fails.
3. **`qmd query "query"`** - Hybrid + reranking. Avoid unless user explicitly requests highest quality.

## Common Commands

```bash
# Fast keyword search (DEFAULT - use this first)
qmd search "authentication" -n 10

# Search specific collection
qmd search "api routes" -c my-project

# Get file paths only (for deciding what to read)
qmd search "database schema" --files

# JSON output for parsing
qmd search "error handling" --json

# Semantic search (slower, use as fallback)
qmd vsearch "how does the login flow work"
```

## Retrieve Documents

```bash
# Get specific file
qmd get "path/to/file.md"

# Get by document ID from search results
qmd get "#docid"

# Get multiple files
qmd multi-get "docs/*.md" --json
```

## Workflow Example

**Bad (token expensive):**
```
1. Read src/auth/login.ts (800 tokens)
2. Read src/auth/session.ts (600 tokens)
3. Read src/auth/middleware.ts (500 tokens)
4. Read src/auth/types.ts (400 tokens)
→ Found answer in middleware.ts
Total: 2300 tokens
```

**Good (token efficient):**
```
1. qmd search "authentication middleware" --files (response: 50 tokens)
   → Returns: src/auth/middleware.ts:45-62
2. Read only the relevant section (150 tokens)
Total: 200 tokens (90% savings!)
```

## Tips for Claude

- **Search before reading**: Always try qmd search first
- **Use --files flag**: Get paths without content to decide what to read
- **Be specific**: More specific queries = better results
- **Check collections**: Use `qmd status` to see indexed collections
- **Combine with cartographer**: CODEBASE_MAP.md gives structure, qmd gives content

## Maintenance

```bash
qmd status          # Check index health and collections
qmd update          # Re-index changed files (fast)
qmd embed           # Update vector embeddings (slower)
```
