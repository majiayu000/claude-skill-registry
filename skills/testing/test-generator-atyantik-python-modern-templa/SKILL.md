---
name: test-generator
description: Generate comprehensive test boilerplate following project TDD conventions. Use when creating new tests for modules, classes, or functions. Automatically creates tests with proper structure, type hints, docstrings, and AAA pattern.
---

# Test Boilerplate Generator

## ⚠️ MANDATORY: Read Project Documentation First

**BEFORE generating tests, you MUST read and understand the following project documentation:**

### Core Project Documentation

1. **README.md** - Project overview, features, and getting started
2. **AI_DOCS/project-context.md** - Tech stack, architecture, development workflow
3. **AI_DOCS/code-conventions.md** - Code style, formatting, best practices (especially for tests)
4. **AI_DOCS/tdd-workflow.md** - TDD process, testing standards, coverage requirements (CRITICAL)

### Session Context (if available)

5. **.ai-context/ACTIVE_TASKS.md** - Current tasks and priorities
6. **.ai-context/CONVENTIONS.md** - Project-specific conventions
7. **.ai-context/RECENT_DECISIONS.md** - Recent architectural decisions
8. **.ai-context/LAST_SESSION_SUMMARY.md** - Previous session summary

### Additional AI Documentation

9. **AI_DOCS/ai-tools.md** - Session management workflow
10. **AI_DOCS/ai-skills.md** - Other specialized skills/agents available

### Why This Matters

- **Testing Standards**: Follow project-specific test structure and conventions
- **TDD Patterns**: Use AAA pattern, proper fixtures, and parametrization
- **Code Quality**: Generate tests with type hints, docstrings, proper imports
- **Mock Guidelines**: Understand when to mock vs. use real code
- **Coverage Goals**: Generate tests that help reach 80%+ coverage

**After reading these files, proceed with your test generation task below.**

---

## Overview

Automatically generate comprehensive test boilerplate that follows this project's strict TDD and quality standards.

## When to Use

- Creating tests for a new module, class, or function
- Starting TDD workflow (write tests FIRST!)
- Need test templates with proper structure
- Want parametrized test examples
- Creating test fixtures

## What This Skill Generates

✅ Test files with proper imports and structure
✅ Test classes organized by functionality
✅ Parametrized test templates
✅ AAA pattern (Arrange-Act-Assert) structure
✅ Complete type hints
✅ Google-style docstrings
✅ Fixture templates (when needed)

## Usage Examples

### Generate Tests for a Module

```bash
# User provides source file
generate tests for src/python_modern_template/validators.py
```

**Output:** Creates `tests/test_validators.py` with:
- Test class for each function/class
- Parametrized test cases
- Edge case test templates
- Proper imports and structure

### Generate Tests for a Specific Function

```bash
# User describes the function
generate tests for validate_email function that checks email format
```

**Output:** Creates test class with:
- Basic functionality tests
- Edge cases (empty, invalid format, special characters)
- Parametrized test cases
- Error handling tests

### Generate Fixture Template

```bash
# User needs test fixtures
generate pytest fixture for database connection
```

**Output:** Creates conftest.py entry with proper fixture structure

## Step-by-Step Process

### Step 1: Analyze Source Code

If source file provided:
1. Read the source file
2. Identify all public functions and classes
3. Analyze function signatures (parameters, return types)
4. Identify error cases (raises clauses)

If described by user:
1. Extract function/class name
2. Understand parameters and return type
3. Identify test scenarios from description

### Step 2: Choose Template

Select appropriate template from `templates/`:
- `test_function.py` - Simple function tests
- `test_class.py` - Class with methods tests
- `test_parametrized.py` - Data-driven tests
- `test_async.py` - Async function tests
- `test_exception.py` - Error handling tests
- `conftest_fixture.py` - Pytest fixtures

### Step 3: Generate Test Code

Use templates from `.claude/skills/test-generator/templates/` directory.

**Template Variables:**
- `{module_name}` - Source module name
- `{class_name}` - Class being tested
- `{function_name}` - Function being tested
- `{test_class_name}` - Generated test class name
- `{import_path}` - Full import path
- `{param_names}` - Function parameters
- `{return_type}` - Function return type

### Step 4: Add Test Cases

Generate test cases for:
1. **Happy path** - Normal successful execution
2. **Edge cases** - Boundary values, empty inputs, None values
3. **Error cases** - Invalid inputs, exceptions
4. **Parametrized cases** - Multiple input combinations

### Step 5: Format and Save

1. Apply proper formatting (Black, isort)
2. Ensure type hints and docstrings
3. Save to appropriate test file
4. Display summary of generated tests

