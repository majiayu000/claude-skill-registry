---
name: nestjs_specialist
router_kit: DevOpsKit
description: Comprehensive NestJS framework guide with Drizzle ORM integration. Use when building NestJS applications, setting up APIs, implementing authentication, working with databases, or integrating Drizzle ORM. Covers controllers, providers, modules, middleware, guards, interceptors, testing, microservices, GraphQL, and database patterns.
license: Complete terms in LICENSE.txt
metadata:
  skillport:
    category: auto-healed
    tags: [architecture, automation, backend framework, best practices, clean code, coding, collaboration, compliance, debugging, decorators, dependency injection, design patterns, development, documentation, efficiency, git, modules, nestjs specialist, optimization, productivity, programming, project management, quality assurance, refactoring, software engineering, standards, testing, typescript, utilities, version control, workflow]
---

# NestJS Framework with Drizzle ORM

## When to Use
- Building REST APIs or GraphQL servers with NestJS
- Setting up authentication and authorization
- Implementing middleware, guards, or interceptors
- Working with databases (TypeORM, Drizzle ORM)
- Creating microservices architecture
- Writing unit and integration tests
- Setting up OpenAPI/Swagger documentation

## Core Architecture

### Module Structure
```typescript
import { Module } from '@nestjs/common';

@Module({
  imports: [/* other modules */],
  controllers: [/* controllers */],
  providers: [/* providers */],
  exports: [/* exported providers */],
})
export class FeatureModule {}
```

### Controller Pattern
```typescript
import { Controller, Get, Post, Body, Param, Query } from '@nestjs/common';

@Controller('users')
export class UsersController {
  @Get()
  findAll(@Query() query: any) {
    return 'This returns all users';
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return `This returns user #${id}`;
  }

  @Post()
  create(@Body() createUserDto: any) {
    return 'This creates a user';
  }
}
```

### Service with Dependency Injection
```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  constructor(/* inject dependencies */) {}

  findAll() {
    return 'Users service logic';
  }
}
```

## Database Integration with Drizzle

### Setup with Drizzle ORM

#### Installation
```bash
# Using npm
npm install drizzle-orm pg
npm install -D drizzle-kit tsx @types/pg

# Using yarn
yarn add drizzle-orm pg
yarn add -D drizzle-kit tsx @types/pg
```

#### Configuration
```typescript
// drizzle.config.ts
import 'dotenv/config';
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  out: './drizzle',
  schema: './src/db/schema.ts',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

#### Database Schema
```typescript
// src/db/schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

#### Database Service
```typescript
// src/db/database.service.ts
import { Injectable } from '@nestjs/common';
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';
import * as schema from './schema';

@Injectable()
export class DatabaseService {
  private db: ReturnType<typeof drizzle>;

  constructor() {
    const pool = new Pool({
      connectionString: process.env.DATABASE_URL,
    });
    this.db = drizzle(pool, { schema });
  }

  get database() {
    return this.db;
  }
}
```

#### User Repository with Drizzle
```typescript
// src/users/user.repository.ts
import { Injectable } from '@nestjs/common';
import { DatabaseService } from '../db/database.service';
import { users } from '../db/schema';
import { eq } from 'drizzle-orm';

@Injectable()
export class UserRepository {
  constructor(private db: DatabaseService) {}

  async findAll() {
    return this.db.database.select().from(users);
  }

  async findOne(id: number) {
    const result = await this.db.database
      .select()
      .from(users)
      .where(eq(users.id, id))
      .limit(1);
    return result[0];
  }

  async create(data: typeof users.$inferInsert) {
    const result = await this.db.database
      .insert(users)
      .values(data)
      .returning();
    return result[0];
  }

  async update(id: number, data: Partial<typeof users.$inferInsert>) {
    const result = await this.db.database
      .update(users)
      .set(data)
      .where(eq(users.id, id))
      .returning();
    return result[0];
  }

  async remove(id: number) {
    const result = await this.db.database
      .delete(users)
      .where(eq(users.id, id))
      .returning();
    return result[0];
  }
}
```

#### Complete User Module
```typescript
// src/users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { UserRepository } from './user.repository';
import { DatabaseService } from '../db/database.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService, UserRepository, DatabaseService],
  exports: [UsersService],
})
export class UsersModule {}
```

#### User Service Implementation
```typescript
// src/users/users.service.ts
import { Injectable } from '@nestjs/common';
import { UserRepository } from './user.repository';
import { User } from './interfaces/user.interface';

@Injectable()
export class UsersService {
  constructor(private userRepository: UserRepository) {}

  async findAll(): Promise<User[]> {
    return this.userRepository.findAll();
  }

