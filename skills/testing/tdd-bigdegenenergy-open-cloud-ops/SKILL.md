---
name: tdd
description: Test-Driven Development patterns and red-green-refactor workflow. Auto-triggers when writing tests first, implementing TDD, or discussing test coverage.
---

# Test-Driven Development

## The Red-Green-Refactor Cycle

1. **RED**: Write a failing test that defines expected behavior
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code quality while keeping tests green

## Critical Rules

- Never write production code without a failing test first
- Only write enough code to make the current test pass
- Refactor only when tests are green
- Run tests after every change

## Test Structure (AAA Pattern)

```
// Arrange - Set up test data and conditions
// Act - Execute the code under test
// Assert - Verify the expected outcome
```

## Test Naming Convention

```
test_[unit]_[scenario]_[expected_result]

Examples:
- test_calculateTotal_emptyCart_returnsZero
- test_userLogin_invalidPassword_throwsAuthError
- test_parseDate_invalidFormat_returnsNull
```

## Test Doubles

| Type | Purpose | Use When |
|------|---------|----------|
| **Stub** | Returns canned data | Testing with specific inputs |
| **Mock** | Verifies interactions | Checking method calls |
| **Fake** | Working implementation | Need realistic behavior |
| **Spy** | Records calls | Observing side effects |

## Coverage Targets

- Unit tests: >90% line coverage
- Integration tests: Critical paths covered
- E2E tests: Happy paths + key error scenarios

## Anti-Patterns to Avoid

- Testing implementation details (test behavior, not internals)
- Overly specific assertions (leads to brittle tests)
- Test interdependence (each test must be isolated)
- Testing trivial code (getters/setters)
- Ignoring flaky tests (fix or remove immediately)

## TDD for Different Contexts

### API Endpoints
1. Test request validation
2. Test business logic
3. Test response format
4. Test error handling

### UI Components
1. Test rendering with props
2. Test user interactions
3. Test state changes
4. Test accessibility

### Database Operations
1. Test CRUD operations
2. Test constraints/validation
3. Test transactions
4. Test edge cases (null, empty)
