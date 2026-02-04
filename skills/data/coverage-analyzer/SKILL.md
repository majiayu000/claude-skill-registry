---
name: coverage-analyzer
description: Advanced coverage analysis with actionable insights. Use to identify coverage gaps, suggest specific tests, track coverage trends, and highlight critical uncovered code. Essential for reaching 80%+ coverage target.
---

# Coverage Analyzer

## ⚠️ MANDATORY: Read Project Documentation First

**BEFORE starting coverage analysis, you MUST read and understand the following project documentation:**

### Core Project Documentation

1. **README.md** - Project overview, features, and getting started
2. **AI_DOCS/project-context.md** - Tech stack, architecture, development workflow
3. **AI_DOCS/code-conventions.md** - Code style, formatting, best practices
4. **AI_DOCS/tdd-workflow.md** - TDD process, testing standards, coverage requirements

### Session Context (if available)

5. **.ai-context/ACTIVE_TASKS.md** - Current tasks and priorities
6. **.ai-context/CONVENTIONS.md** - Project-specific conventions
7. **.ai-context/RECENT_DECISIONS.md** - Recent architectural decisions
8. **.ai-context/LAST_SESSION_SUMMARY.md** - Previous session summary

### Additional AI Documentation

9. **AI_DOCS/ai-tools.md** - Session management workflow
10. **AI_DOCS/ai-skills.md** - Other specialized skills/agents available

### Why This Matters

- **Coverage Requirements**: Understand project-specific coverage thresholds (80%+ minimum)
- **Testing Patterns**: Follow established testing conventions when suggesting tests
- **Code Context**: Understand module structure and dependencies
- **Recent Changes**: Be aware of recent test additions or coverage improvements

**After reading these files, proceed with your coverage analysis task below.**

---

## Overview

Provide advanced test coverage analysis with actionable insights for improving coverage to meet the 80%+ requirement.

## When to Use

- After running `make coverage` to understand gaps
- Before completing a feature (ensure adequate coverage)
- When coverage is below 80% target
- To identify critical uncovered code paths
- For tracking coverage trends over time

## What This Skill Provides

✅ **Detailed Coverage Analysis**
- Current coverage percentage
- Uncovered lines by file
- Missing branches

✅ **Actionable Recommendations**
- Specific tests to write
- Code locations needing tests
- Priority of coverage gaps

✅ **Coverage Gaps Identification**
- Critical uncovered paths (error handling)
- Edge cases not tested
- Integration points missing tests

✅ **Test Suggestions**
- Concrete test code recommendations
- Parametrized test suggestions
- Fixture recommendations

✅ **Trend Tracking**
- Coverage history over time
- Improvement/regression detection
- Progress toward 80%+ goal

## Usage Examples

### Analyze Current Coverage

```bash
# Generate detailed coverage analysis
analyze test coverage
```

**Output:** Comprehensive report with gaps and recommendations

### Find Critical Gaps

```bash
# Focus on critical uncovered code
show critical coverage gaps
```

**Output:** High-priority uncovered code (error handling, security, edge cases)

### Get Test Suggestions

```bash
# Get specific test recommendations
suggest tests for uncovered code in src/python_modern_template/validators.py
```

**Output:** Concrete test cases to add

### Track Coverage Trends

```bash
# See coverage over time
show coverage trend for last month
```

**Output:** Graph showing coverage changes

## Step-by-Step Analysis Process

### Step 1: Run Coverage

```bash
# Generate coverage report
make coverage
```

This creates:
- Terminal output with overall percentage
- HTML report in `htmlcov/`
- `.coverage` data file

### Step 2: Parse Coverage Data

Read coverage data from multiple sources:

```bash
# Read terminal output for overall stats
# Read htmlcov/index.html for detailed breakdown
# Parse .coverage file for line-by-line data
```

### Step 3: Identify Uncovered Lines

