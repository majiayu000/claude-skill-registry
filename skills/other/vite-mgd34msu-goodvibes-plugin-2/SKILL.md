---
name: vitest
description: Tests JavaScript and TypeScript applications with Vitest including unit tests, mocking, coverage, and React component testing. Use when writing tests, setting up test infrastructure, mocking dependencies, or measuring code coverage.
---

# Vitest

Blazing fast unit test framework powered by Vite with native TypeScript and ESM support.

## Quick Start

**Install:**
```bash
npm install -D vitest
```

**Add to package.json:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest --coverage"
  }
}
```

**Configure vitest.config.ts:**
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    include: ['**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
    },
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

## Basic Testing

### Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  afterEach(() => {
    // Cleanup
  });

  it('should add two numbers', () => {
    expect(calculator.add(2, 3)).toBe(5);
  });

  it('should subtract two numbers', () => {
    expect(calculator.subtract(5, 3)).toBe(2);
  });

  describe('division', () => {
    it('should divide two numbers', () => {
      expect(calculator.divide(6, 2)).toBe(3);
    });

    it('should throw on division by zero', () => {
      expect(() => calculator.divide(6, 0)).toThrow('Division by zero');
    });
  });
});
```

### Common Assertions

```typescript
import { expect } from 'vitest';

// Equality
expect(value).toBe(5);                    // Strict equality
expect(value).toEqual({ a: 1 });          // Deep equality
expect(value).toStrictEqual({ a: 1 });    // Strict deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3, 5);        // Floating point

// Strings
expect(value).toMatch(/pattern/);
expect(value).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toEqual(expect.arrayContaining([1, 2]));

// Objects
expect(object).toHaveProperty('key');
expect(object).toHaveProperty('key', 'value');
expect(object).toMatchObject({ partial: true });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('error message');
expect(() => fn()).toThrowError(/pattern/);

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow('error');

// Negation
expect(value).not.toBe(5);
```

### Async Testing

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('async operations', () => {
  // Async/await
  it('should fetch data', async () => {
    const data = await fetchData();
    expect(data).toEqual({ id: 1 });
  });

  // Returning promise
  it('should resolve correctly', () => {
    return expect(fetchData()).resolves.toEqual({ id: 1 });
  });

  // Using done callback
  it('should call callback', (done) => {
    fetchWithCallback((data) => {
      expect(data).toBeDefined();
      done();
    });
  });

  // Testing rejected promises
  it('should reject on error', async () => {
    await expect(fetchInvalidData()).rejects.toThrow('Not found');
  });
});
```

## Mocking

### Function Mocks

```typescript
import { vi, describe, it, expect, beforeEach } from 'vitest';

describe('mocking functions', () => {
  const mockFn = vi.fn();

  beforeEach(() => {
    mockFn.mockClear(); // Clear calls, keep implementation
    // mockFn.mockReset(); // Clear everything
    // mockFn.mockRestore(); // Restore original (for spies)
  });

  it('should track calls', () => {
    mockFn('arg1', 'arg2');

    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledTimes(1);
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
  });

  it('should return mocked values', () => {
    mockFn.mockReturnValue(42);
    expect(mockFn()).toBe(42);

    mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2);
    expect(mockFn()).toBe(1);
    expect(mockFn()).toBe(2);
  });

  it('should mock implementation', () => {
    mockFn.mockImplementation((x) => x * 2);
    expect(mockFn(5)).toBe(10);
  });

  it('should mock resolved values', async () => {
    mockFn.mockResolvedValue({ data: 'test' });
    await expect(mockFn()).resolves.toEqual({ data: 'test' });
  });
});
```

### Module Mocks

```typescript
import { vi, describe, it, expect } from 'vitest';

// Mock entire module
vi.mock('./database', () => ({
  getUser: vi.fn().mockResolvedValue({ id: 1, name: 'Test' }),
  saveUser: vi.fn().mockResolvedValue(true),
}));

// Mock with factory
vi.mock('./api', () => {
  return {
    fetchPosts: vi.fn(() => Promise.resolve([])),
  };
});

// Partial mock
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    formatDate: vi.fn(() => '2024-01-01'),
  };
});

import { getUser } from './database';
import { fetchPosts } from './api';

describe('module mocking', () => {
  it('should use mocked module', async () => {
    const user = await getUser(1);
    expect(user).toEqual({ id: 1, name: 'Test' });
  });
});
```

### Spies

```typescript
import { vi, describe, it, expect } from 'vitest';

