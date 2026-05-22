---
name: aurora-development
description: >
    Expert NestJS development with CQRS architecture for Aurora projects. Covers
    commands, queries, handlers, business logic placement, guards, interceptors,
    and custom decorators, Value Objects. Trigger: When implementing NestJS
    components, CQRS handlers, business logic, guards, interceptors, or custom
    decorators in Aurora projects.
license: MIT
metadata:
    author: aurora
    version: '1.1'
    auto_invoke:
        'Implementing NestJS/Aurora components, handlers, services, guards,
        interceptors'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

**This is the PRIMARY skill for IMPLEMENTING code in Aurora/NestJS projects.**

Use this skill when:

- **Writing business logic in command/query handlers** (validations, rules,
  checks)
- **Implementing any custom code** in Aurora-generated handlers
- Creating guards, interceptors, pipes, or custom decorators
- Implementing NestJS-specific features (middleware, exception filters)
- Working with dependency injection (DI) and inversion of control (IoC)
- Integrating with Sequelize ORM
- Testing with Jest (unit and e2e)

**Note:** For understanding CQRS architecture (what are Commands, Handlers,
etc.), see `aurora-cqrs` skill.

**Always combine with:**

- `prettier` skill for code formatting (MANDATORY after every edit)
- `typescript` skill for strict type patterns
- `aurora-cqrs` skill for CQRS architecture reference (structure, editable
  zones)
- `aurora-project-structure` skill for file locations
- `aurora-criteria` skill for QueryStatement filters

---

## Critical Patterns

### ⚠️ Code Formatting (CRITICAL!)

**MANDATORY: Use `prettier` skill after EVERY file modification**

After editing/creating ANY file:

1. ✅ **IMMEDIATELY** invoke `prettier` skill
2. ✅ Format the modified file(s)
3. ✅ Verify formatting succeeded
4. ✅ Continue to next task

```bash
# Quick reference (see prettier skill for full details)
npm run format -- <file-path>
```

**See `.claude/skills/prettier/SKILL.md` for:**

- Complete formatting commands
- Workflow patterns
- Integration with other skills
- Troubleshooting
- Configuration details

**❌ NEVER skip formatting or leave unformatted code**

---

### ⚠️ Business Logic Placement (CRITICAL!)

**MUST follow these rules:**

#### ✅ Command Handler (execute() method)

**PUT HERE:**

- ✅ Business validations (e.g., price > 0, year >= 2008)
- ✅ Complex business rules (e.g., check last maintenance date)
- ✅ Pre-validation queries (e.g., find duplicates)
- ✅ Duplicate checks
- ✅ External service calls (e.g., notifications, APIs)
- ✅ Transformations or calculations before persisting

```typescript
@CommandHandler(CreateMaintenanceHistoryCommand)
export class CreateMaintenanceHistoryCommandHandler {
    constructor(
        private readonly service: CreateMaintenanceHistoryService,
        private readonly repository: TeslaIMaintenanceHistoryRepository,
    ) {}

    async execute(command: CreateMaintenanceHistoryCommand): Promise<void> {
        /* #region AI-generated code */
        // ✅ CORRECT: Business validation BEFORE service call
        const lastMaintenance = await this.repository.find({
            queryStatement: {
                where: { unitId: { '[eq]': command.payload.unitId } },
                order: [{ workshopEntryDate: 'desc' }],
                limit: 1,
            },
            cQMetadata: command.cQMetadata,
        });

        if (lastMaintenance) {
            const daysDiff = calculateDaysDifference(
                lastMaintenance.workshopEntryDate.value,
            );
            if (daysDiff > 365) {
                throw new TeslaUnitNotRevisedInOneYearException(
                    'Unit has not been serviced in over a year',
                );
            }
        }
        /* #endregion AI-generated code */

        // Call service (only persistence)
        await this.service.main(payload, command.cQMetadata);
    }
}
```

#### ❌ Service (main() method)

