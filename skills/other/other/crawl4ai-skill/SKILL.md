---
name: crawl4ai
description: Complete toolkit for web crawling and data extraction using Crawl4AI. This skill should be used when users need to scrape websites, extract structured data, handle JavaScript-heavy pages, crawl multiple URLs, or build automated web data pipelines. Includes optimized extraction patterns with schema generation for efficient, LLM-free extraction.
version: 0.7.4
crawl4ai_version: ">=0.7.4"
last_updated: 2025-01-19
---

# Crawl4AI

## Overview

This skill provides comprehensive support for web crawling and data extraction using the Crawl4AI library, including the complete SDK reference, ready-to-use scripts for common patterns, and optimized workflows for efficient data extraction.

## Quick Start

### Installation Check
```bash
# Verify installation
crawl4ai-doctor

# If issues, run setup
crawl4ai-setup
```

### Basic First Crawl
```python
import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com")
        print(result.markdown[:500])  # First 500 chars

asyncio.run(main())
```

### Using Provided Scripts
```bash
# Simple markdown extraction
python scripts/basic_crawler.py https://example.com

# Batch processing
python scripts/batch_crawler.py urls.txt

# Data extraction
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"
```

## Core Crawling Fundamentals

### 1. Basic Crawling

Understanding the core components for any crawl:

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# Browser configuration (controls browser behavior)
browser_config = BrowserConfig(
    headless=True,  # Run without GUI
    viewport_width=1920,
    viewport_height=1080,
    user_agent="custom-agent"  # Optional custom user agent
)

# Crawler configuration (controls crawl behavior)
crawler_config = CrawlerRunConfig(
    page_timeout=30000,  # 30 seconds timeout
    screenshot=True,  # Take screenshot
    remove_overlay_elements=True  # Remove popups/overlays
)

# Execute crawl with arun()
async with AsyncWebCrawler(config=browser_config) as crawler:
    result = await crawler.arun(
        url="https://example.com",
        config=crawler_config
    )

    # CrawlResult contains everything
    print(f"Success: {result.success}")
    print(f"HTML length: {len(result.html)}")
    print(f"Markdown length: {len(result.markdown)}")
    print(f"Links found: {len(result.links)}")
```

### 2. Configuration Deep Dive

**BrowserConfig** - Controls the browser instance:
- `headless`: Run with/without GUI
- `viewport_width/height`: Browser dimensions
- `user_agent`: Custom user agent string
- `cookies`: Pre-set cookies
- `headers`: Custom HTTP headers

**CrawlerRunConfig** - Controls each crawl:
- `page_timeout`: Maximum page load/JS execution time (ms)
- `wait_for`: CSS selector or JS condition to wait for (optional)
- `cache_mode`: Control caching behavior
- `js_code`: Execute custom JavaScript
- `screenshot`: Capture page screenshot
- `session_id`: Persist session across crawls

### 3. Content Processing

Basic content operations available in every crawl:

```python
result = await crawler.arun(url)

# Access extracted content
markdown = result.markdown  # Clean markdown
html = result.html  # Raw HTML
text = result.cleaned_html  # Cleaned HTML

# Media and links
images = result.media["images"]
videos = result.media["videos"]
internal_links = result.links["internal"]
external_links = result.links["external"]

# Metadata
title = result.metadata["title"]
description = result.metadata["description"]
```

## Markdown Generation (Primary Use Case)

### 1. Basic Markdown Extraction

Crawl4AI excels at generating clean, well-formatted markdown:

```python
# Simple markdown extraction
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://docs.example.com")

    # High-quality markdown ready for LLMs
    with open("documentation.md", "w") as f:
        f.write(result.markdown)
```

### 2. Fit Markdown (Content Filtering)

Use content filters to get only relevant content:

```python
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Option 1: Pruning filter (removes low-quality content)
pruning_filter = PruningContentFilter(threshold=0.4, threshold_type="fixed")

# Option 2: BM25 filter (relevance-based filtering)
bm25_filter = BM25ContentFilter(user_query="machine learning tutorials", bm25_threshold=1.0)

md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)

config = CrawlerRunConfig(markdown_generator=md_generator)

result = await crawler.arun(url, config=config)
# Access filtered content
print(result.markdown.fit_markdown)  # Filtered markdown
print(result.markdown.raw_markdown)  # Original markdown
```

### 3. Markdown Customization

Control markdown generation with options:

```python
config = CrawlerRunConfig(
    # Exclude elements from markdown
    excluded_tags=["nav", "footer", "aside"],

    # Focus on specific CSS selector
    css_selector=".main-content",

    # Clean up formatting
    remove_forms=True,
    remove_overlay_elements=True,

    # Control link handling
    exclude_external_links=True,
    exclude_internal_links=False
)

