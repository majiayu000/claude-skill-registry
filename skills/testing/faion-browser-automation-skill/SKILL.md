---
name: faion-browser-automation-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Browser Automation Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Provides comprehensive patterns for browser automation using Puppeteer and Playwright. Covers web scraping, E2E testing, screenshot/PDF generation, form automation, and headless browser operations.

## 3-Layer Architecture

```
Layer 1: Domain Skills - orchestrators
    ↓ call
Layer 2: Agents (faion-browser-agent) - executors
    ↓ use
Layer 3: Technical Skills (this) - tools
```

---

# Section 1: Puppeteer

## Overview

Puppeteer is Google's Node.js library for controlling Chrome/Chromium via DevTools Protocol.

**Installation:**
```bash
npm install puppeteer
# or for lighter version without bundled browser
npm install puppeteer-core
```

## Basic Setup

### Standard Launch

```javascript
const puppeteer = require('puppeteer');

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new', // or true for old headless, false for visible
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();
  await page.goto('https://example.com');

  // ... operations ...

  await browser.close();
}
```

### With Custom User Agent

```javascript
const page = await browser.newPage();
await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
await page.setViewport({ width: 1920, height: 1080 });
```

## Navigation

### Page Navigation

```javascript
// Navigate with options
await page.goto('https://example.com', {
  waitUntil: 'networkidle0', // or 'load', 'domcontentloaded', 'networkidle2'
  timeout: 30000
});

// Wait for navigation after click
await Promise.all([
  page.waitForNavigation({ waitUntil: 'networkidle0' }),
  page.click('a.nav-link')
]);

// Go back/forward
await page.goBack();
await page.goForward();

// Reload
await page.reload({ waitUntil: 'networkidle0' });
```

### Wait Strategies

```javascript
// Wait for selector
await page.waitForSelector('#element', { visible: true, timeout: 5000 });

// Wait for XPath
await page.waitForXPath('//button[contains(text(), "Submit")]');

// Wait for function
await page.waitForFunction(() => document.querySelector('#data').innerText !== '');

// Wait for network idle
await page.waitForNetworkIdle({ idleTime: 500 });

// Wait for response
await page.waitForResponse(response =>
  response.url().includes('/api/data') && response.status() === 200
);
```

## Selectors and Interaction

### Element Selection

```javascript
// CSS selectors
const element = await page.$('#id');           // Single element
const elements = await page.$$('.class');      // All matching

// Evaluate in page context
const text = await page.$eval('#title', el => el.textContent);
const texts = await page.$$eval('.items', els => els.map(el => el.textContent));

// Check existence
const exists = await page.$('#element') !== null;
```

### User Interactions

```javascript
// Click
await page.click('#button');
await page.click('#button', { button: 'right', clickCount: 2 });

// Type
await page.type('#input', 'Hello World', { delay: 100 });

// Clear and type
await page.click('#input', { clickCount: 3 });
await page.type('#input', 'New text');

// Keyboard
await page.keyboard.press('Enter');
await page.keyboard.down('Shift');
await page.keyboard.press('ArrowDown');
await page.keyboard.up('Shift');

// Mouse
await page.mouse.move(100, 200);
await page.mouse.click(100, 200);
await page.mouse.wheel({ deltaY: 500 });

// Hover
await page.hover('#menu-item');
```

## Form Handling

### Input Types

```javascript
// Text input
await page.type('#name', 'John Doe');

// Select dropdown
await page.select('#country', 'US');
await page.select('#multi', 'opt1', 'opt2'); // Multiple

// Checkbox/Radio
await page.click('#agree-checkbox');
await page.click('input[name="gender"][value="male"]');

// File upload
const input = await page.$('input[type="file"]');
await input.uploadFile('/path/to/file.pdf');

// Date input
await page.$eval('#date', (el, value) => el.value = value, '2026-01-18');
```

### Form Submission

```javascript
// Submit form
await page.click('button[type="submit"]');

// Or trigger form submit
await page.$eval('form', form => form.submit());

// Wait for response after submit
const [response] = await Promise.all([
  page.waitForNavigation(),
  page.click('button[type="submit"]')
]);
```

