---
name: generate-e2e-test
description: Generate an end-to-end test for a given feature or user story. Use when the user asks to create E2E tests, automate workflows, test user flows, or convert manual workflows into Playwright tests. Leverages Playwright MCP to perform the workflow interactively before generating test code.
argument-hint: Write/paste your workflow description here along with hints about where to write the code.
allowed-tools: mcp__Playwright_browser_click, mcp__Playwright_browser_console_messages, mcp__Playwright_browser_drag, mcp__Playwright_browser_evaluate, mcp__Playwright_browser_file_upload, mcp__Playwright_browser_fill_form, mcp__Playwright_browser_handle_dialog, mcp__Playwright_browser_hover, mcp__Playwright_browser_navigate, mcp__Playwright_browser_navigate_back, mcp__Playwright_browser_network_requests, mcp__Playwright_browser_press_key, mcp__Playwright_browser_resize, mcp__Playwright_browser_select_option, mcp__Playwright_browser_snapshot, mcp__Playwright_browser_take_screenshot, mcp__Playwright_browser_type, mcp__Playwright_browser_wait_for, mcp__Playwright_browser_mouse_click_xy, mcp__Playwright_browser_mouse_drag_xy, mcp__Playwright_browser_mouse_move_xy, mcp__Playwright_browser_verify_element_visible, mcp__Playwright_browser_verify_text_visible, mcp__Playwright_browser_verify_value, Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# Generate E2E Test

This Skill converts workflow descriptions into working automated end-to-end tests by first performing the workflow step-by-step using Playwright MCP browser tools, then generating and refining test code based on the actual interaction.

## Overview

Convert the following workflow description into working automated tests:

$ARGUMENTS

## Process

### 1. Initial Setup

- Start Playwright MCP browser session using `browser_navigate` to target URL
- Ask the user to authenticate and perform any initialization steps if needed (there are likely already helper methods in the project test platform files for this)
- Take initial snapshot using `browser_snapshot` to understand page structure and confirm readiness to begin with the user

### 2. Manual Workflow Execution

For each step in the described workflow:

**Capture state**: Use `browser_snapshot` before each interaction to understand the current page structure

**Perform action**: Execute using appropriate MCP tools:
- `browser_click` - Click buttons, links, or elements
- `browser_type` - Type text into fields
- `browser_fill_form` - Fill multiple form fields at once
- `browser_select_option` - Select from dropdowns
- `browser_press_key` - Press keyboard keys
- Other browser tools as needed

**Collect selectors**:
- Primary: Note `ref` values from accessibility snapshots (most stable)
- Fallback: Use `browser_evaluate` with queries like `document.querySelector('[data-testid="..."]')` if needed

**Verify outcomes**: Use `browser_wait_for` or snapshot to confirm expected results after each action

**Document**: Track successful selector patterns and interaction sequences for test generation

### 3. Generate Test Code

**Read project conventions**: Review `TESTING.md` for:
- Test runner setup and syntax
- Available helper methods and fixtures
- Assertion patterns
- File naming and location conventions

**Write test spec**: Transform recorded workflow into test code using:
- Collected selectors (prefer stable attributes: data-testid, aria-label, role+name)
- Project's testing patterns from TESTING.md
- Appropriate waits and assertions
- Helper methods from `tests/e2e/utils/test-helpers.ts`

**File location**: Place test in appropriate directory under `tests/e2e/` based on feature area:
- `tests/e2e/admin/` - Super admin features
- `tests/e2e/auth/` - Authentication flows
- `tests/e2e/client/` - Client-specific features
- `tests/e2e/dashboard/` - Dashboard pages
- `tests/e2e/marketing/` - Public pages
- `tests/e2e/workouts/` - Workout features

### 4. Validate & Refine

**Run test**: Execute using project's test command from TESTING.md:
```bash
pnpm test:e2e:ai tests/e2e/your-test.spec.ts
```

**Debug failures**:
- If selector issues: Return to MCP browser, use `browser_snapshot` and `browser_evaluate` to find better selectors
- If timing issues: Add appropriate waits using `waitForElementWithRetry` or similar helpers
- If assertion failures: Verify expected values using MCP tools

**Iterate**: Repeat debugging until test passes consistently

## Key MCP Tools Usage

**Discovery**:
- `browser_snapshot` (primary) - Get page structure and element information
- `browser_evaluate` (for complex queries) - Execute JavaScript to query DOM

**Actions**:
- `browser_click` - Click elements
- `browser_type` - Type text
- `browser_fill_form` - Fill multiple form fields
- `browser_select_option` - Select dropdown options
- `browser_press_key` - Press keyboard keys

**Validation**:
- `browser_wait_for` - Wait for elements or conditions
- `browser_verify_*` tools - Verify element visibility, text, and values

**Debugging**:
- `browser_console_messages` - Check console errors
- `browser_network_requests` - Inspect network activity
- `browser_take_screenshot` - Capture visual state

## Best Practices

### Selector Strategy
- Prefer accessibility-based selectors (role, aria-label) over fragile CSS
- Use test utilities like `getByRole()`, `getByText()`, `getByLabel()` from Playwright
- Always verify selectors return only a single element to avoid strict mode violations
- Check if actions are in dropdown menus (look for "More actions" buttons)

### Waiting and Timing
- Always wait for elements/text after navigation or async operations
- Use helper methods like `waitForElementWithRetry()` for robust waiting
- For table data: Use `waitForTableLoaded(page)` before interacting with table elements

### Test Structure
- Use fixtures from `tests/e2e/fixtures.ts` for pre-configured test data
- Test both happy path and error conditions when specified
- Scope selectors to specific containers to avoid matching toast notifications
- Clean up test data using protected email patterns (`e2e-*@example.com`)

### Navigation
- Use `navigateToPage()` helper instead of `page.goto()` for reliable client-side routing
- Wait for content-based conditions, not just `domcontentloaded`

## Examples

### Simple Form Test
```typescript
import { test, expect } from './fixtures'
import { navigateToPage, expectToast } from './utils/test-helpers'

test('user can create exercise', async ({ page, superAdminUser }) => {
  await navigateToPage(page, '/super-admin/exercises')

  await page.getByRole('button', { name: 'Add Exercise' }).click()
  await page.getByLabel('Name').fill('Bench Press')
  await page.getByLabel('Muscle Group').selectOption('Chest')

  await page.getByRole('button', { name: 'Save' }).click()
  await expectToast(page, 'Exercise created successfully')
})
```

### Workflow with Dropdown Menu
```typescript
test('user can delete exercise', async ({ page, superAdminUser }) => {
  await navigateToPage(page, '/super-admin/exercises')

  // Open dropdown menu first
  const row = page.locator('tr').filter({ hasText: 'Bench Press' })
  await row.locator('[aria-label*="More actions"]').click()

  // Then select delete action
  await page.getByRole('menuitem', { name: 'Delete' }).click()
  await page.getByRole('button', { name: 'Confirm' }).click()

  await expectToast(page, 'Exercise deleted successfully')
})
```

## Requirements

- Playwright MCP server must be running and connected
- Development server should be running at http://localhost:3000
- Project must have `TESTING.md` and test utilities configured

## Troubleshooting

If tests fail:
1. Read the AI Coding Agent Reporter output in `test-report-for-coding-agents/all-failures.md`
2. Check console logs using `browser_console_messages`
3. Inspect DOM structure with `browser_snapshot`
4. Verify network requests with `browser_network_requests`
5. Take screenshots at failure points with `browser_take_screenshot`

If stuck debugging, ask a human to inspect the Playwright trace in `playwright-report/` which contains detailed execution information.
