---
name: playwright-fixtures-and-hooks
description: Use when managing test state and infrastructure with reusable Playwright fixtures and lifecycle hooks for efficient test setup and teardown.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Playwright Fixtures and Hooks

Master Playwright's fixture system and lifecycle hooks to create reusable
test infrastructure, manage test state, and build maintainable test suites.
This skill covers built-in fixtures, custom fixtures, and best practices
for test setup and teardown.

## Built-in Fixtures

### Core Fixtures

```typescript
import { test, expect } from '@playwright/test';

test('using built-in fixtures', async ({
  page,      // Page instance
  context,   // Browser context
  browser,   // Browser instance
  request,   // API request context
}) => {
  // Each test gets fresh page and context
  await page.goto('https://example.com');
  await expect(page).toHaveTitle(/Example/);
});
```

### Page Fixture

```typescript
test('page fixture examples', async ({ page }) => {
  // Navigate
  await page.goto('https://example.com');

  // Interact
  await page.getByRole('button', { name: 'Click me' }).click();

  // Wait
  await page.waitForLoadState('networkidle');

  // Evaluate
  const title = await page.title();
  expect(title).toBe('Example Domain');
});
```

### Context Fixture

```typescript
test('context fixture examples', async ({ context, page }) => {
  // Add cookies
  await context.addCookies([
    {
      name: 'session',
      value: 'abc123',
      domain: 'example.com',
      path: '/',
    },
  ]);

  // Set permissions
  await context.grantPermissions(['geolocation']);

  // Create additional page in same context
  const page2 = await context.newPage();
  await page2.goto('https://example.com');

  // Both pages share cookies and storage
  await page.goto('https://example.com');
});
```

### Browser Fixture

```typescript
test('browser fixture examples', async ({ browser }) => {
  // Create custom context with options
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    locale: 'en-US',
    timezoneId: 'America/New_York',
    permissions: ['geolocation'],
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  await context.close();
});
```

### Request Fixture

```typescript
test('API testing with request fixture', async ({ request }) => {
  // Make GET request
  const response = await request.get('https://api.example.com/users');
  expect(response.ok()).toBeTruthy();
  expect(response.status()).toBe(200);

  const users = await response.json();
  expect(users).toHaveLength(10);

  // Make POST request
  const createResponse = await request.post('https://api.example.com/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com',
    },
  });
  expect(createResponse.ok()).toBeTruthy();
});
```

## Custom Fixtures

### Basic Custom Fixture

```typescript
// fixtures/base-fixtures.ts
import { test as base } from '@playwright/test';

type MyFixtures = {
  timestamp: string;
};

export const test = base.extend<MyFixtures>({
  timestamp: async ({}, use) => {
    const timestamp = new Date().toISOString();
    await use(timestamp);
  },
});

export { expect } from '@playwright/test';
```

```typescript
// tests/example.spec.ts
import { test, expect } from '../fixtures/base-fixtures';

test('using custom timestamp fixture', async ({ timestamp, page }) => {
  console.log(`Test started at: ${timestamp}`);
  await page.goto('https://example.com');
});
```

### Fixture with Setup and Teardown

```typescript
import { test as base } from '@playwright/test';

type DatabaseFixtures = {
  database: Database;
};

export const test = base.extend<DatabaseFixtures>({
  database: async ({}, use) => {
    // Setup: Create database connection
    const db = await createDatabaseConnection();
    console.log('Database connected');

    // Provide fixture to test
    await use(db);

    // Teardown: Close database connection
    await db.close();
    console.log('Database closed');
  },
});
```

### Fixture Scopes: Test vs Worker

```typescript
import { test as base } from '@playwright/test';

type TestScopedFixtures = {
  uniqueId: string;
};

type WorkerScopedFixtures = {
  apiToken: string;
};

export const test = base.extend<TestScopedFixtures, WorkerScopedFixtures>({
  // Test-scoped: Created for each test
  uniqueId: async ({}, use) => {
    const id = `test-${Date.now()}-${Math.random()}`;
    await use(id);
  },

  // Worker-scoped: Created once per worker
  apiToken: [
    async ({}, use) => {
      const token = await generateApiToken();
      await use(token);
      await revokeApiToken(token);
    },
    { scope: 'worker' },
  ],
});
```

## Authentication Fixtures

### Authenticated User Fixture

```typescript
// fixtures/auth-fixtures.ts
import { test as base } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ browser }, use) => {
    // Create new context with authentication
    const context = await browser.newContext({
      storageState: 'auth.json',
    });

    const page = await context.newPage();
    await use(page);

    await context.close();
  },
});

export { expect } from '@playwright/test';
```

