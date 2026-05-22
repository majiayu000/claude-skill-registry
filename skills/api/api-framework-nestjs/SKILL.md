---
name: api-framework-nestjs
description: NestJS backend framework - modules, controllers, services, DI, guards, pipes, interceptors, exception filters, middleware, DTOs with class-validator
---

# NestJS Patterns

> **Quick Guide:** NestJS is an opinionated, modular Node.js framework built on TypeScript. Use modules to organize features, controllers for HTTP routing, services for business logic with dependency injection, DTOs with class-validator for validation, guards for auth, and exception filters for error handling. Key gotchas: always register services in module `providers`, always enable `ValidationPipe` globally with `whitelist: true`, never put business logic in controllers, never instantiate services with `new`. NestJS 11 is the current stable version (SWC default compiler, Express v5, reversed termination hooks).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@Injectable()` on every service and register it in the module `providers` array)**

**(You MUST enable `ValidationPipe` globally with `whitelist: true` and `forbidNonWhitelisted: true`)**

**(You MUST use DTOs with class-validator decorators for ALL request body validation — never validate manually in controllers)**

**(You MUST throw NestJS built-in HTTP exceptions (`NotFoundException`, `BadRequestException`, etc.) — never send raw status codes)**

**(You MUST use constructor injection for dependencies — never instantiate services manually with `new`)**

</critical_requirements>

---

**Auto-detection:** NestJS, @nestjs/common, @nestjs/core, @Module, @Controller, @Injectable, @Get, @Post, @Body, @Param, @Query, @UseGuards, @UseInterceptors, @UsePipes, @UseFilters, CanActivate, NestInterceptor, PipeTransform, ExceptionFilter, ValidationPipe, class-validator, class-transformer

**When to use:**

- Building structured backend APIs with TypeScript and dependency injection
- Applications requiring modular architecture with clear separation of concerns
- REST APIs with declarative validation, authentication, and role-based access
- Projects needing the guard/interceptor/pipe/filter request lifecycle

**When NOT to use:**

- Simple scripts or serverless functions that don't need a framework
- Projects where Express/Fastify alone is sufficient (no DI, no modules needed)
- Frontend code

**Detailed Resources:**

- [examples/core.md](examples/core.md) — Feature modules, CRUD, DTOs, dynamic modules, exception filters, custom providers
- [examples/database.md](examples/database.md) — NestJS DI patterns for database integration, transactions
- [examples/auth.md](examples/auth.md) — Passport.js integration, JWT strategy, auth guards, RBAC
- [examples/testing.md](examples/testing.md) — Unit testing with `Test.createTestingModule`, e2e with supertest
- [examples/advanced.md](examples/advanced.md) — Interceptors, custom pipes, custom decorators, config, CQRS, Swagger
- [reference.md](reference.md) — CLI commands, project structure, decorator tables, decision frameworks

---

<philosophy>

## Philosophy

NestJS enforces a **modular, decorator-driven architecture** inspired by Angular. Every feature is organized into modules containing controllers (HTTP layer), services (business logic), and supporting infrastructure (guards, pipes, interceptors, filters).

**Core principles:**

1. **Modularity** — Group related controllers, services, and providers into feature modules. Modules are the primary organizational unit.
2. **Dependency injection** — Never instantiate services manually. Declare them as `@Injectable()` and let NestJS resolve the dependency graph via constructor injection.
3. **Decorator-driven** — Decorators (`@Controller`, `@Get`, `@Body`, `@UseGuards`) attach metadata that NestJS uses to build routing, validation, and middleware pipelines.
4. **Separation of concerns** — Controllers handle HTTP request/response. Services handle business logic. Guards handle authorization. Pipes handle validation/transformation. Filters handle exceptions.
5. **Convention over configuration** — Follow NestJS conventions (one module per feature, one controller per resource, DTOs for validation) to get batteries-included functionality.

</philosophy>

---

<patterns>

## Key Patterns

### Module System

Every NestJS app has a root `AppModule` that imports feature modules. Each feature module groups its controller, service, and providers. Export services that other modules need.

```typescript
// Feature module — one per resource
@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService], // Available to other modules
})
export class UsersModule {}
```

**Why good:** Encapsulation per feature, explicit dependency graph via imports/exports, testable in isolation

See [examples/core.md](examples/core.md) for complete CRUD module, dynamic modules, and custom providers.

---

### Controllers — Thin Routing Layer

Controllers should only extract request data and delegate to services. No business logic.

```typescript
@Controller("users")
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get(":id")
  findOne(@Param("id", ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

**Why good:** `ParseIntPipe` validates and converts param, `@HttpCode` for explicit status, thin delegation to service

**Anti-pattern:** Business logic, manual validation, or database access in controllers — always delegate to services.

---

### DTOs with class-validator

Use DTOs with class-validator decorators for all request validation. Enable `ValidationPipe` globally.

```typescript
const MIN_PASSWORD_LENGTH = 8;

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(MIN_PASSWORD_LENGTH)
  password: string;
}

// Update DTO — reuses validation rules
export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

```typescript
// main.ts — Enable globally
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true, // Strip unknown properties
    forbidNonWhitelisted: true, // Reject unknown properties
    transform: true, // Auto-transform to DTO instances
  }),
);
```

**Why good:** Declarative validation, `whitelist` prevents mass-assignment, `PartialType` avoids duplicating rules

See [examples/core.md](examples/core.md) for nested DTOs, query DTOs with pagination, and validation groups.

---

### Services and Dependency Injection

Services contain business logic. Decorate with `@Injectable()` and inject via constructor.

```typescript
@Injectable()
export class UsersService {
  findOne(id: number): User {
    const user = this.users.find((u) => u.id === id);
    if (!user) {
      throw new NotFoundException(`User with id ${id} not found`);
    }
    return user;
  }
}
```

**Why good:** `@Injectable()` enables DI, throws NestJS HTTP exceptions, pure business logic with no HTTP concerns

#### Custom Providers

Use token-based injection for non-class providers (factory, value, class providers):

```typescript
const DATABASE_CONNECTION = "DATABASE_CONNECTION";

