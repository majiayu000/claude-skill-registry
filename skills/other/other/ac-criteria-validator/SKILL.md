---
name: ac-criteria-validator
description: Validate acceptance criteria and feature completion. Use when checking if features pass, validating test results, verifying acceptance criteria, or determining feature completion status.
---

# AC Criteria Validator

Validate acceptance criteria and determine feature completion.

## Purpose

Validates that implemented features meet their acceptance criteria, determining when `passes` can transition from `false` to `true`.

## Quick Start

```python
from scripts.criteria_validator import CriteriaValidator

validator = CriteriaValidator(project_dir)
result = await validator.validate_feature("auth-001")
print(result.passes)  # True/False
print(result.criteria_results)
```

## Validation Result

```json
{
  "feature_id": "auth-001",
  "passes": true,
  "criteria_results": [
    {
      "criterion": "Valid registration creates user",
      "passed": true,
      "evidence": "test_valid_registration passed",
      "method": "test_execution"
    },
    {
      "criterion": "Invalid email shows error",
      "passed": true,
      "evidence": "test_invalid_email passed",
      "method": "test_execution"
    }
  ],
  "test_summary": {
    "total": 5,
    "passed": 5,
    "failed": 0,
    "coverage": 87.5
  },
  "validated_at": "2024-01-15T10:30:00Z"
}
```

## Validation Methods

### Test Execution
- Run associated test files
- Check all tests pass
- Verify coverage threshold
- Capture test output

### Code Analysis
- Check implementation exists
- Verify function signatures
- Validate error handling
- Check documentation

### Manual Criteria
- UI/UX requirements
- Performance benchmarks
- Security requirements
- Accessibility standards

## Validation Rules

```yaml
validation:
  require_all_tests_pass: true
  minimum_coverage: 80
  require_no_lint_errors: true
  require_type_checks: true

  custom_rules:
    - name: "no_console_logs"
      pattern: "console\\.log"
      severity: "warning"
```

## Workflow

1. **Load**: Get feature and criteria
2. **Discover**: Find related tests
3. **Execute**: Run test suite
4. **Analyze**: Check each criterion
5. **Report**: Return validation result

## State Transition

```
CRITICAL: passes can ONLY transition false → true

Before validation:
  {"passes": false, "status": "in_progress"}

After successful validation:
  {"passes": true, "status": "completed"}

NEVER:
  {"passes": true} → {"passes": false}
```

## Integration

- Input: Feature from `ac-state-tracker`
- Uses: `ac-test-generator` test files
- Output: Validation for state update

## API Reference

See `scripts/criteria_validator.py` for full implementation.