### Multiple User Roles

```typescript
// fixtures/multi-user-fixtures.ts
import { test as base } from '@playwright/test';

type UserFixtures = {
  adminPage: Page;
  userPage: Page;
  guestPage: Page;
};

export const test = base.extend<UserFixtures>({
  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth/admin.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  userPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth/user.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  guestPage: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});
```

### Authentication Setup

```typescript
// auth/setup.ts
import { test as setup } from '@playwright/test';

setup('authenticate as admin', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('Email').fill('admin@example.com');
  await page.getByLabel('Password').fill('admin123');
  await page.getByRole('button', { name: 'Login' }).click();

  await page.waitForURL('**/dashboard');

  await page.context().storageState({ path: 'auth/admin.json' });
});

setup('authenticate as user', async ({ page }) => {
  await page.goto('https://example.com/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('user123');
  await page.getByRole('button', { name: 'Login' }).click();

  await page.waitForURL('**/dashboard');

  await page.context().storageState({ path: 'auth/user.json' });
});
```

## Database Fixtures

### Test Database Fixture

```typescript
// fixtures/database-fixtures.ts
import { test as base } from '@playwright/test';
import { PrismaClient } from '@prisma/client';

type DatabaseFixtures = {
  db: PrismaClient;
  cleanDb: void;
};

export const test = base.extend<DatabaseFixtures>({
  db: [
    async ({}, use) => {
      const db = new PrismaClient();
      await use(db);
      await db.$disconnect();
    },
    { scope: 'worker' },
  ],

  cleanDb: async ({ db }, use) => {
    // Clean database before test
    await db.user.deleteMany();
    await db.product.deleteMany();
    await db.order.deleteMany();

    await use();

    // Clean database after test
    await db.user.deleteMany();
    await db.product.deleteMany();
    await db.order.deleteMany();
  },
});
```

### Seeded Data Fixture

```typescript
// fixtures/seed-fixtures.ts
import { test as base } from './database-fixtures';

type SeedFixtures = {
  testUser: User;
  testProducts: Product[];
};

export const test = base.extend<SeedFixtures>({
  testUser: async ({ db, cleanDb }, use) => {
    const user = await db.user.create({
      data: {
        email: 'test@example.com',
        name: 'Test User',
        password: 'hashedpassword',
      },
    });

    await use(user);
  },

  testProducts: async ({ db, cleanDb }, use) => {
    const products = await db.product.createMany({
      data: [
        { name: 'Product 1', price: 10.99 },
        { name: 'Product 2', price: 20.99 },
        { name: 'Product 3', price: 30.99 },
      ],
    });

    const allProducts = await db.product.findMany();
    await use(allProducts);
  },
});
```

## API Mocking Fixtures

### Mock API Fixture

```typescript
// fixtures/mock-api-fixtures.ts
import { test as base } from '@playwright/test';

type MockApiFixtures = {
  mockApi: void;
};

export const test = base.extend<MockApiFixtures>({
  mockApi: async ({ page }, use) => {
    // Mock API responses
    await page.route('**/api/users', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'User 1' },
          { id: 2, name: 'User 2' },
        ]),
      });
    });

    await page.route('**/api/products', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Product 1', price: 10 },
          { id: 2, name: 'Product 2', price: 20 },
        ]),
      });
    });

    await use();

    // Cleanup: Unroute all
    await page.unrouteAll();
  },
});
```

### Conditional Mocking

```typescript
// fixtures/conditional-mock-fixtures.ts
import { test as base } from '@playwright/test';

type ConditionalMockFixtures = {
  mockFailedApi: void;
  mockSlowApi: void;
};

export const test = base.extend<ConditionalMockFixtures>({
  mockFailedApi: async ({ page }, use) => {
    await page.route('**/api/**', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal Server Error' }),
      });
    });

    await use();
    await page.unrouteAll();
  },

  mockSlowApi: async ({ page }, use) => {
    await page.route('**/api/**', async (route) => {
      // Simulate slow network
      await new Promise((resolve) => setTimeout(resolve, 3000));
      await route.continue();
    });

    await use();
    await page.unrouteAll();
  },
});
```

## Lifecycle Hooks

### Test Hooks

