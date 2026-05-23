---
name: brave-search
description: Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser required.

## Setup

Run once before first use:

```bash
cd "${CODEX_HOME:-~/.codex}/skills/brave-search"
npm ci
```

Needs env: `BRAVE_API_KEY` (primary) or `BRAVE_AI_API_KEY` (fallback).

The script tries `BRAVE_API_KEY` first, then `BRAVE_AI_API_KEY` if the first is missing or rate-limited. If both fail, it falls back to HTML scraping.

## Search

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
./content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing

## Attribution

This skill was copied from steipete/agent-scripts.
Upstream: https://github.com/steipete/agent-scripts
License: MIT (see LICENSE)
