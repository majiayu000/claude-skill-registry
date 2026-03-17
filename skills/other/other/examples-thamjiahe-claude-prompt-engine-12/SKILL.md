---
name: "Vitest Unit Testing"
description: "Write fast unit tests with Vitest, coverage reporting, mocking, and snapshots. Apply when testing utilities, components, services, or building test coverage."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Vitest Unit Testing

Systematic unit testing with Vitest for fast, reliable test feedback.

## Overview

This Skill enforces:
- Test-driven development (TDD) with Vitest
- Component testing with React
- Mocking and spying
- Snapshot testing
- Code coverage reporting
- Watch mode for development
- Parallel test execution

Apply when writing unit tests, testing components, or building test coverage.

## Setup Vitest

### Install Dependencies

```bash
npm install -D vitest @vitest/ui
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D jsdom  # For DOM testing
```

### Configure vitest.config.ts

```ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/*.spec.ts'
      ]
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  }
});
```

### Setup File

```ts
// vitest.setup.ts
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';

// Cleanup after each test
afterEach(() => {
  cleanup();
});
```

### Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```

## Writing Unit Tests

### Basic Test Structure

```ts
// src/utils/helpers.test.ts
import { describe, it, expect } from 'vitest';
import { add, multiply } from './helpers';

describe('Math Helpers', () => {
  describe('add', () => {
    it('should add two numbers correctly', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(add(-5, 3)).toBe(-2);
    });

    it('should handle zero', () => {
      expect(add(0, 5)).toBe(5);
    });
  });

  describe('multiply', () => {
    it('should multiply two numbers correctly', () => {
      expect(multiply(3, 4)).toBe(12);
    });

    it('should return 0 when multiplying by 0', () => {
      expect(multiply(5, 0)).toBe(0);
    });
  });
});
```

### Component Testing

```tsx
// src/components/Button.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick handler when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click</Button>);
    
    const button = screen.getByRole('button');
    await user.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('renders disabled button', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Mocking

### Mocking Functions

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('User Service', () => {
  let mockFetch: any;

  beforeEach(() => {
    mockFetch = vi.fn();
  });

  it('fetches user data', async () => {
    mockFetch.mockResolvedValue({
      json: async () => ({ id: 1, name: 'Alice' })
    });

    // Use mockFetch in your function
    const response = await mockFetch();
    const data = await response.json();

    expect(data).toEqual({ id: 1, name: 'Alice' });
    expect(mockFetch).toHaveBeenCalledTimes(1);
  });

  it('handles fetch error', async () => {
    mockFetch.mockRejectedValue(new Error('Network error'));

    await expect(mockFetch()).rejects.toThrow('Network error');
  });
});
```

### Mocking Modules

```ts
// src/services/api.test.ts
import { describe, it, expect, vi } from 'vitest';
import { fetchUsers } from './api';

// Mock the entire module
vi.mock('../lib/http', () => ({
  get: vi.fn(() => Promise.resolve([{ id: 1, name: 'Alice' }]))
}));

describe('API Service', () => {
  it('fetches users', async () => {
    const users = await fetchUsers();
    expect(users).toHaveLength(1);
    expect(users[0].name).toBe('Alice');
  });
});
```

### Partial Mocking

```ts
import { describe, it, expect, vi } from 'vitest';

vi.mock('../utils', async () => {
  const actual = await vi.importActual('../utils');
  return {
    ...actual,
    dateUtil: {
      now: () => new Date('2025-01-01')
    }
  };
});
```

## Spying

```ts
import { describe, it, expect, vi, spyOn } from 'vitest';
import { logger } from './logger';

describe('Spy on function', () => {
  it('spies on console.log', () => {
    const consoleSpy = spyOn(console, 'log');

    console.log('test message');

    expect(consoleSpy).toHaveBeenCalledWith('test message');
    expect(consoleSpy).toHaveBeenCalledTimes(1);

    consoleSpy.mockRestore();
  });
});
```

## Async Testing

```ts
import { describe, it, expect, vi } from 'vitest';

describe('Async Operations', () => {
  it('waits for promise to resolve', async () => {
    const fetchData = () =>
      new Promise(resolve => 
        setTimeout(() => resolve('data'), 100)
      );

    const data = await fetchData();
    expect(data).toBe('data');
  });

  it('handles async errors', async () => {
    const failingFetch = () =>
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Network error')), 100)
      );

    await expect(failingFetch()).rejects.toThrow('Network error');
  });
});
```

## Snapshot Testing

```tsx
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { Card } from './Card';

describe('Card Snapshot', () => {
  it('matches snapshot', () => {
    const { container } = render(
      <Card title="Test">Content</Card>
    );

    expect(container).toMatchSnapshot();
  });
});
```

## Code Coverage

### Run Coverage

```bash
npm run test:coverage
```

### Coverage Configuration

```ts
// vitest.config.ts
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      lines: 80,        // Minimum line coverage
      functions: 80,
      branches: 75,
      statements: 80,
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.test.ts'
      ]
    }
  }
});
```

## Vitest UI

```bash
npm run test:ui
# Opens interactive UI at http://localhost:51204/__vitest__/
```

## Performance Benefits

```
Framework | Time (500 tests)
----------|----------------
Jest      | ~8 seconds
Vitest    | ~3 seconds
Mocha     | ~6 seconds
```

Vitest is **~2.7x faster** than Jest!

## Anti-Patterns

```ts
// ❌ BAD: Slow synchronous operations
it('slow test', () => {
  for (let i = 0; i < 1000000; i++) {
    // Pointless loop
  }
});

// ❌ BAD: Global state pollution
let counter = 0;
it('increments counter', () => {
  counter++;
  expect(counter).toBe(1);
});
it('another test', () => {
  expect(counter).toBe(1);  // Depends on previous test!
});

// ✅ GOOD: Use beforeEach for setup
let counter: number;
beforeEach(() => {
  counter = 0;
});

// ❌ BAD: Testing implementation details
vi.spyOn(obj, 'privateMethod');

// ✅ GOOD: Test behavior, not implementation
expect(result).toBe(expectedValue);

// ❌ BAD: Snapshot without understanding
expect(largeObject).toMatchSnapshot();
// Snapshot bloat, hard to review

// ✅ GOOD: Targeted snapshots
expect({ name, email }).toMatchSnapshot();
```

## Verification Before Production

- [ ] Unit test coverage >= 80%
- [ ] No console warnings in tests
- [ ] Async tests properly handled
- [ ] Mocks cleaned up (mockRestore)
- [ ] No flaky tests (random failures)
- [ ] Tests isolated (no dependencies)
- [ ] Snapshot tests reviewed
- [ ] Coverage report passing

## Integration with Project Standards

Enforces T-1 through T-10:
- Colocated tests (same directory as source)
- Pure logic tested separately
- Edge cases covered
- Fast feedback (RED-GREEN-REFACTOR)

## Resources

- Vitest Docs: https://vitest.dev
- Testing Library: https://testing-library.com
- Vitest Examples: https://github.com/vitest-dev/vitest/tree/main/examples
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
