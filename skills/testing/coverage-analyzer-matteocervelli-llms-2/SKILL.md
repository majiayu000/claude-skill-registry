---
name: coverage-analyzer
description: Analyze test coverage with detailed metrics, identify gaps, and generate
  comprehensive reports. Use when measuring code coverage, finding untested code,
  or validating coverage thresholds.
allowed-tools: Read, Bash, Grep, Glob
---

# Coverage Analyzer Skill

## Purpose

This skill provides comprehensive test coverage analysis, gap identification, threshold validation, and detailed reporting to ensure code quality and adequate test coverage across the codebase.

## When to Use

- Measuring test coverage for a module or project
- Identifying untested code and coverage gaps
- Validating coverage meets threshold (≥ 80%)
- Generating coverage reports for review
- Analyzing coverage trends over time
- Finding missing branch coverage

## Coverage Analysis Workflow

### 1. Basic Coverage Measurement

**Run Tests with Coverage:**
```bash
# Install pytest-cov if not installed
pip install pytest-cov

# Basic coverage measurement
pytest --cov=src tests/

# Coverage with terminal report
pytest --cov=src --cov-report=term tests/

# Coverage with missing lines
pytest --cov=src --cov-report=term-missing tests/

# Coverage for specific module
pytest --cov=src.tools.feature tests/
```

**Quick Coverage Check:**
```bash
# Show percentage only
pytest --cov=src --cov-report=term tests/ | grep TOTAL

# Check if coverage meets threshold
pytest --cov=src --cov-fail-under=80 tests/

# Quiet mode with coverage
pytest --cov=src --cov-report=term -q tests/
```

**Deliverable:** Basic coverage metrics

---

### 2. Detailed Coverage Analysis

**Generate Detailed Reports:**
```bash
# HTML coverage report (most detailed)
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html in browser

# XML coverage report (for CI/CD)
pytest --cov=src --cov-report=xml tests/

# JSON coverage report
pytest --cov=src --cov-report=json tests/

# Multiple report formats
pytest --cov=src \
  --cov-report=html \
  --cov-report=xml \
  --cov-report=term-missing \
  tests/
```

**Analyze Coverage by Module:**
```bash
# Show coverage for each file
pytest --cov=src --cov-report=term tests/

# Coverage with line numbers
pytest --cov=src --cov-report=term-missing tests/

# Annotated source files
pytest --cov=src --cov-report=annotate tests/
# Creates .py,cover files with coverage annotations
```

**Deliverable:** Detailed coverage reports

---

### 3. Coverage Gap Identification

**Find Untested Code:**
```bash
# Show missing lines
pytest --cov=src --cov-report=term-missing tests/

# Show missing branches
pytest --cov=src --cov-branch --cov-report=term-missing tests/

# Generate HTML report to visualize gaps
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html to see line-by-line coverage
```

**Identify Low Coverage Modules:**
```bash
# Run coverage and parse output
pytest --cov=src --cov-report=term tests/ | grep -v "100%"

# Find files below 80% coverage
pytest --cov=src --cov-report=term tests/ | awk '$NF ~ /%/ && $NF+0 < 80'

# Sort by coverage percentage
pytest --cov=src --cov-report=term tests/ | sort -k4 -n
```

**Analyze Coverage by Test Type:**
```bash
# Coverage from unit tests only
pytest --cov=src --cov-report=term tests/unit/

# Coverage from integration tests only
pytest --cov=src --cov-report=term tests/integration/

# Combined coverage
pytest --cov=src --cov-report=term tests/unit/ tests/integration/

# Incremental coverage (append mode)
pytest --cov=src --cov-append --cov-report=term tests/unit/
pytest --cov=src --cov-append --cov-report=term tests/integration/
```

**Deliverable:** Coverage gap analysis

---

### 4. Branch Coverage Analysis

**Measure Branch Coverage:**
```bash
# Enable branch coverage
pytest --cov=src --cov-branch --cov-report=term-missing tests/

# Branch coverage with HTML report
pytest --cov=src --cov-branch --cov-report=html tests/

# Show partial branches
pytest --cov=src --cov-branch --cov-report=term-missing tests/ | grep "!->"
```

**Analyze Conditional Coverage:**
```bash
# Find untested conditionals
pytest --cov=src --cov-branch --cov-report=term-missing tests/ | grep "if"

# Check switch/case coverage
pytest --cov=src --cov-branch --cov-report=term-missing tests/ | grep "case"
```

**Deliverable:** Branch coverage metrics

---

### 5. Coverage Threshold Validation

**Validate Minimum Coverage:**
```bash
# Fail if coverage below 80%
pytest --cov=src --cov-fail-under=80 tests/

# Fail if coverage below 90%
pytest --cov=src --cov-fail-under=90 tests/

# Check with specific threshold and report
pytest --cov=src --cov-fail-under=80 --cov-report=term-missing tests/
```

**Per-Module Thresholds:**
```bash
# Core logic: 90% minimum
pytest --cov=src.core --cov-fail-under=90 tests/

# Utilities: 85% minimum
pytest --cov=src.utils --cov-fail-under=85 tests/

# Interfaces: 80% minimum
pytest --cov=src.interfaces --cov-fail-under=80 tests/
```

