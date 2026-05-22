---
name: playwright
description: General-purpose browser automation skill for Playwright. Use this skill when the user wants to automate browser tasks like testing login flows, scraping data, taking screenshots, filling forms, clicking elements, or any interactive web automation. This skill provides smart utilities for session management, error handling, and development server detection. NOT for scheduled monitoring (use web-monitor-bot instead).
---

# Playwright Browser Automation

## Overview

This skill enables general-purpose browser automation using Playwright. It's designed for one-off automation tasks, interactive testing, and ad-hoc browser scripting. The skill includes intelligent utilities for session persistence, error handling, server detection, and common automation patterns extracted from production bots.

## When to Use This Skill

Invoke this skill when the user requests:
- "Automate logging into this website"
- "Take screenshots of this page"
- "Fill out this form automatically"
- "Test this login flow"
- "Extract data from this website"
- "Click through this multi-step process"
- Any interactive browser automation task

**DO NOT use for scheduled monitoring** - use the `web-monitor-bot` skill instead for cron-based periodic checks with analytics.

## Quick Start

### 1. Installation

Install dependencies in your project or test directory:

```bash
npm install playwright playwright-extra puppeteer-extra-plugin-stealth dotenv
npx playwright install chromium
```

### 2. Run a Script

Execute automation scripts using the provided runner:

```bash
node run.js path/to/your-script.js
```

Or run inline code:

```bash
node run.js "await page.goto('https://example.com'); await page.screenshot({ path: 'screenshot.png' });"
```

Or pipe code via stdin:

```bash
cat script.js | node run.js
```

### 3. Use Helper Utilities

Import the utilities library for advanced patterns:

```javascript
const utils = require('./lib/utils.js');

// Safe click with retry
await utils.safeClick(page, 'button.submit', { retries: 3 });

// Type with human-like delays
await utils.humanType(page, '#email', 'user@example.com');

// Session management
await utils.saveCookies(context, 'session.json');
await utils.loadCookies(context, 'session.json');

// Screenshot with error handling
await utils.captureScreenshot(page, 'step-1.png');
```

## Core Features

### Session Persistence

Save and restore browser sessions to avoid repeated logins:

```javascript
const { saveCookies, loadCookies } = require('./lib/utils.js');

// After successful login
await saveCookies(context, 'my-session.json');

// On subsequent runs
const hasCookies = await loadCookies(context, 'my-session.json');
if (hasCookies) {
  console.log('Session restored!');
  await page.goto(protectedUrl);
} else {
  // Perform login
}
```

**Benefits:**
- Skip login flows on repeated runs
- Maintain authentication state
- Avoid rate limiting from frequent logins
- Faster execution times

### Development Server Detection

Automatically detect running development servers before executing scripts:

```javascript
const { detectDevServers } = require('./lib/utils.js');

const servers = await detectDevServers();
if (servers.length > 0) {
  console.log('Found servers:', servers);
  // Use detected server URLs in your automation
}
```

### Stealth Mode

Built-in stealth plugin to bypass basic bot detection:

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();

chromium.use(stealth);

const browser = await chromium.launch({
  headless: false,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});
```

### Error Handling & Retries

Robust error handling with automatic retries:

```javascript
const { retryWithBackoff } = require('./lib/utils.js');

// Retry an operation up to 3 times with exponential backoff
const result = await retryWithBackoff(async () => {
  await page.waitForSelector('.dynamic-content', { timeout: 10000 });
  return await page.textContent('.dynamic-content');
}, { maxRetries: 3, initialDelay: 1000 });
```

## Common Automation Patterns

### Pattern 1: Login Flow Automation

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
const { saveCookies, loadCookies, humanType, safeClick } = require('./lib/utils.js');

chromium.use(stealth);

const browser = await chromium.launch({ headless: false });
const context = await browser.newContext();
const page = await context.newPage();

// Try to load saved session
const hasCookies = await loadCookies(context, 'session.json');

if (!hasCookies) {
  // Perform login
  await page.goto('https://example.com/login');
  await humanType(page, '#email', 'user@example.com');
  await humanType(page, '#password', 'password123');
  await safeClick(page, 'button[type="submit"]');

  await page.waitForNavigation();

  // Save session for next time
  await saveCookies(context, 'session.json');
  console.log('Login successful, session saved!');
} else {
  console.log('Using saved session');
  await page.goto('https://example.com/dashboard');
}

await browser.close();
```

