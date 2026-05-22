---
name: jest-advanced
description: Use when advanced Jest features including custom matchers, parameterized tests with test.each, coverage configuration, and performance optimization.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Jest Advanced

Master advanced Jest features including custom matchers, parameterized tests with test.each, coverage configuration, and performance optimization. This skill covers sophisticated testing techniques for complex scenarios and large test suites.

## Custom Matchers

### Creating Custom Matchers

```javascript
// matchers/toBeWithinRange.js
export function toBeWithinRange(received, floor, ceiling) {
  const pass = received >= floor && received <= ceiling;
  if (pass) {
    return {
      message: () =>
        `expected ${received} not to be within range ${floor} - ${ceiling}`,
      pass: true
    };
  } else {
    return {
      message: () =>
        `expected ${received} to be within range ${floor} - ${ceiling}`,
      pass: false
    };
  }
}

// jest.setup.js
import { toBeWithinRange } from './matchers/toBeWithinRange';

expect.extend({
  toBeWithinRange
});

// test file
describe('Custom matcher', () => {
  it('should check if number is within range', () => {
    expect(5).toBeWithinRange(1, 10);
    expect(15).not.toBeWithinRange(1, 10);
  });
});
```

### Async Custom Matcher

```javascript
// matchers/toResolveWithin.js
export async function toResolveWithin(received, timeout) {
  const startTime = Date.now();
  try {
    await received;
    const duration = Date.now() - startTime;
    const pass = duration <= timeout;

    return {
      message: () =>
        pass
          ? `expected promise not to resolve within ${timeout}ms (resolved in ${duration}ms)`
          : `expected promise to resolve within ${timeout}ms (took ${duration}ms)`,
      pass
    };
  } catch (error) {
    return {
      message: () => `expected promise to resolve but it rejected with ${error}`,
      pass: false
    };
  }
}

// Usage
expect.extend({ toResolveWithin });

it('should resolve quickly', async () => {
  await expect(fetchData()).toResolveWithin(1000);
});
```

### Type-Safe Custom Matchers (TypeScript)

```typescript
// matchers/index.ts
interface CustomMatchers<R = unknown> {
  toBeWithinRange(floor: number, ceiling: number): R;
  toHaveValidEmail(): R;
}

declare global {
  namespace jest {
    interface Expect extends CustomMatchers {}
    interface Matchers<R> extends CustomMatchers<R> {}
    interface InverseAsymmetricMatchers extends CustomMatchers {}
  }
}

export function toBeWithinRange(
  this: jest.MatcherContext,
  received: number,
  floor: number,
  ceiling: number
): jest.CustomMatcherResult {
  const pass = received >= floor && received <= ceiling;
  return {
    message: () =>
      pass
        ? `expected ${received} not to be within range ${floor} - ${ceiling}`
        : `expected ${received} to be within range ${floor} - ${ceiling}`,
    pass
  };
}

export function toHaveValidEmail(
  this: jest.MatcherContext,
  received: string
): jest.CustomMatcherResult {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const pass = emailRegex.test(received);
  return {
    message: () =>
      pass
        ? `expected ${received} not to be a valid email`
        : `expected ${received} to be a valid email`,
    pass
  };
}

// jest.setup.ts
import * as matchers from './matchers';
expect.extend(matchers);
```

## Parameterized Tests

### test.each with Arrays

```javascript
describe('Addition', () => {
  test.each([
    [1, 1, 2],
    [1, 2, 3],
    [2, 1, 3],
  ])('add(%i, %i) should equal %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });
});
```

### test.each with Objects

```javascript
describe('User validation', () => {
  test.each([
    { email: 'test@example.com', valid: true },
    { email: 'invalid', valid: false },
    { email: 'test@', valid: false },
    { email: '@example.com', valid: false },
  ])('validateEmail($email) should return $valid', ({ email, valid }) => {
    expect(validateEmail(email)).toBe(valid);
  });
});
```

### test.each with Template Literals