const databaseProvider = {
  provide: DATABASE_CONNECTION,
  useFactory: async (configService: ConfigService) => {
    return createConnection(configService.get("database"));
  },
  inject: [ConfigService],
};

// Inject with @Inject token
constructor(@Inject(DATABASE_CONNECTION) private readonly db: Connection) {}
```

See [examples/core.md](examples/core.md) for complete provider examples.

---

### Exception Handling

Throw NestJS built-in HTTP exceptions from services. Use exception filters for custom error response formatting.

```typescript
// Service — throw built-in exceptions
throw new NotFoundException("Resource not found");
throw new ConflictException("Resource already exists");
throw new BadRequestException("Invalid input");
throw new UnauthorizedException("Authentication required");
```

**Key point:** NestJS auto-converts these to proper HTTP responses with correct status codes. Never send raw status codes.

For custom error response shapes, use a global `@Catch()` exception filter. See [examples/core.md](examples/core.md).

---

### Guards and Middleware

Guards decide whether a request proceeds (authorization). Middleware runs before routing (logging, CORS).

```typescript
// Guard — implements CanActivate
@Injectable()
export class JwtAuthGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest<Request>();
    // Validate token, attach user to request
    return true;
  }
}

// Apply to routes
@UseGuards(JwtAuthGuard, RolesGuard)
@Controller("admin")
export class AdminController {}
```

**Why good:** Guards are injectable (can use services), composable (run in order), use `Reflector` for metadata-driven access control

See [examples/auth.md](examples/auth.md) for JWT auth, Passport.js integration, RBAC, and `@Public()` decorator.

---

### Interceptors

Interceptors wrap handler execution for cross-cutting concerns (response wrapping, logging, caching).

```typescript
@Injectable()
export class TransformResponseInterceptor<T> implements NestInterceptor {
  intercept(
    context: ExecutionContext,
    next: CallHandler,
  ): Observable<ApiResponse<T>> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}
