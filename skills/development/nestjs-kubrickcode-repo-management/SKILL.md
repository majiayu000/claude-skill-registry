---
name: nestjs
description: |
  Provides NestJS framework development standards and architectural patterns. Ensures domain-centric architecture, proper dependency injection, and decorator pattern utilization. Specializes in modular design, providers and services, middleware and guards, interceptors and pipes, custom decorators, and microservices architecture.
  Use when: developing NestJS applications, designing module structure (@Module), creating controllers (@Controller) and services (@Injectable), implementing REST or GraphQL APIs, configuring dependency injection, building middleware and guards, creating custom decorators, implementing authentication/authorization, designing microservices with NestJS, or integrating with TypeORM/Prisma for database access.
---

# NestJS Development Standards

## Module Organization Principles

### Domain-Centric Modularization

Organize modules by business domain, not by function.

- ❌ Bad: `controllers/`, `services/`, `repositories/`
- ✅ Good: `users/`, `products/`, `orders/`

### Single Responsibility Module

Each module is responsible for only one domain.

- Separate common functionality into `common/` or `shared/` modules
- Inter-domain communication must go through Services only

## Dependency Injection Rules

### Constructor Injection Only

Property injection (@Inject) is forbidden.

```typescript
// ✅ Good
constructor(private readonly userService: UserService) {}

// ❌ Bad
@Inject() userService: UserService;
```

### Provider Registration Location

Providers are registered only in the module where they are used.

- Minimize global providers
- Use forRoot/forRootAsync only in AppModule

## Decorator Usage Rules

### Prioritize Custom Decorators

Abstract repeated decorator combinations into custom decorators.

```typescript
// Create custom decorator when combining 3+ decorators
@Auth() // Integrates @UseGuards + @ApiBearerAuth + @CurrentUser
```

### Decorator Order

Arrange in execution order from top to bottom.

1. Metadata decorators (@ApiTags, @Controller, @Resolver)
2. Guards/Interceptors (@UseGuards, @UseInterceptors)
3. Route decorators (@Get, @Post, @Query, @Mutation)
4. Parameter decorators (@Body, @Param, @Args)

## DTO/Entity Rules

### DTO is Pure Data Transfer

Business logic is forbidden; only validation is allowed.

```typescript
// ✅ Good: Validation only
class CreateUserDto {
  @IsEmail()
  email: string;
}

// ❌ Bad: Contains business logic
class CreateUserDto {
  toEntity(): User {} // Forbidden
}
```

### Separate Entity and DTO

Never return Entity directly; always convert to DTO.

- Request: CreateInput, UpdateInput (GraphQL) / CreateDto, UpdateDto (REST)
- Response: Type definition or plain object

## Error Handling

### Domain-Specific Exception Filter

Each domain has its own Exception Filter.

```typescript
@Module({
  providers: [
    {
      provide: APP_FILTER,
      useClass: UserExceptionFilter,
    },
  ],
})
```

### Explicit Error Throwing

Always throw Exception explicitly in all error situations.

- REST: Use HttpException series
- GraphQL: Use GraphQLError or custom error
- Forbid implicit null/undefined returns
- Error messages should be understandable by users