```javascript
describe('String operations', () => {
  test.each`
    input        | method      | expected
    ${'hello'}   | ${'upper'}  | ${'HELLO'}
    ${'WORLD'}   | ${'lower'}  | ${'world'}
    ${'HeLLo'}   | ${'title'}  | ${'Hello'}
  `('transform $input using $method should return $expected',
    ({ input, method, expected }) => {
      expect(transform(input, method)).toBe(expected);
    }
  );
});
```

### describe.each for Multiple Test Suites

```javascript
describe.each([
  { browser: 'Chrome', version: 90 },
  { browser: 'Firefox', version: 88 },
  { browser: 'Safari', version: 14 },
])('Browser compatibility - $browser', ({ browser, version }) => {
  it(`should support ${browser} version ${version}`, () => {
    expect(isSupported(browser, version)).toBe(true);
  });

  it(`should handle ${browser} specific features`, () => {
    expect(getFeatures(browser)).toBeDefined();
  });
});
```

## Coverage Configuration

### Advanced Coverage Settings

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],

  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**',
    '!src/**/types/**',
    '!src/index.{js,ts}',
  ],

  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/core/': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95
    },
    './src/utils/': {
      branches: 85,
      functions: 90,
      lines: 90,
      statements: 90
    }
  },

  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/',
    '/__mocks__/',
    '/coverage/'
  ]
};
```

### Custom Coverage Reporter

```javascript
// custom-reporter.js
class CustomCoverageReporter {
  constructor(globalConfig, options) {
    this._globalConfig = globalConfig;
    this._options = options;
  }

  onRunComplete(contexts, results) {
    const { coverageMap } = results;

    if (!coverageMap) {
      return;
    }

    const summary = coverageMap.getCoverageSummary();
    const metrics = {
      lines: summary.lines.pct,
      statements: summary.statements.pct,
      functions: summary.functions.pct,
      branches: summary.branches.pct
    };

    console.log('\nCoverage Summary:');
    console.log(`Lines:      ${metrics.lines}%`);
    console.log(`Statements: ${metrics.statements}%`);
    console.log(`Functions:  ${metrics.functions}%`);
    console.log(`Branches:   ${metrics.branches}%`);

    // Send to external service
    if (this._options.webhook) {
      this.sendToWebhook(metrics, this._options.webhook);
    }
  }

  async sendToWebhook(metrics, url) {
    // Implementation
  }
}

module.exports = CustomCoverageReporter;

// jest.config.js
module.exports = {
  coverageReporters: [
    'text',
    ['./custom-reporter.js', { webhook: 'https://example.com/coverage' }]
  ]
};
```

## Performance Optimization

### Running Tests in Parallel

```javascript
// jest.config.js
module.exports = {
  maxWorkers: '50%', // Use 50% of available CPU cores
  // or specify a number
  // maxWorkers: 4,

  // Parallelize tests within a file
  maxConcurrency: 5,

  // Cache directory
  cacheDirectory: '.jest-cache',

  // Run tests in band for debugging
  // runInBand: false
};
```

### Selective Test Execution

```javascript
// Run only tests that changed
// package.json
{
  "scripts": {
    "test:changed": "jest --onlyChanged",
    "test:related": "jest --findRelatedTests src/modified-file.js"
  }
}
```

### Test Sharding for CI

```bash
# Split tests across multiple CI machines
jest --shard=1/3  # Run first third
jest --shard=2/3  # Run second third
jest --shard=3/3  # Run last third
```

### Bail on First Failure

```javascript
// jest.config.js
module.exports = {
  bail: 1, // Stop after first failure
  // bail: true, // Stop after any failure
};
```

## Advanced Mocking

### Mock Implementations with Different Return Values

```javascript
describe('Complex mocking', () => {
  it('should return different values on consecutive calls', () => {
    const mockFn = jest
      .fn()
      .mockReturnValueOnce(1)
      .mockReturnValueOnce(2)
      .mockReturnValue(3);

    expect(mockFn()).toBe(1);
    expect(mockFn()).toBe(2);
    expect(mockFn()).toBe(3);
    expect(mockFn()).toBe(3);
  });

  it('should implement complex logic', () => {
    const mockFn = jest.fn((x) => {
      if (x < 0) return 'negative';
      if (x === 0) return 'zero';
      return 'positive';
    });

    expect(mockFn(-5)).toBe('negative');
    expect(mockFn(0)).toBe('zero');
    expect(mockFn(5)).toBe('positive');
  });
});
```

### Mock Module Factories

```javascript
// dynamic-mock.test.js
jest.mock('./api', () => {
  const actual = jest.requireActual('./api');
  return {
    ...actual,
    fetchUser: jest.fn(),
    // Use a factory for dynamic values
    getDefaultUser: jest.fn(() => ({
      id: Math.random(),
      name: 'Test User'
    }))
  };
});

