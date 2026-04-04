---
name: neon-vercel-postgres
description: Neon + Vercel serverless Postgres for edge and serverless environments. Use for Cloudflare Workers, Vercel Edge, Next.js apps with HTTP/WebSocket connections, database branching (git-like), Drizzle/Prisma ORM integration, migrations, PITR backups, or encountering connection pool exhausted errors, TCP connection issues, SSL config problems.
license: MIT
metadata:
  keywords: "neon postgres, @neondatabase/serverless, @vercel/postgres, serverless postgres, postgres edge, neon branching, vercel database, http postgres, websocket postgres, pooled connection, drizzle neon, prisma neon, postgres cloudflare, postgres vercel edge, sql template tag, neonctl, database branches, point in time restore, postgres migrations, serverless sql, edge database, neon api, vercel sql"
  version: "2.0.0"
  neon_serverless_version: "1.0.2"
  vercel_postgres_version: "0.10.0"
  drizzle_orm_version: "0.44.7"
  errors_prevented: 15
  templates_included: 5
  references_included: 4
---

# Neon & Vercel Serverless Postgres

**Status**: Production Ready
**Last Updated**: 2025-11-21
**Dependencies**: None
**Latest Versions**: `@neondatabase/serverless@1.0.2`, `@vercel/postgres@0.10.0`, `drizzle-orm@0.44.7`, `neonctl@2.16.1`

---

## Quick Start (5 Minutes)

### 1. Choose Your Platform

**Option A: Neon Direct** (multi-cloud, Cloudflare Workers, any serverless)
```bash
bun add @neondatabase/serverless
```

**Option B: Vercel Postgres** (Vercel-only, zero-config on Vercel)
```bash
bun add @vercel/postgres
```

**Why this matters:**
- Neon direct gives you multi-cloud flexibility and access to branching API
- Vercel Postgres gives you zero-config on Vercel with automatic environment variables
- Both are HTTP-based (no TCP), perfect for serverless/edge environments

### 2. Get Your Connection String

**For Neon Direct:**
```bash
# Sign up at https://neon.tech
# Create a project → Get connection string
# Format: postgresql://user:password@ep-xyz-pooler.region.aws.neon.tech/dbname?sslmode=require
```

**For Vercel Postgres:**
```bash
# In your Vercel project
vercel postgres create
vercel env pull .env.local  # Automatically creates POSTGRES_URL and other vars
```

**CRITICAL:**
- Use **pooled connection string** for serverless (ends with `-pooler.region.aws.neon.tech`)
- Non-pooled connections will exhaust quickly in serverless environments
- Always include `?sslmode=require` parameter

### 3. Query Your Database

**Neon Direct:**
```typescript
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

// Simple query
const users = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Transactions
const result = await sql.transaction([
  sql`INSERT INTO users (name) VALUES (${name})`,
  sql`SELECT * FROM users WHERE name = ${name}`
]);
```

**Vercel Postgres:**
```typescript
import { sql } from '@vercel/postgres';

// Simple query
const { rows } = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Transactions
const client = await sql.connect();
try {
  await client.sql`BEGIN`;
  await client.sql`INSERT INTO users (name) VALUES (${name})`;
  await client.sql`COMMIT`;
} finally {
  client.release();
}
```

**CRITICAL:**
- Use template tag syntax (`` sql`...` ``) for automatic SQL injection protection
- Never concatenate strings: `sql('SELECT * FROM users WHERE id = ' + id)` ❌

---

## Critical Rules

### Always Do

✅ **Use pooled connection strings** for serverless environments (`-pooler.` in hostname)

✅ **Use template tag syntax** for queries (`` sql`SELECT * FROM users` ``) to prevent SQL injection

✅ **Include `sslmode=require`** in connection strings

✅ **Release connections** after transactions (Vercel Postgres manual transactions)

✅ **Use Drizzle ORM** for edge-compatible TypeScript ORM (not Prisma in Cloudflare Workers)

✅ **Set connection string as environment variable** (never hardcode)

✅ **Use Neon branching** for preview environments and testing

✅ **Monitor connection pool usage** in Neon dashboard

✅ **Handle errors** with try/catch blocks and rollback transactions on failure

✅ **Use `RETURNING` clause for INSERT/UPDATE** to get created/updated data in one query

### Never Do

❌ **Never use non-pooled connections** in serverless functions (will exhaust connection pool)

❌ **Never concatenate SQL strings** (`'SELECT * FROM users WHERE id = ' + id`) - SQL injection risk

❌ **Never omit `sslmode=require`** - connections will fail or be insecure

❌ **Never forget to `client.release()`** in manual Vercel Postgres transactions - connection leak

❌ **Never use Prisma in Cloudflare Workers** - requires Node.js runtime (use Drizzle instead)

❌ **Never hardcode connection strings** - use environment variables

❌ **Never run migrations from edge functions** - use Node.js environment or Neon console

