---
name: brave-search-api
description: This skill enables web searching using Brave Search API directly via curl. Use when searching for current information, news, articles, or web content. MCP server not required - calls API directly.
---

# Brave Search API (Direct)

## Overview

This skill enables web searching using the Brave Search API directly via curl commands. No MCP server required - saves context tokens.

## API Key

Environment variable: `BRAVE_API_KEY`

## Web Search

### Endpoint
```
GET https://api.search.brave.com/res/v1/web/search
```

### Parameters
- `q` (required): Search query
- `count` (optional): Results count (1-20, default 10)
- `offset` (optional): Pagination offset

### Usage

Generate and execute this curl command:

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=QUERY&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

### Example

```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=xterm.js+WebGL+tutorial&count=5" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq '.web.results[] | {title, url, description}'
```

## Local Search

### Endpoint
```
GET https://api.search.brave.com/res/v1/local/search
```

### Usage

```bash
curl -s "https://api.search.brave.com/res/v1/local/search?q=coffee+near+Shibuya" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"
```

## Response Processing

Use `jq` to extract relevant fields:

```bash
# Get titles and URLs
| jq '.web.results[] | {title, url}'

# Get descriptions
| jq '.web.results[] | {title, description}'

# Get first 3 results
| jq '.web.results[:3]'
```

## Common Workflows

### Research a Technology
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=VS+Code+extension+development+2024&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq '.web.results[:5] | .[] | {title, url}'
```

### Find Error Solutions
```bash
curl -s "https://api.search.brave.com/res/v1/web/search?q=WebGL+context+lost+solution&count=10" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq '.web.results[] | {title, url, description}'
```

## Notes

- URL encode spaces as `+` or `%20`
- API key must be set in environment
- Rate limits apply per subscription tier
