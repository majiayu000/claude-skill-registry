---
name: writing-playwright-tests
description: Provides patterns for writing maintainable E2E test scripts with Playwright, focusing on selector strategies, page objects, and wait handling for legacy application retrofitting.
---

# Playwright E2E Testing Skill

## 1. Selector Strategy Hierarchy

Use selectors in this priority order for maximum resilience:

```typescript
// BEST: Explicit test identifiers
page.getByTestId('submit-button')

// GOOD: Semantic role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { level: 1 })
page.getByRole('textbox', { name: 'Email' })

// GOOD: User-visible text
page.getByText('Welcome back')
page.getByLabel('Email address')
page.getByPlaceholder('Enter your email')

// ACCEPTABLE: When above options unavailable
page.locator('[data-cy="element"]')  // Cypress migration
page.locator('#unique-id')            // Stable IDs only

// AVOID: Brittle structural selectors
page.locator('.btn-primary')          // Classes change
page.locator('div > span:nth-child(2)') // Structure changes
page.locator('//div[@class="foo"]')   // XPath fragile
```

### Adding Test IDs to Legacy Apps

When retrofitting, add data-testid attributes incrementally:

```html
<!-- Before: Relies on brittle class selector -->
<button class="btn btn-primary submit-form">Submit</button>

<!-- After: Resilient test identifier -->
<button class="btn btn-primary submit-form" data-testid="contact-form-submit">Submit</button>
```

Naming convention for test IDs:
```
{component}-{element}-{qualifier}
contact-form-submit
user-list-row-{id}
modal-confirm-button
nav-menu-toggle
```

## 2. Page Object Model

### Basic Page Object

```typescript
// pages/login.page.ts
import { Page, Locator } from '@playwright/test';

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
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
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
    await expect(this.errorMessage).toContainText(message);
  }
}
```

### Page Object with Component Composition

```typescript
// components/data-table.component.ts
import { Page, Locator } from '@playwright/test';

export class DataTableComponent {
  readonly container: Locator;
  readonly rows: Locator;
  readonly searchInput: Locator;
  readonly pagination: Locator;

  constructor(page: Page, containerSelector: string) {
    this.container = page.locator(containerSelector);
    this.rows = this.container.getByRole('row');
    this.searchInput = this.container.getByPlaceholder('Search');
    this.pagination = this.container.locator('[data-testid="pagination"]');
  }

  async search(term: string) {
    await this.searchInput.fill(term);
    await this.searchInput.press('Enter');
  }

  async getRowCount(): Promise<number> {
    return await this.rows.count() - 1; // Exclude header
  }

  async clickRow(index: number) {
    await this.rows.nth(index + 1).click(); // Skip header
  }
}

// pages/contacts.page.ts
export class ContactsPage {
  readonly page: Page;
  readonly table: DataTableComponent;
  readonly addButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.table = new DataTableComponent(page, '[data-testid="contacts-table"]');
    this.addButton = page.getByRole('button', { name: 'Add Contact' });
  }
}
```

## 3. Wait Strategies

### Explicit Waits

```typescript
// Wait for navigation
await page.waitForURL('**/dashboard');
await page.waitForURL(/\/users\/\d+/);

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for element state
await expect(element).toBeVisible();
await expect(element).toBeEnabled();
await expect(element).toHaveText('Ready');

// Wait for element to appear
await page.waitForSelector('[data-testid="results"]');

// Wait for element to disappear
await expect(page.getByTestId('loading')).toBeHidden();
```

### Waiting for Dynamic Content

```typescript
// Wait for API response before asserting
await page.waitForResponse(resp =>
  resp.url().includes('/api/contacts') && resp.status() === 200
);

// Wait for specific number of elements
await expect(page.getByRole('listitem')).toHaveCount(10);

// Custom wait with polling
await expect(async () => {
  const count = await page.getByRole('row').count();
  expect(count).toBeGreaterThan(5);
}).toPass({ timeout: 10000 });
```

### Handling Loading States

```typescript
async function waitForTableLoad(page: Page, tableLocator: Locator) {
  // Wait for loading indicator to disappear
  await expect(page.getByTestId('table-loading')).toBeHidden();

  // Wait for at least one row
  await expect(tableLocator.getByRole('row')).not.toHaveCount(0);
}

async function waitForModalClose(page: Page) {
  await expect(page.getByRole('dialog')).toBeHidden();
}
```

## 4. Test Structure

### Basic Test File

