---
name: neon
version: 1.0.0
description: Neon serverless Postgres platform with branching, autoscaling, scale-to-zero, and edge-compatible drivers for modern application development
---

# Neon Serverless Postgres

> Serverless PostgreSQL with database branching, autoscaling compute, and edge-compatible drivers.

## When to Use This Skill

- Building serverless or edge applications needing Postgres
- Implementing database branching for dev/test/preview environments
- Setting up autoscaling databases with scale-to-zero
- Integrating Postgres with Vercel, Next.js, or edge runtimes
- Storing vector embeddings with pgvector for AI applications
- Migrating from traditional Postgres to serverless architecture

## Quick Start

### Create Project with CLI

```bash
# Install Neon CLI
npm install -g neonctl

# Authenticate
neonctl auth

# Create project
neonctl projects create --name my-app

# Get connection string
neonctl connection-string
```

### AI-Guided Setup

```bash
# Auto-configure for your codebase
npx neonctl@latest init
```

### Connection String Format

```
postgresql://[user]:[password]@[endpoint].neon.tech/[dbname]?sslmode=require&channel_binding=require
```

**Pooled Connection** (for high concurrency):
```
postgresql://[user]:[password]@[endpoint]-pooler.neon.tech/[dbname]?sslmode=require
```

---

## Core Concepts

### Architecture: Separation of Compute and Storage

```
┌─────────────────────────────────────────────────────┐
│                    Neon Platform                     │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Compute 1  │  │  Compute 2  │  │  Compute N  │ │
│  │  (Branch A) │  │  (Branch B) │  │  (Read Rep) │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│  ┌──────┴────────────────┴────────────────┴──────┐ │
│  │              Shared Storage Layer              │ │
│  │        (Copy-on-write, Instant Branching)      │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Branching** | Copy-on-write database clones for dev/test/preview |
| **Autoscaling** | Dynamic compute sizing (0.25-56 CU) |
| **Scale-to-Zero** | Automatic suspension after inactivity |
| **Instant Restore** | Point-in-time recovery within retention window |
| **Read Replicas** | Distribute read workloads |
| **Serverless Driver** | HTTP/WebSocket for edge runtimes |

### Compute Units (CU)

| CU | RAM | Max Connections |
|----|-----|-----------------|
| 0.25 | 1 GB | 104 |
| 0.5 | 2 GB | 225 |
| 1 | 4 GB | 225 |
| 2 | 8 GB | 450 |
| 4 | 16 GB | 901 |
| 8 | 32 GB | 1,802 |
| 16 | 64 GB | 3,604 |
| 56 | 224 GB | 4,000+ |

---

## Branching

### What Are Branches?

Branches are **copy-on-write clones** of your database. They're instant to create, fully isolated, and don't impact parent performance.

```
main (production)
├── dev (development copy)
├── staging (pre-production)
├── preview-pr-123 (PR preview)
└── test-migration (schema testing)
```

### Create Branch via CLI

```bash
# Branch from main
neonctl branches create --name dev --project-id <project_id>

# Branch from specific point in time
neonctl branches create --name restore-point --parent main --timestamp "2024-01-15T10:00:00Z"

# Branch from another branch
neonctl branches create --name feature-x --parent dev
```

### Branch Use Cases

**Development**: Isolated copies for each developer
```bash
neonctl branches create --name dev-alice
neonctl branches create --name dev-bob
```

**Testing**: Validate schema changes safely
```bash
neonctl branches create --name test-migration
# Run migrations on test branch
# If successful, apply to main
```

**Preview Deployments**: Automatic branches for PRs (Vercel integration)

**Temporary Environments**: TTL-based expiration for CI/CD
```bash
# Branch auto-deleted after TTL
neonctl branches create --name ci-test --ttl 3600  # 1 hour
```

### Branch Operations

```bash
# List branches
neonctl branches list --project-id <project_id>

