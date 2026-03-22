---
name: playwright
description: Write, debug, and maintain Playwright tests and scrapers with resilient selectors, flaky test fixes, and CI/CD integration.
---

## Trigger

Use when writing Playwright tests, debugging failures, scraping with Playwright, or setting up CI/CD pipelines.

## Selector Priority (Always)

1. `getByRole()` — accessible, resilient
2. `getByTestId()` — explicit, stable
3. `getByLabel()`, `getByPlaceholder()` — form elements
4. `getByText()` — visible content (exact match preferred)
5. CSS/XPath — last resort, avoid nth-child and generated classes

## Critical Rules

- **Never use `page.waitForTimeout()`** — use `waitFor*` methods or `expect` with polling
- **Always close contexts** — `browser.close()` or `context.close()` to prevent memory leaks
- **Prefer `networkidle` with caution** — SPAs may never reach idle; use DOM-based waits instead
- **Use `test.describe.configure({ mode: 'parallel' })`** — for independent tests
- **Trace on failure only** — `trace: 'on-first-retry'` in config, not always-on

## Quick Fixes

| Symptom | Fix |
|---------|-----|
| Element not found | Use `waitFor()` before interaction, check frame context |
| Flaky clicks | Use `click({ force: true })` or `waitFor({ state: 'visible' })` first |
| Timeout in CI | Increase timeout, add `expect.poll()`, check viewport size |
| Stale element | Re-query the locator, avoid storing element references |
| Auth lost between tests | Use `storageState` to persist cookies/localStorage |

## Scraping Patterns

```js
// Basic scrape with Playwright
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (compatible; bot/1.0)'
});
const page = await context.newPage();

await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });

// Wait for specific element
await page.waitForSelector('.article-content');

// Extract data
const data = await page.$$eval('.article', articles =>
  articles.map(a => ({
    title: a.querySelector('h2')?.textContent?.trim(),
    url: a.querySelector('a')?.href,
    date: a.querySelector('time')?.getAttribute('datetime')
  }))
);

await browser.close();
```

## Test Structure (Laravel Dusk compatible)

```js
// playwright.config.ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30_000,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: 'http://localhost',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

```js
// Basic test
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Login' }).click();
  await expect(page).toHaveURL('/dashboard');
});
```

## Auth State Persistence

```js
// Save auth state
await page.goto('/login');
await page.getByLabel('Email').fill('admin@example.com');
await page.getByLabel('Password').fill('secret');
await page.getByRole('button', { name: 'Login' }).click();
await page.context().storageState({ path: 'auth.json' });

// Reuse in other tests
const context = await browser.newContext({ storageState: 'auth.json' });
```

## Screenshot / PDF

```js
await page.screenshot({ path: 'screenshot.png', fullPage: true });
await page.pdf({ path: 'page.pdf', format: 'A4' });
```

## Useful CLI Commands

```bash
npx playwright test                         # Run all tests
npx playwright test --headed               # With browser visible
npx playwright test --debug                # Debug mode (step-by-step)
npx playwright test --grep "login"         # Filter by test name
npx playwright show-report                 # Open HTML report
npx playwright codegen https://example.com # Record interactions → code
```
