---
name: firecrawl-scraper
description: |
  Convert websites into LLM-ready data with Firecrawl API. Features: scrape, crawl, map, search, extract, agent (autonomous), batch operations, and change tracking. Handles JavaScript, anti-bot bypass, PDF/DOCX parsing, and branding extraction. Prevents 10 documented errors.

  Use when: scraping websites, crawling sites, web search + scrape, autonomous data gathering, monitoring content changes, extracting brand/design systems, or troubleshooting content not loading, JavaScript rendering, bot detection, v2 migration, job status errors, DNS resolution, or stealth mode pricing.
user-invocable: true
---

# Firecrawl Web Scraper Skill

**Status**: Production Ready
**Last Updated**: 2026-01-20
**Official Docs**: https://docs.firecrawl.dev
**API Version**: v2
**SDK Versions**: firecrawl-py 4.13.0+, @mendable/firecrawl-js 4.11.1+

---

## What is Firecrawl?

Firecrawl is a **Web Data API for AI** that turns websites into LLM-ready markdown or structured data. It handles:

- **JavaScript rendering** - Executes client-side JavaScript to capture dynamic content
- **Anti-bot bypass** - Gets past CAPTCHA and bot detection systems
- **Format conversion** - Outputs as markdown, HTML, JSON, screenshots, summaries
- **Document parsing** - Processes PDFs, DOCX files, and images
- **Autonomous agents** - AI-powered web data gathering without URLs
- **Change tracking** - Monitor content changes over time
- **Branding extraction** - Extract color schemes, typography, logos

---

## API Endpoints Overview

| Endpoint | Purpose | Use Case |
|----------|---------|----------|
| `/scrape` | Single page | Extract article, product page |
| `/crawl` | Full site | Index docs, archive sites |
| `/map` | URL discovery | Find all pages, plan strategy |
| `/search` | Web search + scrape | Research with live data |
| `/extract` | Structured data | Product prices, contacts |
| `/agent` | Autonomous gathering | No URLs needed, AI navigates |
| `/batch-scrape` | Multiple URLs | Bulk processing |

---

## 1. Scrape Endpoint (`/v2/scrape`)

Scrapes a single webpage and returns clean, structured content.

### Basic Usage

```python
from firecrawl import Firecrawl
import os

app = Firecrawl(api_key=os.environ.get("FIRECRAWL_API_KEY"))

# Basic scrape
doc = app.scrape(
    url="https://example.com/article",
    formats=["markdown", "html"],
    only_main_content=True
)

print(doc.markdown)
print(doc.metadata)
```

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: process.env.FIRECRAWL_API_KEY });

const result = await app.scrapeUrl('https://example.com/article', {
  formats: ['markdown', 'html'],
  onlyMainContent: true
});

console.log(result.markdown);
```

### Output Formats

| Format | Description |
|--------|-------------|
| `markdown` | LLM-optimized content |
| `html` | Full HTML |
| `rawHtml` | Unprocessed HTML |
| `screenshot` | Page capture (with viewport options) |
| `links` | All URLs on page |
| `json` | Structured data extraction |
| `summary` | AI-generated summary |
| `branding` | Design system data |
| `changeTracking` | Content change detection |

### Advanced Options

```python
doc = app.scrape(
    url="https://example.com",
    formats=["markdown", "screenshot"],
    only_main_content=True,
    remove_base64_images=True,
    wait_for=5000,  # Wait 5s for JS
    timeout=30000,
    # Location & language
    location={"country": "AU", "languages": ["en-AU"]},
    # Cache control
    max_age=0,  # Fresh content (no cache)
    store_in_cache=True,
    # Stealth mode for complex sites
    stealth=True,
    # Custom headers
    headers={"User-Agent": "Custom Bot 1.0"}
)
```

### Browser Actions

Perform interactions before scraping:

```python
doc = app.scrape(
    url="https://example.com",
    actions=[
        {"type": "click", "selector": "button.load-more"},
        {"type": "wait", "milliseconds": 2000},
        {"type": "scroll", "direction": "down"},
        {"type": "write", "selector": "input#search", "text": "query"},
        {"type": "press", "key": "Enter"},
        {"type": "screenshot"}  # Capture state mid-action
    ]
)
```

### JSON Mode (Structured Extraction)

```python
# With schema
doc = app.scrape(
    url="https://example.com/product",
    formats=["json"],
    json_options={
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "price": {"type": "number"},
                "in_stock": {"type": "boolean"}
            }
        }
    }
)

