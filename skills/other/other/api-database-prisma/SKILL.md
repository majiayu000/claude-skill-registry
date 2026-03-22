---
name: api-database-prisma
description: Prisma ORM, type-safe queries, migrations, relations
---

# Database with Prisma ORM

> **Quick Guide:** Use Prisma ORM for type-safe database queries with auto-generated TypeScript types. Schema-first design with declarative migrations. Use `include` for relations, `$transaction` for atomic operations. Singleton pattern required in development to avoid connection exhaustion. Always use `tx` (not `prisma`) inside interactive transaction callbacks.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use the singleton pattern for PrismaClient in development to prevent connection exhaustion from hot reloading)**

**(You MUST use `tx` parameter (NOT `prisma`) inside interactive transaction callbacks to ensure atomicity)**

**(You MUST use `include` or nested `select` for relational queries - avoid N+1 by fetching relations in the same query)**

**(You MUST define `@relation` with explicit `fields` and `references` for all foreign key relationships)**

</critical_requirements>

---

**Auto-detection:** prisma, @prisma/client, PrismaClient, prisma.schema, prisma migrate, findUnique, findMany, include, $transaction

**When to use:**

- Type-safe database queries with auto-generated TypeScript types
- Schema-first development with declarative migrations
- Applications requiring strong relational data modeling
- Rapid prototyping with Prisma Studio GUI

**When NOT to use:**

- Need raw SQL performance for complex queries (Prisma adds overhead)
- Edge/serverless requiring minimal cold start (consider lighter ORMs)
- Non-TypeScript projects (lose primary benefit)
- Need fine-grained control over generated SQL

**Key patterns covered:**

- PrismaClient singleton (development hot reload safety)
- CRUD operations with type-safe filters and pagination
- Relational queries with `include` and nested `select`
- Transactions (nested writes, batch, interactive)
- Schema design (models, relations, enums, indexes)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Singleton setup, CRUD, filtering, pagination
- [examples/relations.md](examples/relations.md) - Relational queries, includes, N+1 prevention
- [examples/transactions.md](examples/transactions.md) - Atomic operations, interactive transactions, error handling
- [reference.md](reference.md) - Decision frameworks, anti-patterns, performance

---

<philosophy>

## Philosophy

**Prisma ORM** provides a declarative schema language that generates type-safe database clients. The schema serves as the single source of truth for your data model, TypeScript types, and migrations.

**Core principles:**

1. **Schema-first design** - Define models in `schema.prisma`, generate everything else
2. **Type safety everywhere** - All queries fully typed based on your schema
3. **Declarative migrations** - Schema changes automatically generate migration SQL
4. **Intuitive API** - Queries read like English (`prisma.user.findMany()`)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: PrismaClient Singleton

Use singleton pattern to prevent connection pool exhaustion during development hot reloading. Without this, each hot reload creates a new PrismaClient with its own connection pool, quickly exhausting database connections.

```typescript
// lib/db/client.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

const createPrismaClient = () => {
  return new PrismaClient({
    log:
      process.env.NODE_ENV === "development"
        ? ["query", "error", "warn"]
        : ["error"],
  });
};

export const prisma = globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

**Why good:** `globalThis` persists across hot reloads, conditional logging avoids production noise

```typescript
// BAD: New client every import
export const prisma = new PrismaClient(); // New instance on every hot reload
```

**Why bad:** Exhausts database connections (default 100 for PostgreSQL) after repeated hot reloads

> See [examples/core.md](examples/core.md) for serverless connection patterns.

---

### Pattern 2: Schema Design

Define models with relations, constraints, and defaults. The schema is the source of truth.

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}
```

**Why good:** `cuid()` for collision-resistant IDs, `@updatedAt` auto-tracks changes, `@relation` with `onDelete: Cascade` prevents orphans, `@@index` on foreign keys, `@@map` for snake_case DB tables with PascalCase in code

---

### Pattern 3: CRUD with Type-Safe Filters

All queries are fully typed based on your schema. Key operations:

```typescript
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

// Find by unique field - returns T | null
const user = await prisma.user.findUnique({
  where: { email: "alice@example.com" },
});

// Find many with filters + pagination
const users = await prisma.user.findMany({
  where: {
    role: { in: ["USER", "MODERATOR"] },
    createdAt: { gte: new Date("2024-01-01") },
  },
  orderBy: { name: "asc" },
  take: DEFAULT_PAGE_SIZE,
});

// Upsert - atomic create-or-update
const upserted = await prisma.user.upsert({
  where: { email: "alice@example.com" },
  create: { email: "alice@example.com", name: "Alice" },
  update: { name: "Alice Updated" },
});
```

