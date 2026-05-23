---
name: firecrawl-scraper
description: |
  Complete knowledge domain for Firecrawl v2 API - web scraping and crawling that converts websites into LLM-ready markdown or structured data.

  Use when: scraping websites, crawling entire sites, extracting web content, converting HTML to markdown, building web scrapers, handling dynamic JavaScript content, bypassing anti-bot protection, extracting structured data from web pages, or when encountering "content not loading", "JavaScript rendering issues", or "blocked by bot detection".

  Keywords: firecrawl, firecrawl api, web scraping, web crawler, scrape website, crawl website, extract content, html to markdown, site crawler, content extraction, web automation, firecrawl-py, firecrawl-js, llm ready data, structured data extraction, bot bypass, javascript rendering, scraping api, crawling api, map urls, batch scraping
license: MIT
---

# Firecrawl Web Scraper Skill

**Status**: Production Ready ✅
**Last Updated**: 2025-10-24
**Official Docs**: https://docs.firecrawl.dev
**API Version**: v2

---

## What is Firecrawl?

Firecrawl is a **Web Data API for AI** that turns entire websites into LLM-ready markdown or structured data. It handles:

- **JavaScript rendering** - Executes client-side JavaScript to capture dynamic content
- **Anti-bot bypass** - Gets past CAPTCHA and bot detection systems
- **Format conversion** - Outputs as markdown, JSON, or structured data
- **Screenshot capture** - Saves visual representations of pages
- **Browser automation** - Full headless browser capabilities

---

## API Endpoints

### 1. `/v2/scrape` - Single Page Scraping
Scrapes a single webpage and returns clean, structured content.

**Use Cases**:
- Extract article content
- Get product details
- Scrape specific pages
- Convert HTML to markdown

**Key Options**:
- `formats`: ["markdown", "html", "screenshot"]
- `onlyMainContent`: true/false (removes nav, footer, ads)
- `waitFor`: milliseconds to wait before scraping
- `actions`: browser automation actions (click, scroll, etc.)

### 2. `/v2/crawl` - Full Site Crawling
Crawls all accessible pages from a starting URL.

**Use Cases**:
- Index entire documentation sites
- Archive website content
- Build knowledge bases
- Scrape multi-page content

**Key Options**:
- `limit`: max pages to crawl
- `maxDepth`: how many links deep to follow
- `allowedDomains`: restrict to specific domains
- `excludePaths`: skip certain URL patterns

### 3. `/v2/map` - URL Discovery
Maps all URLs on a website without scraping content.

**Use Cases**:
- Find sitemap
- Discover all pages
- Plan crawling strategy
- Audit website structure

### 4. `/v2/extract` - Structured Data Extraction
Uses AI to extract specific data fields from pages.

**Use Cases**:
- Extract product prices and names
- Parse contact information
- Build structured datasets
- Custom data schemas

**Key Options**:
- `schema`: Zod or JSON schema defining desired structure
- `systemPrompt`: guide AI extraction behavior

---

## Authentication

Firecrawl requires an API key for all requests.

### Get API Key
1. Sign up at https://www.firecrawl.dev
2. Go to dashboard → API Keys
3. Copy your API key (starts with `fc-`)

### Store Securely
**NEVER hardcode API keys in code!**

```bash
# .env file
FIRECRAWL_API_KEY=fc-your-api-key-here
```

```bash
# .env.local (for local development)
FIRECRAWL_API_KEY=fc-your-api-key-here
```

---

## Python SDK Usage

### Installation

```bash
pip install firecrawl-py
```

**Latest Version**: `firecrawl-py v4.5.0+`

### Basic Scrape

```python
import os
from firecrawl import FirecrawlApp

# Initialize client
app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

# Scrape a single page
result = app.scrape_url(
    url="https://example.com/article",
    params={
        "formats": ["markdown", "html"],
        "onlyMainContent": True
    }
)

# Access markdown content
markdown = result.get("markdown")
print(markdown)
```

