---
name: turso
description: Implements Turso edge SQLite database with libSQL client, embedded replicas, and vector search. Use when building edge-first apps, implementing embedded databases, or needing SQLite with global replication.
---

# Turso

Turso is an edge-hosted SQLite database built on libSQL. It provides global replication, embedded replicas for ultra-low latency, and native vector search.

## Quick Start

### Create Database

```bash
# Install CLI
brew install tursodatabase/tap/turso

# Authenticate
turso auth login

# Create database
turso db create my-app

# Get connection URL
turso db show my-app --url

# Create auth token
turso db tokens create my-app
```

### Install Client

```bash
npm install @libsql/client
```

### Basic Connection

```typescript
import { createClient } from '@libsql/client'

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!
})

// Execute query
const result = await client.execute('SELECT * FROM users')
console.log(result.rows)
```

## CRUD Operations

### Create Table

```typescript
await client.execute(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
  )
`)
```

### Insert

```typescript
// Single insert with parameters
const result = await client.execute({
  sql: 'INSERT INTO users (email, name) VALUES (?, ?)',
  args: ['user@example.com', 'John Doe']
})

console.log('Inserted ID:', result.lastInsertRowid)

// Named parameters
await client.execute({
  sql: 'INSERT INTO users (email, name) VALUES (:email, :name)',
  args: { email: 'alice@example.com', name: 'Alice' }
})
```

### Select

```typescript
// All rows
const { rows } = await client.execute('SELECT * FROM users')

// With parameters
const { rows } = await client.execute({
  sql: 'SELECT * FROM users WHERE id = ?',
  args: [userId]
})

// Single row
const user = rows[0]
```

### Update

```typescript
const result = await client.execute({
  sql: 'UPDATE users SET name = ? WHERE id = ?',
  args: ['Updated Name', userId]
})

console.log('Rows affected:', result.rowsAffected)
```

### Delete

```typescript
await client.execute({
  sql: 'DELETE FROM users WHERE id = ?',
  args: [userId]
})
```

## Batch Operations

Execute multiple statements in a single round-trip:

```typescript
const results = await client.batch([
  {
    sql: 'INSERT INTO users (email, name) VALUES (?, ?)',
    args: ['user1@example.com', 'User 1']
  },
  {
    sql: 'INSERT INTO users (email, name) VALUES (?, ?)',
    args: ['user2@example.com', 'User 2']
  },
  'SELECT * FROM users'
], 'write')

// Last result contains SELECT output
const users = results[2].rows
```

## Transactions

```typescript
const transaction = await client.transaction('write')

try {
  await transaction.execute({
    sql: 'INSERT INTO accounts (user_id, balance) VALUES (?, ?)',
    args: [userId, 1000]
  })

  await transaction.execute({
    sql: 'UPDATE users SET has_account = 1 WHERE id = ?',
    args: [userId]
  })

  await transaction.commit()
} catch (error) {
  await transaction.rollback()
  throw error
}
```

## Embedded Replicas

Embedded replicas provide local read access with automatic sync from the primary database.

### Setup

```typescript
import { createClient } from '@libsql/client'

const client = createClient({
  url: 'file:local-replica.db',  // Local file
  syncUrl: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!,
  syncInterval: 60  // Sync every 60 seconds
})

// Manual sync
await client.sync()
```

### Read-Your-Writes Pattern

```typescript
// Write to remote, sync, then read locally
await client.execute({
  sql: 'INSERT INTO posts (title) VALUES (?)',
  args: ['New Post']
})

await client.sync()

// Now read from local replica
const { rows } = await client.execute('SELECT * FROM posts')
```

### Platform-Specific Setup

#### Cloudflare Workers

```typescript
// wrangler.toml
// [vars]
// TURSO_DATABASE_URL = "libsql://..."
// TURSO_AUTH_TOKEN = "..."

import { createClient } from '@libsql/client/web'

export default {
  async fetch(request: Request, env: Env) {
    const client = createClient({
      url: env.TURSO_DATABASE_URL,
      authToken: env.TURSO_AUTH_TOKEN
    })

    const { rows } = await client.execute('SELECT * FROM users')
    return Response.json(rows)
  }
}
```

#### Vercel Edge

```typescript
// Use HTTP client for edge runtime
import { createClient } from '@libsql/client/web'

export const runtime = 'edge'

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!
})

