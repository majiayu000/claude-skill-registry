---
name: fix-all-tests
description: Fix all failing tests by running the test suite and spawning subagents to fix each failing test file. Use when the user asks to fix all tests, fix failing tests, or update tests to match current code.
---

# Fix All Tests

Fix all failing tests by running the full test suite, then spawning parallel subagents to fix each failing test file.

**Key assumption**: The implementation code is correct. Tests need to be updated to match current behavior.

## Workflow

### Step 1: Run the Full Test Suite

Run all tests and capture output:

```bash
npm run test 2>&1
```

Parse the output to identify all failing test files.

### Step 2: Extract Failing Test Files

From the test output, identify each unique test file that has failures. Look for patterns like:

- `FAIL src/path/to/test.spec.ts`
- `● Test Suite: path/to/test`

Create a list of all failing test file paths.

### Step 3: Spawn Subagents for Each Failing File

For each failing test file, spawn a subagent using the Task tool with these parameters:

```
subagent_type: "generalPurpose"
description: "Fix tests in [filename]"
prompt: |
  Fix the failing tests in [full file path].

  IMPORTANT: Assume the implementation code is CORRECT. The tests need to be updated to match the current behavior.

  Steps:
  1. Read the failing test file
  2. Read the implementation file(s) being tested
  3. Understand what the code actually does
  4. Update the test expectations to match the actual behavior
  5. Run the specific test file to verify: npm run test -- [file path]
  6. Repeat until all tests in this file pass
  7. Lint the file: npm run lint -- [file path] --fix
  8. Fix any remaining lint errors

  Do NOT modify implementation code - only update tests.
```

**Parallelization**: Launch up to 4 subagents concurrently. If more than 4 files are failing, wait for some to complete before launching more.

### Step 4: Verify All Tests Pass

After all subagents complete, run the full test suite again:

```bash
npm run test
```

If any tests still fail, repeat Step 3 for remaining failures.

## Example Subagent Prompt

For a file `src/features/auth/auth.spec.ts`:

```
Fix the failing tests in src/features/auth/auth.spec.ts.

IMPORTANT: Assume the implementation code is CORRECT. The tests need to be updated to match the current behavior.

Steps:
1. Read the failing test file
2. Read the implementation file(s) being tested
3. Understand what the code actually does
4. Update the test expectations to match the actual behavior
5. Run the specific test file to verify: npm run test -- src/features/auth/auth.spec.ts
6. Repeat until all tests in this file pass
7. Lint the file: npm run lint -- src/features/auth/auth.spec.ts --fix
8. Fix any remaining lint errors

Do NOT modify implementation code - only update tests.
```

## Notes

- If a subagent cannot fix a test, it should report the issue rather than modifying implementation code
- Some test failures may be interdependent - fixing one may fix others
- Each subagent lints its file after fixing tests