# Custom markdown generation
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

generator = DefaultMarkdownGenerator(
    options={
        "ignore_links": False,
        "ignore_images": False,
        "image_alt_text": True
    }
)
```

## Data Extraction

### 1. Schema-Based Extraction (Most Efficient)

For repetitive patterns, generate schema once and reuse:

```bash
# Step 1: Generate schema with LLM (one-time)
python scripts/extraction_pipeline.py --generate-schema https://shop.com "extract products"

# Step 2: Use schema for fast extraction (no LLM)
python scripts/extraction_pipeline.py --use-schema https://shop.com generated_schema.json
```

### 2. Manual CSS/JSON Extraction

When you know the structure:

```python
schema = {
    "name": "articles",
    "baseSelector": "article.post",
    "fields": [
        {"name": "title", "selector": "h2", "type": "text"},
        {"name": "date", "selector": ".date", "type": "text"},
        {"name": "content", "selector": ".content", "type": "text"}
    ]
}

extraction_strategy = JsonCssExtractionStrategy(schema=schema)
config = CrawlerRunConfig(extraction_strategy=extraction_strategy)
```

### 3. LLM-Based Extraction

For complex or irregular content:

```python
extraction_strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o-mini",
    instruction="Extract key financial metrics and quarterly trends"
)
```

## Advanced Patterns

### 1. Deep Crawling

Discover and crawl links from a page:

```python
# Basic link discovery
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url)

    # Extract and process discovered links
    internal_links = result.links.get("internal", [])
    external_links = result.links.get("external", [])

    # Crawl discovered internal links
    for link in internal_links:
        if "/blog/" in link and "/tag/" not in link:  # Filter links
            sub_result = await crawler.arun(link)
            # Process sub-page

    # For advanced deep crawling, consider using URL seeding patterns
    # or custom crawl strategies (see complete-sdk-reference.md)
```

### 2. Batch & Multi-URL Processing

Efficiently crawl multiple URLs:

```python
urls = ["https://site1.com", "https://site2.com", "https://site3.com"]

async with AsyncWebCrawler() as crawler:
    # Concurrent crawling with arun_many()
    results = await crawler.arun_many(
        urls=urls,
        config=crawler_config,
        max_concurrent=5  # Control concurrency
    )

    for result in results:
        if result.success:
            print(f"✅ {result.url}: {len(result.markdown)} chars")
```

### 3. Session & Authentication

Handle login-required content:

```python
# First crawl - establish session and login
login_config = CrawlerRunConfig(
    session_id="user_session",
    js_code="""
    document.querySelector('#username').value = 'myuser';
    document.querySelector('#password').value = 'mypass';
    document.querySelector('#submit').click();
    """,
    wait_for="css:.dashboard"  # Wait for post-login element
)

await crawler.arun("https://site.com/login", config=login_config)

# Subsequent crawls - reuse session
config = CrawlerRunConfig(session_id="user_session")
await crawler.arun("https://site.com/protected-content", config=config)
```

### 4. Dynamic Content Handling

For JavaScript-heavy sites:

```python
config = CrawlerRunConfig(
    # Wait for dynamic content
    wait_for="css:.ajax-content",

    # Execute JavaScript
    js_code="""
    // Scroll to load content
    window.scrollTo(0, document.body.scrollHeight);

    // Click load more button
    document.querySelector('.load-more')?.click();
    """,

    # Note: For virtual scrolling (Twitter/Instagram-style),
    # use virtual_scroll_config parameter (see docs)

    # Extended timeout for slow loading
    page_timeout=60000
)
```

### 5. Anti-Detection & Proxies

Avoid bot detection:

```python
# Proxy configuration
browser_config = BrowserConfig(
    headless=True,
    proxy_config={
        "server": "http://proxy.server:8080",
        "username": "user",
        "password": "pass"
    }
)

# For stealth/undetected browsing, consider:
# - Rotating user agents via user_agent parameter
# - Using different viewport sizes
# - Adding delays between requests

# Rate limiting
import asyncio
for url in urls:
    result = await crawler.arun(url)
    await asyncio.sleep(2)  # Delay between requests
```

## Common Use Cases

### Documentation to Markdown
```python
# Convert entire documentation site to clean markdown
async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://docs.example.com")

    # Save as markdown for LLM consumption
    with open("docs.md", "w") as f:
        f.write(result.markdown)
```

### E-commerce Product Monitoring
```python
# Generate schema once for product pages
# Then monitor prices/availability without LLM costs
schema = load_json("product_schema.json")
products = await crawler.arun_many(product_urls,
    config=CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema)))
