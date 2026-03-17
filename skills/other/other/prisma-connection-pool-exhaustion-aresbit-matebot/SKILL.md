---
name: prisma-connection-pool-exhaustion
description: |
  Fix Prisma "Too many connections" and connection pool exhaustion errors in 
  serverless environments (Vercel, AWS Lambda, Netlify). Use when: (1) Error 
  "P2024: Timed out fetching a new connection from the pool", (2) PostgreSQL 
  "too many connections for role", (3) Database works locally but fails in 
  production serverless, (4) Intermittent database timeouts under load.
author: Claude Code
version: 1.0.0
date: 2024-02-20
---

# Prisma Connection Pool Exhaustion in Serverless

## Problem

Serverless functions create a new Prisma client instance on each cold start. Each 
instance opens multiple database connections (default: 5 per instance). With many 
concurrent requests, this quickly exhausts the database's connection limit (often 
20-100 for managed databases).

## Context / Trigger Conditions

This skill applies when you see:

- `P2024: Timed out fetching a new connection from the connection pool`
- PostgreSQL: `FATAL: too many connections for role "username"`
- MySQL: `Too many connections`
- Works fine locally with `npm run dev` but fails in production
- Errors appear during traffic spikes, then resolve
- Database dashboard shows connections at or near limit

Environment indicators:
- Deploying to Vercel, AWS Lambda, Netlify Functions, or similar
- Using Prisma with PostgreSQL, MySQL, or another connection-based database
- Database is managed (PlanetScale, Supabase, Neon, RDS, etc.)

## Solution

### Step 1: Use Connection Pooling Service

The recommended solution is to use a connection pooler like PgBouncer or Prisma 
Accelerate, which sits between your serverless functions and the database.

**For Supabase:**
```
# .env
# Use the pooled connection string (port 6543, not 5432)
DATABASE_URL="postgresql://user:pass@db.xxx.supabase.co:6543/postgres?pgbouncer=true"
```

**For Neon:**
```
# .env  
DATABASE_URL="postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require"
# Neon has built-in pooling
```

**For Prisma Accelerate:**
```bash
npx prisma generate --accelerate
```

### Step 2: Configure Prisma Connection Limits

In your `schema.prisma`:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Limit connections per Prisma instance
  relationMode = "prisma"
}
```

In your connection URL or Prisma client:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma = globalForPrisma.prisma || new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?connection_limit=1'
    }
  }
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

### Step 3: Singleton Pattern (Development)

Prevent hot-reload from creating new clients:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

### Step 4: URL Parameters

Add these to your connection string:

```
?connection_limit=1&pool_timeout=20&connect_timeout=10
```

- `connection_limit=1`: One connection per serverless instance
- `pool_timeout=20`: Wait up to 20s for available connection
- `connect_timeout=10`: Fail fast if can't connect in 10s

## Verification

After applying fixes:

1. Deploy to production
2. Run a load test: `npx autocannon -c 100 -d 30 https://your-app.com/api/test`
3. Check database dashboard—connections should stay within limits
4. No more P2024 errors in logs

## Example

**Before** (error under load):
```
[ERROR] PrismaClientKnownRequestError:
Invalid `prisma.user.findMany()` invocation:
Timed out fetching a new connection from the connection pool.
```

**After** (with connection pooling):
```
# Using Supabase pooler URL
DATABASE_URL="postgresql://...@db.xxx.supabase.co:6543/postgres?pgbouncer=true&connection_limit=1"
```

Database connections stable at 10-15 even under heavy load.

## Notes

- Different managed databases have different pooling solutions—check your provider's docs
- PlanetScale (MySQL) uses a different architecture and doesn't have this issue
- `connection_limit=1` is aggressive; start there and increase if you see latency
- The singleton pattern only helps in development; in production serverless, each 
  instance is isolated
- If using Prisma with Next.js API routes, each route invocation may be a separate 
  serverless function
- Consider Prisma Accelerate for built-in caching + pooling: https://www.prisma.io/accelerate
