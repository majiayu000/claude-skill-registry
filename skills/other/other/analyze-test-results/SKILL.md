---
name: analyze-test-results
description: Analyze test failures and CI artifacts to identify and fix bugs
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
context: auto
---

# Analyze Test Results Skill

Analyze test results from CI or local runs to identify failures, diagnose root causes, and fix bugs.

## When to Use

- After tests fail (CI or local)
- After running `/download-ci-artifacts`
- When asked to "fix test failures"
- When asked to "analyze test results"

## Workflow

### 1. Locate Test Results

```bash
# From CI artifacts
cat ci-artifacts/test-report/test-report.md

# From local run
uv run pytest MouseMaster/Testing/Python/ -v --tb=long 2>&1 | tee test-output.log
```

### 2. Parse JUnit XML (if available)

```bash
# Extract failed tests from XML
grep -E "(failure|error)" ci-artifacts/unit/unit-tests.xml | head -20
```

### 3. For Each Failure

#### a. Identify the failing test

```
FAILED MouseMaster/Testing/Python/test_event_handler.py::TestClass::test_name
```

#### b. Read the test file

Understand what the test expects:
- What behavior is being tested?
- What are the assertions?
- What mocks are set up?

#### c. Read the implementation

Find the code being tested and understand:
- Current behavior
- Why it might fail
- Edge cases

#### d. Diagnose root cause

Common issues:
- **Mock not configured**: Check mock setup in test
- **API changed**: Update test or implementation
- **Race condition**: Add proper synchronization
- **Missing dependency**: Check imports and fixtures

### 4. Fix the Issue

Apply the minimal fix needed:

```python
# If test expectation is wrong
# → Update the test

# If implementation is wrong
# → Fix the implementation, re-run tests

# If mock setup is incomplete
# → Add proper mock configuration
```

### 5. Verify Fix

```bash
# Run specific failing test
uv run pytest MouseMaster/Testing/Python/test_file.py::TestClass::test_name -v

# Run full suite
uv run pytest MouseMaster/Testing/Python/ -v
```

## Analyzing Slicer Test Failures

### Read Slicer output log

```bash
cat ci-artifacts/slicer/slicer-output.log
```

### Common Slicer issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Extension not loaded | Check module paths |
| `AttributeError: 'NoneType'` | Widget not ready | Add processEvents() |
| `RuntimeError: widget deleted` | View closed | Check object lifetime |
| `Qt assertion` | Invalid UI operation | Run on main thread |

### Screenshot analysis

If screenshots captured, review with:

```bash
# View manifest
cat ci-artifacts/screenshots/manifest.json

# Then use /review-ui-screenshots skill
```

## Decision Rules

### Fix immediately
- Clear implementation bugs
- Missing mock configuration
- Import errors
- Typos

### Investigate more
- Intermittent failures
- Platform-specific issues
- Complex logic errors

### Report only
- Test infrastructure issues
- CI configuration problems
- External dependency failures

## Report Format

After analysis:

```markdown
## Test Analysis Report

### Failures Found
| Test | Error | Root Cause |
|------|-------|------------|
| test_name | AssertionError | Incorrect mock setup |

### Fixes Applied
- `file.py:123` - Fixed mock configuration
- `test.py:45` - Updated assertion

### Remaining Issues
- Issue requiring further investigation

### Verification
- [ ] All tests pass locally
- [ ] Lint passes
- [ ] Type check passes
```

## Integration

After fixing:

1. Run `/run-tests` to verify
2. Commit with `fix: description of fix`
3. Push to trigger CI

## Related Skills

- `/download-ci-artifacts` - Get artifacts first
- `/review-ui-screenshots` - Analyze UI issues
- `/fix-bad-practices` - Fix code quality issues
