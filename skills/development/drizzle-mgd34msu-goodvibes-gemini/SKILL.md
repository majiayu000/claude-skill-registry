---
name: drizzle
description: Builds type-safe database applications with Drizzle ORM including schema definition, queries, relations, and migrations. Use when working with databases in TypeScript, defining schemas, writing type-safe queries, or managing migrations.
---

# Drizzle ORM

Lightweight, type-safe TypeScript ORM with zero dependencies and SQL-first approach.

## Quick Start

**Install:**
```bash
# PostgreSQL
npm install drizzle-orm postgres
npm install -D drizzle-kit

# MySQL
npm install drizzle-orm mysql2
npm install -D drizzle-kit

# SQLite
npm install drizzle-orm better-sqlite3
npm install -D drizzle-kit @types/better-sqlite3
```

**Project structure:**
```
src/
  db/
    index.ts        # Database connection
    schema.ts       # Table definitions
    relations.ts    # Relation definitions
drizzle.config.ts   # Drizzle Kit config
```

## Database Connection

### PostgreSQL

```typescript
// db/index.ts
import { drizzle } from 'drizzle-orm/postgres-js';
import postgres from 'postgres';
import * as schema from './schema';

const connectionString = process.env.DATABASE_URL!;
const client = postgres(connectionString);

export const db = drizzle(client, { schema });
```

### MySQL

```typescript
// db/index.ts
import { drizzle } from 'drizzle-orm/mysql2';
import mysql from 'mysql2/promise';
import * as schema from './schema';

const connection = await mysql.createConnection({
  host: 'localhost',
  user: 'root',
  database: 'mydb',
});

export const db = drizzle(connection, { schema });
```

### SQLite

```typescript
// db/index.ts
import { drizzle } from 'drizzle-orm/better-sqlite3';
import Database from 'better-sqlite3';
import * as schema from './schema';

const sqlite = new Database('sqlite.db');
export const db = drizzle(sqlite, { schema });
```

### Turso (Edge SQLite)

```typescript
import { drizzle } from 'drizzle-orm/libsql';
import { createClient } from '@libsql/client';
import * as schema from './schema';

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN,
});

export const db = drizzle(client, { schema });
```

## Schema Definition

### PostgreSQL Tables

```typescript
// db/schema.ts
import {
  pgTable,
  serial,
  varchar,
  text,
  integer,
  boolean,
  timestamp,
  uuid,
  jsonb,
} from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }),
  bio: text('bio'),
  age: integer('age'),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

export const posts = pgTable('posts', {
  id: uuid('id').primaryKey().defaultRandom(),
  title: varchar('title', { length: 255 }).notNull(),
  content: text('content'),
  published: boolean('published').default(false),
  authorId: integer('author_id')
    .notNull()
    .references(() => users.id),
  metadata: jsonb('metadata'),
  createdAt: timestamp('created_at').defaultNow(),
});

export const comments = pgTable('comments', {
  id: serial('id').primaryKey(),
  content: text('content').notNull(),
  postId: uuid('post_id')
    .notNull()
    .references(() => posts.id, { onDelete: 'cascade' }),
  authorId: integer('author_id')
    .notNull()
    .references(() => users.id),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### MySQL Tables

```typescript
import {
  mysqlTable,
  serial,
  varchar,
  text,
  int,
  boolean,
  timestamp,
  json,
} from 'drizzle-orm/mysql-core';