# Reset branch to parent state
neonctl branches reset --name dev --parent main

# Delete branch
neonctl branches delete --name feature-completed

# Rename branch
neonctl branches rename --name old-name --new-name new-name
```

---

## Autoscaling & Scale-to-Zero

### Autoscaling Configuration

Autoscaling dynamically adjusts compute between min and max limits:

```bash
# Configure via CLI
neonctl computes update <compute_id> \
  --autoscaling-min 0.5 \
  --autoscaling-max 4
```

**Console Path**: Branches → Select Branch → Edit Compute

### Scale-to-Zero

Computes automatically suspend after inactivity:

| Plan | Default Timeout | Configurable |
|------|-----------------|--------------|
| Free | 5 minutes | No |
| Launch | 5 minutes | Yes (can disable) |
| Scale | Configurable | 1 min to always-on |

**Activation Time**: ~500ms cold start when compute resumes

### Connection Timeout for Scale-to-Zero

```javascript
// Add connect_timeout for cold starts
const connectionString = process.env.DATABASE_URL + '&connect_timeout=10';
```

---

## Serverless Driver

### Installation

```bash
npm install @neondatabase/serverless
```

### HTTP Queries (Recommended for Serverless/Edge)

```typescript
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

// Template literal syntax (parameterized)
const users = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Multiple values
const results = await sql`
  SELECT * FROM products
  WHERE category = ${category}
  AND price < ${maxPrice}
`;
```

### HTTP Transactions

```typescript
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

const [order, items] = await sql.transaction([
  sql`INSERT INTO orders (user_id, total) VALUES (${userId}, ${total}) RETURNING *`,
  sql`INSERT INTO order_items (order_id, product_id) SELECT ... RETURNING *`
], {
  isolationLevel: 'Serializable',
  readOnly: false
});
```

### WebSocket Connections (for Session/Interactive Transactions)

```typescript
import { Pool, neonConfig } from '@neondatabase/serverless';
import ws from 'ws';

// Required for Node.js environments
neonConfig.webSocketConstructor = ws;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// Interactive transaction
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('UPDATE accounts SET balance = balance - $1 WHERE id = $2', [100, fromId]);
  await client.query('UPDATE accounts SET balance = balance + $1 WHERE id = $2', [100, toId]);
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}

await pool.end();
```

### HTTP vs WebSocket Decision

| Use Case | Protocol |
|----------|----------|
| Single query | HTTP |
| Non-interactive transaction | HTTP |
| Edge runtime (Vercel/Cloudflare) | HTTP |
| Session-based transactions | WebSocket |
| Interactive transactions | WebSocket |
| Multiple queries per connection | WebSocket |

---

## ORM Integration

### Prisma

**Schema Configuration**:
```prisma
// prisma/schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")      // Pooled connection
  directUrl = env("DIRECT_URL")        // Direct for migrations
}

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]  // For serverless driver
}
```

**Environment Variables**:
```env
# Pooled for application
DATABASE_URL="postgresql://user:pass@ep-xxx-pooler.neon.tech/db?sslmode=require"
# Direct for migrations
DIRECT_URL="postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require"
```

**With Serverless Driver** (Prisma 5.4.2+):
```typescript
import { Pool, neonConfig } from '@neondatabase/serverless';
import { PrismaNeon } from '@prisma/adapter-neon';
import { PrismaClient } from '@prisma/client';
import ws from 'ws';

neonConfig.webSocketConstructor = ws;

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const adapter = new PrismaNeon(pool);
const prisma = new PrismaClient({ adapter });
```

### Drizzle ORM

**Installation**:
```bash
npm install drizzle-orm @neondatabase/serverless
npm install -D drizzle-kit
```

**Configuration**:
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

**Schema Definition**:
```typescript
// src/db/schema.ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  email: text('email').unique().notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

