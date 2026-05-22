---
name: jest-nestjs
description: >
  Jest + NestJS testing patterns for unit and e2e tests in Aurora projects.
  Trigger: When writing tests, mocking dependencies, or implementing test coverage in NestJS/Aurora.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Writing tests, mocking services, testing handlers"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

Use this skill when:
- Writing unit tests for handlers, services, or aggregates
- Creating e2e tests for API endpoints
- Mocking NestJS dependencies (repositories, services, event bus)
- Testing CQRS commands and queries
- Testing Aurora-generated code
- Setting up test fixtures and factories
- Implementing test coverage strategies

## Testing Philosophy in Aurora/NestJS

**Unit Tests**: Test individual components in isolation
- Handlers (Command/Query)
- Services
- Aggregates and Value Objects
- Mappers

**e2e Tests**: Test complete flows through the API layer
- REST endpoints (Controllers)
- GraphQL resolvers
- Authentication/Authorization
- Database interactions

---

## Unit Testing Patterns

### 1. Testing Command Handlers

**Goal**: Verify business logic, validations, and repository interactions.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { EventPublisher } from '@nestjs/cqrs';
import { CreateTeslaCommandHandler } from './create-tesla.command-handler';
import { CreateTeslaCommand } from './create-tesla.command';
import { ITeslaRepository } from '../../domain/tesla.repository';
import { TeslaMockRepository } from '../../infrastructure/mock/tesla.mock-repository';

describe('CreateTeslaCommandHandler', () => {
    let handler: CreateTeslaCommandHandler;
    let repository: ITeslaRepository;
    let publisher: EventPublisher;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [
                CreateTeslaCommandHandler,
                {
                    provide: ITeslaRepository,
                    useClass: TeslaMockRepository,
                },
                {
                    provide: EventPublisher,
                    useValue: {
                        mergeObjectContext: jest.fn().mockReturnValue({
                            commit: jest.fn(),
                        }),
                    },
                },
            ],
        }).compile();

        handler = module.get<CreateTeslaCommandHandler>(CreateTeslaCommandHandler);
        repository = module.get<ITeslaRepository>(ITeslaRepository);
        publisher = module.get<EventPublisher>(EventPublisher);
    });

    describe('execute', () => {
        it('should create tesla with valid data', async () => {
            // Arrange
            const command = new CreateTeslaCommand({
                payload: {
                    id: 'tesla-uuid',
                    model: 'Model S',
                    year: 2023,
                    price: 79990,
                    isActive: true,
                },
            });

            const createSpy = jest.spyOn(repository, 'create');

            // Act
            await handler.execute(command);

            // Assert
            expect(createSpy).toHaveBeenCalledTimes(1);
            expect(createSpy).toHaveBeenCalledWith(
                expect.objectContaining({
                    id: expect.any(Object),
                    model: expect.any(Object),
                    year: expect.any(Object),
                }),
            );
        });

        it('should throw exception when price is invalid', async () => {
            // Arrange
            const command = new CreateTeslaCommand({
                payload: {
                    id: 'tesla-uuid',
                    model: 'Model S',
                    year: 2023,
                    price: -100, // Invalid price
                    isActive: true,
                },
            });

            // Act & Assert
            await expect(handler.execute(command)).rejects.toThrow(
                'Price must be greater than 0',
            );
        });

        it('should throw exception when year is before 2008', async () => {
            // Arrange
            const command = new CreateTeslaCommand({
                payload: {
                    id: 'tesla-uuid',
                    model: 'Roadster',
                    year: 2005, // Before Tesla first car
                    price: 109000,
                    isActive: true,
                },
            });

            // Act & Assert
            await expect(handler.execute(command)).rejects.toThrow(
                'Tesla first car (Roadster) was released in 2008',
            );
        });
    });
});
```

**Key Patterns:**
- ✅ Use `Test.createTestingModule()` for DI container
- ✅ Mock repositories with interfaces (`ITeslaRepository`)
- ✅ Mock EventPublisher for CQRS events
- ✅ Test happy path + edge cases + error paths
- ✅ Use descriptive test names: "should [expected behavior] when [condition]"
- ✅ Follow AAA pattern: Arrange, Act, Assert

---

### 2. Testing Query Handlers

**Goal**: Verify data retrieval and filtering logic.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { FindTeslaByIdQueryHandler } from './find-tesla-by-id.query-handler';
import { FindTeslaByIdQuery } from './find-tesla-by-id.query';
import { ITeslaRepository } from '../../domain/tesla.repository';
import { TeslaMockRepository } from '../../infrastructure/mock/tesla.mock-repository';
import { Tesla } from '../../domain/tesla.aggregate';

describe('FindTeslaByIdQueryHandler', () => {
    let handler: FindTeslaByIdQueryHandler;
    let repository: ITeslaRepository;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [
                FindTeslaByIdQueryHandler,
                {
                    provide: ITeslaRepository,
                    useClass: TeslaMockRepository,
                },
            ],
        }).compile();

        handler = module.get<FindTeslaByIdQueryHandler>(FindTeslaByIdQueryHandler);
        repository = module.get<ITeslaRepository>(ITeslaRepository);
    });

    it('should return tesla when found', async () => {
        // Arrange
        const teslaMock = Tesla.register({
            id: 'tesla-uuid',
            model: 'Model 3',
            year: 2023,
            price: 42990,
            isActive: true,
        });

        jest.spyOn(repository, 'findById').mockResolvedValue(teslaMock);

        const query = new FindTeslaByIdQuery({ id: 'tesla-uuid' });

        // Act
        const result = await handler.execute(query);

        // Assert
        expect(result).toBe(teslaMock);
        expect(repository.findById).toHaveBeenCalledWith('tesla-uuid');
    });

    it('should return null when not found', async () => {
        // Arrange
        jest.spyOn(repository, 'findById').mockResolvedValue(null);
        const query = new FindTeslaByIdQuery({ id: 'non-existent-uuid' });

        // Act
        const result = await handler.execute(query);

        // Assert
        expect(result).toBeNull();
    });
});
```

