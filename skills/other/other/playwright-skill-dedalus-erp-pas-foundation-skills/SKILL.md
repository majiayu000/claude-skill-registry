---
name: playwright-skill
description: Complete browser automation and web testing with Playwright. Auto-detects dev servers, manages server lifecycle, writes clean test scripts to /tmp. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, debug dynamic webapps, automate any browser task. Use when user wants to test websites, automate browser interactions, validate web functionality, or perform any browser-based testing.
---

# Playwright Web Testing & Automation

Comprehensive web testing skill using Playwright. Write custom JavaScript code for any testing or automation task.

## Decision Tree: Choosing Your Approach

```
User task → Is server already running?
    ├─ Yes → Direct Testing
    │   ├─ Static HTML? → Navigate directly (file:// or http://)
    │   └─ Dynamic webapp? → Use Reconnaissance-Then-Action pattern
    │
    └─ No → Server Management Required
        ├─ Single server → Start server, then test
        └─ Multiple servers → Start all servers, coordinate testing
```

## CRITICAL WORKFLOW

1. **CheckTesting  if server is running** - Detect running dev servers OR start servers if needed
2. **Write scripts to /tmp** - NEVER write test files to skill directory; always use `/tmp/playwright-test-*.js`
3. **Use visible browser by default** - Always use `headless: false` unless user specifically requests headless mode
4. **Wait for dynamic content** - Use `waitForLoadState('networkidle')` before inspecting dynamic webapps
5. **Parameterize URLs** - Always make URLs configurable via constant at top of script

## Reconnaissance-Then-Action Pattern

For dynamic webapps where you don't know the DOM structure upfront:

```javascript
// /tmp/playwright-test-reconnaissance.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3000';

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // STEP 1: Navigate and wait for dynamic content
  await page.goto(TARGET_URL);
  await page.waitForLoadState('networkidle'); // CRITICAL for dynamic apps

  // STEP 2: Reconnaissance - discover what's on the page
  await page.screenshot({ path: '/tmp/inspect.png', fullPage: true });
  
  const buttons = await page.locator('button').all();
  console.log(`Found ${buttons.length} buttons`);
  
  for (let i = 0; i < buttons.length; i++) {
    const text = await buttons[i].textContent();
    console.log(`  Button ${i}: "${text}"`);
  }

  // STEP 3: Action - interact with discovered elements
  const loginButton = page.locator('button:has-text("Login")');
  if (await loginButton.isVisible()) {
    await loginButton.click();
    console.log('✅ Clicked login button');
  }

  await browser.close();
})();
```

## Server Management

### Check for Running Servers

```bash
# Check if port is in use
lsof -i :3000  # Mac/Linux
netstat -ano | findstr :3000  # Windows
```

### Start Server Before Testing

```javascript
// /tmp/playwright-test-with-server.js
const { chromium } = require('playwright');
const { spawn } = require('child_process');

const TARGET_URL = 'http://localhost:3000';

(async () => {
  // Start server
  console.log('Starting server...');
  const server = spawn('npm', ['run', 'dev'], { shell: true });
  
  server.stdout.on('data', (data) => console.log(`Server: ${data}`));
  server.stderr.on('data', (data) => console.error(`Server Error: ${data}`));

  // Wait for server to be ready
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Run tests
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto(TARGET_URL);
  await page.waitForLoadState('networkidle');
  
  // Your test logic here
  console.log('Title:', await page.title());
  
  await browser.close();
  
  // Clean up server
  server.kill();
  console.log('✅ Tests complete, server stopped');
})();
```

## Common Patterns

### Test a Page (Multiple Viewports)

```javascript
// /tmp/playwright-test-responsive.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detected

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 100 });
  const page = await browser.newPage();

  // Desktop test
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(TARGET_URL);
  console.log('Desktop - Title:', await page.title());
  await page.screenshot({ path: '/tmp/desktop.png', fullPage: true });

  // Mobile test
  await page.setViewportSize({ width: 375, height: 667 });
  await page.screenshot({ path: '/tmp/mobile.png', fullPage: true });

  await browser.close();
})();
```

### Test Login Flow

```javascript
// /tmp/playwright-test-login.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detected

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/login`);

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Wait for redirect
  await page.waitForURL('**/dashboard');
  console.log('✅ Login successful, redirected to dashboard');

  await browser.close();
})();
```

### Fill and Submit Form

```javascript
// /tmp/playwright-test-form.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detected

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const page = await browser.newPage();

  await page.goto(`${TARGET_URL}/contact`);

  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('textarea[name="message"]', 'Test message');
  await page.click('button[type="submit"]');

  // Verify submission
  await page.waitForSelector('.success-message');
  console.log('✅ Form submitted successfully');

  await browser.close();
})();
```

### Check for Broken Links

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000');

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
  console.log(`❌ Broken links:`, results.broken);

  await browser.close();
})();
```

### Take Screenshot with Error Handling

```javascript
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    await page.goto('http://localhost:3000', {
      waitUntil: 'networkidle',
      timeout: 10000,
    });

    await page.screenshot({
      path: '/tmp/screenshot.png',
      fullPage: true,
    });

    console.log('📸 Screenshot saved to /tmp/screenshot.png');
  } catch (error) {
    console.error('❌ Error:', error.message);
  } finally {
    await browser.close();
  }
})();
```

### Test Responsive Design

