---
name: vendix-backend-auth
description: Authentication and Authorization patterns.
metadata:
  scope: [root]
  auto_invoke: "Implementing authentication"
---
# Vendix Backend Authentication & Authorization

> **Auth Pattern** - Estrategia global de JWT con decoradores para acceso público, roles y permisos granulares.

## 🎯 Authentication Architecture

Vendix implementa **autenticación JWT global** con autorización basada en roles y permisos usando decoradores.

---
metadata:
  scope: [root]
  auto_invoke: "Implementing authentication"

## 🔐 Global JWT Strategy

### Configuration in app.module.ts

```typescript
import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { JwtStrategy } from './auth/strategies/jwt.strategy';
import { AuthGuard } from './common/guards/auth.guard';

@Module({
  imports: [
    PassportModule.register({ defaultStrategy: 'jwt' }),
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: {
        expiresIn: process.env.JWT_EXPIRES_IN || '1d',
      },
    }),
  ],
  providers: [
    JwtStrategy,
    {
      provide: APP_GUARD,  // Global guard - ALL routes protected by default
      useClass: AuthGuard,
    },
  ],
  exports: [PassportModule, JwtModule],
})
export class AuthModule {}
```

**Key Point:** `APP_GUARD` makes JWT authentication **global by default**. All routes require authentication UNLESS marked with `@Public()`.

---

## 🚪 Public Routes

### @Public() Decorator

**File:** `common/decorators/public.decorator.ts`

```typescript
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';

export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

### Usage

```typescript
import { Public } from '@/common/decorators/public.decorator';

@Controller('auth')
export class AuthController {
  @Public()  // No authentication required
  @Post('login')
  async login(@Body() login_dto: LoginDto) {
    return this.authService.login(login_dto);
  }

  @Public()  // No authentication required
  @Post('register')
  async register(@Body() register_dto: RegisterDto) {
    return this.authService.register(register_dto);
  }

  @Post('logout')  // Requires authentication (default)
  async logout() {
    return this.authService.logout();
  }
}
```

**When to use `@Public()`:**
- Login/register endpoints
- Password reset
- Public catalog (when accessed by domain)
- Health checks
- Webhook endpoints

---

## 👥 Role-Based Access

### @Roles() Decorator

**File:** `common/decorators/roles.decorator.ts`

```typescript
import { SetMetadata } from '@nestjs/common';

export const ROLES_KEY = 'roles';

export const Roles = (...roles: string[]) => SetMetadata(ROLES_KEY, roles);
```

### RolesGuard

**File:** `common/guards/roles.guard.ts`

```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { ROLES_KEY } from '../decorators/roles.decorator';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const required_roles = this.reflector.getAllAndOverride<string[]>(
      ROLES_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!required_roles) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return required_roles.some((role) => user.roles?.includes(role));
  }
}
```

### Usage

```typescript
import { Roles } from '@/common/decorators/roles.decorator';
import { RolesGuard } from '@/common/guards/roles.guard';
import { UseGuards } from '@nestjs/common';

@Controller('superadmin')
@UseGuards(AuthGuard, RolesGuard)  // Apply both guards
export class SuperAdminController {
  @Roles('super_admin')
  @Get('system-stats')
  async getSystemStats() {
    // Only accessible by users with 'super_admin' role
    return this.superadminService.getSystemStats();
  }

  @Roles('super_admin', 'organization_admin')
  @Get('organization-stats')
  async getOrganizationStats() {
    // Accessible by super_admin OR organization_admin
  }
}
```

**Available Roles:**
- `super_admin` - Full system access
- `organization_admin` - Organization-wide access
- `store_admin` - Store-wide access
- `store_user` - Limited store access

---

## 🔑 Permission-Based Access

### @Permissions() Decorator

**File:** `common/decorators/permissions.decorator.ts`

```typescript
import { SetMetadata } from '@nestjs/common';

export const PERMISSIONS_KEY = 'permissions';

export const Permissions = (...permissions: string[]) =>
  SetMetadata(PERMISSIONS_KEY, permissions);
```

### PermissionsGuard

**File:** `common/guards/permissions.guard.ts`

```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PERMISSIONS_KEY } from '../decorators/permissions.decorator';

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const required_permissions = this.reflector.getAllAndOverride<string[]>(
      PERMISSIONS_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (!required_permissions) {
      return true;
    }

    const { user } = context.switchToHttp().getRequest();
    return required_permissions.every((permission) =>
      user.permissions?.includes(permission),
    );
  }
}
```

### Usage

```typescript
import { Permissions } from '@/common/decorators/permissions.decorator';
import { PermissionsGuard } from '@/common/guards/permissions.guard';

@Controller('catalog')
@UseGuards(AuthGuard, PermissionsGuard)
export class CatalogController {
  @Permissions('catalog:read')
  @Get('products')
  async getProducts() {
    // Requires catalog:read permission
  }

  @Permissions('catalog:write')
  @Post('products')
  async createProduct() {
    // Requires catalog:write permission
  }