# Without schema (prompt-only)
doc = app.scrape(
    url="https://example.com/product",
    formats=["json"],
    json_options={
        "prompt": "Extract the product name, price, and availability"
    }
)
```

### Branding Extraction

Extract design system and brand identity:

```python
doc = app.scrape(
    url="https://example.com",
    formats=["branding"]
)

# Returns:
# - Color schemes and palettes
# - Typography (fonts, sizes, weights)
# - Spacing and layout metrics
# - UI component styles
# - Logo and imagery URLs
# - Brand personality traits
```

---

## 2. Crawl Endpoint (`/v2/crawl`)

Crawls all accessible pages from a starting URL.

```python
result = app.crawl(
    url="https://docs.example.com",
    limit=100,
    max_depth=3,
    allowed_domains=["docs.example.com"],
    exclude_paths=["/api/*", "/admin/*"],
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

for page in result.data:
    print(f"Scraped: {page.metadata.source_url}")
    print(f"Content: {page.markdown[:200]}...")
```

### Async Crawl with Webhooks

```python
# Start crawl (returns immediately)
job = app.start_crawl(
    url="https://docs.example.com",
    limit=1000,
    webhook="https://your-domain.com/webhook"
)

print(f"Job ID: {job.id}")

# Or poll for status
status = app.check_crawl_status(job.id)
```

---

## 3. Map Endpoint (`/v2/map`)

Rapidly discover all URLs on a website without scraping content.

```python
urls = app.map(url="https://example.com")

print(f"Found {len(urls)} pages")
for url in urls[:10]:
    print(url)
```

Use for: sitemap discovery, crawl planning, website audits.

---

## 4. Search Endpoint (`/search`) - NEW

Perform web searches and optionally scrape the results in one operation.

```python
# Basic search
results = app.search(
    query="best practices for React server components",
    limit=10
)

for result in results:
    print(f"{result.title}: {result.url}")

# Search + scrape results
results = app.search(
    query="React server components tutorial",
    limit=5,
    scrape_options={
        "formats": ["markdown"],
        "only_main_content": True
    }
)

for result in results:
    print(f"{result.title}")
    print(result.markdown[:500])
```

### Search Options

```python
results = app.search(
    query="machine learning papers",
    limit=20,
    # Filter by source type
    sources=["web", "news", "images"],
    # Filter by category
    categories=["github", "research", "pdf"],
    # Location
    location={"country": "US"},
    # Time filter
    tbs="qdr:m",  # Past month (qdr:h=hour, qdr:d=day, qdr:w=week, qdr:y=year)
    timeout=30000
)
```

**Cost**: 2 credits per 10 results + scraping costs if enabled.

---

## 5. Extract Endpoint (`/v2/extract`)

AI-powered structured data extraction from single pages, multiple pages, or entire domains.

### Single Page

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str
    in_stock: bool

result = app.extract(
    urls=["https://example.com/product"],
    schema=Product,
    system_prompt="Extract product information"
)

print(result.data)
```

### Multi-Page / Domain Extraction

```python
# Extract from entire domain using wildcard
result = app.extract(
    urls=["example.com/*"],  # All pages on domain
    schema=Product,
    system_prompt="Extract all products"
)

# Enable web search for additional context
result = app.extract(
    urls=["example.com/products"],
    schema=Product,
    enable_web_search=True  # Follow external links
)
```

### Prompt-Only Extraction (No Schema)

```python
result = app.extract(
    urls=["https://example.com/about"],
    prompt="Extract the company name, founding year, and key executives"
)
# LLM determines output structure
```

---

## 6. Agent Endpoint (`/agent`) - NEW

Autonomous web data gathering without requiring specific URLs. The agent searches, navigates, and gathers data using natural language prompts.

```python
# Basic agent usage
result = app.agent(
    prompt="Find the pricing plans for the top 3 headless CMS platforms and compare their features"
)

print(result.data)

# With schema for structured output
from pydantic import BaseModel
from typing import List

class CMSPricing(BaseModel):
    name: str
    free_tier: bool
    starter_price: float
    features: List[str]

result = app.agent(
    prompt="Find pricing for Contentful, Sanity, and Strapi",
    schema=CMSPricing
)

# Optional: focus on specific URLs
result = app.agent(
    prompt="Extract the enterprise pricing details",
    urls=["https://contentful.com/pricing", "https://sanity.io/pricing"]
)
```

### Agent Models

| Model | Best For | Cost |
|-------|----------|------|
| `spark-1-mini` (default) | Simple extractions, high volume | Standard |
| `spark-1-pro` | Complex analysis, ambiguous data | 60% more |

```python
result = app.agent(
    prompt="Analyze competitive positioning...",
    model="spark-1-pro"  # For complex tasks
)
```

### Async Agent

```python
# Start agent (returns immediately)
job = app.start_agent(
    prompt="Research market trends..."
)

# Poll for results
status = app.check_agent_status(job.id)
if status.status == "completed":
    print(status.data)
```

**Note**: Agent is in Research Preview. 5 free daily requests, then credit-based billing.

---

## 7. Batch Scrape - NEW

Process multiple URLs efficiently in a single operation.

### Synchronous (waits for completion)

```python
results = app.batch_scrape(
    urls=[
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ],
    formats=["markdown"],
    only_main_content=True
)

for page in results.data:
    print(f"{page.metadata.source_url}: {len(page.markdown)} chars")
```

### Asynchronous (with webhooks)

```python
job = app.start_batch_scrape(
    urls=url_list,
    formats=["markdown"],
    webhook="https://your-domain.com/webhook"
)

# Webhook receives events: started, page, completed, failed
```

```typescript
const job = await app.startBatchScrape(urls, {
  formats: ['markdown'],
  webhook: 'https://your-domain.com/webhook'
});

// Poll for status
const status = await app.checkBatchScrapeStatus(job.id);
```

---

## 8. Change Tracking - NEW

Monitor content changes over time by comparing scrapes.

```python
# Enable change tracking
doc = app.scrape(
    url="https://example.com/pricing",
    formats=["markdown", "changeTracking"]
)

# Response includes:
print(doc.change_tracking.status)  # new, same, changed, removed
print(doc.change_tracking.previous_scrape_at)
print(doc.change_tracking.visibility)  # visible, hidden
```

### Comparison Modes

```python
# Git-diff mode (default)
doc = app.scrape(
    url="https://example.com/docs",
    formats=["markdown", "changeTracking"],
    change_tracking_options={
        "mode": "diff"
    }
)
print(doc.change_tracking.diff)  # Line-by-line changes

# JSON mode (structured comparison)
doc = app.scrape(
    url="https://example.com/pricing",
    formats=["markdown", "changeTracking"],
    change_tracking_options={
        "mode": "json",
        "schema": {"type": "object", "properties": {"price": {"type": "number"}}}
    }
)
# Costs 5 credits per page
```

**Change States**:
- `new` - Page not seen before
- `same` - No changes since last scrape
- `changed` - Content modified
- `removed` - Page no longer accessible

---

## Authentication

```bash
# Get API key from https://www.firecrawl.dev/app
# Store in environment
FIRECRAWL_API_KEY=fc-your-api-key-here
```

**Never hardcode API keys!**

---

## Cloudflare Workers Integration

**The Firecrawl SDK cannot run in Cloudflare Workers** (requires Node.js). Use the REST API directly:

```typescript
interface Env {
  FIRECRAWL_API_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { url } = await request.json<{ url: string }>();

    const response = await fetch('https://api.firecrawl.dev/v2/scrape', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${env.FIRECRAWL_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url,
        formats: ['markdown'],
        onlyMainContent: true
      })
    });

    const result = await response.json();
    return Response.json(result);
  }
};
```

---

## Rate Limits & Pricing

### Warning: Stealth Mode Pricing Change (May 2025)

Stealth mode now costs **5 credits per request** when actively used. Default behavior uses "auto" mode which only charges stealth credits if basic fails.

**Recommended pattern**:
```python
# Use auto mode (default) - only charges 5 credits if stealth is needed
doc = app.scrape(url, formats=["markdown"])

# Or conditionally enable stealth for specific errors
if error_status_code in [401, 403, 500]:
    doc = app.scrape(url, formats=["markdown"], proxy="stealth")
```

### Unified Billing (November 2025)

Credits and tokens merged into single system. Extract endpoint uses credits (15 tokens = 1 credit).

### Pricing Tiers

| Tier | Credits/Month | Notes |
|------|---------------|-------|
| Free | 500 | Good for testing |
| Hobby | 3,000 | $19/month |
| Standard | 100,000 | $99/month |
| Growth | 500,000 | $399/month |

**Credit Costs**:
- Scrape: 1 credit (basic), 5 credits (stealth)
- Crawl: 1 credit per page
- Search: 2 credits per 10 results
- Extract: 5 credits per page (changed from tokens in v2.6.0)
- Agent: Dynamic (complexity-based)
- Change Tracking JSON mode: +5 credits

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Empty content | JS not loaded | Add `wait_for: 5000` or use `actions` |
| Rate limit exceeded | Over quota | Check dashboard, upgrade plan |
| Timeout error | Slow page | Increase `timeout`, use `stealth: true` |
| Bot detection | Anti-scraping | Use `stealth: true`, add `location` |
| Invalid API key | Wrong format | Must start with `fc-` |

---

## Known Issues Prevention

This skill prevents **10** documented issues:

### Issue #1: Stealth Mode Pricing Change (May 2025)

**Error**: Unexpected credit costs when using stealth mode
**Source**: [Stealth Mode Docs](https://docs.firecrawl.dev/features/stealth-mode) | [Changelog](https://www.firecrawl.dev/changelog)
**Why It Happens**: Starting May 8th, 2025, Stealth Mode proxy requests cost **5 credits per request** (previously included in standard pricing). This is a significant billing change.
**Prevention**: Use auto mode (default) which only charges stealth credits if basic fails

```python
# RECOMMENDED: Use auto mode (default)
doc = app.scrape(url, formats=['markdown'])
# Auto retries with stealth (5 credits) only if basic fails

# Or conditionally enable based on error status
try:
    doc = app.scrape(url, formats=['markdown'], proxy='basic')
except Exception as e:
    if e.status_code in [401, 403, 500]:
        doc = app.scrape(url, formats=['markdown'], proxy='stealth')
```

**Stealth Mode Options**:
- `auto` (default): Charges 5 credits only if stealth succeeds after basic fails
- `basic`: Standard proxies, 1 credit cost
- `stealth`: 5 credits per request when actively used

---

### Issue #2: v2.0.0 Breaking Changes - Method Renames

**Error**: `AttributeError: 'FirecrawlApp' object has no attribute 'scrape_url'`
**Source**: [v2.0.0 Release](https://github.com/firecrawl/firecrawl/releases/tag/v2.0.0) | [Migration Guide](https://docs.firecrawl.dev/migrate-to-v2)
**Why It Happens**: v2.0.0 (August 2025) renamed SDK methods across all languages
**Prevention**: Use new method names

**JavaScript/TypeScript**:
- `scrapeUrl()` → `scrape()`
- `crawlUrl()` → `crawl()` or `startCrawl()`
- `asyncCrawlUrl()` → `startCrawl()`
- `checkCrawlStatus()` → `getCrawlStatus()`

**Python**:
- `scrape_url()` → `scrape()`
- `crawl_url()` → `crawl()` or `start_crawl()`

```python
# OLD (v1)
doc = app.scrape_url("https://example.com")

# NEW (v2)
doc = app.scrape("https://example.com")
```

---

### Issue #3: v2.0.0 Breaking Changes - Format Changes

**Error**: `'extract' is not a valid format`
**Source**: [v2.0.0 Release](https://github.com/firecrawl/firecrawl/releases/tag/v2.0.0)
**Why It Happens**: Old `"extract"` format renamed to `"json"` in v2.0.0
**Prevention**: Use new object format for JSON extraction

```python
# OLD (v1)
doc = app.scrape_url(
    url="https://example.com",
    params={
        "formats": ["extract"],
        "extract": {"prompt": "Extract title"}
    }
)

# NEW (v2)
doc = app.scrape(
    url="https://example.com",
    formats=[{"type": "json", "prompt": "Extract title"}]
)

# With schema
doc = app.scrape(
    url="https://example.com",
    formats=[{
        "type": "json",
        "prompt": "Extract product info",
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "price": {"type": "number"}
            }
        }
    }]
)
```

**Screenshot format also changed**:
```python
# NEW: Screenshot as object
formats=[{
    "type": "screenshot",
    "fullPage": True,
    "quality": 80,
    "viewport": {"width": 1920, "height": 1080}
}]
```

---

### Issue #4: v2.0.0 Breaking Changes - Crawl Options

**Error**: `'allowBackwardCrawling' is not a valid parameter`
**Source**: [v2.0.0 Release](https://github.com/firecrawl/firecrawl/releases/tag/v2.0.0)
**Why It Happens**: Several crawl parameters renamed or removed in v2.0.0
**Prevention**: Use new parameter names

**Parameter Changes**:
- `allowBackwardCrawling` → Use `crawlEntireDomain` instead
- `maxDepth` → Use `maxDiscoveryDepth` instead
- `ignoreSitemap` (bool) → `sitemap` ("only", "skip", "include")

```python
# OLD (v1)
app.crawl_url(
    url="https://docs.example.com",
    params={
        "allowBackwardCrawling": True,
        "maxDepth": 3,
        "ignoreSitemap": False
    }
)

# NEW (v2)
app.crawl(
    url="https://docs.example.com",
    crawl_entire_domain=True,
    max_discovery_depth=3,
    sitemap="include"  # "only", "skip", or "include"
)
```

---

### Issue #5: v2.0.0 Default Behavior Changes

**Error**: Stale cached content returned unexpectedly
**Source**: [v2.0.0 Release](https://github.com/firecrawl/firecrawl/releases/tag/v2.0.0)
**Why It Happens**: v2.0.0 changed several defaults
**Prevention**: Be aware of new defaults

**Default Changes**:
- `maxAge` now defaults to **2 days** (cached by default)
- `blockAds`, `skipTlsVerification`, `removeBase64Images` enabled by default

```python
# Force fresh data if needed
doc = app.scrape(url, formats=['markdown'], max_age=0)

# Disable cache entirely
doc = app.scrape(url, formats=['markdown'], store_in_cache=False)
```

---

### Issue #6: Job Status Race Condition

**Error**: `"Job not found"` when checking crawl status immediately after creation
**Source**: [GitHub Issue #2662](https://github.com/firecrawl/firecrawl/issues/2662)
**Why It Happens**: Database replication delay between job creation and status endpoint availability
**Prevention**: Wait 1-3 seconds before first status check, or implement retry logic

```python
import time

# Start crawl
job = app.start_crawl(url="https://docs.example.com")
print(f"Job ID: {job.id}")

# REQUIRED: Wait before first status check
time.sleep(2)  # 1-3 seconds recommended

# Now status check succeeds
status = app.get_crawl_status(job.id)

# Or implement retry logic
def get_status_with_retry(job_id, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            return app.get_crawl_status(job_id)
        except Exception as e:
            if "Job not found" in str(e) and attempt < max_retries - 1:
                time.sleep(delay)
                continue
            raise

status = get_status_with_retry(job.id)
```

---

### Issue #7: DNS Errors Return HTTP 200

**Error**: DNS resolution failures return `success: false` with HTTP 200 status instead of 4xx
**Source**: [GitHub Issue #2402](https://github.com/firecrawl/firecrawl/issues/2402) | Fixed in v2.7.0
**Why It Happens**: Changed in v2.7.0 for consistent error handling
**Prevention**: Check `success` field and `code` field, don't rely on HTTP status alone

```typescript
const result = await app.scrape('https://nonexistent-domain-xyz.com');

// DON'T rely on HTTP status code
// Response: HTTP 200 with { success: false, code: "SCRAPE_DNS_RESOLUTION_ERROR" }

// DO check success field
if (!result.success) {
    if (result.code === 'SCRAPE_DNS_RESOLUTION_ERROR') {
        console.error('DNS resolution failed');
    }
    throw new Error(result.error);
}
```

**Note**: DNS resolution errors still charge 1 credit despite failure.

---

### Issue #8: Bot Detection Still Charges Credits

**Error**: Cloudflare error page returned as "successful" scrape, credits charged
**Source**: [GitHub Issue #2413](https://github.com/firecrawl/firecrawl/issues/2413)
**Why It Happens**: Fire-1 engine charges credits even when bot detection prevents access
**Prevention**: Validate content isn't an error page before processing; use stealth mode for protected sites

```python
# First attempt without stealth
doc = app.scrape(url="https://protected-site.com", formats=["markdown"])

# Validate content isn't an error page
if "cloudflare" in doc.markdown.lower() or "access denied" in doc.markdown.lower():
    # Retry with stealth (costs 5 credits if successful)
    doc = app.scrape(url, formats=["markdown"], stealth=True)
```

**Cost Impact**: Basic scrape charges 1 credit even on failure, stealth retry charges additional 5 credits.

---

### Issue #9: Self-Hosted Anti-Bot Fingerprinting Weakness

**Error**: `"All scraping engines failed!"` (SCRAPE_ALL_ENGINES_FAILED) on sites with anti-bot measures
**Source**: [GitHub Issue #2257](https://github.com/firecrawl/firecrawl/issues/2257)
**Why It Happens**: Self-hosted Firecrawl lacks advanced anti-fingerprinting techniques present in cloud service
**Prevention**: Use Firecrawl cloud service for sites with strong anti-bot measures, or configure proxy

```bash
# Self-hosted fails on Cloudflare-protected sites
curl -X POST 'http://localhost:3002/v2/scrape' \
-H 'Authorization: Bearer YOUR_API_KEY' \
-d '{
  "url": "https://www.example.com/",
  "pageOptions": { "engine": "playwright" }
}'
# Error: "All scraping engines failed!"

# Workaround: Use cloud service instead
# Cloud service has better anti-fingerprinting
```

**Note**: This affects self-hosted v2.3.0+ with default docker-compose setup. Warning present: "⚠️ WARNING: No proxy server provided. Your IP address may be blocked."

---

### Issue #10: Cache Performance Best Practices (Community-sourced)

**Suboptimal**: Not leveraging cache can make requests 500% slower
**Source**: [Fast Scraping Docs](https://docs.firecrawl.dev/features/fast-scraping) | [Blog Post](https://www.firecrawl.dev/blog/mastering-firecrawl-scrape-endpoint)
**Why It Matters**: Default `maxAge` is 2 days in v2+, but many use cases need different strategies
**Prevention**: Use appropriate cache strategy for your content type

```python
# Fresh data (real-time pricing, stock prices)
doc = app.scrape(url, formats=["markdown"], max_age=0)

# 10-minute cache (news, blogs)
doc = app.scrape(url, formats=["markdown"], max_age=600000)  # milliseconds

# Use default cache (2 days) for static content
doc = app.scrape(url, formats=["markdown"])  # maxAge defaults to 172800000

# Don't store in cache (one-time scrape)
doc = app.scrape(url, formats=["markdown"], store_in_cache=False)

# Require minimum age before re-scraping (v2.7.0+)
doc = app.scrape(url, formats=["markdown"], min_age=3600000)  # 1 hour minimum
```

**Performance Impact**:
- Cached response: Milliseconds
- Fresh scrape: Seconds
- Speed difference: **Up to 500%**

---

## Package Versions

| Package | Version | Last Checked |
|---------|---------|--------------|
| firecrawl-py | 4.13.0+ | 2026-01-20 |
| @mendable/firecrawl-js | 4.11.1+ | 2026-01-20 |
| API Version | v2 | Current |

---

## Official Documentation

- **Docs**: https://docs.firecrawl.dev
- **Python SDK**: https://docs.firecrawl.dev/sdks/python
- **Node.js SDK**: https://docs.firecrawl.dev/sdks/node
- **API Reference**: https://docs.firecrawl.dev/api-reference
- **GitHub**: https://github.com/mendableai/firecrawl
- **Dashboard**: https://www.firecrawl.dev/app

---

**Token Savings**: ~65% vs manual integration
**Error Prevention**: 10 documented issues (v2 migration, stealth pricing, job status race, DNS errors, bot detection billing, self-hosted limitations, cache optimization)
**Production Ready**: Yes
**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added Known Issues Prevention section with 10 documented errors from TIER 1-2 research findings; added v2 migration guidance; documented stealth mode pricing change and unified billing model
