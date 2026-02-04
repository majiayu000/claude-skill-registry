---
name: route-tester
displayName: API Route Testing
description: Framework-agnostic HTTP API route testing patterns, authentication strategies, and integration testing best practices. Supports REST APIs with JWT cookie authentication and other common auth patterns.
---

# API Route Testing Skill

This skill provides framework-agnostic guidance for testing HTTP API routes and endpoints across any backend framework (Express, Next.js API Routes, FastAPI, Django REST, Flask, etc.).

## Core Testing Principles

### 1. Test Types for API Routes

**Unit Tests**
- Test individual route handlers in isolation
- Mock dependencies (database, external APIs)
- Fast execution (< 50ms per test)
- Focus on business logic

**Integration Tests**
- Test full request/response cycle
- Real database (test instance)
- Authentication flow included
- Slower but more comprehensive

**End-to-End Tests**
- Test from client perspective
- Full authentication flow
- Real services (or close replicas)
- Most realistic, slowest execution

### 2. Authentication Testing Patterns

#### JWT Cookie Authentication
```typescript
// Common pattern across frameworks
describe('Protected Route Tests', () => {
  let authCookie: string;

  beforeEach(async () => {
    // Login and get JWT cookie
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'password123' });

    authCookie = loginResponse.headers['set-cookie'][0];
  });

  it('should access protected route with valid cookie', async () => {
    const response = await request(app)
      .get('/api/protected/resource')
      .set('Cookie', authCookie);

    expect(response.status).toBe(200);
  });

  it('should reject access without cookie', async () => {
    const response = await request(app)
      .get('/api/protected/resource');

    expect(response.status).toBe(401);
  });
});
```

#### JWT Bearer Token Authentication
```typescript
describe('Bearer Token Auth', () => {
  let token: string;

  beforeEach(async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'password123' });

    token = response.body.token;
  });

  it('should authenticate with bearer token', async () => {
    const response = await request(app)
      .get('/api/protected/resource')
      .set('Authorization', `Bearer ${token}`);

    expect(response.status).toBe(200);
  });
});
```

### 3. HTTP Method Testing

**GET Requests**
```typescript
describe('GET /api/users', () => {
  it('should return paginated users', async () => {
    const response = await request(app)
      .get('/api/users?page=1&limit=10');

    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('data');
    expect(response.body).toHaveProperty('pagination');
    expect(Array.isArray(response.body.data)).toBe(true);
  });

  it('should filter users by query params', async () => {
    const response = await request(app)
      .get('/api/users?role=admin');

    expect(response.status).toBe(200);
    expect(response.body.data.every(u => u.role === 'admin')).toBe(true);
  });
});
```

**POST Requests**
```typescript
describe('POST /api/users', () => {
  it('should create new user with valid data', async () => {
    const newUser = {
      name: 'John Doe',
      email: 'john@example.com',
      role: 'user'
    };

    const response = await request(app)
      .post('/api/users')
      .set('Cookie', authCookie)
      .send(newUser);

    expect(response.status).toBe(201);
    expect(response.body).toMatchObject(newUser);
    expect(response.body).toHaveProperty('id');
  });

  it('should reject invalid data', async () => {
    const invalidUser = {
      name: 'John Doe'
      // Missing required email field
    };

    const response = await request(app)
      .post('/api/users')
      .set('Cookie', authCookie)
      .send(invalidUser);

    expect(response.status).toBe(400);
    expect(response.body).toHaveProperty('errors');
  });
});
```

**PUT/PATCH Requests**
```typescript
describe('PATCH /api/users/:id', () => {
  it('should update user fields', async () => {
    const updates = { name: 'Jane Doe' };

    const response = await request(app)
      .patch('/api/users/123')
      .set('Cookie', authCookie)
      .send(updates);

    expect(response.status).toBe(200);
    expect(response.body.name).toBe('Jane Doe');
  });

  it('should return 404 for non-existent user', async () => {
    const response = await request(app)
      .patch('/api/users/999999')
      .set('Cookie', authCookie)
      .send({ name: 'Test' });

    expect(response.status).toBe(404);
  });
});
```

**DELETE Requests**
```typescript
describe('DELETE /api/users/:id', () => {
  it('should delete user and return success', async () => {
    const response = await request(app)
      .delete('/api/users/123')
      .set('Cookie', authCookie);

    expect(response.status).toBe(204);
  });

  it('should prevent unauthorized deletion', async () => {
    const response = await request(app)
      .delete('/api/users/123');
      // No auth cookie

    expect(response.status).toBe(401);
  });
});
```

### 4. Response Validation

**Status Codes**
```typescript
describe('HTTP Status Codes', () => {
  it('200 OK - Successful GET', async () => {
    const response = await request(app).get('/api/users');
    expect(response.status).toBe(200);
  });

  it('201 Created - Successful POST', async () => {
    const response = await request(app).post('/api/users').send(validData);
    expect(response.status).toBe(201);
  });

  it('204 No Content - Successful DELETE', async () => {
    const response = await request(app).delete('/api/users/123');
    expect(response.status).toBe(204);
  });

  it('400 Bad Request - Invalid input', async () => {
    const response = await request(app).post('/api/users').send({});
    expect(response.status).toBe(400);
  });

  it('401 Unauthorized - Missing auth', async () => {
    const response = await request(app).get('/api/protected');
    expect(response.status).toBe(401);
  });

  it('403 Forbidden - Insufficient permissions', async () => {
    const response = await request(app).delete('/api/admin/users/123').set('Cookie', userCookie);
    expect(response.status).toBe(403);
  });

  it('404 Not Found - Non-existent resource', async () => {
    const response = await request(app).get('/api/users/999999');
    expect(response.status).toBe(404);
  });

  it('500 Internal Server Error - Server failure', async () => {
    // Test error handling
    mockDatabase.findOne.mockRejectedValue(new Error('DB Error'));
    const response = await request(app).get('/api/users/123');
    expect(response.status).toBe(500);
  });
});
```