### Pattern 2: Form Filling & Submission

```javascript
const { humanType, safeClick, captureScreenshot } = require('./lib/utils.js');

await page.goto('https://example.com/form');

// Fill form fields with human-like typing
await humanType(page, '#name', 'John Doe');
await humanType(page, '#email', 'john@example.com', { delay: 50 });
await page.selectOption('#country', 'US');
await page.check('#terms');

// Screenshot before submission
await captureScreenshot(page, 'before-submit.png');

// Submit with retry logic
await safeClick(page, 'button#submit', { retries: 3 });

// Wait for success
await page.waitForSelector('.success-message', { timeout: 15000 });
await captureScreenshot(page, 'after-submit.png');
```

### Pattern 3: Data Extraction

```javascript
const { retryWithBackoff } = require('./lib/utils.js');

await page.goto('https://example.com/data');

// Extract data with retry logic
const data = await retryWithBackoff(async () => {
  await page.waitForSelector('.data-table', { timeout: 10000 });

  const rows = await page.$$('.data-table tr');
  const results = [];

  for (const row of rows) {
    const cells = await row.$$('td');
    const rowData = await Promise.all(cells.map(cell => cell.textContent()));
    results.push(rowData);
  }

  return results;
}, { maxRetries: 3 });

console.log('Extracted data:', data);
```

### Pattern 4: Multi-Step Workflow

```javascript
const { safeClick, humanType, captureScreenshot } = require('./lib/utils.js');

// Step 1: Search
await page.goto('https://example.com');
await humanType(page, '#search', 'playwright automation');
await safeClick(page, 'button.search');
await page.waitForTimeout(2000);
await captureScreenshot(page, 'step-1-search.png');

// Step 2: Filter results
await safeClick(page, '.filter-option[data-filter="recent"]');
await page.waitForTimeout(1000);
await captureScreenshot(page, 'step-2-filtered.png');

// Step 3: Select item
await safeClick(page, '.result-item:first-child');
await page.waitForNavigation();
await captureScreenshot(page, 'step-3-details.png');

// Step 4: Complete action
await safeClick(page, 'button.add-to-cart');
await page.waitForSelector('.cart-notification', { timeout: 5000 });
await captureScreenshot(page, 'step-4-added.png');
```

### Pattern 5: Screenshot Capture with Responsive Testing

```javascript
const { captureScreenshot } = require('./lib/utils.js');

const viewports = [
  { width: 1920, height: 1080, name: 'desktop' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 375, height: 667, name: 'mobile' }
];

for (const viewport of viewports) {
  await page.setViewportSize({ width: viewport.width, height: viewport.height });
  await page.goto('https://example.com');
  await captureScreenshot(page, `screenshot-${viewport.name}.png`);
}
```

### Pattern 6: Cloudflare Challenge Handling (Production-Ready)

```javascript
const { detectCloudflare, saveCookies } = require('./lib/utils.js');

await page.goto('https://protected-site.com');

// Intelligent Cloudflare detection with 90s polling
try {
  const wasBlocked = await detectCloudflare(page, context, 'initial page load', {
    maxWaitSeconds: 90,        // Poll for up to 90 seconds
    pollIntervalSeconds: 10,   // Check every 10 seconds
    cookiePath: 'session.json' // Save cookies immediately after solve
  });

  if (wasBlocked) {
    console.log('Cloudflare challenge auto-solved! Proceeding...');
  } else {
    console.log('No Cloudflare challenge detected');
  }

  // Continue with automation
  await page.click('.protected-button');

} catch (error) {
  // Challenge not solved after 90s
  console.error('Cloudflare blocked:', error.message);
  // Screenshots auto-saved: cloudflare-detected.png, cloudflare-timeout.png
  process.exit(1);
}
```

