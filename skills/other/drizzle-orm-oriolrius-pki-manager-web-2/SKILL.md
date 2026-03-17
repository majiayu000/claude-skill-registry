---
name: Drizzle ORM
description: Expert guidance for Drizzle ORM including schema definition, queries, relations, migrations, TypeScript integration with SQLite/PostgreSQL, and Drizzle Studio. Use this when working with type-safe database operations, schema management, or ORM queries.
---

# Drizzle ORM

Expert assistance with Drizzle ORM - TypeScript ORM for SQL databases.

## Overview

Drizzle ORM is a lightweight TypeScript ORM:
- **Type-Safe**: Full TypeScript type inference
- **SQL-Like**: Familiar SQL syntax, not a new query language
- **Performant**: Zero overhead, generates efficient SQL
- **Multiple Databases**: PostgreSQL, MySQL, SQLite support
- **Migrations**: Built-in migration system
- **Drizzle Studio**: Visual database browser

## Installation

```bash
# Core packages
npm install drizzle-orm
npm install --save-dev drizzle-kit

# Database driver (choose one)
npm install better-sqlite3              # For SQLite
npm install @types/better-sqlite3 --save-dev

# Or for PostgreSQL
npm install postgres                     # For PostgreSQL
npm install pg                           # Alternative PostgreSQL driver
```

## Quick Start (SQLite)

### 1. Define Schema

```typescript
// src/db/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').notNull().unique(),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().$defaultFn(() => new Date()),
});

export const posts = sqliteTable('posts', {
  id: text('id').primaryKey(),
  title: text('title').notNull(),
  content: text('content').notNull(),
  userId: text('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull().$defaultFn(() => new Date()),
});
```

### 2. Create Database Client

```typescript
// src/db/client.ts
import { drizzle } from 'drizzle-orm/better-sqlite3';
import Database from 'better-sqlite3';
import * as schema from './schema';

const sqlite = new Database('sqlite.db');
export const db = drizzle(sqlite, { schema });
```

### 3. Use in Application

```typescript
import { db } from './db/client';
import { users, posts } from './db/schema';
import { eq } from 'drizzle-orm';

// Insert
const newUser = await db.insert(users).values({
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
}).returning();

// Query
const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, '1'));

// Update
await db.update(users)
  .set({ name: 'Jane Doe' })
  .where(eq(users.id, '1'));

// Delete
await db.delete(users).where(eq(users.id, '1'));
```

## Schema Definition

### Column Types (SQLite)

```typescript
import { sqliteTable, text, integer, real, blob } from 'drizzle-orm/sqlite-core';

export const examples = sqliteTable('examples', {
  // Text
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  description: text('description'),

  // Integer
  age: integer('age'),
  count: integer('count').default(0),

  // Boolean (stored as integer 0/1)
  isActive: integer('is_active', { mode: 'boolean' }).default(true),

  // Timestamp (stored as integer unix epoch)
  createdAt: integer('created_at', { mode: 'timestamp' }),
  updatedAt: integer('updated_at', { mode: 'timestamp_ms' }), // milliseconds

  // Real (floating point)
  price: real('price'),

  // Blob (binary data)
  data: blob('data', { mode: 'buffer' }),

  // JSON (stored as text)
  metadata: text('metadata', { mode: 'json' }).$type<{ key: string; value: number }>(),
});
```

### Constraints

```typescript
import { sqliteTable, text, integer, primaryKey, unique index } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(), // Unique constraint
  name: text('name').notNull(), // Not null
  age: integer('age').default(18), // Default value
}, (table) => ({
  // Composite unique constraint
  emailNameUnique: unique().on(table.email, table.name),
  // Index
  emailIdx: index('email_idx').on(table.email),
  // Composite index
  nameAgeIdx: index('name_age_idx').on(table.name, table.age),
}));

// Composite primary key
export const userRoles = sqliteTable('user_roles', {
  userId: text('user_id').notNull(),
  roleId: text('role_id').notNull(),
}, (table) => ({
  pk: primaryKey({ columns: [table.userId, table.roleId] }),
}));
```

### Check Constraints

```typescript
import { sql } from 'drizzle-orm';
import { sqliteTable, text, integer, check } from 'drizzle-orm/sqlite-core';

export const certificates = sqliteTable('certificates', {
  id: text('id').primaryKey(),
  status: text('status').notNull(),
  serialNumber: text('serial_number').notNull(),
}, (table) => ({
  // Check constraint
  statusCheck: check('status_check', sql`${table.status} IN ('active', 'revoked', 'expired')`),
}));
```

### Foreign Keys

