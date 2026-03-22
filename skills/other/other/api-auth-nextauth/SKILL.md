---
name: api-auth-nextauth
description: Auth.js (NextAuth v5) authentication patterns - configuration, providers, session strategies, middleware, database adapters, role-based access, Edge compatibility
---

# Auth.js (NextAuth v5) Patterns

> **Quick Guide:** Configure Auth.js in a root `auth.ts` file exporting `{ auth, handlers, signIn, signOut }` from `NextAuth()`. Use the unified `auth()` function everywhere (Server Components, Route Handlers, middleware). Default session strategy is JWT (cookie-based); add a database adapter for persistent sessions. Protect routes via middleware or per-page `auth()` checks.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST configure Auth.js in a root `auth.ts` file and export `{ auth, handlers, signIn, signOut }` from `NextAuth()`)**

**(You MUST use the unified `auth()` function for server-side session access - NOT the deprecated `getServerSession()`, `getSession()`, or `getToken()`)**

**(You MUST use `AUTH_SECRET` environment variable - `NEXTAUTH_SECRET` is deprecated in v5)**

**(You MUST use `AUTH_` prefixed environment variables for provider credentials (e.g., `AUTH_GITHUB_ID`, `AUTH_GITHUB_SECRET`) - they are auto-detected)**

**(You MUST split auth config into `auth.config.ts` (Edge-compatible) and `auth.ts` (with adapter) when using database sessions with middleware)**

**(You MUST check session inside Server Actions and API routes - middleware alone is NOT sufficient for authorization)**

</critical_requirements>

---

**Auto-detection:** Auth.js, NextAuth, next-auth, authjs, auth.ts, auth.config.ts, NextAuth(), signIn, signOut, auth(), handlers, SessionProvider, useSession, AUTH_SECRET, OAuth provider, credentials provider, database adapter, @auth/prisma-adapter, @auth/drizzle-adapter, authorized callback, jwt callback, session callback, middleware auth

**When to use:**

- Adding authentication to Next.js, SvelteKit, Express, or Qwik apps
- Implementing OAuth login (GitHub, Google, Discord, etc.) with 80+ built-in providers
- Building email/magic link authentication flows
- Need JWT or database-backed session management
- Projects requiring Edge-compatible middleware authentication

**When NOT to use:**

- Building a custom auth system from scratch (Auth.js is opinionated)
- Need fine-grained organization/team management (consider Better Auth)
- Mobile-only apps without web frontend (consider Firebase Auth)
- Need self-hosted auth with plugin architecture (consider Better Auth)

**Key patterns covered:**

- Auth configuration (`auth.ts`, `auth.config.ts`)
- OAuth providers (GitHub, Google, Credentials, Email)
- Session strategies (JWT vs database)
- Session access (Server Components, Route Handlers, Client Components)
- Middleware/proxy route protection
- Database adapters (Prisma, Drizzle)
- Callbacks (jwt, session, signIn, redirect)
- Role-based access control
- Edge compatibility split configuration

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core patterns:**

- [examples/core.md](examples/core.md) - Auth configuration, providers, callbacks
- [examples/session.md](examples/session.md) - Session strategies, session access patterns
- [examples/middleware.md](examples/middleware.md) - Route protection, middleware, Edge compatibility
- [examples/database.md](examples/database.md) - Database adapters, Prisma, Drizzle
- [examples/patterns.md](examples/patterns.md) - Role-based access, magic links, account linking

---

<philosophy>

## Philosophy

Auth.js (v5) consolidates authentication into a **single, unified API**. The `auth()` function replaces `getServerSession`, `getSession`, `withAuth`, and `getToken` from v4 for server-side use. `useSession()` remains the correct client-side API. Configuration lives in a root file, not in API routes.

**Core principles:**

1. **Framework-agnostic** - Works with Next.js, SvelteKit, Express, Qwik
2. **Unified API** - Single `auth()` function for all contexts
3. **Provider ecosystem** - 80+ built-in OAuth providers with auto-detection of `AUTH_*` env vars
4. **JWT by default** - Stateless sessions in encrypted cookies, no database required
5. **Edge-compatible** - Middleware runs on Edge runtime with split configuration
6. **Progressive complexity** - Start with OAuth, add database adapter, then customize callbacks

