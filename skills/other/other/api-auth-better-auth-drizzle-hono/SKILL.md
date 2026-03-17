---
name: api-auth-better-auth-drizzle-hono
description: Better Auth patterns, sessions, OAuth
---

# Authentication with Better Auth

> **Quick Guide:** Use Better Auth (v1.4+) for type-safe, self-hosted authentication in TypeScript apps. It provides email/password, OAuth, 2FA, sessions, stateless auth, and organization multi-tenancy out of the box. Integrates seamlessly with Hono and Drizzle ORM. Auth.js is now maintained by the Better Auth team.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST mount Better Auth handler on `/api/auth/*` BEFORE any other middleware that depends on session)**

**(You MUST configure CORS middleware BEFORE auth routes when client and server are on different origins)**

**(You MUST use environment variables for ALL secrets (clientId, clientSecret, BETTER_AUTH_SECRET) - NEVER hardcode)**

**(You MUST run `npx @better-auth/cli generate` then `npx drizzle-kit generate` and `npx drizzle-kit migrate` after adding plugins - `migrate` only works with Kysely adapter)**

**(You MUST use `auth.$Infer.Session` types for type-safe session access in middleware)**

**(You MUST use `authClient.requestPasswordReset` - `authClient.forgotPassword` was renamed in v1.4)**

</critical_requirements>

---

**Auto-detection:** Better Auth, betterAuth, createAuthClient, auth.handler, auth.api.getSession, socialProviders, twoFactor plugin, organization plugin, drizzleAdapter, session management, OAuth providers, stateless sessions, cookieCache, genericOAuth, passkey, SCIM

**When to use:**

- Building self-hosted authentication (no vendor lock-in)
- Need email/password + OAuth + 2FA in one solution
- Multi-tenant SaaS with organization/team management
- Type-safe session management with Hono
- Projects requiring database-stored sessions

**When NOT to use:**

- Serverless with strict cold start requirements (consider Clerk/Auth0)
- Need managed authentication with zero setup (consider Clerk)
- Simple static sites without user accounts
- Mobile-only apps (consider Firebase Auth)

**Note:** Auth.js/NextAuth is now maintained by the Better Auth team - consider Better Auth for new projects.

**Key patterns covered:**

- Server configuration (auth.ts) with plugins
- Hono integration with session middleware
- Email/password authentication flows
- OAuth providers (GitHub, Google, etc.) and Generic OAuth plugin
- Two-factor authentication (TOTP)
- Organization and multi-tenancy
- Session management, cookie caching, and stateless sessions
- Drizzle ORM database adapter
- Client-side React integration with useSession
- Performance optimization with cookieCache and experimental joins
- Passkey authentication (separate package: @better-auth/passkey)

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Sign up, sign in, client setup, Drizzle adapter
  - [oauth.md](examples/oauth.md) - GitHub, Google OAuth providers, Generic OAuth plugin
  - [two-factor.md](examples/two-factor.md) - TOTP setup, enable, verify
  - [organizations.md](examples/organizations.md) - Multi-tenancy, invitations
  - [sessions.md](examples/sessions.md) - Session config, cookie caching, stateless sessions
  - [v1.4-features.md](examples/v1.4-features.md) - Stateless auth, performance, Generic OAuth
- For decision frameworks, anti-patterns, and red flags, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Better Auth follows a **TypeScript-first, self-hosted** approach to authentication. Your user data stays in your database, with no vendor lock-in. The plugin architecture enables progressive complexity - start simple and add features as needed.

**Note on Auth.js:** Auth.js (formerly NextAuth.js) is now maintained and overseen by the Better Auth team. Better Auth is the recommended path forward for new TypeScript projects.

**Core principles:**

1. **Type safety throughout** - Session types flow from server to client
2. **Database as source of truth** - Sessions stored in your DB, not JWTs only (with optional stateless mode in v1.4+)
3. **Plugin-based extensibility** - Add 2FA, organizations, passkeys, SCIM when needed
4. **Framework-agnostic** - Works with Hono, Next.js, SvelteKit, Remix, etc.
5. **Performance-focused** - Experimental joins (2-3x faster), cookie caching, stateless sessions

