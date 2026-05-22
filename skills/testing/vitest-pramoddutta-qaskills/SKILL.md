---
name: Vitest Testing
description: Modern JavaScript and TypeScript testing with Vitest, covering unit testing, integration testing, mocking, snapshots, browser mode, and Vite integration.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [vitest, unit-testing, vite, typescript, javascript, mocking, snapshots]
testingTypes: [unit, integration]
frameworks: []
languages: [typescript, javascript]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# Vitest Testing Skill

You are an expert software engineer specializing in testing with Vitest. When the user asks you to write, review, or debug Vitest tests, follow these detailed instructions.

## Core Principles

1. **Blazing fast** -- Vitest is designed for speed with native ESM support and smart test running.
2. **Vite-native** -- Leverages Vite's config, transformers, and plugins for seamless integration.
3. **Jest-compatible API** -- Familiar API makes migration from Jest straightforward.
4. **Watch mode first** -- Vitest excels at watch mode with instant feedback.
5. **Test isolation** -- Each test should be independent and deterministic.

## Project Structure

```
project/
  src/
    components/
      Button.tsx
      Button.test.tsx
    services/
      user.service.ts
      user.service.test.ts
    utils/
      validators.ts
      validators.test.ts
  tests/
    integration/
      api.test.ts
      db.test.ts
    fixtures/
      test-data.ts
    setup.ts
  vitest.config.ts
  vite.config.ts
```

## Configuration

### Basic Config

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setup.ts',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.test.ts',
        '**/*.spec.ts',
        '**/types/',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    include: ['**/*.{test,spec}.{ts,tsx}'],
    exclude: ['node_modules', 'dist', 'build'],
    testTimeout: 10000,
    hookTimeout: 10000,
  },
});
```

### Advanced Config with Multiple Environments

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    environmentMatchGlobs: [
      ['**/*.test.tsx', 'jsdom'],
      ['**/*.browser.test.ts', 'jsdom'],
      ['**/*.node.test.ts', 'node'],
      ['**/*.edge.test.ts', 'edge-runtime'],
    ],
    poolOptions: {
      threads: {
        singleThread: false,
        isolate: true,
      },
    },
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{ts,tsx}'],
    },
    benchmark: {
      include: ['**/*.bench.{ts,tsx}'],
    },
  },
});
```

## Writing Tests

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { sum, multiply } from './math';

