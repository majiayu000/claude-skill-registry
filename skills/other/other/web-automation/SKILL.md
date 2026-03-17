---
name: web-automation
description: Web automation and scraping using Playwright, Puppeteer, Selenium, Scrapy, and n8n workflows. Create browser automation scripts, web scrapers, and workflow automations. Use when automating browser interactions, scraping websites, building crawlers, or creating no-code automations. Triggers on web scraping, browser automation, selenium, puppeteer, scrapy, crawler, n8n workflow.
---

# Web Automation

Comprehensive web automation covering browser automation, web scraping, and workflow automation tools.

## Quick Decision Guide

```
Need browser automation?
+-- Modern testing/scraping --> Playwright (recommended)
+-- Chrome-only, PDF/screenshots --> Puppeteer
+-- Legacy/cross-browser --> Selenium
+-- Serverless/API-based --> Browserless

Need data scraping?
+-- Large-scale crawling --> Scrapy
+-- Dynamic content (JS) --> Playwright
+-- Simple HTML --> BeautifulSoup

Need workflow automation?
+-- Visual workflows --> n8n
```

## Playwright (Recommended)

### Installation

```bash
npm init playwright@latest
# or
pip install playwright
playwright install
```

### Basic Example

```typescript
import { chromium } from "playwright";

async function scrape() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto("https://example.com");
  await page.waitForSelector(".content");

  const title = await page.textContent("h1");
  const links = await page.$$eval("a", (els) =>
    els.map((el) => ({ text: el.textContent, href: el.href }))
  );

  await browser.close();
  return { title, links };
}
```

### Common Patterns

```typescript
// Screenshot
await page.screenshot({ path: "screenshot.png", fullPage: true });

// PDF generation
await page.pdf({ path: "page.pdf", format: "A4" });

// Fill forms
await page.fill('input[name="email"]', "user@example.com");
await page.click('button[type="submit"]');

// Wait for navigation
await Promise.all([page.waitForNavigation(), page.click("a.next-page")]);

// Handle dialogs
page.on("dialog", (dialog) => dialog.accept());
```

## Puppeteer

### Installation

```bash
npm install puppeteer
```

### Basic Example

```javascript
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();

  await page.goto("https://example.com");
  await page.screenshot({ path: "example.png" });

  await browser.close();
})();
```

## Scrapy (Python)

### Installation

```bash
pip install scrapy
scrapy startproject myproject
```

### Spider Example

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

## Best Practices

### Rate Limiting

```typescript
// Add delays between requests
await page.waitForTimeout(1000 + Math.random() * 2000);
```

### User Agent Rotation

```typescript
const userAgents = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...",
];

await page.setUserAgent(
  userAgents[Math.floor(Math.random() * userAgents.length)]
);
```

### Error Handling

```typescript
try {
  await page.goto(url, { timeout: 30000 });
} catch (error) {
  if (error.name === "TimeoutError") {
    console.log("Page load timeout, retrying...");
    await page.goto(url, { timeout: 60000 });
  }
}
```

### Respectful Scraping

1. Check `robots.txt` before scraping
2. Add reasonable delays between requests
3. Identify your bot with a custom User-Agent
4. Cache responses to avoid repeated requests
5. Respect rate limits and Terms of Service

## When to Use This Skill

- Automating browser interactions for testing
- Scraping data from websites
- Generating PDFs or screenshots
- Building web crawlers
- Creating workflow automations
- Monitoring website changes

## Tool Comparison

| Tool | Strengths | Best For |
|------|-----------|----------|
| Playwright | Cross-browser, modern API | E2E testing, SPA scraping |
| Puppeteer | Chrome-focused, mature | PDF generation, screenshots |
| Selenium | Wide browser support | Legacy systems, cross-browser |
| Scrapy | High performance, Python | Large-scale crawling |
| Browserless | Serverless, scalable | Cloud automation |
