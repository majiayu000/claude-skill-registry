---
name: cloudflare-browser-rendering
description: Cloudflare Browser Rendering with Puppeteer/Playwright. Use for screenshots, PDFs, web scraping, or encountering rendering errors, timeout issues, memory exceeded.

  Keywords: browser rendering cloudflare, @cloudflare/puppeteer, @cloudflare/playwright,
  puppeteer workers, playwright workers, screenshot cloudflare, pdf generation workers,
  web scraping cloudflare, headless chrome workers, browser automation, puppeteer.launch,
  playwright.chromium.launch, browser binding, session management, puppeteer.sessions,
  puppeteer.connect, browser.close, browser.disconnect, XPath not supported, browser timeout,
  concurrency limit, keep_alive, page.screenshot, page.pdf, page.goto, page.evaluate,
  incognito context, session reuse, batch scraping, crawling websites
license: MIT
metadata:
  version: "1.0.0"
  last_verified: "2025-11-27"
  puppeteer_version: "1.0.4"
  playwright_version: "1.0.0"
  workers_types_version: "4.20251125.0"
  wrangler_version: "4.50.0"
  production_tested: true
  errors_prevented: 6
  references_included: 6
---

# Cloudflare Browser Rendering - Complete Reference

Production-ready knowledge domain for building browser automation workflows with Cloudflare Browser Rendering.

**Status**: Production Ready ✅
**Last Updated**: 2025-11-25
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: @cloudflare/puppeteer@1.0.4, @cloudflare/playwright@1.0.0, wrangler@4.50.0, @cloudflare/workers-types@4.20251125.0

---

## Table of Contents

