---
name: generate-tests
description: Generate comprehensive test files for new or existing code. Creates test suites with proper mocking, edge cases, and error handling.
---

# Generate Tests Skill

Generate Vitest test files for new or existing code. Creates comprehensive test suites following project conventions and best practices.

## When to Use

- After implementing new features
- After creating new API routes
- After creating new utility functions
- When refactoring existing code
- When requested with `/generate-tests`

## Instructions

### Phase 1: Analyze Target Code

**Goal**: Understand what needs to be tested

1. **Identify the target**:
   ```bash
   # Check recent changes
   git diff --name-only HEAD~5

   # Or if specific file provided
   # Read the file contents
   ```

2. **Categorize the code type**:
   - **API Routes** (`app/api/**/*.ts`) → Integration tests with MSW
   - **Utility Functions** (`lib/**/*.ts`, `src/utils/**/*.ts`) → Unit tests
   - **React Components** (`src/components/**/*.tsx`) → Component tests with React Testing Library
   - **Hooks** (`hooks/**/*.ts`) → Hook tests with renderHook
   - **Context Providers** (`src/context/**/*.tsx`) → Context tests

3. **Identify test requirements**:
   - Input/output contracts
   - Edge cases
   - Error handling
   - Dependencies to mock

---

### Phase 2: Generate Test File

**Goal**: Create comprehensive test suite following project patterns

#### Test File Location
```
src/component.tsx      → tests/components/component.test.tsx
app/api/route.ts       → tests/api/route-name.test.ts
lib/utility.ts         → tests/lib/utility.test.ts
hooks/useHook.ts       → tests/hooks/useHook.test.ts
```

#### Test File Template

```typescript
/**
 * [Component/Function Name] Tests
 *
 * Tests for [brief description]
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

// Import the code under test
import { functionUnderTest } from '@/path/to/code';

// Import test utilities
import { createMockUser, createMockProject } from '@/tests/setup';

describe('[Component/Function Name]', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  describe('[function/feature name]', () => {
    it('should [expected behavior] when [condition]', () => {
      // Arrange
      const input = /* setup */;

      // Act
      const result = functionUnderTest(input);

      // Assert
      expect(result).toBe(/* expected */);
    });

    it('should handle [edge case]', () => {
      // Test edge case
    });

    it('should throw when [error condition]', () => {
      expect(() => functionUnderTest(invalidInput)).toThrow();
    });
  });
});
```

---

### Phase 3: Test Patterns by Code Type

#### API Route Tests

```typescript
import { describe, it, expect } from 'vitest';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const API_BASE = 'http://localhost:3001';

// Mock handlers
const handlers = [
  http.get(`${API_BASE}/api/resource`, () => {
    return HttpResponse.json({ items: [] });
  }),

  http.post(`${API_BASE}/api/resource`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ item: { id: '1', ...body } }, { status: 201 });
  }),
];

const server = setupServer(...handlers);

describe('Resource API', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  describe('GET /api/resource', () => {
    it('should return list of resources', async () => {
      const response = await fetch(`${API_BASE}/api/resource`);
      const data = await response.json();

      expect(response.ok).toBe(true);
      expect(data.items).toEqual([]);
    });
  });

  describe('POST /api/resource', () => {
    it('should create a new resource', async () => {
      const response = await fetch(`${API_BASE}/api/resource`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Test' }),
      });

      expect(response.status).toBe(201);
      const data = await response.json();
      expect(data.item.name).toBe('Test');
    });
  });

  describe('Error handling', () => {
    it('should handle server errors', async () => {
      server.use(
        http.get(`${API_BASE}/api/resource`, () => {
          return HttpResponse.json({ error: 'Server error' }, { status: 500 });
        })
      );

      const response = await fetch(`${API_BASE}/api/resource`);
      expect(response.status).toBe(500);
    });
  });
});
```

#### Utility Function Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { utilityFunction } from '@/lib/utility';

describe('utilityFunction', () => {
  it('should return expected output for valid input', () => {
    expect(utilityFunction('input')).toBe('expected');
  });

  it('should handle empty input', () => {
    expect(utilityFunction('')).toBe('');
  });

  it('should handle null/undefined', () => {
    expect(utilityFunction(null)).toBeNull();
    expect(utilityFunction(undefined)).toBeUndefined();
  });

  it('should throw for invalid input', () => {
    expect(() => utilityFunction(-1)).toThrow('Invalid input');
  });
});
```

#### React Component Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Component } from '@/src/components/Component';

// Mock dependencies
vi.mock('@/hooks/useApi', () => ({
  api: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('Component', () => {
  it('should render correctly', () => {
    render(<Component />);
    expect(screen.getByRole('heading')).toBeInTheDocument();
  });

  it('should handle user interaction', async () => {
    const onSubmit = vi.fn();
    render(<Component onSubmit={onSubmit} />);

    fireEvent.click(screen.getByRole('button'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalled();
    });
  });

  it('should display loading state', () => {
    render(<Component isLoading />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display error state', () => {
    render(<Component error="Something went wrong" />);
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });
});
```

