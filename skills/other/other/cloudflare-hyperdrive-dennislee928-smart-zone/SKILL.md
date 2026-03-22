---
name: cloudflare-hyperdrive
description: |
  Connect Workers to PostgreSQL/MySQL with Hyperdrive's global pooling and caching. Use when: connecting to existing databases, setting up connection pools, using node-postgres/mysql2, integrating Drizzle/Prisma, or troubleshooting pool acquisition failures, TLS errors, or nodejs_compat missing. Prevents 11 documented errors.
user-invocable: true
---

# Cloudflare Hyperdrive

**Status**: Production Ready ✅
**Last Updated**: 2026-01-09
**Dependencies**: cloudflare-worker-base (recommended for Worker setup)
**Latest Versions**: wrangler@4.58.0, pg@8.16.3+ (minimum), postgres@3.4.8, mysql2@3.16.0

**Recent Updates (2025)**:
- **July 2025**: Configurable connection counts (min 5, max ~20 Free/~100 Paid)
- **May 2025**: 5x faster cache hits (regional prepared statement caching), FedRAMP Moderate authorization
- **April 2025**: Free plan availability (10 configs), MySQL GA support
- **March 2025**: 90% latency reduction (pools near database), IP access control (standard CF IP ranges)
- **nodejs_compat_v2**: pg driver no longer requires node_compat mode (auto-enabled with compatibility_date 2024-09-23+)
- **Limits**: 25 Hyperdrive configurations per account (Paid), 10 per account (Free)

---

## Quick Start (5 Minutes)

### 1. Create Hyperdrive Configuration

```bash
# For PostgreSQL
npx wrangler hyperdrive create my-postgres-db \
  --connection-string="postgres://user:password@db-host.cloud:5432/database"

# For MySQL
npx wrangler hyperdrive create my-mysql-db \
  --connection-string="mysql://user:password@db-host.cloud:3306/database"

# Output:
# ✅ Successfully created Hyperdrive configuration
#
# [[hyperdrive]]
# binding = "HYPERDRIVE"
# id = "a76a99bc-7901-48c9-9c15-c4b11b559606"
```

**Save the `id` value** - you'll need it in the next step!

---

### 2. Configure Bindings in wrangler.jsonc

Add to your `wrangler.jsonc`:

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-09-23",
  "compatibility_flags": ["nodejs_compat"],  // REQUIRED for database drivers
  "hyperdrive": [
    {
      "binding": "HYPERDRIVE",                     // Available as env.HYPERDRIVE
      "id": "a76a99bc-7901-48c9-9c15-c4b11b559606"  // From wrangler hyperdrive create
    }
  ]
}
```

**CRITICAL:**
- `nodejs_compat` flag is **REQUIRED** for all database drivers
- `binding` is how you access Hyperdrive in code (`env.HYPERDRIVE`)
- `id` is the Hyperdrive configuration ID (NOT your database ID)

---

### 3. Install Database Driver

```bash
# For PostgreSQL (choose one)
npm install pg           # node-postgres (most common)
npm install postgres     # postgres.js (modern, minimum v3.4.5)

# For MySQL
npm install mysql2       # mysql2 (minimum v3.13.0)
```

---

### 4. Query Your Database

**PostgreSQL with node-postgres (pg):**
```typescript
import { Client } from "pg";

type Bindings = {
  HYPERDRIVE: Hyperdrive;
};

export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const client = new Client({
      connectionString: env.HYPERDRIVE.connectionString
    });

    await client.connect();

    try {
      const result = await client.query('SELECT * FROM users LIMIT 10');
      return Response.json({ users: result.rows });
    } finally {
      // Clean up connection AFTER response is sent
      ctx.waitUntil(client.end());
    }
  }
};
```

**MySQL with mysql2:**
```typescript
import { createConnection } from "mysql2/promise";

