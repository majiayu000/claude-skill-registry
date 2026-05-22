---
name: infra-env
description: Environment variable conventions and security practices for Next.js projects. This skill should be used when setting up environment configuration, managing secrets, or establishing security patterns for a new project.
---

# Environment Variables Skill

Conventions and security practices for managing environment variables in Next.js projects.

## When to Use This Skill

- Setting up a new project's environment configuration
- Adding new environment variables
- Reviewing security of environment handling
- Creating `.env.example` templates
- Troubleshooting environment issues

## Core Principles

1. **Never commit secrets** - `.env*` files with real values stay out of git
2. **Document with examples** - `.env.example` shows structure without values
3. **Prefix client-safe vars** - Only `NEXT_PUBLIC_*` reaches the browser
4. **Validate at startup** - Fail fast if required vars are missing
5. **Use typed configuration** - Type-safe access to environment

## File Hierarchy

| File | Purpose | Git? |
|------|---------|------|
| `.env` | Default values (shared) | Optional |
| `.env.local` | Local overrides (secrets) | Never |
| `.env.development` | Dev-specific defaults | Optional |
| `.env.production` | Prod defaults (no secrets) | Optional |
| `.env.example` | Template for developers | Always |

**Load order** (later overrides earlier):
1. `.env`
2. `.env.local`
3. `.env.development` / `.env.production` (based on NODE_ENV)
4. `.env.development.local` / `.env.production.local`

## Standard .env.example

Create `.env.example` as documentation:

```bash
# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================
# Copy this file to .env.local and fill in the values
# NEVER commit .env.local to git
# =============================================================================

# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_APP_NAME=MyApp

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
# PostgreSQL connection string
# Format: postgres://USER:PASSWORD@HOST:PORT/DATABASE
DATABASE_URL=postgres://postgres:postgres@localhost:5432/myapp

# -----------------------------------------------------------------------------
# Authentication (Better Auth)
# -----------------------------------------------------------------------------
# Generate with: openssl rand -base64 32
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-here
BETTER_AUTH_URL=http://localhost:3000

# OAuth Providers (get from provider console)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# -----------------------------------------------------------------------------
# Third-Party Services (Optional)
# -----------------------------------------------------------------------------
# Analytics
# NEXT_PUBLIC_POSTHOG_KEY=
# NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com

# Email (Resend)
# RESEND_API_KEY=

# Storage (S3/R2/Minio)
# S3_BUCKET=
# S3_REGION=
# S3_ACCESS_KEY_ID=
# S3_SECRET_ACCESS_KEY=
# S3_ENDPOINT=

# -----------------------------------------------------------------------------
# Development Only
# -----------------------------------------------------------------------------
# Set to 'true' to enable debug features
# DEBUG=false
```

## Naming Conventions

### Server-Only Variables (Default)

```bash
# Database
DATABASE_URL=...

# Auth secrets
BETTER_AUTH_SECRET=...
GOOGLE_CLIENT_SECRET=...

# API keys
RESEND_API_KEY=...
OPENAI_API_KEY=...
```

### Client-Accessible Variables

**Must start with `NEXT_PUBLIC_`**:

```bash
# URLs and public identifiers
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_POSTHOG_KEY=phc_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_xxx
```

### Naming Style

- Use `SCREAMING_SNAKE_CASE`
- Be descriptive: `DATABASE_URL` not `DB`
- Group by service: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- Prefix third-party: `RESEND_API_KEY`, `STRIPE_SECRET_KEY`

## Type-Safe Environment

### Environment Validation

Create `src/lib/env.ts`:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  // Database
  DATABASE_URL: z.string().url(),
  
  // Auth
  BETTER_AUTH_SECRET: z.string().min(32),
  BETTER_AUTH_URL: z.string().url(),
  
  // OAuth (optional in development)
  GOOGLE_CLIENT_ID: z.string().optional(),
  GOOGLE_CLIENT_SECRET: z.string().optional(),
  GITHUB_CLIENT_ID: z.string().optional(),
  GITHUB_CLIENT_SECRET: z.string().optional(),
  
  // Public
  NEXT_PUBLIC_APP_URL: z.string().url(),
  
  // Node environment
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

// Validate at module load
const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('❌ Invalid environment variables:');
  console.error(parsed.error.flatten().fieldErrors);
  throw new Error('Invalid environment variables');
}

export const env = parsed.data;
```

### Usage

```typescript
import { env } from '@/lib/env';

// Type-safe access
const dbUrl = env.DATABASE_URL;
const isProduction = env.NODE_ENV === 'production';
```

### Client Environment

For client-side validation, create `src/lib/env-client.ts`:

```typescript
import { z } from 'zod';

