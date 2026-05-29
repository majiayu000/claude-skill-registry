---
name: env-config-validator
description: Validate environment configuration files, detect missing or misconfigured variables, and generate typed env schemas. Use when asked to validate env files, check environment config, generate .env.example, audit env variables, or create typed env validation.
---

# Env Config Validator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Read the `.env` file (and `.env.local`, `.env.development`, `.env.production` if they exist).
2. Scan the codebase for `process.env.*` and `import.meta.env.*` references.
3. Compare: find missing variables, unused variables, and misconfigurations.
4. Detect security issues: sensitive values, duplicates, invalid formats.
5. Generate or update `.env.example` and optionally a typed env validation schema.

## Detection Rules

### Missing Variables

Scan all `.ts`, `.tsx`, `.js`, `.jsx` files for `process.env.VARIABLE_NAME` patterns. Flag any variable referenced in code but absent from `.env`.

```
🔴 MISSING: DATABASE_URL
   Referenced in: lib/prisma.ts:3, lib/db.ts:7
   Not defined in any .env file

🔴 MISSING: NEXTAUTH_SECRET
   Referenced in: lib/auth.ts:12
   Not defined in any .env file
```

### Unused Variables

Variables defined in `.env` but never referenced in code.

```
🟡 UNUSED: LEGACY_API_URL
   Defined in: .env:14
   No references found in codebase
```

Exclude from this check: variables used by frameworks implicitly (e.g., `PORT`, `NODE_ENV`, `HOSTNAME`, `NEXT_PUBLIC_*` referenced in client code).

### Empty Values

```
🟡 EMPTY: SMTP_HOST=
   Defined in: .env:22
   Variable exists but has no value
```

### Duplicate Definitions

```
🔴 DUPLICATE: NEXT_PUBLIC_API_URL
   Line 5: NEXT_PUBLIC_API_URL=https://api.example.com
   Line 18: NEXT_PUBLIC_API_URL=https://staging.example.com
   Last definition wins — likely unintentional
```

### Invalid Format

```
🟡 FORMAT: PORT=three thousand
   Expected: numeric value
   Suggested: PORT=3000

🟡 FORMAT: DEBUG=yes
   Expected: boolean-like value (true/false, 1/0)
   Suggested: DEBUG=true
```

### Security Issues

Flag variables that appear to contain real secrets (not placeholders):

```
🔴 SECRET EXPOSED: STRIPE_SECRET_KEY=sk_live_abc123...
   This looks like a real API key. Ensure .env is in .gitignore.

🔴 SECRET EXPOSED: DATABASE_URL=postgresql://admin:realpassword@prod-db:5432/app
   Connection string contains credentials.
```

Check that `.gitignore` includes `.env` and `.env.local`. Warn if it does not.

## Generate .env.example

Produce a `.env.example` file with all required variables, replacing real values with descriptive placeholders.

```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"

# Authentication (generate with: openssl rand -base64 32)
NEXTAUTH_SECRET="your-nextauth-secret-here"
NEXTAUTH_URL="http://localhost:3000"

# External APIs
STRIPE_SECRET_KEY="sk_test_..."
STRIPE_PUBLISHABLE_KEY="pk_test_..."

# Email
SMTP_HOST="smtp.example.com"
SMTP_PORT="587"
SMTP_USER="your-email@example.com"
SMTP_PASS="your-smtp-password"

# Public (exposed to browser)
NEXT_PUBLIC_API_URL="http://localhost:3000/api"
NEXT_PUBLIC_APP_NAME="My App"
```

Rules for placeholder generation:
- URLs: use `http://localhost:*` or `https://example.com`
- Secrets/keys: use `your-*-here` or the service's test key prefix (e.g., `sk_test_...`)
- Booleans: use `true` or `false`
- Numbers: use the typical default (e.g., `3000` for PORT)
- Connection strings: use `protocol://user:password@localhost:port/dbname`

## Generate Typed Env Schema

### T3 Env Pattern (Next.js)

```typescript
// env.ts
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NEXTAUTH_SECRET: z.string().min(1),
    NEXTAUTH_URL: z.string().url().optional(),
    STRIPE_SECRET_KEY: z.string().startsWith("sk_"),
    SMTP_HOST: z.string().min(1),
    SMTP_PORT: z.coerce.number().int().min(1).max(65535),
    SMTP_USER: z.string().email(),
    SMTP_PASS: z.string().min(1),
    NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
    NEXT_PUBLIC_APP_NAME: z.string().min(1),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
    NEXTAUTH_URL: process.env.NEXTAUTH_URL,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    SMTP_HOST: process.env.SMTP_HOST,
    SMTP_PORT: process.env.SMTP_PORT,
    SMTP_USER: process.env.SMTP_USER,
    SMTP_PASS: process.env.SMTP_PASS,
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_APP_NAME: process.env.NEXT_PUBLIC_APP_NAME,
  },
});
```

### Plain Zod Pattern (non-Next.js)

```typescript
// env.ts
import { z } from "zod";

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  PORT: z.coerce.number().int().default(3000),
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  API_KEY: z.string().min(1),
});

export const env = envSchema.parse(process.env);
export type Env = z.infer<typeof envSchema>;
```

## Naming Convention Audit

Flag variables that don't follow standard prefixes:

| Prefix | Purpose |
|---|---|
| `DATABASE_` | Database configuration |
| `NEXT_PUBLIC_` | Client-exposed variables (Next.js) |
| `NEXTAUTH_` | NextAuth.js / Auth.js configuration |
| `AUTH_` | Authentication-related |
| `SMTP_` / `EMAIL_` | Email service |
| `STRIPE_` / `PAYMENT_` | Payment provider |
| `AWS_` / `S3_` | AWS services |
| `REDIS_` | Redis configuration |

```
🔵 NAMING: apiKey
   Convention: use SCREAMING_SNAKE_CASE with descriptive prefix
   Suggested: EXTERNAL_API_KEY
```

## Output Format

```
## Env Validation Report

### Summary
| Category | Count |
|----------|-------|
| 🔴 Missing | N |
| 🔴 Security | N |
| 🟡 Unused | N |
| 🟡 Format | N |
| 🔵 Naming | N |

### Findings

[Grouped by severity, each with file location and recommendation]

### Generated Files
- `.env.example` — [created/updated]
- `env.ts` — [created/updated] (typed validation schema)
```

## Auto-Fix

After identifying issues, automatically generate: (1) an updated `.env.example` with all missing variables added with placeholder values, (2) a typed env schema file using the configured validation library. Ask the user before overwriting existing files.

## Reference

See [references/env-patterns.md](references/env-patterns.md) for T3 env setup details and common variable catalogs.
