---
name: qa-testing-playwright
description: "End-to-end web application testing with Playwright: scope control, stable selectors, parallelization/sharding, flake control, network mocking vs real services, visual testing tradeoffs, and CI/CD integration."
---

# QA Testing (Playwright, Dec 2025) — Quick Reference

This skill enables high-signal, cost-aware E2E testing of web applications using Playwright.

Core references: Playwright best practices (https://playwright.dev/docs/best-practices), locators (https://playwright.dev/docs/locators), retries (https://playwright.dev/docs/test-retries), sharding (https://playwright.dev/docs/test-sharding), and the trace viewer (https://playwright.dev/docs/trace-viewer).

---

## Core QA (Default)

### Scope Control (What E2E Is For)

- E2E exists to protect critical user journeys and high-risk integrations.
- Keep E2E thin; push most coverage down to unit/integration/contract tests.
- Test the contract and user intent, not CSS structure.

### Selector Strategy (Stability First)

- Prefer user-facing locators: `getByRole`, `getByLabel`, `getByText` (Playwright locators: https://playwright.dev/docs/locators).
- Use `data-testid` as a last resort for complex widgets or non-semantic UI.
- Avoid XPath and brittle CSS selectors.

### Flake Control (Make CI Reliable)

- Avoid sleeps; rely on Playwright auto-wait and web-first assertions (https://playwright.dev/docs/best-practices).
- Use retries as a signal, not a crutch; investigate rerun-pass tests as flakes (https://playwright.dev/docs/test-retries).
- Always capture traces/screenshots/video on failure; use trace viewer to localize root cause (https://playwright.dev/docs/trace-viewer).
- If clicks are intercepted by overlays, prefer keyboard activation or close the overlay rather than `force: true`.

### CI Economics (Parallelize and Shard)

- Run smoke E2E on PRs; run full regression on schedule or per-release [Inference].
- Shard long suites across machines to keep PR feedback fast (https://playwright.dev/docs/test-sharding).

### Do / Avoid

Do:
- Make tests independent and deterministic (isolated state, stable data).
- Use network mocking for third-party dependencies; test your integration contract, not their UI.

Avoid:
- “Test everything E2E” as a default.
- Weakening assertions to “fix” flakes (silent regressions).

## Quick Reference

| Task | Command | When to Use |
|------|---------|-------------|
| Init Playwright | `npm init playwright@latest` | New project setup |
| Run all tests | `npx playwright test` | Full test suite |
| Run with UI | `npx playwright test --ui` | Debugging, visual mode |
| Run specific test | `npx playwright test login.spec.ts` | Targeted testing |
| Generate code | `npx playwright codegen` | Record interactions |
| Show report | `npx playwright show-report` | View test results |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Write E2E tests for web application
- Test user authentication flows
- Verify form submissions and validation
- Test responsive designs across viewports
- Automate browser interactions
- Set up Playwright in CI/CD
- Debug failing E2E tests

---

## Quick Start

### Installation

```bash
# Initialize Playwright
npm init playwright@latest

# Or add to existing project
npm install -D @playwright/test
npx playwright install
```

### Project Structure

```text
project/
├── playwright.config.ts
├── tests/
│   ├── auth.spec.ts
│   ├── checkout.spec.ts
│   └── fixtures/
│       └── auth.fixture.ts
├── pages/
│   ├── LoginPage.ts
│   └── DashboardPage.ts
└── .github/workflows/
    └── playwright.yml
```

---

## Core Testing Patterns

### Browser Policy (Bundled vs Stable Channels)

- Default: bundled browsers are designed for reliable automation.
- When you must test against stable Chrome/Edge (policy/compliance, media codecs), use browser channels (see Playwright “Browsers”: https://playwright.dev/docs/browsers).

### Locator Priority (2025 Best Practice)

Use role locators as the **primary approach** — they test from the user's perspective:

```typescript
// 1. Role locators (preferred)
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('button', { name: 'Sign in' }).click();
await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

// 2. Label/text locators
await page.getByLabel('Email').fill('user@example.com');
await page.getByText('Sign in').click();

// 3. Test IDs (fallback for complex scenarios)
await page.getByTestId('user-avatar').click();
```

### Common UI Flake Patterns

- Overlay intercepts pointer events: use keyboard activation to follow the accessible path.
- Menus: open via `button` role, select `menuitem` role to avoid hidden link clicks.

```typescript
const menuButton = page.getByRole('button', { name: /open menu/i });
await menuButton.focus();
await menuButton.press('Enter');

const menuItem = page.getByRole('menuitem', { name: /year ahead/i });
await menuItem.focus();
await menuItem.press('Enter');
```

### Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.getByRole('textbox', { name: 'Email' }).fill('wrong@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid');
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByRole('textbox', { name: 'Email' });
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(message);
  }
}

// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test('login with valid credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

### Authentication Fixture

```typescript
// fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login');
    await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page).toHaveURL('/dashboard');

    // Use authenticated page in test
    await use(page);
  },
});

// tests/dashboard.spec.ts
import { test } from '../fixtures/auth.fixture';
import { expect } from '@playwright/test';

test('authenticated user can access dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  await expect(authenticatedPage.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

---

## Common Scenarios

### Form Testing

```typescript
test('should validate form fields', async ({ page }) => {
  await page.goto('/signup');

  // Submit empty form
  await page.click('[data-testid="submit"]');

  // Check validation messages
  await expect(page.locator('[data-testid="email-error"]')).toHaveText('Email is required');
  await expect(page.locator('[data-testid="password-error"]')).toHaveText('Password is required');

  // Fill with invalid email
  await page.fill('[data-testid="email"]', 'invalid-email');
  await page.click('[data-testid="submit"]');
  await expect(page.locator('[data-testid="email-error"]')).toHaveText('Invalid email format');
});
```

### API Mocking

```typescript
test('should handle API errors gracefully', async ({ page }) => {
  // Mock API to return error
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/users');
  await expect(page.locator('[data-testid="error-banner"]')).toContainText('Failed to load');
});

test('should display user data from API', async ({ page }) => {
  // Mock successful response
  await page.route('**/api/users', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([
        { id: 1, name: 'John Doe' },
        { id: 2, name: 'Jane Smith' },
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.locator('[data-testid="user-list"] li')).toHaveCount(2);
});
```

### Responsive Testing

```typescript
import { devices } from '@playwright/test';

test.describe('Responsive Design', () => {
  test('mobile navigation', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/');

    // Mobile menu should be hidden
    await expect(page.locator('[data-testid="desktop-nav"]')).toBeHidden();

    // Hamburger menu should be visible
    await expect(page.locator('[data-testid="mobile-menu-button"]')).toBeVisible();

    // Open mobile menu
    await page.click('[data-testid="mobile-menu-button"]');
    await expect(page.locator('[data-testid="mobile-nav"]')).toBeVisible();
  });
});

// playwright.config.ts - Multiple devices
export default defineConfig({
  projects: [
    { name: 'Desktop Chrome', use: { ...devices['Desktop Chrome'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
    { name: 'Tablet', use: { ...devices['iPad Pro'] } },
  ],
});
```

### Visual Regression

```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});

test('button states', async ({ page }) => {
  await page.goto('/components');

  const button = page.locator('[data-testid="primary-button"]');

  // Default state
  await expect(button).toHaveScreenshot('button-default.png');

  // Hover state
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');

  // Focus state
  await button.focus();
  await expect(button).toHaveScreenshot('button-focus.png');
});
```

---

## Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['junit', { outputFile: 'results.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### CI/CD Integration

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      - name: Run Playwright tests
        run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

---

## Debugging

```bash
# Run with UI mode
npx playwright test --ui

# Run in headed mode
npx playwright test --headed

# Run in debug mode (step through)
npx playwright test --debug

# Generate test code
npx playwright codegen http://localhost:3000

# Show trace viewer
npx playwright show-trace trace.zip
```

---

## Optional: AI / Automation

Do:
- Use AI to scaffold tests and page objects, then enforce selector rules, remove sleeps, and add explicit oracles.
- Use AI to summarize failing traces/logs, but base fixes on evidence and stable assertions.

Avoid:
- Auto-healing by weakening assertions or switching to brittle selectors.
- Generating tests that lock onto CSS structure instead of user-facing roles/labels.

---

## Navigation

**Resources**
- [resources/playwright-patterns.md](resources/playwright-patterns.md) — Advanced testing patterns
- [resources/playwright-ci.md](resources/playwright-ci.md) — CI/CD configurations
- [data/sources.json](data/sources.json) — Playwright documentation links

**Templates**
- [templates/template-playwright-e2e-review-checklist.md](templates/template-playwright-e2e-review-checklist.md) — E2E review checklist (selectors, parallelization, flake rules)

**Related Skills**
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — General testing strategies
- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) — Frontend development
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — CI/CD integration