**Deliverable:** Threshold validation report

---

### 6. Coverage Configuration

**Configure .coveragerc:**
```ini
# .coveragerc
[run]
source = src
omit =
    tests/*
    */__init__.py
    */venv/*
    */.venv/*
    */migrations/*

branch = True

[report]
exclude_lines =
    # Default pragmas
    pragma: no cover

    # Don't complain about missing debug-only code
    def __repr__
    def __str__

    # Don't complain if tests don't hit defensive assertion code
    raise AssertionError
    raise NotImplementedError

    # Don't complain if non-runnable code isn't run
    if __name__ == .__main__.:
    if TYPE_CHECKING:

    # Don't complain about abstract methods
    @abstractmethod

precision = 2
show_missing = True

[html]
directory = htmlcov

[xml]
output = coverage.xml
```

**Configure pyproject.toml:**
```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "tests/*",
    "*/__init__.py",
    "*/venv/*",
    "*/.venv/*",
]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]
precision = 2
show_missing = true
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

**Deliverable:** Coverage configuration

---

### 7. Coverage Reporting

**Generate Coverage Reports:**
```bash
# Terminal report
pytest --cov=src --cov-report=term tests/

# Terminal report with missing lines
pytest --cov=src --cov-report=term-missing tests/

# HTML report for detailed analysis
pytest --cov=src --cov-report=html tests/

# XML report for CI/CD integration
pytest --cov=src --cov-report=xml tests/

# JSON report for programmatic access
pytest --cov=src --cov-report=json tests/

# All reports
pytest --cov=src \
  --cov-report=term-missing \
  --cov-report=html \
  --cov-report=xml \
  --cov-report=json \
  tests/
```

**Coverage Summary Report:**
```markdown
# Coverage Report

## Overall Coverage: 87%

### By Module
| Module | Coverage | Missing Lines |
|--------|----------|---------------|
| src.core | 95% | 45-47, 89 |
| src.utils | 88% | 12-15, 67-70 |
| src.interfaces | 82% | 23, 56-58 |
| src.models | 100% | - |

### Critical Gaps
1. Error handling in `src.core.process()` (lines 45-47)
2. Edge case validation in `src.utils.validate()` (lines 67-70)
3. Exception paths in `src.interfaces.execute()` (lines 56-58)

### Recommendations
- Add tests for error conditions in core module
- Improve edge case coverage in utilities
- Test exception handling in interfaces

### Status
✅ Overall coverage: 87% (target: 80%)
✅ Core business logic: 95% (target: 90%)
✅ Utilities: 88% (target: 85%)
✅ All thresholds met
```

**Deliverable:** Comprehensive coverage reports

---

### 8. Coverage Trend Analysis

**Track Coverage Over Time:**
```bash
# Generate coverage badge
pip install coverage-badge
coverage-badge -o coverage.svg

# Save coverage history
pytest --cov=src --cov-report=json tests/
mv coverage.json coverage-$(date +%Y%m%d).json

# Compare coverage between runs
coverage json
python -c "import json; print(json.load(open('coverage.json'))['totals']['percent_covered'])"
```

**Coverage Diff:**
```bash
# Coverage for current branch
pytest --cov=src --cov-report=json tests/
cp coverage.json coverage-current.json

# Coverage for main branch
git checkout main
pytest --cov=src --cov-report=json tests/
cp coverage.json coverage-main.json

# Compare
diff <(jq '.totals.percent_covered' coverage-main.json) \
     <(jq '.totals.percent_covered' coverage-current.json)
```

**Deliverable:** Coverage trends and comparisons

---

## Coverage Analysis Patterns

### Quick Coverage Check

```bash
# Fast coverage check during development
pytest --cov=src --cov-report=term-missing -q tests/unit/
```

### Comprehensive Coverage Analysis

```bash
# Full coverage analysis with all reports
pytest --cov=src \
  --cov-branch \
  --cov-report=html \
  --cov-report=xml \
  --cov-report=term-missing \
  --cov-fail-under=80 \
  tests/
```

### CI/CD Coverage Check

```bash
# Coverage check for CI/CD pipeline
pytest --cov=src \
  --cov-report=xml \
  --cov-report=term \
  --cov-fail-under=80 \
  tests/
```

### Coverage Gap Investigation

```bash
# Find and analyze coverage gaps
pytest --cov=src --cov-report=html tests/
# Open htmlcov/index.html
# Click on files with low coverage
# Review highlighted untested lines
```

---

## Coverage Metrics and Thresholds

### Coverage Targets

**By Module Type:**
- Core Business Logic: ≥ 90%
- Services/APIs: ≥ 85%
- Utilities/Helpers: ≥ 85%
- Models/DTOs: ≥ 90%
- Interfaces/Contracts: ≥ 80%
- CLI/Main: ≥ 70%

**By Coverage Type:**
- Line Coverage: ≥ 80%
- Branch Coverage: ≥ 75%
- Function Coverage: ≥ 85%

**Overall Project:**
- Minimum: 80%
- Target: 85%
- Excellent: 90%+

### Acceptable Exclusions

```python
# Acceptable to exclude from coverage
def __repr__(self):  # pragma: no cover
    return f"Object({self.id})"

