---
skill_name: jest-patterns
skill_category: testing
description: Jest testing patterns, anti-patterns, and quality rules
allowed_tools: [Read, Edit, Write, Grep, Bash]
token_estimate: 1800
version: 1.0
last_updated: 2026-01-13
owner: Claude Copilot
status: active
tags: [jest, testing, javascript, typescript, unit-test, integration-test, quality]
related_skills: [javascript-patterns, react-patterns, pytest-patterns]
trigger_files: ["*.test.ts", "*.test.js", "*.spec.ts", "*.spec.js", "jest.config.*", "__tests__/**"]
trigger_keywords: [jest, test, spec, mock, describe, it, expect, beforeEach, afterEach]
---

# Jest Patterns

Modern Jest testing patterns, anti-patterns, and quality rules for JavaScript/TypeScript.

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Test Behavior** | Test what code does, not how it does it |
| **Isolation** | Each test independent, no shared state |
| **AAA Pattern** | Arrange → Act → Assert structure |
| **Fast Feedback** | Tests run in milliseconds |

## Patterns vs Anti-Patterns

### Test Structure (AAA)

```typescript
// GOOD: Clear AAA structure
describe('UserService', () => {
  it('should create user with valid data', async () => {
    // Arrange
    const userData = { name: 'John', email: 'john@example.com' };
    const mockRepo = { save: jest.fn().mockResolvedValue({ id: '1', ...userData }) };
    const service = new UserService(mockRepo);

    // Act
    const result = await service.createUser(userData);

    // Assert
    expect(result.id).toBe('1');
    expect(mockRepo.save).toHaveBeenCalledWith(userData);
  });
});

// BAD: Mixed arrange/act/assert
it('creates user', async () => {
  const service = new UserService({ save: jest.fn() });
  expect(await service.createUser({ name: 'John' })).toBeDefined();
  // What are we testing? Unclear!
});
```

### Mocking

```typescript
// GOOD: Minimal, focused mocks
const mockFetch = jest.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ data: 'test' })
});

// GOOD: Reset mocks between tests
beforeEach(() => {
  jest.clearAllMocks();
});

// GOOD: Mock only what's necessary
jest.mock('./database', () => ({
  query: jest.fn()
}));

// BAD: Over-mocking implementation details
jest.mock('./service', () => ({
  __esModule: true,
  default: jest.fn().mockImplementation(() => ({
    method1: jest.fn(),
    method2: jest.fn(),
    method3: jest.fn(),
    // 20 more methods...
  }))
}));
```

### Assertions

```typescript
// GOOD: Specific, meaningful assertions
expect(user.name).toBe('John');
expect(errors).toHaveLength(2);
expect(result).toEqual({ id: '1', status: 'active' });
expect(callback).toHaveBeenCalledWith('arg1', expect.any(Number));

// GOOD: Custom matchers for domain concepts
expect(response).toBeSuccessful();
expect(user).toHavePermission('admin');

// BAD: Vague assertions
expect(result).toBeTruthy();
expect(data).toBeDefined();
expect(obj).toMatchObject({}); // Always passes!

// BAD: Multiple unrelated assertions
expect(user.name).toBe('John');
expect(user.email).toBe('john@example.com');
expect(user.createdAt).toBeDefined();
expect(user.updatedAt).toBeDefined();
expect(user.deletedAt).toBeNull();
// Better: Use snapshot or single toEqual
```

### Async Testing

```typescript
// GOOD: async/await
it('should fetch user data', async () => {
  const data = await fetchUser('123');
  expect(data.name).toBe('John');
});

// GOOD: Test rejections
it('should reject for invalid user', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('User not found');
});

// GOOD: waitFor for async UI updates
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// BAD: done callback (error-prone)
it('fetches data', (done) => {
  fetchUser('123').then((data) => {
    expect(data).toBeDefined();
    done();
  });
});

// BAD: No await (test passes incorrectly)
it('should fail', () => {
  expect(asyncOperation()).rejects.toThrow(); // Missing await!
});
```

### Test Organization

```typescript
// GOOD: Descriptive nested describes
describe('ShoppingCart', () => {
  describe('addItem', () => {
    it('should add new item to empty cart', () => {});
    it('should increment quantity for existing item', () => {});
    it('should throw for invalid item', () => {});
  });

  describe('removeItem', () => {
    it('should remove item from cart', () => {});
    it('should throw for item not in cart', () => {});
  });
});

// GOOD: Setup/teardown at appropriate levels
describe('Database tests', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });
});

// BAD: Flat, unclear structure
test('cart add', () => {});
test('cart add existing', () => {});
test('cart remove', () => {});
test('cart clear', () => {});
```