```typescript
import { test, expect } from '@playwright/test';

test.describe('User Management', () => {
  test.beforeAll(async () => {
    // Runs once before all tests in this describe block
    console.log('Setting up test suite');
  });

  test.beforeEach(async ({ page }) => {
    // Runs before each test
    await page.goto('https://example.com');
    console.log('Test starting');
  });

  test.afterEach(async ({ page }, testInfo) => {
    // Runs after each test
    console.log(`Test ${testInfo.status}: ${testInfo.title}`);

    if (testInfo.status !== testInfo.expectedStatus) {
      // Test failed - capture additional debug info
      const screenshot = await page.screenshot();
      await testInfo.attach('failure-screenshot', {
        body: screenshot,
        contentType: 'image/png',
      });
    }
  });

  test.afterAll(async () => {
    // Runs once after all tests in this describe block
    console.log('Cleaning up test suite');
  });

  test('test 1', async ({ page }) => {
    // Test implementation
  });

  test('test 2', async ({ page }) => {
    // Test implementation
  });
});
```

### Nested Hooks

```typescript
test.describe('Parent Suite', () => {
  test.beforeEach(async ({ page }) => {
    console.log('Parent beforeEach');
    await page.goto('https://example.com');
  });

  test.describe('Child Suite 1', () => {
    test.beforeEach(async ({ page }) => {
      console.log('Child 1 beforeEach');
      await page.getByRole('link', { name: 'Products' }).click();
    });

    test('test in child 1', async ({ page }) => {
      // Parent beforeEach runs first, then child beforeEach
    });
  });

  test.describe('Child Suite 2', () => {
    test.beforeEach(async ({ page }) => {
      console.log('Child 2 beforeEach');
      await page.getByRole('link', { name: 'About' }).click();
    });

    test('test in child 2', async ({ page }) => {
      // Parent beforeEach runs first, then child beforeEach
    });
  });
});
```

### Conditional Hooks

```typescript
test.describe('Feature Tests', () => {
  test.beforeEach(async ({ page, browserName }) => {
    // Skip setup for Firefox
    if (browserName === 'firefox') {
      test.skip();
    }

    await page.goto('https://example.com');
  });

  test.afterEach(async ({ page }, testInfo) => {
    // Only run teardown for failed tests
    if (testInfo.status === 'failed') {
      await page.screenshot({ path: `failure-${testInfo.title}.png` });
    }
  });

  test('feature test', async ({ page }) => {
    // Test implementation
  });
});
```

## Fixture Dependencies

### Dependent Fixtures

```typescript
// fixtures/dependent-fixtures.ts
import { test as base } from '@playwright/test';

type DependentFixtures = {
  config: Config;
  apiClient: ApiClient;
  authenticatedClient: ApiClient;
};

export const test = base.extend<DependentFixtures>({
  // Base fixture
  config: async ({}, use) => {
    const config = {
      apiUrl: process.env.API_URL || 'http://localhost:3000',
      timeout: 30000,
    };
    await use(config);
  },

  // Depends on config
  apiClient: async ({ config }, use) => {
    const client = new ApiClient(config.apiUrl, config.timeout);
    await use(client);
  },

  // Depends on apiClient
  authenticatedClient: async ({ apiClient }, use) => {
    const token = await apiClient.login('user@example.com', 'password');
    apiClient.setAuthToken(token);
    await use(apiClient);
  },
});
```

### Combining Multiple Fixtures

```typescript
// fixtures/combined-fixtures.ts
import { test as base } from '@playwright/test';

type CombinedFixtures = {
  setupComplete: void;
};

export const test = base.extend<CombinedFixtures>({
  setupComplete: async (
    { page, db, mockApi, testUser },
    use
  ) => {
    // All dependent fixtures are initialized
    await page.goto('https://example.com');
    await page.context().addCookies([
      {
        name: 'userId',
        value: testUser.id.toString(),
        domain: 'example.com',
        path: '/',
      },
    ]);

    await use();
  },
});
```

## Advanced Fixture Patterns

### Factory Fixtures

```typescript
// fixtures/factory-fixtures.ts
import { test as base } from '@playwright/test';

type FactoryFixtures = {
  createUser: (data: Partial<User>) => Promise<User>;
  createProduct: (data: Partial<Product>) => Promise<Product>;
};

export const test = base.extend<FactoryFixtures>({
  createUser: async ({ db }, use) => {
    const users: User[] = [];

    const createUser = async (data: Partial<User>) => {
      const user = await db.user.create({
        data: {
          email: data.email || `user-${Date.now()}@example.com`,
          name: data.name || 'Test User',
          password: data.password || 'password123',
          ...data,
        },
      });
      users.push(user);
      return user;
    };

    await use(createUser);

    // Cleanup: Delete all created users
    for (const user of users) {
      await db.user.delete({ where: { id: user.id } });
    }
  },

  createProduct: async ({ db }, use) => {
    const products: Product[] = [];

    const createProduct = async (data: Partial<Product>) => {
      const product = await db.product.create({
        data: {
          name: data.name || `Product ${Date.now()}`,
          price: data.price || 9.99,
          description: data.description || 'Test product',
          ...data,
        },
      });
      products.push(product);
      return product;
    };

    await use(createProduct);

    // Cleanup: Delete all created products
    for (const product of products) {
      await db.product.delete({ where: { id: product.id } });
    }
  },
});
```

