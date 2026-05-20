---
name: better-auth
description: Skill for integrating Better Auth - comprehensive TypeScript authentication framework for Cloudflare D1, Next.js, Nuxt, and 15+ frameworks. Use when adding auth, encountering D1 adapter errors, or implementing OAuth/2FA/RBAC features.
keywords: better-auth, authentication, cloudflare d1 auth, drizzle orm auth, kysely auth, self-hosted auth, typescript auth, clerk alternative, auth.js alternative, social login, oauth providers, session management, jwt tokens, 2fa, two-factor, passkeys, webauthn, multi-tenant auth, organizations, teams, rbac, role-based access, google auth, github auth, microsoft auth, apple auth, magic links, email password, better-auth setup, drizzle d1, kysely d1, session serialization error, cors auth, d1 adapter, nextjs auth, nuxt auth, remix auth, sveltekit auth, expo auth, react native auth, postgresql auth, mongodb auth, mysql auth, stripe auth, api keys, sso, saml, scim, admin dashboard, background tasks, oauth 2.1, cli
license: MIT
metadata:
  version: "2.2.0"
  package_version: "1.4.9"
  last_verified: "2025-12-26"
  errors_prevented: 15
  templates_included: 4
  references_included: 26
---

# better-auth

**Status**: Production Ready
**Last Updated**: 2025-12-26
**Package**: `better-auth@1.4.9` (ESM-only)
**Dependencies**: Drizzle ORM or Kysely (required for D1)

---

## Quick Start (5 Minutes)

### Installation

**Option 1: Drizzle ORM (Recommended)**
```bash
bun add better-auth drizzle-orm drizzle-kit
```

**Option 2: Kysely**
```bash
bun add better-auth kysely @noxharmonium/kysely-d1
```

### ⚠️ v1.4.0+ Requirements

better-auth v1.4.0+ is **ESM-only**. Ensure:

**package.json**:
```json
{
  "type": "module"
}
```

**Upgrading from v1.3.x?** Load `references/migration-guide-1.4.0.md`

### ⚠️ CRITICAL: D1 Adapter Requirements

better-auth **DOES NOT** have a direct `d1Adapter()`. You **MUST** use either:
1. **Drizzle ORM** (recommended) - `drizzleAdapter()`
2. **Kysely** (alternative) - Kysely instance with D1Dialect

```typescript
// ❌ WRONG - This doesn't exist
import { d1Adapter } from 'better-auth/adapters/d1'

// ✅ CORRECT - Use Drizzle
import { drizzleAdapter } from 'better-auth/adapters/drizzle'
import { drizzle } from 'drizzle-orm/d1'
```

### Minimal Setup (Cloudflare Workers + Drizzle)

**1. Create D1 Database:**
```bash
wrangler d1 create my-app-db
```

**2. Define Schema** (`src/db/schema.ts`):
```typescript
import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const user = sqliteTable("user", {
  id: text().primaryKey(),
  name: text().notNull(),
  email: text().notNull().unique(),
  emailVerified: integer({ mode: "boolean" }).notNull().default(false),
  image: text(),
});

export const session = sqliteTable("session", {
  id: text().primaryKey(),
  userId: text().notNull().references(() => user.id, { onDelete: "cascade" }),
  token: text().notNull(),
  expiresAt: integer({ mode: "timestamp" }).notNull(),
});

// See references/database-schema.ts for complete schema
```

**3. Initialize Auth** (`src/auth.ts`):
```typescript
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { drizzle } from "drizzle-orm/d1";
import * as schema from "./db/schema";

export function createAuth(env: { DB: D1Database; BETTER_AUTH_SECRET: string }) {
  const db = drizzle(env.DB, { schema });

  return betterAuth({
    baseURL: env.BETTER_AUTH_URL,
    secret: env.BETTER_AUTH_SECRET,
    database: drizzleAdapter(db, { provider: "sqlite" }),
    emailAndPassword: { enabled: true },
  });
}
```

**4. Create Worker** (`src/index.ts`):
```typescript
import { Hono } from "hono";
import { createAuth } from "./auth";

const app = new Hono<{ Bindings: Env }>();

app.all("/api/auth/*", async (c) => {
  const auth = createAuth(c.env);
  return auth.handler(c.req.raw);
});

export default app;
```

