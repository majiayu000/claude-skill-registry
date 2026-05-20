---
name: firecrawl-scraping
description: Web page and website scraping with Firecrawl API. Use this skill when scraping web articles, blog posts, documentation pages, paywalled content, or JavaScript-heavy sites. Triggers on requests to scrape websites, extract article content, convert pages to markdown, or handle anti-bot protection.
---

# Firecrawl Scraping

## Overview

Scrape individual web pages and convert them to clean, LLM-ready markdown. Handles JavaScript rendering, anti-bot protection, and dynamic content.

## Quick Decision Tree

```
What are you scraping?
│
├── Single page (article, blog, docs)
│   └── references/single-page.md
│   └── Script: scripts/firecrawl_scrape.py
│
└── Entire website (multiple pages, crawling)
    └── references/website-crawler.md
    └── (Use Apify Website Content Crawler for multi-page)
```

## Environment Setup

```bash
# Required in .env
FIRECRAWL_API_KEY=fc-your-api-key-here
```

Get your API key: https://firecrawl.dev/app/api-keys

## Common Usage

### Simple Scrape
```bash
python scripts/firecrawl_scrape.py "https://example.com/article"
```

### With Options
```bash
python scripts/firecrawl_scrape.py "https://wsj.com/article" \
  --proxy stealth \
  --format markdown summary \
  --timeout 60000
```

## Proxy Modes

| Mode | Use Case |
|------|----------|
| `basic` | Standard sites, fastest |
| `stealth` | Anti-bot protection, premium content (WSJ, NYT) |
| `auto` | Let Firecrawl decide (recommended) |

## Output Formats

- `markdown` - Clean markdown content (default)
- `html` - Raw HTML
- `summary` - AI-generated summary
- `screenshot` - Page screenshot
- `links` - All links on page

## Cost

~1 credit per page. Stealth proxy may use additional credits.

## Security Notes

### Credential Handling
- Store `FIRECRAWL_API_KEY` in `.env` file (never commit to git)
- API keys can be regenerated at https://firecrawl.dev/app/api-keys
- Never log or print API keys in script output
- Use environment variables, not hardcoded values

### Data Privacy
- Only scrapes publicly accessible web pages
- Scraped content is processed by Firecrawl servers temporarily
- Markdown output stored locally in `.tmp/` directory
- Screenshots (if requested) are stored locally
- No persistent data retention by Firecrawl after request

### Access Scopes
- API key provides full access to scraping features
- No granular permission scopes available
- Monitor usage via Firecrawl dashboard

### Compliance Considerations
- **Robots.txt**: Firecrawl respects robots.txt by default
- **Public Content Only**: Only scrape publicly accessible pages
- **Terms of Service**: Respect target site ToS
- **Rate Limiting**: Built-in rate limiting prevents abuse
- **Stealth Proxy**: Use stealth mode only when necessary (paywalled news, not auth bypass)
- **GDPR**: Scraped content may contain PII - handle accordingly
- **Copyright**: Respect intellectual property rights of scraped content

## Troubleshooting

### Common Issues

#### Issue: Credits exhausted
**Symptoms:** API returns "insufficient credits" or quota exceeded error
**Cause:** Account credits depleted
**Solution:**
- Check credit balance at https://firecrawl.dev/app
- Upgrade plan or purchase additional credits
- Reduce scraping frequency
- Use `basic` proxy mode to conserve credits

#### Issue: Page not rendering correctly
**Symptoms:** Empty content or partial HTML returned
**Cause:** JavaScript-heavy page not fully loading
**Solution:**
- Enable JavaScript rendering with `--js-render` flag
- Increase timeout with `--timeout 60000` (60 seconds)
- Try `stealth` proxy mode for protected sites
- Wait for specific elements with `--wait-for` selector

#### Issue: 403 Forbidden error
**Symptoms:** Script returns 403 status code
**Cause:** Site blocking automated access
**Solution:**
- Enable `stealth` proxy mode
- Add delay between requests
- Try at different times (some sites rate limit by time)
- Check if site requires login (not supported)

#### Issue: Empty markdown output
**Symptoms:** Scrape succeeds but markdown is empty or malformed
**Cause:** Dynamic content loaded after page load, or unusual page structure
**Solution:**
- Increase wait time for JavaScript to execute
- Use `--wait-for` to wait for specific content
- Try `html` format to see raw content
- Check if content is in an iframe (not always supported)

#### Issue: Timeout errors
**Symptoms:** Request times out before completion
**Cause:** Slow page load or large page content
**Solution:**
- Increase timeout value (up to 120000ms)
- Use `basic` proxy for faster response
- Target specific page sections if possible
- Check if site is experiencing issues

## Resources

- **references/single-page.md** - Single page scraping details
- **references/website-crawler.md** - Multi-page website crawling

## Integration Patterns

### Scrape and Analyze
**Skills:** firecrawl-scraping → parallel-research
**Use case:** Scrape competitor pages, then analyze content strategy
**Flow:**
1. Scrape competitor website pages with Firecrawl
2. Convert to clean markdown
3. Use parallel-research to analyze positioning, messaging, features

### Scrape and Document
**Skills:** firecrawl-scraping → content-generation
**Use case:** Create summary documents from web research
**Flow:**
1. Scrape multiple article pages on a topic
2. Combine markdown content
3. Generate summary document via content-generation

### Scrape and Enrich CRM
**Skills:** firecrawl-scraping → attio-crm
**Use case:** Enrich company records with website data
**Flow:**
1. Scrape company website (about page, team page, product pages)
2. Extract key information (funding, team size, products)
3. Update company record in Attio CRM with enriched data
