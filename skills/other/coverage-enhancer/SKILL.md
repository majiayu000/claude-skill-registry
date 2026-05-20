---
name: coverage-enhancer
description: Analyze existing test suites and source code to suggest additional unit tests that improve test coverage. Use this skill when working with test files and source code to identify untested code paths, missing edge cases, uncovered branches, untested error conditions, and gaps in test coverage. Supports major testing frameworks (pytest, Jest, JUnit, Go testing, etc.) and generates targeted test suggestions based on coverage analysis.
---

# Coverage Enhancer

Analyze existing tests and source code to identify coverage gaps, then suggest specific additional tests to improve overall test coverage and code quality.

## Core Capabilities

### 1. Coverage Gap Analysis

Identify untested areas in source code:
- **Uncovered lines** - Code never executed by tests
- **Uncovered branches** - Conditional paths not tested
- **Uncovered functions** - Methods/functions without tests
- **Missing error handling tests** - Exception paths not verified
- **Untested edge cases** - Boundary conditions not covered
- **Insufficient scenarios** - Limited test diversity

### 2. Existing Test Analysis

Understand current test coverage by:
- Parsing existing test files
- Identifying tested functions and methods
- Recognizing test patterns and frameworks
- Detecting coverage tools in use
- Analyzing test quality and completeness

### 3. Test Suggestion Generation

Generate specific, actionable test recommendations:
- Complete test code in the project's framework
- Clear test names describing what's being tested
- Setup, execution, and assertion steps
- Integration with existing test structure
- Prioritized by coverage impact

## Coverage Analysis Workflow

### Step 1: Analyze Existing Tests

Read and understand the current test suite:

**Identify test framework:**
```python
# pytest
def test_something():
    assert result == expected

# unittest
class TestSomething(unittest.TestCase):
    def test_method(self):
        self.assertEqual(result, expected)
```

**Map tested functionality:**
- Which functions/methods have tests?
- What scenarios are covered?
- What assertions are made?
- What inputs are tested?

**Identify test patterns:**
- Naming conventions
- Setup/teardown patterns
- Fixture usage
- Mock/stub patterns

### Step 2: Analyze Source Code

Examine the implementation to find gaps:

**Identify code paths:**
```python
def process(value):
    if value < 0:        # Branch 1
        raise ValueError
    elif value == 0:     # Branch 2
        return None
    else:                # Branch 3
        return value * 2
```

**Find untested branches:**
- If/else conditions not covered
- Switch/case statements
- Exception handlers (try/except/finally)
- Early returns
- Loop edge cases (zero iterations, one iteration, many)

**Identify uncovered functions:**
- Helper functions without tests
- Private methods (if testing them is valuable)
- Class methods and properties
- Static/class methods

### Step 3: Prioritize Coverage Gaps

Focus on high-value additions:

**Priority 1: Critical paths**
- Error handling and validation
- Security-sensitive code
- Data integrity operations
- Public API methods

**Priority 2: Complex logic**
- Conditional logic with multiple branches
- Loops with edge cases
- State transitions
- Algorithm implementations

**Priority 3: Completeness**
- Untested helper functions
- Missing edge cases
- Property getters/setters
- Simple utility functions

### Step 4: Generate Test Suggestions

Create specific, ready-to-use tests:

**Format:**
```python
# Suggested test for uncovered branch: negative input validation
def test_process_negative_input():
    """Test that negative values raise ValueError."""
    with pytest.raises(ValueError):
        process(-1)

# Reason: This tests the value < 0 branch which is currently uncovered
# Coverage impact: +5 lines, +1 branch
```

**Include:**
1. Test name (descriptive)
2. Test implementation (complete code)
3. Explanation of what's being tested
4. Coverage impact estimate
5. Integration notes (where to add in test file)

### Step 5: Suggest Coverage Tool Integration

Recommend running coverage analysis:

