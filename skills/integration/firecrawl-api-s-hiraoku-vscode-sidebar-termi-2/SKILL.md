---
name: firecrawl-api
description: This skill enables web scraping and content extraction using Firecrawl API directly via curl. Use when scraping web pages, crawling websites, or extracting structured data. MCP server not required.
---

# Firecrawl API (Direct)

## Overview

Firecrawl provides powerful web scraping and content extraction. This skill uses the API directly via curl - no MCP server required.

## API Key

Environment variable: `FIRECRAWL_API_KEY`

## Scrape Single Page

Extract content from a single URL.

### Endpoint
```
POST https://api.firecrawl.dev/v1/scrape
```

### Usage
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["markdown"]
  }'
```

### Parameters
- `url` (required): URL to scrape
- `formats` (optional): Output formats - `markdown`, `html`, `rawHtml`, `links`
- `onlyMainContent` (optional): Extract main content only (default: true)
- `waitFor` (optional): Wait time in ms for dynamic content

### Example with Options
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com/api",
    "formats": ["markdown"],
    "onlyMainContent": true,
    "waitFor": 1000
  }' | jq '.data.markdown'
```

## Map Website URLs

Discover all URLs on a website.

### Endpoint
```
POST https://api.firecrawl.dev/v1/map
```

### Usage
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/map" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com"
  }' | jq '.links[]'
```

## Search Web

Search the web and optionally scrape results.

### Endpoint
```
POST https://api.firecrawl.dev/v1/search
```

### Usage
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/search" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "xterm.js WebGL performance",
    "limit": 5
  }'
```

## Crawl Website

Crawl multiple pages from a website.

### Endpoint
```
POST https://api.firecrawl.dev/v1/crawl
```

### Usage
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/crawl" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "limit": 10,
    "maxDepth": 2
  }'
```

This returns a job ID. Check status with:
```bash
curl -s "https://api.firecrawl.dev/v1/crawl/JOB_ID" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY"
```

## Common Workflows

### Scrape Documentation
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://xtermjs.org/docs/",
    "formats": ["markdown"]
  }' | jq '.data.markdown'
```

### Extract Links from Page
```bash
curl -s -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "formats": ["links"]
  }' | jq '.data.links[]'
```

## Response Processing

```bash
# Get markdown content
| jq '.data.markdown'

# Get metadata
| jq '.data.metadata'

# Get title and description
| jq '.data.metadata | {title, description}'
```

## Notes

- API key required (set FIRECRAWL_API_KEY)
- Credits consumed per request
- Use `waitFor` for JavaScript-heavy pages
- Crawl jobs are async - poll for completion
