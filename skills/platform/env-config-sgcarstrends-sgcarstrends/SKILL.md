---
name: env-config
description: Manage environment variables across dev/staging/prod environments and SST config. Use when adding new secrets, updating environment-specific configs, or debugging environment issues.
allowed-tools: Read, Edit, Grep
---

# Environment Configuration Skill

This skill helps you manage environment variables and secrets across the monorepo.

## When to Use This Skill

- Adding new environment variables
- Configuring stage-specific variables
- Setting up secrets for deployment
- Debugging environment variable issues
- Managing API keys and tokens
- Configuring database connections
- Setting up third-party integrations

## Environment File Structure

```
sgcarstrends/
├── .env.example              # Example env file (committed)
├── .env.local                # Local development (not committed)
├── .env.test                 # Test environment (not committed)
├── apps/
│   ├── api/
│   │   ├── .env.example
│   │   └── .env.local
│   └── web/
│       ├── .env.example
│       └── .env.local
└── packages/
    └── database/
        ├── .env.example
        └── .env.local
```

## Environment Variable Categories

### Database

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database

# Connection pooling (optional)
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
```

### Redis

```env
# Upstash Redis
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
```

### AI Services

```env
# Google Gemini
GOOGLE_GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-1.5-pro-latest
```

### Workflows & Queues

```env
# QStash
QSTASH_TOKEN=your-qstash-token
QSTASH_CURRENT_SIGNING_KEY=your-signing-key
QSTASH_NEXT_SIGNING_KEY=your-next-signing-key
```

### Social Media

```env
# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Twitter
TWITTER_BEARER_TOKEN=your-bearer-token

# LinkedIn
LINKEDIN_ACCESS_TOKEN=your-access-token
LINKEDIN_ORG_ID=your-org-id
```

### Error Reporting

```env
# Discord (workflow error logging only)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### Storage

```env
# Vercel Blob
BLOB_READ_WRITE_TOKEN=vercel_blob_token
```

### Next.js Public Variables

```env
# Public variables (exposed to browser)
NEXT_PUBLIC_API_URL=https://api.sgcarstrends.com
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SITE_URL=https://sgcarstrends.com
```

### Build & Runtime

```env
# Node environment
NODE_ENV=development  # development | production | test

# Next.js
NEXT_TELEMETRY_DISABLED=1
```

## Environment File Examples

### Root .env.example

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sgcarstrends

# Redis
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here

# AI Services
GOOGLE_GEMINI_API_KEY=your-api-key

# Workflows
QSTASH_TOKEN=your-qstash-token

# Social Media
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id

# Error Reporting (Discord webhook)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Storage
BLOB_READ_WRITE_TOKEN=vercel_blob_token
```

### apps/web/.env.example

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:3000

# Database (for server components)
DATABASE_URL=postgresql://user:password@localhost:5432/sgcarstrends

# Redis
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here

# Analytics
NEXT_PUBLIC_GA_MEASUREMENT_ID=G-XXXXXXXXXX

# Site URL
NEXT_PUBLIC_SITE_URL=http://localhost:3001
```

### apps/api/.env.example

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sgcarstrends

# Redis
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here

# All other API-specific vars...
```

## Stage-Specific Configuration

### Development

```env
# .env.local (development)
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/sgcarstrends_dev
NEXT_PUBLIC_API_URL=http://localhost:3000
NEXT_PUBLIC_SITE_URL=http://localhost:3001
```

### Staging

```env
# Staging (set in SST or CI/CD)
NODE_ENV=production
DATABASE_URL=postgresql://...staging...
NEXT_PUBLIC_API_URL=https://api.staging.sgcarstrends.com
NEXT_PUBLIC_SITE_URL=https://staging.sgcarstrends.com
```

### Production

```env
# Production (set in SST or CI/CD)
NODE_ENV=production
DATABASE_URL=postgresql://...production...
NEXT_PUBLIC_API_URL=https://api.sgcarstrends.com
NEXT_PUBLIC_SITE_URL=https://sgcarstrends.com
```

## SST Configuration

### Using Environment Variables in SST

```typescript
// infra/api.ts
import { StackContext, Function } from "sst/constructs";

export function API({ stack, app }: StackContext) {
  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    environment: {
      NODE_ENV: app.stage === "production" ? "production" : "development",
      DATABASE_URL: process.env.DATABASE_URL!,
      UPSTASH_REDIS_REST_URL: process.env.UPSTASH_REDIS_REST_URL!,
      UPSTASH_REDIS_REST_TOKEN: process.env.UPSTASH_REDIS_REST_TOKEN!,
      GOOGLE_GEMINI_API_KEY: process.env.GOOGLE_GEMINI_API_KEY!,
      QSTASH_TOKEN: process.env.QSTASH_TOKEN!,
      DISCORD_WEBHOOK_URL: process.env.DISCORD_WEBHOOK_URL!,
      TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN!,
      TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID!,
    },
  });

  return { api };
}
```

### SST Secrets

For sensitive values, use SST secrets:

```bash
# Set secret for specific stage
npx sst secrets set DATABASE_URL "postgresql://..." --stage production
npx sst secrets set UPSTASH_REDIS_REST_TOKEN "token" --stage production

