---
name: playwright-testing
description: Comprehensive guide for modern front-end testing with Playwright (2025). This skill should be used when writing end-to-end tests, component tests, or visual regression tests for web applications using Playwright. Covers Page Object Model patterns, TypeScript integration, modern SPA testing strategies, accessibility testing, and CI/CD automation with GitHub Actions.
---

# Playwright Testing

## Overview

To build reliable, maintainable end-to-end tests for modern web applications, follow Playwright best practices with TypeScript, Page Object Model patterns, and automated CI/CD integration. This skill provides comprehensive guidance for testing SPAs (React, Vue, Angular) and traditional web applications using Playwright's powerful automation capabilities.

**Current Playwright Version:** 1.48+ (as of 2025)
**Language:** TypeScript with strict typing
**Test Runner:** Playwright Test (@playwright/test)
**CI/CD:** GitHub Actions, Docker support
**Standard Patterns:** Page Object Model, Fixtures, Component Testing

## Decision Tree: Choosing Your Testing Approach

```
User Request → What type of test are you creating?
    |
    ├─ End-to-end user flow test?
    │   ├─ Single page interaction? → Use Quick Start: Basic Test
    │   └─ Multi-page workflow? → Use Page Object Model Pattern
    │
    ├─ Component testing in isolation?
    │   └─ Load references/component-testing-guide.md
    │
    ├─ Visual regression testing?
    │   └─ Load references/visual-testing-guide.md
    │
    ├─ Setting up new Playwright project?
    │   └─ Run scripts/init-playwright.ts
    │
    ├─ Creating reusable page objects?
    │   ├─ Run scripts/generate-page-object.ts for scaffolding
    │   └─ Load references/page-object-patterns.md for patterns
    │
    ├─ Debugging flaky tests?
    │   └─ Load references/anti-patterns.md
    │
    ├─ Optimizing test selectors?
    │   └─ Load references/locator-strategies.md
    │
    └─ Setting up CI/CD pipeline?
        └─ Use assets/workflows/playwright-tests.yml
```

## Quick Start: Basic Test

### Simple Test with TypeScript

```typescript
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  // Navigate to application
  await page.goto('https://app.example.com');

  // Interact with elements using recommended locators
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('SecurePass123');
  await page.getByRole('button', { name: 'Sign in' }).click();

  // Assert expected outcomes
  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Welcome back' })).toBeVisible();
});
```

### Test with Multiple Assertions

```typescript
import { test, expect } from '@playwright/test';

test.describe('Shopping Cart', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/products');
  });

  test('add item to cart', async ({ page }) => {
    // Find and click product
    const product = page.getByRole('article').filter({ hasText: 'Premium Headphones' });
    await product.getByRole('button', { name: 'Add to cart' }).click();

    // Verify cart updated
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // Navigate to cart
    await page.getByRole('link', { name: 'Cart' }).click();

    // Verify item in cart
    await expect(page.getByRole('heading', { name: 'Premium Headphones' })).toBeVisible();
    await expect(page.getByText('$199.99')).toBeVisible();
  });
});
```

## Workflow: Creating Comprehensive Test Suites

Follow this structured approach to build maintainable test suites for your application.

### Step 1: Analyze Application Structure

To begin testing effectively:

1. **Map user journeys**: Identify critical paths users take
2. **Identify page boundaries**: Determine logical page groupings
3. **List reusable components**: Find common UI patterns
4. **Document test data needs**: Understand data dependencies

### Step 2: Set Up Project Structure

Initialize your Playwright project with proper TypeScript configuration:

```bash
# Run initialization script
npx tsx scripts/init-playwright.ts
```

This creates:
- TypeScript configuration with strict typing
- Playwright config with parallel execution
- Base fixture setup
- Initial folder structure

### Step 3: Implement Page Objects

Create page objects for reusable, maintainable tests:

