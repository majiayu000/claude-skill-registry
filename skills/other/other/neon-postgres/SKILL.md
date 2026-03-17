---
name: neon-postgres
description: Neon PostgreSQL serverless database - connection pooling, branching, serverless driver, and optimization. Use when deploying to Neon or building serverless applications.
---

# Neon PostgreSQL Skill

Serverless PostgreSQL with branching, autoscaling, and instant provisioning.

## Quick Start

### Create Database

1. Go to [console.neon.tech](https://console.neon.tech)
2. Create a new project
3. Copy connection string

### Installation

```bash
# npm
npm install @neondatabase/serverless

# pnpm
pnpm add @neondatabase/serverless

# yarn
yarn add @neondatabase/serverless

# bun
bun add @neondatabase/serverless
```

## Connection Strings

```env
# Direct connection (for migrations, scripts)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# Pooled connection (for application)
DATABASE_URL_POOLED=postgresql://user:password@ep-xxx-pooler.us-east-1.aws.neon.tech/dbname?sslmode=require
```

## Key Concepts

| Concept | Guide |
|---------|-------|
| **Serverless Driver** | [reference/serverless-driver.md](reference/serverless-driver.md) |
| **Connection Pooling** | [reference/pooling.md](reference/pooling.md) |
| **Branching** | [reference/branching.md](reference/branching.md) |
| **Autoscaling** | [reference/autoscaling.md](reference/autoscaling.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **Next.js Integration** | [examples/nextjs.md](examples/nextjs.md) |
| **Edge Functions** | [examples/edge.md](examples/edge.md) |
| **Migrations** | [examples/migrations.md](examples/migrations.md) |
| **Branching Workflow** | [examples/branching-workflow.md](examples/branching-workflow.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/db.ts](templates/db.ts) | Database connection |
| [templates/neon.config.ts](templates/neon.config.ts) | Neon configuration |

## Connection Methods

### HTTP (Serverless - Recommended)

Best for: Edge functions, serverless, one-shot queries

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

// Simple query
const posts = await sql`SELECT * FROM posts WHERE published = true`;

// With parameters
const post = await sql`SELECT * FROM posts WHERE id = ${postId}`;

// Insert
await sql`INSERT INTO posts (title, content) VALUES (${title}, ${content})`;
```

### WebSocket (Connection Pooling)

Best for: Long-running connections, transactions

```typescript
import { Pool } from "@neondatabase/serverless";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const client = await pool.connect();
try {
  await client.query("BEGIN");
  await client.query("INSERT INTO posts (title) VALUES ($1)", [title]);
  await client.query("COMMIT");
} catch (e) {
  await client.query("ROLLBACK");
  throw e;
} finally {
  client.release();
}
```

## With Drizzle ORM

### HTTP Driver

```typescript
// src/db/index.ts
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

### WebSocket Driver

```typescript
// src/db/index.ts
import { Pool } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-serverless";
import * as schema from "./schema";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });
```

## Branching

Neon branches are copy-on-write clones of your database.

### CLI Commands

```bash
# Install Neon CLI
npm install -g neonctl

# Login
neonctl auth

# List branches
neonctl branches list

# Create branch
neonctl branches create --name feature-x

# Get connection string
neonctl connection-string feature-x

# Delete branch
neonctl branches delete feature-x
```

### Branch Workflow

```bash
# Create branch for feature
neonctl branches create --name feature-auth --parent main

# Get connection string for branch
export DATABASE_URL=$(neonctl connection-string feature-auth)

# Work on feature...

# When done, merge via application migrations
neonctl branches delete feature-auth
```

### CI/CD Integration

```yaml
# .github/workflows/preview.yml
name: Preview
on: pull_request

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create Neon Branch
        uses: neondatabase/create-branch-action@v5
        id: branch
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          api_key: ${{ secrets.NEON_API_KEY }}
          branch_name: preview-${{ github.event.pull_request.number }}

      - name: Run Migrations
        env:
          DATABASE_URL: ${{ steps.branch.outputs.db_url }}
        run: npx drizzle-kit migrate
```

## Connection Pooling

### When to Use Pooling

| Scenario | Connection Type |
|----------|-----------------|
| Edge/Serverless functions | HTTP (neon) |
| API routes with transactions | WebSocket Pool |
| Long-running processes | WebSocket Pool |
| One-shot queries | HTTP (neon) |

### Pooler URL

```env
# Without pooler (direct)
postgresql://user:pass@ep-xxx.aws.neon.tech/db

# With pooler (add -pooler to endpoint)
postgresql://user:pass@ep-xxx-pooler.aws.neon.tech/db
```

## Autoscaling

Configure in Neon console:

- **Min compute**: 0.25 CU (can scale to zero)
- **Max compute**: Up to 8 CU
- **Scale to zero delay**: 5 minutes (default)

### Handle Cold Starts

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!, {
  fetchOptions: {
    // Increase timeout for cold starts
    signal: AbortSignal.timeout(10000),
  },
});
```

## Best Practices

### 1. Use HTTP for Serverless

```typescript
// Good - HTTP for serverless
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);

// Avoid - Pool in serverless (connection exhaustion)
import { Pool } from "@neondatabase/serverless";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

### 2. Connection String per Environment

```env
# .env.development
DATABASE_URL=postgresql://...@ep-dev-branch...

# .env.production
DATABASE_URL=postgresql://...@ep-main...
```

### 3. Use Prepared Statements

```typescript
// Good - parameterized query
const result = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Bad - string interpolation (SQL injection risk)
const result = await sql(`SELECT * FROM users WHERE id = '${userId}'`);
```

### 4. Handle Errors

```typescript
import { neon, NeonDbError } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

try {
  await sql`INSERT INTO users (email) VALUES (${email})`;
} catch (error) {
  if (error instanceof NeonDbError) {
    if (error.code === "23505") {
      // Unique violation
      throw new Error("Email already exists");
    }
  }
  throw error;
}
```

## Next.js App Router

```typescript
// app/posts/page.tsx
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

export default async function PostsPage() {
  const posts = await sql`SELECT * FROM posts ORDER BY created_at DESC`;

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

## Drizzle + Neon Complete Setup

```typescript
// src/db/index.ts
import { neon } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-http";
import * as schema from "./schema";

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });

// src/db/schema.ts
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const posts = pgTable("posts", {
  id: serial("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/db/schema.ts",
  out: "./src/db/migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```
