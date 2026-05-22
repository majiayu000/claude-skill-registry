---
name: ts-test-engineer
description: "This skill should be used when the user asks to 'write unit tests', 'add integration tests', 'create tests for React components', 'fix failing test', 'improve test coverage', 'add Playwright tests', 'test this component', 'add fast-check tests', or needs guidance on Vitest, React Testing Library, Playwright, property testing with fast-check, MSW mocking, or test patterns for TypeScript/Next.js. Covers modern TypeScript testing best practices."
---

# TypeScript Test Engineer Skill

Expert guidance for writing, reviewing, and fixing tests in TypeScript/Next.js applications.

## Core Principles

### 1. Test Pyramid Strategy
- **Unit tests** (70%): Fast, isolated, no browser/server
- **Integration tests** (20%): Component interactions, API routes
- **E2E tests** (10%): Critical user flows with Playwright

### 2. Testability Over Mocking
Design code to be testable:
- Pure functions for business logic
- Dependency injection via props/context
- Separate data fetching from rendering
- Small, focused components

### 3. Test Behavior, Not Implementation
- Test what the user sees/does, not internal state
- Avoid testing implementation details (internal state, private methods)
- Tests should survive refactoring if behavior unchanged

### 4. Property Tests > Example Tests (When Applicable)
Prefer property-based tests for:
- Pure functions with invariants
- Parsers, validators, transformers
- Discriminated union handling
- Serialization/deserialization

---

## Property-Based Testing (fast-check)

Property tests find edge cases automatically. Use for pure functions and type transformations.

### When to Use Property Tests
| Use Property Tests | Use Example Tests |
|-------------------|-------------------|
| Pure functions | Component rendering |
| Validation logic | User interactions |
| Parsers/serializers | API integration |
| State transitions | Specific business scenarios |
| Type narrowing | Visual regression |

### Installation
```bash
npm install -D fast-check
```

### Common Property Patterns

#### 1. Invariants - "This should always be true"
```typescript
import fc from 'fast-check';
import { describe, it, expect } from 'vitest';

describe('calculateTotal', () => {
  it('should never return negative', () => {
    fc.assert(
      fc.property(
        fc.integer({ min: 0, max: 1000 }),
        fc.integer({ min: 0, max: 100 }),
        (price, discount) => {
          const total = calculateTotal(price, discount);
          expect(total).toBeGreaterThanOrEqual(0);
        }
      )
    );
  });
});
```

#### 2. Round-Trip / Symmetry
```typescript
it('serialize then deserialize = identity', () => {
  fc.assert(
    fc.property(userArbitrary, (user) => {
      const json = JSON.stringify(user);
      const restored = JSON.parse(json);
      expect(restored).toEqual(user);
    })
  );
});
```

#### 3. Idempotence
```typescript
it('normalizing twice equals normalizing once', () => {
  fc.assert(
    fc.property(fc.string(), (input) => {
      const once = normalize(input);
      const twice = normalize(once);
      expect(twice).toBe(once);
    })
  );
});
```

#### 4. Commutativity
```typescript
it('merge order should not matter', () => {
  fc.assert(
    fc.property(configArbitrary, configArbitrary, (a, b) => {
      expect(mergeConfig(a, b)).toEqual(mergeConfig(b, a));
    })
  );
});
```

### Custom Arbitraries
```typescript
const userArbitrary = fc.record({
  id: fc.uuid(),
  email: fc.emailAddress(),
  name: fc.string({ minLength: 1, maxLength: 100 }),
  role: fc.constantFrom('admin', 'user', 'guest'),
});

const orderArbitrary = fc.record({
  id: fc.uuid(),
  items: fc.array(orderItemArbitrary, { minLength: 1, maxLength: 10 }),
  status: fc.constantFrom('draft', 'pending', 'paid', 'shipped'),
});
```

---

## Unit Testing with Vitest

### Basic Structure
```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('OrderService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should calculate total with discount', () => {
    // Arrange
    const order = createOrder({ items: [{ price: 100, qty: 2 }] });

    // Act
    const total = calculateTotal(order, { discount: 10 });

    // Assert
    expect(total).toBe(180);
  });
});
```

### Testing Discriminated Unions with ts-pattern
```typescript
import { match } from 'ts-pattern';

type Result<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };

describe('Result handling', () => {
  it('should handle all states exhaustively', () => {
    const results: Result<string>[] = [
      { status: 'success', data: 'hello' },
      { status: 'error', error: 'failed' },
      { status: 'loading' },
    ];

    results.forEach((result) => {
      const message = match(result)
        .with({ status: 'success' }, ({ data }) => `Got: ${data}`)
        .with({ status: 'error' }, ({ error }) => `Error: ${error}`)
        .with({ status: 'loading' }, () => 'Loading...')
        .exhaustive();

      expect(typeof message).toBe('string');
    });
  });

  // Property test for exhaustive handling
  it('should handle any valid result', () => {
    const resultArbitrary = fc.oneof(
      fc.record({ status: fc.constant('success' as const), data: fc.string() }),
      fc.record({ status: fc.constant('error' as const), error: fc.string() }),
      fc.record({ status: fc.constant('loading' as const) })
    );

    fc.assert(
      fc.property(resultArbitrary, (result) => {
        expect(() => handleResult(result)).not.toThrow();
      })
    );
  });
});
```

### Testing Async Code
```typescript
it('should fetch user data', async () => {
  const user = await fetchUser('123');

  expect(user).toMatchObject({
    id: '123',
    name: expect.any(String),
  });
});

it('should handle fetch errors', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('User not found');
});
```