**DO NOT PUT HERE:**

- ❌ Business validations → Put in Handler
- ❌ Business rules → Put in Handler
- ❌ Pre-validation queries → Put in Handler

**Services are ONLY for:**

- ✅ Creating aggregate with factory pattern
- ✅ Persisting via repository
- ✅ Publishing domain events (created, updated, deleted)

```typescript
@Injectable()
export class CreateMaintenanceHistoryService {
    constructor(
        private readonly publisher: EventPublisher,
        private readonly repository: TeslaIMaintenanceHistoryRepository,
    ) {}

    async main(payload, cQMetadata): Promise<void> {
        // ✅ ONLY persistence and events (NO business logic)
        const maintenanceHistory = TeslaMaintenanceHistory.register(
            payload.id,
            payload.unitId,
            payload.workshopEntryDate,
            payload.workshopExitDate,
            new TeslaMaintenanceHistoryCreatedAt({ currentTimestamp: true }),
            new TeslaMaintenanceHistoryUpdatedAt({ currentTimestamp: true }),
            null,
        );

        await this.repository.create(maintenanceHistory, {
            createOptions: cQMetadata?.repositoryOptions,
        });

        const register = this.publisher.mergeObjectContext(maintenanceHistory);
        register.created({ payload: maintenanceHistory, cQMetadata });
        register.commit();
    }
}
```

#### 🔑 Decision Tree

```
What am I implementing?
│
├─ Validation, business rule, pre-check query
│  └─ ✅ Command Handler (execute method)
│      - Inject repository if you need queries
│      - Add logic BEFORE calling service
│
└─ Persistence, aggregate creation, events
   └─ ✅ Service (main method)
       - NO validations here
       - Only create, persist, publish events
```

---

### ⚠️ Querying with Relations (CRITICAL!)

**BEFORE writing queries that need related data:**

1. ✅ **Read `.aurora.yaml` schema using `aurora-schema` skill**
2. ✅ **Identify relationships in `aggregateProperties`**
3. ✅ **Use `include` in QueryStatement (see `aurora-criteria` skill)**

```typescript
/* #region AI-generated code */
// 1. Check cliter/tesla/unit.aurora.yaml for 'model' relationship
// 2. Use include to load relation in single query
const queryStatement: QueryStatement = {
    where: { id: unitId },
    include: [{ association: 'model' }], // Field name from YAML relationship
};

const unit = await this.unitRepository.find({
    queryStatement,
    cQMetadata: command.cQMetadata,
});

// Access related entity
if (unit && unit.model) {
    unit.model.isActive = new TeslaModelIsActive(false);
}
/* #endregion AI-generated code */
```

**Benefits:**

- ✅ Single query (avoid N+1 problem)
- ✅ Better performance
- ❌ Never make sequential queries for related data

**See:**

- `aurora-schema` skill - Read/analyze YAML schemas
- `aurora-criteria` skill - QueryStatement with include syntax

---

### Marking Custom Code

**ALWAYS mark custom code with AI-generated comments:**

```typescript
/* #region AI-generated code */
// Custom logic here
if (condition) {
    // implementation
}
/* #endregion AI-generated code */
```

**Rules:**

- Mark complete logical blocks
- DO NOT break syntax with comments
- Preserve existing code outside regions

---

## NestJS Components

### Command Handler

```typescript
import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { CreateUserCommand } from './create-user.command';
import { UserRepository } from '@infrastructure/user/repositories/user.repository';

@CommandHandler(CreateUserCommand)
export class CreateUserHandler implements ICommandHandler<CreateUserCommand> {
    constructor(
        private readonly service: CreateUserService,
        private readonly repository: UserRepository, // Inject if needed for validations
    ) {}

    async execute(command: CreateUserCommand): Promise<void> {
        const { payload } = command;

        /* #region AI-generated code */
        // Business validation: Check duplicates
        const existingUser = await this.repository.find({
            queryStatement: {
                where: { email: payload.email },
            },
        });

        if (existingUser) {
            throw new ConflictException('User already exists');
        }

        // Business rule: isLocked=true → isActive=false
        if (payload.isLocked === true) {
            payload.isActive = false;
        }
        /* #endregion AI-generated code */

        // Call service (only persistence)
        await this.service.main(payload, command.cQMetadata);
    }
}
```

