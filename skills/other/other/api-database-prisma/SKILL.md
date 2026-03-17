---
name: api-database-prisma
description: Prisma ORM, type-safe queries, migrations, relations
---

# Database with Prisma ORM

> **Quick Guide:** Use Prisma ORM for type-safe database queries with auto-generated TypeScript types. Schema-first design with declarative migrations. Use `include` for relations, `$transaction` for atomic operations. Singleton pattern required in development to avoid connection exhaustion.

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

**Detailed Resources:**

- For code examples:
  - [queries.md](examples/queries.md) - CRUD operations, filtering, and sorting
  - [relations.md](examples/relations.md) - Relational queries, includes, N+1 prevention
  - [transactions.md](examples/transactions.md) - Atomic operations and interactive transactions
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

**Auto-detection:** prisma, @prisma/client, PrismaClient, prisma.schema, prisma migrate, findUnique, findMany, include, $transaction

**When to use:**

- Type-safe database queries with auto-generated TypeScript types
- Schema-first development with declarative migrations
- Rapid prototyping with Prisma Studio GUI
- Applications requiring strong relational data modeling

**When NOT to use:**

- Need raw SQL performance for complex queries (Prisma adds overhead)
- Edge runtime environments (use Drizzle with HTTP drivers)
- Non-TypeScript projects (lose primary benefit)
- Need fine-grained control over generated SQL

**Key patterns covered:**

- PrismaClient singleton (development hot reload safety)
- Schema definition (models, relations, enums)
- CRUD operations (create, read, update, delete, upsert)
- Relational queries with `include` and nested `select`
- Filtering with `where`, `AND`, `OR`, `NOT`
- Pagination (offset and cursor-based)
- Transactions (nested writes, batch, interactive)
- Migrations with Prisma Migrate

---

<philosophy>

## Philosophy

**Prisma ORM** provides a declarative schema language that generates type-safe database clients. The schema serves as the single source of truth for your data model, TypeScript types, and migrations.

**Core principles:**

1. **Schema-first design** - Define models in `schema.prisma`, generate everything else
2. **Type safety everywhere** - All queries fully typed based on your schema
3. **Declarative migrations** - Schema changes automatically generate migration SQL
4. **Intuitive API** - Queries read like English (`prisma.user.findMany()`)

**When to use Prisma:**

- Greenfield projects needing rapid development with type safety
- Teams wanting clear schema documentation
- Applications with complex relational data models
- Projects requiring visual database management (Prisma Studio)

**When NOT to use Prisma:**

- Performance-critical applications needing optimized raw SQL
- Edge/serverless requiring minimal cold start (use lighter ORMs)
- Legacy databases with unconventional naming (mapping overhead)
- Need for advanced database features not yet supported

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: PrismaClient Singleton

Use singleton pattern to prevent connection pool exhaustion during development hot reloading.

#### Configuration

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

**Why good:** `globalThis` persists across hot reloads preventing "10 Prisma Clients running" warning, conditional logging avoids production noise, factory function allows configuration changes

```typescript
// WRONG: New client every import
import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient(); // Creates new instance on every hot reload
```

**Why bad:** Each hot reload creates new PrismaClient with its own connection pool, quickly exhausts database connections (PostgreSQL default is 100)

---

### Pattern 2: Schema Definition

Define models with relations, constraints, and defaults in `schema.prisma`.

#### Basic Model

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      Role     @default(USER)
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users") // Maps to snake_case table name
}

model Post {
  id          String   @id @default(cuid())
  title       String
  content     String?
  published   Boolean  @default(false)
  author      User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId    String
  categories  Category[]
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([authorId])
  @@map("posts")
}

model Profile {
  id     String  @id @default(cuid())
  bio    String?
  user   User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String  @unique

  @@map("profiles")
}

model Category {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]

  @@map("categories")
}
```

**Why good:** `@id @default(cuid())` generates collision-resistant IDs, `@updatedAt` auto-updates timestamp, `@relation` with `onDelete: Cascade` prevents orphaned records, `@@index` optimizes foreign key lookups, `@@map` allows snake_case in DB with PascalCase in code

---

### Pattern 3: CRUD Operations

Type-safe create, read, update, delete operations.

#### Constants

```typescript
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;
```

#### Create Operations

```typescript
// Create single record
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    role: "USER",
  },
});

// Create with relation
const userWithProfile = await prisma.user.create({
  data: {
    email: "bob@example.com",
    name: "Bob",
    profile: {
      create: { bio: "Software engineer" },
    },
  },
  include: { profile: true },
});

// Bulk create
const createCount = await prisma.user.createMany({
  data: [
    { email: "user1@example.com", name: "User 1" },
    { email: "user2@example.com", name: "User 2" },
  ],
  skipDuplicates: true, // Ignore conflicts on unique fields
});
```

#### Read Operations

```typescript
// Find by unique field
const user = await prisma.user.findUnique({
  where: { email: "alice@example.com" },
});