describe('Dynamic mocks', () => {
  it('should generate different default users', () => {
    const user1 = getDefaultUser();
    const user2 = getDefaultUser();
    expect(user1.id).not.toBe(user2.id);
  });
});
```

### Mocking ES6 Classes

```javascript
// Database.js
export class Database {
  constructor(config) {
    this.config = config;
  }

  async connect() {
    // Implementation
  }

  async query(sql) {
    // Implementation
  }
}

// Database.test.js
import { Database } from './Database';

jest.mock('./Database');

describe('Database mock', () => {
  beforeEach(() => {
    Database.mockClear();
  });

  it('should mock class constructor', () => {
    const mockConnect = jest.fn();
    const mockQuery = jest.fn().mockResolvedValue([{ id: 1 }]);

    Database.mockImplementation(() => ({
      connect: mockConnect,
      query: mockQuery
    }));

    const db = new Database({ host: 'localhost' });
    expect(Database).toHaveBeenCalledWith({ host: 'localhost' });

    db.connect();
    expect(mockConnect).toHaveBeenCalled();
  });
});
```

## Advanced Assertions

### Asymmetric Matchers

```javascript
describe('Asymmetric matchers', () => {
  it('should match part of an object', () => {
    const user = {
      id: 1,
      name: 'John',
      email: 'john@example.com',
      createdAt: new Date()
    };

    expect(user).toEqual({
      id: expect.any(Number),
      name: 'John',
      email: expect.stringContaining('@'),
      createdAt: expect.any(Date)
    });
  });

  it('should match array containing', () => {
    const arr = [1, 2, 3, 4, 5];
    expect(arr).toEqual(expect.arrayContaining([2, 4]));
  });

  it('should match object containing', () => {
    const obj = { a: 1, b: 2, c: 3 };
    expect(obj).toEqual(expect.objectContaining({ a: 1, c: 3 }));
  });

  it('should use custom matchers', () => {
    expect({ a: 1, b: 2 }).toEqual({
      a: expect.any(Number),
      b: expect.any(Number)
    });
  });
});
```

### Complex Assertions

```javascript
describe('Complex assertions', () => {
  it('should verify complex data structures', () => {
    const response = {
      status: 200,
      data: {
        users: [
          { id: 1, name: 'John', roles: ['admin'] },
          { id: 2, name: 'Jane', roles: ['user'] }
        ],
        meta: {
          total: 2,
          page: 1
        }
      }
    };

    expect(response).toMatchObject({
      status: 200,
      data: {
        users: expect.arrayContaining([
          expect.objectContaining({
            name: 'John',
            roles: expect.arrayContaining(['admin'])
          })
        ]),
        meta: {
          total: expect.any(Number)
        }
      }
    });
  });
});
```

## Test Isolation and Cleanup

### Resetting Module Registry

```javascript
describe('Module isolation', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  it('should load fresh module instance', () => {
    const module1 = require('./counter');
    module1.increment();
    expect(module1.getCount()).toBe(1);

    jest.resetModules();

    const module2 = require('./counter');
    expect(module2.getCount()).toBe(0);
  });
});
```

### Clearing vs Resetting vs Restoring Mocks

```javascript
describe('Mock cleanup', () => {
  const mockFn = jest.fn();

  beforeEach(() => {
    mockFn.mockReturnValue(42);
  });

  afterEach(() => {
    // jest.clearAllMocks();    // Clears call history
    // jest.resetAllMocks();    // Clears call history and implementations
    // jest.restoreAllMocks();  // Restores original implementations
  });

  it('should understand mock cleanup', () => {
    mockFn();
    expect(mockFn).toHaveBeenCalledTimes(1);

    // clearAllMocks: Removes call history but keeps implementation
    jest.clearAllMocks();
    expect(mockFn).toHaveBeenCalledTimes(0);
    expect(mockFn()).toBe(42); // Implementation still works

    // resetAllMocks: Removes call history and implementation
    jest.resetAllMocks();
    expect(mockFn()).toBeUndefined(); // No implementation

    // restoreAllMocks: Restores original (for spies)
    const obj = { method: () => 'original' };
    const spy = jest.spyOn(obj, 'method');
    spy.mockReturnValue('mocked');
    expect(obj.method()).toBe('mocked');
    jest.restoreAllMocks();
    expect(obj.method()).toBe('original');
  });
});
```

## Testing Strategies

### Contract Testing

```javascript
// Define contract
const userContract = {
  id: expect.any(Number),
  name: expect.any(String),
  email: expect.stringMatching(/^[^\s@]+@[^\s@]+\.[^\s@]+$/),
  roles: expect.arrayContaining([expect.any(String)]),
  createdAt: expect.any(String)
};

