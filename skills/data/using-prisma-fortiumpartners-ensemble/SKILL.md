---
name: using-prisma
description: Prisma 5+ ORM with schema-first design, type-safe client, migrations, and database integrations (Supabase, PlanetScale, Neon). Use for TypeScript/JavaScript database access.
---

# Prisma ORM Development Skill

**Version**: 1.1.0 | **Target**: <500 lines | **Purpose**: Fast reference for Prisma operations

---

## Overview

**What is Prisma**: Type-safe ORM with schema-first design for TypeScript/JavaScript. Auto-generates client from schema with full IntelliSense support.

**When to Use This Skill**:
- Database schema design and migrations
- Type-safe CRUD operations
- Relation handling and query optimization
- Integration with Supabase, PlanetScale, Neon

**Auto-Detection Triggers**:
- `schema.prisma` file present
- `@prisma/client` in dependencies
- `prisma` in devDependencies
- User mentions "Prisma", "ORM", or database models

**Progressive Disclosure**:
- **This file (SKILL.md)**: Quick reference for immediate use
- **[REFERENCE.md](REFERENCE.md)**: Comprehensive patterns, advanced queries, production deployment

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Schema Basics](#schema-basics)
3. [CLI Commands](#cli-commands)
4. [Client Operations](#client-operations)
5. [Relations](#relations)
6. [Transactions](#transactions)
7. [Database Integrations](#database-integrations)
8. [Error Handling](#error-handling)
9. [Testing Patterns](#testing-patterns)
10. [Quick Reference Card](#quick-reference-card)

---

## Project Structure

```
my_project/
├── prisma/
│   ├── schema.prisma          # Schema definition
│   ├── migrations/            # Migration history
│   └── seed.ts                # Database seeding
├── src/
│   └── lib/prisma.ts          # Client singleton
└── package.json
```

---

## Schema Basics

### Datasource Configuration

```prisma
// PostgreSQL (local)
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Supabase (with pooling) - see Database Integrations
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")      // Pooled connection
  directUrl = env("DIRECT_URL")        // Direct for migrations
}

generator client {
  provider = "prisma-client-js"
}
```

### Model Definition

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  bio       String?                    // Optional
  role      Role     @default(USER)
  active    Boolean  @default(true)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  posts     Post[]                     // Relation

  @@index([email])
}

enum Role {
  USER
  ADMIN
}
```

### Common Field Types

| Type | Example | Notes |
|------|---------|-------|
| `String` | `name String` | Text |
| `String?` | `bio String?` | Optional text |
| `Int` | `count Int` | Integer |
| `Float` | `price Float` | Decimal |
| `Boolean` | `active Boolean` | true/false |
| `DateTime` | `createdAt DateTime` | Timestamp |
| `Json` | `metadata Json` | JSON object |
| `String[]` | `tags String[]` | PostgreSQL array |

> **More patterns**: See [REFERENCE.md - Schema Design Patterns](REFERENCE.md#2-schema-design-patterns) for soft delete, audit fields, polymorphic relations, and multi-tenancy patterns.

---

## CLI Commands

### Development Workflow

```bash
npx prisma init                      # Initialize Prisma
npx prisma generate                  # Generate client after schema changes
npx prisma db push                   # Push schema (no migrations)
npx prisma migrate dev --name init   # Create migration
npx prisma migrate reset             # Reset database
npx prisma studio                    # Open GUI
```

### Production Workflow

```bash
npx prisma generate                  # Generate client (required in CI)
npx prisma migrate deploy            # Apply pending migrations
npx prisma migrate status            # Check migration status
```

### Database Inspection

```bash
npx prisma db pull                   # Pull schema from existing DB
npx prisma validate                  # Validate schema
npx prisma format                    # Format schema file
```

---

## Client Operations

### Client Singleton

```typescript
// src/lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

### CRUD Operations

```typescript
// Create
const user = await prisma.user.create({
  data: { email: "user@example.com", name: "John" },
});

// Read
const user = await prisma.user.findUnique({
  where: { id: "user_id" },
});

// Update
const updated = await prisma.user.update({
  where: { id: "user_id" },
  data: { name: "New Name" },
});

// Upsert
const upserted = await prisma.user.upsert({
  where: { email: "user@example.com" },
  update: { name: "Updated" },
  create: { email: "user@example.com", name: "New" },
});

// Delete
const deleted = await prisma.user.delete({
  where: { id: "user_id" },
});
```

### Filtering

```typescript
const users = await prisma.user.findMany({
  where: {
    email: { contains: "@example.com" },
    role: { in: ["ADMIN", "USER"] },
    createdAt: { gte: new Date("2024-01-01") },
    OR: [
      { name: { startsWith: "John" } },
      { name: { startsWith: "Jane" } },
    ],
  },
});
```

### Pagination

```typescript
// Offset pagination
const users = await prisma.user.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: "desc" },
});

// Cursor pagination (more efficient)
const users = await prisma.user.findMany({
  take: 10,
  cursor: { id: "last_seen_id" },
  skip: 1,
});
```

### Select and Include

```typescript
// Select specific fields
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
});

// Include relations
const users = await prisma.user.findMany({
  include: { posts: { where: { published: true }, take: 5 } },
});
```

> **More patterns**: See [REFERENCE.md - Query Optimization](REFERENCE.md#6-query-optimization) for N+1 prevention, cursor pagination, and aggregation patterns.

---

## Relations

### One-to-Many

```prisma
model User {
  id    String @id @default(cuid())
  posts Post[]
}

model Post {
  id       String @id @default(cuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
  @@index([authorId])
}
```

### Many-to-Many (Implicit)

```prisma
model Post {
  id         String     @id @default(cuid())
  categories Category[]
}

model Category {
  id    String @id @default(cuid())
  posts Post[]
}
```

### Relation Queries

```typescript
// Create with relation
const user = await prisma.user.create({
  data: {
    email: "author@example.com",
    posts: { create: { title: "First Post" } },
  },
  include: { posts: true },
});

// Filter by relation
const usersWithPosts = await prisma.user.findMany({
  where: { posts: { some: { published: true } } },
});
```

> **More patterns**: See [REFERENCE.md - Advanced Relations](REFERENCE.md#3-advanced-relations) for self-relations, polymorphic patterns, and explicit many-to-many.

---

## Transactions

### Interactive Transaction

```typescript
const result = await prisma.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData });
  await tx.inventory.update({
    where: { id: productId },
    data: { stock: { decrement: 1 } },
  });
  if ((await tx.inventory.findUnique({ where: { id: productId } }))!.stock < 0) {
    throw new Error("Insufficient stock");
  }
  return order;
});
```

### Sequential Transaction

```typescript
const [users, posts] = await prisma.$transaction([
  prisma.user.findMany(),
  prisma.post.findMany(),
]);
```

> **More patterns**: See [REFERENCE.md - Transactions & Concurrency](REFERENCE.md#7-transactions--concurrency) for isolation levels, optimistic locking, and deadlock prevention.

---

## Database Integrations

### Supabase

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")      // Transaction pooler
  directUrl = env("DIRECT_URL")        // Direct for migrations
}
```

```env
DATABASE_URL="postgres://postgres.[ref]:password@aws-0-region.pooler.supabase.com:6543/postgres?pgbouncer=true"
DIRECT_URL="postgres://postgres.[ref]:password@aws-0-region.supabase.com:5432/postgres"
```

### PlanetScale

```prisma
datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
  relationMode = "prisma"  // Required: no foreign keys
}
```

### Neon

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

> **More patterns**: See [REFERENCE.md - Database Integrations](REFERENCE.md#4-database-integrations) for Supabase Auth integration, connection pooling, and edge runtime setup.

---

## Error Handling

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| P2002 | Unique constraint failed | Duplicate value |
| P2003 | Foreign key constraint failed | Missing relation |
| P2025 | Record not found | Update/delete on missing record |
| P2024 | Connection pool timeout | Too many connections |

### Error Handling Pattern

```typescript
import { Prisma } from "@prisma/client";

try {
  await prisma.user.create({ data });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === "P2002") {
      throw new ConflictError("Email already exists");
    }
    if (error.code === "P2025") {
      throw new NotFoundError("Record not found");
    }
  }
  throw error;
}
```

> **More patterns**: See [REFERENCE.md - Error Handling](REFERENCE.md#9-security--row-level-security) for comprehensive error mapping and retry strategies.

---

## Testing Patterns

### Mock Client

```typescript
import { mockDeep, DeepMockProxy } from "jest-mock-extended";
import { PrismaClient } from "@prisma/client";

export const prismaMock = mockDeep<PrismaClient>();

jest.mock("./lib/prisma", () => ({
  prisma: prismaMock,
}));

// In tests
prismaMock.user.create.mockResolvedValue(mockUser);
```

### Test Database Setup

```typescript
beforeEach(async () => {
  await prisma.$executeRaw`TRUNCATE TABLE "User" CASCADE`;
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

> **More patterns**: See [REFERENCE.md - Testing Strategies](REFERENCE.md#10-production-deployment) for integration testing, test containers, and CI/CD setup.

---

## Quick Reference Card

```bash
# Development
npx prisma generate          # Regenerate client
npx prisma db push           # Push schema changes
npx prisma migrate dev       # Create migration
npx prisma studio            # GUI browser

# Production
npx prisma generate          # Required in CI
npx prisma migrate deploy    # Apply migrations
```

```typescript
// CRUD
prisma.model.create({ data })
prisma.model.findUnique({ where })
prisma.model.findMany({ where, orderBy, take, skip })
prisma.model.update({ where, data })
prisma.model.delete({ where })
prisma.model.upsert({ where, create, update })

// Relations
include: { relation: true }
include: { relation: { where, take } }
where: { relation: { some: {} } }

// Transactions
prisma.$transaction(async (tx) => { ... })
prisma.$transaction([query1, query2])
```

---

**Progressive Disclosure**: Start here for quick reference. Load [REFERENCE.md](REFERENCE.md) for comprehensive patterns, advanced configurations, and production deployment.

**Skill Version**: 1.1.0
