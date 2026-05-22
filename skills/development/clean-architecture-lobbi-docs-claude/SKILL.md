---
name: clean-architecture
description: Clean Architecture and SOLID principles implementation including dependency injection, layer separation, domain-driven design, hexagonal architecture, and code quality patterns
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
dependencies: []
triggers:
  - clean architecture
  - solid principles
  - dependency injection
  - clean code
  - hexagonal architecture
  - domain driven design
  - ddd
  - layer architecture
  - onion architecture
  - code quality
  - refactoring
  - design patterns
  - inversion of control
  - ioc
---

# Clean Architecture Skill

Comprehensive guide for implementing Clean Architecture, SOLID principles, and maintainable code structures.

## When to Use This Skill

Activate this skill when:
- Designing new service architecture
- Refactoring legacy code to clean architecture
- Implementing dependency injection
- Defining domain boundaries
- Creating layer separation
- Applying SOLID principles
- Reviewing architectural decisions
- Setting up project structure

---

## Clean Architecture Overview

### The Dependency Rule

**Dependencies must point inward.** Inner layers must not know about outer layers.

```
┌─────────────────────────────────────────────────────────────┐
│                     EXTERNAL LAYER                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                 INFRASTRUCTURE LAYER                     │ │
│  │  ┌─────────────────────────────────────────────────────┐ │ │
│  │  │               APPLICATION LAYER                      │ │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │ │ │
│  │  │  │                DOMAIN LAYER                      │ │ │ │
│  │  │  │         (Entities, Value Objects)                │ │ │ │
│  │  │  └─────────────────────────────────────────────────┘ │ │ │
│  │  │    (Use Cases, Application Services)                  │ │ │
│  │  └─────────────────────────────────────────────────────┘ │ │
│  │  (Repositories, External Services, ORM)                   │ │
│  └─────────────────────────────────────────────────────────┘ │
│  (Web Framework, Database, UI, External APIs)                 │
└─────────────────────────────────────────────────────────────┘

                Dependencies point INWARD →
```

---

## Layer Definitions

### 1. Domain Layer (Core)

The heart of the application. Contains:
- **Entities**: Business objects with identity
- **Value Objects**: Immutable objects without identity
- **Domain Events**: Events that occur in the domain
- **Domain Services**: Stateless operations on domain objects
- **Repository Interfaces**: Abstractions for data access

```typescript
// src/domain/entities/user.entity.ts
export class User {
  constructor(
    public readonly id: UserId,
    public email: Email,
    public name: UserName,
    private passwordHash: PasswordHash,
    public readonly createdAt: Date
  ) {}

  changePassword(newPassword: Password, hasher: PasswordHasher): void {
    this.passwordHash = hasher.hash(newPassword);
  }

  validatePassword(password: Password, hasher: PasswordHasher): boolean {
    return hasher.verify(password, this.passwordHash);
  }
}

// src/domain/value-objects/email.vo.ts
export class Email {
  private constructor(private readonly value: string) {}

  static create(email: string): Email {
    if (!this.isValid(email)) {
      throw new InvalidEmailError(email);
    }
    return new Email(email.toLowerCase());
  }

  private static isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  toString(): string {
    return this.value;
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}

// src/domain/repository-interfaces/user.repository.ts
export interface UserRepository {
  findById(id: UserId): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: UserId): Promise<void>;
}
```

### 2. Application Layer

Orchestrates domain objects to perform use cases:
- **Use Cases**: Single responsibility application operations
- **Application Services**: Coordinate multiple use cases
- **DTOs**: Data transfer objects for boundaries
- **Ports**: Interfaces for external dependencies

```typescript
// src/application/use-cases/create-user.use-case.ts
export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
}

export interface CreateUserOutput {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

export class CreateUserUseCase {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly passwordHasher: PasswordHasher,
    private readonly eventEmitter: DomainEventEmitter
  ) {}

  async execute(input: CreateUserInput): Promise<CreateUserOutput> {
    // Validate email uniqueness
    const existingUser = await this.userRepository.findByEmail(
      Email.create(input.email)
    );
    if (existingUser) {
      throw new EmailAlreadyExistsError(input.email);
    }

    // Create domain entity
    const user = new User(
      UserId.generate(),
      Email.create(input.email),
      UserName.create(input.name),
      this.passwordHasher.hash(Password.create(input.password)),
      new Date()
    );

    // Persist
    await this.userRepository.save(user);

    // Emit domain event
    this.eventEmitter.emit(new UserCreatedEvent(user));

    // Return DTO
    return {
      id: user.id.toString(),
      email: user.email.toString(),
      name: user.name.toString(),
      createdAt: user.createdAt
    };
  }
}
```

