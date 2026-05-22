---
name: nextauth
description: Implements authentication with Auth.js/NextAuth.js v5 including OAuth providers, credentials, sessions, and route protection. Use when adding authentication to Next.js, configuring OAuth providers, or protecting routes.
---

# NextAuth.js / Auth.js

Flexible authentication library for Next.js with 80+ OAuth providers and database adapters.

## Quick Start

**Install:**
```bash
npm install next-auth@beta
```

**Generate secret:**
```bash
npx auth secret
```

This adds `AUTH_SECRET` to `.env.local`.

## Configuration

### Auth Config

```typescript
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    GitHub,
    Google,
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        // Validate credentials against database
        const user = await getUserFromDb(
          credentials.email as string,
          credentials.password as string
        );

        if (!user) return null;

        return {
          id: user.id,
          email: user.email,
          name: user.name,
        };
      },
    }),
  ],
});
```

### Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

### Environment Variables

```bash
# .env.local
AUTH_SECRET=your-generated-secret

# OAuth Providers
AUTH_GITHUB_ID=your-github-client-id
AUTH_GITHUB_SECRET=your-github-client-secret

AUTH_GOOGLE_ID=your-google-client-id
AUTH_GOOGLE_SECRET=your-google-client-secret
```

## OAuth Providers

### GitHub

```typescript
import GitHub from 'next-auth/providers/github';

export const { handlers, auth } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
  ],
});
```

### Google

```typescript
import Google from 'next-auth/providers/google';

export const { handlers, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
      authorization: {
        params: {
          prompt: 'consent',
          access_type: 'offline',
          response_type: 'code',
        },
      },
    }),
  ],
});
```

### Discord

```typescript
import Discord from 'next-auth/providers/discord';

export const { handlers, auth } = NextAuth({
  providers: [Discord],
});
```

## Credentials Provider

```typescript
import Credentials from 'next-auth/providers/credentials';
import { compare } from 'bcryptjs';

export const { handlers, auth } = NextAuth({
  providers: [
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });

        if (!user || !user.password) {
          return null;
        }

        const isValid = await compare(
          credentials.password as string,
          user.password
        );

        if (!isValid) {
          return null;
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.image,
        };
      },
    }),
  ],
  pages: {
    signIn: '/login',
  },
});
```

## Session Management

### Get Session (Server)

```typescript
// In Server Components
import { auth } from '@/auth';

export default async function Page() {
  const session = await auth();

  if (!session) {
    return <div>Please sign in</div>;
  }

  return (
    <div>
      <p>Welcome, {session.user?.name}</p>
      <p>Email: {session.user?.email}</p>
    </div>
  );
}
```

### Get Session (Client)

```tsx
'use client';

import { useSession } from 'next-auth/react';

export function UserInfo() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (status === 'unauthenticated') {
    return <div>Not signed in</div>;
  }

  return (
    <div>
      <p>Signed in as {session?.user?.name}</p>
    </div>
  );
}
```

### Session Provider

```tsx
// app/layout.tsx
import { SessionProvider } from 'next-auth/react';
import { auth } from '@/auth';

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  return (
    <html lang="en">
      <body>
        <SessionProvider session={session}>
          {children}
        </SessionProvider>
      </body>
    </html>
  );
}
```

## Sign In / Sign Out

### Server Actions

```typescript
// app/actions.ts
'use server';

import { signIn, signOut } from '@/auth';

export async function handleSignIn(provider: string) {
  await signIn(provider, { redirectTo: '/dashboard' });
}

export async function handleSignOut() {
  await signOut({ redirectTo: '/' });
}
```

### UI Components

```tsx
'use client';

import { signIn, signOut } from 'next-auth/react';

export function SignInButton() {
  return (
    <button onClick={() => signIn('github')}>
      Sign in with GitHub
    </button>
  );
}

export function SignOutButton() {
  return (
    <button onClick={() => signOut()}>
      Sign out
    </button>
  );
}

// Or using server actions
import { handleSignIn, handleSignOut } from './actions';

export function AuthButtons() {
  return (
    <div>
      <form action={() => handleSignIn('github')}>
        <button type="submit">Sign in with GitHub</button>
      </form>
      <form action={handleSignOut}>
        <button type="submit">Sign out</button>
      </form>
    </div>
  );
}
```

## Route Protection

### Middleware

