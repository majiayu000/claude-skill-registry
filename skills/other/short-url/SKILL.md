---
name: short-url
description: Create short URLs via AceDataCloud API. Use when generating shortened links for sharing, or batch-creating multiple short URLs at once. Supports custom slugs and expiration.
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
compatibility: Requires ACEDATACLOUD_API_TOKEN environment variable. Optionally pair with mcp-short-url for tool-use.
---

# Short URL Service

Create short URLs through AceDataCloud's URL shortening API.

## Authentication

```bash
export ACEDATACLOUD_API_TOKEN="your-token-here"
```

## Quick Start

```bash
curl -X POST https://api.acedata.cloud/short-url \
  -H "Authorization: Bearer $ACEDATACLOUD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very-long-url-path?with=params"}'
```

## Workflows

### 1. Create a Single Short URL

```json
POST /short-url
{
  "url": "https://example.com/article/2024/awesome-content",
  "expires_in": 86400
}
```

Response:

```json
{
  "short_url": "https://acda.cc/abc123",
  "url": "https://example.com/article/2024/awesome-content"
}
```

### 2. Batch Create Short URLs

Create multiple short URLs in one request.

```json
POST /short-url/batch
{
  "urls": [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
  ]
}
```

## Parameters

### Single

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | Yes | The original long URL to shorten |
| `expires_in` | No | Expiration in seconds (omit for permanent) |

### Batch

| Parameter | Required | Description |
|-----------|----------|-------------|
| `urls` | Yes | Array of URLs to shorten |

## MCP Server

```bash
pip install mcp-short-url
```

Or hosted: `https://short-url.mcp.acedata.cloud/mcp`

Key tools: `create_short_url`, `batch_create_short_urls`

## Gotchas

- Short URLs use the `acda.cc` domain
- Results are returned synchronously — no task polling needed
- Batch endpoint accepts an array and returns an array in the same order
- If `expires_in` is omitted, the short URL is permanent
