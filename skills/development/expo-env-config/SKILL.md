---
name: expo-env-config
description: This skill should be used when creating, modifying, or accessing environment variables in this Expo/React Native codebase. It enforces type-safe, validated environment configuration using Zod schemas. Use this skill when adding new environment variables, setting up env validation, or writing code that reads from process.env.
---

# Expo Environment Configuration

## Overview

This skill enforces type-safe, validated environment variable management for Expo/React Native using Zod schemas. Environment variables are validated at build time and provide full TypeScript inference, regardless of their source (`.env` files, EAS Build secrets, CI/CD pipelines, or command-line exports).

## Why This Pattern?

Unlike NestJS's `@nestjs/config`, Expo has no official type-safe env solution. The Zod validation pattern provides:

1. **Type safety** - Full TypeScript inference via `z.infer<typeof schema>`
2. **Build-time validation** - Fails fast with clear error messages before deployment
3. **Source agnostic** - Works with `.env`, EAS secrets, CI variables
4. **Testing support** - Easy mocking via module aliases

## Core Pattern

### Environment Schema (`src/lib/env.ts`)

```typescript
import { z } from "zod";

/**
 * Environment variable schema with Zod validation.
 * Variables are validated at module load time.
 */
const envSchema = z.object({
  // Required variables
  EXPO_PUBLIC_API_URL: z.string().url(),
  EXPO_PUBLIC_APP_ENV: z.enum(["development", "staging", "production"]),

  // Optional variables with defaults
  EXPO_PUBLIC_SENTRY_DSN: z.string().optional(),
  EXPO_PUBLIC_FEATURE_FLAG: z
    .string()
    .transform(v => v === "true")
    .default("false"),
});

/**
 * Validated environment configuration.
 * Throws at module load if validation fails.
 */
export const env = envSchema.parse(process.env);

/**
 * Type-safe environment configuration.
 */
export type Env = z.infer<typeof envSchema>;
```

### Usage in Components/Hooks

```typescript
import { env } from "@/lib/env";

// Full autocomplete and type safety
const apiUrl = env.EXPO_PUBLIC_API_URL; // string
const isDev = env.EXPO_PUBLIC_APP_ENV === "development"; // boolean
```

## Build-Time Validation (`app.config.ts`)

For variables needed during the build process, validate in `app.config.ts`:

```javascript
// app.config.ts
const { z } = require("zod");

const buildEnvSchema = z.object({
  EXPO_PUBLIC_API_URL: z.string().url(),
  EXPO_PUBLIC_APP_ENV: z.enum(["development", "staging", "production"]),
  // Build-only secrets (not exposed to client)
  SENTRY_AUTH_TOKEN: z.string().optional(),
});

// Throws during `eas build` if invalid
const env = buildEnvSchema.parse(process.env);

module.exports = {
  name: "MyApp",
  slug: "my-app",
  extra: {
    apiUrl: env.EXPO_PUBLIC_API_URL,
    appEnv: env.EXPO_PUBLIC_APP_ENV,
  },
};
```

## Variable Sources

Environment variables arrive in `process.env` from multiple sources:

| Source | When Available | How Set |
|--------|----------------|---------|
| `.env.local` | Local dev | Expo CLI auto-loads |
| `.env.development` | Local dev | Copied to `.env.local` via npm script |
| `eas.json` env | EAS Build | `build.production.env` section |
| EAS Secrets | EAS Build | `eas secret:create` |
| CI Variables | CI builds | GitHub Actions / GitLab CI settings |

The Zod pattern validates `process.env` directly - it doesn't care how variables got there.

## Testing Pattern

### Jest Setup (`jest.setup.local.ts`)

```typescript
// Mock the env module for all tests
jest.mock("@/lib/env", () => ({
  env: {
    EXPO_PUBLIC_API_URL: "https://test.example.com",
    EXPO_PUBLIC_APP_ENV: "development",
    EXPO_PUBLIC_SENTRY_DSN: undefined,
    EXPO_PUBLIC_FEATURE_FLAG: false,
  },
}));
```

### Override in Specific Tests

```typescript
import { env } from "@/lib/env";

jest.mock("@/lib/env");

describe("ProductionFeature", () => {
  beforeEach(() => {
    (env as jest.Mocked<typeof env>).EXPO_PUBLIC_APP_ENV = "production";
  });

  it("should behave differently in production", () => {
    // Test production-specific behavior
  });
});
```

## ESLint Enforcement

This pattern is enforced by ESLint's `no-restricted-syntax` rule in `eslint.config.mjs`:

