---
name: testing-playwright
description: Apply when writing end-to-end tests: user flows, cross-browser testing, visual regression, and API testing.
version: 1.0.0
tokens: ~650
confidence: high
sources:
  - https://playwright.dev/docs/intro
  - https://playwright.dev/docs/locators
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [testing, e2e, playwright, automation]
---

## When to Use

Apply when writing end-to-end tests: user flows, cross-browser testing, visual regression, and API testing.

## Patterns

### Pattern 1: Basic Page Test
```typescript
// Source: https://playwright.dev/docs/intro
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('https://myapp.com');

  await expect(page).toHaveTitle(/My App/);
  await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
});
```

### Pattern 2: Locator Strategies
```typescript
// Source: https://playwright.dev/docs/locators
// Preferred: accessible locators
page.getByRole('button', { name: 'Submit' });
page.getByLabel('Email');
page.getByPlaceholder('Enter email');
page.getByText('Welcome back');

// Data attributes (for complex cases)
page.getByTestId('submit-btn');

// CSS/XPath (last resort)
page.locator('.card >> text=Title');
page.locator('xpath=//div[@class="item"]');
```

### Pattern 3: User Flow Test
```typescript
// Source: https://playwright.dev/docs/intro
test('user can complete checkout', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Add to cart
  await page.goto('/products');
  await page.getByRole('button', { name: 'Add to cart' }).first().click();

  // Checkout
  await page.getByRole('link', { name: 'Cart' }).click();
  await page.getByRole('button', { name: 'Checkout' }).click();

  // Verify success
  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

### Pattern 4: Page Object Model
```typescript
// Source: https://playwright.dev/docs/pom
// pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('Email').fill(email);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Sign in' }).click();
  }
}

// test.spec.ts
test('login flow', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@test.com', 'pass');
  await expect(page).toHaveURL('/dashboard');
});
```

### Pattern 5: API Testing
```typescript
// Source: https://playwright.dev/docs/api-testing
import { test, expect } from '@playwright/test';

test('API returns users', async ({ request }) => {
  const response = await request.get('/api/users');

  expect(response.ok()).toBeTruthy();
  const users = await response.json();
  expect(users.length).toBeGreaterThan(0);
});

test('create user via API', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: { name: 'John', email: 'john@test.com' },
  });

  expect(response.status()).toBe(201);
});
```

### Pattern 6: Visual Regression
```typescript
// Source: https://playwright.dev/docs/test-snapshots
test('homepage visual', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});

// Component screenshot
test('button states', async ({ page }) => {
  const button = page.getByRole('button');
  await expect(button).toHaveScreenshot('button-default.png');

  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');
});
```

## Anti-Patterns

- **Hardcoded waits** - Use auto-waiting locators
- **Brittle selectors** - Prefer role/label over CSS
- **No isolation** - Each test should be independent
- **Testing too much** - E2E for critical paths only

## Verification Checklist

- [ ] Tests use accessible locators
- [ ] Page Object Model for complex flows
- [ ] No hardcoded sleeps (use waitFor)
- [ ] Tests isolated and independent
- [ ] Visual tests have baseline images
