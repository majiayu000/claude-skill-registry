---
name: drizzle-orm-patterns
description: Provides comprehensive Drizzle ORM patterns for schema definition, CRUD operations, relations, queries, transactions, and migrations. Proactively use for any Drizzle ORM development including defining database schemas, writing type-safe queries, implementing relations, managing transactions, and setting up migrations with Drizzle Kit. Supports PostgreSQL, MySQL, SQLite, MSSQL, and CockroachDB.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Drizzle ORM Patterns

## Overview

Expert guide for building type-safe database applications with Drizzle ORM. Covers schema definition, relations, queries, transactions, and migrations for all supported databases.

## When to Use

- Defining database schemas with tables, columns, and constraints
- Creating relations between tables (one-to-one, one-to-many, many-to-many)
- Writing type-safe CRUD queries
- Implementing complex joins and aggregations
- Managing database transactions with rollback
- Setting up migrations with Drizzle Kit
- Working with PostgreSQL, MySQL, SQLite, MSSQL, or CockroachDB

## Instructions

1. **Identify your database dialect** - Choose PostgreSQL, MySQL, SQLite, MSSQL, or CockroachDB
2. **Define your schema** - Use the appropriate table function (pgTable, mysqlTable, etc.)
3. **Set up relations** - Define relations using `relations()` or `defineRelations()` for complex relationships
4. **Initialize the database client** - Create your Drizzle client with proper credentials
5. **Write queries** - Use the query builder for type-safe CRUD operations
6. **Handle transactions** - Wrap multi-step operations in transactions when needed
7. **Set up migrations** - Configure Drizzle Kit for schema management

## Examples

### Example 1: Create a Complete Schema with Relations

```typescript
import { pgTable, serial, text, integer, timestamp } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// Define tables
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: timestamp('created_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  authorId: integer('author_id').references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
});

// Define relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, { fields: [posts.authorId], references: [users.id] }),
}));
```

### Example 2: CRUD Operations

```typescript
import { eq } from 'drizzle-orm';

// Insert
const [newUser] = await db.insert(users).values({
  name: 'John',
  email: 'john@example.com',
}).returning();

// Select with filter
const [user] = await db.select().from(users).where(eq(users.email, 'john@example.com'));

// Update
const [updated] = await db.update(users)
  .set({ name: 'John Updated' })
  .where(eq(users.id, 1))
  .returning();

// Delete
await db.delete(users).where(eq(users.id, 1));
```

### Example 3: Transaction with Rollback

```typescript
async function transferFunds(fromId: number, toId: number, amount: number) {
  await db.transaction(async (tx) => {
    const [from] = await tx.select().from(accounts).where(eq(accounts.userId, fromId));

    if (from.balance < amount) {
      tx.rollback(); // Rolls back all changes
    }

    await tx.update(accounts)
      .set({ balance: sql`${accounts.balance} - ${amount}` })
      .where(eq(accounts.userId, fromId));

    await tx.update(accounts)
      .set({ balance: sql`${accounts.balance} + ${amount}` })
      .where(eq(accounts.userId, toId));
  });
}
```

## Schema Definition

### PostgreSQL Table

```typescript
import { pgTable, serial, text, integer, boolean, timestamp, pgEnum } from 'drizzle-orm/pg-core';

// Enum definition
export const rolesEnum = pgEnum('roles', ['guest', 'user', 'admin']);

// Table with all column types
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  role: rolesEnum().default('user'),
  verified: boolean('verified').notNull().default(false),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});
```

### MySQL Table

```typescript
import { mysqlTable, serial, text, int, tinyint, datetime } from 'drizzle-orm/mysql-core';

export const users = mysqlTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  verified: tinyint('verified').notNull().default(0),
  createdAt: datetime('created_at').notNull().defaultNow(),
});
```

### SQLite Table

```typescript
import { sqliteTable, integer, text } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
});
```

### Indexes and Constraints

```typescript
import { uniqueIndex, index, primaryKey } from 'drizzle-orm/pg-core';

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  title: text('title').notNull(),
  slug: text('slug').notNull(),
  authorId: integer('author_id').references(() => users.id),
  createdAt: timestamp('created_at').notNull().defaultNow(),
}, (table) => [
  uniqueIndex('slug_idx').on(table.slug),
  index('author_idx').on(table.authorId),
  index('created_idx').on(table.createdAt),
]);
```

### Composite Primary Key

```typescript
export const usersToGroups = pgTable('users_to_groups', {
  userId: integer('user_id').notNull().references(() => users.id),
  groupId: integer('group_id').notNull().references(() => groups.id),
}, (table) => [
  primaryKey({ columns: [table.userId, table.groupId] }),
]);
```

## Relations

### One-to-Many (v1 syntax)

```typescript
import { relations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
}));

export const posts = pgTable('posts', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  authorId: integer('author_id').references(() => users.id),
});

export const postsRelations = relations(posts, ({ one }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
}));
```

### One-to-One

