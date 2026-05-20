---
name: better-auth
description: Guide for implementing Better Auth - a framework-agnostic authentication and authorization framework for TypeScript. Use when adding authentication features like email/password, OAuth, 2FA, passkeys, or advanced auth functionality to applications.
license: MIT
version: 1.0.0
---

# Better Auth Skill

Better Auth is a comprehensive, framework-agnostic authentication and authorization framework for TypeScript that provides built-in support for email/password authentication, social sign-on, and a powerful plugin ecosystem for advanced features.

## When to Use This Skill

Use this skill when:
- Implementing authentication in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up 2FA, passkeys, magic links, or other advanced auth features
- Building multi-tenant applications with organization support
- Implementing session management and user management
- Working with any framework (Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express, etc.)

## Core Concepts

### Key Features

- **Framework Agnostic**: Works with any framework (Next.js, Nuxt, Svelte, Remix, Hono, Express, etc.)
- **Built-in Auth Methods**: Email/password and OAuth 2.0 social providers
- **Plugin Ecosystem**: Easy-to-add advanced features (2FA, passkeys, magic link, username, email OTP, organization, etc.)
- **Database Flexibility**: Supports SQLite, PostgreSQL, MySQL, MongoDB, and more
- **ORM Support**: Built-in adapters for Drizzle, Prisma, Kysely, and MongoDB
- **Type Safety**: Full TypeScript support with excellent type inference
- **Session Management**: Built-in session handling for both client and server

### Architecture

Better Auth follows a client-server architecture:
1. **Server Instance** (`better-auth`): Handles auth logic, database operations, and API routes
2. **Client Instance** (`better-auth/client`): Provides hooks and methods for authentication
3. **Plugins**: Extend both server and client functionality

## Installation & Setup

### Step 1: Install Package

```bash
npm install better-auth
# or
pnpm add better-auth
# or
yarn add better-auth
# or
bun add better-auth
```

### Step 2: Environment Variables

Create `.env` file:

```env
BETTER_AUTH_SECRET=<generated-secret-key>
BETTER_AUTH_URL=http://localhost:3000
```

Generate secret: Use openssl or a random string generator (min 32 characters).

### Step 3: Create Auth Server Instance

Create `auth.ts` in project root, `lib/`, `utils/`, or nested under `src/`, `app/`, or `server/`:

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    // Database configuration
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true // Users auto sign-in after signup
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }
  }
});
```

### Step 4: Database Configuration

Choose your database setup:

**Direct Database Connection:**

```ts
import { betterAuth } from "better-auth";
import Database from "better-sqlite3";
// or import { Pool } from "pg";
// or import { createPool } from "mysql2/promise";

export const auth = betterAuth({
  database: new Database("./sqlite.db"),
  // or: new Pool({ connectionString: process.env.DATABASE_URL })
  // or: createPool({ host: "localhost", user: "root", ... })
});
```

**ORM Adapter:**

```ts
// Drizzle
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg", // or "mysql", "sqlite"
  }),
});

// Prisma
import { prismaAdapter } from "better-auth/adapters/prisma";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: "postgresql",
  }),
});

// MongoDB
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { client } from "@/db";

export const auth = betterAuth({
  database: mongodbAdapter(client),
});
```

### Step 5: Create Database Schema

Use Better Auth CLI:

```bash
# Generate schema/migration files
npx @better-auth/cli generate

