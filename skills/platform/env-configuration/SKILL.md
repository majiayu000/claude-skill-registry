---
name: env-configuration
description: Apply when managing application configuration: environment variables, secrets management, and config validation.
version: 1.0.0
tokens: ~550
confidence: high
sources:
  - https://12factor.net/config
  - https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [configuration, environment, security, devops]
---

## When to Use

Apply when managing application configuration: environment variables, secrets management, and config validation.

## Patterns

### Pattern 1: Environment File Structure
```bash
# Source: https://12factor.net/config
# .env.example (commit this - template without secrets)
DATABASE_URL=postgres://user:pass@localhost:5432/myapp
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here
NODE_ENV=development

# .env.local (DO NOT COMMIT - actual secrets)
DATABASE_URL=postgres://prod:secret@prod-db:5432/myapp
API_KEY=sk_live_abc123

# .env.development / .env.production (environment defaults)
NEXT_PUBLIC_API_URL=http://localhost:3000/api
LOG_LEVEL=debug
```

### Pattern 2: Zod Validation at Startup
```typescript
// Source: https://zod.dev/
// src/config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url().optional(),
  API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

// Validate on import - fails fast at startup
export const env = envSchema.parse(process.env);

// Type-safe access throughout app
console.log(env.DATABASE_URL); // string (validated)
```

### Pattern 3: Next.js Environment Variables
```typescript
// Source: https://nextjs.org/docs/app/building-your-application/configuring/environment-variables
// NEXT_PUBLIC_ prefix = exposed to browser
// Without prefix = server-only

// .env.local
DATABASE_URL=secret         // Server only
NEXT_PUBLIC_API_URL=/api    // Available in browser

// Usage in code
// Server component/API route
const dbUrl = process.env.DATABASE_URL;

// Client component
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Pattern 4: Config Object Pattern
```typescript
// Source: Best practice pattern
// src/config/index.ts
import { env } from './env';

export const config = {
  isDev: env.NODE_ENV === 'development',
  isProd: env.NODE_ENV === 'production',

  server: {
    port: env.PORT,
    host: env.HOST || '0.0.0.0',
  },

  database: {
    url: env.DATABASE_URL,
    poolSize: env.DB_POOL_SIZE || 10,
  },

  auth: {
    jwtSecret: env.JWT_SECRET,
    tokenExpiry: '1h',
  },

  features: {
    enableBeta: env.ENABLE_BETA_FEATURES === 'true',
  },
} as const;

// Usage
import { config } from '@/config';
if (config.features.enableBeta) { /* ... */ }
```

### Pattern 5: .gitignore for Env Files
```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.development.local
.env.production.local

# Keep example
!.env.example
```

### Pattern 6: Required vs Optional
```typescript
// Source: https://zod.dev/
const envSchema = z.object({
  // Required - app won't start without these
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),

  // Optional with defaults
  PORT: z.coerce.number().default(3000),
  LOG_LEVEL: z.string().default('info'),

  // Optional without default
  SENTRY_DSN: z.string().url().optional(),

  // Conditional (required in production)
  REDIS_URL: z.string().url().optional()
    .refine(
      (val) => process.env.NODE_ENV !== 'production' || val,
      'REDIS_URL required in production'
    ),
});
```

## Anti-Patterns

- **Hardcoded secrets** - Always use environment variables
- **Secrets in .env.example** - Only placeholder values
- **No validation** - Fail fast with Zod at startup
- **NEXT_PUBLIC_ for secrets** - Exposes to browser

## Verification Checklist

- [ ] .env.example committed with placeholders
- [ ] .env.local in .gitignore
- [ ] Zod validation at app startup
- [ ] Secrets not prefixed with NEXT_PUBLIC_
- [ ] Required vs optional clearly defined
