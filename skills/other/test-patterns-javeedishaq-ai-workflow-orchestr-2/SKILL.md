# Test Patterns

Testing patterns for reliable, maintainable, and fast tests.

> **Template Usage:** Customize for your test framework (Vitest, Jest, Playwright, etc.) and assertion library.

## Test Structure

```typescript
// user.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { userService } from '@/services/user.service';
import { createTestUser, cleanupTestData } from '@/tests/helpers';

describe('UserService', () => {
  let testUserId: string;

  beforeEach(async () => {
    // Setup: Create test data
    const user = await createTestUser();
    testUserId = user.id;
  });

  afterEach(async () => {
    // Cleanup: Remove test data
    await cleanupTestData();
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      const result = await userService.findById(testUserId);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toBeDefined();
        expect(result.data?.id).toBe(testUserId);
      }
    });

    it('should return null when not found', async () => {
      const result = await userService.findById('non-existent-id');

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data).toBeNull();
      }
    });
  });

  describe('create', () => {
    it('should create user with valid input', async () => {
      const input = {
        email: 'newuser@example.com',
        name: 'New User',
      };

      const result = await userService.create(input);

      expect(result.success).toBe(true);
      if (result.success) {
        expect(result.data.email).toBe(input.email);
        expect(result.data.name).toBe(input.name);
      }
    });

    it('should fail when email already exists', async () => {
      const existingUser = await createTestUser();

      const result = await userService.create({
        email: existingUser.email,
        name: 'Another User',
      });

      expect(result.success).toBe(false);
      if (!result.success) {
        expect(result.error.code).toBe('EMAIL_EXISTS');
      }
    });
  });
});
```

## Test Helpers

```typescript
// tests/helpers.ts
import { db } from '@/lib/db';
import { faker } from '@faker-js/faker';

// Track created test data for cleanup
const createdIds: { table: string; id: string }[] = [];

export async function createTestUser(overrides = {}) {
  const user = await db.user.create({
    data: {
      email: faker.internet.email(),
      name: faker.person.fullName(),
      ...overrides,
    },
  });

  createdIds.push({ table: 'user', id: user.id });
  return user;
}

export async function cleanupTestData() {
  // Delete in reverse order to respect FK constraints
  for (const { table, id } of createdIds.reverse()) {
    try {
      await db[table].delete({ where: { id } });
    } catch {
      // Ignore if already deleted
    }
  }
  createdIds.length = 0;
}
```

## E2E Test Pattern

```typescript
// e2e/user-flow.test.ts
import { test, expect } from '@playwright/test';

test.describe('User Registration Flow', () => {
  test('should register new user successfully', async ({ page }) => {
    // Navigate
    await page.goto('/register');

    // Fill form
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="name"]', 'Test User');

    // Submit
    await page.click('button[type="submit"]');

    // Assert redirect
    await expect(page).toHaveURL('/dashboard');

    // Assert success state
    await expect(page.getByText('Welcome, Test User')).toBeVisible();
  });

  test('should show error for existing email', async ({ page }) => {
    await page.goto('/register');

    await page.fill('[name="email"]', 'existing@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await expect(page.getByText('Email already in use')).toBeVisible();
  });
});
```

## API Testing Pattern

```typescript
// api/users.test.ts
import { describe, it, expect } from 'vitest';
import { createServer } from '@/server';

describe('POST /api/users', () => {
  const app = createServer();

  it('should create user with valid data', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'test@example.com',
        name: 'Test User',
      },
      headers: {
        authorization: 'Bearer valid-token',
      },
    });

    expect(response.statusCode).toBe(201);
    expect(response.json()).toMatchObject({
      success: true,
      data: {
        email: 'test@example.com',
        name: 'Test User',
      },
    });
  });

  it('should return 400 for invalid data', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/users',
      payload: {
        email: 'invalid-email',
      },
      headers: {
        authorization: 'Bearer valid-token',
      },
    });

    expect(response.statusCode).toBe(400);
    expect(response.json().success).toBe(false);
  });

  it('should return 401 without auth', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/users',
      payload: { email: 'test@example.com' },
    });

    expect(response.statusCode).toBe(401);
  });
});
```

## Mocking Pattern

```typescript
// tests/mocks.ts
import { vi } from 'vitest';

// Mock external service
vi.mock('@/lib/email', () => ({
  sendEmail: vi.fn().mockResolvedValue({ success: true }),
}));

// Mock with implementation
vi.mock('@/lib/stripe', () => ({
  createPayment: vi.fn().mockImplementation(async (amount) => ({
    id: 'pay_mock_123',
    amount,
    status: 'succeeded',
  })),
}));

// Usage in test
import { sendEmail } from '@/lib/email';

it('should send welcome email after registration', async () => {
  await userService.register({ email: 'test@example.com' });

  expect(sendEmail).toHaveBeenCalledWith({
    to: 'test@example.com',
    template: 'welcome',
  });
});
```

## Test Database Setup

```typescript
// tests/setup.ts
import { beforeAll, afterAll } from 'vitest';
import { db, resetDatabase } from '@/lib/db';

beforeAll(async () => {
  // Use test database
  process.env.DATABASE_URL = process.env.TEST_DATABASE_URL;

  // Reset to clean state
  await resetDatabase();
});

afterAll(async () => {
  await db.$disconnect();
});
```

## Coverage Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
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

## Checklist

- [ ] Tests are isolated (no shared state)
- [ ] Cleanup runs in afterEach/afterAll
- [ ] No hardcoded IDs (use factories)
- [ ] Tests run in parallel safely
- [ ] Mocks external services
- [ ] Tests both happy and error paths
- [ ] Coverage meets thresholds
- [ ] No flaky tests
