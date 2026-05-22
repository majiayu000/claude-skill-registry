---
name: "Drizzle ORM"
description: "TypeScript-first ORM patterns for PostgreSQL, MySQL, and SQLite. Use when writing database schemas, queries, migrations, relations, or transactions with Drizzle ORM."
---

# Drizzle ORM

## What This Skill Does

Provides comprehensive guidance for Drizzle ORM - a lightweight, TypeScript-first ORM that mirrors SQL syntax while maintaining full type safety. Covers schema definition, queries, relations, transactions, and migrations for PostgreSQL, MySQL, and SQLite.

## Prerequisites

- `drizzle-orm` package installed
- `drizzle-kit` for migrations
- Database driver (pg, mysql2, better-sqlite3, etc.)

## Quick Start

```typescript
// 1. Define schema
import { pgTable, serial, text } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
});

// 2. Initialize database connection
import { drizzle } from "drizzle-orm/node-postgres";
const db = drizzle(process.env.DATABASE_URL);

// 3. Query with full type safety
const allUsers = await db.select().from(users);
//    ^? { id: number; name: string; }[]
```

---

## Core Philosophy

### Key Principles

1. **SQL-Like Syntax:** Drizzle mirrors SQL structure, not abstracted ORM patterns
2. **Type Safety First:** Full TypeScript inference from schema to queries
3. **Explicit Over Magic:** No hidden queries, lazy loading, or N+1 problems
4. **Composable Queries:** Build queries programmatically with type safety
5. **Database-First or Code-First:** Choose your migration strategy

### Two Query APIs

**SQL-Like Query Builder** (Core API):
```typescript
await db.select().from(users).where(eq(users.id, 1));
```

**Relational Query Builder** (Simpler for relations):
```typescript
await db.query.users.findMany({
  with: { posts: true }
});
```

Both are fully type-safe and generate identical SQL under the hood.

---

## Schema Definition Patterns

### Basic Table Definition

```typescript
import { pgTable, serial, text, integer, boolean, timestamp } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  age: integer("age"),
  verified: boolean("verified").default(false),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Type inference helpers
type User = typeof users.$inferSelect;      // { id: number; name: string; ... }
type NewUser = typeof users.$inferInsert;   // Omits id, uses defaults
```

### Column Aliases (TypeScript != Database)

```typescript
// Use different names in code vs database
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  firstName: text("first_name"),  // TS: firstName, DB: first_name
  lastName: text("last_name"),
});

// Or use automatic snake_case mapping
const db = drizzle({
  connection: process.env.DATABASE_URL,
  casing: "snake_case"  // Auto-converts camelCase -> snake_case
});
```

### Dialect-Specific Tables

```typescript
// PostgreSQL
import { pgTable, serial, text } from "drizzle-orm/pg-core";
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name"),
});

// MySQL
import { mysqlTable, int, varchar } from "drizzle-orm/mysql-core";
export const users = mysqlTable("users", {
  id: int("id").primaryKey().autoincrement(),
  name: varchar("name", { length: 255 }),
});

// SQLite
import { sqliteTable, integer, text } from "drizzle-orm/sqlite-core";
export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  name: text("name"),
});
```

### Constraints & Indexes

```typescript
import { pgTable, serial, text, uniqueIndex, index } from "drizzle-orm/pg-core";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: text("email").notNull(),
  name: text("name"),
}, (table) => [
  uniqueIndex("email_idx").on(table.email),
  index("name_idx").on(table.name),
  index("name_email_idx").on(table.name, table.email),
]);
```

### Foreign Keys & Relations

```typescript
import { pgTable, serial, text, integer } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
});

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  content: text("content").notNull(),
  authorId: integer("author_id")
    .notNull()
    .references(() => users.id, {
      onDelete: "cascade",
      onUpdate: "cascade"
    }),
});

// Define relations for relational queries (query-only, not DB constraints)
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### Enums

```typescript
// PostgreSQL native enum
import { pgEnum, pgTable, serial } from "drizzle-orm/pg-core";

