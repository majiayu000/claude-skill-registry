---
name: "Playwright E2E Testing"
description: "Build end-to-end tests with Playwright, Feature Object pattern, cross-browser testing, and visual regression. Apply when testing critical user flows, automating regression testing, or validating integrations."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Playwright E2E Testing

Systematic end-to-end testing with Playwright ensuring critical user flows work correctly.

## Overview

This Skill enforces:
- Feature Object pattern (replaces Page Object)
- Arrange-Act-Assert test structure
- Cross-browser testing (Chromium, Firefox, WebKit)
- Reliable selectors (getByRole, getByTestId)
- Visual regression testing
- Network mocking and interception
- Parallel test execution
- CI/CD integration

Apply when testing critical user flows, automating regression testing, or validating integrations.

## Setup Playwright

### Install

```bash
npm install -D @playwright/test
npx playwright install
```

### Configure playwright.config.ts

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:debug": "playwright test --debug"
  }
}
```

## Feature Object Pattern

### Directory Structure

```
e2e/
├── features/
│   ├── auth.feature.ts      # Authentication flows
│   ├── users.feature.ts     # User management
│   └── dashboard.feature.ts # Dashboard features
├── fixtures/
│   ├── api.fixture.ts       # API interactions
│   └── ui.fixture.ts        # UI interactions
└── tests/
    ├── auth.spec.ts
    ├── users.spec.ts
    └── dashboard.spec.ts
```

### Feature Object (Auth)

```ts
// e2e/features/auth.feature.ts
import { Page } from '@playwright/test';

export class AuthFeature {
  constructor(private page: Page) {}

  async navigateToLogin() {
    await this.page.goto('/login');
  }

  async enterEmail(email: string) {
    await this.page.getByLabel('Email').fill(email);
  }

  async enterPassword(password: string) {
    await this.page.getByLabel('Password').fill(password);
  }

  async clickLoginButton() {
    await this.page.getByRole('button', { name: /login/i }).click();
  }

  async verifyLoginSuccess() {
    await this.page.waitForURL('/dashboard');
    await expect(this.page).toHaveURL('/dashboard');
  }

  async verifyLoginError(message: string) {
    const error = this.page.getByRole('alert');
    await expect(error).toContainText(message);
  }

  async logout() {
    await this.page.getByRole('button', { name: /logout/i }).click();
    await this.page.waitForURL('/login');
  }
}
```

### Fixture Setup

```ts
// e2e/fixtures/test.fixture.ts
import { test as base } from '@playwright/test';
import { AuthFeature } from '../features/auth.feature';
import { DashboardFeature } from '../features/dashboard.feature';

type Fixtures = {
  auth: AuthFeature;
  dashboard: DashboardFeature;
};

export const test = base.extend<Fixtures>({
  auth: async ({ page }, use) => {
    const auth = new AuthFeature(page);
    await use(auth);
  },
  dashboard: async ({ page }, use) => {
    const dashboard = new DashboardFeature(page);
    await use(dashboard);
  }
});

export { expect } from '@playwright/test';
```

## Arrange-Act-Assert Pattern

### Login Test

```ts
// e2e/tests/auth.spec.ts
import { test, expect } from '../fixtures/test.fixture';

test.describe('Authentication', () => {
  test('successful login flow', async ({ auth }) => {
    // ARRANGE: Navigate to login page
    await auth.navigateToLogin();

    // ACT: Enter credentials and submit
    await auth.enterEmail('user@example.com');
    await auth.enterPassword('password123');
    await auth.clickLoginButton();

    // ASSERT: Verify login success
    await auth.verifyLoginSuccess();
  });

  test('login with invalid credentials', async ({ auth }) => {
    // ARRANGE
    await auth.navigateToLogin();

    // ACT
    await auth.enterEmail('user@example.com');
    await auth.enterPassword('wrongpassword');
    await auth.clickLoginButton();

    // ASSERT
    await auth.verifyLoginError('Invalid credentials');
  });

  test('logout flow', async ({ page, auth }) => {
    // ARRANGE: Login first
    await auth.navigateToLogin();
    await auth.enterEmail('user@example.com');
    await auth.enterPassword('password123');
    await auth.clickLoginButton();
    await page.waitForURL('/dashboard');

    // ACT
    await auth.logout();

    // ASSERT
    await expect(page).toHaveURL('/login');
  });
});
```

## Selectors (getByRole, getByTestId)

### Recommended Selectors

```ts
// ✅ GOOD: Accessible selectors
await page.getByRole('button', { name: /submit/i }).click();
await page.getByRole('textbox', { name: /email/i }).fill('user@example.com');
await page.getByLabel('Password').fill('password');
await page.getByText('Welcome, Alice').isVisible();

// ✅ GOOD: Test IDs (for complex elements)
<div data-testid="user-profile">Profile</div>
await page.getByTestId('user-profile').click();

// ❌ BAD: Fragile selectors (auto-generated)
await page.locator('.css-1a2b3c4d').click();  // Will break on CSS change

// ❌ BAD: XPath (brittle)
await page.locator('//*[@class="button"]').click();

