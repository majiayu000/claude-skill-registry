---
name: kysely
description: Implements Kysely type-safe SQL query builder with full TypeScript inference, migrations, and multi-database support. Use when building type-safe SQL queries, needing a lightweight ORM alternative, or wanting SQL control with TypeScript safety.
---

# Kysely

Kysely is a type-safe TypeScript SQL query builder. It provides full autocompletion and type inference while compiling to plain SQL.

## Quick Start

```bash
npm install kysely
npm install pg  # PostgreSQL
# or: mysql2, better-sqlite3
```

## Database Type Definition

Define your schema as TypeScript interfaces:

```typescript
// src/db/types.ts
import {
  ColumnType,
  Generated,
  Insertable,
  Selectable,
  Updateable
} from 'kysely'

// Table definitions
interface UserTable {
  id: Generated<number>
  email: string
  name: string | null
  created_at: ColumnType<Date, string | undefined, never>
}

interface PostTable {
  id: Generated<number>
  title: string
  content: string | null
  author_id: number
  published: boolean
  created_at: ColumnType<Date, string | undefined, never>
}

// Database interface
export interface Database {
  users: UserTable
  posts: PostTable
}

// Helper types for each table
export type User = Selectable<UserTable>
export type NewUser = Insertable<UserTable>
export type UserUpdate = Updateable<UserTable>

export type Post = Selectable<PostTable>
export type NewPost = Insertable<PostTable>
export type PostUpdate = Updateable<PostTable>
```

## Client Setup

### PostgreSQL

```typescript
// src/db/index.ts
import { Kysely, PostgresDialect } from 'kysely'
import { Pool } from 'pg'
import { Database } from './types'

const dialect = new PostgresDialect({
  pool: new Pool({
    connectionString: process.env.DATABASE_URL,
    max: 10
  })
})

export const db = new Kysely<Database>({ dialect })
```

### MySQL

```typescript
import { Kysely, MysqlDialect } from 'kysely'
import { createPool } from 'mysql2'

const dialect = new MysqlDialect({
  pool: createPool({
    uri: process.env.DATABASE_URL
  })
})

export const db = new Kysely<Database>({ dialect })
```

### SQLite

```typescript
import { Kysely, SqliteDialect } from 'kysely'
import Database from 'better-sqlite3'

const dialect = new SqliteDialect({
  database: new Database('db.sqlite')
})

export const db = new Kysely<Database>({ dialect })
```

## CRUD Operations

### Select

```typescript
// Select all columns
const users = await db
  .selectFrom('users')
  .selectAll()
  .execute()

// Select specific columns
const emails = await db
  .selectFrom('users')
  .select(['id', 'email'])
  .execute()

// With alias
const result = await db
  .selectFrom('users')
  .select([
    'id',
    'email',
    'name as full_name'
  ])
  .execute()

// Single row
const user = await db
  .selectFrom('users')
  .selectAll()
  .where('id', '=', userId)
  .executeTakeFirst()

// Single row or throw
const user = await db
  .selectFrom('users')
  .selectAll()
  .where('id', '=', userId)
  .executeTakeFirstOrThrow()
```

### Where Clauses

```typescript
// Equality
.where('email', '=', 'user@example.com')

// Comparison
.where('age', '>', 18)
.where('age', '>=', 21)

// IN
.where('status', 'in', ['active', 'pending'])

// LIKE
.where('name', 'like', '%john%')

// IS NULL
.where('deleted_at', 'is', null)

// IS NOT NULL
.where('verified_at', 'is not', null)

// Multiple conditions (AND)
.where('status', '=', 'active')
.where('role', '=', 'admin')

// OR conditions
.where(({ or, eb }) =>
  or([
    eb('status', '=', 'active'),
    eb('role', '=', 'admin')
  ])
)

// Complex conditions
.where(({ and, or, eb }) =>
  and([
    eb('status', '=', 'active'),
    or([
      eb('role', '=', 'admin'),
      eb('role', '=', 'moderator')
    ])
  ])
)
```

