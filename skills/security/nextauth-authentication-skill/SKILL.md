---
name: "NextAuth.js Authentication"
description: "Implement authentication with NextAuth.js v5, Google OAuth, credentials provider, session management, and protected routes. Apply when building auth flows, protecting routes, managing sessions, or implementing RBAC."
allowed-tools: Read, Write, Edit, Bash
version: 1.0.0
---

# NextAuth.js Authentication

Systematic authentication implementation with NextAuth.js v5, OAuth providers, and session management.

## Overview

This Skill enforces:
- NextAuth.js v5 configuration
- Google OAuth and credentials providers
- Session management with JWT
- Protected routes with middleware
- Role-based access control (RBAC)
- Secure password hashing
- Token refresh strategies

Apply when implementing authentication, protecting routes, or managing user sessions.

## Setup NextAuth.js v5

### Install Dependencies

```bash
npm install next-auth@beta bcryptjs
npm install -D @types/bcryptjs
```

### Create Auth Configuration

```ts
// lib/auth.ts
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'jwt' },
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await db.user.findUnique({
          where: { email: credentials.email as string }
        });

        if (!user || !user.passwordHash) {
          return null;
        }

        const isValid = await bcrypt.compare(
          credentials.password as string,
          user.passwordHash
        );

        if (!isValid) {
          return null;
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          role: user.role
        };
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    }
  },
  pages: {
    signIn: '/login',
    error: '/auth/error'
  },
  secret: process.env.NEXTAUTH_SECRET
});
```

### Environment Variables

```
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Google OAuth Setup

### Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API
4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
5. Set authorized redirect URIs:
   - Development: `http://localhost:3000/api/auth/callback/google`
   - Production: `https://yourdomain.com/api/auth/callback/google`

### Configure Google Provider

```ts
// lib/auth.ts
Google({
  clientId: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  authorization: {
    params: {
      prompt: 'consent',
      access_type: 'offline',
      response_type: 'code'
    }
  }
})
```

## API Route Handler

```ts
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/lib/auth';

export const { GET, POST } = handlers;
```

## Sign In Page

```tsx
// app/login/page.tsx
'use client';

import { signIn } from 'next-auth/react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  const handleCredentialsSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const result = await signIn('credentials', {
      email,
      password,
      redirect: false
    });

    if (result?.error) {
      setError('Invalid credentials');
    } else {
      router.push('/dashboard');
    }
  };

  const handleGoogleSignIn = () => {
    signIn('google', { callbackUrl: '/dashboard' });
  };

  return (
    <div>
      <h1>Sign In</h1>
      
      {/* Google Sign In */}
      <button onClick={handleGoogleSignIn}>
        Sign in with Google
      </button>

      <div>OR</div>

      {/* Credentials Sign In */}
      <form onSubmit={handleCredentialsSignIn}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        
        {error && <p className="error">{error}</p>}
        
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}
```

## Sign Up (Registration)

```tsx
// app/api/auth/register/route.ts
import { NextResponse } from 'next/server';
import bcrypt from 'bcryptjs';
import { db } from '@/lib/db';

export async function POST(request: Request) {
  try {
    const { email, password, name } = await request.json();

    // Validate input
    if (!email || !password || !name) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Check if user exists
    const existingUser = await db.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      return NextResponse.json(
        { error: 'User already exists' },
        { status: 409 }
      );
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);

    // Create user
    const user = await db.user.create({
      data: {
        email,
        name,
        passwordHash
      }
    });

    return NextResponse.json(
      { message: 'User created', userId: user.id },
      { status: 201 }
    );
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

## Protected Routes with Middleware

```ts
// middleware.ts
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const session = req.auth;

  // Public routes
  const publicRoutes = ['/', '/login', '/register'];
  if (publicRoutes.includes(pathname)) {
    return NextResponse.next();
  }

  // Require authentication
  if (!session) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Admin-only routes
  if (pathname.startsWith('/admin')) {
    if (session.user.role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard', req.url));
    }
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
};
```

## Server-Side Session Access

```tsx
// app/dashboard/page.tsx
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <p>Email: {session.user.email}</p>
      <p>Role: {session.user.role}</p>
    </div>
  );
}
```

## Client-Side Session Access

```tsx
// app/components/UserProfile.tsx
'use client';

import { useSession, signOut } from 'next-auth/react';

export function UserProfile() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <div>Not signed in</div>;
  }

  return (
    <div>
      <p>{session.user.name}</p>
      <p>{session.user.email}</p>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}
```

## Role-Based Access Control (RBAC)

```tsx
// lib/rbac.ts
export const PERMISSIONS = {
  admin: ['create', 'read', 'update', 'delete'],
  editor: ['create', 'read', 'update'],
  viewer: ['read']
};

export function hasPermission(role: string, action: string): boolean {
  return PERMISSIONS[role as keyof typeof PERMISSIONS]?.includes(action) ?? false;
}

// Usage in Server Component
import { auth } from '@/lib/auth';
import { hasPermission } from '@/lib/rbac';

export default async function Page() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  const canDelete = hasPermission(session.user.role, 'delete');

  return (
    <div>
      {canDelete && <button>Delete</button>}
    </div>
  );
}
```

## Session Provider for Client Components

```tsx
// app/providers.tsx
'use client';

import { SessionProvider } from 'next-auth/react';

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>;
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

## Anti-Patterns

```tsx
// ❌ BAD: Storing password plaintext
const user = await db.user.create({
  data: {
    password: password  // NEVER!
  }
});

// ✅ GOOD: Hash password
const passwordHash = await bcrypt.hash(password, 10);
const user = await db.user.create({
  data: { passwordHash }
});

// ❌ BAD: No session check
export default function DashboardPage() {
  return <div>Dashboard</div>;
}

// ✅ GOOD: Check session
export default async function DashboardPage() {
  const session = await auth();
  if (!session) redirect('/login');
  return <div>Dashboard</div>;
}

// ❌ BAD: Client-side only protection
'use client';
export default function Page() {
  const { data: session } = useSession();
  if (!session) return <div>Not allowed</div>;
  // Still accessible by disabling JS!
}

// ✅ GOOD: Server-side protection
export default async function Page() {
  const session = await auth();
  if (!session) redirect('/login');
  return <div>Protected content</div>;
}
```

## Verification Before Production

- [ ] NextAuth.js v5 configured
- [ ] Google OAuth credentials set up
- [ ] Credentials provider working
- [ ] Passwords hashed with bcrypt (never plaintext)
- [ ] Session management with JWT
- [ ] Middleware protecting routes
- [ ] RBAC implemented for admin routes
- [ ] Sign in/sign up pages functional
- [ ] Session provider wraps app
- [ ] Environment variables configured
- [ ] NEXTAUTH_SECRET set (never commit)

## Integration with Project Standards

Enforces security best practices:
- S-1: Passwords hashed with bcrypt
- S-5: Secrets in environment variables
- AP-1: Authentication required for admin routes
- S-8: RBAC for authorization

## Resources

- NextAuth.js v5: https://authjs.dev
- Google OAuth Setup: https://console.cloud.google.com
- Prisma Adapter: https://authjs.dev/reference/adapter/prisma