# Or migrate directly (Kysely adapter only)
npx @better-auth/cli migrate
```

### Step 6: Mount API Handler

Create catch-all route for `/api/auth/*`:

**Next.js (App Router):**
```ts
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

**Nuxt:**
```ts
// server/api/auth/[...all].ts
import { auth } from "~/utils/auth";

export default defineEventHandler((event) => {
  return auth.handler(toWebRequest(event));
});
```

**SvelteKit:**
```ts
// hooks.server.ts
import { auth } from "$lib/auth";
import { svelteKitHandler } from "better-auth/svelte-kit";

export async function handle({ event, resolve }) {
  return svelteKitHandler({ event, resolve, auth });
}
```

**Hono:**
```ts
import { Hono } from "hono";
import { auth } from "./auth";

const app = new Hono();
app.on(["POST", "GET"], "/api/auth/*", (c) => auth.handler(c.req.raw));
```

**Express:**
```ts
import express from "express";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth";

const app = express();
app.all("/api/auth/*", toNodeHandler(auth));
```

### Step 7: Create Client Instance

Create `auth-client.ts`:

```ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000"
});
```

## Authentication Methods

### Email & Password

**Server Configuration:**
```ts
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    autoSignIn: true, // default: true
  }
});
```

**Client Usage:**

```ts
// Sign Up
const { data, error } = await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",
  image: "https://example.com/avatar.jpg", // optional
  callbackURL: "/dashboard" // optional
}, {
  onSuccess: (ctx) => {
    // redirect or show success
  },
  onError: (ctx) => {
    alert(ctx.error.message);
  }
});

// Sign In
const { data, error } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
  callbackURL: "/dashboard",
  rememberMe: true // default: true
});
```

### Social OAuth

**Server Configuration:**
```ts
export const auth = betterAuth({
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    // Other providers: apple, discord, facebook, etc.
  }
});
```

**Client Usage:**
```ts
await authClient.signIn.social({
  provider: "github",
  callbackURL: "/dashboard",
  errorCallbackURL: "/error",
  newUserCallbackURL: "/welcome",
});
```

### Sign Out

```ts
await authClient.signOut({
  fetchOptions: {
    onSuccess: () => {
      router.push("/login");
    }
  }
});
```

## Session Management

### Client-Side Session

**Using Hooks (React/Vue/Svelte/Solid):**

```tsx
// React
import { authClient } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session, isPending, error } = authClient.useSession();

  if (isPending) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>Welcome, {session?.user.name}!</div>;
}

// Vue
<script setup>
import { authClient } from "~/lib/auth-client";
const session = authClient.useSession();
</script>

<template>
  <div v-if="session.data">{{ session.data.user.email }}</div>
</template>

// Svelte
<script>
import { authClient } from "$lib/auth-client";
const session = authClient.useSession();
</script>

<p>{$session.data?.user.email}</p>
```

**Using getSession:**
```ts
const { data: session, error } = await authClient.getSession();
```

### Server-Side Session

```ts
// Next.js
import { auth } from "./auth";
import { headers } from "next/headers";

const session = await auth.api.getSession({
  headers: await headers()
});

// Hono
app.get("/protected", async (c) => {
  const session = await auth.api.getSession({
    headers: c.req.raw.headers
  });

  if (!session) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  return c.json({ user: session.user });
});
```

## Plugin System

Better Auth's plugin system allows adding advanced features easily.

### Using Plugins

**Server-Side:**
```ts
import { betterAuth } from "better-auth";
import { twoFactor, organization, username } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    twoFactor(),
    organization(),
    username(),
  ]
});
```

**Client-Side:**
```ts
import { createAuthClient } from "better-auth/client";
import {
  twoFactorClient,
  organizationClient,
  usernameClient
} from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    twoFactorClient({
      twoFactorPage: "/two-factor"
    }),
    organizationClient(),
    usernameClient()
  ]
});
```

**After Adding Plugins:**
```bash
# Regenerate schema
npx @better-auth/cli generate

# Apply migration
npx @better-auth/cli migrate
```

### Popular Plugins

#### Two-Factor Authentication (2FA)

```ts
// Server
import { twoFactor } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [twoFactor()]
});

// Client
import { twoFactorClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [
    twoFactorClient({ twoFactorPage: "/two-factor" })
  ]
});

// Usage
await authClient.twoFactor.enable({ password: "userPassword" });
await authClient.twoFactor.verifyTOTP({
  code: "123456",
  trustDevice: true
});
```

#### Username Authentication

```ts
// Server
import { username } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [username()]
});

// Client
import { usernameClient } from "better-auth/client/plugins";

// Sign up with username
await authClient.signUp.username({
  username: "johndoe",
  password: "securePassword123",
  name: "John Doe"
});
```

#### Magic Link

```ts
import { magicLink } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    magicLink({
      sendMagicLink: async ({ email, url }) => {
        // Send email with magic link
        await sendEmail(email, url);
      }
    })
  ]
});
```

#### Passkey (WebAuthn)

```ts
import { passkey } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [passkey()]
});

// Client
await authClient.passkey.register();
await authClient.passkey.signIn();
```

#### Organization/Multi-Tenancy

```ts
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [organization()]
});

// Client
await authClient.organization.create({
  name: "Acme Corp",
  slug: "acme"
});

await authClient.organization.inviteMember({
  organizationId: "org-id",
  email: "user@example.com",
  role: "member"
});
```

## Advanced Configuration

### Email Verification

```ts
export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url }) => {
      await sendEmail(user.email, url);
    },
    sendOnSignUp: true
  }
});
```

### Rate Limiting

```ts
export const auth = betterAuth({
  rateLimit: {
    enabled: true,
    window: 60, // seconds
    max: 10 // requests
  }
});
```

### Custom Session Expiration

```ts
export const auth = betterAuth({
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days in seconds
    updateAge: 60 * 60 * 24 // Update every 24 hours
  }
});
```

### CORS Configuration

```ts
export const auth = betterAuth({
  advanced: {
    corsOptions: {
      origin: ["https://example.com"],
      credentials: true
    }
  }
});
```

## Database Schema

### Core Tables

Better Auth requires these core tables:
- `user`: User accounts
- `session`: Active sessions
- `account`: OAuth provider connections
- `verification`: Email verification tokens

**Auto-generate with CLI:**
```bash
npx @better-auth/cli generate
```

**Manual schema available in docs:** Check `/docs/concepts/database#core-schema`

## Best Practices

1. **Environment Variables**: Always use environment variables for secrets
2. **HTTPS in Production**: Set `BETTER_AUTH_URL` to HTTPS URL
3. **Session Security**: Use secure cookies in production
4. **Error Handling**: Implement proper error handling on client and server
5. **Type Safety**: Leverage TypeScript types for better DX
6. **Plugin Order**: Some plugins depend on others, check documentation
7. **Database Migrations**: Always run migrations after adding plugins
8. **Rate Limiting**: Enable rate limiting for production
9. **Email Verification**: Implement email verification for security
10. **Password Requirements**: Customize password validation as needed

## Common Patterns

### Protected Routes (Server-Side)

```ts
// Next.js middleware
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers
  });

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"]
};
```

### User Profile Updates

```ts
await authClient.updateUser({
  name: "New Name",
  image: "https://example.com/new-avatar.jpg"
});
```

### Password Management

```ts
// Change password
await authClient.changePassword({
  currentPassword: "oldPassword",
  newPassword: "newPassword"
});

// Reset password (forgot password)
await authClient.forgetPassword({
  email: "user@example.com",
  redirectTo: "/reset-password"
});

await authClient.resetPassword({
  token: "reset-token",
  password: "newPassword"
});
```

## Troubleshooting

### Common Issues

1. **"Unable to find auth instance"**
   - Ensure `auth.ts` is in correct location (root, lib/, utils/)
   - Export auth instance as `auth` or default export

2. **Database connection errors**
   - Verify database credentials
   - Check if database server is running
   - Ensure correct adapter for your database

3. **CORS errors**
   - Configure `corsOptions` in advanced settings
   - Ensure client and server URLs match

4. **Plugin not working**
   - Run migrations after adding plugins
   - Check plugin is added to both server and client
   - Verify plugin configuration

## Framework-Specific Guides

- **Next.js**: Use Next.js plugin for server actions
- **Nuxt**: Configure server middleware
- **SvelteKit**: Use hooks.server.ts
- **Astro**: Set up API routes properly
- **Hono/Express**: Use appropriate node handlers

## Resources

- Documentation: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
- Plugins: https://www.better-auth.com/docs/plugins
- Examples: https://www.better-auth.com/docs/examples

## Implementation Checklist

When implementing Better Auth:

- [ ] Install `better-auth` package
- [ ] Set up environment variables (SECRET, URL)
- [ ] Create auth server instance
- [ ] Configure database/adapter
- [ ] Run schema migration
- [ ] Configure authentication methods
- [ ] Mount API handler
- [ ] Create client instance
- [ ] Implement sign-up/sign-in UI
- [ ] Add session management
- [ ] Set up protected routes
- [ ] Add plugins as needed
- [ ] Test authentication flow
- [ ] Configure email sending (if needed)
- [ ] Set up error handling
- [ ] Enable rate limiting for production