export const roleEnum = pgEnum("role", ["guest", "user", "admin"]);

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  role: roleEnum().default("guest"),
});

// SQLite (no native enum, use text with type constraint)
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey(),
  role: text("role").$type<"guest" | "user" | "admin">().default("guest"),
});
```

### Reusable Column Patterns

```typescript
// columns.helpers.ts
import { timestamp } from "drizzle-orm/pg-core";

export const timestamps = {
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
  deletedAt: timestamp("deleted_at"),
};

// users.ts
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name"),
  ...timestamps,  // Spread pattern
});
```

---

## Query Building & Execution

### Basic SELECT Queries

```typescript
// Select all columns
const allUsers = await db.select().from(users);

// Partial select
const names = await db.select({
  id: users.id,
  name: users.name
}).from(users);

// Select with SQL expression
import { sql } from "drizzle-orm";

const result = await db.select({
  id: users.id,
  lowerName: sql<string>`lower(${users.name})`.as("lower_name"),
}).from(users);
```

### Filtering with WHERE

```typescript
import { eq, gt, gte, lt, lte, ne, like, ilike, inArray, between, and, or, not, isNull, isNotNull } from "drizzle-orm";

// Single condition
await db.select().from(users).where(eq(users.id, 42));

// Multiple conditions (AND)
await db.select().from(users).where(
  and(
    eq(users.role, "admin"),
    gt(users.age, 18)
  )
);

// OR conditions
await db.select().from(users).where(
  or(
    eq(users.role, "admin"),
    eq(users.role, "moderator")
  )
);

// Common operators
await db.select().from(users).where(gt(users.age, 18));           // age > 18
await db.select().from(users).where(like(users.name, "%John%"));  // name LIKE '%John%'
await db.select().from(users).where(ilike(users.email, "%@gmail.com")); // case-insensitive
await db.select().from(users).where(inArray(users.id, [1, 2, 3]));
await db.select().from(users).where(between(users.age, 18, 65));
await db.select().from(users).where(isNull(users.deletedAt));
```

### Dynamic/Conditional Filters

```typescript
import { and, type SQL } from "drizzle-orm";

const searchUsers = async (filters: { name?: string; minAge?: number }) => {
  const conditions: SQL[] = [];

  if (filters.name) {
    conditions.push(like(users.name, `%${filters.name}%`));
  }
  if (filters.minAge) {
    conditions.push(gte(users.age, filters.minAge));
  }

  return db.select().from(users)
    .where(conditions.length > 0 ? and(...conditions) : undefined);
};
```

### ORDER BY, LIMIT, OFFSET

```typescript
import { asc, desc } from "drizzle-orm";

// Pagination
await db.select().from(users)
  .orderBy(desc(users.createdAt))
  .limit(10)
  .offset(20);

// Pagination helper
const getUsers = async (page = 1, pageSize = 10) => {
  return db.select().from(users)
    .orderBy(users.id)
    .limit(pageSize)
    .offset((page - 1) * pageSize);
};
```

### Aggregations

```typescript
import { count, sum, avg, min, max } from "drizzle-orm";

// Count with groupBy
const roleStats = await db.select({
  role: users.role,
  count: count(),
}).from(users).groupBy(users.role);

// $count helper (simplified count)
const userCount = await db.$count(users);
const adminCount = await db.$count(users, eq(users.role, "admin"));
```

---

## INSERT Operations

### Basic Insert

```typescript
// Insert single row
await db.insert(users).values({
  name: "John Doe",
  email: "john@example.com",
});

// Insert multiple rows
await db.insert(users).values([
  { name: "Alice", email: "alice@example.com" },
  { name: "Bob", email: "bob@example.com" },
]);
```

### Insert with RETURNING (PostgreSQL/SQLite)

```typescript
const [user] = await db.insert(users)
  .values({ name: "Jane", email: "jane@example.com" })
  .returning();

