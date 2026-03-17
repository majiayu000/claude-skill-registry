---
name: web-testing-playwright-e2e
description: Playwright E2E testing patterns - test structure, Page Object Model, locator strategies, assertions, network mocking, visual regression, parallel execution, fixtures, and configuration
---

# Playwright E2E Testing Patterns

> **Quick Guide:** Use Playwright for end-to-end tests that verify complete user workflows through the real application. Focus on critical user journeys, use accessibility-based locators (getByRole), and leverage auto-waiting assertions.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use getByRole() as your primary locator strategy - it mirrors how users interact with the page)**

**(You MUST test complete user workflows end-to-end - login flows, checkout processes, form submissions)**

**(You MUST use web-first assertions that auto-wait - toBeVisible(), toHaveText(), not manual sleeps)**

**(You MUST isolate tests - each test runs independently with its own browser context)**

**(You MUST use named constants for test data - no magic strings or numbers in test files)**

</critical_requirements>

---

**Auto-detection:** Playwright, E2E testing, end-to-end testing, browser automation, page.goto, test.describe, expect(page), getByRole, getByTestId, toBeVisible

**When to use:**

- Testing critical user-facing workflows (login, checkout, form submission)
- Multi-step user journeys that span multiple pages
- Cross-browser compatibility testing
- Testing real integration with backend APIs
- Visual regression testing with screenshots

**When NOT to use:**

- Testing pure utility functions (use unit tests)
- Testing individual component variants in isolation (use component testing tools)
- API-only testing without UI (use API testing)

**Key patterns covered:**

- Test structure and organization (test.describe, test, hooks)
- Page Object Model pattern for maintainability
- Locator strategies prioritizing accessibility
- Web-first assertions with auto-waiting
- Network mocking and interception
- Visual regression testing
- Parallel execution and configuration
- Clock API for time-dependent testing (v1.45+)
- ARIA snapshot testing for accessibility (v1.49+)
- Worker-scoped fixtures for performance
- Locator operators: and(), or(), filter({ visible, hasNot }) (v1.50+)
- New accessibility assertions (v1.44+): toHaveAccessibleName, toHaveRole

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Playwright E2E tests verify that your application works correctly from the user's perspective. They interact with the real browser, navigate through actual pages, and validate user-visible behavior.

**Core Principles:**

1. **Test user-visible behavior** - Focus on what end users see and interact with, not implementation details
2. **Use accessibility locators** - getByRole mirrors how screen readers and users interact with pages
3. **Isolate tests completely** - Each test has its own browser context, cookies, and storage
4. **Trust auto-waiting** - Playwright automatically waits for elements, no manual sleeps needed
5. **Mock external dependencies** - Use route interception for third-party APIs to ensure reliability

**When E2E tests provide the most value:**

- Critical business workflows (authentication, payments, core features)
- User journeys spanning multiple pages or components
- Testing real backend integration
- Cross-browser compatibility verification
- Catching integration bugs that unit tests miss

**When E2E tests may not be the best choice:**

- Testing pure utility functions (unit tests are faster and more precise)
- Testing component styling variants (use visual testing tools)
- Testing every edge case (balance with unit and integration tests)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Test Structure and Organization

Use `test.describe` to group related tests, `test` for individual test cases, and hooks for setup/teardown.

#### Test File Structure

```typescript
// tests/e2e/auth/login-flow.spec.ts
import { test, expect } from "@playwright/test";

const LOGIN_URL = "/login";
const DASHBOARD_URL = "/dashboard";
const VALID_EMAIL = "user@example.com";
const VALID_PASSWORD = "securePassword123";

test.describe("Login Flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(LOGIN_URL);
  });

  test("successful login redirects to dashboard", async ({ page }) => {
    await page.getByLabel(/email/i).fill(VALID_EMAIL);
    await page.getByLabel(/password/i).fill(VALID_PASSWORD);
    await page.getByRole("button", { name: /sign in/i }).click();

    await expect(page).toHaveURL(DASHBOARD_URL);
    await expect(page.getByRole("heading", { name: /welcome/i })).toBeVisible();
  });

  test("shows validation error for empty email", async ({ page }) => {
    await page.getByRole("button", { name: /sign in/i }).click();

    await expect(page.getByText(/email is required/i)).toBeVisible();
  });
});
```

**Why good:** Groups related tests logically, beforeEach eliminates repetition while maintaining isolation, named constants prevent magic strings, descriptive test names document expected behavior