**Client Setup**:
```typescript
// src/db/index.ts
import { neon } from '@neondatabase/serverless';
import { drizzle } from 'drizzle-orm/neon-http';
import * as schema from './schema';

const sql = neon(process.env.DATABASE_URL!);
export const db = drizzle(sql, { schema });
```

**Migrations**:
```bash
# Generate migrations
npx drizzle-kit generate

# Apply migrations
npx drizzle-kit migrate
```

---

## Framework Integration

### Next.js App Router

**Server Component**:
```typescript
// app/users/page.tsx
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

export default async function UsersPage() {
  const users = await sql`SELECT * FROM users ORDER BY created_at DESC`;

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**Server Action**:
```typescript
// app/actions.ts
'use server';

import { neon } from '@neondatabase/serverless';
import { revalidatePath } from 'next/cache';

const sql = neon(process.env.DATABASE_URL!);

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;

  await sql`INSERT INTO users (name, email) VALUES (${name}, ${email})`;
  revalidatePath('/users');
}
```

### Vercel Integration

**Automatic Branch Creation**:
1. Install Neon integration from Vercel Marketplace
2. Connect your Neon project
3. Preview deployments automatically get database branches

**Environment Variables** (auto-configured):
- `DATABASE_URL` - Pooled connection string
- `DATABASE_URL_UNPOOLED` - Direct connection string

### Edge Functions (Vercel/Cloudflare)

```typescript
// Only HTTP driver works in edge runtime
import { neon } from '@neondatabase/serverless';

export const runtime = 'edge';

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!);
  const data = await sql`SELECT NOW()`;
  return Response.json(data);
}
```

---

## AI & Vector Search (pgvector)

### Enable pgvector

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Create Vector Table

```sql
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding vector(1536),  -- OpenAI embedding dimension
  metadata JSONB
);

-- Create index for similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### Store Embeddings

```typescript
import { neon } from '@neondatabase/serverless';
import OpenAI from 'openai';

const sql = neon(process.env.DATABASE_URL!);
const openai = new OpenAI();

async function storeDocument(content: string, metadata: object) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: content,
  });

  const embedding = response.data[0].embedding;

  await sql`
    INSERT INTO documents (content, embedding, metadata)
    VALUES (${content}, ${JSON.stringify(embedding)}::vector, ${JSON.stringify(metadata)})
  `;
}
```

### Similarity Search

```typescript
async function search(query: string, limit = 5) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: query,
  });

  const queryEmbedding = response.data[0].embedding;

  const results = await sql`
    SELECT content, metadata, 1 - (embedding <=> ${JSON.stringify(queryEmbedding)}::vector) as similarity
    FROM documents
    ORDER BY embedding <=> ${JSON.stringify(queryEmbedding)}::vector
    LIMIT ${limit}
  `;

  return results;
}
```

### RAG Pattern

```typescript
async function ragQuery(userQuestion: string) {
  // 1. Find relevant documents
  const context = await search(userQuestion, 3);

  // 2. Generate response with context
  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: `Answer based on this context:\n${context.map(d => d.content).join('\n\n')}`
      },
      { role: 'user', content: userQuestion }
    ]
  });

  return response.choices[0].message.content;
}
```

---

## PostgreSQL Extensions

### Commonly Used Extensions

```sql
-- Vector similarity search
CREATE EXTENSION vector;

-- Full-text search (built-in, no CREATE needed)
-- Use: to_tsvector(), to_tsquery()

-- UUID generation
CREATE EXTENSION "uuid-ossp";
SELECT uuid_generate_v4();

-- Cryptographic functions
CREATE EXTENSION pgcrypto;
SELECT crypt('password', gen_salt('bf'));

-- Geospatial
CREATE EXTENSION postgis;

-- Job scheduling
CREATE EXTENSION pg_cron;
-- Note: Jobs only run when compute is active

-- Statistics
CREATE EXTENSION pg_stat_statements;
```

### Check Available Extensions