### Option Fixtures

```typescript
// fixtures/option-fixtures.ts
import { test as base } from '@playwright/test';

type OptionsFixtures = {
  slowNetwork: boolean;
};

export const test = base.extend<OptionsFixtures>({
  slowNetwork: [false, { option: true }],

  page: async ({ page, slowNetwork }, use) => {
    if (slowNetwork) {
      await page.route('**/*', async (route) => {
        await new Promise((resolve) => setTimeout(resolve, 1000));
        await route.continue();
      });
    }

    await use(page);
  },
});
```

```typescript
// tests/slow-network.spec.ts
import { test, expect } from '../fixtures/option-fixtures';

test('test with slow network', async ({ page }) => {
  test.use({ slowNetwork: true });

  await page.goto('https://example.com');
  // This will be slow due to network throttling
});

test('test with normal network', async ({ page }) => {
  await page.goto('https://example.com');
  // Normal speed
});
```

## Test Info and Attachments

### Using Test Info

```typescript
test('example with test info', async ({ page }, testInfo) => {
  console.log(`Test title: ${testInfo.title}`);
  console.log(`Project: ${testInfo.project.name}`);
  console.log(`Retry: ${testInfo.retry}`);

  await page.goto('https://example.com');

  // Attach screenshot
  const screenshot = await page.screenshot();
  await testInfo.attach('page-screenshot', {
    body: screenshot,
    contentType: 'image/png',
  });

  // Attach JSON data
  await testInfo.attach('test-data', {
    body: JSON.stringify({ foo: 'bar' }),
    contentType: 'application/json',
  });

  // Attach text
  await testInfo.attach('notes', {
    body: 'Test completed successfully',
    contentType: 'text/plain',
  });
});
```

### Conditional Test Execution

```typescript
test('browser-specific test', async ({ page, browserName }) => {
  test.skip(browserName === 'webkit', 'Not supported in Safari');

  await page.goto('https://example.com');
  // Test only runs in Chromium and Firefox
});

test('slow test', async ({ page }) => {
  test.slow(); // Triple timeout for this test

  await page.goto('https://slow-site.example.com');
  // Long-running operations
});

test('expected to fail', async ({ page }) => {
  test.fail(); // Mark as expected failure

  await page.goto('https://example.com');
  await expect(page.getByText('Non-existent')).toBeVisible();
});
```

## Fixture Best Practices

### Organizing Fixtures

```text
fixtures/
├── index.ts              # Export all fixtures
├── auth-fixtures.ts      # Authentication fixtures
├── database-fixtures.ts  # Database fixtures
├── mock-api-fixtures.ts  # API mocking fixtures
└── page-fixtures.ts      # Page-related fixtures
```

```typescript
// fixtures/index.ts
import { test as authTest } from './auth-fixtures';
import { test as dbTest } from './database-fixtures';
import { test as mockTest } from './mock-api-fixtures';

export const test = authTest.extend(dbTest.fixtures).extend(mockTest.fixtures);

export { expect } from '@playwright/test';
```

### Fixture Naming Conventions

```typescript
// Good naming
export const test = base.extend({
  authenticatedPage: async ({}, use) => { /* ... */ },
  testUser: async ({}, use) => { /* ... */ },
  mockApi: async ({}, use) => { /* ... */ },
});

// Avoid
export const test = base.extend({
  page2: async ({}, use) => { /* ... */ },  // Not descriptive
  data: async ({}, use) => { /* ... */ },   // Too generic
  fixture1: async ({}, use) => { /* ... */ }, // Meaningless name
});
```

## When to Use This Skill

- Setting up reusable test infrastructure
- Managing authentication state across tests
- Creating database seeding and cleanup logic
- Implementing API mocking for tests
- Building factory fixtures for test data generation
- Establishing test lifecycle patterns
- Creating worker-scoped fixtures for performance
- Organizing complex test setup and teardown
- Implementing conditional test behavior
- Building type-safe fixture systems

## Resources

- Playwright Fixtures: <https://playwright.dev/docs/test-fixtures>
- Playwright Test Hooks: <https://playwright.dev/docs/test-hooks>
- Playwright API Testing: <https://playwright.dev/docs/api-testing>
