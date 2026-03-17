---
name: jest
description: Write JavaScript/TypeScript tests with Jest including unit tests, mocking, snapshots, and coverage. Test React components, async code, and Node.js. Use for JavaScript testing, React testing, or test automation.
---

# Jest Testing Framework

## Quick Reference

| Command | Purpose |
|---------|---------|
| `jest` | Run all tests |
| `jest --watch` | Watch mode |
| `jest --coverage` | Generate coverage |
| `jest path/to/test` | Run specific test |
| `jest -t "pattern"` | Run matching tests |

## 1. Setup

### Installation

```bash
# JavaScript
npm install --save-dev jest

# TypeScript
npm install --save-dev jest ts-jest @types/jest
npx ts-jest config:init

# React
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

### Configuration (jest.config.js)

```javascript
module.exports = {
  // Test environment
  testEnvironment: 'node', // or 'jsdom' for browser

  // TypeScript
  preset: 'ts-jest',

  // Test file patterns
  testMatch: ['**/__tests__/**/*.test.[jt]s?(x)'],

  // Coverage
  collectCoverageFrom: ['src/**/*.{js,ts,tsx}', '!src/**/*.d.ts'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },

  // Module resolution
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss)$': 'identity-obj-proxy'
  },

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // Transform
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest'
  }
};
```

### Setup File (jest.setup.js)

```javascript
import '@testing-library/jest-dom';

// Global mocks
global.fetch = jest.fn();

// Cleanup after each test
afterEach(() => {
  jest.clearAllMocks();
});
```

## 2. Basic Tests

### Test Structure

```javascript
describe('Calculator', () => {
  // Setup before all tests
  beforeAll(() => {
    console.log('Starting Calculator tests');
  });

  // Setup before each test
  beforeEach(() => {
    // Reset state
  });

  // Cleanup after each test
  afterEach(() => {
    jest.clearAllMocks();
  });

  // Cleanup after all tests
  afterAll(() => {
    console.log('Finished Calculator tests');
  });

  describe('add', () => {
    it('adds two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('adds negative numbers', () => {
      expect(add(-1, -2)).toBe(-3);
    });

    it.each([
      [1, 2, 3],
      [0, 0, 0],
      [-1, 1, 0]
    ])('adds %i + %i to equal %i', (a, b, expected) => {
      expect(add(a, b)).toBe(expected);
    });
  });

  // Skip test
  it.skip('skipped test', () => {
    // This test is skipped
  });

  // Only run this test
  it.only('only this test runs', () => {
    // Only this test runs in this file
  });
});
```

### Matchers

```javascript
// Equality
expect(value).toBe(expected);           // Strict equality
expect(value).toEqual(expected);        // Deep equality
expect(value).toStrictEqual(expected);  // Strict deep equality

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
expect(value).toBeCloseTo(0.3, 5);      // Floating point

// Strings
expect(string).toMatch(/regex/);
expect(string).toContain('substring');

// Arrays
expect(array).toContain(item);
expect(array).toHaveLength(3);
expect(array).toContainEqual({ id: 1 }); // Deep equality

// Objects
expect(obj).toHaveProperty('key');
expect(obj).toHaveProperty('key', 'value');
expect(obj).toMatchObject({ subset: true });

// Exceptions
expect(() => throwError()).toThrow();
expect(() => throwError()).toThrow('error message');
expect(() => throwError()).toThrow(ErrorClass);

// Negation
expect(value).not.toBe(expected);
```

## 3. Mocking

### Mock Functions

```javascript
// Create mock function
const mockFn = jest.fn();
const mockFnWithReturn = jest.fn().mockReturnValue(42);
const mockFnWithImpl = jest.fn((x) => x * 2);

// Mock implementations
mockFn.mockReturnValue(10);
mockFn.mockReturnValueOnce(5);
mockFn.mockResolvedValue({ data: 'async' });
mockFn.mockRejectedValue(new Error('failed'));
mockFn.mockImplementation((x) => x * 2);

// Assertions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(3);
expect(mockFn).toHaveBeenCalledWith(arg1, arg2);
expect(mockFn).toHaveBeenLastCalledWith(arg);
expect(mockFn).toHaveBeenNthCalledWith(2, arg);
expect(mockFn).toHaveReturnedWith(value);
```

### Mock Modules

```javascript
// Mock entire module
jest.mock('./database');

// With implementation
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'John' }),
  updateUser: jest.fn().mockResolvedValue({ success: true })
}));

// Partial mock
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  formatDate: jest.fn().mockReturnValue('2024-01-01')
}));

// Manual mock (__mocks__/module.js)
// Automatically used when jest.mock('./module') is called
```

### Mock Classes

```javascript
jest.mock('./UserService');

const UserService = require('./UserService');

// Mock instance methods
UserService.prototype.getUser = jest.fn().mockResolvedValue({ id: 1 });