```typescript
export const profiles = pgTable('profiles', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id).unique(),
  bio: text('bio'),
});

export const profilesRelations = relations(profiles, ({ one }) => ({
  user: one(users, {
    fields: [profiles.userId],
    references: [users.id],
  }),
}));
```

### Many-to-Many (v2 syntax)

```typescript
import { defineRelations } from 'drizzle-orm';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const groups = pgTable('groups', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
});

export const usersToGroups = pgTable('users_to_groups', {
  userId: integer('user_id').notNull().references(() => users.id),
  groupId: integer('group_id').notNull().references(() => groups.id),
}, (t) => [primaryKey({ columns: [t.userId, t.groupId] })]);

export const relations = defineRelations({ users, groups, usersToGroups }, (r) => ({
  users: {
    groups: r.many.groups({
      from: r.users.id.through(r.usersToGroups.userId),
      to: r.groups.id.through(r.usersToGroups.groupId),
    }),
  },
  groups: {
    participants: r.many.users(),
  },
}));
```

### Self-Referential Relation

```typescript
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  invitedBy: integer('invited_by').references((): AnyPgColumn => users.id),
});

export const usersRelations = relations(users, ({ one }) => ({
  invitee: one(users, {
    fields: [users.invitedBy],
    references: [users.id],
  }),
}));
```

## CRUD Operations

### Insert

```typescript
import { eq } from 'drizzle-orm';

// Single insert
await db.insert(users).values({
  name: 'John',
  email: 'john@example.com',
});

// Multiple inserts
await db.insert(users).values([
  { name: 'John', email: 'john@example.com' },
  { name: 'Jane', email: 'jane@example.com' },
]);

// Returning inserted row
const [newUser] = await db.insert(users).values({
  name: 'John',
  email: 'john@example.com',
}).returning();
```

### Select

```typescript
// Select all
const allUsers = await db.select().from(users);

// Select specific columns
const result = await db.select({
  id: users.id,
  name: users.name,
}).from(users);

// Select with where
const user = await db.select().from(users).where(eq(users.id, 1));

// Select first match
const [user] = await db.select().from(users).where(eq(users.id, 1));

// $count shorthand
const count = await db.$count(users);
const activeCount = await db.$count(users, eq(users.verified, true));
```

### Update

```typescript
await db.update(users)
  .set({ name: 'John Updated' })
  .where(eq(users.id, 1));

// With returning
const [updatedUser] = await db.update(users)
  .set({ verified: true })
  .where(eq(users.email, 'john@example.com'))
  .returning();
```

### Delete

```typescript
await db.delete(users).where(eq(users.id, 1));

// With returning
const [deletedUser] = await db.delete(users)
  .where(eq(users.email, 'john@example.com'))
  .returning();
```

## Query Operators

```typescript
import { eq, ne, gt, gte, lt, lte, like, ilike, inArray, isNull, isNotNull, and, or, between, exists, notExists } from 'drizzle-orm';

// Comparison
eq(users.id, 1)
ne(users.name, 'John')
gt(users.age, 18)
gte(users.age, 18)
lt(users.age, 65)
lte(users.age, 65)

// String matching
like(users.name, '%John%')      // case-sensitive
ilike(users.name, '%john%')     // case-insensitive

// Null checks
isNull(users.deletedAt)
isNotNull(users.deletedAt)

// Array
inArray(users.id, [1, 2, 3])

// Range
between(users.createdAt, startDate, endDate)

// Combining conditions
and(
  gte(users.age, 18),
  eq(users.verified, true)
)

or(
  eq(users.role, 'admin'),
  eq(users.role, 'moderator')
)
```

## Pagination

```typescript
import { asc, desc } from 'drizzle-orm';

// Basic pagination
const page = 1;
const pageSize = 10;

const users = await db
  .select()
  .from(users)
  .orderBy(asc(users.id))
  .limit(pageSize)
  .offset((page - 1) * pageSize);

// Cursor-based pagination (more efficient)
const lastId = 100;
const users = await db
  .select()
  .from(users)
  .where(gt(users.id, lastId))
  .orderBy(asc(users.id))
  .limit(10);
```

## Joins

```typescript
import { eq } from 'drizzle-orm';

// Left join
const result = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));

// Inner join
const result = await db
  .select()
  .from(users)
  .innerJoin(posts, eq(users.id, posts.authorId));

// Multiple joins
const result = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId))
  .leftJoin(comments, eq(posts.id, comments.postId));

// Partial select with join
const usersWithPosts = await db
  .select({
    userId: users.id,
    userName: users.name,
    postTitle: posts.title,
  })
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));

// Self-join with alias
import { alias } from 'drizzle-orm';
const parent = alias(users, 'parent');
const result = await db
  .select()
  .from(users)
  .leftJoin(parent, eq(parent.id, users.parentId));
```

## Aggregations

