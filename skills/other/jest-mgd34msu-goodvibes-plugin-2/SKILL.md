---
name: jest
description: Tests JavaScript and TypeScript applications with Jest test runner including mocking, snapshot testing, and code coverage. Use when setting up testing, writing unit tests, or when user mentions Jest, test runner, or JavaScript testing.
---

# Jest

Delightful JavaScript testing framework with zero configuration and rich mocking capabilities.

## Quick Start

```bash
# Install
npm install -D jest @types/jest

# With TypeScript
npm install -D jest ts-jest @types/jest
npx ts-jest config:init

# Or with Babel
npm install -D jest @babel/preset-env @babel/preset-typescript
```

## Configuration

### jest.config.ts

```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts', '**/*.test.ts', '**/*.spec.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/__tests__/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  clearMocks: true,
  verbose: true,
};

export default config;
```

### For React (with Testing Library)

```typescript
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', { tsconfig: 'tsconfig.jest.json' }],
  },
};

export default config;
```

### jest.setup.ts

```typescript
import '@testing-library/jest-dom';

// Global mocks
global.fetch = jest.fn();

// Extend expect
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} ${pass ? 'not ' : ''}to be within range ${floor} - ${ceiling}`,
    };
  },
});

declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
    }
  }
}
```

## Basic Tests

### Test Structure

```typescript
import { describe, it, expect, test, beforeEach, afterEach } from '@jest/globals';

describe('Calculator', () => {
  let calculator: Calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  afterEach(() => {
    // Cleanup
  });

  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(calculator.add(1, 2)).toBe(3);
    });

    it('should handle negative numbers', () => {
      expect(calculator.add(-1, -2)).toBe(-3);
    });

    test.each([
      [1, 2, 3],
      [0, 0, 0],
      [-1, 1, 0],
      [100, 200, 300],
    ])('add(%i, %i) should return %i', (a, b, expected) => {
      expect(calculator.add(a, b)).toBe(expected);
    });
  });

  describe('divide', () => {
    it('should throw when dividing by zero', () => {
      expect(() => calculator.divide(10, 0)).toThrow('Division by zero');
    });
  });
});
```

### Common Matchers

```typescript
// Equality
expect(value).toBe(expected);           // ===
expect(value).toEqual(expected);        // Deep equality
expect(value).toStrictEqual(expected);  // Deep + undefined props

// Truthiness
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeGreaterThanOrEqual(3);
expect(value).toBeLessThan(5);
expect(value).toBeCloseTo(0.3, 5);  // Floating point

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');
expect(string).toHaveLength(5);

// Arrays
expect(array).toContain(item);
expect(array).toContainEqual(object);
expect(array).toHaveLength(3);

// Objects
expect(object).toHaveProperty('key');
expect(object).toHaveProperty('nested.key', value);
expect(object).toMatchObject({ key: value });

// Exceptions
expect(() => fn()).toThrow();
expect(() => fn()).toThrow('message');
expect(() => fn()).toThrow(ErrorType);

// Negation
expect(value).not.toBe(other);

// Asymmetric matchers
expect(value).toEqual(expect.any(Number));
expect(value).toEqual(expect.stringContaining('sub'));
expect(value).toEqual(expect.arrayContaining([1, 2]));
expect(value).toEqual(expect.objectContaining({ key: value }));
```

## Async Testing

### Promises

```typescript
// Return promise
test('fetches user data', () => {
  return fetchUser(1).then((user) => {
    expect(user.name).toBe('Alice');
  });
});

// Async/await
test('fetches user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});

// Resolves/rejects
test('resolves to user', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ name: 'Alice' });
});

test('rejects with error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('User not found');
});
```

### Callbacks

```typescript
test('callback with done', (done) => {
  fetchDataWithCallback((error, data) => {
    try {
      expect(error).toBeNull();
      expect(data).toEqual({ success: true });
      done();
    } catch (e) {
      done(e);
    }
  });
});
```

### Timers

```typescript
jest.useFakeTimers();

test('delays execution', () => {
  const callback = jest.fn();

  delayedCall(callback, 1000);
  expect(callback).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);
  expect(callback).toHaveBeenCalledTimes(1);
});

test('with modern timers', () => {
  jest.useFakeTimers({ advanceTimers: true });

  const callback = jest.fn();
  setTimeout(callback, 1000);

  jest.runAllTimers();
  expect(callback).toHaveBeenCalled();
});