### Crawl Multiple Pages

```python
import os
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

# Start crawl
crawl_result = app.crawl_url(
    url="https://docs.example.com",
    params={
        "limit": 100,
        "scrapeOptions": {
            "formats": ["markdown"]
        }
    },
    poll_interval=5  # Check status every 5 seconds
)

# Process results
for page in crawl_result.get("data", []):
    url = page.get("url")
    markdown = page.get("markdown")
    print(f"Scraped: {url}")
```

### Extract Structured Data

```python
import os
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

# Define schema
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "product_price": {"type": "number"},
        "availability": {"type": "string"}
    },
    "required": ["company_name", "product_price"]
}

# Extract data
result = app.extract(
    urls=["https://example.com/product"],
    params={
        "schema": schema,
        "systemPrompt": "Extract product information from the page"
    }
)

print(result)
```

---

## TypeScript/Node.js SDK Usage

### Installation

```bash
npm install @mendable/firecrawl-js
# or
pnpm add @mendable/firecrawl-js
# or use the unscoped package:
npm install firecrawl
```

**Latest Version**: `@mendable/firecrawl-js v4.4.1+` (or `firecrawl v4.4.1+`)

### Basic Scrape

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

// Initialize client
const app = new FirecrawlApp({
  apiKey: process.env.FIRECRAWL_API_KEY
});

// Scrape a single page
const result = await app.scrapeUrl('https://example.com/article', {
  formats: ['markdown', 'html'],
  onlyMainContent: true
});

// Access markdown content
const markdown = result.markdown;
console.log(markdown);
```

### Crawl Multiple Pages

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({
  apiKey: process.env.FIRECRAWL_API_KEY
});

// Start crawl
const crawlResult = await app.crawlUrl('https://docs.example.com', {
  limit: 100,
  scrapeOptions: {
    formats: ['markdown']
  }
});

// Process results
for (const page of crawlResult.data) {
  console.log(`Scraped: ${page.url}`);
  console.log(page.markdown);
}
```

### Extract Structured Data with Zod

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';
import { z } from 'zod';

const app = new FirecrawlApp({
  apiKey: process.env.FIRECRAWL_API_KEY
});

// Define schema with Zod
const schema = z.object({
  company_name: z.string(),
  product_price: z.number(),
  availability: z.string()
});

// Extract data
const result = await app.extract({
  urls: ['https://example.com/product'],
  schema: schema,
  systemPrompt: 'Extract product information from the page'
});

console.log(result);
```

---

## Common Use Cases

### 1. Documentation Scraping

**Scenario**: Convert entire documentation site to markdown for RAG/chatbot

```python
app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

docs = app.crawl_url(
    url="https://docs.myapi.com",
    params={
        "limit": 500,
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True
        },
        "allowedDomains": ["docs.myapi.com"]
    }
)

# Save to files
for page in docs.get("data", []):
    filename = page["url"].replace("https://", "").replace("/", "_") + ".md"
    with open(f"docs/{filename}", "w") as f:
        f.write(page["markdown"])
```

### 2. Product Data Extraction

**Scenario**: Extract structured product data for e-commerce

```typescript
const schema = z.object({
  title: z.string(),
  price: z.number(),
  description: z.string(),
  images: z.array(z.string()),
  in_stock: z.boolean()
});

const products = await app.extract({
  urls: productUrls,
  schema: schema,
  systemPrompt: 'Extract all product details including price and availability'
});
```

### 3. News Article Scraping

**Scenario**: Extract clean article content without ads/navigation

```python
article = app.scrape_url(
    url="https://news.com/article",
    params={
        "formats": ["markdown"],
        "onlyMainContent": True,
        "removeBase64Images": True
    }
)

# Get clean markdown
content = article.get("markdown")
```

---

## Error Handling

### Python

```python
from firecrawl import FirecrawlApp
from firecrawl.exceptions import FirecrawlException

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))

