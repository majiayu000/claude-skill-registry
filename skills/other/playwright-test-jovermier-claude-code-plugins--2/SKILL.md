---
name: playwright-test
description: Playwright end-to-end testing patterns and best practices
updated: 2026-01-11
---

# Playwright Testing Skill

End-to-end testing patterns with Playwright for Astro 5.16 + React 19 projects.

## Project Context

- **Framework**: Check your project configuration for framework versions
- **Testing**: Playwright E2E testing
- **Runtime**: Dev server management (PM2 if available in Coder, check coder-environment skill)
- **Headless mode**: Tests run headless by default; check workspace for headed mode support
- **Test utilities**: Check your project for available test helpers
- **Artifacts**: Traces, videos, and screenshots saved to `test-results/` on failure

## Base URL Configuration

**CRITICAL**: Base URLs should be configured in the Playwright config file(s), never in test files.

Ideally, the base URL is set via `use.baseURL` in the config file, which may read from environment variables.

For projects testing multiple environments, separate config files can be used (e.g., `playwright.config.ci.ts`, `playwright.config.staging.ts`) and selected via the `--config` flag.

Test files should always use root-relative paths (starting with `/`) and rely on the config to provide the full base URL.

### Web Server Configuration

**DO NOT configure Playwright to start a web server.** Playwright should assume the server is already running.

**DON'T** - Never add `webServer` configuration:

```typescript
// ❌ WRONG - Do not configure webServer in playwright.config.ts
export default defineConfig({
  webServer: {
    command: "[package-manager] start",
    url: "BASE_URL must be set via environment variable",
  },
});
```

**DO** - The config file already handles base URL:

```typescript
// ✅ CORRECT - Server managed externally, config reads from .env.local
// This is already implemented in playwright.config.ts
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig, devices } from "@playwright/test";
import { config } from "dotenv";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env.local
const envResult = config({ path: resolve(__dirname, ".env.local") });

if (envResult.error) {
  console.warn(
    "Warning: .env.local not found, relying on existing environment variables."
  );
}

const baseURL = process.env.APP_SERVER_URL;

if (!baseURL) {
  throw new Error(
    "Missing baseURL! Set BASE_URL, PLAYWRIGHT_BASE_URL, or ensure VITE_CONVEX_URL is defined in .env.local."
  );
}

export default defineConfig({
  use: { baseURL },
});
```

**Rationale**: This project uses PM2 to manage the dev server with fast refresh. Playwright tests should connect to the already-running server, not start a new one. The config file loads `.env.local` (which contains environment configuration) and falls back to shell environment variables. Set `BASE_URL` in `.env.local` or your shell environment to point to the running dev server.

### Test Files MUST Use Root-Relative Paths

**DO** - Use root-relative paths in test files:

```typescript
// ✅ CORRECT
await page.goto("/");
await page.goto("/about");
await page.goto("/blog/my-post");
```

**DON'T** - Never include base URL in test files:

```typescript
// ❌ WRONG - Base URL should not be hardcoded in tests
await page.goto("http://localhost:3000"); // NEVER use localhost
await page.goto("http://localhost:3000/about"); // ALWAYS use environment variables
```

**DON'T** - Never provide fallback URLs:

```typescript
// ❌ WRONG - No fallback URLs, NEVER hardcode localhost
const baseUrl = process.env.APP_SERVER_URL || "http://localhost:3000";
await page.goto(baseUrl);
```

### Running Tests Against Different Environments

The config file reads `BASE_URL` from `.env.local` or the environment. For most cases, just run:

```bash
# Run tests - uses BASE_URL from .env.local or environment
[package-manager] run [test-script]

# Override for a different environment
BASE_URL=<your-dev-url> [package-manager] run [test-script]

# Using a specific config file for an environment
[package-manager] run [test-script] --config=playwright.config.staging.ts
```

**CRITICAL**: Never hardcode `localhost` URLs. Always use environment variables or the actual deployment URL.

## Test File Structure

```typescript
// tests/my-feature.spec.ts
import { test, expect } from "@playwright/test";

test("describes the behavior", async ({ page }) => {
  await page.goto("/");
  // test implementation
});
```

## Test Patterns

### Navigation