// Return specific columns
const [result] = await db.insert(users)
  .values({ name: "Jane", email: "jane@example.com" })
  .returning({ insertedId: users.id });
```

### Upserts (ON CONFLICT)

```typescript
// Do nothing on conflict
await db.insert(users)
  .values({ id: 1, name: "John", email: "john@example.com" })
  .onConflictDoNothing({ target: users.email });

// Update on conflict
await db.insert(users)
  .values({ email: "john@example.com", name: "John Updated" })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: "John Updated" },
  });
```

---

## UPDATE Operations

### Basic Update

```typescript
await db.update(users)
  .set({ name: "Mr. Dan" })
  .where(eq(users.id, 42));

// Undefined values are ignored, use null explicitly
await db.update(users)
  .set({
    middleName: null,        // Sets to NULL
    nickname: undefined,     // Ignored (not updated)
  })
  .where(eq(users.id, 1));
```

### Update with SQL Expressions

```typescript
// Increment counter
await db.update(posts)
  .set({ views: sql`${posts.views} + 1` })
  .where(eq(posts.id, 1));
```

### Update with RETURNING (PostgreSQL/SQLite)

```typescript
const [updatedUser] = await db.update(users)
  .set({ name: "John Smith" })
  .where(eq(users.id, 1))
  .returning();
```

---

## DELETE Operations

```typescript
// Delete with WHERE
await db.delete(users).where(eq(users.id, 42));

// Delete with RETURNING
const deletedUsers = await db.delete(users)
  .where(eq(users.role, "guest"))
  .returning();
```

---

## Relations & Joins

### Relational Query API

```typescript
// Must pass schema to drizzle()
import * as schema from "./schema";
const db = drizzle({ client, schema });

// Find with relations
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

// Nested relations with filters
const result = await db.query.users.findMany({
  columns: {
    id: true,
    name: true,
  },
  with: {
    posts: {
      where: (posts, { eq }) => eq(posts.published, true),
      limit: 5,
      orderBy: (posts, { desc }) => [desc(posts.createdAt)],
      columns: {
        id: true,
        title: true,
      },
    },
  },
});
```

### SQL Joins (Core API)

```typescript
import { eq } from "drizzle-orm";

// LEFT JOIN
const result = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));
// Result: { users: User; posts: Post | null }[]

// INNER JOIN
const result = await db
  .select()
  .from(users)
  .innerJoin(posts, eq(users.id, posts.authorId));
// Result: { users: User; posts: Post }[]

// Partial select with joins
const result = await db
  .select({
    userId: users.id,
    userName: users.name,
    postTitle: posts.title,
  })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));
```

---

## Transactions

### Basic Transaction

```typescript
await db.transaction(async (tx) => {
  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));

  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} + 100` })
    .where(eq(accounts.userId, 2));
});
```

### Transaction Rollback

```typescript
await db.transaction(async (tx) => {
  const [account] = await tx.select()
    .from(accounts)
    .where(eq(accounts.userId, 1));

  if (account.balance < 100) {
    tx.rollback();  // Throws error to rollback
  }

  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));
});
```

### Return Values from Transactions

```typescript
const newBalance = await db.transaction(async (tx) => {
  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));

  const [account] = await tx.select({ balance: accounts.balance })
    .from(accounts)
    .where(eq(accounts.userId, 1));

  return account.balance;
});
```

---

## Migrations

### Configuration File

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",  // "mysql" | "sqlite" | "turso"
  schema: "./src/db/schema",
  out: "./drizzle",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Migration Commands

```bash
# Generate migration files
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push without migrations (prototyping only)
npx drizzle-kit push

# Pull from database
npx drizzle-kit pull

# Check for pending migrations
npx drizzle-kit check

# Studio (database browser)
npx drizzle-kit studio
```

### Runtime Migrations

