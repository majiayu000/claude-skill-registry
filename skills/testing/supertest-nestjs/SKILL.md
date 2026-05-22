---
name: supertest-nestjs
description: >
  Supertest patterns and best practices for NestJS e2e API testing.
  Trigger: When writing e2e tests, testing HTTP endpoints, or testing authentication flows in NestJS.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Writing e2e tests, testing API endpoints, HTTP testing"
---

## When to Use

Use this skill when:
- Writing e2e tests for REST API endpoints
- Testing GraphQL mutations and queries via HTTP
- Testing authentication flows (JWT, OAuth, Basic Auth)
- Testing file upload endpoints
- Testing HTTP error responses and status codes
- Setting up request headers and authorization
- Asserting response bodies and structures
- Testing CRUD operations through controllers

---

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

### Status Code Assertions

```typescript
.expect(200)                          // Assert status code
.expect(201, { id: '123' })           // Assert status + body object
.expect(404)                          // Not found
.expect(400)                          // Bad request
.expect(401)                          // Unauthorized
.expect(403)                          // Forbidden
.expect(500)                          // Internal server error
```

### Header Manipulation

```typescript
// Set request headers
.set('Authorization', 'Bearer token')
.set('Content-Type', 'application/json')
.set('Accept', 'application/json')
.set('X-Custom-Header', 'value')

// Assert response headers
.expect('Content-Type', /json/)
.expect('Content-Type', 'application/json; charset=utf-8')
```

### Response Body Assertions

```typescript
// Exact object match
.expect({ id: '123', name: 'Test' })

// Regex match on body
.expect(/pattern/)

// Custom assertions
.expect((res) => {
    expect(res.body).toHaveProperty('id');
    expect(res.body.name).toBe('Test');
})
```

---

## Testing REST Endpoints

### 1. Testing CRUD Operations

```typescript
import * as request from 'supertest';
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import { AppModule } from '../src/app.module';

describe('Tesla Model E2E', () => {
    let app: INestApplication;
    let teslaId: string;

    beforeAll(async () => {
        const moduleFixture: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();
    });

    afterAll(async () => {
        await app.close();
    });

    describe('POST /tesla/model/create', () => {
        it('should create new tesla model', async () => {
            const response = await request(app.getHttpServer())
                .post('/tesla/model/create')
                .set('Accept', 'application/json')
                .send({
                    id: 'model-uuid-1',
                    name: 'Model S',
                    description: 'Premium sedan',
                    price: 79990,
                    isActive: true,
                })
                .expect(201)
                .expect('Content-Type', /json/);

            expect(response.body).toHaveProperty('id');
            expect(response.body.name).toBe('Model S');
            teslaId = response.body.id;
        });

        it('should return 400 when name is null', () => {
            return request(app.getHttpServer())
                .post('/tesla/model/create')
                .set('Accept', 'application/json')
                .send({
                    id: 'model-uuid-2',
                    name: null,
                    price: 79990,
                })
                .expect(400)
                .expect((res) => {
                    expect(res.body.message).toContain('name');
                    expect(res.body.message).toContain('cannot be null');
                });
        });

        it('should return 400 when price is negative', () => {
            return request(app.getHttpServer())
                .post('/tesla/model/create')
                .send({
                    id: 'model-uuid-3',
                    name: 'Model X',
                    price: -1000,
                })
                .expect(400);
        });
    });

    describe('GET /tesla/model/find/:id', () => {
        it('should return tesla model by id', () => {
            return request(app.getHttpServer())
                .get(`/tesla/model/find/${teslaId}`)
                .set('Accept', 'application/json')
                .expect(200)
                .expect((res) => {
                    expect(res.body.id).toBe(teslaId);
                    expect(res.body.name).toBe('Model S');
                });
        });

        it('should return 404 when model not found', () => {
            return request(app.getHttpServer())
                .get('/tesla/model/find/non-existent-id')
                .expect(404);
        });
    });

    describe('PUT /tesla/model/update', () => {
        it('should update tesla model', () => {
            return request(app.getHttpServer())
                .put('/tesla/model/update')
                .send({
                    id: teslaId,
                    price: 89990,
                })
                .expect(200)
                .expect((res) => {
                    expect(res.body.price).toBe(89990);
                });
        });
    });

    describe('DELETE /tesla/model/delete/:id', () => {
        it('should delete tesla model', async () => {
            await request(app.getHttpServer())
                .delete(`/tesla/model/delete/${teslaId}`)
                .expect(200);

            // Verify deletion
            return request(app.getHttpServer())
                .get(`/tesla/model/find/${teslaId}`)
                .expect(404);
        });
    });
});
```

