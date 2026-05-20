---
name: readwise-search
description: Search Readwise highlights. Use when the user wants to find highlights, quotes, notes, or annotations from their reading library. Triggers on "search highlights", "find in readwise", "what did I highlight about", "my notes on".
context: fork
agent: librarian
user-invocable: false
---

# Readwise Highlight Search

## Decision Tree

```
1. Do you know the EXACT document or author?
   YES -> Use fulltext filters (--full-text-queries)
   NO  -> Use vector search (semantic query)
2. Need document-level results (not highlights)?
   YES -> Use `readwise reader-search-documents --query "term"`
          or `readwise reader-list-documents` with --tag or --category filters
   NO  -> Use `readwise readwise-search-highlights`
3. Need keyword-exact match in highlight text?
   YES -> Use `readwise-custom highlights --search "term"` (v2 API)
   NO  -> Use vector search
```

## Quick Reference

### Vector + Fulltext Search (Highlights) — Official CLI

```bash
# Semantic search
readwise readwise-search-highlights --vector-search-term "fiduciary duty broker-dealer"

# With fulltext filters
readwise readwise-search-highlights --vector-search-term "regulation" \
  --full-text-queries '[{"field_name": "document_author", "search_term": "Jackson"}]'

# JSON output for piping
readwise readwise-search-highlights --vector-search-term "query" --json
```

**Fulltext filter fields** (via `--full-text-queries` JSON array):

| field_name | Searches |
|------------|----------|
| `document_author` | Document author name |
| `document_title` | Document title |
| `highlight_note` | Highlight notes/annotations |
| `highlight_plaintext` | Highlight text content |
| `highlight_tags` | Tags on highlights |

### Document Search (Hybrid) — Official CLI

```bash
# Hybrid search across document content
readwise reader-search-documents --query "proxy advisors"

# With filters
readwise reader-search-documents --query "regulation" --author-search "Jackson" --category-in article
readwise reader-search-documents --query "proxy" --tags-in "corps" --location-in later,archive

# By tag (no search, just filter)
readwise reader-list-documents --tag "proxy advisors" --json

# By category and location
readwise reader-list-documents --category article --location archive

# Recent updates
readwise reader-list-documents --updated-after 2026-01-01T00:00:00Z --limit 20
```

### Keyword Highlight Search — Custom CLI

```bash
# Exact text search across highlights (v2 API)
readwise-custom highlights --search "fiduciary" --limit 20 --json
```

## When to Use Each

| Need | Command | CLI |
|------|---------|-----|
| Semantic/conceptual highlight search | `readwise readwise-search-highlights --vector-search-term "query"` | Official |
| Hybrid document content search | `readwise reader-search-documents --query "term"` | Official |
| Keyword-exact match in highlights | `readwise-custom highlights --search "term"` | Custom |
| Documents by tag | `readwise reader-list-documents --tag "X"` | Official |
| Specific document | `readwise reader-get-document-details --document-id <id>` | Official |

## Output Format

Use `--json` for structured output. JSON search results include a `score` field (higher = more relevant, >0.01 typically meaningful).