```typescript
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";

const db = drizzle(process.env.DATABASE_URL!);

await migrate(db, { migrationsFolder: "./drizzle" });
```

---

## Advanced Query Patterns

### WITH Clause (CTEs)

```typescript
const sq = db.$with("sq").as(
  db.select().from(users).where(eq(users.id, 42))
);

const result = await db.with(sq).select().from(sq);
```

### Subqueries

```typescript
// Subquery in WHERE
const result = await db.select().from(users).where(
  inArray(
    users.id,
    db.select({ id: posts.authorId }).from(posts)
  )
);
```

### Dynamic Query Building

```typescript
import { type PgSelect } from "drizzle-orm/pg-core";

function withPagination<T extends PgSelect>(
  qb: T,
  page = 1,
  pageSize = 10
) {
  return qb.limit(pageSize).offset((page - 1) * pageSize);
}

let dynamicQuery = db.select().from(users).$dynamic();
dynamicQuery = withPagination(dynamicQuery, 2, 20);
const results = await dynamicQuery;
```

### Prepared Statements

```typescript
const prepared = db.select()
  .from(users)
  .where(eq(users.id, placeholder("id")))
  .prepare("get_user_by_id");

const user = await prepared.execute({ id: 1 });
```

---

## The Magic `sql` Operator

### Basic Usage

```typescript
import { sql } from "drizzle-orm";

// Raw SQL in queries (parameterized - safe from injection)
await db.execute(sql`SELECT * FROM users WHERE id = ${42}`);

// In SELECT with type annotation
const result = await db.select({
  id: users.id,
  upperName: sql<string>`upper(${users.name})`,
}).from(users);
```

### Type Annotations

```typescript
const result = await db.select({
  count: sql<number>`count(*)`.mapWith(Number),
  avg: sql<number>`avg(${users.age})`,
}).from(users);
```

### Raw SQL (No Escaping) - Use with Caution

```typescript
// sql.raw() - no parameterization (dangerous with user input!)
const tableName = "users";
await db.execute(sql`SELECT * FROM ${sql.raw(tableName)}`);
```

### Building SQL Dynamically

```typescript
const conditions = [
  sql`${users.age} > 18`,
  sql`${users.verified} = true`,
];
const where = sql.join(conditions, sql` AND `);
// Result: age > 18 AND verified = true
```

---

## Common Patterns & Best Practices

### Repository Pattern

```typescript
export class UsersRepository {
  async findById(id: number) {
    return db.query.users.findFirst({
      where: (users, { eq }) => eq(users.id, id),
    });
  }

  async create(data: typeof users.$inferInsert) {
    const [user] = await db.insert(users).values(data).returning();
    return user;
  }

  async update(id: number, data: Partial<typeof users.$inferInsert>) {
    const [user] = await db.update(users)
      .set(data)
      .where(eq(users.id, id))
      .returning();
    return user;
  }
}
```

### Soft Deletes

```typescript
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  deletedAt: timestamp("deleted_at"),
});

const activeUsers = () =>
  db.select().from(users).where(isNull(users.deletedAt));

const softDelete = async (id: number) => {
  await db.update(users)
    .set({ deletedAt: new Date() })
    .where(eq(users.id, id));
};
```

### Incremental Fields

```typescript
// Increment views
await db.update(posts)
  .set({ views: sql`${posts.views} + 1` })
  .where(eq(posts.id, postId));

// Toggle boolean
await db.update(users)
  .set({ verified: sql`NOT ${users.verified}` })
  .where(eq(users.id, userId));
```

---

## Critical Rules & Gotchas

### Schema & Types

| DO | DON'T |
|----|-------|
| Use dialect-specific table constructors (`pgTable`, `mysqlTable`, `sqliteTable`) | Mix table constructors across dialects |
| Export tables and relations for relational queries | Forget to export schema for Drizzle Kit |
| Use `$inferSelect` and `$inferInsert` for type inference | Use optional (`?`) in TS types instead of schema validators |
| Use `.notNull()` to enforce required fields | Assume foreign keys exist without defining them |

