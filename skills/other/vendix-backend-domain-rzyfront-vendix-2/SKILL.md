---
name: vendix-backend-domain
description: Hexagonal architecture and domain structure.
metadata:
  scope: [root]
  auto_invoke: "Working on backend domains"
---
# Vendix Backend Domain Architecture

> **Backend Domain Pattern** - Arquitectura hexagonal basada en dominios con separación clara de responsabilidades.

## 🏗️ Domain Architecture

Vendix backend sigue una **arquitectura hexagonal basada en dominios**, donde cada dominio representa un área de negocio claramente delimitada.

### Structure

```
apps/backend/src/domains/
├── auth/                    # Autenticación y JWT
│   ├── auth.module.ts
│   ├── auth.controller.ts
│   ├── auth.service.ts
│   ├── dto/
│   │   ├── login.dto.ts
│   │   ├── register.dto.ts
│   │   └── refresh-token.dto.ts
│   └── interfaces/
│       └── auth.interface.ts
│
├── organization/            # Organizaciones y usuarios
│   ├── organization.module.ts
│   ├── organization.controller.ts
│   ├── organization.service.ts
│   ├── dto/
│   └── interfaces/
│
├── store/                   # Tiendas
│   ├── store.module.ts
│   ├── store.controller.ts
│   ├── store.service.ts
│   ├── settings/            # NUEVO: Store settings (branding, fonts, ecommerce)
│   │   ├── settings.service.ts
│   │   ├── interfaces/
│   │   │   └── store-settings.interface.ts
│   │   └── defaults/
│   │       └── default-store-settings.ts
│   ├── products/
│   ├── brands/
│   ├── categories/
│   └── ecommerce/           # Ecommerce operations
│
├── ecommerce/               # Catálogo público de e-commerce
│   ├── catalog/
│   ├── cart/
│   ├── checkout/
│   ├── wishlist/
│   └── account/
│
├── superadmin/              # Administración global del sistema
│   ├── superadmin.module.ts
│   ├── system-management.controller.ts
│   └── system.service.ts
│
├── public/                  # Dominios públicos (landing pages)
│   └── domains/
│       ├── public-domains.module.ts
│       ├── public-domains.controller.ts
│       └── public-domains.service.ts
│
└── common/                  # Utilidades compartidas
    ├── middleware/
    ├── guards/
    ├── decorators/
    ├── interceptors/
    ├── context/
    ├── services/            # S3, helpers, etc.
    └── responses/
```

---

## 🔄 App Type Standard (NEW)

### App Type Enum

The backend uses a unified `app_type_enum` across the entire system:

```prisma
enum app_type_enum {
  VENDIX_LANDING     # Public: Vendix SaaS landing
  VENDIX_ADMIN       # Private: Super admin panel
  ORG_LANDING        # Public: Organization landing
  ORG_ADMIN          # Private: Organization admin
  STORE_LANDING      # Public: Store landing
  STORE_ADMIN        # Private: Store admin panel
  STORE_ECOMMERCE    # Public: Store e-commerce
}

model domain_settings {
  app_type  app_type_enum  @default(VENDIX_LANDING) // <--- Source of Truth
  config    Json?                                      // Now nullable (legacy)
  // ...
}

model user_settings {
  app_type  app_type_enum  @default(STORE_ADMIN) // Override post-login
  // ...
}
```

### Domain Resolution

**File:** `domains/public/domains/public-domains.service.ts`

The `resolveDomain()` method now returns:
- `app`: Direct from `domain_settings.app_type` (NOT `config.app`)
- `branding`: From `store_settings.settings.branding`
- `fonts`: From `store_settings.settings.fonts`
- `ecommerce`: From `store_settings.settings.ecommerce`
- `publication`: From `store_settings.settings.publication`
- `config`: Legacy (kept for backward compatibility)

---
metadata:
  scope: [root]
  auto_invoke: "Working on backend domains"

## 📦 Domain Module Pattern

Cada dominio sigue este patrón estándar:

### 1. Module File

**File:** `{domain}.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { PrismaModule } from '@/prisma/prisma.module';
import { {Domain}Controller } from './{domain}.controller';
import { {Domain}Service } from './{domain}.service';
import { AuthGuard } from '@/common/guards/auth.guard';

@Module({
  imports: [PrismaModule],
  controllers: [{Domain}Controller],
  providers: [
    {Domain}Service,
    // Add domain-specific providers here
  ],
  exports: [{Domain}Service],
})
export class {Domain}Module {}
```

