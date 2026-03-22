---
name: d1-database
description: >-
  Build serverless applications with Cloudflare D1 — SQLite at the edge. Use
  when someone asks to "serverless database", "Cloudflare D1", "SQLite at the
  edge", "database for Workers", "edge database", or "serverless SQL". Covers
  schema setup, queries, migrations, Workers integration, and Drizzle ORM.
license: Apache-2.0
compatibility: "Cloudflare Workers. Wrangler CLI. SQLite-compatible."
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: data-ai
  tags: ["database", "cloudflare", "d1", "sqlite", "edge"]
---

# Cloudflare D1

## Overview

D1 is Cloudflare's serverless SQLite database — runs at the edge alongside Workers. Zero connection overhead (it's in the same data center as your Worker), SQLite query syntax, automatic replication, and pay-per-query pricing. Perfect for read-heavy workloads, content sites, and applications where latency matters.

## When to Use

- Building on Cloudflare Workers and need a database
- Read-heavy applications (blogs, content sites, APIs)
- Want SQLite simplicity with global distribution
- Serverless applications with no connection pooling headaches
- Edge-first applications where database latency matters

## Instructions

### Setup

```bash
# Create a D1 database
npx wrangler d1 create my-database

# Add to wrangler.toml
```

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxxx-xxxx-xxxx"
```

### Schema and Migrations

```bash
# Create migration
npx wrangler d1 migrations create my-database init
```

```sql
-- migrations/0001_init.sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  author_id INTEGER NOT NULL REFERENCES users(id),
  published BOOLEAN DEFAULT FALSE,
  created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_published ON posts(published);
```

```bash
# Apply migrations
npx wrangler d1 migrations apply my-database
```

### Queries in Workers

```typescript
// src/index.ts — Cloudflare Worker with D1
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/posts" && request.method === "GET") {
      const { results } = await env.DB.prepare(
        `SELECT posts.*, users.name as author_name
         FROM posts
         JOIN users ON posts.author_id = users.id
         WHERE posts.published = TRUE
         ORDER BY posts.created_at DESC
         LIMIT ?`
      ).bind(20).all();

      return Response.json({ posts: results });
    }

    if (url.pathname === "/api/posts" && request.method === "POST") {
      const body = await request.json();
      const result = await env.DB.prepare(
        "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?) RETURNING *"
      ).bind(body.title, body.content, body.authorId).first();

      return Response.json({ post: result }, { status: 201 });
    }

    return new Response("Not found", { status: 404 });
  },
};
```

### With Drizzle ORM

```typescript
// src/db/schema.ts — Drizzle schema for D1
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  email: text("email").notNull().unique(),
  name: text("name").notNull(),
});

export const posts = sqliteTable("posts", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  title: text("title").notNull(),
  content: text("content").notNull(),
  authorId: integer("author_id").notNull().references(() => users.id),
  published: integer("published", { mode: "boolean" }).default(false),
});
```

```typescript
// src/index.ts — Using Drizzle with D1
import { drizzle } from "drizzle-orm/d1";
import { eq } from "drizzle-orm";
import * as schema from "./db/schema";

export default {
  async fetch(request: Request, env: Env) {
    const db = drizzle(env.DB, { schema });

    const publishedPosts = await db.query.posts.findMany({
      where: eq(schema.posts.published, true),
      with: { author: true },
      orderBy: (posts, { desc }) => [desc(posts.id)],
      limit: 20,
    });

    return Response.json({ posts: publishedPosts });
  },
};
```

## Examples

### Example 1: Build a blog API on the edge

**User prompt:** "Create a blog API with Cloudflare Workers and D1 for posts and comments."

The agent will create D1 schema, migrations, CRUD endpoints in a Worker, and Drizzle ORM integration.

### Example 2: User authentication with D1

**User prompt:** "Store user accounts in D1 with email/password auth."

The agent will create users table, password hashing with Web Crypto API, session management, and auth middleware.

## Guidelines

- **SQLite syntax** — D1 is SQLite under the hood
- **Prepared statements with `.bind()`** — prevent SQL injection
- **`.first()` for single row, `.all()` for multiple** — query methods
- **Migrations via Wrangler** — version-controlled schema changes
- **Read replicas are automatic** — D1 replicates globally
- **Write latency is higher** — writes go to primary; reads are fast everywhere
- **5MB row limit** — not for large blobs
- **Free tier: 5M reads, 100K writes/day** — generous for small apps
- **Drizzle ORM recommended** — type-safe queries with D1 adapter
- **Local development** — `wrangler dev` uses local SQLite