// Find first matching
const admin = await prisma.user.findFirst({
  where: { role: "ADMIN" },
  orderBy: { createdAt: "desc" },
});

// Find many with filtering
const users = await prisma.user.findMany({
  where: {
    role: { in: ["USER", "MODERATOR"] },
    createdAt: { gte: new Date("2024-01-01") },
  },
  orderBy: { name: "asc" },
  take: DEFAULT_PAGE_SIZE,
});
```

#### Update Operations

```typescript
// Update single record
const updated = await prisma.user.update({
  where: { id: userId },
  data: { name: "Updated Name" },
});

// Update many
const updateCount = await prisma.user.updateMany({
  where: { role: "USER" },
  data: { role: "MODERATOR" },
});

// Upsert (create or update)
const upserted = await prisma.user.upsert({
  where: { email: "alice@example.com" },
  create: { email: "alice@example.com", name: "Alice" },
  update: { name: "Alice Updated" },
});
```

#### Delete Operations

```typescript
// Delete single record
const deleted = await prisma.user.delete({
  where: { id: userId },
});

// Delete many
const deleteCount = await prisma.user.deleteMany({
  where: { createdAt: { lt: new Date("2020-01-01") } },
});
```

**Why good:** Type-safe operations catch errors at compile time, `findUnique` returns `T | null` forcing null handling, `skipDuplicates` handles bulk insert conflicts gracefully, `upsert` is atomic avoiding race conditions

---

### Pattern 4: Relational Queries

Fetch related data efficiently using `include` or nested `select`.

#### Include Pattern

```typescript
// Include related records
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

// Deeply nested includes
const postWithDetails = await prisma.post.findUnique({
  where: { id: postId },
  include: {
    author: {
      include: { profile: true },
    },
    categories: true,
  },
});
```

#### Select Pattern (Optimized)

```typescript
// Select specific fields only
const userSummary = await prisma.user.findUnique({
  where: { id: userId },
  select: {
    id: true,
    name: true,
    email: true,
    posts: {
      select: { id: true, title: true },
      where: { published: true },
    },
  },
});
```

**Why good:** `include` fetches all fields of relations, `select` fetches only specified fields reducing payload, filtering within `include`/`select` happens at database level, single query avoids N+1 problem

```typescript
// WRONG: N+1 query pattern
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({
    where: { authorId: user.id },
  });
}
```

**Why bad:** Executes N+1 queries (1 for users + N for each user's posts), extremely slow with large datasets

---

### Pattern 5: Filtering and Sorting

Build complex queries with type-safe filters.

#### Basic Filters

```typescript
// Equality and comparisons
const posts = await prisma.post.findMany({
  where: {
    published: true,
    createdAt: { gte: new Date("2024-01-01") },
    title: { contains: "prisma", mode: "insensitive" },
  },
});

// Combining with AND (implicit)
const users = await prisma.user.findMany({
  where: {
    role: "USER",
    email: { endsWith: "@company.com" },
    name: { not: null },
  },
});
```

#### Logical Operators

```typescript
// OR conditions
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: { endsWith: "@gmail.com" } },
      { email: { endsWith: "@outlook.com" } },
    ],
  },
});

// Combined AND, OR, NOT
const posts = await prisma.post.findMany({
  where: {
    AND: [
      { published: true },
      {
        OR: [
          { title: { contains: "prisma" } },
          { content: { contains: "prisma" } },
        ],
      },
    ],
    NOT: { authorId: excludedUserId },
  },
});
```

#### Relation Filters

```typescript
// Filter by related records
const usersWithPublishedPosts = await prisma.user.findMany({
  where: {
    posts: {
      some: { published: true }, // At least one published post
    },
  },
});

const usersWithAllPublishedPosts = await prisma.user.findMany({
  where: {
    posts: {
      every: { published: true }, // All posts are published
    },
  },
});
```

**Why good:** `mode: "insensitive"` enables case-insensitive search, relation filters (`some`, `every`, `none`) eliminate manual joins, type inference catches invalid field names at compile time

---

### Pattern 6: Pagination

Implement offset and cursor-based pagination.

#### Offset Pagination

```typescript
const DEFAULT_PAGE_SIZE = 20;
const MAX_PAGE_SIZE = 100;

type PaginationParams = {
  page?: number;
  pageSize?: number;
};

