---
name: cloudflare-browser-rendering
description: |
  Add headless Chrome automation with Puppeteer/Playwright on Cloudflare Workers. Use when: taking screenshots, generating PDFs, web scraping, crawling sites, browser automation, or troubleshooting XPath errors, browser timeouts, binding not passed errors, session limits, page.evaluate __name errors, or waitForSelector timeout issues.
user-invocable: true
---

# Cloudflare Browser Rendering - Complete Reference

Production-ready knowledge domain for building browser automation workflows with Cloudflare Browser Rendering.

**Status**: Production Ready ✅
**Last Updated**: 2026-01-21
**Dependencies**: cloudflare-worker-base (for Worker setup)
**Latest Versions**: @cloudflare/puppeteer@1.0.4, @cloudflare/playwright@1.1.0, wrangler@4.59.3

**Recent Updates (2025)**:
- **Sept 2025**: Playwright v1.55 GA, Stagehand framework support (Workers AI), /links excludeExternalLinks param
- **Aug 2025**: Billing GA (Aug 20), /sessions endpoint in local dev, X-Browser-Ms-Used header
- **July 2025**: Playwright v1.54.1 + MCP v0.0.30, Playwright local dev support (wrangler@4.26.0+), Puppeteer v22.13.1 sync, /content returns title, /json custom_ai param, /screenshot viewport 1920x1080 default
- **June 2025**: Web Bot Auth headers auto-included
- **April 2025**: Playwright support launched, free tier introduced

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
npm install @cloudflare/puppeteer
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
npx wrangler deploy
```

Test at: `https://your-worker.workers.dev/?url=https://example.com`

**CRITICAL:**
- Always pass `env.MYBROWSER` to `puppeteer.launch()` (not undefined)
- Always call `browser.close()` when done (or use `browser.disconnect()` for session reuse)
- Use `nodejs_compat` compatibility flag

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