For each source file:
- List uncovered line numbers
- Group by type (functions, error handling, edge cases)
- Prioritize by criticality

### Step 4: Analyze Context

For each uncovered section:
- Read surrounding code
- Understand what the code does
- Identify why it's not covered
- Determine appropriate test type

### Step 5: Generate Recommendations

Create specific test suggestions:
- Test function name
- Test scenario
- Example test code
- Parameters to test

### Step 6: Calculate Priority

**CRITICAL** - Must cover immediately:
- Error handling paths
- Security-related code
- Data validation
- Authorization checks

**HIGH** - Should cover soon:
- Edge cases
- Boundary conditions
- Integration points
- Public API functions

**MEDIUM** - Good to cover:
- Internal helper functions
- Logging statements
- Configuration parsing

**LOW** - Optional:
- Debug code
- Development-only paths
- Deprecated functions

## Analysis Report Format

```markdown
# Test Coverage Analysis

## Executive Summary

**Current Coverage:** 75.3%
**Target:** 80%+
**Gap:** 4.7% (23 uncovered lines)
**Status:** ⚠️ Below target

**Breakdown:**
- src/python_modern_template/: 73.2% (18 uncovered lines)
- tests/: 100% (fully covered)

---

## Critical Gaps (MUST FIX)

### 1. Error Handling in validators.py ⚠️ CRITICAL

**File:** src/python_modern_template/validators.py
**Lines:** 45-52 (8 lines)
**Function:** `validate_email()`

**Uncovered Code:**
```python
45: except ValueError as e:
46:     logger.error(f"Email validation failed: {e}")
47:     raise ValidationError(
48:         "Invalid email format"
49:     ) from e
50: except Exception:
51:     logger.critical("Unexpected validation error")
52:     return False
```

**Why Critical:** Error handling paths are not tested, could hide bugs

**Recommended Test:**
```python
def test_validate_email_value_error_handling() -> None:
    """Test email validation handles ValueError correctly."""
    # Arrange
    invalid_email = "not-an-email"

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        validate_email(invalid_email)

    assert "Invalid email format" in str(exc_info.value)
    assert exc_info.value.__cause__ is not None

def test_validate_email_unexpected_error_handling() -> None:
    """Test email validation handles unexpected errors."""
    # Arrange
    # Mock to raise unexpected exception
    with patch('validators.EMAIL_REGEX.match', side_effect=RuntimeError("Unexpected")):
        # Act
        result = validate_email("test@example.com")

        # Assert
        assert result is False
```

**Impact:** Covers 8 lines, adds 3.5% coverage

---

### 2. Edge Case in parser.py ⚠️ CRITICAL

**File:** src/python_modern_template/parser.py
**Lines:** 67-70 (4 lines)
**Function:** `parse_config()`

**Uncovered Code:**
```python
67: if not config_data:
68:     logger.warning("Empty configuration provided")
69:     return DEFAULT_CONFIG
70:     # Unreachable line removed
```

**Why Critical:** Edge case handling not tested

**Recommended Test:**
```python
def test_parse_config_empty_data() -> None:
    """Test parser handles empty configuration."""
    # Arrange
    empty_config = {}

    # Act
    result = parse_config(empty_config)

    # Assert
    assert result == DEFAULT_CONFIG

def test_parse_config_none_data() -> None:
    """Test parser handles None configuration."""
    # Arrange
    # Act
    result = parse_config(None)

    # Assert
    assert result == DEFAULT_CONFIG
