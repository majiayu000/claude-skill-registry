---
name: nestjs
description: Provides comprehensive NestJS framework patterns with Drizzle ORM integration for building scalable server-side applications. Generates REST/GraphQL APIs, implements authentication guards, creates database schemas, and sets up microservices. Use when building NestJS applications, setting up APIs, implementing authentication, working with databases, or integrating Drizzle ORM.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# NestJS Framework with Drizzle ORM

## Overview

Provides NestJS patterns with Drizzle ORM for building production-ready server-side applications. Covers CRUD modules, JWT authentication, database operations, migrations, testing, microservices, and GraphQL integration.

## When to Use

- Building REST APIs or GraphQL servers with NestJS
- Setting up authentication and authorization with JWT
- Implementing database operations with Drizzle ORM
- Creating microservices with TCP/Redis transport
- Writing unit and integration tests
- Running database migrations with drizzle-kit

## Instructions

1. **Install dependencies**: `npm i drizzle-orm pg && npm i -D drizzle-kit tsx`
2. **Define schema**: Create `src/db/schema.ts` with Drizzle table definitions
3. **Create DatabaseService**: Inject Drizzle client as a NestJS provider
4. **Build CRUD module**: Controller → Service → Repository pattern
5. **Add validation**: Use class-validator DTOs with ValidationPipe
6. **Implement guards**: Create JWT/Roles guards for route protection
7. **Write tests**: Use `@nestjs/testing` with mocked repositories
8. **Run migrations**: `npx drizzle-kit generate` → **Verify SQL** → `npx drizzle-kit migrate`

## Examples

### Complete CRUD Module with Drizzle

```typescript
// src/db/schema.ts
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});

// src/users/dto/create-user.dto.ts
export class CreateUserDto {
  @IsString() @IsNotEmpty() name: string;
  @IsEmail() email: string;
}

// src/users/user.repository.ts
@Injectable()
export class UserRepository {
  constructor(private db: DatabaseService) {}

  async findAll() {
    return this.db.database.select().from(users);
  }

  async create(data: typeof users.$inferInsert) {
    return this.db.database.insert(users).values(data).returning();
  }
}

// src/users/users.service.ts
@Injectable()
export class UsersService {
  constructor(private repo: UserRepository) {}

  async create(dto: CreateUserDto) {
    return this.repo.create(dto);
  }
}

// src/users/users.controller.ts
@Controller('users')
export class UsersController {
  constructor(private service: UsersService) {}

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.service.create(dto);
  }
}

// src/users/users.module.ts
@Module({
  controllers: [UsersController],
  providers: [UsersService, UserRepository, DatabaseService],
  exports: [UsersService],
})
export class UsersModule {}
```

### JWT Authentication Guard

```typescript
@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  canActivate(context: ExecutionContext) {
    const token = context.switchToHttp().getRequest()
      .headers.authorization?.split(' ')[1];
    if (!token) return false;
    try {
      const decoded = this.jwtService.verify(token);
      context.switchToHttp().getRequest().user = decoded;
      return true;
    } catch {
      return false;
    }
  }
}
```

### Database Transactions

```typescript
async transferFunds(fromId: number, toId: number, amount: number) {
  return this.db.database.transaction(async (tx) => {
    await tx.update(accounts)
      .set({ balance: sql`${accounts.balance} - ${amount}` })
      .where(eq(accounts.id, fromId));
    await tx.update(accounts)
      .set({ balance: sql`${accounts.balance} + ${amount}` })
      .where(eq(accounts.id, toId));
  });
}
```

### Unit Testing with Mocks

```typescript
describe('UsersService', () => {
  let service: UsersService;
  let repo: jest.Mocked<UserRepository>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        UsersService,
        { provide: UserRepository, useValue: { findAll: jest.fn(), create: jest.fn() } },
      ],
    }).compile();
    service = module.get(UsersService);
    repo = module.get(UserRepository);
  });

  it('should create user', async () => {
    const dto = { name: 'John', email: 'john@example.com' };
    repo.create.mockResolvedValue({ id: 1, ...dto, createdAt: new Date() });
    expect(await service.create(dto)).toMatchObject(dto);
  });
});
```

## Constraints and Warnings

- **DTOs required**: Always use DTOs with class-validator, never accept raw objects
- **Transactions**: Keep transactions short; avoid nested transactions
- **Guards order**: JWT guard must run before Roles guard
- **Environment variables**: Never hardcode DATABASE_URL or JWT_SECRET
- **Migrations**: Run `drizzle-kit generate` after schema changes before deploying
- **Circular dependencies**: Use `forwardRef()` carefully; prefer module restructuring

## Best Practices

- Validate all inputs with global `ValidationPipe`
- Use transactions for multi-table operations
- Document APIs with OpenAPI/Swagger decorators

## References

Advanced patterns and detailed examples available in:
- `references/reference.md` - Core patterns, guards, interceptors, microservices, GraphQL
- `references/drizzle-reference.md` - Drizzle ORM installation, configuration, queries
- `references/workflow-optimization.md` - Development workflows, parallel execution strategies
