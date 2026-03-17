---
name: mcp-firecrawl
description: This skill provides guidance for using Firecrawl MCP for web scraping and content extraction. Use when scraping web pages, crawling websites, searching the web with content extraction, mapping site URLs, or extracting structured data from web pages.
---

# Firecrawl MCP

## Overview

This skill enables web scraping and content extraction using Firecrawl through MCP. Firecrawl provides powerful capabilities for scraping single pages, crawling entire websites, searching with content extraction, and extracting structured data.

## When to Use This Skill

- Scraping content from single web pages
- Crawling multiple pages on a website
- Searching the web with automatic content extraction
- Discovering all URLs on a website
- Extracting structured data (prices, names, details)

## Tool Selection Guide

| Task | Tool | Notes |
|------|------|-------|
| Single page content | `firecrawl_scrape` | Fast, reliable |
| Find URLs on site | `firecrawl_map` | Discovery only |
| Web search | `firecrawl_search` | With optional scraping |
| Multiple pages | `firecrawl_map` + `firecrawl_scrape` | Better than crawl |
| Structured data | `firecrawl_extract` | Uses LLM extraction |
| Full site crawl | `firecrawl_crawl` | Use with caution |

## Core Tools

### firecrawl_scrape

Scrape content from a single URL. Most powerful and reliable scraper.

**Tool:** `mcp__firecrawl__firecrawl_scrape`

```
mcp__firecrawl__firecrawl_scrape({
  url: "https://docs.example.com/api",
  formats: ["markdown"],
  onlyMainContent: true,
  maxAge: 172800000
})
```

**Key Parameters:**
- `url`: Target URL
- `formats`: Output formats - "markdown", "html", "links"
- `onlyMainContent`: Extract only main content (recommended)
- `maxAge`: Cache TTL in ms (500% faster with cache)

### firecrawl_search

Search the web and optionally scrape results.

**Tool:** `mcp__firecrawl__firecrawl_search`

**Without scraping (preferred):**
```
mcp__firecrawl__firecrawl_search({
  query: "xterm.js terminal tutorial",
  limit: 5
})
```

**With scraping:**
```
mcp__firecrawl__firecrawl_search({
  query: "VS Code extension API",
  limit: 3,
  scrapeOptions: {
    formats: ["markdown"],
    onlyMainContent: true
  }
})
```

**Search Operators:**
| Operator | Example | Description |
|----------|---------|-------------|
| `""` | `"exact phrase"` | Exact match |
| `-` | `-deprecated` | Exclude term |
| `site:` | `site:github.com` | Specific site |
| `inurl:` | `inurl:docs` | URL contains |
| `intitle:` | `intitle:tutorial` | Title contains |

### firecrawl_map

Discover all URLs on a website.

**Tool:** `mcp__firecrawl__firecrawl_map`

```
mcp__firecrawl__firecrawl_map({
  url: "https://docs.example.com",
  limit: 100,
  search: "api"
})
```

### firecrawl_extract

Extract structured data using LLM.

**Tool:** `mcp__firecrawl__firecrawl_extract`

```
mcp__firecrawl__firecrawl_extract({
  urls: ["https://shop.example.com/product/123"],
  prompt: "Extract product details",
  schema: {
    type: "object",
    properties: {
      name: { type: "string" },
      price: { type: "number" }
    },
    required: ["name", "price"]
  }
})
```

### firecrawl_crawl

Crawl multiple pages (use sparingly).

**Tool:** `mcp__firecrawl__firecrawl_crawl`

```
mcp__firecrawl__firecrawl_crawl({
  url: "https://docs.example.com/guide",
  maxDiscoveryDepth: 2,
  limit: 10
})
```

**Warning:** Crawl can return large responses. Keep limits low.

## Best Practices

1. **Prefer scrape over crawl**: Use `map` + `scrape` for better control
2. **Use caching**: Add `maxAge` for repeated requests
3. **Search then scrape**: Search without formats, then scrape relevant URLs
4. **Limit crawl depth**: Keep `maxDiscoveryDepth` and `limit` low
5. **Use onlyMainContent**: Get cleaner content without navigation

## References

For complete tool parameters, see `references/tools.md`.
