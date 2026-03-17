---
name: firecrawl-scraper
description: Firecrawl v2.5 API for web scraping/crawling to LLM-ready markdown. Use for site extraction, dynamic content, or encountering JavaScript rendering, bot detection, content loading errors.

  Keywords: firecrawl, firecrawl api, web scraping, web crawler, scrape website, crawl website, extract content, html to markdown, site crawler, content extraction, web automation, firecrawl-py, firecrawl-js, llm ready data, structured data extraction, bot bypass, javascript rendering, scraping api, crawling api, map urls, batch scraping
license: MIT
---

# Firecrawl Web Scraper Skill

**Status**: Production Ready ✅
**Last Updated**: 2025-11-21
**Official Docs**: https://docs.firecrawl.dev
**API Version**: v2.5

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

## SDK Quick Start

### Python

```bash
pip install firecrawl-py  # v4.5.0+
```

```python
from firecrawl import FirecrawlApp
import os

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))
result = app.scrape_url("https://example.com", params={"formats": ["markdown"], "onlyMainContent": True})
print(result.get("markdown"))
```

### TypeScript/Node.js

```bash
bun add @mendable/firecrawl-js  # v4.4.1+
```

```typescript
import FirecrawlApp from '@mendable/firecrawl-js';

const app = new FirecrawlApp({ apiKey: process.env.FIRECRAWL_API_KEY });
const result = await app.scrapeUrl('https://example.com', { formats: ['markdown'], onlyMainContent: true });
console.log(result.markdown);
```

**See**: `templates/` for crawl, extract, and advanced examples

---

## Common Use Cases

| Use Case | Endpoint | Key Options |
|----------|----------|-------------|
| Documentation scraping | `crawl_url()` | `limit: 500`, `allowedDomains` |
| Product data extraction | `extract()` | Zod schema + `systemPrompt` |
| News article scraping | `scrape_url()` | `onlyMainContent: true`, `removeBase64Images` |
| URL discovery | `map()` | Find all pages before crawling |

**See**: `references/common-patterns.md` for complete examples.

---

## Error Handling

```python
# Python
try:
    result = app.scrape_url("https://example.com")
except FirecrawlException as e:
    print(f"Firecrawl error: {e}")
```

```typescript
// TypeScript
try {
  const result = await app.scrapeUrl('https://example.com');
} catch (error) {
  console.error('Error:', error.message);
}
```

---

## Rate Limits & Best Practices

| Best Practice | Why |
|---------------|-----|
| Use `onlyMainContent: true` | Reduces credits, cleaner output |
| Set reasonable `limit` | Avoid excessive costs |
| Use `map` endpoint first | Plan crawling strategy |
| Cache results | Avoid re-scraping |
| Batch extract calls | More efficient for multiple URLs |

**Credits**: Free tier = 500/month, paid tiers higher.

---

## Cloudflare Workers Integration

⚠️ **SDK cannot run in Workers** (Node.js dependencies). Use direct REST API:

```typescript
const response = await fetch('https://api.firecrawl.dev/v2/scrape', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.FIRECRAWL_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ url, formats: ['markdown'], onlyMainContent: true })
});
```

**See**: `references/common-patterns.md` for complete Workers example with caching.

---

## When to Use This Skill

| ✅ Use Firecrawl | ❌ Don't Use |
|------------------|--------------|
| Modern JS-rendered sites | Simple static HTML (use cheerio) |
| Clean markdown for LLMs | Existing Puppeteer setup works |
| RAG/chatbot content | Direct API available |
| Structured data extraction | Budget constraints |
| Bot protection bypass | |

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "Invalid API Key" | Key not set | Check `$FIRECRAWL_API_KEY` starts with `fc-` |
| "Rate limit exceeded" | Monthly credits used | Check dashboard, upgrade plan |
| "Timeout error" | Page slow to load | Add `waitFor: 10000` |
| "Content is empty" | JS loads late | Add `actions: [{type: "wait", milliseconds: 3000}]` |

---

## Advanced Features

| Feature | Usage |
|---------|-------|
| **Browser actions** | `actions: [{type: "click", selector: "button"}]` |
| **Custom headers** | `headers: {"User-Agent": "Custom Bot"}` |
| **Webhooks** | `webhook: "https://your-domain.com/webhook"` |
| **Screenshots** | `formats: ["screenshot"]` |

**See**: `references/endpoints.md` for complete API reference.

---

## When to Load References

| Reference | Load When... |
|-----------|--------------|
| `endpoints.md` | Need complete API endpoint documentation |
| `common-patterns.md` | Cloudflare Workers, caching, batch processing, error handling |

---

## Package Versions

| Package | Version |
|---------|---------|
| firecrawl-py | 4.5.0+ |
| @mendable/firecrawl-js | 4.4.1+ |
| API | v2 |

**Note**: Node.js SDK requires Node.js >=22.0.0, cannot run in Workers.

---

**Official Docs**: https://docs.firecrawl.dev | **GitHub**: https://github.com/mendableai/firecrawl

**Token Savings**: ~60% | **Production Ready**: ✅