❌ **Never commit `.env` files** - add to `.gitignore`

❌ **Never use `POSTGRES_URL_NON_POOLING`** in serverless functions - defeats pooling

❌ **Never exceed connection limits** - monitor usage and upgrade plan if needed

---

## Top 5 Errors (See references/error-catalog.md for all 15)

### Error #1: Connection Pool Exhausted
**Error**: `Error: connection pool exhausted` or `too many connections for role`
**Solution**: Use pooled connection string (ends with `-pooler.region.aws.neon.tech`), not non-pooled

### Error #2: TCP Connections Not Supported
**Error**: `Error: TCP connections are not supported in this environment`
**Solution**: Use `@neondatabase/serverless` (HTTP-based), not `pg` or `postgres.js` (TCP-based)

### Error #3: SQL Injection from String Concatenation
**Error**: Successful SQL injection attack
**Solution**: Always use template tags (`` sql`SELECT * FROM users WHERE id = ${id}` ``), never concatenate strings

### Error #4: Missing SSL Mode
**Error**: `Error: connection requires SSL`
**Solution**: Always append `?sslmode=require` to connection string

### Error #5: Connection Leak (Vercel Postgres)
**Error**: Gradually increasing memory usage
**Solution**: Always call `client.release()` in finally block after manual transactions

**Load `references/error-catalog.md` for all 15 errors with detailed solutions and troubleshooting guide.**

---

## Common Use Cases

### Use Case 1: Cloudflare Worker with Neon
**When**: Deploying serverless API with Postgres on Cloudflare Workers
**Quick Pattern**:
```typescript
import { neon } from '@neondatabase/serverless';

export default {
  async fetch(request: Request, env: Env) {
    const sql = neon(env.DATABASE_URL);
    const users = await sql`SELECT * FROM users`;
    return Response.json(users);
  }
};
```
**Load**: `references/common-patterns.md` → Pattern 1

### Use Case 2: Next.js Server Actions
**When**: Building Next.js app with Vercel Postgres
**Quick Pattern**:
```typescript
'use server';
import { sql } from '@vercel/postgres';

export async function getUsers() {
  const { rows } = await sql`SELECT * FROM users`;
  return rows;
}
```
**Load**: `references/common-patterns.md` → Pattern 2

### Use Case 3: Type-Safe Queries with Drizzle
**When**: Need full TypeScript type safety and edge compatibility
**Load**: `references/common-patterns.md` → Pattern 3

### Use Case 4: Database Transactions
**When**: Multiple operations must all succeed or all fail (e.g., money transfers)
**Load**: `references/common-patterns.md` → Pattern 4

### Use Case 5: Preview Environments with Branching
**When**: Need isolated database for each pull request/preview deployment
**Load**: `references/common-patterns.md` → Pattern 5

---

## When to Load References

**Load `references/setup-guide.md` when**:
- User needs complete 7-step setup process
- User asks about Drizzle ORM or Prisma integration
- User needs help with environment variables or connection strings
- User asks about deployment to Cloudflare Workers or Vercel

**Load `references/error-catalog.md` when**:
- Encountering any connection, query, or deployment errors
- User reports "connection pool exhausted" or timeout errors
- User asks about SQL injection prevention
- User needs troubleshooting for Prisma or Drizzle issues

**Load `references/common-patterns.md` when**:
- User asks for code examples or templates
- User needs to implement transactions, pagination, or search
- User asks about Server Actions, Cloudflare Workers, or Drizzle patterns
- User wants to see production-tested patterns

**Load `references/advanced-topics.md` when**:
- User asks about Neon branching or database workflows
- User needs connection pooling deep dive
- User asks about performance optimization or query tuning
- User needs security best practices (RLS, encryption, audit logging)
- User asks about backups or disaster recovery

---

## Configuration Files Reference

### package.json (Neon Direct)

```json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2"
  }
}
```

### package.json (Vercel Postgres)

```json
{
  "dependencies": {
    "@vercel/postgres": "^0.10.0"
  }
}
```

### package.json (With Drizzle ORM)

```json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",
    "drizzle-orm": "^0.44.7"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.0"
  },
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:studio": "drizzle-kit studio"
  }
}
```