```javascript
// /tmp/playwright-test-responsive-full.js
const { chromium } = require('playwright');

const TARGET_URL = 'http://localhost:3001'; // Auto-detected

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  const viewports = [
    { name: 'Desktop', width: 1920, height: 1080 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Mobile', width: 375, height: 667 },
  ];

  for (const viewport of viewports) {
    console.log(
      `Testing ${viewport.name} (${viewport.width}x${viewport.height})`,
    );
 & Discovery

```javascript
// Check visibility
const isVisible = await page.locator('button').isVisible();

// Get text
const text = await page.locator('h1').textContent();

// Get attribute
const href = await page.locator('a').getAttribute('href');

// Find all elements
const allButtons = await page.locator('button').all();
const allLinks = await page.locator('a').all();

// Check if element exists
const count = await page.locator('.modal').count();
console.log(`Found ${count} modals`);
```

### Network & Console

```javascript
// Intercept requests
await page.route('**/api/**', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ mocked: true })
  });
});

// Wait for response
const response = await page.waitForResponse('**/api/data');
console.log(await response.json());

// Capture console logs
page.on('console', msg => {
  console.log(`Browser console [${msg.type()}]:`, msg.text());
});
```

## Best Practices

### ✅ DO

- **Wait for networkidle on dynamic apps** - Always use `page.waitForLoadState('networkidle')` before inspecting DOM on SPAs/React/Vue apps
- **Use reconnaissance pattern** - Take screenshot, inspect DOM, then act based on what you find
- **Visible browser by default** - Use `headless: false` for easier debugging
- **Descriptive selectors** - Use `text=`, `role=`, or data attributes over brittle CSS selectors
- **Error handling** - Wrap automation in try-catch blocks
- **Clean up resources** - Always close browser and kill servers

### ❌ DON'T

- **Don't inspect before networkidle** - On dynamic webapps, DOM may not be ready yet
- **Don't use fixed timeouts** - Use `waitForSelector()` or `waitForLoadState()` instead of arbitrary waits
- **Don't write to skill directory** - Always use `/tmp` for test scripts
- **Don't hardcode URLs** - Use constants at top of script for easy modificationeadless: false,  // Visible browser
  slowMo: 50       // Slow down by 50ms
});

const page = await browser.newPage();

// Navigate
await page.goto('https://example.com', {
  waitUntil: 'networkidle'  // Wait for network to be idle
});

// Close
await browser.close();
```

### Selectors & Interactions

```javascript
// Click
await page.click('button.submit');
await page.dblclick('.item');

// Fill input
await page.fill('input[name="email"]', 'test@example.com');
await page.getByLabel('Email').fill('user@example.com');

// Checkbox
await page.check('input[type="checkbox"]');
await page.uncheck('input[type="checkbox"]');

// Select dropdown
await page.selectOption('select#country', 'usa');

// Type with delay
await page.type('#username', 'testuser', { delay: 100 });
```

### Waiting Strategies

```javascript
// Wait for navigation
await page.waitForURL('**/dashboard');
await page.waitForLoadState('networkidle');

// Wait for element
await page.waitForSelector('.success-message');
await page.waitForSelector('.spinner', { state: 'hidden' });

// Wait for timeout (use sparingly)
await page.waitForTimeout(1000);
```

### Screenshots

```javascript
// Full page screenshot
await page.screenshot({
  path: '/tmp/screenshot.png',
  fullPage: true
});

// Element screenshot
await page.locator('.chart').screenshot({
  path: '/tmp/chart.png'
});
```Quick Tips

- **Visible browser** - Always `headless: false` unless explicitly requested
- **Write to /tmp** - Scripts go to `/tmp/playwright-test-*.js`, never to project directories
- **Parameterize URLs** - Use `TARGET_URL` constant at top of script
- **Slow down** - Use `slowMo: 100` to see actions in real-time
- **Wait smart** - Use `waitForLoadState('networkidle')` for dynamic apps before inspecting
- **Error handling** - Wrap in try-catch with proper cleanup in finally block
- **Progress feedback** - Use `console.log()` to
const text = await page.locator('h1').textContent();

// Get attribute
const href = await page.locator('a').getAttribute('href');
```

### Network

```javascript
// Intercept requests
await page.route('**/api/**', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ mocked: true })
  });
});

// Wait for response
const response = await page.waitForResponse('**/api/data');
console.log(await response.json());
```

## Tips

- **DEFAULT: Visible browser** - Always use `headless: false` unless user explicitly asks for headless mode
- **Use /tmp for test files** - Write to `/tmp/playwright-test-*.js`, never to skill directory or user's project
- **Parameterize URLs** - Put detected/provided URL in a `TARGET_URL` constant at the top of every script
- **Slow down:** Use `slowMo: 100` to make actions visible and easier to follow
- **Wait strategies:** Use `waitForURL`, `waitForSelector`, `waitForLoadState` instead of fixed timeouts
- **Error handling:** Always use try-catch for robust automation
- **Console output:** Use `console.log()` to track progress and show what's happening

## Common Use Cases

**Visual Testing:**
- Take screenshots at different viewports
- Compare visual changes
- Test responsive design

**Functional Testing:**
- Test login flows
- Form validation
- Navigation flows
- Error handling

**Validation:**
- Check for broken links
- Verify images load
- Test page load times
- Check accessibility

**Automation:**
- Fill forms automatically
- Click through user flows
- Extract data from pages
- Generate reports

## Notes

- Each automation is custom-written for your specific request
- Not limited to pre-built scripts - any browser task possible
- Auto-detects running dev servers to eliminate hardcoded URLs
- Test scripts written to `/tmp` for automatic cleanup (no clutter)
- Progressive disclosure - load advanced documentation only when needed

## References

- [Playwright Documentation](https://playwright.dev)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Best Practices](https://playwright.dev/docs/best-practices)