```typescript
// Bad Example - No organization, magic strings
test("login test", async ({ page }) => {
  await page.goto("/login");
  await page.locator("#email").fill("user@example.com");
  await page.locator("#password").fill("password123");
  await page.locator("button").click();
  await page.waitForTimeout(2000); // Manual sleep!
  expect(page.url()).toContain("dashboard");
});
```

**Why bad:** No test grouping makes navigation difficult, magic strings scattered throughout break when values change, CSS selectors are fragile and break on refactoring, manual timeout instead of auto-waiting causes flaky tests

---

### Pattern 2: Page Object Model

Encapsulate page structure and interactions in reusable classes to improve maintainability.

#### Page Object Implementation

```typescript
// tests/e2e/pages/login-page.ts
import type { Page, Locator } from "@playwright/test";

const LOGIN_URL = "/login";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly signInButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel(/email/i);
    this.passwordInput = page.getByLabel(/password/i);
    this.signInButton = page.getByRole("button", { name: /sign in/i });
    this.errorMessage = page.getByRole("alert");
  }

  async goto() {
    await this.page.goto(LOGIN_URL);
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }
}
```

#### Using Page Objects in Tests

```typescript
// tests/e2e/auth/login-flow.spec.ts
import { test, expect } from "@playwright/test";
import { LoginPage } from "../pages/login-page";

const VALID_EMAIL = "user@example.com";
const VALID_PASSWORD = "securePassword123";
const DASHBOARD_URL = "/dashboard";

test.describe("Login Flow", () => {
  test("successful login", async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login(VALID_EMAIL, VALID_PASSWORD);

    await expect(page).toHaveURL(DASHBOARD_URL);
  });

  test("shows error for invalid credentials", async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login("wrong@example.com", "wrongpassword");

    await expect(loginPage.errorMessage).toBeVisible();
  });
});
```

**Why good:** Centralizes element locators in one place making UI changes easy to update, methods encapsulate complex interactions improving readability, page objects are reusable across multiple tests reducing duplication

**When to use:** Tests spanning multiple interactions on the same page, reusable flows across test files.

**When not to use:** Simple one-off tests where inline locators are clearer.

---

### Pattern 3: Locator Strategies

Prioritize accessibility-based locators that mirror how users interact with your application.

#### Locator Priority (Best to Worst)

```typescript
// Preferred: Accessibility-based locators
await page.getByRole("button", { name: /submit/i }); // BEST - mirrors user interaction
await page.getByLabel(/email address/i); // Form fields by label
await page.getByText(/welcome back/i); // Visible text
await page.getByPlaceholder("Search..."); // Placeholder text
await page.getByAltText("Company logo"); // Image alt text
await page.getByTitle("Close dialog"); // Title attribute

// Acceptable: Test IDs for complex cases
await page.getByTestId("user-avatar"); // When no semantic role exists

// Avoid: Implementation-dependent selectors
await page.locator("#submit-btn"); // Fragile ID selector
await page.locator(".btn-primary"); // CSS class can change
await page.locator("div > button:nth-child(2)"); // DOM structure dependent
```

**Why good:** getByRole matches accessibility tree ensuring keyboard navigability works, survives UI refactoring since roles and labels are stable, validates accessibility as a side effect

#### Chaining and Filtering

```typescript
// Filter within a list
await page
  .getByRole("listitem")
  .filter({ hasText: "Product A" })
  .getByRole("button", { name: /add to cart/i })
  .click();

// Scope to a specific region
const sidebar = page.getByRole("complementary");
await sidebar.getByRole("link", { name: /settings/i }).click();

// Filter by nested element
await page
  .getByRole("row")
  .filter({ has: page.getByText("Active") })
  .getByRole("button", { name: /edit/i })
  .click();

// Filter by NOT having element (v1.50+)
await page
  .getByRole("listitem")
  .filter({ hasNot: page.getByText("Out of stock") })
  .first()
  .click();

// Filter only visible elements (v1.51+)
await page.locator("button").filter({ visible: true }).click();
```

**Why good:** Chains narrow down to specific elements without fragile selectors, filter() handles dynamic lists gracefully, scoping to regions prevents selecting wrong elements

#### Locator Operators (v1.50+)

```typescript
// Combine conditions with .and() - element must match both
const subscribedButton = page
  .getByRole("button")
  .and(page.getByTitle("Subscribe"));
await subscribedButton.click();

// Match either alternative with .or() - useful for conditional UI
const newEmail = page.getByRole("button", { name: "New" });
const dialog = page.getByText("Confirm security settings");
await expect(newEmail.or(dialog).first()).toBeVisible();
```

**Why good:** `.and()` creates precise matches without fragile selectors, `.or()` handles conditional UI states elegantly, both compose with existing locators

---

