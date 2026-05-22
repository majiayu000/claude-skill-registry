---
name: bknd-deploy-hosting
description: Use when deploying a Bknd application to production hosting. Covers Cloudflare Workers/Pages, Node.js/Bun servers, Docker, Vercel, AWS Lambda, and other platforms.
---

# Deploy to Hosting

Deploy your Bknd application to various hosting platforms.

## Prerequisites

- Working Bknd application locally
- Schema defined and tested
- Database provisioned (see `bknd-database-provision`)
- Environment variables prepared (see `bknd-env-config`)

## When to Use UI Mode

- Cloudflare/Vercel dashboards for environment variables
- Platform-specific deployment settings
- Viewing deployment logs

## When to Use Code Mode

- All deployment configuration and commands
- Adapter setup for target platform
- CI/CD pipeline configuration

## Platform Selection Guide

| Platform | Best For | Database Options | Cold Start |
|----------|----------|------------------|------------|
| **Cloudflare Workers** | Edge, global low-latency | D1, Turso | ~0ms |
| **Cloudflare Pages** | Static + API | D1, Turso | ~0ms |
| **Vercel** | Next.js apps | Turso, Neon | ~200ms |
| **Node.js/Bun VPS** | Full control, dedicated | Any | N/A |
| **Docker** | Containerized, portable | Any | N/A |
| **AWS Lambda** | Serverless, pay-per-use | Turso, RDS | ~500ms |

## Code Approach

### Cloudflare Workers

**Step 1: Install Wrangler**

```bash
npm install -D wrangler
```

**Step 2: Create `wrangler.toml`**

```toml
name = "my-bknd-app"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-d1-database-id"

# Optional: R2 for media storage
[[r2_buckets]]
binding = "R2_BUCKET"
bucket_name = "my-bucket"

[vars]
ENVIRONMENT = "production"
```

**Step 3: Configure Adapter**

```typescript
// src/index.ts
import { hybrid, type CloudflareBkndConfig } from "bknd/adapter/cloudflare";
import { d1Sqlite } from "bknd/adapter/cloudflare";
import { em, entity, text } from "bknd";

const schema = em({
  posts: entity("posts", {
    title: text().required(),
  }),
});

export default hybrid<CloudflareBkndConfig>({
  app: (env) => ({
    connection: d1Sqlite({ binding: env.DB }),
    schema,
    isProduction: true,
    auth: {
      jwt: {
        secret: env.JWT_SECRET,
      },
    },
    config: {
      media: {
        enabled: true,
        adapter: {
          type: "r2",
          config: { bucket: env.R2_BUCKET },
        },
      },
    },
  }),
});
```

**Step 4: Create D1 Database**

```bash
# Create database
wrangler d1 create my-database

# Copy the database_id to wrangler.toml
```

**Step 5: Set Secrets**

```bash
wrangler secret put JWT_SECRET
# Enter your secret (min 32 chars)
```

**Step 6: Deploy**

```bash
wrangler deploy
```

---

### Cloudflare Pages (with Functions)

**Step 1: Create `functions/api/[[bknd]].ts`**

```typescript
import { hybrid, type CloudflareBkndConfig } from "bknd/adapter/cloudflare";
import { d1Sqlite } from "bknd/adapter/cloudflare";
import schema from "../../bknd.config";

export const onRequest = hybrid<CloudflareBkndConfig>({
  app: (env) => ({
    connection: d1Sqlite({ binding: env.DB }),
    schema,
    isProduction: true,
    auth: {
      jwt: { secret: env.JWT_SECRET },
    },
  }),
});
```

**Step 2: Configure Pages**

In Cloudflare dashboard:
1. Connect your git repository
2. Set build command (if any)
3. Add D1 binding under Settings > Functions > D1 Database Bindings
4. Add environment variables under Settings > Environment Variables

---

### Node.js / Bun (VPS)

**Step 1: Create Production Entry**

