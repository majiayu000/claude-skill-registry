---
name: browser-test
description: Execute browser-based UI testing using Chrome MCP tools. Tests user interactions, visual outcomes, captures evidence. Use for UI features after implementation and security review.
allowed-tools: Read, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__find, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__form_input, mcp__claude-in-chrome__javascript_tool
---

# Browser Testing Skill

## Purpose
Execute browser-based UI testing for web applications using Claude in Chrome MCP tools. Verify UI acceptance criteria, capture evidence, and validate user flows.

## When to Use

Mandatory for:
- UI components or page changes
- User interaction flows (clicks, forms, navigation)
- Visual features (modals, toasts, animations)
- Responsive design changes

Optional for:
- Backend-only changes
- API-only features
- Non-visual refactoring

## Browser Testing Process

### Step 1: Load Spec and Identify UI Criteria

```bash
# Load spec
cat .claude/specs/active/<slug>.md
```

Extract UI-specific acceptance criteria:
- User interactions (button clicks, form submissions)
- Visual feedback (toasts, modals, error messages)
- Navigation (redirects, route changes)
- State changes (UI updates, data display)

Example:
```markdown
## UI Acceptance Criteria (from spec)
- AC1.3: Confirmation toast displayed after logout
- AC2.3: Retry button appears on network error
- AC1.2: User redirected to /login page
```

### Step 2: Get Browser Context

```javascript
// Get existing tabs
tabs_context_mcp({ createIfEmpty: true });

// Create new tab for testing
tabs_create_mcp();
```

**Best practice**: Use a fresh tab for each test session to avoid state pollution.

### Step 3: Navigate to Test Environment

```javascript
navigate({
  url: "http://localhost:3000/dashboard", // or staging URL
  tabId: <tabId>
});
```

**Environment options**:
- Local dev: `http://localhost:3000`
- Staging: `https://staging.example.com`
- Production: Only for smoke tests, never for destructive tests

### Step 4: Execute UI Test Cases

For each UI acceptance criterion, execute a test case.

#### Test Case Structure

```markdown
**Test Case**: AC1.3 - Confirmation toast after logout

**Steps**:
1. Navigate to /dashboard
2. Find logout button
3. Click logout button
4. Wait for toast to appear
5. Verify toast message

**Expected**: Toast with message "You have been logged out"

**Evidence**: Screenshot of toast
```

#### Executing Test Steps

```javascript
// Step 1: Navigate
navigate({ url: "http://localhost:3000/dashboard", tabId });

// Step 2: Find element
find({ query: "logout button", tabId });
// Returns: ref_1 (logout button reference)

// Step 3: Interact
computer({
  action: "left_click",
  ref: "ref_1",
  tabId
});

// Step 4: Wait and verify
await computer({ action: "wait", duration: 1, tabId });

// Step 5: Take evidence screenshot
computer({ action: "screenshot", tabId });
// Screenshot captured with ID for later reference
```

### Step 5: Verify Outcomes

Use multiple verification methods:

#### Visual Verification
```javascript
// Take screenshot
const screenshot = computer({ action: "screenshot", tabId });

// Use find to locate expected element
find({ query: "confirmation toast", tabId });
// Returns: ref_2 if found, error if not
```

#### DOM Verification
```javascript
// Read page to check element exists
read_page({ tabId, filter: "all" });
// Returns accessibility tree with elements

// Or use JavaScript to verify
javascript_tool({
  tabId,
  action: "javascript_exec",
  text: `
    const toast = document.querySelector('[role="status"]');
    toast?.textContent.includes("logged out");
  `
});
// Returns: true/false
```

#### Navigation Verification
```javascript
// Check current URL
javascript_tool({
  tabId,
  action: "javascript_exec",
  text: "window.location.pathname"
});
// Returns: "/login" (verify redirect)
```

### Step 6: Handle Failures and Errors

#### Element Not Found
```javascript
find({ query: "logout button", tabId });
// Error: "No elements found matching 'logout button'"
```

**Actions**:
1. Take screenshot to see current page state
2. Try alternative selectors ("button with text logout", "sign out button")
3. Check if page loaded correctly (read_page)
4. If element genuinely missing → Report as test failure

#### Interaction Failed
```javascript
computer({ action: "left_click", ref: "ref_1", tabId });
// Element not clickable, or click has no effect
```

**Actions**:
1. Wait for page to settle (animations, loading)
2. Scroll element into view
3. Try alternative interaction (keyboard instead of mouse)
4. Report as test failure if truly broken