```typescript
export const posts = sqliteTable('posts', {
  id: text('id').primaryKey(),
  userId: text('user_id')
    .notNull()
    .references(() => users.id, {
      onDelete: 'cascade',  // Delete posts when user is deleted
      onUpdate: 'cascade',  // Update posts when user id changes
    }),
  title: text('title').notNull(),
});

// Self-referencing foreign key
export const categories = sqliteTable('categories', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  parentId: text('parent_id').references((): AnyPgColumn => categories.id),
});
```

### Default Values

```typescript
import { sql } from 'drizzle-orm';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),

  // SQL default
  createdAt: integer('created_at').default(sql`(unixepoch())`),

  // TypeScript default function
  id: text('id').$defaultFn(() => crypto.randomUUID()),
  createdAt: integer('created_at', { mode: 'timestamp' }).$defaultFn(() => new Date()),
});
```

## Queries

### Select

```typescript
import { eq, and, or, gt, gte, lt, lte, like, inArray } from 'drizzle-orm';

// Select all columns
const allUsers = await db.select().from(users);

// Select specific columns
const names = await db.select({
  id: users.id,
  name: users.name,
}).from(users);

// Where clauses
const user = await db.select().from(users).where(eq(users.id, '1'));

// Multiple conditions
const activeAdults = await db.select().from(users).where(
  and(
    eq(users.isActive, true),
    gte(users.age, 18)
  )
);

// Or conditions
const results = await db.select().from(users).where(
  or(
    eq(users.role, 'admin'),
    eq(users.role, 'moderator')
  )
);

// Like operator
const johns = await db.select().from(users).where(like(users.name, '%John%'));

// In array
const specificUsers = await db.select().from(users).where(
  inArray(users.id, ['1', '2', '3'])
);

// Comparison operators
const adults = await db.select().from(users).where(gte(users.age, 18));
const minors = await db.select().from(users).where(lt(users.age, 18));

// Order by
const sorted = await db.select().from(users).orderBy(users.name);
const descending = await db.select().from(users).orderBy(desc(users.createdAt));

// Limit and offset
const paginated = await db.select().from(users).limit(10).offset(20);

// Get single result
const user = await db.select().from(users).where(eq(users.id, '1')).get();
```

### Joins

```typescript
import { eq } from 'drizzle-orm';

// Inner join
const usersWithPosts = await db
  .select()
  .from(users)
  .innerJoin(posts, eq(posts.userId, users.id));

// Left join
const allUsersWithPosts = await db
  .select()
  .from(users)
  .leftJoin(posts, eq(posts.userId, users.id));

// Select specific columns from joined tables
const results = await db
  .select({
    userId: users.id,
    userName: users.name,
    postTitle: posts.title,
  })
  .from(users)
  .leftJoin(posts, eq(posts.userId, users.id));

// Multiple joins
const data = await db
  .select()
  .from(posts)
  .innerJoin(users, eq(posts.userId, users.id))
  .leftJoin(comments, eq(comments.postId, posts.id));
```

### Aggregations

```typescript
import { count, sum, avg, min, max } from 'drizzle-orm';

// Count
const userCount = await db.select({ count: count() }).from(users);

// Count with condition
const activeCount = await db
  .select({ count: count() })
  .from(users)
  .where(eq(users.isActive, true));

// Group by
const postsByUser = await db
  .select({
    userId: posts.userId,
    postCount: count(),
  })
  .from(posts)
  .groupBy(posts.userId);

// Multiple aggregations
const stats = await db
  .select({
    total: count(),
    avgAge: avg(users.age),
    minAge: min(users.age),
    maxAge: max(users.age),
  })
  .from(users);

// Having clause
const activeUsers = await db
  .select({
    userId: posts.userId,
    postCount: count(),
  })
  .from(posts)
  .groupBy(posts.userId)
  .having(({ postCount }) => gt(postCount, 5));
```

### Subqueries

```typescript
import { sql } from 'drizzle-orm';

// Subquery in WHERE
const sq = db.select({ userId: posts.userId }).from(posts).groupBy(posts.userId);

const activePosters = await db
  .select()
  .from(users)
  .where(inArray(users.id, sq));

// Subquery as column
const usersWithPostCount = await db
  .select({
    id: users.id,
    name: users.name,
    postCount: sql<number>`(
      SELECT COUNT(*)
      FROM ${posts}
      WHERE ${posts.userId} = ${users.id}
    )`,
  })
  .from(users);
```

## Insert

### Single Insert

```typescript
// Insert one
await db.insert(users).values({
  id: '1',
  name: 'John',
  email: 'john@example.com',
});

// Insert with returning
const newUser = await db.insert(users)
  .values({
    id: '2',
    name: 'Jane',
    email: 'jane@example.com',
  })
  .returning();

// Return specific columns
const user = await db.insert(users)
  .values({ id: '3', name: 'Bob', email: 'bob@example.com' })
  .returning({ id: users.id, name: users.name });
```

