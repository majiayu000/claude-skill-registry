---
name: bknd-env-config
description: Use when configuring environment variables for Bknd projects. Covers .env files, secrets management, env injection in config, platform-specific variables, and production security.
---

# Environment Variables Configuration

Configure environment variables for Bknd applications across development and production.

## Prerequisites

- Bknd project initialized (`bknd.config.ts` exists)
- Understanding of your deployment target (local, Cloudflare, Vercel, etc.)

## When to Use UI Mode

- Viewing current config via admin panel
- N/A for environment variables - all done via code/files

## When to Use Code Mode

- Creating `.env` files
- Configuring secrets in `bknd.config.ts`
- Setting up platform-specific env vars
- All environment configuration tasks

## Code Approach

### Step 1: Create .env File

Create `.env` in project root:

```bash
# Database
DB_URL=file:data.db
DB_TOKEN=

# Auth
JWT_SECRET=your-secret-here-min-32-chars

# Server
PORT=3000

# Development
LOCAL=true
```

### Step 2: Inject Env in Config

Access env vars via the `env` parameter in `bknd.config.ts`:

```typescript
import type { CliBkndConfig } from "bknd";

export default {
  app: (env) => ({
    connection: {
      url: env.DB_URL ?? "file:data.db",
      authToken: env.DB_TOKEN,
    },
    auth: {
      jwt: {
        secret: env.JWT_SECRET ?? "dev-secret-change-in-prod",
      },
    },
  }),
} satisfies CliBkndConfig;
```

The `env` parameter receives all environment variables loaded from `.env` files and system environment.

### Step 3: Use .dev.vars for Dev Overrides (Optional)

Bknd loads env files in order (later takes precedence):
1. `.env` - Base configuration
2. `.dev.vars` - Development-specific overrides (Cloudflare style)

Create `.dev.vars` for local dev overrides:

```bash
# .dev.vars - Dev-only, overrides .env
DB_URL=:memory:
JWT_SECRET=dev-only-secret
```

## Common Environment Variables

### Database

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_URL` | Database connection URL | `file:data.db`, `libsql://db.turso.io` |
| `DB_TOKEN` | LibSQL/Turso auth token | `eyJhbGciOiJFZERTQSIs...` |

### Authentication

| Variable | Description | Example |
|----------|-------------|---------|
| `JWT_SECRET` | JWT signing secret (min 32 chars) | `your-very-long-secret-key-here` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | `123456.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | `GOCSPX-xxx` |
| `GITHUB_CLIENT_ID` | GitHub OAuth client ID | `Iv1.abc123` |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth secret | `secret_xxx` |

### Media/Storage

| Variable | Description | Example |
|----------|-------------|---------|
| `S3_ACCESS_KEY` | S3/R2 access key | `AKIAIOSFODNN7EXAMPLE` |
| `S3_SECRET_KEY` | S3/R2 secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| `S3_ENDPOINT` | S3-compatible endpoint | `https://bucket.s3.region.amazonaws.com` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | `my-cloud` |
| `CLOUDINARY_API_KEY` | Cloudinary API key | `123456789012345` |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | `abcdefghijk...` |

### Server

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `3000` |
| `LOCAL` | Disable telemetry | - |
| `NODE_ENV` / `ENVIRONMENT` | Environment mode | `development` |

## Complete Configuration Example

```typescript
import type { CliBkndConfig } from "bknd";
import { em, entity, text } from "bknd";

const schema = em({
  posts: entity("posts", { title: text().required() }),
});

export default {
  app: (env) => ({
    // Database
    connection: {
      url: env.DB_URL ?? "file:data.db",
      authToken: env.DB_TOKEN,
    },

    // Production flag
    isProduction: env.NODE_ENV === "production",

    // Pass all secrets to app
    secrets: env,
  }),

  config: {
    data: schema.toJSON(),

    // Auth with env-based secrets
    auth: {
      enabled: true,
      jwt: {
        secret: env.JWT_SECRET,
        issuer: "my-app",
      },
      strategies: {
        password: { enabled: true },
        google: env.GOOGLE_CLIENT_ID ? {
          config: {
            name: "google",
            type: "oidc",
            client: {
              client_id: env.GOOGLE_CLIENT_ID,
              client_secret: env.GOOGLE_CLIENT_SECRET,
            },
          },
        } : undefined,
      },
    },

    // Media with env-based adapter config
    media: {
      enabled: true,
      adapter: {
        type: "s3",
        config: {
          access_key: env.S3_ACCESS_KEY,
          secret_access_key: env.S3_SECRET_KEY,
          url: env.S3_ENDPOINT,
        },
      },
    },
  },
} satisfies CliBkndConfig;
```

## Platform-Specific Configuration

### Cloudflare Workers/Pages

Use `wrangler.toml` for non-secret vars and dashboard for secrets:

```toml
# wrangler.toml
[vars]
ENVIRONMENT = "production"
```

Set secrets via CLI:
```bash
npx wrangler secret put JWT_SECRET
npx wrangler secret put DB_TOKEN
```