const getPaginatedUsers = async ({
  page = 1,
  pageSize = DEFAULT_PAGE_SIZE,
}: PaginationParams) => {
  const take = Math.min(pageSize, MAX_PAGE_SIZE);
  const skip = (page - 1) * take;

  const [users, total] = await prisma.$transaction([
    prisma.user.findMany({
      skip,
      take,
      orderBy: { createdAt: "desc" },
    }),
    prisma.user.count(),
  ]);

  return {
    data: users,
    meta: {
      total,
      page,
      pageSize: take,
      totalPages: Math.ceil(total / take),
    },
  };
};
```

**When to use:** Small datasets, need random page access, traditional page navigation UI

#### Cursor Pagination

```typescript
type CursorPaginationParams = {
  cursor?: string;
  take?: number;
};

const getCursorPaginatedPosts = async ({
  cursor,
  take = DEFAULT_PAGE_SIZE,
}: CursorPaginationParams) => {
  const posts = await prisma.post.findMany({
    take: take + 1, // Fetch one extra to check for next page
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1, // Skip the cursor itself
    }),
    orderBy: { id: "asc" },
    where: { published: true },
  });

  const hasNextPage = posts.length > take;
  const data = hasNextPage ? posts.slice(0, -1) : posts;

  return {
    data,
    nextCursor: hasNextPage ? data[data.length - 1]?.id : undefined,
  };
};
```

**When to use:** Large datasets, infinite scroll UI, real-time data where offset would shift

**Why good:** Cursor pagination scales to millions of rows efficiently, offset pagination provides familiar page numbers, `take + 1` pattern efficiently detects next page existence

---

### Pattern 7: Transactions

Ensure atomic operations with transactions.

#### Nested Writes (Implicit Transaction)

```typescript
// Atomic creation of related records
const user = await prisma.user.create({
  data: {
    email: "alice@example.com",
    name: "Alice",
    profile: {
      create: { bio: "Developer" },
    },
    posts: {
      create: [
        { title: "First Post", published: true },
        { title: "Draft Post" },
      ],
    },
  },
  include: { profile: true, posts: true },
});
// All succeed or all fail - no partial state
```

#### Batch Transaction

```typescript
// Multiple independent operations atomically
const [deletedPosts, updatedUser] = await prisma.$transaction([
  prisma.post.deleteMany({ where: { authorId: userId, published: false } }),
  prisma.user.update({
    where: { id: userId },
    data: { name: "Updated Name" },
  }),
]);
```

#### Interactive Transaction

```typescript
// Complex logic with reads and conditional writes
const MINIMUM_BALANCE = 0;

const transferFunds = async (fromId: string, toId: string, amount: number) => {
  return await prisma.$transaction(async (tx) => {
    // Read within transaction
    const sender = await tx.account.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } },
    });

    // Validate business logic
    if (sender.balance < MINIMUM_BALANCE) {
      throw new Error("Insufficient funds");
    }

    // Complete the transfer
    const recipient = await tx.account.update({
      where: { id: toId },
      data: { balance: { increment: amount } },
    });

    return { sender, recipient };
  });
};
```

**Why good:** Nested writes are cleanest for creating related records, batch transactions combine multiple models atomically, interactive transactions enable complex business logic with rollback on error

```typescript
// WRONG: Using prisma instead of tx
await prisma.$transaction(async (tx) => {
  await prisma.post.create({ data: { title: "Post" } }); // Uses prisma, not tx!
  await tx.user.update({ where: { id: "1" }, data: { name: "Updated" } });
});
```

**Why bad:** Operations using `prisma` bypass transaction context, only `tx` operations will rollback on failure, causes inconsistent data

---

### Pattern 8: Connection Management

Handle connections properly for different environments.

#### Graceful Shutdown

```typescript
// Handle cleanup on process termination
process.on("beforeExit", async () => {
  await prisma.$disconnect();
});

// For server shutdown hooks
const shutdown = async () => {
  await prisma.$disconnect();
  process.exit(0);
};
```

#### Connection in Serverless

```typescript
// lib/db/serverless-client.ts
import { PrismaClient } from "@prisma/client";

// Serverless environments create new instances per invocation
// Use connection pooler (PgBouncer, Prisma Accelerate) for production
export const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL_WITH_POOLER, // Connection pooler URL
    },
  },
});
```

**Why good:** Graceful shutdown prevents connection leaks, connection pooler handles serverless connection management, separate URL for pooled connections

</patterns>

---

<integration>

## Integration Guide

### Usage in Application Code

Import the singleton client and use throughout your application:

```typescript
// In your application code
import { prisma } from "@/lib/db/client";

// Query data
const users = await prisma.user.findMany();
```

### Type Reuse

Use Prisma's generated types with your validation layer:

```typescript
import type { Prisma } from "@prisma/client";

// Prisma generates input/output types based on your schema
type CreateUserInput = Prisma.UserCreateInput;
type UserWithPosts = Prisma.UserGetPayload<{
  include: { posts: true };
}>;
```

### Environment Configuration

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"

# For serverless with connection pooler
DATABASE_URL_WITH_POOLER="postgresql://user:password@pooler.example.com:6543/mydb"
```

</integration>

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