### Bulk Insert

```typescript
// Insert multiple
await db.insert(users).values([
  { id: '1', name: 'John', email: 'john@example.com' },
  { id: '2', name: 'Jane', email: 'jane@example.com' },
  { id: '3', name: 'Bob', email: 'bob@example.com' },
]);

// Bulk insert with returning
const newUsers = await db.insert(users)
  .values([
    { id: '4', name: 'Alice', email: 'alice@example.com' },
    { id: '5', name: 'Charlie', email: 'charlie@example.com' },
  ])
  .returning();
```

### Upsert (Insert or Update)

```typescript
// SQLite 3.24+ (ON CONFLICT)
await db.insert(users)
  .values({ id: '1', name: 'John', email: 'john@example.com' })
  .onConflictDoUpdate({
    target: users.id,
    set: { name: 'John Updated', email: 'john.updated@example.com' },
  });

// Do nothing on conflict
await db.insert(users)
  .values({ id: '1', name: 'John', email: 'john@example.com' })
  .onConflictDoNothing();

// Update specific columns
await db.insert(users)
  .values({ id: '1', name: 'John', email: 'john@example.com' })
  .onConflictDoUpdate({
    target: users.id,
    set: { updatedAt: sql`CURRENT_TIMESTAMP` },
  });
```

## Update

```typescript
import { eq } from 'drizzle-orm';

// Update single row
await db.update(users)
  .set({ name: 'John Updated' })
  .where(eq(users.id, '1'));

// Update multiple columns
await db.update(users)
  .set({
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
  })
  .where(eq(users.id, '2'));

// Update with returning
const updated = await db.update(users)
  .set({ name: 'Bob Updated' })
  .where(eq(users.id, '3'))
  .returning();

// Update with SQL expression
await db.update(users)
  .set({ age: sql`${users.age} + 1` })
  .where(eq(users.id, '1'));

// Conditional update
await db.update(users)
  .set({ status: 'active' })
  .where(and(
    eq(users.verified, true),
    gte(users.createdAt, new Date('2024-01-01'))
  ));
```

## Delete

```typescript
// Delete single row
await db.delete(users).where(eq(users.id, '1'));

// Delete multiple rows
await db.delete(users).where(inArray(users.id, ['1', '2', '3']));

// Delete with condition
await db.delete(users).where(lt(users.createdAt, new Date('2023-01-01')));

// Delete with returning
const deleted = await db.delete(users)
  .where(eq(users.id, '1'))
  .returning();

// Delete all (be careful!)
await db.delete(users);
```

## Transactions

```typescript
// Simple transaction
await db.transaction(async (tx) => {
  await tx.insert(users).values({ id: '1', name: 'John', email: 'john@example.com' });
  await tx.insert(posts).values({ id: '1', title: 'First Post', userId: '1' });
});

// Transaction with rollback
try {
  await db.transaction(async (tx) => {
    await tx.insert(users).values({ id: '1', name: 'John', email: 'john@example.com' });

    // This will cause transaction to rollback
    throw new Error('Rollback!');

    await tx.insert(posts).values({ id: '1', title: 'Post', userId: '1' });
  });
} catch (error) {
  console.error('Transaction failed:', error);
}

// Nested transactions
await db.transaction(async (tx1) => {
  await tx1.insert(users).values({ id: '1', name: 'John', email: 'john@example.com' });

  await tx1.transaction(async (tx2) => {
    await tx2.insert(posts).values({ id: '1', title: 'Post', userId: '1' });
  });
});
```

## Relations

### Define Relations

```typescript
// src/db/schema.ts
import { relations } from 'drizzle-orm';
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
});

export const posts = sqliteTable('posts', {
  id: text('id').primaryKey(),
  title: text('title').notNull(),
  userId: text('user_id').notNull().references(() => users.id),
});

export const comments = sqliteTable('comments', {
  id: text('id').primaryKey(),
  content: text('content').notNull(),
  postId: text('post_id').notNull().references(() => posts.id),
  userId: text('user_id').notNull().references(() => users.id),
});

// Define relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.userId],
    references: [users.id],
  }),
  comments: many(comments),
}));

export const commentsRelations = relations(comments, ({ one }) => ({
  post: one(posts, {
    fields: [comments.postId],
    references: [posts.id],
  }),
  author: one(users, {
    fields: [comments.userId],
    references: [users.id],
  }),
}));
```

### Query with Relations