**Rules:**
- Import `PrismaModule` for database access
- Export services used by other modules
- Use dependency injection properly
- Keep imports minimal

---

### 2. Controller File

**File:** `{domain}.controller.ts`

```typescript
import { Controller, Post, Body, Get, UseGuards } from '@nestjs/common';
import { {Domain}Service } from './{domain}.service';
import { {Action}Dto } from './dto/{action}-dto.dto';
import { AuthGuard } from '@/common/guards/auth.guard';
import { Public } from '@/common/decorators/public.decorator';
import { Permissions } from '@/common/decorators/permissions.decorator';

@Controller('domains/:domain_id/{domain}')  // Multi-tenant route
export class {Domain}Controller {
  constructor(
    private readonly {domain}_service: {Domain}Service,
    private readonly response_service: ResponseService,
  ) {}

  @Public()
  @Post('public-action')
  async publicAction(@Body() dto: {Action}Dto) {
    const result = await this.{domain}_service.publicAction(dto);
    return this.response_service.success(result);
  }

  @UseGuards(AuthGuard)
  @Permissions('{domain}:read')
  @Get()
  async findAll() {
    const result = await this.{domain}_service.findAll();
    return this.response_service.success(result);
  }

  @UseGuards(AuthGuard)
  @Permissions('{domain}:write')
  @Post('create')
  async create(@Body() dto: {Action}Dto) {
    const result = await this.{domain}_service.create(dto);
    return this.response_service.success(result, 'Created successfully');
  }
}
```

**Rules:**
- Inject both domain service and ResponseService
- Use `@Public()` for public endpoints
- Use `@Permissions()` for granular access control
- Always return through `response_service`
- Follow REST conventions

---

### 3. Service File

**File:** `{domain}.service.ts`

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { PrismaService } from '@/prisma/services/prisma.service';
import { RequestContextService } from '@/common/context/request-context.service';

@Injectable()
export class {Domain}Service {
  constructor(
    private readonly prisma: PrismaService,
    private readonly context: RequestContextService,
  ) {}

  async findAll() {
    // Context is automatically applied (organization_id, store_id)
    return this.prisma.{model}.findMany({
      where: {
        organization_id: this.context.organization_id,
        store_id: this.context.store_id,
      },
    });
  }

  async findOne(id: number) {
    const entity = await this.prisma.{model}.findUnique({
      where: { id },
    });

    if (!entity) {
      throw new NotFoundException('{Entity} not found');
    }

    return entity;
  }

  async create(dto: {CreateDto}) {
    // Multi-tenant context is automatic
    return this.prisma.{model}.create({
      data: {
        ...dto,
        organization_id: this.context.organization_id,
        store_id: this.context.store_id,
      },
    });
  }

  async update(id: number, dto: {UpdateDto}) {
    return this.prisma.{model}.update({
      where: { id },
      data: dto,
    });
  }

  async delete(id: number) {
    return this.prisma.{model}.delete({
      where: { id },
    });
  }
}
```

**Rules:**
- Use `RequestContextService` for multi-tenant context
- Never hardcode `organization_id` or `store_id`
- Use dependency injection for PrismaService
- Throw proper exceptions (`NotFoundException`, etc.)
- Return early for validation (early return pattern)

---

## 🔐 Authentication & Authorization

### Public Routes

```typescript
import { Public } from '@/common/decorators/public.decorator';

@Public()
@Post('login')
async login() {
  // Accessible without authentication
}
```

### Protected Routes

```typescript
import { UseGuards } from '@nestjs/common';
import { AuthGuard } from '@/common/guards/auth.guard';

@UseGuards(AuthGuard)
@Get('profile')
async getProfile() {
  // Requires valid JWT
}
```

### Role-Based Access

```typescript
import { Roles } from '@/common/decorators/roles.decorator';

@Roles('super_admin')
@Get('admin-only')
async adminOnly() {
  // Only super_admin role
}
```

### Permission-Based Access

```typescript
import { Permissions } from '@/common/decorators/permissions.decorator';

