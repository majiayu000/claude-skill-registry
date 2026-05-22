---
name: "testing-skill"
description: "TDD patterns, test writing strategies, coverage guidance, mocking patterns. Use when: write tests, TDD, test coverage, unit test, integration test, E2E test, mocking, test organization, pytest, vitest, jest."
---

<objective>
Comprehensive testing skill covering TDD workflow, test pyramid strategy, mocking patterns, and coverage guidance. Framework-agnostic patterns applicable to pytest, vitest, jest, and other testing frameworks.

This skill emphasizes writing tests that provide confidence without becoming maintenance burdens. Tests should be fast, reliable, and focused on behavior rather than implementation details.
</objective>

<core_principles>
## The Testing Mindset

1. **Tests are documentation** - A failing test is a specification that hasn't been implemented
2. **Test behavior, not implementation** - Tests should survive refactoring
3. **Fast feedback loops** - Unit tests run in milliseconds, not seconds
4. **Isolation by default** - Each test should be independent
5. **Arrange-Act-Assert** - Clear structure in every test
</core_principles>

<tdd_workflow>
## TDD: Red-Green-Refactor

```
┌─────────────────────────────────────────────────────────┐
│                    TDD CYCLE                             │
│                                                          │
│    ┌─────────┐                                          │
│    │   RED   │ ◄─── Write a failing test                │
│    └────┬────┘                                          │
│         │                                                │
│         ▼                                                │
│    ┌─────────┐                                          │
│    │  GREEN  │ ◄─── Write minimum code to pass          │
│    └────┬────┘                                          │
│         │                                                │
│         ▼                                                │
│    ┌─────────┐                                          │
│    │REFACTOR │ ◄─── Clean up while tests stay green     │
│    └────┬────┘                                          │
│         │                                                │
│         └──────────────► Back to RED                    │
└─────────────────────────────────────────────────────────┘
```

### The Rules

1. **Write a failing test first** - Never write production code without a failing test
2. **Write only enough test to fail** - Compilation failures count as failures
3. **Write only enough code to pass** - No more, no less
4. **Refactor only when green** - Never refactor with failing tests

### Common TDD Mistakes

| Mistake | Why It's Wrong | Instead |
|---------|----------------|---------|
| Writing tests after code | Tests become confirmation bias | Red-Green-Refactor |
| Testing private methods | Tests implementation, not behavior | Test public interface |
| Big leaps in test complexity | Hard to debug failures | Baby steps |
| Skipping refactor step | Technical debt accumulates | Always clean up |
</tdd_workflow>

<test_pyramid>
## The Test Pyramid

```
                    ┌───────────┐
                    │    E2E    │  Few, slow, expensive
                    │   Tests   │  (minutes)
                    └─────┬─────┘
                          │
               ┌──────────┴──────────┐
               │   Integration Tests  │  Some, medium speed
               │   (API, Database)    │  (seconds)
               └──────────┬───────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │          Unit Tests                │  Many, fast, cheap
        │    (Functions, Components)         │  (milliseconds)
        └────────────────────────────────────┘
```

### Distribution Guidelines

| Type | Percentage | Speed | Scope |
|------|------------|-------|-------|
| Unit | 70-80% | <10ms each | Single function/component |
| Integration | 15-25% | <1s each | Multiple components, DB |
| E2E | 5-10% | <30s each | Full user flows |

### What to Test Where

**Unit Tests:**
- Pure functions
- Business logic
- Data transformations
- Validation rules
- Component rendering

**Integration Tests:**
- API endpoints
- Database operations
- Service interactions
- Component integration

**E2E Tests:**
- Critical user flows (login, checkout)
- Happy paths only
- Smoke tests
</test_pyramid>

<when_to_mock>
## Mocking Strategy

### The London vs Detroit Schools

**London School (Mockist):**
- Mock all dependencies
- Test in complete isolation
- Tests are very focused

**Detroit School (Classicist):**
- Only mock external services
- Test natural units together
- Tests are more realistic

**Recommended: Pragmatic approach**
- Mock external services (APIs, DBs in unit tests)
- Don't mock your own code unless necessary
- Use real implementations in integration tests

### What to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own pure functions |
| File system (in unit tests) | Data transformations |
| Network requests | Business logic |
| Time/randomness | In-memory data structures |
| Expensive computations | Simple utilities |

### Mocking Patterns

