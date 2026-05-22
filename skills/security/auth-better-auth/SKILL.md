---
name: auth-better-auth
description: Better Auth integration for Next.js 16 with Drizzle adapter. This skill should be used when connecting to a Better Auth instance, configuring OAuth providers, or implementing protected routes with proxy.ts.
---

# Better Auth Skill

Integration patterns for connecting to Better Auth in Next.js 16 projects using the Drizzle adapter.

## When to Use This Skill

- Connecting a Next.js app to Better Auth
- Configuring OAuth providers (Google, GitHub, etc.)
- Implementing protected routes with Next.js 16 proxy.ts
- Adding auth state to React components

## Core Concepts

### What Better Auth Provides

Better Auth is a TypeScript-first authentication framework that handles:
- OAuth flows (Google, GitHub, Apple, etc.)
- Session management
- User/account storage
- JWT tokens (optional)

This skill covers **connecting to** Better Auth, not building the auth service itself.

## Setup

### Package Installation

```bash
npm install better-auth
```

### Environment Variables

Add to `.env.local`:

```bash
# Better Auth
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000

# OAuth Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## Auth Configuration

### Server-Side Auth

Create `src/lib/auth.ts`:

```typescript
import { betterAuth } from 'better-auth';
import { drizzleAdapter } from 'better-auth/adapters/drizzle';
import { nextCookies } from 'better-auth/next-js';
import { db } from '@/lib/db';

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
  }),
  
  emailAndPassword: {
    enabled: false, // Enable if needed
  },
  
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
  
  trustedOrigins: [
    process.env.BETTER_AUTH_URL || 'http://localhost:3000',
  ],
  
  plugins: [
    nextCookies(), // Must be last plugin
  ],
});

export type Session = typeof auth.$Infer.Session;
export type User = typeof auth.$Infer.User;
```

### Client-Side Auth

Create `src/lib/auth-client.ts`:

```typescript
import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:3000',
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
```

## API Route Handler

Create `src/app/api/auth/[...all]/route.ts`:

```typescript
import { auth } from '@/lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';

