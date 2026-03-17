---
name: testing-strategy
description: Guide for running and writing tests in the Orient monorepo. Use when asked to "run tests", "write tests", "add test coverage", "debug failing tests", "check which tests to run", or when making code changes that require testing. Covers test categories (unit, integration, E2E), monorepo test execution, mock usage, and test patterns for services, handlers, tools, and database operations.
---

# Testing Strategy

## Quick Reference - Monorepo Test Commands

### Run All Tests

```bash
# Run all tests (root + packages)
pnpm test

# Run with turborepo (parallel, cached)
pnpm turbo test
```

### Package-Specific Tests

```bash
# Core package
pnpm --filter @orientbot/core test

# Database package
pnpm --filter @orientbot/database test
pnpm --filter @orientbot/database test:e2e  # E2E tests

# MCP Tools package
pnpm --filter @orientbot/mcp-tools test
```

### Root-Level Tests (during migration)

```bash
# Run all unit + integration tests
npm test

# Run only unit tests
npm run test:unit

# Run integration tests
npm run test:integration

# Run E2E tests (requires SQLite database)
npm run test:e2e

# CI mode (excludes E2E)
npm run test:ci

# Watch mode
npm run test:watch

# With coverage
npm run test:coverage
```

### Specific Test Files

```bash
# Single test file
npm test -- src/services/__tests__/jiraService.test.ts

# Package test file
pnpm --filter @orientbot/core test -- __tests__/config.test.ts

# Pattern matching
npm test -- --testNamePattern="chatPermission"
```

## Test Categories

### Unit Tests (\*.test.ts)

- **Location**: `packages/*/\__tests__/*.test.ts` and `src/**/\__tests__/*.test.ts`
- **Purpose**: Test isolated service/handler logic with mocked dependencies
- **Dependencies**: None - all external services mocked
- **When to write**: For business logic, utility functions, service methods

### Integration Tests (\*.integration.test.ts)

- **Location**: `src/services/__tests__/*.integration.test.ts`, `tests/integration/`
- **Purpose**: Test handler flows with multiple mocked components working together
- **Dependencies**: None - uses mock factories for external APIs
- **When to write**: For MCP tool handlers, multi-service workflows, skill editing flows

### E2E Tests (\*.e2e.test.ts)

- **Location**: `src/db/__tests__/*.e2e.test.ts`, `tests/e2e/`
- **Purpose**: Test real database operations with SQLite, or real OpenCode server interactions
- **Dependencies**: SQLite database file OR OpenCode server
- **When to write**: For database schema changes, complex queries, OpenCode session management
- **Note**: Skipped automatically in CI if required services are not running

### Contract Tests (\*.contract.test.ts)

- **Location**: `tests/contracts/`
- **Purpose**: Verify package public APIs remain stable
- **When to write**: When changing package exports

### Docker Tests (tests/docker/)

- **Location**: `tests/docker/`
- **Purpose**: Verify Dockerfiles build and containers start correctly
- **Dependencies**: Docker runtime
- **When to write**: When modifying Dockerfiles, compose files, or container entry points
- **Skip with**: `SKIP_DOCKER_TESTS=1`

```bash
# Run all Docker tests
pnpm test:docker:files

# Run build validation only
pnpm test:docker:build

# Skip slow build tests (just check Dockerfile existence)
SKIP_DOCKER_TESTS=1 pnpm test:docker:files
```

**Docker Test Categories:**

| Test File         | Purpose                                                 |
| ----------------- | ------------------------------------------------------- |
| `build.test.ts`   | Verify Dockerfile existence and optionally build images |
| `startup.test.ts` | Verify containers start and run correctly               |
| `compose.test.ts` | Validate docker-compose.v2.yml structure and syntax     |

## Package Test Structure

```
orienter/
├── packages/
│   ├── core/
│   │   ├── __tests__/
│   │   │   ├── config.test.ts
│   │   │   └── utils.test.ts
│   │   └── vitest.config.ts
│   ├── database/
│   │   ├── __tests__/
│   │   │   ├── schema.test.ts
│   │   │   └── client.e2e.test.ts
│   │   └── vitest.config.ts
│   └── mcp-tools/
│       ├── __tests__/
│       │   └── registry.test.ts
│       └── vitest.config.ts
├── tests/
│   ├── docker/                 # Docker build and startup tests
│   │   ├── build.test.ts       # Dockerfile validation
│   │   ├── startup.test.ts     # Container startup tests
│   │   └── compose.test.ts     # Compose file validation
│   ├── e2e/                    # System-level E2E tests
│   ├── integration/            # Cross-package integration
│   └── contracts/              # Package API stability
├── src/                        # Legacy tests (during migration)
│   └── */__tests__/*.test.ts
└── vitest.workspace.ts         # Workspace orchestration
```