export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const connection = await createConnection({
      host: env.HYPERDRIVE.host,
      user: env.HYPERDRIVE.user,
      password: env.HYPERDRIVE.password,
      database: env.HYPERDRIVE.database,
      port: env.HYPERDRIVE.port,
      disableEval: true  // REQUIRED for Workers (eval() not supported)
    });

    try {
      const [rows] = await connection.query('SELECT * FROM users LIMIT 10');
      return Response.json({ users: rows });
    } finally {
      ctx.waitUntil(connection.end());
    }
  }
};
```

---

### 5. Deploy

```bash
npx wrangler deploy
```

**That's it!** Your Worker now connects to your existing database via Hyperdrive with:
- ✅ Global connection pooling
- ✅ Automatic query caching
- ✅ Reduced latency (eliminates 7 round trips)

---

## Known Issues Prevention

This skill prevents **11** documented issues with sources and solutions.

### Issue #1: Windows/macOS Local Development - Hostname Resolution Failure

**Error**: Connection fails with hostname like `xxx.hyperdrive.local`
**Source**: [GitHub Issue #11556](https://github.com/cloudflare/workers-sdk/issues/11556)
**Platforms**: Windows, macOS 26 Tahoe, Ubuntu 24.04 LTS (wrangler@4.54.0+)
**Why It Happens**: Hyperdrive local proxy hostname fails to resolve on certain platforms
**Prevention**:

Use environment variable for local development:
```bash
export CLOUDFLARE_HYPERDRIVE_LOCAL_CONNECTION_STRING_HYPERDRIVE="postgres://user:password@localhost:5432/db"
npx wrangler dev
```

Or use `wrangler dev --remote` (caution: uses production database)

**Status**: Open issue, workaround available

---

### Issue #2: postgres.js Hangs with IP Addresses

**Error**: Connection hangs indefinitely with no error message
**Source**: [GitHub Issue #6179](https://github.com/cloudflare/workers-sdk/issues/6179)
**Why It Happens**: Using IP address instead of hostname in connection string causes postgres.js to hang
**Prevention**:

```typescript
// ❌ WRONG - IP address causes indefinite hang
const connection = "postgres://user:password@192.168.1.100:5432/db"

// ✅ CORRECT - Use hostname
const connection = "postgres://user:password@db.example.com:5432/db"
```

**Additional Gotcha**: Miniflare (local dev) only supports A-z0-9 characters in passwords, despite Postgres allowing special characters. Use simple passwords for local development.

---

### Issue #3: MySQL 8.0.43 Authentication Plugin Not Supported

**Error**: "unsupported authentication method"
**Source**: [GitHub Issue #10617](https://github.com/cloudflare/workers-sdk/issues/10617)
**Why It Happens**: MySQL 8.0.43+ introduces new authentication method not supported by Hyperdrive
**Prevention**:

Use MySQL 8.0.40 or earlier, or configure user to use supported auth plugin:
```sql
ALTER USER 'username'@'%' IDENTIFIED WITH caching_sha2_password BY 'password';
```

**Supported Auth Plugins**: Only `caching_sha2_password` and `mysql_native_password`
**Status**: Known issue tracked as CFSQL-1392

---

### Issue #4: Local SSL/TLS Not Supported for Remote Databases

**Error**: SSL required but connection fails in local development
**Source**: [GitHub Issue #10124](https://github.com/cloudflare/workers-sdk/issues/10124)
**Why It Happens**: Hyperdrive local mode doesn't support SSL connections to remote databases (e.g., Neon, cloud providers)
**Prevention**:

Use conditional connection in code:
```typescript
const url = env.isLocal ? env.DB_URL : env.HYPERDRIVE.connectionString;
const client = postgres(url, {
  fetch_types: false,
  max: 2,
});
```

**Alternative**: Use `wrangler dev --remote` (⚠️ connects to production database)
**Timeline**: SSL support planned for 2026 (requires workerd/Workers runtime changes, tracked as SQC-645)

---

### Issue #5: Transaction Mode Resets SET Statements Between Queries

**Error**: SET statements don't persist across queries
**Source**: [Cloudflare Hyperdrive Docs - How Hyperdrive Works](https://developers.cloudflare.com/hyperdrive/configuration/how-hyperdrive-works/)
**Why It Happens**: Hyperdrive operates in transaction mode where connections are returned to pool after each transaction and RESET
**Prevention**:

```typescript
// ❌ WRONG - SET won't persist across queries
await client.query('SET search_path TO myschema');
await client.query('SELECT * FROM mytable'); // Uses default search_path!