**5. Deploy:**
```bash
bunx drizzle-kit generate
wrangler d1 migrations apply my-app-db --remote
wrangler deploy
```

---

## Decision Tree

**For code examples and syntax, always consult [better-auth.com/docs](https://better-auth.com/docs).**

```
Is this a new/empty project?
├─ YES → New project setup
│   1. Identify framework (Next.js, Nuxt, Workers, etc.)
│   2. Choose database (D1, PostgreSQL, MongoDB, MySQL)
│   3. Install better-auth + Drizzle/Kysely
│   4. Create auth.ts + auth-client.ts
│   5. Set up route handler (see Quick Start above)
│   6. Run migrations (Drizzle Kit for D1)
│   7. Add features via plugins (2FA, organizations, etc.)
│
└─ NO → Does project have existing auth?
    ├─ YES → Migration/enhancement
    │   • Audit current auth for gaps
    │   • Plan incremental migration
    │   • See references/framework-comparison.md for migration guides
    │
    └─ NO → Add auth to existing project
        1. Analyze project structure
        2. Install better-auth + adapter
        3. Create auth config (see Quick Start)
        4. Add route handler to existing routes
        5. Run schema migrations
        6. Integrate into existing pages/components
```

---

## Critical Rules

### MUST DO

✅ Use Drizzle/Kysely adapter (d1Adapter doesn't exist)
✅ Use Drizzle Kit for migrations (not `better-auth migrate`)
✅ Set BETTER_AUTH_SECRET via `wrangler secret put`
✅ Configure CORS with `credentials: true`
✅ Match OAuth callback URLs exactly (no trailing slash)
✅ Apply migrations to local D1 before `wrangler dev`
✅ Use camelCase column names in schema

### NEVER DO

❌ Use `d1Adapter` or `better-auth migrate` with D1
❌ Forget CORS credentials or mismatch OAuth URLs
❌ Use snake_case columns without CamelCasePlugin
❌ Skip local migrations or hardcode secrets
❌ Leave sendVerificationEmail unimplemented

### ⚠️ v1.4.0+ Breaking Changes

**ESM-only** (no CommonJS):
```json
// package.json required
{ "type": "module" }
```

**API Renames**:
- `forgetPassword` → `requestPasswordReset`
- POST `/account-info` → GET `/account-info`

**Callback Signatures**:
```typescript
// v1.3.x: request parameter
sendVerificationEmail: async ({ user, url, request }) => {}

// v1.4.0+: ctx parameter
sendVerificationEmail: async ({ user, url, ctx }) => {}
```

**Load `references/migration-guide-1.4.0.md` when upgrading from <1.4.0**

### New in v1.4.4-1.4.8

**Key additions since v1.4.3**:

- **Background Tasks** (v1.4.8): Global `backgroundTasks` config to defer email sending
- **New OAuth Providers**: Patreon (v1.4.8), Vercel (v1.4.3), Kick (v1.4.6) with refresh tokens
- **OAuth 2.1 Plugin** (v1.4.8): Standards-compliant OAuth implementation
- **CLI Tool** (v1.4.4): `better-auth` CLI with project scaffolding
- **SAML/SSO**: Clock skew validation (v1.4.7), InResponseTo, OIDC discovery
- **Admin Permissions** (v1.4.7): Admin role with granular user update permissions
- **ctx.isTrustedDomain** (v1.4.6): Helper for domain verification

**Load `references/v1.4-features.md` for detailed implementation guides.**

---

## Quick Reference

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `BETTER_AUTH_SECRET` | Encryption secret (min 32 chars) | Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_URL` | Base URL | `https://example.com` or `http://localhost:8787` |
| `DATABASE_URL` | Database connection (optional for D1) | PostgreSQL/MySQL connection string |

**Note**: Only define `baseURL`/`secret` in config if env vars are NOT set.

### CLI Commands

| Command | Purpose |
|---------|---------|
| `npx @better-auth/cli@latest migrate` | Apply schema (built-in Kysely adapter only) |
| `npx @better-auth/cli@latest generate` | Generate schema for Prisma/Drizzle |
| `bunx drizzle-kit generate` | **D1: Use this** to generate Drizzle migrations |
| `wrangler d1 migrations apply DB_NAME` | **D1: Use this** to apply migrations |

**Re-run after adding/changing plugins.**

### Core Config Options

| Option | Notes |
|--------|-------|
| `appName` | Optional display name |
| `baseURL` | Only if `BETTER_AUTH_URL` not set |
| `basePath` | Default `/api/auth`. Set `/` for root. |
| `secret` | Only if `BETTER_AUTH_SECRET` not set (min 32 chars) |
| `database` | **Required** for most features. Use `drizzleAdapter()` or Kysely for D1 |
| `secondaryStorage` | Redis/KV for sessions & rate limits |
| `emailAndPassword` | `{ enabled: true }` to activate |
| `socialProviders` | `{ google: { clientId, clientSecret }, ... }` |
| `plugins` | Array of plugins (import from dedicated paths) |
| `trustedOrigins` | CSRF whitelist for cross-origin requests |

### Common Plugins

Import from **dedicated paths** for tree-shaking:
```typescript
import { twoFactor } from "better-auth/plugins/two-factor"
import { organization } from "better-auth/plugins/organization"
import { passkey } from "@better-auth/passkey"  // Separate package
```

**NOT** `from "better-auth/plugins"`.

---

## Top 5 Errors (See references/error-catalog.md for all 15)

### Error #1: "d1Adapter is not exported"
**Problem**: Trying to use non-existent `d1Adapter`
**Solution**: Use `drizzleAdapter` or Kysely instead (see Quick Start above)

### Error #2: Schema Generation Fails
**Problem**: `better-auth migrate` doesn't work with D1
**Solution**: Use `bunx drizzle-kit generate` then `wrangler d1 migrations apply`

### Error #3: CamelCase vs snake_case Mismatch
**Problem**: Database uses `email_verified` but better-auth expects `emailVerified`
**Solution**: Use camelCase in schema or add `CamelCasePlugin` to Kysely

### Error #4: CORS Errors
**Problem**: `Access-Control-Allow-Origin` errors, cookies not sent
**Solution**: Configure CORS with `credentials: true` and correct origins

### Error #5: OAuth Redirect URI Mismatch
**Problem**: Social sign-in fails with "redirect_uri_mismatch"
**Solution**: Ensure exact match: `https://yourdomain.com/api/auth/callback/google`

**Load `references/error-catalog.md` for all 15 errors with detailed solutions.**

---

## Common Use Cases

### Use Case 1: Email/Password Authentication
**When**: Basic authentication without social providers
**Quick Pattern**:
```typescript
// Client
await authClient.signIn.email({
  email: "user@example.com",
  password: "password123",
});

// Server - enable in config
emailAndPassword: {
  enabled: true,
  requireEmailVerification: true,
}
```
**Load**: `references/setup-guide.md` → Step 5

### Use Case 2: Social Authentication (45+ Providers)
**When**: Allow users to sign in with social accounts
**Supported**: Google, GitHub, Microsoft, Apple, Discord, TikTok, Twitch, Spotify, LinkedIn, Slack, Reddit, Facebook, Twitter/X, Patreon, Vercel, Kick, and 30+ more.
**Quick Pattern**:
```typescript
// Client
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
});

// Server config
socialProviders: {
  google: {
    clientId: env.GOOGLE_CLIENT_ID,
    clientSecret: env.GOOGLE_CLIENT_SECRET,
    scope: ["openid", "email", "profile"],
  },
}
```
**Load**: `references/setup-guide.md` → Step 5

### Use Case 3: Protected API Routes
**When**: Need to verify user is authenticated
**Quick Pattern**:
```typescript
app.get("/api/protected", async (c) => {
  const auth = createAuth(c.env);
  const session = await auth.api.getSession({
    headers: c.req.raw.headers,
  });

  if (!session) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  return c.json({ data: "protected", user: session.user });
});
```
**Load**: `references/cloudflare-worker-drizzle.ts`

### Use Case 4: Multi-Tenant with Organizations
**When**: Building SaaS with teams/organizations
**Load**: `references/advanced-features.md` → Organizations & Teams

### Use Case 5: Two-Factor Authentication
**When**: Need extra security with 2FA/TOTP
**Load**: `references/advanced-features.md` → Two-Factor Authentication

---

## When to Load References

**Load `references/setup-guide.md` when**:
- User needs complete 8-step setup walkthrough
- User asks about Kysely adapter alternative
- User needs help with migrations or deployment
- User asks about wrangler.toml configuration

**Load `references/error-catalog.md` when**:
- Encountering any of the 12 documented errors
- User reports D1 adapter, schema, CORS, or OAuth issues
- User asks about troubleshooting or debugging
- User needs prevention checklist

**Load `references/advanced-features.md` when**:
- User asks about 2FA, passkeys, or magic links
- User needs organizations, teams, or RBAC
- User asks about rate limiting or session management
- User wants migration guide from Clerk or Auth.js
- User needs security best practices or performance optimization

**Load `references/cloudflare-worker-drizzle.ts` when**:
- User needs complete Worker implementation example
- User asks for production-ready code
- User wants to see full auth flow with protected routes

**Load `references/cloudflare-worker-kysely.ts` when**:
- User prefers Kysely over Drizzle
- User asks for Kysely-specific implementation

**Load `references/database-schema.ts` when**:
- User needs complete better-auth schema with all tables
- User asks about custom tables or schema extension
- User needs TypeScript types for database

**Load `references/react-client-hooks.tsx` when**:
- User building React/Next.js frontend
- User needs login forms, session hooks, or protected routes
- User asks about client-side implementation

**Load `references/configuration-guide.md` when**:
- User asks about production configuration
- User needs environment variable setup or wrangler.toml
- User asks about session configuration or ESM setup
- User needs CORS configuration, rate limiting, or API keys
- User asks about troubleshooting configuration issues

**Load `references/framework-comparison.md` when**:
- User asks "better-auth vs Clerk" or "vs Auth.js"
- User needs help choosing auth framework
- User wants feature comparison, migration advice, or cost analysis
- User asks about v1.4.0+ new features (database joins, stateless sessions)

**Load `references/migration-guide-1.4.0.md` when**:
- User upgrading from better-auth <1.4.0 to 1.4.0+
- User encounters `forgetPassword` errors or ESM issues
- User asks about breaking changes or migration steps
- User needs to migrate callback functions or API endpoints

**Load `references/v1.4-features.md` when**:
- User asks about background tasks or deferred email sending
- User needs Patreon, Vercel, or Kick OAuth provider setup
- User asks about OAuth 2.1 compliance
- User needs SAML/SSO with clock skew or OIDC discovery
- User asks about the better-auth CLI tool
- User needs admin role permissions configuration
- User asks about ctx.isTrustedDomain or domain verification

**Load `references/nextjs/README.md` when**:
- User building Next.js app with PostgreSQL (not Cloudflare D1)
- User needs organizations and 2FA example
- User asks about Next.js-specific implementation

**Load `references/nextjs/postgres-example.ts` when**:
- User needs complete Next.js API route implementation
- User wants to see organizations + 2FA in practice
- User asks for PostgreSQL setup with Drizzle

### Framework-Specific Setup

**Load `references/frameworks/nextjs.md` when**:
- User building with Next.js (App Router or Pages Router)
- User needs middleware, Server Components, or API routes

**Load `references/frameworks/nuxt.md` when**:
- User building with Nuxt 3
- User needs H3 handlers, composables, or server routes

**Load `references/frameworks/remix.md` when**:
- User building with Remix
- User needs loader/action patterns or session handling

**Load `references/frameworks/sveltekit.md` when**:
- User building with SvelteKit
- User needs hooks, load functions, or stores

**Load `references/frameworks/api-frameworks.md` when**:
- User building with Express, Fastify, NestJS, or Hono (non-Cloudflare)
- User needs middleware or route configuration

**Load `references/frameworks/expo-mobile.md` when**:
- User building React Native or Expo app
- User needs SecureStore, deep linking, or mobile auth

### Database Adapters

**Load `references/databases/postgresql.md` when**:
- User using PostgreSQL with Drizzle or Prisma
- User needs Neon, Supabase, or connection pooling setup

**Load `references/databases/mongodb.md` when**:
- User using MongoDB
- User needs Atlas setup or indexes

**Load `references/databases/mysql.md` when**:
- User using MySQL or PlanetScale
- User needs Vitess compatibility guidance

### Plugin Guides

**Load `references/plugins/authentication.md` when**:
- User needs 2FA, passkeys, magic links, email OTP, or anonymous users
- User asks about enhanced authentication methods

**Load `references/plugins/enterprise.md` when**:
- User needs organizations, SSO/SAML, SCIM, or admin dashboard
- User building multi-tenant or enterprise application

**Load `references/plugins/api-tokens.md` when**:
- User needs API keys, bearer tokens, JWT, or OIDC provider
- User building API authentication for third parties

**Load `references/plugins/payments.md` when**:
- User needs Stripe or Polar integration
- User building subscription or payment features

---

## Configuration Reference

**Quick Config** (ESM-only in v1.4.0+):
```typescript
export const auth = betterAuth({
  baseURL: env.BETTER_AUTH_URL,
  secret: env.BETTER_AUTH_SECRET,
  database: drizzleAdapter(db, { provider: "sqlite" }),
});
```

**Load `references/configuration-guide.md` for**:
- Production configuration with email/password and social providers
- wrangler.toml setup and environment variables
- Session configuration, CORS setup, and ESM requirements
- Rate limiting, API keys (v1.4.0+), and troubleshooting

---

## Using Bundled Resources

### References (references/)

- **setup-guide.md** - Complete 8-step setup (D1 → Drizzle → Deploy)
- **error-catalog.md** - All 12 errors with solutions and prevention checklist
- **advanced-features.md** - 2FA, organizations, rate limiting, passkeys, magic links, migrations
- **configuration-guide.md** - Production config, environment variables, CORS, rate limiting
- **framework-comparison.md** - better-auth vs Clerk vs Auth.js, migration paths, TCO
- **migration-guide-1.4.0.md** - Upgrading from v1.3.x to v1.4.0+ (ESM, API changes)
- **cloudflare-worker-drizzle.ts** - Complete Worker with Drizzle auth
- **cloudflare-worker-kysely.ts** - Complete Worker with Kysely auth
- **database-schema.ts** - Complete better-auth Drizzle schema
- **react-client-hooks.tsx** - React components with auth hooks
- **v1.4-features.md** - Background tasks, new OAuth providers, SAML/SSO, CLI

### Framework References (references/frameworks/)
- **nextjs.md** - Next.js App/Pages Router integration
- **nuxt.md** - Nuxt 3 with H3 and composables
- **remix.md** - Remix loaders, actions, sessions
- **sveltekit.md** - SvelteKit hooks and stores
- **api-frameworks.md** - Express, Fastify, NestJS, Hono
- **expo-mobile.md** - React Native and Expo

### Database References (references/databases/)
- **postgresql.md** - PostgreSQL with Drizzle/Prisma, Neon/Supabase
- **mongodb.md** - MongoDB adapter and Atlas
- **mysql.md** - MySQL and PlanetScale

### Plugin References (references/plugins/)
- **authentication.md** - 2FA, passkeys, magic links, email OTP, anonymous
- **enterprise.md** - Organizations, SSO, SCIM, admin
- **api-tokens.md** - API keys, bearer tokens, JWT, OIDC
- **payments.md** - Stripe, Polar integrations

### Next.js Examples (references/nextjs/)
- **README.md** - Next.js + PostgreSQL setup guide (not D1)
- **postgres-example.ts** - Complete API route with organizations, 2FA, email verification

### Client Integration

**Create auth client** (`src/lib/auth-client.ts`):
```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8787",
});
```

**Use in React**:
```typescript
import { authClient } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session, isPending } = authClient.useSession();

  if (isPending) return <div>Loading...</div>;
  if (!session) return <div>Not authenticated</div>;

  return (
    <div>
      <p>Welcome, {session.user.email}</p>
      <button onClick={() => authClient.signOut()}>Sign Out</button>
    </div>
  );
}
```

---

## Dependencies

**Required**:
- `better-auth@^1.4.9` - Core authentication framework (ESM-only)

**Choose ONE adapter**:
- `drizzle-orm@^0.44.7` + `drizzle-kit@^0.31.7` (recommended)
- `kysely@^0.28.8` + `@noxharmonium/kysely-d1@^0.4.0` (alternative)

**Optional**:
- `@cloudflare/workers-types` - TypeScript types for Workers
- `hono@^4.0.0` - Web framework for routing
- `@better-auth/passkey` - Passkey plugin (v1.4.0+, separate package)
- `@better-auth/api-key` - API key auth (v1.4.0+)

---

## Beyond Cloudflare D1

This skill focuses on **Cloudflare Workers + D1**. better-auth also supports:

**Frameworks** (18 total): Next.js, Nuxt, Remix, SvelteKit, Astro, Express, NestJS, Fastify, Elysia, Expo, and more.

**Databases** (9 adapters): PostgreSQL, MongoDB, MySQL, Prisma, MS SQL, and others.

**Additional Plugins**: Anonymous auth, Email OTP, JWT, Multi-Session, OIDC Provider, payment integrations (Stripe, Polar).

**For non-Cloudflare setups**, load the appropriate framework or database reference file, or consult the official docs: https://better-auth.com/docs

---

## Official Documentation

- **better-auth Docs**: https://better-auth.com
- **GitHub**: https://github.com/better-auth/better-auth (22.4k ⭐)
- **Examples**: https://github.com/better-auth/better-auth/tree/main/examples
- **Drizzle Docs**: https://orm.drizzle.team/docs/get-started-sqlite
- **Kysely Docs**: https://kysely.dev/
- **Discord**: https://discord.gg/better-auth

---

## Framework Comparison

**Load `references/framework-comparison.md` for**:
- Complete feature comparison: better-auth vs Clerk vs Auth.js
- v1.4.0+ new features (database joins, stateless sessions, API keys)
- Migration paths, cost analysis, and performance benchmarks
- Recommendations by use case and 5-year TCO

---

## Production Examples

**Verified working repositories** (all use Drizzle or Kysely):

1. **zwily/example-react-router-cloudflare-d1-drizzle-better-auth** - Drizzle
2. **matthewlynch/better-auth-react-router-cloudflare-d1** - Kysely
3. **foxlau/react-router-v7-better-auth** - Drizzle
4. **zpg6/better-auth-cloudflare** - Drizzle (includes CLI)

**Note**: Check each repo's better-auth version. Repos on v1.3.x need v1.4.0+ migration (see `references/migration-guide-1.4.0.md`). None use a direct `d1Adapter` - all require Drizzle/Kysely.

---

## Complete Setup Checklist

- [ ] Verified ESM support (`"type": "module"` in package.json) - v1.4.0+ required
- [ ] Installed better-auth@1.4.9+ + Drizzle OR Kysely
- [ ] Created D1 database with wrangler
- [ ] Defined database schema with required tables (user, session, account, verification)
- [ ] Generated and applied migrations to D1
- [ ] Set BETTER_AUTH_SECRET environment variable
- [ ] Configured baseURL in auth config
- [ ] Enabled authentication methods (emailAndPassword, socialProviders)
- [ ] Configured CORS with credentials: true
- [ ] Set OAuth callback URLs in provider settings
- [ ] Tested auth routes (/api/auth/*)
- [ ] Tested sign-in, sign-up, session verification
- [ ] Using requestPasswordReset (not forgetPassword) - v1.4.0+ API
- [ ] Deployed to Cloudflare Workers

---

**Questions? Issues?**

1. Check `references/error-catalog.md` for all 15 errors and solutions
2. Review `references/setup-guide.md` for complete 8-step setup
3. See `references/advanced-features.md` for 2FA, organizations, and more
4. Check official docs: https://better-auth.com
5. Ensure you're using **Drizzle or Kysely** (not non-existent d1Adapter)