const clientEnvSchema = z.object({
  NEXT_PUBLIC_APP_URL: z.string().url(),
  NEXT_PUBLIC_POSTHOG_KEY: z.string().optional(),
});

export const clientEnv = clientEnvSchema.parse({
  NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  NEXT_PUBLIC_POSTHOG_KEY: process.env.NEXT_PUBLIC_POSTHOG_KEY,
});
```

## Security Practices

### Never Do

```bash
# ❌ Secrets in .env.example with real values
API_KEY=sk_live_real_key_here

# ❌ Secrets with NEXT_PUBLIC_ prefix
NEXT_PUBLIC_DATABASE_URL=postgres://...

# ❌ Committing .env.local
# (should be in .gitignore)
```

### Always Do

```bash
# ✅ Placeholder values in .env.example
API_KEY=your-api-key-here

# ✅ Secrets stay server-only
DATABASE_URL=postgres://...

# ✅ Only public info gets NEXT_PUBLIC_
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### .gitignore

Ensure these are in `.gitignore`:

```
# Environment files with secrets
.env.local
.env.*.local
.env.development.local
.env.production.local

# Keep .env.example in git
!.env.example
```

### Secret Generation

```bash
# Generate random secret (32 bytes, base64)
openssl rand -base64 32

# Generate random secret (hex)
openssl rand -hex 32

# Generate UUID
uuidgen
```

## Per-Environment Configuration

### Development

```bash
# .env.development
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Production

```bash
# Set in deployment platform (Railway, Vercel, AWS)
# Never in files committed to git

NODE_ENV=production
DATABASE_URL=postgres://prod-user:prod-pass@prod-host:5432/prod-db
BETTER_AUTH_SECRET=production-secret-here
NEXT_PUBLIC_APP_URL=https://myapp.com
```

### Testing

```bash
# .env.test
NODE_ENV=test
DATABASE_URL=postgres://postgres:postgres@localhost:5432/myapp_test
```

## Platform-Specific Setup

### Local Development

1. Copy template: `cp .env.example .env.local`
2. Fill in values for local services
3. Start Docker services: `docker compose up -d`
4. Run app: `npm run dev`

### Railway

```bash
# Set via CLI
railway variables --set DATABASE_URL=postgres://...
railway variables --set BETTER_AUTH_SECRET=...

# Or use Railway dashboard
# Settings → Variables → Add Variable
```

### Vercel

```bash
# Set via CLI
vercel env add DATABASE_URL production
vercel env add BETTER_AUTH_SECRET production

# Or use Vercel dashboard
# Settings → Environment Variables
```

### AWS ECS

Use AWS Secrets Manager or Parameter Store:

```bash
# Store secret
aws secretsmanager create-secret \
  --name myapp/production/database-url \
  --secret-string "postgres://..."

# Reference in task definition
"secrets": [
  {
    "name": "DATABASE_URL",
    "valueFrom": "arn:aws:secretsmanager:region:account:secret:myapp/production/database-url"
  }
]
```

## Debugging Environment Issues

### Check What's Loaded

```typescript
// Temporary debug (remove before commit!)
console.log('DATABASE_URL exists:', !!process.env.DATABASE_URL);
console.log('NODE_ENV:', process.env.NODE_ENV);
```

### Common Issues

**Variable undefined at runtime:**
- Check file is named correctly (`.env.local` not `.env.local.txt`)
- Restart dev server after adding new variables
- Verify variable name matches exactly (case-sensitive)

**Client can't access variable:**
- Must have `NEXT_PUBLIC_` prefix
- Must rebuild after adding (for production builds)

**Wrong value used:**
- Check load order (`.env.local` overrides `.env`)
- Clear `.next` cache: `rm -rf .next`

**Works locally, fails in production:**
- Variables set in deployment platform?
- Names match exactly?
- No extra spaces or quotes in values?

## Checklist for New Projects

- [ ] Create `.env.example` with all variables
- [ ] Add `.env.local` to `.gitignore`
- [ ] Set up `src/lib/env.ts` for validation
- [ ] Document required vs optional variables
- [ ] Generate secrets with proper randomness
- [ ] Configure deployment platform variables
- [ ] Test with production-like values locally

## Quick Reference

| Variable Type | Prefix | Accessible In |
|---------------|--------|---------------|
| Server secret | None | Server only |
| Public config | `NEXT_PUBLIC_` | Server + Client |

| File | Committed? | Contains Secrets? |
|------|------------|-------------------|
| `.env.example` | Yes | No (placeholders) |
| `.env` | Optional | No |
| `.env.local` | No | Yes |