Access in config:
```typescript
import type { CloudflareBkndConfig } from "bknd/adapter/cloudflare";

export default {
  app: (env) => ({
    connection: env.DB,  // D1 binding
    isProduction: env.ENVIRONMENT === "production",
    secrets: env,
  }),
} satisfies CloudflareBkndConfig;
```

### Vercel

Use Vercel dashboard or CLI for env vars:

```bash
vercel env add JWT_SECRET production
vercel env add DB_URL production
```

Or `.env.local` for local development (auto-loaded by Next.js):
```bash
# .env.local
DB_URL=file:data.db
JWT_SECRET=dev-secret
```

### Docker

Pass via docker-compose or `-e` flag:

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DB_URL=file:/data/app.db
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - .env.production
```

## Generate .env Template

Use CLI to generate env template from your config:

```bash
# Output required secrets as template
npx bknd secrets --template --format env

# Save to file
npx bknd secrets --template --format env --out .env.example
```

This creates a template without actual values, safe for version control.

## SyncSecrets Option

Auto-generate `.env.example` on config changes:

```typescript
export default {
  syncSecrets: {
    enabled: true,
    outFile: ".env.example",
    format: "env",  // or "json"
  },
  app: (env) => ({ ... }),
} satisfies CliBkndConfig;
```

## Environment-Based Feature Flags

Conditionally enable features based on environment:

```typescript
export default {
  app: (env) => ({
    connection: { url: env.DB_URL ?? "file:data.db" },
  }),
  config: {
    auth: {
      enabled: true,
      // Only enable OAuth in production (requires secrets)
      strategies: {
        password: { enabled: true },
        google: env.GOOGLE_CLIENT_ID ? {
          config: {
            name: "google",
            type: "oidc",
            client: {
              client_id: env.GOOGLE_CLIENT_ID,
              client_secret: env.GOOGLE_CLIENT_SECRET,
            },
          },
        } : undefined,
      },
    },
    // Only enable S3 media in production
    media: env.S3_ACCESS_KEY ? {
      enabled: true,
      adapter: {
        type: "s3",
        config: {
          access_key: env.S3_ACCESS_KEY,
          secret_access_key: env.S3_SECRET_KEY,
          url: env.S3_ENDPOINT,
        },
      },
    } : {
      enabled: false,
    },
  },
} satisfies CliBkndConfig;
```

## Database Connection Priority

Bknd resolves database connection in order:
1. `--db-url` CLI argument
2. Config file `connection.url`
3. `--memory` flag (uses `:memory:`)
4. `DB_URL` environment variable
5. Fallback: `file:data.db`

## Verification

**Check env loading:**
```bash
# Server logs show connection source
npx bknd run
# Look for: "Using connection from ..."
```

**Test env injection:**
```typescript
// Temporarily log env in config
app: (env) => {
  console.log("Loaded env:", Object.keys(env));
  return { ... };
},
```

**Verify secrets command:**
```bash
npx bknd secrets --template
```

## Common Pitfalls

### .env Not Loading

**Problem:** Env vars undefined in config

**Fix:** Check file location and format:
```bash
# .env must be in project root (same level as bknd.config.ts)
ls -la .env

# No quotes around values
DB_URL=file:data.db     # Correct
DB_URL="file:data.db"   # May cause issues
```

### JWT_SECRET Too Short

**Problem:** Auth fails or warning about weak secret

**Fix:** Use minimum 32 characters:
```bash
# Generate secure secret
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
# or
openssl rand -hex 32
```

### Secrets in Version Control

**Problem:** Committed `.env` with real secrets

**Fix:**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".dev.vars" >> .gitignore

# Remove from git history if committed
git rm --cached .env
```

### Platform Env Not Available

**Problem:** `env.VAR` is undefined in deployed app

**Fix:** Platform-specific setup:
- **Vercel:** Add via dashboard or `vercel env add`
- **Cloudflare:** Add via `wrangler secret put` or dashboard
- **Docker:** Check `environment:` or `env_file:` in compose

### Wrong Fallback in Production

**Problem:** Using dev defaults in production

**Fix:** Fail fast instead of fallback:
```typescript
app: (env) => {
  if (!env.JWT_SECRET && env.NODE_ENV === "production") {
    throw new Error("JWT_SECRET required in production");
  }
  return {
    auth: {
      jwt: { secret: env.JWT_SECRET ?? "dev-only" },
    },
  };
},
```

## DOs and DON'Ts

**DO:**
- Use `.env.example` as template (no real values)
- Generate JWT_SECRET with crypto-safe randomness
- Use platform-specific secret management in production
- Validate required secrets on app start
- Use `syncSecrets` to keep `.env.example` updated

**DON'T:**
- Commit `.env` with real secrets
- Use weak or short JWT secrets
- Hardcode secrets in config files
- Use same secrets across environments
- Log env vars containing secrets

## Related Skills

- **bknd-local-setup** - Initial project setup
- **bknd-setup-auth** - Configure authentication
- **bknd-oauth-setup** - OAuth provider configuration
- **bknd-storage-config** - Storage adapter configuration
- **bknd-production-config** - Production configuration
- **bknd-deploy-hosting** - Deployment options