## Screenshot and PDF

### Screenshots

```javascript
// Full page
await page.screenshot({
  path: 'fullpage.png',
  fullPage: true
});

// Specific element
const element = await page.$('#chart');
await element.screenshot({ path: 'chart.png' });

// With options
await page.screenshot({
  path: 'screenshot.png',
  type: 'png', // or 'jpeg', 'webp'
  quality: 80, // jpeg/webp only
  clip: { x: 0, y: 0, width: 800, height: 600 },
  omitBackground: true // transparent background
});

// As base64
const base64 = await page.screenshot({ encoding: 'base64' });
```

### PDF Generation

```javascript
await page.pdf({
  path: 'document.pdf',
  format: 'A4', // or 'Letter', 'Legal', etc.
  printBackground: true,
  margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
  displayHeaderFooter: true,
  headerTemplate: '<div style="font-size:10px;text-align:center;width:100%;">Header</div>',
  footerTemplate: '<div style="font-size:10px;text-align:center;width:100%;"><span class="pageNumber"></span>/<span class="totalPages"></span></div>'
});

// Custom page size
await page.pdf({
  path: 'custom.pdf',
  width: '8.5in',
  height: '11in'
});
```

## Cookie and Session Management

### Cookies

```javascript
// Get all cookies
const cookies = await page.cookies();

// Get specific cookie
const sessionCookie = cookies.find(c => c.name === 'session_id');

// Set cookies
await page.setCookie({
  name: 'auth_token',
  value: 'abc123',
  domain: '.example.com',
  path: '/',
  httpOnly: true,
  secure: true
});

// Delete cookies
await page.deleteCookie({ name: 'auth_token' });

// Save and restore cookies
const cookies = await page.cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies));

const savedCookies = JSON.parse(fs.readFileSync('cookies.json'));
await page.setCookie(...savedCookies);
```

### Local/Session Storage

```javascript
// Set localStorage
await page.evaluate(() => {
  localStorage.setItem('key', 'value');
});

// Get localStorage
const value = await page.evaluate(() => localStorage.getItem('key'));

// Clear storage
await page.evaluate(() => {
  localStorage.clear();
  sessionStorage.clear();
});
```

## Request Interception

### Basic Interception

```javascript
await page.setRequestInterception(true);

page.on('request', request => {
  // Block images and CSS
  if (['image', 'stylesheet'].includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});

// Modify requests
page.on('request', request => {
  if (request.url().includes('/api/')) {
    request.continue({
      headers: {
        ...request.headers(),
        'Authorization': 'Bearer token123'
      }
    });
  } else {
    request.continue();
  }
});

// Mock responses
page.on('request', request => {
  if (request.url().endsWith('/api/data')) {
    request.respond({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ mocked: true })
    });
  } else {
    request.continue();
  }
});
```

### Response Handling

```javascript
page.on('response', async response => {
  if (response.url().includes('/api/data')) {
    const data = await response.json();
    console.log('API Response:', data);
  }
});
```

## Stealth Mode

### Using puppeteer-extra-plugin-stealth

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({ headless: true });
```

### Manual Evasion Techniques

```javascript
// Override webdriver property
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
});

// Override plugins
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
  });
});

// Override languages
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
  });
});
```

---

# Section 2: Playwright

## Overview

Playwright is Microsoft's cross-browser automation library supporting Chromium, Firefox, and WebKit.

**Installation:**
```bash
npm install playwright
# Install browsers
npx playwright install
```

## Basic Setup

### Standard Launch

```javascript
const { chromium, firefox, webkit } = require('playwright');