### Query Handler

```typescript
import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { GetUsersQuery } from './get-users.query';
import { UserMapper } from '@domain/user/user.mapper';

@QueryHandler(GetUsersQuery)
export class GetUsersHandler implements IQueryHandler<GetUsersQuery> {
    private readonly mapper: UserMapper = new UserMapper();

    constructor(
        private readonly service: GetUsersService,
        private readonly cache: CacheService, // Custom service
    ) {}

    async execute(query: GetUsersQuery): Promise<UserResponse[]> {
        /* #region AI-generated code */
        // Try cache first
        const cacheKey = `users:${JSON.stringify(query.queryStatement)}`;
        const cached = await this.cache.get(cacheKey);
        if (cached) return cached;
        /* #endregion AI-generated code */

        const users = await this.service.main(
            query.queryStatement,
            query.constraint,
            query.cQMetadata,
        );

        if (query.cQMetadata?.excludeMapModelToAggregate) {
            return users;
        }

        const responses = this.mapper.mapAggregatesToResponses(users);

        /* #region AI-generated code */
        // Cache results for 1 hour
        await this.cache.set(cacheKey, responses, 3600);
        /* #endregion AI-generated code */

        return responses;
    }
}
```

### Guard

```typescript
import {
    Injectable,
    CanActivate,
    ExecutionContext,
    ForbiddenException,
} from '@nestjs/common';

@Injectable()
export class UserNotLockedGuard implements CanActivate {
    /* #region AI-generated code */
    canActivate(context: ExecutionContext): boolean {
        const request = context.switchToHttp().getRequest();
        const user = request.user;

        if (user?.isLocked) {
            throw new ForbiddenException('User account is locked');
        }

        return true;
    }
    /* #endregion AI-generated code */
}
```

### Interceptor

```typescript
import {
    Injectable,
    NestInterceptor,
    ExecutionContext,
    CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
    /* #region AI-generated code */
    intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
        const now = Date.now();
        const request = context.switchToHttp().getRequest();

        return next.handle().pipe(
            tap(() => {
                const elapsed = Date.now() - now;
                console.log(`${request.method} ${request.url} - ${elapsed}ms`);
            }),
        );
    }
    /* #endregion AI-generated code */
}
```

### Custom Decorator

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
    (data: unknown, ctx: ExecutionContext) => {
        /* #region AI-generated code */
        const request = ctx.switchToHttp().getRequest();
        return request.user;
        /* #endregion AI-generated code */
    },
);

// Usage in controller:
@Get('profile')
getProfile(@CurrentUser() user: User) {
    return user;
}
```

### Pipe

```typescript
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
    /* #region AI-generated code */
    transform(value: string): number {
        const val = parseInt(value, 10);
        if (isNaN(val)) {
            throw new BadRequestException('Validation failed: not a number');
        }
        return val;
    }
    /* #endregion AI-generated code */
}
```

### Exception Filter

```typescript
import {
    ExceptionFilter,
    Catch,
    ArgumentsHost,
    HttpException,
} from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
    /* #region AI-generated code */
    catch(exception: HttpException, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();
        const status = exception.getStatus();

        response.status(status).json({
            statusCode: status,
            timestamp: new Date().toISOString(),
            message: exception.message,
        });
    }
    /* #endregion AI-generated code */
}
```

---

## Code Style & Conventions

### Import Order

```typescript
// 1. Node.js
import { readFile } from 'fs/promises';

// 2. NestJS
import { Injectable, Controller } from '@nestjs/common';
import { CommandHandler } from '@nestjs/cqrs';

