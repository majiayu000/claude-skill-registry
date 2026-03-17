---
name: crawl4ai
description: This skill should be used when users need to scrape websites, extract structured data, handle JavaScript-heavy pages, crawl multiple URLs, or build automated web data pipelines. Includes optimized extraction patterns with schema generation for efficient, LLM-free extraction.
---

# Crawl4AI

## Overview

Crawl4AI provides comprehensive web crawling and data extraction capabilities. This skill supports both **CLI** (recommended for quick tasks) and **Python SDK** (for programmatic control).

**Choose your interface:**

- **CLI** (`crwl`) - Quick, scriptable commands: [CLI Guide](references/cli-guide.md)
- **Python SDK** - Full programmatic control: [SDK Guide](references/sdk-guide.md)

---

## Quick Start

### Installation

```bash
pip install crawl4ai
crawl4ai-setup

# Verify installation
crawl4ai-doctor
```

### CLI (Recommended)

```bash
# Basic crawling - returns markdown
crwl https://example.com

# Get markdown output
crwl https://example.com -o markdown

# JSON output with cache bypass
crwl https://example.com -o json -v --bypass-cache

# See more examples
crwl --example
```

### Python SDK

```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:500])

asyncio.run(main())
```

For SDK configuration details: [SDK Guide - Configuration](references/sdk-guide.md#configuration) (lines 61-150)

---

## Core Concepts

### Configuration Layers

Both CLI and SDK use the same underlying configuration:

| Concept | CLI | SDK |
|---------|-----|-----|
| Browser settings | `-B browser.yml` or `-b "param=value"` | `BrowserConfig(...)` |
| Crawl settings | `-C crawler.yml` or `-c "param=value"` | `CrawlerRunConfig(...)` |
| Extraction | `-e extract.yml -s schema.json` | `extraction_strategy=...` |
| Content filter | `-f filter.yml` | `markdown_generator=...` |

### Key Parameters

**Browser Configuration:**

- `headless`: Run with/without GUI
- `viewport_width/height`: Browser dimensions
- `user_agent`: Custom user agent
- `proxy_config`: Proxy settings

**Crawler Configuration:**

- `page_timeout`: Max page load time (ms)
- `wait_for`: CSS selector or JS condition to wait for
- `cache_mode`: bypass, enabled, disabled
- `js_code`: JavaScript to execute
- `css_selector`: Focus on specific element

For complete parameters: [CLI Config](references/cli-guide.md#configuration) | [SDK Config](references/sdk-guide.md#configuration)

### Output Content

Every crawl returns:

- **markdown** - Clean, formatted markdown
- **html** - Raw HTML
- **links** - Internal and external links discovered
- **media** - Images, videos, audio found
- **extracted_content** - Structured data (if extraction configured)

---

## Markdown Generation (Primary Use Case)

Crawl4AI excels at generating clean, well-formatted markdown:

### CLI

```bash
# Basic markdown
crwl https://docs.example.com -o markdown

# Filtered markdown (removes noise)
crwl https://docs.example.com -o markdown-fit

# With content filter
crwl https://docs.example.com -f filter_bm25.yml -o markdown-fit
```

**Filter configuration:**

```yaml
# filter_bm25.yml (relevance-based)
type: "bm25"
query: "machine learning tutorials"
threshold: 1.0
```

### Python SDK

```python
from crawl4ai.content_filter_strategy import BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

bm25_filter = BM25ContentFilter(user_query="machine learning", bm25_threshold=1.0)
md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)

config = CrawlerRunConfig(markdown_generator=md_generator)
result = await crawler.arun(url, config=config)

print(result.markdown.fit_markdown)  # Filtered
print(result.markdown.raw_markdown)  # Original
```

For content filters: [Content Processing](references/complete-sdk-reference.md#content-processing) (lines 2481-3101)

---

## Data Extraction

### 1. Schema-Based CSS Extraction (Most Efficient)

**No LLM required** - fast, deterministic, cost-free.

**CLI:**

```bash
# Generate schema once (uses LLM)
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"

# Use schema for extraction (no LLM)
crwl https://shop.com -e extract_css.yml -s product_schema.json -o json
```

**Schema format:**

```json
{
  "name": "products",
  "baseSelector": ".product-card",
  "fields": [
    {"name": "title", "selector": "h2", "type": "text"},
    {"name": "price", "selector": ".price", "type": "text"},
    {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
  ]
}
```

### 2. LLM-Based Extraction

For complex or irregular content:

**CLI:**

```yaml
# extract_llm.yml
type: "llm"
provider: "openai/gpt-4o-mini"
instruction: "Extract product names and prices"
api_token: "your-token"
```

```bash
crwl https://shop.com -e extract_llm.yml -o json
```

For extraction details: [Extraction Strategies](references/complete-sdk-reference.md#extraction-strategies) (lines 4522-5429)

---

## Advanced Patterns

### Dynamic Content (JavaScript-Heavy Sites)

**CLI:**

```bash
crwl https://example.com -c "wait_for=css:.ajax-content,scan_full_page=true,page_timeout=60000"
```

**Crawler config:**

```yaml
# crawler.yml
wait_for: "css:.ajax-content"
scan_full_page: true
page_timeout: 60000
delay_before_return_html: 2.0
```

### Multi-URL Processing

**CLI (sequential):**

```bash
for url in url1 url2 url3; do crwl "$url" -o markdown; done
```

**Python SDK (concurrent):**

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
results = await crawler.arun_many(urls, config=config)
```

For batch processing: [arun_many() Reference](references/complete-sdk-reference.md#arunmany-reference) (lines 1057-1224)

### Session & Authentication

**CLI:**

```yaml
# login_crawler.yml
session_id: "user_session"
js_code: |
  document.querySelector('#username').value = 'user';
  document.querySelector('#password').value = 'pass';
  document.querySelector('#submit').click();
wait_for: "css:.dashboard"
```

```bash
# Login
crwl https://site.com/login -C login_crawler.yml

# Access protected content (session reused)
crwl https://site.com/protected -c "session_id=user_session"
```

For session management: [Advanced Features](references/complete-sdk-reference.md#advanced-features) (lines 5429-5940)

### Anti-Detection & Proxies

**CLI:**

```yaml
# browser.yml
headless: true
proxy_config:
  server: "http://proxy:8080"
  username: "user"
  password: "pass"
user_agent_mode: "random"
```

```bash
crwl https://example.com -B browser.yml
```

---

## Common Use Cases

### Documentation to Markdown

```bash
crwl https://docs.example.com -o markdown > docs.md
```

### E-commerce Product Monitoring

```bash
# Generate schema once
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"

# Monitor (no LLM costs)
crwl https://shop.com -e extract_css.yml -s schema.json -o json
```

### News Aggregation

```bash
# Multiple sources with filtering
for url in news1.com news2.com news3.com; do
  crwl "https://$url" -f filter_bm25.yml -o markdown-fit
done
```

### Interactive Q&A

```bash
# First view content
crwl https://example.com -o markdown

# Then ask questions
crwl https://example.com -q "What are the main conclusions?"
crwl https://example.com -q "Summarize the key points"
```

---

## Resources

### Provided Scripts

- **scripts/extraction_pipeline.py** - Schema generation and extraction
- **scripts/basic_crawler.py** - Simple markdown extraction
- **scripts/batch_crawler.py** - Multi-URL processing

### Reference Documentation

| Document | Purpose |
|----------|---------|
| [CLI Guide](references/cli-guide.md) | Command-line interface reference |
| [SDK Guide](references/sdk-guide.md) | Python SDK quick reference |
| [Complete SDK Reference](references/complete-sdk-reference.md) | Full API documentation (5900+ lines) |

---

## Best Practices

1. **Start with CLI** for quick tasks, SDK for automation
2. **Use schema-based extraction** - 10-100x more efficient than LLM
3. **Enable caching during development** - `--bypass-cache` only when needed
4. **Set appropriate timeouts** - 30s normal, 60s+ for JS-heavy sites
5. **Use content filters** for cleaner, focused markdown
6. **Respect rate limits** - Add delays between requests

---

## Troubleshooting

### JavaScript Not Loading

```bash
crwl https://example.com -c "wait_for=css:.dynamic-content,page_timeout=60000"
```

### Bot Detection Issues

```bash
crwl https://example.com -B browser.yml
```

```yaml
# browser.yml
headless: false
viewport_width: 1920
viewport_height: 1080
user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

### Content Not Extracted

```bash
# Debug: see full output
crwl https://example.com -o all -v

# Try different wait strategy
crwl https://example.com -c "wait_for=js:document.querySelector('.content')!==null"
```

### Session Issues

```bash
# Verify session
crwl https://site.com -c "session_id=test" -o all | grep -i session
```

---

For comprehensive API documentation, see [Complete SDK Reference](references/complete-sdk-reference.md).
