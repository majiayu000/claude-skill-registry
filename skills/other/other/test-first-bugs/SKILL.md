---
name: test-first-bugs
description: This skill should be used when the user reports a bug, describes unexpected behavior, says something is "broken", "not working", "failing", mentions an "error", "issue", or "problem" in code, or asks to "fix" something. Enforces test-driven bug fixing workflow.
---

# Test-first bug fixing

Enforce a disciplined bug-fixing workflow that prevents regression and parallelizes fix attempts.

## Core workflow

When a bug is reported, follow these steps in order:

### Phase 1: Reproduce and document

1. **Understand the bug** — Gather details about expected vs actual behavior
2. **Identify the test location** — Determine where tests live in the project (check for `tests/`, `__tests__/`, `spec/`, `*.test.*`, `*.spec.*` patterns)
3. **Write a failing test** — Create a test that demonstrates the bug

### Phase 2: Fix with subagents

4. **Launch fix subagents** — Use the Task tool with `subagent_type=general-purpose` to attempt fixes
5. **Run the test** — Verify the fix by running the specific test
6. **Iterate if needed** — If test still fails, launch additional subagents with new approaches

### Phase 3: Verify and complete

7. **Run full test suite** — Ensure no regressions were introduced
8. **Report success** — Confirm the bug is fixed with passing test as proof

## Writing the failing test

### Test naming convention

Name the test to describe the bug:

```python
# Python (pytest)
def test_user_login_fails_when_email_has_uppercase():
    ...

# Python (unittest)
def test_should_handle_empty_input_without_crashing(self):
    ...
```

```javascript
// JavaScript (Jest/Vitest)
it('should not crash when input array is empty', () => { ... });
test('handles special characters in username', () => { ... });
```

```typescript
// TypeScript
describe('UserService', () => {
  it('returns null when user not found instead of throwing', () => { ... });
});
```

### Test structure

Every bug reproduction test follows this pattern:

```python
def test_bug_description():
    # 1. ARRANGE - Set up the conditions that trigger the bug
    input_data = create_problematic_input()

    # 2. ACT - Perform the action that causes the bug
    result = function_under_test(input_data)

    # 3. ASSERT - Verify the expected (correct) behavior
    assert result == expected_value  # This should FAIL initially
```

### Finding the right test file

Check the project structure for existing test patterns:

```bash
# Find test files
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*.py" | head -20

# Find test directories
ls -la tests/ __tests__/ spec/ test/ 2>/dev/null

# Check package.json for test command
grep -A5 '"test"' package.json
```

## Launching fix subagents

Use the Task tool to parallelize fix attempts:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Fix [bug description]"
- prompt: Include:
  1. The bug description
  2. The failing test location and contents
  3. Suspected cause (if known)
  4. Constraint: "Run the test to verify your fix works"
```

### Parallel fix strategies

Launch multiple subagents with different approaches:

1. **Direct fix agent** — Focus on the immediate code causing the bug
2. **Root cause agent** — Investigate deeper architectural issues
3. **Edge case agent** — Look for similar bugs in related code

## When projects lack tests

If the project has no test infrastructure:

1. **Set up minimal test framework** first
2. **Create the test file** in a sensible location
3. **Document the test setup** for future use

### Quick test setup commands

```bash
# Python
pip install pytest
mkdir -p tests && touch tests/__init__.py

# JavaScript/TypeScript
npm install --save-dev jest
# or
npm install --save-dev vitest

# Go
# Tests are built-in, create *_test.go files
```

## Verifying the fix

After subagent reports completion:

```bash
# Run the specific test
pytest tests/test_module.py::test_bug_description -v
npm test -- --grep "bug description"
go test -run TestBugDescription -v

# Run full suite to check for regressions
pytest
npm test
go test ./...
```

## Example workflow

**User reports:** "The login function crashes when email has spaces"

**Phase 1 — Write failing test:**
```python
# tests/test_auth.py
def test_login_handles_email_with_spaces():
    """Bug: Login crashes when email contains spaces"""
    auth = AuthService()

    # This should return an error, not crash
    result = auth.login("user @example.com", "password")

    assert result.success == False
    assert "invalid email" in result.error.lower()
```

**Run test to confirm it fails:**
```bash
pytest tests/test_auth.py::test_login_handles_email_with_spaces -v
# Expected: FAILED (demonstrates the bug)
```

**Phase 2 — Launch subagent:**
```
Task tool:
- subagent_type: "general-purpose"
- description: "Fix email space crash"
- prompt: "Fix the login crash when email contains spaces.

  Bug: AuthService.login() crashes instead of returning error when email has spaces.

  Failing test: tests/test_auth.py::test_login_handles_email_with_spaces

  After fixing, run: pytest tests/test_auth.py::test_login_handles_email_with_spaces -v

  The test must pass to confirm the fix."
```

**Phase 3 — Verify:**
```bash
# Specific test passes
pytest tests/test_auth.py::test_login_handles_email_with_spaces -v
# PASSED

# No regressions
pytest tests/test_auth.py -v
# All tests pass
```

## Integration with hooks

The `bug-report-detector` hook in this plugin automatically:
1. Detects when a user reports a bug
2. Reminds Claude to follow the test-first workflow
3. Blocks Edit/Write tools until a test file has been created or modified

## Additional resources

### Reference files

- **`references/test-frameworks.md`** — Framework-specific test patterns
- **`references/common-bugs.md`** — Common bug patterns and test strategies

### Example files

- **`examples/python-bug-test.py`** — Python pytest example
- **`examples/js-bug-test.js`** — JavaScript Jest example

### Scripts

- **`scripts/find-tests.sh`** — Locate test infrastructure in a project