## Templates Reference

### Template: Simple Function Test

**File:** `templates/test_function.py`

```python
"""Tests for {module_name}.{function_name}."""

from __future__ import annotations

import pytest

from {import_path} import {function_name}


class Test{FunctionNameCamelCase}:
    """Test cases for {function_name}."""

    def test_{function_name}_basic(self) -> None:
        """Test basic functionality of {function_name}."""
        # Arrange
        # TODO: Set up test data

        # Act
        result = {function_name}()

        # Assert
        # TODO: Add assertions
        assert result is not None

    def test_{function_name}_with_valid_input(self) -> None:
        """Test {function_name} with valid input."""
        # Arrange
        # TODO: Prepare valid input

        # Act
        # TODO: Call function

        # Assert
        # TODO: Verify result
        pass

    def test_{function_name}_with_invalid_input(self) -> None:
        """Test {function_name} handles invalid input."""
        # Arrange
        # TODO: Prepare invalid input

        # Act & Assert
        with pytest.raises(ValueError):
            {function_name}()  # TODO: Add invalid input

    def test_{function_name}_edge_cases(self) -> None:
        """Test {function_name} edge cases."""
        # TODO: Test empty input, None, boundary values
        pass
```

### Template: Parametrized Test

**File:** `templates/test_parametrized.py`

```python
"""Tests for {module_name}.{function_name}."""

from __future__ import annotations

import pytest

from {import_path} import {function_name}


class Test{FunctionNameCamelCase}:
    """Parametrized test cases for {function_name}."""

    @pytest.mark.parametrize(
        "input_value,expected",
        [
            # Happy path cases
            ("valid_input_1", "expected_output_1"),
            ("valid_input_2", "expected_output_2"),

            # Edge cases
            ("", "expected_for_empty"),
            (None, "expected_for_none"),

            # TODO: Add more test cases
        ],
    )
    def test_{function_name}_parametrized(
        self,
        input_value: str,  # TODO: Adjust type
        expected: str,  # TODO: Adjust type
    ) -> None:
        """Test {function_name} with various inputs."""
        # Act
        result = {function_name}(input_value)

        # Assert
        assert result == expected

    @pytest.mark.parametrize(
        "invalid_input,expected_error",
        [
            ("invalid_1", ValueError),
            ("invalid_2", TypeError),
            # TODO: Add more error cases
        ],
    )
    def test_{function_name}_error_cases(
        self,
        invalid_input: str,  # TODO: Adjust type
        expected_error: type[Exception],
    ) -> None:
        """Test {function_name} raises appropriate errors."""
        # Act & Assert
        with pytest.raises(expected_error):
            {function_name}(invalid_input)
```

### Template: Class with Methods Test

**File:** `templates/test_class.py`

```python
"""Tests for {module_name}.{class_name}."""

from __future__ import annotations

import pytest

from {import_path} import {class_name}


class Test{ClassName}:
    """Test cases for {class_name}."""

    @pytest.fixture
    def instance(self) -> {class_name}:
        """Create {class_name} instance for testing."""
        return {class_name}()  # TODO: Add initialization parameters

    def test_initialization(self, instance: {class_name}) -> None:
        """Test {class_name} initialization."""
        # Assert
        assert isinstance(instance, {class_name})
        # TODO: Verify initial state

    def test_method_name(self, instance: {class_name}) -> None:
        """Test method_name behavior."""
        # Arrange
        # TODO: Set up test data

        # Act
        result = instance.method_name()  # TODO: Add actual method

        # Assert
        # TODO: Verify result
        assert result is not None
```

### Template: Async Function Test

**File:** `templates/test_async.py`

```python
"""Tests for async {module_name}.{function_name}."""

from __future__ import annotations

import pytest

from {import_path} import {function_name}


class Test{FunctionNameCamelCase}:
    """Test cases for async {function_name}."""

    @pytest.mark.asyncio
    async def test_{function_name}_basic(self) -> None:
        """Test basic async functionality."""
        # Arrange
        # TODO: Set up test data

        # Act
        result = await {function_name}()

        # Assert
        assert result is not None

    @pytest.mark.asyncio
    async def test_{function_name}_concurrent(self) -> None:
        """Test concurrent execution."""
        # Arrange
        import asyncio

        # Act
        results = await asyncio.gather(
            {function_name}(),
            {function_name}(),
        )

        # Assert
        assert len(results) == 2
```

### Template: Pytest Fixture

**File:** `templates/conftest_fixture.py`