  async findOne(id: number): Promise<User> {
    const user = await this.userRepository.findOne(id);
    if (!user) {
      throw new Error('User not found');
    }
    return user;
  }

  async create(userData: Partial<User>): Promise<User> {
    return this.userRepository.create(userData);
  }

  async update(id: number, userData: Partial<User>): Promise<User> {
    await this.findOne(id); // Verify user exists
    return this.userRepository.update(id, userData);
  }

  async remove(id: number): Promise<User> {
    await this.findOne(id); // Verify user exists
    return this.userRepository.remove(id);
  }
}
```

## Authentication & Authorization

### JWT Authentication Guard
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  canActivate(context: ExecutionContext) {
    const request = context.switchToHttp().getRequest();
    const token = request.headers.authorization?.split(' ')[1];

    if (!token) {
      return false;
    }

    try {
      const decoded = this.jwtService.verify(token);
      request.user = decoded;
      return true;
    } catch {
      return false;
    }
  }
}
```

### Roles-Based Guard
```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user.roles?.includes(role));
  }
}
```

## Validation with Pipes

### Validation Pipe
```typescript
import { PipeTransform, Injectable, ArgumentMetadata, BadRequestException } from '@nestjs/common';
import { validate } from 'class-validator';
import { plainToClass } from 'class-transformer';

@Injectable()
export class ValidationPipe implements PipeTransform {
  async transform(value: any, { metatype }: ArgumentMetadata) {
    if (!metatype || !this.toValidate(metatype)) {
      return value;
    }

    const object = plainToClass(metatype, value);
    const errors = await validate(object);

    if (errors.length > 0) {
      throw new BadRequestException(errors);
    }

    return value;
  }

  private toValidate(metatype: Function): boolean {
    const types: Function[] = [String, Boolean, Number, Array, Object];
    return !types.includes(metatype);
  }
}
```

## Exception Handling

### Global Exception Filter
```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Request, Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message: exception.message,
    });
  }
}
```

## Testing Patterns

### Unit Testing Services
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';
import { UserRepository } from './user.repository';

describe('UsersService', () => {
  let service: UsersService;
  let repository: jest.Mocked<UserRepository>;

  beforeEach(async () => {
    const mockRepository = {
      findAll: jest.fn(),
      findOne: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      remove: jest.fn(),
    } as any;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: UserRepository,
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<UsersService>(UsersService);
    repository = module.get(UserRepository);
  });

  it('should return all users', async () => {
    const expectedUsers = [{ id: 1, name: 'John', email: 'john@example.com' }];
    repository.findAll.mockResolvedValue(expectedUsers);

    const result = await service.findAll();
    expect(result).toEqual(expectedUsers);
    expect(repository.findAll).toHaveBeenCalled();
  });
});
```

### E2E Testing with Drizzle
```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';
import { DatabaseService } from '../src/db/database.service';
import { drizzle } from 'drizzle-orm/node-postgres';
import { migrate } from 'drizzle-node-postgres/migrator';
import { migrate as drizzleMigrate } from 'drizzle-orm/node-postgres/migrator';

describe('UsersController (e2e)', () => {
  let app: INestApplication;
  let db: DatabaseService;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    db = moduleFixture.get<DatabaseService>(DatabaseService);

    // Run migrations
    await drizzleMigrate(db.database, { migrationsFolder: './drizzle' });

    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  beforeEach(async () => {
    // Clean database
    await db.database.delete(users).execute();
  });

  it('/users (POST)', () => {
    const createUserDto = {
      name: 'Test User',
      email: 'test@example.com',
    };

    return request(app.getHttpServer())
      .post('/users')
      .send(createUserDto)
      .expect(201)
      .expect((res) => {
        expect(res.body).toMatchObject(createUserDto);
        expect(res.body).toHaveProperty('id');
      });
  });

  it('/users (GET)', async () => {
    // First create a user
    await db.database.insert(users).values({
      name: 'Test User',
      email: 'test@example.com',
    });

    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
        expect(res.body).toHaveLength(1);
      });
  });
});
```

## Migrations with Drizzle

### Generating Migrations
```bash
npx drizzle-kit generate
```

### Running Migrations
```typescript
// src/migrations/migration.service.ts
import { Injectable } from '@nestjs/common';
import { migrate } from 'drizzle-orm/node-postgres/migrator';
import { DatabaseService } from '../db/database.service';

@Injectable()
export class MigrationService {
  constructor(private db: DatabaseService) {}

