---
name: nestjs
description: |
  NestJS modular API architecture with controllers, services, guards, middleware, and dependency injection patterns.
  Use when: building API endpoints, implementing services, creating guards/interceptors, handling authentication/authorization, or any backend business logic with NestJS
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# NestJS Skill

NestJS provides a structured, Angular-inspired architecture for Node.js backends. It enforces separation of concerns through modules, controllers, and services with built-in dependency injection. Use decorators for routing, validation, and metadata.

## Quick Start

### Module Structure

```typescript
// src/products/products.module.ts
@Module({
  imports: [TypeOrmModule.forFeature([Product])],
  controllers: [ProductsController],
  providers: [ProductsService],
  exports: [ProductsService],
})
export class ProductsModule {}
```

### Controller Pattern

```typescript
// src/products/products.controller.ts
@Controller('products')
export class ProductsController {
  constructor(private readonly productsService: ProductsService) {}

  @Get()
  findAll(@Query() query: FindProductsDto) {
    return this.productsService.findAll(query);
  }

  @Post()
  @UseGuards(JwtAuthGuard)
  create(@Body() dto: CreateProductDto, @Request() req) {
    return this.productsService.create(dto, req.user.id);
  }
}
```

### Service Pattern

```typescript
// src/products/products.service.ts
@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private readonly productRepo: Repository<Product>,
  ) {}

  async findAll(query: FindProductsDto): Promise<Product[]> {
    return this.productRepo.find({ where: query });
  }
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Module | Feature boundary, DI container | `@Module({ providers: [...] })` |
| Controller | HTTP routing, request handling | `@Controller('users')` |
| Service | Business logic, injectable | `@Injectable()` |
| Guard | Auth/authorization checks | `@UseGuards(AuthGuard)` |
| Pipe | Validation, transformation | `@UsePipes(ValidationPipe)` |
| Interceptor | Response transformation, logging | `@UseInterceptors(LoggingInterceptor)` |

## Common Patterns

### Global Validation

```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}));
```

### Exception Filter

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    
    response.status(status).json({
      statusCode: status,
      message: exception.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

## See Also

- [routes](references/routes.md) - Controller routing patterns
- [services](references/services.md) - Service layer and DI
- [database](references/database.md) - TypeORM/Prisma integration
- [auth](references/auth.md) - Guards and authentication
- [errors](references/errors.md) - Exception handling

## Related Skills

- See the **typescript** skill for strict typing patterns
- See the **prisma** skill for database ORM alternative to TypeORM
- See the **postgresql** skill for database design
- See the **zod** skill for runtime validation
- See the **jest** skill for unit testing NestJS services