// ❌ BAD: Overly specific
await page.locator('div > section > form > button').click();
```

## Critical Admin Flows

### User Management Test

```ts
// e2e/features/admin.feature.ts
export class AdminFeature {
  constructor(private page: Page) {}

  async navigateToUsers() {
    await this.page.goto('/admin/users');
  }

  async createUser(user: { name: string; email: string; role: string }) {
    await this.page.getByRole('button', { name: /new user/i }).click();
    await this.page.getByLabel('Name').fill(user.name);
    await this.page.getByLabel('Email').fill(user.email);
    await this.page.getByLabel('Role').selectOption(user.role);
    await this.page.getByRole('button', { name: /create/i }).click();
    await this.page.waitForSelector('text=User created');
  }

  async deleteUser(email: string) {
    // Find user row and click delete
    const row = this.page.locator(`tr:has-text("${email}")`);
    await row.getByRole('button', { name: /delete/i }).click();

    // Confirmation dialog
    await this.page.getByRole('button', { name: /confirm/i }).click();
    await this.page.waitForSelector('text=User deleted');
  }

  async verifyUserExists(email: string) {
    await expect(this.page.locator('table')).toContainText(email);
  }
}

// e2e/tests/admin.spec.ts
test('admin creates and deletes user', async ({ page, admin }) => {
  // ARRANGE
  await admin.navigateToUsers();

  // ACT
  await admin.createUser({
    name: 'John Doe',
    email: 'john@example.com',
    role: 'admin'
  });

  // ASSERT
  await admin.verifyUserExists('john@example.com');

  // ACT: Delete user
  await admin.deleteUser('john@example.com');

  // ASSERT: User gone
  await expect(page.locator('table')).not.toContainText('john@example.com');
});
```

## Network Mocking

### Mock API Responses

```ts
test('handles API failure gracefully', async ({ page }) => {
  // Mock API to return error
  await page.route('/api/users', route => {
    route.abort('failed');
  });

  await page.goto('/users');

  // Verify error message shown
  await expect(page.getByText('Failed to load users')).toBeVisible();
});

test('intercept and modify response', async ({ page }) => {
  await page.route('/api/users', route => {
    route.continue();
    // Wait for response
    const response = route.response();
    if (response) {
      const json = response.json();
      json.then(data => {
        // Response intercepted and logged
        console.log('Users API Response:', data);
      });
    }
  });

  await page.goto('/users');
});
```

## Visual Regression Testing

### Screenshot Comparison

```ts
test('dashboard layout', async ({ page }) => {
  await page.goto('/dashboard');
  
  // Take screenshot
  await expect(page).toHaveScreenshot('dashboard.png');
});

test('responsive design', async ({ browser }) => {
  const contexts = [
    { name: 'desktop', width: 1920, height: 1080 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'mobile', width: 375, height: 812 }
  ];

  for (const context of contexts) {
    const page = await browser.newPage({
      viewport: { width: context.width, height: context.height }
    });

    await page.goto('/dashboard');
    await expect(page).toHaveScreenshot(`dashboard-${context.name}.png`);
    await page.close();
  }
});
```

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
      - run: npm run build
      - run: npx playwright install --with-deps

      - run: npm run test:e2e

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Anti-Patterns

```ts
// ❌ BAD: Hard-coded waits
await page.waitForTimeout(5000);

// ✅ GOOD: Wait for element
await page.getByRole('button').waitFor({ state: 'visible' });

// ❌ BAD: Vague test names
test('test login', async ({ auth }) => {});

// ✅ GOOD: Descriptive test names
test('successfully login with valid credentials', async ({ auth }) => {});

// ❌ BAD: No error handling
const button = page.locator('button');
await button.click();
// Button might not exist!

// ✅ GOOD: Check existence first
await expect(page.getByRole('button')).toBeVisible();
await page.getByRole('button').click();

// ❌ BAD: Fragile selectors
await page.locator('div:nth-child(3) > button').click();

// ✅ GOOD: Semantic selectors
await page.getByRole('button', { name: /submit/i }).click();
```

## Running Tests

```bash
# Run all tests
npm run test:e2e

# Run specific file
npx playwright test auth.spec.ts

# Run in UI mode
npm run test:e2e:ui

# Debug mode
npm run test:e2e:debug

# Report
npx playwright show-report
```

## Verification Before Production

- [ ] Critical user flows covered
- [ ] Cross-browser tests passing
- [ ] No hard-coded waits
- [ ] Reliable selectors used
- [ ] Visual regressions checked
- [ ] Network edge cases mocked
- [ ] Mobile testing included
- [ ] CI/CD integrated
- [ ] Tests run in parallel
- [ ] Reports generated

## Integration with Project Standards

Enforces T-7, T-9:
- E2E tests for critical admin flows
- Admin portal features tested
- User journey validation
- Integration verification

## Resources

- Playwright Docs: https://playwright.dev
- Selectors Guide: https://playwright.dev/docs/locators
- Best Practices: https://playwright.dev/docs/best-practices
- CI/CD: https://playwright.dev/docs/ci
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