### Pattern 4: Web-First Assertions

Use assertions that automatically wait and retry until the condition is met.

#### Auto-Waiting Assertions

```typescript
import { test, expect } from "@playwright/test";

const TIMEOUT_LONG_MS = 10000;

test("web-first assertions with auto-waiting", async ({ page }) => {
  // Auto-waits for element to be visible
  await expect(page.getByText("Welcome")).toBeVisible();

  // Auto-waits for text content to match
  await expect(page.getByRole("heading")).toHaveText("Dashboard");

  // Auto-waits for URL to match
  await expect(page).toHaveURL(/\/dashboard/);

  // Auto-waits with custom timeout
  await expect(page.getByRole("status")).toHaveText("Complete", {
    timeout: TIMEOUT_LONG_MS,
  });

  // Negated assertions also auto-wait
  await expect(page.getByRole("progressbar")).not.toBeVisible();
});
```

**Why good:** Auto-waiting eliminates flaky tests from race conditions, no manual sleeps or arbitrary timeouts needed, retries automatically until condition met or timeout exceeded

```typescript
// Bad Example - Manual waiting
test("manual waiting is flaky", async ({ page }) => {
  await page.click("button");
  await page.waitForTimeout(2000); // Arbitrary sleep!
  const text = await page.textContent(".result");
  expect(text).toBe("Success"); // Non-waiting assertion
});
```

**Why bad:** Fixed timeouts are either too short (flaky) or too long (slow), doesn't adapt to actual page load time, manual assertions don't retry on failure

#### Soft Assertions

```typescript
test("soft assertions continue after failure", async ({ page }) => {
  await page.goto("/profile");

  // These won't stop the test if they fail
  await expect.soft(page.getByTestId("avatar")).toBeVisible();
  await expect.soft(page.getByText("Premium Member")).toBeVisible();
  await expect
    .soft(page.getByRole("link", { name: /settings/i }))
    .toBeEnabled();

  // Test continues, all failures reported at end
});
```

**Why good:** Collects all failures in one test run, useful for validating multiple independent conditions, reduces test re-runs during debugging

---

### Pattern 5: Network Mocking and Interception

Mock external APIs and control network conditions for reliable, isolated tests.

#### Mocking API Responses

```typescript
import { test, expect } from "@playwright/test";

const API_USERS_ENDPOINT = "**/api/users";
const MOCK_USER_ID = "user-123";
const MOCK_USER_NAME = "John Doe";
const MOCK_USER_EMAIL = "john@example.com";

test("displays user profile from mocked API", async ({ page }) => {
  // Intercept API call and return mock data
  await page.route(API_USERS_ENDPOINT, (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: MOCK_USER_ID,
        name: MOCK_USER_NAME,
        email: MOCK_USER_EMAIL,
      }),
    });
  });

  await page.goto("/profile");

  await expect(page.getByText(MOCK_USER_NAME)).toBeVisible();
  await expect(page.getByText(MOCK_USER_EMAIL)).toBeVisible();
});
```

**Why good:** Eliminates flakiness from external API availability, enables testing error states and edge cases, controls exact data for predictable assertions

#### Simulating Error States

```typescript
const API_USERS_ENDPOINT = "**/api/users";
const HTTP_SERVER_ERROR = 500;
const HTTP_NETWORK_OFFLINE = "failed";

test("handles API error gracefully", async ({ page }) => {
  await page.route(API_USERS_ENDPOINT, (route) => {
    route.fulfill({
      status: HTTP_SERVER_ERROR,
      body: JSON.stringify({ error: "Internal server error" }),
    });
  });

  await page.goto("/profile");

  await expect(page.getByText(/something went wrong/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /retry/i })).toBeVisible();
});

test("handles network failure", async ({ page }) => {
  await page.route(API_USERS_ENDPOINT, (route) =>
    route.abort(HTTP_NETWORK_OFFLINE),
  );

  await page.goto("/profile");

  await expect(page.getByText(/network error/i)).toBeVisible();
});
```

**Why good:** Tests error handling without breaking external services, simulates conditions that are hard to reproduce otherwise, ensures user sees appropriate feedback

#### Modifying Real Responses

```typescript
test("modifies API response for testing", async ({ page }) => {
  await page.route("**/api/products", async (route) => {
    // Make the real request
    const response = await route.fetch();
    const json = await response.json();

    // Modify the response
    json.products = json.products.map((p: { price: number }) => ({
      ...p,
      price: p.price * 0.9, // Apply 10% discount
    }));

    // Return modified response
    await route.fulfill({ response, json });
  });

  await page.goto("/products");

  // Test with modified data
});
```