---

### 3. Mocking Repositories

**Create Mock Repositories** for testing without database:

```typescript
// src/@core/tesla/infrastructure/mock/tesla.mock-repository.ts
import { Injectable } from '@nestjs/common';
import { ITeslaRepository } from '../../domain/tesla.repository';
import { Tesla } from '../../domain/tesla.aggregate';
import { TeslaId } from '../../domain/value-objects';

@Injectable()
export class TeslaMockRepository implements ITeslaRepository {
    private teslas: Tesla[] = [];

    async create(tesla: Tesla): Promise<void> {
        this.teslas.push(tesla);
    }

    async findById(id: TeslaId): Promise<Tesla | null> {
        return this.teslas.find(t => t.id.value === id.value) || null;
    }

    async update(tesla: Tesla): Promise<void> {
        const index = this.teslas.findIndex(t => t.id.value === tesla.id.value);
        if (index !== -1) {
            this.teslas[index] = tesla;
        }
    }

    async delete(id: TeslaId): Promise<void> {
        this.teslas = this.teslas.filter(t => t.id.value !== id.value);
    }

    async find(query: any): Promise<Tesla[]> {
        return this.teslas;
    }

    // Implement all ITeslaRepository methods...
}
```

**Why Mock Repositories?**
- ✅ Faster tests (no DB connection)
- ✅ Deterministic (no external state)
- ✅ Isolated (test only handler logic)

---

### 4. Mocking External Services

```typescript
describe('CreateOrderCommandHandler', () => {
    let handler: CreateOrderCommandHandler;
    let paymentService: PaymentService;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [
                CreateOrderCommandHandler,
                {
                    provide: PaymentService,
                    useValue: {
                        processPayment: jest.fn(),
                        refund: jest.fn(),
                    },
                },
            ],
        }).compile();

        handler = module.get(CreateOrderCommandHandler);
        paymentService = module.get(PaymentService);
    });

    it('should process payment when creating order', async () => {
        // Arrange
        const command = new CreateOrderCommand({ amount: 1000 });
        jest.spyOn(paymentService, 'processPayment').mockResolvedValue({
            transactionId: 'txn-123',
            status: 'success',
        });

        // Act
        await handler.execute(command);

        // Assert
        expect(paymentService.processPayment).toHaveBeenCalledWith({
            amount: 1000,
        });
    });

    it('should handle payment failure', async () => {
        // Arrange
        const command = new CreateOrderCommand({ amount: 1000 });
        jest.spyOn(paymentService, 'processPayment').mockRejectedValue(
            new Error('Payment declined'),
        );

        // Act & Assert
        await expect(handler.execute(command)).rejects.toThrow('Payment declined');
    });
});
```

