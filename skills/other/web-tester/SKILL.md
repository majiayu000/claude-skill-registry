---
name: web-tester
description: Frontend testing with browser automation, assertions, and visual regression. Use when testing web UIs, validating user flows, checking responsive design, form submissions, login flows, or detecting visual regressions. Supports dev server auto-detection, assertion collection, and screenshot comparison.
---

# Web Tester

Browser-based frontend testing with Playwright. Test user flows, validate UI behavior, and detect visual regressions.

## Features

- **Browser automation** - Navigate, click, fill forms, take screenshots
- **Assertions** - Collect all test results, report failures at end
- **Visual diff** - Compare screenshots against baselines with perceptual diff
- **Dev server detection** - Auto-detect running local servers

## Setup (First Time)

```bash
cd $SKILL_DIR && npm run setup
```

This installs Playwright and Chromium. Only needed once.

## Quick Start

### 1. Detect dev servers

```bash
cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
```

### 2. Write test to /tmp

```javascript
// /tmp/test-homepage.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await helpers.createContext(browser);
  const page = await context.newPage();

  // Create test with assertions
  const test = helpers.createTest('Homepage Test');

  await page.goto('http://localhost:3000');
  
  test.assert(await page.title() !== '', 'Page has title');
  await test.assertVisible(page, 'nav', 'Navigation is visible');
  await test.assertText(page, 'h1', 'Welcome', 'Hero heading contains Welcome');

  // Visual regression check
  await helpers.compareScreenshot(page, 'homepage');

  await test.finish();
  await browser.close();
})();
```

### 3. Execute

```bash
cd $SKILL_DIR && node run.js /tmp/test-homepage.js
```

## Assertions API

Create a test to collect assertions:

```javascript
const test = helpers.createTest('My Test');

// Basic assertion
test.assert(condition, 'Description');

// Element visibility
await test.assertVisible(page, 'selector', 'Description');

// Text content
await test.assertText(page, 'selector', 'expected text', 'Description');

// URL check
await test.assertUrl(page, '/dashboard', 'Description');

// Element count
await test.assertCount(page, '.item', 5, 'Description');

// Attribute check
await test.assertAttribute(page, 'input', 'type', 'email', 'Description');

// Finish and save results
await test.finish();
```

Results are saved to `/tmp/test-results.json`.

### View results

```bash
cd $SKILL_DIR && node run.js --show-results
```

### Clear results

```bash
cd $SKILL_DIR && node run.js --clear-results
```

## Visual Regression API

Compare screenshots against baselines:

```javascript
await helpers.compareScreenshot(page, 'screenshot-name', {
  threshold: 0.5,              // Diff threshold % (default: 0.5)
  baselineDir: './baselines',  // Baseline folder (default: ./visual-baselines)
  fullPage: true               // Full page screenshot (default: true)
});
```

### Baseline workflow

1. **First run** - Creates baseline, marks as "pending approval"
2. **Subsequent runs** - Compares against baseline
3. **If different** - Saves `.current.png` and `.diff.png` for review

### Manage baselines

```bash
# List all baselines and their status
cd $SKILL_DIR && node run.js --list-baselines

# Approve all pending baselines (with confirmation)
cd $SKILL_DIR && node run.js --approve-baselines

# Approve specific baseline
cd $SKILL_DIR && node run.js --approve-baseline homepage

# Reject baseline (keep old, delete current/diff)
cd $SKILL_DIR && node run.js --reject-baseline homepage
```

## Common Patterns

### Test login flow

```javascript
// /tmp/test-login.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  const test = helpers.createTest('Login Flow');

  await page.goto('http://localhost:3000/login');

  await helpers.safeType(page, 'input[name="email"]', 'test@example.com');
  await helpers.safeType(page, 'input[name="password"]', 'password123');
  await helpers.safeClick(page, 'button[type="submit"]');

  await page.waitForURL('**/dashboard');
  await test.assertUrl(page, '/dashboard', 'Redirected to dashboard');
  await test.assertVisible(page, '.user-menu', 'User menu visible');

  await test.finish();
  await browser.close();
})();
```

### Test responsive design

```javascript
// /tmp/test-responsive.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const test = helpers.createTest('Responsive Design');

  const viewports = [
    { name: 'desktop', width: 1920, height: 1080 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'mobile', width: 375, height: 667 }
  ];

  for (const vp of viewports) {
    const context = await browser.newContext({ viewport: vp });
    const page = await context.newPage();

    await page.goto('http://localhost:3000');
    await helpers.compareScreenshot(page, `homepage-${vp.name}`);
    
    await test.assertVisible(page, 'nav', `Nav visible on ${vp.name}`);
    await context.close();
  }

  await test.finish();
  await browser.close();
})();
```

### Test form validation

```javascript
// /tmp/test-form.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  const test = helpers.createTest('Form Validation');

  await page.goto('http://localhost:3000/contact');

  // Submit empty form
  await helpers.safeClick(page, 'button[type="submit"]');
  await test.assertVisible(page, '.error-message', 'Shows error for empty form');

  // Fill and submit
  await helpers.safeType(page, 'input[name="email"]', 'test@example.com');
  await helpers.safeType(page, 'textarea[name="message"]', 'Hello');
  await helpers.safeClick(page, 'button[type="submit"]');

  await test.assertVisible(page, '.success-message', 'Shows success message');

  await test.finish();
  await browser.close();
})();
```

## Helper Functions

```javascript
const helpers = require('./lib/helpers');

// Browser setup
await helpers.launchBrowser('chromium', { headless: false });
await helpers.createContext(browser, { viewport: { width: 1920, height: 1080 } });
await helpers.createPage(context);

// Dev server detection
const servers = await helpers.detectDevServers();

// Safe interactions (with retry)
await helpers.safeClick(page, 'button', { retries: 3 });
await helpers.safeType(page, 'input', 'text', { clear: true });

// Page utilities
await helpers.waitForPageReady(page, { waitUntil: 'networkidle' });
await helpers.takeScreenshot(page, 'my-screenshot');
await helpers.handleCookieBanner(page);
await helpers.scrollPage(page, 'bottom');

// Data extraction
const texts = await helpers.extractTexts(page, '.list-item');
const tableData = await helpers.extractTableData(page, 'table');
```

## Inline Execution

For quick tests, run inline code:

```bash
cd $SKILL_DIR && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3000');
console.log('Title:', await page.title());
await takeScreenshot(page, 'quick-check');
await browser.close();
"
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VISUAL_BASELINE_DIR` | Baseline directory (default: `./visual-baselines`) |
| `HEADLESS` | Run browser headless if `true` (default: `false`) |
| `SLOW_MO` | Slow down actions by ms |
| `PW_HEADER_NAME` + `PW_HEADER_VALUE` | Add custom HTTP header |
| `PW_EXTRA_HEADERS` | JSON object of extra headers |

## CLI Reference

```bash
# Execute test file
node run.js /tmp/test.js

# Execute inline code
node run.js "await page.goto('...')"

# Baseline management
node run.js --list-baselines
node run.js --approve-baselines
node run.js --approve-baseline <name>
node run.js --reject-baseline <name>

# Results management
node run.js --show-results
node run.js --clear-results

# Help
node run.js --help
```

## Tips

- **Always detect servers first** for localhost testing
- **Write tests to /tmp** to avoid cluttering projects
- **Use `headless: false`** by default for easier debugging
- **Visual baselines** need human approval before becoming authoritative
- **Assertions continue on failure** - all results reported at end
