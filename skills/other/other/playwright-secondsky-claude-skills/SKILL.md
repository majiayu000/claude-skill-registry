---
name: playwright
description: Browser automation and E2E testing with Playwright. Auto-detects dev servers, writes clean test scripts. Test pages, fill forms, take screenshots, check responsive design, validate UX, test login flows, check links, automate any browser task. Use for cross-browser testing, visual regression, API testing, component testing in TypeScript/JavaScript and Python projects.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, TodoWrite
---

# Playwright - Browser Automation & E2E Testing

Expert knowledge for browser automation and end-to-end testing with Playwright - a modern cross-browser testing framework.

**IMPORTANT - Path Resolution:**
This skill can be installed in different locations. Before executing commands, determine the skill directory based on where you loaded this SKILL.md file, and use that path in all commands. Replace `$SKILL_DIR` with the actual discovered path.

Common installation paths:
- Plugin system: `~/.claude/plugins/*/playwright/skills/playwright`
- Manual global: `~/.claude/skills/playwright`
- Project-specific: `<project>/.claude/skills/playwright`

## CRITICAL WORKFLOW - Follow These Steps

When automating browser tasks:

1. **Auto-detect dev servers** - For localhost testing, ALWAYS run server detection FIRST:
   ```bash
   cd $SKILL_DIR && node -e "require('./lib/helpers').detectDevServers().then(servers => console.log(JSON.stringify(servers)))"
   ```
   - If **1 server found**: Use it automatically, inform user
   - If **multiple servers found**: Ask user which one to test
   - If **no servers found**: Ask for URL or offer to help start dev server

2. **Write scripts to /tmp** - NEVER write test files to skill directory; always use `/tmp/playwright-test-*.js`

3. **Use visible browser by default** - Always use `headless: false` unless user specifically requests headless mode

4. **Parameterize URLs** - Always make URLs configurable via constant at top of script

5. **Execute via run.js** - Always run: `cd $SKILL_DIR && node run.js /tmp/playwright-test-*.js`

## Quick Start

### First-Time Setup

```bash
# Navigate to skill directory
cd $SKILL_DIR

# Install using bun (preferred)
bun run setup

# Or using npm
npm run setup:npm
```

This installs Playwright and Chromium browser. Only needed once.

### Installation (For E2E Testing Projects)

```bash
# Using Bun (preferred)
bun add -d @playwright/test
bunx playwright install

# Using npm
npm init playwright@latest
```

### Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'bun run dev',
    url: 'http://localhost:3000',
  },
})
```

## Browser Automation Patterns

### How It Works

1. You describe what you want to test/automate
2. I auto-detect running dev servers (or ask for URL)
3. I write custom Playwright code in `/tmp/playwright-test-*.js`
4. I execute it via: `cd $SKILL_DIR && node run.js /tmp/playwright-test-*.js`
5. Results displayed in real-time, browser window visible

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

Execute: `cd $SKILL_DIR && node run.js /tmp/playwright-test-responsive.js`

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

  await page.waitForURL('**/dashboard');
  console.log('✅ Login successful, redirected to dashboard');

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

## E2E Testing Patterns

### Running Tests

```bash
# Run all tests
bunx playwright test

# Headed mode (see browser)
bunx playwright test --headed

# Specific file
bunx playwright test tests/login.spec.ts

# Debug mode
bunx playwright test --debug

# UI mode (interactive)
bunx playwright test --ui

# Specific browser
bunx playwright test --project=chromium

# Generate report
bunx playwright show-report
```

### Writing Tests

```typescript
import { test, expect } from '@playwright/test'

test.describe('Login flow', () => {
  test('successful login', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('link', { name: 'Login' }).click()
    await page.getByLabel('Email').fill('user@example.com')
    await page.getByLabel('Password').fill('password123')
    await page.getByRole('button', { name: 'Sign in' }).click()

    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
  })

  test('shows error for invalid credentials', async ({ page }) => {
    await page.goto('/login')
    await page.getByLabel('Email').fill('wrong@example.com')
    await page.getByLabel('Password').fill('wrongpassword')
    await page.getByRole('button', { name: 'Sign in' }).click()

    await expect(page.getByText('Invalid credentials')).toBeVisible()
  })
})
```

## Selectors (Best Practices)

```typescript
// ✅ Role-based (recommended)
await page.getByRole('button', { name: 'Submit' })
await page.getByRole('link', { name: 'Home' })

// ✅ Text/Label
await page.getByText('Hello World')
await page.getByLabel('Email')

// ✅ Test ID (fallback)
await page.getByTestId('submit-button')

// ❌ Avoid CSS selectors (brittle)
await page.locator('.btn-primary')
```

## Assertions

```typescript
// Visibility
await expect(page.getByText('Success')).toBeVisible()
await expect(page.getByRole('button')).toBeEnabled()

// Text
await expect(page.getByRole('heading')).toHaveText('Welcome')
await expect(page.getByRole('alert')).toContainText('error')

// Attributes
await expect(page.getByRole('link')).toHaveAttribute('href', '/home')

// URL/Title
await expect(page).toHaveURL('/dashboard')
await expect(page).toHaveTitle('Dashboard')