#### Unexpected Behavior
```javascript
// Expected redirect to /login, but stayed on /dashboard
javascript_tool({ text: "window.location.pathname", tabId });
// Returns: "/dashboard" (unexpected)
```

**Action**: Document failure with evidence (screenshot) and report.

### Step 7: Capture Evidence

For each test case, capture evidence:

```javascript
// Screenshot of key states
computer({ action: "screenshot", tabId });

// Zoom in on specific element
computer({
  action: "zoom",
  region: [x0, y0, x1, y1], // Element bounds
  tabId
});
```

**Evidence includes**:
- Initial state before interaction
- Interaction point (e.g., button being clicked)
- Final state after interaction
- Error states (if testing error paths)

### Step 8: Document Test Results

Create test results document:

```markdown
# Browser Test Results: <Task Name>

**Date**: 2026-01-02 17:30
**Environment**: http://localhost:3000
**Browser**: Chrome

---

## Test Cases

### TC1: Logout Button Click (AC1.1, AC1.2)
**Status**: ✅ PASS

**Steps**:
1. ✅ Navigated to http://localhost:3000/dashboard
2. ✅ Found logout button (ref_1)
3. ✅ Clicked logout button
4. ✅ Verified redirect to /login

**Evidence**: screenshot-001.png, screenshot-002.png

**Result**: User successfully logged out and redirected

---

### TC2: Confirmation Toast (AC1.3)
**Status**: ✅ PASS

**Steps**:
1. ✅ Clicked logout button
2. ✅ Toast appeared with message "You have been logged out"
3. ✅ Toast auto-dismissed after 3 seconds

**Evidence**: screenshot-003.png

**Result**: Confirmation toast displayed correctly

---

### TC3: Retry Button on Error (AC2.3)
**Status**: ❌ FAIL

**Steps**:
1. ✅ Simulated network error (DevTools network throttling)
2. ✅ Clicked logout button
3. ❌ Expected retry button, but only error message shown

**Evidence**: screenshot-004.png

**Result**: FAILURE - Retry button not rendered

**Issue**: Implementation missing retry button component

---

## Summary

**Passed**: 2/3 (67%)
**Failed**: 1/3 (33%)

**Blocker**: TC3 failure blocks merge - retry button required per spec AC2.3

**Action**: Fix retry button implementation, re-run browser tests
```

### Step 9: Update Spec with Browser Test Evidence

Add results to spec:

```markdown
## Browser Test Results

**Date**: 2026-01-02 17:30
**Environment**: localhost:3000

| AC | Test Case | Status | Evidence |
|----|-----------|--------|----------|
| AC1.1 | Logout clears auth | ✅ Pass | screenshot-001.png |
| AC1.2 | Redirect to /login | ✅ Pass | screenshot-002.png |
| AC1.3 | Confirmation toast | ✅ Pass | screenshot-003.png |
| AC2.3 | Retry button | ❌ Fail | screenshot-004.png |

**Overall**: 3/4 pass (75%) - 1 blocking failure
```

### Step 10: Handle Test Failures

If tests fail:

1. **Verify failure is real** (not test issue):
   - Re-run test to confirm not flaky
   - Check environment is correct
   - Verify test steps match spec

2. **Document failure clearly**:
   - Screenshot showing actual vs expected
   - Steps to reproduce
   - Severity (blocking or minor)

3. **Route to fix**:
   - Use `/implement` to fix implementation
   - Update spec if expectation was wrong
   - Re-run browser tests after fix

## Testing Patterns

### Pattern 1: Form Submission

```javascript
// Find form fields
find({ query: "email input", tabId });
// Returns: ref_1

find({ query: "password input", tabId });
// Returns: ref_2

// Fill form
form_input({ ref: "ref_1", value: "test@example.com", tabId });
form_input({ ref: "ref_2", value: "password123", tabId });

// Find and click submit
find({ query: "submit button", tabId });
// Returns: ref_3

computer({ action: "left_click", ref: "ref_3", tabId });

// Verify outcome
await computer({ action: "wait", duration: 1, tabId });
computer({ action: "screenshot", tabId });
```

### Pattern 2: Modal Interaction

```javascript
// Open modal
find({ query: "delete button", tabId });
computer({ action: "left_click", ref: "ref_1", tabId });

// Verify modal appears
await computer({ action: "wait", duration: 0.5, tabId });
find({ query: "confirmation dialog", tabId });
// Returns: ref_2

// Interact with modal
find({ query: "confirm delete button", tabId });
computer({ action: "left_click", ref: "ref_3", tabId });

// Verify modal dismissed
await computer({ action: "wait", duration: 0.5, tabId });
computer({ action: "screenshot", tabId });
```

