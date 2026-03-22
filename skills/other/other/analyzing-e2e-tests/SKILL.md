---
name: analyzing-e2e-tests
description: Use when analyzing end-to-end tests including browser automation, API workflows, and full system testing
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
---

# Analyzing E2E Tests

**Output:** `docs/unwind/layers/e2e-tests/` (folder with index.md + section files)

**Principles:** See `analysis-principles.md` - completeness, machine-readable, link to source, no commentary, incremental writes.

## Output Structure

```
docs/unwind/layers/e2e-tests/
├── index.md           # Test summary, browser matrix
├── config.md          # Playwright/Cypress config, CI setup
├── page-objects.md    # Page object definitions
├── fixtures.md        # Test data and fixtures
└── flows.md           # User flow tests
```

For large codebases, split by feature:
```
docs/unwind/layers/e2e-tests/
├── index.md
├── config.md
├── auth-tests.md
├── checkout-tests.md
└── ...
```

## Process (Incremental Writes)

**Step 1: Setup**
```bash
mkdir -p docs/unwind/layers/e2e-tests/
```
Write initial `index.md`:
```markdown
# E2E Tests

## Sections
- [Configuration](config.md) - _pending_
- [Page Objects](page-objects.md) - _pending_
- [Test Fixtures](fixtures.md) - _pending_
- [User Flows](flows.md) - _pending_

## Summary
_Analysis in progress..._
```

**Step 2: Analyze and write config.md**
1. Find Playwright/Cypress config, CI setup
2. Write `config.md` immediately
3. Update `index.md`

**Step 3: Analyze and write page-objects.md**
1. Find all page object definitions
2. Write `page-objects.md` immediately
3. Update `index.md`

**Step 4: Analyze and write fixtures.md**
1. Find test data and fixtures
2. Write `fixtures.md` immediately
3. Update `index.md`

**Step 5: Analyze and write flows.md**
1. Find all user flow tests
2. Write `flows.md` immediately
3. Update `index.md`

**Step 6: Finalize index.md**
Add test summary and browser matrix

## Output Format

```markdown
# E2E Tests

## Configuration

### Playwright Config

[playwright.config.ts](https://github.com/owner/repo/blob/main/playwright.config.ts)

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
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

## Test Summary

| Feature | Tests | Browsers |
|---------|-------|----------|
| Authentication | 5 | Chrome, Firefox, Safari |
| Order Flow | 8 | Chrome, Firefox, Safari |
| Admin Panel | 4 | Chrome |

## Page Objects

### LoginPage

[LoginPage.ts](https://github.com/owner/repo/blob/main/e2e/pages/LoginPage.ts)

```typescript
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async getErrorMessage() {
    return this.page.textContent('[data-testid="error"]');
  }
}
```

[Continue for ALL page objects...]

## Authentication Tests

### auth.spec.ts

[auth.spec.ts](https://github.com/owner/repo/blob/main/e2e/auth.spec.ts)

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('Authentication', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]')).toBeVisible();
  });

  test('invalid credentials shows error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrongpassword');

    await expect(page.locator('[data-testid="error"]')).toHaveText('Invalid credentials');
  });

  test('logout clears session', async ({ page }) => {
    // Login first
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    // Logout
    await page.click('[data-testid="logout"]');

    await expect(page).toHaveURL('/login');
  });
});
```

## Order Flow Tests

### order.spec.ts

[order.spec.ts](https://github.com/owner/repo/blob/main/e2e/order.spec.ts)

```typescript
test.describe('Order Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');
  });

  test('complete order flow', async ({ page }) => {
    // Add product to cart
    await page.goto('/products');
    await page.click('[data-testid="product-1"] [data-testid="add-to-cart"]');

    // Go to cart
    await page.click('[data-testid="cart-icon"]');
    await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1);

    // Checkout
    await page.click('[data-testid="checkout"]');
    await page.fill('[data-testid="card-number"]', '4242424242424242');
    await page.fill('[data-testid="expiry"]', '12/25');
    await page.fill('[data-testid="cvc"]', '123');
    await page.click('[data-testid="place-order"]');

    // Confirm
    await expect(page).toHaveURL(/\/orders\/\d+/);
    await expect(page.locator('[data-testid="order-status"]')).toHaveText('Confirmed');
  });
});
```

[Continue for ALL test files...]

## Test Fixtures

### test-data.ts

[test-data.ts](https://github.com/owner/repo/blob/main/e2e/fixtures/test-data.ts)

```typescript
export const testUsers = {
  standard: {
    email: 'user@example.com',
    password: 'password123',
  },
  admin: {
    email: 'admin@example.com',
    password: 'admin123',
  },
};

export const testProducts = [
  { id: 1, name: 'Test Product', price: 29.99 },
];
```

## CI Integration

[.github/workflows/e2e.yml](https://github.com/owner/repo/blob/main/.github/workflows/e2e.yml)

```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Unknowns

- [List anything unclear]
```

## Refresh Mode

If `docs/unwind/layers/e2e-tests/` exists, compare current state and add `## Changes Since Last Review` section to `index.md`.