## Decision Tree - Which Tests to Run

| Modified Package/File                           | Tests to Run               | Command                                                      |
| ----------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| `packages/core/src/**`                          | Core unit tests            | `pnpm --filter @orientbot/core test`                         |
| `packages/database/src/**`                      | Database tests             | `pnpm --filter @orientbot/database test`                     |
| `packages/database/src/schema/**`               | Database E2E               | `pnpm --filter @orientbot/database test:e2e`                 |
| `packages/mcp-tools/src/**`                     | MCP Tools tests            | `pnpm --filter @orientbot/mcp-tools test`                    |
| `packages/dashboard-frontend/src/routes.ts`     | Frontend routing tests     | `pnpm --filter @orientbot/dashboard-frontend test -- routes` |
| `packages/dashboard-frontend/src/components/**` | Frontend component tests   | `pnpm --filter @orientbot/dashboard-frontend test`           |
| `packages/dashboard-frontend/src/api.ts`        | API client + constants     | `pnpm --filter @orientbot/dashboard-frontend test`           |
| `packages/dashboard-frontend/src/App.tsx`       | Frontend integration tests | `pnpm --filter @orientbot/dashboard-frontend test`           |
| `packages/bot-whatsapp/src/services/**`         | WhatsApp service tests     | `pnpm --filter @orientbot/bot-whatsapp test`                 |
| `src/services/*.ts`                             | Service unit tests         | `npm test -- src/services/__tests__/<name>.test.ts`          |
| `src/services/openCode*.ts`                     | OpenCode E2E               | `npx vitest run tests/e2e/opencode-session.e2e.test.ts`      |
| `src/tools/*.ts`                                | Tool tests                 | `npm run test:tools`                                         |
| `src/db/*.ts`                                   | E2E database tests         | `npm run test:e2e`                                           |
| `packages/*/Dockerfile`                         | Docker tests               | `pnpm test:docker:files`                                     |
| `docker/docker-compose*.yml`                    | Docker compose tests       | `pnpm test:docker:files`                                     |
| `packages/*/src/main.ts`                        | Entry point + Docker tests | Package test + `pnpm test:docker:files`                      |
| Multiple files                                  | All tests                  | `npm run test:ci`                                            |

## Writing New Tests

### Package Unit Test Template

```typescript
/**
 * Unit Tests for [ModuleName]
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Mock @orientbot/core if needed
vi.mock('@orientbot/core', () => ({
  createServiceLogger: () => ({
    debug: vi.fn(),
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
    startOperation: () => ({ success: vi.fn(), failure: vi.fn() }),
  }),
  loadConfig: () => ({
    /* mock config */
  }),
}));

describe('ModuleName', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('methodName', () => {
    it('should do something when condition is met', async () => {
      // Arrange
      const input = { key: 'value' };

      // Act
      const result = await doSomething(input);

      // Assert
      expect(result).toBeDefined();
    });
  });
});
```

### Frontend Routing Tests (React/Vitest)

Test routing utilities (`getRouteState`, `getRoutePath`) for React applications:

```typescript
/**
 * Tests for Frontend URL Routing
 * Location: packages/dashboard-frontend/__tests__/routes.test.ts
 */

import { describe, it, expect } from 'vitest';
import { getRouteState, getRoutePath, ROUTES } from '../src/routes';

describe('Frontend URL Routing', () => {
  // Test route constants exist
  describe('ROUTES constants', () => {
    it('should have all expected route paths', () => {
      expect(ROUTES.SETTINGS).toBe('/settings');
      expect(ROUTES.SETTINGS_APPEARANCE).toBe('/settings/appearance');
    });
  });

  // Test getRouteState - derives state from URL pathname
  describe('getRouteState', () => {
    it('should match route path and return correct view state', () => {
      const state = getRouteState('/settings/appearance');
      expect(state.globalView).toBe('settings');
      expect(state.settingsView).toBe('appearance');
    });

    it('should return default state for unknown paths', () => {
      const state = getRouteState('/unknown');
      expect(state.globalView).toBeNull();
      expect(state.activeService).toBe('whatsapp'); // default
    });
  });

  // Test getRoutePath - generates URL from view state
  describe('getRoutePath', () => {
    it('should return correct path for view', () => {
      expect(getRoutePath('settings', 'whatsapp', 'appearance')).toBe('/settings/appearance');
    });
  });

  // Test round-trip consistency
  describe('route consistency', () => {
    it('should have matching getRouteState and getRoutePath', () => {
      const path = getRoutePath('settings', 'whatsapp', 'appearance');
      const state = getRouteState(path);
      expect(state.globalView).toBe('settings');
      expect(state.settingsView).toBe('appearance');
    });
  });
});
```

