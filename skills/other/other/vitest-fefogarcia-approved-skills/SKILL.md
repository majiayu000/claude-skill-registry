---
name: vitest
description: |
  Build fast unit and integration tests with Vitest 4.x. Covers configuration for Workers/React/Node, vi.mock/vi.spyOn patterns, snapshot testing, in-source testing, workspace configuration, and browser mode.

  Use when: setting up tests, migrating from Jest, mocking modules, testing React components, or configuring monorepo workspaces. Keywords: vitest, test, unit test, vi.mock, vi.spyOn, snapshot, coverage, Jest migration.
license: MIT
---

# Vitest - Modern Test Framework

**Status**: Production Ready
**Last Updated**: 2026-02-06
**Vitest Version**: 4.x
**Vite Compatibility**: 6.x

---

## Quick Start

```bash
# Install
pnpm add -D vitest

# Add to package.json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage"
  }
}
```

---

## Configuration

### Minimal Config (vitest.config.ts)

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
});
```

### React Config

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    css: true,
  },
});
```

### Cloudflare Workers Config

```typescript
import { defineConfig } from 'vitest/config';
import { cloudflare } from '@cloudflare/vite-plugin';

export default defineConfig({
  plugins: [cloudflare()],
  test: {
    globals: true,
    environment: 'node',
    // Workers tests often need longer timeouts for D1/KV
    testTimeout: 10000,
  },
});
```

---

## Mocking Patterns

### vi.mock - Module Mocking

```typescript
import { vi, describe, it, expect } from 'vitest';
import { fetchUser } from './api';

// Mock entire module
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
}));

describe('User component', () => {
  it('fetches user data', async () => {
    // Type-safe mock implementation
    vi.mocked(fetchUser).mockResolvedValue({ id: 1, name: 'Test' });

    // ... test code

    expect(fetchUser).toHaveBeenCalledWith(1);
  });
});
```

### vi.spyOn - Spy on Methods

```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Date handling', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-01-01'));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('uses mocked date', () => {
    expect(new Date().getFullYear()).toBe(2026);
  });
});
```

### vi.stubGlobal - Global Mocks

```typescript
import { vi, describe, it, expect } from 'vitest';

describe('Environment', () => {
  it('mocks fetch globally', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: 'test' }),
    });

    vi.stubGlobal('fetch', mockFetch);

    const response = await fetch('/api/test');
    expect(mockFetch).toHaveBeenCalledWith('/api/test');

    vi.unstubAllGlobals();
  });
});
```

---

## Snapshot Testing

### Basic Snapshots

```typescript
import { describe, it, expect } from 'vitest';

describe('Component output', () => {
  it('matches snapshot', () => {
    const result = renderComponent({ title: 'Hello' });
    expect(result).toMatchSnapshot();
  });

  it('matches inline snapshot', () => {
    const result = { name: 'test', count: 42 };
    expect(result).toMatchInlineSnapshot(`
      {
        "count": 42,
        "name": "test",
      }
    `);
  });
});
```

### Update Snapshots

```bash
# Update all snapshots
vitest run --update

# Interactive update
vitest --ui
```

---

## In-Source Testing

Test code directly in source files (tree-shaken in production):

```typescript
// src/utils/math.ts
export function add(a: number, b: number): number {
  return a + b;
}

// In-source test block
if (import.meta.vitest) {
  const { describe, it, expect } = import.meta.vitest;

  describe('add', () => {
    it('adds two numbers', () => {
      expect(add(1, 2)).toBe(3);
    });
  });
}
```

**Config for in-source testing:**

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    includeSource: ['src/**/*.{js,ts}'],
  },
  define: {
    'import.meta.vitest': 'undefined', // Tree-shake in production
  },
});
```

---

## Workspace Configuration (Monorepos)

```typescript
// vitest.workspace.ts
import { defineWorkspace } from 'vitest/config';

