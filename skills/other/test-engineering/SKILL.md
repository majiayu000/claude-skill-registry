---
name: test-engineering
description: Use when the Integrator is writing unit tests, e2e tests, designing test strategies, improving test coverage, creating test fixtures, or mocking dependencies. Activates for any testing-related work including TDD, test refactoring, or test debugging.
version: 1.0.0
---

# Test Engineering Expertise

## When This Applies

Apply this guidance when:
- Writing unit tests for new or existing code
- Designing end-to-end test scenarios
- Creating test fixtures and mocks
- Evaluating test coverage
- Debugging failing tests

## Unit Test Principles

### Structure: Arrange-Act-Assert

Every test should follow this pattern:
```
test("should calculate total with tax", () => {
  // Arrange — Set up test data and dependencies
  const cart = createCart([{ price: 100 }, { price: 50 }]);
  const taxRate = 0.1;

  // Act — Execute the code under test
  const total = calculateTotal(cart, taxRate);

  // Assert — Verify the result
  expect(total).toBe(165);
});
```

### What to Test

| Test | Example |
|------|---------|
| **Happy path** | Valid input produces expected output |
| **Edge cases** | Empty input, boundary values, max/min |
| **Error cases** | Invalid input, missing data, exceptions |
| **State transitions** | Before/after mutation operations |

### What NOT to Test

- Private implementation details (test behavior, not internals)
- Third-party library functionality
- Trivial getters/setters with no logic
- The programming language itself

### Naming Convention

Test names should describe the scenario and expected outcome:
- `should return empty array when no items match filter`
- `should throw ValidationError when email is invalid`
- `should update timestamp after successful save`

## E2E Test Design

### Scenario Structure

```
Feature: User authentication
  Scenario: Successful login
    Given a registered user with email "user@example.com"
    When they submit valid credentials
    Then they receive an auth token
    And they can access protected resources
```

### E2E Best Practices

1. **Test user-visible behavior** — Not internal APIs
2. **Use realistic data** — Don't test with "test123"
3. **Independent tests** — Each test sets up and tears down its own state
4. **Stable selectors** — Use data-testid, not CSS classes
5. **Reasonable timeouts** — Account for async operations

## Mocking Strategy

### When to Mock

| Mock | Don't Mock |
|------|-----------|
| External APIs and services | The code under test |
| Database in unit tests | Pure functions |
| File system in unit tests | Data transformations |
| Time/randomness | Simple dependencies |

### Mock Levels

1. **Stub** — Returns canned data (simplest)
2. **Spy** — Records calls for verification
3. **Mock** — Stubs + spies + expected behavior
4. **Fake** — Working alternative implementation (e.g., in-memory database)

## Test Coverage Guidelines

- Aim for meaningful coverage, not 100% line coverage
- New features: cover all public interfaces and error paths
- Bug fixes: add a regression test that fails without the fix
- Critical paths (auth, payments, data mutations): high coverage required
- Utilities and helpers: cover edge cases thoroughly

## Pre-Commit Test Checklist

Before committing (via `/commit-work`), verify:
1. All existing tests still pass
2. New tests added for new functionality
3. Regression test added for bug fixes
4. No test depends on external services without mocking
5. No flaky tests (run twice to confirm)
6. Test names clearly describe what they verify
