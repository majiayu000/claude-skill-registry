---
name: infra-config-setup-env
description: Environment configuration, Zod validation
---

# Environment Management

> **Quick Guide:** Per-app .env files. Framework-specific prefixes (`NEXT_PUBLIC_*` for Next.js, `VITE_*` for Vite). Zod validation at startup. Maintain .env.example templates. Never commit secrets (.gitignore). Environment-based feature flags.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST validate ALL environment variables with Zod at application startup)**

**(You MUST use framework-specific prefixes for client-side variables - `NEXT_PUBLIC_*` for Next.js, `VITE_*` for Vite)**

**(You MUST maintain .env.example templates with ALL required variables documented)**

**(You MUST never commit secrets to version control - use .env.local and CI secrets)**

**(You MUST use per-app .env files - NOT root-level .env files)**

</critical_requirements>

---

**Auto-detection:** Environment variables, .env files, Zod validation, t3-env, @t3-oss/env, secrets management, `NEXT_PUBLIC_` prefix, `VITE_` prefix, feature flags, z.stringbool

**When to use:**

- Setting up Zod validation for type-safe environment variables at startup
- Managing per-app .env files with framework-specific prefixes
- Securing secrets (never commit, use .env.local and CI secrets)
- Implementing environment-based feature flags

**When NOT to use:**

- Runtime configuration changes (use an external feature flag service)
- User-specific settings (use database or user preferences)
- Frequently changing values (use configuration API or database)
- Complex A/B testing with gradual rollouts (use a dedicated feature flag service)

**Key patterns covered:**

- Per-app .env files (not root-level, prevents conflicts)
- Zod validation at startup for type safety and early failure
- T3 Env pattern for Next.js/Vite projects (recommended)
- Framework-specific prefixes (`NEXT_PUBLIC_*` for client, `VITE_*` for Vite client)
- .env.example templates for documentation and onboarding

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [examples/core.md](examples/core.md) - Essential patterns (per-app .env, Zod validation)
  - [examples/t3-env.md](examples/t3-env.md) - T3 Env pattern for Next.js/Vite (recommended)
  - [examples/naming-and-templates.md](examples/naming-and-templates.md) - Framework prefixes, .env.example
  - [examples/security-and-secrets.md](examples/security-and-secrets.md) - Secret management
  - [examples/feature-flags-and-config.md](examples/feature-flags-and-config.md) - Feature flags, centralized config
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Environment management follows the principle that **configuration is code** -- it should be validated, typed, and versioned. The system uses per-app .env files with framework-specific prefixes, Zod validation at startup, and strict security practices to prevent secret exposure.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Per-App Environment Files

Each app/package has its own `.env` file to prevent conflicts and clarify ownership.

#### File Structure

```
apps/
├── client-next/
│   ├── .env                    # Local development (NEXT_PUBLIC_API_URL)
│   └── .env.production         # Production overrides
├── client-react/
│   ├── .env                    # Local development
│   └── .env.production         # Production overrides
└── server/
    ├── .env                    # Local server config
    ├── .env.example            # Template for new developers
    └── .env.local.example      # Local overrides template

packages/
├── api/
│   └── .env                    # API package config
└── api-mocks/
    └── .env                    # Mock server config
```

#### File Types and Purpose

1. **`.env`** - Default development values (committed for apps, gitignored for sensitive packages)
2. **`.env.example`** - Documentation template (committed, shows all required variables)
3. **`.env.local`** - Local developer overrides (gitignored, takes precedence over `.env`)
4. **`.env.production`** - Production configuration (committed or in CI secrets)
5. **`.env.local.example`** - Local override template (committed)

#### Loading Order and Precedence

**Next.js loading order (highest to lowest priority):**

1. `process.env` (already set in environment)
2. `.env.$(NODE_ENV).local` (e.g., `.env.production.local`)
3. `.env.local` (not loaded when `NODE_ENV=test`)
4. `.env.$(NODE_ENV)` (e.g., `.env.production`)
5. `.env`

**Vite loading order:**

1. `.env.[mode].local` (e.g., `.env.production.local`)
2. `.env.[mode]` (e.g., `.env.production`)
3. `.env.local`
4. `.env`

**Exception:** Shared variables can go in your build tool's env configuration for cache invalidation

See [examples/core.md](examples/core.md) for complete code examples.

---

### Pattern 2: Type-Safe Environment Variables with Zod

Validate environment variables at application startup using Zod schemas. Define a schema, parse at startup, export a typed `env` object.

