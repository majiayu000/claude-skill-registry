---
name: vendix-backend-api
description: API endpoint patterns.
metadata:
  scope: [root]
  auto_invoke: "Creating API endpoints"
---
# Vendix Backend API Patterns

> **API Response Pattern** - Respuestas estandarizadas, DTOs y estructura de controladores.

## 🎯 Standard API Response

### ResponseService

**File:** `common/responses/response.service.ts`

```typescript
import { Injectable } from '@nestjs/common';

interface SuccessResponse<T> {
  success: true;
  data: T;
  message?: string;
  meta?: any;
}

interface ErrorResponse {
  success: false;
  error: {
    message: string;
    code?: string;
    details?: any;
  };
}

@Injectable()
export class ResponseService {
  success<T>(data: T, message?: string, meta?: any): SuccessResponse<T> {
    return {
      success: true,
      data,
      message,
      meta,
    };
  }

  error(message: string, code?: string, details?: any): ErrorResponse {
    return {
      success: false,
      error: {
        message,
        code,
        details,
      },
    };
  }

  paginated<T>(data: T[], meta: PaginationMeta) {
    return this.success(data, undefined, { pagination: meta });
  }
}

interface PaginationMeta {
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}
```

---
metadata:
  scope: [root]
  auto_invoke: "Creating API endpoints"

## 📦 Controller Pattern

### Standard Controller Structure

```typescript
import { Controller, Get, Post, Put, Delete, Body, Param, Query } from '@nestjs/common';
import { {Domain}Service } from './{domain}.service';
import { ResponseService } from '@/common/responses/response.service';
import { {Action}Dto } from './dto/{action}-dto.dto';
import { Public } from '@/common/decorators/public.decorator';
import { Permissions } from '@/common/decorators/permissions.decorator';

@Controller('domains/:domain_id/{resource}')  // Multi-tenant route
export class {Resource}Controller {
  constructor(
    private readonly {resource}_service: {Resource}Service,
    private readonly response_service: ResponseService,
  ) {}

  @Get()
  async findAll(@Query() query_dto: Query{Resource}Dto) {
    const result = await this.{resource}_service.findAll(query_dto);
    return this.response_service.paginated(result.data, result.meta);
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    const result = await this.{resource}_service.findOne(+id);
    return this.response_service.success(result);
  }

  @Post()
  @Permissions('{resource}:write')
  async create(@Body() create_dto: Create{Resource}Dto) {
    const result = await this.{resource}_service.create(create_dto);
    return this.response_service.success(result, 'Created successfully');
  }

  @Put(':id')
  @Permissions('{resource}:write')
  async update(@Param('id') id: string, @Body() update_dto: Update{Resource}Dto) {
    const result = await this.{resource}_service.update(+id, update_dto);
    return this.response_service.success(result, 'Updated successfully');
  }

  @Delete(':id')
  @Permissions('{resource}:delete')
  async remove(@Param('id') id: string) {
    await this.{resource}_service.remove(+id);
    return this.response_service.success(null, 'Deleted successfully');
  }
}
```

---

## 📝 DTO Patterns

### Create DTO

```typescript
import { IsString, IsEmail, IsOptional, MinLength, IsNumber, IsBoolean } from 'class-validator';

export class CreateUserDto {
  @IsString()
  @MinLength(3)
  user_name: string;

  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;

  @IsOptional()
  @IsString()
  phone_number?: string;

  @IsOptional()
  @IsBoolean()
  is_active?: boolean = true;
}
```

### Update DTO (Partial)

```typescript
import { PartialType } from '@nestjs/mapped-types';
import { CreateUserDto } from './create-user.dto';

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

### Query DTO

```typescript
import { IsOptional, IsString, IsNumber, IsBoolean } from 'class-validator';
import { Type } from 'class-transformer';

export class QueryUserDto {
  @IsOptional()
  @IsString()
  search?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  page?: number = 1;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  limit?: number = 10;

  @IsOptional()
  @IsString()
  sort_by?: string = 'created_at';

  @IsOptional()
  @IsString()
  sort_order?: 'asc' | 'desc' = 'desc';

  @IsOptional()
  @IsBoolean()
  include_deleted?: boolean = false;
}
```

---

## 🔄 Service Response Pattern

### Standard Service Methods

```typescript
@Injectable()
export class UserService {
  constructor(
    private readonly prisma: EcommercePrismaService,
    private readonly response_service: ResponseService,
  ) {}