**Key Patterns:**
- ✅ Use `beforeAll` to setup app, `afterAll` to cleanup
- ✅ Store created IDs for subsequent tests
- ✅ Test happy path first, then error cases
- ✅ Always set `Accept` header for REST endpoints
- ✅ Verify deletion by attempting to find deleted resource

---

### 2. Testing Pagination and Filtering

```typescript
describe('GET /tesla/model/paginate', () => {
    beforeAll(async () => {
        // Seed database with test data
        await repository.insert([
            { id: '1', name: 'Model S', price: 79990, isActive: true },
            { id: '2', name: 'Model 3', price: 42990, isActive: true },
            { id: '3', name: 'Model X', price: 89990, isActive: false },
            { id: '4', name: 'Model Y', price: 52990, isActive: true },
        ]);
    });

    it('should return paginated results', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/paginate')
            .query({ limit: 2, offset: 0 })
            .expect(200)
            .expect((res) => {
                expect(res.body.data).toHaveLength(2);
                expect(res.body.total).toBe(4);
                expect(res.body).toHaveProperty('count');
            });
    });

    it('should filter by active status', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/paginate')
            .query({
                query: JSON.stringify({
                    where: { isActive: true }
                })
            })
            .expect(200)
            .expect((res) => {
                expect(res.body.data).toHaveLength(3);
                expect(res.body.data.every(m => m.isActive)).toBe(true);
            });
    });

    it('should filter by price range', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/paginate')
            .query({
                query: JSON.stringify({
                    where: {
                        price: { $gte: 50000, $lte: 80000 }
                    }
                })
            })
            .expect(200)
            .expect((res) => {
                expect(res.body.data.length).toBeGreaterThan(0);
                res.body.data.forEach(model => {
                    expect(model.price).toBeGreaterThanOrEqual(50000);
                    expect(model.price).toBeLessThanOrEqual(80000);
                });
            });
    });

    it('should sort by price descending', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/paginate')
            .query({
                query: JSON.stringify({
                    order: [['price', 'DESC']]
                })
            })
            .expect(200)
            .expect((res) => {
                const prices = res.body.data.map(m => m.price);
                const sortedPrices = [...prices].sort((a, b) => b - a);
                expect(prices).toEqual(sortedPrices);
            });
    });
});
```

---

## Authentication Testing

### 1. JWT Bearer Token Authentication