**When to use Better Auth:**

- Self-hosted authentication with full control
- Multi-tenant SaaS with organizations/teams
- Need 2FA, passkeys, or enterprise SSO (SCIM)
- TypeScript projects requiring type-safe auth
- High-performance auth with database optimization

**When NOT to use:**

- Need managed auth with zero maintenance
- Serverless with aggressive cold start budgets (though stateless mode helps)
- Cloudflare Workers without `nodejs_compat` flag (v1.4+ requirement)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Server Configuration (auth.ts)

Create the auth instance with database adapter and configuration. This is the single source of truth for authentication.

#### Constants

```typescript
// lib/auth.ts
const SESSION_EXPIRES_IN_SECONDS = 60 * 60 * 24 * 7; // 7 days
const SESSION_UPDATE_AGE_SECONDS = 60 * 60 * 24; // 1 day (refresh daily)
const PASSWORD_MIN_LENGTH = 8;
const PASSWORD_MAX_LENGTH = 128;
```

#### Basic Setup

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";

import { db } from "@/lib/db";

const SESSION_EXPIRES_IN_SECONDS = 60 * 60 * 24 * 7;
const SESSION_UPDATE_AGE_SECONDS = 60 * 60 * 24;

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg", // or "sqlite" or "mysql"
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },
  session: {
    expiresIn: SESSION_EXPIRES_IN_SECONDS,
    updateAge: SESSION_UPDATE_AGE_SECONDS,
  },
  trustedOrigins: [process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"],
});

// Named export (project convention)
export { auth };
```

**Why good:** Single auth instance exported for reuse, drizzleAdapter connects to existing DB, named constants make session policy clear, environment variables for URLs

```typescript
// BAD Example - Anti-patterns
import { betterAuth } from "better-auth";

const auth = betterAuth({
  database: {
    url: "postgres://user:pass@localhost:5432/db", // BAD: Hardcoded credentials
  },
  session: {
    expiresIn: 604800, // BAD: Magic number (what is this?)
  },
  trustedOrigins: ["http://localhost:3000"], // BAD: Hardcoded URL
});

export default auth; // BAD: Default export
```

**Why bad:** Hardcoded credentials leak in source control, magic numbers obscure session policy, hardcoded URLs break in production, default export prevents tree-shaking

---

### Pattern 2: Hono Integration with Session Middleware

Mount Better Auth handler and create middleware for session access in routes.

#### Handler Setup

```typescript
// app/api/[[...route]]/route.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { handle } from "hono/vercel";

import { auth } from "@/lib/auth";

const CORS_MAX_AGE_SECONDS = 86400;

const app = new Hono().basePath("/api");

// CRITICAL: CORS must be configured BEFORE auth routes
app.use(
  "/auth/*",
  cors({
    origin: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    allowHeaders: ["Content-Type", "Authorization"],
    allowMethods: ["POST", "GET", "OPTIONS"],
    credentials: true,
    maxAge: CORS_MAX_AGE_SECONDS,
  }),
);

// Mount Better Auth handler on /api/auth/*
app.on(["POST", "GET"], "/auth/*", (c) => {
  return auth.handler(c.req.raw);
});

// Named exports for Next.js
export const GET = handle(app);
export const POST = handle(app);
export { app };
```

**Why good:** CORS before auth prevents preflight failures, `c.req.raw` provides Web Standard Request that Better Auth expects, named exports follow convention

#### Session Middleware

```typescript
// middleware/auth-middleware.ts
import type { Context, Next } from "hono";
import { createMiddleware } from "hono/factory";

import { auth } from "@/lib/auth";

type AuthVariables = {
  user: typeof auth.$Infer.Session.user | null;
  session: typeof auth.$Infer.Session.session | null;
};

export const authMiddleware = createMiddleware<{ Variables: AuthVariables }>(
  async (c: Context, next: Next) => {
    const session = await auth.api.getSession({
      headers: c.req.raw.headers,
    });

    c.set("user", session?.user ?? null);
    c.set("session", session?.session ?? null);

    await next();
  },
);

