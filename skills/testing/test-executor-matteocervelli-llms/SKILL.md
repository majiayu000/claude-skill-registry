---
name: test-executor
description: Execute test suites with proper configuration, parallel execution, and
  detailed reporting. Use when running unit tests, integration tests, or full test
  suites.
allowed-tools: Read, Bash, Grep, Glob
---

# Test Executor Skill

## Purpose

This skill provides systematic test execution capabilities across different test types (unit, integration, e2e) with proper configuration, parallel execution, test filtering, and comprehensive reporting.

## When to Use

- Running unit tests for a module or feature
- Executing integration tests with external dependencies
- Running full test suite before commit/PR
- Debugging failing tests with verbose output
- Checking test execution time and performance
- Running tests in different environments (dev, CI/CD)

## Test Execution Workflow

### 1. Test Discovery and Planning

**Identify Test Scope:**
```bash
# Discover all test files
pytest --collect-only

# Count tests by directory
pytest --collect-only tests/unit/
pytest --collect-only tests/integration/
pytest --collect-only tests/e2e/

# Show test structure
pytest --collect-only -q
```

**Analyze Test Organization:**
```bash
# List all test files
find tests/ -name "test_*.py" -o -name "*_test.py"

# Count tests by type
ls tests/unit/test_*.py | wc -l
ls tests/integration/test_*.py | wc -l

# Check for test markers
grep -r "@pytest.mark" tests/
```

**Deliverable:** Test inventory and execution plan

---

### 2. Unit Test Execution

**Run All Unit Tests:**
```bash
# Basic execution
pytest tests/unit/

# Verbose output with test names
pytest tests/unit/ -v

# Extra verbose with test details
pytest tests/unit/ -vv

# Show print statements
pytest tests/unit/ -s

# Fail fast (stop on first failure)
pytest tests/unit/ -x

# Run last failed tests only
pytest tests/unit/ --lf
```

**Run Specific Tests:**
```bash
# Run specific test file
pytest tests/unit/test_feature.py

# Run specific test function
pytest tests/unit/test_feature.py::test_function_name

# Run specific test class
pytest tests/unit/test_feature.py::TestClassName

# Run specific test method
pytest tests/unit/test_feature.py::TestClassName::test_method_name

# Run tests matching pattern
pytest tests/unit/ -k "test_create"
pytest tests/unit/ -k "test_create or test_update"
pytest tests/unit/ -k "not slow"
```

**Run with Markers:**
```bash
# Run only fast tests
pytest tests/unit/ -m "not slow"

# Run only smoke tests
pytest tests/unit/ -m "smoke"

# Run tests with multiple markers
pytest tests/unit/ -m "smoke and not slow"

# List available markers
pytest --markers
```

**Deliverable:** Unit test execution results

---

### 3. Integration Test Execution

**Run Integration Tests:**
```bash
# Run all integration tests
pytest tests/integration/ -v

# Run with longer timeout for external services
pytest tests/integration/ --timeout=300

# Run with specific environment
ENV=test pytest tests/integration/

# Skip slow integration tests
pytest tests/integration/ -m "not slow"
```

**Run with Database/Services:**
```bash
# Run with test database
pytest tests/integration/ --db-url=sqlite:///test.db

# Run with Docker containers (if using testcontainers)
pytest tests/integration/ --with-docker

# Run with mocked external services
pytest tests/integration/ --mock-external

# Run with real external services
pytest tests/integration/ --real-services
```

**Deliverable:** Integration test results

---

### 4. End-to-End Test Execution

**Run E2E Tests:**
```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run with specific browser (if web app)
pytest tests/e2e/ --browser=chrome
pytest tests/e2e/ --browser=firefox

# Run headless
pytest tests/e2e/ --headless

# Run with screenshots on failure
pytest tests/e2e/ --screenshot-on-failure
```

**Deliverable:** E2E test results

---

### 5. Parallel Test Execution

