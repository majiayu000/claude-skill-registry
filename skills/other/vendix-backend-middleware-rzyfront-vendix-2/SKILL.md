---
name: vendix-backend-middleware
description: Middleware configuration.
metadata:
  scope: [root]
  auto_invoke: "Configuring middleware"
---
# Vendix Backend Middleware & Domain Resolution

> **Middleware Pattern** - Resolución de dominios dinámicos, contexto multi-tenant y middlewares personalizados.

## 🌐 Domain Resolution Middleware

### Purpose

El **DomainResolverMiddleware** es responsable de:
1. **Resolver subdominios** (ej: `tienda.tiendavendix.com`)
2. **Extraer store_id y organization_id** del dominio
3. **Inyectar contexto** en la solicitud para multi-tenancy
4. **Cachear resultados** para optimizar rendimiento

---
metadata:
  scope: [root]
  auto_invoke: "Configuring middleware"

## 🔧 DomainResolverMiddleware

**File:** `common/middleware/domain-resolver.middleware.ts`

```typescript
import { Injectable, NestMiddleware, NotFoundException } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import { PrismaService } from '@/prisma/services/prisma.service';
import LRU from 'lru-cache';

interface DomainInfo {
  store_id: number;
  organization_id: number;
  domain_type: 'store' | 'organization' | 'vendix_core';
}

@Injectable()
export class DomainResolverMiddleware implements NestMiddleware {
  private cache = new LRU<string, DomainInfo>({
    max: 500,  // Max 500 cached domains
    ttl: 1000 * 60 * 5,  // 5 minutes TTL
  });

  constructor(private readonly prisma: PrismaService) {}

  async use(req: Request, res: Response, next: NextFunction) {
    const host = req.headers.host;  // tienda.tiendavendix.com

    // Check cache first
    const cached = this.cache.get(host);
    if (cached) {
      req['store_id'] = cached.store_id;
      req['organization_id'] = cached.organization_id;
      req['domain_type'] = cached.domain_type;
      return next();
    }

    // Resolve domain
    const domain_info = await this.resolveDomain(host);

    if (!domain_info) {
      throw new NotFoundException('Domain not found');
    }

    // Cache result
    this.cache.set(host, domain_info);

    // Inject into request
    req['store_id'] = domain_info.store_id;
    req['organization_id'] = domain_info.organization_id;
    req['domain_type'] = domain_info.domain_type;

    next();
  }

  private async resolveDomain(host: string): Promise<DomainInfo | null> {
    // Extract subdomain
    const subdomain = this.extractSubdomain(host);

    // Check for vendix core domain
    if (this.isVendixCoreDomain(host)) {
      return {
        store_id: null,
        organization_id: null,
        domain_type: 'vendix_core',
      };
    }

    // Try to resolve as store domain
    const store = await this.prisma.stores.findFirst({
      where: { domain_name: subdomain, is_active: true },
      select: {
        id: true,
        organization_id: true,
      },
    });

    if (store) {
      return {
        store_id: store.id,
        organization_id: store.organization_id,
        domain_type: 'store',
      };
    }

    // Try to resolve as organization domain
    const organization = await this.prisma.organizations.findFirst({
      where: { domain_name: subdomain, is_active: true },
      select: {
        id: true,
      },
    });

    if (organization) {
      return {
        store_id: null,
        organization_id: organization.id,
        domain_type: 'organization',
      };
    }

    return null;
  }

  private extractSubdomain(host: string): string {
    // tienda.tiendavendix.com -> tienda
    const parts = host.split('.');
    return parts[0];
  }

  private isVendixCoreDomain(host: string): boolean {
    // Check if it's the main vendix domain
    const core_domains = [
      'vendix.com',
      'tiendavendix.com',
      'localhost',
    ];

    return core_domains.some(domain => host.includes(domain));
  }
}
```

---

## 📦 Middleware Registration

**File:** `app.module.ts`

```typescript
import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { DomainResolverMiddleware } from './common/middleware/domain-resolver.middleware';

@Module({
  // ... module configuration
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(DomainResolverMiddleware)
      .forRoutes('*');  // Apply to ALL routes
  }
}
```

---

## 🎯 RequestContextService

**File:** `common/context/request-context.service.ts`

```typescript
import { Injectable, Scope } from '@nestjs/common';
import { REQUEST } from '@nestjs/core';
import { Request } from 'express';

@Injectable({ scope: Scope.REQUEST })
export class RequestContextService {
  constructor(@Inject(REQUEST) private readonly request: Request) {}

  get user_id(): number {
    return this.request['user']?.id;
  }

  get organization_id(): number {
    return this.request['organization_id'];
  }

  get store_id(): number {
    return this.request['store_id'];
  }

  get domain_type(): string {
    return this.request['domain_type'];
  }

  get roles(): string[] {
    return this.request['user']?.roles || [];
  }

  get is_super_admin(): boolean {
    return this.roles.includes('super_admin');
  }

  get is_owner(): boolean {
    return this.roles.includes('organization_admin') ||
           this.roles.includes('store_admin');
  }
}
```

**Key Features:**
- **REQUEST scope** - New instance per request
- Access to domain context from middleware
- Access to user context from JWT
- Helper methods for role checks

---

## 🔐 Custom Middlewares

### Logging Middleware

**File:** `common/middleware/logging.middleware.ts`

```typescript
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggingMiddleware implements NestMiddleware {
  private logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const { method, originalUrl, ip } = req;
    const user_agent = req.get('user-agent') || '';

    const start = Date.now();

    res.on('finish', () => {
      const { statusCode } = res;
      const content_length = res.get('content-length');
      const response_time = Date.now() - start;

      this.logger.log(
        `${method} ${originalUrl} ${statusCode} ${content_length}b - ${response_time}ms - ${ip} - ${user_agent}`,
      );
    });

    next();
  }
}
```