```typescript
test("navigates to a page", async ({ page }) => {
  await page.goto("/about");
  await expect(page).toHaveURL(/\/about/);
});
```

### Element Visibility

```typescript
test("shows element on page", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("h1")).toBeVisible();
});
```

### Clicking and Interaction

```typescript
test("button click triggers action", async ({ page }) => {
  await page.goto("/");
  await page.click('button[type="submit"]');
  await expect(page.locator(".success-message")).toBeVisible();
});
```

### Form Submission

```typescript
test("form submission works", async ({ page }) => {
  await page.goto("/contact");
  await page.fill('input[name="email"]', "test@example.com");
  await page.fill('textarea[name="message"]', "Hello");
  await page.click('button[type="submit"]');
  await expect(page.locator(".success")).toBeVisible();
});
```

### Responsive Design

```typescript
test.describe("mobile", () => {
  test.use({ viewport: { width: 375, height: 667 } });
  test("mobile layout works", async ({ page }) => {
    await page.goto("/");
    await expect(page.locator(".mobile-menu")).toBeVisible();
  });
});
```

### Async State

```typescript
test("content loads asynchronously", async ({ page }) => {
  await page.goto("/dashboard");
  await page.waitForSelector('[data-testid="loaded-content"]');
  await expect(page.locator('[data-testid="loaded-content"]')).toBeVisible();
});
```

### Error States

```typescript
test("shows error message on failure", async ({ page }) => {
  await page.goto("/form");
  await page.click('button[type="submit"]');
  await expect(page.locator(".error-message")).toBeVisible();
  await expect(page.locator(".error-message")).toContainText("required");
});
```

## Selectors

Use semantic, accessible selectors:

**DO**:

```typescript
page.locator('button[type="submit"]');
page.locator('nav a[href="/about"]');
page.locator("h1");
page.getByRole("button", { name: "Submit" });
page.getByLabelText("Email");
```

**DON'T**:

```typescript
page.locator(".btn-primary"); // Fragile class names
page.locator("#submit-btn"); // Implementation detail
page.locator("div > div > p"); // Brittle structure
```

## When to Write Tests

Write tests for:

- New page/route creation
- Component behavior changes
- Form submission flows
- Navigation between pages
- User interactions (clicks, inputs, form submissions)
- Conditional rendering based on state
- Responsive design verification
- API integration testing

## Test Organization

### Test Groups

Use `test.describe()` to group related tests:

```typescript
test.describe("user authentication", () => {
  test("login with valid credentials", async ({ page }) => {
    // ...
  });

  test("shows error for invalid credentials", async ({ page }) => {
    // ...
  });
});
```

### Before/After Hooks

```typescript
test.beforeEach(async ({ page }) => {
  // Setup before each test
  await page.goto("/login");
});

test.afterEach(async ({ page }) => {
  // Cleanup after each test
});
```

## Fixtures

Create custom fixtures for reusable test utilities:

```typescript
// tests/fixtures.ts
import { test as base } from "@playwright/test";

export const test = base.extend<{
  authenticatedPage: Page;
}>({
  authenticatedPage: async ({ page }, use) => {
    // Perform login
    await page.goto("/login");
    await page.fill('input[name="email"]', "test@example.com");
    await page.fill('input[name="password"]', "password");
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");
    await use(page);
  },
});
```

## Page Object Model

Organize page interactions into reusable classes:

```typescript
// tests/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async assertErrorMessage(message: string) {
    await expect(this.page.locator(".error")).toContainText(message);
  }
}
```

## Network Interception

Mock or intercept network requests:

```typescript
test("mocks API response", async ({ page }) => {
  await page.route("**/api/data", (route) => {
    route.fulfill({
      status: 200,
      body: JSON.stringify({ mock: "data" }),
    });
  });

  await page.goto("/dashboard");
});
```

## Visual Regression Testing

Compare screenshots against baseline:

```typescript
test("visual regression", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("homepage.png");
});
```

## Debugging

### Headed Mode

Run tests with a visible browser for debugging:

```bash
HEADED=true pnpm test
```

### Slow Motion

Add delays between actions in config:

```typescript
use: {
  launchOptions: {
    slowMo: 100, // 100ms delay between actions
  },
}
```

## Accessibility Testing