```typescript
// pages/LoginPage.ts
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

**Use the page object generator for scaffolding:**
```bash
npx tsx scripts/generate-page-object.ts --url="/login" --name="LoginPage"
```

### Step 4: Write Test Scenarios

Structure tests using Given-When-Then pattern:

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Authentication', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    // Given: Valid user credentials
    const email = 'user@example.com';
    const password = 'ValidPass123';

    // When: User attempts to login
    await loginPage.login(email, password);

    // Then: User is redirected to dashboard
    await expect(page).toHaveURL('/dashboard');
  });

  test('invalid credentials show error', async () => {
    // When: User enters invalid credentials
    await loginPage.login('bad@email.com', 'wrong');

    // Then: Error message is displayed
    await loginPage.expectError('Invalid email or password');
  });
});
```

### Step 5: Implement Visual Testing

Add visual regression tests for UI consistency:

```typescript
import { test, expect } from '@playwright/test';

test('homepage visual consistency', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
    animations: 'disabled'
  });

  // Component screenshot
  const header = page.getByRole('banner');
  await expect(header).toHaveScreenshot('header.png');
});
```

**Update baselines when intentional changes are made:**
```bash
npx tsx scripts/visual-baseline.ts --update
```

### Step 6: Configure CI/CD

Deploy the GitHub Actions workflow for automated testing:

```yaml
# .github/workflows/playwright.yml
name: Playwright Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

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
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

## Core Testing Principles

### 1. Test User Behavior, Not Implementation

Write tests from the user's perspective:

```typescript
// ✅ Good: Tests user-visible behavior
await page.getByRole('button', { name: 'Submit order' }).click();
await expect(page.getByText('Order confirmed')).toBeVisible();

// ❌ Bad: Tests implementation details
await page.locator('#submit-btn-2947').click();
await expect(page.locator('.success-msg-div')).toHaveClass('visible');
```

### 2. Use Semantic Locators

Prefer accessible, semantic locators that won't break with styling changes:

```typescript
// Priority order for locators:
// 1. User-facing attributes
await page.getByRole('button', { name: 'Save' });
await page.getByLabel('Email address');
await page.getByPlaceholder('Search products...');
await page.getByText('Welcome back');

// 2. Test IDs (when needed for complex elements)
await page.getByTestId('product-card-12345');

// 3. CSS/XPath (avoid when possible)
await page.locator('css=.dynamic-content'); // Last resort
```

### 3. Isolate Test State

Each test should run independently:

```typescript
test.describe('User Profile', () => {
  // Create fresh user for each test
  test.beforeEach(async ({ page, request }) => {
    const user = await createTestUser(request);
    await authenticateUser(page, user);
  });

  test.afterEach(async ({ request }, testInfo) => {
    // Cleanup test data
    await cleanupTestUser(request, testInfo);
  });

  test('update profile name', async ({ page }) => {
    // Test runs with isolated user
  });
});
```

### 4. Handle Asynchronous Operations

Playwright auto-waits, but be explicit when needed:

```typescript
// Auto-wait handles most cases
await page.getByRole('button', { name: 'Load data' }).click();
await expect(page.getByTestId('data-table')).toBeVisible();

// Explicit wait for specific conditions
await page.waitForResponse(resp =>
  resp.url().includes('/api/data') && resp.status() === 200
);

// Wait for network idle
await page.waitForLoadState('networkidle');
```

### 5. Implement Retry Logic Wisely

Configure retries for flaky scenarios, but investigate root causes:

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: {
    // Retry navigation on failure
    navigationTimeout: 30000,
    actionTimeout: 15000,
  },
});

// Per-test retry configuration
test('flaky integration test', async ({ page }) => {
  test.info().annotations.push({
    type: 'flaky',
    description: 'External API occasionally slow'
  });
  // Test implementation
});
```

## Testing Modern SPAs

### React Testing Patterns

```typescript
// Wait for React to hydrate
await page.waitForFunction(() => window.React && window.React.version);

// Test React components
const component = page.getByTestId('user-list');
await expect(component).toBeVisible();
await expect(component.locator('[data-testid="user-item"]')).toHaveCount(5);
```

### Vue Testing Patterns

```typescript
// Wait for Vue app to mount
await page.waitForFunction(() => window.Vue && document.querySelector('#app').__vue__);

// Interact with Vue components
await page.getByRole('button', { name: 'Toggle' }).click();
await expect(page.getByTestId('toggle-state')).toHaveText('active');
```

