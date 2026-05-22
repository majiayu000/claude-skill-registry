---
name: better-auth-ts
description: Better Auth TypeScript/JavaScript authentication library. Use when implementing auth in Next.js, React, Express, or any TypeScript project. Covers email/password, OAuth, JWT, sessions, 2FA, magic links, social login with Next.js 16 proxy.ts patterns.
---

# Better Auth TypeScript Skill

Better Auth is a framework-agnostic authentication and authorization library for TypeScript.

## Quick Start

### Installation

```bash
# npm
npm install better-auth

# pnpm
pnpm add better-auth

# yarn
yarn add better-auth

# bun
bun add better-auth
```

### Basic Setup

See [templates/auth-server.ts](templates/auth-server.ts) for a complete template.

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: yourDatabaseAdapter, // See ORM guides below
  emailAndPassword: { enabled: true },
});
```

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});
```

## ORM Integration (Choose One)

**IMPORTANT**: Always use CLI to generate/migrate schema:

```bash
npx @better-auth/cli generate  # See current schema
npx @better-auth/cli migrate   # Create/update tables
```

| ORM | Guide |
|-----|-------|
| **Drizzle** | [reference/drizzle.md](reference/drizzle.md) |
| **Prisma** | [reference/prisma.md](reference/prisma.md) |
| **Kysely** | [reference/kysely.md](reference/kysely.md) |
| **MongoDB** | [reference/mongodb.md](reference/mongodb.md) |
| **Direct DB** | Use `pg` Pool directly (see templates) |

## Next.js 16 Integration

### API Route

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth.handler);
```

### Proxy (Replaces Middleware)

In Next.js 16, `middleware.ts` → `proxy.ts`:

```typescript
// proxy.ts
import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function proxy(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    return NextResponse.redirect(new URL("/sign-in", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

Migration: `npx @next/codemod@canary middleware-to-proxy .`

### Server Component

```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) redirect("/sign-in");

  return <h1>Welcome {session.user.name}</h1>;
}
```

## Authentication Examples

| Pattern | Guide |
|---------|-------|
| **Email/Password** | [examples/email-password.md](examples/email-password.md) |
| **Social OAuth** | [examples/social-oauth.md](examples/social-oauth.md) |
| **Two-Factor (2FA)** | [examples/two-factor.md](examples/two-factor.md) |
| **Magic Link** | [examples/magic-link.md](examples/magic-link.md) |

## Quick Examples

### Sign In

```typescript
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "password",
});
```

### Social OAuth

```typescript
await authClient.signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
});
```

### Sign Out

```typescript
await authClient.signOut();
```

### Get Session

```typescript
const session = await authClient.getSession();
```

## Plugins

```typescript
import { twoFactor, magicLink, jwt, organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    twoFactor(),
    magicLink({ sendMagicLink: async ({ email, url }) => { /* send email */ } }),
    jwt(),
    organization(),
  ],
});
```

**After adding plugins, always run:**
```bash
npx @better-auth/cli migrate
```

## Advanced Patterns

See [reference/advanced-patterns.md](reference/advanced-patterns.md) for:
- Stateless mode (no database)
- Redis session storage
- Custom user fields
- Rate limiting
- Organization hooks
- SSO configuration
- Multi-tenant setup

## Templates

| Template | Purpose |
|----------|---------|
| [templates/auth-server.ts](templates/auth-server.ts) | Server configuration template |
| [templates/auth-client.ts](templates/auth-client.ts) | Client configuration template |

## Environment Variables

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
NEXT_PUBLIC_APP_URL=http://localhost:3000
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret

# OAuth (as needed)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```

## Error Handling

```typescript
// Client
const { data, error } = await authClient.signIn.email({ email, password });
if (error) {
  console.error(error.message, error.status);
}

// Server
import { APIError } from "better-auth/api";
try {
  await auth.api.signInEmail({ body: { email, password } });
} catch (error) {
  if (error instanceof APIError) {
    console.log(error.message, error.status);
  }
}
```

## Key Commands

```bash
# Generate schema
npx @better-auth/cli generate

# Migrate database
npx @better-auth/cli migrate

# Next.js 16 middleware migration
npx @next/codemod@canary middleware-to-proxy .
```

## Version Info

- Docs: https://www.better-auth.com/docs
- Releases: https://github.com/better-auth/better-auth/releases

**Always check latest docs before implementation - APIs may change between versions.**