---

## e2e Testing Patterns

### 1. Testing REST Controllers

**Goal**: Test complete request/response cycle through controllers.

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../../../app.module';

describe('TeslaController (e2e)', () => {
    let app: INestApplication;

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

    describe('POST /tesla', () => {
        it('should create new tesla', () => {
            return request(app.getHttpServer())
                .post('/tesla')
                .send({
                    model: 'Model Y',
                    year: 2023,
                    price: 52990,
                    isActive: true,
                })
                .expect(201)
                .expect((res) => {
                    expect(res.body).toHaveProperty('id');
                    expect(res.body.model).toBe('Model Y');
                });
        });

        it('should return 400 when validation fails', () => {
            return request(app.getHttpServer())
                .post('/tesla')
                .send({
                    model: '', // Invalid: empty model
                    year: 2023,
                    price: 52990,
                })
                .expect(400)
                .expect((res) => {
                    expect(res.body.message).toContain('model');
                });
        });
    });

    describe('GET /tesla/:id', () => {
        it('should return tesla by id', async () => {
            // Arrange: Create tesla first
            const createRes = await request(app.getHttpServer())
                .post('/tesla')
                .send({
                    model: 'Cybertruck',
                    year: 2024,
                    price: 79990,
                    isActive: true,
                });

            const teslaId = createRes.body.id;

            // Act & Assert
            return request(app.getHttpServer())
                .get(`/tesla/${teslaId}`)
                .expect(200)
                .expect((res) => {
                    expect(res.body.id).toBe(teslaId);
                    expect(res.body.model).toBe('Cybertruck');
                });
        });

        it('should return 404 when not found', () => {
            return request(app.getHttpServer())
                .get('/tesla/non-existent-id')
                .expect(404);
        });
    });

    describe('PUT /tesla/:id', () => {
        it('should update tesla', async () => {
            // Arrange: Create tesla
            const createRes = await request(app.getHttpServer())
                .post('/tesla')
                .send({
                    model: 'Roadster',
                    year: 2025,
                    price: 200000,
                    isActive: true,
                });

            const teslaId = createRes.body.id;

            // Act & Assert
            return request(app.getHttpServer())
                .put(`/tesla/${teslaId}`)
                .send({
                    price: 250000, // Updated price
                })
                .expect(200)
                .expect((res) => {
                    expect(res.body.price).toBe(250000);
                });
        });
    });

    describe('DELETE /tesla/:id', () => {
        it('should delete tesla', async () => {
            // Arrange: Create tesla
            const createRes = await request(app.getHttpServer())
                .post('/tesla')
                .send({
                    model: 'Model X',
                    year: 2023,
                    price: 79990,
                    isActive: true,
                });

            const teslaId = createRes.body.id;

            // Act: Delete
            await request(app.getHttpServer())
                .delete(`/tesla/${teslaId}`)
                .expect(200);

            // Assert: Verify deleted
            return request(app.getHttpServer())
                .get(`/tesla/${teslaId}`)
                .expect(404);
        });
    });
});
```

**Key Patterns:**
- ✅ Use `supertest` for HTTP testing
- ✅ Import full `AppModule` for real integration
- ✅ Setup/teardown with `beforeAll`/`afterAll`
- ✅ Test CRUD operations
- ✅ Test validation errors (400)
- ✅ Test not found cases (404)
- ✅ Create fixtures in `beforeEach` when needed

---

### 2. Testing GraphQL Resolvers

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../../../app.module';

describe('TeslaResolver (e2e)', () => {
    let app: INestApplication;

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

    describe('createTesla mutation', () => {
        it('should create tesla via GraphQL', () => {
            const mutation = `
                mutation {
                    createTesla(input: {
                        model: "Model S Plaid"
                        year: 2023
                        price: 129990
                        isActive: true
                    }) {
                        id
                        model
                        year
                        price
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query: mutation })
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.createTesla).toHaveProperty('id');
                    expect(res.body.data.createTesla.model).toBe('Model S Plaid');
                });
        });
    });

    describe('findTeslaById query', () => {
        it('should find tesla by id', async () => {
            // Arrange: Create tesla first
            const createMutation = `
                mutation {
                    createTesla(input: {
                        model: "Model 3 Performance"
                        year: 2023
                        price: 53990
                        isActive: true
                    }) {
                        id
                    }
                }
            `;

            const createRes = await request(app.getHttpServer())
                .post('/graphql')
                .send({ query: createMutation });

            const teslaId = createRes.body.data.createTesla.id;

            // Act: Query by ID
            const query = `
                query {
                    findTeslaById(id: "${teslaId}") {
                        id
                        model
                        year
                        price
                    }
                }
            `;

            return request(app.getHttpServer())
                .post('/graphql')
                .send({ query })
                .expect(200)
                .expect((res) => {
                    expect(res.body.data.findTeslaById.id).toBe(teslaId);
                    expect(res.body.data.findTeslaById.model).toBe('Model 3 Performance');
                });
        });
    });
});
```

---

## Testing Aurora-Specific Patterns

### 1. Testing Value Objects

```typescript
import { TeslaYear } from './tesla-year.value-object';

