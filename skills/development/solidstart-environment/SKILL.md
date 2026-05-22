---
name: solidstart-environment
description: "SolidStart environment variables: VITE_ prefix for public variables, process.env for server-only, .env files, type safety with env.d.ts, runtime vs build-time variables."
metadata:
  globs:
    - "**/.env*"
    - "**/env.d.ts"
    - "**/*env*"
---

# SolidStart Environment Variables

Complete guide to managing environment variables in SolidStart. Understand the difference between public (client-side) and private (server-only) variables.

## Public Environment Variables

Public variables are safe to expose to client-side code. They must be prefixed with `VITE_` and are injected during build time.

### Basic Setup

Create a `.env` file in the project root:

```env
VITE_API_URL=https://api.example.com
VITE_APP_NAME=My App
VITE_USER_ID=123
```

Access in client code:

```tsx
function MyComponent() {
  return (
    <div>
      <h2>API: {import.meta.env.VITE_API_URL}</h2>
      <p>App: {import.meta.env.VITE_APP_NAME}</p>
    </div>
  );
}
```

**Key points:**
- Must use `VITE_` prefix
- Injected at build time
- Available in client code
- Access via `import.meta.env.VITE_*`

### Type Safety

Create `env.d.ts` for TypeScript autocomplete:

```typescript
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_NAME: string;
  readonly VITE_USER_ID: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

Now TypeScript will autocomplete and type-check your environment variables.

## Private Environment Variables

Private variables are server-only and should NOT use the `VITE_` prefix. Access them via `process.env` in server code.

### Basic Setup

```env
DB_HOST=somedb://192.110.0
DB_PASSWORD=super_secret_password_hash
API_SECRET_KEY=secret123
```

Access in server code:

```tsx
"use server";

export async function getData() {
  const client = new DB({
    host: process.env.DB_HOST,
    password: process.env.DB_PASSWORD,
  });
  
  // Use private variables
  const apiKey = process.env.API_SECRET_KEY;
  
  return client.query();
}
```

**Key points:**
- NO `VITE_` prefix
- Only accessible in server code
- Use `process.env` to access
- Not exposed to client

### Type Safety for Server Variables

Add to `env.d.ts`:

```typescript
declare namespace NodeJS {
  interface ProcessEnv {
    readonly DB_HOST: string;
    readonly DB_PASSWORD: string;
    readonly API_SECRET_KEY: string;
  }
}
```

## Environment Files

### Development (.env)

```env
VITE_API_URL=http://localhost:3000
DB_HOST=localhost
DB_PASSWORD=dev_password
```

### Production (.env.production)

```env
VITE_API_URL=https://api.production.com
DB_HOST=prod-db.example.com
DB_PASSWORD=prod_secret_password
```

### Local Override (.env.local)

```env
# Overrides .env, not committed to git
VITE_API_URL=http://localhost:4000
```

**File priority (highest to lowest):**
1. `.env.local` (always loaded, ignored by git)
2. `.env.[mode].local` (e.g., `.env.production.local`)
3. `.env.[mode]` (e.g., `.env.production`)
4. `.env`

## Security Best Practices

### ❌ Never Expose Secrets

```env
# ❌ WRONG - This will be exposed to client!
VITE_DB_PASSWORD=secret123

# ✅ CORRECT - No VITE_ prefix
DB_PASSWORD=secret123
```

### ✅ Verify Client Exposure

```tsx
// Check what's exposed
console.log(import.meta.env.VITE_SECRET_KEY); // ✅ Exposed (if prefixed)
console.log(import.meta.env.DB_PASSWORD);     // ✅ undefined (safe)
```

### ✅ Use Server Actions for Secrets

```tsx
// ❌ WRONG - Exposes API key to client
function ClientComponent() {
  const apiKey = import.meta.env.VITE_API_KEY; // Exposed!
  fetch(`/api?key=${apiKey}`);
}

