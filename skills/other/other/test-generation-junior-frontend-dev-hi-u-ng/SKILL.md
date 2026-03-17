---
name: test-generation
description: Generate comprehensive tests following project testing patterns.
  Use after implementing features.
---

# Test Generation Skill

## Purpose
Create consistent, comprehensive tests.

## Test Patterns

### Unit Test Pattern
Reference: [patterns/unit-tests.md](patterns/unit-tests.md)

```typescript
describe('[Unit Under Test]', () => {
  describe('[method/function]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = ...;
      const expected = ...;

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toEqual(expected);
    });

    it('should throw [error] when [invalid condition]', () => {
      // Arrange
      const invalidInput = ...;

      // Act & Assert
      expect(() => functionUnderTest(invalidInput))
        .toThrow(ExpectedError);
    });
  });
});
```

### Integration Test Pattern
Reference: [patterns/integration-tests.md](patterns/integration-tests.md)

### E2E Test Pattern
Reference: [patterns/e2e-tests.md](patterns/e2e-tests.md)

## Coverage Targets

| Type | Lines | Functions | Branches |
|------|-------|-----------|----------|
| Unit | 80% | 80% | 70% |
| Integration | 60% | 60% | 50% |
| E2E | Critical paths | - | - |

## Test Naming Convention

```
[should/does] [expected behavior] [when/given] [condition]
```

Examples:
- `should return user when valid ID provided`
- `should throw NotFoundError when user does not exist`
- `should disable button when form is invalid`

## What to Test

- Happy path (normal operation)
- Edge cases (boundaries)
- Error cases (exceptions)
- State transitions

## Test Structure

### AAA Pattern
```typescript
// Arrange - set up test data and conditions
const input = createTestInput();
const mockService = createMock();

// Act - execute the code under test
const result = await functionUnderTest(input);

// Assert - verify the outcome
expect(result).toEqual(expectedOutput);
expect(mockService.method).toHaveBeenCalledWith(expectedArgs);
```

### BDD Style
```typescript
describe('User Service', () => {
  describe('when creating a user', () => {
    it('should save the user to the database', () => { });
    it('should send a welcome email', () => { });
    it('should return the created user', () => { });
  });

  describe('when the email is invalid', () => {
    it('should throw a ValidationError', () => { });
  });
});
```

## Test Template
Use: [templates/test-template.ts](templates/test-template.ts)

## Best Practices

### Do
- Test behavior, not implementation
- Use descriptive test names
- Keep tests independent
- Use factories for test data
- Mock external dependencies

### Don't
- Test private methods directly
- Share state between tests
- Use production data in tests
- Over-mock (test should be meaningful)
- Write flaky tests

## Storage Location
Save test reports to: `docs/reviews/test-report-{session}.md`