  async findAll(query: QueryUserDto) {
    const { page, limit, search, sort_by, sort_order } = query;

    const skip = (page - 1) * limit;

    const where = {
      ...this.prisma.organizationWhere,
      ...(search && {
        OR: [
          { user_name: { contains: search, mode: 'insensitive' } },
          { email: { contains: search, mode: 'insensitive' } },
        ],
      }),
    };

    const [data, total] = await Promise.all([
      this.prisma.users.findMany({
        where,
        skip,
        take: limit,
        orderBy: { [sort_by]: sort_order },
      }),
      this.prisma.users.count({ where }),
    ]);

    return {
      data,
      meta: {
        total,
        page,
        limit,
        total_pages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(id: number) {
    const user = await this.prisma.users.findFirst({
      where: {
        id,
        ...this.prisma.organizationWhere,
      },
    });

    if (!user) {
      throw new NotFoundException('User not found');
    }

    return user;
  }

  async create(create_dto: CreateUserDto) {
    // Check if email exists
    const existing = await this.prisma.users.findUnique({
      where: { email: create_dto.email },
    });

    if (existing) {
      throw new ConflictException('Email already exists');
    }

    // Hash password
    const hashed_password = await bcrypt.hash(create_dto.password, 10);

    // Create user
    const user = await this.prisma.users.create({
      data: {
        ...create_dto,
        password: hashed_password,
        organization_id: this.prisma.context.organization_id,
      },
      select: {
        id: true,
        user_name: true,
        email: true,
        phone_number: true,
        is_active: true,
        created_at: true,
      },  // Exclude password from response
    });

    return user;
  }

  async update(id: number, update_dto: UpdateUserDto) {
    await this.findOne(id);  // Check existence

    if (update_dto.password) {
      update_dto.password = await bcrypt.hash(update_dto.password, 10);
    }

    const user = await this.prisma.users.update({
      where: { id },
      data: update_dto,
      select: {
        id: true,
        user_name: true,
        email: true,
        phone_number: true,
        is_active: true,
        updated_at: true,
      },
    });

    return user;
  }

  async remove(id: number) {
    await this.findOne(id);  // Check existence

    await this.prisma.users.delete({
      where: { id },
    });
  }
}
```

---

## 🌐 HTTP Status Codes

### Standard Status Codes

| Scenario | Status Code | Description |
|----------|-------------|-------------|
| Success | 200 | Request succeeded |
| Created | 201 | Resource created |
| No Content | 204 | Success, no response body |
| Bad Request | 400 | Invalid input |
| Unauthorized | 401 | Not authenticated |
| Forbidden | 403 | Authenticated but not authorized |
| Not Found | 404 | Resource not found |
| Conflict | 409 | Resource conflict (duplicate) |
| Unprocessable Entity | 422 | Validation error |
| Internal Server Error | 500 | Server error |

### Usage in Controllers

```typescript
@Post()
@HttpCode(HttpStatus.CREATED)  // 201
async create(@Body() dto: CreateDto) {
  return this.service.create(dto);
}

@Delete(':id')
@HttpCode(HttpStatus.NO_CONTENT)  // 204
async remove(@Param('id') id: string) {
  await this.service.remove(+id);
}
```

---

## 🎯 Error Handling

### Exception Filters

**File:** `common/filters/http-exception.filter.ts`

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException } from '@nestjs/common';
import { Response } from 'express';

@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception.getStatus();
    const exception_response = exception.getResponse();

    const error_response = {
      success: false,
      error: {
        message: exception.message,
        code: exception.name,
        details: exception_response,
      },
    };

    response.status(status).json(error_response);
  }
}
```

### Global Exception Filter

**File:** `main.ts`

```typescript
import { ValidationPipe } from '@nestjs/common';
import { HttpExceptionFilter } from './common/filters/http-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,  // Strip properties not in DTO
      transform: true,  // Auto-transform types
      forbidNonWhitelisted: true,  // Throw error for non-whitelisted
    }),
  );

  app.useGlobalFilters(new HttpExceptionFilter());

  await app.listen(3000);
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `common/responses/response.service.ts` | Standardized responses |
| `common/filters/http-exception.filter.ts` | Global error handling |
| `main.ts` | Global pipes and filters |
| `dto/*.dto.ts` | Data transfer objects |

---

## Related Skills

- `vendix-backend-domain` - Domain architecture
- `vendix-backend-auth` - Authentication and authorization
- `vendix-validation` - Validation patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