```javascript
"no-restricted-syntax": [
  "error",
  {
    selector: "MemberExpression[object.name='process'][property.name='env']",
    message: "Direct process.env access is forbidden. Import { env } from '@/lib/env' instead.",
  },
],
```

**Exceptions** (files allowed to use `process.env`):
- `lib/env.ts` - The env validation module itself
- `app.config.ts` - Expo build config
- `codegen.ts` - GraphQL codegen config
- `playwright.config.ts` - E2E test config
- `lighthouserc.js` - Lighthouse CI config

## Core Rules

### 1. Always Prefix with EXPO_PUBLIC_

Variables without this prefix are not available in client code:

```typescript
// CORRECT - available in client
EXPO_PUBLIC_API_URL=https://api.example.com

// INCORRECT - only available at build time
API_URL=https://api.example.com
```

### 2. Never Access process.env Directly

Always use the validated `env` object:

```typescript
// CORRECT - type-safe, validated
import { env } from "@/lib/env";
const url = env.EXPO_PUBLIC_API_URL;

// INCORRECT - untyped, unvalidated
const url = process.env.EXPO_PUBLIC_API_URL;
```

### 3. Validate Early, Fail Fast

Validation happens at module load. If a required variable is missing, the app fails immediately with a clear error rather than at runtime.

### 4. Use Transforms for Non-String Types

Environment variables are always strings. Use Zod transforms:

```typescript
const envSchema = z.object({
  // Boolean from string
  EXPO_PUBLIC_DEBUG: z
    .string()
    .transform(v => v === "true")
    .default("false"),

  // Number from string
  EXPO_PUBLIC_TIMEOUT_MS: z
    .string()
    .transform(v => parseInt(v, 10))
    .default("5000"),

  // Array from comma-separated string
  EXPO_PUBLIC_ALLOWED_HOSTS: z
    .string()
    .transform(v => v.split(",").map(s => s.trim()))
    .default(""),
});
```

### 5. Separate Client vs Build-Only Variables

Keep sensitive build-time variables out of the client schema:

```typescript
// Client variables (embedded in JS bundle)
const clientSchema = z.object({
  EXPO_PUBLIC_API_URL: z.string().url(),
});

// Build-only variables (NOT in bundle)
const buildSchema = z.object({
  SENTRY_AUTH_TOKEN: z.string(),
  EAS_PROJECT_ID: z.string(),
});
```

## File Organization

```
src/
  lib/
    env.ts              # Main env schema and exports
app.config.ts           # Build-time validation (if needed)
.env.localhost          # Local development (git-ignored)
.env.development        # Development environment
.env.staging            # Staging environment
.env.production         # Production environment
```

## Detailed Reference

For comprehensive patterns, transforms, and testing examples:

- **[references/validation-patterns.md](references/validation-patterns.md)** - Advanced Zod schemas, transforms, and refinements

## Anti-Patterns to Avoid

### Never use process.env directly in components

```typescript
// WRONG - untyped, could be undefined
const Component = () => {
  const url = process.env.EXPO_PUBLIC_API_URL;
  // url is string | undefined, no validation
};

// CORRECT - validated and typed
import { env } from "@/lib/env";
const Component = () => {
  const url = env.EXPO_PUBLIC_API_URL;
  // url is string, guaranteed to be valid URL
};
```

### Never skip validation for "simple" variables

```typescript
// WRONG - skipping validation
export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:3000";

// CORRECT - always validate
const envSchema = z.object({
  EXPO_PUBLIC_API_URL: z.string().url().default("http://localhost:3000"),
});
export const { EXPO_PUBLIC_API_URL: API_URL } = envSchema.parse(process.env);
```

### Never store secrets in EXPO_PUBLIC_ variables

```typescript
// WRONG - secrets exposed in client bundle
EXPO_PUBLIC_API_SECRET=super-secret-key

// CORRECT - secrets only at build time, passed securely
SENTRY_AUTH_TOKEN=secret  # Build-only, not in bundle
```

## Validation Checklist

When adding or modifying environment variables:

- [ ] Variable is prefixed with `EXPO_PUBLIC_` (if needed in client code)
- [ ] Variable is added to the Zod schema in `src/lib/env.ts`
- [ ] Appropriate Zod type/transform is used (url, enum, boolean transform, etc.)
- [ ] Default value provided for optional variables
- [ ] Jest mock updated in `jest.setup.local.ts`
- [ ] Variable documented in `.env.example` or `.env.development`
- [ ] Sensitive values use EAS Secrets, not `.env` files
