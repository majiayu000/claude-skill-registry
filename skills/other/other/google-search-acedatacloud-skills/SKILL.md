---
name: google-search
description: Search the web using Google via AceDataCloud API. Use when searching for web pages, images, news, maps, local places, or videos. Supports localization, time filtering, and pagination. Returns structured results with titles, snippets, URLs, and rich data.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-serp for tool-use.
---

# Google Search (SERP)

Search the web through AceDataCloud's Google SERP API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/serp/google \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "latest AI news", "search_type": "search"}'
```

## Search Types

| Type | Description | Returns |
|------|-------------|---------|
| `search` | Web search (default) | Organic results, knowledge graph, rich snippets |
| `images` | Image search | Image URLs, titles, sources |
| `news` | News articles | Headlines, sources, publish dates |
| `maps` | Map results | Locations, coordinates |
| `places` | Local businesses/places | Name, address, rating, reviews |
| `videos` | Video results | Video URLs, thumbnails, duration |

## Parameters

```json
POST /serp/google
{
  "query": "your search query",
  "search_type": "search",
  "country": "us",
  "language": "en",
  "time_range": "qdr:w",
  "number": 10,
  "page": 1
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search query (required) |
| `search_type` | string | One of: search, images, news, maps, places, videos |
| `country` | string | Country code (e.g., "us", "uk", "cn", "jp") |
| `language` | string | Language code (e.g., "en", "zh", "ja") |
| `time_range` | string | Time filter (see below) |
| `number` | int | Number of results per page |
| `page` | int | Page number for pagination |

## Time Range Options

| Value | Period |
|-------|--------|
| `qdr:h` | Past hour |
| `qdr:d` | Past 24 hours |
| `qdr:w` | Past week |
| `qdr:m` | Past month |
| `qdr:y` | Past year |

## Response Structure

Web search returns structured data including:
- `organic_results`: Main search results with title, link, snippet
- `knowledge_graph`: Entity information panel (when available)
- `related_searches`: Related query suggestions

## MCP Server

```bash
pip install mcp-serp
```

Or hosted: `https://serp.mcp.acedata.cloud/mcp`

Key tool: `serp_google_search`

## Gotchas

- Default search type is `"search"` (web). Always specify `search_type` for non-web searches
- Country and language codes affect result localization significantly
- `number` controls results per page, not total results — use `page` for pagination
- Time range only applies to web search and news, not images or places
- Image search returns thumbnail and full-size URLs — use full-size for downloads
- Places search works best with location-specific queries (e.g., "restaurants near Times Square")
