---
name: writing-tests
description: Use when writing tests for peek-stash-browser. Covers Vitest + React Testing Library (client) and Vitest + integration testing (server). Follow these conventions exactly.
---

# Writing Tests for Peek

## Stack

- **Framework**: Vitest 3.x (both client and server)
- **Client**: React Testing Library 16.x, happy-dom, @testing-library/user-event
- **Server unit**: Vitest in node environment, sequential execution
- **Server integration**: Real HTTP client against live server + Stash test instance

## Client Tests

### Location & Naming

Tests live in `client/tests/` mirroring the source structure:

```
client/tests/
  components/ui/       # UI component tests
  components/cards/    # Card component tests
  components/timeline/ # Timeline tests
  hooks/               # Hook tests
  utils/               # Utility function tests
  integration/         # Integration tests
  mocks/               # Mock providers
  mockData.js          # Shared test data factories
  testUtils.jsx        # Shared rendering helpers
  setup.js             # Global browser API mocks
```

File naming: `ComponentName.test.jsx` or `hookName.test.js`

### Test Structure

```jsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";

describe("ComponentName", () => {
  const defaultProps = { /* ... */ };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("Rendering", () => {
    it("renders with correct aria-label", () => {
      render(<Component {...defaultProps} />);
      expect(screen.getByRole("option")).toHaveAttribute("aria-label", "expected");
    });
  });

  describe("Interactions", () => {
    it("calls onClick when clicked", async () => {
      const user = userEvent.setup();
      const onClick = vi.fn();
      render(<Component {...defaultProps} onClick={onClick} />);
      await user.click(screen.getByRole("button"));
      expect(onClick).toHaveBeenCalledWith("expected-arg");
    });
  });
});
```

### Key Conventions

- **Query priority**: `getByRole` > `getByText` > `getByTestId` (accessibility-first)
- **User events**: Always use `userEvent.setup()`, not `fireEvent`
- **Async**: Use `await user.click()`, `waitFor()`, and `act()` properly
- **Mock callbacks**: `vi.fn()` for all callback props
- **Group by behavior**: Nest `describe()` blocks by "Rendering", "Interactions", "Edge Cases"
- **Clear mocks**: `vi.clearAllMocks()` in `beforeEach()`

### Test Data Factories (`mockData.js`)

```javascript
import { createScene, createPerformer, createStudio, resetIdCounter } from "@tests/mockData";

// Factory with overrides
const scene = createScene({ title: "Custom Title", rating100: 85 });
const performer = createPerformer({ name: "Jane", gender: "FEMALE" });

// Reset counters between test suites
beforeEach(() => resetIdCounter());
```

### Rendering Helpers (`testUtils.jsx`)

```jsx
import { renderWithProviders, createMockApi, flushPromises } from "@tests/testUtils";

// Render with router context
renderWithProviders(<Component />, { route: "/scenes/123" });

// Mock API for components that fetch
const mockApi = createMockApi();
```

### Hook Tests

```javascript
import { renderHook, act } from "@testing-library/react";

it("updates when input changes", () => {
  const { result, rerender } = renderHook(
    ({ query }) => useMyHook(query),
    { initialProps: { query: "initial" } }
  );
  expect(result.current).toBe(expectedInitial);

  rerender({ query: "updated" });
  expect(result.current).toBe(expectedUpdated);
});
```

### Path Aliases

```javascript
import Component from "@/components/Component";  // src/
import { mockData } from "@tests/mockData";       // tests/
```

### What's Mocked Globally (setup.js)

- `window.matchMedia` - returns `{ matches: false }`
- `IntersectionObserver` - no-op observe/unobserve
- `ResizeObserver` - no-op observe/unobserve
- `Element.scrollIntoView` - no-op

## Server Unit Tests

### Location & Naming

```
server/tests/
  services/          # Service logic
  filters/           # Filter logic
  controllers/       # Controller tests
  routes/            # Route tests
  middleware/        # Middleware tests
  schemas/           # Schema validation
  helpers/           # Test utilities
    mockDataGenerators.ts
```

File naming: `ServiceName.test.ts`

### Mocking Prisma

```typescript
// Mock BEFORE importing the service under test
vi.mock("../../prisma/singleton.js", () => ({
  default: {
    user: { findUnique: vi.fn(), findMany: vi.fn() },
    scene: { findFirst: vi.fn(), count: vi.fn() },
  },
}));

import { myService } from "../../services/MyService.js";
import prisma from "../../prisma/singleton.js";
const mockPrisma = vi.mocked(prisma);
```

### Key Conventions

- **Sequential execution**: `fileParallelism: false` prevents DB conflicts
- **Mock before import**: Always `vi.mock()` before importing the module
- **Typed mocks**: Use `vi.mocked()` for TypeScript type safety
- **No real DB**: Unit tests never touch SQLite

## Server Integration Tests

### Location & Naming