1. [Quick Start (5 minutes)](#quick-start-5-minutes)
2. [Browser Rendering Overview](#browser-rendering-overview)
3. [Puppeteer API Reference](#puppeteer-api-reference)
4. [Playwright API Reference](#playwright-api-reference)
5. [Session Management](#session-management)
6. [Common Patterns](#common-patterns)
7. [Pricing & Limits](#pricing--limits)
8. [Known Issues Prevention](#known-issues-prevention)
9. [Production Checklist](#production-checklist)

---

## Quick Start (5 minutes)

### 1. Add Browser Binding

**wrangler.jsonc:**
```jsonc
{
  "name": "browser-worker",
  "main": "src/index.ts",
  "compatibility_date": "2023-03-14",
  "compatibility_flags": ["nodejs_compat"],
  "browser": {
    "binding": "MYBROWSER"
  }
}
```

**Why nodejs_compat?** Browser Rendering requires Node.js APIs and polyfills.

### 2. Install Puppeteer

```bash
bun add @cloudflare/puppeteer
```

### 3. Take Your First Screenshot

```typescript
import puppeteer from "@cloudflare/puppeteer";

interface Env {
  MYBROWSER: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url") || "https://example.com";

    // Launch browser
    const browser = await puppeteer.launch(env.MYBROWSER);
    const page = await browser.newPage();

    // Navigate and capture
    await page.goto(url);
    const screenshot = await page.screenshot();

    // Clean up
    await browser.close();

    return new Response(screenshot, {
      headers: { "content-type": "image/png" }
    });
  }
};
```

### 4. Deploy

```bash
bunx wrangler deploy
```

Test at: `https://your-worker.workers.dev/?url=https://example.com`

**CRITICAL:**
- Always pass `env.MYBROWSER` to `puppeteer.launch()` (not undefined)
- Always call `browser.close()` when done (or use `browser.disconnect()` for session reuse)
- Use `nodejs_compat` compatibility flag

---

## When to Load References

**Load immediately when user mentions**:

- `puppeteer-api.md` → "API reference", "Puppeteer methods", "Browser class", "Page methods", "complete API"
- `patterns.md` → "examples", "how to", "screenshot", "PDF", "scraping", "automation", "form filling"
- `session-management.md` → "sessions", "hibernation", "connection pooling", "state management", "Durable Objects"
- `pricing-and-limits.md` → "cost", "pricing", "limits", "quotas", "billing", "rate limits"
- `common-errors.md` → errors, debugging, "not working", troubleshooting, "issue #4", "issue #5", "issue #6"
- `puppeteer-vs-playwright.md` → "Playwright", "comparison", "which library", "differences"

**Load proactively when**:
- Building new automation → Load `patterns.md`
- Debugging errors → Load `common-errors.md`
- Optimizing costs → Load `pricing-and-limits.md`
- Managing sessions → Load `session-management.md`
- Need complete API → Load `puppeteer-api.md`

---

## Browser Rendering Overview

### What is Browser Rendering?

Cloudflare Browser Rendering provides headless Chromium browsers running on Cloudflare's global network. Use familiar tools like Puppeteer and Playwright to automate browser tasks:

- **Screenshots** - Capture visual snapshots of web pages
- **PDF Generation** - Convert HTML/URLs to PDFs
- **Web Scraping** - Extract content from dynamic websites
- **Testing** - Automate frontend tests
- **Crawling** - Navigate multi-page workflows

### Two Integration Methods

| Method | Best For | Complexity |
|--------|----------|-----------|
| **Workers Bindings** | Complex automation, custom workflows, session management | Advanced |
| **REST API** | Simple screenshot/PDF tasks | Simple |

**This skill covers Workers Bindings** (the advanced method with full Puppeteer/Playwright APIs).

### Puppeteer vs Playwright

| Feature | Puppeteer | Playwright |
|---------|-----------|------------|
| **API Familiarity** | Most popular | Growing adoption |
| **Package** | `@cloudflare/puppeteer@1.0.4` | `@cloudflare/playwright@1.0.0` |
| **Session Management** | ✅ Advanced APIs | ⚠️ Basic |
| **Browser Support** | Chromium only | Chromium only (Firefox/Safari not yet supported) |
| **Best For** | Screenshots, PDFs, scraping | Testing, frontend automation |

**Recommendation**: Use Puppeteer for most use cases. Playwright is ideal if you're already using it for testing.

---

## Puppeteer API Reference

**Core classes for browser automation**:

1. **Core Functions** - `launch()`, `connect()`, `sessions()`, `history()`, `limits()`
2. **Browser API** - `newPage()`, `sessionId()`, `close()`, `disconnect()`, `createBrowserContext()`
3. **Page API** - `goto()`, `screenshot()`, `pdf()`, `content()`, `setContent()`, `evaluate()`, `waitForSelector()`, `type()`, `click()`

**Quick Example:**
```typescript
const browser = await puppeteer.launch(env.MYBROWSER);
const page = await browser.newPage();
await page.goto("https://example.com");
const screenshot = await page.screenshot({ fullPage: true });
await browser.close();
```

**Load `references/puppeteer-api.md` when implementing browser automation, scraping, debugging Puppeteer-specific issues, or needing complete API signatures and method details.**

---

## Playwright API Reference

Playwright provides a similar API to Puppeteer with slight differences.

### Installation

```bash
bun add @cloudflare/playwright
```

### Basic Example

```typescript
import { env } from "cloudflare:test";
import { chromium } from "@cloudflare/playwright";

interface Env {
  BROWSER: Fetcher;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const browser = await chromium.launch(env.BROWSER);
    const page = await browser.newPage();

    await page.goto("https://example.com");
    const screenshot = await page.screenshot();

    await browser.close();

    return new Response(screenshot, {
      headers: { "content-type": "image/png" }
    });
  }
};
```

### Key Differences from Puppeteer

| Feature | Puppeteer | Playwright |
|---------|-----------|------------|
| **Import** | `import puppeteer from "@cloudflare/puppeteer"` | `import { chromium } from "@cloudflare/playwright"` |
| **Launch** | `puppeteer.launch(env.MYBROWSER)` | `chromium.launch(env.BROWSER)` |
| **Session API** | ✅ Advanced (sessions, history, limits) | ⚠️ Basic |
| **Auto-waiting** | Manual `waitForSelector()` | Built-in auto-waiting |
| **Selectors** | CSS only | CSS, text, XPath (via evaluate workaround) |

**Recommendation**: Stick with Puppeteer unless you have existing Playwright tests to migrate.

---

## Session Management

Browser sessions are managed using Durable Objects for state persistence across multiple requests. Sessions support hibernation, automatic cleanup, and concurrent connection handling.

**Key Patterns**:
- **Session Reuse** - Use `puppeteer.sessions()` and `puppeteer.connect()` to reuse browsers
- **Browser Contexts** - Isolate cookies/cache while sharing browser instance
- **Multiple Tabs** - Use tabs (`newPage()`) instead of multiple browsers for batch operations
- **Disconnect vs Close** - Use `disconnect()` to keep session alive, `close()` to terminate

**Load `references/session-management.md` for complete session lifecycle management, hibernation patterns, connection pooling strategies, and production examples.**

---

## Common Patterns

**6 production-ready browser automation patterns**:

1. **Screenshot with KV Caching** - Cache screenshots for high-traffic URLs, reduce browser usage
2. **PDF Generation from HTML** - Convert custom HTML to PDF for invoices, reports, documents
3. **Web Scraping with Structured Data** - Extract product information, prices, content from web pages
4. **Batch Scraping Multiple URLs** - Efficiently scrape multiple sites using tabs in single browser
5. **AI-Enhanced Scraping** - Combine Browser Rendering with Workers AI for adaptive data extraction
6. **Form Filling and Automation** - Automate login flows, form submissions, multi-step workflows

**Quick Example** (Screenshot with caching):
```typescript
const browser = await puppeteer.launch(env.MYBROWSER);
const page = await browser.newPage();
await page.goto(url);
const screenshot = await page.screenshot({ fullPage: true });
await env.CACHE.put(url, screenshot, { expirationTtl: 86400 });
await browser.close();
```

**Load `references/patterns.md` when implementing browser automation patterns, scraping, PDF generation, or needing complete production examples with error handling and optimizations.**

---

## Pricing & Limits

Browser Rendering charges based on CPU time (paid plans only). Free tier: 10 minutes/day. Paid tier: 10 hours/month included, then $0.09 per browser hour + $2.00 per concurrent browser above 10.

**Load `references/pricing-and-limits.md` for complete pricing tiers, quota details, rate limiting strategies, and cost optimization techniques.**

---

## Known Issues Prevention

This skill prevents **6 documented issues**. Top 3 critical errors detailed below:

---

### Issue #1: XPath Selectors Not Supported ⚠️

**Error:** "XPath selector not supported" or selector failures
**Source:** https://developers.cloudflare.com/browser-rendering/faq/#why-cant-i-use-an-xpath-selector-when-using-browser-rendering-with-puppeteer
**Why It Happens:** XPath poses a security risk to Workers
**Prevention:** Use CSS selectors or `page.evaluate()` with XPathEvaluator

**Solution:**
```typescript
// ❌ Don't use XPath directly (not supported)
// await page.$x('/html/body/div/h1')

// ✅ Use CSS selector
const heading = await page.$("div > h1");

// ✅ Or use XPath in page.evaluate()
const innerHtml = await page.evaluate(() => {
  return new XPathEvaluator()
    .createExpression("/html/body/div/h1")
    .evaluate(document, XPathResult.FIRST_ORDERED_NODE_TYPE)
    .singleNodeValue.innerHTML;
});
```

---

### Issue #2: Browser Binding Not Passed ⚠️

**Error:** "Cannot read properties of undefined (reading 'fetch')"
**Source:** https://developers.cloudflare.com/browser-rendering/faq/#cannot-read-properties-of-undefined-reading-fetch
**Why It Happens:** `puppeteer.launch()` called without browser binding
**Prevention:** Always pass `env.MYBROWSER` to launch

**Solution:**
```typescript
// ❌ Missing browser binding
const browser = await puppeteer.launch(); // Error!

// ✅ Pass binding
const browser = await puppeteer.launch(env.MYBROWSER);
```

---

### Issue #3: Browser Timeout (60 seconds) ⚠️

**Error:** Browser closes unexpectedly after 60 seconds
**Source:** https://developers.cloudflare.com/browser-rendering/platform/limits/#note-on-browser-timeout
**Why It Happens:** Default timeout is 60 seconds of inactivity
**Prevention:** Use `keep_alive` option to extend up to 10 minutes

**Solution:**
```typescript
// Extend timeout to 5 minutes for long-running tasks
const browser = await puppeteer.launch(env.MYBROWSER, {
  keep_alive: 300000 // 5 minutes = 300,000 ms
});
```

**Note:** Browser closes if no devtools commands for the specified duration.

---

### Additional Issues (4-6)

**Load `references/common-errors.md` for complete error catalog including**:
- Issue #4: Concurrency limits and rate limiting
- Issue #5: Local development request size limits
- Issue #6: Bot protection and WAF bypass strategies

Plus solutions for page crashes, authentication issues, resource loading errors, and debugging strategies.

---

## Production Checklist

**Critical Items Before Deployment:**
- ✅ Browser binding + `nodejs_compat` flag configured
- ✅ Error handling with try-finally cleanup
- ✅ Rate limit checks and retry logic
- ✅ Session reuse for performance
- ✅ KV caching for repeated operations
- ✅ Input validation (prevent SSRF)
- ✅ Monitoring dashboard at https://dash.cloudflare.com

**Load `references/patterns.md` for production-ready templates with complete error handling, monitoring, and security patterns.**

---

## Dependencies

**Required**: `@cloudflare/puppeteer@1.0.4`, `wrangler@4.50.0`, `@cloudflare/workers-types@4.20251125.0`
**Related Skills**: `cloudflare-worker-base` (Worker setup), `cloudflare-kv` (caching), `cloudflare-workers-ai` (AI scraping)

---

## Official Documentation

- **Browser Rendering Docs**: https://developers.cloudflare.com/browser-rendering/
- **Puppeteer API**: https://pptr.dev/api/
- **Playwright API**: https://playwright.dev/docs/api/class-playwright
- **Cloudflare Puppeteer Fork**: https://github.com/cloudflare/puppeteer
- **Cloudflare Playwright Fork**: https://github.com/cloudflare/playwright
- **Pricing**: https://developers.cloudflare.com/browser-rendering/platform/pricing/
- **Limits**: https://developers.cloudflare.com/browser-rendering/platform/limits/

---

## Package Versions (Verified 2025-11-27)

```json
{
  "dependencies": {
    "@cloudflare/puppeteer": "^1.0.4"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20251125.0",
    "wrangler": "^4.50.0"
  }
}
```

**Alternative (Playwright):**
```json
{
  "dependencies": {
    "@cloudflare/playwright": "^1.0.0"
  }
}
```

---

## Troubleshooting

### Problem: "Cannot read properties of undefined (reading 'fetch')"
**Solution:** Pass browser binding to puppeteer.launch():
```typescript
const browser = await puppeteer.launch(env.MYBROWSER); // Not just puppeteer.launch()
```

### Problem: XPath selectors not working
**Solution:** Use CSS selectors or page.evaluate() with XPathEvaluator (see Issue #1)

### Problem: Browser closes after 60 seconds
**Solution:** Extend timeout with keep_alive:
```typescript
const browser = await puppeteer.launch(env.MYBROWSER, { keep_alive: 300000 });
```

### Problem: Rate limit reached
**Solution:** Reuse sessions, use tabs, check limits before launching (see Issue #4)

### Problem: Local dev request > 1MB fails
**Solution:** Enable remote binding in wrangler.jsonc:
```jsonc
{ "browser": { "binding": "MYBROWSER", "remote": true } }
```

### Problem: Website blocks as bot
**Solution:** Cannot bypass. If your own zone, create WAF skip rule (see Issue #6)

---

**Questions? Issues?**

1. Check `references/common-errors.md` for detailed solutions
2. Review `references/session-management.md` for performance optimization
3. Verify browser binding is configured in wrangler.jsonc
4. Check official docs: https://developers.cloudflare.com/browser-rendering/
5. Ensure `nodejs_compat` compatibility flag is enabled