```sql
SELECT * FROM pg_available_extensions ORDER BY name;
```

---

## Neon CLI Reference

### Installation

```bash
# macOS
brew install neonctl

# npm (Node.js 18+)
npm install -g neonctl

# Without installation
npx neonctl <command>
```

### Authentication

```bash
# Interactive browser auth
neonctl auth

# API key auth
export NEON_API_KEY=your_key
# or
neonctl --api-key your_key <command>
```

### Project Management

```bash
# Create project
neonctl projects create --name my-project

# List projects
neonctl projects list

# Get project details
neonctl projects get --project-id <id>

# Delete project
neonctl projects delete --project-id <id>
```

### Branch Management

```bash
# Create branch
neonctl branches create --name feature-x --project-id <id>

# Create branch from point in time
neonctl branches create --name restore --parent main --timestamp "2024-01-15T10:00:00Z"

# List branches
neonctl branches list --project-id <id>

# Reset branch to parent
neonctl branches reset --name dev --parent main

# Delete branch
neonctl branches delete --name old-branch --project-id <id>

# Compare schemas
neonctl branches schema-diff --base main --compare dev
```

### Database Operations

```bash
# Create database
neonctl databases create --name mydb --branch main --project-id <id>

# List databases
neonctl databases list --branch main --project-id <id>

# Delete database
neonctl databases delete --name mydb --branch main --project-id <id>
```

### Connection String

```bash
# Get connection string
neonctl connection-string --project-id <id> --branch main

# Pooled connection
neonctl connection-string --project-id <id> --branch main --pooled

# Specific database
neonctl connection-string --project-id <id> --database mydb
```

### Role Management

```bash
# Create role
neonctl roles create --name app_user --branch main --project-id <id>

# List roles
neonctl roles list --branch main --project-id <id>
```

---

## Data Migration

### From Existing Postgres

```bash
# Export from source (use direct connection, not pooled)
pg_dump -Fc -v -d "postgresql://user:pass@source-host/dbname" -f backup.dump

# Restore to Neon (use direct connection)
pg_restore -v -d "postgresql://user:pass@ep-xxx.neon.tech/dbname" backup.dump
```

**Important Flags**:
```bash
# Skip ownership (Neon doesn't support ALTER OWNER)
pg_restore -O -v -d <connection> backup.dump

# Skip tablespaces and large objects
pg_dump --no-tablespaces --no-blobs ...
```

### Schema-Only Migration

```bash
# Dump schema only
pg_dump --schema-only -f schema.sql <source_connection>

# Apply schema
psql -f schema.sql <neon_connection>
```

---

## Neon API

### Authentication

```bash
curl -H "Authorization: Bearer $NEON_API_KEY" \
  https://console.neon.tech/api/v2/projects
```

### Common Endpoints

```bash
# List projects
GET /projects

# Create project
POST /projects
{
  "project": {
    "name": "my-project"
  }
}

# Create branch
POST /projects/{project_id}/branches
{
  "branch": {
    "name": "dev",
    "parent_id": "br-xxx"
  }
}

# Get connection URI
GET /projects/{project_id}/connection_uri?branch_id=br-xxx&database_name=neondb

# List endpoints (computes)
GET /projects/{project_id}/endpoints

# Start/Suspend compute
POST /projects/{project_id}/endpoints/{endpoint_id}/start
POST /projects/{project_id}/endpoints/{endpoint_id}/suspend
```

### Rate Limits

- **700 requests/minute** (11/second average)
- **Bursts up to 40 requests/second** per route
- HTTP 429 when exceeded

---

## Pricing Quick Reference

### Plans Overview

| Plan | Compute | Storage | Best For |
|------|---------|---------|----------|
| **Free** | 100 CU-hr/mo | 0.5 GB | Prototypes |
| **Launch** | $0.106/CU-hr | $0.35/GB-mo | Startups |
| **Scale** | $0.222/CU-hr | $0.35/GB-mo | Production |