```typescript
// index.ts
import { serve, type BunBkndConfig } from "bknd/adapter/bun";
// or for Node.js:
// import { serve } from "bknd/adapter/node";

const config: BunBkndConfig = {
  connection: {
    url: process.env.DB_URL!,
    authToken: process.env.DB_TOKEN,
  },
  isProduction: true,
  auth: {
    jwt: {
      secret: process.env.JWT_SECRET!,
      expires: "7d",
    },
  },
  config: {
    media: {
      enabled: true,
      adapter: {
        type: "s3",
        config: {
          bucket: process.env.S3_BUCKET!,
          region: process.env.S3_REGION!,
          accessKeyId: process.env.S3_ACCESS_KEY!,
          secretAccessKey: process.env.S3_SECRET_KEY!,
        },
      },
    },
    guard: {
      enabled: true,
    },
  },
};

serve(config);
```

**Step 2: Set Environment Variables**

```bash
export DB_URL="libsql://your-db.turso.io"
export DB_TOKEN="your-turso-token"
export JWT_SECRET="your-32-char-minimum-secret"
export PORT=3000
```

**Step 3: Run with Process Manager**

```bash
# Using PM2
npm install -g pm2
pm2 start "bun run index.ts" --name bknd-app

# Or systemd (create /etc/systemd/system/bknd.service)
```

---

### Docker

**Step 1: Create `Dockerfile`**

```dockerfile
FROM oven/bun:1.0-alpine

WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

COPY . .

# Create data directory for SQLite (if using file-based)
RUN mkdir -p /app/data

ENV PORT=3000

EXPOSE 3000

CMD ["bun", "run", "index.ts"]
```

**Step 2: Create `docker-compose.yml`**

```yaml
version: "3.8"
services:
  bknd:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - bknd-data:/app/data
    environment:
      - DB_URL=file:/app/data/bknd.db
      - JWT_SECRET=${JWT_SECRET}
      - NODE_ENV=production
    restart: unless-stopped

volumes:
  bknd-data:
```

**Step 3: Deploy**

```bash
# Build and run
docker compose up -d

# View logs
docker compose logs -f bknd
```

---

### Vercel (Next.js)

**Step 1: Create API Route**

```typescript
// app/api/bknd/[[...bknd]]/route.ts
export { GET, POST, PUT, DELETE, PATCH } from "bknd/adapter/nextjs";
```

**Step 2: Create `bknd.config.ts`**

```typescript
import type { NextjsBkndConfig } from "bknd/adapter/nextjs";
import { em, entity, text } from "bknd";

const schema = em({
  posts: entity("posts", {
    title: text().required(),
  }),
});

type Database = (typeof schema)["DB"];
declare module "bknd" {
  interface DB extends Database {}
}

export default {
  app: (env) => ({
    connection: {
      url: env.DB_URL,
      authToken: env.DB_TOKEN,
    },
    schema,
    isProduction: env.NODE_ENV === "production",
    auth: {
      jwt: { secret: env.JWT_SECRET },
    },
  }),
} satisfies NextjsBkndConfig;
```

**Step 3: Set Vercel Environment Variables**

In Vercel dashboard or CLI:

```bash
vercel env add DB_URL
vercel env add DB_TOKEN
vercel env add JWT_SECRET
```

**Step 4: Deploy**

```bash
vercel deploy --prod
```

---

### AWS Lambda

**Step 1: Install Dependencies**

```bash
npm install -D serverless serverless-esbuild
```

**Step 2: Create `handler.ts`**

```typescript
import { createHandler } from "bknd/adapter/aws";

export const handler = createHandler({
  connection: {
    url: process.env.DB_URL!,
    authToken: process.env.DB_TOKEN,
  },
  isProduction: true,
  auth: {
    jwt: { secret: process.env.JWT_SECRET! },
  },
});
```

**Step 3: Create `serverless.yml`**