**Features:**
- **Smart polling**: Checks every 10s for up to 90s (not single wait)
- **Block tracking**: Tracks consecutive/total blocks in `cloudflare-blocks.json`
- **Auto-screenshots**: `cloudflare-detected.png` (when detected), `cloudflare-cleared.png` (when solved), `cloudflare-timeout.png` (if fails)
- **Cookie persistence**: Saves session immediately after challenge clears
- **Progress updates**: Console logs every 30s during wait

**Block Tracking:**
```javascript
const { getCloudflareBlocks } = require('./lib/utils.js');

const blocks = getCloudflareBlocks();
console.log(`Consecutive blocks: ${blocks.consecutive}`);
console.log(`Total blocks: ${blocks.total}`);
console.log(`Last 10 events:`, blocks.history.slice(-10));
```

## Utility Functions Reference

### Session Management

```javascript
// Save browser cookies to file
await saveCookies(context, filepath);

// Load browser cookies from file
const restored = await loadCookies(context, filepath);
// Returns: true if cookies were loaded, false if file doesn't exist
```

### Safe Interactions

```javascript
// Click with automatic retry and error handling
await safeClick(page, selector, { retries: 3, timeout: 10000 });

// Click with human-like mouse movement (curved path + random position)
await humanClick(page, selector, { timeout: 10000 });

// Type with human-like delays (randomized between chars)
await humanType(page, selector, text, { delay: 100 });

// Generate random delay for timing variation
const delay = randomDelay(1000, 2500); // Returns random ms between 1000-2500
await page.waitForTimeout(delay);
```

### Screenshots

```javascript
// Capture screenshot with automatic error handling
await captureScreenshot(page, filepath);
```

### Retry Logic

```javascript
// Retry async operation with exponential backoff
const result = await retryWithBackoff(asyncFunction, {
  maxRetries: 3,
  initialDelay: 1000,
  backoffMultiplier: 2
});
```

### Server Detection

```javascript
// Detect running development servers on localhost
const servers = await detectDevServers();
// Returns: Array of { port, url } objects
```

## Advanced Configuration

### Timeout Strategies

Implement dynamic timeouts based on conditions:

```javascript
const isPeakTime = new Date().getHours() === 17; // 5 PM
const timeout = isPeakTime ? 60000 : 30000;

await page.goto(url, { timeout });
await page.waitForSelector(selector, { timeout });
```

### Headless vs. Headed Mode

```javascript
// Headed (visible browser) - useful for debugging
const browser = await chromium.launch({ headless: false });

// Headless (background) - useful for production/CI
const browser = await chromium.launch({ headless: true });
```

### Custom User Agents

```javascript
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
});
```

### Browser Arguments

```javascript
const browser = await chromium.launch({
  headless: false,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled'
  ]
});
```

## Best Practices

### 1. Use Session Persistence

Always save cookies after authentication to speed up subsequent runs:

```javascript
// After login
await saveCookies(context, 'session.json');

// Before automation
const hasCookies = await loadCookies(context, 'session.json');
```

### 2. Implement Retry Logic

Use retries for flaky network requests or dynamic content:

```javascript
await retryWithBackoff(async () => {
  await page.waitForSelector('.dynamic-element', { timeout: 10000 });
  return await page.textContent('.dynamic-element');
}, { maxRetries: 3 });
```

### 3. Capture Screenshots on Errors

Always save evidence when things go wrong:

```javascript
try {
  await page.click('.submit-button');
} catch (error) {
  await captureScreenshot(page, 'error.png');
  throw error;
}
```

### 4. Use Human-Like Interactions

Avoid detection by simulating natural human behavior:

```javascript
const { humanClick, humanType, randomDelay } = require('./lib/utils.js');

// Bad: Instant, robotic interactions
await page.fill('#input', text);
await page.click('button');

// Good: Human-like behavior
await humanType(page, '#input', text, { delay: 50 });
await page.waitForTimeout(randomDelay(500, 1500)); // Random pause
await humanClick(page, 'button'); // Mouse movement + random click position
```