### Insert

```typescript
// Insert single row
const result = await db
  .insertInto('users')
  .values({
    email: 'user@example.com',
    name: 'John Doe'
  })
  .executeTakeFirst()

// Get inserted ID
const { insertId } = result

// Insert and return
const user = await db
  .insertInto('users')
  .values({
    email: 'user@example.com',
    name: 'John Doe'
  })
  .returningAll()
  .executeTakeFirstOrThrow()

// Insert multiple
await db
  .insertInto('users')
  .values([
    { email: 'alice@example.com', name: 'Alice' },
    { email: 'bob@example.com', name: 'Bob' }
  ])
  .execute()

// Insert from select
await db
  .insertInto('archived_users')
  .columns(['email', 'name'])
  .expression(
    db.selectFrom('users')
      .select(['email', 'name'])
      .where('status', '=', 'inactive')
  )
  .execute()
```

### Update

```typescript
// Update by condition
const result = await db
  .updateTable('users')
  .set({ name: 'Updated Name' })
  .where('id', '=', userId)
  .executeTakeFirst()

console.log('Rows updated:', result.numUpdatedRows)

// Update and return
const updatedUser = await db
  .updateTable('users')
  .set({ name: 'Updated Name' })
  .where('id', '=', userId)
  .returningAll()
  .executeTakeFirst()

// Update with expression
await db
  .updateTable('users')
  .set(eb => ({
    login_count: eb('login_count', '+', 1),
    last_login: eb.fn('now')
  }))
  .where('id', '=', userId)
  .execute()
```

### Delete

```typescript
// Delete by condition
const result = await db
  .deleteFrom('users')
  .where('id', '=', userId)
  .executeTakeFirst()

console.log('Rows deleted:', result.numDeletedRows)

// Delete and return
const deletedUser = await db
  .deleteFrom('users')
  .where('id', '=', userId)
  .returningAll()
  .executeTakeFirst()

// Delete with subquery
await db
  .deleteFrom('posts')
  .where('author_id', 'in',
    db.selectFrom('users')
      .select('id')
      .where('status', '=', 'deleted')
  )
  .execute()
```

## Joins

```typescript
// Inner join
const postsWithAuthors = await db
  .selectFrom('posts')
  .innerJoin('users', 'users.id', 'posts.author_id')
  .select([
    'posts.id',
    'posts.title',
    'users.name as author_name'
  ])
  .execute()

// Left join
const usersWithPosts = await db
  .selectFrom('users')
  .leftJoin('posts', 'posts.author_id', 'users.id')
  .select([
    'users.id',
    'users.name',
    'posts.title'
  ])
  .execute()

// Multiple joins
const result = await db
  .selectFrom('posts')
  .innerJoin('users', 'users.id', 'posts.author_id')
  .leftJoin('comments', 'comments.post_id', 'posts.id')
  .select([
    'posts.title',
    'users.name as author',
    db.fn.count('comments.id').as('comment_count')
  ])
  .groupBy(['posts.id', 'users.name'])
  .execute()
```

## Aggregations

```typescript
// Count
const { count } = await db
  .selectFrom('users')
  .select(db.fn.countAll().as('count'))
  .executeTakeFirstOrThrow()

// Sum, Avg, Min, Max
const stats = await db
  .selectFrom('orders')
  .select([
    db.fn.sum('total').as('total_revenue'),
    db.fn.avg('total').as('avg_order'),
    db.fn.min('total').as('min_order'),
    db.fn.max('total').as('max_order')
  ])
  .executeTakeFirstOrThrow()

// Group by
const salesByCategory = await db
  .selectFrom('products')
  .innerJoin('orders', 'orders.product_id', 'products.id')
  .select([
    'products.category',
    db.fn.sum('orders.quantity').as('total_sold')
  ])
  .groupBy('products.category')
  .having(db.fn.sum('orders.quantity'), '>', 100)
  .execute()
```

