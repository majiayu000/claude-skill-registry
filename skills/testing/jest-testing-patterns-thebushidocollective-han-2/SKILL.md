---
name: jest-testing-patterns
description: Use when jest testing patterns including unit tests, mocks, spies, snapshots, and assertion techniques for comprehensive test coverage.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Jest Testing Patterns

Master Jest testing patterns including unit tests, mocks, spies, snapshots, and assertion techniques for comprehensive test coverage. This skill covers the fundamental patterns and practices for writing effective, maintainable tests using Jest.

## Basic Test Structure

### Test Suite Organization

```javascript
describe('Calculator', () => {
  describe('add', () => {
    it('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should add negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it('should handle zero', () => {
      expect(add(0, 5)).toBe(5);
    });
  });

  describe('subtract', () => {
    it('should subtract two numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });
  });
});
```

### Setup and Teardown

```javascript
describe('Database operations', () => {
  let db;

  // Runs once before all tests in this describe block
  beforeAll(async () => {
    db = await initializeDatabase();
  });

  // Runs once after all tests in this describe block
  afterAll(async () => {
    await db.close();
  });

  // Runs before each test
  beforeEach(() => {
    db.clear();
  });

  // Runs after each test
  afterEach(() => {
    db.resetMocks();
  });

  it('should insert a record', async () => {
    const result = await db.insert({ name: 'John' });
    expect(result.id).toBeDefined();
  });

  it('should find a record', async () => {
    await db.insert({ id: 1, name: 'John' });
    const result = await db.findById(1);
    expect(result.name).toBe('John');
  });
});
```

## Matchers and Assertions

### Common Matchers

```javascript
describe('Matchers', () => {
  it('should test equality', () => {
    expect(2 + 2).toBe(4); // Strict equality
    expect({ a: 1 }).toEqual({ a: 1 }); // Deep equality
    expect([1, 2, 3]).toStrictEqual([1, 2, 3]); // Strict deep equality
  });

  it('should test truthiness', () => {
    expect(true).toBeTruthy();
    expect(false).toBeFalsy();
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
    expect('value').toBeDefined();
  });

  it('should test numbers', () => {
    expect(4).toBeGreaterThan(3);
    expect(4).toBeGreaterThanOrEqual(4);
    expect(3).toBeLessThan(4);
    expect(3).toBeLessThanOrEqual(3);
    expect(0.1 + 0.2).toBeCloseTo(0.3, 5);
  });

  it('should test strings', () => {
    expect('team').not.toMatch(/I/);
    expect('Christoph').toMatch(/stop/);
    expect('hello world').toContain('world');
  });

  it('should test arrays and iterables', () => {
    const list = ['apple', 'banana', 'cherry'];
    expect(list).toContain('banana');
    expect(list).toHaveLength(3);
    expect(new Set(list)).toContain('apple');
  });

  it('should test objects', () => {
    expect({ a: 1, b: 2 }).toHaveProperty('a');
    expect({ a: 1, b: 2 }).toHaveProperty('a', 1);
    expect({ a: { b: { c: 1 } } }).toHaveProperty('a.b.c', 1);
  });

  it('should test exceptions', () => {
    expect(() => {
      throw new Error('error');
    }).toThrow();
    expect(() => {
      throw new Error('Invalid input');
    }).toThrow('Invalid input');
    expect(() => {
      throw new Error('Invalid input');
    }).toThrow(/Invalid/);
  });
});
```

### Async Assertions

```javascript
describe('Async tests', () => {
  // Using async/await
  it('should fetch data', async () => {
    const data = await fetchData();
    expect(data).toBeDefined();
  });

  // Using promises
  it('should fetch data with promise', () => {
    return fetchData().then(data => {
      expect(data).toBeDefined();
    });
  });

  // Testing promise rejection
  it('should handle errors', async () => {
    await expect(fetchInvalidData()).rejects.toThrow('Not found');
  });

  // Using resolves/rejects
  it('should resolve with data', async () => {
    await expect(fetchData()).resolves.toEqual({ id: 1 });
  });

  it('should reject with error', async () => {
    await expect(fetchInvalidData()).rejects.toThrow();
  });
});
```

## Mocking

### Function Mocks