async function main() {
  // Choose browser
  const browser = await chromium.launch({
    headless: true,
    slowMo: 50 // slow down operations
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Custom User Agent'
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  await browser.close();
}
```

### Browser Contexts

```javascript
// Isolated context with storage state
const context = await browser.newContext({
  storageState: 'auth.json', // saved login state
  locale: 'en-US',
  timezoneId: 'America/New_York',
  geolocation: { longitude: -73.935242, latitude: 40.730610 },
  permissions: ['geolocation']
});

// Save storage state
await context.storageState({ path: 'auth.json' });
```

## Auto-Waiting

Playwright automatically waits for elements. No explicit waits needed for most operations.

```javascript
// These auto-wait for element to be actionable
await page.click('#button');      // waits for element, enabled, stable
await page.fill('#input', 'text'); // waits for element, enabled, editable
await page.check('#checkbox');    // waits for element, enabled, stable

// Explicit waits when needed
await page.waitForSelector('#dynamic-element');
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
await page.waitForFunction(() => window.dataLoaded === true);
```

## Selectors

### Selector Types

```javascript
// CSS
await page.click('#button');
await page.click('.class');

// Text
await page.click('text=Click me');
await page.click('text=/submit/i'); // regex

// XPath
await page.click('xpath=//button[@type="submit"]');

// Role (accessibility)
await page.click('role=button[name="Submit"]');
await page.click('role=link[name="Learn more"]');

// Chained selectors
await page.click('.parent >> .child');
await page.click('.form >> text=Submit');

// Has-text filter
await page.click('article:has-text("Breaking News")');

// Nth match
await page.click('.item >> nth=0'); // first
await page.click('.item >> nth=-1'); // last
```

### Locators (Recommended)

```javascript
// Create reusable locators
const submitButton = page.locator('button[type="submit"]');
const emailInput = page.locator('#email');

// Chain locators
const form = page.locator('form.login');
const username = form.locator('#username');
const password = form.locator('#password');

// Filter locators
const activeItems = page.locator('.item').filter({ hasText: 'Active' });
const specificRow = page.locator('tr').filter({ has: page.locator('td', { hasText: 'John' }) });

// Use locators
await emailInput.fill('user@example.com');
await submitButton.click();
```

## Form Handling

### Input Types

```javascript
// Text
await page.fill('#name', 'John Doe');

// Select
await page.selectOption('#country', 'US');
await page.selectOption('#multi', ['opt1', 'opt2']);

// Checkbox/Radio
await page.check('#agree');
await page.uncheck('#newsletter');
await page.setChecked('#terms', true);

// File upload
await page.setInputFiles('#upload', 'file.pdf');
await page.setInputFiles('#upload', ['file1.pdf', 'file2.pdf']);
await page.setInputFiles('#upload', []); // clear

// Date
await page.fill('#date', '2026-01-18');

// Content editable
await page.fill('[contenteditable]', 'Rich text content');
```

### Focus and Blur

```javascript
await page.focus('#input');
await page.blur('#input');

// Dispatch events
await page.dispatchEvent('#input', 'change');
```

## Screenshot and PDF

### Screenshots

```javascript
// Full page
await page.screenshot({ path: 'full.png', fullPage: true });

// Element
await page.locator('#chart').screenshot({ path: 'chart.png' });

// Options
await page.screenshot({
  path: 'screenshot.png',
  type: 'png',
  clip: { x: 0, y: 0, width: 800, height: 600 },
  omitBackground: true,
  animations: 'disabled', // wait for animations
  caret: 'hide', // hide text cursor
  scale: 'css' // or 'device'
});

// As buffer
const buffer = await page.screenshot();
```

### PDF Generation

```javascript
await page.pdf({
  path: 'document.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
  displayHeaderFooter: true,
  headerTemplate: '<div>Header</div>',
  footerTemplate: '<div><span class="pageNumber"></span></div>'
});
```

## Network Interception

### Route Handling

```javascript
// Block resources
await page.route('**/*.{png,jpg,jpeg}', route => route.abort());

// Modify requests
await page.route('**/api/**', route => {
  route.continue({
    headers: {
      ...route.request().headers(),
      'Authorization': 'Bearer token'
    }
  });
});

// Mock responses
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Mock User' }])
  });
});

// Modify response
await page.route('**/api/data', async route => {
  const response = await route.fetch();
  const json = await response.json();
  json.modified = true;
  route.fulfill({ response, json });
});
```

### Request/Response Events

```javascript
// Listen to requests
page.on('request', request => {
  console.log('>>', request.method(), request.url());
});

