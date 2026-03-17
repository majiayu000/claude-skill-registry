---
name: api-testing
description: HTTP API testing for TypeScript (Supertest) and Python (httpx, pytest). Test REST APIs, GraphQL, request/response validation, authentication, and error handling.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, TodoWrite
---

# API Testing

Expert knowledge for testing HTTP APIs with Supertest (TypeScript/JavaScript) and httpx/pytest (Python).

## TypeScript/JavaScript (Supertest)

### Installation

```bash
# Using Bun
bun add -d supertest @types/supertest

# or: npm install -D supertest @types/supertest
```

### Basic Setup

```typescript
import { describe, it, expect } from 'vitest'
import request from 'supertest'
import { app } from './app'

describe('API Tests', () => {
  it('returns health status', async () => {
    const response = await request(app)
      .get('/api/health')
      .expect(200)

    expect(response.body).toEqual({ status: 'ok' })
  })

  it('creates a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John Doe', email: 'john@example.com' })
      .expect(201)

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      name: 'John Doe',
    })
  })

  it('validates required fields', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'John Doe' })
      .expect(400)
  })
})
```

### Request Methods

```typescript
// GET
await request(app).get('/api/users').expect(200)

// POST with body
await request(app)
  .post('/api/users')
  .send({ name: 'John' })
  .expect(201)

// PUT
await request(app)
  .put('/api/users/1')
  .send({ name: 'Jane' })
  .expect(200)

// DELETE
await request(app).delete('/api/users/1').expect(204)
```

### Headers and Query Parameters

```typescript
// Set headers
await request(app)
  .get('/api/protected')
  .set('Authorization', 'Bearer token123')
  .expect(200)

// Query parameters
await request(app)
  .get('/api/users')
  .query({ page: 1, limit: 10 })
  .expect(200)
```

### Authentication Testing

```typescript
describe('Authentication', () => {
  let authToken: string

  beforeAll(async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'user@example.com', password: 'password123' })
      .expect(200)

    authToken = response.body.token
  })

  it('accesses protected endpoint', async () => {
    await request(app)
      .get('/api/protected')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200)
  })

  it('rejects without token', async () => {
    await request(app).get('/api/protected').expect(401)
  })
})
```

### Error Handling

```typescript
it('handles validation errors', async () => {
  const response = await request(app)
    .post('/api/users')
    .send({ email: 'invalid-email' })
    .expect(400)

  expect(response.body).toMatchObject({
    error: 'Validation failed',
    details: expect.any(Array),
  })
})

it('handles not found', async () => {
  await request(app).get('/api/users/999999').expect(404)
})
```

## Python (httpx + pytest)

### Installation

```bash
uv add --dev httpx pytest-asyncio
```

### Basic Setup

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_user():
    response = client.post(
        "/api/users",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data

def test_not_found():
    response = client.get("/api/users/999")
    assert response.status_code == 404
```

### Fixtures

```python
@pytest.fixture
def auth_token(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "password123"}
    )
    return response.json()["token"]

def test_protected_endpoint(client, auth_token):
    response = client.get(
        "/api/protected",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
```

### File Upload

```python
def test_file_upload(client, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    with open(test_file, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert response.status_code == 200
```

## GraphQL Testing

```typescript
it('queries GraphQL endpoint', async () => {
  const query = `
    query GetUser($id: ID!) {
      user(id: $id) { id name email }
    }
  `

  const response = await request(app)
    .post('/graphql')
    .send({ query, variables: { id: '1' } })
    .expect(200)

  expect(response.body.data.user).toMatchObject({
    id: '1',
    name: expect.any(String),
  })
})
```

## Performance Testing

```typescript
it('responds within acceptable time', async () => {
  const start = Date.now()
  await request(app).get('/api/users').expect(200)
  const duration = Date.now() - start
  expect(duration).toBeLessThan(100) // 100ms threshold
})
```

## Best Practices

- Group related endpoints in `describe` blocks
- Reset database between tests
- Validate status codes first
- Check response structure
- Test error message format
- Mock external services
- Test both happy path and error cases

## See Also

- `vitest-testing` - Unit testing framework
- `playwright-testing` - E2E API testing
- `test-quality-analysis` - Test quality patterns