```bash
# Python
pytest --cov=mymodule --cov-report=html

# JavaScript
npm test -- --coverage

# Java
mvn test jacoco:report

# Go
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

## Coverage Analysis Patterns

### Pattern 1: Branch Coverage

**Uncovered code:**
```python
def calculate_discount(price, customer_type):
    if customer_type == "premium":
        return price * 0.8
    elif customer_type == "regular":
        return price * 0.9
    else:
        return price
```

**Existing test:**
```python
def test_calculate_discount_premium():
    assert calculate_discount(100, "premium") == 80
```

**Suggested additions:**
```python
def test_calculate_discount_regular():
    """Test discount calculation for regular customers."""
    assert calculate_discount(100, "regular") == 90
    # Coverage: Tests the 'regular' branch

def test_calculate_discount_no_discount():
    """Test that unknown customer types get no discount."""
    assert calculate_discount(100, "guest") == 100
    # Coverage: Tests the else branch

def test_calculate_discount_edge_cases():
    """Test discount calculation with edge case prices."""
    assert calculate_discount(0, "premium") == 0
    assert calculate_discount(0.01, "premium") == 0.008
    # Coverage: Tests edge cases within covered branches
```

### Pattern 2: Exception Path Coverage

**Uncovered code:**
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Existing test:**
```python
def test_divide_normal():
    assert divide(10, 2) == 5