export const { GET, POST } = toNextJsHandler(auth.handler);
```

This handles all auth endpoints:
- `/api/auth/signin/*` - Sign in flows
- `/api/auth/signup` - Registration
- `/api/auth/signout` - Sign out
- `/api/auth/session` - Session info
- `/api/auth/callback/*` - OAuth callbacks

## Route Protection with proxy.ts

### Next.js 16 Proxy (replaces middleware.ts)

Create `proxy.ts` at project root:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

const protectedRoutes = ['/dashboard', '/settings', '/profile'];
const authRoutes = ['/login', '/signup'];

export async function proxy(request: NextRequest): Promise<NextResponse> {
  const { pathname } = request.nextUrl;
  
  const isProtectedRoute = protectedRoutes.some((route) => 
    pathname.startsWith(route)
  );
  const isAuthRoute = authRoutes.some((route) => 
    pathname.startsWith(route)
  );
  
  // Skip auth check for non-protected routes
  if (!isProtectedRoute && !isAuthRoute) {
    return NextResponse.next();
  }
  
  // Get session
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  
  // Redirect unauthenticated users from protected routes
  if (isProtectedRoute && !session) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('redirect', pathname);
    return NextResponse.redirect(loginUrl);
  }
  
  // Redirect authenticated users from auth routes
  if (isAuthRoute && session) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Quick Cookie Check (Faster, Less Secure)

For performance-critical paths where you only need presence check:

```typescript
import { getSessionCookie } from 'better-auth/next-js';

export async function proxy(request: NextRequest): Promise<NextResponse> {
  // Fast path - just check cookie existence
  const sessionCookie = getSessionCookie(request);
  
  if (!sessionCookie && isProtectedRoute(request.nextUrl.pathname)) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  
  return NextResponse.next();
}
```

**Note**: Cookie presence doesn't guarantee valid session. Always validate in API routes.

## Server Component Usage

### Getting Session in Server Components

```typescript
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  
  if (!session) {
    redirect('/login');
  }
  
  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Helper Function

Create `src/lib/auth-utils.ts`:

```typescript
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { redirect } from 'next/navigation';

export async function getSession() {
  return auth.api.getSession({
    headers: await headers(),
  });
}

export async function requireSession() {
  const session = await getSession();
  
  if (!session) {
    redirect('/login');
  }
  
  return session;
}
```

Usage:

```typescript
export default async function SettingsPage() {
  const session = await requireSession();
  
  return <SettingsForm user={session.user} />;
}
```

## Client Component Usage

### Session Hook

```typescript
'use client';

import { useSession, signOut } from '@/lib/auth-client';

export function UserMenu() {
  const { data: session, isPending } = useSession();
  
  if (isPending) {
    return <Skeleton className="h-8 w-8 rounded-full" />;
  }
  
  if (!session) {
    return <a href="/login">Sign In</a>;
  }
  
  return (
    <DropdownMenu>
      <DropdownMenuTrigger>
        <Avatar>
          <AvatarImage src={session.user.image} />
          <AvatarFallback>{session.user.name?.[0]}</AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuItem onClick={() => signOut()}>
          Sign Out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### Sign In Buttons

```typescript
'use client';

import { signIn } from '@/lib/auth-client';

export function LoginPage() {
  return (
    <div className="flex flex-col gap-4">
      <h1>Sign In</h1>
      
      <button
        onClick={() => signIn.social({ provider: 'google' })}
        className="btn btn-outline"
      >
        Continue with Google
      </button>
      
      <button
        onClick={() => signIn.social({ provider: 'github' })}
        className="btn btn-outline"
      >
        Continue with GitHub
      </button>
    </div>
  );
}
```

## API Route Authentication

### Protected API Routes

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

export async function GET(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }
  
  // Access user info
  const userId = session.user.id;
  
  // ... rest of handler
}
```

### Helper for API Routes

```typescript
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';
import { NextResponse } from 'next/server';

export async function withAuth<T>(
  handler: (session: Session) => Promise<T>
): Promise<NextResponse> {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  
  if (!session) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }
  
  try {
    const result = await handler(session);
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

## Database Schema

Better Auth requires these tables. Add to your Drizzle schema:

```typescript
import { pgTable, text, timestamp, boolean } from 'drizzle-orm/pg-core';

export const user = pgTable('user', {
  id: text('id').primaryKey(),
  name: text('name'),
  email: text('email').notNull().unique(),
  emailVerified: boolean('email_verified').notNull().default(false),
  image: text('image'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});

export const session = pgTable('session', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  token: text('token').notNull().unique(),
  expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
  ipAddress: text('ip_address'),
  userAgent: text('user_agent'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});

export const account = pgTable('account', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => user.id, { onDelete: 'cascade' }),
  accountId: text('account_id').notNull(),
  providerId: text('provider_id').notNull(),
  accessToken: text('access_token'),
  refreshToken: text('refresh_token'),
  accessTokenExpiresAt: timestamp('access_token_expires_at', { withTimezone: true }),
  refreshTokenExpiresAt: timestamp('refresh_token_expires_at', { withTimezone: true }),
  scope: text('scope'),
  idToken: text('id_token'),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});

export const verification = pgTable('verification', {
  id: text('id').primaryKey(),
  identifier: text('identifier').notNull(),
  value: text('value').notNull(),
  expiresAt: timestamp('expires_at', { withTimezone: true }).notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).notNull().defaultNow(),
});
```

Or generate with CLI:

```bash
npx @better-auth/cli generate
```

## Troubleshooting

### "Invalid session" errors

- Check `BETTER_AUTH_SECRET` is set and consistent
- Verify `BETTER_AUTH_URL` matches your domain
- Ensure cookies are being set (check devtools)

### OAuth callback fails

- Verify callback URL in provider dashboard matches your app
- Check client ID/secret are correct
- Ensure `trustedOrigins` includes your domain

### Session not persisting

- Check `nextCookies()` plugin is added (must be last)
- Verify `httpOnly` and `secure` settings for production

## Security Checklist

- [ ] `BETTER_AUTH_SECRET` is random, 32+ characters
- [ ] OAuth secrets stored in environment variables
- [ ] `trustedOrigins` is properly configured
- [ ] HTTPS in production
- [ ] Always validate session in API routes (not just proxy)
- [ ] Protect sensitive routes in proxy.ts