  @Permissions('catalog:write', 'inventory:update')
  @Patch('products/:id')
  async updateProduct() {
    // Requires BOTH permissions
  }
}
```

**Permission Format:** `{resource}:{action}`

**Available Permissions:**
```
catalog:read, catalog:write
inventory:read, inventory:write, inventory:update
orders:read, orders:write, orders:manage
users:read, users:write, users:delete
stores:read, stores:write, stores:delete
organizations:read, organizations:write
payments:read, payments:process, payments:refund
```

---

## 🎯 Combining Guards

### Multiple Guards

```typescript
@Controller('admin')
@UseGuards(AuthGuard, RolesGuard, PermissionsGuard)
export class AdminController {
  @Roles('organization_admin', 'store_admin')
  @Permissions('users:write')
  @Post('users')
  async createUser() {
    // Must have:
    // 1. Valid JWT (AuthGuard)
    // 2. One of the roles (RolesGuard)
    // 3. The permission (PermissionsGuard)
  }
}
```

### Guard Execution Order

1. **AuthGuard** - Validates JWT token
2. **RolesGuard** - Checks role membership
3. **PermissionsGuard** - Checks specific permissions

---

## 📜 JWT Strategy

### JwtStrategy Implementation

**File:** `auth/strategies/jwt.strategy.ts`

```typescript
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { UserService } from '@/domains/organization/user/user.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private readonly user_service: UserService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate(payload: any) {
    const user = await this.user_service.findById(payload.sub);

    if (!user || !user.is_active) {
      throw new UnauthorizedException('User not found or inactive');
    }

    return {
      id: user.id,
      email: user.email,
      roles: user.roles,
      permissions: user.permissions,
      organization_id: user.organization_id,
      main_store_id: user.main_store_id,
    };
  }
}
```

---

## 🔑 Token Management

### Login Endpoint

```typescript
@Public()
@Post('login')
async login(@Body() login_dto: LoginDto) {
  const user = await this.validateUser(login_dto);

  if (!user) {
    throw new UnauthorizedException('Invalid credentials');
  }

  const payload = {
    sub: user.id,
    email: user.email,
    roles: user.roles,
    organization_id: user.organization_id,
  };

  const access_token = this.jwt_service.sign(payload);

  return {
    access_token,
    token_type: 'Bearer',
    expires_in: process.env.JWT_EXPIRES_IN || '1d',
  };
}
```

### Refresh Token

```typescript
@Public()
@Post('refresh')
async refresh(@Body() refresh_dto: RefreshTokenDto) {
  // Validate refresh token
  const user = await this.validateRefreshToken(refresh_dto.refresh_token);

  // Generate new access token
  const access_token = this.generateAccessToken(user);

  return {
    access_token,
    token_type: 'Bearer',
  };
}
```

---

## 🛡️ AuthGuard Implementation

**File:** `common/guards/auth.guard.ts`

```typescript
import { Injectable, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { AuthGuard as PassportAuthGuard } from '@nestjs/passport';
import { Observable } from 'rxjs';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator';
import { Reflector } from '@nestjs/core';

@Injectable()
export class AuthGuard extends PassportAuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const is_public = this.reflector.getAllAndOverride<boolean>(
      IS_PUBLIC_KEY,
      [context.getHandler(), context.getClass()],
    );

    if (is_public) {
      return true;  // Skip auth for @Public() routes
    }

    return super.canActivate(context);
  }

  handleRequest(err: any, user: any, info: any) {
    if (err || !user) {
      throw err || new UnauthorizedException('Invalid or missing token');
    }
    return user;
  }
}
```

**Key Features:**
- Checks for `@Public()` decorator first
- Falls back to JWT validation
- Throws `UnauthorizedException` for invalid tokens

---

## 🎯 Usage Patterns

### Controller-Level Guards

```typescript
@Controller('api')
@UseGuards(AuthGuard)
export class ApiController {
  // All routes require authentication

  @Public()
  @Get('health')
  health() {
    // Except this one
  }
}
```

### Method-Level Guards

```typescript
@Controller('users')
@UseGuards(AuthGuard)
export class UsersController {
  @Get()
  findAll() {
    // Auth required
  }

  @Get('profile')
  getProfile(@Request() req) {
    // Access user via req.user
    return req.user;
  }
}
```

### Accessing User in Controllers

```typescript
@Post('create-order')
async createOrder(@Request() req, @Body() dto: CreateOrderDto) {
  const user_id = req.user.id;
  const organization_id = req.user.organization_id;

  return this.orderService.createOrder({
    ...dto,
    user_id,
    organization_id,
  });
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `app.module.ts` | Global guard configuration |
| `auth/strategies/jwt.strategy.ts` | JWT validation strategy |
| `common/guards/auth.guard.ts` | Authentication guard with @Public() support |
| `common/guards/roles.guard.ts` | Role-based access control |
| `common/guards/permissions.guard.ts` | Permission-based access control |
| `common/decorators/public.decorator.ts` | Mark public routes |
| `common/decorators/roles.decorator.ts` | Require specific roles |
| `common/decorators/permissions.decorator.ts` | Require specific permissions |

---

## Related Skills

- `vendix-backend-domain` - Domain architecture with auth
- `vendix-backend-middleware` - Middleware and domain resolution
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
