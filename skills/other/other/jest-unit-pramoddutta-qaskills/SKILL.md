---
name: Jest Unit Testing
description: Unit testing skill using Jest for TypeScript and JavaScript, covering mocking, spies, snapshots, coverage, async testing, and custom matchers.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [jest, unit-testing, mocking, coverage, typescript, javascript]
testingTypes: [unit]
frameworks: [jest]
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Jest Unit Testing Skill

You are an expert software engineer specializing in unit testing with Jest. When the user asks you to write, review, or debug Jest unit tests, follow these detailed instructions.

## Core Principles

1. **Test behavior, not implementation** -- Tests should verify what code does, not how it does it.
2. **One assertion focus per test** -- Each test should verify a single logical concept.
3. **Arrange-Act-Assert** -- Structure every test into setup, execution, and verification.
4. **Fast and isolated** -- Unit tests must run in milliseconds and have no external dependencies.
5. **Descriptive names** -- Test names should read as specifications of the code's behavior.

## Project Structure

```
src/
  services/
    user.service.ts
    user.service.test.ts
    order.service.ts
    order.service.test.ts
  utils/
    validators.ts
    validators.test.ts
    formatters.ts
    formatters.test.ts
  models/
    user.model.ts
  __mocks__/
    axios.ts
    database.ts
  __tests__/
    integration/
      user-order.test.ts
jest.config.ts
```

## Configuration

```typescript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
    '!src/**/index.ts',
  ],
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  coverageReporters: ['text', 'lcov', 'json-summary'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  setupFilesAfterSetup: ['<rootDir>/jest.setup.ts'],
  clearMocks: true,
  restoreMocks: true,
};

export default config;
```

## Writing Tests

### Basic Test Structure

```typescript
// validators.ts
export function isValidEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function isStrongPassword(password: string): boolean {
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password) &&
    /[!@#$%^&*]/.test(password)
  );
}
```

```typescript
// validators.test.ts
import { isValidEmail, isStrongPassword } from './validators';

describe('isValidEmail', () => {
  it('should return true for valid email addresses', () => {
    expect(isValidEmail('user@example.com')).toBe(true);
    expect(isValidEmail('first.last@domain.co.uk')).toBe(true);
    expect(isValidEmail('user+tag@example.com')).toBe(true);
  });

  it('should return false for invalid email addresses', () => {
    expect(isValidEmail('')).toBe(false);
    expect(isValidEmail('not-an-email')).toBe(false);
    expect(isValidEmail('@missing-local.com')).toBe(false);
    expect(isValidEmail('missing-at.com')).toBe(false);
    expect(isValidEmail('spaces here@bad.com')).toBe(false);
  });
});

describe('isStrongPassword', () => {
  it('should accept a strong password', () => {
    expect(isStrongPassword('SecurePass1!')).toBe(true);
  });

  it('should reject passwords shorter than 8 characters', () => {
    expect(isStrongPassword('Ab1!')).toBe(false);
  });

  it('should reject passwords without uppercase letters', () => {
    expect(isStrongPassword('lowercase1!')).toBe(false);
  });

  it('should reject passwords without lowercase letters', () => {
    expect(isStrongPassword('UPPERCASE1!')).toBe(false);
  });

  it('should reject passwords without numbers', () => {
    expect(isStrongPassword('NoNumbers!')).toBe(false);
  });

  it('should reject passwords without special characters', () => {
    expect(isStrongPassword('NoSpecial1')).toBe(false);
  });
});
```

### Testing Classes and Services

```typescript
// user.service.ts
import { UserRepository } from './user.repository';
import { EmailService } from './email.service';

export class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(email: string, name: string): Promise<User> {
    const existing = await this.userRepo.findByEmail(email);
    if (existing) {
      throw new Error('User already exists');
    }

    const user = await this.userRepo.create({ email, name });
    await this.emailService.sendWelcomeEmail(user.email, user.name);
    return user;
  }

  async getUser(id: string): Promise<User | null> {
    return this.userRepo.findById(id);
  }

  async deleteUser(id: string): Promise<void> {
    const user = await this.userRepo.findById(id);
    if (!user) {
      throw new Error('User not found');
    }
    await this.userRepo.delete(id);
  }
}
```