try:
    result = app.scrape_url("https://example.com")
except FirecrawlException as e:
    print(f"Firecrawl error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### TypeScript

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({
  apiKey: process.env.FIRECRAWL_API_KEY
});

try {
  const result = await app.scrapeUrl('https://example.com');
} catch (error) {
  if (error.response) {
    // API error
    console.error('API Error:', error.response.data);
  } else {
    // Network or other error
    console.error('Error:', error.message);
  }
}
```

---

## Rate Limits & Best Practices

### Rate Limits
- **Free tier**: 500 credits/month
- **Paid tiers**: Higher limits based on plan
- Credits consumed vary by endpoint and options

### Best Practices

1. **Use `onlyMainContent: true`** to reduce credits and get cleaner data
2. **Set reasonable limits** on crawls to avoid excessive costs
3. **Handle retries** with exponential backoff for transient errors
4. **Cache results** locally to avoid re-scraping same content
5. **Use `map` endpoint first** to plan crawling strategy
6. **Batch extract calls** when processing multiple URLs
7. **Monitor credit usage** in dashboard

---

## Cloudflare Workers Integration

### ⚠️ Important: SDK Compatibility

**The Firecrawl SDK cannot run in Cloudflare Workers** due to Node.js dependencies (specifically `axios` which uses Node.js `http` module). Workers require Web Standard APIs.

**✅ Use the direct REST API with `fetch` instead** (see example below).

**Alternative**: Self-host with [workers-firecrawl](https://github.com/G4brym/workers-firecrawl) - a Workers-native implementation (requires Workers Paid Plan, only implements `/search` endpoint).

---

### Workers Example: Direct REST API

This example uses the `fetch` API to call Firecrawl directly - works perfectly in Cloudflare Workers:

```typescript
interface Env {
  FIRECRAWL_API_KEY: string;
  SCRAPED_CACHE?: KVNamespace; // Optional: for caching results
}

interface FirecrawlScrapeResponse {
  success: boolean;
  data: {
    markdown?: string;
    html?: string;
    metadata: {
      title?: string;
      description?: string;
      language?: string;
      sourceURL: string;
    };
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== 'POST') {
      return Response.json({ error: 'Method not allowed' }, { status: 405 });
    }

    try {
      const { url } = await request.json<{ url: string }>();

      if (!url) {
        return Response.json({ error: 'URL is required' }, { status: 400 });
      }

      // Check cache (optional)
      if (env.SCRAPED_CACHE) {
        const cached = await env.SCRAPED_CACHE.get(url, 'json');
        if (cached) {
          return Response.json({ cached: true, data: cached });
        }
      }

      // Call Firecrawl API directly using fetch
      const response = await fetch('https://api.firecrawl.dev/v2/scrape', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${env.FIRECRAWL_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          formats: ['markdown'],
          onlyMainContent: true,
          removeBase64Images: true
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Firecrawl API error (${response.status}): ${errorText}`);
      }

      const result = await response.json<FirecrawlScrapeResponse>();

      // Cache for 1 hour (optional)
      if (env.SCRAPED_CACHE && result.success) {
        await env.SCRAPED_CACHE.put(
          url,
          JSON.stringify(result.data),
          { expirationTtl: 3600 }
        );
      }

      return Response.json({
        cached: false,
        data: result.data
      });

    } catch (error) {
      console.error('Scraping error:', error);
      return Response.json(
        { error: error instanceof Error ? error.message : 'Unknown error' },
        { status: 500 }
      );
    }
  }
};
```

**Environment Setup**: Add `FIRECRAWL_API_KEY` in Wrangler secrets:

```bash
npx wrangler secret put FIRECRAWL_API_KEY
```

**Optional KV Binding** (for caching - add to `wrangler.jsonc`):

```jsonc
{
  "kv_namespaces": [
    {
      "binding": "SCRAPED_CACHE",
      "id": "your-kv-namespace-id"
    }
  ]
}
```

See `templates/firecrawl-worker-fetch.ts` for a complete production-ready example.

---

## When to Use This Skill

✅ **Use Firecrawl when:**
- Scraping modern websites with JavaScript
- Need clean markdown output for LLMs
- Building RAG systems from web content
- Extracting structured data at scale
- Dealing with bot protection
- Need reliable, production-ready scraping

❌ **Don't use Firecrawl when:**
- Scraping simple static HTML (use cheerio/beautifulsoup)
- Have existing Puppeteer/Playwright setup working well
- Working with APIs (use direct API calls instead)
- Budget constraints (free tier has limits)

---

## Common Issues & Solutions

### Issue: "Invalid API Key"
**Cause**: API key not set or incorrect
**Fix**:
```bash
# Check env variable is set
echo $FIRECRAWL_API_KEY

# Verify key format (should start with fc-)
```

### Issue: "Rate limit exceeded"
**Cause**: Exceeded monthly credits
**Fix**:
- Check usage in dashboard
- Upgrade plan or wait for reset
- Use `onlyMainContent: true` to reduce credits

### Issue: "Timeout error"
**Cause**: Page takes too long to load
**Fix**:
```python
result = app.scrape_url(url, params={"waitFor": 10000})  # Wait 10s
```

### Issue: "Content is empty"
**Cause**: Content loaded via JavaScript after initial render
**Fix**:
```python
result = app.scrape_url(url, params={
    "waitFor": 5000,
    "actions": [{"type": "wait", "milliseconds": 3000}]
})
```

---

## Advanced Features

### Browser Actions

Perform interactions before scraping:

```python
result = app.scrape_url(
    url="https://example.com",
    params={
        "actions": [
            {"type": "click", "selector": "button.load-more"},
            {"type": "wait", "milliseconds": 2000},
            {"type": "scroll", "direction": "down"}
        ]
    }
)
```

### Custom Headers

```python
result = app.scrape_url(
    url="https://example.com",
    params={
        "headers": {
            "User-Agent": "Custom Bot 1.0",
            "Accept-Language": "en-US"
        }
    }
)
```

### Webhooks for Long Crawls

Instead of polling, receive results via webhook:

```python
crawl = app.crawl_url(
    url="https://docs.example.com",
    params={
        "limit": 1000,
        "webhook": "https://your-domain.com/webhook"
    }
)
```

---

## Package Versions

| Package | Version | Last Checked |
|---------|---------|--------------|
| firecrawl-py | 4.5.0+ | 2025-10-20 |
| @mendable/firecrawl-js (or firecrawl) | 4.4.1+ | 2025-10-24 |
| API Version | v2 | Current |

**Note**: The Node.js SDK requires Node.js >=22.0.0 and cannot run in Cloudflare Workers. Use direct REST API calls in Workers (see Cloudflare Workers Integration section).

---

## Official Documentation

- **Docs**: https://docs.firecrawl.dev
- **Python SDK**: https://docs.firecrawl.dev/sdks/python
- **Node.js SDK**: https://docs.firecrawl.dev/sdks/node
- **API Reference**: https://docs.firecrawl.dev/api-reference
- **GitHub**: https://github.com/mendableai/firecrawl
- **Dashboard**: https://www.firecrawl.dev/app

---

## Next Steps After Using This Skill

1. **Store scraped data**: Use Cloudflare D1, R2, or KV to persist results
2. **Build RAG system**: Combine with Vectorize for semantic search
3. **Add scheduling**: Use Cloudflare Queues for recurring scrapes
4. **Process content**: Use Workers AI to analyze scraped data

---

**Token Savings**: ~60% vs manual integration
**Error Prevention**: API authentication, rate limiting, format handling
**Production Ready**: ✅
