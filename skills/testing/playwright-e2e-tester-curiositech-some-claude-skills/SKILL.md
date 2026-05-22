---
name: playwright-e2e-tester
description: Expert in end-to-end testing with Playwright, the modern cross-browser testing framework. Specializes in test generation, page object patterns, visual regression testing, and CI/CD integration. Handles complex testing scenarios including authentication flows, API mocking, and mobile emulation.
version: 1.0.0
category: testing
tags: [e2e, playwright, testing, automation, ci-cd, cross-browser]
---

# Playwright E2E Tester

## Overview

Expert in end-to-end testing with Playwright, the modern cross-browser testing framework. Specializes in test generation, page object patterns, visual regression testing, and CI/CD integration. Handles complex testing scenarios including authentication flows, API mocking, and mobile emulation.

## When to Use

- Setting up Playwright in a new or existing project
- Writing E2E tests for critical user flows
- Debugging flaky tests or test failures
- Implementing visual regression testing
- Configuring Playwright for CI/CD pipelines
- Migrating from Cypress, Selenium, or Puppeteer
- Testing authenticated flows with session management
- Cross-browser testing (Chromium, Firefox, WebKit)

## Capabilities

### Test Generation & Writing
- Generate Playwright tests from user stories or acceptance criteria
- Write tests using best practices (locators, assertions, waits)
- Implement Page Object Model (POM) patterns
- Create reusable test fixtures and utilities
- Handle dynamic content and race conditions

### Configuration & Setup
- Configure `playwright.config.ts` for different environments
- Set up projects for multiple browsers and viewports
- Configure base URL, timeouts, and retries
- Implement global setup/teardown for auth
- Set up test reporters (HTML, JSON, JUnit)

### Advanced Patterns
- API mocking with `route()` and `fulfill()`
- Network interception and request validation
- Visual regression with `toHaveScreenshot()`
- Accessibility testing with `@axe-core/playwright`
- Mobile emulation and device testing
- Geolocation and permissions mocking

### CI/CD Integration
- GitHub Actions workflow configuration
- Parallel test execution with sharding
- Artifact collection (traces, screenshots, videos)
- Flaky test detection and retry strategies
- Test result reporting and notifications

### Debugging & Maintenance
- Use Playwright Inspector and Trace Viewer
- Debug with `page.pause()` and headed mode
- Analyze test traces for failures
- Reduce test flakiness with proper waits
- Maintain test stability over time

## Dependencies

Works well with:
- `vitest-testing-patterns` - Unit test patterns that complement E2E
- `github-actions-pipeline-builder` - CI/CD pipeline setup
- `accessibility-auditor` - Extended accessibility testing
- `api-architect` - API contract testing alongside E2E

## Examples

### Basic Test Structure
```typescript
import { test, expect } from '@playwright/test';

test.describe('User Authentication', () => {
  test('should allow user to sign in', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('securepassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
    await expect(page).toHaveURL('/dashboard');
  });
});
```

### Page Object Pattern
```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly signInButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.signInButton = page.getByRole('button', { name: 'Sign In' });
  }

  async goto() {
    await this.page.goto('/login');
  }

  async signIn(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }
}
```

### Auth Setup Fixture
```typescript
// fixtures/auth.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    // Perform authentication
    await page.goto('/login');
    await page.getByLabel('Email').fill(process.env.TEST_USER!);
    await page.getByLabel('Password').fill(process.env.TEST_PASS!);
    await page.getByRole('button', { name: 'Sign In' }).click();

    // Wait for auth to complete
    await page.waitForURL('/dashboard');

    // Use the authenticated page in tests
    await use(page);
  },
});
```

### GitHub Actions CI
```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
```

### Visual Regression Test
```typescript
test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot comparison
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    maxDiffPixelRatio: 0.01,
  });

  // Component-level screenshot
  const hero = page.getByTestId('hero-section');
  await expect(hero).toHaveScreenshot('hero-section.png');
});
```

### API Mocking
```typescript
test('displays products from API', async ({ page }) => {
  // Mock the API response
  await page.route('**/api/products', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Product A', price: 29.99 },
        { id: 2, name: 'Product B', price: 49.99 },
      ]),
    });
  });

  await page.goto('/products');

  await expect(page.getByText('Product A')).toBeVisible();
  await expect(page.getByText('$29.99')).toBeVisible();
});
```

## Best Practices

1. **Use role-based locators** - Prefer `getByRole()`, `getByLabel()`, `getByText()` over CSS selectors
2. **Avoid hard waits** - Use `waitForSelector()`, `waitForURL()`, or assertions instead of `waitForTimeout()`
3. **Isolate tests** - Each test should be independent and not rely on state from other tests
4. **Use fixtures** - Share setup logic through fixtures rather than `beforeEach` hooks
5. **Keep tests focused** - Test one user flow per test, avoid testing multiple unrelated things
6. **Handle flakiness proactively** - Use proper waits, retries, and stable locators
7. **Organize with Page Objects** - Encapsulate page interactions for maintainability
8. **Run in CI** - Always run E2E tests in CI before merging

## Common Pitfalls

- **Flaky locators**: Avoid fragile selectors like `nth-child(3)` or auto-generated class names
- **Race conditions**: Always wait for elements/navigation before interacting
- **Shared state**: Tests should not depend on execution order
- **Slow tests**: Use API calls to set up state instead of UI interactions when possible
- **Missing cleanup**: Clean up test data to avoid pollution between runs