```typescript
// user.service.test.ts
import { UserService } from './user.service';
import { UserRepository } from './user.repository';
import { EmailService } from './email.service';

// Mock the dependencies
jest.mock('./user.repository');
jest.mock('./email.service');

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockUserRepo = new UserRepository() as jest.Mocked<UserRepository>;
    mockEmailService = new EmailService() as jest.Mocked<EmailService>;
    userService = new UserService(mockUserRepo, mockEmailService);
  });

  describe('createUser', () => {
    it('should create a user and send welcome email', async () => {
      const newUser = { id: '1', email: 'new@example.com', name: 'New User' };
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockResolvedValue(newUser);
      mockEmailService.sendWelcomeEmail.mockResolvedValue(undefined);

      const result = await userService.createUser('new@example.com', 'New User');

      expect(result).toEqual(newUser);
      expect(mockUserRepo.findByEmail).toHaveBeenCalledWith('new@example.com');
      expect(mockUserRepo.create).toHaveBeenCalledWith({
        email: 'new@example.com',
        name: 'New User',
      });
      expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(
        'new@example.com',
        'New User'
      );
    });

    it('should throw error if user already exists', async () => {
      mockUserRepo.findByEmail.mockResolvedValue({
        id: '1',
        email: 'existing@example.com',
        name: 'Existing',
      });

      await expect(
        userService.createUser('existing@example.com', 'Duplicate')
      ).rejects.toThrow('User already exists');

      expect(mockUserRepo.create).not.toHaveBeenCalled();
      expect(mockEmailService.sendWelcomeEmail).not.toHaveBeenCalled();
    });
  });

  describe('getUser', () => {
    it('should return user when found', async () => {
      const user = { id: '1', email: 'user@example.com', name: 'User' };
      mockUserRepo.findById.mockResolvedValue(user);

      const result = await userService.getUser('1');

      expect(result).toEqual(user);
      expect(mockUserRepo.findById).toHaveBeenCalledWith('1');
    });

    it('should return null when user not found', async () => {
      mockUserRepo.findById.mockResolvedValue(null);

      const result = await userService.getUser('nonexistent');

      expect(result).toBeNull();
    });
  });

  describe('deleteUser', () => {
    it('should delete an existing user', async () => {
      const user = { id: '1', email: 'user@example.com', name: 'User' };
      mockUserRepo.findById.mockResolvedValue(user);
      mockUserRepo.delete.mockResolvedValue(undefined);

      await userService.deleteUser('1');

      expect(mockUserRepo.delete).toHaveBeenCalledWith('1');
    });

    it('should throw error when deleting non-existent user', async () => {
      mockUserRepo.findById.mockResolvedValue(null);

      await expect(userService.deleteUser('nonexistent')).rejects.toThrow(
        'User not found'
      );
    });
  });
});
```

## Mocking Patterns

### Manual Mocks

```typescript
// __mocks__/axios.ts
const axios = {
  get: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  put: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} })),
  create: jest.fn(function () {
    return axios;
  }),
  interceptors: {
    request: { use: jest.fn() },
    response: { use: jest.fn() },
  },
};

export default axios;
```

### Spying on Methods

```typescript
it('should call console.error on failure', async () => {
  const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

  await processData(invalidData);

  expect(consoleSpy).toHaveBeenCalledWith(
    expect.stringContaining('Processing failed')
  );

  consoleSpy.mockRestore();
});
```

### Mocking Timers

```typescript
describe('Debounce function', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should debounce function calls', () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 300);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(300);

    expect(fn).toHaveBeenCalledTimes(1);
  });

  it('should reset timer on subsequent calls', () => {
    const fn = jest.fn();
    const debounced = debounce(fn, 300);

    debounced();
    jest.advanceTimersByTime(200);
    debounced(); // resets the timer
    jest.advanceTimersByTime(200);

    expect(fn).not.toHaveBeenCalled();

    jest.advanceTimersByTime(100);
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
```

### Mocking Modules

```typescript
// Mock an entire module
jest.mock('fs', () => ({
  readFileSync: jest.fn(() => 'mocked content'),
  writeFileSync: jest.fn(),
  existsSync: jest.fn(() => true),
}));

// Mock with factory function
jest.mock('./config', () => ({
  getConfig: () => ({
    apiUrl: 'http://test-api.example.com',
    timeout: 1000,
  }),
}));

// Partial mock -- keep some original implementations
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  fetchData: jest.fn(),
}));
```

