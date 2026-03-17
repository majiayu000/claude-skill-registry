---
name: fuzzing-input-generator
description: Generate randomized and edge-case inputs to detect unexpected failures, bugs, and security vulnerabilities through fuzz testing. Use when creating test cases for robustness testing, generating adversarial inputs, testing error handling, finding edge cases, or security testing. Produces Python test code with fuzzing inputs for strings, numbers, and structured data focusing on edge cases, invalid inputs, and random valid inputs. Triggers when users ask to generate fuzz tests, create randomized test inputs, test edge cases, find bugs through fuzzing, or generate adversarial test cases.
---

# Fuzzing Input Generator

## Overview

Generate comprehensive fuzz testing inputs to uncover bugs, crashes, and security vulnerabilities by systematically testing functions with edge cases, invalid inputs, and randomized data.

## Workflow

### 1. Analyze the Target Function

Understand what needs to be fuzzed:

**Identify input types:**
- Strings (text, paths, URLs, etc.)
- Numbers (integers, floats)
- Booleans
- Collections (lists, dicts, sets)
- Structured data (JSON, XML)
- Files or binary data
- Combinations of above

**Understand expected behavior:**
- What are valid inputs?
- What should happen with invalid inputs?
- Are there documented constraints?
- What error handling exists?

**Extract function signature:**
```python
def process_user_input(name: str, age: int, email: str) -> dict:
    """Process user registration data."""
    # Analyze: expects string, int, string
    # Constraints: name non-empty, age > 0, email format
```

### 2. Select Fuzzing Strategy

Choose appropriate fuzzing approaches:

#### Edge Case Fuzzing

Test boundary conditions and special values:
- Empty inputs
- Very large inputs
- Minimum/maximum values
- Zero, negative numbers
- Special characters
- Null/None values

#### Invalid Input Fuzzing

Test with malformed or incorrect data:
- Wrong types
- Invalid formats
- Out-of-range values
- Malformed structures
- Encoding issues

#### Random Valid Fuzzing

Generate random but technically valid inputs:
- Random strings of various lengths
- Random numbers in valid ranges
- Random but well-formed structures
- Valid but unusual combinations

#### Security Fuzzing

Test for vulnerabilities:
- Injection attacks (SQL, command, XSS)
- Path traversal
- Buffer overflows
- Format string attacks
- Unicode exploits

### 3. Generate Fuzz Test Code

Create Python test functions with fuzzing inputs.

#### Basic Template

```python
import pytest
import random
import string

def fuzz_<function_name>():
    """Fuzz test for <function_name>."""

    # Edge cases
    edge_cases = [
        # Add specific edge case inputs
    ]

    # Invalid inputs
    invalid_inputs = [
        # Add invalid inputs
    ]

    # Random valid inputs
    def generate_random_valid():
        # Generate random but valid input
        pass

    # Test edge cases
    for input_data in edge_cases:
        try:
            result = function_under_test(input_data)
            # Check result or at least that it doesn't crash
        except Exception as e:
            # Document or assert expected exceptions
            pass

    # Test invalid inputs
    for input_data in invalid_inputs:
        # Similar testing pattern
        pass

    # Test random inputs
    for _ in range(100):
        random_input = generate_random_valid()
        # Test with random input
```

### 4. Generate Input Categories

Create comprehensive input sets for each parameter type. See [fuzzing-patterns.md](references/fuzzing-patterns.md) for extensive patterns.

#### String Inputs

```python
def generate_string_fuzz_inputs():
    """Generate fuzz inputs for string parameters."""
    return [
        # Empty and whitespace
        "",
        " ",
        "   ",
        "\t",
        "\n",
        "\r\n",

        # Length edge cases
        "a",                    # Single char
        "a" * 100,              # Medium
        "a" * 10000,            # Long
        "a" * 1000000,          # Very long

        # Special characters
        "!@#$%^&*()",
        "'",
        "\"",
        "\\",
        "<script>alert(1)</script>",

        # Unicode
        "🔥",
        "你好",
        "مرحبا",

        # Injection patterns
        "'; DROP TABLE users--",
        "../../../etc/passwd",
        "${var}",

        # Format strings
        "%s%s%s",
        "{0}{1}{2}",

        # Null bytes
        "\x00",
        "test\x00test",
    ]
```

#### Number Inputs

