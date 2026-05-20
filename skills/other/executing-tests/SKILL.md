---
name: executing-tests
description: |
  Executes test cases from a TestLink plan using browser automation and records
  pass/fail results per case. Use when a QA engineer wants to execute tests,
  run tests, execute a test plan, or run test cases against an application.
disable-model-invocation: true
tools:
  - testlink-mcp:get_test_cases_for_test_plan
  - testlink-mcp:read_test_case
  - testlink-mcp:create_test_execution
  - playwright-mcp:browser_navigate
  - playwright-mcp:browser_resize
  - playwright-mcp:browser_snapshot
  - playwright-mcp:browser_click
  - playwright-mcp:browser_type
  - playwright-mcp:browser_take_screenshot
---

# executing-tests

Executes test cases from a TestLink plan using browser automation and records pass/fail results.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Get test cases for plan, show execution status summary
- [ ] For each test case:
  - [ ] Read test steps from TestLink
  - [ ] Execute via browser (navigate, click, type, screenshot)
  - [ ] Record result (p/f/b + notes)
- [ ] Validate: Total executed, passed, failed, blocked, pass rate %
```

## Steps

### Step 1: Get Test Cases for Plan

Run `/tl-read-execution` to fetch all test cases assigned to the test plan and display an execution status summary (not executed, passed, failed, blocked).

**MCP tool:** `testlink-mcp:get_test_cases_for_test_plan`

### Step 2: Execute Each Test Case

Run `/tl-execute-case` for each test case in the plan:

1. **Read** the test case from TestLink to get steps, preconditions, and expected results
   - **MCP tool:** `testlink-mcp:read_test_case`

2. **Set up browser:** navigate to application URL, resize to 1280px, authenticate
   - **MCP tools:** `playwright-mcp:browser_navigate`, `playwright-mcp:browser_resize`

3. **Execute each step** sequentially:
   - Take snapshot to understand current page state
   - Perform the action (click, type, select, navigate)
   - Verify actual result against expected result
   - Document pass/fail for each step

4. **Capture screenshots** at key verification points
   - **MCP tool:** `playwright-mcp:browser_take_screenshot`

### Step 3: Record Results

Run `/tl-create-execution` after executing each test case to record the result in TestLink:
- Status: `p` (pass), `f` (fail), `b` (blocked)
- Notes: specific observations, failure details, or "All steps completed successfully"

**IMPORTANT:** Use NUMERIC test case ID, not external format (e.g., "5" not "PROJ-1")

**MCP tool:** `testlink-mcp:create_test_execution`

### Validate (Final Summary)

After all test cases are executed, report:

```
Total Test Cases: N
├── Passed: N
├── Failed: N
├── Blocked: N
└── Not Executed: N

Pass Rate: XX%
```

## Expected Input

- TestLink test plan ID
- Application URL
- Login credentials (optional)

## Next Step

Review failed test cases and create bug reports if needed.
