---
name: brave-search
description: Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required.
metadata: {"marketbot":{"emoji":"🦁","requires":{"bins":["npm","node"]}}}
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser required.

## Setup

Run once before first use to install dependencies:

```bash
cd skills/brave-search
npm install
```

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

## Dependencies

- `@mozilla/readability`
- `jsdom`
- `turndown`