```

**Suggested addition:**
```python
def test_divide_by_zero():
    """Test that dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
    # Coverage: Tests the exception path (b == 0 branch)
    # Impact: +2 lines, +1 branch
```

### Pattern 3: Loop Coverage

**Uncovered code:**
```python
def find_max(numbers):
    if not numbers:
        return None

    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    return max_val
```

**Existing test:**
```python
def test_find_max_normal():
    assert find_max([1, 5, 3, 2]) == 5
```

**Suggested additions:**
```python
def test_find_max_empty():
    """Test that empty list returns None."""
    assert find_max([]) is None
    # Coverage: Tests the 'if not numbers' branch

def test_find_max_single_element():
    """Test with single element (zero loop iterations)."""
    assert find_max([42]) == 42
    # Coverage: Tests loop with zero iterations

def test_find_max_all_equal():
    """Test with all identical elements."""
    assert find_max([5, 5, 5, 5]) == 5
    # Coverage: Tests loop where condition never true

def test_find_max_negative_numbers():
    """Test with negative numbers."""
    assert find_max([-5, -1, -10, -3]) == -1
    # Coverage: Edge case for comparison logic
```

### Pattern 4: Error Handler Coverage

**Uncovered code:**
```python
def load_config(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filename}: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error loading {filename}: {e}")
```

**Existing test:**
```python
def test_load_config_success(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"key": "value"}')
    assert load_config(str(config_file)) == {"key": "value"}
```

**Suggested additions:**
```python
def test_load_config_file_not_found():
    """Test that missing file returns empty dict."""
    assert load_config("nonexistent.json") == {}
    # Coverage: Tests FileNotFoundError exception path

def test_load_config_invalid_json(tmp_path):
    """Test that invalid JSON raises ValueError."""
    config_file = tmp_path / "bad.json"
    config_file.write_text("{invalid json}")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_config(str(config_file))
    # Coverage: Tests JSONDecodeError exception path

def test_load_config_permission_error(tmp_path):
    """Test that permission errors raise RuntimeError."""
    config_file = tmp_path / "protected.json"
    config_file.write_text('{"key": "value"}')
    config_file.chmod(0o000)

    with pytest.raises(RuntimeError, match="Unexpected error"):
        load_config(str(config_file))
    # Coverage: Tests generic Exception handler
```

### Pattern 5: State Transition Coverage

**Uncovered code:**
```python
class Connection:
    def __init__(self):
        self.state = "closed"

    def connect(self):
        if self.state == "connected":
            raise RuntimeError("Already connected")
        self.state = "connected"

    def disconnect(self):
        if self.state == "closed":
            raise RuntimeError("Not connected")
        self.state = "closed"
```

**Existing test:**
```python
def test_connection_happy_path():
    conn = Connection()
    conn.connect()
    assert conn.state == "connected"
```

**Suggested additions:**
```python
def test_connection_double_connect():
    """Test that connecting twice raises error."""
    conn = Connection()
    conn.connect()

    with pytest.raises(RuntimeError, match="Already connected"):
        conn.connect()
    # Coverage: Tests invalid state transition

def test_connection_disconnect_when_not_connected():
    """Test that disconnecting when closed raises error."""
    conn = Connection()

    with pytest.raises(RuntimeError, match="Not connected"):
        conn.disconnect()
    # Coverage: Tests disconnect precondition check

def test_connection_full_lifecycle():
    """Test complete connect-disconnect cycle."""
    conn = Connection()
    assert conn.state == "closed"

    conn.connect()
    assert conn.state == "connected"

    conn.disconnect()
    assert conn.state == "closed"
    # Coverage: Tests all valid state transitions
```

## Coverage Metrics

### Line Coverage

Percentage of code lines executed by tests:

```
Total lines: 100
Covered lines: 75
Coverage: 75%
```

**Target:** 80%+ for critical code, 60%+ overall

### Branch Coverage

Percentage of conditional branches tested:

```python
if condition:    # Branch 1
    do_something()
else:            # Branch 2
    do_other()

# 100% branch coverage requires testing both paths
```

**Target:** 70%+ for complex logic

### Function Coverage

Percentage of functions with at least one test:

**Target:** 90%+ for public APIs

### Path Coverage

All possible execution paths tested:

```python
def complex(a, b, c):
    if a:          # 2 branches
        if b:      # 2 branches
            if c:  # 2 branches
                return "all true"
```

Total paths: 2³ = 8 paths

**Target:** Cover critical paths, not necessarily all combinations

## Integration with Coverage Tools

### Python (pytest + coverage)

**Run coverage:**
```bash
pytest --cov=mymodule --cov-report=term-missing --cov-report=html
```

**Read coverage report:**
```python
# Look for:
# - Missing lines (shown in report)
# - Uncovered branches (with --cov-branch)
# - Files with low coverage (<80%)
```

**Suggest tests based on missing lines**

### JavaScript (Jest)

**Run coverage:**
```bash
npm test -- --coverage --verbose
```

**Read coverage output:**
```javascript
// coverage/lcov-report/index.html shows:
// - Uncovered lines (highlighted in red)
// - Uncovered branches
// - Function coverage
```

### Java (JaCoCo)

**Run coverage:**
```bash
mvn test jacoco:report
```

**Read report:**
```
target/site/jacoco/index.html
```

### Go

**Run coverage:**
```bash
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Test Suggestion Template

When suggesting tests, use this format:

```
## Coverage Gap: [Description]

**Location:** [file:line or function name]
**Current Coverage:** [X%]
**Impact:** +[N] lines, +[M] branches

### Suggested Test:

[Complete test code]

**Explanation:**
[What this test covers and why it's important]

**Where to add:**
[In which test file, near which existing test]
```

### Example:

```
## Coverage Gap: Error handling for invalid input

**Location:** src/validator.py:45-48
**Current Coverage:** 60% (missing exception path)
**Impact:** +3 lines, +1 branch

### Suggested Test:

```python
def test_validate_email_invalid_format():
    """Test that invalid email format raises ValueError."""
    with pytest.raises(ValueError, match="Invalid email format"):
        validate_email("not-an-email")

    # Additional invalid cases
    with pytest.raises(ValueError):
        validate_email("")
    with pytest.raises(ValueError):
        validate_email("@example.com")
```

**Explanation:**
This test covers the exception path when email validation fails.
Currently, only the happy path (valid emails) is tested.
This improves branch coverage and ensures proper error messages.

**Where to add:**
In tests/test_validator.py, after test_validate_email_valid
```

## Best Practices

1. **Start with existing tests** - Always read current tests first to understand patterns
2. **Match the style** - Use same framework, naming, and structure as existing tests
3. **Focus on value** - Prioritize high-impact coverage gaps over achieving 100%
4. **Test behavior, not implementation** - Focus on what the code does, not how
5. **Keep tests isolated** - Each test should be independent
6. **Use descriptive names** - Test names should explain what's being verified
7. **Add explanations** - Comment why each test is needed for coverage
8. **Suggest coverage tools** - Help users measure and track coverage
9. **Consider mutation testing** - Suggest tests that would catch actual bugs
10. **Balance coverage and maintainability** - Don't over-test trivial code

## Common Coverage Gaps

### Gap 1: Error Cases Not Tested

```python
# Often only happy path is tested
def parse_int(s):
    return int(s)  # ValueError not tested

# Suggest:
def test_parse_int_invalid():
    with pytest.raises(ValueError):
        parse_int("not a number")
```

### Gap 2: Edge Cases Missing

```python
# Common values tested, boundaries ignored
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

# Need tests for:
# - value == min_val
# - value == max_val
# - value < min_val
# - value > max_val
```

### Gap 3: Else Branches Untested

```python
if condition:
    # Tested
    do_something()
else:
    # Never tested!
    do_other()
```

### Gap 4: Loop Edge Cases

```python
for item in collection:
    process(item)

# Need tests for:
# - Empty collection
# - Single item
# - Many items
```

### Gap 5: Cleanup/Finally Not Tested

```python
try:
    risky_operation()
finally:
    cleanup()  # Often not verified

# Suggest test that verifies cleanup happens
```

## Language-Specific Patterns

For language-specific coverage patterns and testing approaches:

- **Python**: See [references/python_coverage.md](references/python_coverage.md)
- **JavaScript/TypeScript**: See [references/javascript_coverage.md](references/javascript_coverage.md)
- **Java**: See [references/java_coverage.md](references/java_coverage.md)
- **Go**: See [references/go_coverage.md](references/go_coverage.md)

## Example: Complete Coverage Analysis

**Source code:**
```python
def calculate_grade(score):
    """Calculate letter grade from numeric score."""
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")

    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'
```

**Existing tests:**
```python
def test_calculate_grade_a():
    assert calculate_grade(95) == 'A'

def test_calculate_grade_c():
    assert calculate_grade(75) == 'C'
```

**Coverage analysis:**
- Line coverage: 60% (6/10 lines)
- Branch coverage: 40% (2/5 grade ranges, 0/2 error checks)

**Suggested tests:**
```python
def test_calculate_grade_invalid_negative():
    """Test that negative scores raise ValueError."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_grade(-1)
    # Coverage: +2 lines (score < 0 branch)

