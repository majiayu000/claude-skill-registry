---
name: nestjs-best-practices
description: Provides comprehensive NestJS best practices including modular architecture, dependency injection scoping, exception filters, DTO validation with class-validator, and Drizzle ORM integration. Use when designing NestJS modules, implementing providers, creating exception filters, validating DTOs, or integrating Drizzle ORM within NestJS applications.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# NestJS Best Practices

## Overview

This skill provides a curated set of best practices for building production-grade NestJS applications. All guidelines are grounded in the [Official NestJS Documentation](https://docs.nestjs.com/) and enforce consistent, maintainable, and scalable patterns.

## When to Use

- Designing or refactoring NestJS module architecture
- Implementing dependency injection with custom or scoped providers
- Creating exception filters and standardizing error responses
- Validating DTOs with `class-validator` and `ValidationPipe`
- Integrating Drizzle ORM within NestJS providers
- Reviewing NestJS code for architectural anti-patterns
- Onboarding new developers to a NestJS codebase

## Instructions

### 1. Modular Architecture

Follow strict module encapsulation. Each domain feature should be its own `@Module()`:

- Export only what other modules need — keep internal providers private
- Use `forwardRef()` only as a last resort for circular dependencies; prefer restructuring
- Group related controllers, services, and repositories within the same module
- Use a `SharedModule` for cross-cutting concerns (logging, configuration, caching)

See `references/arch-module-boundaries.md` for enforcement rules.

### 2. Dependency Injection

Choose the correct provider scope based on use case:

| Scope       | Lifecycle                    | Use Case                                   |
|-------------|------------------------------|---------------------------------------------|
| `DEFAULT`   | Singleton (shared)           | Stateless services, repositories            |
| `REQUEST`   | Per-request instance         | Request-scoped data (tenant, user context)  |
| `TRANSIENT` | New instance per injection   | Stateful utilities, per-consumer caches     |

- Default to `DEFAULT` scope — only use `REQUEST` or `TRANSIENT` when justified
- Use constructor injection exclusively — avoid property injection
- Register custom providers with `useClass`, `useValue`, `useFactory`, or `useExisting`

See `references/di-provider-scoping.md` for enforcement rules.

### 3. Request Lifecycle

Understand and respect the NestJS request processing pipeline:

```
Middleware → Guards → Interceptors (before) → Pipes → Route Handler → Interceptors (after) → Exception Filters
```

- **Middleware**: Cross-cutting concerns (logging, CORS, body parsing)
- **Guards**: Authorization and authentication checks (return `true`/`false`)
- **Interceptors**: Transform response data, add caching, measure timing
- **Pipes**: Validate and transform input parameters
- **Exception Filters**: Catch and format error responses

### 4. Error Handling

Standardize error responses across the application:

- Extend `HttpException` for HTTP-specific errors
- Create domain-specific exception classes (e.g., `OrderNotFoundException`)
- Implement a global `ExceptionFilter` for consistent error formatting
- Use the Result pattern for expected business logic failures
- Never silently swallow exceptions

See `references/error-exception-filters.md` for enforcement rules.

### 5. Validation

Enforce input validation at the API boundary:

- Enable `ValidationPipe` globally with `transform: true` and `whitelist: true`
- Decorate all DTO properties with `class-validator` decorators
- Use `class-transformer` for type coercion (`@Type()`, `@Transform()`)
- Create separate DTOs for Create, Update, and Response operations
- Never trust raw user input — validate everything

See `references/api-validation-dto.md` for enforcement rules.

### 6. Database Patterns (Drizzle ORM)

Integrate Drizzle ORM following NestJS provider conventions:

- Wrap the Drizzle client in an injectable provider
- Use the Repository pattern for data access encapsulation
- Define schemas in dedicated schema files per domain module
- Use transactions for multi-step operations
- Keep database logic out of controllers

See `references/db-drizzle-patterns.md` for enforcement rules.

## Best Practices

| Area               | Do                                      | Don't                                    |
|--------------------|------------------------------------------|------------------------------------------|
| Modules            | One module per domain feature            | Dump everything in `AppModule`           |
| DI Scoping         | Default to singleton scope               | Use `REQUEST` scope without justification|
| Error Handling     | Custom exception filters + domain errors | Bare `try/catch` with `console.log`      |
| Validation         | Global `ValidationPipe` + DTO decorators | Manual `if` checks in controllers        |
| Database           | Repository pattern with injected client  | Direct DB queries in controllers         |
| Testing            | Unit test services, e2e test controllers | Skip tests or test implementation details|
| Configuration      | `@nestjs/config` with typed schemas      | Hardcode values or use `process.env`     |

## Examples

### Example 1: Creating a New Domain Module

When building a new "Product" feature:

```typescript
// product/product.module.ts
@Module({
  imports: [DatabaseModule],
  controllers: [ProductController],
  providers: [ProductService, ProductRepository],
  exports: [ProductService],
})
export class ProductModule {}
```

### Example 2: DTO with Full Validation

```typescript
// product/dto/create-product.dto.ts
import { IsString, IsNumber, IsPositive, MaxLength } from 'class-validator';

export class CreateProductDto {
  @IsString()
  @MaxLength(255)
  readonly name: string;

  @IsNumber()
  @IsPositive()
  readonly price: number;
}
```

### Example 3: Service with Proper Error Handling

```typescript
@Injectable()
export class ProductService {
  constructor(private readonly productRepository: ProductRepository) {}

  async findById(id: string): Promise<Product> {
    const product = await this.productRepository.findById(id);
    if (product === null) {
      throw new ProductNotFoundException(id);
    }
    return product;
  }
}
```

## Constraints and Warnings

1. **Do not mix scopes without justification** — `REQUEST`-scoped providers cascade to all dependents
2. **Never access database directly from controllers** — always go through service and repository layers
3. **Avoid `forwardRef()`** — restructure modules to eliminate circular dependencies
4. **Do not skip `ValidationPipe`** — always validate at the API boundary with DTOs
5. **Never hardcode secrets** — use `@nestjs/config` with environment variables
6. **Keep modules focused** — one domain feature per module, avoid "god modules"

## References

- `references/architecture.md` — Deep-dive into NestJS architectural patterns
- `references/` — Individual enforcement rules with correct/incorrect examples
- `assets/templates/` — Starter templates for common NestJS components
