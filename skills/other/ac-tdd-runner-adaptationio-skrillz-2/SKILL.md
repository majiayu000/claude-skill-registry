---
name: ac-tdd-runner
description: Run TDD cycle for feature implementation. Use when implementing features with RED-GREEN-REFACTOR, running test-driven development, automating TDD workflow, or ensuring test-first development.
---

# AC TDD Runner

Automate the Test-Driven Development cycle for feature implementation.

## Purpose

Enforces the RED-GREEN-REFACTOR cycle, ensuring all features are implemented with test-first methodology for quality and maintainability.

## Quick Start

```python
from scripts.tdd_runner import TDDRunner

runner = TDDRunner(project_dir)
result = await runner.run_cycle(feature)
```

## TDD Cycle

### RED Phase
Write failing tests first:
```python
red_result = await runner.red_phase(feature)
# Creates test file with failing tests
# Verifies tests actually fail
```

### GREEN Phase
Implement minimum code to pass:
```python
green_result = await runner.green_phase(feature)
# Implements code
# Runs tests until all pass
# Minimum necessary implementation
```

### REFACTOR Phase
Clean up while tests pass:
```python
refactor_result = await runner.refactor_phase(feature)
# Improve code structure
# Ensure tests still pass
# Apply coding standards
```

## Cycle Result

```json
{
  "feature_id": "auth-001",
  "cycle_complete": true,
  "phases": {
    "red": {
      "success": true,
      "tests_created": 5,
      "all_tests_fail": true
    },
    "green": {
      "success": true,
      "iterations": 3,
      "all_tests_pass": true
    },
    "refactor": {
      "success": true,
      "changes_made": ["extracted_helper", "renamed_variable"],
      "tests_still_pass": true
    }
  },
  "coverage": 92.5,
  "duration_ms": 120000
}
```

## RED Phase Details

1. Generate test file from feature test_cases
2. Write test functions with proper structure
3. Run tests to verify they fail
4. If tests pass unexpectedly, add more specific assertions

## GREEN Phase Details

1. Analyze failing tests
2. Write minimum implementation
3. Run tests
4. If tests fail, iterate on implementation
5. Stop when all tests pass

## REFACTOR Phase Details

1. Identify code smells
2. Apply refactoring patterns
3. Run tests after each change
4. Revert if tests fail
5. Continue until code is clean

## Configuration

```json
{
  "max_green_iterations": 10,
  "coverage_threshold": 80,
  "refactoring_patterns": [
    "extract_method",
    "rename_for_clarity",
    "remove_duplication"
  ],
  "test_framework": "pytest"
}
```

## Integration

- Uses: `ac-test-generator` for RED phase
- Uses: `ac-criteria-validator` for GREEN verification
- Reports to: `ac-task-executor`

## API Reference

See `scripts/tdd_runner.py` for full implementation.
