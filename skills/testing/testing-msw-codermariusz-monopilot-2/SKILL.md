---
name: testing-msw
description: Apply when mocking API calls in tests or development: intercepting requests, simulating error states, and testing loading states.
version: 1.0.0
tokens: ~600
confidence: high
sources:
  - https://mswjs.io/docs/getting-started
  - https://mswjs.io/docs/best-practices/typescript
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [testing, msw, mocking, api]
---

## When to Use

Apply when mocking API calls in tests or development: intercepting requests, simulating error states, and testing loading states.

## Patterns

### Pattern 1: Setup Handlers
```typescript
// Source: https://mswjs.io/docs/getting-started
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'John' },
      { id: '2', name: 'Jane' },
    ]);
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  }),
];
```

### Pattern 2: Test Setup
```typescript
// Source: https://mswjs.io/docs/getting-started
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// jest.setup.ts or vitest.setup.ts
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Pattern 3: Test-Specific Overrides
```typescript
// Source: https://mswjs.io/docs/best-practices/typescript
import { http, HttpResponse } from 'msw';
import { server } from './mocks/server';

test('handles server error', async () => {
  // Override for this test only
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json(
        { error: 'Server error' },
        { status: 500 }
      );
    })
  );

  render(<UserList />);
  expect(await screen.findByText(/error/i)).toBeInTheDocument();
});

test('handles empty list', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json([]);
    })
  );

  render(<UserList />);
  expect(await screen.findByText(/no users/i)).toBeInTheDocument();
});
```

### Pattern 4: Request Assertions
```typescript
// Source: https://mswjs.io/docs/best-practices/typescript
test('sends correct data', async () => {
  let capturedBody: unknown;

  server.use(
    http.post('/api/users', async ({ request }) => {
      capturedBody = await request.json();
      return HttpResponse.json({ id: '1' }, { status: 201 });
    })
  );

  render(<CreateUserForm />);
  await userEvent.type(screen.getByLabelText(/name/i), 'John');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(capturedBody).toEqual({ name: 'John' });
  });
});
```

### Pattern 5: Delayed Responses (Loading States)
```typescript
// Source: https://mswjs.io/docs/api/delay
import { http, HttpResponse, delay } from 'msw';

server.use(
  http.get('/api/users', async () => {
    await delay(100); // Simulate network delay
    return HttpResponse.json([{ id: '1', name: 'John' }]);
  })
);

test('shows loading state', async () => {
  render(<UserList />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  expect(await screen.findByText('John')).toBeInTheDocument();
});
```

### Pattern 6: Browser Setup (Development)
```typescript
// Source: https://mswjs.io/docs/getting-started
// src/mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);

// main.tsx (development only)
if (process.env.NODE_ENV === 'development') {
  const { worker } = await import('./mocks/browser');
  await worker.start();
}
```

## Anti-Patterns

- **Not resetting handlers** - Always resetHandlers in afterEach
- **Global mocks in tests** - Use server.use() for test-specific
- **No error scenarios** - Test 4xx and 5xx responses
- **Mocking too much** - Integration tests should hit real APIs

## Verification Checklist

- [ ] Server setup in test config (beforeAll/afterAll)
- [ ] Handlers reset after each test
- [ ] Error states tested with overrides
- [ ] Loading states tested with delay()
- [ ] Request body assertions where needed