### Queries

| DO | DON'T |
|----|-------|
| Use prepared statements for repeated queries | Chain multiple `.where()` calls (use `and()` or `or()`) |
| Use `.$dynamic()` for conditional query building | Use `sql.raw()` with user input (SQL injection risk) |
| Explicitly type `sql<T>` for custom expressions | Forget `.as()` when using `sql` in SELECT |
| Use `.mapWith()` for runtime type transformations | Assume `sql<T>` performs runtime type casting |

### Relations

| DO | DON'T |
|----|-------|
| Define relations for relational query API | Confuse relations (query-only) with foreign keys (DB constraints) |
| Pass schema to `drizzle()` for relational queries | Expect relations to create foreign keys automatically |
| Use `relationName` to disambiguate multiple relations | Use relational queries without passing schema |

### Transactions

| DO | DON'T |
|----|-------|
| Use transactions for multi-step operations | Catch errors inside transactions without re-throwing |
| Use nested transactions (savepoints) when needed | Use original `db` inside transaction callback (use `tx`) |
| Call `tx.rollback()` to abort | Assume transactions are SERIALIZABLE by default |

### Performance

| DO | DON'T |
|----|-------|
| Use indexes on foreign keys and frequently queried columns | Select all columns when you need only a few |
| Use prepared statements for repeated queries | Perform N+1 queries (use joins or relational queries) |
| Batch operations in transactions | Forget to add indexes on join columns |

---

## Database-Specific Features

### PostgreSQL

```typescript
// Arrays
export const posts = pgTable("posts", {
  tags: text("tags").array(),
});

// JSON/JSONB
export const users = pgTable("users", {
  metadata: jsonb("metadata").$type<{ theme: string }>(),
});

// UUID
export const users = pgTable("users", {
  id: uuid("id").defaultRandom().primaryKey(),
});

// Schemas (namespaces)
const mySchema = pgSchema("my_schema");
export const users = mySchema.table("users", { ... });
```

### SQLite

```typescript
// INTEGER PRIMARY KEY = auto-increment
export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
});

// Type-safe enums (using text + TypeScript)
export const users = sqliteTable("users", {
  role: text("role").$type<"admin" | "user">().default("user"),
});
```

---

## Reference Map

### Core Documentation
- Quick Start: https://orm.drizzle.team/docs/get-started
- Schema Declaration: https://orm.drizzle.team/docs/sql-schema-declaration
- Database Connection: https://orm.drizzle.team/docs/connect-overview
- Queries Overview: https://orm.drizzle.team/docs/data-querying
- Migrations: https://orm.drizzle.team/docs/migrations

### Query Operations
- Select: https://orm.drizzle.team/docs/select
- Insert: https://orm.drizzle.team/docs/insert
- Update: https://orm.drizzle.team/docs/update
- Delete: https://orm.drizzle.team/docs/delete
- Relational Queries: https://orm.drizzle.team/docs/rqb
- Joins: https://orm.drizzle.team/docs/joins
- Filters & Operators: https://orm.drizzle.team/docs/operators

### Advanced Features
- Transactions: https://orm.drizzle.team/docs/transactions
- Dynamic Query Building: https://orm.drizzle.team/docs/dynamic-query-building
- Magic sql Operator: https://orm.drizzle.team/docs/sql

### Migrations & Tools
- Drizzle Kit Overview: https://orm.drizzle.team/docs/kit-overview
- drizzle-kit generate: https://orm.drizzle.team/docs/drizzle-kit-generate
- drizzle-kit migrate: https://orm.drizzle.team/docs/drizzle-kit-migrate
- drizzle-kit push: https://orm.drizzle.team/docs/drizzle-kit-push
- drizzle-kit studio: https://orm.drizzle.team/docs/drizzle-kit-studio
