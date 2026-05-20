---
name: run-comprehensive-tests
description: Execute comprehensive test suite with validation, coverage reporting, and failure analysis. Works with any TypeScript/JavaScript testing framework (Jest, Vitest, Mocha, etc.). Returns structured output with pass/fail status, coverage metrics, and detailed error analysis.
---

# Run Comprehensive Tests

## Purpose

Execute the complete test suite for TypeScript/JavaScript projects, validate results, and provide structured output for workflow decisions.

## When to Use

- During Quality Assurance phase of development workflows
- Before creating pull requests
- After implementing new features or bug fixes
- When validating refactoring changes
- As part of CI/CD pipeline validation

## Supported Test Frameworks

Works with any test framework:
- **Vitest**: Modern Vite-based testing
- **Jest**: Popular React/Node testing
- **Mocha/Chai**: Traditional Node testing
- **Jasmine**: Behavior-driven testing
- Detects via package.json scripts or direct commands

## Instructions

### Step 1: Run Test Suite

```bash
# Run all tests with coverage
npm run test

# For CI environments, use CI mode
CI=true npm run test -- --coverage
```

### Step 2: Parse Results

Extract key metrics from test output:
- **Total tests**: Number of test cases
- **Passed**: Successfully passing tests
- **Failed**: Failing tests (with details)
- **Coverage**: Code coverage percentage
- **Duration**: Test execution time

### Step 3: Analyze Failures (Enhanced)

If tests fail, parse actual error messages from output:

```bash
# Extract failure details from test output
# Look for patterns like:
# - "FAIL src/components/Card.test.tsx"
# - "  ● Test suite failed to run"
# - "  Expected: true, Received: false"
# - "    at Object.<anonymous> (src/file.ts:42:15)"

# Parse each failure:
for FAILURE in $(grep -n "FAIL\|●\|Error:" test-output.txt); do
  # Extract file path
  FILE=$(echo "$FAILURE" | grep -oP 'src/[^:]+\.tsx?')

  # Extract error message (not hardcoded "Test failed")
  ERROR_MSG=$(echo "$FAILURE" | grep -oP '(Expected|Error|AssertionError).*' | head -1)

  # Extract line number from stack trace
  LINE=$(echo "$FAILURE" | grep -oP 'at.*:(\d+):' | grep -oP '\d+' | head -1)

  # Store for structured output
done
```

Categorize failure types:
- **Assertion failures**: Expected vs Received mismatches
- **Type errors**: TypeScript type mismatches
- **Timeout errors**: Test exceeded time limit
- **Import errors**: Module resolution failures
- **Syntax errors**: JavaScript/TypeScript syntax issues

### Step 4: Return Structured Results

Provide results in this format:

```json
{
  "status": "pass" | "fail",
  "summary": {
    "total": 45,
    "passed": 45,
    "failed": 0,
    "coverage": 87.5,
    "duration": "12.3s"
  },
  "failures": [
    {
      "file": "src/components/CharacterCard.test.tsx",
      "test": "should render character portrait",
      "error": "Expected element to exist",
      "line": 42
    }
  ]
}
```

## Exit Codes

- **0**: All tests passed
- **1**: One or more tests failed
- **2**: Test configuration error

## Common Issues

### Issue: Tests timeout
**Solution**: Increase timeout in `vite.config.ts`:
```ts
test: {
  testTimeout: 10000, // 10 seconds
}
```

### Issue: Coverage below threshold
**Solution**: Check `package.json` for coverage thresholds and add tests for uncovered code

### Issue: Import errors in tests
**Solution**: Verify test setup in `vitest.setup.ts` and ensure all mocks are configured

## Integration with Conductor Workflow

The Conductor agent uses this skill in Phase 3 (Quality Assurance):

```markdown
**Phase 3, Step 1**: Run comprehensive tests

Using the `run-comprehensive-tests` skill:
- Execute full test suite
- Validate all tests pass
- Check coverage meets 80% threshold
- If failures: delegate to debugger agent
```

## Related Skills

- `validate-coverage` - Deep dive into coverage metrics
- `debug-test-failures` - Systematic test failure debugging
- `quality-gate` - Complete quality validation workflow

## Best Practices

1. **Always run tests before committing** - Prevents broken builds
2. **Fix tests immediately** - Don't accumulate test debt
3. **Monitor coverage trends** - Aim for increasing coverage over time
4. **Categorize failures** - Helps route to appropriate debugging approach

## Examples

See `examples.md` in this skill directory for detailed examples of test execution and result parsing.