// 3. External libraries
import { v4 as uuid } from 'uuid';

// 4. Internal (@app, @domain, @infrastructure)
import { UserRepository } from '@infrastructure/iam/user/repositories/user.repository';

// 5. Relative
import { CreateUserCommand } from './create-user.command';
```

### Naming Conventions

| Type        | Pattern                   | Example              |
| ----------- | ------------------------- | -------------------- |
| Command     | `[Action][Entity]Command` | `CreateUserCommand`  |
| Query       | `[Action][Entity]Query`   | `FindUserByIdQuery`  |
| Handler     | `[Action][Entity]Handler` | `CreateUserHandler`  |
| Event       | `[Entity][Action]Event`   | `UserCreatedEvent`   |
| Service     | `[Entity]Service`         | `UserService`        |
| Guard       | `[Purpose]Guard`          | `JwtAuthGuard`       |
| Interceptor | `[Purpose]Interceptor`    | `LoggingInterceptor` |
| Pipe        | `[Purpose]Pipe`           | `ValidationPipe`     |
| Decorator   | `[Purpose]`               | `CurrentUser`        |

### Formatting

- **Indentation**: 4 spaces
- **Braces**: New line for classes/methods
- **Semicolons**: Required
- **Quotes**: Single quotes

```typescript
@Injectable()
export class MyService {
    constructor(private readonly repository: UserRepository) {}

    async myMethod(id: string): Promise<User> {
        return await this.repository.findById(id);
    }
}
```

---

## Dependency Injection

### Constructor Injection (Preferred)

```typescript
@Injectable()
export class UserService {
    constructor(
        private readonly repository: UserRepository,
        private readonly logger: Logger,
        private readonly eventBus: EventBus,
    ) {}
}
```

### Module Registration

```typescript
@Module({
    imports: [CqrsModule],
    controllers: [UserController],
    providers: [
        UserService,
        CreateUserHandler,
        GetUsersHandler,
        UserRepository,
    ],
    exports: [UserService],
})
export class UserModule {}
```

---

## Testing Patterns

### Unit Test (Handler)

```typescript
describe('CreateUserHandler', () => {
    let handler: CreateUserHandler;
    let service: CreateUserService;
    let repository: UserRepository;

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            providers: [
                CreateUserHandler,
                {
                    provide: CreateUserService,
                    useValue: { main: jest.fn() },
                },
                {
                    provide: UserRepository,
                    useValue: { find: jest.fn() },
                },
            ],
        }).compile();

        handler = module.get<CreateUserHandler>(CreateUserHandler);
        service = module.get<CreateUserService>(CreateUserService);
        repository = module.get<UserRepository>(UserRepository);
    });

    it('should throw ConflictException if user exists', async () => {
        jest.spyOn(repository, 'find').mockResolvedValue({ id: '1' });

        await expect(
            handler.execute({ payload: { email: 'test@example.com' } }),
        ).rejects.toThrow(ConflictException);
    });
});
```

---

## Decision Trees

### When to use Guard vs Interceptor vs Pipe?

```
Need authentication/authorization?
└─ Use Guard (before route handler)

Need to transform input data?
└─ Use Pipe (before route handler, per parameter)

Need to transform response or add cross-cutting logic?
└─ Use Interceptor (before and after route handler)

Need request/response logging?
└─ Use Middleware or Interceptor

Need to catch and format exceptions?
└─ Use Exception Filter
```

### Where to add custom logic?

```
Need validation before save?
└─ Add in CommandHandler.execute() before service call

Need to react to events?
└─ Create EventHandler

Need to coordinate multiple operations?
└─ Create Saga

Need to transform data?
└─ Use Mapper

Need custom query logic?
└─ Add in QueryHandler.execute() before/after service call

