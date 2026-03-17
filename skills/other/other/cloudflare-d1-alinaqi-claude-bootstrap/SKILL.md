---
name: cloudflare-d1
description: Cloudflare D1 SQLite database with Workers, Drizzle ORM, migrations
---

# Cloudflare D1 Skill

*Load with: base.md + typescript.md*

Cloudflare D1 is a serverless SQLite database designed for Cloudflare Workers with global distribution and zero cold starts.

**Sources:** [D1 Docs](https://developers.cloudflare.com/d1/) | [Drizzle + D1](https://orm.drizzle.team/docs/connect-cloudflare-d1) | [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)

---

## Core Principle

**SQLite at the edge, migrations in version control, Drizzle for type safety.**

D1 brings SQLite's simplicity to serverless. Design for horizontal scale (multiple small databases) rather than vertical (one large database). Use Drizzle ORM for type-safe queries and migrations.

---

## D1 Stack

| Component | Purpose |
|-----------|---------|
| **D1** | Serverless SQLite database |
| **Workers** | Edge runtime for your application |
| **Wrangler** | CLI for development and deployment |
| **Drizzle ORM** | Type-safe ORM with migrations |
| **Drizzle Kit** | Migration tooling |
| **Hono** | Lightweight web framework (optional) |

---

## Project Setup

### Create Worker Project
```bash
# Create new project
npm create cloudflare@latest my-app -- --template "worker-typescript"
cd my-app

# Install dependencies
npm install drizzle-orm
npm install -D drizzle-kit
```

### Create D1 Database
```bash
# Create database (creates both local and remote)
npx wrangler d1 create my-database

# Output:
# [[d1_databases]]
# binding = "DB"
# database_name = "my-database"
# database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Configure wrangler.toml
```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
migrations_dir = "drizzle"
migrations_table = "drizzle_migrations"
```

### Generate TypeScript Types
```bash
# Generate env types from wrangler.toml
npx wrangler types

# Creates worker-configuration.d.ts:
# interface Env {
#   DB: D1Database;
# }
```

---

## Drizzle ORM Setup

### Schema Definition
```typescript
// src/db/schema.ts
import { sqliteTable, text, integer, real, blob } from 'drizzle-orm/sqlite-core';
import { sql } from 'drizzle-orm';

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  role: text('role', { enum: ['user', 'admin'] }).default('user'),
  createdAt: text('created_at').default(sql`CURRENT_TIMESTAMP`),
  updatedAt: text('updated_at').default(sql`CURRENT_TIMESTAMP`)
});

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  title: text('title').notNull(),
  content: text('content'),
  authorId: integer('author_id').references(() => users.id),
  published: integer('published', { mode: 'boolean' }).default(false),
  viewCount: integer('view_count').default(0),
  createdAt: text('created_at').default(sql`CURRENT_TIMESTAMP`)
});

export const tags = sqliteTable('tags', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull().unique()
});

export const postTags = sqliteTable('post_tags', {
  postId: integer('post_id').references(() => posts.id),
  tagId: integer('tag_id').references(() => tags.id)
});

// Type exports
export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Post = typeof posts.$inferSelect;
export type NewPost = typeof posts.$inferInsert;
```

### Drizzle Config
```typescript
// drizzle.config.ts
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
  driver: 'd1-http',
  dbCredentials: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
    databaseId: process.env.CLOUDFLARE_DATABASE_ID!,
    token: process.env.CLOUDFLARE_D1_TOKEN!
  }
});
```

### Database Client
```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/d1';
import * as schema from './schema';

export function createDb(d1: D1Database) {
  return drizzle(d1, { schema });
}

export type Database = ReturnType<typeof createDb>;
export * from './schema';
```

---

## Migration Workflow

### Generate Migration
```bash
# Generate migration from schema changes
npx drizzle-kit generate

# Output: drizzle/0000_initial.sql
```

### Apply Migrations Locally
```bash
# Apply to local D1
npx wrangler d1 migrations apply my-database --local

# Or via Drizzle
npx drizzle-kit migrate
```

### Apply Migrations to Production
```bash
# Apply to remote D1
npx wrangler d1 migrations apply my-database --remote

# Preview first (dry run)
npx wrangler d1 migrations apply my-database --remote --dry-run
```

### Migration File Example
```sql
-- drizzle/0000_initial.sql
CREATE TABLE `users` (
  `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  `email` text NOT NULL,
  `name` text NOT NULL,
  `role` text DEFAULT 'user',
  `created_at` text DEFAULT CURRENT_TIMESTAMP,
  `updated_at` text DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX `users_email_unique` ON `users` (`email`);

CREATE TABLE `posts` (
  `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  `title` text NOT NULL,
  `content` text,
  `author_id` integer REFERENCES `users`(`id`),
  `published` integer DEFAULT false,
  `view_count` integer DEFAULT 0,
  `created_at` text DEFAULT CURRENT_TIMESTAMP
);
```

---

## Worker Implementation

### Basic Worker with Hono
```typescript
// src/index.ts
import { Hono } from 'hono';
import { createDb, users, posts } from './db';
import { eq, desc } from 'drizzle-orm';