describe('TeslaYear', () => {
    it('should create valid year', () => {
        const year = new TeslaYear(2023);
        expect(year.value).toBe(2023);
    });

    it('should throw when year is before 2008', () => {
        expect(() => new TeslaYear(2005)).toThrow(
            'Tesla first car was released in 2008',
        );
    });

    it('should throw when year is in future', () => {
        const futureYear = new Date().getFullYear() + 5;
        expect(() => new TeslaYear(futureYear)).toThrow(
            'Year cannot be in the future',
        );
    });
});
```

### 2. Testing Aggregates

```typescript
import { Tesla } from './tesla.aggregate';
import { TeslaCreatedEvent } from './events/tesla-created.event';

describe('Tesla Aggregate', () => {
    describe('register', () => {
        it('should create new tesla and emit TeslaCreatedEvent', () => {
            // Act
            const tesla = Tesla.register({
                id: 'tesla-uuid',
                model: 'Model S',
                year: 2023,
                price: 79990,
                isActive: true,
            });

            // Assert
            expect(tesla.id.value).toBe('tesla-uuid');
            expect(tesla.model.value).toBe('Model S');
            expect(tesla.getUncommittedEvents()).toHaveLength(1);
            expect(tesla.getUncommittedEvents()[0]).toBeInstanceOf(TeslaCreatedEvent);
        });
    });

    describe('update', () => {
        it('should update tesla and emit TeslaUpdatedEvent', () => {
            // Arrange
            const tesla = Tesla.register({
                id: 'tesla-uuid',
                model: 'Model S',
                year: 2023,
                price: 79990,
                isActive: true,
            });

            tesla.commit(); // Clear events

            // Act
            tesla.update({
                price: 89990,
            });

            // Assert
            expect(tesla.price.value).toBe(89990);
            expect(tesla.getUncommittedEvents()).toHaveLength(1);
        });
    });
});
```

---

## Test Organization

### Directory Structure

```
src/@core/tesla/
├── application/
│   ├── commands/
│   │   ├── create-tesla.command-handler.spec.ts
│   │   └── update-tesla.command-handler.spec.ts
│   └── queries/
│       ├── find-tesla-by-id.query-handler.spec.ts
│       └── paginate-teslas.query-handler.spec.ts
├── domain/
│   ├── tesla.aggregate.spec.ts
│   └── value-objects/
│       ├── tesla-year.spec.ts
│       └── tesla-price.spec.ts
└── infrastructure/
    └── mock/
        └── tesla.mock-repository.ts