**Key patterns for routing tests:**

1. **Route constants** - Verify all route paths are defined correctly
2. **getRouteState** - Test URL → state derivation for each route pattern
3. **getRoutePath** - Test state → URL generation
4. **Round-trip consistency** - Ensure `getRouteState(getRoutePath(...))` returns expected state
5. **Default handling** - Test fallback behavior for unknown routes

**Run frontend tests:**

```bash
pnpm --filter dashboard-frontend test
pnpm --filter dashboard-frontend test -- __tests__/routes.test.ts
```

### Frontend Component Tests (React/Vitest)

Test React components with mocking strategies for async state management, fetch calls, and browser APIs:

```typescript
/**
 * Component Tests with Async State Management
 * Location: packages/dashboard-frontend/__tests__/MyComponent.test.tsx
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import MyComponent from '../src/components/MyComponent';

// Mock the API module
vi.mock('../src/api', async () => {
  const actual = await vi.importActual('../src/api');
  return {
    ...actual,
    saveData: vi.fn(),
    fetchData: vi.fn(),
  };
});

import { saveData, fetchData } from '../src/api';
const mockSaveData = saveData as ReturnType<typeof vi.fn>;
const mockFetchData = fetchData as ReturnType<typeof vi.fn>;

// Mock fetch for direct API calls
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Wrapper component for router context
function TestWrapper({ children }: { children: React.ReactNode }) {
  return <BrowserRouter>{children}</BrowserRouter>;
}

describe('MyComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    mockFetch.mockReset();
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe('Loading State', () => {
    it('should show loading state initially', () => {
      // Mock fetch that never resolves to keep loading state
      mockFetch.mockImplementation(() => new Promise(() => {}));

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });
  });

  describe('Async Data Fetching', () => {
    it('should fetch and display data', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ items: ['a', 'b', 'c'] }),
      });

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText('a')).toBeInTheDocument();
      });
    });

    it('should handle fetch errors gracefully', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ error: 'Server error' }),
      });

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText(/error/i)).toBeInTheDocument();
      });
    });
  });

  describe('Polling Behavior', () => {
    it('should poll for updates', async () => {
      let callCount = 0;
      mockFetch.mockImplementation(() => {
        callCount++;
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            status: callCount === 1 ? 'pending' : 'complete',
            data: callCount > 1 ? 'result' : null,
          }),
        });
      });

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      // Wait for transition from pending to complete
      await waitFor(() => {
        expect(screen.getByText('result')).toBeInTheDocument();
      }, { timeout: 5000 });

      expect(callCount).toBeGreaterThanOrEqual(2);
    });
  });

  describe('LocalStorage Interaction', () => {
    it('should persist state to localStorage', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      });

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      fireEvent.click(screen.getByText('Save'));

      await waitFor(() => {
        expect(localStorage.getItem('my_key')).toBeTruthy();
      });
    });

    it('should restore state from localStorage', () => {
      localStorage.setItem('my_key', 'saved_value');

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      expect(screen.getByDisplayValue('saved_value')).toBeInTheDocument();
    });
  });

  describe('Form Submission', () => {
    it('should validate and submit form', async () => {
      mockSaveData.mockResolvedValue({ success: true });

      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      // Fill form
      fireEvent.change(screen.getByLabelText('Name'), {
        target: { value: 'Test Value' },
      });

      // Submit
      fireEvent.click(screen.getByText('Submit'));

      await waitFor(() => {
        expect(mockSaveData).toHaveBeenCalledWith('Test Value');
      });
    });

    it('should show validation error for invalid input', async () => {
      render(
        <TestWrapper>
          <MyComponent />
        </TestWrapper>
      );

      // Submit without filling required field
      fireEvent.click(screen.getByText('Submit'));

      await waitFor(() => {
        expect(screen.getByText('Name is required')).toBeInTheDocument();
      });
    });
  });
});
```