export async function GET() {
  const { rows } = await client.execute('SELECT * FROM users')
  return Response.json(rows)
}
```

## Vector Search

Turso has native vector support for AI applications:

```typescript
// Create table with vector column
await client.execute(`
  CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    content TEXT,
    embedding F32_BLOB(1536)  -- OpenAI embedding dimension
  )
`)

// Insert with embedding
const embedding = await getEmbedding('Hello world')  // Your embedding function
await client.execute({
  sql: 'INSERT INTO documents (content, embedding) VALUES (?, vector(?))',
  args: ['Hello world', JSON.stringify(embedding)]
})

// Similarity search
const queryEmbedding = await getEmbedding('greeting')
const { rows } = await client.execute({
  sql: `
    SELECT id, content,
           vector_distance_cos(embedding, vector(?)) as distance
    FROM documents
    ORDER BY distance
    LIMIT 10
  `,
  args: [JSON.stringify(queryEmbedding)]
})
```

## Drizzle ORM Integration

```bash
npm install drizzle-orm
npm install -D drizzle-kit
```

### Schema Definition

```typescript
// src/db/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core'

export const users = sqliteTable('users', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: text('created_at').default('CURRENT_TIMESTAMP')
})

export const posts = sqliteTable('posts', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  title: text('title').notNull(),
  content: text('content'),
  authorId: integer('author_id').references(() => users.id)
})
```

### Client Setup

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/libsql'
import { createClient } from '@libsql/client'
import * as schema from './schema'

const client = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!
})

export const db = drizzle(client, { schema })
```

### Queries

```typescript
import { db } from './db'
import { users, posts } from './db/schema'
import { eq } from 'drizzle-orm'

// Insert
const newUser = await db.insert(users).values({
  email: 'user@example.com',
  name: 'John'
}).returning()

// Select with relations
const usersWithPosts = await db.query.users.findMany({
  with: { posts: true }
})

// Update
await db.update(users)
  .set({ name: 'Updated' })
  .where(eq(users.id, 1))

// Delete
await db.delete(users).where(eq(users.id, 1))
```

## Prisma Integration

```bash
npm install prisma @prisma/client @prisma/adapter-libsql @libsql/client
```

### Schema

```prisma
// prisma/schema.prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider = "sqlite"
  url      = "file:./dev.db"
}

model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
  posts Post[]
}

model Post {
  id       Int    @id @default(autoincrement())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId Int
}
```

### Client Setup

```typescript
import { PrismaClient } from '@prisma/client'
import { PrismaLibSQL } from '@prisma/adapter-libsql'
import { createClient } from '@libsql/client'

const libsql = createClient({
  url: process.env.TURSO_DATABASE_URL!,
  authToken: process.env.TURSO_AUTH_TOKEN!
})

const adapter = new PrismaLibSQL(libsql)
const prisma = new PrismaClient({ adapter })

// Use normally
const users = await prisma.user.findMany()
```

## Multi-Region Replication

### Add Replica Locations

```bash
# List available locations
turso db locations

# Add replica in specific region
turso db replicate my-app fra  # Frankfurt
turso db replicate my-app syd  # Sydney

# List replicas
turso db show my-app
```

### Closest Replica Routing

Turso automatically routes reads to the closest replica. The primary handles writes and propagates changes.

## CLI Reference

```bash
# Database operations
turso db create <name> [--location <loc>]
turso db destroy <name>
turso db list
turso db show <name>

# Replicas
turso db replicate <name> <location>
turso db unreplicate <name> <location>
turso db locations

# Tokens
turso db tokens create <name> [--expiration <duration>]
turso db tokens revoke <name> <token>

# Shell access
turso db shell <name>

# Groups (for multi-db)
turso group create <name>
turso db create <name> --group <group>
```

## Environment Variables

```env
# .env
TURSO_DATABASE_URL="libsql://your-db-your-org.turso.io"
TURSO_AUTH_TOKEN="your-auth-token"

# For embedded replicas
TURSO_SYNC_URL="libsql://your-db-your-org.turso.io"
TURSO_LOCAL_DB="file:local.db"
```

## Best Practices

1. **Use embedded replicas for read-heavy workloads** - Eliminates network latency
2. **Batch related operations** - Single round-trip for multiple statements
3. **Use transactions for consistency** - Wrap related writes
4. **Sync strategically** - Balance freshness vs. performance
5. **Add replicas near users** - Reduce read latency globally
6. **Use parameterized queries** - Prevent SQL injection

## References

- [Embedded Replicas Guide](references/embedded-replicas.md)
- [Vector Search Patterns](references/vector-search.md)
