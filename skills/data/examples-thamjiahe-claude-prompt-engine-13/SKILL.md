---
name: "Neon Serverless PostgreSQL"
description: "Configure serverless PostgreSQL databases on Neon with connection pooling, branching, and Edge Function integration. Apply when setting up serverless databases, connecting from Edge Functions, or managing database branches."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Neon Serverless PostgreSQL

Systematic Neon database setup for serverless applications with cost optimization and performance.

## Overview

This Skill enforces:
- Serverless PostgreSQL setup
- Connection pooling and HTTP connection mode
- Database branching for development
- Environment variable configuration
- Edge Function integration (Vercel, Netlify, Cloudflare)
- Zero-downtime deployments
- Autoscaling configuration

Apply when setting up serverless databases, connecting from Edge Functions, or managing environments.

## Neon Workflow

**Every Neon setup follows this process**:

```
Step 1: Create Neon project
  ↓
Step 2: Get connection string
  ↓
Step 3: Set up database branches
  ↓
Step 4: Configure for environment
  ↓
Step 5: Connect from application
  ↓
Step 6: Set up autoscaling
```

## Step 1: Create Neon Project

### Sign Up and Create Project

1. Visit https://neon.tech
2. Sign up with GitHub or email
3. Click "Create Project"
4. Choose region (closest to your users)
5. Select PostgreSQL version (14, 15, 16)

### Get Connection Details

Connection string format:

```
postgresql://[user]:[password]@[host].neon.tech/[dbname]?sslmode=require
```

## Step 2: Connection Modes

### Pooler Connection (Recommended for Edge Functions)

```
postgresql://[user]:[password]@[host]-pooler.neon.tech/[dbname]?sslmode=require
```

**Why pooler for Edge Functions**:
- Connection pooling (many connections share few TCP connections)
- Optimized for serverless (many short-lived connections)
- Lower latency
- Cost-effective

### Regular Connection (For long-lived connections)

```
postgresql://[user]:[password]@[host].neon.tech/[dbname]?sslmode=require
```

## Step 3: Environment Configuration

### Local Development

Create `.env.local`:

```bash
DATABASE_URL="postgresql://[user]:[password]@[host]-pooler.neon.tech/[dbname]?sslmode=require"
```

Add to `.gitignore`:

```
.env.local
.env.*.local
```

### Vercel Environment Variables

Set in Vercel dashboard → Settings → Environment Variables:

```
DATABASE_URL (for all environments: Development, Preview, Production)
```

### GitHub Secrets (for CI/CD)

```
DATABASE_URL
NEON_API_KEY
```

## Step 4: Database Branching

### Create Development Branch

```bash
# Using Neon CLI
neon branches create --name development

# Get development database connection string
neon connection-string development
```

### Git-like Branching Workflow

```
main (production database)
  ↓
development (feature development)
  ↓
feature-x (isolated testing)
```

**Benefits**:
- Data isolation between environments
- Test migrations safely
- Reset databases quickly
- PR previews with separate databases

### Manage Branches

```bash
# List all branches
neon branches list

# Create branch from main
neon branches create --name staging --parent main

# Delete branch
neon branches delete development

# Reset branch to main state
neon branches delete feature-x
neon branches create --name feature-x --parent main
```

## Step 5: Connection Strategies

### For Next.js API Routes (Server-side)

```ts
// lib/db.ts
import { Pool } from '@neondatabase/serverless';
import ws from 'ws';

// Set WebSocket constructor for Node.js < 21
if (typeof global !== 'undefined' && !global.WebSocket) {
  global.WebSocket = ws as any;
}

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export async function query(sql: string, params: unknown[] = []) {
  const client = await pool.connect();
  try {
    return await client.query(sql, params);
  } finally {
    client.release();
  }
}
```

### For Vercel Edge Functions

```ts
// api/edge-query.ts
import { neon } from '@neondatabase/serverless';

export const config = {
  runtime: 'edge',
  regions: ['iad1']  // Closest to Neon
};

export default async (req: Request) => {
  const sql = neon(process.env.DATABASE_URL!);

  const [user] = await sql`SELECT * FROM users WHERE id = ${123}`;

  return new Response(JSON.stringify(user), {
    headers: { 'content-type': 'application/json' }
  });
};
```

### For Netlify Functions

```ts
// netlify/functions/query.ts
import { neon } from '@neondatabase/serverless';

export default async (event: any) => {
  const sql = neon(process.env.DATABASE_URL!);

  const users = await sql`SELECT * FROM users LIMIT 10`;

  return {
    statusCode: 200,
    body: JSON.stringify(users)
  };
};
```