```typescript
import { count, sum, avg, min, max, sql, gt } from 'drizzle-orm';

// Count all
const [{ value }] = await db.select({ value: count() }).from(users);

// Count with condition
const [{ value }] = await db
  .select({ value: count(users.id) })
  .from(users)
  .where(gt(users.age, 18));

// Sum, Avg
const [stats] = await db
  .select({
    totalAge: sum(users.age),
    avgAge: avg(users.age),
  })
  .from(users);

// Min, Max
const [extremes] = await db
  .select({
    oldest: min(users.age),
    youngest: max(users.age),
  })
  .from(users);

// Group by with having
const ageGroups = await db
  .select({
    age: users.age,
    count: sql<number>`cast(count(${users.id}) as int)`,
  })
  .from(users)
  .groupBy(users.age)
  .having(({ count }) => gt(count, 1));
```

## Transactions

```typescript
// Basic transaction
await db.transaction(async (tx) => {
  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));

  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} + 100` })
    .where(eq(accounts.userId, 2));
});

// Transaction with rollback
await db.transaction(async (tx) => {
  const [account] = await tx.select()
    .from(accounts)
    .where(eq(accounts.userId, 1));

  if (account.balance < 100) {
    tx.rollback(); // Throws exception
  }

  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));
});

// Transaction with return value
const newBalance = await db.transaction(async (tx) => {
  await tx.update(accounts)
    .set({ balance: sql`${accounts.balance} - 100` })
    .where(eq(accounts.userId, 1));

  const [account] = await tx.select()
    .from(accounts)
    .where(eq(accounts.userId, 1));

  return account.balance;
});

// Nested transactions (savepoints)
await db.transaction(async (tx) => {
  await tx.insert(users).values({ name: 'John' });

  await tx.transaction(async (tx2) => {
    await tx2.insert(posts).values({ title: 'Hello', authorId: 1 });
  });
});
```

## Drizzle Kit Migrations

### Configuration (drizzle.config.ts)

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### package.json Scripts

```json
{
  "scripts": {
    "generate": "drizzle-kit generate",
    "migrate": "drizzle-kit migrate",
    "push": "drizzle-kit push",
    "pull": "drizzle-kit pull"
  }
}
```

### CLI Commands

```bash
# Generate migration files from schema
npx drizzle-kit generate

# Apply pending migrations
npx drizzle-kit migrate

# Push schema directly to DB (for development)
npx drizzle-kit push

# Pull schema from existing database
npx drizzle-kit pull
```

### Programmatic Migration

```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { migrate } from 'drizzle-orm/node-postgres/migrator';

const db = drizzle(process.env.DATABASE_URL);
await migrate(db, { migrationsFolder: './drizzle' });
```

## Type Inference

```typescript
// Infer insert type
type NewUser = typeof users.$inferInsert;
// { id: number; name: string; email: string; ... }

// Infer select type
type User = typeof users.$inferSelect;
// { id: number; name: string; email: string; ... }

// Use in functions
async function createUser(data: typeof users.$inferInsert) {
  return db.insert(users).values(data).returning();
}

async function getUser(id: number): Promise<typeof users.$inferSelect> {
  const [user] = await db.select().from(users).where(eq(users.id, id));
  return user;
}
```

## Common Patterns

### Soft Delete

```typescript
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  deletedAt: timestamp('deleted_at'),
});

// Query non-deleted only
const activeUsers = await db
  .select()
  .from(users)
  .where(isNull(users.deletedAt));

// Soft delete
await db
  .update(users)
  .set({ deletedAt: new Date() })
  .where(eq(users.id, id));
```

### Upsert

```typescript
import { onConflict } from 'drizzle-orm';

await db
  .insert(users)
  .values({ id: 1, name: 'John', email: 'john@example.com' })
  .onConflict(onConflict(users.email).doUpdateSet({
    name: excluded.name,
  }));
```

### Batch Operations

```typescript
// Batch insert
await db.insert(users).values(batch).returning();

// Batch update
const updates = batch.map(item => ({
  id: item.id,
  name: item.name,
}));
await db.insert(users).values(updates).onConflictDoNothing();
```

## Best Practices

1. **Type Safety**: Always use TypeScript and leverage `$inferInsert` / `$inferSelect`
2. **Relations**: Define relations using the relations() API for nested queries
3. **Transactions**: Use transactions for multi-step operations that must succeed together
4. **Migrations**: Use `generate` + `migrate` in production, `push` for development
5. **Indexes**: Add indexes on frequently queried columns and foreign keys
6. **Soft Deletes**: Use `deletedAt` timestamp instead of hard deletes when possible
7. **Pagination**: Use cursor-based pagination for large datasets
8. **Query Optimization**: Use `.limit()` and `.where()` to fetch only needed data

## Constraints and Warnings

- **Foreign Key Constraints**: Always define references using arrow functions `() => table.column` to avoid circular dependency issues
- **Transaction Rollback**: Calling `tx.rollback()` throws an exception - use try/catch if needed
- **Returning Clauses**: Not all databases support `.returning()` - check your dialect compatibility
- **Type Inference**: Use `InferSelectModel` and `InferInsertModel` from `drizzle-orm` for newer type-safe patterns
- **Batch Operations**: Large batch inserts may hit database limits - chunk into smaller batches
- **Migrations in Production**: Always test migrations in staging before applying to production
- **Soft Delete Queries**: Remember to always filter `deletedAt IS NULL` in queries