```javascript
describe('Function mocking', () => {
  it('should mock a function', () => {
    const mockFn = jest.fn();
    mockFn('arg1', 'arg2');

    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  it('should mock return values', () => {
    const mockFn = jest.fn()
      .mockReturnValue(42)
      .mockReturnValueOnce(1)
      .mockReturnValueOnce(2);

    expect(mockFn()).toBe(1);
    expect(mockFn()).toBe(2);
    expect(mockFn()).toBe(42);
  });

  it('should mock async functions', async () => {
    const mockFn = jest.fn()
      .mockResolvedValue('success')
      .mockResolvedValueOnce('first call');

    expect(await mockFn()).toBe('first call');
    expect(await mockFn()).toBe('success');
  });

  it('should mock implementations', () => {
    const mockFn = jest.fn((a, b) => a + b);
    expect(mockFn(1, 2)).toBe(3);

    mockFn.mockImplementation((a, b) => a * b);
    expect(mockFn(2, 3)).toBe(6);
  });
});
```

### Module Mocking

```javascript
// __mocks__/axios.js
export default {
  get: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} }))
};

// userService.test.js
import axios from 'axios';
import { getUser, createUser } from './userService';

jest.mock('axios');

describe('UserService', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should get user', async () => {
    const mockUser = { id: 1, name: 'John' };
    axios.get.mockResolvedValue({ data: mockUser });

    const user = await getUser(1);

    expect(axios.get).toHaveBeenCalledWith('/users/1');
    expect(user).toEqual(mockUser);
  });

  it('should create user', async () => {
    const newUser = { name: 'Jane' };
    const createdUser = { id: 2, name: 'Jane' };
    axios.post.mockResolvedValue({ data: createdUser });

    const user = await createUser(newUser);

    expect(axios.post).toHaveBeenCalledWith('/users', newUser);
    expect(user).toEqual(createdUser);
  });
});
```

### Partial Mocking

```javascript
// utils.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export const multiply = (a, b) => a * b;

// calculator.test.js
import * as utils from './utils';

jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  multiply: jest.fn()
}));

describe('Calculator', () => {
  it('should use real add function', () => {
    expect(utils.add(2, 3)).toBe(5);
  });

  it('should use mocked multiply function', () => {
    utils.multiply.mockReturnValue(10);
    expect(utils.multiply(2, 3)).toBe(10);
    expect(utils.multiply).toHaveBeenCalledWith(2, 3);
  });
});
```

## Spies

### Spying on Methods

```javascript
describe('Spies', () => {
  it('should spy on object methods', () => {
    const calculator = {
      add: (a, b) => a + b
    };

    const spy = jest.spyOn(calculator, 'add');
    calculator.add(2, 3);

    expect(spy).toHaveBeenCalled();
    expect(spy).toHaveBeenCalledWith(2, 3);
    expect(spy).toHaveReturnedWith(5);

    spy.mockRestore();
  });

  it('should spy and mock implementation', () => {
    const logger = {
      log: (message) => console.log(message)
    };

    const spy = jest.spyOn(logger, 'log').mockImplementation(() => {});
    logger.log('test');

    expect(spy).toHaveBeenCalledWith('test');
    spy.mockRestore();
  });

  it('should spy on getter', () => {
    const obj = {
      get value() {
        return 42;
      }
    };

    const spy = jest.spyOn(obj, 'value', 'get').mockReturnValue(100);
    expect(obj.value).toBe(100);
    spy.mockRestore();
  });
});
```

### Spying on Global Functions

```javascript
describe('Global spies', () => {
  it('should spy on console.log', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation();
    console.log('test message');

    expect(spy).toHaveBeenCalledWith('test message');
    spy.mockRestore();
  });

  it('should spy on Date', () => {
    const mockDate = new Date('2024-01-01');
    const spy = jest.spyOn(global, 'Date').mockImplementation(() => mockDate);

    expect(new Date()).toBe(mockDate);
    spy.mockRestore();
  });
});
```

## Snapshot Testing

### Basic Snapshots

```javascript
import { render } from '@testing-library/react';
import Button from './Button';

describe('Button component', () => {
  it('should match snapshot', () => {
    const { container } = render(<Button label="Click me" />);
    expect(container.firstChild).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const user = {
      name: 'John Doe',
      age: 30
    };
    expect(user).toMatchInlineSnapshot(`
      {
        "age": 30,
        "name": "John Doe",
      }
    `);
  });
});
```

### Property Matchers

```javascript
describe('Snapshot with dynamic data', () => {
  it('should match snapshot with property matchers', () => {
    const user = {
      id: generateId(),
      createdAt: new Date(),
      name: 'John Doe'
    };

    expect(user).toMatchSnapshot({
      id: expect.any(String),
      createdAt: expect.any(Date)
    });
  });
});
```

### Custom Serializers

```javascript
// custom-serializer.js
module.exports = {
  test(val) {
    return val && val.hasOwnProperty('_reactInternalFiber');
  },
  serialize(val, config, indentation, depth, refs, printer) {
    return `<ReactElement ${val.type} />`;
  }
};

// jest.config.js
module.exports = {
  snapshotSerializers: ['./custom-serializer.js']
};
```

