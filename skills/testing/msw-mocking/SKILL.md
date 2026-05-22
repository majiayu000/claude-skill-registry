---
name: msw-mocking
description: Mock Service Worker (MSW) 2.x for API mocking. Use when testing frontend components with network mocking, simulating API errors, or creating deterministic API responses in tests.
context: fork
agent: test-generator
version: 2.0.0
tags: [msw, testing, mocking, frontend, 2026]
author: SkillForge
user-invocable: false
---

# MSW (Mock Service Worker) 2.x

Network-level API mocking for frontend tests using MSW 2.x.

## When to Use

- Frontend component testing
- Simulating API responses and errors
- Network delay simulation
- GraphQL mocking
- WebSocket mocking (NEW in 2.x)

## Quick Reference

```typescript
// Core imports
import { http, HttpResponse, graphql, ws, delay, passthrough } from 'msw';
import { setupServer } from 'msw/node';

// Basic handler
http.get('/api/users/:id', ({ params }) => {
  return HttpResponse.json({ id: params.id, name: 'User' });
});

// Error response
http.get('/api/fail', () => {
  return HttpResponse.json({ error: 'Not found' }, { status: 404 });
});

// Delay simulation
http.get('/api/slow', async () => {
  await delay(2000);
  return HttpResponse.json({ data: 'response' });
});

// Passthrough (NEW in 2.x)
http.get('/api/real', () => passthrough());
```

## Test Setup

```typescript
// vitest.setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './src/mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Runtime Override

```typescript
import { http, HttpResponse } from 'msw';
import { server } from '../mocks/server';

test('shows error on API failure', async () => {
  server.use(
    http.get('/api/users/:id', () => {
      return HttpResponse.json({ error: 'Not found' }, { status: 404 });
    })
  );

  render(<UserProfile id="123" />);
  expect(await screen.findByText(/not found/i)).toBeInTheDocument();
});
```

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ NEVER mock fetch directly
jest.spyOn(global, 'fetch').mockResolvedValue(...)

// ❌ NEVER mock axios module
jest.mock('axios')

// ❌ NEVER test implementation details
expect(fetch).toHaveBeenCalledWith('/api/...')

// ✅ ALWAYS use MSW
server.use(http.get('/api/...', () => HttpResponse.json({...})))

// ✅ ALWAYS test user-visible behavior
expect(await screen.findByText('Success')).toBeInTheDocument()
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Handler location | `src/mocks/handlers.ts` |
| Default behavior | Return success |
| Override scope | Per-test with `server.use()` |
| Unhandled requests | Error (catch missing mocks) |
| GraphQL | Use `graphql.query/mutation` |
| WebSocket | Use `ws.link()` for WS mocking |

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/msw-2x-api.md](references/msw-2x-api.md) | Complete MSW 2.x API reference |
| [examples/handler-patterns.md](examples/handler-patterns.md) | CRUD, auth, error, and upload examples |
| [checklists/msw-setup-checklist.md](checklists/msw-setup-checklist.md) | Setup and review checklists |
| [templates/handlers-template.ts](templates/handlers-template.ts) | Starter template for new handlers |

## Related Skills

- `unit-testing` - Component isolation
- `integration-testing` - Full integration tests
- `vcr-http-recording` - Python equivalent

## Capability Details

### http-request-mocking
**Keywords:** http.get, http.post, http handler, REST mock
**Solves:**
- Mock REST API endpoints
- Intercept HTTP requests at network level
- Create request handlers for testing

### graphql-mocking
**Keywords:** graphql.query, graphql.mutation, GraphQL handler, mock GraphQL
**Solves:**
- Mock GraphQL queries and mutations
- Handle GraphQL variables in mocks
- Test GraphQL error scenarios

### websocket-mocking
**Keywords:** WebSocket, ws mock, real-time mock, socket mock
**Solves:**
- Mock WebSocket connections
- Simulate real-time events
- Test WebSocket message handling

### error-simulation
**Keywords:** error simulation, network error, 500 error, mock error
**Solves:**
- Simulate API errors in tests
- Test error handling UI
- Mock network failures

### network-delay-simulation
**Keywords:** delay, latency, slow response, loading state
**Solves:**
- Simulate slow network responses
- Test loading state UI
- Verify timeout handling

### runtime-handler-override
**Keywords:** runtime override, use.once, test-specific handler, override
**Solves:**
- Override handlers for specific tests
- Create one-time response handlers
- Customize responses per test