// ✅ CORRECT - SET within transaction
await client.query('BEGIN');
await client.query('SET search_path TO myschema');
await client.query('SELECT * FROM mytable'); // Now uses myschema
await client.query('COMMIT');
```

**⚠️ WARNING**: Wrapping multiple operations in a single transaction to maintain SET state will affect Hyperdrive's performance and scaling.

---

### Issue #6: Prisma Client Reuse Causes Hangs in Workers (Community-sourced)

**Error**: Worker hangs and times out after first request
**Source**: [GitHub Issue #28193](https://github.com/prisma/prisma/issues/28193)
**Verified**: Multiple users confirmed
**Why It Happens**: Prisma's connection pool attempts to reuse connections across request contexts, violating Workers' I/O isolation
**Prevention**:

```typescript
// ❌ WRONG - Global Prisma client reused across requests
const prisma = new PrismaClient({ adapter });

export default {
  async fetch(request: Request, env: Bindings) {
    // First request: works
    // Subsequent requests: hang indefinitely
    const users = await prisma.user.findMany();
    return Response.json({ users });
  }
};

// ✅ CORRECT - Create new client per request
export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const pool = new Pool({
      connectionString: env.HYPERDRIVE.connectionString,
      max: 5
    });
    const adapter = new PrismaPg(pool);
    const prisma = new PrismaClient({ adapter });

    try {
      const users = await prisma.user.findMany();
      return Response.json({ users });
    } finally {
      ctx.waitUntil(pool.end());
    }
  }
};
```

---

### Issue #7: Neon Serverless Driver Incompatible with Hyperdrive (Community-sourced)

**Error**: Hyperdrive provides no benefit with Neon serverless driver
**Source**: [Neon GitHub Repo](https://github.com/neondatabase/serverless), [Cloudflare Docs](https://developers.cloudflare.com/workers/databases/third-party-integrations/neon/)
**Why It Happens**: Neon's serverless driver uses WebSockets instead of TCP, bypassing Hyperdrive's connection pooling
**Prevention**:

```typescript
// ❌ WRONG - Neon serverless driver bypasses Hyperdrive
import { neon } from '@neondatabase/serverless';
const sql = neon(env.HYPERDRIVE.connectionString);
// This uses WebSockets, not TCP - Hyperdrive doesn't help

// ✅ CORRECT - Use traditional TCP driver with Hyperdrive
import postgres from 'postgres';
const sql = postgres(env.HYPERDRIVE.connectionString, {
  prepare: true,
  max: 5
});
```

**Official Recommendation**: Neon documentation states "On Cloudflare Workers, consider using Cloudflare Hyperdrive instead of this driver"

---

### Issue #8: Supabase - Must Use Direct Connection String, Not Pooled (Community-sourced)

**Error**: Double-pooling causes connection issues
**Source**: [Cloudflare Docs - Supabase](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-database-providers/supabase/)
**Why It Happens**: Using Supabase pooled connection (Supavisor) creates double-pooling; Supavisor doesn't support prepared statements
**Prevention**:

```bash
# ❌ WRONG - Using Supabase pooled connection (Supavisor)
npx wrangler hyperdrive create my-supabase \
  --connection-string="postgres://user:password@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# ✅ CORRECT - Use Supabase direct connection
npx wrangler hyperdrive create my-supabase \
  --connection-string="postgres://user:password@db.projectref.supabase.co:5432/postgres"
```

**Reason**: Hyperdrive provides its own pooling; double-pooling causes issues and breaks caching

---

### Issue #9: Drizzle ORM with Nitro 3 - 95% Failure Rate with useDatabase (Community-sourced)

**Error**: 500 errors approximately 95% of the time
**Source**: [GitHub Issue #3893](https://github.com/nitrojs/nitro/issues/3893)
**Verified**: Reproduced by multiple users
**Why It Happens**: Nitro 3's built-in `useDatabase` (db0/integrations/drizzle) has I/O isolation issues
**Prevention**:

```typescript
// ❌ WRONG - Nitro's useDatabase fails ~95% of the time
import { useDatabase } from 'db0';
import { drizzle } from 'db0/integrations/drizzle';