### Mocking with vi
```typescript
import { vi } from 'vitest';

// Mock module
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

// Mock implementation
const mockFetch = vi.mocked(fetchUser);
mockFetch.mockResolvedValue({ id: '1', name: 'Test' });

// Spy on method
const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
expect(spy).toHaveBeenCalledWith('error message');
```

---

## React Component Testing

### React Testing Library Setup
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';

describe('LoginForm', () => {
  it('should submit with valid credentials', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('should show validation errors', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });
});
```

### Testing Loading/Error States
```typescript
it('should show loading state', () => {
  render(<UserProfile userId="1" isLoading />);

  expect(screen.getByRole('progressbar')).toBeInTheDocument();
});

it('should show error state', () => {
  render(<UserProfile userId="1" error="Failed to load" />);

  expect(screen.getByRole('alert')).toHaveTextContent('Failed to load');
});
```

### Testing Hooks
```typescript
import { renderHook, act } from '@testing-library/react';

describe('useCounter', () => {
  it('should increment', () => {
    const { result } = renderHook(() => useCounter(0));

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

---

## API Mocking with MSW

### Setup
```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Test User',
    });
  }),

  http.post('/api/orders', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '123', ...body }, { status: 201 });
  }),

  http.get('/api/error', () => {
    return HttpResponse.json({ error: 'Not found' }, { status: 404 });
  }),
];

// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Test Setup
```typescript
// vitest.setup.ts
import { beforeAll, afterAll, afterEach } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterAll(() => server.close());
afterEach(() => server.resetHandlers());
```

### Override Handlers in Tests
```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

it('should handle API error', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({ error: 'Server error' }, { status: 500 });
    })
  );

  render(<UserProfile userId="1" />);

  await waitFor(() => {
    expect(screen.getByRole('alert')).toBeInTheDocument();
  });
});
```

---

## Next.js Specific Testing

For App Router testing, Server Components, and API route testing, see: **[references/nextjs-testing.md](references/nextjs-testing.md)**

Quick patterns:

```typescript
// Testing Server Components (via integration)
import { render, screen } from '@testing-library/react';

// Server components need async rendering
it('should render server component', async () => {
  const Component = await ServerComponent({ id: '1' });
  render(Component);

  expect(screen.getByText('User Data')).toBeInTheDocument();
});

// Testing API routes
import { GET } from '@/app/api/users/route';

it('should return users', async () => {
  const request = new Request('http://localhost/api/users');
  const response = await GET(request);
  const data = await response.json();

  expect(response.status).toBe(200);
  expect(data).toHaveLength(3);
});
```

---

## E2E Testing with Playwright

For comprehensive Playwright patterns, see: **[references/e2e-playwright.md](references/e2e-playwright.md)**

Quick patterns:

```typescript
import { test, expect } from '@playwright/test';

test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');

  await page.click('[data-testid="add-to-cart"]');
  await page.click('[data-testid="checkout"]');

  await page.fill('[name="email"]', 'test@example.com');
  await page.click('button[type="submit"]');

  await expect(page.locator('.confirmation')).toBeVisible();
});
```

---

## Test Anti-Patterns to Avoid

### 1. Testing Implementation Details
```typescript
// BAD: testing internal state
expect(component.state.isOpen).toBe(true);

// GOOD: test what user sees
expect(screen.getByRole('dialog')).toBeVisible();
```

### 2. Over-Mocking
```typescript
// BAD: mocking everything
vi.mock('./utils');
vi.mock('./helpers');
vi.mock('./formatters');

// GOOD: use real implementations for pure functions
import { formatDate, calculateTotal } from './utils';
```

### 3. Snapshot Overuse
```typescript
// BAD: meaningless snapshot
expect(component).toMatchSnapshot();

// GOOD: targeted assertions
expect(screen.getByRole('heading')).toHaveTextContent('Welcome');
expect(screen.getByRole('list').children).toHaveLength(3);
```

### 4. Not Testing Edge Cases
```typescript
// GOOD: test edge cases
describe('parseInput', () => {
  it.each([
    ['', null],
    ['   ', null],
    ['invalid', null],
    ['123', 123],
    ['-1', -1],
    ['0', 0],
  ])('parseInput(%s) = %s', (input, expected) => {
    expect(parseInput(input)).toBe(expected);
  });
});
```

### 5. Flaky Async Tests
```typescript
// BAD: arbitrary timeout
await new Promise(r => setTimeout(r, 1000));

// GOOD: wait for specific condition
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

---

## Test Execution Commands

```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Single file
npm test -- src/utils/parser.test.ts

# Coverage report
npm test -- --coverage

# Run specific pattern
npm test -- -t "should validate"

# E2E tests
npx playwright test

# E2E with UI
npx playwright test --ui

# E2E specific file
npx playwright test checkout.spec.ts
```

---

## Reference Files

For detailed patterns, see:
- **[references/vitest-patterns.md](references/vitest-patterns.md)**: Advanced Vitest configuration, custom matchers
- **[references/nextjs-testing.md](references/nextjs-testing.md)**: App Router, Server Components, API routes
- **[references/e2e-playwright.md](references/e2e-playwright.md)**: Playwright setup, auth, visual testing

---

## Checklist for New Tests

- [ ] Test name describes behavior, not implementation
- [ ] Uses Testing Library queries (getByRole, getByLabelText)
- [ ] Avoids implementation details
- [ ] Independent of other tests
- [ ] Fast (unit < 100ms)
- [ ] Covers happy path + key error cases
- [ ] No arbitrary waits/timeouts
- [ ] Uses MSW for API mocking (not fetch mocks)
