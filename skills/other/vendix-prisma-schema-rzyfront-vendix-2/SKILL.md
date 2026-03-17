---
name: vendix-prisma-schema
description: Prisma schema editing.
metadata:
  scope: [root]
  auto_invoke: "Editing Schema"
---
# Vendix Prisma Schema Pattern

> **Schema Editing & Migrations** - Edición de schema.prisma, relaciones y workflow de migraciones en desarrollo.

## 🎯 Schema Structure

**File:** `apps/backend/prisma/schema.prisma`

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

---

## 📝 Naming Conventions

### Database Objects

```prisma
// ✅ CORRECT - Tables in snake_case
model users {}
model product_variants {}
model sales_order_items {}

// ✅ CORRECT - Enums in snake_case with _enum suffix
enum user_state_enum {
  ACTIVE
  INACTIVE
  PENDING
}

// ❌ WRONG - Tables in PascalCase
model Users {}
model ProductVariants {}

// ❌ WRONG - Enums in PascalCase
enum UserState {}
```

### Fields

```prisma
// ✅ CORRECT - Fields in snake_case
model users {
  id               Int
  user_name        String
  email_address    String
  organization_id  Int
  main_store_id    Int?
  created_at       DateTime
  updated_at       DateTime
}

// ❌ WRONG - Fields in camelCase
model users {
  id               Int
  userName         String
  emailAddress     String
  organizationId   Int
  createdAt        DateTime
}
```

---

## 🔗 Relationship Patterns

### One-to-Many

```prisma
model organizations {
  id        Int       @id @default(autoincrement())
  name      String
  users     users[]   // One organization has many users
  stores    stores[]  // One organization has many stores
}

model users {
  id              Int            @id @default(autoincrement())
  organization_id Int
  organization    organizations  @relation(fields: [organization_id], references: [id])

  // Index for foreign key
  @@index([organization_id])
}
```

### Many-to-Many

```prisma
model users {
  id         Int          @id @default(autoincrement())
  user_name  String
  store_users store_users[]  // Join table
}

model stores {
  id         Int          @id @default(autoincrement())
  name       String
  store_users store_users[]  // Join table
}

// Join table
model store_users {
  user_id    Int
  store_id   Int
  role       String

  user       users     @relation(fields: [user_id], references: [id], onDelete: Cascade)
  store      stores    @relation(fields: [store_id], references: [id], onDelete: Cascade)

  @@id([user_id, store_id])  // Composite primary key
}
```

### Self-Referencing

```prisma
model users {
  id           Int      @id @default(autoincrement())
  user_name    String
  manager_id   Int?
  manager      users?   @relation("ManagerRelation", fields: [manager_id], references: [id])
  subordinates users[]  @relation("ManagerRelation")
}
```

---

## 🎨 Field Types & Attributes

### Common Field Types

```prisma
model products {
  id            Int      @id @default(autoincrement())
  name          String
  description   String?  @db.Text
  base_price    Decimal  @db.Decimal(10, 2)
  is_active     Boolean  @default(true)
  stock_quantity Int     @default(0)
  created_at    DateTime @default(now())
  updated_at    DateTime @updatedAt

  // Enums
  status        product_status_enum @default(ACTIVE)

  // JSON field for metadata
  metadata      Json?

  // Array of strings (PostgreSQL specific)
  tags          String[]

  // Indexes
  @@index([organization_id, store_id])
  @@index([is_active])
}

enum product_status_enum {
  ACTIVE
  INACTIVE
  DRAFT
  ARCHIVED
}
```

### Field Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `@id` | Primary key | `id Int @id` |
| `@default(value)` | Default value | `created_at DateTime @default(now())` |
| `@unique` | Unique constraint | `email String @unique` |
| `@relation` | Define relation | `organization organizations @relation(...)` |
| `@map(name)` | Map to different column name | `user_name String @map("userName")` |
| `@updatedAt` | Auto-update timestamp | `updated_at DateTime @updatedAt` |
| `@db.Type` | Database-specific type | `price Decimal @db.Decimal(10,2)` |
| `@@index` | Define index | `@@index([field1, field2])` |
| `@@unique` | Unique constraint on multiple fields | `@@unique([email, organization_id])` |
| `@@map` | Map table to different name | `@@map("users")` |