**Why good:** Combines real API behavior with controlled modifications, useful for testing transformations or specific scenarios, maintains realistic response structure

---

### Pattern 6: Visual Regression Testing

Capture and compare screenshots to detect unintended visual changes.

#### Basic Screenshot Comparison

```typescript
import { test, expect } from "@playwright/test";

test("homepage visual regression", async ({ page }) => {
  await page.goto("/");

  // Full page screenshot comparison
  await expect(page).toHaveScreenshot("homepage.png");
});

test("component visual regression", async ({ page }) => {
  await page.goto("/components/button");

  // Element-specific screenshot
  const button = page.getByRole("button", { name: /primary/i });
  await expect(button).toHaveScreenshot("primary-button.png");
});
```

**Why good:** Catches unintended visual changes automatically, baseline images serve as visual documentation, element-specific screenshots reduce noise from dynamic content

#### Handling Dynamic Content

```typescript
const SCREENSHOT_ANIMATION_DELAY_MS = 500;

test("screenshot with dynamic content handled", async ({ page }) => {
  await page.goto("/dashboard");

  // Mask dynamic elements
  await expect(page).toHaveScreenshot("dashboard.png", {
    mask: [page.getByTestId("current-time"), page.getByTestId("random-ad")],
  });

  // Or wait for animations to complete
  await expect(page).toHaveScreenshot("dashboard-stable.png", {
    animations: "disabled",
  });

  // Custom threshold for acceptable differences
  await expect(page).toHaveScreenshot("dashboard-fuzzy.png", {
    maxDiffPixels: 100,
  });
});
```

**Why good:** Masking prevents false positives from timestamps or ads, disabling animations ensures deterministic screenshots, threshold allows minor acceptable variations

---

### Pattern 7: Test Fixtures and Hooks

Use fixtures for reusable setup and hooks for test lifecycle management.

#### Built-in Fixtures

```typescript
import { test, expect } from "@playwright/test";

// page - isolated browser page
// context - browser context (cookies, storage)
// browser - browser instance
// request - API testing context

test("using built-in fixtures", async ({ page, context }) => {
  // Each test gets a fresh page
  await page.goto("/app");

  // Access context for cookies
  await context.addCookies([
    { name: "session", value: "abc123", domain: "localhost", path: "/" },
  ]);
});
```

#### Custom Fixtures

```typescript
// tests/e2e/fixtures.ts
import { test as base } from "@playwright/test";
import { LoginPage } from "./pages/login-page";
import { DashboardPage } from "./pages/dashboard-page";

const AUTH_SESSION_TOKEN = "test-session-token";
const AUTH_COOKIE_NAME = "session";
const AUTH_COOKIE_DOMAIN = "localhost";

// Extend base test with custom fixtures
export const test = base.extend<{
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  authenticatedPage: void;
}>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  // Auto-fixture that runs for every test
  authenticatedPage: [
    async ({ page, context }, use) => {
      // Setup: Add auth cookie
      await context.addCookies([
        {
          name: AUTH_COOKIE_NAME,
          value: AUTH_SESSION_TOKEN,
          domain: AUTH_COOKIE_DOMAIN,
          path: "/",
        },
      ]);
      await use();
      // Teardown: Clear cookies
      await context.clearCookies();
    },
    { auto: true }, // Runs automatically for all tests
  ],
});

export { expect } from "@playwright/test";
```

#### Using Custom Fixtures

```typescript
// tests/e2e/dashboard.spec.ts
import { test, expect } from "./fixtures";

test("dashboard shows user data", async ({ page, dashboardPage }) => {
  await dashboardPage.goto();

  await expect(page.getByRole("heading", { name: /dashboard/i })).toBeVisible();
});
```

**Why good:** Fixtures encapsulate setup and teardown together, auto fixtures eliminate repetitive auth setup, page objects as fixtures improve reusability

#### Hooks for Common Setup

```typescript
import { test, expect } from "@playwright/test";

test.describe("User Settings", () => {
  // Runs once before all tests in this describe block
  test.beforeAll(async ({ browser }) => {
    // One-time setup (e.g., seed database)
  });

  // Runs before each test
  test.beforeEach(async ({ page }) => {
    await page.goto("/settings");
  });

  // Runs after each test
  test.afterEach(async ({ page }) => {
    // Cleanup (e.g., reset user preferences)
  });

  // Runs once after all tests
  test.afterAll(async ({ browser }) => {
    // Final cleanup
  });

  test("can update profile", async ({ page }) => {
    // Test implementation
  });
});
```

**Why good:** beforeAll/afterAll handle expensive one-time setup, beforeEach ensures consistent starting state, afterEach prevents test pollution

