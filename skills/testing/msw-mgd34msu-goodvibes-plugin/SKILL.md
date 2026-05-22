---
name: msw
description: Mocks APIs with Mock Service Worker including request handlers, server/browser setup, and testing integration. Use when mocking APIs in tests, developing without backend, or simulating network conditions.
---

# Mock Service Worker (MSW)

API mocking library for browser and Node.js with network-level interception.

## Quick Start

**Install:**
```bash
npm install msw --save-dev
```

**Project structure:**
```
src/
  mocks/
    handlers.ts    # Request handlers
    browser.ts     # Browser setup
    server.ts      # Node.js setup
```

## Request Handlers

### REST Handlers

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // GET request
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'John Doe' },
      { id: 2, name: 'Jane Smith' },
    ]);
  }),

  // GET with params
  http.get('/api/users/:id', ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id: Number(id),
      name: 'John Doe',
      email: 'john@example.com',
    });
  }),

  // POST request
  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: 3, ...body },
      { status: 201 }
    );
  }),

  // PUT request
  http.put('/api/users/:id', async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();
    return HttpResponse.json({ id: Number(id), ...body });
  }),

  // DELETE request
  http.delete('/api/users/:id', ({ params }) => {
    return new HttpResponse(null, { status: 204 });
  }),

  // PATCH request
  http.patch('/api/users/:id', async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();
    return HttpResponse.json({ id: Number(id), ...body });
  }),
];
```

### Query Parameters

```typescript
http.get('/api/search', ({ request }) => {
  const url = new URL(request.url);
  const query = url.searchParams.get('q');
  const page = url.searchParams.get('page') || '1';

  return HttpResponse.json({
    query,
    page: Number(page),
    results: [
      { id: 1, title: `Result for "${query}"` },
    ],
  });
}),
```

### Headers

```typescript
http.get('/api/protected', ({ request }) => {
  const authHeader = request.headers.get('Authorization');

  if (!authHeader?.startsWith('Bearer ')) {
    return HttpResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  return HttpResponse.json({ data: 'protected data' });
}),
```

### Response with Headers

```typescript
http.get('/api/data', () => {
  return HttpResponse.json(
    { data: 'value' },
    {
      headers: {
        'X-Custom-Header': 'custom-value',
        'Cache-Control': 'no-cache',
      },
    }
  );
}),
```

## Node.js Setup (Testing)

### Setup Server

```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Vitest Integration

```typescript
// src/test/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from '../mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    setupFiles: ['./src/test/setup.ts'],
  },
});
```

### Jest Integration

```typescript
// src/test/setup.ts
import { server } from '../mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

```javascript
// jest.config.js
module.exports = {
  setupFilesAfterEnv: ['./src/test/setup.ts'],
};
```

## Browser Setup

### Initialize Worker

```bash
npx msw init public/ --save
```

### Setup Worker

```typescript
// src/mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

export const worker = setupWorker(...handlers);
```

### Start in Development

```typescript
// src/main.tsx or src/index.tsx
async function enableMocking() {
  if (process.env.NODE_ENV !== 'development') {
    return;
  }

  const { worker } = await import('./mocks/browser');
  return worker.start({
    onUnhandledRequest: 'bypass',
  });
}

enableMocking().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <App />
  );
});
```

### Next.js Integration

```typescript
// src/mocks/index.ts
export async function initMocks() {
  if (typeof window === 'undefined') {
    const { server } = await import('./server');
    server.listen();
  } else {
    const { worker } = await import('./browser');
    await worker.start();
  }
}
```

```typescript
// app/providers.tsx
'use client';

import { useEffect, useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [mockingEnabled, setMockingEnabled] = useState(false);

  useEffect(() => {
    async function enableMocking() {
      if (process.env.NODE_ENV === 'development') {
        const { initMocks } = await import('@/mocks');
        await initMocks();
      }
      setMockingEnabled(true);
    }
    enableMocking();
  }, []);

  if (!mockingEnabled) {
    return null;
  }

  return <>{children}</>;
}
```

## GraphQL Handlers

```typescript
import { graphql, HttpResponse } from 'msw';