export default eventHandler(async () => {
  const db = useDatabase();
  const users = await drizzle(db).select().from(usersTable);
  // Fails ~95% of the time with 500 error
});

// ✅ CORRECT - Create Drizzle client directly
import postgres from 'postgres';
import { drizzle } from 'drizzle-orm/postgres-js';

export default eventHandler(async (event) => {
  const sql = postgres(event.context.cloudflare.env.HYPERDRIVE.connectionString, {
    max: 5,
    prepare: true
  });
  const db = drizzle(sql);
  const users = await db.select().from(usersTable);
  event.context.cloudflare.ctx.waitUntil(sql.end());
  return { users };
});
```

**Error Message**: "Cannot perform I/O on behalf of a different request"

---

### Issue #10: postgres.js Version Requirements for Caching (Community-sourced)

**Error**: Prepared statement caching doesn't work properly
**Source**: [Cloudflare Docs](https://developers.cloudflare.com/hyperdrive/examples/connect-to-postgres/postgres-drivers-and-libraries/postgres-js/)
**Why It Happens**: postgres.js versions before 3.4.5 don't support Hyperdrive's prepared statement caching properly
**Prevention**:

```bash
# Minimum version for Hyperdrive compatibility
npm install postgres@3.4.5

# Current recommended version
npm install postgres@3.4.8
```

**Related**: May 2025 prepared statement caching improvements require minimum version 3.4.5

---

### Issue #11: WebSocket-Based Database Drivers Not Compatible

**Error**: Hyperdrive provides no benefit or causes connection issues
**Source**: General pattern from Neon serverless driver issue
**Why It Happens**: Hyperdrive requires TCP connections; WebSocket-based drivers bypass the TCP pooling layer
**Prevention**:

Use traditional TCP-based drivers (pg, postgres.js, mysql2) instead of WebSocket-based drivers.

**Affected Drivers**: Any database driver using WebSockets instead of TCP

---

## How Hyperdrive Works

Hyperdrive eliminates 7 connection round trips (TCP + TLS + auth) by:
- Edge connection setup near Worker (low latency)
- Connection pooling near database (March 2025: 90% latency reduction)
- Query caching at edge (May 2025: 5x faster cache hits)

**Result**: Single-region databases feel globally distributed.

---

## Setup Steps

### Prerequisites

- Cloudflare account with Workers access
- PostgreSQL (v9.0-17.x) or MySQL (v5.7-8.x) database
- Database accessible via public internet (TLS/SSL required) or private network (Cloudflare Tunnel)
- **April 2025**: Available on Free plan (10 configs) and Paid plan (25 configs)

### Connection String Formats

```bash
# PostgreSQL
postgres://user:password@host:5432/database
postgres://user:password@host:5432/database?sslmode=require

# MySQL
mysql://user:password@host:3306/database

# URL-encode special chars: p@ssw$rd → p%40ssw%24rd
```

---

## Connection Patterns

### Single Connection (pg.Client)
```typescript
const client = new Client({ connectionString: env.HYPERDRIVE.connectionString });
await client.connect();
const result = await client.query('SELECT ...');
ctx.waitUntil(client.end());  // CRITICAL: Non-blocking cleanup
```
**Use for**: Simple queries, single query per request

### Connection Pool (pg.Pool)
```typescript
const pool = new Pool({
  connectionString: env.HYPERDRIVE.connectionString,
  max: 5  // CRITICAL: Workers limit is 6 connections (July 2025: configurable ~20 Free, ~100 Paid)
});
const [result1, result2] = await Promise.all([
  pool.query('SELECT ...'),
  pool.query('SELECT ...')
]);
ctx.waitUntil(pool.end());
```
**Use for**: Parallel queries in single request

### Connection Cleanup Rule
**ALWAYS use `ctx.waitUntil(client.end())`** - non-blocking cleanup after response sent
**NEVER use `await client.end()`** - blocks response, adds latency

---

## ORM Integration

### Drizzle ORM
```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const sql = postgres(env.HYPERDRIVE.connectionString, { max: 5 });
const db = drizzle(sql);
const allUsers = await db.select().from(users);
ctx.waitUntil(sql.end());
```

### Prisma ORM

**⚠️ CRITICAL**: Do NOT reuse Prisma client across requests in Workers. Create new client per request.

```typescript
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "@prisma/client";
import { Pool } from "pg";