**Key patterns for React component tests:**

1. **Mock fetch globally** - Use `global.fetch = vi.fn()` for direct API calls
2. **Mock API modules** - Use `vi.mock('../src/api')` for imported API functions
3. **Router context** - Wrap components in `BrowserRouter` when using `<Link>` or `useNavigate`
4. **localStorage cleanup** - Clear in `beforeEach` and `afterEach` to prevent test pollution
5. **Polling tests** - Use `callCount` tracking and `waitFor` with timeout
6. **Form testing** - Use `fireEvent.change` for inputs, `fireEvent.click` for buttons

### Testing Select/Dropdown Components

```typescript
import { COUNTRY_CODES } from '../src/api';

describe('Country Code Dropdown', () => {
  it('should have correct structure for all entries', () => {
    COUNTRY_CODES.forEach((country) => {
      expect(country).toHaveProperty('code');
      expect(country).toHaveProperty('name');
      expect(country).toHaveProperty('flag');
    });
  });

  it('should match longest prefix first', () => {
    const phone = '972501234567';

    // Sort by length descending (longer codes first)
    const sortedCodes = [...COUNTRY_CODES].sort(
      (a, b) => b.code.length - a.code.length
    );

    const match = sortedCodes.find((c) => phone.startsWith(c.code));
    expect(match?.code).toBe('972'); // Matches 972, not 97 or 9
  });

  it('should select option in dropdown', async () => {
    render(<TestWrapper><MyForm /></TestWrapper>);

    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: '44' } });

    expect(select).toHaveValue('44');
  });
});
```

### Testing UI State Transitions

```typescript
describe('UI State Transitions', () => {
  it('should transition through states correctly', async () => {
    let callCount = 0;
    mockFetch.mockImplementation(() => {
      callCount++;
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          isConnected: callCount > 1,
          syncState: callCount === 2 ? 'syncing' : callCount > 2 ? 'ready' : 'idle',
          syncProgress: { chatsReceived: callCount * 10, isLatest: callCount > 2 },
        }),
      });
    });

    render(<TestWrapper><StatusPanel /></TestWrapper>);

    // Initial loading
    expect(screen.getByText('Loading...')).toBeInTheDocument();

    // After first fetch - not connected
    await waitFor(() => {
      expect(screen.getByText('Not Connected')).toBeInTheDocument();
    });

    // Simulate connection event (via polling)
    await waitFor(() => {
      expect(screen.getByText('Syncing...')).toBeInTheDocument();
    }, { timeout: 5000 });

    // Final state - ready
    await waitFor(() => {
      expect(screen.getByText('Connected')).toBeInTheDocument();
    }, { timeout: 5000 });
  });
});
```

### Mocking Browser APIs

```typescript
// Mock window.confirm
const mockConfirm = vi.fn();
window.confirm = mockConfirm;

describe('Confirmation Dialogs', () => {
  it('should show confirmation before destructive action', async () => {
    mockConfirm.mockReturnValue(true);

    render(<TestWrapper><DangerButton /></TestWrapper>);
    fireEvent.click(screen.getByText('Delete'));

    expect(mockConfirm).toHaveBeenCalledWith(
      expect.stringContaining('Are you sure')
    );
  });

  it('should cancel action if user declines', async () => {
    mockConfirm.mockReturnValue(false);
    mockFetch.mockClear();

    render(<TestWrapper><DangerButton /></TestWrapper>);
    fireEvent.click(screen.getByText('Delete'));

    expect(mockFetch).not.toHaveBeenCalled();
  });
});

// Mock window.open for OAuth flows
const mockOpen = vi.fn();
window.open = mockOpen;

// Mock navigator.clipboard
const mockClipboard = {
  writeText: vi.fn().mockResolvedValue(undefined),
  readText: vi.fn().mockResolvedValue(''),
};
Object.assign(navigator, { clipboard: mockClipboard });
```

**Run frontend component tests:**

