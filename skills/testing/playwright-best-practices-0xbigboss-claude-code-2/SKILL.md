---
name: playwright-best-practices
description: Provides Playwright test patterns for resilient locators, Page Object Models, fixtures, web-first assertions, and network mocking. Must use when writing or modifying Playwright tests (.spec.ts, .test.ts files with @playwright/test imports).
---

# Playwright Best Practices

## CLI Context: Prevent Context Overflow

When running Playwright tests from Claude Code or any CLI agent, always use minimal reporters to prevent verbose output from consuming the context window.

**Use `--reporter=line` or `--reporter=dot` for CLI test runs:**

```bash
# REQUIRED: Use minimal reporter to prevent context overflow
npx playwright test --reporter=line
npx playwright test --reporter=dot

# BAD: Default reporter generates thousands of lines, floods context
npx playwright test
```

Configure `playwright.config.ts` to use minimal reporters by default when `CI` or `CLAUDE` env vars are set:

```ts
reporter: process.env.CI || process.env.CLAUDE
  ? [['line'], ['html', { open: 'never' }]]
  : 'list',
```

## Locator Priority (Most to Least Resilient)

Always prefer user-facing attributes:

1. `page.getByRole('button', { name: 'Submit' })` - accessibility roles
2. `page.getByLabel('Email')` - form control labels
3. `page.getByPlaceholder('Search...')` - input placeholders
4. `page.getByText('Welcome')` - visible text (non-interactive)
5. `page.getByAltText('Logo')` - image alt text
6. `page.getByTitle('Settings')` - title attributes
7. `page.getByTestId('submit-btn')` - explicit test contracts
8. CSS/XPath - last resort, avoid

```ts
// BAD: Brittle selectors tied to implementation
page.locator('button.btn-primary.submit-form')
page.locator('//div[@class="container"]/form/button')
page.locator('#app > div:nth-child(2) > button')

// GOOD: User-facing, resilient locators
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Password')
```

### Chaining and Filtering

```ts
// Scope within a region
const card = page.getByRole('listitem').filter({ hasText: 'Product A' });
await card.getByRole('button', { name: 'Add to cart' }).click();

// Filter by child locator
const row = page.getByRole('row').filter({
  has: page.getByRole('cell', { name: 'John' })
});

// Combine conditions
const visibleSubmit = page.getByRole('button', { name: 'Submit' }).and(page.locator(':visible'));
const primaryOrSecondary = page.getByRole('button', { name: 'Save' }).or(page.getByRole('button', { name: 'Update' }));
```

### Strictness

Locators throw if multiple elements match. Use `first()`, `last()`, `nth()` only when intentional:

```ts
// Throws if multiple buttons match
await page.getByRole('button', { name: 'Delete' }).click();

// Explicit selection when needed
await page.getByRole('listitem').first().click();
await page.getByRole('row').nth(2).getByRole('button').click();
```

## Web-First Assertions

Use async assertions that auto-wait and retry:

```ts
// BAD: No auto-wait, flaky
expect(await page.getByText('Success').isVisible()).toBe(true);

// GOOD: Auto-waits up to timeout
await expect(page.getByText('Success')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
await expect(page.getByTestId('status')).toHaveText('Submitted');
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveTitle('Dashboard');

// Collections
await expect(page.getByRole('listitem')).toHaveCount(5);
await expect(page.getByRole('listitem')).toHaveText(['Item 1', 'Item 2', 'Item 3']);

// Soft assertions (continue on failure, report all)
await expect.soft(locator).toBeVisible();
await expect.soft(locator).toHaveText('Expected');
// Test continues, failures compiled at end
```

## Page Object Model

Encapsulate page interactions. Define locators as readonly properties in constructor.

```ts
// pages/base.page.ts
import { type Page, type Locator, expect } from '@playwright/test';
import debug from 'debug';

export abstract class BasePage {
  protected readonly log: debug.Debugger;

  constructor(
    protected readonly page: Page,
    protected readonly timeout = 30_000
  ) {
    this.log = debug(`test:page:${this.constructor.name}`);
  }

  protected async safeClick(locator: Locator, description?: string) {
    this.log('clicking: %s', description ?? locator);
    await expect(locator).toBeVisible({ timeout: this.timeout });
    await expect(locator).toBeEnabled({ timeout: this.timeout });
    await locator.click();
  }

  protected async safeFill(locator: Locator, value: string) {
    await expect(locator).toBeVisible({ timeout: this.timeout });
    await locator.fill(value);
  }

  abstract isLoaded(): Promise<void>;
}
```

```ts
// pages/login.page.ts
import { type Locator, type Page, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
    await this.isLoaded();
  }

  async isLoaded() {
    await expect(this.emailInput).toBeVisible();
  }

  async login(email: string, password: string) {
    await this.safeFill(this.emailInput, email);
    await this.safeFill(this.passwordInput, password);
    await this.safeClick(this.submitButton, 'Sign in button');
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toHaveText(message);
  }
}
```

## Fixtures

Prefer fixtures over beforeEach/afterEach. Fixtures encapsulate setup + teardown, run on-demand, and compose with dependencies.

```ts
// fixtures/index.ts
import { test as base, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { DashboardPage } from '../pages/dashboard.page';

type TestFixtures = {
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
};

export const test = base.extend<TestFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

export { expect };
```

### Worker-Scoped Fixtures

Use for expensive setup shared across tests (database connections, authenticated users):

