---
name: wallaby-testing
description: Check test status and debug failing tests using Wallaby.js real-time test results. Use after making code changes to verify tests pass, when checking if tests are failing, debugging test errors, analyzing assertions, inspecting runtime values, checking coverage, updating snapshots, or when user mentions Wallaby, tests, coverage, or test status.
compatibility: Requires Wallaby.js VS Code extension installed and running
metadata:
  author: wallaby.js
  version: "1.0"
---

# Wallaby Testing Skill

Check test status and debug failing tests using Wallaby.js real-time test execution data.

## When to Use

- **After code changes** - Verify tests pass after modifications
- **Checking test status** - See if any tests are failing
- **Debugging failures** - Analyze test errors and exceptions
- **Inspecting runtime values** - Examine variable states during tests
- **Understanding coverage** - See which code paths tests execute
- **Updating snapshots** - When snapshot changes are needed
- User mentions "tests", "test status", "run tests", or "Wallaby"

## Available Wallaby Tools

Use these tools to gather test information:

| Tool | Purpose |
|------|---------|
| `wallaby_failingTests` | Get all failing tests with errors and stack traces |
| `wallaby_failingTestsForFile` | Get failing tests for a specific file |
| `wallaby_allTests` | Get all tests (useful when there are no failures but you need test IDs) |
| `wallaby_allTestsForFile` | Get tests covering/executing a specific file |
| `wallaby_failingTestsForFileAndLine` | Get failing tests covering/executing a specific file and line |
| `wallaby_allTestsForFileAndLine` | Get tests covering a specific line |
| `wallaby_runtimeValues` | Inspect variable values at a code location |
| `wallaby_runtimeValuesByTest` | Get runtime values for a specific test |
| `wallaby_coveredLinesForFile` | Get coverage data for a file |
| `wallaby_coveredLinesForTest` | Get lines covered by a specific test |
| `wallaby_testById` | Get detailed test data by ID |
| `wallaby_updateTestSnapshots` | Update snapshots for a test |
| `wallaby_updateFileSnapshots` | Update all snapshots in a file |
| `wallaby_updateProjectSnapshots` | Update all snapshots in the project |

### What Inputs These Tools Need

- **For file-scoped tools** (like `wallaby_failingTestsForFile`, `wallaby_coveredLinesForFile`): pass the workspace-relative file path.
- **For line-scoped tools** (like `wallaby_allTestsForFileAndLine`, `wallaby_runtimeValues`): pass `file`, `line`, and the exact `lineContent` string from the file.
- **For test-scoped tools** (like `wallaby_testById`, `wallaby_runtimeValuesByTest`, `wallaby_coveredLinesForTest`): pass `testId` from `wallaby_failingTests` / `wallaby_allTests`.

## Debugging Workflow

### Step 1: Get Failing Tests

Start by retrieving failing test information:
- Use `wallaby_failingTests` to see all failures
- Review error messages and stack traces
- Note the test ID for further inspection

If there are no failing tests but the user is asking about test status or coverage, use `wallaby_allTests` to confirm the current state and to obtain test IDs.

### Step 2: Locate Related Code (Optional)

If the error and stack trace from Step 1 don't provide enough context:
- Use `wallaby_coveredLinesForTest` with the test ID
- Focus analysis on covered source files
- Identify which code paths are executed
- Skip this step if the failure cause is already clear

### Step 3: Inspect Runtime Values (Optional)

Examine variable states at failure points or other points of interest:
- Use `wallaby_runtimeValues` for specific locations
- Use `wallaby_runtimeValuesByTest` for test-specific values
- Compare expected vs actual values
- Skip this step if the failure cause is already clear

### Step 4: Implement Fix

Based on analysis:
- Identify the root cause
- Make targeted code changes
- Reference runtime values in your explanation

### Step 5: Verify Fix

After changes:
- Wallaby re-runs tests automatically
- Use `wallaby_testById` to confirm test passes
- Check no regressions with `wallaby_failingTests`

### Step 6: Update Snapshots (if needed)

When snapshots need updating:
- Use `wallaby_updateTestSnapshots` for specific tests
- Use `wallaby_updateFileSnapshots` for all in a file
- Use `wallaby_updateProjectSnapshots` only when many snapshots changed
- Verify tests pass after updates

## Example: Debugging an Assertion Failure

<example>
User: "The calculator test is failing"

1. Call wallaby_failingTests → Get test ID and error
   Error shows: "expected 4, got 5" in multiply function
2. (Optional) Call wallaby_coveredLinesForTest(testId) → Skip if error is clear
3. (Optional) Call wallaby_runtimeValues(file, line, expression) → Skip if cause is obvious
4. Analyze: multiply used + instead of *
5. Fix: Change + to * in calculator.js
6. Call wallaby_failingTests → Confirm no failures remain
</example>

## Best Practices

- **Use Wallaby tools first** - They provide real-time data without re-running tests
- **Get test IDs early** - Many tools require the test ID from initial queries
- **Inspect runtime values** - More reliable than guessing variable states
- **Verify after fixes** - Always confirm the test passes before finishing
- **Check for regressions** - Ensure fixes don't break other tests