### 3. Infrastructure Layer

Implements interfaces defined in inner layers:
- **Repository Implementations**: Database access
- **External Service Adapters**: Third-party integrations
- **ORM Configurations**: Database mappings
- **Messaging**: Queue/event implementations

```typescript
// src/infrastructure/repositories/postgresql-user.repository.ts
export class PostgreSQLUserRepository implements UserRepository {
  constructor(private readonly db: Database) {}

  async findById(id: UserId): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE id = $1',
      [id.toString()]
    );
    return row ? this.toDomain(row) : null;
  }

  async findByEmail(email: Email): Promise<User | null> {
    const row = await this.db.query(
      'SELECT * FROM users WHERE email = $1',
      [email.toString()]
    );
    return row ? this.toDomain(row) : null;
  }

  async save(user: User): Promise<void> {
    await this.db.query(
      `INSERT INTO users (id, email, name, password_hash, created_at)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (id) DO UPDATE SET
         email = $2, name = $3, password_hash = $4`,
      [user.id.toString(), user.email.toString(), user.name.toString(),
       user.passwordHash, user.createdAt]
    );
  }

  private toDomain(row: UserRow): User {
    return new User(
      UserId.fromString(row.id),
      Email.create(row.email),
      UserName.create(row.name),
      PasswordHash.fromString(row.password_hash),
      row.created_at
    );
  }
}
```

### 4. External/Presentation Layer

Entry points to the application:
- **Controllers**: HTTP request handlers
- **CLI**: Command-line interfaces
- **GraphQL Resolvers**: GraphQL handlers
- **Message Handlers**: Queue consumers

```typescript
// src/presentation/http/controllers/user.controller.ts
export class UserController {
  constructor(
    private readonly createUserUseCase: CreateUserUseCase,
    private readonly getUserUseCase: GetUserUseCase
  ) {}

  async create(req: Request, res: Response): Promise<void> {
    try {
      const result = await this.createUserUseCase.execute({
        email: req.body.email,
        name: req.body.name,
        password: req.body.password
      });

      res.status(201).json(result);
    } catch (error) {
      if (error instanceof EmailAlreadyExistsError) {
        res.status(409).json({ error: error.message });
      } else if (error instanceof ValidationError) {
        res.status(400).json({ error: error.message });
      } else {
        throw error;
      }
    }
  }
}
```

---

## Project Structure

### Recommended Directory Structure

```
src/
├── domain/                          # Domain Layer (Core)
│   ├── entities/
│   │   ├── user.entity.ts
│   │   └── order.entity.ts
│   ├── value-objects/
│   │   ├── email.vo.ts
│   │   ├── money.vo.ts
│   │   └── user-id.vo.ts
│   ├── events/
│   │   ├── user-created.event.ts
│   │   └── order-placed.event.ts
│   ├── services/
│   │   └── pricing.domain-service.ts
│   ├── repositories/                 # Interfaces only!
│   │   ├── user.repository.ts
│   │   └── order.repository.ts
│   └── errors/
│       ├── domain-error.ts
│       └── validation-error.ts
│
├── application/                      # Application Layer
│   ├── use-cases/
│   │   ├── user/
│   │   │   ├── create-user.use-case.ts
│   │   │   ├── get-user.use-case.ts
│   │   │   └── update-user.use-case.ts
│   │   └── order/
│   │       ├── create-order.use-case.ts
│   │       └── cancel-order.use-case.ts
│   ├── services/
│   │   └── notification.service.ts
│   ├── ports/                        # Secondary ports
│   │   ├── email.port.ts
│   │   └── payment.port.ts
│   └── dto/
│       ├── user.dto.ts
│       └── order.dto.ts
│
├── infrastructure/                   # Infrastructure Layer
│   ├── repositories/
│   │   ├── postgresql-user.repository.ts
│   │   └── postgresql-order.repository.ts
│   ├── adapters/
│   │   ├── sendgrid-email.adapter.ts
│   │   └── stripe-payment.adapter.ts
│   ├── orm/
│   │   ├── prisma/
│   │   │   └── schema.prisma
│   │   └── migrations/
│   ├── messaging/
│   │   ├── rabbitmq-publisher.ts
│   │   └── rabbitmq-consumer.ts
│   └── config/
│       └── database.config.ts
│
├── presentation/                     # Presentation Layer
│   ├── http/
│   │   ├── controllers/
│   │   │   ├── user.controller.ts
│   │   │   └── order.controller.ts
│   │   ├── middleware/
│   │   │   ├── auth.middleware.ts
│   │   │   └── error-handler.middleware.ts
│   │   ├── routes/
│   │   │   └── index.ts
│   │   └── validators/
│   │       └── user.validator.ts
│   ├── graphql/
│   │   ├── resolvers/
│   │   └── schema/
│   └── cli/
│       └── commands/
│
├── shared/                           # Cross-cutting concerns
│   ├── kernel/
│   │   ├── result.ts
│   │   └── either.ts
│   └── utils/
│       └── date.utils.ts
│
└── container/                        # Dependency Injection
    ├── container.ts
    └── providers/
        ├── user.provider.ts
        └── order.provider.ts
```

