---
name: vue-playwright-testing
description: Comprehensive guide for testing Vue 3 applications with Playwright (2025). This skill should be used when writing end-to-end tests or component tests for Vue apps, testing Vue Router navigation, reactive state changes, authentication flows, or setting up Playwright in Vue projects.
---

# Vue 3 + Playwright Testing

## Overview

To build reliable tests for Vue 3 applications, use Playwright for both end-to-end testing and experimental component testing. Playwright integrates seamlessly with Vue's reactivity system, Vue Router navigation, and Vite build pipeline. This skill provides Vue-specific guidance for writing maintainable tests while avoiding common pitfalls like timeout anti-patterns.

**Current Versions:** Playwright 1.48+, Vue 3.5+, Vite 6+
**Standard Approach:** Semantic locators, conditional waits, API mocking
**Key Philosophy:** Never use arbitrary timeouts to fix flaky tests

## Decision Tree: What Type of Test?

```
Vue Test Request → What are you testing?
    |
    ├─ End-to-end user flow (login, forms, navigation)?
    │   ├─ Single page interaction? → Use Quick Start: E2E Test
    │   └─ Multi-page workflow? → Load references/e2e-patterns.md
    │
    ├─ Individual Vue component in isolation?
    │   └─ Load references/component-testing.md
    │
    ├─ Vue Router navigation or page transitions?
    │   └─ Load references/vue-specific-patterns.md → Router section
    │
    ├─ Reactive state changes or Pinia store?
    │   └─ Load references/vue-specific-patterns.md → State Management
    │
    ├─ Authentication flow?
    │   └─ Load references/vue-specific-patterns.md → Authentication
    │
    ├─ Test is failing intermittently/flaky?
    │   └─ Load references/best-practices.md → Debugging Flaky Tests section
    │
    └─ Setting up Playwright in Vue project?
        └─ Use Quick Start: Project Setup
```

## Quick Start: Project Setup

### Initialize Playwright in Vue Project

```bash
npm init playwright@latest -- --ct
```

This command:
- Installs `@playwright/test` and `@playwright/experimental-ct-vue`
- Downloads browsers
- Creates `playwright.config.ts`
- Sets up test structure

For Vue projects with Vite, ensure `playwright.config.ts` includes:

```typescript
import { defineConfig, devices } from '@playwright/test';
import react from '@vitejs/plugin-react';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
});
```

## Quick Start: E2E Test

### Basic E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('user can login successfully', async ({ page }) => {
    // Use semantic locators (getByLabel, getByRole)
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');

    // Click submit button
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Wait for URL change (condition-based, not timeout)
    await expect(page).toHaveURL('/dashboard');

    // Assert Vue app rendered correctly
    await expect(page.getByRole('heading', { name: /Welcome/i })).toBeVisible();
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.getByLabel('Email').fill('bad@email.com');
    await page.getByLabel('Password').fill('wrong');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Wait for error message to appear
    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
  });
});
```

## Quick Start: Component Test

### Testing Vue Component in Isolation

```typescript
import { test, expect } from '@playwright/experimental-ct-vue';
import Button from './Button.vue';

test('button emits click event', async ({ mount }) => {
  const messages: string[] = [];

  const component = await mount(Button, {
    props: { label: 'Click me' },
    on: {
      click: () => messages.push('clicked')
    }
  });

  await component.getByRole('button').click();
  expect(messages).toEqual(['clicked']);
});
```

## Core Vue 3 + Playwright Principles

### 1. Never Use Arbitrary Timeouts to Fix Flaky Tests

**❌ BAD: Masking the real issue**
```typescript
// This is a code smell - something is wrong
await page.waitForTimeout(3000);
await page.click('button');
```

**✅ GOOD: Wait for the specific condition**
```typescript
// Wait for button to be enabled
await page.locator('button:not([disabled])').waitFor();
await page.getByRole('button').click();

// Or use Playwright's auto-waiting
await page.getByRole('button', { name: 'Submit' }).click();
```

**Why?** Arbitrary timeouts hide race conditions, selector problems, or network issues. When you see a flaky test, investigate the root cause:
- Is the selector wrong? Use dev tools to verify
- Is data loading? Wait for the API response
- Is Vue not mounted yet? Check the condition
- Is the element disabled? Wait for the disabled attribute to be removed

### 2. Use Semantic Locators for Stability

Priority order (most stable to least):

```typescript
// ✅ 1. User-facing text/roles (most stable)
await page.getByRole('button', { name: 'Save' });
await page.getByLabel('Email');
await page.getByPlaceholder('Search...');
await page.getByText('Welcome');

// ✅ 2. Test IDs (when semantic locators insufficient)
await page.getByTestId('product-card');

