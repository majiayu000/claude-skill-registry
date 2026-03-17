---
name: vendix-backend-prisma
description: Prisma services and DB patterns.
metadata:
  scope: [root]
  auto_invoke: "Working with Prisma services"
---
# Vendix Backend Prisma Services

> **Prisma Service Pattern** - Servicios Prisma dedicados por dominio con contexto multi-tenant automático.

## 🎯 Core Principle

**Cada dominio tiene SU PROPIO servicio Prisma extendido** con acceso contextual automático a `organization_id` y `store_id`.

---
metadata:
  scope: [root]
  auto_invoke: "Working with Prisma services"

## 📁 Directory Structure

```
apps/backend/src/prisma/
├── prisma.module.ts                    # Prisma module
├── schema.prisma                       # Database schema
├── migrations/                         # Migration files
└── services/
    ├── prisma.service.ts               # Base PrismaService
    ├── ecommerce-prisma.service.ts     # E-commerce domain
    ├── organization-prisma.service.ts  # Organization domain
    ├── superadmin-prisma.service.ts    # SuperAdmin domain
    └── public-prisma.service.ts        # Public domain
```

---

## 🔧 Base PrismaService

**File:** `services/prisma.service.ts`

```typescript
import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  constructor() {
    super({
      log: ['query', 'info', 'warn', 'error'],
    });
  }

  async onModuleInit() {
    await this.$connect();
  }

  async onModuleDestroy() {
    await this.$disconnect();
  }
}
```

**Features:**
- Extends `PrismaClient` with lifecycle hooks
- Logging enabled for development
- Auto-connect on module init
- Auto-disconnect on module destroy

---

## 🏢 Domain-Specific Prisma Services

### Pattern: Extended PrismaService

Each domain gets its own PrismaService with domain-specific helpers.

#### Example: E-commerce PrismaService

**File:** `services/ecommerce-prisma.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { RequestContextService } from '@/common/context/request-context.service';

@Injectable()
export class EcommercePrismaService extends PrismaService {
  constructor(
    private readonly context: RequestContextService,
  ) {
    super();
  }

  // Automatically filter by organization_id
  get organizationWhere() {
    return {
      organization_id: this.context.organization_id,
    };
  }

  // Automatically filter by store_id
  get storeWhere() {
    return {
      ...this.organizationWhere,
      store_id: this.context.store_id,
    };
  }

  // Products with automatic scoping
  get products() {
    return this.prisma.products;
  }

  // Product variants scoped to store
  async findProductVariants(product_id: number) {
    return this.product_variants.findMany({
      where: {
        product_id,
        ...this.storeWhere,
      },
    });
  }

  // Categories scoped to organization
  async findCategories() {
    return this.categories.findMany({
      where: this.organizationWhere,
    });
  }

  // Cart items scoped to store and user
  async findCartItems(user_id: number) {
    return this.cart_items.findMany({
      where: {
        user_id,
        ...this.storeWhere,
      },
      include: {
        product: true,
        product_variant: true,
      },
    });
  }

  // Orders with full relations
  async findOrderWithItems(order_id: number) {
    return this.sales_orders.findUnique({
      where: { id: order_id },
      include: {
        customer: true,
        items: {
          include: {
            product: true,
            product_variant: true,
          },
        },
      },
    });
  }
}
```

---

### Example: Organization PrismaService

**File:** `services/organization-prisma.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { RequestContextService } from '@/common/context/request-context.service';

@Injectable()
export class OrganizationPrismaService extends PrismaService {
  constructor(
    private readonly context: RequestContextService,
  ) {
    super();
  }

  get organizationWhere() {
    return {
      organization_id: this.context.organization_id,
    };
  }

  // Users in current organization
  async findOrganizationUsers() {
    return this.users.findMany({
      where: this.organizationWhere,
      include: {
        store_users: {
          include: {
            store: true,
          },
        },
      },
    });
  }

  // Stores in current organization
  async findOrganizationStores() {
    return this.stores.findMany({
      where: this.organizationWhere,
    });
  }

  // Create user in organization
  async createUserInOrganization(data: any) {
    return this.users.create({
      data: {
        ...data,
        organization_id: this.context.organization_id,
      },
    });
  }

  // Check if user is in organization
  async isUserInOrganization(user_id: number): Promise<boolean> {
    const count = await this.users.count({
      where: {
        id: user_id,
        organization_id: this.context.organization_id,
      },
    });

    return count > 0;
  }
}
```

---

### Example: SuperAdmin PrismaService

**File:** `services/superadmin-prisma.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { RequestContextService } from '@/common/context/request-context.service';

@Injectable()
export class SuperAdminPrismaService extends PrismaService {
  constructor(
    private readonly context: RequestContextService,
  ) {
    super();
  }

  // SuperAdmin bypasses organization filtering
  // Can access ALL organizations

  async findAllOrganizations() {
    return this.organizations.findMany({
      include: {
        users: true,
        stores: true,
      },
    });
  }

  async findOrganizationStats(organization_id: number) {
    const [user_count, store_count, order_count] = await Promise.all([
      this.users.count({ where: { organization_id } }),
      this.stores.count({ where: { organization_id } }),
      this.sales_orders.count({ where: { organization_id } }),
    ]);

    return {
      user_count,
      store_count,
      order_count,
    };
  }

  async systemWideStats() {
    const [
      total_organizations,
      total_users,
      total_stores,
      total_orders,
    ] = await Promise.all([
      this.organizations.count(),
      this.users.count(),
      this.stores.count(),
      this.sales_orders.count(),
    ]);

    return {
      total_organizations,
      total_users,
      total_stores,
      total_orders,
    };
  }
}
```

