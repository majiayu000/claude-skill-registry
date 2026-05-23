---
name: knowledge-base
description: Ingest URLs, documents, and transcripts into a searchable knowledge base. Query past research and curated documentation using full-text search. Trigger words: ingest, knowledge base, look up, search knowledge, what do we know about, research, index this, add to knowledge base.
license: MIT
metadata:
  author: sagemindai
  version: "1.0"
  requires: instar
  homepage: https://instar.sh
  user_invocable: "true"
---

# knowledge-base -- Searchable Knowledge Base for Instar Agents

Build a searchable knowledge base from external sources -- URLs, documents, transcripts, PDFs. Uses the existing MemoryIndex (FTS5) for search, so no new dependencies.

---

## How It Works

The knowledge base is a set of markdown files in `.instar/knowledge/` that MemoryIndex indexes alongside your other memory files. Each file has YAML frontmatter for metadata and is tracked in a catalog for browsing.

```
.instar/knowledge/
  catalog.json            # Registry of all ingested sources
  articles/               # Ingested web articles
  transcripts/            # Video/audio transcripts
  docs/                   # Curated reference documentation
```

---

## Ingesting Content

### Via CLI

```bash
# Ingest text content directly
instar knowledge ingest "Article content here..." --title "My Article" --tags "AI,agents"

# Ingest from a URL (fetch first, then ingest)
# Step 1: Fetch the content
python3 .claude/scripts/smart-fetch.py "https://example.com/article" --auto > /tmp/fetched.md
# Step 2: Ingest it
instar knowledge ingest "$(cat /tmp/fetched.md)" --title "Article Title" --url "https://example.com/article" --tags "topic1,topic2"
```

### Via API

```bash
curl -X POST http://localhost:4040/knowledge/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The article content...",
    "title": "Article Title",
    "url": "https://example.com/article",
    "type": "article",
    "tags": ["AI", "infrastructure"],
    "summary": "Brief description"
  }'
```

### Via Agent Workflow

When the agent wants to ingest content during a session:

1. Fetch the content (WebFetch, smart-fetch, transcript tools, or Read for local files)
2. Clean it (strip navigation, ads, boilerplate)
3. Call the ingest API or write the file manually:

```bash
# Write the markdown file with frontmatter
cat > .instar/knowledge/articles/2026-02-25-my-article.md << 'EOF'
---
title: "My Article"
source: "https://example.com/article"
ingested: "2026-02-25"
tags: ["AI", "infrastructure"]
---

# My Article

[Cleaned article content here]
EOF

# Sync the index to pick up the new file
instar memory sync
```

---

## Searching Knowledge

### CLI

```bash
# Search within knowledge base only
instar knowledge search "notification batching"

# Search all memory (including knowledge)
instar memory search "notification batching"
```

### API

```bash
# Knowledge-scoped search
curl "http://localhost:4040/memory/search?q=notification+batching&source=knowledge/&limit=5"

# Browse the catalog
curl "http://localhost:4040/knowledge/catalog"
curl "http://localhost:4040/knowledge/catalog?tag=AI"
```

---

## Managing Sources

### List all sources

```bash
instar knowledge list
instar knowledge list --tag AI
```

### Remove a source

```bash
# Find the source ID from the list
instar knowledge list

# Remove it
instar knowledge remove kb_20260225123456_abc123

# Re-sync the index
instar memory sync
```

### Via API

```bash
# Remove
curl -X DELETE "http://localhost:4040/knowledge/kb_20260225123456_abc123"
```

---

## MemoryIndex Configuration

To enable knowledge base indexing, add these sources to your `.instar/config.json` memory section:

```json
{
  "memory": {
    "enabled": true,
    "sources": [
      { "path": "AGENT.md", "type": "markdown", "evergreen": true },
      { "path": "USER.md", "type": "markdown", "evergreen": true },
      { "path": "knowledge/articles/", "type": "markdown", "evergreen": false },
      { "path": "knowledge/transcripts/", "type": "markdown", "evergreen": false },
      { "path": "knowledge/docs/", "type": "markdown", "evergreen": true }
    ]
  }
}
```

**Source behavior:**
- `articles/` and `transcripts/` use `evergreen: false` -- recent content ranks higher (30-day temporal decay)
- `docs/` uses `evergreen: true` -- reference documentation doesn't decay

---

## Content Types

| Type | Directory | Temporal Decay | Best For |
|------|-----------|----------------|----------|
| `article` | `articles/` | Yes (30-day) | Web articles, blog posts, news |
| `transcript` | `transcripts/` | Yes (30-day) | YouTube videos, podcasts, meetings |
| `doc` | `docs/` | No (evergreen) | API docs, manuals, reference material |

---

## Tips

- **Always sync after ingesting**: `instar memory sync` updates the FTS5 index
- **Use tags consistently**: Tags enable filtered browsing via `instar knowledge list --tag X`
- **Include source URLs**: Helps trace back to original content
- **Clean before ingesting**: Strip navigation, ads, cookie banners for better search results
- **Use smart-fetch for URLs**: `python3 .claude/scripts/smart-fetch.py URL --auto` gets clean markdown