```bash
pnpm --filter @orientbot/dashboard-frontend test
pnpm --filter @orientbot/dashboard-frontend test -- __tests__/MyComponent.test.tsx
pnpm --filter @orientbot/dashboard-frontend test -- --testNamePattern="state transition"
```

### Cross-Package Integration Test Template

```typescript
/**
 * Integration Tests for [Feature]
 * Tests interaction between @orientbot/core and @orientbot/database
 */

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { loadConfig } from '@orientbot/core';
import { getDatabase, closeDatabase } from '@orientbot/database';

describe('Feature Integration', () => {
  beforeAll(async () => {
    // Setup shared resources
  });

  afterAll(async () => {
    await closeDatabase();
  });

  it('should work across packages', async () => {
    const config = loadConfig();
    const db = getDatabase();

    // Test cross-package interaction
  });
});
```

## Mock Usage

### Standard Mocks

```typescript
// Mock @orientbot/core logger
vi.mock('@orientbot/core', () => ({
  createServiceLogger: () => ({
    debug: vi.fn(),
    info: vi.fn(),
    warn: vi.fn(),
    error: vi.fn(),
    startOperation: () => ({
      success: vi.fn(),
      failure: vi.fn(),
    }),
  }),
}));

// Mock legacy paths (for src/ files)
vi.mock('../../utils/logger', () => import('../../__mocks__/logger'));
vi.mock('../../config', () => import('../../__mocks__/config'));
```

For detailed mock usage, see [references/mock-catalog.md](references/mock-catalog.md).
For test patterns, see [references/test-patterns.md](references/test-patterns.md).
For file-test mapping, see [references/file-test-mapping.md](references/file-test-mapping.md).

## Testing Database Services

Database services (e.g., `StorageDatabase`, `SchedulerDatabase`) require special testing approaches due to their reliance on SQLite connections.

### Integration vs Unit Test Trade-offs

| Approach                  | Pros                                       | Cons                                     | When to Use                     |
| ------------------------- | ------------------------------------------ | ---------------------------------------- | ------------------------------- |
| **Unit tests with mocks** | Fast, no DB needed, isolated               | Complex mocking, may miss real DB issues | Simple logic, utility methods   |
| **Integration tests**     | Tests real DB behavior, catches SQL errors | Slower, requires SQLite                  | Schema changes, complex queries |
| **API-level tests**       | Tests full stack, simpler mocking          | Less granular                            | Bridge endpoints, service APIs  |

**Recommended approach**: Test database services through their API endpoints (like bridge API tests) rather than mocking `pg.Pool` directly. This provides better coverage with simpler test code.

### Mocking SQLite/Drizzle (Complex - Often Avoid)

Mocking the Drizzle ORM is complex. Prefer API-level testing instead:

```typescript
// WARNING: This pattern is complex and fragile
// Prefer API-level testing instead

vi.mock('@orientbot/database', () => ({
  getDatabase: () => ({
    select: vi.fn().mockReturnValue({
      from: vi.fn().mockReturnValue({
        where: vi.fn().mockResolvedValue([]),
      }),
    }),
    insert: vi.fn().mockReturnValue({
      values: vi.fn().mockResolvedValue({ rowsAffected: 1 }),
    }),
  }),
}));
```

**Why direct mocking is problematic:**

1. Drizzle ORM has a fluent API with method chaining
2. You need to mock each method in the chain
3. Transaction testing requires careful mock sequencing
4. Mock setup is verbose and error-prone

### Better Pattern: API-Level Testing

Test database functionality through the API layer that uses it:

```typescript
/**
 * Test storage functionality through the bridge API
 * Much simpler than mocking pg.Pool directly
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import express from 'express';
import request from 'supertest';

describe('Bridge API Storage Endpoints', () => {
  let app: express.Express;
  let mockStorageDb: {
    set: ReturnType<typeof vi.fn>;
    get: ReturnType<typeof vi.fn>;
    delete: ReturnType<typeof vi.fn>;
    list: ReturnType<typeof vi.fn>;
    clear: ReturnType<typeof vi.fn>;
  };

  beforeEach(() => {
    // Mock the database service (not pg.Pool)
    mockStorageDb = {
      set: vi.fn().mockResolvedValue(undefined),
      get: vi.fn().mockResolvedValue(null),
      delete: vi.fn().mockResolvedValue(true),
      list: vi.fn().mockResolvedValue([]),
      clear: vi.fn().mockResolvedValue(0),
    };

    // Create express app with mocked service
    app = express();
    app.use(express.json());

    // Mount your route handler with mocked service
    app.post('/api/apps/bridge', async (req, res) => {
      const { method, params } = req.body;

      switch (method) {
        case 'storage.get':
          const value = await mockStorageDb.get('app', params.key);
          return res.json({ data: value });
        // ... other methods
      }
    });
  });

  it('should return stored value', async () => {
    mockStorageDb.get.mockResolvedValue({ items: ['a', 'b'] });

    const response = await request(app)
      .post('/api/apps/bridge')
      .send({ method: 'storage.get', params: { key: 'data' } });

    expect(response.status).toBe(200);
    expect(response.body.data).toEqual({ items: ['a', 'b'] });
  });
});
```