```typescript
// GOOD: Mock external dependency
const mockFetch = vi.fn().mockResolvedValue({ data: [] });

// BAD: Mocking your own utilities
const mockFormatDate = vi.fn(); // Don't do this

// GOOD: Dependency injection for testability
function createService(httpClient = fetch) {
  return {
    getData: () => httpClient('/api/data')
  };
}

// In test:
const mockClient = vi.fn();
const service = createService(mockClient);
```
</when_to_mock>

<test_structure>
## Test Organization

### File Naming

```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx      # Colocated test
├── utils/
│   ├── format.ts
│   └── format.test.ts
└── __tests__/               # Or separate folder
    └── integration/
        └── api.test.ts
```

### Test Naming

```typescript
// Pattern: describe what + when + expected result
describe('UserService', () => {
  describe('createUser', () => {
    it('returns user object when given valid email', () => {});
    it('throws ValidationError when email is invalid', () => {});
    it('sends welcome email after successful creation', () => {});
  });
});

// Alternative: BDD style
describe('UserService', () => {
  describe('when creating a user with valid data', () => {
    it('should return the created user', () => {});
    it('should send a welcome email', () => {});
  });

  describe('when email is invalid', () => {
    it('should throw ValidationError', () => {});
  });
});
```

### Arrange-Act-Assert

```typescript
it('calculates total with discount', () => {
  // Arrange - set up test data
  const cart = createCart([
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 }
  ]);
  const discount = 0.1;

  // Act - perform the action
  const total = calculateTotal(cart, discount);

  // Assert - verify result
  expect(total).toBe(225); // (200 + 50) * 0.9
});
```
</test_structure>

<what_not_to_test>
## What NOT to Test

### Skip These

1. **Framework code** - React's useState, Express routing
2. **Third-party libraries** - They have their own tests
3. **Trivial getters/setters** - No logic = no test needed
4. **Implementation details** - Private methods, internal state
5. **One-line functions** - Unless they have complex logic

### Focus On

1. **Business logic** - Where bugs hide
2. **Edge cases** - Nulls, empty arrays, boundaries
3. **Error paths** - What happens when things fail
4. **User-facing behavior** - What users actually do
5. **Regressions** - Bugs that came back once

### Coverage Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Line coverage | 70-80% | Higher isn't always better |
| Branch coverage | 70-80% | More important than lines |
| Critical paths | 100% | Auth, payments, data mutations |

**Warning:** 100% coverage doesn't mean good tests. Bad tests can hit every line without testing anything meaningful.
</what_not_to_test>

<references>
For detailed patterns, load the appropriate reference:

| Topic | Reference File | When to Load |
|-------|----------------|--------------|
| Unit testing patterns | `reference/unit-testing.md` | Writing unit tests, mocking |
| Integration testing | `reference/integration-testing.md` | API tests, database tests |
| Test organization | `reference/test-organization.md` | Structuring test suites |
| Coverage strategies | `reference/coverage-strategies.md` | Setting coverage goals |

**To load:** Ask for the specific topic or check if context suggests it.
</references>

<framework_patterns>
## Quick Reference by Framework

### pytest (Python)
```python
# Fixtures
@pytest.fixture
def user():
    return User(name="test")

def test_user_greet(user):
    assert user.greet() == "Hello, test"

# Parametrize
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

### vitest/jest (TypeScript)
```typescript
// Basic test
test('adds numbers', () => {
  expect(add(1, 2)).toBe(3);
});

// Mock
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ name: 'test' })
}));

// Component test
import { render, screen } from '@testing-library/react';

test('renders button', () => {
  render(<Button>Click</Button>);
  expect(screen.getByRole('button')).toHaveTextContent('Click');
});
```

### Testing Library Principles
1. Query by role, not test ID
2. Test what users see, not implementation
3. Prefer `userEvent` over `fireEvent`
4. Avoid testing internal state
</framework_patterns>

<checklist>
## Testing Checklist

Before marking code complete:

- [ ] Unit tests cover happy path
- [ ] Unit tests cover error cases
- [ ] Edge cases tested (null, empty, boundary)
- [ ] Integration tests for API endpoints
- [ ] No flaky tests (run 3x to verify)
- [ ] Tests are independent (run in any order)
- [ ] Test names describe behavior
- [ ] No hardcoded timeouts (use waitFor)
- [ ] Mocks are reset between tests
- [ ] Coverage meets project standards
</checklist>
