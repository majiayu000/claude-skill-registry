---
name: bknd-database-provision
description: Use when setting up a production database for Bknd. Covers SQLite file, LibSQL/Turso, Cloudflare D1, PostgreSQL, Neon, Supabase, and Xata configuration.
---

# Provision Production Database

Set up and configure a production database for your Bknd application.

## Prerequisites

- Bknd application with schema defined
- Account on chosen database provider (for cloud databases)
- Environment for storing connection credentials

## When to Use UI Mode

- Creating databases via provider dashboards (Turso, Neon, Cloudflare, Supabase)
- Managing database settings and access tokens
- Viewing database metrics and logs

## When to Use Code Mode

- Configuring database connection in Bknd
- CLI commands for database creation
- Schema sync and migrations

## Database Selection Guide

| Database | Best For | Platform Compatibility | Cost |
|----------|----------|------------------------|------|
| **SQLite File** | VPS, Docker, single-server | Node.js, Bun | Free |
| **LibSQL/Turso** | Serverless, edge, global | All platforms | Free tier |
| **Cloudflare D1** | Cloudflare Workers | Cloudflare only | Free tier |
| **PostgreSQL** | Complex queries, transactions | VPS, Docker | Self-hosted |
| **Neon** | Serverless Postgres | Vercel, Lambda | Free tier |
| **Supabase** | Postgres + extras | Any | Free tier |
| **Xata** | Serverless + search | Any | Free tier |

---

## SQLite File (VPS/Docker)

**Best for:** Single-server deployments with full control

### Step 1: Configure Connection

```typescript
// bknd.config.ts
export default {
  app: (env) => ({
    connection: {
      url: env.DB_URL ?? "file:data.db",  // Relative to cwd
    },
  }),
};
```

### Step 2: Set Environment Variable

```bash
# Relative path (project directory)
DB_URL=file:data.db

# Absolute path (recommended for production)
DB_URL=file:/var/data/myapp/bknd.db
```

### Step 3: Ensure Directory Exists

```bash
mkdir -p /var/data/myapp
```

### Docker Volume

```yaml
# docker-compose.yml
services:
  bknd:
    volumes:
      - bknd-data:/app/data
    environment:
      - DB_URL=file:/app/data/bknd.db

volumes:
  bknd-data:
```

---

## LibSQL / Turso

**Best for:** Serverless, edge deployments, global distribution

### Step 1: Install Turso CLI

```bash
# macOS/Linux
curl -sSfL https://get.tur.so/install.sh | bash

# Authenticate
turso auth login
```

### Step 2: Create Database

```bash
# Create database
turso db create my-bknd-db

# Optional: Specify region
turso db create my-bknd-db --location lax  # Los Angeles
```

### Step 3: Get Connection Details

```bash
# Get connection URL
turso db show my-bknd-db --url
# Output: libsql://my-bknd-db-username.turso.io

# Create auth token
turso db tokens create my-bknd-db
# Output: eyJhbGciOi...
```

### Step 4: Configure Bknd

```typescript
// bknd.config.ts
export default {
  app: (env) => ({
    connection: {
      url: env.DB_URL,       // libsql://...
      authToken: env.DB_TOKEN,
    },
  }),
};
```

### Step 5: Set Environment Variables

```bash
DB_URL=libsql://my-bknd-db-username.turso.io
DB_TOKEN=eyJhbGciOi...
```

### Turso Locations

Common regions: `ams` (Amsterdam), `fra` (Frankfurt), `lax` (LA), `lhr` (London), `nrt` (Tokyo), `syd` (Sydney)

```bash
turso db locations  # List all regions
```

---

## Cloudflare D1

**Best for:** Cloudflare Workers deployments

### Step 1: Create D1 Database

```bash
wrangler d1 create my-bknd-db
```

Output:
```
Created D1 database 'my-bknd-db'
database_name = "my-bknd-db"
database_id = "abc123-def456-..."
```

### Step 2: Configure wrangler.toml

```toml
name = "my-bknd-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-bknd-db"
database_id = "abc123-def456-..."
```

### Step 3: Configure Bknd Adapter

```typescript
// src/index.ts
import { hybrid, type CloudflareBkndConfig } from "bknd/adapter/cloudflare";
import { d1Sqlite } from "bknd/adapter/cloudflare";

export default hybrid<CloudflareBkndConfig>({
  app: (env) => ({
    connection: d1Sqlite({ binding: env.DB }),
    isProduction: true,
  }),
});
```

### D1 CLI Commands

```bash
# List databases
wrangler d1 list

# Execute SQL (local dev)
wrangler d1 execute my-bknd-db --local --command "SELECT * FROM posts"

# Execute SQL (production)
wrangler d1 execute my-bknd-db --command "SELECT * FROM posts"

# Export backup
wrangler d1 backup create my-bknd-db
```

---

## PostgreSQL (Self-Hosted)

**Best for:** Complex queries, large datasets, existing Postgres infrastructure

### Step 1: Install Adapter

```bash
npm install postgres
# or
npm install pg
```

### Step 2: Configure Connection

**Using `postgres` (recommended):**

```typescript
import { PostgresJsConnection } from "bknd/adapter/postgres";

export default {
  app: (env) => ({
    connection: new PostgresJsConnection({
      connectionString: env.DATABASE_URL,
    }),
  }),
};
```

**Using `pg`:**

```typescript
import { PgPostgresConnection } from "bknd/adapter/postgres";

export default {
  app: (env) => ({
    connection: new PgPostgresConnection({
      connectionString: env.DATABASE_URL,
    }),
  }),
};
```

