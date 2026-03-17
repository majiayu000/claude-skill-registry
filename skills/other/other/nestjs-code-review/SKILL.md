---
name: nestjs-code-review
description: Provides comprehensive code review capability for NestJS applications, analyzing controllers, services, modules, guards, interceptors, pipes, dependency injection, and database integration patterns. Use when reviewing NestJS code changes, before merging pull requests, after implementing new features, or for architecture validation. Triggers on "review NestJS code", "NestJS code review", "check my NestJS controller/service".
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# NestJS Code Review

## Overview

This skill provides structured, comprehensive code review for NestJS applications. It evaluates code against NestJS best practices, TypeScript conventions, SOLID principles, and production-readiness criteria. The review produces actionable findings categorized by severity (Critical, Warning, Suggestion) with concrete code examples for improvements.

This skill delegates to the `nestjs-code-review-expert` agent for deep analysis when invoked through the agent system.

## When to Use

- Reviewing NestJS controllers, services, modules, or providers before merging
- Validating proper use of decorators (`@Controller`, `@Injectable`, `@Module`, etc.)
- Checking dependency injection patterns and provider scoping
- Reviewing REST API endpoints for standards compliance
- Evaluating error handling with exception filters
- Assessing guard and interceptor implementations
- Reviewing database integration (TypeORM, Prisma, Drizzle ORM)
- Validating DTO definitions and validation pipes
- After implementing new NestJS features or refactoring modules
- Checking microservices patterns (message/event patterns, transport layers)

## Instructions

1. **Identify Scope**: Determine which NestJS files and modules are under review. Use `glob` and `grep` to discover controllers, services, modules, guards, interceptors, and pipes in the target area.

2. **Analyze Module Structure**: Verify proper module organization — each feature should have its own module with clearly defined imports, controllers, providers, and exports. Check for circular dependencies and proper module boundaries.

3. **Review Dependency Injection**: Validate that all injectable services use constructor injection. Check provider scoping (singleton, request, transient) matches the intended lifecycle. Ensure no direct instantiation bypasses the DI container.

4. **Evaluate Controllers**: Review HTTP method usage, route naming, status codes, request/response DTOs, validation pipes, and OpenAPI decorators. Confirm controllers are thin — business logic belongs in services.

5. **Assess Services & Business Logic**: Check that services encapsulate business logic properly. Verify error handling, transaction management, and proper separation from infrastructure concerns. Look for service methods that are too large or have too many responsibilities.

6. **Check Security**: Review guard implementations, authentication/authorization patterns, input validation with class-validator, and protection against common vulnerabilities (injection, XSS, CSRF).

7. **Review Testing**: Assess test coverage for controllers, services, guards, and pipes. Verify proper mocking strategies and that tests validate behavior, not implementation details.

8. **Produce Review Report**: Generate a structured report with severity-classified findings (Critical, Warning, Suggestion), positive observations, and prioritized recommendations with code examples.

## Examples

### Example 1: Reviewing a Controller

```typescript
// ❌ Bad: Fat controller with business logic and missing validation
@Controller('users')
export class UserController {
  constructor(private readonly userRepo: Repository<User>) {}

  @Post()
  async create(@Body() body: any) {
    const user = this.userRepo.create(body);
    return this.userRepo.save(user);
  }
}

// ✅ Good: Thin controller with proper DTOs, validation, and service delegation
@Controller('users')
@ApiTags('Users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create a new user' })
  @ApiResponse({ status: 201, type: UserResponseDto })
  async create(
    @Body(ValidationPipe) createUserDto: CreateUserDto,
  ): Promise<UserResponseDto> {
    return this.userService.create(createUserDto);
  }
}
```

### Example 2: Reviewing Dependency Injection