def test_calculate_grade_invalid_too_high():
    """Test that scores above 100 raise ValueError."""
    with pytest.raises(ValueError, match="between 0 and 100"):
        calculate_grade(101)
    # Coverage: +0 lines (same as above, but tests second condition)

def test_calculate_grade_b():
    """Test B grade threshold."""
    assert calculate_grade(85) == 'B'
    # Coverage: +1 line (score >= 80 branch)

def test_calculate_grade_d():
    """Test D grade threshold."""
    assert calculate_grade(65) == 'D'
    # Coverage: +1 line (score >= 60 branch)

def test_calculate_grade_f():
    """Test F grade for failing scores."""
    assert calculate_grade(45) == 'F'
    # Coverage: +1 line (else branch)

def test_calculate_grade_boundaries():
    """Test exact boundary values."""
    assert calculate_grade(90) == 'A'  # Exact boundary
    assert calculate_grade(89) == 'B'  # Just below
    assert calculate_grade(80) == 'B'  # Exact boundary
    assert calculate_grade(79) == 'C'  # Just below
    assert calculate_grade(70) == 'C'  # Exact boundary
    assert calculate_grade(60) == 'D'  # Exact boundary
    assert calculate_grade(0) == 'F'   # Lower bound
    assert calculate_grade(100) == 'A' # Upper bound
    # Coverage: Ensures all boundaries work correctly
```

**Result:** 100% line coverage, 100% branch coverage