export const handlers = [
  // Query
  graphql.query('GetUser', ({ variables }) => {
    const { id } = variables;
    return HttpResponse.json({
      data: {
        user: {
          id,
          name: 'John Doe',
          email: 'john@example.com',
        },
      },
    });
  }),

  // Mutation
  graphql.mutation('CreateUser', ({ variables }) => {
    const { input } = variables;
    return HttpResponse.json({
      data: {
        createUser: {
          id: '123',
          ...input,
        },
      },
    });
  }),

  // With custom endpoint
  graphql.link('https://api.example.com/graphql').query('GetPosts', () => {
    return HttpResponse.json({
      data: {
        posts: [
          { id: '1', title: 'Hello World' },
        ],
      },
    });
  }),
];
```

## Testing Patterns

### Override Handlers Per Test

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('handles error response', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json(
        { error: 'Internal Server Error' },
        { status: 500 }
      );
    })
  );

  // Test error handling
  render(<UserList />);
  await screen.findByText('Error loading users');
});

test('handles empty response', async () => {
  server.use(
    http.get('/api/users', () => {
      return HttpResponse.json([]);
    })
  );

  render(<UserList />);
  await screen.findByText('No users found');
});
```

### Delay Responses

```typescript
import { delay, http, HttpResponse } from 'msw';

http.get('/api/users', async () => {
  await delay(1000); // 1 second delay
  return HttpResponse.json([{ id: 1, name: 'John' }]);
}),

// Infinite delay (for testing loading states)
http.get('/api/data', async () => {
  await delay('infinite');
  return HttpResponse.json({ data: 'never returns' });
}),
```

### Network Errors

```typescript
import { http, HttpResponse } from 'msw';

http.get('/api/users', () => {
  return HttpResponse.error();
}),
```

### Passthrough

```typescript
import { http, passthrough } from 'msw';

http.get('/api/analytics', () => {
  return passthrough();
}),
```

## Request Assertions

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('sends correct data', async () => {
  let requestBody: any;

  server.use(
    http.post('/api/users', async ({ request }) => {
      requestBody = await request.json();
      return HttpResponse.json({ id: 1 });
    })
  );

  // Trigger the request
  await createUser({ name: 'John', email: 'john@example.com' });

  // Assert request body
  expect(requestBody).toEqual({
    name: 'John',
    email: 'john@example.com',
  });
});
```

## Cookies

```typescript
http.get('/api/session', ({ cookies }) => {
  const sessionId = cookies.sessionId;

  if (!sessionId) {
    return HttpResponse.json(
      { error: 'No session' },
      { status: 401 }
    );
  }

  return HttpResponse.json({ user: 'John' });
}),

// Set cookies in response
http.post('/api/login', () => {
  return HttpResponse.json(
    { success: true },
    {
      headers: {
        'Set-Cookie': 'sessionId=abc123; Path=/; HttpOnly',
      },
    }
  );
}),
```

## Streaming Responses

```typescript
import { http, HttpResponse } from 'msw';

http.get('/api/stream', () => {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(encoder.encode('Hello'));
      controller.enqueue(encoder.encode(' '));
      controller.enqueue(encoder.encode('World'));
      controller.close();
    },
  });

  return new HttpResponse(stream, {
    headers: {
      'Content-Type': 'text/plain',
    },
  });
}),
```

## Best Practices

1. **Keep handlers in separate file** - Easy to maintain and reuse
2. **Use type-safe request bodies** - Define interfaces
3. **Reset handlers after tests** - Prevent test pollution
4. **Mock at network level** - Not implementation details
5. **Use onUnhandledRequest** - Catch missing handlers

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting resetHandlers | Add to afterEach |
| Wrong handler order | Specific routes before generic |
| Missing async/await | Await request.json() |
| Hardcoded URLs | Use relative or env vars |
| Not initializing worker | Call worker.start() |

## Reference Files

- [references/handlers.md](references/handlers.md) - Handler patterns
- [references/testing.md](references/testing.md) - Testing strategies
- [references/graphql.md](references/graphql.md) - GraphQL mocking