// Named export
export { authMiddleware };
```

**Why good:** Type-safe Variables with `auth.$Infer.Session` ensures c.get("user") is correctly typed, null fallback prevents undefined access

#### Protected Routes

```typescript
// routes/protected.ts
import { OpenAPIHono, createRoute } from "@hono/zod-openapi";

import { authMiddleware } from "@/middleware/auth-middleware";
import { ErrorResponseSchema, UserSchema } from "@/schemas";

const HTTP_STATUS_UNAUTHORIZED = 401;

const app = new OpenAPIHono();

// Apply auth middleware globally or per-route
app.use("*", authMiddleware);

const getMeRoute = createRoute({
  method: "get",
  path: "/me",
  operationId: "getCurrentUser",
  tags: ["Auth"],
  responses: {
    200: {
      description: "Current user",
      content: { "application/json": { schema: UserSchema } },
    },
    401: {
      description: "Unauthorized",
      content: { "application/json": { schema: ErrorResponseSchema } },
    },
  },
});

app.openapi(getMeRoute, async (c) => {
  const user = c.get("user");

  if (!user) {
    return c.json(
      { error: "unauthorized", message: "Authentication required" },
      HTTP_STATUS_UNAUTHORIZED,
    );
  }

  return c.json({ user }, 200);
});

export { app as protectedRoutes };
```

**Why good:** authMiddleware sets typed user/session, null check returns proper 401, OpenAPI route documents auth requirement

```typescript
// BAD Example - No type safety
app.use("*", async (c, next) => {
  const session = await auth.api.getSession({
    headers: c.req.raw.headers,
  });

  // BAD: No type annotation - c.user is any
  c.user = session?.user;

  await next();
});

app.get("/me", async (c) => {
  // BAD: c.user is any - no autocomplete, no type checking
  if (!c.user) {
    return c.json({ error: "Unauthorized" }, 401); // BAD: Magic number
  }
  return c.json(c.user);
});
```

**Why bad:** No AuthVariables type = any access, magic 401 requires hunting for status meaning, direct c.user assignment bypasses Hono's type system

---

### Pattern 3: Email/Password Authentication

Configure email/password auth with proper password requirements and error handling.

#### Server Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";

import { db } from "@/lib/db";
import { sendEmail } from "@/lib/email";

const PASSWORD_RESET_EXPIRY_SECONDS = 3600; // 1 hour

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg" }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
    requireEmailVerification: true,
    sendResetPassword: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `<a href="${url}">Click here to reset your password</a>`,
      });
    },
  },
  emailVerification: {
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Click here to verify your email</a>`,
      });
    },
  },
});

export { auth };
```

**Why good:** Email verification prevents fake signups, custom email sender integrates with your email service, password requirements enforced server-side

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST mount Better Auth handler on `/api/auth/*` BEFORE any other middleware that depends on session)**

**(You MUST configure CORS middleware BEFORE auth routes when client and server are on different origins)**

**(You MUST use environment variables for ALL secrets (clientId, clientSecret, BETTER_AUTH_SECRET) - NEVER hardcode)**

**(You MUST run `npx @better-auth/cli generate` then `npx drizzle-kit generate` and `npx drizzle-kit migrate` after adding plugins - `migrate` only works with Kysely adapter)**

**(You MUST use `auth.$Infer.Session` types for type-safe session access in middleware)**

**(You MUST use `authClient.requestPasswordReset` - `authClient.forgotPassword` was renamed in v1.4)**

**Failure to follow these rules will cause authentication failures, security vulnerabilities, or runtime errors.**

</critical_reminders>

---

## Sources

- [Better Auth Official Documentation](https://www.better-auth.com/)
- [Better Auth GitHub Repository](https://github.com/better-auth/better-auth)
- [Hono Integration Guide](https://www.better-auth.com/docs/integrations/hono)
- [Two-Factor Authentication Plugin](https://www.better-auth.com/docs/plugins/2fa)
- [Organization Plugin](https://www.better-auth.com/docs/plugins/organization)
- [Drizzle Adapter Documentation](https://www.better-auth.com/docs/adapters/drizzle)