afterEach(() => {
  jest.useRealTimers();
});
```

## Mocking

### Function Mocks

```typescript
// Create mock function
const mockFn = jest.fn();

// With implementation
const mockAdd = jest.fn((a, b) => a + b);

// Mock return values
mockFn.mockReturnValue(42);
mockFn.mockReturnValueOnce(1).mockReturnValueOnce(2);
mockFn.mockResolvedValue({ data: 'value' });
mockFn.mockRejectedValue(new Error('Failed'));

// Assertions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('lastArg');
expect(mockFn).toHaveBeenNthCalledWith(1, 'firstCallArg');
expect(mockFn).toHaveReturnedWith(42);
```

### Module Mocks

```typescript
// __mocks__/axios.ts
const axios = {
  get: jest.fn(),
  post: jest.fn(),
  create: jest.fn(() => axios),
};
export default axios;

// In test file
jest.mock('axios');
import axios from 'axios';

const mockedAxios = axios as jest.Mocked<typeof axios>;

test('fetches data', async () => {
  mockedAxios.get.mockResolvedValue({ data: { users: [] } });

  const result = await fetchUsers();

  expect(mockedAxios.get).toHaveBeenCalledWith('/api/users');
  expect(result).toEqual({ users: [] });
});
```

### Partial Mocks

```typescript
// Mock specific exports
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  expensiveOperation: jest.fn(),
}));

// Mock with factory
jest.mock('./database', () => {
  return {
    connect: jest.fn().mockResolvedValue(true),
    query: jest.fn(),
  };
});
```

### Spy on Methods

```typescript
const video = {
  play() {
    return true;
  },
};

test('plays video', () => {
  const spy = jest.spyOn(video, 'play');
  video.play();

  expect(spy).toHaveBeenCalled();
  spy.mockRestore();
});

// Spy on prototype
jest.spyOn(Date.prototype, 'toISOString').mockReturnValue('2024-01-01');
```

### Manual Mocks

```typescript
// __mocks__/fs.ts
const fs = jest.createMockFromModule('fs') as typeof import('fs');

let mockFiles: Record<string, string> = {};

fs.readFileSync = jest.fn((path: string) => {
  if (path in mockFiles) {
    return mockFiles[path];
  }
  throw new Error(`ENOENT: ${path}`);
});

(fs as any).__setMockFiles = (files: Record<string, string>) => {
  mockFiles = files;
};

export default fs;
```

## Snapshot Testing

```typescript
// Basic snapshot
test('renders correctly', () => {
  const tree = renderer.create(<Button label="Click me" />).toJSON();
  expect(tree).toMatchSnapshot();
});

// Inline snapshot
test('formats date', () => {
  expect(formatDate(new Date('2024-01-15'))).toMatchInlineSnapshot(
    `"January 15, 2024"`
  );
});

// Property matchers for dynamic values
test('creates user', () => {
  const user = createUser('Alice');
  expect(user).toMatchSnapshot({
    id: expect.any(String),
    createdAt: expect.any(Date),
  });
});

// Update snapshots: jest --updateSnapshot
```

## Code Coverage

```bash
# Run with coverage
jest --coverage

# Coverage report options
jest --coverage --coverageReporters="text" --coverageReporters="html"
```

```typescript
// jest.config.ts coverage options
{
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    './src/utils/': {
      branches: 100,
      statements: 100,
    },
  },
}
```

## Testing React Components

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form with user data', async () => {
  const handleSubmit = jest.fn();
  const user = userEvent.setup();

  render(<LoginForm onSubmit={handleSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(handleSubmit).toHaveBeenCalledWith({
    email: 'test@example.com',
    password: 'password123',
  });
});

test('shows error on invalid input', async () => {
  render(<LoginForm />);

  fireEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
  });
});

test('fetches and displays users', async () => {
  const mockUsers = [{ id: 1, name: 'Alice' }];
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: () => Promise.resolve(mockUsers),
  });

  render(<UserList />);

  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  await waitFor(() => {
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });
});
```

## Running Tests

```bash
# Run all tests
jest

# Watch mode
jest --watch

# Run specific file
jest path/to/test.spec.ts

# Run tests matching pattern
jest --testNamePattern="should add"

# Run only changed files
jest --onlyChanged

# Parallel execution
jest --maxWorkers=4

# Debug mode
node --inspect-brk node_modules/.bin/jest --runInBand
```

## Reference Files

- [mocking-patterns.md](references/mocking-patterns.md) - Advanced mocking techniques
- [performance.md](references/performance.md) - Optimizing test performance