```python
def generate_number_fuzz_inputs():
    """Generate fuzz inputs for numeric parameters."""
    return [
        # Integers
        0,
        1,
        -1,
        2**31 - 1,              # Max 32-bit int
        -2**31,                 # Min 32-bit int
        2**63 - 1,              # Max 64-bit int
        -2**63,                 # Min 64-bit int

        # Floats
        0.0,
        -0.0,
        float('inf'),
        float('-inf'),
        float('nan'),
        1e308,                  # Near max float
        1e-308,                 # Near min float
        0.1 + 0.2,              # Precision issue

        # Edge cases
        None,
        "123",                  # String number
        "not a number",
        [],
        {},
    ]
```

#### Structured Data Inputs

```python
def generate_json_fuzz_inputs():
    """Generate fuzz inputs for JSON/dict parameters."""
    return [
        # Empty
        {},
        [],
        None,

        # Type confusion
        {"number": "123"},
        {"bool": "true"},
        {"array": "[]"},

        # Deep nesting
        {"a": {"b": {"c": {"d": {"e": "deep"}}}}},
        [[[[["nested"]]]]],

        # Large structures
        {f"key{i}": i for i in range(1000)},
        [i for i in range(10000)],

        # Special keys
        {"": "empty key"},
        {"key with spaces": "value"},
        {"key.with.dots": "value"},

        # Mixed types
        {"str": "text", "num": 123, "bool": True, "null": None, "arr": [1, 2]},

        # Invalid JSON strings
        "{invalid}",
        '{"unclosed": ',
        '{"key": undefined}',
    ]
```

### 5. Write Complete Test Functions

Generate executable test code:

#### Example 1: String Processing Function

```python
import pytest
import random
import string

def test_fuzz_process_username():
    """Fuzz test for username processing."""

    def process_username(username: str) -> str:
        """Function under test."""
        if not username:
            raise ValueError("Username cannot be empty")
        if len(username) > 50:
            raise ValueError("Username too long")
        return username.strip().lower()

    # Edge case inputs
    edge_cases = [
        "",                      # Empty
        " ",                     # Space only
        "a",                     # Single char
        "A" * 50,                # Max length
        "A" * 51,                # Over max
        "  user  ",              # Surrounding spaces
        "User123",               # Mixed case
        "user@name",             # Special chars
        "user\nname",            # Newline
        "🔥user",                # Unicode
        "\x00user",              # Null byte
    ]

    # Invalid inputs
    invalid_inputs = [
        None,
        123,
        [],
        {},
        True,
    ]

    # Test edge cases
    for username in edge_cases:
        try:
            result = process_username(username)
            assert isinstance(result, str)
            assert len(result) <= 50
        except ValueError as e:
            # Expected for empty or too long
            assert "empty" in str(e) or "too long" in str(e)
        except Exception as e:
            pytest.fail(f"Unexpected exception for '{username}': {e}")

    # Test invalid types
    for username in invalid_inputs:
        try:
            result = process_username(username)
            pytest.fail(f"Should reject invalid type: {type(username)}")
        except (TypeError, AttributeError):
            pass  # Expected

    # Random fuzzing
    for _ in range(100):
        length = random.randint(0, 100)
        chars = string.ascii_letters + string.digits + " !@#$"
        random_username = ''.join(random.choice(chars) for _ in range(length))

        try:
            result = process_username(random_username)
            # Verify properties that should always hold
            if random_username.strip():
                assert result.islower()
                assert len(result) <= 50
        except ValueError:
            # Expected for empty or too long
            pass
```

#### Example 2: Numeric Validation Function

```python
import pytest
import math

def test_fuzz_validate_age():
    """Fuzz test for age validation."""

    def validate_age(age: int) -> bool:
        """Function under test."""
        return 0 <= age <= 150

    # Edge case inputs
    edge_cases = [
        0,                       # Min valid
        1,
        150,                     # Max valid
        -1,                      # Just below min
        151,                     # Just above max
        18,                      # Common value
        65,                      # Another common
        2**31 - 1,               # Max int
        -2**31,                  # Min int
    ]

    # Invalid/special inputs
    special_inputs = [
        None,
        "25",                    # String
        25.5,                    # Float
        float('inf'),
        float('-inf'),
        float('nan'),
        [],
        {},
        True,                    # 1 in Python
        False,                   # 0 in Python
    ]

    # Test edge cases
    for age in edge_cases:
        try:
            result = validate_age(age)
            assert isinstance(result, bool)
            if 0 <= age <= 150:
                assert result is True
            else:
                assert result is False
        except Exception as e:
            pytest.fail(f"Unexpected exception for {age}: {e}")

    # Test invalid types
    for age in special_inputs:
        try:
            result = validate_age(age)
            # Document behavior with non-int types
        except (TypeError, ValueError):
            pass  # May be expected

    # Random fuzzing
    for _ in range(100):
        random_age = random.randint(-1000, 1000)
        try:
            result = validate_age(random_age)
            assert result == (0 <= random_age <= 150)
        except Exception as e:
            pytest.fail(f"Failed for random age {random_age}: {e}")
```

