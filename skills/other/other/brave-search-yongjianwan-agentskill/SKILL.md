---
name: brave-search
description: Use Brave Search API to search the web and return structured results (title/url/snippet). Trigger when the user asks to enable Brave search, configure Brave API key, or perform web search using Brave.
metadata: {"openclaw":{"emoji":"🔎","requires":{"bins":["node"],"env":["BRAVE_API_KEY"]},"primaryEnv":"BRAVE_API_KEY","homepage":"https://brave.com/search/api/"}}
---

# Brave Search

Use Brave Search API via the bundled script.

## Requirements

- Set `BRAVE_API_KEY` in the Gateway environment (recommended) or in `~/.openclaw/.env`.
- Get API key from: https://api.search.brave.com/

## Commands

- Run a search:
  - `node {baseDir}/scripts/brave_search.mjs "<query>" --count 5`

- Search news:
  - `node {baseDir}/scripts/brave_search.mjs "<query>" --type news --count 5`

## Notes

- This skill does not modify `web_search`; it provides a Brave-backed alternative you can invoke when you specifically want Brave Search.
- Free tier: 2000 requests/month, 1 req/sec
