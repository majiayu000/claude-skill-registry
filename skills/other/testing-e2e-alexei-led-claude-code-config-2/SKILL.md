---
name: testing-e2e
description: E2E testing with Playwright MCP for browser automation, test generation, and UI testing. Use when discussing E2E tests, Playwright, browser testing, UI automation, visual testing, or accessibility testing. Supports TypeScript tests and Go/HTMX web applications.
user-invocable: true
context: fork
argument-hint: "[run|record|generate|verify <feature>]"
allowed-tools:
  - Task
  - TaskOutput
  - TodoWrite
  - Bash(npx playwright *)
  - Bash(npm *)
  - Bash(bun *)
  - Read
  - Grep
  - Glob
  - LS
  - AskUserQuestion
  - mcp__playwright__*
---

# E2E Testing with Playwright

Execute E2E testing workflows using Playwright MCP.

**Use TodoWrite** to track these 4 phases:

1. Determine action (parse args or ask)
2. Execute action (run/record/generate/verify)
3. Verify results
4. Present output

---

## Phase 1: Parse Arguments

**$ARGUMENTS:**

- `run` → Run existing E2E tests
- `record` → Record browser session for test generation
- `generate` → Generate test from URL or page description
- `verify <feature>` → Verify specific feature works in browser
- (empty) → Ask what to do

If no argument provided, use AskUserQuestion:

| Header | Question                      | Options                                                                                                                                                                      |
| ------ | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Action | What E2E testing task to run? | 1. **Run tests** - Execute existing Playwright tests 2. **Record** - Record browser session 3. **Generate** - Create test from URL/description 4. **Verify** - Check feature |

---

## Phase 2: Execute Action

### Run Tests

```bash
npx playwright test
```

For specific test:

```bash
npx playwright test login.spec.ts
```

For headed mode (visible browser):

```bash
npx playwright test --headed
```

### Record Session

Use Playwright MCP tools for browser interaction:

1. `browser_navigate` - Go to target URL
2. `browser_snapshot` - Inspect page structure
3. `browser_click`, `browser_type`, `browser_fill_form` - Interact
4. Generate test file with Page Object pattern

### Generate Test

**Spawn playwright-tester agent:**

```
Task(
  subagent_type="playwright-tester",
  description="Generate E2E test",
  prompt="Generate E2E test for:
  URL: {target URL}
  Flow: {user flow description}

  Requirements:
  - Use Page Object pattern
  - Use semantic locators (getByRole, getByLabel, getByText)
  - Include assertions for expected outcomes
  - No hardcoded waits (use waitFor patterns)
  - Include accessibility checks where appropriate"
)
```

### Verify Feature

**Spawn playwright-tester agent for feature verification:**

```
Task(
  subagent_type="playwright-tester",
  description="Verify feature",
  prompt="Verify this feature works correctly in the browser:
  Feature: {feature description}

  Steps:
  1. Navigate to appropriate page
  2. Execute user flow
  3. Assert expected outcomes
  4. Report PASS/FAIL with evidence (screenshots if needed)"
)
```

---

## Phase 3: Verify Results

```bash
npx playwright test --headed
```

If tests fail, review output and fix issues.

---

## Phase 4: Output

```
E2E TESTING
===========
Action: {run|record|generate|verify}
Result: {outcome}
Tests: {pass/fail count}

Details:
- [test results or generation summary]
```

---

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

---

**Execute E2E testing workflow now.**