describe('Math utilities', () => {
  it('should add two numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });

  it('should multiply two numbers', () => {
    expect(multiply(4, 5)).toBe(20);
  });

  it('should handle zero', () => {
    expect(sum(0, 0)).toBe(0);
    expect(multiply(5, 0)).toBe(0);
  });

  it('should handle negative numbers', () => {
    expect(sum(-1, 1)).toBe(0);
    expect(multiply(-2, 3)).toBe(-6);
  });
});
```

### Testing Classes and Services

```typescript
// user.service.ts
export class UserService {
  constructor(
    private apiClient: ApiClient,
    private cache: Cache
  ) {}

  async getUser(id: string): Promise<User> {
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return JSON.parse(cached);

    const user = await this.apiClient.get(`/users/${id}`);
    await this.cache.set(`user:${id}`, JSON.stringify(user), 3600);
    return user;
  }

  async createUser(data: CreateUserDto): Promise<User> {
    return this.apiClient.post('/users', data);
  }
}
```

```typescript
// user.service.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { UserService } from './user.service';

describe('UserService', () => {
  let userService: UserService;
  let mockApiClient: any;
  let mockCache: any;

  beforeEach(() => {
    mockApiClient = {
      get: vi.fn(),
      post: vi.fn(),
    };

    mockCache = {
      get: vi.fn(),
      set: vi.fn(),
    };

    userService = new UserService(mockApiClient, mockCache);
  });

  describe('getUser', () => {
    it('should return cached user if available', async () => {
      const cachedUser = { id: '1', name: 'Cached User' };
      mockCache.get.mockResolvedValue(JSON.stringify(cachedUser));

      const result = await userService.getUser('1');

      expect(result).toEqual(cachedUser);
      expect(mockCache.get).toHaveBeenCalledWith('user:1');
      expect(mockApiClient.get).not.toHaveBeenCalled();
    });

    it('should fetch user from API if not cached', async () => {
      const user = { id: '1', name: 'API User' };
      mockCache.get.mockResolvedValue(null);
      mockApiClient.get.mockResolvedValue(user);

      const result = await userService.getUser('1');

      expect(result).toEqual(user);
      expect(mockApiClient.get).toHaveBeenCalledWith('/users/1');
      expect(mockCache.set).toHaveBeenCalledWith(
        'user:1',
        JSON.stringify(user),
        3600
      );
    });
  });

  describe('createUser', () => {
    it('should create a new user', async () => {
      const newUser = { id: '2', name: 'New User', email: 'new@example.com' };
      mockApiClient.post.mockResolvedValue(newUser);

      const result = await userService.createUser({
        name: 'New User',
        email: 'new@example.com',
      });

      expect(result).toEqual(newUser);
      expect(mockApiClient.post).toHaveBeenCalledWith('/users', {
        name: 'New User',
        email: 'new@example.com',
      });
    });
  });
});
```

## Mocking Patterns

### Function Mocking

```typescript
import { vi, describe, it, expect } from 'vitest';

describe('Function mocking', () => {
  it('should mock a function', () => {
    const mockFn = vi.fn();
    mockFn.mockReturnValue(42);

    expect(mockFn()).toBe(42);
    expect(mockFn).toHaveBeenCalledOnce();
  });

  it('should mock implementation', () => {
    const mockFn = vi.fn((x: number) => x * 2);

    expect(mockFn(5)).toBe(10);
    expect(mockFn).toHaveBeenCalledWith(5);
  });

  it('should mock resolved value', async () => {
    const mockFn = vi.fn();
    mockFn.mockResolvedValue({ id: 1, name: 'Test' });

    const result = await mockFn();
    expect(result).toEqual({ id: 1, name: 'Test' });
  });

  it('should mock rejected value', async () => {
    const mockFn = vi.fn();
    mockFn.mockRejectedValue(new Error('Failed'));

    await expect(mockFn()).rejects.toThrow('Failed');
  });
});
```

### Module Mocking

```typescript
// __mocks__/axios.ts
import { vi } from 'vitest';

export default {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  create: vi.fn(() => ({
    get: vi.fn(),
    post: vi.fn(),
  })),
};
```

```typescript
// api.test.ts
import { describe, it, expect, vi } from 'vitest';

vi.mock('axios');

import axios from 'axios';
import { fetchUser } from './api';

describe('API', () => {
  it('should fetch user data', async () => {
    const mockUser = { id: 1, name: 'Test User' };
    vi.mocked(axios.get).mockResolvedValue({ data: mockUser });

    const user = await fetchUser('1');

    expect(user).toEqual(mockUser);
    expect(axios.get).toHaveBeenCalledWith('/api/users/1');
  });
});
```

### Partial Module Mocking

```typescript
import { vi } from 'vitest';

// Mock only specific exports
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    fetchData: vi.fn(),
  };
});
```

### Spying

```typescript
import { vi, describe, it, expect } from 'vitest';

describe('Spying', () => {
  it('should spy on console.error', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});

    console.error('Test error');

    expect(spy).toHaveBeenCalledWith('Test error');
    spy.mockRestore();
  });

  it('should spy on object method', () => {
    const obj = {
      method: (x: number) => x * 2,
    };

    const spy = vi.spyOn(obj, 'method');
    obj.method(5);

    expect(spy).toHaveBeenCalledWith(5);
    expect(spy).toHaveReturnedWith(10);
  });
});
```

## Timer Mocking

```typescript
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';

describe('Timer tests', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should debounce function calls', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 300);

    debounced();
    debounced();
    debounced();

    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(300);

    expect(fn).toHaveBeenCalledOnce();
  });

  it('should throttle function calls', () => {
    const fn = vi.fn();
    const throttled = throttle(fn, 100);

    throttled();
    expect(fn).toHaveBeenCalledOnce();

    throttled();
    expect(fn).toHaveBeenCalledOnce(); // still once

    vi.advanceTimersByTime(100);
    throttled();
    expect(fn).toHaveBeenCalledTimes(2);
  });

  it('should handle setTimeout', () => {
    const callback = vi.fn();
    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalledOnce();
  });
});
```

## Snapshot Testing

```typescript
import { describe, it, expect } from 'vitest';

describe('Snapshot tests', () => {
  it('should match snapshot', () => {
    const data = {
      id: 1,
      name: 'Test User',
      roles: ['admin', 'user'],
      createdAt: new Date('2024-01-01'),
    };

    expect(data).toMatchSnapshot();
  });

  it('should match inline snapshot', () => {
    const formatted = formatUserName({ first: 'John', last: 'Doe' });

    expect(formatted).toMatchInlineSnapshot(`"John Doe"`);
  });

  it('should match file snapshot', () => {
    const html = renderComponent({ title: 'Test', count: 5 });
    expect(html).toMatchFileSnapshot('./__snapshots__/component.html');
  });
});
```

## Testing React Components

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button component', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should handle click events', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));

    expect(onClick).toHaveBeenCalledOnce();
  });

  it('should be disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('should apply variant classes', () => {
    render(<Button variant="primary">Primary</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });
});
```

## Async Testing