if __name__ == "__main__":  # pragma: no cover
    main()

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional

@abstractmethod
def interface_method(self):  # pragma: no cover
    pass

def debug_helper():  # pragma: no cover
    # Debug code not run in production
    pass
```

---

## Coverage Analysis Checklist

### Pre-Analysis
- [ ] Tests are running and passing
- [ ] pytest-cov installed
- [ ] Coverage configuration set (.coveragerc or pyproject.toml)
- [ ] Exclusions configured properly

### Analysis
- [ ] Line coverage calculated
- [ ] Branch coverage calculated
- [ ] Coverage by module analyzed
- [ ] Coverage gaps identified
- [ ] Critical gaps prioritized

### Threshold Validation
- [ ] Overall coverage ≥ 80%
- [ ] Core business logic ≥ 90%
- [ ] Utilities ≥ 85%
- [ ] No critical code untested
- [ ] Branch coverage ≥ 75%

### Reporting
- [ ] Terminal report generated
- [ ] HTML report generated (for detailed review)
- [ ] XML report generated (for CI/CD)
- [ ] Coverage summary documented
- [ ] Gaps documented with recommendations

---

## Common Coverage Commands

### Quick Reference

```bash
# Basic coverage
pytest --cov=src tests/

# Coverage with gaps
pytest --cov=src --cov-report=term-missing tests/

# Coverage with threshold
pytest --cov=src --cov-fail-under=80 tests/

# Branch coverage
pytest --cov=src --cov-branch --cov-report=term-missing tests/

# HTML report
pytest --cov=src --cov-report=html tests/

# Full analysis
pytest --cov=src \
  --cov-branch \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=80 \
  tests/
```

---

## Coverage Analysis Troubleshooting

### Coverage Tool Not Found

```bash
# Install pytest-cov
pip install pytest-cov

# Verify installation
pytest --version
pip show pytest-cov
```

### Incorrect Coverage (Too Low/High)

```bash
# Check source configuration
cat .coveragerc
cat pyproject.toml

# Verify source parameter
pytest --cov=src tests/  # Correct
pytest --cov tests/      # Wrong - testing test code

# Clear coverage cache
rm -rf .coverage htmlcov/
pytest --cov=src tests/
```

### Missing Files in Coverage

```bash
# Check omit configuration
grep -A5 "\[run\]" .coveragerc

# Verify files are imported
pytest --cov=src --cov-report=term tests/ | grep "filename"

# Check test imports
grep -r "^import\|^from" tests/
```

### Branch Coverage Not Working

```bash
# Enable branch coverage
pytest --cov=src --cov-branch tests/

# Check configuration
grep "branch" .coveragerc

# Verify branches exist
grep -r "if\|else\|elif" src/
```

---

## Integration with Test Runner Specialist

**Input:** Completed test execution with coverage enabled
**Process:** Analyze coverage, identify gaps, validate thresholds
**Output:** Coverage report with gap analysis and recommendations
**Next Step:** Report to test-runner-specialist for decision

---

## Coverage Analysis Best Practices

### Development
- Check coverage frequently during TDD
- Aim for >90% coverage on new code
- Review coverage reports locally
- Fix coverage gaps before committing

### Pre-Commit
- Verify coverage meets threshold
- Review coverage diff vs main branch
- Ensure new code is well tested
- Check branch coverage for complex logic

### CI/CD
- Generate coverage reports for every build
- Fail build if coverage below threshold
- Track coverage trends over time
- Archive coverage reports

### Review
- Focus on critical paths first
- Prioritize business logic coverage
- Don't chase 100% coverage unnecessarily
- Exclude unreachable code appropriately

---

## Coverage Gap Prioritization

### High Priority (Fix Immediately)
- Core business logic uncovered
- Error handling paths untested
- Security-critical code uncovered
- Data validation missing tests
- API endpoints without tests

### Medium Priority (Fix Soon)
- Utilities with <80% coverage
- Branch coverage gaps in logic
- Edge cases not tested
- Configuration parsing untested

### Low Priority (Fix When Possible)
- Representation methods (__repr__, __str__)
- Debug/logging code
- CLI help text
- Non-critical utilities

### Acceptable to Exclude
- Abstract methods
- TYPE_CHECKING blocks
- if __name__ == "__main__"
- Platform-specific code not running in CI
- Deprecated code scheduled for removal

---

## Supporting Resources

- **pytest-cov documentation**: https://pytest-cov.readthedocs.io
- **coverage.py documentation**: https://coverage.readthedocs.io
- **Coverage best practices**: https://testing.googleblog.com
- **Sample .coveragerc**: In project root

---

## Success Metrics

- [ ] Coverage calculated accurately
- [ ] Overall coverage ≥ 80%
- [ ] Critical code coverage ≥ 90%
- [ ] Coverage gaps identified
- [ ] Reports generated successfully
- [ ] Thresholds validated
- [ ] Recommendations provided