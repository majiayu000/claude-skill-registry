---
name: playwright-automation
description: Browser automation and testing with Playwright. Use when testing web applications, automating browser tasks, taking screenshots, or validating UI behavior.
allowed-tools: Read, Bash, Write, Edit
---
# Playwright Browser Automation

> Inspired by [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill) and [anthropics/skills](https://github.com/anthropics/skills)

## Purpose

Automate browser interactions for testing, scraping, and validation using Playwright.

## Core Workflow

### 1. Server Detection (for localhost testing)

```javascript
// Check if dev server is running
const http = require('http');

function checkServer(port) {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${port}`, (res) => {
      resolve(true);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(1000, () => {
      req.destroy();
      resolve(false);
    });
  });
}
```

### 2. Script Creation

Write test scripts to `/tmp/playwright-test-*.js`:

```javascript
const { chromium } = require('playwright');

(async () => {
  // Configuration
  const URL = 'http://localhost:3000';

  // Launch browser (visible by default)
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    // Navigate and wait for load
    await page.goto(URL);
    await page.waitForLoadState('networkidle');

    // Your automation here

  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: '/tmp/error-screenshot.png' });
  } finally {
    await browser.close();
  }
})();
```

### 3. Execution

```bash
# Run the script
node /tmp/playwright-test-*.js

# Or with npx
npx playwright test
```

## Common Patterns

### Screenshot Capture

```javascript
// Full page screenshot
await page.screenshot({
  path: '/tmp/screenshot.png',
  fullPage: true
});

// Element screenshot
const element = await page.locator('.hero-section');
await element.screenshot({ path: '/tmp/hero.png' });

// With timestamp
const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
await page.screenshot({ path: `/tmp/screenshot-${timestamp}.png` });
```

### Form Automation

```javascript
// Fill form fields
await page.fill('input[name="email"]', 'test@example.com');
await page.fill('input[name="password"]', 'secretpassword');

// Click submit
await page.click('button[type="submit"]');

// Wait for navigation
await page.waitForURL('**/dashboard');
```

### Login Flow

```javascript
async function login(page, email, password) {
  await page.goto('/login');
  await page.waitForLoadState('networkidle');

  await page.fill('#email', email);
  await page.fill('#password', password);
  await page.click('button:has-text("Sign In")');

  // Wait for redirect
  await page.waitForURL('**/dashboard', { timeout: 10000 });

  return page.url().includes('/dashboard');
}
```

### Responsive Testing

```javascript
const viewports = [
  { name: 'desktop', width: 1920, height: 1080 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'mobile', width: 375, height: 667 }
];

for (const viewport of viewports) {
  await page.setViewportSize({
    width: viewport.width,
    height: viewport.height
  });
  await page.screenshot({
    path: `/tmp/screenshot-${viewport.name}.png`
  });
}
```

### Link Checking

```javascript
async function checkLinks(page) {
  const links = await page.locator('a[href]').all();
  const results = [];

  for (const link of links) {
    const href = await link.getAttribute('href');
    if (href.startsWith('http')) {
      try {
        const response = await page.request.head(href);
        results.push({
          url: href,
          status: response.status(),
          ok: response.ok()
        });
      } catch (e) {
        results.push({ url: href, status: 'error', ok: false });
      }
    }
  }

  return results;
}
```

### Table Data Extraction

```javascript
async function extractTable(page, selector) {
  const rows = await page.locator(`${selector} tr`).all();
  const data = [];

  for (const row of rows) {
    const cells = await row.locator('td, th').allTextContents();
    data.push(cells);
  }

  return data;
}
```

### Console Log Capture

```javascript
// Listen to console messages
page.on('console', msg => {
  console.log(`[${msg.type()}] ${msg.text()}`);
});

// Listen to errors
page.on('pageerror', error => {
  console.error('Page error:', error.message);
});
```

## Selectors Best Practices

```javascript
// Prefer: Text content
await page.click('button:has-text("Submit")');

// Prefer: ARIA roles
await page.click('role=button[name="Submit"]');

// Prefer: Test IDs
await page.click('[data-testid="submit-button"]');

// Avoid: Complex CSS paths
// ❌ await page.click('div.container > form > div:nth-child(3) > button');
```

## Wait Strategies

```javascript
// Wait for network idle (recommended for SPAs)
await page.waitForLoadState('networkidle');

// Wait for specific element
await page.waitForSelector('.dashboard-loaded');

// Wait for response
await page.waitForResponse('**/api/data');

// Custom wait
await page.waitForFunction(() => {
  return document.querySelector('.loading') === null;
});

// Avoid: Fixed timeouts
// ❌ await page.waitForTimeout(5000);
```

## Error Handling

```javascript
try {
  await page.goto(URL, { timeout: 30000 });
  await page.waitForLoadState('networkidle');

  // Automation steps...

} catch (error) {
  console.error('Test failed:', error.message);

  // Capture failure state
  await page.screenshot({
    path: `/tmp/failure-${Date.now()}.png`,
    fullPage: true
  });

  // Capture HTML for debugging
  const html = await page.content();
  require('fs').writeFileSync('/tmp/failure-page.html', html);

} finally {
  await browser.close();
}
```

## Multi-Server Setup

```bash
# Start multiple servers in the background, run the test, then clean up.
set -euo pipefail

npm run dev > /tmp/playwright-dev.log 2>&1 &
DEV_PID=$!
npm run api > /tmp/playwright-api.log 2>&1 &
API_PID=$!

cleanup() {
  kill "$DEV_PID" "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT

wait_for_port() {
  local port="$1"
  node - "$port" <<'NODE'
const net = require("node:net");

const port = Number(process.argv[2]);
const deadline = Date.now() + 30000;

function attempt() {
  const socket = net.createConnection({ host: "127.0.0.1", port });
  let settled = false;

  const retry = () => {
    if (settled) return;
    settled = true;
    socket.destroy();
    if (Date.now() > deadline) {
      console.error(`Timed out waiting for port ${port}`);
      process.exit(1);
    }
    setTimeout(attempt, 250);
  };

  socket.setTimeout(1000);
  socket.on("connect", () => {
    settled = true;
    socket.end();
    process.exit(0);
  });
  socket.on("error", retry);
  socket.on("timeout", retry);
}

attempt();
NODE
}

wait_for_port 3000
wait_for_port 5000

node /tmp/playwright-test.js
```

## Quick Reference

```javascript
// Navigation
await page.goto(url);
await page.goBack();
await page.reload();

// Interactions
await page.click(selector);
await page.fill(selector, text);
await page.type(selector, text);  // With keystrokes
await page.press(selector, 'Enter');
await page.hover(selector);
await page.selectOption(selector, value);
await page.check(selector);  // Checkbox

// Assertions
await expect(page).toHaveTitle(/Dashboard/);
await expect(page.locator('.msg')).toHaveText('Success');
await expect(page.locator('button')).toBeEnabled();

// Information
const text = await page.textContent(selector);
const value = await page.inputValue(selector);
const visible = await page.isVisible(selector);
```
