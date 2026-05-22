---
name: leann-search
description: Semantic search across codebase using LEANN vector index
allowed-tools: [Bash, Read]
---

# LEANN Semantic Search

Use LEANN for meaning-based code search instead of grep.

## When to Use

- **Conceptual queries**: "how does authentication work", "where are errors handled"
- **Understanding patterns**: "streaming implementation", "provider architecture"
- **Finding related code**: code that's semantically similar but uses different terms

## When NOT to Use

- **Exact matches**: Use Grep for `class Foo`, `def bar`, specific identifiers
- **Regex patterns**: Use Grep for `error.*handling`, `import.*from`
- **File paths**: Use Glob for `*.test.ts`, `src/**/*.py`

## Commands

```bash
# Search the current project's index
leann search <index-name> "<query>" --top-k 5

# List available indexes
leann list

# Example
leann search rigg "how do providers handle streaming" --top-k 5
```

## MCP Tool (in Claude Code)

```
leann_search(index_name="rigg", query="your semantic query", top_k=5)
```

## Rebuilding the Index

When codebase changes significantly:

```bash
cd /path/to/project
leann build <project-name> --docs src tests scripts \
  --file-types '.ts,.py,.md,.json' \
  --no-recompute --no-compact \
  --embedding-mode sentence-transformers \
  --embedding-model all-MiniLM-L6-v2
```

## How It Works

1. LEANN uses sentence embeddings to understand *meaning*
2. Searches find conceptually similar code, not just text matches
3. Results ranked by semantic similarity score (0-1)

## Grep vs LEANN Decision

| Query Type | Tool | Example |
|------------|------|---------|
| Natural language | LEANN | "how does caching work" |
| Class/function name | Grep | "class CacheManager" |
| Pattern matching | Grep | `error\|warning` |
| Find implementations | LEANN | "rate limiting logic" |