page.on('response', response => {
  console.log('<<', response.status(), response.url());
});

// Wait for specific response
const responsePromise = page.waitForResponse('**/api/data');
await page.click('#load-data');
const response = await responsePromise;
const data = await response.json();
```

## Video Recording

```javascript
const context = await browser.newContext({
  recordVideo: {
    dir: 'videos/',
    size: { width: 1280, height: 720 }
  }
});

const page = await context.newPage();
// ... perform actions ...

// Save video (closes page)
await page.close();
const video = await page.video();
const path = await video.path();
```

## Tracing

```javascript
// Start tracing
await context.tracing.start({
  screenshots: true,
  snapshots: true,
  sources: true
});

// ... perform actions ...

// Stop and save
await context.tracing.stop({ path: 'trace.zip' });

// View trace: npx playwright show-trace trace.zip
```

---

# Section 3: Web Scraping Techniques

## Element Extraction

### Basic Extraction

```javascript
// Single value
const title = await page.$eval('h1', el => el.textContent);
const href = await page.$eval('a.link', el => el.href);

// Multiple values
const items = await page.$$eval('.product', products =>
  products.map(p => ({
    name: p.querySelector('.name')?.textContent,
    price: p.querySelector('.price')?.textContent,
    image: p.querySelector('img')?.src
  }))
);

// Playwright locator approach
const texts = await page.locator('.item').allTextContents();
const count = await page.locator('.item').count();
```

### Table Extraction

```javascript
const tableData = await page.$$eval('table tbody tr', rows =>
  rows.map(row => {
    const cells = row.querySelectorAll('td');
    return {
      col1: cells[0]?.textContent?.trim(),
      col2: cells[1]?.textContent?.trim(),
      col3: cells[2]?.textContent?.trim()
    };
  })
);
```

### Attribute Extraction

```javascript
// Single attribute
const src = await page.$eval('img', el => el.getAttribute('src'));

// All attributes
const attrs = await page.$eval('#element', el =>
  Object.fromEntries(
    [...el.attributes].map(attr => [attr.name, attr.value])
  )
);
```

## Pagination Handling

### Next Button Pattern

```javascript
async function scrapeAllPages(page) {
  const allData = [];

  while (true) {
    // Scrape current page
    const data = await page.$$eval('.item', items =>
      items.map(item => item.textContent)
    );
    allData.push(...data);

    // Check for next button
    const nextButton = await page.$('a.next:not(.disabled)');
    if (!nextButton) break;

    // Click and wait
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      nextButton.click()
    ]);
  }

  return allData;
}
```

### Infinite Scroll Pattern

```javascript
async function scrapeInfiniteScroll(page) {
  let previousHeight = 0;
  const allData = [];

  while (true) {
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Wait for new content
    await page.waitForTimeout(2000);

    // Check if more content loaded
    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    if (newHeight === previousHeight) break;
    previousHeight = newHeight;

    // Extract new items
    const items = await page.$$eval('.item', els => els.map(e => e.textContent));
    allData.push(...items.slice(allData.length));
  }

  return allData;
}
```

### Load More Button Pattern

```javascript
async function scrapeLoadMore(page) {
  while (true) {
    const loadMoreBtn = await page.$('button.load-more');
    if (!loadMoreBtn) break;

    const isVisible = await loadMoreBtn.isIntersectingViewport();
    if (!isVisible) break;

    await loadMoreBtn.click();
    await page.waitForSelector('.item:nth-child(n+10)'); // wait for new items
  }

  return await page.$$eval('.item', items => items.map(i => i.textContent));
}
```

## Rate Limiting and Throttling

### Request Delay

```javascript
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapeWithDelay(urls, page) {
  const results = [];

  for (const url of urls) {
    await page.goto(url);
    const data = await extractData(page);
    results.push(data);

    // Random delay between 1-3 seconds
    await delay(1000 + Math.random() * 2000);
  }

  return results;
}
```

### Concurrent Requests with Limit

```javascript
const pLimit = require('p-limit');

