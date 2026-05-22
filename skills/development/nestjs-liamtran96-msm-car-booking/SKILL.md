---
name: nestjs
description: NestJS - A progressive Node.js framework for building efficient, scalable server-side applications with TypeScript.
---

# NestJS Framework

NestJS is a progressive Node.js framework for building efficient, scalable server-side applications. It uses TypeScript and combines elements of OOP, FP, and FRP.

## When to Use This Skill

Use this skill when:
- Building Node.js backend applications with TypeScript
- Working with NestJS controllers, providers, and modules
- Implementing guards, pipes, interceptors, and middleware
- Setting up authentication and authorization
- Building microservices or GraphQL APIs
- Working with WebSockets
- Configuring the NestJS CLI

## Quick Reference

### Basic Controller

```typescript
import { Controller, Get, Post, Body, Param } from '@nestjs/common';

@Controller('users')
export class UsersController {
  @Get()
  findAll() {
    return [];
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return { id };
  }

  @Post()
  create(@Body() createDto: CreateUserDto) {
    return createDto;
  }
}
```

### Basic Provider/Service

```typescript
import { Injectable } from '@nestjs/common';

@Injectable()
export class UsersService {
  private users = [];

  findAll() {
    return this.users;
  }

  findOne(id: string) {
    return this.users.find(u => u.id === id);
  }
}
```

### Basic Module

```typescript
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService]
})
export class UsersModule {}
```

### Guard Example

```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return !!request.headers.authorization;
  }
}
```

### Pipe Example

```typescript
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

@Injectable()
export class ParseIntPipe implements PipeTransform<string, number> {
  transform(value: string): number {
    const val = parseInt(value, 10);
    if (isNaN(val)) {
      throw new BadRequestException('Validation failed');
    }
    return val;
  }
}
```

### Interceptor Example

```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');
    const now = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`After... ${Date.now() - now}ms`)),
    );
  }
}
```

### Exception Filter Example

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();

    response.status(status).json({
      statusCode: status,
      message: exception.message,
    });
  }
}
```

### Middleware Example

```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    console.log(`${req.method} ${req.url}`);
    next();
  }
}
```

## Key Concepts

### Dependency Injection
NestJS uses a powerful dependency injection system. Mark classes with `@Injectable()` and inject them via constructor parameters.

### Decorators
NestJS makes heavy use of decorators:
- `@Controller()` - Define a controller
- `@Get()`, `@Post()`, `@Put()`, `@Delete()` - HTTP methods
- `@Injectable()` - Mark a class as a provider
- `@Module()` - Define a module
- `@UseGuards()`, `@UsePipes()`, `@UseInterceptors()` - Apply cross-cutting concerns

### Request Lifecycle
1. Middleware
2. Guards
3. Interceptors (pre)
4. Pipes
5. Route Handler
6. Interceptors (post)
7. Exception Filters

## Documentation Reference

See the `references/` folder for detailed documentation on:

- [Getting Started](references/getting_started.md) - First steps, introduction (7 pages)
- [Fundamentals](references/fundamentals.md) - Controllers, providers, modules, DI (30 pages)
- [Techniques](references/techniques.md) - Database, validation, caching, etc. (27 pages)
- [Security](references/security.md) - Authentication, authorization (6 pages)
- [GraphQL](references/graphql.md) - Apollo, resolvers, mutations (17 pages)
- [Microservices](references/microservices.md) - Redis, Kafka, gRPC, NATS (10 pages)
- [WebSockets](references/websockets.md) - Gateways, adapters (5 pages)
- [OpenAPI](references/openapi.md) - Swagger documentation (5 pages)
- [CLI](references/cli.md) - Workspaces, libraries (5 pages)
- [Recipes](references/recipes.md) - CQRS, Prisma, health checks (12 pages)
