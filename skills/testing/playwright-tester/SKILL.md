---
name: playwright-tester
description: Capture screenshots and run E2E tests with Playwright. Use for frontend debugging, visual inspection, or user flow validation. (project)
---

# Playwright Tester for Codel Text

Complete browser automation skill combining quick CLI screenshots with advanced JavaScript automation capabilities.

## When to Use

Use proactively when:
- User asks to view/screenshot a page
- Frontend behavior needs visual verification
- Testing user flows (login, onboarding, admin actions)
- Debugging UI issues
- Validating responsive design
- Running E2E tests
- Complex browser automation needed

## Setup (First Time)

```bash
cd .claude/skills/playwright-tester
npm run setup
```

This installs Playwright and Chromium browser. Only needed once.

## Project Configuration

**Default Frontend Server:** `http://100.93.144.78:5172` (Tailscale)
**Local Alternative:** `http://localhost:5172`

**Common Endpoints:**
- `/` - Home page
- `/admin` - Admin dashboard (call diagnostics)
- `/conversations` - Conversation list
- `/onboarding` - User onboarding flow

## Quick Screenshots (Simple Approach)

For fast, one-off screenshots, use the Playwright CLI directly:

### Basic Screenshot
```bash
playwright screenshot http://100.93.144.78:5172/admin /tmp/screenshot.png --viewport-size=1920,1080
```

### With Wait Time (for dynamic content)
```bash
playwright screenshot http://100.93.144.78:5172/admin /tmp/screenshot.png --viewport-size=1920,1080 --wait-for-timeout 3000
```

### Mobile View
```bash
playwright screenshot http://100.93.144.78:5172/admin /tmp/mobile.png --viewport-size=375,667
```

### Full Page Screenshot
```bash
playwright screenshot http://100.93.144.78:5172/admin /tmp/fullpage.png --full-page
```

### Common Viewports

| Device | Size |
|--------|------|
| Desktop HD | `--viewport-size=1920,1080` |
| Desktop | `--viewport-size=1280,720` |
| Tablet (iPad) | `--viewport-size=768,1024` |
| Mobile (iPhone) | `--viewport-size=375,667` |
| Mobile (Android) | `--viewport-size=360,640` |

## Advanced Automation (JavaScript Executor)

For complex tasks, write custom Playwright code and execute via `run.js`. The executor auto-wraps code and provides proper module resolution.

### Critical Workflow

**Step 1: Auto-detect dev servers (if testing localhost)**

```bash
cd .claude/skills/playwright-tester && node -e "require('./lib/helpers').detectDevServers().then(servers => console.log(JSON.stringify(servers)))"
```

- If **1 server found**: Use it automatically
- If **multiple servers found**: Ask user which to test
- If **no servers found**: Use default Tailscale IP or ask for URL

**Step 2: Write automation script to /tmp**

Always parameterize URLs at the top of the script:

```javascript
// /tmp/playwright-test-admin.js
const { chromium } = require('playwright');

// Project default or auto-detected
const TARGET_URL = 'http://100.93.144.78:5172';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/admin`);
  console.log('Page loaded:', await page.title());

  await page.screenshot({ path: '/tmp/admin-screenshot.png', fullPage: true });
  console.log('📸 Screenshot saved to /tmp/admin-screenshot.png');

  await browser.close();
})();
```

**Step 3: Execute from skill directory**

```bash
cd .claude/skills/playwright-tester && node run.js /tmp/playwright-test-admin.js
```

## Common Automation Patterns

### Test Responsive Design

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://100.93.144.78:5172';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 }
  ];

  for (const viewport of viewports) {
    console.log(`Testing ${viewport.name} (${viewport.width}x${viewport.height})`);

    await page.setViewportSize({
      width: viewport.width,
      height: viewport.height
    });

    await page.goto(TARGET_URL);
    await page.waitForTimeout(1000);

    await page.screenshot({
      path: `/tmp/${viewport.name.toLowerCase()}.png`,
      fullPage: true
    });
  }

  console.log('✅ All viewports tested');
  await browser.close();
})();
```

### Test Admin Dashboard Flow

```javascript
// /tmp/playwright-test-admin-flow.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

const TARGET_URL = 'http://100.93.144.78:5172';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  // Navigate to admin page
  await page.goto(`${TARGET_URL}/admin`);
  console.log('📍 Loaded admin page');

  // Wait for content to load
  await page.waitForSelector('text=CALL DIAGNOSTICS', { timeout: 10000 });
  console.log('✅ Call diagnostics section loaded');

  // Take screenshot
  await helpers.takeScreenshot(page, 'admin-dashboard');

  // Check for segments
  const segments = await page.locator('[data-testid="segment-card"]').count();
  console.log(`✅ Found ${segments} segment cards`);

  // Verify specific elements exist
  const hasUnhealthyMarker = await page.locator('text=Unhealthy').count();
  console.log(`✅ Health indicators: ${hasUnhealthyMarker > 0 ? 'Present' : 'Missing'}`);

  await browser.close();
})();
```

### Test Form Submission

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');
const helpers = require('./lib/helpers');

const TARGET_URL = 'http://100.93.144.78:5172';

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/contact`);

  // Use helpers for robust typing
  await helpers.safeType(page, 'input[name="name"]', 'John Doe');
  await helpers.safeType(page, 'input[name="email"]', 'john@example.com');
  await helpers.safeType(page, 'textarea[name="message"]', 'Test message');

  // Use helpers for robust clicking
  await helpers.safeClick(page, 'button[type="submit"]');

  // Verify submission
  await page.waitForSelector('.success-message', { timeout: 5000 });
  console.log('✅ Form submitted successfully');

  await browser.close();
})();
```

