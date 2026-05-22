---
name: testing-workflow
description: Run and manage functional tests (unit, integration, E2E, mutation). Use when running tests, debugging test failures, ensuring test coverage, or fixing mutation testing issues. Covers PHPUnit, Behat, and Infection. For K6 load/performance tests, use the load-testing skill instead.
---

# Testing Workflow Skill

## Context (Input)

- Code changes require test validation
- Test failures need debugging
- Coverage/mutation targets must be met

## Task (Function)

Execute appropriate test suite and ensure 100% pass rate with required coverage.

**Note**: For K6 load/performance testing, see [load-testing skill](../load-testing/SKILL.md).

## Test Commands Quick Reference

| Test Type   | Command                  | Runtime  | Coverage | Location           |
| ----------- | ------------------------ | -------- | -------- | ------------------ |
| Unit        | `make unit-tests`        | 2-3 min  | 100%     | tests/Unit/        |
| Integration | `make integration-tests` | 3-5 min  | Full     | tests/Integration/ |
| E2E (Behat) | `make behat`             | 5-10 min | BDD      | features/          |
| All Tests   | `make all-tests`         | 8-15 min | 100%     | All                |
| Mutation    | `make infection`         | Variable | 100% MSI | Unit tests         |

**Load Testing**: Use [load-testing skill](../load-testing/SKILL.md) for K6 performance tests.

## Execution Workflow

### Step 1: Run Tests

```bash
make unit-tests           # For quick validation
make all-tests            # For comprehensive check
```

### Step 2: Check Results

- ✅ **All Pass + 100% coverage** → Complete
- ❌ **Failures detected** → Go to Step 3

### Step 3: Debug Failures

Identify failure type and apply fix:

| Failure Type      | Debug Command           | Common Fixes                              |
| ----------------- | ----------------------- | ----------------------------------------- |
| Assertion failure | PHPUnit output          | Fix logic, update test expectations       |
| Coverage < 100%   | Coverage report         | Add missing test cases                    |
| Escaped mutants   | `make infection` output | Test edge cases, strengthen assertions    |
| Behat scenario    | Feature output          | Fix application logic or step definitions |
| Type error        | Stack trace             | Fix type hints, mock returns              |

### Step 4: Fix and Re-test

```bash
# Fix the code/tests
make unit-tests           # Re-run to verify fix
```

Repeat Steps 2-4 until all tests pass with 100% coverage.

## Mutation Testing (Infection)

**Goal**: 100% Mutation Score Indicator (MSI) - Zero escaped mutants

### Run Mutation Tests

```bash
make infection
```

### Fix Escaped Mutants

1. Review mutation diff in output
2. Add test case for uncaught mutation
3. Strengthen assertion specificity
4. Consider refactoring for testability

**Example**: If mutant changes `>` to `>=`, add boundary test case.

## Faker Usage in Tests

**Setup**: Tests extend `UnitTestCase` which provides `$this->faker`

```php
// Good - Dynamic test data
$this->faker->email();
$this->faker->lexify('??');  // 2 random letters
$this->faker->unique()->ulid();

// Bad - Hardcoded values
'test@example.com'
'AB'
```

**Available**:

- `$this->faker->ulid()` - Domain ULID via custom provider
- All standard Faker methods (email, name, word, etc.)

## Load Testing

**Commands**:

```bash
make smoke-load-tests      # Minimal load, 5-10 min
make average-load-tests    # Normal traffic, 15-25 min
make stress-load-tests     # High load, 20-30 min
make spike-load-tests      # Extreme spikes, 25-35 min
```

**Prerequisites**:

- Test database seeded (`make setup-test-db`)
- Docker containers running (`make start`)
- K6 Docker image built

## Constraints (Parameters)

**NEVER**:

- Cancel long-running tests mid-execution
- Commit with failing tests
- Accept coverage < 100%
- Allow escaped mutants
- Run tests outside Docker (use `make` commands)

**ALWAYS**:

- Use Faker for dynamic test data
- Mock external dependencies in unit tests
- Use real DB in integration tests
- Ensure deterministic test results

## Format (Output)

**Unit Tests Success**:

```
OK (X tests, Y assertions)
✅ COVERAGE SUCCESS: Line coverage is 100%
```

**Mutation Testing Success**:

```
100% MSI
0 escaped mutants
```

## Verification Checklist

- [ ] All tests pass
- [ ] Coverage is 100%
- [ ] Zero escaped mutants (if running mutation tests)
- [ ] No hardcoded test values (use Faker)
- [ ] Tests run in Docker container via `make`
