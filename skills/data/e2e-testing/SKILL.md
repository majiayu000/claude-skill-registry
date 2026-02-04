---
name: e2e-testing
description: End-to-end testing expert for Playwright, Cypress, visual regression (Percy, Chromatic), and UI testing. Use for E2E tests, browser automation, visual diffs, or debugging flaky tests.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# E2E Testing Expert - Playwright, Visual Regression, UI Testing

## Core Expertise

- **Playwright/Cypress** for browser automation
- **Visual regression** with Percy, Chromatic, BackstopJS
- **UI testing** with Testing Library patterns
- **Accessibility testing** with axe-core
- **Mobile emulation** and device testing

## Playwright Fundamentals

### Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully', async ({ page }) => {
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome')).toBeVisible();
  });
});
```

### Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  readonly emailInput = this.page.getByLabel('Email');
  readonly passwordInput = this.page.getByLabel('Password');
  readonly loginButton = this.page.getByRole('button', { name: 'Login' });

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

### Fixtures

```typescript
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

export const test = base.extend<{ loginPage: LoginPage }>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },
});
```

## Visual Regression

### Playwright Screenshots

```typescript
test('homepage matches baseline', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    animations: 'disabled',
  });
});

// Responsive screenshots
await page.setViewportSize({ width: 1920, height: 1080 });
await expect(page).toHaveScreenshot('desktop.png');

await page.setViewportSize({ width: 375, height: 667 });
await expect(page).toHaveScreenshot('mobile.png');
```

### Percy Integration

```typescript
import { percySnapshot } from '@percy/playwright';

test('visual diff with Percy', async ({ page }) => {
  await page.goto('/dashboard');
  await percySnapshot(page, 'Dashboard');
});
```

### Chromatic (Storybook)

```json
// package.json
{
  "scripts": {
    "chromatic": "chromatic --project-token=$CHROMATIC_PROJECT_TOKEN"
  }
}
```

## Accessibility Testing

```typescript
import AxeBuilder from '@axe-core/playwright';

test('accessibility audit', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});

// Keyboard navigation
test('keyboard navigation', async ({ page }) => {
  await page.goto('/form');
  await page.keyboard.press('Tab');
  await expect(page.getByLabel('Email')).toBeFocused();
});
```

## Mobile Testing

```typescript
import { devices } from '@playwright/test';

test.use(devices['iPhone 13 Pro']);

test('mobile navigation', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible();
});
```

## Network Mocking

```typescript
test('mock API response', async ({ page }) => {
  await page.route('/api/users', async (route) => {
    await route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, name: 'John' }]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('John')).toBeVisible();
});
```

## Debugging Flaky Tests

```typescript
// Proper waiting (NOT setTimeout)
await page.waitForLoadState('networkidle');
await page.waitForSelector('.content', { state: 'visible' });

// Retry configuration
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

## CI/CD Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Best Practices

1. **Use stable locators** (roles, labels, test IDs)
2. **Page Object Model** for maintainability
3. **Wait for conditions**, not timeouts
4. **Isolate test data** per test
5. **Mock external APIs** to reduce flakiness
6. **Disable animations** for visual tests
7. **Run parallel** in CI for speed
8. **Save traces/screenshots** on failure

## Test Organization

```
e2e/
├── fixtures/
│   └── auth.fixture.ts
├── pages/
│   ├── LoginPage.ts
│   └── DashboardPage.ts
├── tests/
│   ├── auth.spec.ts
│   └── dashboard.spec.ts
└── playwright.config.ts
```

## Related Skills

- `qa-engineer` - Overall test strategy
- `unit-testing` - Unit and integration tests
