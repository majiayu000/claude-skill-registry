---
name: testing-principles
description: Core testing principles for any language. Use when writing tests or reviewing test code without a language-specific testing skill loaded.
durability: encoded-preference
---

# Testing Principles

## Test Pyramid (No Overlap Strategy)

Avoid duplication - write appropriate tests at each layer:

1. **E2E Tests** (ATDD approach, critical flows)
   - Critical user flows (main success + key error scenarios)
   - Use Gherkin (.feature files) with Given-When-Then format
   - Use Scenario Outline + Examples table for multiple cases
   - Write scenarios BEFORE implementation (ATDD)

2. **Integration Tests** (majority of tests)
   - API endpoints, database operations
   - Edge cases and boundary conditions not covered by E2E
   - Component interactions

3. **Unit Tests** (as needed)
   - Pure logic not coverable by Integration tests
   - Utility functions, complex calculations

## Test-Driven Development

**Always write tests before implementation.** See `/tdd` command for the full RED-GREEN-REFACTOR workflow.

## Cross-US Test Safety Net

When implementing multiple User Stories sequentially, tests from earlier USs serve as the safety net for refactoring their code. Previously-committed code with passing tests is NOT frozen -- it is actively refactorable.

- Tests from US1 protect US1's behavior during US2's REFACTOR phase
- If tests stay GREEN after refactoring, the refactoring is safe
- Duplication across US boundaries is a refactoring target, same as duplication within a single US

## Characterization Tests (Legacy Code)

**Characterization tests capture what code actually does, not what it should do.** Write them before refactoring any untested legacy code.

**When to use**: REFACTOR phase needs to modify code that:
- Was written before the project adopted TDD
- Has no existing test coverage
- Would be risky to change without verification

### Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Refactoring untested code without characterization tests | Write characterization tests first, confirm GREEN, then refactor |
| Writing characterization tests for what code *should* do | Capture what code *actually* does (warts and all) |
| Skipping characterization tests for "simple" legacy code | If it has no tests, it needs characterization tests before refactoring |

## Test Structure (AAA Pattern)

Every test should follow Arrange-Act-Assert:

```
// Arrange - Set up test data and conditions
// Act - Execute the code under test
// Assert - Verify the expected outcome
```

Keep tests focused: one behavior per test.

## Common Testing Mistakes

### Test User-Visible Behavior, Not Implementation

```typescript
// ❌ WRONG: Testing internal state
expect(component.state.count).toBe(5)

// ✅ CORRECT: Test what users see
expect(screen.getByText('Count: 5')).toBeInTheDocument()
```

### Use Semantic Selectors, Not Brittle CSS

```typescript
// ❌ WRONG: Breaks easily
await page.click('.css-class-xyz')

// ✅ CORRECT: Resilient to changes
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
```

### Prefer Integration Tests Over Excessive Mocking

Reserve mocks for external services and non-deterministic behavior. Prefer real dependencies where feasible.

### Keep Tests Independent

```typescript
// ❌ WRONG: Tests depend on each other
test('creates user', () => { /* ... */ })
test('updates same user', () => { /* depends on previous */ })

// ✅ CORRECT: Each test sets up its own data
test('creates user', () => { const user = createTestUser() })
test('updates user', () => { const user = createTestUser() })
```

## Quality Checklist

- [ ] Tests cover acceptance criteria
- [ ] Scenario Outline + Examples cover edge cases
- [ ] Tests are independent (no shared state)
- [ ] Test names describe the behavior being tested
- [ ] Tests verify user-visible behavior, not implementation
- [ ] Selectors are semantic (text, role, data-testid)