```

**Impact:** Covers 4 lines, adds 1.7% coverage

---

## High Priority Gaps

### 3. Integration Point in api_client.py

**File:** src/python_modern_template/api_client.py
**Lines:** 112-118 (7 lines)
**Function:** `retry_with_backoff()`

**Uncovered Code:**
```python
112: @retry(max_attempts=3, backoff=2.0)
113: def retry_with_backoff(self, operation: Callable) -> Any:
114:     """Retry operation with exponential backoff."""
115:     try:
116:         return operation()
117:     except ConnectionError:
118:         logger.warning("Connection failed, retrying...")
```

**Why High:** Integration logic with retry mechanism

**Recommended Test:**
```python
@pytest.mark.parametrize("attempt,should_succeed", [
    (1, True),  # Succeeds first try
    (2, True),  # Succeeds second try
    (3, True),  # Succeeds third try
    (4, False), # Fails after max attempts
])
def test_retry_with_backoff(attempt: int, should_succeed: bool) -> None:
    """Test retry mechanism with various scenarios."""
    # Arrange
    client = APIClient()
    call_count = 0

    def flaky_operation():
        nonlocal call_count
        call_count += 1
        if call_count < attempt:
            raise ConnectionError("Connection failed")
        return "success"

    # Act & Assert
    if should_succeed:
        result = client.retry_with_backoff(flaky_operation)
        assert result == "success"
        assert call_count == attempt
    else:
        with pytest.raises(ConnectionError):
            client.retry_with_backoff(flaky_operation)
```

**Impact:** Covers 7 lines, adds 3.0% coverage

---

## Coverage By Module

| Module | Coverage | Uncovered Lines | Priority |
|--------|----------|----------------|----------|
| validators.py | 65% | 12 | CRITICAL |
| parser.py | 80% | 4 | HIGH |
| api_client.py | 75% | 7 | HIGH |
| utils.py | 95% | 1 | LOW |

**Total:** 75.3% (23 uncovered lines)

---

## Quick Win Recommendations

These tests would quickly boost coverage:

1. **Add error handling tests** (validators.py)
   - +3.5% coverage
   - 10 minutes to write

2. **Add edge case tests** (parser.py)
   - +1.7% coverage
   - 5 minutes to write

3. **Add integration tests** (api_client.py)
   - +3.0% coverage
   - 15 minutes to write

**Total Impact:** +8.2% coverage (reaching 83.5%)
**Total Time:** ~30 minutes

---

## Coverage Trend

```
Week 1: 70% ███████░░░
Week 2: 72% ███████▓░░
Week 3: 75% ████████░░
Week 4: 75% ████████░░  ← Current (stalled)

Target: 80% ████████▓░
```

**Trend:** +5% over 3 weeks, then stalled
**Recommendation:** Focus on quick wins above to break through 80%

---

## Detailed File Analysis

### src/python_modern_template/validators.py (65% coverage)

**Covered:**
- Basic email validation (happy path)
- URL validation (happy path)
- Phone number validation

**Not Covered:**
- Error handling (lines 45-52)
- Edge cases (empty strings, None)
- Invalid format handling

**Missing Test Types:**
- Parametrized tests for invalid inputs
- Exception handling tests
- Edge case tests

### src/python_modern_template/parser.py (80% coverage)

**Covered:**
- Standard config parsing
- Type conversion
- Default value handling

**Not Covered:**
- Empty config handling (lines 67-70)

**Missing Test Types:**
- Edge case tests (empty, None)

### src/python_modern_template/api_client.py (75% coverage)

**Covered:**
- Basic API calls
- Authentication
- Response parsing

**Not Covered:**
- Retry logic (lines 112-118)
- Connection error handling
- Backoff mechanism

**Missing Test Types:**
- Integration tests with retries
- Failure scenario tests

---

## Next Steps

### Immediate Actions (30 minutes)

1. **Add error handling tests to validators.py**
   ```bash
   # Edit tests/test_validators.py
   # Add test_validate_email_value_error_handling()
   # Add test_validate_email_unexpected_error_handling()
   ```

2. **Add edge case tests to parser.py**
   ```bash
   # Edit tests/test_parser.py
   # Add test_parse_config_empty_data()
   # Add test_parse_config_none_data()
   ```

3. **Add integration tests to api_client.py**
   ```bash
   # Edit tests/test_api_client.py
   # Add test_retry_with_backoff()
   ```

4. **Run coverage again**
   ```bash
   make coverage
   ```

**Expected Result:** 83.5% coverage (exceeds 80% target!)

### Verify Implementation

```bash
# Run tests to ensure they fail (TDD)
make test