```typescript
import { describe, it, expect } from 'vitest';

describe('Async tests', () => {
  it('should handle async/await', async () => {
    const result = await fetchData();
    expect(result.status).toBe('success');
  });

  it('should handle promises with resolves', async () => {
    await expect(fetchUser('1')).resolves.toEqual({
      id: '1',
      name: 'Test User',
    });
  });

  it('should handle promise rejections', async () => {
    await expect(fetchUser('invalid')).rejects.toThrow('User not found');
  });

  it('should test multiple async operations', async () => {
    const [user, posts] = await Promise.all([
      fetchUser('1'),
      fetchPosts('1'),
    ]);

    expect(user.id).toBe('1');
    expect(posts).toHaveLength(5);
  });
});
```

## Testing with Context and Fixtures

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('User operations', () => {
  let testUser: User;

  beforeEach<{ user: User }>(async (context) => {
    // Setup runs before each test
    testUser = await createTestUser();
    context.user = testUser;
  });

  it<{ user: User }>('should update user name', async ({ user }) => {
    await updateUserName(user.id, 'New Name');
    const updated = await getUser(user.id);
    expect(updated.name).toBe('New Name');
  });

  it<{ user: User }>('should delete user', async ({ user }) => {
    await deleteUser(user.id);
    await expect(getUser(user.id)).rejects.toThrow('Not found');
  });
});
```

## Browser Mode (Experimental)

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      name: 'chromium',
      provider: 'playwright',
      headless: true,
    },
  },
});
```

```typescript
// button.browser.test.ts
import { describe, it, expect } from 'vitest';
import { page } from '@vitest/browser/context';

describe('Button in real browser', () => {
  it('should interact with button', async () => {
    await page.goto('/button-demo');

    const button = await page.locator('button');
    await button.click();

    const counter = await page.locator('#counter');
    await expect(counter).toHaveText('1');
  });
});
```

## Best Practices

1. **Use globals or imports** -- Choose between `globals: true` or explicit imports.
2. **Co-locate tests** -- Keep `*.test.ts` files next to source files for quick access.
3. **Use beforeEach for setup** -- Ensure each test starts with clean state.
4. **Leverage watch mode** -- Vitest's watch mode is incredibly fast and smart.
5. **Use vi.mock at top level** -- Hoisting ensures mocks are ready before imports.
6. **Test behavior, not implementation** -- Focus on what functions do, not how.
7. **Use descriptive test names** -- Tests should read like specifications.
8. **Keep tests isolated** -- No shared mutable state between tests.
9. **Use coverage wisely** -- Aim for high coverage but don't chase 100%.
10. **Prefer integration over unit** -- Test realistic user flows when possible.

## Anti-Patterns to Avoid

1. **Mocking everything** -- Over-mocking tests nothing real.
2. **Testing implementation details** -- Tests should survive refactoring.
3. **Shared mutable state** -- Use beforeEach to reset state.
4. **Giant test files** -- Split by feature or component.
5. **No test isolation** -- Tests should run in any order.
6. **Hardcoded waits** -- Use proper async patterns instead of delays.
7. **Snapshot abuse** -- Don't snapshot large objects without reason.
8. **Testing framework code** -- Don't test that Array.map works.
9. **Ignoring test failures** -- Never commit with `test.skip` or `.only`.
10. **Not cleaning up** -- Use afterEach or cleanup functions.

## Running Tests

```bash
# Run all tests
vitest

# Run in watch mode (default)
vitest watch

# Run once (CI mode)
vitest run

# Run specific file
vitest run src/utils/validators.test.ts

# Run with UI
vitest --ui

# Run with coverage
vitest --coverage

# Run tests matching pattern
vitest --reporter=verbose --grep="user"

# Run in browser mode
vitest --browser

# Run benchmarks
vitest bench
```

## Debugging

```typescript
// Use test.only to isolate tests
it.only('should debug this test', () => {
  // debugger; // Breakpoint
  expect(true).toBe(true);
});

// Use console.log for quick debugging
it('should log values', () => {
  const value = computeValue();
  console.log('Computed value:', value);
  expect(value).toBe(42);
});
```

## Custom Matchers

```typescript
// tests/setup.ts
import { expect } from 'vitest';

expect.extend({
  toBeWithinRange(received: number, floor: number, ceiling: number) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} to be within range ${floor} - ${ceiling}`,
    };
  },
});

declare module 'vitest' {
  interface Assertion<T = any> {
    toBeWithinRange(floor: number, ceiling: number): T;
  }
}
```

## Integration with Vite Plugins

Vitest automatically uses your Vite config, including plugins like:
- `@vitejs/plugin-react` for React JSX support
- `vite-tsconfig-paths` for TypeScript path mapping
- Any custom Vite plugins for asset handling

This makes Vitest the natural choice for Vite-based projects.