---

## Dependency Injection

### Container Setup

```typescript
// src/container/container.ts
import { Container } from 'inversify';
import { TYPES } from './types';

// Domain
import { UserRepository } from '@/domain/repositories/user.repository';

// Application
import { CreateUserUseCase } from '@/application/use-cases/user/create-user.use-case';

// Infrastructure
import { PostgreSQLUserRepository } from '@/infrastructure/repositories/postgresql-user.repository';

// Presentation
import { UserController } from '@/presentation/http/controllers/user.controller';

const container = new Container();

// Bind repositories (interface → implementation)
container.bind<UserRepository>(TYPES.UserRepository)
  .to(PostgreSQLUserRepository)
  .inSingletonScope();

// Bind use cases
container.bind<CreateUserUseCase>(TYPES.CreateUserUseCase)
  .to(CreateUserUseCase)
  .inTransientScope();

// Bind controllers
container.bind<UserController>(TYPES.UserController)
  .to(UserController)
  .inTransientScope();

export { container };
```

### Type Symbols

```typescript
// src/container/types.ts
export const TYPES = {
  // Repositories
  UserRepository: Symbol.for('UserRepository'),
  OrderRepository: Symbol.for('OrderRepository'),

  // Use Cases
  CreateUserUseCase: Symbol.for('CreateUserUseCase'),
  GetUserUseCase: Symbol.for('GetUserUseCase'),

  // Adapters
  EmailAdapter: Symbol.for('EmailAdapter'),
  PaymentAdapter: Symbol.for('PaymentAdapter'),

  // Controllers
  UserController: Symbol.for('UserController'),
  OrderController: Symbol.for('OrderController'),
};
```

---

## SOLID in Clean Architecture

### Single Responsibility

Each layer has one responsibility:
- Domain: Business rules
- Application: Use case orchestration
- Infrastructure: Technical concerns
- Presentation: User interface

### Open/Closed

Add features by adding new use cases, not modifying existing ones:

```typescript
// Add new feature: UpdateUserUseCase
// Don't modify: CreateUserUseCase
export class UpdateUserUseCase { /* ... */ }
```

### Liskov Substitution

Repository implementations are fully substitutable:

```typescript
// Both work with UserRepository interface
const postgresRepo: UserRepository = new PostgreSQLUserRepository(db);
const mongoRepo: UserRepository = new MongoUserRepository(client);
const memoryRepo: UserRepository = new InMemoryUserRepository();
```

### Interface Segregation

Small, focused interfaces:

```typescript
// BAD: Fat interface
interface UserService {
  create(data): User;
  update(id, data): User;
  delete(id): void;
  sendEmail(id): void;
  generateReport(id): Report;
  exportToCSV(id): string;
}

// GOOD: Segregated
interface UserCreator { create(data): User; }
interface UserUpdater { update(id, data): User; }
interface UserDeleter { delete(id): void; }
interface UserEmailer { sendEmail(id): void; }
```

### Dependency Inversion

All dependencies point to abstractions:

```typescript
// Application layer defines the port (interface)
export interface EmailPort {
  send(to: string, subject: string, body: string): Promise<void>;
}

// Infrastructure implements the adapter
export class SendGridEmailAdapter implements EmailPort {
  async send(to: string, subject: string, body: string): Promise<void> {
    await this.sendgrid.send({ to, subject, text: body });
  }
}

// Use case depends on abstraction, not implementation
export class CreateUserUseCase {
  constructor(private readonly emailPort: EmailPort) {}
}
```

---

## Testing Strategy

### Unit Tests (Domain & Application)

