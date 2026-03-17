---
name: run-comprehensive-tests
description: Execute comprehensive test suite (Vitest/Jest) with coverage reporting and failure analysis. Returns structured output with test counts (total/passed/failed), coverage percentage, duration, and detailed failure information. Used for quality gates and CI/CD validation.
---

# Run Comprehensive Tests

Executes the complete test suite with coverage tracking and provides structured results for workflow decisions.

## Usage

This skill runs `npm run test` (or equivalent) and parses the output for test results and coverage metrics.

## Output Format

### All Tests Passing

```json
{
  "status": "pass",
  "summary": {
    "total": 45,
    "passed": 45,
    "failed": 0,
    "coverage": 87.5,
    "duration": "12.3s"
  },
  "failures": [],
  "canProceed": true
}
```

### Tests Failing

```json
{
  "status": "fail",
  "summary": {
    "total": 45,
    "passed": 42,
    "failed": 3,
    "coverage": 85.2,
    "duration": "11.8s"
  },
  "failures": [
    {
      "file": "src/components/CharacterCard.test.tsx",
      "test": "should render character portrait",
      "error": "Expected element to exist",
      "line": 42
    }
  ],
  "canProceed": false,
  "details": "3 test(s) failed"
}
```

## When to Use

- Quality Assurance phase (Conductor Phase 3)
- Before creating pull requests
- After implementing features or bug fixes
- As part of quality-gate workflow
- CI/CD pipeline validation

## Test Framework Support

- Vitest (primary)
- Jest (fallback)
- Coverage reporting via c8 or Istanbul

## Requirements

- Test framework installed (npm packages)
- Test scripts configured in package.json
- Typical script: `"test": "vitest run --coverage"`
