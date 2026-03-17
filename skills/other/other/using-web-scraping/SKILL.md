---
name: using-web-scraping
description: Search and scrape public web content with headless Chrome and DuckDuckGo using safe practices.
---

# Web Scraping Skill — Chrome (Playwright) + DuckDuckGo

A privacy-minded, agent-facing web-scraping skill that uses headless Chrome (Playwright/Puppeteer) and DuckDuckGo for search. Focuses on: reliable navigation, extracting structured text, obeying robots.txt, and rate-limiting.

## When to use
- Collect public webpage content for summarization, metadata extraction, or link discovery.
- Use DuckDuckGo for queries when you want a privacy-respecting search source.
- NOT for bypassing paywalls, scraping private/logged-in content, or violating Terms of Service.

## Safety & etiquette
- Always check and respect `/robots.txt` before scraping a site.
- Rate-limit requests (default: 1 request/sec) and use polite `User-Agent` strings.
- Avoid executing arbitrary user-provided JavaScript on scraped pages.
- Only scrape public content; if login is required, return `login_required` instead of attempting to bypass.

## Capabilities
- Search DuckDuckGo and return top-N result links.
- Visit result pages in headless Chrome and extract `title`, `meta description`, `main` text (or best-effort article text), and `canonical` URL.
- Return results as structured JSON for downstream consumption.

## Examples
### Node.js (Playwright)
```javascript
const { chromium } = require('playwright');

async function ddgSearchAndScrape(query) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ userAgent: 'open-skills-bot/1.0' });

  // DuckDuckGo search
  await page.goto('https://duckduckgo.com/');
  await page.fill('input[name="q"]', query);
  await page.keyboard.press('Enter');
  await page.waitForSelector('.result__title a');

  // collect top result URL
  const href = await page.getAttribute('.result__title a', 'href');
  if (!href) { await browser.close(); return []; }

  // visit result and extract
  await page.goto(href, { waitUntil: 'domcontentloaded' });
  const title = await page.title();
  const description = await page.locator('meta[name="description"]').getAttribute('content').catch(() => null);
  const article = await page.locator('article, main, #content').first().innerText().catch(() => null);

  await browser.close();
  return [{ url: href, title, description, text: article }];
}

// usage
// ddgSearchAndScrape('open-source agent runtimes').then(console.log);
```

## Agent prompt (copy/paste)
```text
You are an agent with a web-scraping skill. For any `search:` task, use DuckDuckGo to find relevant pages, then open each page in a headless Chrome instance (Playwright/Puppeteer) and extract `title`, `meta description`, `main text`, and `canonical` URL. Always:
- Check and respect robots.txt
- Rate-limit requests (<=1 req/sec)
- Use a clear `User-Agent` and do not execute arbitrary page JS
Return results as JSON: [{url,title,description,text}] or `login_required` if a page needs authentication.
```

## Quick setup
- Node: `npm i playwright` and run `npx playwright install` for browser binaries.
- Python: `pip install playwright` and `playwright install`.

## Tips
- Use `page.route` to block large assets (images, fonts) when you only need text.
- Respect site terms and introduce exponential backoff for retries.

## See also
- [using-youtube-download.md](using-youtube-download.md) — media-specific scraping and download examples.