// ✅ CORRECT - Keep secret on server
"use server";
export async function fetchData() {
  const apiKey = process.env.API_SECRET_KEY; // Server-only
  return fetch(`/api?key=${apiKey}`);
}
```

## Runtime vs Build-Time

### Build-Time Variables (VITE_*)

```tsx
// Replaced at build time
const apiUrl = import.meta.env.VITE_API_URL;
// After build: const apiUrl = "https://api.example.com";
```

**Characteristics:**
- Replaced during build
- Different values per build
- Cannot change at runtime
- Bundled into client code

### Runtime Variables (Server)

```tsx
// Accessed at runtime
const dbHost = process.env.DB_HOST;
// Value from environment at runtime
```

**Characteristics:**
- Accessed at runtime
- Can change without rebuild
- Server-only access
- Not bundled

## Common Patterns

### API Configuration

```env
# .env
VITE_API_URL=http://localhost:3000
VITE_API_TIMEOUT=5000
```

```tsx
// Client code
const apiUrl = import.meta.env.VITE_API_URL;
const timeout = Number(import.meta.env.VITE_API_TIMEOUT) || 5000;

fetch(`${apiUrl}/data`, { signal: AbortSignal.timeout(timeout) });
```

### Database Configuration

```env
# .env (server-only)
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
```

```tsx
// Server code
"use server";

export async function connectDB() {
  const db = new Database(process.env.DATABASE_URL);
  const redis = new Redis(process.env.REDIS_URL);
  return { db, redis };
}
```

### Feature Flags

```env
# .env
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false
```

```tsx
// Client code
const enableAnalytics = import.meta.env.VITE_ENABLE_ANALYTICS === "true";
const enableDebug = import.meta.env.VITE_ENABLE_DEBUG === "true";

if (enableAnalytics) {
  initAnalytics();
}

if (enableDebug) {
  console.log("Debug mode enabled");
}
```

### Environment-Specific Config

```tsx
// config.ts
export const config = {
  apiUrl: import.meta.env.VITE_API_URL || "http://localhost:3000",
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
  mode: import.meta.env.MODE,
};
```

## TypeScript Setup

Complete `env.d.ts` example:

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  // Public variables (VITE_ prefix)
  readonly VITE_API_URL: string;
  readonly VITE_APP_NAME: string;
  readonly VITE_ENABLE_ANALYTICS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare namespace NodeJS {
  interface ProcessEnv {
    // Server-only variables (no VITE_ prefix)
    readonly DATABASE_URL: string;
    readonly DB_PASSWORD: string;
    readonly API_SECRET_KEY: string;
    readonly REDIS_URL: string;
  }
}
```

## Vite Built-in Variables

Vite provides built-in environment variables:

```tsx
import.meta.env.MODE          // "development" | "production"
import.meta.env.DEV           // true in dev, false in prod
import.meta.env.PROD          // false in dev, true in prod
import.meta.env.SSR           // true when running in SSR
import.meta.env.BASE_URL      // Base public path
```

## Deployment Considerations

### Platform-Specific Setup

Different platforms handle environment variables differently:

**Vercel:**
- Set in dashboard or `vercel.json`
- Automatically available as `process.env`

**Netlify:**
- Set in dashboard or `netlify.toml`
- Available as `process.env`

**Node.js:**
- Use `.env` files with dotenv
- Or set in system environment

### Build-Time vs Runtime

```tsx
// Build-time (VITE_*)
const apiUrl = import.meta.env.VITE_API_URL;
// Set before build, bundled into code

// Runtime (server)
const dbUrl = process.env.DATABASE_URL;
// Set at runtime, not bundled
```

## Best Practices

1. **Always prefix public variables with `VITE_`:**
   - Prevents accidental exposure
   - Clear distinction between public/private

2. **Never use `VITE_` for secrets:**
   - Secrets should be server-only
   - Use `process.env` without prefix

3. **Use TypeScript for type safety:**
   - Define in `env.d.ts`
   - Get autocomplete and type checking

4. **Use `.env.local` for local overrides:**
   - Not committed to git
   - Overrides other env files

5. **Document required variables:**
   - List in README
   - Provide `.env.example` template

6. **Validate environment variables:**
   ```tsx
   const requiredEnv = {
     apiUrl: import.meta.env.VITE_API_URL,
   };
   
   if (!requiredEnv.apiUrl) {
     throw new Error("VITE_API_URL is required");
   }
   ```

## Summary

- **Public variables**: `VITE_` prefix, `import.meta.env`, client-accessible
- **Private variables**: No prefix, `process.env`, server-only
- **Type safety**: Define in `env.d.ts`
- **Security**: Never expose secrets with `VITE_` prefix
- **Build-time**: VITE_ variables replaced during build
- **Runtime**: Server variables accessed at runtime