```

See [examples/advanced.md](examples/advanced.md) for logging, caching, and custom pipe patterns.

</patterns>

---

<decision_framework>

## Decision Framework

### Request Lifecycle

```
Incoming Request
  → Middleware (logging, CORS, body parsing)
    → Guards (authentication, authorization)
      → Interceptors (pre-handler: transform request, start timing)
        → Pipes (validation, transformation)
          → Route Handler (controller method)
        → Interceptors (post-handler: transform response, log timing)
  → Exception Filters (catch and format errors)
→ Response
```

### Which Layer to Use

```
Need to process raw request before routing?
├─ YES → Middleware (logging, CORS, rate limiting)
└─ NO → Does it decide allow/deny for a route?
    ├─ YES → Guard (auth, roles, permissions)
    └─ NO → Does it transform/validate input data?
        ├─ YES → Pipe (validation, type coercion)
        └─ NO → Does it wrap handler execution?
            ├─ YES → Interceptor (timing, caching, response mapping)
            └─ NO → Does it handle errors?
                ├─ YES → Exception Filter
                └─ NO → Put it in the service layer
```

### Module Organization

```
Is this a cross-cutting concern (auth, config, logging)?
├─ YES → Global module or shared module
└─ NO → Is it a business feature (users, orders, products)?
    ├─ YES → Feature module (users.module.ts)
    └─ NO → Is it infrastructure (database, cache, queue)?
        ├─ YES → Infrastructure module
        └─ NO → Part of the closest feature module
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Putting business logic in controllers instead of services
- Missing `@Injectable()` on services (DI fails silently at runtime)
- Not enabling `ValidationPipe` globally (DTOs are not validated)
- Using `any` for request body instead of typed DTOs
- Instantiating services with `new` instead of constructor injection
- Throwing raw `Error` instead of NestJS HTTP exceptions (produces 500 instead of proper status)

**Medium Priority Issues:**

- Not exporting services from modules (other modules can't import them)
- Importing the entire module when you only need one service
- Missing `whitelist: true` on ValidationPipe (mass-assignment vulnerability)
- Using `@Res()` decorator outside streaming scenarios (opts out of NestJS response handling)
- Not using `PartialType` / `PickType` / `OmitType` for update DTOs (duplicated validation)

**Common Mistakes:**

- Circular module dependencies — restructure with `forwardRef()` or extract shared logic
- Forgetting to register providers in the module — service injection fails at runtime
- Using synchronous guards for async operations — return `Promise<boolean>` or `Observable<boolean>`
- Not handling all exception types in custom filters — always have a catch-all for unknown errors

**Gotchas and Edge Cases:**

- `@UseGuards(AuthGuard)` takes a class reference, not an instance — NestJS instantiates via DI
- `ValidationPipe` with `transform: true` converts query params to their declared types automatically
- Guards execute AFTER middleware but BEFORE interceptors and pipes
- `@Catch()` with no arguments catches ALL exceptions, not just HttpException
- `IntrinsicException` (NestJS 11) throws without framework auto-logging — useful for expected flow control
- NestJS 11: Termination lifecycle hooks (`OnModuleDestroy`, `OnApplicationShutdown`) now execute in reverse order
- NestJS 11: Express v5 requires named wildcards (`/*splat` instead of `/*`)
- NestJS 11: SWC is the default compiler (20x faster builds)
- NestJS 11: `ParseDatePipe` is now built-in — no need for custom date parsing pipes
- Request-scoped providers (`Scope.REQUEST`) affect performance — use only when needed
- `forwardRef()` should be a last resort — circular deps usually signal a design issue

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@Injectable()` on every service and register it in the module `providers` array)**

**(You MUST enable `ValidationPipe` globally with `whitelist: true` and `forbidNonWhitelisted: true`)**

**(You MUST use DTOs with class-validator decorators for ALL request body validation — never validate manually in controllers)**

**(You MUST throw NestJS built-in HTTP exceptions (`NotFoundException`, `BadRequestException`, etc.) — never send raw status codes)**

**(You MUST use constructor injection for dependencies — never instantiate services manually with `new`)**

**Failure to follow these rules will produce unvalidated, untestable NestJS code with broken dependency injection.**

</critical_reminders>
