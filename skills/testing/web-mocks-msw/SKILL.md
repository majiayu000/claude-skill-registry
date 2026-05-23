---
name: web-mocks-msw
description: MSW handlers, browser/server workers, test data. Use when setting up API mocking for development or testing, creating mock handlers with variants, or sharing mocks between browser and Node environments.
---

# API Mocking with MSW

> **Quick Guide:** Handlers with variant switching (default, empty, error). Shared between browser (dev) and Node (tests). Separate mock data from handlers for reusability. Type-safe using your API's generated types. Use `setupWorker` (browser) and `setupServer` (Node) -- never swap them.

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Mock data, variant handlers, server worker, per-test overrides, runtime switching, network simulation
- [examples/browser.md](examples/browser.md) - Browser worker setup, SPA/SSR integration
- [reference.md](reference.md) - Decision frameworks, red flags, anti-patterns

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST separate mock data from handlers - handlers in `handlers/`, data in `mocks/`)**

**(You MUST use `setupWorker` for browser/development and `setupServer` for Node/tests - NEVER swap them)**

**(You MUST reset handlers after each test with `server.resetHandlers()` in `afterEach`)**

**(You MUST use named constants for HTTP status codes and delays - NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** MSW, msw, mock handlers, mock data, API mocking, setupWorker, setupServer, http.get, HttpResponse

**When to use:**

- Mocking API responses during development before backend is ready
- Testing different API scenarios (success, empty, error states)
- Sharing the same mock definitions between browser dev and Node test environments
- Simulating network conditions (latency, timeouts)
- Per-test handler overrides for isolated test scenarios

**When NOT to use:**

- Integration tests needing real backend validation (use a test database)
- Production builds (MSW should never ship to production)
- Pure function unit tests with no network calls
- Testing actual network failure modes (use test containers)

**Key patterns covered:**

- Handler/data separation for reusability and type safety
- Variant-based handlers (default, empty, error scenarios)
- Browser worker for development, server worker for tests
- Per-test handler overrides with `server.use()`
- Runtime variant switching for UI development

---

<philosophy>

## Philosophy

MSW intercepts network requests at the service worker (browser) or class extension (Node) level, providing realistic API mocking without changing application code. Keep mock data separate from handlers for reusability, type handlers against your generated API types, and organize handlers by domain/feature.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Separate Mock Data from Handlers

Define mock data as typed constants separate from MSW handlers. This enables type safety from your generated API types and reusability across handlers.

```typescript
// mocks/features.ts
import type { GetFeaturesResponse } from "./api-types";

export const defaultFeatures: GetFeaturesResponse = {
  features: [
    { id: "1", name: "Dark mode", status: "done" },
    { id: "2", name: "Auth", status: "in progress" },
  ],
};

export const emptyFeatures: GetFeaturesResponse = { features: [] };
```

For full variant handler examples, see [examples/core.md](examples/core.md).

**When not to use:** When mock data is truly one-off and specific to a single test case (use inline data in the test instead).

---

### Pattern 2: Handlers with Variant Switching

Create handlers that support multiple response scenarios (default, empty, error) with runtime switching for development and explicit overrides for testing.

```typescript
import { http, HttpResponse } from "msw";

const API_ENDPOINT = "api/v1/features";
const HTTP_STATUS_OK = 200;
const HTTP_STATUS_INTERNAL_SERVER_ERROR = 500;

export const getFeaturesHandlers = {
  defaultHandler: () =>
    http.get(API_ENDPOINT, () =>
      HttpResponse.json(defaultFeatures, { status: HTTP_STATUS_OK }),
    ),
  emptyHandler: () =>
    http.get(API_ENDPOINT, () =>
      HttpResponse.json(emptyFeatures, { status: HTTP_STATUS_OK }),
    ),
  errorHandler: () =>
    http.get(
      API_ENDPOINT,
      () =>
        new HttpResponse("Server error", {
          status: HTTP_STATUS_INTERNAL_SERVER_ERROR,
        }),
    ),
};
```

For full implementation with runtime switching, see [examples/core.md](examples/core.md).

---

### Pattern 3: Browser Worker (Development) vs Server Worker (Tests)

- Use `setupWorker` from `msw/browser` for browser/development
- Use `setupServer` from `msw/node` for Node/tests
- **Never swap them** -- `setupWorker` needs service worker APIs, `setupServer` needs Node APIs

```typescript
// browser-worker.ts
import { setupWorker } from "msw/browser";
export const browserWorker = setupWorker(...handlers);

// server-worker.ts
import { setupServer } from "msw/node";
export const server = setupServer(...handlers);
```

For browser app integration (SPA and SSR), see [examples/browser.md](examples/browser.md).

---

### Pattern 4: Test Lifecycle

Always follow this lifecycle to prevent test pollution:

```typescript
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Use `server.use()` for per-test overrides -- they are automatically cleaned up by `resetHandlers()`.

For per-test override examples, see [examples/core.md](examples/core.md).

</patterns>

---

<red_flags>

## RED FLAGS

- ❌ Using `setupWorker` in Node tests or `setupServer` in browser -- wrong API for environment causes cryptic failures
- ❌ Not resetting handlers between tests (`afterEach(() => server.resetHandlers())`) -- causes test pollution
- ❌ Mixing handlers and mock data in same file -- reduces reusability and type safety
- ❌ Missing `await` when starting browser worker before render -- race conditions cause intermittent failures
- ⚠️ Only testing happy path (no empty/error variants) -- incomplete coverage
- ⚠️ No `onUnhandledRequest` configuration -- unclear which requests are mocked vs real

**Gotchas & Edge Cases:**

- `delay()` with no arguments is automatically negated in Node.js -- use explicit duration if you need delay in tests
- Handler overrides via `server.use()` persist until `resetHandlers()` -- they do NOT auto-reset between tests
- `http.all()` matches any HTTP method on a path -- convenient but can mask bugs if overused
- Dynamic imports are required for browser worker in SSR frameworks to avoid server bundling issues

See [reference.md](reference.md) for detailed anti-pattern examples.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST separate mock data from handlers - handlers in `handlers/`, data in `mocks/`)**

**(You MUST use `setupWorker` for browser/development and `setupServer` for Node/tests - NEVER swap them)**

**(You MUST reset handlers after each test with `server.resetHandlers()` in `afterEach`)**

**(You MUST use named constants for HTTP status codes and delays - NO magic numbers)**

**Failure to follow these rules will cause test pollution, environment-specific failures, and hard-to-debug race conditions.**

</critical_reminders>