### Testing Async Database Operations

For async database operations, use these patterns:

```typescript
describe('Async Database Operations', () => {
  it('should handle successful async operation', async () => {
    mockDb.create.mockResolvedValue({ id: 1, name: 'test' });

    const result = await service.createItem({ name: 'test' });

    expect(result.id).toBe(1);
    expect(mockDb.create).toHaveBeenCalledWith({ name: 'test' });
  });

  it('should handle async rejection', async () => {
    mockDb.create.mockRejectedValue(new Error('Connection failed'));

    await expect(service.createItem({ name: 'test' })).rejects.toThrow('Connection failed');
  });

  it('should handle multiple sequential operations', async () => {
    mockDb.get
      .mockResolvedValueOnce(null) // First call
      .mockResolvedValueOnce({ id: 1 }); // Second call

    const first = await service.findItem('missing');
    const second = await service.findItem('exists');

    expect(first).toBeNull();
    expect(second).toEqual({ id: 1 });
  });
});
```

### E2E Database Tests

For tests that need a real database:

```typescript
/**
 * E2E Database Test Template
 * Requires: DATABASE_URL or TEST_DATABASE_URL environment variable
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import { StorageDatabase } from '../../packages/dashboard/src/services/storageDatabase.js';

const TEST_DB_URL = process.env.TEST_DATABASE_URL || process.env.DATABASE_URL;
const dbAvailable = !!TEST_DB_URL;

describe.skipIf(!dbAvailable)('StorageDatabase E2E', () => {
  let db: StorageDatabase;
  const testAppName = `test-app-${Date.now()}`; // Unique per test run

  beforeAll(async () => {
    db = new StorageDatabase(TEST_DB_URL);
    await db.initialize();
  });

  afterAll(async () => {
    // Clean up test data
    await db.clear(testAppName);
    await db.close();
  });

  beforeEach(async () => {
    // Reset state between tests
    await db.clear(testAppName);
  });

  it('should set and get a value', async () => {
    await db.set(testAppName, 'key1', { data: 'value1' });
    const result = await db.get(testAppName, 'key1');
    expect(result).toEqual({ data: 'value1' });
  });

  it('should list keys for an app', async () => {
    await db.set(testAppName, 'a', 1);
    await db.set(testAppName, 'b', 2);

    const keys = await db.list(testAppName);
    expect(keys).toContain('a');
    expect(keys).toContain('b');
  });
});
```

### Test Data Isolation

When testing database services, ensure test isolation:

```typescript
// Use unique identifiers per test run
const testAppName = `test-${Date.now()}-${Math.random().toString(36).slice(2)}`;

// Or use test-specific prefixes
const TEST_PREFIX = 'test_';

beforeEach(async () => {
  // Clean up any previous test data
  await db.query(`DELETE FROM app_storage WHERE app_name LIKE '${TEST_PREFIX}%'`);
});

afterAll(async () => {
  // Final cleanup
  await db.query(`DELETE FROM app_storage WHERE app_name LIKE '${TEST_PREFIX}%'`);
});
```

### Decision Tree: Database Test Approach

```
Need to test database service?
│
├─ Is it simple CRUD logic?
│  └─ YES → Mock the service interface, test through API
│
├─ Does it involve complex SQL/transactions?
│  └─ YES → Write E2E test with real database
│
├─ Are you testing permission/capability checks?
│  └─ YES → Mock at service level, test API responses
│
└─ Are you testing error handling?
   └─ Use mockRejectedValue() at service level
```

## Coverage Requirements

Coverage thresholds (enforced in CI):

