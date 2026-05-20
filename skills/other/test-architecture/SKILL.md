---
name: test-architecture
description: >
  Test organization, fixtures, factories (factory_boy/faker), test isolation,
  database cleanup, and test configuration. Use when the user is setting up a test
  suite, organizing test files, creating test fixtures, or dealing with test isolation issues.
---

# Test Architecture

Well-structured tests are maintainable, fast, and reliable. This skill covers how to organize test files, create reusable fixtures and factories, ensure test isolation, and configure test environments.

## When to Use
- User is setting up a new test suite or framework
- User asks about test file organization or naming
- User needs test fixtures, factories, or seed data
- Tests are flaky due to shared state or ordering issues
- User asks about database cleanup between tests
- User needs test configuration (vitest.config, jest.config, conftest.py)

## Core Patterns

### Test File Organization

Co-locate tests with source files for discoverability:

```
src/
  services/
    auth.ts
    auth.test.ts          # Unit tests next to source
    billing.ts
    billing.test.ts
  routes/
    users.ts
    users.test.ts
test/
  integration/
    api.test.ts           # Integration tests in separate dir
  e2e/
    login.spec.ts         # E2E tests in dedicated dir
  fixtures/
    users.json            # Shared test data
  factories/
    user.factory.ts       # Data factories
  helpers/
    setup.ts              # Test setup utilities
    db.ts                 # Database helpers
```

### Fixtures: Static Test Data

Fixtures are pre-defined data objects for predictable testing:

```typescript
// test/fixtures/users.ts
export const validUser = {
  email: 'test@example.com',
  name: 'Test User',
  role: 'member',
} as const

export const adminUser = {
  email: 'admin@example.com',
  name: 'Admin User',
  role: 'admin',
} as const

export const invalidUser = {
  email: 'not-an-email',
  name: '',
  role: 'unknown',
} as const
```

Usage in tests:

```typescript
import { validUser, adminUser } from '../fixtures/users'

it('creates a user', async () => {
  const result = await createUser(validUser)
  expect(result.email).toBe(validUser.email)
})
```

### Factories: Dynamic Test Data

Factories generate unique test data with sensible defaults. Override only what matters for each test:

**TypeScript (with custom factory):**

```typescript
// test/factories/user.factory.ts
let counter = 0

interface UserOverrides {
  email?: string
  name?: string
  role?: string
}

export function buildUser(overrides: UserOverrides = {}) {
  counter += 1
  return {
    email: `user-${counter}@test.com`,
    name: `User ${counter}`,
    role: 'member',
    ...overrides,
  }
}

// Usage
it('creates admin user', () => {
  const user = buildUser({ role: 'admin' })
  // user.email is unique, user.role is 'admin'
})
```

**Python (with factory_boy and Faker):**

```python
# test/factories.py
import factory
from faker import Faker
from myapp.models import User

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.email())
    name = factory.LazyAttribute(lambda _: fake.name())
    role = "member"

# Usage
def test_create_admin():
    user = UserFactory(role="admin")
    assert user.role == "admin"
    assert "@" in user.email  # Unique, realistic email
```

### Test Isolation

Each test must run independently. No test should depend on another's side effects:

```typescript
// test/helpers/setup.ts
import { beforeEach, afterEach, afterAll } from 'vitest'
import { db } from '../../src/db'

beforeEach(async () => {
  await db.migrate.latest()      // Ensure schema is current
})

afterEach(async () => {
  await db.raw('TRUNCATE TABLE users CASCADE')
  await db.raw('TRUNCATE TABLE posts CASCADE')
})

afterAll(async () => {
  await db.destroy()             // Close connection pool
})
```

### Database Cleanup Strategies

Three approaches, pick one per project:

| Strategy | How | Best For |
|----------|-----|----------|
| Truncate (recommended) | `TRUNCATE TABLE x CASCADE` in afterEach | Most projects |
| Transaction rollback | Begin txn in beforeEach, rollback in afterEach | Fast cleanup, no cascade issues |
| Dedicated test DB | Django `@pytest.fixture(autouse=True)` with `db` fixture | Django/framework-managed |

### Test Configuration

**Vitest:**

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    setupFiles: ['./test/helpers/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      thresholds: { lines: 80, branches: 80, functions: 80 },
    },
    include: ['src/**/*.test.ts'],
    exclude: ['node_modules', 'dist'],
  },
})
```

**pytest:**

```ini
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--strict-markers --tb=short -q"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]

[tool.coverage.report]
fail_under = 80
```

## Anti-Patterns

- **Shared mutable state between tests**: Global variables modified by tests cause ordering dependencies. Each test must set up its own state.
- **Not closing database connections**: Forgetting `afterAll(() => db.destroy())` causes connection pool exhaustion and hanging test processes.
- **Testing against production database**: Always use a separate test database or in-memory alternative. Never run tests against production data.
- **Huge fixture files**: A 500-line JSON fixture is hard to maintain. Use factories that generate data dynamically with only the relevant fields overridden.
- **Skipping cleanup**: Tests that leave data behind cause the next test to fail intermittently. Always truncate or rollback.
- **Importing test helpers into production code**: The `test/` directory should never be imported by `src/`. Keep test utilities isolated.

## Quick Reference

| Concept | Purpose | Location |
|---------|---------|----------|
| Fixtures | Static, predictable test data | `test/fixtures/` |
| Factories | Dynamic, unique test data | `test/factories/` |
| Helpers | Reusable test utilities | `test/helpers/` |
| Setup | beforeEach/afterEach/afterAll | `test/helpers/setup.ts` |
| Config | Test runner configuration | `vitest.config.ts` / `jest.config.ts` |

**Isolation**: Each test sets up and tears down its own state.
**Cleanup**: Truncate tables or rollback transactions after each test.
**Connections**: Always close DB pools in afterAll.
**Coverage**: Configure 80% threshold in test runner config.
