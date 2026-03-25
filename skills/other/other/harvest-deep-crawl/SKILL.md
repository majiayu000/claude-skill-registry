---
name: harvest-deep-crawl
description: Multi-page deep crawling - documentation sites, wikis, knowledge bases
allowed-tools: [Bash, Read, Write, WebFetch, WebSearch]
keywords: [crawl, deep, multi-page, documentation, wiki, site, knowledge-base, depth]
---

# Harvest Deep Crawl

Crawl multi-page websites following internal links to a specified depth. Ideal for building complete knowledge bases from documentation sites, wikis, and reference materials.

## Usage

```
/crawl <url> --depth <N>
```

## Examples

```bash
# Crawl docs site 3 levels deep
/crawl https://docs.example.com --depth 3

# Crawl a specific section
/crawl https://docs.example.com/api --depth 2

# Crawl with page limit
/crawl https://wiki.example.com --depth 5 --max-pages 50
```

## Parameters

| Param | Default | Description |
|-------|---------|-------------|
| `--depth` | 2 | Max link-following depth |
| `--max-pages` | 100 | Max pages to crawl |
| `--same-domain` | true | Stay on same domain |
| `--include` | * | URL pattern to include |
| `--exclude` | - | URL pattern to exclude |

## How It Works

1. Start at root URL, extract all internal links
2. Follow links up to specified depth (BFS order)
3. Extract content from each page
4. Deduplicate pages with > 90% content overlap
5. Build table of contents from page hierarchy
6. Merge into coherent knowledge base
7. Save to `.claude/cache/agents/harvest/crawl-{domain}/`

## Output Structure

```
crawl-{domain}-{timestamp}/
  index.md          # Table of contents + summary
  page-001.md       # First page content
  page-002.md       # Second page content
  ...
  metadata.json     # Crawl stats, URLs, timings
```

## Crawl Engine

### Primary: crawl4ai (Docker port 11235)

```bash
curl -s http://localhost:11235/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://docs.example.com"],
    "max_depth": 3,
    "same_domain": true,
    "word_count_threshold": 50
  }'
```

### Fallback: Manual Link Following

When Docker unavailable:
1. WebFetch root URL
2. Parse links from markdown output
3. WebFetch each linked page (depth-limited)
4. Compile results

## Use Cases

| Scenario | Depth | Max Pages |
|----------|-------|-----------|
| API reference | 2-3 | 50 |
| Full documentation site | 3-5 | 100 |
| Wiki section | 2 | 30 |
| Changelog history | 1-2 | 20 |
| Tutorial series | 2-3 | 30 |

## Rules

- Respect robots.txt
- Max 2 requests/second
- Skip binary files (PDF, images, videos)
- Detect and skip infinite pagination
- Cache results for 24 hours