describe('spying', () => {
  it('should spy on object method', () => {
    const obj = {
      method: (x: number) => x * 2,
    };

    const spy = vi.spyOn(obj, 'method');

    obj.method(5);

    expect(spy).toHaveBeenCalledWith(5);
    expect(spy).toHaveReturnedWith(10);

    spy.mockRestore();
  });

  it('should spy and mock', () => {
    const spy = vi.spyOn(console, 'log').mockImplementation(() => {});

    console.log('test');

    expect(spy).toHaveBeenCalledWith('test');

    spy.mockRestore();
  });
});
```

### Timers

```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('timer mocking', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should advance timers', () => {
    const callback = vi.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
  });

  it('should run all timers', () => {
    const callback = vi.fn();

    setTimeout(callback, 100);
    setTimeout(callback, 200);

    vi.runAllTimers();

    expect(callback).toHaveBeenCalledTimes(2);
  });

  it('should mock Date', () => {
    vi.setSystemTime(new Date(2024, 0, 1));

    expect(new Date().getFullYear()).toBe(2024);
  });
});
```

## React Testing

### Setup

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

### Component Testing

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Counter } from './Counter';

describe('Counter', () => {
  it('should render initial count', () => {
    render(<Counter initialCount={5} />);

    expect(screen.getByText('Count: 5')).toBeInTheDocument();
  });

  it('should increment on click', async () => {
    const user = userEvent.setup();
    render(<Counter initialCount={0} />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('should call onChange when count changes', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();

    render(<Counter initialCount={0} onChange={onChange} />);

    await user.click(screen.getByRole('button', { name: /increment/i }));

    expect(onChange).toHaveBeenCalledWith(1);
  });
});
```

### Testing Hooks

```tsx
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('should initialize with provided value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should update when props change', () => {
    const { result, rerender } = renderHook(
      ({ initial }) => useCounter(initial),
      { initialProps: { initial: 0 } }
    );

    expect(result.current.count).toBe(0);

    rerender({ initial: 10 });
    // Note: depends on hook implementation
  });
});
```

### Testing with Context

```tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ThemeProvider } from './ThemeContext';
import { ThemedButton } from './ThemedButton';

const renderWithTheme = (ui: React.ReactElement, theme = 'light') => {
  return render(
    <ThemeProvider initialTheme={theme}>{ui}</ThemeProvider>
  );
};

describe('ThemedButton', () => {
  it('should apply light theme styles', () => {
    renderWithTheme(<ThemedButton>Click</ThemedButton>, 'light');

    expect(screen.getByRole('button')).toHaveClass('theme-light');
  });

  it('should apply dark theme styles', () => {
    renderWithTheme(<ThemedButton>Click</ThemedButton>, 'dark');

    expect(screen.getByRole('button')).toHaveClass('theme-dark');
  });
});
```

### Testing Async Components

```tsx
import { render, screen, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { UserProfile } from './UserProfile';

vi.mock('./api', () => ({
  fetchUser: vi.fn().mockResolvedValue({ name: 'John Doe' }),
}));

describe('UserProfile', () => {
  it('should show loading state', () => {
    render(<UserProfile userId="1" />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display user after loading', async () => {
    render(<UserProfile userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });

  it('should show error state', async () => {
    const { fetchUser } = await import('./api');
    vi.mocked(fetchUser).mockRejectedValueOnce(new Error('Failed'));

    render(<UserProfile userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('Error loading user')).toBeInTheDocument();
    });
  });
});
```

## Snapshot Testing

```typescript
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { Card } from './Card';

describe('Card', () => {
  it('should match snapshot', () => {
    const { container } = render(
      <Card title="Test" description="Description" />
    );

    expect(container).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const { container } = render(<Card title="Test" />);

    expect(container.innerHTML).toMatchInlineSnapshot(`
      "<div class=\\"card\\"><h2>Test</h2></div>"
    `);
  });
});
```

## Coverage

**Install coverage provider:**
```bash
npm install -D @vitest/coverage-v8
```

**Configure:**
```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
});
```

**Run:**
```bash
npm run test:coverage
```

## Test Patterns

### Test Utils

```typescript
// test/utils.tsx
import { render } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export function renderWithProviders(
  ui: React.ReactElement,
  options = {}
) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
    options
  );
}

export * from '@testing-library/react';
```

### Data Builders

```typescript
// test/factories.ts
interface User {
  id: string;
  name: string;
  email: string;
}

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: '1',
    name: 'Test User',
    email: 'test@example.com',
    ...overrides,
  };
}

// Usage
const user = createUser({ name: 'Custom Name' });
```

## Best Practices

1. **One assertion focus** - Each test verifies one behavior
2. **Descriptive names** - Clear test descriptions
3. **Arrange-Act-Assert** - Consistent test structure
4. **Avoid test interdependence** - Tests run in isolation
5. **Mock external dependencies** - Control test environment

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Testing implementation | Test behavior and outcomes |
| Over-mocking | Only mock external dependencies |
| Brittle selectors | Use accessible queries |
| Missing cleanup | Use afterEach cleanup |
| Ignoring async | Always await async operations |

## Reference Files

- [references/patterns.md](references/patterns.md) - Advanced test patterns
- [references/mocking.md](references/mocking.md) - Mocking strategies
- [references/react.md](references/react.md) - React testing patterns