```python
"""Pytest fixtures for {test_module}."""

from __future__ import annotations

from collections.abc import Generator

import pytest


@pytest.fixture
def {fixture_name}() -> Generator[{ResourceType}, None, None]:
    """Provide {description} for tests.

    Yields:
        {ResourceType}: {Description of what is yielded}
    """
    # Setup
    resource = {ResourceType}()  # TODO: Initialize resource

    try:
        yield resource
    finally:
        # Teardown
        pass  # TODO: Add cleanup code
```

## Quality Standards

All generated tests MUST include:

✅ **Type Hints**
- All test functions annotated with `-> None`
- All fixture functions with proper return types
- All parameters with type hints

✅ **Docstrings**
- Every test function has descriptive docstring
- Docstring explains WHAT is being tested, not HOW
- Clear and concise

✅ **AAA Pattern**
```python
def test_example() -> None:
    """Test description."""
    # Arrange - Set up test data
    data = prepare_test_data()

    # Act - Execute the function
    result = function_under_test(data)

    # Assert - Verify the result
    assert result == expected
```

✅ **Proper Imports**
```python
from __future__ import annotations  # Always first

import pytest

from python_modern_template.module import function
```

✅ **No Excessive Mocking**
- Use real code where possible
- Only mock: HTTP, DB, File I/O, time, random
- Never mock: internal functions, validators, processors

## Output Format

After generating tests, provide:

```markdown
## Generated Test File: tests/test_{module}.py

**Summary:**
- Test Classes: X
- Test Functions: X
- Parametrized Tests: X
- Fixtures: X
- Lines of Code: ~XXX

**Test Coverage:**
- Function 1: 4 test cases (happy path, edge cases, error handling)
- Function 2: 3 test cases
- Total: X test cases

**Next Steps:**
1. Review generated tests and customize TODO sections
2. Add specific test data for your use case
3. Run tests to verify they fail (TDD red phase):
   ```bash
   make test
   ```
4. Implement the functionality
5. Run tests again to verify they pass
6. Check coverage:
   ```bash
   make coverage
   ```

**Files Created/Modified:**
- ✅ tests/test_{module}.py (NEW)
- ⚠️  Remember to implement tests before the actual code (TDD!)
```

## Integration with Project Tools

This skill integrates with:
- `make test` - Run generated tests
- `make coverage` - Verify test coverage
- `make format` - Format generated code
- `tdd-reviewer` agent - Verify TDD compliance

## Script Usage

For programmatic generation, use:

```bash
# Generate from source file
python .claude/skills/test-generator/scripts/generate.py \
  --source src/python_modern_template/module.py \
  --output tests/test_module.py

# Generate from function name
python .claude/skills/test-generator/scripts/generate.py \
  --function validate_email \
  --module validators \
  --template parametrized
```

## Best Practices

1. **Start with generated boilerplate, then customize**
2. **Review all TODO comments** - replace with actual test data
3. **Run tests immediately** - they should fail initially (TDD)
4. **Use parametrized tests** for multiple input cases
5. **Avoid over-mocking** - use real code where possible
6. **Aim for edge cases** - empty, None, invalid, boundary values
7. **Test one thing per test** - focused, clear assertions

## Examples in Action

### Example 1: Generate tests for email validator

**User Request:**
```
generate tests for the validate_email function in src/python_modern_template/validators.py
```

**Skill Actions:**
1. Read src/python_modern_template/validators.py
2. Identify validate_email function signature
3. Choose parametrized template (multiple test cases)
4. Generate tests/test_validators.py with:
   - Valid email cases
   - Invalid email cases (no @, multiple @, etc.)
   - Edge cases (empty, whitespace, very long)
   - Error handling tests

### Example 2: Generate tests for a new class

**User Request:**
```
I'm creating a UserManager class with methods: create_user, delete_user, find_user. Generate tests.
```

**Skill Actions:**
1. Choose class template
2. Generate test class with:
   - Fixture for UserManager instance
   - Test for each method
   - Test initialization
   - Test error cases
3. Add parametrized tests for find_user (various search criteria)

### Example 3: Generate async tests

**User Request:**
```
Generate tests for async function fetch_data(url: str) -> dict
```

**Skill Actions:**
1. Choose async template
2. Generate async tests with:
   - Basic fetch test with mock HTTP
   - Error handling (timeout, 404, 500)
   - Concurrent fetch tests
3. Add pytest-asyncio marker

## Remember

**TDD Workflow:**
1. Generate tests FIRST (this skill)
2. Run tests (they should FAIL)
3. Implement code
4. Run tests (they should PASS)
5. Refactor while keeping tests green

This skill helps you start TDD right—tests first, always!
