---
name: pytest Test Framework
description: Execute and generate pytest tests for Python projects with fixtures, parametrization, and mocking support
version: 1.0.0
---

# pytest Test Framework

## Purpose

Provide pytest test execution and generation for Python projects, supporting:
- Test file generation from templates
- Test execution with structured output
- Fixtures and parametrized tests
- Mock and monkeypatch support

## Usage

### Generate Test File

```bash
python generate-test.py \
  --source src/calculator.py \
  --output tests/test_calculator.py \
  --type unit \
  --description "Calculator fails to handle division by zero"
```

### Execute Tests

```bash
python run-test.py \
  --file tests/test_calculator.py \
  --config pytest.ini
```

## Output Format

### Test Generation
```json
{
  "success": true,
  "testFile": "tests/test_calculator.py",
  "testCount": 3,
  "template": "unit-test"
}
```

### Test Execution
```json
{
  "success": false,
  "passed": 2,
  "failed": 1,
  "total": 3,
  "duration": 0.234,
  "failures": [
    {
      "test": "test_divide_by_zero",
      "error": "AssertionError: Expected ZeroDivisionError",
      "file": "tests/test_calculator.py",
      "line": 15
    }
  ]
}
```

## Integration

Used by deep-debugger for Python project testing:
1. Invoke test-detector to identify pytest
2. Invoke generate-test.py to create failing test
3. Invoke run-test.py to validate test fails
4. Re-run after fix to verify passing
