---
name: test-generation
description: Playwright test code generation from test case specifications. Use when writing automated tests, creating page objects, or generating test spec files. Triggers on "write tests", "generate automation", "create spec file", "page object", "Playwright code".
---

# Test Generation

Generate Playwright test code from test case designs.

## MANDATORY: Use Discovered Data, Not Assumptions

**⚠️ NEVER write tests with assumed error messages, selectors, or behaviors!**

Before writing ANY test that asserts on:
- Error messages → Discover the actual text first
- Validation messages → Discover HTML5 or custom validation first
- Element selectors → Discover from accessibility snapshot first
- Success states → Discover redirect URL or success message first

```typescript
// ❌ WRONG - Assumed error text (you don't know what it actually says!)
await expect(page.locator('.error')).toContainText('Invalid credentials');

// ✅ CORRECT - Use text discovered via browser_run_code
await expect(page.getByRole('alert')).toContainText('Email sau parolă incorectă');
```

**Workflow:**
1. Run `browser_run_code` to trigger the behavior (login failure, validation error, etc.)
2. Capture actual error text and selectors
3. Use those exact values in your test assertions

See `site-discovery` skill → Phase 4 for discovery examples.

## File Structure

```
tests/
├── auth.spec.ts           # Authentication tests
├── navigation.spec.ts     # Navigation tests
├── [feature].spec.ts      # Feature-specific tests
pages/
├── login.page.ts          # Page objects
├── [page].page.ts
```

## Page Object Pattern

```typescript
// pages/login.page.ts
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
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
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

  async expectLoaded() {
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }
}
```

## Test Spec Pattern

```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';

test.describe('Authentication - Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('valid credentials redirect to dashboard', async ({ page }) => {
    // Arrange
    const email = process.env.TEST_USER_EMAIL!;
    const password = process.env.TEST_USER_PASSWORD!;

    // Act
    await loginPage.login(email, password);

    // Assert
    await expect(page).toHaveURL(/dashboard/);
  });

  test('invalid password shows error', async ({ page }) => {
    // Act
    await loginPage.login('user@example.com', 'wrongpassword');

    // Assert
    await loginPage.expectError('Invalid credentials');
    await expect(page).toHaveURL(/login/);
  });
});
```

## Qase Integration

Link tests to Qase case IDs:

```typescript
test('valid login @qase(1)', async ({ page }) => {
  // Links to Qase case ID 1
});

// Or via annotation
test('valid login', async ({ page }) => {
  test.info().annotations.push({ type: 'qase', description: '1' });
});
```

## Test Naming Convention

```
[action] should [expected result]
```

Examples:
- `valid credentials should redirect to dashboard`
- `empty email should show validation error`
- `add to cart button should update cart count`

## Assertions Reference

```typescript
// Visibility
await expect(element).toBeVisible();
await expect(element).toBeHidden();

// Text
await expect(element).toHaveText('exact');
await expect(element).toContainText('partial');

// URL
await expect(page).toHaveURL(/dashboard/);
await expect(page).toHaveURL('https://example.com/path');

// Attributes
await expect(element).toHaveAttribute('href', '/path');
await expect(element).toHaveClass(/active/);

// State
await expect(element).toBeEnabled();
await expect(element).toBeDisabled();
await expect(element).toBeChecked();

// Count
await expect(elements).toHaveCount(5);

// Value
await expect(input).toHaveValue('text');
```

## Data-Driven Tests

```typescript
const testCases = [
  { email: '', password: 'pass', error: 'Email required' },
  { email: 'bad', password: 'pass', error: 'Invalid email' },
  { email: 'user@test.com', password: '', error: 'Password required' },
];

for (const { email, password, error } of testCases) {
  test(`shows "${error}" for invalid input`, async ({ page }) => {
    await loginPage.login(email, password);
    await loginPage.expectError(error);
  });
}
```

See [references/templates.md](references/templates.md) for more patterns.
