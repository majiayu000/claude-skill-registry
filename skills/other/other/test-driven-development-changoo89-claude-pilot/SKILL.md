---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code. Red-Green-Refactor cycle ensures tests pass.
---

# SKILL: Test-Driven Development

> **Purpose**: Red-Green-Refactor cycle for reliable code with tests
> **Target**: Coder agent implementing features or bugfixes

---

## Quick Start

### When to Use This Skill
- Implementing new features
- Fixing bugs
- Refactoring existing code
- Adding new functionality

### Quick Reference
| Phase | Action | Verify |
|-------|--------|--------|
| **RED** | Write failing test | `npm test` → FAIL |
| **GREEN** | Minimal implementation | `npm test` → PASS |
| **REFACTOR** | Clean up code | `npm test && npm run lint` → PASS |
| **REPEAT** | Until criteria met | All quality gates pass |

---

## Core Concepts

### The TDD Cycle

**Step 1: RED** - Write a failing test
```typescript
// src/auth.service.test.ts
describe('AuthService', () => {
  it('should authenticate valid user', async () => {
    const service = new AuthService();
    const result = await service.authenticate('user@example.com', 'password');
    expect(result).toBe(true);
  });
});
```

**Verify test fails**: `npm test` → FAIL: AuthService is not defined

**Step 2: GREEN** - Write minimal code to pass
```typescript
// src/auth.service.ts
export class AuthService {
  async authenticate(email: string, password: string): Promise<boolean> {
    return true;  // Minimal implementation
  }
}
```

**Verify test passes**: `npm test` → PASS

**Step 3: REFACTOR** - Clean up
```typescript
// src/auth.service.ts
export class AuthService {
  constructor(private users: UserRepository) {}

  async authenticate(email: string, password: string): Promise<boolean> {
    const user = await this.users.findByEmail(email);
    if (!user) return false;
    return await user.verifyPassword(password);
  }
}
```

**Verify tests still pass**: `npm test && npm run lint` → PASS

---

## Test Patterns

### Arrange-Act-Assert
```typescript
it('should calculate total with discount', () => {
  const cart = new Cart();  // Arrange
  cart.applyDiscount('SUMMER20');  // Act
  expect(cart.total).toBe(80);  // Assert
});
```

### Given-When-Then
```typescript
it('should reject invalid card', () => {
  const payment = new PaymentService();  // Given
  const result = payment.process({ number: 'invalid' }, 100);  // When
  expect(result.success).toBe(false);  // Then
});
```

---

## Test Coverage

### Coverage Targets
- **Overall**: ≥80% line coverage
- **Core modules**: ≥90% line coverage
- **Critical paths**: 100% coverage

### Measure Coverage
```bash
npm test -- --coverage  # Generate report
open coverage/lcov-report/index.html  # View in browser
```

---

## Common Patterns

### Testing Async Code
```typescript
// Promise-based
it('should fetch user', async () => {
  const user = await service.getUser(1);
  expect(user.name).toBe('Alice');
});

// Callback-based
it('should emit event', (done) => {
  service.on('event', (data) => {
    expect(data).toBe('expected');
    done();
  });
  service.trigger();
});

// Timer-based
jest.useFakeTimers();
it('should timeout after 5s', () => {
  service.start();
  jest.advanceTimersByTime(5000);
  expect(service.timedOut).toBe(true);
});
```

### Mocking Dependencies
```typescript
const mockRepository = {
  findByEmail: jest.fn().mockResolvedValue({ id: 1, email: 'test@example.com' })
};
const service = new AuthService(mockRepository);

await service.authenticate('test@example.com', 'password');
expect(mockRepository.findByEmail).toHaveBeenCalledWith('test@example.com');
```

### Error Testing
```typescript
it('should throw on invalid input', () => {
  expect(() => service.validate(null)).toThrow('Invalid input');
  expect(() => service.validate('')).toThrow('Email required');
});
```

---

## Ralph Loop Integration

**Autonomous iteration until all tests pass**:

1. **Entry**: Immediately after first code change
2. **Max iterations**: 7
3. **Verification**: Tests, type-check, lint, coverage
4. **Exit**: All quality gates pass

**See**: @.claude/skills/ralph-loop/SKILL.md

---

## Quality Gates

After implementation:
- [ ] All tests pass (`npm test`)
- [ ] Coverage ≥80% overall, ≥90% core (`npm test -- --coverage`)
- [ ] Type check clean (`npm run type-check`)
- [ ] Lint clean (`npm run lint`)
- [ ] No console.log statements (use proper logging)

---

## Related Skills

- **ralph-loop**: Autonomous iteration until all tests pass
- **code-quality-gates**: Formatting, type-check, linting
- **vibe-coding**: Code quality standards (≤50 lines/function)

---

**Version**: claude-pilot 4.2.0