### For Cloudflare Workers

```ts
// src/index.ts
import { neon } from '@neondatabase/serverless';

export default {
  async fetch(request: Request, env: any) {
    const sql = neon(env.DATABASE_URL);

    const [post] = await sql`SELECT * FROM posts WHERE id = ${1}`;

    return new Response(JSON.stringify(post), {
      headers: { 'content-type': 'application/json' }
    });
  }
};
```

## Step 6: Autoscaling Configuration

### Set Compute Auto-Suspend

Neon automatically pauses compute when unused (saves costs):

```
Settings → Compute Options
- Auto-suspend: 5 minutes (default)
- Auto-suspend delay: Can be customized
```

### Set Connection Pooling Limits

```
Settings → Pooler Settings
- Pool size: 10-100 connections
- Connection timeout: 30s
```

## Step 7: Database Operations

### Create Tables

```sql
-- Using Neon SQL Editor or psql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Query from Node.js

```ts
import { neon } from '@neondatabase/serverless';

const sql = neon(process.env.DATABASE_URL!);

// Single row query
const [user] = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Multiple rows
const users = await sql`SELECT * FROM users LIMIT 10`;

// Insert
const [newUser] = await sql`
  INSERT INTO users (email, name) 
  VALUES (${email}, ${name})
  RETURNING *
`;

// Update
const [updated] = await sql`
  UPDATE users 
  SET name = ${name} 
  WHERE id = ${userId}
  RETURNING *
`;

// Delete
await sql`DELETE FROM users WHERE id = ${userId}`;
```

## Anti-Patterns

```ts
// ❌ BAD: Creating Pool outside request handler
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export async function GET(req: Request) {
  const client = await pool.connect();  // Reuses connections
  // ...
}

// ✅ GOOD: Create Pool inside request handler
export async function GET(req: Request) {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const client = await pool.connect();
  try {
    // Query
  } finally {
    await client.release();
    await pool.end();
  }
}

// ❌ BAD: Connection string in code
const sql = neon('postgresql://user:password@host/db');

// ✅ GOOD: Use environment variable
const sql = neon(process.env.DATABASE_URL!);

// ❌ BAD: Forgetting to close connections
const client = await pool.connect();
const result = await client.query('SELECT * FROM users');
// No release!

// ✅ GOOD: Always release connection
const client = await pool.connect();
try {
  const result = await client.query('SELECT * FROM users');
} finally {
  client.release();
}
```

## Connection Troubleshooting

### Connection Timeout

```bash
# Issue: Taking too long to connect
# Solution: Use pooler connection instead of direct connection
# Change: host.neon.tech → host-pooler.neon.tech
```

### SSL Certificate Error

```bash
# Issue: SSL certificate validation failed
# Solution: Add sslmode=require to connection string
DATABASE_URL="postgresql://...?sslmode=require"
```

### Too Many Connections

```bash
# Issue: Error: too many connections
# Solution: Enable connection pooling or increase pool size
```

## Backup and Recovery

### Automatic Backups

Neon automatically backs up every transaction. Access via:

1. Neon console → Branches → branch name
2. Under "Backups" section
3. Restore from point-in-time

### Manual Export

```bash
# Export data
pg_dump postgres://user:password@host/db > backup.sql

# Restore data
psql postgres://user:password@host/db < backup.sql
```

## Verification Before Production

- [ ] Connection string configured in environment variables
- [ ] Pooler connection used for Edge Functions
- [ ] Database branches set up (main, development, staging)
- [ ] Connection pooling enabled
- [ ] Autoscaling configured
- [ ] Secrets not hardcoded
- [ ] SSL mode enabled (sslmode=require)
- [ ] Backups tested
- [ ] Read replicas configured (if needed)
- [ ] Monitoring alerts set up

## Common Operations

```bash
# Get connection string
neon connection-string

# List databases
neon databases list

# Get branch list
neon branches list

# Create backup
pg_dump $DATABASE_URL > backup.sql

# Restore from backup
psql $DATABASE_URL < backup.sql

# Reset branch (delete all data)
neon branches delete branch-name
neon branches create --name branch-name --parent main
```

## Integration with Project Standards

Enforces database best practices:
- D-1: Database models defined
- D-2: Validation at API and DB layers
- S-5: Environment variables for secrets
- No hardcoded credentials
- Connection pooling for efficiency

## Resources

- Neon Documentation: https://neon.tech/docs
- Serverless Driver: https://github.com/neondatabase/serverless
- Connection Pooling: https://neon.tech/docs/connect/connection-pooling
- Branching: https://neon.tech/docs/guide/branch
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
