---
name: free-search
description: Free web search (DuckDuckGo HTML) without paid APIs.
metadata: {"openclaw":{"emoji":"🔎","os":["darwin","linux"],"requires":{"bins":["node"]}}}
---

# Free Search (DuckDuckGo)

Use this skill when the user asks to **search the web** but wants to avoid paid search APIs.

## What it does

- Runs a small local script that queries DuckDuckGo's HTML endpoint.
- Returns top results as JSON (title + URL + snippet when available).

## How to use

When you need web search results, run:

```bash
node "{baseDir}/ddg_search.mjs" "<query>" --max 5 --json
```

Then:

- Show the top results.
- Ask which result(s) to open/summarize.

## Constraints / policy

- Do not attempt to bypass paywalls or logins.
- If a site blocks scraping, report it and propose alternatives (official APIs, RSS, public pages).