# List secrets
npx sst secrets list --stage production

# Remove secret
npx sst secrets remove DATABASE_URL --stage production
```

Access in code:

```typescript
import { Config } from "sst/node/config";

export const handler = async () => {
  const databaseUrl = Config.DATABASE_URL;
  // Use secret...
};
```

Define in SST config:

```typescript
// infra/api.ts
import { Config } from "sst/constructs";

export function API({ stack }: StackContext) {
  const DATABASE_URL = new Config.Secret(stack, "DATABASE_URL");

  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    bind: [DATABASE_URL],
  });
}
```

## TypeScript Type Safety

### Declare Environment Variables

```typescript
// env.d.ts (root or app-specific)
declare global {
  namespace NodeJS {
    interface ProcessEnv {
      // Database
      DATABASE_URL: string;

      // Redis
      UPSTASH_REDIS_REST_URL: string;
      UPSTASH_REDIS_REST_TOKEN: string;

      // AI
      GOOGLE_GEMINI_API_KEY: string;
      GEMINI_MODEL?: string;

      // Workflows
      QSTASH_TOKEN: string;

      // Social Media
      TELEGRAM_BOT_TOKEN: string;
      TELEGRAM_CHAT_ID: string;

      // Error Reporting
      DISCORD_WEBHOOK_URL: string;

      // Storage
      BLOB_READ_WRITE_TOKEN: string;

      // Next.js Public
      NEXT_PUBLIC_API_URL: string;
      NEXT_PUBLIC_SITE_URL: string;
      NEXT_PUBLIC_GA_MEASUREMENT_ID?: string;

      // Build
      NODE_ENV: "development" | "production" | "test";
    }
  }
}

export {};
```

### Validate Environment Variables

```typescript
// lib/env.ts
import { z } from "zod";

const envSchema = z.object({
  // Database
  DATABASE_URL: z.string().url(),

  // Redis
  UPSTASH_REDIS_REST_URL: z.string().url(),
  UPSTASH_REDIS_REST_TOKEN: z.string().min(1),

  // AI
  GOOGLE_GEMINI_API_KEY: z.string().min(1),

  // Workflows
  QSTASH_TOKEN: z.string().min(1),

  // Social Media
  TELEGRAM_BOT_TOKEN: z.string().optional(),
  TELEGRAM_CHAT_ID: z.string().optional(),

  // Error Reporting
  DISCORD_WEBHOOK_URL: z.string().url().optional(),

  // Next.js
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_SITE_URL: z.string().url(),

  // Build
  NODE_ENV: z.enum(["development", "production", "test"]),
});

export const env = envSchema.parse(process.env);

// Usage
import { env } from "./lib/env";
const db = new Database(env.DATABASE_URL);
```

## Loading Environment Variables

### Next.js

Next.js automatically loads `.env.local`:

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },
};

export default nextConfig;
```

### Drizzle Studio

```typescript
// packages/database/drizzle.config.ts
import { defineConfig } from "drizzle-kit";
import * as dotenv from "dotenv";

// Load environment variables
dotenv.config({ path: "../../.env.local" });

export default defineConfig({
  schema: "./src/db/schema",
  out: "./migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### Vitest

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import * as dotenv from "dotenv";

// Load test environment
dotenv.config({ path: ".env.test" });

export default defineConfig({
  test: {
    env: {
      DATABASE_URL: process.env.DATABASE_URL!,
    },
  },
});
```

## GitHub Actions

### Secrets Configuration

Set secrets in GitHub:
1. Go to repository Settings
2. Secrets and variables → Actions
3. Add repository secrets

### Use in Workflows

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      UPSTASH_REDIS_REST_URL: ${{ secrets.UPSTASH_REDIS_REST_URL }}
      UPSTASH_REDIS_REST_TOKEN: ${{ secrets.UPSTASH_REDIS_REST_TOKEN }}
      GOOGLE_GEMINI_API_KEY: ${{ secrets.GOOGLE_GEMINI_API_KEY }}

    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        run: pnpm deploy:prod
```

## Debugging Environment Issues

### Check Variables Are Set

```typescript
// Check at runtime
console.log("DATABASE_URL:", process.env.DATABASE_URL ? "✓ Set" : "✗ Not set");
console.log("REDIS_URL:", process.env.UPSTASH_REDIS_REST_URL ? "✓ Set" : "✗ Not set");

// Fail early if missing
if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL is required");
}
```

### Use dotenv-cli

```bash
# Install
pnpm add -D dotenv-cli