```typescript
// lib/env.ts
const envSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_API_TIMEOUT: z.coerce.number().default(DEFAULT_API_TIMEOUT_MS),
  VITE_ENABLE_ANALYTICS: z.stringbool().default(false), // Zod 4+ (NOT z.coerce.boolean())
});
export const env = envSchema.parse(import.meta.env);
```

**Key gotchas:**

- `z.coerce.boolean()` converts `"false"` to `true` (string is truthy) - always use `z.stringbool()` instead
- Use `error.issues` (not `error.errors`) for Zod 4 error handling

> **Note:** For Next.js/Vite projects, consider T3 Env (`@t3-oss/env-nextjs` or `@t3-oss/env-core`) for client/server variable separation and build-time validation. See [examples/t3-env.md](examples/t3-env.md).

See [examples/core.md](examples/core.md) for complete good/bad comparisons.

---

### Pattern 3: Framework-Specific Naming Conventions

Use framework-specific prefixes for client-side variables and SCREAMING_SNAKE_CASE for all environment variables.

#### Mandatory Conventions

1. **SCREAMING_SNAKE_CASE** - All environment variables use uppercase with underscores
2. **Descriptive names** - Variable names clearly indicate purpose
3. **Framework prefixes** - Use `NEXT_PUBLIC_*` (Next.js) or `VITE_*` (Vite) for client-side variables

#### Framework Prefixes

**Next.js:**

- `NEXT_PUBLIC_*` - Client-side accessible (embedded in bundle) - use for API URLs, public keys, feature flags
- No prefix - Server-side only (database URLs, secret keys, API tokens)

**Vite:**

- `VITE_*` - Client-side accessible (embedded in bundle) - use for API URLs, public configuration
- No prefix - Build-time only (not exposed to client)

**Node.js/Server:**

- `NODE_ENV` - Standard environment (`development`, `production`, `test`)
- `PORT` - Server port number
- No prefix - All variables available server-side

See [examples/naming-and-templates.md](examples/naming-and-templates.md) for complete code examples with good/bad comparisons.

</patterns>

---

<integration>

## Integration Guide

**Core dependencies:**

- **Zod** (v4+): Runtime validation and type inference for environment variables
- **T3 Env** (`@t3-oss/env-nextjs`, `@t3-oss/env-core`): Recommended wrapper for client/server separation

**Framework support:**

- **Next.js**: Automatic .env file loading with `NEXT_PUBLIC_*` prefix for client-side
- **Vite**: Automatic .env file loading with `VITE_*` prefix for client-side

**Monorepo considerations:**

- Declare shared env vars in your build tool's env configuration for cache invalidation
- Use per-app .env files even in monorepos to prevent conflicts

**Replaces / Conflicts with:**

- Hardcoded configuration values (use env vars instead)
- Runtime feature flag services for simple boolean flags (use env vars first, upgrade when needing gradual rollouts)

</integration>

---

<decision_framework>

## Decision Framework

See [reference.md](reference.md) for complete decision frameworks including environment configuration and feature flag decisions.

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Committing secrets to version control (.env files with real credentials)
- Using environment variables directly without Zod validation (causes runtime errors)
- Using `NEXT_PUBLIC_*` or `VITE_*` prefix for secrets (embeds in client bundle)

**Medium Priority Issues:**

- Missing .env.example documentation (poor onboarding experience)
- Using production secrets in development (security risk)
- Root-level .env in monorepo (causes conflicts)

**Gotchas:**

- Next.js/Vite embed prefixed variables at **build time**, not runtime - requires rebuild to change
- Environment variables are strings - use `z.coerce.number()` for numbers, use `z.stringbool()` for booleans (Zod 4+)
- **CRITICAL:** `z.coerce.boolean()` converts "false" to `true` (string is truthy) - use `z.stringbool()` (Zod 4+) instead
- Empty string env vars are NOT `undefined` - use T3 Env's `emptyStringAsUndefined: true` option
- Monorepo build tool caches may NOT be invalidated by env changes unless declared in the tool's env configuration

See [reference.md](reference.md) for complete RED FLAGS, anti-patterns, and checklists.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST validate ALL environment variables with Zod at application startup)**

**(You MUST use framework-specific prefixes for client-side variables - `NEXT_PUBLIC_*` for Next.js, `VITE_*` for Vite)**

**(You MUST maintain .env.example templates with ALL required variables documented)**

**(You MUST never commit secrets to version control - use .env.local and CI secrets)**

**(You MUST use per-app .env files - NOT root-level .env files)**

**Failure to follow these rules will cause runtime errors, security vulnerabilities, and configuration confusion.**

</critical_reminders>