test/
└── e2e/
    ├── tesla/
    │   ├── tesla.controller.e2e-spec.ts
    │   └── tesla.resolver.e2e-spec.ts
    └── fixtures/
        └── tesla.fixtures.ts
```

---

## Best Practices

### ✅ DO

1. **Isolate tests**: Each test should be independent
2. **Use descriptive names**: "should throw error when price is negative"
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Mock external dependencies**: Database, APIs, services
5. **Test edge cases**: Null, undefined, empty arrays, boundaries
6. **Test error paths**: Exceptions, validation errors
7. **Use factories/fixtures**: Reusable test data builders
8. **Keep tests fast**: Unit tests < 100ms, e2e < 1s
9. **Clean up**: Use `afterEach` to reset state
10. **Test one thing**: One assertion per test (when possible)

### ❌ DON'T

1. **Don't test implementation details**: Test behavior, not internals
2. **Don't test framework code**: Trust NestJS, TypeORM, etc.
3. **Don't share state**: Between tests or describe blocks
4. **Don't use real database**: In unit tests (use mocks)
5. **Don't skip tests**: Fix or remove broken tests
6. **Don't test getters/setters**: Unless they have logic
7. **Don't mock everything**: Sometimes real objects are better
8. **Don't duplicate tests**: Avoid redundant test cases
9. **Don't test generated code**: Trust Aurora generation (test custom logic only)
10. **Don't ignore coverage**: Aim for >80% on custom code

---

## Coverage Guidelines

**Target Coverage:**
- Custom handlers: 100% (all custom logic)
- Services: 90%+ (critical business logic)
- Aggregates: 90%+ (domain rules)
- Value Objects: 80%+ (validation logic)
- Controllers/Resolvers: 80%+ (e2e coverage acceptable)
- Generated code: Skip (trust Aurora)

**Run Coverage:**
```bash
# Unit tests with coverage
npm run test:cov

# e2e tests
npm run test:e2e

# Watch mode for TDD
npm run test:watch
```

---

## Common Mocking Patterns

### EventBus Mock

```typescript
{
    provide: EventBus,
    useValue: {
        publish: jest.fn(),
    },
}
```

### QueryBus Mock

```typescript
{
    provide: QueryBus,
    useValue: {
        execute: jest.fn(),
    },
}
```

### CommandBus Mock

```typescript
{
    provide: CommandBus,
    useValue: {
        execute: jest.fn(),
    },
}
```

---

## Jest Configuration

**jest.config.js** (typical Aurora setup):

```javascript
module.exports = {
    moduleFileExtensions: ['js', 'json', 'ts'],
    rootDir: 'src',
    testRegex: '.*\\.spec\\.ts$',
    transform: {
        '^.+\\.(t|j)s$': 'ts-jest',
    },
    collectCoverageFrom: [
        '**/*.(t|j)s',
        '!**/*.module.ts',
        '!**/*.index.ts',
        '!**/node_modules/**',
        '!**/dist/**',
        '!**/infrastructure/seeds/**',
    ],
    coverageDirectory: '../coverage',
    testEnvironment: 'node',
    moduleNameMapper: {
        '^@app/(.*)$': '<rootDir>/$1',
        '^@core/(.*)$': '<rootDir>/@core/$1',
        '^@api/(.*)$': '<rootDir>/@api/$1',
    },
};
```

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Test handler | `Test.createTestingModule()` + mock repository |
| Mock repository | Use custom mock class implementing interface |
| Test validation | Expect exception to be thrown |
| e2e REST | `supertest` + `app.getHttpServer()` |
| e2e GraphQL | `supertest` + GraphQL query string |
| Test aggregate | Call methods + verify events |
| Test VO | Constructor + validation rules |
| Coverage | `npm run test:cov` |

---

## Remember

- **Unit tests** = Fast, isolated, mock dependencies
- **e2e tests** = Slow, integrated, real dependencies
- **Test custom logic only**: Don't test Aurora-generated code
- **Mark your code**: Use `#region AI-generated code` in handlers
- **TDD when possible**: Write test → Implement → Refactor
