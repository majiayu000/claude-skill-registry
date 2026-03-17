---
name: test-writer
description: Write comprehensive tests following TDD principles
tags:
  technology: [python, typescript, javascript]
  feature: [testing, tdd]
  priority: high
---

# Test Writer Skill

## When to Use

Use this skill when you need to:
- Write tests for new features
- Add tests for existing code (increase coverage)
- Write integration or E2E tests

## Instructions

### Step 1: Understand the Requirements

Read the acceptance criteria and identify:
- Happy path scenarios
- Edge cases
- Error conditions
- Integration points

### Step 2: Choose Test Type

| Scenario | Test Type | Framework |
|----------|-----------|-----------|
| Single function/class | Unit test | pytest / jest |
| Multiple components | Integration | pytest / jest |
| Full user flow | E2E | Playwright |
| API endpoints | API test | httpx / supertest |

### Step 3: Write Tests

#### Unit Test Template (Python)
```python
import pytest
from src.module import function_under_test

class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self):
        """Test normal operation."""
        result = function_under_test(valid_input)
        assert result == expected_output

    def test_edge_case_empty_input(self):
        """Test with empty input."""
        result = function_under_test([])
        assert result == []

    def test_error_invalid_input(self):
        """Test error handling for invalid input."""
        with pytest.raises(ValueError, match="Invalid input"):
            function_under_test(invalid_input)
```

#### Unit Test Template (TypeScript)
```typescript
import { describe, it, expect } from 'vitest';
import { functionUnderTest } from '../src/module';

describe('functionName', () => {
  it('should handle normal operation', () => {
    const result = functionUnderTest(validInput);
    expect(result).toEqual(expectedOutput);
  });

  it('should handle edge case with empty input', () => {
    const result = functionUnderTest([]);
    expect(result).toEqual([]);
  });

  it('should throw error for invalid input', () => {
    expect(() => functionUnderTest(invalidInput)).toThrow('Invalid input');
  });
});
```

### Step 4: Run and Verify Failure

```bash
# Python
pytest tests/test_new_feature.py -v

# TypeScript
npm test -- tests/new-feature.test.ts
```

Tests MUST fail before implementation.

### Step 5: Report

```json
{
  "status": "tests_written",
  "tests_count": 5,
  "test_file": "tests/test_feature.py",
  "ready_for_implementation": true
}
```
