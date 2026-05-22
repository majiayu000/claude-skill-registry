---
name: playwright-writing
description: Write reliable Playwright E2E tests following official best practices. Prioritizes user-facing locators, web-first assertions, and test isolation. NEVER mock application data. Avoid explicit waits unless component-specific. Use when writing, reviewing, or debugging Playwright tests.
version: 1.0.0
dependencies: "@playwright/test"
---

# Playwright Writing

## Purpose
Guide the creation of reliable, maintainable Playwright E2E tests that test real user-visible behavior against real application data.

## When NOT to Use
- Unit tests (use Jest/Vitest instead)
- Integration tests that don't need browser automation
- API-only testing (use Playwright's API testing or dedicated tools)
- Performance/load testing (use k6, Artillery, etc.)

---

## 🚫 FORBIDDEN Patterns (Zero Tolerance)

### Never Mock Application Data
**Your tests MUST hit your real API endpoints.**

```typescript
// ❌ FORBIDDEN - mocking YOUR app's API
await page.route('/api/users', route => route.fulfill({
  body: JSON.stringify([{ id: 1, name: 'Mock User' }])
}));

await page.route('/api/products/**', route => route.fulfill({
  body: JSON.stringify({ price: 99.99 })
}));
```

**Exception:** External third-party APIs you don't control:
```typescript
// ✅ ACCEPTABLE - mocking external third-party
await page.route('https://api.stripe.com/**', route => route.fulfill({
  body: JSON.stringify({ success: true })
}));

await page.route('https://analytics.google.com/**', route => route.abort());
```

### Never Use Explicit Timeouts
**`page.waitForTimeout()` is FORBIDDEN.**

```typescript
// ❌ FORBIDDEN - arbitrary wait
await page.waitForTimeout(2000);
await page.waitForTimeout(500);

// ❌ FORBIDDEN - sleep/delay patterns
await new Promise(resolve => setTimeout(resolve, 1000));
```

**Use web-first assertions that auto-wait instead:**
```typescript
// ✅ CORRECT - waits for condition automatically
await expect(page.getByText('Loaded')).toBeVisible();
await expect(page.getByRole('button')).toBeEnabled();
```

### Never Use CSS Class Selectors
**CSS classes are for styling, not testing.**

```typescript
// ❌ FORBIDDEN - CSS class selectors
page.locator('.btn-primary')
page.locator('.submit-form')
page.locator('.MuiButton-root')
page.locator('.card-container > .item')

// ❌ FORBIDDEN - complex CSS selectors
page.locator('div.sidebar ul.menu li.active a')
```

### Never Use Manual Assertions Without Await
**Always use web-first assertions.**

```typescript
// ❌ FORBIDDEN - manual assertion
expect(await page.locator('#status').isVisible()).toBe(true);
expect(await page.getByText('Hello').textContent()).toBe('Hello');

// ✅ CORRECT - web-first assertion
await expect(page.getByTestId('status')).toBeVisible();
await expect(page.getByText('Hello')).toHaveText('Hello');
```

---

## ✅ REQUIRED Patterns

### Web-First Assertions
Web-first assertions auto-wait and auto-retry until the condition is met.

```typescript
// ✅ These wait and retry automatically
await expect(page).toHaveTitle(/Dashboard/);
await expect(page.getByRole('heading')).toHaveText('Welcome');
await expect(page.getByTestId('submit')).toBeEnabled();
await expect(page.getByRole('alert')).toBeVisible();
await expect(page.getByRole('listitem')).toHaveCount(3);
```

**Common web-first matchers:**
- `toBeVisible()` - element is visible
- `toBeEnabled()` / `toBeDisabled()` - element state
- `toHaveText()` - exact or partial text match
- `toHaveValue()` - input value
- `toHaveAttribute()` - attribute check
- `toBeChecked()` - checkbox/radio state
- `toHaveCount()` - number of elements

### User-Facing Locators
Locators should reflect how users find elements.

```typescript
// ✅ REQUIRED - user-facing locators
page.getByRole('button', { name: 'Submit' })
page.getByRole('link', { name: 'Sign up' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('heading', { level: 1 })
page.getByLabel('Password')
page.getByPlaceholder('Search...')
page.getByText('Welcome back')
page.getByTestId('user-profile')  // fallback when needed
```

### Test Isolation
Each test gets a fresh browser context. Use `beforeEach` for setup.

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to starting point
    await page.goto('/dashboard');

    // Login if needed
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Wait for dashboard to load
    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  });

  test('shows user profile', async ({ page }) => {
    await page.getByRole('link', { name: 'Profile' }).click();
    await expect(page.getByText('Profile Settings')).toBeVisible();
  });

  test('displays notifications', async ({ page }) => {
    await page.getByRole('button', { name: 'Notifications' }).click();
    await expect(page.getByRole('list')).toBeVisible();
  });
});
```

---

## Locator Priority Hierarchy

Use locators in this order of preference:

| Priority | Locator | When to Use |
|----------|---------|-------------|
| 1 | `getByRole()` | Buttons, links, headings, inputs - accessibility semantics |
| 2 | `getByText()` | Unique visible text content |
| 3 | `getByLabel()` | Form fields with labels |
| 4 | `getByPlaceholder()` | Inputs with placeholder text |
| 5 | `getByTestId()` | Complex components, disambiguation needed |
| ❌ | `.locator('.class')` | NEVER use CSS classes |

### Chaining and Filtering
For complex scenarios, chain and filter locators:

```typescript
// Filter by text within a container
const product = page.getByRole('listitem').filter({ hasText: 'Product 2' });
await product.getByRole('button', { name: 'Add to cart' }).click();