**Why good:** Type-safe operations catch errors at compile time, `findUnique` returns `T | null` forcing null handling, `upsert` is atomic

> See [examples/core.md](examples/core.md) for complete CRUD operations, filtering, and pagination patterns.

---

### Pattern 4: Relational Queries

Fetch related data efficiently using `include` or nested `select` to avoid N+1 queries.

```typescript
// Include related records - single query
const userWithPosts = await prisma.user.findUnique({
  where: { id: userId },
  include: {
    posts: {
      where: { published: true },
      orderBy: { createdAt: "desc" },
      take: 10,
    },
    profile: true,
  },
});

// Select specific fields only - smaller payload
const userSummary = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    name: true,
    posts: { select: { id: true, title: true } },
  },
});
```

**Why good:** Single query avoids N+1, `include` fetches all fields, `select` reduces payload

```typescript
// BAD: N+1 query pattern
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id },
  }); // N additional queries!
}
```

**Why bad:** 1 query for users + N queries for posts, extremely slow at scale

> See [examples/relations.md](examples/relations.md) for relation filters, many-to-many, self-relations, and include vs select patterns.

---

### Pattern 5: Transactions

Ensure atomic operations across multiple writes.

```typescript
// Nested writes - implicit transaction
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    profile: { create: { bio: "Developer" } },
    posts: { create: [{ title: "First Post", published: true }] },
  },
  include: { profile: true, posts: true },
});

// Interactive transaction - complex logic with rollback
const MINIMUM_BALANCE = 0;

const transferFunds = async (fromId: string, toId: string, amount: number) => {
  return await prisma.$transaction(async (tx) => {
    const sender = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    if (sender.balance < MINIMUM_BALANCE) {
      throw new Error("Insufficient funds"); // Rolls back everything
    }

    return await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });
  });
};
```

**Why good:** Nested writes are cleanest for related records, interactive transactions enable business logic with automatic rollback

```typescript
// BAD: Using prisma instead of tx
await prisma.$transaction(async (tx) => {
  await prisma.post.create({ data: { title: "Post" } }); // Uses prisma, not tx!
});
```

**Why bad:** Operations using `prisma` bypass transaction context, won't rollback on failure

> See [examples/transactions.md](examples/transactions.md) for batch transactions, error handling, optimistic concurrency, and transaction options.

---

### Pattern 6: Connection Management

Handle connections properly for different environments.

```typescript
// Graceful shutdown
process.on("beforeExit", async () => {
  await prisma.$disconnect();
});

// Serverless: use connection pooler (PgBouncer, Prisma Accelerate)
export const prisma = new PrismaClient({
  datasources: {
    db: { url: process.env.DATABASE_URL_WITH_POOLER },
  },
});
```

**Why good:** Graceful shutdown prevents connection leaks, connection pooler handles serverless connection management

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Creating PrismaClient on every import - exhausts database connections during hot reload
- Using `prisma` instead of `tx` in interactive transactions - bypasses transaction context
- N+1 queries in loops - use `include` or `select` instead
- Missing `@relation` attributes - ambiguous foreign keys cause migration errors

**Medium Priority Issues:**

- No indexes on frequently filtered columns - slow queries as data grows
- Offset pagination on large tables - performance degrades linearly
- Missing `onDelete` cascade - orphaned records when parent deleted
- Fetching all fields with `include` when only some needed - use `select`

**Gotchas & Edge Cases:**

- `createMany` doesn't return created records (use `createManyAndReturn` on PostgreSQL/CockroachDB/SQLite)
- `updateMany` and `deleteMany` don't trigger `@updatedAt` hooks
- Implicit many-to-many tables can't have extra fields - use explicit join model
- `Json` fields are typed as `JsonValue` - need runtime validation at parse boundary
- `Decimal` fields return `Prisma.Decimal` type - convert with `.toNumber()`
- Interactive transactions have default 5s timeout - increase with `timeout` option
- Interactive transactions hold database connections - keep them short
- `findFirst` without `orderBy` returns non-deterministic results
- Enum changes require a migration to add/remove values

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use the singleton pattern for PrismaClient in development to prevent connection exhaustion from hot reloading)**

**(You MUST use `tx` parameter (NOT `prisma`) inside interactive transaction callbacks to ensure atomicity)**

**(You MUST use `include` or nested `select` for relational queries - avoid N+1 by fetching relations in the same query)**

**(You MUST define `@relation` with explicit `fields` and `references` for all foreign key relationships)**

**Failure to follow these rules will exhaust database connections, break transaction atomicity, cause N+1 performance problems, and create unclear relation definitions.**

</critical_reminders>
