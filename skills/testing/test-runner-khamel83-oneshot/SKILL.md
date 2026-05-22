---
name: test-runner
description: "Run tests, analyze results, and improve coverage. Supports pytest, jest, go test, and cargo test. Use when user says 'run tests', 'test', 'coverage', 'pytest', 'jest', or asks about test results."
allowed-tools: Bash, Read, Write, Edit
---

# Test Runner

You are an expert at running tests and analyzing results.

## When To Use

- User says "Run tests", "Check if tests pass"
- User asks "What's the coverage?"
- Before commits or PRs
- After implementing a feature

## Inputs

- Test framework in use (pytest, jest, go test, etc.)
- Optional: specific test files or patterns

## Outputs

- Test results summary
- Coverage report (if requested)
- List of failing tests with analysis

## Workflow

### 1. Detect Test Framework

```
pytest.ini / pyproject.toml → pytest
package.json with jest → jest
*_test.go → go test
Cargo.toml → cargo test
```

### 2. Run Tests

```bash
# Python
pytest -v --tb=short

# Node
npm test

# Go
go test ./...

# Rust
cargo test
```

### 3. Analyze Failures

For each failure:
- File
- Test name
- Assertion
- Expected vs actual

Categorize:
- Logic error
- Missing mock
- Flaky test
- Environment issue

### 4. Coverage (if requested)

```bash
# Python
pytest --cov=src --cov-report=term-missing

# Node
npm test -- --coverage

# Go
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

### 5. Report

```markdown
## Test Results

**Total**: X passed, Y failed, Z skipped
**Coverage**: X% (target: 80%)

### Failing Tests
1. `test_name` - [reason]
2. `test_name` - [reason]

### Coverage Gaps
- `module.py` - lines 45-50 not covered
```

## Test Commands by Framework

### Python (pytest)

```bash
# Run all tests
pytest

# Verbose with short traceback
pytest -v --tb=short

# Run specific file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login

# With coverage
pytest --cov=src --cov-report=term-missing

# Stop on first failure
pytest -x

# Run failed tests from last run
pytest --lf
```

### Node (jest)

```bash
# Run all tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test -- auth.test.js
```

### Go

```bash
# Run all tests
go test ./...

# Verbose
go test -v ./...

# Coverage
go test -coverprofile=coverage.out ./...

# Specific package
go test ./pkg/auth
```

### Rust

```bash
# Run all tests
cargo test

# Specific test
cargo test test_name

# Show output
cargo test -- --nocapture
```

## Test Quality Guidelines

### Good Tests

- Test behavior, not implementation
- One assertion per test (when possible)
- Clear test names
- Isolated (no shared state)
- Fast (mock external services)

### Coverage Targets

| Type | Target |
|------|--------|
| Unit tests | 80%+ |
| Integration | Key paths |
| E2E | Critical flows |

## Anti-Patterns

- Ignoring flaky tests
- Deleting failing tests instead of fixing them
- Testing implementation details instead of behavior
- No tests for bug fixes (write test first)
- Over-mocking (test too far from reality)

## Keywords

test, tests, pytest, jest, coverage, run tests, test results, failing tests