```yaml
service: bknd-api

provider:
  name: aws
  runtime: nodejs20.x
  region: us-east-1
  environment:
    DB_URL: ${env:DB_URL}
    DB_TOKEN: ${env:DB_TOKEN}
    JWT_SECRET: ${env:JWT_SECRET}

plugins:
  - serverless-esbuild

functions:
  api:
    handler: handler.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
      - http:
          path: /
          method: ANY
```

**Step 4: Deploy**

```bash
serverless deploy --stage prod
```

---

## Pre-Deployment Checklist

```bash
# 1. Generate types
npx bknd types

# 2. Test locally with production-like config
DB_URL="your-prod-db" JWT_SECRET="your-secret" npx bknd run

# 3. Verify schema sync
# Schema auto-syncs on first request in production
```

## Environment Variables (All Platforms)

| Variable | Required | Description |
|----------|----------|-------------|
| `DB_URL` | Yes | Database connection URL |
| `DB_TOKEN` | Depends | Auth token (Turso/LibSQL) |
| `JWT_SECRET` | Yes | Min 32 chars for security |
| `PORT` | No | Server port (default: 3000) |

## Common Pitfalls

### "Module not found" for Native SQLite

**Problem:** `better-sqlite3` not available in serverless

**Fix:** Use LibSQL/Turso instead of file-based SQLite:
```typescript
connection: {
  url: "libsql://your-db.turso.io",
  authToken: process.env.DB_TOKEN,
}
```

### "JWT_SECRET required" Error

**Problem:** Auth fails in production

**Fix:** Set JWT_SECRET environment variable:
```bash
# Cloudflare
wrangler secret put JWT_SECRET

# Vercel
vercel env add JWT_SECRET

# Docker
docker run -e JWT_SECRET="your-secret" ...
```

### Cold Start Timeouts (Lambda)

**Problem:** First request times out

**Fix:**
- Use lighter database (Turso over RDS)
- Reduce bundle size
- Enable provisioned concurrency for critical functions

### D1 Binding Not Found

**Problem:** `env.DB is undefined`

**Fix:** Check wrangler.toml D1 binding:
```toml
[[d1_databases]]
binding = "DB"  # Must match env.DB in code
database_name = "my-database"
database_id = "actual-id-from-wrangler-d1-create"
```

### Media Uploads Fail in Serverless

**Problem:** Local storage doesn't work in serverless

**Fix:** Use cloud storage adapter:
```typescript
config: {
  media: {
    adapter: {
      type: "s3",  // or "r2", "cloudinary"
      config: { /* credentials */ },
    },
  },
}
```

### CORS Errors

**Problem:** Frontend can't access API

**Fix:** Configure CORS in your adapter:
```typescript
// Most adapters handle this automatically
// For custom needs, check platform docs
```

## Deployment Commands Reference

```bash
# Cloudflare Workers
wrangler deploy
wrangler tail  # View logs

# Vercel
vercel deploy --prod
vercel logs

# Docker
docker compose up -d
docker compose logs -f

# AWS Lambda
serverless deploy --stage prod
serverless logs -f api
```

## DOs and DON'Ts

**DO:**
- Set `isProduction: true` in production config
- Use cloud storage (S3/R2/Cloudinary) for media
- Set strong JWT_SECRET (min 32 chars)
- Enable Guard for authorization
- Test with production database before deploying
- Use environment variables for all secrets

**DON'T:**
- Use file-based SQLite in serverless
- Hardcode secrets in code
- Deploy without testing schema sync
- Use local storage adapter in production
- Skip JWT_SECRET configuration
- Commit `.env` files with real secrets

## Related Skills

- **bknd-database-provision** - Set up production database
- **bknd-production-config** - Production security settings
- **bknd-storage-config** - Configure media storage
- **bknd-env-config** - Environment variable setup
- **bknd-local-setup** - Local development (pre-deploy testing)