### Free Tier Limits

- 100 compute hours/month
- 0.5 GB storage
- 10 branches per project
- 5 minute scale-to-zero (fixed)
- Up to 2 CU autoscaling

### Cost Optimization

```bash
# 1. Use scale-to-zero for dev/test branches
# 2. Set appropriate autoscaling limits
# 3. Use pooled connections to reduce compute time
# 4. Delete unused branches
# 5. Monitor usage in Neon Console
```

---

## Common Patterns

### Connection Pool Setup

```typescript
// Singleton pattern for serverless
import { Pool, neonConfig } from '@neondatabase/serverless';
import ws from 'ws';

neonConfig.webSocketConstructor = ws;

let pool: Pool | null = null;

export function getPool() {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 10,
    });
  }
  return pool;
}
```

### Retry Logic for Cold Starts

```typescript
import { neon } from '@neondatabase/serverless';
import retry from 'async-retry';

const sql = neon(process.env.DATABASE_URL!);

async function queryWithRetry<T>(query: Promise<T>): Promise<T> {
  return retry(
    async () => query,
    {
      retries: 3,
      minTimeout: 1000,
      maxTimeout: 5000,
    }
  );
}

// Usage
const users = await queryWithRetry(sql`SELECT * FROM users`);
```

### Environment-Based Branching

```typescript
// middleware.ts or config
function getDatabaseUrl() {
  const env = process.env.VERCEL_ENV || 'development';

  switch (env) {
    case 'production':
      return process.env.DATABASE_URL_PRODUCTION;
    case 'preview':
      return process.env.DATABASE_URL_PREVIEW;  // Auto-set by Vercel integration
    default:
      return process.env.DATABASE_URL_DEV;
  }
}
```

---

## Troubleshooting

### Connection Issues

**Problem**: Connection timeout on cold start
```typescript
// Solution: Increase connect_timeout
const url = process.env.DATABASE_URL + '&connect_timeout=15';
```

**Problem**: Too many connections
```typescript
// Solution: Use pooled connection string
// Change: ep-xxx.neon.tech
// To:     ep-xxx-pooler.neon.tech
```

**Problem**: SSL connection required
```typescript
// Solution: Ensure sslmode in connection string
const url = '...?sslmode=require&channel_binding=require';
```

### Migration Issues

**Problem**: `pg_dump` fails with pooled connection
```bash
# Solution: Use direct (unpooled) connection for pg_dump/pg_restore
# Remove -pooler from hostname
```

**Problem**: Permission denied on restore
```bash
# Solution: Use -O flag to skip ownership
pg_restore -O -d <connection> backup.dump
```

### Performance Issues

**Problem**: Slow queries after scale-to-zero
```
# Cause: Cold start ~500ms
# Solution:
# 1. Disable scale-to-zero for production
# 2. Use connection pooling
# 3. Implement retry logic
```

**Problem**: High memory usage
```sql
-- Check and optimize queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Consider increasing CU or optimizing queries
```

---

## Best Practices Summary

1. **Use pooled connections** for applications (`-pooler` hostname)
2. **Use direct connections** for migrations and `pg_dump`
3. **Set `connect_timeout`** to handle cold starts (10-15s)
4. **Use HTTP driver** for serverless/edge functions
5. **Create branches** for dev/test (they're free when idle)
6. **Monitor compute hours** on free tier
7. **Enable scale-to-zero** for non-production branches
8. **Use environment variables** for connection strings
9. **Implement retry logic** for transient failures
10. **Delete unused branches** to reduce clutter

---

## Related Skills

- **prisma** - ORM with Neon adapter support
- **drizzle** - Type-safe ORM for Neon
- **vercel** - Seamless Neon integration
- **nextjs** - Server Components with Neon
- **pgvector** - Vector similarity search
- **cloudflare-workers** - Edge runtime with Neon HTTP driver
