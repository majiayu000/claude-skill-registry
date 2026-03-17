---
name: web-mocks-msw
description: MSW handlers, browser/server workers, test data. Use when setting up API mocking for development or testing, creating mock handlers with variants, or sharing mocks between browser and Node environments.
---

# API Mocking with MSW

> **Quick Guide:** Centralized mocks in `@repo/api-mocks`. Handlers with variant switching (default, empty, error). Shared between browser (dev) and Node (tests). Type-safe using generated types from `@repo/api/types`.

**Detailed Resources:**

- For code examples, see [examples/](examples/) (core, browser, node, testing, advanced)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Using This Skill

**(You MUST separate mock data from handlers - handlers in `handlers/`, data in `mocks/`)**

**(You MUST use `setupWorker` for browser/development and `setupServer` for Node/tests - NEVER swap them)**

**(You MUST reset handlers after each test with `serverWorker.resetHandlers()` in `afterEach`)**

**(You MUST use generated types from `@repo/api/types` - NEVER manually define API response types)**

**(You MUST use named constants for HTTP status codes and delays - NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** MSW setup, mock handlers, mock data, API mocking, testing mocks, development mocks, setupWorker, setupServer

**When to use:**

- Setting up MSW for development and testing
- Creating centralized mock handlers with variant switching
- Sharing mocks between browser (dev) and Node (tests)
- Testing different API scenarios (success, empty, error)
- Simulating network latency and error conditions

**When NOT to use:**

- Integration tests that need real backend validation (use test database instead)
- Production builds (MSW should never ship to production)
- Simple unit tests of pure functions (no network calls to mock)
- When you need to test actual network failure modes (use test containers)

**Key patterns covered:**

- Centralized mock package structure with handlers and data separation
- Variant-based handlers (default, empty, error scenarios)
- Browser worker for development, server worker for tests
- Per-test handler overrides for specific scenarios
- Runtime variant switching for UI development

---

<philosophy>

## Philosophy

MSW (Mock Service Worker) intercepts network requests at the service worker level, providing realistic API mocking without changing application code. This skill enforces a centralized approach where mocks live in a dedicated package (`@repo/api-mocks`), enabling consistent behavior across development and testing environments.

**When to use MSW:**

- Developing frontend features before backend API is ready
- Testing different API response scenarios (success, empty, error states)
- Simulating network conditions (latency, timeouts)
- Creating a consistent development environment across team
- End-to-end testing with controlled API responses

**When NOT to use MSW:**

- Integration tests that need real backend validation (use test database)
- Production builds (MSW should never ship to production)
- Simple unit tests of pure functions (no network calls)
- When you need to test actual network failure modes (use test containers)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Centralized Mock Package Structure

Organize all mocks in a dedicated workspace package with clear separation between handlers (MSW request handlers) and mock data (static response data).

#### Package Structure

```
packages/api-mocks/
├── src/
│   ├── handlers/
│   │   ├── index.ts              # Export all handlers
│   │   └── features/
│   │       └── get-features.ts   # MSW handlers with variants
│   ├── mocks/
│   │   ├── index.ts              # Export all mock data
│   │   └── features.ts           # Mock data
│   ├── browser-worker.ts         # Browser MSW worker (development)
│   ├── server-worker.ts          # Node.js MSW server (tests)
│   └── manage-mock-selection.ts  # Variant switching logic
└── package.json
```

For package configuration examples, see [examples/core.md](examples/core.md#package-configuration).

---

### Pattern 2: Separate Mock Data from Handlers

Define mock data as typed constants in `mocks/` directory, completely separate from MSW handlers. This enables type safety from generated API types and reusability across handlers.

For code examples, see [examples/core.md](examples/core.md#mock-data-separation).

**When not to use:** When mock data is truly one-off and specific to a single test case (use inline data in the test instead).

---

### Pattern 3: Handlers with Variant Switching

Create handlers that support multiple response scenarios (default, empty, error) with runtime switching for development and explicit overrides for testing.

Key principles:

- Named constants for HTTP status codes
- Response factories for consistency
- Variant switching via centralized state
- Explicit handler exports for per-test overrides

For implementation examples, see [examples/core.md](examples/core.md#variant-handlers).

---

### Pattern 4: Browser Worker for Development

Set up MSW browser worker to intercept requests during development. Key considerations:

- Use `setupWorker` from `msw/browser`
- Await worker start before rendering app
- Configure `onUnhandledRequest: "bypass"` for unmocked requests

For app integration examples, see [examples/browser.md](examples/browser.md).

---

### Pattern 5: Server Worker for Tests

Set up MSW server worker for Node.js test environment:

- Use `setupServer` from `msw/node`
- Lifecycle: `beforeAll` listen, `afterEach` reset, `afterAll` close
- Always reset handlers to prevent test pollution

For test setup examples, see [examples/node.md](examples/node.md).

</patterns>

---

<integration>

## Integration Guide

**Works with any:**

- **Data fetching solution**: MSW intercepts fetch calls at the network level - your data fetching library sees normal responses
- **Test runner**: Server worker integrates via test setup file (lifecycle hooks)
- **Testing utilities**: Works seamlessly with any component testing library
- **Frontend framework**: Browser worker integrates via app entry point

**Test runner configuration (generic):**

```typescript
// test-setup.ts (configure in your test runner)
import { serverWorker } from "@repo/api-mocks/serverWorker";

// Use your test runner's lifecycle hooks
beforeAll(() => serverWorker.listen());
afterEach(() => serverWorker.resetHandlers());
afterAll(() => serverWorker.close());
```

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST separate mock data from handlers - handlers in `handlers/`, data in `mocks/`)**

**(You MUST use `setupWorker` for browser/development and `setupServer` for Node/tests - NEVER swap them)**

**(You MUST reset handlers after each test with `serverWorker.resetHandlers()` in `afterEach`)**

**(You MUST use generated types from `@repo/api/types` - NEVER manually define API response types)**

**(You MUST use named constants for HTTP status codes and delays - NO magic numbers)**

**Failure to follow these rules will cause test pollution, type drift from real API, environment-specific failures, and hard-to-debug race conditions.**

</critical_reminders>