#### Example 3: JSON API Function

```python
import pytest
import json
import random

def test_fuzz_parse_user_data():
    """Fuzz test for JSON user data parsing."""

    def parse_user_data(data: dict) -> dict:
        """Function under test."""
        name = data["name"]
        age = int(data["age"])
        email = data.get("email", "")

        if not name:
            raise ValueError("Name required")
        if age < 0:
            raise ValueError("Age must be non-negative")

        return {"name": name.strip(), "age": age, "email": email}

    # Edge case inputs
    edge_cases = [
        {"name": "John", "age": 25},                    # Valid
        {"name": "John", "age": 25, "email": "j@e.com"}, # With optional
        {"name": " John ", "age": 0},                   # Whitespace
        {"name": "A" * 1000, "age": 150},               # Long name
        {"name": "🔥", "age": 1},                       # Unicode
        {},                                             # Empty
        {"name": ""},                                   # Empty name
        {"name": "John", "age": -1},                    # Negative age
        {"name": "John", "age": "25"},                  # String age
        {"name": None, "age": 25},                      # None value
        {"extra": "field", "name": "John", "age": 25},  # Extra fields
    ]

    # Test edge cases
    for data in edge_cases:
        try:
            result = parse_user_data(data)
            assert isinstance(result, dict)
            assert "name" in result
            assert "age" in result
            assert isinstance(result["age"], int)
            assert result["age"] >= 0
        except (KeyError, ValueError, TypeError) as e:
            # Expected for invalid inputs
            pass
        except Exception as e:
            pytest.fail(f"Unexpected exception for {data}: {e}")

    # Random fuzzing
    name_chars = string.ascii_letters + " "
    for _ in range(100):
        random_data = {
            "name": ''.join(random.choice(name_chars) for _ in range(random.randint(0, 50))),
            "age": random.randint(-10, 200),
            "email": f"test{random.randint(0, 1000)}@example.com"
        }

        try:
            result = parse_user_data(random_data)
            # Verify invariants
            if random_data["name"].strip() and random_data["age"] >= 0:
                assert result["name"] == random_data["name"].strip()
                assert result["age"] == random_data["age"]
        except (KeyError, ValueError, TypeError):
            # Expected for invalid random inputs
            pass
```

### 6. Organize and Run Tests

Create a complete test suite:

```python
# test_fuzz_suite.py

import pytest
import random
import string
from your_module import function_to_test

class TestFuzzSuite:
    """Comprehensive fuzz testing suite."""

    def test_edge_cases(self):
        """Test boundary conditions and special values."""
        # Edge case tests
        pass

    def test_invalid_inputs(self):
        """Test with malformed and invalid inputs."""
        # Invalid input tests
        pass

    def test_random_valid(self):
        """Test with randomized valid inputs."""
        # Random fuzzing tests
        pass

    def test_security(self):
        """Test for injection and security issues."""
        # Security tests
        pass

    @pytest.mark.slow
    def test_extensive_fuzzing(self):
        """Extended fuzzing with many iterations."""
        # Run 10000+ iterations
        pass
```

**Run the tests:**
```bash
# Run all fuzz tests
pytest test_fuzz_suite.py -v

# Run with coverage
pytest test_fuzz_suite.py --cov=your_module

# Run only fast tests
pytest test_fuzz_suite.py -m "not slow"

# Run extensive fuzzing
pytest test_fuzz_suite.py -m slow
```

### 7. Analyze Results

When fuzzing finds failures:

**Document the failure:**
- Input that caused failure
- Exception or error message
- Expected vs actual behavior

**Create regression tests:**
```python
def test_regression_issue_123():
    """Regression test for crash with null byte."""
    # This input was found by fuzzing
    problematic_input = "test\x00data"

    # Should handle gracefully
    with pytest.raises(ValueError, match="null byte"):
        process_input(problematic_input)
```

