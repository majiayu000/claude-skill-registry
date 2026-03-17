---
name: Web Scraping
description: Extract structured data from websites using Playwright browser automation
triggers:
  - "scrape"
  - "extract data from"
  - "crawl website"
  - "get data from"
  - "fetch content from"
---

# Web Scraping Skill

Extract structured data from websites using Playwright MCP for browser automation and dynamic content handling.

## Capabilities

- Dynamic page scraping (JavaScript-rendered content)
- Form submission and interaction
- Multi-page crawling
- Screenshot capture
- PDF generation from pages
- Authentication handling (where ethical)

## MCP Integration

Uses: `@modelcontextprotocol/server-puppeteer` (if available)

Fallback: Manual Playwright scripts

## Use Cases

### Data Collection
```bash
"scrape top 100 prompts from prompthero.com
 Extract: prompt text, category, likes, model used
 Save to: temp/scraped-data/prompts-{timestamp}.json"
```

### Competitive Intelligence
```bash
"scrape competitor pricing pages:
 - example.com/pricing
 - competitor2.com/pricing
 Extract: plans, features, prices
 Compare with our roadmap
 Save: temp/research/competitive-pricing.json"
```

### Design Inspiration
```bash
"scrape these design showcase sites:
 - awwwards.com (top 10 sites this month)
 - dribbble.com (top UI designs)
 Take full-page screenshots
 Save to: temp/design-inspiration/"
```

### Documentation Extraction
```bash
"scrape LangGraph documentation
 Extract all code examples for supervisor pattern
 Save to: temp/research/langgraph-examples.md"
```

## Output Formats

### Structured Data (JSON)
```json
{
  "source": "https://example.com",
  "scraped_at": "2025-12-31T10:00:00Z",
  "data": [
    {
      "title": "...",
      "content": "...",
      "metadata": {}
    }
  ]
}
```

### Screenshots
- Location: `temp/screenshots/{site}-{timestamp}.png`
- Format: PNG, 1920x1080
- Options: Full page or viewport

## Ethical Guidelines

**MUST FOLLOW**:
- ✅ Respect robots.txt
- ✅ Rate limit: Max 1 request per second
- ✅ Only scrape public data
- ✅ Attribute sources
- ✅ Check Terms of Service

**NEVER**:
- ❌ Bypass authentication without permission
- ❌ Solve CAPTCHAs automatically
- ❌ Scrape personal/private data
- ❌ Overload servers (DDoS)
- ❌ Violate copyright

## Usage Examples

### Basic Scraping
```bash
"Using Playwright MCP, scrape https://example.com/blog
 Extract all article titles and URLs
 Save to temp/scraped-articles.json"
```

### Interactive Scraping
```bash
"Using Playwright MCP:
 1. Navigate to https://example.com/search
 2. Enter query: 'machine learning'
 3. Click search button
 4. Wait for results to load
 5. Extract first 20 results
 6. Save to temp/search-results.json"
```

### Multi-Page Crawling
```bash
"Using Playwright MCP, crawl paginated list:
 Start: https://example.com/items?page=1
 Extract: item name, price, description
 Continue: until no 'Next' button or max 100 pages
 Save: temp/items-catalog.json"
```

### Screenshot Collection
```bash
"Using Playwright MCP, take screenshots:
 Sites: shadcn.com, ui.aceternity.com, magicui.design
 Type: Full-page screenshots
 Save: temp/design-inspiration/{site-name}.png"
```

## Best Practices

1. **Always check robots.txt first**
2. **Use user-agent string** identifying yourself
3. **Respect rate limits** (1 req/sec default)
4. **Cache results** to avoid re-scraping
5. **Handle errors gracefully** (404, timeout, etc.)
6. **Validate data** before saving

---

**Remember**: Scrape responsibly. Respect website owners and terms of service!
