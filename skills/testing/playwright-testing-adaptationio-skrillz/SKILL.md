---
name: playwright-testing
description: Comprehensive Playwright E2E testing framework for browser automation. Use when setting up tests, writing E2E scenarios, debugging test failures, configuring CI/CD pipelines, or running browser automation on WSL2.
---

# Playwright Testing

## Overview

Playwright is the state-of-the-art browser automation framework for 2025, offering cross-browser testing (Chrome, Firefox, Safari/WebKit), built-in codegen, and 35-45% faster parallel execution than alternatives.

**Key Advantages**:
- Cross-browser: Chrome, Firefox, Safari from one codebase
- Multi-language: JavaScript, TypeScript, Python, Java, .NET
- Auto-wait: Intelligent waiting for elements
- Codegen: Record tests by clicking in browser
- Parallelization: Native, free parallel execution
- WSL2 Compatible: Works with Windows Chrome

---

## Quick Start (5 Minutes)

### 1. Initialize Playwright

```bash
# Create new project or add to existing
npm init playwright@latest

# Install browsers
npx playwright install
```

### 2. Configure for WSL2 (if on Windows Subsystem for Linux)

```bash
# Set Windows Chrome as browser
export CHROME_BIN="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# Or use remote debugging (recommended)
# Start Chrome on Windows with: chrome.exe --remote-debugging-port=9222
```

### 3. Write First Test

```typescript
// tests/example.spec.ts
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('https://your-app.com');
  await expect(page).toHaveTitle(/Your App/);
});

test('login works', async ({ page }) => {
  await page.goto('https://your-app.com/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

### 4. Run Tests

```bash
# Run all tests
npx playwright test

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific test file
npx playwright test tests/login.spec.ts

# Run with UI mode (interactive)
npx playwright test --ui
```

---

## Workflow: Creating E2E Tests

### Step 1: Record with Codegen

```bash
# Launch codegen - click in browser, code generates automatically
npx playwright codegen https://your-app.com

# Save authentication state for reuse
npx playwright codegen --save-storage=auth.json https://your-app.com
```

### Step 2: Organize Tests

```
tests/
├── e2e/
│   ├── auth.spec.ts       # Authentication flows
│   ├── dashboard.spec.ts  # Dashboard features
│   └── checkout.spec.ts   # Checkout flow
├── visual/
│   └── screenshots.spec.ts # Visual regression
├── api/
│   └── api.spec.ts        # API testing
└── fixtures/
    └── index.ts           # Shared fixtures
```

### Step 3: Use Page Objects

```typescript
// pages/LoginPage.ts
import { Page } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}

// tests/auth.spec.ts
import { LoginPage } from '../pages/LoginPage';

test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL(/dashboard/);
});
```

### Step 4: Run Parallel Tests

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined,
  retries: process.env.CI ? 2 : 0,
  reporter: [['html'], ['list']],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
    { name: 'webkit', use: { browserName: 'webkit' } },
  ],
});
```

---

## WSL2 Configuration

### Option 1: Windows Chrome (Recommended)

```bash
# Create wrapper script
mkdir -p ~/bin
cat << 'EOF' > ~/bin/chrome-win
#!/bin/bash
"/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" "$@"
EOF
chmod +x ~/bin/chrome-win

# Set environment variable
echo 'export CHROME_BIN="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"' >> ~/.bashrc
source ~/.bashrc
```

### Option 2: Remote Debugging

```bash
# On Windows, start Chrome with debugging:
# chrome.exe --remote-debugging-port=9222

# In Playwright config:
import { chromium } from '@playwright/test';

const browser = await chromium.connectOverCDP('http://localhost:9222');
```

### Option 3: WSLg (Windows 11)

```bash
# WSLg is built into Windows 11 - GUI apps work automatically
wsl --update

# Install Chrome in WSL
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f

# Run headed tests directly
npx playwright test --headed
```

See `references/wsl2-configuration.md` for detailed troubleshooting.

---

## Best Practices

### Locator Strategy (Priority Order)

1. **Role** (best): `page.getByRole('button', { name: 'Submit' })`
2. **Label**: `page.getByLabel('Email')`
3. **Placeholder**: `page.getByPlaceholder('Enter email')`
4. **Test ID**: `page.getByTestId('submit-btn')`
5. **CSS** (avoid): `page.locator('.btn-primary')`

### Auto-Wait (Don't Add Manual Waits)

```typescript
// BAD - manual waits
await page.waitForTimeout(2000);
await page.click('.button');

// GOOD - Playwright auto-waits
await page.click('.button'); // Waits automatically
await expect(page.locator('.result')).toBeVisible(); // Waits for element
```

### Parallel Execution

```typescript
// Run tests in parallel (default)
test.describe.configure({ mode: 'parallel' });

// Run tests serially (when order matters)
test.describe.configure({ mode: 'serial' });
```

See `references/best-practices.md` for comprehensive patterns.

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

See `references/ci-cd-integration.md` for Docker, Railway, and advanced setups.

---

## Debugging

### Trace Viewer

```bash
# Enable traces in config
# trace: 'on-first-retry'

# View trace after test failure
npx playwright show-trace trace.zip
```

### UI Mode

```bash
# Interactive debugging
npx playwright test --ui
```

### Headed Mode

```bash
# See browser during test
npx playwright test --headed --slowmo=500
```

### VS Code Integration

Install "Playwright Test for VS Code" extension for:
- Run tests from editor
- Debug with breakpoints
- View trace inline

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `npx playwright test` | Run all tests |
| `npx playwright test --headed` | Run with visible browser |
| `npx playwright test --ui` | Interactive UI mode |
| `npx playwright codegen <url>` | Record test by clicking |
| `npx playwright show-report` | View HTML report |
| `npx playwright show-trace <file>` | View trace file |
| `npx playwright install` | Install browsers |
| `npx playwright --version` | Check version |

---

## References

- `references/setup-guide.md` - Complete installation guide
- `references/best-practices.md` - Locators, parallelization, patterns
- `references/wsl2-configuration.md` - WSL2 setup and troubleshooting
- `references/ci-cd-integration.md` - GitHub Actions, Docker, Railway

## Scripts

- `scripts/init-playwright.sh` - Initialize Playwright in project
- `scripts/generate-test.ts` - Generate test from URL

---

**Playwright is the recommended testing framework for 2025 - cross-browser, fast, and developer-friendly.**