**Run Tests in Parallel:**
```bash
# Install pytest-xdist if not installed
pip install pytest-xdist

# Run with auto CPU detection
pytest tests/unit/ -n auto

# Run with specific number of workers
pytest tests/unit/ -n 4

# Run with load balancing
pytest tests/unit/ -n auto --dist=loadscope

# Run with worksteal for uneven test distribution
pytest tests/unit/ -n auto --dist=worksteal
```

**Performance Optimization:**
```bash
# Show slowest tests
pytest tests/unit/ --durations=10

# Show slowest 20 tests
pytest tests/unit/ --durations=20

# Profile test execution
pytest tests/unit/ --profile

# Run with timing
time pytest tests/unit/
```

**Deliverable:** Parallel execution metrics

---

### 6. Test Debugging

**Debug Failing Tests:**
```bash
# Show full diff on assertion failures
pytest tests/unit/ -vv

# Drop into debugger on failure
pytest tests/unit/ --pdb

# Drop into debugger on first failure
pytest tests/unit/ -x --pdb

# Show local variables in traceback
pytest tests/unit/ -l

# Show captured output on failure
pytest tests/unit/ --tb=short
pytest tests/unit/ --tb=long
pytest tests/unit/ --tb=native
```

**Rerun Failed Tests:**
```bash
# Rerun last failed tests
pytest tests/unit/ --lf

# Run failed first, then others
pytest tests/unit/ --ff

# Rerun failed tests with more verbosity
pytest tests/unit/ --lf -vv

# Clear cache and rerun
pytest tests/unit/ --cache-clear
```

**Deliverable:** Debug output and failure analysis

---

### 7. Test Reporting

**Generate Test Reports:**
```bash
# Generate JUnit XML report (for CI/CD)
pytest tests/ --junitxml=reports/junit.xml

# Generate HTML report
pip install pytest-html
pytest tests/ --html=reports/report.html --self-contained-html

# Generate JSON report
pip install pytest-json-report
pytest tests/ --json-report --json-report-file=reports/report.json

# Generate multiple reports
pytest tests/ \
  --junitxml=reports/junit.xml \
  --html=reports/report.html \
  --self-contained-html
```

**Test Summary:**
```bash
# Short summary
pytest tests/ -q

# Summary with reasons for skipped/failed tests
pytest tests/ -ra

# Summary for passed tests
pytest tests/ -rP

# Summary for failed tests
pytest tests/ -rf

# Summary for errors
pytest tests/ -rE

# Summary for all
pytest tests/ -rA
```

**Deliverable:** Test reports in multiple formats

---

### 8. CI/CD Integration

**Run Tests in CI/CD Pipeline:**
```bash
# Standard CI test run
pytest tests/ \
  --junitxml=reports/junit.xml \
  --cov=src \
  --cov-report=xml \
  --cov-report=html \
  -v

# With strict markers (fail on unknown markers)
pytest tests/ --strict-markers

# With warnings as errors
pytest tests/ -W error

# With maximum verbosity for CI logs
pytest tests/ -vv --tb=short
```

**GitHub Actions Example:**
```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    pytest tests/ \
      --junitxml=reports/junit.xml \
      --cov=src \
      --cov-report=xml \
      --cov-fail-under=80 \
      -v
```

**Deliverable:** CI/CD-ready test execution

---

## Test Execution Patterns

### Full Test Suite

```bash
# Complete test run with all checks
pytest tests/ \
  -v \
  --cov=src \
  --cov-report=html \
  --cov-report=term-missing \
  --junitxml=reports/junit.xml \
  --html=reports/report.html \
  --self-contained-html
```

### Fast Feedback Loop

```bash
# Quick tests for development
pytest tests/unit/ \
  -x \
  --ff \
  --tb=short \
  -q
```

### Pre-Commit Tests

```bash
# Run before committing changes
pytest tests/unit/ tests/integration/ \
  -v \
  --cov=src \
  --cov-fail-under=80
```

### Nightly/Comprehensive Tests