// ❌ WRONG - Global client causes hangs after first request
const prisma = new PrismaClient({ adapter });

export default {
  async fetch(request: Request, env: Bindings) {
    const users = await prisma.user.findMany(); // Hangs after first request
    return Response.json({ users });
  }
};

// ✅ CORRECT - Per-request client
export default {
  async fetch(request: Request, env: Bindings, ctx: ExecutionContext) {
    const pool = new Pool({ connectionString: env.HYPERDRIVE.connectionString, max: 5 });
    const adapter = new PrismaPg(pool);
    const prisma = new PrismaClient({ adapter });

    try {
      const users = await prisma.user.findMany();
      return Response.json({ users });
    } finally {
      ctx.waitUntil(pool.end());
    }
  }
};
```

**Why**: Prisma's connection pool attempts to reuse connections across request contexts, violating Workers' I/O isolation. Source: [GitHub Issue #28193](https://github.com/prisma/prisma/issues/28193)

**Note**: Prisma requires driver adapters (`@prisma/adapter-pg`).

---

## Local Development

### ⚠️ SSL/TLS Limitations in Local Development

**Important**: Local Hyperdrive connections do NOT support SSL. This affects databases that require SSL (e.g., Neon, most cloud providers).

**Workaround - Conditional Connection**:
```typescript
const url = env.isLocal ? env.DB_URL : env.HYPERDRIVE.connectionString;
const client = postgres(url, {
  fetch_types: false,
  max: 2,
});
```

**Alternative**: Use `wrangler dev --remote` (⚠️ connects to production database)

**Timeline**: SSL support planned for 2026 (requires workerd/Workers runtime changes)
**Source**: [GitHub Issue #10124](https://github.com/cloudflare/workers-sdk/issues/10124), tracked as SQC-645

---

### Local Connection Options

**Option 1: Environment Variable (Recommended)**
```bash
export CLOUDFLARE_HYPERDRIVE_LOCAL_CONNECTION_STRING_HYPERDRIVE="postgres://user:password@localhost:5432/local_db"
npx wrangler dev
```
Safe to commit config, no credentials in wrangler.jsonc.

**Option 2: localConnectionString in wrangler.jsonc**
```jsonc
{ "hyperdrive": [{ "binding": "HYPERDRIVE", "id": "prod-id", "localConnectionString": "postgres://..." }] }
```
⚠️ Don't commit credentials to version control.

**Option 3: Remote Development**
```bash
npx wrangler dev --remote  # ⚠️ Uses PRODUCTION database
```

---

## Query Caching

**Cached**: SELECT (non-mutating queries)
**NOT Cached**: INSERT, UPDATE, DELETE, volatile functions (LASTVAL, LAST_INSERT_ID)

**May 2025**: 5x faster cache hits via regional prepared statement caching.

**Critical for postgres.js:**
```typescript
const sql = postgres(env.HYPERDRIVE.connectionString, {
  prepare: true  // REQUIRED for caching
});
```

**Check cache status:**
```typescript
response.headers.get('cf-cache-status');  // HIT, MISS, BYPASS, EXPIRED
```

---

## TLS/SSL Configuration

**SSL Modes**: `require` (default), `verify-ca` (verify CA), `verify-full` (verify CA + hostname)

**Server Certificates (verify-ca/verify-full):**
```bash
npx wrangler cert upload certificate-authority --ca-cert root-ca.pem --name my-ca-cert
npx wrangler hyperdrive create my-db --connection-string="postgres://..." --ca-certificate-id <ID> --sslmode verify-full
```

**Client Certificates (mTLS):**
```bash
npx wrangler cert upload mtls-certificate --cert client-cert.pem --key client-key.pem --name my-cert
npx wrangler hyperdrive create my-db --connection-string="postgres://..." --mtls-certificate-id <ID>
```

---

## Private Database Access (Cloudflare Tunnel)

Connect to databases in private networks (VPCs, on-premises):

```bash
# 1. Install cloudflared (macOS: brew install cloudflare/cloudflare/cloudflared)
# 2. Create tunnel
cloudflared tunnel create my-db-tunnel