**Fix the code:**
```python
def process_input(data: str) -> str:
    # Add validation found necessary by fuzzing
    if "\x00" in data:
        raise ValueError("null byte not allowed")

    # ... rest of function
```

## Example Workflows

### Example 1: Fuzz a Simple Function

**User request:**
> "Generate fuzz tests for this function"

```python
def divide(a: float, b: float) -> float:
    return a / b
```

**Response:**

```python
import pytest
import math

def test_fuzz_divide():
    """Fuzz test for divide function."""

    # Edge cases
    edge_cases = [
        (10, 2),                # Normal
        (0, 1),                 # Zero numerator
        (1, 0),                 # Division by zero
        (-10, 2),               # Negative
        (10, -2),               # Negative divisor
        (float('inf'), 1),      # Infinity
        (1, float('inf')),      # Divide by infinity
        (float('nan'), 1),      # NaN
        (1, float('nan')),      # Divide by NaN
        (1e308, 1e-308),        # Extreme values
    ]

    for a, b in edge_cases:
        try:
            result = divide(a, b)
            # Check result properties
            if b == 0:
                pytest.fail(f"Should raise ZeroDivisionError for b=0")
            if not math.isnan(result):
                assert math.isclose(result, a / b, rel_tol=1e-9)
        except ZeroDivisionError:
            assert b == 0  # Expected
        except Exception as e:
            pytest.fail(f"Unexpected exception for ({a}, {b}): {e}")

    # Random fuzzing
    for _ in range(1000):
        a = random.uniform(-1e10, 1e10)
        b = random.uniform(-1e10, 1e10)

        try:
            result = divide(a, b)
            if abs(b) > 1e-10:  # Avoid near-zero denominators
                expected = a / b
                if not math.isnan(expected):
                    assert math.isclose(result, expected, rel_tol=1e-6)
        except ZeroDivisionError:
            assert abs(b) < 1e-10  # Expected for small denominators
```

### Example 2: Fuzz File Path Handler

**User request:**
> "Create fuzz tests to find path traversal vulnerabilities"

```python
def test_fuzz_file_path_security():
    """Fuzz test for path traversal vulnerabilities."""

    def safe_read_file(filename: str) -> str:
        """Function under test - should prevent path traversal."""
        # Implementation would validate filename
        pass

    # Path traversal attacks
    path_traversal_inputs = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "....//....//etc/passwd",
        "%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252fetc%252fpasswd",
        "file://etc/passwd",
        "/etc/passwd",
        "C:\\Windows\\System32",
        "~/../../etc/passwd",
        ".",
        "..",
        "/",
        "\\",
        "",
        "\x00",
        "file\x00.txt",
        "con",                   # Windows reserved
        "nul",
        "prn",
        "a" * 1000,              # Very long path
        "a/" * 500 + "file.txt", # Very deep path
    ]

    for path in path_traversal_inputs:
        try:
            result = safe_read_file(path)
            # Should either reject or sanitize
            assert not any(danger in path.lower() for danger in ["etc/passwd", "system32", ".."])
        except (ValueError, PermissionError, FileNotFoundError):
            # Expected rejection
            pass
        except Exception as e:
            pytest.fail(f"Unexpected exception for path '{path}': {e}")
```

## Tips for Effective Fuzzing

**Start with known edge cases:**
- Use patterns from [fuzzing-patterns.md](references/fuzzing-patterns.md)
- Include boundary values specific to your domain
- Add past bugs as regression tests

**Think like an attacker:**
- What inputs would you never expect?
- What could break the assumptions?
- What security vulnerabilities exist?

**Use property-based testing:**
- What should ALWAYS be true?
- Roundtrip properties: `decode(encode(x)) == x`
- Idempotence: `f(f(x)) == f(x)`
- Commutativity: `f(x, y) == f(y, x)`

**Monitor coverage:**
```python
# Use coverage.py to find untested code paths
pytest --cov=module --cov-report=html test_fuzz.py
```

**Iterate based on findings:**
- Each bug found reveals assumption
- Add similar inputs to test suite
- Expand fuzzing to related functions

**Balance breadth and depth:**
- Test many input types (breadth)
- Test each type thoroughly (depth)
- Focus on critical/risky code

## Reference

For comprehensive fuzzing patterns and edge cases, see [fuzzing-patterns.md](references/fuzzing-patterns.md).