### Pattern 3: Navigation Flow

```javascript
// Start at page A
navigate({ url: "http://localhost:3000/page-a", tabId });

// Click link to page B
find({ query: "go to page B link", tabId });
computer({ action: "left_click", ref: "ref_1", tabId });

// Verify navigation
await computer({ action: "wait", duration: 1, tabId });
const currentPath = javascript_tool({
  tabId,
  action: "javascript_exec",
  text: "window.location.pathname"
});

// Assert
if (currentPath === "/page-b") {
  // Success
} else {
  // Failure
}
```

### Pattern 4: Error State Testing

```javascript
// Simulate error condition
javascript_tool({
  tabId,
  action: "javascript_exec",
  text: `
    // Mock API to fail
    window.fetch = async () => {
      throw new Error("Network error");
    };
  `
});

// Trigger action that calls API
find({ query: "save button", tabId });
computer({ action: "left_click", ref: "ref_1", tabId });

// Verify error UI
await computer({ action: "wait", duration: 1, tabId });
find({ query: "error message", tabId });
computer({ action: "screenshot", tabId });
```

## Best Practices

### Use Semantic Selectors
```javascript
// Good - Semantic and resilient
find({ query: "logout button", tabId });
find({ query: "button with text logout", tabId });
find({ query: "button with aria-label logout", tabId });

// Avoid - Brittle selectors
// (find tool doesn't use CSS selectors, but JavaScript tool could)
```

### Wait for Interactions to Complete
```javascript
// After click, wait for action to complete
computer({ action: "left_click", ref: "ref_1", tabId });
await computer({ action: "wait", duration: 1, tabId }); // Wait 1 second

// Or check for expected element
find({ query: "success message", tabId });
```

### Capture Evidence Liberally
```javascript
// Before interaction
computer({ action: "screenshot", tabId });

// After interaction
computer({ action: "left_click", ref: "ref_1", tabId });
await computer({ action: "wait", duration: 1, tabId });
computer({ action: "screenshot", tabId });

// Evidence trail for debugging
```

### Clean Up Test State
```javascript
// After tests, reset state
javascript_tool({
  tabId,
  action: "javascript_exec",
  text: "localStorage.clear(); sessionStorage.clear();"
});

// Or create fresh tab for next test
tabs_create_mcp();
```

## Integration with Other Skills

After browser testing:
- If PASS with public API → Trigger `/docs` for documentation, then commit
- If PASS (no public API) → Ready for commit
- If FAIL → Use `/implement` to fix, then re-test

Before browser testing:
- Run `/unify` for spec-impl-test convergence
- Run `/security` for security review
- Browser testing validates UI before final gates

**Documentation trigger**: If the implementation adds or modifies public APIs, user-facing features, or configuration options, dispatch the documenter subagent after browser tests pass (before commit).

## Example Test Suite

### Example: Logout Feature Browser Tests

**Spec ACs**:
- AC1.1: Logout clears token
- AC1.2: Redirect to /login
- AC1.3: Confirmation toast
- AC2.3: Retry button on error

**Test Suite**:

```javascript
// Test 1: Happy path logout
navigate({ url: "http://localhost:3000/dashboard", tabId });
find({ query: "logout button", tabId }); // ref_1
computer({ action: "screenshot", tabId }); // Before
computer({ action: "left_click", ref: "ref_1", tabId });
await computer({ action: "wait", duration: 1, tabId });
computer({ action: "screenshot", tabId }); // After

// Verify redirect (AC1.2)
const path = javascript_tool({
  tabId,
  action: "javascript_exec",
  text: "window.location.pathname"
});
// Result: "/login" ✅

// Verify toast (AC1.3)
find({ query: "confirmation toast", tabId }); // Found ✅

// Test 2: Error path with retry
navigate({ url: "http://localhost:3000/dashboard", tabId });

// Simulate network error
javascript_tool({
  tabId,
  action: "javascript_exec",
  text: "window.fetch = () => Promise.reject(new Error('Network error'));"
});

find({ query: "logout button", tabId }); // ref_1
computer({ action: "left_click", ref: "ref_1", tabId });
await computer({ action: "wait", duration: 1, tabId });

// Verify error message
find({ query: "error message", tabId }); // Found ✅

// Verify retry button (AC2.3)
find({ query: "retry button", tabId }); // Not found ❌
computer({ action: "screenshot", tabId }); // Evidence

// Result: FAIL - Retry button missing
```

**Output**: 3/4 ACs pass, 1 blocking failure (retry button missing)