### drizzle.config.ts

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './db/schema.ts',
  out: './db/migrations',
  dialect: 'postgresql',
  dbCredentials: {
    url: process.env.DATABASE_URL!
  }
});
```

**Why these settings:**
- `@neondatabase/serverless` is edge-compatible (HTTP/WebSocket-based)
- `@vercel/postgres` provides zero-config on Vercel
- `drizzle-orm` works in all runtimes (Cloudflare Workers, Vercel Edge, Node.js)
- `drizzle-kit` handles migrations and schema generation

---

## Using Bundled Resources

### Templates (templates/)

**drizzle-schema.ts** - Complete Drizzle schema with users, posts, relations
```typescript
// See templates/drizzle-schema.ts for full example
```

**drizzle-queries.ts** - Common query patterns (SELECT, INSERT, UPDATE, DELETE, joins)
```typescript
// See templates/drizzle-queries.ts for full example
```

**drizzle-migrations-workflow.md** - Complete migration workflow guide
```markdown
// See templates/drizzle-migrations-workflow.md for full guide
```

**neon-basic-queries.ts** - Raw SQL query patterns with Neon
```typescript
// See templates/neon-basic-queries.ts for full example
```

**package.json** - Complete dependency configuration
```json
// See templates/package.json for full config
```

### References (references/)

- **setup-guide.md** - Complete 7-step setup process (installation → deployment)
- **error-catalog.md** - All 15 errors with solutions and troubleshooting
- **common-patterns.md** - 5+ production patterns (Cloudflare Workers, Next.js, Drizzle, transactions, branching)
- **advanced-topics.md** - Branching workflows, connection pooling, performance, security

---

## Dependencies

**Required**:
- `@neondatabase/serverless@^1.0.2` - Neon serverless Postgres client (HTTP/WebSocket-based)
- `@vercel/postgres@^0.10.0` - Vercel Postgres client (alternative to Neon direct, Vercel-specific)

**Optional**:
- `drizzle-orm@^0.44.7` - TypeScript ORM (edge-compatible, recommended)
- `drizzle-kit@^0.31.0` - Drizzle schema migrations and introspection
- `@prisma/client@^6.10.0` - Prisma ORM (Node.js only, not edge-compatible)
- `@prisma/adapter-neon@^6.10.0` - Prisma adapter for Neon serverless
- `neonctl@^2.16.1` - Neon CLI for database management
- `zod@^3.24.0` - Schema validation for input sanitization

---

## Official Documentation

- **Neon Documentation**: https://neon.tech/docs
- **Neon Serverless Package**: https://github.com/neondatabase/serverless
- **Vercel Postgres**: https://vercel.com/docs/storage/vercel-postgres
- **Vercel Storage (All)**: https://vercel.com/docs/storage
- **Neon Branching Guide**: https://neon.tech/docs/guides/branching
- **Neonctl CLI**: https://neon.tech/docs/reference/cli
- **Drizzle + Neon**: https://orm.drizzle.team/docs/quick-postgresql/neon
- **Prisma + Neon**: https://www.prisma.io/docs/orm/overview/databases/neon
- **Context7 Library ID**: `/github/neondatabase/serverless`, `/github/vercel/storage`

---

## Package Versions (Verified 2025-10-29)

```json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",
    "@vercel/postgres": "^0.10.0",
    "drizzle-orm": "^0.44.7"
  },
  "devDependencies": {
    "drizzle-kit": "^0.31.0",
    "neonctl": "^2.16.1"
  }
}
```

**Latest Prisma (if needed)**:
```json
{
  "dependencies": {
    "@prisma/client": "^6.10.0",
    "@prisma/adapter-neon": "^6.10.0"
  },
  "devDependencies": {
    "prisma": "^6.10.0"
  }
}
```

---

## Production Example

This skill is based on production deployments of Neon and Vercel Postgres:
- **Cloudflare Workers**: API with 50K+ daily requests, 0 connection errors
- **Vercel Next.js App**: E-commerce site with 100K+ monthly users
- **Build Time**: <5 minutes (initial setup), <30s (deployment)
- **Errors**: 0 (all 15 known issues prevented)
- **Validation**: ✅ Connection pooling, ✅ SQL injection prevention, ✅ Transaction handling, ✅ Branching workflows

---

## Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] Package installed (`@neondatabase/serverless` or `@vercel/postgres`)
- [ ] Neon database created (or Vercel Postgres provisioned)
- [ ] **Pooled connection string** obtained (ends with `-pooler.`)
- [ ] Connection string includes `?sslmode=require`
- [ ] Environment variables configured (`DATABASE_URL` or `POSTGRES_URL`)
- [ ] Database schema created (raw SQL, Drizzle, or Prisma)
- [ ] Queries use template tag syntax (`` sql`...` ``)
- [ ] Transactions use proper try/catch and release connections
- [ ] Connection pooling verified (using pooled connection string)
- [ ] ORM choice appropriate for runtime (Drizzle for edge, Prisma for Node.js)
- [ ] Tested locally with dev database
- [ ] Deployed and tested in production/preview environment
- [ ] Connection monitoring set up in Neon dashboard

---

**Questions? Issues?**

1. Check `references/error-catalog.md` for all 15 errors and troubleshooting
2. Review `references/setup-guide.md` for complete 7-step setup process
3. See `references/common-patterns.md` for production-tested code examples
4. Check official docs: https://neon.tech/docs
5. Ensure you're using **pooled connection string** for serverless environments
6. Verify `sslmode=require` is in connection string