describe('User API contract', () => {
  it('should match user contract', async () => {
    const user = await fetchUser(1);
    expect(user).toMatchObject(userContract);
  });

  it('should match users list contract', async () => {
    const users = await fetchUsers();
    expect(users).toEqual(
      expect.arrayContaining([
        expect.objectContaining(userContract)
      ])
    );
  });
});
```

### Data-Driven Testing

```javascript
const testCases = require('./test-data.json');

describe.each(testCases)('Data-driven tests', (testCase) => {
  it(`should handle ${testCase.description}`, () => {
    const result = processData(testCase.input);
    expect(result).toEqual(testCase.expected);
  });
});
```

## Best Practices

1. **Use custom matchers for domain-specific assertions** - Create reusable matchers for common validation patterns
2. **Leverage test.each for parameterized tests** - Reduce duplication and improve test coverage
3. **Configure coverage thresholds per directory** - Set stricter requirements for critical code paths
4. **Optimize test execution with workers** - Use parallel execution for faster test runs
5. **Implement proper mock cleanup** - Understand the difference between clear, reset, and restore
6. **Use asymmetric matchers for flexible assertions** - Match partial objects and dynamic data
7. **Create custom reporters for CI integration** - Send coverage data to external services
8. **Isolate tests with module resets** - Prevent test pollution from shared module state
9. **Use bail for fast feedback** - Stop on first failure during development
10. **Implement contract testing** - Ensure API responses match expected shapes

## Common Pitfalls

1. **Not cleaning up mocks properly** - Using wrong cleanup method leads to test pollution
2. **Over-parameterizing tests** - Too many test.each cases reduce readability
3. **Setting unrealistic coverage thresholds** - 100% coverage requirements slow development
4. **Not using maxWorkers appropriately** - Too many workers can overwhelm CI systems
5. **Forgetting to reset modules** - Shared state between tests causes flaky failures
6. **Creating overly complex custom matchers** - Keep matchers simple and focused
7. **Not typing custom matchers in TypeScript** - Missing types lose IDE support
8. **Misusing asymmetric matchers** - Overly permissive matchers miss bugs
9. **Ignoring coverage reports** - Not acting on coverage gaps reduces test value
10. **Running full suite on every change** - Use --onlyChanged for faster feedback

## When to Use This Skill

- Creating custom matchers for domain-specific validation
- Implementing parameterized tests with many test cases
- Optimizing test suite performance for large projects
- Setting up coverage requirements for CI/CD
- Implementing advanced mocking strategies
- Testing complex data structures with asymmetric matchers
- Creating custom reporters for external integrations
- Debugging test isolation issues
- Implementing contract testing patterns
- Improving test maintainability and reducing duplication
