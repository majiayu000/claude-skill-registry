---
name: playwright
description: Tests web applications with Playwright including E2E tests, locators, assertions, and visual testing. Use when writing end-to-end tests, testing across browsers, automating user flows, or debugging test failures.
---

# Playwright

Cross-browser end-to-end testing framework with auto-wait and powerful debugging.

## Quick Start

**Install:**
```bash
npm init playwright@latest
```

This creates:
- `playwright.config.ts` - Configuration
- `tests/` - Test directory
- `tests-examples/` - Example tests

**Run tests:**
```bash
npx playwright test
npx playwright test --ui          # UI mode
npx playwright test --headed      # See browser
npx playwright show-report        # View report
```

## Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Structure

### Basic Test

```typescript
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/My App/);
});

test('navigates to about', async ({ page }) => {
  await page.goto('/');
  await page.click('text=About');
  await expect(page).toHaveURL('/about');
});
```

### Test Groups

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('shows login form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
  });

  test('logs in with valid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page).toHaveURL('/dashboard');
  });

  test('shows error with invalid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('wrong@example.com');
    await page.getByLabel('Password').fill('wrongpass');
    await page.getByRole('button', { name: 'Login' }).click();

    await expect(page.getByText('Invalid credentials')).toBeVisible();
  });
});
```

## Locators

### Recommended Locators

```typescript
// By role (best for accessibility)
page.getByRole('button', { name: 'Submit' });
page.getByRole('heading', { name: 'Welcome' });
page.getByRole('link', { name: 'Home' });
page.getByRole('textbox', { name: 'Email' });
page.getByRole('checkbox', { name: 'Remember me' });

// By label
page.getByLabel('Email');
page.getByLabel('Password');

// By placeholder
page.getByPlaceholder('Enter your email');

// By text
page.getByText('Welcome to our app');
page.getByText(/welcome/i); // Case-insensitive

// By alt text
page.getByAltText('Company logo');

// By title
page.getByTitle('Close');

// By test ID
page.getByTestId('submit-button');
```

### CSS and XPath

```typescript
// CSS selector
page.locator('.submit-button');
page.locator('#email-input');
page.locator('[data-cy="login-form"]');

// XPath
page.locator('//button[text()="Submit"]');
```

### Filtering and Chaining

```typescript
// Filter by text
page.getByRole('listitem').filter({ hasText: 'Product 1' });

// Filter by child locator
page.getByRole('listitem').filter({
  has: page.getByRole('button', { name: 'Add to cart' }),
});

// Chain locators
page.getByRole('article').getByRole('button', { name: 'Read more' });

// Nth element
page.getByRole('listitem').nth(0);
page.getByRole('listitem').first();
page.getByRole('listitem').last();
```

## Actions

### Click

```typescript
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('link').click({ button: 'right' }); // Right click
await page.getByRole('button').dblclick(); // Double click
await page.getByRole('button').click({ force: true }); // Force click
```

### Fill and Type

```typescript
// Fill (clears first)
await page.getByLabel('Email').fill('user@example.com');

// Type (key by key)
await page.getByLabel('Search').type('playwright');

// Press key
await page.getByLabel('Search').press('Enter');

// Clear
await page.getByLabel('Email').clear();
```

### Select

```typescript
// Select option
await page.getByLabel('Country').selectOption('usa');
await page.getByLabel('Country').selectOption({ label: 'United States' });

// Multi-select
await page.getByLabel('Colors').selectOption(['red', 'blue']);
```

### Check and Uncheck

```typescript
await page.getByLabel('Accept terms').check();
await page.getByLabel('Newsletter').uncheck();

// Toggle
await page.getByLabel('Dark mode').setChecked(true);
```

### Drag and Drop

```typescript
await page.getByTestId('source').dragTo(page.getByTestId('target'));
```

### File Upload

```typescript
await page.getByLabel('Upload file').setInputFiles('path/to/file.pdf');
await page.getByLabel('Upload files').setInputFiles([
  'file1.pdf',
  'file2.pdf',
]);
```

## Assertions

### Element Assertions

```typescript
// Visibility
await expect(page.getByRole('button')).toBeVisible();
await expect(page.getByRole('button')).toBeHidden();