```typescript
// Test domain logic without infrastructure
describe('User', () => {
  it('should validate password correctly', () => {
    const hasher = new BCryptHasher();
    const password = Password.create('SecureP@ss1');
    const user = new User(
      UserId.generate(),
      Email.create('test@example.com'),
      UserName.create('Test User'),
      hasher.hash(password),
      new Date()
    );

    expect(user.validatePassword(password, hasher)).toBe(true);
    expect(user.validatePassword(Password.create('wrong'), hasher)).toBe(false);
  });
});

// Test use cases with mock repositories
describe('CreateUserUseCase', () => {
  it('should create user successfully', async () => {
    const mockRepo = {
      findByEmail: jest.fn().mockResolvedValue(null),
      save: jest.fn().mockResolvedValue(undefined)
    };
    const mockHasher = { hash: jest.fn().mockReturnValue('hashed') };
    const mockEmitter = { emit: jest.fn() };

    const useCase = new CreateUserUseCase(mockRepo, mockHasher, mockEmitter);

    const result = await useCase.execute({
      email: 'test@example.com',
      name: 'Test User',
      password: 'password123'
    });

    expect(result.email).toBe('test@example.com');
    expect(mockRepo.save).toHaveBeenCalled();
    expect(mockEmitter.emit).toHaveBeenCalled();
  });
});
```

### Integration Tests (Infrastructure)

```typescript
describe('PostgreSQLUserRepository', () => {
  let repository: PostgreSQLUserRepository;
  let db: Database;

  beforeAll(async () => {
    db = await createTestDatabase();
    repository = new PostgreSQLUserRepository(db);
  });

  afterAll(async () => {
    await db.close();
  });

  it('should save and retrieve user', async () => {
    const user = createTestUser();

    await repository.save(user);
    const retrieved = await repository.findById(user.id);

    expect(retrieved).not.toBeNull();
    expect(retrieved.email.equals(user.email)).toBe(true);
  });
});
```

### E2E Tests (Full Stack)

```typescript
describe('User API', () => {
  it('should create user via HTTP', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
        password: 'password123'
      });

    expect(response.status).toBe(201);
    expect(response.body.email).toBe('test@example.com');
  });
});
```

---

## Anti-Patterns to Avoid

### 1. Domain Logic in Controllers

```typescript
// BAD
class UserController {
  async create(req, res) {
    // Business logic in controller!
    if (await this.db.query('SELECT * FROM users WHERE email = $1', [req.body.email])) {
      return res.status(409).json({ error: 'Email exists' });
    }
    const hash = await bcrypt.hash(req.body.password, 10);
    await this.db.query('INSERT INTO users...');
  }
}

// GOOD
class UserController {
  async create(req, res) {
    const result = await this.createUserUseCase.execute(req.body);
    res.status(201).json(result);
  }
}
```

### 2. Infrastructure in Domain

```typescript
// BAD
class User {
  async save() {
    await prisma.user.create({ data: this }); // Infrastructure leak!
  }
}

// GOOD
class User {
  // Pure domain logic, no infrastructure
}

// Repository handles persistence
class UserRepository {
  async save(user: User) {
    await prisma.user.create({ data: user.toDTO() });
  }
}
```

### 3. Anemic Domain Model

```typescript
// BAD - No behavior, just data
class User {
  id: string;
  email: string;
  password: string;
}

class UserService {
  changePassword(user: User, newPassword: string) {
    user.password = hash(newPassword); // Logic outside entity
  }
}

// GOOD - Rich domain model
class User {
  constructor(private readonly id: UserId, private passwordHash: PasswordHash) {}

  changePassword(newPassword: Password, hasher: PasswordHasher): void {
    if (!newPassword.isStrong()) {
      throw new WeakPasswordError();
    }
    this.passwordHash = hasher.hash(newPassword);
  }
}
```

---

## Migration Strategy

### Legacy to Clean Architecture

1. **Identify Boundaries**: Find domain concepts
2. **Extract Entities**: Create domain objects
3. **Define Interfaces**: Create repository interfaces
4. **Implement Adapters**: Wrap existing data access
5. **Create Use Cases**: Extract business logic
6. **Refactor Controllers**: Delegate to use cases
7. **Add DI Container**: Wire dependencies
8. **Write Tests**: Cover each layer

---

## Related Resources

- [Development Standards](../../docs/DEVELOPMENT-STANDARDS.md)
- [Architecture Summary](../../docs/ARCHITECTURE-SUMMARY.md)
- [Code Quality Enforcer Agent](../../agents/code-quality-enforcer.md)
- [Robert C. Martin - Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