export const users = mysqlTable('users', {
  id: serial('id').primaryKey(),
  email: varchar('email', { length: 255 }).notNull().unique(),
  name: varchar('name', { length: 100 }),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### SQLite Tables

```typescript
import {
  sqliteTable,
  integer,
  text,
} from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .$defaultFn(() => new Date()),
});
```

### Type Inference

```typescript
// Infer types from schema
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;

export type Post = typeof posts.$inferSelect;
export type NewPost = typeof posts.$inferInsert;
```

## Relations

```typescript
// db/relations.ts
import { relations } from 'drizzle-orm';
import { users, posts, comments } from './schema';

export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
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
    fields: [comments.authorId],
    references: [users.id],
  }),
}));
```

### Many-to-Many

```typescript
// Schema
export const usersToGroups = pgTable('users_to_groups', {
  userId: integer('user_id')
    .notNull()
    .references(() => users.id),
  groupId: integer('group_id')
    .notNull()
    .references(() => groups.id),
}, (t) => ({
  pk: primaryKey({ columns: [t.userId, t.groupId] }),
}));

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  usersToGroups: many(usersToGroups),
}));

export const groupsRelations = relations(groups, ({ many }) => ({
  usersToGroups: many(usersToGroups),
}));

export const usersToGroupsRelations = relations(usersToGroups, ({ one }) => ({
  user: one(users, {
    fields: [usersToGroups.userId],
    references: [users.id],
  }),
  group: one(groups, {
    fields: [usersToGroups.groupId],
    references: [groups.id],
  }),
}));
```

## Queries

### Select

```typescript
import { eq, lt, gte, ne, and, or, like, ilike, between, inArray } from 'drizzle-orm';
import { db } from './db';
import { users, posts } from './db/schema';

// Select all
const allUsers = await db.select().from(users);

// Select specific columns
const userNames = await db.select({
  id: users.id,
  name: users.name,
}).from(users);

// Where clause
const activeUsers = await db.select()
  .from(users)
  .where(eq(users.isActive, true));

// Multiple conditions
const filteredUsers = await db.select()
  .from(users)
  .where(
    and(
      eq(users.isActive, true),
      gte(users.age, 18),
    )
  );

// OR conditions
const results = await db.select()
  .from(users)
  .where(
    or(
      eq(users.name, 'John'),
      eq(users.name, 'Jane'),
    )
  );

// Pattern matching
const matching = await db.select()
  .from(users)
  .where(like(users.email, '%@gmail.com'));

// Case-insensitive (PostgreSQL)
const matchingCI = await db.select()
  .from(users)
  .where(ilike(users.name, '%john%'));

// Range queries
const inRange = await db.select()
  .from(users)
  .where(between(users.age, 18, 65));

// IN operator
const specificUsers = await db.select()
  .from(users)
  .where(inArray(users.id, [1, 2, 3]));
```

### Joins

```typescript
import { eq } from 'drizzle-orm';

// Inner join
const postsWithAuthors = await db.select({
  post: posts,
  author: users,
})
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id));

// Left join
const usersWithPosts = await db.select({
  user: users,
  post: posts,
})
  .from(users)
  .leftJoin(posts, eq(users.id, posts.authorId));

// Multiple joins
const fullData = await db.select()
  .from(posts)
  .innerJoin(users, eq(posts.authorId, users.id))
  .leftJoin(comments, eq(posts.id, comments.postId));
```

### Ordering and Pagination

```typescript
import { asc, desc } from 'drizzle-orm';

// Order by
const orderedUsers = await db.select()
  .from(users)
  .orderBy(desc(users.createdAt));

// Multiple order columns
const sorted = await db.select()
  .from(users)
  .orderBy(asc(users.name), desc(users.createdAt));

// Pagination
const page = await db.select()
  .from(users)
  .limit(10)
  .offset(20);
```

### Aggregations

```typescript
import { count, sum, avg, min, max } from 'drizzle-orm';

// Count
const userCount = await db.select({
  count: count(),
}).from(users);

// Group by
const postsByAuthor = await db.select({
  authorId: posts.authorId,
  postCount: count(posts.id),
})
  .from(posts)
  .groupBy(posts.authorId);

// With having
const activeAuthors = await db.select({
  authorId: posts.authorId,
  postCount: count(posts.id),
})
  .from(posts)
  .groupBy(posts.authorId)
  .having(({ postCount }) => gte(postCount, 5));
```

### Relational Queries

```typescript
// Find many with relations
const usersWithPosts = await db.query.users.findMany({
  with: {
    posts: true,
  },
});

// Nested relations
const postsWithDetails = await db.query.posts.findMany({
  with: {
    author: true,
    comments: {
      with: {
        author: true,
      },
    },
  },
});

// Find first
const user = await db.query.users.findFirst({
  where: (users, { eq }) => eq(users.id, 1),
  with: {
    posts: true,
  },
});

// Select specific columns
const partialPosts = await db.query.posts.findMany({
  columns: {
    id: true,
    title: true,
  },
  with: {
    author: {
      columns: {
        name: true,
      },
    },
  },
});

// Filter nested relations
const recentPosts = await db.query.users.findMany({
  with: {
    posts: {
      where: (posts, { eq }) => eq(posts.published, true),
      orderBy: (posts, { desc }) => [desc(posts.createdAt)],
      limit: 5,
    },
  },
});
```

## Insert

```typescript
// Single insert
await db.insert(users).values({
  email: 'john@example.com',
  name: 'John Doe',
});

// Insert with returning (PostgreSQL, SQLite)
const [newUser] = await db.insert(users)
  .values({
    email: 'jane@example.com',
    name: 'Jane Doe',
  })
  .returning();

// Multiple insert
await db.insert(users).values([
  { email: 'user1@example.com', name: 'User 1' },
  { email: 'user2@example.com', name: 'User 2' },
]);

// Upsert (on conflict)
await db.insert(users)
  .values({
    email: 'john@example.com',
    name: 'John Updated',
  })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'John Updated' },
  });

// On conflict do nothing
await db.insert(users)
  .values({ email: 'john@example.com', name: 'John' })
  .onConflictDoNothing({ target: users.email });
```

## Update

```typescript
// Update with where
await db.update(users)
  .set({ name: 'John Smith' })
  .where(eq(users.id, 1));

// Update with returning
const [updated] = await db.update(users)
  .set({ isActive: false })
  .where(eq(users.id, 1))
  .returning();

// Increment value
await db.update(posts)
  .set({ viewCount: sql`${posts.viewCount} + 1` })
  .where(eq(posts.id, 1));
```

## Delete

```typescript
// Delete with where
await db.delete(users).where(eq(users.id, 1));

// Delete with returning
const [deleted] = await db.delete(users)
  .where(eq(users.id, 1))
  .returning();

// Delete all (be careful!)
await db.delete(users);
```

## Transactions

```typescript
// Basic transaction
await db.transaction(async (tx) => {
  const [user] = await tx.insert(users)
    .values({ email: 'new@example.com', name: 'New User' })
    .returning();

  await tx.insert(posts).values({
    title: 'First Post',
    authorId: user.id,
  });
});

// With rollback
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'test@example.com' });

  // Rollback on condition
  if (someCondition) {
    tx.rollback();
  }

  await tx.insert(posts).values({ title: 'Post', authorId: 1 });
});

// Nested transactions (savepoints)
await db.transaction(async (tx) => {
  await tx.insert(users).values({ email: 'outer@example.com' });

  await tx.transaction(async (tx2) => {
    await tx2.insert(posts).values({ title: 'Nested', authorId: 1 });
  });
});
```

## Migrations

### Configuration

```typescript
// drizzle.config.ts
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

### Commands

```bash
# Generate migration
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate

# Push schema (dev, no migration files)
npx drizzle-kit push

# Pull existing database schema
npx drizzle-kit pull

# Open Drizzle Studio
npx drizzle-kit studio
```

## Raw SQL

```typescript
import { sql } from 'drizzle-orm';

// Raw query
const result = await db.execute(sql`SELECT * FROM users WHERE id = ${userId}`);

// In select
const users = await db.select({
  id: users.id,
  fullName: sql<string>`${users.firstName} || ' ' || ${users.lastName}`,
}).from(users);

// Typed raw
const count = await db.execute<{ count: number }>(
  sql`SELECT COUNT(*) as count FROM users`
);
```

## Prepared Statements

```typescript
import { placeholder } from 'drizzle-orm';

// Prepare statement
const prepared = db.select()
  .from(users)
  .where(eq(users.id, placeholder('id')))
  .prepare('get_user');

// Execute with values
const user = await prepared.execute({ id: 1 });

// Relational prepared
const preparedWithPosts = db.query.users.findFirst({
  where: (users, { eq }) => eq(users.id, placeholder('id')),
  with: { posts: true },
}).prepare('user_with_posts');

const result = await preparedWithPosts.execute({ id: 1 });
```

## Best Practices

1. **Export types from schema** - Use $inferSelect and $inferInsert
2. **Use relations for nested data** - Single query, no N+1
3. **Prepare frequent queries** - Better performance
4. **Use transactions for multi-step ops** - Ensure consistency
5. **Leverage push for development** - Faster iteration

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing schema in drizzle() | Pass { schema } to enable query API |
| Not exporting relations | Export from schema file |
| Using select() for relations | Use db.query for relational queries |
| Raw SQL without typing | Add type parameter to sql`` |
| Forgetting returning() | Add .returning() for inserted data |

## Reference Files

- [references/queries.md](references/queries.md) - Advanced query patterns
- [references/migrations.md](references/migrations.md) - Migration workflows
- [references/relations.md](references/relations.md) - Complex relations