**When to use Auth.js:**

- Need quick OAuth/social login setup with many providers
- Building Next.js apps where middleware route protection is important
- Want JWT sessions without managing a session store
- Need magic link / email authentication
- Multi-framework teams (Next.js + SvelteKit sharing auth patterns)

**When NOT to use Auth.js:**

- Need organization/team management out of the box (Better Auth)
- Need stateful sessions with full audit trail by default (Better Auth)
- Building a pure API without web framework (use passport.js or custom)
- Need 2FA / TOTP built-in (Auth.js requires custom implementation; Better Auth has plugins)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Auth Configuration

The central configuration file exports everything you need from `NextAuth()`.

#### Basic OAuth Setup

```typescript
// auth.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";

export const { auth, handlers, signIn, signOut } = NextAuth({
  providers: [
    GitHub, // Auto-detects AUTH_GITHUB_ID and AUTH_GITHUB_SECRET
    Google, // Auto-detects AUTH_GOOGLE_CLIENT_ID and AUTH_GOOGLE_CLIENT_SECRET
  ],
});
```

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

**Why good:** Single config file exports all auth utilities, providers auto-detect `AUTH_*` env vars, API route is minimal

#### Environment Variables

```bash
# .env.local
AUTH_SECRET="generate-with-npx-auth-secret"  # Required
AUTH_GITHUB_ID="your-github-client-id"       # Auto-detected by GitHub provider
AUTH_GITHUB_SECRET="your-github-secret"      # Auto-detected by GitHub provider
AUTH_GOOGLE_CLIENT_ID="your-google-id"       # Auto-detected by Google provider
AUTH_GOOGLE_CLIENT_SECRET="your-google-secret"
```

**Why good:** `AUTH_` prefix is standardized in v5, `AUTH_SECRET` replaces deprecated `NEXTAUTH_SECRET`, providers auto-detect credentials

---

### Pattern 2: Providers

Auth.js supports OAuth, email/magic link, and credentials authentication. 80+ built-in OAuth providers auto-detect `AUTH_*` env vars.

```typescript
// OAuth: customize profile mapping
GitHub({
  profile(profile) {
    return {
      id: String(profile.id),
      name: profile.name ?? profile.login,
      role: "user",
    };
  },
});

// Credentials: validate input, return null on failure
Credentials({
  async authorize(credentials) {
    const parsed = LoginSchema.safeParse(credentials);
    if (!parsed.success) return null;
    const user = await getUserByEmail(parsed.data.email);
    if (
      !user ||
      !(await verifyPassword(parsed.data.password, user.hashedPassword))
    )
      return null;
    return { id: user.id, name: user.name, email: user.email };
  },
});
```

**Key rules:** Validate input before DB lookup, always hash passwords, return `null` on failure (never throw - it leaks info). See [examples/core.md](examples/core.md) for complete implementations.

---

### Pattern 3: Callbacks

Four callbacks customize auth behavior. Data flows: **jwt callback** (enrich token) -> **session callback** (expose to client).

```typescript
callbacks: {
  jwt({ token, user }) {
    if (user) { token.id = user.id; token.role = user.role ?? "user"; }
    return token;
  },
  session({ session, token }) {
    session.user.id = token.id as string;
    session.user.role = token.role as string;
    return session;
  },
}
```

**Key rules:** JWT callback runs on EVERY `auth()` call (keep lightweight), `user` param is only present at sign-in, never expose OAuth tokens to client. See [examples/core.md](examples/core.md) for complete callback implementations including `signIn` and `redirect`.

---

### Pattern 4: Session Access

The unified `auth()` function replaces `getServerSession`, `getSession`, and `getToken` from v4 for server-side use. `useSession()` remains for Client Components.

| Context          | How to access session                                     |
| ---------------- | --------------------------------------------------------- |
| Server Component | `const session = await auth()`                            |
| Route Handler    | `export const GET = auth(function GET(req) { req.auth })` |
| Server Action    | `const session = await auth()`                            |
| Middleware       | `export { auth as middleware }` or `authorized` callback  |
| Client Component | `useSession()` (requires `SessionProvider` in layout)     |

