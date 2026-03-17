---
description: Run comprehensive test suite (unit, integration, E2E) with coverage reporting
handoffs:
  - label: Fix Test Failures
    agent: backend-engineer
    prompt: Fix the failing tests identified in the test report
    send: false
---

## User Input

```text
$ARGUMENTS
```

Test type options: `unit`, `integration`, `e2e`, `security`, `all` (default: all)

## Task

Run the test suite for the keto meal plan project and generate a comprehensive report.

### Steps

1. **Parse Arguments**:
   - If `$ARGUMENTS` is empty or "all": Run all tests
   - If `$ARGUMENTS` is "unit": Run only unit tests
   - If `$ARGUMENTS` is "integration": Run only integration tests
   - If `$ARGUMENTS` is "e2e": Run only E2E tests
   - If `$ARGUMENTS` is "security": Run only security tests

2. **Navigate to Backend Directory**:
   ```bash
   cd backend
   ```

3. **Run Tests Based on Type**:

   **For Unit Tests**:
   ```bash
   pytest tests/unit/ -v --cov=src/lib --cov=src/services --cov-report=term --cov-report=html:coverage_html
   ```

   **For Integration Tests**:
   ```bash
   pytest tests/integration/ -v
   ```

   **For E2E Tests**:
   ```bash
   pytest tests/e2e/ -v
   ```

   **For Security Tests**:
   ```bash
   pytest tests/security/ -v
   ```

   **For All Tests**:
   ```bash
   pytest tests/ -v --cov=src --cov-report=term --cov-report=html:coverage_html
   ```

4. **Generate Test Report**:
   - Capture test results (passed/failed/skipped counts)
   - Show coverage percentage for unit tests
   - List any failing tests with error messages
   - Show test execution time

5. **Output Summary**:
   ```
   ✅ Test Results Summary
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Test Type: [unit/integration/e2e/all]

   Passed:  XX tests
   Failed:  XX tests
   Skipped: XX tests

   Coverage: XX% (unit tests only)

   [If failures exist, list them here]

   HTML Coverage Report: backend/coverage_html/index.html
   ```

6. **Recommendations**:
   - If coverage <80%: "⚠️ Coverage below 80% target. Add tests for uncovered code."
   - If failures exist: "❌ Fix failing tests before proceeding."
   - If all pass: "✅ All tests passing! Safe to proceed."

## Example Usage

```bash
/test              # Run all tests
/test unit         # Run only unit tests
/test integration  # Run only integration tests
/test e2e          # Run E2E tests
```

## Exit Criteria

- Test execution completes successfully
- Test report generated and displayed
- Coverage report available at `backend/coverage_html/index.html` (for unit tests)
