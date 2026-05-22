---
name: docs-discovery
description: "Technical documentation discovery via context7 and web search. Capabilities: library/framework docs lookup, topic-specific search. Keywords: llms.txt, context7, documentation, library docs, API docs. Use when: searching library documentation, finding framework guides, looking up API references."
version: 7.0.0
---

# Documentation Discovery

**Mission:** Find official library/framework documentation quickly.

## Strategy

### Step 1: Try context7 First

```
mcp__context7__resolve-library-id("{library}")
→ Success? → mcp__context7__get-library-docs("{id}", topic="{topic}")
→ Fail? → Step 2
```

### Step 2: Search for Documentation URLs

**If context7 fails, run these searches in parallel:**

```
WebSearch: "{library} llms.txt"
WebSearch: "{library} official documentation"
```

### Step 3: Fetch Found URLs

**WebFetch the URLs found from Step 2:**
- llms.txt links → fetch and parse
- Documentation pages → fetch and extract content

## Workflow Summary

```
1. context7 (fast, curated)
   ↓ fail
2. WebSearch (parallel):
   - "{library} llms.txt"
   - "{library} official documentation"
   ↓ found URLs
3. WebFetch found URLs
   ↓ content
4. Parse & present to user
```

## Tools

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `mcp__context7__resolve-library-id` | Get context7 library ID |
| 1 | `mcp__context7__get-library-docs` | Fetch docs from context7 |
| 2 | `WebSearch` | Search for llms.txt and docs URLs |
| 3 | `WebFetch` | Fetch documentation content |

## Key Rules

- **context7 first** - Fastest, already curated
- **Search, don't guess** - Don't guess URL patterns, search for them
- **Parallel search** - Run multiple WebSearch queries together
- **Topic filtering** - Use topic param in context7, filter search results by topic