## Ordering and Pagination

```typescript
// Order by
const users = await db
  .selectFrom('users')
  .selectAll()
  .orderBy('created_at', 'desc')
  .orderBy('name', 'asc')
  .execute()

// Limit and offset
const page = await db
  .selectFrom('users')
  .selectAll()
  .orderBy('id')
  .limit(10)
  .offset(20)
  .execute()

// Cursor-based pagination
const nextPage = await db
  .selectFrom('users')
  .selectAll()
  .where('id', '>', lastId)
  .orderBy('id')
  .limit(10)
  .execute()
```

## Transactions

```typescript
// Basic transaction
await db.transaction().execute(async (trx) => {
  const user = await trx
    .insertInto('users')
    .values({ email: 'user@example.com', name: 'John' })
    .returningAll()
    .executeTakeFirstOrThrow()

  await trx
    .insertInto('posts')
    .values({
      title: 'First Post',
      author_id: user.id,
      published: false
    })
    .execute()
})

// Transaction with return value
const result = await db.transaction().execute(async (trx) => {
  // ... operations
  return { success: true }
})
```

## Raw SQL

```typescript
import { sql } from 'kysely'

// Raw expression
const users = await db
  .selectFrom('users')
  .selectAll()
  .where(sql`LOWER(email)`, '=', email.toLowerCase())
  .execute()

// Raw in select
const result = await db
  .selectFrom('users')
  .select([
    'id',
    sql<number>`EXTRACT(YEAR FROM created_at)`.as('year')
  ])
  .execute()

// Full raw query
const users = await sql<User>`
  SELECT * FROM users
  WHERE email = ${email}
`.execute(db)
```

## Migrations

### Setup

```bash
npm install -D kysely-ctl
```

```typescript
// kysely.config.ts
import { defineConfig } from 'kysely-ctl'
import { db } from './src/db'

export default defineConfig({
  kysely: db,
  migrations: {
    migrationFolder: 'migrations'
  }
})
```

### Create Migration

```bash
npx kysely migrate:make add_users_table
```

```typescript
// migrations/001_add_users_table.ts
import { Kysely, sql } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('users')
    .addColumn('id', 'serial', col => col.primaryKey())
    .addColumn('email', 'varchar(255)', col => col.notNull().unique())
    .addColumn('name', 'varchar(255)')
    .addColumn('created_at', 'timestamp', col =>
      col.defaultTo(sql`now()`).notNull()
    )
    .execute()
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('users').execute()
}
```

### Run Migrations

```bash
npx kysely migrate:latest
npx kysely migrate:down
npx kysely migrate:rollback --all
```

## Type Generation

Generate types from existing database:

```bash
npm install -D kysely-codegen
npx kysely-codegen --out-file src/db/types.ts
```

## Plugins

### Camel Case

```typescript
import { Kysely, CamelCasePlugin } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  plugins: [new CamelCasePlugin()]
})

// Now use camelCase in code
interface UserTable {
  id: Generated<number>
  createdAt: Date  // maps to created_at in DB
}
```

### Query Logging

```typescript
import { Kysely, LogEvent } from 'kysely'

const db = new Kysely<Database>({
  dialect,
  log(event: LogEvent) {
    if (event.level === 'query') {
      console.log(event.query.sql)
      console.log(event.query.parameters)
    }
  }
})
```

## Best Practices

1. **One Kysely instance per database** - Reuse connections
2. **Enable strict TypeScript** - Required for full type safety
3. **Use Selectable/Insertable/Updateable** - Proper types for operations
4. **Generate types from DB** - Keep types in sync
5. **Use transactions for related operations** - Data consistency
6. **Call db.destroy() on shutdown** - Clean up connections

```typescript
// Cleanup on shutdown
process.on('SIGINT', async () => {
  await db.destroy()
  process.exit(0)
})
```

## References

- [Advanced Queries](references/advanced-queries.md)
- [Schema Migrations](references/migrations.md)