// Or mock the constructor
UserService.mockImplementation(() => ({
  getUser: jest.fn().mockResolvedValue({ id: 1 }),
  createUser: jest.fn().mockResolvedValue({ id: 2 })
}));
```

### Spy on Methods

```javascript
const obj = {
  method: () => 'original'
};

// Spy without changing behavior
const spy = jest.spyOn(obj, 'method');
obj.method();
expect(spy).toHaveBeenCalled();

// Spy with mock implementation
jest.spyOn(obj, 'method').mockReturnValue('mocked');
expect(obj.method()).toBe('mocked');

// Restore original
spy.mockRestore();
```

### Mock Timers

```javascript
beforeEach(() => {
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

it('calls callback after delay', () => {
  const callback = jest.fn();

  setTimeout(callback, 1000);

  expect(callback).not.toHaveBeenCalled();

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});

it('runs all timers', () => {
  const callback = jest.fn();

  setTimeout(callback, 1000);
  setTimeout(callback, 2000);

  jest.runAllTimers();

  expect(callback).toHaveBeenCalledTimes(2);
});
```

## 4. Async Testing

```javascript
// Promises
it('resolves with data', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});

// Or with resolves/rejects
it('resolves with data', () => {
  return expect(fetchData()).resolves.toEqual({ id: 1 });
});

it('rejects with error', () => {
  return expect(failingFetch()).rejects.toThrow('Network error');
});

// Callbacks
it('calls callback with data', (done) => {
  fetchDataCallback((error, data) => {
    try {
      expect(error).toBeNull();
      expect(data).toEqual({ id: 1 });
      done();
    } catch (e) {
      done(e);
    }
  });
});

// Async with expect.assertions
it('handles multiple assertions', async () => {
  expect.assertions(2);

  const data = await fetchData();
  expect(data.id).toBe(1);
  expect(data.name).toBe('John');
});
```

## 5. Snapshot Testing

```javascript
// Basic snapshot
it('renders correctly', () => {
  const tree = renderer.create(<Button>Click</Button>).toJSON();
  expect(tree).toMatchSnapshot();
});

// Inline snapshot
it('returns user object', () => {
  const user = getUser(1);
  expect(user).toMatchInlineSnapshot(`
    Object {
      "id": 1,
      "name": "John",
    }
  `);
});

// Custom serializer
expect.addSnapshotSerializer({
  test: (val) => val && val.testId,
  print: (val) => `TestID: ${val.testId}`
});

// Update snapshots
// Run: jest --updateSnapshot or jest -u
```

## 6. React Testing

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

describe('LoginForm', () => {
  it('renders form fields', () => {
    render(<LoginForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('shows error for invalid email', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'invalid');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();

    render(<LoginForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123'
      });
    });
  });

  it('renders async content', async () => {
    render(<UserProfile userId={1} />);

    // Wait for loading to finish
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
  });
});
```

## 7. API/HTTP Testing

```javascript
import axios from 'axios';

jest.mock('axios');

describe('API Service', () => {
  it('fetches users', async () => {
    const users = [{ id: 1, name: 'John' }];
    axios.get.mockResolvedValue({ data: users });

    const result = await fetchUsers();

    expect(axios.get).toHaveBeenCalledWith('/api/users');
    expect(result).toEqual(users);
  });

  it('handles error', async () => {
    axios.get.mockRejectedValue(new Error('Network error'));

    await expect(fetchUsers()).rejects.toThrow('Network error');
  });
});

// With MSW (Mock Service Worker)
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.get('/api/users', () => {
    return HttpResponse.json([{ id: 1, name: 'John' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

it('fetches users', async () => {
  const users = await fetchUsers();
  expect(users).toHaveLength(1);
});
```

## 8. Coverage

```bash
# Generate coverage report
jest --coverage

# Coverage thresholds in jest.config.js
coverageThreshold: {
  global: {
    branches: 80,
    functions: 80,
    lines: 80,
    statements: 80
  },
  './src/utils/': {
    branches: 100,
    statements: 100
  }
}
```

## 9. Custom Matchers

```javascript
// jest.setup.js
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    if (pass) {
      return {
        message: () => `expected ${received} not to be within range ${floor} - ${ceiling}`,
        pass: true
      };
    } else {
      return {
        message: () => `expected ${received} to be within range ${floor} - ${ceiling}`,
        pass: false
      };
    }
  }
});

// Usage
expect(100).toBeWithinRange(90, 110);
```

## Best Practices

1. **Test behavior, not implementation** - Focus on what, not how
2. **Use descriptive names** - Clear test descriptions
3. **One assertion per test** - When possible
4. **Arrange-Act-Assert** - Structure tests clearly
5. **Mock external dependencies** - Isolate units
6. **Use beforeEach for setup** - DRY test code
7. **Clean up after tests** - Prevent test pollution
8. **Run tests in watch mode** - Faster feedback
9. **Maintain high coverage** - But focus on quality
10. **Use snapshot tests wisely** - For UI components
