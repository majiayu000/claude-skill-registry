---
name: web-fetch
description: Fetch and extract clean content from URLs using Jina Reader API. Use when users need to read webpage content, extract article text, or fetch URL content for analysis. Triggers on "fetch this page", "read this URL", "extract content from", "get the content of", "what does this page say".
---

# Web Fetch

## Overview

Extract clean, readable content from any URL using Jina Reader API. Returns raw JSON with title, content, and metadata optimized for LLM consumption.

## When to Use

- User wants to read or analyze webpage content
- Need to extract article text from a URL
- Fetching documentation or reference pages
- Converting web pages to clean text for processing

## Workflow

1. Identify the URL from user request
2. Validate URL format
3. Run the fetch script
4. Present extracted content to user

## Usage

```bash
# Basic fetch
uv run --script scripts/web_fetch.py --url "https://example.com"

# With custom timeout
uv run --script scripts/web_fetch.py \
  --url "https://example.com/article" \
  --timeout 60
```

## Parameters

| Parameter   | Default    | Description                           |
| ----------- | ---------- | ------------------------------------- |
| `--url`     | (required) | URL to fetch and extract content from |
| `--timeout` | 30         | Request timeout in seconds            |

## Output Contract

| Scenario    | stdout             | stderr             | exit code |
| ----------- | ------------------ | ------------------ | --------- |
| Success     | Raw JSON from Jina | (empty)            | 0         |
| Invalid URL | (empty)            | Error message      | 1         |
| Timeout     | (empty)            | Timeout error      | 1         |
| HTTP Error  | (empty)            | HTTP error details | 1         |

Success output contains:

- Page title and description
- Clean extracted content (markdown-formatted)
- URL and metadata
- Token usage information

## Prerequisites

- Uses Jina Reader API (no API key required)
- Requires `uv` for running PEP 723 scripts

## Examples

### Fetch a webpage

```bash
uv run --script scripts/web_fetch.py \
  --url "https://docs.python.org/3/whatsnew/3.12.html"
```

### Fetch with longer timeout for slow pages

```bash
uv run --script scripts/web_fetch.py \
  --url "https://example.com/large-article" \
  --timeout 60
```