```typescript
describe('Authentication - JWT', () => {
    let app: INestApplication;
    let accessToken: string;

    beforeAll(async () => {
        const moduleFixture: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();
    });

    describe('Login Flow', () => {
        it('POST /auth/login - should obtain access token', async () => {
            const response = await request(app.getHttpServer())
                .post('/auth/login')
                .send({
                    username: 'admin',
                    password: 'SecurePass123!',
                })
                .set('Content-Type', 'application/json')
                .expect(200);

            expect(response.body).toHaveProperty('access_token');
            expect(response.body).toHaveProperty('token_type', 'Bearer');
            accessToken = response.body.access_token;
        });

        it('POST /auth/login - should fail with invalid credentials', () => {
            return request(app.getHttpServer())
                .post('/auth/login')
                .send({
                    username: 'admin',
                    password: 'wrongpassword',
                })
                .expect(401)
                .expect((res) => {
                    expect(res.body.message).toContain('Unauthorized');
                });
        });

        it('POST /auth/login - should fail with missing credentials', () => {
            return request(app.getHttpServer())
                .post('/auth/login')
                .send({ username: 'admin' })
                .expect(400);
        });
    });

    describe('Protected Routes', () => {
        it('GET /profile - should access with valid token', () => {
            return request(app.getHttpServer())
                .get('/profile')
                .set('Authorization', `Bearer ${accessToken}`)
                .expect(200)
                .expect((res) => {
                    expect(res.body).toHaveProperty('userId');
                    expect(res.body.username).toBe('admin');
                });
        });

        it('GET /profile - should fail without token', () => {
            return request(app.getHttpServer())
                .get('/profile')
                .expect(401);
        });

        it('GET /profile - should fail with invalid token', () => {
            return request(app.getHttpServer())
                .get('/profile')
                .set('Authorization', 'Bearer invalid_token_here')
                .expect(401);
        });

        it('GET /profile - should fail with malformed auth header', () => {
            return request(app.getHttpServer())
                .get('/profile')
                .set('Authorization', accessToken) // Missing "Bearer"
                .expect(401);
        });
    });

    describe('Token Refresh', () => {
        let refreshToken: string;

        it('POST /auth/refresh - should refresh access token', async () => {
            // Assume login returns refresh token
            const loginRes = await request(app.getHttpServer())
                .post('/auth/login')
                .send({ username: 'admin', password: 'SecurePass123!' });

            refreshToken = loginRes.body.refresh_token;

            const response = await request(app.getHttpServer())
                .post('/auth/refresh')
                .send({ refresh_token: refreshToken })
                .expect(200);

            expect(response.body).toHaveProperty('access_token');
            expect(response.body.access_token).not.toBe(accessToken);
        });
    });

    afterAll(async () => {
        await app.close();
    });
});
```

### 2. API Key Authentication

```typescript
describe('Authentication - API Key', () => {
    const validApiKey = 'sk_test_1234567890abcdef';

    it('GET /api/data - with valid API key in header', () => {
        return request(app.getHttpServer())
            .get('/api/data')
            .set('X-API-Key', validApiKey)
            .expect(200);
    });

    it('GET /api/data - with valid API key in query', () => {
        return request(app.getHttpServer())
            .get('/api/data')
            .query({ api_key: validApiKey })
            .expect(200);
    });

    it('GET /api/data - without API key should fail', () => {
        return request(app.getHttpServer())
            .get('/api/data')
            .expect(401);
    });

    it('GET /api/data - with invalid API key should fail', () => {
        return request(app.getHttpServer())
            .get('/api/data')
            .set('X-API-Key', 'invalid_key')
            .expect(401);
    });
});
```

---

## Testing GraphQL

### GraphQL Mutations and Queries