---

### Example: Public PrismaService

**File:** `services/public-prisma.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { RequestContextService } from '@/common/context/request-context.service';

@Injectable()
export class PublicPrismaService extends PrismaService {
  constructor(
    private readonly context: RequestContextService,
  ) {
    super();
  }

  // Public-facing queries with minimal data exposure

  async findPublicProducts(store_id: number) {
    return this.products.findMany({
      where: {
        store_id,
        is_active: true,
        deleted_at: null,
      },
      select: {
        id: true,
        name: true,
        description: true,
        base_price: true,
        images: true,
        product_variants: {
          where: { is_active: true },
          select: {
            id: true,
            sku: true,
            price_adjustment: true,
            stock_quantity: true,
          },
        },
      },
    });
  }

  async findStoreByDomain(domain_name: string) {
    return this.stores.findFirst({
      where: {
        domain_name,
        is_active: true,
      },
      select: {
        id: true,
        name: true,
        description: true,
        logo_url: true,
        theme_config: true,
      },
    });
  }
}
```

---

## 📦 Module Configuration

### Prisma Module

**File:** `prisma.module.ts`

```typescript
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './services/prisma.service';
import { EcommercePrismaService } from './services/ecommerce-prisma.service';
import { OrganizationPrismaService } from './services/organization-prisma.service';
import { SuperAdminPrismaService } from './services/superadmin-prisma.service';
import { PublicPrismaService } from './services/public-prisma.service';

@Global()
@Module({
  providers: [
    PrismaService,
    EcommercePrismaService,
    OrganizationPrismaService,
    SuperAdminPrismaService,
    PublicPrismaService,
  ],
  exports: [
    PrismaService,
    EcommercePrismaService,
    OrganizationPrismaService,
    SuperAdminPrismaService,
    PublicPrismaService,
  ],
})
export class PrismaModule {}
```

**Note:** `@Global()` decorator makes PrismaModule available everywhere without importing.

---

## 🔌 Usage in Domain Services

### Injecting Domain-Specific PrismaService

```typescript
import { Injectable } from '@nestjs/common';
import { EcommercePrismaService } from '@/prisma/services/ecommerce-prisma.service';

@Injectable()
export class CatalogService {
  constructor(
    private readonly prisma: EcommercePrismaService,
  ) {}

  async findAllProducts() {
    // Automatically scoped to store
    return this.prisma.products.findMany({
      where: this.prisma.storeWhere,
    });
  }

  async findProductVariants(product_id: number) {
    // Domain-specific helper method
    return this.prisma.findProductVariants(product_id);
  }
}
```

---

## 🎯 Best Practices

### 1. Always Use Extended Services

```typescript
// ✅ CORRECT: Use domain-specific PrismaService
constructor(
  private readonly prisma: EcommercePrismaService,
) {}

// ❌ WRONG: Use base PrismaService directly
constructor(
  private readonly prisma: PrismaService,
) {}
```

### 2. Leverage Context Helpers

```typescript
// ✅ CORRECT: Use context helpers
where: {
  ...this.prisma.storeWhere,
  status: 'active',
}

// ❌ WRONG: Manually specify context
where: {
  organization_id: this.context.organization_id,
  store_id: this.context.store_id,
  status: 'active',
}
```

### 3. Create Domain-Specific Methods

```typescript
// ✅ CORRECT: Reusable domain methods
async findActiveProducts() {
  return this.products.findMany({
    where: {
      ...this.storeWhere,
      is_active: true,
    },
  });
}

// ❌ WRONG: Repetitive queries everywhere
// (duplication in multiple services)
```

---

## 🔄 Transactions

### Using Transactions

```typescript
async createOrderWithItems(order_data: any, items_data: any[]) {
  return this.prisma.$transaction(async (tx) => {
    // Create order
    const order = await tx.sales_orders.create({
      data: order_data,
    });

    // Create items
    const items = await Promise.all(
      items_data.map(item =>
        tx.sales_order_items.create({
          data: {
            ...item,
            order_id: order.id,
          },
        })
      )
    );

    // Update stock
    for (const item of items_data) {
      await tx.product_variants.update({
        where: { id: item.product_variant_id },
        data: {
          stock_quantity: {
            decrement: item.quantity,
          },
        },
      });
    }

    return { order, items };
  });
}
```

---

## 📊 Query Optimization

### Selective Fields

```typescript
// Only select needed fields
async findProductList() {
  return this.products.findMany({
    select: {
      id: true,
      name: true,
      base_price: true,
      // Excludes large fields like description
    },
  });
}
```

### Pagination

```typescript
async findProductsPaginated(page: number, limit: number) {
  const skip = (page - 1) * limit;

  const [data, total] = await Promise.all([
    this.products.findMany({
      skip,
      take: limit,
      where: this.storeWhere,
    }),
    this.products.count({ where: this.storeWhere }),
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

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `services/prisma.service.ts` | Base PrismaService |
| `services/ecommerce-prisma.service.ts` | E-commerce domain queries |
| `services/organization-prisma.service.ts` | Organization domain queries |
| `services/superadmin-prisma.service.ts` | SuperAdmin domain queries |
| `services/public-prisma.service.ts` | Public domain queries |
| `schema.prisma` | Database schema definition |

---

## Related Skills

- `vendix-backend-domain` - Domain architecture patterns
- `vendix-backend-auth` - Multi-tenant context setup
- `vendix-prisma-schema` - Schema editing patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