```typescript
// ❌ Bad: Direct instantiation bypasses DI
@Injectable()
export class OrderService {
  private readonly logger = new Logger();
  private readonly emailService = new EmailService();

  async createOrder(dto: CreateOrderDto) {
    this.emailService.send(dto.email, 'Order created');
  }
}

// ✅ Good: Proper constructor injection
@Injectable()
export class OrderService {
  private readonly logger = new Logger(OrderService.name);

  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly emailService: EmailService,
  ) {}

  async createOrder(dto: CreateOrderDto): Promise<Order> {
    const order = await this.orderRepository.create(dto);
    await this.emailService.send(dto.email, 'Order created');
    return order;
  }
}
```

### Example 3: Reviewing Error Handling

```typescript
// ❌ Bad: Generic error handling with information leakage
@Get(':id')
async findOne(@Param('id') id: string) {
  try {
    return await this.service.findOne(id);
  } catch (error) {
    throw new HttpException(error.message, 500);
  }
}

// ✅ Good: Domain-specific exceptions with proper HTTP mapping
@Get(':id')
async findOne(@Param('id', ParseUUIDPipe) id: string): Promise<UserResponseDto> {
  const user = await this.userService.findOne(id);
  if (!user) {
    throw new NotFoundException(`User with ID ${id} not found`);
  }
  return user;
}
```

### Example 4: Reviewing Guard Implementation

```typescript
// ❌ Bad: Authorization logic in controller
@Get('admin/dashboard')
async getDashboard(@Req() req: Request) {
  if (req.user.role !== 'admin') {
    throw new ForbiddenException();
  }
  return this.dashboardService.getData();
}

// ✅ Good: Guard-based authorization with decorator
@Get('admin/dashboard')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
async getDashboard(): Promise<DashboardDto> {
  return this.dashboardService.getData();
}
```

### Example 5: Reviewing Module Organization

```typescript
// ❌ Bad: Monolithic module with everything
@Module({
  imports: [TypeOrmModule.forFeature([User, Order, Product, Review])],
  controllers: [UserController, OrderController, ProductController],
  providers: [UserService, OrderService, ProductService, ReviewService],
})
export class AppModule {}

// ✅ Good: Feature-based module organization
@Module({
  imports: [UserModule, OrderModule, ProductModule],
})
export class AppModule {}

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService, UserRepository],
  exports: [UserService],
})
export class UserModule {}
```

## Review Output Format

Structure all code review findings as follows:

### 1. Summary
Brief overview with an overall quality score (1-10) and key observations.

### 2. Critical Issues (Must Fix)
Issues that could cause security vulnerabilities, data corruption, or production failures.

### 3. Warnings (Should Fix)
Issues that violate best practices, reduce maintainability, or could lead to bugs.

### 4. Suggestions (Consider Improving)
Improvements for code readability, performance, or developer experience.

### 5. Positive Observations
Well-implemented patterns and good practices to acknowledge and encourage.

### 6. Recommendations
Prioritized next steps with code examples for the most impactful improvements.

## Best Practices

- Controllers should be thin — delegate all business logic to services
- Use DTOs with class-validator for all request/response payloads
- Apply `ParseUUIDPipe`, `ParseIntPipe`, etc. for parameter validation
- Use domain-specific exception classes extending `HttpException`
- Organize code into feature modules with clear boundaries and exports
- Prefer constructor injection — never use `new` for injectable services
- Apply guards for authentication and authorization, not inline checks
- Use interceptors for cross-cutting concerns (logging, caching, transformation)
- Add OpenAPI decorators (`@ApiTags`, `@ApiOperation`, `@ApiResponse`) to all endpoints
- Write unit tests for services and integration tests for controllers

## Constraints and Warnings

- Do not enforce a single ORM — the codebase may use TypeORM, Prisma, Drizzle, or MikroORM
- Respect existing project conventions even if they differ from NestJS defaults
- Focus on high-confidence issues — avoid false positives on style preferences
- When reviewing microservices patterns, consider transport-layer specific constraints
- Do not suggest architectural rewrites unless critical issues warrant them

## References

See the `references/` directory for detailed review checklists and pattern documentation:
- `references/patterns.md` — NestJS best practice patterns with examples
- `references/anti-patterns.md` — Common NestJS anti-patterns to flag during review
- `references/checklist.md` — Comprehensive review checklist organized by area
