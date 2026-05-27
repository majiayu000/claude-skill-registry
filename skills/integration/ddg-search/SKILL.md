# DuckDuckGo Search

Search the web using DuckDuckGo's HTML interface. No API key required.

## When to Use

- Web searches when you want to avoid API rate limits
- Quick lookups that don't need Brave's advanced features
- Fallback when `web_search` is unavailable or limited
- Any general web search task

## Usage

```bash
# Basic search (returns JSON)
ddg-search "your query"

# Limit results
ddg-search "your query" -n 5

# Region-specific results
ddg-search "your query" -r uk-en

# Plain text output (easier to read)
ddg-search "your query" --text

# Safe search off (for unrestricted results)
ddg-search "your query" --safe off
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-n, --count` | 10 | Number of results to return |
| `-r, --region` | (none) | Region code (e.g., `us-en`, `uk-en`, `de-de`) |
| `-s, --safe` | moderate | Safe search: `off`, `moderate`, `strict` |
| `-t, --text` | false | Output plain text instead of JSON |

## Output

### JSON (default)

```json
{
  "query": "wordpress block development",
  "results": [
    {
      "title": "Block Editor Handbook",
      "url": "https://developer.wordpress.org/block-editor/",
      "snippet": "Documentation for building blocks..."
    }
  ],
  "count": 1
}
```

### Plain Text (`--text`)

```
Query: wordpress block development

1. Block Editor Handbook
   https://developer.wordpress.org/block-editor/
   Documentation for building blocks...
```

## Region Codes

Common region codes for `-r` flag:

- `us-en` — United States
- `uk-en` — United Kingdom
- `ca-en` — Canada (English)
- `au-en` — Australia
- `de-de` — Germany
- `fr-fr` — France
- `es-es` — Spain
- `wt-wt` — No region (worldwide)

## Notes

- Results are from DuckDuckGo's index (may differ from Google/Brave)
- Rate limited to 1 request/second — be patient with multiple searches
- No instant answers or rich snippets — organic results only
- If parsing fails, DuckDuckGo may have changed their HTML structure

## Troubleshooting

**No results returned:**
- Check your query isn't too specific
- Try without region filtering
- Verify internet connectivity

**Error "HTTP 403":**
- You may be rate limited — wait a moment and retry
- Check if DuckDuckGo is accessible in your network