**Key rules:** Server-side imports come from `@/auth`, client-side imports from `next-auth/react`. Never call `auth()` in Client Components. See [examples/session.md](examples/session.md) for complete implementations.

---

### Pattern 5: Sign In / Sign Out Actions

Two approaches: Server Actions (recommended, progressive enhancement) or client-side.

```typescript
// Server-side (recommended): import from @/auth, use Server Actions in forms
import { signIn, signOut } from "@/auth";
// In form action: await signIn("github", { redirectTo: "/dashboard" })
// In form action: await signOut({ redirectTo: "/" })

// Client-side: import from next-auth/react, use onClick handlers
import { signIn, signOut } from "next-auth/react";
// onClick: signIn("github", { callbackUrl: "/dashboard" })
```

**Key rules:** Server-side uses `redirectTo`, client-side uses `callbackUrl`. `signIn()` throws a NEXT_REDIRECT exception internally -- don't wrap in try/catch expecting a return value. See [examples/core.md](examples/core.md) for complete implementations.

---

### Pattern 6: TypeScript Extensions

Extend session and JWT types via declaration merging in `types/next-auth.d.ts`. Declare custom fields (e.g., `id`, `role`) on `Session`, `User`, and `JWT` interfaces using `& DefaultSession["user"]` to preserve defaults. See [examples/core.md](examples/core.md) for the complete type declaration example.

</patterns>

---

<integration>

## Integration Guide

**Auth.js is the authentication layer.** It handles identity verification, session management, and route protection. It does NOT handle authorization logic (role checks, permission systems) -- that is application code.

**Framework support:** Auth.js works with multiple web frameworks via framework-specific packages (`next-auth`, `@auth/sveltekit`, `@auth/express`).

**Database adapters:** For database sessions, Auth.js provides adapter packages (`@auth/prisma-adapter`, `@auth/drizzle-adapter`, etc.) that integrate with your ORM. See [examples/database.md](examples/database.md).

**Session strategy depends on your needs:**

- **JWT (default)** - No database needed, works on Edge, stateless
- **Database** - Requires adapter, server-side session store, supports immediate revocation

**Auth.js does NOT handle:** fine-grained authorization/RBAC, rate limiting, or database queries beyond auth -- those are application-level concerns.

</integration>

---

<red_flags>

## RED FLAGS

- **Using `getServerSession(authOptions)`** -- deprecated in v5; use `auth()` from your `auth.ts`
- **Using `NEXTAUTH_SECRET` or `NEXTAUTH_URL`** -- deprecated; use `AUTH_SECRET` (URL is auto-detected)
- **Credentials provider without rate limiting** -- vulnerable to brute-force attacks
- **Exposing OAuth tokens to client via session callback** -- keep `accessToken`/`refreshToken` server-side only
- **Middleware as sole authorization** -- middleware runs before rendering but does not replace per-route checks in Server Actions/API routes
- **Database adapter imported in middleware** -- database ORMs can't run on Edge runtime; split config into `auth.config.ts` + `auth.ts`
- **Wrapping `signIn()` in try/catch** -- it throws a NEXT_REDIRECT exception internally (this is intentional)
- **JWT callback querying database on every call** -- runs on EVERY `auth()` invocation; keep it lightweight

See [reference.md](reference.md) for the complete anti-pattern list, gotchas, and migration table.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST configure Auth.js in a root `auth.ts` file and export `{ auth, handlers, signIn, signOut }` from `NextAuth()`)**

**(You MUST use the unified `auth()` function for server-side session access - NOT the deprecated `getServerSession()`, `getSession()`, or `getToken()`)**

**(You MUST use `AUTH_SECRET` environment variable - `NEXTAUTH_SECRET` is deprecated in v5)**

**(You MUST use `AUTH_` prefixed environment variables for provider credentials (e.g., `AUTH_GITHUB_ID`, `AUTH_GITHUB_SECRET`) - they are auto-detected)**

**(You MUST split auth config into `auth.config.ts` (Edge-compatible) and `auth.ts` (with adapter) when using database sessions with middleware)**

**(You MUST check session inside Server Actions and API routes - middleware alone is NOT sufficient for authorization)**

**Failure to follow these rules will cause authentication failures, expose deprecated patterns, or create security vulnerabilities.**

</critical_reminders>