Need reusable business logic?
└─ Create custom Service and inject in Handler
```

---

## Best Practices

### ✅ DO

- Always mark custom code with `/* #region AI-generated code */`
- Put business logic in **handlers**, not services
- Inject repository in handlers if you need pre-validation queries
- Use dependency injection for all dependencies
- Create custom services for reusable logic
- Use guards for authentication/authorization
- Use interceptors for logging/caching
- Use pipes for validation
- Write unit tests for handlers
- Follow NestJS naming conventions
- Use TypeScript strict mode (see `typescript` skill)

### ❌ DON'T

- Don't put business logic in services (put in handlers)
- Don't modify generated files (marked with `@aurora-generated`)
- Don't bypass repository (always use repository interface)
- Don't use `any` type (use `unknown` or generics, see `typescript` skill)
- Don't forget to commit events (call `aggregate.commit()`)
- Don't create commands/queries manually (use Aurora CLI)
- Don't mix concerns (keep separation of concerns)

---

## Common Patterns

### Pattern 1: Command with Pre-Validation

```typescript
@CommandHandler(CreateOrderCommand)
export class CreateOrderCommandHandler {
    constructor(
        private readonly service: CreateOrderService,
        private readonly productRepository: ProductRepository,
    ) {}

    async execute(command: CreateOrderCommand): Promise<void> {
        /* #region AI-generated code */
        // Validate product exists and has stock
        const product = await this.productRepository.findById(
            command.payload.productId,
        );

        if (!product) {
            throw new NotFoundException('Product not found');
        }

        if (product.stock < command.payload.quantity) {
            throw new BadRequestException('Insufficient stock');
        }
        /* #endregion AI-generated code */

        await this.service.main(command.payload, command.cQMetadata);
    }
}
```

### Pattern 2: Query with Caching

```typescript
@QueryHandler(GetProductsQuery)
export class GetProductsQueryHandler {
    constructor(
        private readonly service: GetProductsService,
        private readonly cache: CacheService,
    ) {}

    async execute(query: GetProductsQuery): Promise<ProductResponse[]> {
        /* #region AI-generated code */
        const key = `products:${JSON.stringify(query.queryStatement)}`;
        const cached = await this.cache.get(key);
        if (cached) return cached;
        /* #endregion AI-generated code */

        const products = await this.service.main(...);
        const responses = this.mapper.mapAggregatesToResponses(products);

        /* #region AI-generated code */
        await this.cache.set(key, responses, 3600);
        /* #endregion AI-generated code */

        return responses;
    }
}
```

### Pattern 3: Global Exception Filter

```typescript
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
    /* #region AI-generated code */
    catch(exception: unknown, host: ArgumentsHost) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse<Response>();

        const status =
            exception instanceof HttpException
                ? exception.getStatus()
                : HttpStatus.INTERNAL_SERVER_ERROR;

        const message =
            exception instanceof HttpException
                ? exception.message
                : 'Internal server error';

        response.status(status).json({
            statusCode: status,
            timestamp: new Date().toISOString(),
            message,
        });
    }
    /* #endregion AI-generated code */
}
```

---

## Resources

- **NestJS Docs**: https://docs.nestjs.com
- **CQRS Module**: https://docs.nestjs.com/recipes/cqrs
- **Testing**: https://docs.nestjs.com/fundamentals/testing
- **Aurora CQRS**: `.claude/skills/aurora-cqrs/SKILL.md`
- **TypeScript**: `.claude/skills/typescript/SKILL.md`
- **Aurora CLI**: `.claude/skills/aurora-cli/SKILL.md`
- **Project Structure**: `.claude/skills/aurora-project-structure/SKILL.md`

---

## Related Skills

- `aurora-cqrs` - CQRS architecture reference (structure, editable zones, data
  flow)
- `typescript` - Strict type patterns
- `aurora-project-structure` - File locations
- `aurora-criteria` - QueryStatement for filters
- `jest-nestjs` - Testing patterns
- `supertest-nestjs` - E2E API testing