```typescript
// Query with relations
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

// Nested relations
const usersWithPostsAndComments = await db.query.users.findMany({
  with: {
    posts: {
      with: {
        comments: true,
      },
    },
  },
});

// Filter relations
const usersWithRecentPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: (posts, { gte }) => gte(posts.createdAt, new Date('2024-01-01')),
    },
  },
});

// Select specific columns
const data = await db.query.users.findMany({
  columns: {
    id: true,
    name: true,
  },
  with: {
    posts: {
      columns: {
        id: true,
        title: true,
      },
    },
  },
});
```

## Migrations

### Configuration

```typescript
// drizzle.config.ts
import type { Config } from 'drizzle-kit';

export default {
  schema: './src/db/schema.ts',
  out: './drizzle/migrations',
  driver: 'better-sqlite',
  dbCredentials: {
    url: './sqlite.db',
  },
} satisfies Config;
```

### Generate Migrations

```bash
# Generate migration from schema changes
npx drizzle-kit generate:sqlite

# Custom migration name
npx drizzle-kit generate:sqlite --name add_users_table

# Generate with custom config
npx drizzle-kit generate:sqlite --config drizzle.config.ts
```

### Run Migrations

```typescript
// src/db/migrate.ts
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { migrate } from 'drizzle-orm/better-sqlite3/migrator';
import Database from 'better-sqlite3';

const sqlite = new Database('sqlite.db');
const db = drizzle(sqlite);

// Run migrations
await migrate(db, { migrationsFolder: './drizzle/migrations' });

console.log('Migrations complete!');
sqlite.close();
```

### Migration Files

```sql
-- drizzle/migrations/0001_add_users.sql
CREATE TABLE `users` (
  `id` text PRIMARY KEY NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL UNIQUE,
  `created_at` integer NOT NULL
);

CREATE INDEX `email_idx` ON `users` (`email`);
```

## Drizzle Studio

```bash
# Start Drizzle Studio
npx drizzle-kit studio

# Custom port
npx drizzle-kit studio --port 3333

# With custom config
npx drizzle-kit studio --config drizzle.config.ts
```

Access at: http://localhost:4983

## TypeScript Integration

### Infer Types

```typescript
import { InferSelectModel, InferInsertModel } from 'drizzle-orm';
import { users, posts } from './schema';

// Infer select model (what you get from queries)
export type User = InferSelectModel<typeof users>;
export type Post = InferSelectModel<typeof posts>;

// Infer insert model (what you need to insert)
export type InsertUser = InferInsertModel<typeof users>;
export type InsertPost = InferInsertModel<typeof posts>;

// Usage
function createUser(user: InsertUser): Promise<User> {
  return db.insert(users).values(user).returning().get();
}
```

### Typed Queries

```typescript
// Type-safe query builder
const query = db
  .select({
    id: users.id,
    name: users.name,
    postCount: count(posts.id),
  })
  .from(users)
  .leftJoin(posts, eq(posts.userId, users.id))
  .groupBy(users.id);

// Infer result type
type QueryResult = Awaited<ReturnType<typeof query.execute>>;
```

## Best Practices

1. **Use Transactions**: Wrap multiple operations in transactions
2. **Define Relations**: Use relations for easier queries
3. **Type Safety**: Leverage TypeScript type inference
4. **Migrations**: Use migration system, don't modify schema directly in production
5. **Indexes**: Index frequently queried columns
6. **Prepared Statements**: Drizzle automatically uses prepared statements
7. **Connection Management**: Reuse database connection
8. **Studio**: Use Drizzle Studio for visual database exploration
9. **Error Handling**: Handle constraint violations
10. **Performance**: Use `get()` for single results instead of `all()[0]`

## Common Patterns

### Repository Pattern

```typescript
export class UserRepository {
  constructor(private db: ReturnType<typeof drizzle>) {}

  async findById(id: string): Promise<User | undefined> {
    return this.db.select().from(users).where(eq(users.id, id)).get();
  }

  async findAll(): Promise<User[]> {
    return this.db.select().from(users);
  }

  async create(data: InsertUser): Promise<User> {
    return this.db.insert(users).values(data).returning().get();
  }

  async update(id: string, data: Partial<InsertUser>): Promise<User | undefined> {
    return this.db.update(users).set(data).where(eq(users.id, id)).returning().get();
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.db.delete(users).where(eq(users.id, id)).returning();
    return result.length > 0;
  }
}
```

## Resources

- Documentation: https://orm.drizzle.team/docs/overview
- GitHub: https://github.com/drizzle-team/drizzle-orm
- Examples: https://github.com/drizzle-team/drizzle-orm/tree/main/examples
- Drizzle Studio: https://orm.drizzle.team/drizzle-studio/overview