### Check for Broken Links

```javascript
// /tmp/playwright-test-links.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://100.93.144.78:5172';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(TARGET_URL);

  const links = await page.locator('a[href^="http"]').all();
  const results = { working: 0, broken: [] };

  for (const link of links) {
    const href = await link.getAttribute('href');
    try {
      const response = await page.request.head(href);
      if (response.ok()) {
        results.working++;
      } else {
        results.broken.push({ url: href, status: response.status() });
      }
    } catch (e) {
      results.broken.push({ url: href, error: e.message });
    }
  }

  console.log(`✅ Working links: ${results.working}`);
  if (results.broken.length > 0) {
    console.log(`❌ Broken links:`, results.broken);
  }

  await browser.close();
})();
```

## Available Helper Functions

The `lib/helpers.js` module provides robust utilities:

```javascript
const helpers = require('./lib/helpers');

// Auto-detect running dev servers (CRITICAL - use first!)
const servers = await helpers.detectDevServers();
console.log('Found servers:', servers);

// Safe click with retry logic
await helpers.safeClick(page, 'button.submit', { retries: 3 });

// Safe type with clear
await helpers.safeType(page, '#username', 'testuser');

// Take timestamped screenshot
await helpers.takeScreenshot(page, 'test-result');

// Handle cookie banners automatically
await helpers.handleCookieBanner(page);

// Extract table data
const data = await helpers.extractTableData(page, 'table.results');

// Authenticate user
await helpers.authenticate(page,
  { username: 'test@example.com', password: 'pass123' },
  { successIndicator: '.dashboard' }
);

// Scroll page
await helpers.scrollPage(page, 'bottom');

// Extract text from multiple elements
const texts = await helpers.extractTexts(page, '.item-title');

// Retry with exponential backoff
await helpers.retryWithBackoff(async () => {
  await page.click('.flaky-button');
}, 3, 1000);
```

## Inline Execution (Quick Tasks)

For simple one-off tasks, execute inline without creating files:

```bash
cd .claude/skills/playwright-tester && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://100.93.144.78:5172/admin');
await page.screenshot({ path: '/tmp/quick-admin.png', fullPage: true });
console.log('Screenshot saved');
await browser.close();
"
```

**When to use inline vs files:**
- **Inline**: Quick one-off tasks (screenshot, check element, get page title)
- **Files**: Complex tests, responsive checks, anything to re-run or share

## Frontend Server Management

### Start Dev Server
```bash
# From project root
cd frontend && npm run dev

# Specify port explicitly
cd frontend && npx vite --port 5172 --host 0.0.0.0
```

### Check if Running
```bash
# Check process
ps aux | grep vite | grep -v grep

# Check port
netstat -tlnp 2>/dev/null | grep 5172 || ss -tlnp 2>/dev/null | grep 5172

# Test endpoint
curl -s http://localhost:5172 | head -20
curl -s http://100.93.144.78:5172 | head -20
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Playwright not installed | Run `cd .claude/skills/playwright-tester && npm run setup` |
| Module not found | Ensure using `run.js` wrapper for JavaScript execution |
| Browser doesn't open | Verify `headless: false` in script |
| Connection refused | Start frontend: `cd frontend && npm run dev` |
| Blank screenshot | Increase wait timeout or use `--wait-for-selector` |
| Element not found | Add explicit wait: `await page.waitForSelector('.element', { timeout: 10000 })` |
| Frontend not on 5172 | Check port: `ps aux \| grep vite` |

## Decision Tree: CLI vs JavaScript

**Use CLI (playwright screenshot) when:**
- ✅ Taking a simple screenshot
- ✅ One-off visual check
- ✅ Don't need to interact with page
- ✅ No complex logic needed

**Use JavaScript (run.js) when:**
- ✅ Need to interact (click, type, navigate)
- ✅ Testing multi-step flows
- ✅ Need helper utilities
- ✅ Auto-detection of dev servers
- ✅ Complex assertions or data extraction
- ✅ Reusable test scripts

## Tips

- **CRITICAL: Detect servers first** - Run `detectDevServers()` before writing localhost tests
- **Write tests to /tmp** - Never clutter the project directory
- **Parameterize URLs** - Put TARGET_URL constant at top of every script
- **Default: Visible browser** - Use `headless: false` unless specifically requested otherwise
- **Slow down for debugging** - Use `slowMo: 100` to see actions clearly
- **Smart waits** - Use `waitForURL`, `waitForSelector`, not fixed timeouts
- **Error handling** - Use try-catch for robust automation
- **Console output** - Log progress with `console.log()`

## Quick Reference

```bash
# 🔥 Quick screenshot (CLI)
playwright screenshot http://100.93.144.78:5172/admin /tmp/admin.png --viewport-size=1920,1080 --wait-for-timeout 3000

# 🔥 Auto-detect servers (JavaScript)
cd .claude/skills/playwright-tester && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"

# 🔥 Execute automation script (JavaScript)
cd .claude/skills/playwright-tester && node run.js /tmp/playwright-test-mytest.js

# 🔥 Inline quick task (JavaScript)
cd .claude/skills/playwright-tester && node run.js "await page.goto('http://100.93.144.78:5172'); await page.screenshot({path: '/tmp/quick.png'});"

# Start frontend server
cd frontend && npm run dev

# Check server status
curl -s http://100.93.144.78:5172 | head -10
```

## Notes

- Default frontend URL: `http://100.93.144.78:5172` (Tailscale)
- Auto-detects localhost servers when available
- Progressive complexity: start with CLI, escalate to JavaScript when needed
- Test scripts written to `/tmp` for automatic cleanup
- Rich helper library for common automation patterns
- Browser visible by default for debugging (`headless: false`)
