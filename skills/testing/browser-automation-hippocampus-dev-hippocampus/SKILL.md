---
name: browser-automation
description: Browser automation toolkit using Playwright. Supports interacting with web applications, form filling, capturing screenshots, viewing browser logs, and running automated tests. Use when automating browser tasks, testing web UI, or scraping web pages.
keywords: playwright, browser, ブラウザ, 自動化, スクレイピング, e2e, screenshot, スクリーンショット, scraping
---

* Write `@playwright/test` scripts in TypeScript, run with `npx playwright test`
* Use `scripts/with-server.mjs --help` to manage server lifecycle
* Wait for `networkidle` before inspecting DOM on dynamic apps

## Quick Start

* `npx playwright install chromium` - Install browser (one-time)
* `npx playwright test your-test.spec.ts` - Run a test

## Approach

* Static HTML → Read file directly to identify selectors, then write test
* Dynamic app (server not running) → Use `with-server.mjs` to start server, then test
* Dynamic app (server running) → Navigate, wait for `networkidle`, inspect, then act

## Basic Test Structure

```typescript
import {test, expect, type Page} from "@playwright/test";

test("verify homepage loads", async ({page}: {page: Page}) => {
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");
    await expect(page.locator("h1")).toBeVisible();
});
```

## Using with-server.mjs

```bash
# Single server
node scripts/with-server.mjs --server "npm run dev" --port 5173 -- npx playwright test

# Multiple servers
node scripts/with-server.mjs \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- npx playwright test
```

## Best Practices

* Use `expect()` for assertions instead of manual checks
* Browser cleanup is automatic with `@playwright/test`
* Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
* Add waits: `page.waitForSelector()` or `expect().toBeVisible()`

## Reference Files

* `examples/element-discovery.spec.ts` - Discovering buttons, links, inputs
* `examples/static-html-automation.spec.ts` - Using file:// URLs
* `examples/console-logging.spec.ts` - Capturing console logs
