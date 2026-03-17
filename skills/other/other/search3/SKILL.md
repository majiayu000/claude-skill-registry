---
name: search3
description: Meta web search with automatic fallback. Use when user asks to search the web and you want a resilient search pipeline: try Brave web_search first, then Tavily Search API, then Firecrawl Search (or scrape) if earlier providers fail or return no results.
---

# search3 (Brave → Tavily → Firecrawl)

Use this skill to make web search more reliable by falling back across three providers.

## What it does

1) Try **Brave** using the built-in `web_search` tool.
- For Chinese, always use:
  - `search_lang: "zh-hans"`
  - `ui_lang: "zh-CN"`

2) If Brave errors / returns empty, try **Tavily** via script: `{baseDir}/scripts/search3.py tavily ...`

3) If Tavily fails / returns empty, try **Firecrawl** via script: `{baseDir}/scripts/search3.py firecrawl ...`

## How to run (preferred)

Run the helper script and paste the JSON output back into the conversation:

```bash
python3 "{baseDir}/scripts/search3.py" all --query "<your query>" --max-results 8 --lang zh-hans
```

### Provider-only mode

```bash
python3 "{baseDir}/scripts/search3.py" brave --query "..."
python3 "{baseDir}/scripts/search3.py" tavily --query "..."
python3 "{baseDir}/scripts/search3.py" firecrawl --query "..."
```

## Output

The script prints JSON:
- `providerUsed`: brave|tavily|firecrawl
- `query`
- `results`: array of `{ title, url, snippet }`
- `errors`: any provider errors encountered before success

## Requirements

- Uses env vars (already configured in `~/.openclaw/openclaw.json`):
  - `TAVILY_API_KEY`
  - `FIRECRAWL_API_KEY`

If a key is missing, that provider is skipped.