## Anti-Patterns to Avoid

### Flaky Tests

```typescript
// BAD: Time-dependent
it('should expire token', () => {
  const token = createToken();
  // Depends on system time - will fail randomly
  expect(isExpired(token)).toBe(false);
});

// GOOD: Control time
it('should expire token after 1 hour', () => {
  jest.useFakeTimers();
  const token = createToken();

  jest.advanceTimersByTime(59 * 60 * 1000);
  expect(isExpired(token)).toBe(false);

  jest.advanceTimersByTime(2 * 60 * 1000);
  expect(isExpired(token)).toBe(true);
});

// BAD: Random data without seed
it('validates random email', () => {
  const email = `user${Math.random()}@test.com`;
  expect(isValid(email)).toBe(true);
});

// GOOD: Deterministic test data
it('validates various email formats', () => {
  const emails = ['user@test.com', 'user.name@test.co.uk'];
  emails.forEach(email => expect(isValid(email)).toBe(true));
});
```

### Test Coupling

```typescript
// BAD: Tests depend on each other
describe('User flow', () => {
  let userId: string;

  it('creates user', async () => {
    const user = await createUser();
    userId = user.id; // Shared state!
  });

  it('updates user', async () => {
    await updateUser(userId, {}); // Fails if first test fails!
  });
});

// GOOD: Independent tests
describe('User operations', () => {
  it('creates user', async () => {
    const user = await createUser();
    expect(user.id).toBeDefined();
  });

  it('updates existing user', async () => {
    const user = await createUser(); // Own setup
    const updated = await updateUser(user.id, { name: 'New' });
    expect(updated.name).toBe('New');
  });
});
```

### Testing Implementation Details

```typescript
// BAD: Testing private methods/state
it('should update internal counter', () => {
  const component = new Counter();
  component.increment();
  expect(component._internalCount).toBe(1); // Private!
});

// GOOD: Test public behavior
it('should display incremented value', () => {
  const component = new Counter();
  component.increment();
  expect(component.getValue()).toBe(1);
});

// BAD: Testing method calls instead of effects
it('should call logger', () => {
  const logger = { log: jest.fn() };
  doSomething(logger);
  expect(logger.log).toHaveBeenCalled(); // Is this the real requirement?
});

// GOOD: Test the actual effect
it('should record action in audit log', async () => {
  await doSomething();
  const logs = await getAuditLogs();
  expect(logs).toContainEqual(expect.objectContaining({
    action: 'something',
    timestamp: expect.any(Date)
  }));
});
```

### Snapshot Abuse

```typescript
// BAD: Large, unstable snapshots
it('renders page', () => {
  expect(render(<FullPage />)).toMatchSnapshot();
  // 500+ line snapshot that changes constantly
});

// GOOD: Small, focused snapshots
it('renders error state correctly', () => {
  expect(render(<ErrorMessage error="Not found" />)).toMatchSnapshot();
});

// GOOD: Inline snapshots for small values
it('formats date correctly', () => {
  expect(formatDate(date)).toMatchInlineSnapshot(`"Jan 13, 2026"`);
});
```

## Configuration Best Practices

```javascript
// jest.config.js
module.exports = {
  // Clear mocks automatically
  clearMocks: true,

  // Coverage settings
  collectCoverageFrom: ['src/**/*.{ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: { branches: 80, functions: 80, lines: 80 }
  },

  // Fast test execution
  maxWorkers: '50%',

  // Fail fast in CI
  bail: process.env.CI ? 1 : 0,

  // Clear timeout
  testTimeout: 10000,
};
```

## Quality Checklist

| Check | Rule |
|-------|------|
| AAA structure | Arrange → Act → Assert clearly separated |
| Isolation | Tests don't share state |
| No flaky tests | No time/random dependencies |
| Fast execution | Unit tests < 100ms each |
| Clear assertions | Specific matchers, not toBeTruthy |
| Minimal mocking | Only mock what's necessary |
| Descriptive names | Test name describes behavior |
| Cleanup | afterEach/afterAll for side effects |