## Async Testing

```typescript
// Testing resolved promises
it('should resolve with data', async () => {
  const result = await fetchUser('1');
  expect(result.name).toBe('John');
});

// Testing rejected promises
it('should reject with error', async () => {
  await expect(fetchUser('invalid')).rejects.toThrow('Not found');
});

// Testing callbacks
it('should call callback with data', (done) => {
  fetchUserCallback('1', (err, data) => {
    expect(err).toBeNull();
    expect(data.name).toBe('John');
    done();
  });
});

// Testing event emitters
it('should emit data event', (done) => {
  const emitter = new DataEmitter();
  emitter.on('data', (payload) => {
    expect(payload).toEqual({ id: 1 });
    done();
  });
  emitter.start();
});
```

## Snapshot Testing

```typescript
// Component snapshot
it('should render correctly', () => {
  const output = renderComponent({ name: 'Test', count: 5 });
  expect(output).toMatchSnapshot();
});

// Inline snapshot
it('should format user display name', () => {
  const result = formatDisplayName({ first: 'John', last: 'Doe' });
  expect(result).toMatchInlineSnapshot(`"John Doe"`);
});

// Custom serializer
expect.addSnapshotSerializer({
  test: (val) => val instanceof Date,
  print: (val) => `Date(${(val as Date).toISOString()})`,
});
```

## Custom Matchers

```typescript
// jest.setup.ts
expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },

  toBeValidEmail(received: string) {
    const pass = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(received);
    return {
      pass,
      message: () => `expected "${received}" to be a valid email address`,
    };
  },

  toContainObject(received: any[], expected: Record<string, any>) {
    const pass = received.some((item) =>
      Object.entries(expected).every(([key, value]) => item[key] === value)
    );
    return {
      pass,
      message: () =>
        `expected array to contain object matching ${JSON.stringify(expected)}`,
    };
  },
});

// Type declaration
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinRange(floor: number, ceiling: number): R;
      toBeValidEmail(): R;
      toContainObject(expected: Record<string, any>): R;
    }
  }
}
```

## Test Utilities

### Test Data Helpers

```typescript
export function createMockUser(overrides: Partial<User> = {}): User {
  return {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
    createdAt: '2024-01-01T00:00:00Z',
    ...overrides,
  };
}

export function createMockResponse<T>(data: T, status = 200) {
  return {
    data,
    status,
    headers: {},
    config: {},
    statusText: 'OK',
  };
}
```

## Best Practices

1. **One logical assertion per test** -- Multiple `expect` calls are fine if they verify one concept.
2. **Use `describe` blocks** to organize tests by method or feature.
3. **Name tests as specifications** -- `it('should return null when user not found')`.
4. **Mock at the boundary** -- Mock external services, not internal functions.
5. **Use `beforeEach` for setup** -- Ensure clean state for every test.
6. **Set `clearMocks: true`** in config -- Automatically clear mock state between tests.
7. **Prefer `mockResolvedValue` over `mockImplementation`** for simple returns.
8. **Test edge cases** -- Empty strings, null, undefined, zero, negative numbers.
9. **Keep tests fast** -- A slow unit test is usually testing too much.
10. **Maintain coverage thresholds** -- Set minimums and enforce in CI.

## Anti-Patterns to Avoid

1. **Testing implementation details** -- Refactoring should not break tests.
2. **Excessive mocking** -- If you mock everything, you test nothing.
3. **Shared mutable state** -- Never use `let` variables modified across tests without `beforeEach`.
4. **Testing private methods directly** -- Test through the public API.
5. **Snapshot abuse** -- Do not snapshot large objects; the diff becomes meaningless.
6. **No assertions** -- A test without `expect()` always passes and tests nothing.
7. **Ignoring test failures** -- Never use `test.skip` or `.only` in committed code.
8. **Testing framework code** -- Do not test that `Array.map` works.
9. **Giant test files** -- Keep test files focused and under 300 lines.
10. **Not testing error paths** -- The catch/error branches need testing too.

## Running Tests

```bash
# Run all tests
npx jest

# Run specific file
npx jest src/services/user.service.test.ts

# Run tests matching pattern
npx jest --testPathPattern="user"

# Run with coverage
npx jest --coverage

# Watch mode
npx jest --watch

# Run only changed files
npx jest --onlyChanged

# Verbose output
npx jest --verbose
```