// Filter by containing element
await page
  .getByRole('listitem')
  .filter({ has: page.getByRole('heading', { name: 'Premium' }) })
  .getByRole('button', { name: 'Buy' })
  .click();
```

---

## When Waits ARE Acceptable

### Waiting for Network Requests
```typescript
// ✅ Wait for specific API response
await page.waitForResponse('/api/data');
await page.waitForResponse(response =>
  response.url().includes('/api/users') && response.status() === 200
);

// ✅ Wait for navigation to complete
await page.waitForURL('**/dashboard');
```

### Waiting for Page Load States
```typescript
// ✅ Wait for network idle (all requests complete)
await page.waitForLoadState('networkidle');

// ✅ Wait for DOM content loaded
await page.waitForLoadState('domcontentloaded');
```

### Waiting for Specific Elements (via assertions)
```typescript
// ✅ These are web-first assertions that auto-wait
await expect(page.getByText('Loading...')).toBeHidden();
await expect(page.getByRole('dialog')).toBeVisible();
await expect(page.getByRole('progressbar')).toBeHidden();
```

---

## Mantine Component Patterns

Mantine UI components are NOT native HTML elements. They require special handling.

### Mantine Select
Mantine Select is a combination of `<input>` and `<div>` elements. **`selectOption()` does NOT work.**

```typescript
// ❌ DOES NOT WORK with Mantine Select
await page.getByRole('combobox').selectOption('value');
await page.locator('select').selectOption('option');

// ✅ CORRECT pattern for Mantine Select
await page.locator('[data-testid="SetStatusSelect"]').click();  // Open dropdown
await page.locator('div[value="archivePending"]').click();       // Select option
await page.locator('[data-testid="SetStatusButton"]').click();   // Submit if needed
```

### Mantine Menu
```typescript
// ✅ CORRECT pattern for Mantine Menu
await page.locator('[data-testid="UserMenu"]').click();          // Open menu
await page.getByRole('menuitem', { name: 'Settings' }).click();  // Click item
```

### When to Use data-testid
Use `data-testid` when:
- Multiple similar components exist on a page
- Role-based locators cannot uniquely identify the element
- Component structure makes semantic locators unreliable

```typescript
// When you have multiple "Submit" buttons
await page.locator('[data-testid="payment-submit"]').click();
await page.locator('[data-testid="shipping-submit"]').click();
```

---

## NEVER Skip Tests (Zero Tolerance)

**If a test fails, FIX IT. Never skip it.**

```typescript
// ❌ FORBIDDEN - skipping tests
test.skip('user can checkout', async ({ page }) => { ... });

