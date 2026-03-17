---
name: ln-782-test-runner
description: Executes all test suites and reports results with coverage
---

# ln-782-test-runner

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-780-bootstrap-verifier

---

## Purpose

Detects test frameworks, executes all test suites, and reports results including pass/fail counts and optional coverage.

**Scope:**
- Auto-detect test frameworks from project configuration
- Execute test suites for all detected frameworks
- Parse test output for pass/fail counts
- Generate coverage reports when enabled

**Out of Scope:**
- Building projects (handled by ln-781)
- Container operations (handled by ln-783)
- Writing or fixing tests

---

## When to Use

| Scenario | Use This Skill |
|----------|---------------|
| Called by ln-780 orchestrator | Yes |
| Standalone test execution | Yes |
| CI/CD pipeline test step | Yes |
| Build verification needed | No, use ln-781 |

---

## Workflow

### Step 1: Detect Test Frameworks

Identify test frameworks from project configuration files.

| Marker | Test Framework | Project Type |
|--------|---------------|--------------|
| vitest.config.* | Vitest | Node.js |
| jest.config.* | Jest | Node.js |
| *.test.ts in package.json | Vitest/Jest | Node.js |
| xunit / nunit in *.csproj | xUnit/NUnit | .NET |
| pytest.ini / conftest.py | pytest | Python |
| *_test.go files | go test | Go |
| tests/ with Cargo.toml | cargo test | Rust |

### Step 2: Execute Test Suites

Run tests for each detected framework.

| Framework | Execution Strategy |
|-----------|-------------------|
| Vitest | Run in single-run mode with JSON reporter |
| Jest | Run with JSON output |
| xUnit/NUnit | Run with logger for structured output |
| pytest | Run with JSON plugin or verbose output |
| go test | Run with JSON output flag |
| cargo test | Run with standard output parsing |

### Step 3: Parse Results

Extract test results from framework output.

| Metric | Description |
|--------|-------------|
| total | Total number of tests discovered |
| passed | Tests that completed successfully |
| failed | Tests that failed assertions |
| skipped | Tests marked as skip/ignore |
| duration | Total execution time |

### Step 4: Generate Coverage (Optional)

When coverage enabled, collect coverage metrics.

| Framework | Coverage Tool |
|-----------|--------------|
| Vitest/Jest | c8 / istanbul |
| .NET | coverlet |
| pytest | pytest-cov |
| Go | go test -cover |
| Rust | cargo-tarpaulin |

**Coverage Metrics:**
| Metric | Description |
|--------|-------------|
| linesCovered | Lines executed during tests |
| linesTotal | Total lines in codebase |
| percentage | Coverage percentage |

### Step 5: Report Results

Return structured results to orchestrator.

**Result Structure:**

| Field | Description |
|-------|-------------|
| suiteName | Test suite identifier |
| framework | Detected test framework |
| status | passed / failed / error |
| total | Total test count |
| passed | Passed test count |
| failed | Failed test count |
| skipped | Skipped test count |
| duration | Execution time in seconds |
| failures | Array of failure details (test name, message) |
| coverage | Coverage metrics (if enabled) |

---

## Error Handling

| Error Type | Action |
|------------|--------|
| No tests found | Report warning, status = passed (0 tests) |
| Test timeout | Report timeout, include partial results |
| Framework error | Log error, report as error status |
| Missing dependencies | Report missing test dependencies |

---

## Options

| Option | Default | Description |
|--------|---------|-------------|
| skipTests | false | Skip execution if no tests found |
| allowFailures | false | Report success even if tests fail |
| coverage | false | Generate coverage report |
| timeout | 300 | Max execution time in seconds |
| parallel | true | Run test suites in parallel when possible |

---

## Critical Rules

1. **Run all detected test suites** - do not skip suites silently
2. **Parse actual results** - do not rely only on exit code
3. **Include failure details** - provide actionable information for debugging
4. **Respect timeout** - prevent hanging on infinite loops

---

## Definition of Done

- [ ] All test frameworks detected
- [ ] All test suites executed
- [ ] Results parsed and structured
- [ ] Coverage collected (if enabled)
- [ ] Results returned to orchestrator

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