async function scrapeWithConcurrency(urls, browser, concurrency = 3) {
  const limit = pLimit(concurrency);

  const tasks = urls.map(url =>
    limit(async () => {
      const page = await browser.newPage();
      try {
        await page.goto(url);
        return await extractData(page);
      } finally {
        await page.close();
      }
    })
  );

  return Promise.all(tasks);
}
```

## Proxy Rotation

### Single Proxy

```javascript
const browser = await puppeteer.launch({
  args: ['--proxy-server=http://proxy.example.com:8080']
});

// With authentication
const page = await browser.newPage();
await page.authenticate({
  username: 'proxyuser',
  password: 'proxypass'
});
```

### Proxy Pool Rotation

```javascript
const proxies = [
  'http://proxy1.example.com:8080',
  'http://proxy2.example.com:8080',
  'http://proxy3.example.com:8080'
];

let proxyIndex = 0;

async function getNextProxy() {
  const proxy = proxies[proxyIndex];
  proxyIndex = (proxyIndex + 1) % proxies.length;
  return proxy;
}

async function createBrowserWithProxy() {
  const proxy = await getNextProxy();
  return puppeteer.launch({
    args: [`--proxy-server=${proxy}`]
  });
}
```

### Playwright Proxy

```javascript
const browser = await chromium.launch({
  proxy: {
    server: 'http://proxy.example.com:8080',
    username: 'user',
    password: 'pass'
  }
});
```

---

# Section 4: Testing Patterns

## Page Object Model

### Page Object Class

```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = '#username';
    this.passwordInput = '#password';
    this.submitButton = 'button[type="submit"]';
    this.errorMessage = '.error-message';
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.page.fill(this.usernameInput, username);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }

  async getErrorMessage() {
    return await this.page.textContent(this.errorMessage);
  }

  async isLoggedIn() {
    return await this.page.isVisible('.dashboard');
  }
}

module.exports = { LoginPage };
```

### Using Page Objects

```javascript
const { LoginPage } = require('./pages/LoginPage');

describe('Login', () => {
  let loginPage;

  beforeEach(async () => {
    loginPage = new LoginPage(page);
    await loginPage.navigate();
  });

  test('successful login', async () => {
    await loginPage.login('user@example.com', 'password123');
    expect(await loginPage.isLoggedIn()).toBe(true);
  });

  test('invalid credentials', async () => {
    await loginPage.login('wrong@example.com', 'wrongpass');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });
});
```

## Playwright Test Framework

### Basic Test Structure

```javascript
// tests/example.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display title', async ({ page }) => {
    await expect(page).toHaveTitle(/Example/);
  });

  test('should navigate to about', async ({ page }) => {
    await page.click('text=About');
    await expect(page).toHaveURL(/.*about/);
  });
});
```

### Fixtures

```javascript
// fixtures/auth.js
const { test: base } = require('@playwright/test');

exports.test = base.extend({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth.json'
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('/admin/login');
    await page.fill('#username', 'admin');
    await page.fill('#password', 'adminpass');
    await page.click('button[type="submit"]');
    await use(page);
    await context.close();
  }
});
```

### Assertions

```javascript
const { test, expect } = require('@playwright/test');

