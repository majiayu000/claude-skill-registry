---
name: tdd-workflow
description: Test-Driven Development workflow enforcement with RED-GREEN-REFACTOR cycle. Use when implementing features test-first or improving test coverage.
---

# Test-Driven Development (TDD) Workflow

A disciplined approach to development where tests drive design and implementation.

## The TDD Mantra

> "Never write a line of code without a failing test."

## The RED-GREEN-REFACTOR Cycle

### RED Phase: Write a Failing Test

**Goal**: Define the expected behavior BEFORE implementation.

**Rules**:

1. Write the smallest test that fails
2. Test must fail for the RIGHT reason
3. Test should clearly express intent
4. Don't write implementation yet

**Example**:

```typescript
// RED: Test the behavior we want
describe("Calculator", () => {
  it("should add two numbers", () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// Run: npm test
// Result: FAIL - Calculator is not defined
// This is RED ✓
```

**Checklist**:

- [ ] Test is written
- [ ] Test fails when run
- [ ] Failure message is clear
- [ ] Test name describes expected behavior

---

### GREEN Phase: Make the Test Pass

**Goal**: Write the MINIMUM code to pass the test.

**Rules**:

1. Do the simplest thing that works
2. Don't add extra features
3. Don't optimize
4. Just make it green

**Example**:

```typescript
// GREEN: Minimum implementation to pass
class Calculator {
  add(a: number, b: number): number {
    return a + b; // Simplest thing that works
  }
}

// Run: npm test
// Result: PASS
// This is GREEN ✓
```

**Checklist**:

- [ ] Test passes
- [ ] No extra code added
- [ ] Implementation is minimal

---

### REFACTOR Phase: Improve the Code

**Goal**: Clean up while keeping tests green.

**Rules**:

1. Only refactor with passing tests
2. Run tests after each change
3. Improve design, not behavior
4. Small, incremental changes

**Examples of refactoring**:

- Extract methods
- Rename for clarity
- Remove duplication
- Improve performance
- Add types/documentation

**Checklist**:

- [ ] Tests still pass
- [ ] Code is cleaner
- [ ] No behavior changed
- [ ] Ready for next RED

---

## TDD in Practice

### Starting a New Feature

```
1. Write high-level acceptance test (may not run yet)
2. Write first unit test (RED)
3. Implement minimum code (GREEN)
4. Refactor if needed (REFACTOR)
5. Repeat 2-4 until feature complete
6. Verify acceptance test passes
```

### Test Structure (AAA Pattern)

```typescript
it("should [behavior] when [condition]", () => {
  // Arrange - Set up test data and dependencies
  const user = createTestUser({ role: "admin" });
  const service = new UserService();

  // Act - Execute the code under test
  const result = service.getPermissions(user);

  // Assert - Verify expected outcomes
  expect(result).toContain("delete");
  expect(result).toContain("edit");
});
```

### Test Naming Convention

```
[Unit]_[Scenario]_[ExpectedResult]
```

Examples:

- `add_withPositiveNumbers_returnsSum`
- `login_withInvalidPassword_throwsAuthError`
- `getUser_whenNotFound_returnsNull`

---

## Test Categories

### Unit Tests

- Single function/class in isolation
- Mock all dependencies
- Fast (<10ms per test)
- Run constantly during development

### Integration Tests

- Multiple components together
- Real database (test instance)
- Slower but more realistic
- Run before commits

### End-to-End Tests

- Full system through UI
- Slowest, most realistic
- Run in CI/CD pipeline
- Cover critical user paths

---

## TDD Best Practices

### DO:

- Start with the simplest case
- Write one test at a time
- Keep tests independent
- Test behavior, not implementation
- Use descriptive test names
- Commit after each green

### DON'T:

- Write code before tests
- Test private methods directly
- Test framework code
- Overfit tests to implementation
- Skip the refactor phase

---

## Edge Cases to Test

Always test:

- Empty inputs (null, undefined, [], {}, '')
- Boundary values (0, -1, MAX_INT, min/max dates)
- Error conditions (network fail, invalid input)
- Permission boundaries
- Concurrent access
- Unicode/special characters

---

## Test Coverage Guidelines

| Metric     | Minimum | Target |
| ---------- | ------- | ------ |
| Statements | 70%     | 85%    |
| Branches   | 70%     | 80%    |
| Functions  | 80%     | 90%    |
| Lines      | 70%     | 85%    |

Coverage is a metric, not a goal. 100% coverage doesn't mean bug-free.

---

## Quick Reference

```
RED    → Write failing test (define behavior)
GREEN  → Minimum code to pass (make it work)
REFACTOR → Clean up (make it right)
COMMIT → Save progress (make it permanent)
```

---

## Common TDD Mistakes

| Mistake                | Problem       | Solution               |
| ---------------------- | ------------- | ---------------------- |
| Testing implementation | Brittle tests | Test behavior/outcomes |
| Tests too large        | Hard to debug | Smaller, focused tests |
| Shared state           | Flaky tests   | Isolate each test      |
| Slow tests             | Skipped tests | Mock external deps     |
| Testing obvious code   | Wasted time   | Focus on logic         |