```typescript
describe('Tesla GraphQL E2E', () => {
    let app: INestApplication;

    beforeAll(async () => {
        const moduleFixture: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();
    });

    describe('Mutations', () => {
        it('createTeslaModel - should create new model', () => {
            const mutation = `
                mutation {
                    createTeslaModel(input: {
                        name: "Cybertruck"
                        description: "Futuristic pickup truck"
                        price: 79990
                        isActive: true
                    }) {
                        id
                        name
                        price
                        createdAt
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query: mutation })
                .set('Accept', 'application/json')
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.createTeslaModel).toHaveProperty('id');
                    expect(res.body.data.createTeslaModel.name).toBe('Cybertruck');
                    expect(res.body.errors).toBeUndefined();
                });
        });

        it('createTeslaModel - should return error for invalid data', () => {
            const mutation = `
                mutation {
                    createTeslaModel(input: {
                        name: null
                        price: -100
                    }) {
                        id
                        name
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query: mutation })
                .expect(200)
                .expect((res) => {
                    expect(res.body.errors).toBeDefined();
                    expect(res.body.errors[0].message).toContain('validation');
                });
        });

        it('updateTeslaModel - should update existing model', async () => {
            // Create first
            const createMutation = `
                mutation {
                    createTeslaModel(input: {
                        name: "Roadster"
                        price: 200000
                        isActive: true
                    }) {
                        id
                    }
                }
            `;

            const createRes = await request(app.getHttpServer())
                .post('/graphql')
                .send({ query: createMutation });

            const modelId = createRes.body.data.createTeslaModel.id;

            // Update
            const updateMutation = `
                mutation {
                    updateTeslaModel(input: {
                        id: "${modelId}"
                        price: 250000
                    }) {
                        id
                        price
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query: updateMutation })
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.updateTeslaModel.price).toBe(250000);
                });
        });
    });

    describe('Queries', () => {
        let teslaId: string;

        beforeEach(async () => {
            // Seed data
            const mutation = `
                mutation {
                    createTeslaModel(input: {
                        name: "Model 3"
                        price: 42990
                        isActive: true
                    }) {
                        id
                    }
                }
            `;

            const res = await request(app.getHttpServer())
                .post('/graphql')
                .send({ query: mutation });

            teslaId = res.body.data.createTeslaModel.id;
        });

        it('findTeslaModelById - should return model by id', () => {
            const query = `
                query {
                    findTeslaModelById(id: "${teslaId}") {
                        id
                        name
                        price
                        isActive
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query })
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.findTeslaModelById.id).toBe(teslaId);
                    expect(res.body.data.findTeslaModelById.name).toBe('Model 3');
                });
        });

        it('paginateTeslaModels - should return paginated results', () => {
            const query = `
                query {
                    paginateTeslaModels(limit: 10, offset: 0) {
                        data {
                            id
                            name
                        }
                        total
                        count
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query })
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.paginateTeslaModels).toHaveProperty('data');
                    expect(res.body.data.paginateTeslaModels).toHaveProperty('total');
                    expect(Array.isArray(res.body.data.paginateTeslaModels.data)).toBe(true);
                });
        });

        it('findTeslaModels - with filters', () => {
            const query = `
                query {
                    findTeslaModels(where: { isActive: true }) {
                        id
                        name
                        isActive
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query })
                .expect(200)
                .expect((res) => {
                    const models = res.body.data.findTeslaModels;
                    expect(models.every(m => m.isActive)).toBe(true);
                });
        });
    });

    afterAll(async () => {
        await app.close();
    });
});
```

---

## File Upload Testing

```typescript
import * as path from 'path';

describe('File Upload E2E', () => {
    let app: INestApplication;

    beforeAll(async () => {
        const moduleFixture: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
        }).compile();

        app = moduleFixture.createNestApplication();
        await app.init();
    });

    describe('POST /upload/single', () => {
        it('should upload single file successfully', async () => {
            const response = await request(app.getHttpServer())
                .post('/upload/single')
                .field('title', 'Product Image')
                .field('category', 'products')
                .attach('file', path.join(__dirname, 'fixtures/image.jpg'))
                .expect(201);

            expect(response.body).toHaveProperty('fileId');
            expect(response.body).toHaveProperty('filename');
            expect(response.body.filename).toContain('.jpg');
            expect(response.body).toHaveProperty('size');
        });

        it('should fail when file is missing', () => {
            return request(app.getHttpServer())
                .post('/upload/single')
                .field('title', 'Product Image')
                .expect(400)
                .expect((res) => {
                    expect(res.body.message).toContain('file');
                });
        });

        it('should fail when file type is invalid', () => {
            return request(app.getHttpServer())
                .post('/upload/single')
                .attach('file', path.join(__dirname, 'fixtures/malware.exe'))
                .expect(400)
                .expect((res) => {
                    expect(res.body.message).toContain('file type');
                });
        });

        it('should fail when file is too large', () => {
            return request(app.getHttpServer())
                .post('/upload/single')
                .attach('file', path.join(__dirname, 'fixtures/large-file.bin'))
                .expect(413)
                .expect((res) => {
                    expect(res.body.message).toContain('size');
                });
        });
    });

    describe('POST /upload/multiple', () => {
        it('should upload multiple files', async () => {
            const response = await request(app.getHttpServer())
                .post('/upload/multiple')
                .field('title', 'Product Gallery')
                .attach('files', path.join(__dirname, 'fixtures/image1.jpg'))
                .attach('files', path.join(__dirname, 'fixtures/image2.jpg'))
                .attach('files', path.join(__dirname, 'fixtures/image3.jpg'))
                .expect(201);

            expect(response.body.uploadedFiles).toHaveLength(3);
            expect(response.body.uploadedFiles[0]).toHaveProperty('fileId');
        });
    });

    describe('POST /upload/with-metadata', () => {
        it('should upload file with JSON metadata', () => {
            const metadata = {
                category: 'documentation',
                tags: ['important', 'legal'],
                expiresAt: '2025-12-31',
            };

            return request(app.getHttpServer())
                .post('/upload/with-metadata')
                .field('metadata', JSON.stringify(metadata), {
                    contentType: 'application/json',
                })
                .attach('file', path.join(__dirname, 'fixtures/document.pdf'))
                .expect(201)
                .expect((res) => {
                    expect(res.body.metadata).toEqual(metadata);
                });
        });
    });

    afterAll(async () => {
        await app.close();
    });
});
```

---

## Advanced Patterns

### 1. Testing with Database Seeding

```typescript
describe('Tesla E2E with Seeding', () => {
    let app: INestApplication;
    let repository: TeslaIModelRepository;
    let seeder: TeslaMockModelSeeder;

    beforeAll(async () => {
        const module: TestingModule = await Test.createTestingModule({
            imports: [AppModule],
            providers: [TeslaMockModelSeeder],
        }).compile();

        app = module.createNestApplication();
        repository = module.get<TeslaIModelRepository>(TeslaIModelRepository);
        seeder = module.get<TeslaMockModelSeeder>(TeslaMockModelSeeder);

        // Seed database with mock data
        await repository.insert(seeder.collectionSource);

        await app.init();
    });

    it('should find seeded data', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/paginate')
            .expect(200)
            .expect((res) => {
                expect(res.body.data.length).toBeGreaterThan(0);
            });
    });

    afterAll(async () => {
        await app.close();
    });
});
```

### 2. Testing with Custom Test Database

```typescript
beforeAll(async () => {
    const module: TestingModule = await Test.createTestingModule({
        imports: [
            TeslaModule,
            SequelizeModule.forRootAsync({
                imports: [ConfigModule],
                inject: [ConfigService],
                useFactory: (configService: ConfigService) => ({
                    dialect: 'sqlite',
                    storage: ':memory:',
                    logging: false,
                    synchronize: true,
                    autoLoadModels: true,
                }),
            }),
        ],
    }).compile();

    app = module.createNestApplication();
    await app.init();
});
```

### 3. Testing Error Responses

```typescript
describe('Error Handling', () => {
    it('should return 400 for validation errors', () => {
        return request(app.getHttpServer())
            .post('/tesla/model/create')
            .send({ name: '' })
            .expect(400)
            .expect((res) => {
                expect(res.body).toHaveProperty('statusCode', 400);
                expect(res.body).toHaveProperty('message');
                expect(Array.isArray(res.body.message)).toBe(true);
            });
    });

    it('should return 404 for non-existent resource', () => {
        return request(app.getHttpServer())
            .get('/tesla/model/find/non-existent-id')
            .expect(404)
            .expect((res) => {
                expect(res.body.message).toContain('not found');
            });
    });

    it('should return 409 for duplicate entry', () => {
        return request(app.getHttpServer())
            .post('/tesla/model/create')
            .send({
                id: 'duplicate-id',
                name: 'Model S',
            })
            .expect(409);
    });

    it('should return 500 for internal errors', () => {
        return request(app.getHttpServer())
            .post('/tesla/model/trigger-error')
            .expect(500);
    });
});
```

---

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
10. **Don't commit test files**: Add large fixtures to `.gitignore`

---

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

---

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

---

## Remember

- **e2e tests** test the full request/response cycle
- **Use real database** or in-memory for integration
- **Supertest** wraps your NestJS app HTTP server
- **Test authentication flows** completely (login → use token → logout)
- **Verify both success and failure** scenarios
- **Keep tests fast**: Optimize database operations
- **Run e2e separately**: `npm run test:e2e`
