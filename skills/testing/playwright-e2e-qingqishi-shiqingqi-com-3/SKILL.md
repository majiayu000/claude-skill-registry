---
name: playwright-e2e
description: Playwright end-to-end (e2e) testing best practices for user-centric testing using semantic locators. Use when writing E2E tests, integration tests, user flow tests, Playwright tests, test specs, or when the user mentions Playwright, e2e tests, getByRole, test flows, or user testing.
---

# Playwright E2E Testing

## Overview

This project uses Playwright for E2E testing with a focus on user-centric testing that avoids implementation details.

## Test Configuration

- **Unit tests**: Vitest for client components and synchronous server components
- **E2E tests**: Playwright with automatic dev server startup
- **Location**: `e2e/` directory
- **HTML reporter**: Enabled with trace collection on retry
- **Duration**: Full E2E suite takes ~15 minutes

## Core Philosophy: Test Like a User

**Users interact with what they see, not technical implementation details.**

### ✅ Test User-Visible Behavior

- Wait for text to appear/disappear
- Check for visible elements
- Interact with labeled buttons and links
- Verify content changes

### ❌ Avoid Testing Implementation Details

- Don't assert on URLs or pathnames
- Don't check cookies or localStorage
- Don't wait for `networkidle` or technical states
- Don't verify internal state or data structures

## Best Practices

### 1. Use Semantic Locators

Always prefer role-based locators that match how users perceive the page.

**✅ Good:**

```typescript
page.getByRole("button", { name: "Submit" });
page.getByRole("heading", { name: "Welcome" });
page.getByRole("link", { name: "Learn More" });
page.getByLabel("Email address");
page.getByPlaceholder("Enter your name");
page.getByText("Success!");
```

**❌ Bad:**

```typescript
page.locator('button[aria-label="Submit"]'); // CSS selector
page.locator(".submit-btn"); // Class name
page.locator("#submit"); // ID
page.locator('[data-testid="submit"]'); // Test ID
```

### 2. Wait for Visible Changes

Wait for actual UI changes users would see, not technical state.

**✅ Good:**

```typescript
await page.getByRole("button", { name: "Load More" }).click();
await expect(page.getByRole("heading", { name: "Results" })).toBeVisible();
```

**❌ Bad:**

```typescript
await page.waitForLoadState("networkidle");
await page.waitForTimeout(500);
await page.waitForFunction(() => window.location.pathname === "/results");
```

### 3. Simplify Test Setup

Minimize beforeEach steps and avoid redundant operations.

**✅ Good:**

```typescript
test("user can browse products", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Products" })).toBeVisible();

  // Test continues...
});
```

**❌ Bad:**

```typescript
test.beforeEach(async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.context().clearCookies();
  await page.reload();
  await page.waitForLoadState("networkidle");
});

test("user can browse products", async ({ page }) => {
  // Test continues...
});
```

## Complete Example: Before & After

### ❌ Bad: Testing Implementation Details

```typescript
test("language switch", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle"); // Technical state
  await page.context().clearCookies();
  await page.reload();
  await page.waitForLoadState("networkidle");

  const button = page.locator('button[aria-label="Select a language"]'); // CSS selector
  await button.click();
  await page.waitForTimeout(200); // Arbitrary wait

  const option = page.locator('a[aria-label="切换至中文"]');
  await option.click();
  await page.waitForFunction(() => window.location.pathname.includes("/zh")); // URL check

  const cookies = await page.context().cookies(); // Implementation detail
  expect(cookies.find((c) => c.name === "NEXT_LOCALE")?.value).toBe("zh");
});
```

### ✅ Good: Testing User-Visible Behavior

```typescript
test("language switch", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Welcome" })).toBeVisible();

  await page.getByRole("button", { name: "Select a language" }).click();
  await page.getByRole("link", { name: "切换至中文" }).click();

  // Wait for actual content to change
  await expect(page.getByRole("heading", { name: "欢迎" })).toBeVisible();
});
```

## Common Patterns

### Navigation and Verification

```typescript
await page.goto("/products");
await expect(page.getByRole("heading", { name: "Our Products" })).toBeVisible();
```

### Form Interaction

```typescript
await page.getByLabel("Email").fill("user@example.com");
await page.getByLabel("Password").fill("secure123");
await page.getByRole("button", { name: "Sign In" }).click();
await expect(page.getByText("Welcome back!")).toBeVisible();
```

### List Interaction

```typescript
await page.getByRole("button", { name: "Action" }).first().click();
await expect(page.getByText("Action completed")).toBeVisible();
```

### Conditional Elements

```typescript
if (await page.getByRole("button", { name: "Accept" }).isVisible()) {
  await page.getByRole("button", { name: "Accept" }).click();
}
```

## Running Tests

```bash
pnpm test:e2e                              # Run all E2E tests (auto-starts dev server)
pnpm test:e2e e2e/some-file.spec.ts        # Run specific test file
pnpm test:e2e --grep "test name"           # Run tests matching pattern
pnpm test                                  # Run unit tests (Vitest)
```

## Verification Workflow

**IMPORTANT: After writing or modifying E2E tests, YOU must run them to verify they pass.**

1. Run the specific test file or use `--grep` to run just the new test
2. If the test fails, fix the issue and re-run
3. Only report completion after the test passes

Do NOT tell the user to run the tests themselves - run them and report the results.

## Key Reminders

1. **Think like a user** - What would the user see and do?
2. **Use semantic locators** - Roles, labels, text users see
3. **Wait for content** - Visible elements, not technical state
4. **Avoid implementation** - No URLs, cookies, localStorage assertions
5. **Keep it simple** - Minimal setup, clear test flow
