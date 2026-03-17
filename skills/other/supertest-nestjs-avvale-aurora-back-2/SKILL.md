---
name: supertest-nestjs
description: >
  Supertest patterns and best practices for NestJS e2e API testing.
  Trigger: When writing e2e tests, testing HTTP endpoints, or testing authentication flows in NestJS.
license: MIT
metadata:
  author: aurora
  version: "1.1"
  auto_invoke: "Writing e2e tests, testing API endpoints, HTTP testing"
---

## When to Use

Use this skill when:
- Writing e2e tests for REST API endpoints
- Testing GraphQL mutations and queries via HTTP
- Testing authentication flows (JWT, OAuth, Basic Auth)
- Testing file upload endpoints
- Testing HTTP error responses and status codes

## Core Supertest API

### Basic Request Structure

```typescript
import * as request from 'supertest';

// Basic GET request
request(app.getHttpServer())
    .get('/endpoint')
    .expect(200);

// POST with body
request(app.getHttpServer())
    .post('/endpoint')
    .send({ data: 'value' })
    .expect(201);
```

### Header Manipulation

```typescript
// Set request headers
.set('Authorization', 'Bearer token')
.set('Content-Type', 'application/json')
.set('Accept', 'application/json')

// Assert response headers
.expect('Content-Type', /json/)
```

### Response Body Assertions

```typescript
// Custom assertions
.expect((res) => {
    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toBe('Test');
})
```

## Detailed References

- [REST CRUD & Pagination Testing](rest-crud.md) — CRUD operations, pagination, filtering, sorting
- [Authentication Testing](auth-testing.md) — JWT, API Key, protected routes, token refresh
- [GraphQL Testing](graphql-testing.md) — Mutations, queries, error handling
- [Advanced Patterns](advanced-patterns.md) — File upload, DB seeding, custom test DB, error responses

## Best Practices

### ✅ DO

1. **Use async/await**: Modern pattern, cleaner than callbacks
2. **Set headers explicitly**: Always set `Accept` and `Content-Type`
3. **Test error paths**: Not just happy paths
4. **Verify status codes**: Always assert expected HTTP status
5. **Assert response structure**: Check all important fields
6. **Clean up resources**: Use `afterAll` to close app
7. **Use fixtures**: Store test files in `test/fixtures/`
8. **Seed data properly**: Use seeders for consistent data
9. **Test authentication**: Both success and failure scenarios
10. **Use descriptive test names**: "should create model when data is valid"

### ❌ DON'T

1. **Don't skip status assertions**: Always use `.expect(statusCode)`
2. **Don't test implementation**: Test API contracts, not internals
3. **Don't share state**: Each test should be independent
4. **Don't hardcode IDs**: Generate or capture from responses
5. **Don't ignore error messages**: Assert error content, not just status
6. **Don't forget cleanup**: Close app in `afterAll`
7. **Don't mix unit and e2e**: Keep them separate
8. **Don't test generated endpoints**: Focus on custom logic
9. **Don't use production DB**: Use test database or in-memory

## Quick Reference

| Task | Pattern |
|------|---------|
| Basic GET | `request(server).get('/path').expect(200)` |
| POST with body | `.post('/path').send({ data }).expect(201)` |
| Set auth header | `.set('Authorization', 'Bearer token')` |
| Upload file | `.attach('file', filepath)` |
| Assert response | `.expect((res) => { expect(res.body)... })` |
| Test GraphQL | `.post('/graphql').send({ query })` |
| Chain requests | Store response, use in next request |
| Test pagination | `.query({ limit: 10, offset: 0 })` |

## Common HTTP Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE (no body) |
| 400 | Bad Request | Validation errors |
| 401 | Unauthorized | Missing or invalid auth |
| 403 | Forbidden | Valid auth but no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate entry |
| 422 | Unprocessable Entity | Semantic validation error |
| 500 | Internal Server Error | Server exception |

## Remember

- **e2e tests** test the full request/response cycle
- **Use real database** or in-memory for integration
- **Supertest** wraps your NestJS app HTTP server
- **Test authentication flows** completely (login → use token → logout)
- **Verify both success and failure** scenarios
- **Keep tests fast**: Optimize database operations
- **Run e2e separately**: `npm run test:e2e`
