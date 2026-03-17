---
name: playwright
description: 微软开发的跨浏览器自动化框架。使用单一API支持Chromium、Firefox和WebKit，用于测试、爬虫和自动化。
metadata:
  short-description: 跨浏览器自动化框架
source:
  repository: https://github.com/microsoft/playwright
  license: Apache-2.0
  stars: 68k+
---

# Playwright Tool

## Description
Cross-browser automation for testing, scraping, and web automation supporting Chromium, Firefox, and WebKit.

## Source
- Repository: [microsoft/playwright](https://github.com/microsoft/playwright)
- License: Apache-2.0
- Maintainer: Microsoft

## Installation

```bash
npm install playwright
npx playwright install  # Install browsers
```

## Usage Examples

### Browser Automation

```typescript
import { chromium, firefox, webkit } from 'playwright';

async function automateTask() {
  // Launch any browser
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Custom User Agent',
  });
  const page = await context.newPage();
  
  await page.goto('https://example.com');
  
  // Click, type, interact
  await page.click('button.login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  
  // Wait for navigation
  await page.waitForURL('**/dashboard');
  
  await browser.close();
}
```

### Screenshot & PDF

```typescript
async function captureContent(url: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto(url);
  
  // Screenshot
  await page.screenshot({
    path: 'screenshot.png',
    fullPage: true,
  });
  
  // PDF (Chromium only)
  await page.pdf({
    path: 'document.pdf',
    format: 'A4',
    margin: { top: '1cm', bottom: '1cm' },
  });
  
  await browser.close();
}
```

### Web Scraping with Locators

```typescript
async function scrapeProducts(url: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto(url);
  
  // Use locators for reliable element selection
  const products = await page.locator('.product-card').all();
  
  const data = await Promise.all(products.map(async (product) => ({
    name: await product.locator('.name').textContent(),
    price: await product.locator('.price').textContent(),
    rating: await product.locator('.rating').getAttribute('data-value'),
  })));
  
  await browser.close();
  return data;
}
```

### API Testing

```typescript
import { request } from 'playwright';

async function testAPI() {
  const context = await request.newContext({
    baseURL: 'https://api.example.com',
    extraHTTPHeaders: {
      'Authorization': 'Bearer token123',
    },
  });
  
  // GET request
  const response = await context.get('/users');
  const users = await response.json();
  
  // POST request
  const createResponse = await context.post('/users', {
    data: { name: 'John', email: 'john@example.com' },
  });
  
  await context.dispose();
}
```

### E2E Testing

```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toHaveText('Welcome');
});
```

## Tags
`browser`, `testing`, `automation`, `e2e`, `scraping`

## Compatibility
- Codex: ✅
- Claude Code: ✅