type Bindings = {
  DB: D1Database;
};

const app = new Hono<{ Bindings: Bindings }>();

// Middleware to inject db
app.use('*', async (c, next) => {
  c.set('db', createDb(c.env.DB));
  await next();
});

// List users
app.get('/users', async (c) => {
  const db = c.get('db');
  const allUsers = await db.select().from(users);
  return c.json(allUsers);
});

// Get user by ID
app.get('/users/:id', async (c) => {
  const db = c.get('db');
  const id = parseInt(c.req.param('id'));

  const user = await db.select().from(users).where(eq(users.id, id)).get();

  if (!user) {
    return c.json({ error: 'User not found' }, 404);
  }
  return c.json(user);
});

// Create user
app.post('/users', async (c) => {
  const db = c.get('db');
  const body = await c.req.json<{ email: string; name: string }>();

  const result = await db.insert(users).values({
    email: body.email,
    name: body.name
  }).returning();

  return c.json(result[0], 201);
});

// Update user
app.put('/users/:id', async (c) => {
  const db = c.get('db');
  const id = parseInt(c.req.param('id'));
  const body = await c.req.json<Partial<{ email: string; name: string }>>();

  const result = await db.update(users)
    .set({ ...body, updatedAt: new Date().toISOString() })
    .where(eq(users.id, id))
    .returning();

  if (result.length === 0) {
    return c.json({ error: 'User not found' }, 404);
  }
  return c.json(result[0]);
});

// Delete user
app.delete('/users/:id', async (c) => {
  const db = c.get('db');
  const id = parseInt(c.req.param('id'));

  const result = await db.delete(users).where(eq(users.id, id)).returning();

  if (result.length === 0) {
    return c.json({ error: 'User not found' }, 404);
  }
  return c.json({ deleted: true });
});

export default app;
```

### Raw D1 API (Without ORM)
```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/users' && request.method === 'GET') {
      const { results } = await env.DB.prepare(
        'SELECT * FROM users ORDER BY created_at DESC'
      ).all();
      return Response.json(results);
    }

    if (url.pathname === '/users' && request.method === 'POST') {
      const body = await request.json() as { email: string; name: string };

      const result = await env.DB.prepare(
        'INSERT INTO users (email, name) VALUES (?, ?) RETURNING *'
      ).bind(body.email, body.name).first();

      return Response.json(result, { status: 201 });
    }

    return new Response('Not Found', { status: 404 });
  }
};
```

---

## Query Patterns

### Select Queries
```typescript
import { eq, and, or, like, gt, desc, asc, count, sql } from 'drizzle-orm';

// Basic select
const allPosts = await db.select().from(posts);

// Select specific columns
const titles = await db.select({ id: posts.id, title: posts.title }).from(posts);

// Where clause
const published = await db.select().from(posts).where(eq(posts.published, true));

// Multiple conditions
const recentPublished = await db.select().from(posts).where(
  and(
    eq(posts.published, true),
    gt(posts.createdAt, '2024-01-01')
  )
);

// OR conditions
const featured = await db.select().from(posts).where(
  or(
    eq(posts.viewCount, 1000),
    like(posts.title, '%featured%')
  )
);

// Order and limit
const topPosts = await db.select()
  .from(posts)
  .orderBy(desc(posts.viewCount))
  .limit(10);

// Pagination
const page2 = await db.select()
  .from(posts)
  .orderBy(desc(posts.createdAt))
  .limit(10)
  .offset(10);

// Count
const postCount = await db.select({ count: count() }).from(posts);
```

### Joins
```typescript
// Inner join
const postsWithAuthors = await db.select({
  post: posts,
  author: users
})
.from(posts)
.innerJoin(users, eq(posts.authorId, users.id));

// Left join
const allPostsWithAuthors = await db.select()
  .from(posts)
  .leftJoin(users, eq(posts.authorId, users.id));

// Many-to-many via junction table
const postsWithTags = await db.select({
  post: posts,
  tag: tags
})
.from(posts)
.leftJoin(postTags, eq(posts.id, postTags.postId))
.leftJoin(tags, eq(postTags.tagId, tags.id));
```

### Insert, Update, Delete
```typescript
// Insert single
const newUser = await db.insert(users).values({
  email: 'user@example.com',
  name: 'John Doe'
}).returning();

// Insert multiple
await db.insert(users).values([
  { email: 'a@test.com', name: 'Alice' },
  { email: 'b@test.com', name: 'Bob' }
]);

// Upsert (insert or update on conflict)
await db.insert(users)
  .values({ email: 'user@test.com', name: 'New Name' })
  .onConflictDoUpdate({
    target: users.email,
    set: { name: 'New Name' }
  });

// Update
await db.update(posts)
  .set({ published: true })
  .where(eq(posts.id, 1));

// Update with increment
await db.update(posts)
  .set({ viewCount: sql`${posts.viewCount} + 1` })
  .where(eq(posts.id, 1));