### Rate Limiting Middleware

**File:** `common/middleware/rate-limit.middleware.ts`

```typescript
import { Injectable, NestMiddleware, HttpException } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';
import LRU from 'lru-cache';

@Injectable()
export class RateLimitMiddleware implements NestMiddleware {
  private rate_limits = new LRU<string, { count: number; reset_time: number }>({
    max: 1000,
    ttl: 1000 * 60,  // 1 minute
  });

  private readonly LIMIT = 100;  // 100 requests per minute

  use(req: Request, res: Response, next: NextFunction) {
    const key = this.getKey(req);
    const now = Date.now();
    const limit_data = this.rate_limits.get(key);

    if (!limit_data || now > limit_data.reset_time) {
      // First request or window expired
      this.rate_limits.set(key, {
        count: 1,
        reset_time: now + 60000,
      });
      return next();
    }

    if (limit_data.count >= this.LIMIT) {
      throw new HttpException('Too many requests', 429);
    }

    limit_data.count++;
    next();
  }

  private getKey(req: Request): string {
    // Rate limit by IP + user ID (if authenticated)
    const user_id = req['user']?.id || 'anonymous';
    const ip = req.ip;
    return `${ip}:${user_id}`;
  }
}
```

### CORS Middleware

**File:** `common/middleware/cors.middleware.ts`

```typescript
import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class CorsMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    const allowed_origins = [
      'https://vendix.com',
      'https://*.vendix.com',
    ];

    const origin = req.headers.origin;

    if (allowed_origins.some(allowed => origin?.match(allowed))) {
      res.setHeader('Access-Control-Allow-Origin', origin);
    }

    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');
    res.setHeader('Access-Control-Allow-Credentials', 'true');

    if (req.method === 'OPTIONS') {
      return res.sendStatus(204);
    }

    next();
  }
}
```

---

## 📋 Applying Multiple Middlewares

**File:** `app.module.ts`

```typescript
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer
      .apply(
        CorsMiddleware,
        LoggingMiddleware,
        RateLimitMiddleware,
        DomainResolverMiddleware,  // Must be last
      )
      .forRoutes('*')
      .apply(
        // Specific middlewares for specific routes
      )
      .exclude(
        // Exclude certain routes
        'health',
        'public/(.*)',
      )
      .forRoutes('api');
  }
}
```

**Order Matters:**
1. CORS
2. Logging
3. Rate Limiting
4. Domain Resolution (must be last)

---

## 🎯 Usage in Controllers

### Accessing Domain Context

```typescript
@Controller('products')
export class ProductsController {
  constructor(
    private readonly context: RequestContextService,
    private readonly prisma: EcommercePrismaService,
  ) {}

  @Get()
  async findAll() {
    // Context automatically injected from middleware
    return this.prisma.products.findMany({
      where: {
        store_id: this.context.store_id,
        organization_id: this.context.organization_id,
      },
    });
  }
}
```

### Role-Based Context

```typescript
@Controller('admin')
export class AdminController {
  constructor(private readonly context: RequestContextService) {}

  @Get('settings')
  async getSettings() {
    if (this.context.is_super_admin) {
      // Super admin can see all settings
      return this.getSystemSettings();
    }

    if (this.context.is_owner) {
      // Owner can see organization settings
      return this.getOrganizationSettings(this.context.organization_id);
    }

    // Regular user
    return this.getStoreSettings(this.context.store_id);
  }
}
```

---

## 🔍 Domain Types

### Vendix Core Domain

```
vendix.com
tiendavendix.com
localhost
```

**Context:**
- `organization_id`: null
- `store_id`: null
- `domain_type`: 'vendix_core'

**Used for:**
- Super admin panel
- Organization registration
- Landing pages

### Organization Domain

```
mycompany.tiendavendix.com
```

**Context:**
- `organization_id`: 123
- `store_id`: null
- `domain_type`: 'organization'

**Used for:**
- Organization management
- Store selection
- User management

### Store Domain

```
myshop.tiendavendix.com
```

**Context:**
- `organization_id`: 123
- `store_id`: 456
- `domain_type`: 'store'

**Used for:**
- E-commerce catalog
- Shopping cart
- Checkout
- Customer account

---

## 🚀 Performance Optimization

### Caching Strategy

```typescript
private cache = new LRU<string, DomainInfo>({
  max: 500,           // Cache up to 500 domains
  ttl: 1000 * 60 * 5, // 5 minutes TTL
});
```

**Benefits:**
- Reduced database queries
- Faster request processing
- Lower latency

### Cache Invalidation

```typescript
// When a store domain is updated
async updateStoreDomain(store_id: number, new_domain: string) {
  await this.prisma.stores.update({
    where: { id: store_id },
    data: { domain_name: new_domain },
  });

  // Invalidate cache for this domain
  this.cache.del(new_domain);
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `common/middleware/domain-resolver.middleware.ts` | Domain resolution and caching |
| `common/context/request-context.service.ts` | Request-scoped context service |
| `app.module.ts` | Middleware registration |
| `common/middleware/logging.middleware.ts` | HTTP logging |
| `common/middleware/rate-limit.middleware.ts` | Rate limiting |
| `common/middleware/cors.middleware.ts` | CORS handling |

---

## Related Skills

- `vendix-backend-auth` - JWT authentication setup
- `vendix-backend-domain` - Domain architecture patterns
- `vendix-backend-prisma` - Prisma service patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