// ❌ 3. CSS/XPath selectors (avoid - fragile)
await page.locator('css=.dynamic-button');
```

### 3. Test Vue-Specific Behavior

Wait for Vue app to be ready before interactions:

```typescript
// Wait for Vue app to mount
test('app loads correctly', async ({ page }) => {
  await page.goto('/');

  // Playwright auto-waits, but be explicit for Vue:
  await page.waitForFunction(() => {
    // Check Vue app is mounted
    return !!(window as any).__VUE_DEVTOOLS_GLOBAL_HOOK__?.enabled;
  });

  // Now safe to interact
  await page.getByRole('button').click();
});
```

### 4. Test Reactive State Changes

Test observable behavior from reactive updates:

```typescript
test('counter increments', async ({ page }) => {
  await page.goto('/counter');

  // Initial state
  await expect(page.getByText('Count: 0')).toBeVisible();

  // Click increment
  await page.getByRole('button', { name: 'Increment' }).click();

  // Reactive update (Playwright auto-waits for DOM change)
  await expect(page.getByText('Count: 1')).toBeVisible();
});
```

### 5. Mock Network Requests

Control external APIs for consistent tests:

```typescript
test('fetches and displays data', async ({ page }) => {
  // Intercept API calls
  await page.route('**/api/users', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([{ id: 1, name: 'Test User' }])
    });
  });

  await page.goto('/users');

  // Assert mocked data is displayed
  await expect(page.getByText('Test User')).toBeVisible();
});
```

## Common Vue Testing Patterns

### Pattern: Testing Vue Router Navigation

```typescript
test('navigates to product details', async ({ page }) => {
  await page.goto('/products');

  // Click product link
  await page.getByRole('link', { name: 'Product A' }).click();

  // Wait for URL change (conditional, not timeout)
  await expect(page).toHaveURL('/products/1');

  // Assert component mounted with correct data
  await expect(page.getByRole('heading', { name: 'Product A' })).toBeVisible();
});
```

### Pattern: Testing Form Validation

```typescript
test('validates form before submit', async ({ page }) => {
  await page.goto('/contact');

  // Leave required field empty
  await page.getByLabel('Email').fill('');
  await page.getByLabel('Message').fill('Hello');

  // Try to submit
  await page.getByRole('button', { name: 'Send' }).click();

  // Error message should appear
  await expect(page.getByText('Email is required')).toBeVisible();

  // Form should not submit
  await expect(page).toHaveURL('/contact');
});
```

### Pattern: Testing Modal Dialogs

```typescript
test('modal closes on cancel', async ({ page }) => {
  await page.goto('/');

  // Open modal
  await page.getByRole('button', { name: 'Open Dialog' }).click();
  await expect(page.getByRole('dialog')).toBeVisible();

  // Close modal
  await page.getByRole('button', { name: 'Cancel' }).click();

  // Modal should disappear
  await expect(page.getByRole('dialog')).not.toBeVisible();
});
```

## When to Load Reference Files

Load these strategically to optimize context usage:

### references/e2e-patterns.md
- Building multi-page E2E workflows
- Implementing Page Object Model for Vue tests
- Testing complex user journeys
- Multi-step authentication flows

### references/component-testing.md
- Testing Vue components in isolation
- Setting up experimental component testing
- Testing props, events, slots
- Testing composables with components

### references/vue-specific-patterns.md
- Vue Router testing patterns
- Pinia state management testing
- Vue reactivity and computed properties
- Authentication testing in Vue
- Understanding wait patterns for Vue

### references/best-practices.md
- Debugging flaky tests (and why timeouts aren't the answer)
- Selector strategies and troubleshooting
- API mocking patterns
- CI/CD configuration
- Performance optimization

## Tips for Success

1. **Start with semantic locators** - They're more stable and maintainable
2. **Never reach for timeouts first** - If tests are flaky, investigate the root cause
3. **Test user behavior** - Not implementation details or Vue internals
4. **Mock external APIs** - For consistency and speed
5. **Run tests in parallel** - Playwright supports parallel execution by default
6. **Use traces and videos** - For debugging failed tests
7. **Review flaky tests immediately** - Don't ignore intermittent failures
8. **Keep tests focused** - One test should verify one behavior
9. **Set up CI/CD early** - Use provided GitHub Actions workflow
10. **Reference the Vue-specific patterns** - Understand how to wait for Vue correctly

## File Structure

```
my-vue-app/
├── tests/
│   ├── e2e/
│   │   ├── login.spec.ts
│   │   ├── products.spec.ts
│   │   └── checkout.spec.ts
│   ├── fixtures/
│   │   ├── auth.ts
│   │   └── data.ts
│   └── pages/
│       ├── LoginPage.ts
│       ├── ProductsPage.ts
│       └── CheckoutPage.ts
├── playwright.config.ts
└── package.json
```

## Resources

This skill includes references, templates, and scripts:

### references/e2e-patterns.md
Comprehensive guide to E2E testing for Vue applications using Page Object Model and multi-page workflows.

### references/component-testing.md
Guide to testing Vue components in isolation using Playwright's experimental component testing.

### references/vue-specific-patterns.md
Vue-specific testing patterns including Router navigation, Pinia state management, reactivity testing, and proper wait strategies.

### references/best-practices.md
Best practices including timeout anti-patterns, debugging flaky tests, selector strategies, and CI/CD setup.

### assets/playwright.config.template.ts
Production-ready Playwright configuration optimized for Vue with Vite.

### assets/workflows/playwright-vue.yml
GitHub Actions workflow for automated Playwright testing in CI/CD pipeline.

### scripts/init-vue-playwright.ts
Setup script to initialize Playwright in an existing Vue project with proper configuration.