```ts
// fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';

type WorkerFixtures = {
  authenticatedUser: { token: string; userId: string };
};

export const test = base.extend<{}, WorkerFixtures>({
  authenticatedUser: [async ({}, use) => {
    // Expensive setup - runs once per worker
    const user = await createTestUser();
    const token = await authenticateUser(user);

    await use({ token, userId: user.id });

    // Cleanup after all tests in worker
    await deleteTestUser(user.id);
  }, { scope: 'worker' }],
});
```

### Automatic Fixtures

Run for every test without explicit declaration:

```ts
export const test = base.extend<{ autoLog: void }>({
  autoLog: [async ({ page }, use) => {
    page.on('console', msg => console.log(`[browser] ${msg.text()}`));
    await use();
  }, { auto: true }],
});
```

## Authentication

Save authenticated state to reuse. Never log in via UI in every test.

```ts
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});
```

```ts
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### API Authentication (Faster)

```ts
setup('authenticate via API', async ({ request }) => {
  const response = await request.post('/api/auth/login', {
    data: { email: process.env.TEST_USER_EMAIL, password: process.env.TEST_USER_PASSWORD },
  });
  expect(response.ok()).toBeTruthy();
  await request.storageState({ path: authFile });
});
```

## Network Mocking

Set up routes before navigation.

```ts
test('displays mocked data', async ({ page }) => {
  await page.route('**/api/users', route => route.fulfill({
    json: [{ id: 1, name: 'Test User' }],
  }));

  await page.goto('/users');
  await expect(page.getByText('Test User')).toBeVisible();
});

// Modify real response
test('injects item into response', async ({ page }) => {
  await page.route('**/api/items', async route => {
    const response = await route.fetch();
    const json = await response.json();
    json.push({ id: 999, name: 'Injected' });
    await route.fulfill({ response, json });
  });
  await page.goto('/items');
});

// HAR recording
test('uses recorded responses', async ({ page }) => {
  await page.routeFromHAR('./fixtures/api.har', {
    url: '**/api/**',
    update: false, // true to record
  });
  await page.goto('/');
});
```

## Test Isolation

Each test gets fresh browser context. Never share state between tests.

```ts
// BAD: Tests depend on each other
let userId: string;
test('create user', async ({ request }) => {
  userId = (await (await request.post('/api/users', { data: { name: 'Test' } })).json()).id;
});
test('delete user', async ({ request }) => {
  await request.delete(`/api/users/${userId}`); // Depends on previous!
});

// GOOD: Each test creates its own data
test('can delete created user', async ({ request }) => {
  const { id } = await (await request.post('/api/users', { data: { name: 'Test' } })).json();
  const deleteResponse = await request.delete(`/api/users/${id}`);
  expect(deleteResponse.ok()).toBeTruthy();
});
```

## Configuration

```ts
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  // Use minimal reporter in CI/agent contexts to prevent context overflow
  reporter: process.env.CI || process.env.CLAUDE
    ? [['line'], ['html', { open: 'never' }]]
    : 'list',

  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },

  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      dependencies: ['setup'],
    },
  ],

  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Project Structure

```
tests/
  fixtures/           # Custom fixtures (extend base test)
  pages/              # Page Object Models
  helpers/            # Utility functions (API clients, data factories)
  auth.setup.ts       # Authentication setup project
  *.spec.ts           # Test files
playwright/
  .auth/              # Auth state storage (gitignored)
playwright.config.ts
```

Organize tests by feature or user journey. Colocate page objects with tests when possible.

## Helpers (Separate from Pages)

```ts
// helpers/user.helper.ts
import type { Page } from '@playwright/test';
import debug from 'debug';

const log = debug('test:helper:user');

export class UserHelper {
  constructor(private page: Page) {}

  async createUser(data: { name: string; email: string }) {
    log('creating user: %s', data.email);
    const response = await this.page.request.post('/api/users', { data });
    return response.json();
  }

  async deleteUser(id: string) {
    log('deleting user: %s', id);
    await this.page.request.delete(`/api/users/${id}`);
  }
}

// helpers/data.factory.ts
export function createTestUser(overrides: Partial<User> = {}): User {
  return {
    id: crypto.randomUUID(),
    email: `test-${Date.now()}@example.com`,
    name: 'Test User',
    ...overrides,
  };
}
```

## Debugging

```bash
npx playwright test --debug          # Step through with inspector
npx playwright test --trace on       # Record trace for all tests
npx playwright test --ui             # Interactive UI mode
npx playwright codegen localhost:3000 # Generate locators interactively
npx playwright show-report           # View HTML report
```

Enable debug logs: `DEBUG=test:* npx playwright test`

## Anti-Patterns

- `page.waitForTimeout(ms)` - use auto-waiting locators instead
- `page.locator('.class')` - use role/label/testid
- XPath selectors - fragile, use user-facing attributes
- Shared state between tests - each test creates own data
- UI login in every test - use setup project + storageState
- Manual assertions without await - use web-first assertions
- Hardcoded waits - rely on Playwright's auto-waiting
- Default reporter in CI/agent - use `--reporter=line` or `--reporter=dot` to prevent context overflow

## Checklist

- [ ] Locators use role/label/testid, not CSS classes or XPath
- [ ] All assertions use `await expect()` web-first matchers
- [ ] Page objects define locators in constructor
- [ ] No `page.waitForTimeout()` - use auto-waiting
- [ ] Tests isolated - no shared state
- [ ] Auth state reused via setup project
- [ ] Network mocks set up before navigation
- [ ] Test data created per-test or via fixtures
- [ ] Debug logging added for complex flows
- [ ] Minimal reporter (`line`/`dot`) used in CI/agent contexts