**Response Schema Validation**
```typescript
describe('Response Schema', () => {
  it('should match expected schema', async () => {
    const response = await request(app).get('/api/users/123');

    expect(response.body).toEqual({
      id: expect.any(String),
      name: expect.any(String),
      email: expect.any(String),
      role: expect.stringMatching(/^(user|admin)$/),
      createdAt: expect.any(String),
      updatedAt: expect.any(String)
    });
  });
});
```

### 5. Error Handling Tests

```typescript
describe('Error Handling', () => {
  it('should return structured error response', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ invalid: 'data' });

    expect(response.status).toBe(400);
    expect(response.body).toEqual({
      error: expect.any(String),
      message: expect.any(String),
      errors: expect.any(Array)
    });
  });

  it('should handle database errors gracefully', async () => {
    mockDatabase.findOne.mockRejectedValue(new Error('Connection lost'));

    const response = await request(app).get('/api/users/123');

    expect(response.status).toBe(500);
    expect(response.body.error).toBe('Internal Server Error');
  });

  it('should sanitize error messages in production', async () => {
    process.env.NODE_ENV = 'production';

    const response = await request(app).get('/api/error-prone-route');

    expect(response.status).toBe(500);
    expect(response.body.message).not.toContain('stack trace');
    expect(response.body.message).not.toContain('SQL');
  });
});
```

### 6. Test Setup and Teardown

```typescript
describe('API Tests', () => {
  let testDatabase;

  beforeAll(async () => {
    // Initialize test database
    testDatabase = await initTestDatabase();
  });

  afterAll(async () => {
    // Clean up test database
    await testDatabase.close();
  });

  beforeEach(async () => {
    // Seed test data
    await testDatabase.seed();
  });

  afterEach(async () => {
    // Clear test data
    await testDatabase.clear();
  });

  // Tests...
});
```

## Framework-Specific Testing Libraries

While this skill provides framework-agnostic patterns, here are common testing libraries per framework:

- **Express**: supertest, jest, vitest
- **Next.js API Routes**: @testing-library/react, next-test-api-route-handler
- **FastAPI**: pytest, httpx
- **Django REST**: django.test.TestCase, rest_framework.test
- **Flask**: pytest, flask.testing

## Best Practices

1. **Use descriptive test names** - Test names should describe the scenario and expected outcome
2. **Test happy path and edge cases** - Cover both success and failure scenarios
3. **Isolate tests** - Each test should be independent and not rely on other tests
4. **Use realistic test data** - Test data should mimic production data
5. **Clean up after tests** - Always reset state between tests
6. **Mock external dependencies** - Don't call real external APIs in tests
7. **Test authentication edge cases** - Expired tokens, invalid tokens, missing tokens
8. **Validate response schemas** - Ensure APIs return expected structure
9. **Test rate limiting** - Verify rate limits work correctly
10. **Test CORS headers** - Ensure CORS is configured correctly

## Common Pitfalls

❌ **Don't share state between tests**
```typescript
// Bad
let userId;
it('creates user', async () => {
  const response = await request(app).post('/api/users').send(userData);
  userId = response.body.id; // Shared state!
});

it('deletes user', async () => {
  await request(app).delete(`/api/users/${userId}`); // Depends on previous test
});
```

✅ **Do create fresh state for each test**
```typescript
// Good
it('creates user', async () => {
  const response = await request(app).post('/api/users').send(userData);
  expect(response.status).toBe(201);
});

it('deletes user', async () => {
  const user = await createTestUser();
  const response = await request(app).delete(`/api/users/${user.id}`);
  expect(response.status).toBe(204);
});
```

## Additional Resources

See the `resources/` directory for more detailed guides:
- `http-testing-fundamentals.md` - Deep dive into HTTP testing concepts
- `authentication-testing.md` - Authentication strategies and edge cases
- `api-integration-testing.md` - Integration testing patterns and tools

## Quick Reference

**Test Structure**
```typescript
describe('Resource Name', () => {
  describe('HTTP Method /path', () => {
    it('should describe expected behavior', async () => {
      // Arrange
      const testData = {...};

      // Act
      const response = await request(app)
        .method('/path')
        .set('Cookie', authCookie)
        .send(testData);

      // Assert
      expect(response.status).toBe(expectedStatus);
      expect(response.body).toMatchObject(expectedData);
    });
  });
});
```

**Authentication Pattern**
```typescript
let authCookie: string;

beforeEach(async () => {
  const response = await request(app)
    .post('/api/auth/login')
    .send({ email: 'test@example.com', password: 'password123' });

  authCookie = response.headers['set-cookie'][0];
});

// Use authCookie in protected route tests
.set('Cookie', authCookie)
```