// Count
await expect(page.getByRole('listitem')).toHaveCount(5)
```

## Actions

```typescript
// Clicking
await page.getByRole('button').click()
await page.getByText('File').dblclick()

// Typing
await page.getByLabel('Email').fill('user@example.com')
await page.getByLabel('Search').press('Enter')

// Selecting
await page.getByLabel('Country').selectOption('us')

// File Upload
await page.getByLabel('Upload').setInputFiles('path/to/file.pdf')
```

## Network Mocking

```typescript
test('mocks API response', async ({ page }) => {
  await page.route('**/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([{ id: 1, name: 'Test User' }]),
    })
  })

  await page.goto('/users')
  await expect(page.getByText('Test User')).toBeVisible()
})
```

## Visual Testing

```typescript
test('captures screenshot', async ({ page }) => {
  await page.goto('/')
  await page.screenshot({ path: 'screenshot.png', fullPage: true })
  await expect(page).toHaveScreenshot('homepage.png')
})
```

## Authentication State

```typescript
// Save state after login
setup('authenticate', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('user@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Sign in' }).click()
  await page.context().storageState({ path: 'auth.json' })
})

// Reuse in config
use: { storageState: 'auth.json' }
```

## Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test'

export class LoginPage {
  readonly emailInput: Locator
  readonly passwordInput: Locator
  readonly submitButton: Locator

  constructor(page: Page) {
    this.emailInput = page.getByLabel('Email')
    this.passwordInput = page.getByLabel('Password')
    this.submitButton = page.getByRole('button', { name: 'Sign in' })
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email)
    await this.passwordInput.fill(password)
    await this.submitButton.click()
  }
}

// Usage
const loginPage = new LoginPage(page)
await loginPage.login('user@example.com', 'password123')
```

## Available Helpers

Optional utility functions in `lib/helpers.js`:

```javascript
const helpers = require('./lib/helpers');

// Detect running dev servers (CRITICAL - use this first!)
const servers = await helpers.detectDevServers();
console.log('Found servers:', servers);

// Safe click with retry
await helpers.safeClick(page, 'button.submit', { retries: 3 });

// Safe type with clear
await helpers.safeType(page, '#username', 'testuser');

// Take timestamped screenshot
await helpers.takeScreenshot(page, 'test-result');

// Handle cookie banners
await helpers.handleCookieBanner(page);

// Extract table data
const data = await helpers.extractTableData(page, 'table.results');

// Create context with custom headers
const context = await helpers.createContext(browser);
```

## Custom HTTP Headers

Configure custom headers for all HTTP requests via environment variables:

```bash
# Single header (common case)
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd $SKILL_DIR && node run.js /tmp/my-script.js

# Multiple headers (JSON format)
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

Headers are automatically applied when using `helpers.createContext()`.

## Inline Execution (Simple Tasks)

For quick one-off tasks:

```bash
cd $SKILL_DIR && node run.js "
const browser = await chromium.launch({ headless: false });
const page = await browser.newPage();
await page.goto('http://localhost:3001');
await page.screenshot({ path: '/tmp/quick-screenshot.png', fullPage: true });
console.log('Screenshot saved');
await browser.close();
"
```

**When to use:**
- **Inline**: Quick one-off tasks (screenshot, element check)
- **Files**: Complex tests, reusable automation

## Best Practices

- **CRITICAL: Detect servers FIRST** - Always run `detectDevServers()` before writing test code
- **Use /tmp for test files** - Write to `/tmp/playwright-test-*.js`, never to skill directory
- **Parameterize URLs** - Put detected/provided URL in `TARGET_URL` constant
- **DEFAULT: Visible browser** - Always use `headless: false` unless explicitly requested
- **Prefer role-based selectors** - More stable than CSS selectors
- **Trust auto-waiting** - No manual sleeps needed
- **Each test gets fresh context** - Automatic isolation
- **Run tests in parallel** - Default behavior
- **Mock external dependencies** - Use `page.route()`
- **Use trace viewer** - Time-travel debugging

## Tips

- **Slow down:** Use `slowMo: 100` to make actions visible
- **Wait strategies:** Use `waitForURL`, `waitForSelector`, `waitForLoadState` instead of fixed timeouts
- **Error handling:** Always use try-catch for robust automation
- **Console output:** Use `console.log()` to track progress

## Troubleshooting

**Playwright not installed:**
```bash
cd $SKILL_DIR && bun run setup
```

**Module not found:**
Ensure running from skill directory via `run.js` wrapper

**Browser doesn't open:**
Check `headless: false` and ensure display available

**Element not found:**
Add wait: `await page.waitForSelector('.element', { timeout: 10000 })`

## See Also

- `vitest-testing` - Unit and integration testing
- `api-testing` - HTTP API testing
- `test-quality-analysis` - Test quality patterns

## When to Load References

Load `references/API_REFERENCE.md` when you need:
- Advanced selector patterns and locator strategies
- Network interception and request/response mocking
- Authentication patterns and session management
- Visual regression testing setup
- Mobile device emulation configurations
- Performance testing and metrics
- Debugging techniques (trace viewer, inspector)
- CI/CD pipeline integration
- Accessibility testing with axe-core
- Data-driven and parameterized testing
- Page Object Model advanced patterns
- Parallel execution strategies
