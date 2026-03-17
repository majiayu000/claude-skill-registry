---
name: api-testing
description: REST and GraphQL API testing with Playwright. Use when testing APIs, mocking endpoints, validating responses, or integrating API tests with E2E flows.
version: 1.0.0
tags: [testing, api, rest, graphql, playwright, automation]
---

# API Testing with Playwright

Comprehensive API testing for REST and GraphQL endpoints using Playwright's built-in API testing capabilities.

## Quick Start

```typescript
import { test, expect } from '@playwright/test';

test('GET /api/users returns users', async ({ request }) => {
  const response = await request.get('/api/users');

  expect(response.ok()).toBeTruthy();
  expect(response.status()).toBe(200);

  const users = await response.json();
  expect(users).toHaveLength(10);
  expect(users[0]).toHaveProperty('email');
});
```

## Installation

```bash
# Playwright includes API testing - no extra packages needed
npm install -D @playwright/test
```

## Configuration

**playwright.config.ts:**
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  use: {
    baseURL: 'http://localhost:3000',
    extraHTTPHeaders: {
      'Accept': 'application/json',
    },
  },
  projects: [
    {
      name: 'api',
      testMatch: /.*\.api\.spec\.ts/,
    },
    {
      name: 'e2e',
      testMatch: /.*\.e2e\.spec\.ts/,
      use: { browserName: 'chromium' },
    },
  ],
});
```

## REST API Testing

### GET Requests

```typescript
test('fetch user by ID', async ({ request }) => {
  const response = await request.get('/api/users/123');

  expect(response.ok()).toBeTruthy();

  const user = await response.json();
  expect(user.id).toBe(123);
  expect(user.email).toMatch(/@/);
});
```

### POST Requests

```typescript
test('create new user', async ({ request }) => {
  const response = await request.post('/api/users', {
    data: {
      name: 'John Doe',
      email: 'john@example.com',
    },
  });

  expect(response.status()).toBe(201);

  const user = await response.json();
  expect(user.id).toBeDefined();
  expect(user.name).toBe('John Doe');
});
```

### PUT/PATCH Requests

```typescript
test('update user', async ({ request }) => {
  const response = await request.put('/api/users/123', {
    data: {
      name: 'Jane Doe',
    },
  });

  expect(response.ok()).toBeTruthy();

  const user = await response.json();
  expect(user.name).toBe('Jane Doe');
});
```

### DELETE Requests

```typescript
test('delete user', async ({ request }) => {
  const response = await request.delete('/api/users/123');
  expect(response.status()).toBe(204);

  // Verify deletion
  const getResponse = await request.get('/api/users/123');
  expect(getResponse.status()).toBe(404);
});
```

## Authentication

### Bearer Token

```typescript
test.describe('authenticated requests', () => {
  let token: string;

  test.beforeAll(async ({ request }) => {
    const response = await request.post('/api/auth/login', {
      data: {
        email: 'test@example.com',
        password: 'password123',
      },
    });
    const data = await response.json();
    token = data.token;
  });

  test('access protected endpoint', async ({ request }) => {
    const response = await request.get('/api/protected', {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    expect(response.ok()).toBeTruthy();
  });
});
```

### Cookie-Based Auth

```typescript
test('login and access dashboard', async ({ request, context }) => {
  // Login (sets cookie automatically)
  await request.post('/api/auth/login', {
    data: { email: 'test@example.com', password: 'pass' },
  });

  // Cookie is automatically included in subsequent requests
  const response = await request.get('/api/dashboard');
  expect(response.ok()).toBeTruthy();
});
```

## GraphQL Testing

### Query

```typescript
test('GraphQL query users', async ({ request }) => {
  const response = await request.post('/graphql', {
    data: {
      query: `
        query GetUsers {
          users {
            id
            name
            email
          }
        }
      `,
    },
  });

  const { data, errors } = await response.json();
  expect(errors).toBeUndefined();
  expect(data.users).toHaveLength(10);
});
```

### Mutation

```typescript
test('GraphQL create user', async ({ request }) => {
  const response = await request.post('/graphql', {
    data: {
      query: `
        mutation CreateUser($input: CreateUserInput!) {
          createUser(input: $input) {
            id
            name
            email
          }
        }
      `,
      variables: {
        input: {
          name: 'John Doe',
          email: 'john@example.com',
        },
      },
    },
  });

  const { data, errors } = await response.json();
  expect(errors).toBeUndefined();
  expect(data.createUser.id).toBeDefined();
});
```

### With Authentication

```typescript
test('GraphQL with auth', async ({ request }) => {
  const response = await request.post('/graphql', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    data: {
      query: `
        query Me {
          me {
            id
            email
            role
          }
        }
      `,
    },
  });

  const { data } = await response.json();
  expect(data.me.role).toBe('admin');
});
```

## API Mocking (for E2E tests)

### Mock API Responses

```typescript
test('display mocked products', async ({ page }) => {
  // Mock the API
  await page.route('**/api/products', route => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Mock Product', price: 99.99 },
      ]),
    });
  });

  await page.goto('/products');
  await expect(page.locator('.product')).toHaveCount(1);
  await expect(page.locator('.product-name')).toHaveText('Mock Product');
});
```

### Simulate Errors

```typescript
test('handle API error gracefully', async ({ page }) => {
  await page.route('**/api/products', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    });
  });

  await page.goto('/products');
  await expect(page.locator('.error-message')).toBeVisible();
});
```

### Delay Responses

```typescript
test('show loading state', async ({ page }) => {
  await page.route('**/api/products', async route => {
    await new Promise(r => setTimeout(r, 2000));
    route.fulfill({
      status: 200,
      body: JSON.stringify([]),
    });
  });

  await page.goto('/products');
  await expect(page.locator('.loading-spinner')).toBeVisible();
});
```

## Response Validation

### JSON Schema Validation

```typescript
import Ajv from 'ajv';

const ajv = new Ajv();
const userSchema = {
  type: 'object',
  properties: {
    id: { type: 'number' },
    name: { type: 'string' },
    email: { type: 'string', format: 'email' },
  },
  required: ['id', 'name', 'email'],
};

test('validate response schema', async ({ request }) => {
  const response = await request.get('/api/users/1');
  const user = await response.json();

  const validate = ajv.compile(userSchema);
  expect(validate(user)).toBeTruthy();
});
```

### Response Headers

```typescript
test('check response headers', async ({ request }) => {
  const response = await request.get('/api/users');

  expect(response.headers()['content-type']).toContain('application/json');
  expect(response.headers()['x-rate-limit-remaining']).toBeDefined();
});
```

## File Upload

```typescript
import path from 'path';

test('upload file', async ({ request }) => {
  const response = await request.post('/api/upload', {
    multipart: {
      file: {
        name: 'test.pdf',
        mimeType: 'application/pdf',
        buffer: Buffer.from('PDF content'),
      },
      description: 'Test document',
    },
  });

  expect(response.ok()).toBeTruthy();
  const result = await response.json();
  expect(result.filename).toBe('test.pdf');
});
```

## Best Practices

1. **Separate API and E2E tests** - Use different test files/projects
2. **Use fixtures for common data** - Avoid repetition
3. **Test error cases** - 400, 401, 403, 404, 500 responses
4. **Validate response schemas** - Catch breaking changes early
5. **Mock external APIs** - Don't depend on third-party availability
6. **Clean up test data** - Use `afterEach` or `afterAll` hooks

## References

- `references/graphql-testing.md` - Advanced GraphQL patterns
- `references/schema-validation.md` - JSON Schema with Ajv