# 3. Configure config.yml
# tunnel: <TUNNEL_ID>
# ingress:
#   - hostname: db.example.com
#     service: tcp://localhost:5432

# 4. Run tunnel
cloudflared tunnel run my-db-tunnel

# 5. Create Hyperdrive
npx wrangler hyperdrive create my-private-db --connection-string="postgres://user:password@db.example.com:5432/database"
```

---

## Critical Rules

### Always Do

✅ Include `nodejs_compat` in `compatibility_flags`
✅ Use `ctx.waitUntil(client.end())` for connection cleanup
✅ Set `max: 5` for connection pools (Workers limit: 6)
✅ Enable TLS/SSL on your database (Hyperdrive requires it)
✅ Use prepared statements for caching (postgres.js: `prepare: true`)
✅ Set `disableEval: true` for mysql2 driver
✅ Handle errors gracefully with try/catch
✅ Use environment variables for local development connection strings
✅ Test locally with `wrangler dev` before deploying

### Never Do

❌ Skip `nodejs_compat` flag (causes "No such module" errors)
❌ Use private IP addresses directly (use Cloudflare Tunnel instead)
❌ Use `await client.end()` (blocks response, use `ctx.waitUntil()`)
❌ Set connection pool max > 5 (exceeds Workers' 6 connection limit)
❌ Wrap all queries in transactions (limits connection multiplexing)
❌ Use SQL-level PREPARE/EXECUTE/DEALLOCATE (unsupported)
❌ Use advisory locks, LISTEN/NOTIFY (PostgreSQL unsupported features)
❌ Use multi-statement queries in MySQL (unsupported)
❌ Commit database credentials to version control
❌ Use IP addresses in connection strings instead of hostnames (causes postgres.js to hang)
❌ Use Neon serverless driver with Hyperdrive (uses WebSockets, bypasses pooling)
❌ Use Supabase pooled connection string (Supavisor) with Hyperdrive (double-pooling)
❌ Reuse Prisma client instances across requests in Workers (causes hangs and timeouts)
❌ Use Nitro 3's `useDatabase` with Drizzle and Hyperdrive (~95% failure rate)
❌ Expect SET statements to persist across queries (transaction mode resets connections)
❌ Use postgres.js versions before 3.4.5 (breaks prepared statement caching)

---

## Wrangler Commands Reference

```bash
# Create Hyperdrive configuration
wrangler hyperdrive create <name> --connection-string="postgres://..."

# List all Hyperdrive configurations
wrangler hyperdrive list

# Get details of a configuration
wrangler hyperdrive get <hyperdrive-id>

# Update connection string
wrangler hyperdrive update <hyperdrive-id> --connection-string="postgres://..."

# Delete configuration
wrangler hyperdrive delete <hyperdrive-id>

# Upload CA certificate
wrangler cert upload certificate-authority --ca-cert <file>.pem --name <name>