// Delete
await db.delete(posts).where(eq(posts.id, 1));
```

### Transactions
```typescript
// D1 supports transactions via batch
const results = await db.batch([
  db.insert(users).values({ email: 'a@test.com', name: 'A' }),
  db.insert(users).values({ email: 'b@test.com', name: 'B' }),
  db.update(posts).set({ published: true }).where(eq(posts.id, 1))
]);

// Raw D1 batch
const batchResults = await env.DB.batch([
  env.DB.prepare('INSERT INTO users (email, name) VALUES (?, ?)').bind('a@test.com', 'A'),
  env.DB.prepare('INSERT INTO users (email, name) VALUES (?, ?)').bind('b@test.com', 'B')
]);
```

---

## Local Development

### Start Dev Server
```bash
# Local development with D1
npx wrangler dev

# With specific port
npx wrangler dev --port 8787
```

### Database Management
```bash
# Execute SQL locally
npx wrangler d1 execute my-database --local --command "SELECT * FROM users"

# Execute SQL file
npx wrangler d1 execute my-database --local --file ./seed.sql

# Open SQLite shell
npx wrangler d1 execute my-database --local --command ".tables"
```

### Drizzle Studio
```bash
# Run Drizzle Studio for visual DB management
npx drizzle-kit studio
```

### Seed Data
```sql
-- seed.sql
INSERT INTO users (email, name, role) VALUES
  ('admin@example.com', 'Admin User', 'admin'),
  ('user@example.com', 'Test User', 'user');

INSERT INTO posts (title, content, author_id, published) VALUES
  ('First Post', 'Hello World!', 1, true),
  ('Draft Post', 'Work in progress...', 1, false);
```

```bash
# Seed local database
npx wrangler d1 execute my-database --local --file ./seed.sql
```

---

## Multi-Environment Setup

### wrangler.toml
```toml
name = "my-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

# Development
[env.dev]
[[env.dev.d1_databases]]
binding = "DB"
database_name = "my-database-dev"
database_id = "dev-database-id"

# Staging
[env.staging]
[[env.staging.d1_databases]]
binding = "DB"
database_name = "my-database-staging"
database_id = "staging-database-id"

# Production
[env.production]
[[env.production.d1_databases]]
binding = "DB"
database_name = "my-database-prod"
database_id = "prod-database-id"
```

### Deploy to Environments
```bash
# Deploy to staging
npx wrangler deploy --env staging

# Deploy to production
npx wrangler deploy --env production

# Apply migrations to staging
npx wrangler d1 migrations apply my-database-staging --remote --env staging
```

---

## Testing

### Integration Tests
```typescript
// tests/api.test.ts
import { unstable_dev } from 'wrangler';
import type { UnstableDevWorker } from 'wrangler';
import { describe, beforeAll, afterAll, it, expect } from 'vitest';

describe('API', () => {
  let worker: UnstableDevWorker;

  beforeAll(async () => {
    worker = await unstable_dev('src/index.ts', {
      experimental: { disableExperimentalWarning: true }
    });
  });

  afterAll(async () => {
    await worker.stop();
  });

  it('should list users', async () => {
    const res = await worker.fetch('/users');
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(Array.isArray(data)).toBe(true);
  });

  it('should create user', async () => {
    const res = await worker.fetch('/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@test.com', name: 'Test' })
    });
    expect(res.status).toBe(201);
  });
});
```

---

## CLI Quick Reference

```bash
# Database
wrangler d1 create <name>                    # Create database
wrangler d1 list                             # List databases
wrangler d1 info <name>                      # Database info
wrangler d1 delete <name>                    # Delete database

# Migrations
wrangler d1 migrations list <name>           # List migrations
wrangler d1 migrations apply <name> --local  # Apply locally
wrangler d1 migrations apply <name> --remote # Apply to production

# SQL execution
wrangler d1 execute <name> --command "SQL"   # Run SQL
wrangler d1 execute <name> --file ./file.sql # Run SQL file
wrangler d1 execute <name> --local           # Run on local
wrangler d1 execute <name> --remote          # Run on production

# Development
wrangler dev                                 # Start local server
wrangler types                               # Generate TypeScript types
wrangler deploy                              # Deploy to production

# Drizzle
drizzle-kit generate                         # Generate migrations
drizzle-kit migrate                          # Apply migrations
drizzle-kit studio                           # Open Drizzle Studio
drizzle-kit push                             # Push schema (dev only)
```

---

## D1 Limits & Considerations

| Limit | Value |
|-------|-------|
| **Database size** | 10 GB max |
| **Row size** | 1 MB max |
| **SQL statement** | 100 KB max |
| **Batch size** | 1000 statements |
| **Reads per day (free)** | 5 million |
| **Writes per day (free)** | 100,000 |

---

## Anti-Patterns

- **Single large database** - Design for multiple smaller databases (per-tenant)
- **No migrations** - Always version control schema changes
- **Raw SQL everywhere** - Use Drizzle for type safety
- **No connection to remote** - Always test against real D1 before deploy
- **Large blobs in D1** - Use R2 for file storage
- **Complex joins** - D1 is SQLite; keep queries simple
- **No batching** - Use batch for multiple operations
- **Ignoring limits** - Monitor usage on free tier