#### Hook Tests

```typescript
import { describe, it, expect, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useCustomHook } from '@/hooks/useCustomHook';

describe('useCustomHook', () => {
  it('should return initial state', () => {
    const { result } = renderHook(() => useCustomHook());

    expect(result.current.data).toBeNull();
    expect(result.current.isLoading).toBe(false);
  });

  it('should update state on action', async () => {
    const { result } = renderHook(() => useCustomHook());

    act(() => {
      result.current.doSomething();
    });

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });
  });
});
```

---

### Phase 4: Test Coverage Checklist

For each piece of code, ensure tests cover:

#### Functions
- [ ] Happy path (valid inputs)
- [ ] Edge cases (empty, null, undefined)
- [ ] Invalid inputs (wrong types, out of range)
- [ ] Error conditions (throws, rejects)
- [ ] Boundary values (min, max, zero)

#### API Routes
- [ ] Success responses (200, 201)
- [ ] Client errors (400, 401, 403, 404)
- [ ] Server errors (500)
- [ ] Input validation (missing fields, invalid types)
- [ ] Authentication (with/without auth)
- [ ] Authorization (wrong user, wrong role)

#### Components
- [ ] Initial render
- [ ] Loading state
- [ ] Error state
- [ ] Empty state
- [ ] User interactions (click, type, submit)
- [ ] Conditional rendering
- [ ] Props variations

#### Hooks
- [ ] Initial values
- [ ] State updates
- [ ] Side effects
- [ ] Cleanup
- [ ] Error handling

---

### Phase 5: Add Mock Handlers (if needed)

If tests need new API mocks, add to `tests/mocks/handlers.ts`:

```typescript
// Add to handlers array
http.get(`${API_BASE}/api/new-endpoint`, () => {
  return HttpResponse.json({ /* response */ });
}),

http.post(`${API_BASE}/api/new-endpoint`, async ({ request }) => {
  const body = await request.json();
  return HttpResponse.json({ /* response */ }, { status: 201 });
}),
```

---

### Phase 6: Run and Verify Tests

```bash
# Run all tests
npm test

# Run specific test file
npm test tests/api/my-feature.test.ts

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage
```

**Expected output**:
- All tests pass ✓
- Coverage meets minimum thresholds
- No console errors or warnings

---

## Quick Reference

| Code Type | Test Location | Key Imports |
|-----------|---------------|-------------|
| API Route | `tests/api/` | `http`, `HttpResponse`, `setupServer` from msw |
| Utility | `tests/lib/` | `vi` from vitest |
| Component | `tests/components/` | `render`, `screen`, `fireEvent` from RTL |
| Hook | `tests/hooks/` | `renderHook`, `act` from RTL |
| Context | `tests/context/` | Wrapper component pattern |

## Mock Patterns

```typescript
// Mock module
vi.mock('@/lib/module', () => ({
  functionName: vi.fn(),
}));

// Mock implementation
vi.mocked(functionName).mockReturnValue('value');
vi.mocked(functionName).mockResolvedValue('async value');
vi.mocked(functionName).mockRejectedValue(new Error('error'));

// Mock environment variable
process.env.VAR_NAME = 'value';

// Mock fetch
global.fetch = vi.fn().mockResolvedValue({
  ok: true,
  json: async () => ({ data: 'value' }),
});
```

---

## Example Flow

```
User: /generate-tests for the database backup feature

Claude: I'll generate tests for the database backup functionality.

[Phase 1: Analyze target code]
Found code at lib/database-backup.ts with:
- 3 exported functions: createBackup, listBackups, cleanupAutoBackups
- 1 interface: BackupMetadata
- Dependencies: fs, pg, neon

[Phase 2: Generate test structure]
Creating: tests/lib/database-backup.test.ts

[Phase 3: Apply patterns]
- Unit tests for each function
- Mocking fs, pg, and neon modules
- Testing success and error cases

[Phase 4: Coverage checklist]
✓ createBackup: local source, neon source, auto-backup flag, missing config
✓ listBackups: empty, sorted results, missing metadata
✓ cleanupAutoBackups: below threshold, above threshold, manual backups ignored

[Phase 5: No new mock handlers needed]

[Phase 6: Run tests]
$ npm test tests/lib/database-backup.test.ts

✓ database-backup (12 tests)

All tests pass!
```

---

## Notes

- Always follow AAA pattern (Arrange, Act, Assert)
- Keep tests focused - one assertion per test when possible
- Use descriptive test names that explain the expected behavior
- Mock external dependencies (database, file system, network)
- Test both success and failure paths
- Don't test implementation details, test behavior
- Use factory functions from `tests/setup.ts` for mock data
