---
name: vitest
description: Fast Vite-native unit testing framework for JavaScript/TypeScript. ESM-first, Jest-compatible API, with instant HMR. Use for modern frontend testing, Vue/React/Svelte testing, or fast test execution. Triggers on vitest, vite test, vue test, svelte test.
---

# Vitest Testing Framework

A blazing fast unit testing framework powered by Vite.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `vitest` | Run in watch mode |
| `vitest run` | Run once and exit |
| `vitest --coverage` | Generate coverage |
| `vitest --ui` | Open UI dashboard |
| `vitest --reporter=verbose` | Verbose output |

## Why Vitest?

- **Native ESM support** - No configuration needed
- **Vite-powered** - Instant HMR for tests
- **Jest-compatible** - Familiar API, easy migration
- **TypeScript first** - Built-in TypeScript support
- **Fast** - Significantly faster than Jest

## 1. Setup

### Installation

```bash
# Basic installation
npm install -D vitest

# With testing library
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom

# With coverage
npm install -D @vitest/coverage-v8
```

### Configuration (vitest.config.ts)

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    // Test environment
    environment: 'jsdom', // or 'node', 'happy-dom'

    // Global test APIs (describe, it, expect)
    globals: true,

    // Setup files
    setupFiles: ['./src/test/setup.ts'],

    // Include patterns
    include: ['**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],

    // Coverage
    coverage: {
      provider: 'v8', // or 'istanbul'
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/test/'],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    },

    // Reporters
    reporters: ['default', 'html'],

    // Timeout
    testTimeout: 10000,

    // CSS handling
    css: true,

    // Module resolution
    alias: {
      '@': '/src',
    },
  },
});
```

### Setup File (src/test/setup.ts)

```typescript
import '@testing-library/jest-dom';
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Global mocks
vi.mock('./analytics', () => ({
  track: vi.fn(),
}));
```

## 2. Basic Tests

### Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';

describe('Calculator', () => {
  beforeEach(() => {
    // Setup
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('handles edge cases', () => {
    expect(add(0, 0)).toBe(0);
    expect(add(-1, 1)).toBe(0);
  });

  // Skip test
  it.skip('skipped test', () => {});

  // Only run this test
  it.only('only this test', () => {});

  // Todo test
  it.todo('implement this later');

  // Concurrent tests
  it.concurrent('runs in parallel', async () => {
    const result = await fetchData();
    expect(result).toBeDefined();
  });
});
```

### Matchers (Jest-compatible)

```typescript
// Equality
expect(value).toBe(expected);
expect(value).toEqual(expected);
expect(value).toStrictEqual(expected);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeCloseTo(0.3, 5);

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Objects
expect(obj).toHaveProperty('key', 'value');
expect(obj).toMatchObject({ partial: true });

// Exceptions
expect(() => throwError()).toThrow();
expect(() => throwError()).toThrow('message');
expect(() => throwError()).toThrowError(ErrorClass);

// Snapshots
expect(value).toMatchSnapshot();
expect(value).toMatchInlineSnapshot();
```

### Parameterized Tests

```typescript
import { describe, it, expect } from 'vitest';

describe('Math operations', () => {
  it.each([
    [1, 1, 2],
    [2, 2, 4],
    [3, 3, 6],
  ])('add(%i, %i) = %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });

  // With object syntax
  it.each([
    { a: 1, b: 1, expected: 2 },
    { a: 2, b: 2, expected: 4 },
  ])('add($a, $b) = $expected', ({ a, b, expected }) => {
    expect(add(a, b)).toBe(expected);
  });
});
```

## 3. Mocking

### Mock Functions

```typescript
import { vi } from 'vitest';

// Create mock function
const mockFn = vi.fn();
const mockWithReturn = vi.fn().mockReturnValue(42);
const mockAsync = vi.fn().mockResolvedValue({ data: 'test' });

// Implementations
mockFn.mockReturnValue(10);
mockFn.mockReturnValueOnce(5);
mockFn.mockResolvedValue({ data: 'async' });
mockFn.mockRejectedValue(new Error('failed'));
mockFn.mockImplementation((x) => x * 2);

// Assertions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(3);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('last');
```

### Mock Modules

```typescript
import { vi } from 'vitest';

// Mock module
vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ id: 1 }),
}));

// Mock with factory
vi.mock('./database', async () => {
  const actual = await vi.importActual('./database');
  return {
    ...actual,
    connect: vi.fn(),
  };
});

// Auto-mock all exports
vi.mock('./utils');

// Reset mocks
afterEach(() => {
  vi.resetAllMocks();
  vi.restoreAllMocks();
});
```