Use `@axe-core/playwright` for accessibility checks:

```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("page is accessible", async ({ page }) => {
  await page.goto("/");
  const accessibilityScanResults = await new AxeBuilder({ page })
    .include('[role="main"]')
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

## Best Practices

1. **Test user-visible behavior**, not implementation details
2. **Use semantic selectors** over CSS classes
3. **Wait for elements explicitly** using `waitForSelector()` or assertions
4. **Avoid hardcoded waits** - use assertions with `toHaveText()`, `toBeVisible()`, etc.
5. **Keep tests independent** - each test should work in isolation
6. **Use data-testid** attributes when no semantic selector exists
7. **Test edge cases**: empty states, error states, loading states

## Running Tests

```bash
# Run all tests
[package-manager] run [test-script]

# Run specific test file
[package-manager] run [test-script] tests/my-feature.spec.ts

# Run with trace for debugging
[package-manager] run [test-script] -- --trace on

# View trace
npx playwright show-trace test-results/trace.zip

# Run in headed mode (if supported)
HEADED=true [package-manager] run [test-script]
```

## Test Utilities

The project includes [tests/test-utils.ts](tests/test-utils.ts) with powerful testing utilities:

### Environment Variables (from `.env.local`)

- `CONVEX_URL` - Self-hosted Convex backend URL (required)
- `CONVEX_DASHBOARD_URL` - Convex dashboard URL (required)
- `VITE_CONVEX_URL` - Alternative Convex URL for dev

### Console and Network Tracking

Tests automatically track:

- Console errors, warnings, and logs
- Failed network requests (4xx, 5xx)
- Request failures with timing data

```typescript
// Using test-utils.ts extended test fixture
import { test } from "./test-utils";

test("page has no console errors", async ({ page }) => {
  await page.goto("/");
  // Console tracking is automatic with test-utils.ts fixture
  page.assertNoConsoleErrors();
});

// With filter pattern
test("page has no critical errors", async ({ page }) => {
  await page.goto("/");
  // Ignore CORS warnings, fail on others
  page.assertNoConsoleErrors(/CORS/);
});
```

### Available Filter Patterns

```typescript
import { CONSOLE_FILTERS } from "./test-utils";

// Ignore common development warnings
page.assertNoConsoleErrors(CONSOLE_FILTERS.ALL_DEV);

// Ignore only CORS errors
page.assertNoConsoleErrors(CONSOLE_FILTERS.CORS);

// Ignore auth-redirect errors (common in Coder)
page.assertNoConsoleErrors(CONSOLE_FILTERS.AUTH_REDIRECT);
```

### Performance Metrics

```typescript
test("page loads quickly", async ({ page }) => {
  await page.goto("/");
  // Assert performance metrics
  const metrics = await page.assertPerformanceMetrics({
    maxLoadTime: 3000,
    maxDomContentLoaded: 2000,
  });
});
```

### Helper Functions

```typescript
import { gotoAndCheckConsole, expectConsoleErrors } from "./test-utils";

// Navigate and check console in one call
await gotoAndCheckConsole(page, "/my-page", {
  waitForState: "load",
  ignoreErrorsPattern: /CORS/,
});

// Check for specific error patterns
expectConsoleErrors(page, [/expected-error-1/, /expected-error-2/]);
```

## Debugging Artifacts

On test failure, Playwright automatically saves:

| Artifact    | Location                 | When Saved                       |
| ----------- | ------------------------ | -------------------------------- |
| Traces      | `test-results/trace.zip` | On failure (`retain-on-failure`) |
| Screenshots | `test-results/`          | On failure (`only-on-failure`)   |
| Videos      | `test-results/`          | On failure (`retain-on-failure`) |

### Viewing Traces

```bash
# Open trace viewer
npx playwright show-trace test-results/trace.zip

# Run tests with trace always on
[package-manager] run [test-script] -- --trace on
```

## Server Management

Before running tests, verify the dev server is running:

```bash
# Check if dev server is running
# Use PM2 if available (check coder-environment skill), or check process manually
lsof -i :[dev-port]

# View logs to diagnose issues
# Use PM2 logs if available, or container logs for Docker
```

**Server Ports**: Check your project configuration for the development and production ports.
