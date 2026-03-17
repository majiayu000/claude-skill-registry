---
name: mandatory-tdd
description: Enforces Test-Driven Development (TDD) with BDD-style tests and mandatory test execution. Use when (1) Writing any new code or feature, (2) Fixing bugs, (3) Refactoring existing code, (4) Creating pull requests, (5) Closing issues. CRITICAL RULE - Tests MUST be actually executed with proof of passing status and coverage >= 80% before ANY commit, PR, or issue closure.
---

# Mandatory TDD/BDD Testing Strategy

## Core Principles

* **BDD Style:** Use `describe/it` syntax for unit, integration, and functional/API tests
* **Test-First:** Write failing tests before implementation
* **Deterministic:** Use data-testid, role, or label selectors (never brittle CSS/XPath)
* **Fast & Light:** Prefer fast unit/integration tests; save heavy e2e for nightly unless required

## Example BDD Structure

```js
describe('Calculator', () => {
  describe('addition', () => {
    it('adds two positive numbers', () => {
      expect(add(5, 7)).to.equal(12);
    });
  });
});
```

## 🚨 MANDATORY TEST EXECUTION REQUIREMENT 🚨

**BEFORE claiming tests pass or closing any issue:**

1. **ACTUALLY RUN THE TESTS** - Execute test suite with coverage
2. **VERIFY THEY PASS** - Confirm all tests show green/passing status
3. **CHECK COVERAGE** - Verify minimum 80% coverage requirement met
4. **INCLUDE OUTPUT** - Paste actual test execution output in PR/commit/issue

### ❌ ABSOLUTELY FORBIDDEN

* Writing tests but NOT running them
* Claiming "All tests passing" without proof
* Stating "80%+ coverage" without actual coverage report
* Closing issues without running test suite
* Creating PRs without executing pytest/jest/etc.
* Assuming tests work based on syntax checking alone

### ✅ REQUIRED WORKFLOW

**Backend (Python/FastAPI):**
```bash
cd /Users/aideveloper/core/src/backend
python3 -m pytest tests/test_your_feature.py -v --cov=app.your.module --cov-report=term-missing

# Verify output shows:
# - ✓ All tests passed (green checkmarks)
# - ✓ Coverage >= 80%
# - ✓ No import errors or test failures
```

**Frontend (TypeScript/React):**
```bash
cd /Users/aideveloper/core/AINative-website
npm test -- --coverage

# Verify output shows:
# - ✓ All tests passed
# - ✓ Coverage >= 80% for statements, branches, functions, lines
```

### Evidence Requirement

Every PR, commit, or issue closure involving tests MUST include:

```
## Test Execution Evidence

### Command Run:
`pytest tests/test_showcase_videos.py -v --cov=app.api.v1.endpoints.showcase_videos`

### Output:
```
test_create_showcase_video PASSED                                        [  5%]
test_tech_stack_validation PASSED                                        [ 10%]
==================== 20 passed in 3.42s ====================
Coverage: 87%
```

### Coverage Report:
```
app/api/v1/endpoints/showcase_videos.py    422    35    87%
app/schemas/video.py                        192    18    91%
```
```

## Why This Matters

* **Prevents false confidence** - Tests may have import errors, assertion failures
* **Catches infrastructure issues** - Broken test setup, missing dependencies
* **Validates coverage claims** - Actual coverage may be lower than estimated
* **Ensures production readiness** - Code that doesn't pass tests shouldn't ship
* **Saves debugging time** - Finding test failures BEFORE merge, not after

## Enforcement

* **MANDATORY** requirement with **NO EXCEPTIONS**
* Tests must be run LOCALLY before any git commit
* Test output must be included in PR descriptions
* Coverage reports must show actual percentages, not estimates
* If tests cannot run due to infrastructure issues, **DOCUMENT THE ISSUE** and fix it before proceeding
* Never claim "tests passing" without proving it with actual command output

## Violation Consequences

* Broken code merged to main branch
* Production bugs from untested code
* Wasted time debugging issues that tests would have caught
* Loss of confidence in test suite
* Team frustration from preventable bugs

**THIS IS A ZERO-TOLERANCE RULE. ALWAYS RUN TESTS AND PROVIDE PROOF.**

## Reference Files

See `references/bdd-patterns.md` for detailed BDD test pattern examples across unit, integration, and API tests.

See `references/coverage-requirements.md` for detailed coverage configuration, thresholds, and exclusion patterns.