**Core APIs** (complete reference: https://pptr.dev/api/):

**Global Functions:**
- `puppeteer.launch(env.MYBROWSER, options?)` - Launch new browser (CRITICAL: must pass binding)
- `puppeteer.connect(env.MYBROWSER, sessionId)` - Connect to existing session
- `puppeteer.sessions(env.MYBROWSER)` - List running sessions
- `puppeteer.history(env.MYBROWSER)` - List recent sessions (open + closed)
- `puppeteer.limits(env.MYBROWSER)` - Check account limits

**Browser Methods:**
- `browser.newPage()` - Create new tab (preferred over launching new browsers)
- `browser.sessionId()` - Get session ID for reuse
- `browser.close()` - Terminate session
- `browser.disconnect()` - Keep session alive for reuse
- `browser.createBrowserContext()` - Isolated incognito context (separate cookies/cache)

**Page Methods:**
- `page.goto(url, { waitUntil, timeout })` - Navigate (use `"networkidle0"` for dynamic content)
- `page.screenshot({ fullPage, type, quality, clip })` - Capture image
- `page.pdf({ format, printBackground, margin })` - Generate PDF
- `page.evaluate(() => ...)` - Execute JS in browser (data extraction, XPath workaround)
- `page.content()` / `page.setContent(html)` - Get/set HTML
- `page.waitForSelector(selector)` - Wait for element
- `page.type(selector, text)` / `page.click(selector)` - Form interaction

**Critical Patterns:**
```typescript
// Must pass binding
const browser = await puppeteer.launch(env.MYBROWSER); // ✅
// const browser = await puppeteer.launch(); // ❌ Error!

// Session reuse for performance
const sessions = await puppeteer.sessions(env.MYBROWSER);
const freeSessions = sessions.filter(s => !s.connectionId);
if (freeSessions.length > 0) {
  browser = await puppeteer.connect(env.MYBROWSER, freeSessions[0].sessionId);
}

// Keep session alive
await browser.disconnect(); // Don't close

// XPath workaround (not directly supported)
const data = await page.evaluate(() => {
  return new XPathEvaluator()
    .createExpression("/html/body/div/h1")
    .evaluate(document, XPathResult.FIRST_ORDERED_NODE_TYPE)
    .singleNodeValue.innerHTML;
});
```

---

## Playwright API Reference

**Status**: GA (Sept 2025) - Playwright v1.55, MCP v0.0.30 support, local dev support (wrangler@4.26.0+)

**Installation:**
```bash
npm install @cloudflare/playwright
```

**Configuration Requirements (2025 Update):**
```jsonc
{
  "compatibility_flags": ["nodejs_compat"],
  "compatibility_date": "2025-09-15"  // Required for Playwright v1.55
}
```

**Basic Usage:**
```typescript
import { chromium } from "@cloudflare/playwright";

const browser = await chromium.launch(env.BROWSER);
const page = await browser.newPage();
await page.goto("https://example.com");
const screenshot = await page.screenshot();
await browser.close();
```

**Puppeteer vs Playwright:**
- **Import**: `puppeteer` vs `{ chromium }` from "@cloudflare/playwright"
- **Session API**: Puppeteer has advanced session management (sessions/history/limits), Playwright basic
- **Auto-waiting**: Playwright has built-in auto-waiting, Puppeteer requires manual `waitForSelector()`
- **MCP Support**: Playwright MCP v0.0.30 (July 2025), Playwright MCP server available
- **Latest Version**: Playwright v1.57 support (Jan 2026 update)

**Recommendation**: Use Puppeteer for session reuse patterns. Use Playwright if migrating existing tests or need MCP integration.

**Official Docs**: https://developers.cloudflare.com/browser-rendering/playwright/

---

## Session Management

**Why**: Launching new browsers is slow and consumes concurrency limits. Reuse sessions for faster response, lower concurrency usage, better resource utilization.

### Session Reuse Pattern (Critical)

```typescript
async function getBrowser(env: Env): Promise<Browser> {
  const sessions = await puppeteer.sessions(env.MYBROWSER);
  const freeSessions = sessions.filter(s => !s.connectionId);

  if (freeSessions.length > 0) {
    try {
      return await puppeteer.connect(env.MYBROWSER, freeSessions[0].sessionId);
    } catch (e) {
      console.log("Failed to connect, launching new browser");
    }
  }

  return await puppeteer.launch(env.MYBROWSER);
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const browser = await getBrowser(env);

    try {
      const page = await browser.newPage();
      await page.goto("https://example.com");
      const screenshot = await page.screenshot();

      await browser.disconnect(); // ✅ Keep alive for reuse

      return new Response(screenshot, {
        headers: { "content-type": "image/png" }
      });
    } catch (error) {
      await browser.close(); // ❌ Close on error
      throw error;
    }
  }
};
```

**Key Rules:**
- ✅ `browser.disconnect()` - Keep session alive for reuse
- ❌ `browser.close()` - Only on errors or when truly done
- ✅ Always handle connection failures

### Browser Contexts (Cookie/Cache Isolation)

Use `browser.createBrowserContext()` to share browser but isolate cookies/cache:

```typescript
const browser = await puppeteer.launch(env.MYBROWSER);
const context1 = await browser.createBrowserContext(); // User 1
const context2 = await browser.createBrowserContext(); // User 2

const page1 = await context1.newPage();
const page2 = await context2.newPage();
// Separate cookies/cache per context
```

### Multiple Tabs Pattern

**❌ Bad**: Launch 10 browsers for 10 URLs (wastes concurrency)
**✅ Good**: 1 browser, 10 tabs via `Promise.all()` + `browser.newPage()`

```typescript
const browser = await puppeteer.launch(env.MYBROWSER);
const results = await Promise.all(
  urls.map(async (url) => {
    const page = await browser.newPage();
    await page.goto(url);
    const data = await page.evaluate(() => ({ title: document.title }));
    await page.close();
    return { url, data };
  })
);
await browser.close();
```

---

## Common Patterns

### Screenshot with KV Caching

Cache screenshots to reduce browser usage and improve performance:

```typescript
interface Env {
  MYBROWSER: Fetcher;
  CACHE: KVNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url");
    if (!url) return new Response("Missing ?url parameter", { status: 400 });

    const normalizedUrl = new URL(url).toString();

    // Check cache first
    let screenshot = await env.CACHE.get(normalizedUrl, { type: "arrayBuffer" });

    if (!screenshot) {
      const browser = await puppeteer.launch(env.MYBROWSER);
      const page = await browser.newPage();
      await page.goto(normalizedUrl);
      screenshot = await page.screenshot();
      await browser.close();

      // Cache for 24 hours
      await env.CACHE.put(normalizedUrl, screenshot, { expirationTtl: 60 * 60 * 24 });
    }

    return new Response(screenshot, { headers: { "content-type": "image/png" } });
  }
};
```

### AI-Enhanced Scraping

Combine Browser Rendering with Workers AI for structured data extraction:

```typescript
interface Env {
  MYBROWSER: Fetcher;
  AI: Ai;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const { searchParams } = new URL(request.url);
    const url = searchParams.get("url");

    // Scrape page content
    const browser = await puppeteer.launch(env.MYBROWSER);
    const page = await browser.newPage();
    await page.goto(url!, { waitUntil: "networkidle0" });
    const bodyContent = await page.$eval("body", el => el.innerHTML);
    await browser.close();

    // Extract structured data with AI
    const response = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
      messages: [{
        role: "user",
        content: `Extract product info as JSON from this HTML. Include: name, price, description.\n\nHTML:\n${bodyContent.slice(0, 4000)}`
      }]
    });

    return Response.json({ url, product: JSON.parse(response.response) });
  }
};
```

**Other Common Patterns**: PDF generation (`page.pdf()`), structured scraping (`page.evaluate()`), form automation (`page.type()` + `page.click()`). See bundled `templates/` directory.

---

## Pricing & Limits

**Billing GA**: August 20, 2025

**Free Tier**: 10 min/day, 3 concurrent, 3 launches/min, 60s timeout
**Paid Tier**: 10 hrs/month included ($0.09/hr after), 30 concurrent ($2.00/browser after), 30 launches/min, 60s-10min timeout

**Concurrency Calculation**: Monthly average of daily peak usage (e.g., 35 browsers avg = (35 - 30 included) × $2.00 = $10.00/mo)

**Rate Limiting**: Enforced with a **fixed per-second fill rate** (NOT burst-friendly). 30 req/min = 1 req every 2 seconds. You CANNOT send all 30 requests at once, even if quota is unused. Check `puppeteer.limits(env.MYBROWSER)` before launching:

```typescript
const limits = await puppeteer.limits(env.MYBROWSER);
if (limits.allowedBrowserAcquisitions === 0) {
  const delay = limits.timeUntilNextAllowedBrowserAcquisition || 1000;
  await new Promise(resolve => setTimeout(resolve, delay));
}
```

---

## Known Issues Prevention

This skill prevents **8 documented issues**:

---

### Issue #1: XPath Selectors Not Supported

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

### Issue #2: Browser Binding Not Passed (Fetcher Type Confusion)

**Error:** "Cannot read properties of undefined (reading 'fetch')" or "RPC receiver does not implement the method 'launch'"
**Source:** [GitHub Issue #10772](https://github.com/cloudflare/workers-sdk/issues/10772), https://developers.cloudflare.com/browser-rendering/faq/#cannot-read-properties-of-undefined-reading-fetch
**Why It Happens:** `puppeteer.launch()` called without browser binding, or trying to call `env.MYBROWSER.launch()` directly. The browser binding is a **Fetcher** (REST API wrapper), not a browser instance.
**Prevention:** Always pass `env.MYBROWSER` to `puppeteer.launch()` or `chromium.launch()` wrapper

**Solution:**
```typescript
// ❌ Missing browser binding
const browser = await puppeteer.launch(); // Error!

// ❌ Wrong - trying to call launch() on Fetcher directly
const browser = await env.MYBROWSER.launch(); // "RPC receiver does not implement the method 'launch'"

// ✅ Pass binding to Puppeteer/Playwright wrapper
const browser = await puppeteer.launch(env.MYBROWSER);
// or for Playwright:
const browser = await chromium.launch(env.MYBROWSER);
```

**TypeScript Type Explanation:**
```typescript
interface Env {
  MYBROWSER: Fetcher; // It's a Fetcher, not a Browser!
}
```

---

### Issue #3: Browser Timeout (60 seconds)

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

### Issue #4: Concurrency Limits Reached

**Error:** "Rate limit exceeded" or new browser launch fails
**Source:** https://developers.cloudflare.com/browser-rendering/platform/limits/, [Changelog 2025-09-25](https://developers.cloudflare.com/browser-rendering/changelog/)
**Why It Happens:** Exceeded concurrent browser limit (3 free, 30 paid as of Sept 2025)
**Prevention:** Reuse sessions, use tabs instead of multiple browsers, check limits before launching, throttle requests to per-second rate

**Solutions:**
```typescript
// 1. Check limits before launching
const limits = await puppeteer.limits(env.MYBROWSER);
if (limits.allowedBrowserAcquisitions === 0) {
  return new Response("Concurrency limit reached", { status: 429 });
}

// 2. Reuse sessions
const sessions = await puppeteer.sessions(env.MYBROWSER);
const freeSessions = sessions.filter(s => !s.connectionId);
if (freeSessions.length > 0) {
  const browser = await puppeteer.connect(env.MYBROWSER, freeSessions[0].sessionId);
}

// 3. Use tabs instead of multiple browsers
const browser = await puppeteer.launch(env.MYBROWSER);
const page1 = await browser.newPage();
const page2 = await browser.newPage(); // Same browser, different tabs
```

---

### Issue #5: Local Development Request Size Limit

**Error:** Request larger than 1MB fails in `wrangler dev`
**Source:** https://developers.cloudflare.com/browser-rendering/faq/#does-local-development-support-all-browser-rendering-features
**Why It Happens:** Local development limitation
**Prevention:** Use `remote: true` in browser binding for local dev

**Solution:**
```jsonc
// wrangler.jsonc for local development
{
  "browser": {
    "binding": "MYBROWSER",
    "remote": true  // Use real headless browser during dev
  }
}
```

---

### Issue #6: Bot Protection Always Triggered

**Error:** Website blocks requests as bot traffic
**Source:** https://developers.cloudflare.com/browser-rendering/faq/#will-browser-rendering-bypass-cloudflares-bot-protection
**Why It Happens:** Browser Rendering requests always identified as bots
**Prevention:** Cannot bypass; if scraping your own zone, create WAF skip rule (requires Enterprise plan for Bot Management)

**Solution:**
```typescript
// ❌ Cannot bypass bot protection
// Requests will always be identified as bots

// ✅ If scraping your own Cloudflare zone (Enterprise plan only):
// 1. Go to Security > WAF > Custom rules
// 2. Create skip rule with custom header:
//    Header: X-Custom-Auth
//    Value: your-secret-token
// 3. Pass header in your scraping requests

await page.setExtraHTTPHeaders({
  'X-Custom-Auth': 'your-secret-token'
});

// Note: Automatic headers are included:
// - cf-biso-request-id
// - cf-biso-devtools
```

**Important:** Free/Pro/Business plans CANNOT bypass bot detection even on their own sites. Enterprise plan with Bot Management is required for WAF allowlisting.

---

### Issue #7: page.evaluate() Function Name Injection (__name Error)

**Error:** `ReferenceError: __name is not defined`
**Source:** [GitHub Issue #7107](https://github.com/cloudflare/workers-sdk/issues/7107)
**Why It Happens:** esbuild minification (wrangler 3.80.1+) injects `__name()` helper calls in arrow functions with nested function declarations. These run in browser context where the helper doesn't exist.
**Prevention:** Keep `page.evaluate()` functions simple - avoid nested function declarations
**Applies to:** wrangler 3.80.1 - 3.83.0 (fixed in 3.83.0+)

**Solution:**
```typescript
// ❌ Avoid nested function declarations
const data = await page.evaluate(async () => {
  function toNumber(str: string | undefined): number | undefined {
    const num = typeof str === 'string' ? str.replaceAll('.', '').replaceAll(',', '.').match(/[+-]?([0-9]*[.])?[0-9]+/) : false;
    if (num) {
      return Number(num[0]);
    } else {
      return undefined;
    }
  }
  return toNumber('123.456');
});
// Error: ReferenceError: __name is not defined

// ✅ Inline the logic without nested functions
const data = await page.evaluate(async () => {
  const str = '123.456';
  const num = typeof str === 'string' ? str.replaceAll('.', '').replaceAll(',', '.').match(/[+-]?([0-9]*[.])?[0-9]+/) : false;
  return num ? Number(num[0]) : undefined;
});

// ✅ Or update to wrangler 3.83.0+
// npm install wrangler@latest
```

**Note:** This also affects `page.waitForSelector()` with complex callbacks. Fixed in wrangler 3.83.0+ (Nov 2024).

---

### Issue #8: waitForSelector() Timeout Behavior Changed

**Error:** Code that relied on indefinite waiting now times out
**Source:** [Changelog 2026-01-07](https://developers.cloudflare.com/browser-rendering/changelog/)
**Why It Happens:** `waitForSelector()` previously did NOT timeout when selectors weren't found (hung indefinitely). This was fixed to properly honor timeout values.
**Prevention:** Always set explicit timeouts and handle timeout errors
**Applies to:** All code written before Jan 2026 that relied on indefinite waiting

**Solution:**
```typescript
// ❌ Old behavior - would hang forever if selector not found
await page.waitForSelector('#dynamic-element');

// ✅ New behavior - properly times out (set explicit timeout)
try {
  await page.waitForSelector('#dynamic-element', { timeout: 5000 });
} catch (error) {
  if (error.name === 'TimeoutError') {
    console.log('Element not found within 5 seconds');
    // Handle missing element gracefully
  } else {
    throw error;
  }
}

// ✅ Use longer timeout for slow-loading elements
await page.waitForSelector('#slow-element', { timeout: 30000 }); // 30 seconds
```

**Note:** This is a breaking fix (behavior change). Code that relied on indefinite waiting will now timeout and throw errors. Always handle `TimeoutError` gracefully.

---

## Production Checklist

Before deploying Browser Rendering Workers to production:

### Configuration
- [ ] **Browser binding configured** in wrangler.jsonc
- [ ] **nodejs_compat flag enabled** (required for Browser Rendering)
- [ ] **Keep-alive timeout set** if tasks take > 60 seconds
- [ ] **Remote binding enabled** for local development if needed

### Error Handling
- [ ] **Retry logic implemented** for rate limits
- [ ] **Timeout handling** for page.goto()
- [ ] **Browser cleanup** in try-finally blocks
- [ ] **Concurrency limit checks** before launching browsers
- [ ] **Graceful degradation** when browser unavailable

### Performance
- [ ] **Session reuse implemented** for high-traffic routes
- [ ] **Multiple tabs used** instead of multiple browsers
- [ ] **Incognito contexts** for session isolation
- [ ] **KV caching** for repeated screenshots/PDFs
- [ ] **Batch operations** to maximize browser utilization

### Monitoring
- [ ] **Log browser session IDs** for debugging
- [ ] **Track browser duration** for billing estimates
- [ ] **Monitor concurrency usage** with puppeteer.limits()
- [ ] **Alert on rate limit errors**
- [ ] **Dashboard monitoring** at https://dash.cloudflare.com/?to=/:account/workers/browser-rendering

### Security
- [ ] **Input validation** for URLs (prevent SSRF)
- [ ] **Timeout limits** to prevent abuse
- [ ] **Rate limiting** on public endpoints
- [ ] **Authentication** for sensitive scraping endpoints
- [ ] **WAF rules** if scraping your own zone

### Testing
- [ ] **Test screenshot capture** with various page sizes
- [ ] **Test PDF generation** with custom HTML
- [ ] **Test scraping** with dynamic content (networkidle0)
- [ ] **Test error scenarios** (invalid URLs, timeouts)
- [ ] **Load test** concurrency limits

---

## Error Handling Best Practices

**Production Pattern** - Use try-catch with proper cleanup:

```typescript
async function withBrowser<T>(env: Env, fn: (browser: Browser) => Promise<T>): Promise<T> {
  let browser: Browser | null = null;

  try {
    // 1. Check limits before launching
    const limits = await puppeteer.limits(env.MYBROWSER);
    if (limits.allowedBrowserAcquisitions === 0) {
      throw new Error("Rate limit reached");
    }

    // 2. Try session reuse first
    const sessions = await puppeteer.sessions(env.MYBROWSER);
    const freeSessions = sessions.filter(s => !s.connectionId);
    browser = freeSessions.length > 0
      ? await puppeteer.connect(env.MYBROWSER, freeSessions[0].sessionId)
      : await puppeteer.launch(env.MYBROWSER);

    // 3. Execute user function
    const result = await fn(browser);

    // 4. Disconnect (keep alive)
    await browser.disconnect();
    return result;
  } catch (error) {
    // 5. Close on error
    if (browser) await browser.close();
    throw error;
  }
}
```

**Key Principles**: Check limits → Reuse sessions → Execute → Disconnect on success, close on error

---

## Using Bundled Resources

### Templates (templates/)

Ready-to-use code templates for common patterns:

- `basic-screenshot.ts` - Minimal screenshot example
- `screenshot-with-kv-cache.ts` - Screenshot with KV caching
- `pdf-generation.ts` - Generate PDFs from HTML or URLs
- `web-scraper-basic.ts` - Basic web scraping pattern
- `web-scraper-batch.ts` - Batch scrape multiple URLs
- `session-reuse.ts` - Session reuse for performance
- `ai-enhanced-scraper.ts` - Scraping with Workers AI
- `playwright-example.ts` - Playwright alternative example
- `wrangler-browser-config.jsonc` - Browser binding configuration

**Usage:**
```bash
# Copy template to your project
cp ~/.claude/skills/cloudflare-browser-rendering/templates/basic-screenshot.ts src/index.ts
```

### References (references/)

Deep-dive documentation:

- `session-management.md` - Complete session reuse guide
- `pricing-and-limits.md` - Detailed pricing breakdown
- `common-errors.md` - All known issues and solutions
- `puppeteer-vs-playwright.md` - Feature comparison and migration

**When to load:** Reference when implementing advanced patterns or debugging specific issues.

---

## Dependencies

**Required:**
- `@cloudflare/puppeteer@1.0.4` - Puppeteer for Workers
- `wrangler@4.43.0+` - Cloudflare CLI

**Optional:**
- `@cloudflare/playwright@1.0.0` - Playwright for Workers (alternative)
- `@cloudflare/workers-types@4.20251014.0+` - TypeScript types

**Related Skills:**
- `cloudflare-worker-base` - Worker setup with Hono
- `cloudflare-kv` - KV caching for screenshots
- `cloudflare-r2` - R2 storage for generated files
- `cloudflare-workers-ai` - AI-enhanced scraping

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

## Package Versions (Verified 2026-01-21)

```json
{
  "dependencies": {
    "@cloudflare/puppeteer": "^1.0.4"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20251014.0",
    "wrangler": "^4.59.3"
  }
}
```

**Alternative (Playwright):**
```json
{
  "dependencies": {
    "@cloudflare/playwright": "^1.1.0"
  }
}
```

**Note:** Playwright v1.1.0 includes support for Playwright v1.57 (Jan 2026). Wrangler 3.83.0+ fixes the `page.evaluate()` __name injection bug.

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