```typescript
// tests/contacts.spec.ts
import { test, expect } from '@playwright/test';
import { ContactsPage } from '../pages/contacts.page';

test.describe('Contacts Management', () => {
  let contactsPage: ContactsPage;

  test.beforeEach(async ({ page }) => {
    contactsPage = new ContactsPage(page);
    await page.goto('/contacts');
  });

  test('displays contact list', async ({ page }) => {
    await expect(contactsPage.table.rows).not.toHaveCount(0);
  });

  test('filters contacts by search', async ({ page }) => {
    await contactsPage.table.search('John');

    const rows = contactsPage.table.rows;
    await expect(rows).toHaveCount(2);
  });

  test('opens contact details on row click', async ({ page }) => {
    await contactsPage.table.clickRow(0);

    await expect(page).toHaveURL(/\/contacts\/\d+/);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  });
});
```

### Test with Authentication

```typescript
// tests/authenticated.spec.ts
import { test, expect } from '@playwright/test';

// Use authenticated state from fixture
test.use({ storageState: 'playwright/.auth/user.json' });

test.describe('Dashboard (authenticated)', () => {
  test('shows user dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });
});
```

## 5. Common Interactions

### Form Interactions

```typescript
// Text input
await page.getByLabel('Name').fill('John Doe');
await page.getByLabel('Name').clear();

// Select dropdown
await page.getByLabel('Country').selectOption('US');
await page.getByLabel('Country').selectOption({ label: 'United States' });

// Checkbox
await page.getByLabel('Accept terms').check();
await page.getByLabel('Accept terms').uncheck();

// Radio button
await page.getByLabel('Express shipping').check();

// Date picker (fill underlying input)
await page.getByLabel('Start date').fill('2024-01-15');

// File upload
await page.getByLabel('Upload file').setInputFiles('path/to/file.pdf');
await page.getByLabel('Upload file').setInputFiles(['file1.pdf', 'file2.pdf']);
```

### Click Interactions

```typescript
// Standard click
await page.getByRole('button', { name: 'Submit' }).click();

// Double click
await page.getByTestId('row-1').dblclick();

// Right click
await page.getByTestId('item').click({ button: 'right' });

// Click with modifier
await page.getByRole('link').click({ modifiers: ['Control'] });

// Force click (bypasses actionability checks)
await page.getByTestId('hidden-button').click({ force: true });
```

### Keyboard Interactions

```typescript
// Type with delay (for autocomplete)
await page.getByLabel('Search').pressSequentially('playwright', { delay: 100 });

// Special keys
await page.keyboard.press('Enter');
await page.keyboard.press('Escape');
await page.keyboard.press('Tab');

// Key combinations
await page.keyboard.press('Control+a');
await page.keyboard.press('Control+c');
```

## 6. Assertions

### Element Assertions

```typescript
// Visibility
await expect(element).toBeVisible();
await expect(element).toBeHidden();

// State
await expect(element).toBeEnabled();
await expect(element).toBeDisabled();
await expect(element).toBeChecked();
await expect(element).toBeFocused();

// Content
await expect(element).toHaveText('Hello');
await expect(element).toContainText('Hello');
await expect(element).toHaveValue('input value');

// Attributes
await expect(element).toHaveAttribute('href', '/home');
await expect(element).toHaveClass(/active/);

// Count
await expect(page.getByRole('listitem')).toHaveCount(5);
```

### Page Assertions

```typescript
// URL
await expect(page).toHaveURL('https://example.com/dashboard');
await expect(page).toHaveURL(/dashboard/);

// Title
await expect(page).toHaveTitle('Dashboard - App');
await expect(page).toHaveTitle(/Dashboard/);
```

### Soft Assertions

```typescript
// Continue test even if assertion fails
await expect.soft(element).toHaveText('Expected');
await expect.soft(page).toHaveTitle('Title');

// Check for any soft assertion failures
expect(test.info().errors).toHaveLength(0);
```

## 7. Configuration

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
    ['json', { outputFile: 'test-results/results.json' }],
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
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## 8. Quick Reference

### CLI Commands

```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test contacts.spec.ts

# Run tests with UI mode
npx playwright test --ui

# Run in headed mode (see browser)
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Generate code
npx playwright codegen http://localhost:3000

# Show report
npx playwright show-report
```

### Common Patterns

```typescript
// Retry flaky assertion
await expect(element).toBeVisible({ timeout: 10000 });

// Wait between actions (avoid unless necessary)
await page.waitForTimeout(1000);

// Get element text
const text = await element.textContent();

// Check element exists without waiting
const exists = await element.count() > 0;

// Screenshot for debugging
await page.screenshot({ path: 'debug.png', fullPage: true });
```

---

**See REFERENCE.md for**: Authentication fixtures, network mocking, visual regression, debugging traces, CI/CD integration, and legacy app retrofitting strategies.
