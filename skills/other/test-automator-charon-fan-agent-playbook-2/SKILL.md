---
name: test-automator
description: Test automation framework expert for creating and maintaining automated tests. Use when user asks to write tests, automate testing, or improve test coverage.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  hooks:
    after_complete:
      - trigger: session-logger
        mode: auto
        reason: "Log test creation"
---

# Test Automator

Expert in creating and maintaining automated tests for various frameworks and languages.

## When This Skill Activates

Activates when you:
- Ask to write tests
- Mention test automation
- Request test coverage improvement
- Need to set up testing framework

## Testing Pyramid

```
        /\
       /E2E\      - Few, expensive, slow
      /------\
     /  Integration \ - Moderate number
    /--------------\
   /     Unit Tests  \ - Many, cheap, fast
  /------------------\
```

## Unit Testing

### Principles
1. **Test behavior, not implementation**
2. **One assertion per test** (generally)
3. **Arrange-Act-Assert** pattern
4. **Descriptive test names**

### Example (Jest)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // Arrange
      const userData = {
        name: 'John Doe',
        email: 'john@example.com'
      };

      // Act
      const user = await userService.create(userData);

      // Assert
      expect(user.id).toBeDefined();
      expect(user.email).toBe(userData.email);
    });

    it('should throw error for invalid email', async () => {
      // Arrange
      const userData = { email: 'invalid' };

      // Act & Assert
      await expect(userService.create(userData))
        .rejects.toThrow('Invalid email');
    });
  });
});
```

## Integration Testing

### Principles
1. **Test component interactions**
2. **Use test doubles for external services**
3. **Clean up test data**
4. **Run in isolation**

### Example (Supertest)

```typescript
describe('POST /api/users', () => {
  it('should create a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com'
      })
      .expect(201)
      .expect((res) => {
        expect(res.body.id).toBeDefined();
        expect(res.body.email).toBe('john@example.com');
      });
  });
});
```

## E2E Testing

### Principles
1. **Test critical user flows**
2. **Use realistic test data**
3. **Handle async operations properly**
4. **Clean up after tests**

### Example (Playwright)

```typescript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## Test Coverage

### Coverage Goals

| Type | Target |
|------|--------|
| Lines | > 80% |
| Branches | > 75% |
| Functions | > 80% |
| Statements | > 80% |

### Coverage Reports

```bash
# Jest
npm test -- --coverage

# Python (pytest-cov)
pytest --cov=src --cov-report=html

# Go
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

## Testing Best Practices

### DO's
- Write tests before fixing bugs (TDD)
- Test edge cases
- Keep tests independent
- Use descriptive test names
- Mock external dependencies
- Clean up test data

### DON'Ts
- Don't test implementation details
- Don't write brittle tests
- Don't skip tests without a reason
- Don't commit commented-out tests
- Don't test third-party libraries

## Test Naming Conventions

```typescript
// Good: Describes what is being tested
it('should reject invalid email addresses')

// Good: Describes the scenario and outcome
it('returns 401 when user provides invalid credentials')

// Bad: Vague
it('works correctly')
```

## Common Testing Frameworks

| Language | Framework | Command |
|----------|-----------|---------|
| TypeScript/JS | Jest, Vitest | `npm test` |
| Python | pytest | `pytest` |
| Go | testing | `go test` |
| Java | JUnit | `mvn test` |
| Rust | built-in | `cargo test` |

## Scripts

Generate test boilerplate:
```bash
python scripts/generate_test.py <filename>
```

Check test coverage:
```bash
python scripts/coverage_report.py
```

## References

- `references/best-practices.md` - Testing best practices
- `references/examples/` - Framework-specific examples
- `references/mocking.md` - Mocking guidelines