```

### News Aggregation
```python
# Crawl multiple news sources concurrently
news_urls = ["https://news1.com", "https://news2.com", "https://news3.com"]
results = await crawler.arun_many(news_urls, max_concurrent=5)

# Extract articles with Fit Markdown
for result in results:
    if result.success:
        # Get only relevant content
        article = result.fit_markdown
```

### Research & Data Collection
```python
# Academic paper collection with focused extraction
config = CrawlerRunConfig(
    fit_markdown=True,
    fit_markdown_options={
        "query": "machine learning transformers",
        "max_tokens": 10000
    }
)
```

## Resources

### scripts/
- **extraction_pipeline.py** - Three extraction approaches with schema generation
- **basic_crawler.py** - Simple markdown extraction with screenshots
- **batch_crawler.py** - Multi-URL concurrent processing

### references/
- **complete-sdk-reference.md** - Complete SDK documentation (23K words) with all parameters, methods, and advanced features

### Example Code Repository

The Crawl4AI repository includes extensive examples in `docs/examples/`:

#### Core Examples
- **quickstart.py** - Comprehensive starter with all basic patterns:
  - Simple crawling, JavaScript execution, CSS selectors
  - Content filtering, link analysis, media handling
  - LLM extraction, CSS extraction, dynamic content
  - Browser comparison, SSL certificates

#### Specialized Examples
- **amazon_product_extraction_*.py** - Three approaches for e-commerce scraping
- **extraction_strategies_examples.py** - All extraction strategies demonstrated
- **deepcrawl_example.py** - Advanced deep crawling patterns
- **crypto_analysis_example.py** - Complex data extraction with analysis
- **parallel_execution_example.py** - High-performance concurrent crawling
- **session_management_example.py** - Authentication and session handling
- **markdown_generation_example.py** - Advanced markdown customization
- **hooks_example.py** - Custom hooks for crawl lifecycle events
- **proxy_rotation_example.py** - Proxy management and rotation
- **router_example.py** - Request routing and URL patterns

#### Advanced Patterns
- **adaptive_crawling/** - Intelligent crawling strategies
- **c4a_script/** - C4A script examples
- **docker_*.py** - Docker deployment patterns

To explore examples:
```python
# The examples are located in your Crawl4AI installation:
# Look in: docs/examples/ directory

# Start with quickstart.py for comprehensive patterns
# It includes: simple crawl, JS execution, CSS selectors,
# content filtering, LLM extraction, dynamic pages, and more

# For specific use cases:
# - E-commerce: amazon_product_extraction_*.py
# - High performance: parallel_execution_example.py
# - Authentication: session_management_example.py
# - Deep crawling: deepcrawl_example.py

# Run any example directly:
# python docs/examples/quickstart.py
```

## Best Practices

1. **Start with basic crawling** - Understand BrowserConfig, CrawlerRunConfig, and arun() before moving to advanced features
2. **Use markdown generation** for documentation and content - Crawl4AI excels at clean markdown extraction
3. **Try schema generation first** for structured data - 10-100x more efficient than LLM extraction
4. **Enable caching during development** - `cache_mode=CacheMode.ENABLED` to avoid repeated requests
5. **Set appropriate timeouts** - 30s for normal sites, 60s+ for JavaScript-heavy sites
6. **Respect rate limits** - Use delays and `max_concurrent` parameter
7. **Reuse sessions** for authenticated content instead of re-logging

## Troubleshooting

**JavaScript not loading:**
```python
config = CrawlerRunConfig(
    wait_for="css:.dynamic-content",  # Wait for specific element
    page_timeout=60000  # Increase timeout
)
```

**Bot detection issues:**
```python
browser_config = BrowserConfig(
    headless=False,  # Sometimes visible browsing helps
    viewport_width=1920,
    viewport_height=1080,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
)
# Add delays between requests
await asyncio.sleep(random.uniform(2, 5))
```

**Content extraction problems:**
```python
# Debug what's being extracted
result = await crawler.arun(url)
print(f"HTML length: {len(result.html)}")
print(f"Markdown length: {len(result.markdown)}")
print(f"Links found: {len(result.links)}")

# Try different wait strategies
config = CrawlerRunConfig(
    wait_for="js:document.querySelector('.content') !== null"
)
```

**Session/auth issues:**
```python
# Verify session is maintained
config = CrawlerRunConfig(session_id="test_session")
result = await crawler.arun(url, config=config)
print(f"Session ID: {result.session_id}")
print(f"Cookies: {result.cookies}")
```

For more details on any topic, refer to `references/complete-sdk-reference.md` which contains comprehensive documentation of all features, parameters, and advanced usage patterns.