  async runMigrations() {
    try {
      await migrate(this.db.database, { migrationsFolder: './drizzle' });
      console.log('Migrations completed successfully');
    } catch (error) {
      console.error('Migration failed:', error);
      throw error;
    }
  }
}
```

## Configuration Management

### Environment Configuration
```typescript
// src/config/configuration.ts
export default () => ({
  database: {
    url: process.env.DATABASE_URL,
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'default-secret',
    expiresIn: process.env.JWT_EXPIRES_IN || '24h',
  },
  app: {
    port: parseInt(process.env.PORT, 10) || 3000,
  },
});
```

## Advanced Patterns

### Custom Decorators
```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const User = createParamDecorator(
  (data: string, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    return data ? user?.[data] : user;
  },
);
```

### Interceptors for Logging
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const now = Date.now();

    console.log(`[${method}] ${url} - Start`);

    return next
      .handle()
      .pipe(
        tap(() => console.log(`[${method}] ${url} - End ${Date.now() - now}ms`)),
      );
  }
}
```

## Microservices

### TCP Microservice
```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { Transport, MicroserviceOptions } from '@nestjs/microservices';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.TCP,
      options: {
        host: 'localhost',
        port: 8877,
      },
    },
  );
  await app.listen();
}
bootstrap();
```

## GraphQL Integration

### GraphQL Resolver with Drizzle
```typescript
import { Resolver, Query, Mutation, Args } from '@nestjs/graphql';
import { UserRepository } from './user.repository';

@Resolver(() => User)
export class UsersResolver {
  constructor(private userRepository: UserRepository) {}

  @Query(() => [User])
  async users() {
    return this.userRepository.findAll();
  }

  @Mutation(() => User)
  async createUser(@Args('input') input: CreateUserInput) {
    return this.userRepository.create(input);
  }
}
```

## Best Practices

1. **Always use constructor injection** - Never use property injection
2. **Use DTOs for data transfer** - Define interfaces for request/response
3. **Implement proper error handling** - Use exception filters
4. **Validate all inputs** - Use validation pipes
5. **Keep modules focused** - Single responsibility principle
6. **Use environment variables** - Never hardcode credentials
7. **Write comprehensive tests** - Unit and integration tests
8. **Use transactions for complex operations** - Maintain data consistency
9. **Implement proper logging** - Use interceptors for cross-cutting concerns
10. **Use type safety** - Leverage TypeScript features

## Common Patterns with Drizzle

### Transactions
```typescript
async transferFunds(fromId: number, toId: number, amount: number) {
  return this.db.database.transaction(async (tx) => {
    // Debit from account
    await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} - ${amount}` })
      .where(eq(accounts.id, fromId));

    // Credit to account
    await tx
      .update(accounts)
      .set({ balance: sql`${accounts.balance} + ${amount}` })
      .where(eq(accounts.id, toId));
  });
}
```

### Soft Deletes
```typescript
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  deletedAt: timestamp('deleted_at'),
});

async softDelete(id: number) {
  return this.db.database
    .update(users)
    .set({ deletedAt: new Date() })
    .where(eq(users.id, id));
}
```

### Complex Queries with Relations
```typescript
async getUsersWithPosts() {
  return this.db.database
    .select()
    .from(users)
*NestJS Specialist v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [NestJS Documentation](https://docs.nestjs.com/) & [Drizzle ORM NestJS Guide](https://orm.drizzle.team/docs/guides/nestjs)

### Aşama 1: Module Design
- [ ] **Boundary**: Her özellik (Feature) için ayrı bir modül oluştur (UserModule, AuthModule).
- [ ] **DI Types**: "Interface-based" injection kullanmak test edilebilirliği artırır (Provider token kullan).
- [ ] **Config**: `ConfigModule` ve `Joi` validasyonu ile ortam değişkenlerini güvene al.

### Aşama 2: Data Access (Drizzle)
- [ ] **Repo Pattern**: Drizzle kodunu doğrudan Service'e yazma, Repository katmanına soyutla.
- [ ] **Transactions**: İş mantığı gerektirdiğinde `db.transaction()` ile atomikliği sağla.
- [ ] **Migrations**: Şema değişiklikleri için mutlaka migration dosyası oluştur ve versiyonla.

### Aşama 3: Security & Stability
- [ ] **Guards**: Role-based access control (RBAC) için global veya route-bazlı guardları kur.
- [ ] **Interceptors**: Response formatını standardize et (`{ data: ..., meta: ... }`).
- [ ] **Filters**: Global Exception Filter ile hata mesajlarını kullanıcı dostu hale getir (500 hatalarını gizle).

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Döngüsel bağımlılık (Circular Dependency) var mı? |
| 2 | Tüm inputlar DTO ve `class-validator` ile kontrol ediliyor mu? |
| 3 | Controller'lar "Thin", Service'ler "Fat" mi? (Logic service'te mi?) |