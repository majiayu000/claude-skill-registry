---
name: prisma
description: |
  Prisma ORM for type-safe database operations with PostgreSQL.
  Use when: Defining schemas, writing type-safe queries, creating migrations, modeling relations, or replacing raw SQL with ORM patterns.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Prisma Skill

Provides type-safe database operations as an alternative to raw SQL. This codebase currently uses the `pg` library with raw SQL queries. Prisma offers automatic type generation, declarative schema modeling, and migration management - eliminating the manual row mapping and SQL injection risks present in raw SQL approaches.

## Quick Start

### Install and Initialize

```bash
cd backend
npm install prisma @prisma/client
npx prisma init
```

### Schema Definition

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Product {
  id               Int                    @id @default(autoincrement())
  name             String
  shortDescription String                 @map("short_description")
  description      String
  price            Decimal                @db.Decimal(10, 2)
  salePrice        Decimal?               @map("sale_price") @db.Decimal(10, 2)
  imageUrl         String                 @map("image_url")
  inventory        Int                    @default(0)
  categories       Json
  highlights       Json?
  usage            String?
  isNew            Boolean                @default(false) @map("is_new")
  isFeatured       Boolean                @default(false) @map("is_featured")
  salesCount       Int                    @default(0) @map("sales_count")
  createdAt        DateTime               @default(now()) @map("created_at")
  updatedAt        DateTime               @updatedAt @map("updated_at")
  translations     ProductTranslation[]
  orderItems       OrderItem[]
  variants         ProductVariant[]

  @@map("products")
}

model ProductTranslation {
  id              Int      @id @default(autoincrement())
  productId       Int      @map("product_id")
  languageCode    String   @map("language_code") @db.VarChar(10)
  name            String   @db.VarChar(255)
  shortDescription String  @map("short_description")
  description     String
  highlights      Json?
  usage           String?
  slug            String?  @db.VarChar(255)
  createdAt       DateTime @default(now()) @map("created_at")
  updatedAt       DateTime @updatedAt @map("updated_at")
  product         Product  @relation(fields: [productId], references: [id], onDelete: Cascade)
  language        Language @relation(fields: [languageCode], references: [code], onDelete: Cascade)

  @@unique([productId, languageCode])
  @@map("product_translations")
}
```

### Client Usage

```typescript
// backend/src/db/prisma.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'warn', 'error'] : ['error'],
});

export { prisma };
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `@map` | Map field to snake_case column | `@map("created_at")` |
| `@@map` | Map model to table name | `@@map("products")` |
| Relations | Define FK relationships | `product Product @relation(...)` |
| `@db.Decimal` | Specify PostgreSQL types | `@db.Decimal(10, 2)` |
| `@@unique` | Composite unique constraints | `@@unique([productId, languageCode])` |
| Transactions | Atomic operations | `prisma.$transaction([...])` |

## Common Patterns

### Fetching with Translation Fallback

**When:** Getting localized content with English fallback

```typescript
const product = await prisma.product.findUnique({
  where: { id: productId },
  include: {
    translations: {
      where: { languageCode: lang },
    },
  },
});

// Apply translation or fallback to base
const name = product.translations[0]?.name ?? product.name;
```

### Transactions for Orders

**When:** Creating orders with inventory updates

```typescript
await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData });
  
  for (const item of items) {
    await tx.orderItem.create({
      data: { orderId: order.id, ...item },
    });
    await tx.product.update({
      where: { id: item.productId },
      data: { inventory: { decrement: item.quantity } },
    });
  }
  
  return order;
});
```

## See Also

- [patterns](references/patterns.md) - Query patterns and model design
- [workflows](references/workflows.md) - Migrations and schema management

## Related Skills

- See the **postgresql** skill for raw SQL patterns and PostgreSQL-specific features
- See the **typescript** skill for type inference patterns with Prisma
- See the **zod** skill for runtime validation of Prisma inputs