```typescript
// middleware.ts
export { auth as middleware } from '@/auth';

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### With Custom Logic

```typescript
// middleware.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard');
  const isOnAuth = req.nextUrl.pathname.startsWith('/login');

  if (isOnDashboard && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  if (isOnAuth && isLoggedIn) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Authorized Callback

```typescript
// auth.ts
export const { handlers, auth } = NextAuth({
  providers: [...],
  callbacks: {
    authorized: async ({ auth, request }) => {
      const isLoggedIn = !!auth?.user;
      const isProtected = request.nextUrl.pathname.startsWith('/dashboard');

      if (isProtected && !isLoggedIn) {
        return false; // Redirects to signIn page
      }

      return true;
    },
  },
});
```

### API Route Protection

```typescript
// app/api/protected/route.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export const GET = auth(function GET(req) {
  if (!req.auth) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    );
  }

  return NextResponse.json({
    user: req.auth.user,
    message: 'Protected data',
  });
});
```

## Callbacks

### JWT & Session Callbacks

```typescript
// auth.ts
export const { handlers, auth } = NextAuth({
  providers: [...],
  callbacks: {
    jwt: async ({ token, user, account }) => {
      // Add user data to token on sign in
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }

      // Add access token from OAuth
      if (account) {
        token.accessToken = account.access_token;
      }

      return token;
    },
    session: async ({ session, token }) => {
      // Add token data to session
      if (token) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
        session.accessToken = token.accessToken as string;
      }

      return session;
    },
  },
});
```

### Sign In Callback

```typescript
callbacks: {
  signIn: async ({ user, account, profile }) => {
    // Allow OAuth sign in
    if (account?.provider !== 'credentials') {
      return true;
    }

    // Check if user is verified
    const existingUser = await getUserById(user.id);
    if (!existingUser?.emailVerified) {
      return false;
    }

    return true;
  },
}
```

## Database Adapters

### Prisma Adapter

```bash
npm install @auth/prisma-adapter
```

```typescript
// auth.ts
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';

export const { handlers, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [...],
  session: {
    strategy: 'database', // or 'jwt'
  },
});
```

### Drizzle Adapter

```bash
npm install @auth/drizzle-adapter
```

```typescript
import { DrizzleAdapter } from '@auth/drizzle-adapter';
import { db } from '@/db';

export const { handlers, auth } = NextAuth({
  adapter: DrizzleAdapter(db),
  providers: [...],
});
```

## TypeScript Extensions

```typescript
// types/next-auth.d.ts
import { DefaultSession } from 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      role: string;
    } & DefaultSession['user'];
    accessToken?: string;
  }

  interface User {
    role: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string;
    role: string;
    accessToken?: string;
  }
}
```

## Custom Pages

```typescript
// auth.ts
export const { handlers, auth } = NextAuth({
  providers: [...],
  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/auth/error',
    verifyRequest: '/auth/verify',
    newUser: '/onboarding',
  },
});
```

```tsx
// app/login/page.tsx
import { signIn } from '@/auth';

export default function LoginPage() {
  return (
    <div className="flex flex-col gap-4 max-w-md mx-auto mt-20">
      <h1 className="text-2xl font-bold">Sign In</h1>

      <form
        action={async () => {
          'use server';
          await signIn('github', { redirectTo: '/dashboard' });
        }}
      >
        <button className="w-full p-2 bg-gray-900 text-white rounded">
          Sign in with GitHub
        </button>
      </form>

      <form
        action={async () => {
          'use server';
          await signIn('google', { redirectTo: '/dashboard' });
        }}
      >
        <button className="w-full p-2 bg-blue-600 text-white rounded">
          Sign in with Google
        </button>
      </form>
    </div>
  );
}
```

## Best Practices

1. **Use middleware for protection** - Centralized auth checks
2. **Verify near data layer** - Don't rely only on middleware
3. **Extend session types** - Add custom user properties
4. **Use database sessions for sensitive apps** - More secure than JWT
5. **Handle errors gracefully** - Custom error pages

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing AUTH_SECRET | Run `npx auth secret` |
| Exposed credentials | Use environment variables |
| JWT-only with credentials | Consider database sessions |
| Missing session provider | Wrap app with SessionProvider |
| No redirect after auth | Set redirectTo option |

## Reference Files

- [references/providers.md](references/providers.md) - All OAuth providers
- [references/adapters.md](references/adapters.md) - Database adapters
- [references/callbacks.md](references/callbacks.md) - Callback patterns
