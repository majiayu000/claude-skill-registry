---
name: playwright-testing
description: Expert guidance for writing end-to-end tests with Playwright Test framework. Use this skill when writing browser automation tests, creating test suites, working with locators and assertions, mocking network requests, handling authentication, or configuring the Playwright test runner. Trigger keywords include "playwright", "e2e test", "end-to-end", "browser test", "getByRole", "locator", "toBeVisible", "page.goto", "test runner".
---

# Playwright Testing

End-to-end testing framework with auto-waiting, web-first assertions, and multi-browser support.

## Quick Start

```typescript
import { test, expect } from "@playwright/test";

test("user can log in", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill("user@example.com");
    await page.getByLabel("Password").fill("secret");
    await page.getByRole("button", { name: "Sign in" }).click();
    await expect(page.getByText("Welcome")).toBeVisible();
});
```

## Core Concepts

### Locators (Priority Order)

1. `page.getByRole('button', { name: 'Submit' })` — ARIA roles (most resilient)
2. `page.getByLabel('Email')` — Form labels
3. `page.getByText('Welcome')` — Visible text
4. `page.getByTestId('user-menu')` — Test IDs (explicit contracts)
5. `page.getByPlaceholder('Search')` — Placeholder text

Avoid CSS selectors and XPath—they break with DOM changes.

**Chaining and filtering:**

```typescript
// Chain to narrow scope
page.locator(".modal").getByRole("button", { name: "Save" });

// Filter by text or child elements
page.getByRole("listitem").filter({ hasText: "Product" });
page.getByRole("listitem").filter({ has: page.getByRole("button") });
```

See [references/locators.md](references/locators.md) for complete locator API.

### Assertions

Auto-retrying (use these for web elements):

```typescript
await expect(locator).toBeVisible();
await expect(locator).toHaveText("Hello");
await expect(locator).toHaveValue("input text");
await expect(locator).toBeChecked();
await expect(page).toHaveURL(/dashboard/);
```

Non-retrying (for static values):

```typescript
expect(value).toBe(5);
expect(array).toContain("item");
expect(obj).toEqual({ key: "value" });
```

See [references/assertions.md](references/assertions.md) for all assertion types.

### Actions

```typescript
await locator.click();
await locator.fill("text"); // Clear and type
await locator.pressSequentially("t"); // Character by character
await locator.selectOption("value");
await locator.check(); // Checkbox
await locator.setInputFiles("file.pdf");
await page.keyboard.press("Enter");
```

All actions auto-wait for elements to be visible, stable, and enabled.

See [references/actions.md](references/actions.md) for complete action reference.

## Test Structure

```typescript
import { test, expect } from "@playwright/test";

test.describe("Feature", () => {
    test.beforeEach(async ({ page }) => {
        await page.goto("/");
    });

    test("scenario one", async ({ page }) => {
        // Arrange - Act - Assert
    });

    test("scenario two", async ({ page }) => {
        // ...
    });
});
```

### Hooks

- `test.beforeEach()` / `test.afterEach()` — Run before/after each test
- `test.beforeAll()` / `test.afterAll()` — Run once per worker

## Configuration

Minimal `playwright.config.ts`:

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
    testDir: "./tests",
    fullyParallel: true,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 2 : undefined,
    reporter: "html",
    use: {
        baseURL: "http://localhost:3000",
        trace: "on-first-retry",
    },
    projects: [
        { name: "chromium", use: { ...devices["Desktop Chrome"] } },
        { name: "firefox", use: { ...devices["Desktop Firefox"] } },
        { name: "webkit", use: { ...devices["Desktop Safari"] } },
    ],
    webServer: {
        command: "npm run dev",
        url: "http://localhost:3000",
        reuseExistingServer: !process.env.CI,
    },
});
```

See [references/configuration.md](references/configuration.md) for all options.

## CLI Commands

```bash
npx playwright test                    # Run all tests
npx playwright test --ui               # Interactive UI mode
npx playwright test --headed           # Show browser
npx playwright test --debug            # Step-through debugger
npx playwright test -g "login"         # Filter by title
npx playwright test --project=chromium # Specific browser
npx playwright test --last-failed      # Retry failures only
npx playwright codegen                 # Generate tests
npx playwright show-report             # View HTML report
```

## Advanced Features

### Network Mocking

```typescript
await page.route("**/api/users", (route) =>
    route.fulfill({ json: [{ id: 1, name: "Mock User" }] }),
);

await page.route("**/api/error", (route) => route.fulfill({ status: 500 }));
```

### Authentication State

```typescript
// Save auth state after login
await page.context().storageState({ path: "auth.json" });

// Reuse in config
use: {
    storageState: "auth.json";
}
```

### Fixtures

```typescript
const test = base.extend<{ userPage: Page }>({
    userPage: async ({ browser }, use) => {
        const context = await browser.newContext();
        const page = await context.newPage();
        await page.goto("/login");
        // ... login
        await use(page);
        await context.close();
    },
});
```

See [references/advanced.md](references/advanced.md) for network mocking, auth patterns, fixtures, and Page Object Model.

## Best Practices

1. **Use role-based locators** — `getByRole()` is most resilient to changes
2. **Prefer auto-retrying assertions** — `await expect(locator).toBeVisible()` not `locator.isVisible()`
3. **Keep tests isolated** — Each test gets fresh browser context
4. **Avoid hardcoded waits** — Playwright auto-waits; use explicit waits only for custom conditions
5. **Test user behaviour** — Focus on what users see, not implementation details
6. **Use soft assertions sparingly** — `expect.soft()` continues after failure for comprehensive reports