### Step 3: Set Connection String

```bash
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

---

## Neon (Serverless Postgres)

**Best for:** Vercel, serverless, auto-scaling Postgres

### Step 1: Create Project at neon.tech

1. Sign up at [neon.tech](https://neon.tech)
2. Create new project
3. Copy connection string from dashboard

### Step 2: Install Neon Dialect

```bash
npm install kysely-neon
```

### Step 3: Configure Connection

```typescript
import { createCustomPostgresConnection } from "bknd";
import { NeonDialect } from "kysely-neon";

const neon = createCustomPostgresConnection("neon", NeonDialect);

export default {
  app: (env) => ({
    connection: neon({
      connectionString: env.NEON_DATABASE_URL,
    }),
  }),
};
```

### Step 4: Set Environment Variable

```bash
NEON_DATABASE_URL=postgres://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

---

## Supabase

**Best for:** Full-featured Postgres with extras (auth, storage, realtime)

### Step 1: Create Project at supabase.com

1. Sign up at [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings > Database > Connection string

### Step 2: Get Direct Connection String

Use "Direct connection" (not pooler) for Bknd:
```
postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Step 3: Configure Connection

```typescript
export default {
  app: (env) => ({
    connection: {
      url: env.SUPABASE_DB_URL,
    },
  }),
};
```

### Step 4: Set Environment Variable

```bash
SUPABASE_DB_URL=postgresql://postgres:your-password@db.abcdefgh.supabase.co:5432/postgres
```

---

## Xata

**Best for:** Serverless Postgres with built-in search

### Step 1: Create Database at xata.io

1. Sign up at [xata.io](https://xata.io)
2. Create workspace and database

### Step 2: Install Xata Dialect

```bash
npm install @xata.io/kysely
```

### Step 3: Configure Connection

```typescript
import { createCustomPostgresConnection } from "bknd";
import { XataDialect } from "@xata.io/kysely";

const xata = createCustomPostgresConnection("xata", XataDialect);

export default {
  app: (env) => ({
    connection: xata({
      apiKey: env.XATA_API_KEY,
      workspace: "your-workspace",
      database: "your-database",
    }),
  }),
};
```

---

## Schema Sync

After configuring your database, Bknd auto-syncs schema on first request. For manual control:

```bash
# Dry run (preview changes)
npx bknd sync --dry-run

# Apply changes
npx bknd sync

# Force sync (use with caution)
npx bknd sync --force
```

---

## Connection Testing

### Verify Connection

```typescript
// test-connection.ts
import { app } from "bknd";

const bknd = app({
  connection: {
    url: process.env.DB_URL!,
    authToken: process.env.DB_TOKEN,
  },
});

async function test() {
  await bknd.build();
  console.log("Connection successful!");
  console.log("Entities:", Object.keys(bknd.modules.data.entities));
  process.exit(0);
}

test().catch((e) => {
  console.error("Connection failed:", e);
  process.exit(1);
});
```

Run:
```bash
npx tsx test-connection.ts
```

---

## Common Pitfalls

### "Connection refused" or "ECONNREFUSED"

**Problem:** Can't connect to database

**Fix:**
- Verify connection URL format
- Check firewall/security group rules
- Ensure database is running
- For cloud: verify IP allowlist includes your server

### "Auth token required" (LibSQL/Turso)

**Problem:** Missing or invalid auth token

**Fix:**
```bash
# Generate new token
turso db tokens create my-bknd-db

# Set in environment
export DB_TOKEN="eyJhbGciOi..."
```

### "D1 binding not found"

**Problem:** `env.DB is undefined` in Cloudflare Workers

**Fix:** Check wrangler.toml binding name matches code:
```toml
[[d1_databases]]
binding = "DB"  # Must match env.DB
```

### "SSL required" (PostgreSQL)

**Problem:** Connection fails without SSL

**Fix:** Add `?sslmode=require` to connection string:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

### "Unknown database" or "Database does not exist"

**Problem:** Database not created

**Fix:**
```bash
# Turso
turso db create my-bknd-db

# D1
wrangler d1 create my-bknd-db

# PostgreSQL
createdb my-bknd-db
```

### Schema Sync Fails

**Problem:** Migrations fail on production database

**Fix:**
```bash
# Preview changes first
npx bknd sync --dry-run

# If stuck, use --force (data loss possible!)
npx bknd sync --force --drop
```

---

## Migration from Development

### Export Development Data

```bash
# SQLite
sqlite3 data.db .dump > backup.sql

# Using API
curl http://localhost:3000/api/data/posts > posts.json
```

### Import to Production

```bash
# Via seed function (recommended)
# See bknd-seed-data skill

# Direct SQL (SQLite to SQLite only)
cat backup.sql | turso db shell my-bknd-db
```

---

## DOs and DON'Ts

**DO:**
- Use cloud databases (Turso, D1, Neon) for serverless
- Store credentials in environment variables
- Test connection before deploying
- Use SSL for PostgreSQL connections
- Keep auth tokens secure
- Enable backups for production data

**DON'T:**
- Use file-based SQLite in serverless/edge
- Hardcode credentials in source code
- Share auth tokens across environments
- Skip connection testing
- Use `--force --drop` without backups
- Expose database directly to internet (use Bknd API)

---

## Related Skills

- **bknd-deploy-hosting** - Deploy to hosting platforms
- **bknd-production-config** - Production security settings
- **bknd-env-config** - Environment variable setup
- **bknd-seed-data** - Populate database with initial data
- **bknd-local-setup** - Local development (pre-production)
