---
name: jest-nestjs
description: >
  Jest + NestJS testing patterns for unit and e2e tests in Aurora projects.
  Trigger: When writing tests, mocking dependencies, or implementing test coverage in NestJS/Aurora.
license: MIT
metadata:
  author: aurora
  version: "1.1"
  auto_invoke: "Writing tests, mocking services, testing handlers"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

Use this skill when:
- Writing unit tests for handlers, services, or aggregates
- Creating e2e tests for API endpoints
- Mocking NestJS dependencies (repositories, services, event bus)
- Testing CQRS commands and queries
- Testing Aurora-generated code
- Setting up test fixtures and factories

## Testing Philosophy in Aurora/NestJS

**Unit Tests**: Test individual components in isolation
- Handlers (Command/Query), Services, Aggregates/Value Objects, Mappers

**e2e Tests**: Test complete flows through the API layer
- REST endpoints, GraphQL resolvers, Authentication, Database interactions

## Detailed References

- [Unit Testing Patterns](unit-testing.md) — Command/query handlers, mocking repos, mocking external services, bus mocks
- [E2E Testing Patterns](e2e-testing.md) — REST controllers, GraphQL resolvers
- [Aurora-Specific Testing](aurora-testing.md) — Value objects, aggregates, test organization

## Best Practices

### ✅ DO

1. **Isolate tests**: Each test should be independent
2. **Use descriptive names**: "should throw error when price is negative"
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Mock external dependencies**: Database, APIs, services
5. **Test edge cases**: Null, undefined, empty arrays, boundaries
6. **Test error paths**: Exceptions, validation errors
7. **Use factories/fixtures**: Reusable test data builders
8. **Keep tests fast**: Unit tests < 100ms, e2e < 1s
9. **Clean up**: Use `afterEach` to reset state
10. **Test one thing**: One assertion per test (when possible)

### ❌ DON'T

1. **Don't test implementation details**: Test behavior, not internals
2. **Don't test framework code**: Trust NestJS, TypeORM, etc.
3. **Don't share state**: Between tests or describe blocks
4. **Don't use real database**: In unit tests (use mocks)
5. **Don't skip tests**: Fix or remove broken tests
6. **Don't test getters/setters**: Unless they have logic
7. **Don't duplicate tests**: Avoid redundant test cases
8. **Don't test generated code**: Trust Aurora generation (test custom logic only)
9. **Don't ignore coverage**: Aim for >80% on custom code

## Coverage Guidelines

**Target Coverage:**
- Custom handlers: 100% (all custom logic)
- Services: 90%+ (critical business logic)
- Aggregates: 90%+ (domain rules)
- Value Objects: 80%+ (validation logic)
- Controllers/Resolvers: 80%+ (e2e coverage acceptable)
- Generated code: Skip (trust Aurora)

**Run Coverage:**
```bash
npm run test:cov       # Unit tests with coverage
npm run test:e2e       # e2e tests
npm run test:watch     # Watch mode for TDD
```

## Jest Configuration

**jest.config.js** (typical Aurora setup):

```javascript
module.exports = {
    moduleFileExtensions: ['js', 'json', 'ts'],
    rootDir: 'src',
    testRegex: '.*\\.spec\\.ts$',
    transform: {
        '^.+\\.(t|j)s$': 'ts-jest',
    },
    collectCoverageFrom: [
        '**/*.(t|j)s',
        '!**/*.module.ts',
        '!**/*.index.ts',
        '!**/node_modules/**',
        '!**/dist/**',
        '!**/infrastructure/seeds/**',
    ],
    coverageDirectory: '../coverage',
    testEnvironment: 'node',
    moduleNameMapper: {
        '^@app/(.*)$': '<rootDir>/$1',
        '^@core/(.*)$': '<rootDir>/@core/$1',
        '^@api/(.*)$': '<rootDir>/@api/$1',
    },
};
```

## Quick Reference

| Task | Pattern |
|------|---------|
| Test handler | `Test.createTestingModule()` + mock repository |
| Mock repository | Use custom mock class implementing interface |
| Test validation | Expect exception to be thrown |
| e2e REST | `supertest` + `app.getHttpServer()` |
| e2e GraphQL | `supertest` + GraphQL query string |
| Test aggregate | Call methods + verify events |
| Test VO | Constructor + validation rules |
| Coverage | `npm run test:cov` |

## Remember

- **Unit tests** = Fast, isolated, mock dependencies
- **e2e tests** = Slow, integrated, real dependencies
- **Test custom logic only**: Don't test Aurora-generated code
- **Mark your code**: Use `#region AI-generated code` in handlers
- **TDD when possible**: Write test → Implement → Refactor