## Testing Patterns

### Testing React Components

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Form from './Form';

describe('Form component', () => {
  it('should render form fields', () => {
    render(<Form />);

    expect(screen.getByLabelText('Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit' })).toBeInTheDocument();
  });

  it('should handle user input', async () => {
    const user = userEvent.setup();
    render(<Form />);

    const nameInput = screen.getByLabelText('Name');
    await user.type(nameInput, 'John Doe');

    expect(nameInput).toHaveValue('John Doe');
  });

  it('should submit form', async () => {
    const onSubmit = jest.fn();
    render(<Form onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText('Name'), 'John Doe');
    await userEvent.type(screen.getByLabelText('Email'), 'john@example.com');
    await userEvent.click(screen.getByRole('button', { name: 'Submit' }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com'
      });
    });
  });

  it('should display validation errors', async () => {
    render(<Form />);

    const submitButton = screen.getByRole('button', { name: 'Submit' });
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Name is required')).toBeInTheDocument();
    });
  });
});
```

### Testing Async Operations

```javascript
describe('Async operations', () => {
  it('should wait for async operation', async () => {
    const promise = fetchData();
    const data = await promise;
    expect(data).toBeDefined();
  });

  it('should use fake timers', () => {
    jest.useFakeTimers();

    const callback = jest.fn();
    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();
    jest.advanceTimersByTime(1000);
    expect(callback).toHaveBeenCalled();

    jest.useRealTimers();
  });

  it('should run all timers', () => {
    jest.useFakeTimers();

    const callback1 = jest.fn();
    const callback2 = jest.fn();

    setTimeout(callback1, 1000);
    setTimeout(callback2, 2000);

    jest.runAllTimers();

    expect(callback1).toHaveBeenCalled();
    expect(callback2).toHaveBeenCalled();

    jest.useRealTimers();
  });
});
```

### Testing Error Boundaries

```javascript
import { render, screen } from '@testing-library/react';
import ErrorBoundary from './ErrorBoundary';

const ThrowError = () => {
  throw new Error('Test error');
};

describe('ErrorBoundary', () => {
  it('should catch errors and display fallback', () => {
    // Suppress console.error for this test
    const spy = jest.spyOn(console, 'error').mockImplementation();

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();

    spy.mockRestore();
  });

  it('should render children when no error', () => {
    render(
      <ErrorBoundary>
        <div>Content</div>
      </ErrorBoundary>
    );

    expect(screen.getByText('Content')).toBeInTheDocument();
  });
});
```

## Best Practices

1. **Write descriptive test names** - Use clear, specific names that explain what the test verifies
2. **Follow AAA pattern** - Structure tests with Arrange, Act, Assert sections for clarity
3. **Test behavior, not implementation** - Focus on what the code does, not how it does it
4. **Use appropriate matchers** - Choose the most specific matcher for better error messages
5. **Mock external dependencies** - Isolate unit tests from external services and modules
6. **Clean up after tests** - Use afterEach to reset mocks and clean up side effects
7. **Avoid testing private methods** - Test public interfaces and trust implementation details
8. **Use setup and teardown hooks effectively** - Leverage beforeEach/afterEach for common setup
9. **Test edge cases and error conditions** - Don't just test happy paths
10. **Keep tests fast and isolated** - Each test should run independently and quickly

## Common Pitfalls

1. **Not cleaning up mocks between tests** - Leads to test pollution and flaky tests
2. **Testing implementation details** - Makes tests brittle and hard to maintain
3. **Overusing snapshots** - Snapshots should supplement, not replace, specific assertions
4. **Forgetting to await async operations** - Results in false positives and flaky tests
5. **Not using proper matchers** - Generic matchers provide poor error messages
6. **Mocking too much** - Over-mocking reduces test confidence and value
7. **Writing integration tests as unit tests** - Mixing concerns makes tests slow and complex
8. **Not testing error scenarios** - Only testing happy paths leaves bugs uncaught
9. **Shared state between tests** - Global variables and singletons cause test interdependence
10. **Unclear test names** - Vague names make it hard to understand test failures

## When to Use This Skill

- Writing unit tests for functions and classes
- Testing React components with user interactions
- Mocking external dependencies and APIs
- Creating snapshot tests for UI components
- Testing asynchronous code and promises
- Implementing spies to verify function calls
- Testing error handling and edge cases
- Setting up test fixtures and test data
- Debugging failing tests and understanding test output
- Refactoring tests for better maintainability