---

### Pattern 8: Configuration

Configure Playwright for your project's needs in `playwright.config.ts`.

#### Basic Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

const BASE_URL = "http://localhost:3000";
const CI_WORKERS = 2;
const DEFAULT_TIMEOUT_MS = 30000;
const ACTION_TIMEOUT_MS = 10000;
const NAVIGATION_TIMEOUT_MS = 30000;

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? CI_WORKERS : undefined,
  reporter: [["html", { open: "never" }], ["list"]],

  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },

  // Global timeouts
  timeout: DEFAULT_TIMEOUT_MS,
  expect: {
    timeout: ACTION_TIMEOUT_MS,
  },

  // Browser projects
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "mobile-chrome",
      use: { ...devices["Pixel 5"] },
    },
  ],

  // Local dev server
  webServer: {
    command: "npm run dev",
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
  },
});
```

**Why good:** fullyParallel maximizes test speed, retries on CI handle transient failures, trace/screenshot/video only on failure saves resources, projects enable cross-browser testing

#### Environment-Specific Configuration

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

const STAGING_URL = "https://staging.example.com";
const PRODUCTION_URL = "https://example.com";
const LOCAL_URL = "http://localhost:3000";
const CI_WORKERS = 4;

export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL || LOCAL_URL,
  },

  projects: [
    {
      name: "staging",
      use: {
        baseURL: STAGING_URL,
      },
      testMatch: /.*\.e2e\.ts/,
    },
    {
      name: "production",
      use: {
        baseURL: PRODUCTION_URL,
      },
      testMatch: /.*\.smoke\.ts/, // Only smoke tests in prod
    },
  ],
});
```

**Why good:** Separate projects for different environments, production limited to smoke tests for safety, environment variables override defaults

</patterns>

---

<integration>

## Integration Guide

**Works with your test organization:**

- Place E2E tests in dedicated `tests/e2e/` directory at project root
- Organize by user journey, not by component (e.g., `auth/`, `checkout/`, `search/`)
- Use `.spec.ts` extension to distinguish from unit tests

**CI/CD Integration:**

Playwright integrates with CI pipelines through configuration and CLI flags. Use sharding to split tests across machines:

```bash
# Run tests on CI
npx playwright test --shard=1/4

# Update snapshots
npx playwright test --update-snapshots
```

**Debugging Tools:**

- UI Mode: `npx playwright test --ui`
- Debug Mode: `npx playwright test --debug`
- Trace Viewer: `npx playwright show-trace trace.zip`

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `page.waitForTimeout()` with fixed delays - causes flaky or slow tests, use auto-waiting assertions instead
- Using CSS selectors like `.btn-primary` or `#submit-btn` - fragile and break on refactoring, use getByRole
- Not testing error states - only happy paths leaves error handling untested, users will encounter errors
- Tests sharing state or data - causes flaky failures in parallel execution, isolate each test completely

**Medium Priority Issues:**

- Using getByTestId as primary locator - misses accessibility validation, prioritize getByRole
- No network mocking for external APIs - third-party flakiness affects your tests, mock external dependencies
- Running E2E tests only on one browser - cross-browser issues go undetected, test on multiple browsers in CI
- Screenshots without masking dynamic content - timestamps and ads cause false positives, mask dynamic elements

**Common Mistakes:**

- Hardcoded test data scattered throughout files - use named constants for maintainability
- Testing implementation details instead of user behavior - tests break on refactoring unnecessarily
- Not using beforeEach for common setup - leads to duplicated code and inconsistent test state
- Mixing E2E tests with unit tests in the same directory - confuses test runners and organization

**Gotchas and Edge Cases:**

- `toBeVisible()` waits for element, `toBeInTheDocument()` does not - always prefer visibility checks
- Screenshots vary by OS and browser - run visual tests in consistent CI environment
- `beforeAll` runs once per worker, not once globally - use global setup for true one-time setup
- Network routes are global to context - always reset handlers between tests to prevent pollution
- Parallel tests cannot share state - use fixtures for per-test setup, not shared variables

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use getByRole() as your primary locator strategy - it mirrors how users interact with the page)**

**(You MUST test complete user workflows end-to-end - login flows, checkout processes, form submissions)**

**(You MUST use web-first assertions that auto-wait - toBeVisible(), toHaveText(), not manual sleeps)**

**(You MUST isolate tests - each test runs independently with its own browser context)**

**(You MUST use named constants for test data - no magic strings or numbers in test files)**

**Failure to follow these rules will result in flaky tests, false positives, and maintenance nightmares.**

</critical_reminders>