test('assertions', async ({ page }) => {
  // Page assertions
  await expect(page).toHaveTitle('My App');
  await expect(page).toHaveURL(/dashboard/);

  // Element assertions
  await expect(page.locator('h1')).toHaveText('Welcome');
  await expect(page.locator('h1')).toContainText('Welc');
  await expect(page.locator('.item')).toHaveCount(5);
  await expect(page.locator('#button')).toBeVisible();
  await expect(page.locator('#button')).toBeEnabled();
  await expect(page.locator('#input')).toHaveValue('test');
  await expect(page.locator('#input')).toHaveAttribute('placeholder', 'Enter...');
  await expect(page.locator('.active')).toHaveClass(/selected/);

  // Soft assertions (continue on failure)
  await expect.soft(page.locator('h1')).toHaveText('Title');
  await expect.soft(page.locator('h2')).toHaveText('Subtitle');
});
```

---

# Section 5: Error Handling

## Retry Patterns

### Basic Retry

```javascript
async function retry(fn, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`Attempt ${i + 1} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Usage
const data = await retry(async () => {
  await page.goto('https://flaky-site.com');
  return await page.$eval('#data', el => el.textContent);
});
```

### Exponential Backoff

```javascript
async function retryWithBackoff(fn, maxRetries = 5, baseDelay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = baseDelay * Math.pow(2, i) + Math.random() * 1000;
      console.log(`Retry ${i + 1}/${maxRetries} in ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

## Navigation Error Handling

```javascript
async function safeNavigate(page, url, options = {}) {
  try {
    const response = await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 30000,
      ...options
    });

    if (!response.ok()) {
      throw new Error(`HTTP ${response.status()}: ${response.statusText()}`);
    }

    return response;
  } catch (error) {
    if (error.message.includes('net::ERR_')) {
      throw new Error(`Network error: ${error.message}`);
    }
    if (error.message.includes('Timeout')) {
      throw new Error(`Page load timeout: ${url}`);
    }
    throw error;
  }
}
```

## Element Interaction Error Handling

```javascript
async function safeClick(page, selector, options = {}) {
  const { timeout = 5000, retries = 3 } = options;

  for (let i = 0; i < retries; i++) {
    try {
      await page.waitForSelector(selector, { visible: true, timeout });
      await page.click(selector);
      return true;
    } catch (error) {
      if (i === retries - 1) {
        throw new Error(`Failed to click ${selector}: ${error.message}`);
      }
      await page.waitForTimeout(1000);
    }
  }
}

async function safeExtract(page, selector, defaultValue = null) {
  try {
    await page.waitForSelector(selector, { timeout: 5000 });
    return await page.$eval(selector, el => el.textContent?.trim());
  } catch {
    return defaultValue;
  }
}
```

## Browser Crash Recovery

```javascript
async function withBrowserRecovery(fn, options = {}) {
  const { maxRecoveries = 3, launchOptions = {} } = options;
  let browser = null;
  let recoveries = 0;

  while (recoveries < maxRecoveries) {
    try {
      if (!browser || !browser.isConnected()) {
        browser = await puppeteer.launch(launchOptions);
      }
      return await fn(browser);
    } catch (error) {
      if (error.message.includes('Target closed') ||
          error.message.includes('Session closed')) {
        recoveries++;
        console.log(`Browser crashed, recovery attempt ${recoveries}`);
        browser = null;
      } else {
        throw error;
      }
    }
  }

  throw new Error('Max browser recovery attempts exceeded');
}
```

---

# Section 6: Advanced Patterns

## Multi-Tab Handling

```javascript
// Open new tab
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();

// Switch between tabs
const pages = context.pages();
await pages[0].bringToFront();

// Close specific tab
await newPage.close();
```

## iFrame Handling

```javascript
// Puppeteer
const frameHandle = await page.waitForSelector('iframe#myframe');
const frame = await frameHandle.contentFrame();
await frame.click('#button-in-iframe');

// Playwright
const frame = page.frameLocator('iframe#myframe');
await frame.locator('#button-in-iframe').click();

// Multiple nested iframes
const nestedFrame = page
  .frameLocator('#outer-frame')
  .frameLocator('#inner-frame');
await nestedFrame.locator('#deep-button').click();
```

## Dialog Handling

```javascript
// Puppeteer
page.on('dialog', async dialog => {
  console.log(dialog.message());
  await dialog.accept('Input value'); // or dialog.dismiss()
});

// Playwright
page.on('dialog', dialog => dialog.accept());

// Handle specific dialog
const dialogPromise = page.waitForEvent('dialog');
await page.click('#trigger-alert');
const dialog = await dialogPromise;
await dialog.accept();
```

## Download Handling

### Puppeteer

```javascript
const downloadPath = '/tmp/downloads';
const client = await page.target().createCDPSession();
await client.send('Page.setDownloadBehavior', {
  behavior: 'allow',
  downloadPath
});

await page.click('#download-button');
// Wait for file...
```

### Playwright

```javascript
const downloadPromise = page.waitForEvent('download');
await page.click('#download-button');
const download = await downloadPromise;

// Save to specific path
await download.saveAs('/path/to/save/file.pdf');

// Get suggested filename
const filename = download.suggestedFilename();

// Get download stream
const stream = await download.createReadStream();
```

## Geolocation and Permissions

```javascript
// Playwright context
const context = await browser.newContext({
  geolocation: { longitude: -122.4194, latitude: 37.7749 },
  permissions: ['geolocation']
});

// Grant permissions
await context.grantPermissions(['geolocation', 'notifications'], {
  origin: 'https://example.com'
});

// Clear permissions
await context.clearPermissions();

// Puppeteer
await page.setGeolocation({ longitude: -122.4194, latitude: 37.7749 });

const context = browser.defaultBrowserContext();
await context.overridePermissions('https://example.com', ['geolocation']);
```

## Mobile Emulation

### Puppeteer

```javascript
const puppeteer = require('puppeteer');
const iPhone = puppeteer.devices['iPhone 12'];

const page = await browser.newPage();
await page.emulate(iPhone);
await page.goto('https://example.com');
```

### Playwright

```javascript
const { devices } = require('playwright');
const iPhone12 = devices['iPhone 12'];

const context = await browser.newContext({
  ...iPhone12
});

// Custom device
const context = await browser.newContext({
  viewport: { width: 375, height: 812 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0...',
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true
});
```

---

# Section 7: Performance and Optimization

## Memory Management

```javascript
// Close pages when done
await page.close();

// Limit concurrent pages
const MAX_PAGES = 5;
const semaphore = new Semaphore(MAX_PAGES);

async function processUrl(browser, url) {
  await semaphore.acquire();
  const page = await browser.newPage();
  try {
    await page.goto(url);
    return await extractData(page);
  } finally {
    await page.close();
    semaphore.release();
  }
}
```

## Disable Unnecessary Features

```javascript
// Puppeteer launch args for speed
const browser = await puppeteer.launch({
  args: [
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--no-sandbox',
    '--disable-accelerated-2d-canvas',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images', // if images not needed
    '--blink-settings=imagesEnabled=false'
  ]
});

// Block resources
await page.setRequestInterception(true);
page.on('request', request => {
  const blocked = ['image', 'stylesheet', 'font', 'media'];
  if (blocked.includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});
```

## Connection Pooling

```javascript
class BrowserPool {
  constructor(size = 5) {
    this.size = size;
    this.browsers = [];
    this.available = [];
  }

  async initialize() {
    for (let i = 0; i < this.size; i++) {
      const browser = await puppeteer.launch({ headless: true });
      this.browsers.push(browser);
      this.available.push(browser);
    }
  }

  async acquire() {
    while (this.available.length === 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return this.available.pop();
  }

  release(browser) {
    this.available.push(browser);
  }

  async close() {
    await Promise.all(this.browsers.map(b => b.close()));
  }
}
```

---

# Agents Called

| Agent | Purpose |
|-------|---------|
| faion-browser-agent | Execute browser automation tasks using this skill |

---

# Quick Reference

| Task | Puppeteer | Playwright |
|------|-----------|------------|
| Launch | `puppeteer.launch()` | `chromium.launch()` |
| New page | `browser.newPage()` | `context.newPage()` |
| Navigate | `page.goto(url)` | `page.goto(url)` |
| Click | `page.click(selector)` | `page.click(selector)` |
| Type | `page.type(sel, text)` | `page.fill(sel, text)` |
| Select | `page.select(sel, val)` | `page.selectOption(sel, val)` |
| Screenshot | `page.screenshot()` | `page.screenshot()` |
| PDF | `page.pdf()` | `page.pdf()` |
| Wait selector | `page.waitForSelector()` | `page.waitForSelector()` |
| Extract text | `page.$eval(sel, el => el.textContent)` | `page.textContent(sel)` |
| Extract all | `page.$$eval(sel, fn)` | `page.locator(sel).allTextContents()` |

---

*Browser Automation Skill v1.0 - 2026-01-18*
*Layer 3 Technical Skill - Used by faion-browser-agent*
*Covers: Puppeteer, Playwright, Web Scraping, Testing, Screenshots/PDF*