```
server/integration/
  api/               # API endpoint tests
  services/          # Service integration tests
  helpers/
    globalSetup.ts   # One-time server startup + migration + sync
    testClient.ts    # HTTP client with auth
    testSetup.ts     # Ensure admin user exists
  fixtures/
    testEntities.ts  # Test instance entity IDs (git-ignored, copy from .example)
```

File naming: `feature-name.integration.test.ts`

### TestClient Pattern

```typescript
import { adminClient, TestClient } from "../helpers/testClient.js";

// Admin is pre-authenticated via globalSetup
const response = await adminClient.get<{ users: User[] }>("/api/user/all");
expect(response.ok).toBe(true);
expect(response.status).toBe(200);

// Create per-test user clients
const userClient = new TestClient();
await userClient.login("username", "password");
```

### Integration Test Structure

```typescript
describe("Feature Integration Tests", () => {
  let testUserId: number;

  beforeAll(async () => {
    // Create test data via API
    const res = await adminClient.post("/api/user/create", { ... });
    testUserId = res.data.user.id;
  });

  afterAll(async () => {
    // Cleanup test data
    await adminClient.delete(`/api/user/${testUserId}`);
  });

  it("should return 403 for unauthorized access", async () => {
    const response = await guestClient.get("/api/admin/endpoint");
    expect(response.ok).toBe(false);
    expect(response.status).toBe(403);
  });
});
```

### Running Integration Tests

Requires `.env` with `STASH_TEST_URL` and `STASH_TEST_API_KEY` pointing to the test instance.

```bash
npm run test:integration          # Standard run
npm run test:integration:fresh    # Fresh database (FRESH_DB=true)
npm run test:integration:watch    # Watch mode
```

### Test Stash Instance

Integration tests run against a dedicated test Stash instance. Connection details are configured via environment variables — not hardcoded.

**Required `.env` variables:**
- `STASH_TEST_URL` — GraphQL endpoint of the test Stash instance
- `STASH_TEST_API_KEY` — API key for authentication

**Setting up test entities:**
Test entities can be created/modified via Stash GraphQL API:
```bash
curl -s "$STASH_TEST_URL" \
  -H "ApiKey: $STASH_TEST_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"query": "mutation { ... }"}'
```

Common mutations:
- `groupCreate(input: { name: "..." })`
- `sceneUpdate(input: { id: "X", groups: [{ group_id: "Y" }] })`
- `galleryCreate(input: { title: "...", tag_ids: [...] })`
- `imageUpdate(input: { id: "X", gallery_ids: ["Y"] })`
- `performerUpdate(input: { id: "X", tag_ids: [...] })`
- `metadataScan(input: { paths: ["/images"] })`

**First-time setup:**
1. Set `STASH_TEST_URL` and `STASH_TEST_API_KEY` in `.env`
2. Copy `server/integration/fixtures/testEntities.example.ts` to `testEntities.ts`
3. Fill in entity IDs from your Stash library

## E2E Tests (Playwright)

### Location & Naming

```
e2e/
  auth.setup.ts       # Login and save storage state
  global-setup.ts     # Bootstrap admin user on fresh DB
  auth.spec.ts        # Auth flow tests
  navigation.spec.ts  # Page navigation tests
```

File naming: `feature-name.spec.ts`

### Configuration

- Config: `playwright.config.ts` (project root)
- Browser: Chromium only (expand later)
- Auth: Storage state saved by setup project, reused by all tests
- CI: Playwright starts server + client via `webServer` config
- Local: Tests run against docker-compose at `localhost:6969`

### Key Conventions

- **Locator priority**: `getByRole` > `getByText` > `getByTestId` (same as RTL)
- **No `waitForTimeout()`**: Use `expect(locator).toBeVisible()` or `waitForURL()`
- **Web-first assertions**: `expect(locator)` auto-retries
- **Isolate tests**: No shared state, no execution-order dependencies
- **Mock external only**: Never mock the app itself; mock third-party APIs if needed

### Running E2E Tests

```bash
# Requires docker-compose running (or set E2E_BASE_URL)
npm run test:e2e              # Headless
npm run test:e2e:headed       # With browser visible
npm run test:e2e:ui           # Playwright UI mode
```

### Coverage Thresholds

Both client and server enforce coverage thresholds in CI. If coverage drops below thresholds, the build fails.

| Metric | Client | Server |
|--------|--------|--------|
| Statements | 35% | 63% |
| Branches | 76% | 72% |
| Functions | 42% | 68% |
| Lines | 35% | 63% |

## Running Tests

```bash
# Client
cd client && npm test             # Watch mode
cd client && npm run test:run     # Single run
cd client && npm run test:coverage

# Server unit
cd server && npm test
cd server && npm run test:run
cd server && npm run test:coverage

# Server integration
cd server && npm run test:integration

# E2E
npm run test:e2e
```