---

## 🔄 Migration Workflow

### Development Mode

```bash
# 1. Make changes to schema.prisma

# 2. Create migration (auto-applies in development)
npx prisma migrate dev --name describe_your_changes

# This will:
# - Generate migration SQL
# - Apply migration to database
# - Regenerate Prisma Client

# 3. Verify migration was applied
npx prisma migrate status

# 4. If needed, reset database (WARNING: deletes all data)
npx prisma migrate reset
```

### Production Mode

```bash
# 1. Create migration without applying
npx prisma migrate dev --create-only --name describe_your_changes

# 2. Review generated migration SQL
# Edit migration if needed

# 3. Apply migration (production environment)
npx prisma migrate deploy
```

---

## 🎯 Schema Editing Workflow

### Step 1: Backup Current State

```bash
# Export current schema
npx prisma migrate diff \
  --from-empty \
  --to-schema-datamodel prisma/schema.prisma \
  --script > backup.sql
```

### Step 2: Edit Schema

```prisma
// Example: Adding new field
model products {
  id            Int      @id @default(autoincrement())
  name          String
  weight        Decimal?  @db.Decimal(10, 2)  // NEW FIELD
  dimensions    Json?                         // NEW FIELD
}
```

### Step 3: Create Migration

```bash
npx prisma migrate dev --name add_product_weight_and_dimensions
```

### Step 4: Review Migration

```sql
-- Migration SQL
ALTER TABLE "products" ADD COLUMN "weight" DECIMAL(10,2);
ALTER TABLE "products" ADD COLUMN "dimensions" JSONB;
```

### Step 5: Apply & Test

```bash
# Migration applied automatically
# Verify with Docker logs
docker logs --tail 40 vendix_backend
```

---

## 🔍 Common Schema Patterns

### Soft Delete Pattern

```prisma
model users {
  id         Int       @id @default(autoincrement())
  user_name  String
  deleted_at DateTime?  // Soft delete timestamp
  is_active  Boolean   @default(true)

  @@index([deleted_at])
}

// Query for non-deleted records
const users = await prisma.users.findMany({
  where: {
    deleted_at: null,
    is_active: true,
  },
});
```

### Timestamps Pattern

```prisma
model base_model {
  id         Int      @id @default(autoincrement())
  created_at DateTime @default(now())
  updated_at DateTime @updatedAt
}
```

### Multi-Tenant Pattern

```prisma
model products {
  id              Int      @id @default(autoincrement())
  name            String
  organization_id Int      // Tenant ID
  store_id        Int      // Sub-tenant ID

  organization    organizations @relation(fields: [organization_id], references: [id])
  store           stores        @relation(fields: [store_id], references: [id])

  @@index([organization_id, store_id])
}
```

---

## 🚫 Common Mistakes

### ❌ WRONG: PascalCase Tables

```prisma
model Users {  // ❌ WRONG
  id Int @id
  UserName String  // ❌ WRONG
}
```

### ✅ CORRECT: snake_case Tables

```prisma
model users {  // ✅ CORRECT
  id        Int      @id
  user_name String   // ✅ CORRECT
}
```

### ❌ WRONG: Missing Foreign Key Indexes

```prisma
model products {
  id              Int
  organization_id Int  // ❌ Missing index
}
```

### ✅ CORRECT: With Indexes

```prisma
model products {
  id              Int
  organization_id Int

  @@index([organization_id])  // ✅ Index for foreign key
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `prisma/schema.prisma` | Database schema definition |
| `prisma/migrations/` | Migration files |
| `prisma/services/` | Extended Prisma services |

---

## Related Skills

- `vendix-backend-prisma` - Prisma service patterns
- `vendix-prisma-seed` - Seed data patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