### Angular Testing Patterns

```typescript
// Wait for Angular to bootstrap
await page.waitForFunction(() => window.getAllAngularTestabilities);

// Test Angular forms
await page.getByLabel('Username').fill('testuser');
await page.getByLabel('Email').fill('test@example.com');
await expect(page.getByRole('button', { name: 'Submit' })).toBeEnabled();
```

## Quick Reference: Common Patterns

### Authentication Flow
```typescript
export async function authenticateUser(page: Page, credentials: UserCredentials) {
  await page.goto('/login');
  await page.getByLabel('Email').fill(credentials.email);
  await page.getByLabel('Password').fill(credentials.password);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await page.waitForURL('/dashboard');
}
```

### API Mocking
```typescript
await page.route('**/api/users', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Test User' }])
  });
});
```

### File Upload
```typescript
const fileInput = page.getByLabel('Upload file');
await fileInput.setInputFiles('path/to/file.pdf');
await expect(page.getByText('file.pdf')).toBeVisible();
```

### Accessibility Testing
```typescript
import { injectAxe, checkA11y } from 'axe-playwright';

test('page is accessible', async ({ page }) => {
  await page.goto('/');
  await injectAxe(page);
  await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: { html: true }
  });
});
```

## Resources

This skill includes comprehensive reference materials and templates:

### references/page-object-patterns.md
Advanced Page Object Model patterns including fixtures, page managers, composition patterns, and enterprise-scale organization strategies.

**Load when:** Implementing page objects, organizing large test suites, or creating reusable test components.

### references/component-testing-guide.md
Guide for testing UI components in isolation for React, Vue, and Angular applications, including mounting strategies and state management.

**Load when:** Testing individual components, setting up component test harnesses, or testing component interactions.

### references/visual-testing-guide.md
Visual regression testing strategies including screenshot comparison, viewport testing, cross-browser visual testing, and baseline management.

**Load when:** Implementing visual tests, managing screenshot baselines, or debugging visual differences.

### references/locator-strategies.md
Modern selector strategies for reliable element location, including auto-waiting patterns, shadow DOM traversal, and dynamic content handling.

**Load when:** Writing resilient selectors, debugging flaky locators, or handling complex DOM structures.

### references/anti-patterns.md
Common Playwright testing mistakes and how to avoid them, including test coupling, hard-coded waits, and improper assertion patterns.

**Load when:** Reviewing test quality, debugging failures, or training team members on best practices.

### Scripts
- **init-playwright.ts**: Initialize Playwright in existing project with TypeScript
- **generate-page-object.ts**: Generate page object scaffolding from URL
- **visual-baseline.ts**: Manage visual regression baselines

### Templates
- **base-page.template.ts**: Base page class with common functionality
- **component-test.template.ts**: Component testing setup
- **fixture.template.ts**: Custom fixture patterns
- **playwright.config.template.ts**: Production-ready configuration

## Tips for Success

1. **Start with critical paths**: Test the most important user journeys first
2. **Use data-testid sparingly**: Prefer semantic selectors, use test IDs only when necessary
3. **Run tests in parallel**: Configure workers for faster execution
4. **Mock external dependencies**: Use route handlers to control external services
5. **Review test reports**: Analyze failures to identify patterns
6. **Keep tests focused**: One test should verify one behavior
7. **Maintain test independence**: Tests should not depend on execution order

## When to Load Reference Files

To optimize context usage, load reference files strategically:

- **Load page-object-patterns.md** when:
  - Implementing Page Object Model
  - Creating reusable test utilities
  - Organizing large test suites
  - Need fixture patterns

- **Load component-testing-guide.md** when:
  - Testing components in isolation
  - Setting up component test environment
  - Working with framework-specific components

- **Load visual-testing-guide.md** when:
  - Implementing screenshot tests
  - Managing visual baselines
  - Setting up visual regression workflow

- **Load locator-strategies.md** when:
  - Writing complex selectors
  - Debugging flaky tests
  - Working with dynamic content

- **Load anti-patterns.md** when:
  - Reviewing existing tests
  - Training team members
  - Debugging test failures
  - Improving test quality