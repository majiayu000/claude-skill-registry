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

### Step 1: Load Spec Group and Identify UI Criteria

```bash
# Load spec group
cat .claude/specs/groups/<spec-group-id>/manifest.json
cat .claude/specs/groups/<spec-group-id>/spec.md

# List atomic specs
ls .claude/specs/groups/<spec-group-id>/atomic/

# Read atomic specs for UI-related acceptance criteria
cat .claude/specs/groups/<spec-group-id>/atomic/as-001-*.md
```

Extract UI-specific acceptance criteria from atomic specs:
- User interactions (button clicks, form submissions)
- Visual feedback (toasts, modals, error messages)
- Navigation (redirects, route changes)
- State changes (UI updates, data display)

Example:
```markdown
## UI Acceptance Criteria (from atomic specs)
- as-001 AC1: Logout button visible in UserMenu
- as-001 AC2: Clicking logout triggers logout flow
- as-003 AC1: User redirected to /login page
- as-004 AC1: Confirmation toast displayed after logout
- as-004 AC2: Error message shown on network failure
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

For each UI acceptance criterion in atomic specs, execute a test case.

#### Test Case Structure

```markdown
**Test Case**: as-004 AC1 - Confirmation toast after logout

**Atomic Spec**: as-004 (Error Handling & Feedback)

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
**Spec Group**: .claude/specs/groups/<spec-group-id>/

---

## Test Cases by Atomic Spec

### as-001: Logout Button UI

#### TC1: Logout Button Click (as-001 AC1, AC2)
**Status**: ✅ PASS

**Steps**:
1. ✅ Navigated to http://localhost:3000/dashboard
2. ✅ Found logout button (ref_1)
3. ✅ Clicked logout button
4. ✅ Verified logout flow initiated

**Evidence**: screenshot-001.png, screenshot-002.png

**Result**: Logout button renders and triggers logout

---

### as-003: Post-Logout Redirect

#### TC2: Redirect to Login (as-003 AC1)
**Status**: ✅ PASS

**Steps**:
1. ✅ Clicked logout button
2. ✅ Verified redirect to /login

**Evidence**: screenshot-003.png

**Result**: User redirected to login page

---

### as-004: Error Handling & Feedback

#### TC3: Confirmation Toast (as-004 AC1)
**Status**: ✅ PASS

**Steps**:
1. ✅ Clicked logout button
2. ✅ Toast appeared with message "You have been logged out"
3. ✅ Toast auto-dismissed after 3 seconds

**Evidence**: screenshot-004.png

**Result**: Confirmation toast displayed correctly

#### TC4: Retry Button on Error (as-004 AC2)
**Status**: ❌ FAIL

**Steps**:
1. ✅ Simulated network error (DevTools network throttling)
2. ✅ Clicked logout button
3. ❌ Expected retry button, but only error message shown

**Evidence**: screenshot-005.png

**Result**: FAILURE - Retry button not rendered

**Issue**: Implementation missing retry button component

---

## Summary

**Atomic Specs Tested**: 3 (as-001, as-003, as-004)

**Per Atomic Spec**:
- as-001: ✅ 1/1 pass
- as-003: ✅ 1/1 pass
- as-004: ⚠️ 1/2 pass (1 fail)

**Overall**: 3/4 (75%)

**Blocker**: TC4 failure blocks merge - retry button required per as-004 AC2

**Action**: Fix retry button implementation, re-run browser tests
```

### Step 9: Update Manifest and Atomic Specs with Browser Test Evidence

Update `manifest.json` with browser test status:

```json
{
  "convergence": {
    "browser_tested": true  // or false if blocking failures
  },
  "decision_log": [
    {
      "timestamp": "<ISO timestamp>",
      "actor": "agent",
      "action": "browser_test_complete",
      "details": "3/4 pass - 1 blocking failure in as-004 AC2"
    }
  ]
}
```

Add browser test evidence to atomic specs:

```markdown
## Browser Test Evidence

| AC | Test Case | Status | Evidence |
|----|-----------|--------|----------|
| AC1 | Toast displayed | ✅ Pass | screenshot-004.png |
| AC2 | Retry button | ❌ Fail | screenshot-005.png |

**Browser Test Status**: ⚠️ 1/2 pass
```

Summary in spec group:

```markdown
## Browser Test Results

**Date**: 2026-01-02 17:30
**Environment**: localhost:3000

| Atomic Spec | AC | Test Case | Status | Evidence |
|-------------|-----|-----------|--------|----------|
| as-001 | AC1 | Logout button | ✅ Pass | screenshot-001.png |
| as-003 | AC1 | Redirect to /login | ✅ Pass | screenshot-003.png |
| as-004 | AC1 | Confirmation toast | ✅ Pass | screenshot-004.png |
| as-004 | AC2 | Retry button | ❌ Fail | screenshot-005.png |

**Overall**: 3/4 pass (75%) - 1 blocking failure in as-004
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

**Spec Group**: sg-logout-button

**Atomic Spec UI ACs**:
- as-001 AC1: Logout button visible
- as-001 AC2: Click triggers logout
- as-003 AC1: Redirect to /login
- as-004 AC1: Confirmation toast
- as-004 AC2: Retry button on error

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

// Verify retry button (as-004 AC2)
find({ query: "retry button", tabId }); // Not found ❌
computer({ action: "screenshot", tabId }); // Evidence

// Result: FAIL - Retry button missing
```

**Output**:
- as-001: ✅ 2/2 ACs pass
- as-003: ✅ 1/1 AC pass
- as-004: ⚠️ 1/2 ACs pass (retry button missing)

**Overall**: 4/5 ACs pass, 1 blocking failure in as-004 AC2