```bash
# Full test suite including slow tests
pytest tests/ \
  -v \
  --cov=src \
  --cov-report=html \
  --durations=20 \
  --junitxml=reports/junit.xml
```

---

## Test Configuration

### pytest.ini Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
    smoke: marks tests as smoke tests

# Options
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings

# Coverage
[coverage:run]
source = src
omit = tests/*,*/__init__.py

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### pyproject.toml Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "e2e: marks end-to-end tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

---

## Test Execution Checklist

### Pre-Execution
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Test database/services running (if needed)
- [ ] Environment variables set
- [ ] Previous test artifacts cleaned

### Execution
- [ ] Unit tests running and passing
- [ ] Integration tests running and passing
- [ ] E2E tests running and passing (if applicable)
- [ ] No skipped tests (or justified)
- [ ] No flaky tests detected

### Post-Execution
- [ ] All tests passed
- [ ] Test reports generated
- [ ] Coverage calculated (separate skill)
- [ ] Performance metrics captured
- [ ] Cleanup completed

---

## Common Test Execution Commands

### Quick Reference

```bash
# Fast unit tests
pytest tests/unit/ -x --ff -q

# All tests with coverage
pytest tests/ --cov=src --cov-report=term-missing

# CI/CD full run
pytest tests/ \
  --junitxml=reports/junit.xml \
  --cov=src \
  --cov-report=xml \
  --cov-fail-under=80 \
  -v

# Debug specific test
pytest tests/unit/test_feature.py::test_function -vv --pdb

# Parallel execution
pytest tests/unit/ -n auto

# Performance analysis
pytest tests/ --durations=10

# Rerun failures
pytest tests/ --lf -vv
```

---

## Test Execution Troubleshooting

### Tests Not Found

```bash
# Check test discovery
pytest --collect-only

# Verify pytest.ini configuration
cat pytest.ini

# Check file naming
ls tests/test_*.py
```

### Import Errors

```bash
# Check PYTHONPATH
echo $PYTHONPATH

# Install package in development mode
pip install -e .

# Verify imports
python -c "import src.module"
```

### Slow Tests

```bash
# Identify slow tests
pytest tests/ --durations=20

# Run in parallel
pytest tests/ -n auto

# Skip slow tests during development
pytest tests/ -m "not slow"
```

### Flaky Tests

```bash
# Run tests multiple times
for i in {1..10}; do pytest tests/ || break; done

# Run in random order
pip install pytest-randomly
pytest tests/ --randomly-seed=1234

# Use pytest-rerunfailures
pip install pytest-rerunfailures
pytest tests/ --reruns 3
```

---

## Integration with Test Runner Specialist

**Input:** Test execution request from specialist agent
**Process:** Execute tests with appropriate configuration
**Output:** Test results, execution logs, and metrics
**Next Step:** Coverage analysis by coverage-analyzer skill

---

## Test Execution Best Practices

### Development
- Run unit tests frequently (every few minutes)
- Use `-x --ff` for fast feedback
- Focus on relevant tests with `-k` pattern matching
- Keep unit tests fast (< 1 minute total)

### Pre-Commit
- Run unit and integration tests
- Verify coverage meets threshold
- Check for flaky tests
- Ensure all tests pass

### CI/CD
- Run full test suite
- Generate reports for tracking
- Fail on coverage below threshold
- Run tests in parallel for speed
- Archive test artifacts

### Debugging
- Use `-vv` for detailed output
- Use `--pdb` to drop into debugger
- Use `-l` to show local variables
- Run single test in isolation

---

## Supporting Resources

- **pytest documentation**: https://docs.pytest.org
- **pytest-cov**: Coverage plugin
- **pytest-xdist**: Parallel execution plugin
- **pytest-html**: HTML report generation

---

## Success Metrics

- [ ] All tests discovered and executed
- [ ] Test execution time acceptable (unit < 1 min, full < 10 min)
- [ ] Test reports generated successfully
- [ ] No flaky tests detected
- [ ] Tests pass consistently
- [ ] Performance metrics captured