@Permissions('catalog:write')
@Post('products')
async createProduct() {
  // Requires catalog:write permission
}
```

---

## 🌐 Multi-Tenancy

### Automatic Context Injection

**From:** `app.module.ts`

```typescript
providers: [
  {
    provide: APP_GUARD,
    useClass: AuthGuard,
  },
  RequestContextService,  // Automatic multi-tenant context
],
```

### Usage in Services

```typescript
constructor(
  private readonly context: RequestContextService,
) {}

async createProduct(dto: CreateProductDto) {
  return this.prisma.product.create({
    data: {
      ...dto,
      organization_id: this.context.organization_id,  // Auto-injected
      store_id: this.context.store_id,                // Auto-injected
    },
  });
}
```

**Never bypass the context!** Always use `this.context` for tenant IDs.

---

## 📝 DTOs (Data Transfer Objects)

### Create DTO

```typescript
// dto/create-{entity}.dto.ts
import { IsString, IsEmail, IsOptional, MinLength } from 'class-validator';

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
}
```

### Update DTO

```typescript
// dto/update-{entity}.dto.ts
import { PartialType } from '@nestjs/mapped-types';
import { CreateUserDto } from './create-user.dto';

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

### Query DTO

```typescript
// dto/query-{entity}.dto.ts
import { IsOptional, IsString, IsNumber } from 'class-validator';
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
}
```

---

## 🎯 Domain Routing

### Multi-Tenant Routes

```typescript
@Controller('domains/:domain_id/organizations/:organization_id/{resource}')
export class ResourceController {
  // Routes include domain and organization for multi-tenancy
}
```

### Store-Level Routes

```typescript
@Controller('domains/:domain_id/stores/:store_id/{resource}')
export class StoreResourceController {
  // Store-scoped routes
}
```

---

## 📋 Common Patterns

### Error Handling

```typescript
async findUser(id: number) {
  // Early return for validation
  if (!id || id <= 0) {
    throw new BadRequestException('Invalid ID');
  }

  try {
    const user = await this.prisma.users.findUnique({ where: { id } });

    if (!user) {
      throw new NotFoundException('User not found');
    }

    return user;
  } catch (error) {
    // Handle Prisma errors
    if (error.code === 'P2002') {
      throw new ConflictException('User already exists');
    }
    throw error;
  }
}
```

### Pagination

```typescript
async findAll(query: QueryDto) {
  const page = query.page || 1;
  const limit = query.limit || 10;
  const skip = (page - 1) * limit;

  const [data, total] = await Promise.all([
    this.prisma.resource.findMany({
      skip,
      take: limit,
      where: this.buildWhereClause(query),
    }),
    this.prisma.resource.count({ where: this.buildWhereClause(query) }),
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
```

### Soft Delete

```typescript
async delete(id: number) {
  return this.prisma.resource.update({
    where: { id },
    data: {
      deleted_at: new Date(),
      is_active: false,
    },
  });
}

async findActive() {
  return this.prisma.resource.findMany({
    where: {
      deleted_at: null,
      is_active: true,
    },
  });
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `app.module.ts` | Root module with global guards and context |
| `common/guards/auth.guard.ts` | JWT authentication guard |
| `common/decorators/public.decorator.ts` | Mark public routes |
| `common/decorators/permissions.decorator.ts` | Permission-based access |
| `common/context/request-context.service.ts` | Multi-tenant context |
| `common/responses/response.service.ts` | Standardized responses |
| `domains/public/domains/public-domains.service.ts` | Domain resolution with app_type |
| `domains/store/settings/interfaces/store-settings.interface.ts` | Store settings interfaces |
| `domains/store/settings/defaults/default-store-settings.ts` | Default store settings |

---

## 📝 App Type Migration Notes

### Before (Legacy):
```typescript
// Old way - config.app nested in config JSON
config: {
  app: 'STORE_ADMIN',
  branding: { ... }
}
```

### After (New Standard):
```typescript
// New way - app_type directly on domain
app_type: 'STORE_ADMIN'  // Source of Truth

// Branding from store_settings.settings.branding
branding: {
  name: string;
  primary_color: string;
  // ...
}
```

---

## Related Skills

- `vendix-backend-prisma` - Prisma service patterns
- `vendix-backend-auth` - JWT and authorization patterns
- `vendix-backend-middleware` - Middleware and domain resolution
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