# Verify uncovered code is exercised
# Fix any test issues
# Re-run coverage
make coverage

# Should see 80%+ coverage
```

---

## Additional Recommendations

### Use Parametrized Tests

For multiple similar test cases:

```python
@pytest.mark.parametrize("email,valid", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False),
    ("test@", False),
    ("@example.com", False),
])
def test_validate_email_parametrized(email: str | None, valid: bool) -> None:
    """Test email validation with various inputs."""
    if valid:
        assert validate_email(email) is True
    else:
        assert validate_email(email) is False
```

### Use Fixtures for Common Setup

```python
@pytest.fixture
def sample_config():
    """Provide sample configuration for tests."""
    return {
        "api_url": "https://api.example.com",
        "timeout": 30,
        "retries": 3,
    }

def test_parse_config_with_defaults(sample_config):
    """Test config parsing with defaults."""
    result = parse_config(sample_config)
    assert result["timeout"] == 30
```

### Focus on Critical Paths

Priority order:
1. Error handling (catch exceptions)
2. Edge cases (empty, None, invalid)
3. Security checks (validation, authorization)
4. Integration points (API calls, database)
5. Business logic
6. Utility functions

---

## Coverage Best Practices

1. **Write tests FIRST (TDD)** - Coverage comes naturally
2. **Test behavior, not implementation** - Focus on what, not how
3. **Use real code over mocks** - Only mock external dependencies
4. **Aim for 100% of new code** - Don't lower the bar
5. **Track trends** - Ensure coverage doesn't regress
6. **Review uncovered code regularly** - Don't let gaps accumulate

---

## Integration with Quality Tools

### With make check

```bash
# Coverage is part of quality gates
make check

# Must pass 80%+ coverage requirement
```

### With TDD Reviewer

```bash
# TDD reviewer checks coverage compliance
[tdd-reviewer]

# Includes coverage verification
```

### With Coverage Command

```bash
# Generate HTML report
make coverage

# View in browser
open htmlcov/index.html
```

---

## Remember

> "Coverage percentage is a measure, not a goal."
> "Aim for meaningful tests, not just high numbers."

**Good coverage means:**
- ✅ Critical paths tested
- ✅ Error handling verified
- ✅ Edge cases covered
- ✅ Integration points tested

**Bad coverage means:**
- ❌ Tests just to hit lines
- ❌ Meaningless assertions
- ❌ Over-mocking everything
- ❌ Ignoring critical gaps

Focus on **quality coverage**, not just quantity!
```

## Advanced Features

### Historical Tracking

Store coverage data over time:

```bash
# Save current coverage
echo "$(date +%Y-%m-%d),$(coverage report | grep TOTAL | awk '{print $4}')" >> .coverage_history

# View trend
cat .coverage_history
```

### Per-Module Breakdown

Analyze each module separately:

```bash
# Get coverage for specific module
coverage report --include="src/python_modern_template/validators.py"
```

### Branch Coverage

Not just line coverage, but branch coverage:

```bash
# Enable branch coverage in pyproject.toml
[tool.pytest.ini_options]
branch = true

# Shows uncovered branches (if/else not both tested)
```

### Diff Coverage

Focus on changed lines only:

```bash
# Install diff-cover
pip install diff-cover

# Check coverage of git diff
diff-cover htmlcov/coverage.xml --compare-branch=main
```

## Remember

Coverage analysis is a **tool for improvement**, not a report card. Use it to:
- Find gaps in testing
- Prioritize test writing
- Track progress
- Ensure quality

But always remember: **100% coverage ≠ bug-free code**. Write meaningful tests!
