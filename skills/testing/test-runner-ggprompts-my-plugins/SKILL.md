---
name: test-runner
description: "Test runner checkpoint for conductor gates. Detects test framework (jest, pytest, cargo test, go test, etc.), runs tests, and captures output. Returns structured result with pass/fail status and failed test details."
user-invocable: true
---

# Test Runner Checkpoint

Test execution checkpoint that auto-detects the project's test framework and runs tests.

## What This Skill Does

1. Detects test framework from project files
2. Runs appropriate test command
3. Parses test output for results
4. Writes result to checkpoint file

## Workflow

### Step 1: Detect Test Framework

Check for test framework indicators:

```bash
# Node.js projects
ls package.json 2>/dev/null && cat package.json | grep -E '"test"|"jest"|"vitest"|"mocha"'

# Python projects
ls pytest.ini pyproject.toml setup.py requirements.txt 2>/dev/null

# Rust projects
ls Cargo.toml 2>/dev/null

# Go projects
ls go.mod 2>/dev/null

# General
ls Makefile 2>/dev/null && grep -E "^test:" Makefile
```

**Framework Detection Priority:**

| Indicator | Framework | Command |
|-----------|-----------|---------|
| `package.json` with "test" script | npm | `npm test` |
| `package.json` with vitest | vitest | `npm test` or `npx vitest` |
| `package.json` with jest | jest | `npm test` or `npx jest` |
| `pytest.ini` or `conftest.py` | pytest | `pytest` |
| `pyproject.toml` with pytest | pytest | `pytest` |
| `Cargo.toml` | cargo | `cargo test` |
| `go.mod` | go | `go test ./...` |
| `Makefile` with test target | make | `make test` |

### Step 2: Run Tests

Execute the detected test command and capture output:

```bash
# Example for npm
npm test 2>&1 | tee /tmp/test-output.txt
TEST_EXIT_CODE=${PIPESTATUS[0]}
echo "Exit code: $TEST_EXIT_CODE"

# Example for pytest
pytest --tb=short 2>&1 | tee /tmp/test-output.txt
TEST_EXIT_CODE=${PIPESTATUS[0]}

# Example for cargo
cargo test 2>&1 | tee /tmp/test-output.txt
TEST_EXIT_CODE=${PIPESTATUS[0]}
```

### Step 3: Parse Test Output

Extract test results from output. Common patterns:

**Jest/Vitest:**
```
Tests:       3 failed, 12 passed, 15 total
```

**Pytest:**
```
====== 2 failed, 10 passed in 1.23s ======
```

**Cargo:**
```
test result: FAILED. 8 passed; 2 failed; 0 ignored
```

**Go:**
```
FAIL    mypackage       0.123s
```

### Step 4: Create Structured Result

```json
{
  "checkpoint": "test-runner",
  "timestamp": "2026-01-19T12:00:00Z",
  "passed": false,
  "framework": "jest",
  "command": "npm test",
  "exit_code": 1,
  "summary_line": "Tests: 2 failed, 15 passed, 17 total",
  "failed_tests": [
    {
      "name": "UserService.login should validate credentials",
      "file": "src/services/user.test.ts",
      "error": "Expected 200 but got 401"
    }
  ],
  "stats": {
    "total": 17,
    "passed": 15,
    "failed": 2,
    "skipped": 0
  },
  "output": "[truncated test output...]"
}
```

**Result Fields:**
- `passed`: true if all tests pass (exit code 0)
- `framework`: detected test framework
- `command`: exact command that was run
- `exit_code`: process exit code
- `failed_tests`: array of `{name, file?, error?}` for each failure
- `stats`: test count statistics
- `output`: raw output (truncated if very long)

### Step 5: Write Checkpoint File

```bash
mkdir -p .checkpoints
cat > .checkpoints/test-runner.json << 'EOF'
{
  "checkpoint": "test-runner",
  ...
}
EOF
```

## Decision Criteria

**Pass if:**
- All tests pass (exit code 0)
- Test output shows 0 failures

**Fail if:**
- Any test fails
- Tests fail to run (syntax error, missing deps)
- Test command not found

## Special Cases

### No Tests Found

If no test framework detected:

```json
{
  "passed": true,
  "framework": "none",
  "summary": "No test framework detected - skipping"
}
```

This counts as pass (can't fail tests that don't exist).

### Tests Timeout

Set reasonable timeout (5 minutes default):

```bash
timeout 300 npm test 2>&1 | tee /tmp/test-output.txt
```

If timeout:
```json
{
  "passed": false,
  "error": "Tests timed out after 300 seconds"
}
```

### Flaky Tests

If tests fail intermittently, note in output but still fail:
```json
{
  "passed": false,
  "note": "This test may be flaky - consider retry"
}
```

## Example Usage

When invoked as `/test-runner`:

```
Running Test Runner checkpoint...

Detecting test framework...
Found package.json with "test" script using Jest.

Running: npm test
[test output streams...]

Parsing results...
Tests: 2 failed, 15 passed, 17 total

Failed tests:
1. UserService.login should validate credentials
   File: src/services/user.test.ts
   Error: Expected 200 but got 401

2. API.fetchData should handle timeout
   File: src/api/fetch.test.ts
   Error: Timeout exceeded

Result:
{
  "passed": false,
  "framework": "jest",
  "failed_tests": [...],
  "stats": {"total": 17, "passed": 15, "failed": 2}
}

Checkpoint result written to .checkpoints/test-runner.json
```

## Framework-Specific Notes

### Jest/Vitest
- Use `--json` flag for machine-readable output if parsing is complex
- `npx jest --json --outputFile=/tmp/jest-results.json`

### Pytest
- Use `--tb=short` for concise tracebacks
- `pytest --json-report --json-report-file=/tmp/pytest.json` if plugin available

### Cargo
- `cargo test -- --format=json` for JSON output (nightly)
- Standard output parsing works for stable

### Go
- `go test -json ./...` for JSON output
- Parse per-line JSON for test events