// Enabled/Disabled
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByRole('button')).toBeDisabled();

// Checked
await expect(page.getByRole('checkbox')).toBeChecked();
await expect(page.getByRole('checkbox')).not.toBeChecked();

// Text content
await expect(page.getByRole('heading')).toHaveText('Welcome');
await expect(page.getByRole('heading')).toContainText('Welcome');

// Value
await expect(page.getByLabel('Email')).toHaveValue('user@example.com');

// Attribute
await expect(page.getByRole('link')).toHaveAttribute('href', '/about');

// Class
await expect(page.getByRole('button')).toHaveClass(/primary/);

// Count
await expect(page.getByRole('listitem')).toHaveCount(5);
```

### Page Assertions

```typescript
await expect(page).toHaveTitle('My App');
await expect(page).toHaveTitle(/My App/);
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveURL(/dashboard/);
```

### Response Assertions

```typescript
const response = await page.goto('/');
expect(response?.status()).toBe(200);
```

## Waiting

### Auto-Wait

Playwright auto-waits for elements to be actionable. Manual waits:

```typescript
// Wait for element
await page.getByRole('button').waitFor();
await page.getByRole('button').waitFor({ state: 'hidden' });

// Wait for URL
await page.waitForURL('/dashboard');
await page.waitForURL(/dashboard/);

// Wait for response
await page.waitForResponse('/api/users');
await page.waitForResponse((response) =>
  response.url().includes('/api') && response.status() === 200
);

// Wait for request
await page.waitForRequest('/api/users');

// Wait for load state
await page.waitForLoadState('networkidle');

// Custom timeout
await page.getByRole('button').click({ timeout: 10000 });
```

## Page Objects

```typescript
// pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
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

## Fixtures

```typescript
// fixtures.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';

type MyFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: Page;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },

  authenticatedPage: async ({ page }, use) => {
    // Login before test
    await page.goto('/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForURL('/dashboard');

    await use(page);
  },
});

export { expect } from '@playwright/test';

// tests/dashboard.spec.ts
import { test, expect } from '../fixtures';

test('shows user info', async ({ authenticatedPage }) => {
  await expect(authenticatedPage.getByText('Welcome')).toBeVisible();
});
```

## API Testing

```typescript
import { test, expect } from '@playwright/test';

test('API: create user', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com',
    },
  });

  expect(response.ok()).toBeTruthy();

  const user = await response.json();
  expect(user.name).toBe('John Doe');
});

test('API: get users', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();

  const users = await response.json();
  expect(users.length).toBeGreaterThan(0);
});
```

## Visual Testing

```typescript
test('screenshot comparison', async ({ page }) => {
  await page.goto('/');

  // Full page
  await expect(page).toHaveScreenshot('homepage.png');

  // Element
  await expect(page.getByRole('navigation')).toHaveScreenshot('nav.png');

  // With options
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
    threshold: 0.2,
  });
});
```

## Debugging

```bash
# Debug mode
npx playwright test --debug

# UI mode
npx playwright test --ui

# Headed mode
npx playwright test --headed

# Trace viewer
npx playwright show-trace trace.zip
```

```typescript
// Pause in test
await page.pause();

// Console log
console.log(await page.content());
console.log(await page.getByRole('heading').textContent());
```

## Best Practices

1. **Use role locators** - Most reliable and accessible
2. **Add test IDs sparingly** - Only when roles don't work
3. **Use page objects** - Reusable, maintainable
4. **Avoid hardcoded waits** - Use auto-wait
5. **Run in CI** - Catch regressions early

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using sleep/wait | Use auto-wait or waitFor |
| Fragile selectors | Use role-based locators |
| No assertions | Always verify outcomes |
| Tests depend on order | Make tests independent |
| Hardcoded data | Use fixtures |

## Reference Files

- [references/locators.md](references/locators.md) - Locator strategies
- [references/fixtures.md](references/fixtures.md) - Advanced fixtures
- [references/ci.md](references/ci.md) - CI configuration