- Statements: 60%
- Branches: 50%
- Functions: 60%
- Lines: 60%

View coverage report:

```bash
npm run test:coverage
pnpm --filter @orientbot/core test:coverage
```

## Debugging Failed Tests

### Common Issues

1. **Mock not resetting between tests**

   ```typescript
   afterEach(() => {
     vi.clearAllMocks();
   });
   ```

2. **Package import issues**
   - Ensure packages are built: `pnpm build`
   - Check workspace dependencies in package.json

3. **Async timing issues**

   ```typescript
   beforeEach(() => {
     vi.useFakeTimers();
   });
   afterEach(() => {
     vi.useRealTimers();
   });
   await vi.advanceTimersByTimeAsync(5000);
   ```

4. **E2E test skipped unexpectedly**
   - Ensure `DATABASE_URL` or `TEST_DATABASE_URL` is set
   - Check database directory exists: `mkdir -p .dev-data/instance-0`

## OpenCode E2E Tests

### Prerequisites

OpenCode E2E tests require the development environment running. **IMPORTANT**: Use `./run.sh dev` to start the dev environment - this configures OpenCode on the correct port with proper model settings.

```bash
# Start the dev environment (includes OpenCode on port 4099)
./run.sh dev

# In another terminal, run the OpenCode E2E tests
npx vitest run tests/e2e/opencode-session.e2e.test.ts
npx vitest run tests/e2e/session-commands.e2e.test.ts
```

### Key Configuration

| Setting       | Value                 | Notes                                     |
| ------------- | --------------------- | ----------------------------------------- |
| OpenCode Port | `4099`                | Dev environment uses port 4099 (not 4096) |
| Default Model | `openai/gpt-4o-mini`  | Uses OpenCode Zen proxy (FREE tier)       |
| Config File   | `opencode.local.json` | Contains model and MCP server settings    |

### Available Test Files

- `tests/e2e/opencode-session.e2e.test.ts` - Tests session creation, deletion, message sending, token tracking, summarization, context preservation
- `tests/e2e/session-commands.e2e.test.ts` - Tests /reset, /compact, /help commands for WhatsApp and Slack handlers

### Writing OpenCode E2E Tests

```typescript
/**
 * OpenCode E2E Test Template
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { execSync } from 'child_process';
import { createOpenCodeClient } from '../../src/services/openCodeClient.js';

// Default to port 4099 (dev environment) - see ./run.sh dev
const OPENCODE_URL = process.env.OPENCODE_URL || 'http://localhost:4099';

// Synchronous availability check at module load time
// This ensures describe.skipIf works correctly
function isOpenCodeAvailableSync(): boolean {
  try {
    const result = execSync(`curl -s --connect-timeout 2 ${OPENCODE_URL}/global/health`, {
      encoding: 'utf-8',
      timeout: 5000,
    });
    const health = JSON.parse(result);
    return health.healthy === true;
  } catch {
    return false;
  }
}

const openCodeAvailable = isOpenCodeAvailableSync();

describe('My OpenCode E2E Tests', () => {
  let client;

  beforeAll(async () => {
    if (openCodeAvailable) {
      client = createOpenCodeClient(OPENCODE_URL);
    }
  });

  // Tests are skipped if OpenCode is not running
  describe.skipIf(!openCodeAvailable)('Feature Tests', () => {
    it('should work with OpenCode', async () => {
      const session = await client.createSession('Test');
      expect(session.id).toBeDefined();
    });
  });
});
```

### Common Issues

1. **Tests skipped even though OpenCode is running**
   - Verify OpenCode is on port 4099 (dev port): `curl http://localhost:4099/global/health`
   - The standalone `opencode serve` uses port 4096 by default, but tests expect 4099

2. **Model not found errors** (ProviderModelNotFoundError)
   - Ensure using `openai/gpt-4o-mini` model format (not `grok-code` or `xai/grok-code`)
   - This routes through OpenCode Zen proxy which provides free access

3. **Malformed JSON errors on summarize**
   - The summarize endpoint requires model info in the body: `{ providerID, modelID }`

4. **Streaming response parse errors**
   - Check model configuration - some models return streaming responses
   - The `openai/gpt-4o-mini` model returns proper JSON responses

## Turborepo Caching

Test results are cached by turborepo. To force re-run:

```bash
pnpm turbo test --force
```