### Spies

```typescript
import { vi } from 'vitest';

const obj = {
  method: (x: number) => x * 2,
};

// Spy on method
const spy = vi.spyOn(obj, 'method');
obj.method(5);

expect(spy).toHaveBeenCalledWith(5);
expect(spy).toHaveReturnedWith(10);

// Spy with mock implementation
vi.spyOn(obj, 'method').mockReturnValue(100);
```

### Timer Mocks

```typescript
import { vi, beforeEach, afterEach } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

it('handles timers', () => {
  const callback = vi.fn();

  setTimeout(callback, 1000);
  expect(callback).not.toHaveBeenCalled();

  vi.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledTimes(1);
});

it('runs all timers', () => {
  const callback = vi.fn();

  setTimeout(callback, 1000);
  setTimeout(callback, 2000);

  vi.runAllTimers();
  expect(callback).toHaveBeenCalledTimes(2);
});
```

## 4. Async Testing

```typescript
// Async/await
it('fetches data', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});

// Promises
it('resolves with data', () => {
  return expect(fetchData()).resolves.toEqual({ id: 1 });
});

it('rejects with error', () => {
  return expect(failingFetch()).rejects.toThrow('Network error');
});

// With assertions count
it('makes multiple assertions', async () => {
  expect.assertions(2);

  const data = await fetchData();
  expect(data.id).toBe(1);
  expect(data.name).toBe('John');
});
```

## 5. React Testing

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('handles click', async () => {
    const onClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={onClick}>Click</Button>);
    await user.click(screen.getByRole('button'));

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('shows loading state', () => {
    render(<Button loading>Submit</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveTextContent('Loading...');
  });
});

describe('Form', () => {
  it('submits with valid data', async () => {
    const onSubmit = vi.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });
});
```

## 6. Vue Testing

```typescript
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.vue';

describe('Counter', () => {
  it('increments count', async () => {
    const wrapper = mount(Counter);

    expect(wrapper.text()).toContain('0');

    await wrapper.find('button').trigger('click');

    expect(wrapper.text()).toContain('1');
  });

  it('accepts initial value', () => {
    const wrapper = mount(Counter, {
      props: { initialCount: 10 },
    });

    expect(wrapper.text()).toContain('10');
  });
});
```

## 7. Snapshot Testing

```typescript
import { expect, it } from 'vitest';
import { render } from '@testing-library/react';

it('matches snapshot', () => {
  const { container } = render(<Button>Click</Button>);
  expect(container).toMatchSnapshot();
});

it('matches inline snapshot', () => {
  const user = getUser(1);
  expect(user).toMatchInlineSnapshot(`
    {
      "id": 1,
      "name": "John",
    }
  `);
});

// Update snapshots: vitest -u
```

## 8. Coverage

```bash
# Run with coverage
vitest run --coverage

# With specific reporter
vitest run --coverage --coverage.reporter=lcov
```

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      reportsDirectory: './coverage',
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    },
  },
});
```

## 9. CI/CD Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx vitest run --coverage
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

## 10. Migration from Jest

### Config Changes

```typescript
// jest.config.js -> vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true, // Use global describe/it/expect
    environment: 'jsdom',
    setupFiles: ['./jest.setup.ts'], // Reuse setup
  },
});
```

### API Differences

```typescript
// Jest -> Vitest
jest.fn() -> vi.fn()
jest.mock() -> vi.mock()
jest.spyOn() -> vi.spyOn()
jest.useFakeTimers() -> vi.useFakeTimers()
jest.clearAllMocks() -> vi.clearAllMocks()

// Import vi in files (or set globals: true)
import { vi } from 'vitest';
```

## Best Practices

1. **Use globals: true** - Cleaner test files
2. **Leverage HMR** - Keep vitest running in watch mode
3. **Parallel by default** - Tests run concurrently
4. **Use happy-dom** - Faster than jsdom for most cases
5. **Inline snapshots** - Better for small outputs
6. **Type-safe mocks** - Leverage TypeScript
7. **Fast setup** - Keep setup files minimal
8. **Coverage thresholds** - Enforce quality
9. **Browser mode** - For accurate DOM testing
10. **UI mode** - vitest --ui for visual debugging
