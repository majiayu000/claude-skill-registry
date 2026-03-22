---
name: webserp
description: Web search across 7 engines in parallel with browser impersonation. Use when the agent needs current information from the web — news, documentation, recent events, or anything beyond training data. Returns structured JSON (SearXNG-compatible) with title, URL, and content. Uses curl_cffi to mimic real browser fingerprints so requests don't get blocked. Install with `pip install webserp`. No API keys needed.
---

# webserp

Metasearch CLI — queries Google, DuckDuckGo, Brave, Yahoo, Mojeek, Startpage, and Presearch in parallel. Uses curl_cffi for browser impersonation. Results like a browser, speed like an API.

## When to use webserp

1. You need current/recent information not in your training data
2. You need to verify facts or find sources
3. You need to discover URLs, documentation, or code repositories
4. The user asks about recent events, releases, or news

## Install

```bash
pip install webserp
```

No API keys, no configuration. Just install and search.

## Usage

```bash
# Search all 7 engines (default)
webserp "how to deploy docker containers"

# Search specific engines
webserp "python async tutorial" --engines google,brave,duckduckgo

# Limit results per engine
webserp "rust vs go" --max-results 5

# Show which engines succeeded/failed
webserp "test query" --verbose

# Set per-engine timeout
webserp "query" --timeout 15

# Use a proxy
webserp "query" --proxy "socks5://127.0.0.1:1080"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-e, --engines` | Comma-separated engine list | all |
| `-n, --max-results` | Max results per engine | 10 |
| `--timeout` | Per-engine timeout (seconds) | 10 |
| `--proxy` | Proxy URL for all requests | none |
| `--verbose` | Show engine status in stderr | false |

## Output format

JSON to stdout (SearXNG-compatible):

```json
{
  "query": "deployment issue",
  "number_of_results": 42,
  "results": [
    {
      "title": "How to fix Docker deployment issues",
      "url": "https://example.com/docker-fix",
      "content": "Common Docker deployment problems and solutions...",
      "engine": "google"
    }
  ],
  "suggestions": [],
  "unresponsive_engines": []
}
```

Parse with `jq` or any JSON parser. The `results` array contains `title`, `url`, `content`, and `engine` for each result. `unresponsive_engines` lists any engines that failed with the error reason.

## Tips

- Use `--max-results 5` to keep output concise when you just need a few links
- Use `--engines google,brave` to target specific engines for faster results
- Use `--verbose` (writes to stderr) to see which engines responded — the JSON on stdout is unaffected
- Results are deduplicated by URL across engines — you won't get the same link twice