# Run command with env file
pnpm dotenv -e .env.local -- pnpm dev

# Run tests with test env
pnpm dotenv -e .env.test -- pnpm test
```

### Debug Script

```typescript
// scripts/check-env.ts
import * as dotenv from "dotenv";

dotenv.config({ path: ".env.local" });

const requiredVars = [
  "DATABASE_URL",
  "UPSTASH_REDIS_REST_URL",
  "UPSTASH_REDIS_REST_TOKEN",
];

console.log("Checking environment variables...\n");

let missing = 0;

for (const varName of requiredVars) {
  const value = process.env[varName];

  if (value) {
    console.log(`✓ ${varName}`);
  } else {
    console.log(`✗ ${varName} - MISSING`);
    missing++;
  }
}

if (missing > 0) {
  console.error(`\n❌ ${missing} required variables are missing!`);
  process.exit(1);
} else {
  console.log("\n✅ All required variables are set!");
}
```

Add to package.json:

```json
{
  "scripts": {
    "check-env": "tsx scripts/check-env.ts"
  }
}
```

## Common Patterns

### Conditional Loading

```typescript
// Load different configs based on environment
const config = {
  development: {
    apiUrl: "http://localhost:3000",
    debug: true,
  },
  production: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL,
    debug: false,
  },
  test: {
    apiUrl: "http://localhost:3000",
    debug: false,
  },
}[process.env.NODE_ENV || "development"];
```

### Default Values

```typescript
const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
  cacheTimeout: parseInt(process.env.CACHE_TIMEOUT || "3600", 10),
  enableFeature: process.env.ENABLE_FEATURE === "true",
};
```

### Required vs Optional

```typescript
// Required (throw if missing)
const databaseUrl = process.env.DATABASE_URL!;

// Optional (with default)
const cacheTimeout = process.env.CACHE_TIMEOUT || "3600";

// Optional (may be undefined)
const optionalKey: string | undefined = process.env.OPTIONAL_KEY;
```

## Security Best Practices

### 1. Never Commit Secrets

```gitignore
# .gitignore
.env
.env.local
.env.*.local
.env.development.local
.env.test.local
.env.production.local
```

### 2. Use Environment-Specific Files

```
.env.example        ✅ Committed (no sensitive data)
.env.local          ❌ Not committed (has secrets)
.env.development    ❌ Not committed
.env.production     ❌ Not committed
```

### 3. Rotate Secrets Regularly

```bash
# Update secret for all stages
npx sst secrets set API_KEY "new-key" --stage dev
npx sst secrets set API_KEY "new-key" --stage staging
npx sst secrets set API_KEY "new-key" --stage production
```

### 4. Least Privilege

Only grant necessary permissions:
- Database: Use read-only user for read operations
- API keys: Use restricted scopes
- AWS: Use IAM roles with minimal permissions

### 5. Audit Access

```bash
# Check who has access to secrets
npx sst secrets list --stage production

# Review CloudWatch logs for unauthorized access
```

## Testing with Environment Variables

```typescript
// __tests__/api.test.ts
import { describe, it, expect, beforeAll } from "vitest";

describe("API Tests", () => {
  beforeAll(() => {
    // Set test environment variables
    process.env.DATABASE_URL = "postgresql://test:test@localhost:5432/test";
    process.env.UPSTASH_REDIS_REST_URL = "https://test.upstash.io";
  });

  it("uses correct environment", () => {
    expect(process.env.DATABASE_URL).toContain("test");
  });
});
```

## Troubleshooting

### Variables Not Loading

**Issue**: Environment variables are undefined
**Solutions**:
1. Check file name is exactly `.env.local`
2. Restart development server
3. Verify file is in correct directory
4. Check for syntax errors in .env file

### Next.js Public Variables

**Issue**: `NEXT_PUBLIC_` variables not available in browser
**Solutions**:
1. Ensure variable starts with `NEXT_PUBLIC_`
2. Restart Next.js dev server
3. Check browser console for actual value

### SST Secrets Not Working

**Issue**: SST secrets return undefined
**Solutions**:
1. Verify secret is set for correct stage
2. Check `bind` configuration in SST
3. Use `Config` import from `sst/node/config`

## References

- Next.js Environment Variables: https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
- SST Config: https://docs.sst.dev/config
- Related files:
  - `.env.example` - Example environment file
  - `infra/` - SST infrastructure with env config
  - Root CLAUDE.md - Project documentation

## Best Practices

1. **Use .env.example**: Provide template for required variables
2. **Type Safety**: Define types for environment variables
3. **Validation**: Validate on application startup
4. **SST Secrets**: Use for sensitive production values
5. **Never Commit**: Add `.env.local` to `.gitignore`
6. **Document**: Comment what each variable is for
7. **Stage-Specific**: Use different values per environment
8. **Fail Fast**: Validate required variables at startup