// ❌ FORBIDDEN - commenting out tests
// test('user can checkout', async ({ page }) => { ... });

// ❌ FORBIDDEN - conditional skipping to hide failures
test('user can checkout', async ({ page }) => {
  test.skip(true, 'TODO: fix later');  // ❌ NEVER DO THIS
});
```

### When a Test Fails
1. **Investigate the failure** - Is it a code bug or test bug?
2. **Fix the root cause** - Either in application code or test code
3. **Re-run to verify** - Test must pass consistently
4. **Never use `.skip()` as a solution** - Skipping hides bugs

### Temporary Skip ONLY For
These are the ONLY acceptable temporary skip reasons:
- Feature is intentionally disabled in this environment
- External dependency is known to be down (with ticket to re-enable)
- Test requires infrastructure not yet available

**Even then, add a follow-up ticket and timeline.**

---

## Test Structure Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature: User Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('successful login redirects to dashboard', async ({ page }) => {
    // Arrange - already done in beforeEach

    // Act
    await page.getByLabel('Email').fill('valid@example.com');
    await page.getByLabel('Password').fill('correctpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Assert
    await expect(page).toHaveURL(/.*dashboard/);
    await expect(page.getByRole('heading', { name: 'Welcome' })).toBeVisible();
  });

  test('invalid credentials shows error message', async ({ page }) => {
    // Act
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // Assert
    await expect(page.getByRole('alert')).toHaveText('Invalid credentials');
    await expect(page).toHaveURL('/login');  // Stays on login page
  });
});
```

---

## Codegen Usage

Generate tests and locators using Playwright's codegen tool.

```bash
# Generate test by recording interactions
npx playwright codegen https://your-app.com

# Generate with specific viewport
npx playwright codegen --viewport-size=1280,720 https://your-app.com

# Generate for mobile device
npx playwright codegen --device="iPhone 13" https://your-app.com
```

**After generating:**
1. Review generated locators - upgrade CSS selectors to user-facing locators
2. Add proper assertions - codegen focuses on actions
3. Add test isolation - wrap in `test.describe` with `beforeEach`
4. Remove any `waitForTimeout` calls

---

## Debugging & Running Tests

### Running Tests
```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test auth.spec.ts

# Run tests matching name
npx playwright test -g "login"

# Run in headed mode (see browser)
npx playwright test --headed

# Run specific browser
npx playwright test --project=chromium
```

### Debugging
```bash
# UI Mode - visual debugger (RECOMMENDED)
npx playwright test --ui

# Debug mode with inspector
npx playwright test --debug

# Debug specific test from line number
npx playwright test auth.spec.ts:25 --debug
```

### Viewing Reports
```bash
# Show HTML report
npx playwright show-report

# Generate trace for CI debugging
npx playwright test --trace on
```

---

## Best Practices Checklist

Before committing Playwright tests, verify:

### Locators
- [ ] Using user-facing locators (`getByRole`, `getByText`, `getByLabel`)
- [ ] NO CSS class selectors
- [ ] `data-testid` only when semantic locators insufficient
- [ ] Locators are resilient to minor UI changes

### Assertions
- [ ] All assertions use web-first matchers with `await expect()`
- [ ] No manual `isVisible()` / `textContent()` checks
- [ ] Assertions verify user-visible behavior

### No Forbidden Patterns
- [ ] NO `page.waitForTimeout()` calls
- [ ] NO mocking of application APIs
- [ ] NO skipped tests (`.skip()`)
- [ ] NO commented-out tests

### Test Quality
- [ ] Each test is independent (no shared state)
- [ ] `beforeEach` handles common setup
- [ ] Tests verify real application behavior
- [ ] Mantine components use correct click patterns

### Before Merge
- [ ] All tests pass locally: `npx playwright test`
- [ ] Tests pass on all target browsers
- [ ] No flaky tests (run 3x to verify)


---

## Related Agent

For comprehensive E2E testing guidance that coordinates this and other Playwright skills, use the **`playwright-e2e-expert`** agent.