# Upload client certificate pair
wrangler cert upload mtls-certificate --cert <cert>.pem --key <key>.pem --name <name>
```

---

## Supported Databases

**PostgreSQL (v9.0-17.x)**: AWS RDS/Aurora, Google Cloud SQL, Azure, Neon, Supabase, PlanetScale, Timescale, CockroachDB, Materialize, Fly.io, pgEdge, Prisma Postgres

**MySQL (v5.7-8.x)**: AWS RDS/Aurora, Google Cloud SQL, Azure, PlanetScale, MariaDB (April 2025 GA)

**NOT Supported**: SQL Server, MongoDB, Oracle

---

## Unsupported Features

### PostgreSQL
- SQL-level prepared statements (`PREPARE`, `EXECUTE`, `DEALLOCATE`)
- Advisory locks
- `LISTEN` and `NOTIFY`
- Per-session state modifications

### MySQL
- Non-UTF8 characters in queries
- `USE` statements
- Multi-statement queries
- Protocol-level prepared statements (`COM_STMT_PREPARE`)
- `COM_INIT_DB` messages
- Auth plugins other than `caching_sha2_password` or `mysql_native_password`

**Workaround**: For unsupported features, create a second direct client connection (without Hyperdrive).

---

## Performance Best Practices

1. **Avoid long-running transactions** - Limits connection multiplexing
2. **Use prepared statements** - Enables query caching (postgres.js: `prepare: true`)
3. **Set max: 5 for pools** - Stays within Workers' 6 connection limit
4. **Disable fetch_types if not needed** - Reduces latency (postgres.js)
5. **Use ctx.waitUntil() for cleanup** - Non-blocking connection close
6. **Cache-friendly queries** - Prefer SELECT over complex joins
7. **Index frequently queried columns** - Improves query performance
8. **Monitor with Hyperdrive analytics** - Track cache hit ratios and latency
9. **⚠️ SET statement persistence** - SET commands don't persist across queries due to transaction mode. Wrap SET + query in BEGIN/COMMIT if needed (impacts performance)

---

## Troubleshooting

See `references/troubleshooting.md` for complete error reference with solutions.

**Quick fixes:**

| Error | Solution |
|-------|----------|
| "No such module 'node:*'" | Add `nodejs_compat` to compatibility_flags |
| "TLS not supported by database" | Enable SSL/TLS on your database |
| "Connection refused" | Check firewall rules, allow public internet or use Tunnel |
| "Failed to acquire connection" | Use `ctx.waitUntil()` for cleanup, avoid long transactions |
| "Code generation from strings disallowed" | Set `disableEval: true` in mysql2 config |
| "Bad hostname" | Verify DNS resolves, check for typos |
| "Invalid database credentials" | Check username/password (case-sensitive) |

---

## Metrics and Analytics

[Hyperdrive Dashboard](https://dash.cloudflare.com/?to=/:account/workers/hyperdrive) → Select config → Metrics tab

**Available**: Query count, cache hit ratio, query latency (p50/p95/p99), connection latency, query/result bytes, error rate

---

## Credential Rotation

```bash
# Option 1: Create new config (zero downtime)
wrangler hyperdrive create my-db-v2 --connection-string="postgres://new-creds..."
# Update wrangler.jsonc, deploy, delete old config

# Option 2: Update existing
wrangler hyperdrive update <id> --connection-string="postgres://new-creds..."
```

**Best practice**: Separate configs for staging/production.

---

## References

- [Official Documentation](https://developers.cloudflare.com/hyperdrive/)
- [Get Started Guide](https://developers.cloudflare.com/hyperdrive/get-started/)
- [How Hyperdrive Works](https://developers.cloudflare.com/hyperdrive/configuration/how-hyperdrive-works/)
- [Query Caching](https://developers.cloudflare.com/hyperdrive/configuration/query-caching/)
- [Local Development](https://developers.cloudflare.com/hyperdrive/configuration/local-development/)
- [TLS/SSL Certificates](https://developers.cloudflare.com/hyperdrive/configuration/tls-ssl-certificates-for-hyperdrive/)
- [Troubleshooting Guide](https://developers.cloudflare.com/hyperdrive/observability/troubleshooting/)
- [Wrangler Commands](https://developers.cloudflare.com/hyperdrive/reference/wrangler-commands/)
- [Supported Databases](https://developers.cloudflare.com/hyperdrive/reference/supported-databases-and-features/)

---

**Last verified**: 2026-01-21 | **Skill version**: 3.0.0 | **Changes**: Added 11 Known Issues Prevention entries (6 TIER 1, 5 TIER 2), expanded Prisma/Local Dev/Performance sections with critical warnings, updated Never Do rules

**Package Versions**: wrangler@4.58.0, pg@8.16.3+ (minimum), postgres@3.4.5+ (minimum for caching), postgres@3.4.8 (recommended), mysql2@3.16.0
**Production Tested**: Based on official Cloudflare documentation and community examples