export default defineWorkspace([
  // Each package can have its own config
  'packages/*/vitest.config.ts',

  // Or define inline
  {
    test: {
      name: 'unit',
      include: ['src/**/*.test.ts'],
      environment: 'node',
    },
  },
  {
    test: {
      name: 'browser',
      include: ['src/**/*.browser.test.ts'],
      browser: {
        enabled: true,
        provider: 'playwright',
        name: 'chromium',
      },
    },
  },
]);
```

---

## Browser Mode Testing

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: 'playwright', // or 'webdriverio'
      name: 'chromium',
      headless: true,
    },
  },
});
```

```bash
# Install browser provider
pnpm add -D @vitest/browser playwright
```

---

## Coverage

```bash
# Install coverage provider
pnpm add -D @vitest/coverage-v8

# Run with coverage
vitest run --coverage
```

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
      ],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80,
      },
    },
  },
});
```

---

## Jest Migration

### Key Differences

| Jest | Vitest |
|------|--------|
| `jest.fn()` | `vi.fn()` |
| `jest.mock()` | `vi.mock()` |
| `jest.spyOn()` | `vi.spyOn()` |
| `jest.useFakeTimers()` | `vi.useFakeTimers()` |
| `jest.clearAllMocks()` | `vi.clearAllMocks()` |
| `@jest/globals` | `vitest` |

### Migration Steps

1. **Replace imports:**
```typescript
// Before (Jest)
import { jest } from '@jest/globals';

// After (Vitest)
import { vi } from 'vitest';
```

2. **Update config:**
```typescript
// jest.config.js → vitest.config.ts
export default defineConfig({
  test: {
    globals: true, // Enables describe/it/expect without imports
    environment: 'jsdom',
  },
});
```

3. **Replace jest. with vi.:**
```bash
# Quick replace (review changes carefully)
find src -name "*.test.ts" -exec sed -i 's/jest\./vi./g' {} \;
```

---

## Common Patterns

### Testing Async Code

```typescript
import { describe, it, expect } from 'vitest';

describe('async operations', () => {
  it('resolves promise', async () => {
    const result = await fetchData();
    expect(result).toBeDefined();
  });

  it('rejects with error', async () => {
    await expect(failingOperation()).rejects.toThrow('Expected error');
  });
});
```

### Testing with Fixtures

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('with fixtures', () => {
  let testData: TestData;

  beforeEach(() => {
    testData = createTestFixture();
  });

  it('uses fixture', () => {
    expect(testData.id).toBeDefined();
  });
});
```

### Parameterized Tests

```typescript
import { describe, it, expect } from 'vitest';

describe.each([
  { input: 1, expected: 2 },
  { input: 2, expected: 4 },
  { input: 3, expected: 6 },
])('double($input)', ({ input, expected }) => {
  it(`returns ${expected}`, () => {
    expect(double(input)).toBe(expected);
  });
});
```

---

## Debugging

### Run Single Test

```bash
vitest run -t "test name"
vitest run src/specific.test.ts
```

### Debug Mode

```bash
# With Node inspector
node --inspect-brk ./node_modules/vitest/vitest.mjs run

# Or use Vitest UI
vitest --ui
```

### Watch Mode

```bash
vitest          # Watch mode (default)
vitest run      # Single run
vitest watch    # Explicit watch
```

---

## Troubleshooting

### "Cannot find module" in mocks

```typescript
// Ensure mock path matches import path exactly
vi.mock('./api'); // Matches: import { x } from './api'
vi.mock('../api'); // Different! Won't work for './api' imports
```

### ESM/CJS Issues

```typescript
// vitest.config.ts - for CJS dependencies
export default defineConfig({
  test: {
    deps: {
      inline: ['problematic-cjs-package'],
    },
  },
});
```

### Globals Not Defined

```typescript
// If using globals: true but TypeScript complains
// Add to tsconfig.json:
{
  "compilerOptions": {
    "types": ["vitest/globals"]
  }
}
```

---

## See Also

- `testing-patterns` skill - General testing patterns
- `testing-library` skill - React Testing Library integration
- Official docs: https://vitest.dev