**Anti-Detection Checklist:**
- ✅ Use `humanClick()` instead of `.click()` (adds mouse movement)
- ✅ Use `humanType()` instead of `.fill()` (adds typing delays)
- ✅ Use `randomDelay()` for all `waitForTimeout()` calls (avoid fixed timing)
- ✅ Add random pauses between actions (humans don't act instantly)
- ✅ Handle Cloudflare with `detectCloudflare()` (smart polling + tracking)

### 5. Clean Up Resources

Always close browsers and remove temporary files:

```javascript
try {
  // ... automation code ...
} finally {
  await browser.close();
  // Clean up lock files, temp files, etc.
}
```

## File Organization

Recommended structure for automation projects:

```
my-automation/
├── run.js              # Script runner
├── lib/
│   └── utils.js        # Utility functions
├── scripts/
│   ├── login.js        # Login automation
│   ├── scrape.js       # Data extraction
│   └── test-flow.js    # Test workflows
├── sessions/
│   └── cookies.json    # Saved sessions
├── screenshots/        # Captured images
├── .env                # Environment variables
└── package.json
```

## Environment Variables

Use `.env` files for configuration:

```bash
# .env
TARGET_URL=https://example.com
LOGIN_EMAIL=user@example.com
LOGIN_PASSWORD=secretpass
HEADLESS=false
TIMEOUT=30000
```

Load in scripts:

```javascript
require('dotenv').config();

const targetUrl = process.env.TARGET_URL;
const headless = process.env.HEADLESS === 'true';
const timeout = parseInt(process.env.TIMEOUT) || 30000;
```

## Troubleshooting

### Script not finding elements

1. Use `page.waitForSelector()` before interactions
2. Increase timeout values for slow-loading pages
3. Verify selectors in browser DevTools
4. Use `captureScreenshot()` to see page state

### Bot detection issues

1. Enable stealth mode with `playwright-extra`
2. Use `humanType()` instead of `fill()`
3. Add random delays: `await page.waitForTimeout(Math.random() * 2000 + 1000)`
4. Use realistic user agents
5. Handle Cloudflare challenges with manual intervention pattern

### Session not persisting

1. Ensure cookies are saved after successful login
2. Check file permissions on cookie file
3. Verify cookie expiration times
4. Re-login and save fresh cookies

### Timeouts on slow pages

1. Increase timeout values: `{ timeout: 60000 }`
2. Use `waitUntil: 'domcontentloaded'` instead of `'load'`
3. Implement retry logic with backoff
4. Check network tab for slow requests

## Comparison with web-monitor-bot

| Feature | playwright (this skill) | web-monitor-bot |
|---------|------------------------|-----------------|
| **Use Case** | One-off automation tasks | Scheduled monitoring |
| **Execution** | Manual/on-demand | Cron-based periodic |
| **Analytics** | No | Yes (built-in dashboard) |
| **Notifications** | Manual implementation | Slack/webhook integration |
| **Session Management** | Yes (utilities) | Yes (built-in) |
| **Concurrency Control** | Manual | Lock files (built-in) |
| **Best For** | Testing, scraping, workflows | Availability tracking, alerts |

## Examples

See the `examples/` directory for complete working scripts:

- `examples/login-flow.js` - Full login automation with session persistence
- `examples/form-submission.js` - Multi-step form filling
- `examples/data-extraction.js` - Scraping with retry logic
- `examples/screenshot-tool.js` - Responsive screenshot capture
- `examples/cloudflare-handler.js` - Handling bot protection

## Resources

### Dependencies
- [Playwright](https://playwright.dev/) - Browser automation framework
- [playwright-extra](https://github.com/berstend/puppeteer-extra/tree/master/packages/playwright-extra) - Plugin support
- [puppeteer-extra-plugin-stealth](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth) - Bot detection bypass

### Documentation
- [Playwright API Docs](https://playwright.dev/docs/api/class-playwright)
- [Selectors Guide](https://playwright.dev/docs/selectors)
- [Best Practices](https://playwright.dev/docs/best-practices)

## License

MIT
