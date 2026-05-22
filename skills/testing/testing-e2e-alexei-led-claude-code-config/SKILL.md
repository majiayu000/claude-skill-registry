---
name: testing-e2e
description: E2E testing with Playwright MCP for browser automation, test generation, and UI testing. Use when discussing E2E tests, Playwright, browser testing, UI automation, visual testing, or accessibility testing. Supports TypeScript tests and Go/HTMX web applications.
user-invocable: false
context: fork
agent: playwright-tester
allowed-tools:
  - Task
  - mcp__playwright__*
---

# E2E Testing with Playwright

Use Playwright MCP tools for browser automation and E2E testing.

## Quick Start

```
/test:e2e run      # Run existing tests
/test:e2e record   # Record browser session
/test:e2e generate # Generate test from URL
```

## Spawn Agent

```
Task(subagent_type="playwright-tester", prompt="<task>")
```

## Key Tools

| Tool                       | Purpose                |
| -------------------------- | ---------------------- |
| `browser_navigate`         | Go to URL              |
| `browser_snapshot`         | Get accessibility tree |
| `browser_click`            | Click elements         |
| `browser_type`             | Type text              |
| `browser_fill_form`        | Fill form fields       |
| `browser_generate_locator` | Get best locator       |
| `browser_verify_text`      | Assert text content    |

## Supported Stacks

- **TypeScript**: Playwright Test with Page Objects
- **Go/HTMX**: Test HTMX interactions, form submissions, partial updates

## HTMX Testing Tips

- Use `browser_snapshot` to verify DOM updates after HTMX swaps
- Test `hx-trigger`, `hx-swap`, `hx-target` behaviors
- Verify `HX-*` response headers in network requests
- Assert partial page updates without full reload

## Error Scenarios & Handling

### Element Not Found

```typescript
// BAD: Immediate failure
await page.click("#submit-btn");

// GOOD: Wait with timeout + fallback
const btn = page.locator("#submit-btn");
if ((await btn.count()) === 0) {
  // Try alternative selector
  await page.click('button[type="submit"]');
} else {
  await btn.click();
}
```

**Recovery strategies:**

1. Use `browser_snapshot` to inspect current DOM state
2. Try alternative locators (text, role, data-testid)
3. Check if element is in iframe/shadow DOM
4. Verify page loaded correctly (check URL, title)

### Timeout Errors

| Error              | Cause                    | Solution                          |
| ------------------ | ------------------------ | --------------------------------- |
| Navigation timeout | Slow page load           | Increase timeout, check network   |
| Action timeout     | Element not interactable | Wait for visibility/enabled state |
| Expect timeout     | Assertion failed         | Verify DOM state with snapshot    |

```typescript
// Configure timeouts
test.setTimeout(60000); // Test timeout
page.setDefaultTimeout(30000); // Action timeout

// Or per-action
await page.click("#btn", { timeout: 10000 });
```

### Network Issues

```typescript
// Wait for network idle
await page.waitForLoadState("networkidle");

// Mock failing endpoints
await page.route("**/api/**", (route) => {
  route.fulfill({ status: 500, body: "Server Error" });
});
```

### Flaky Test Patterns

**Avoid:**

- Fixed `page.waitForTimeout(1000)` delays
- Brittle selectors like `.btn-23`
- Tests depending on animation timing

**Prefer:**

- `waitForSelector`, `waitForLoadState`
- Role/text-based selectors: `getByRole('button', { name: 'Submit' })`
- Retry patterns for known flaky operations

### Debugging Failed Tests

1. **Get snapshot**: `browser_snapshot` shows accessibility tree
2. **Screenshot**: Capture current visual state
3. **Console logs**: Check browser console for JS errors
4. **Network tab**: Verify API calls succeeded
5. **Trace**: Enable Playwright trace for post-mortem

```bash
# Run with trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```
