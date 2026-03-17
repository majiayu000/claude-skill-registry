---
name: auth-scaffold
description: Scaffold authentication with Auth.js (NextAuth v5), including providers, session handling, middleware protection, and role-based access. Use when asked to set up auth, add login, protect routes, or implement authentication.
---

# Auth Scaffold

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Generation Process

1. Determine auth requirements (providers, session strategy, RBAC)
2. Generate Auth.js configuration
3. Generate auth helper and route handler
4. Generate sign-in/sign-out components
5. Generate middleware for route protection

## Auth.js Configuration

Create `auth.ts` at the project root:

```typescript
import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import Google from 'next-auth/providers/google';
import GitHub from 'next-auth/providers/github';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';
import bcrypt from 'bcryptjs';

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  pages: {
    signIn: '/login',
  },
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Credentials({
      async authorize(credentials) {
        const parsed = loginSchema.safeParse(credentials);
        if (!parsed.success) return null;

        const user = await prisma.user.findUnique({
          where: { email: parsed.data.email },
        });

        if (!user?.hashedPassword) return null;

        const valid = await bcrypt.compare(parsed.data.password, user.hashedPassword);
        if (!valid) return null;

        return { id: user.id, name: user.name, email: user.email, role: user.role };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.sub!;
        session.user.role = token.role as string;
      }
      return session;
    },
  },
});
```

## Prisma Schema Extension

Add these models required by Auth.js to `prisma/schema.prisma`:

```prisma
enum Role {
  USER
  ADMIN
}

model User {
  id             String    @id @default(cuid())
  name           String?
  email          String?   @unique
  emailVerified  DateTime?
  image          String?
  hashedPassword String?
  role           Role      @default(USER)
  accounts       Account[]
  sessions       Session[]
  createdAt      DateTime  @default(now())
  updatedAt      DateTime  @updatedAt
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

## Route Handler

Create `app/api/auth/[...nextauth]/route.ts`:

```typescript
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

## Auth Helper

Create `lib/auth.ts` for convenient session access:

```typescript
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export { auth } from '@/auth';

export async function requireAuth() {
  const session = await auth();
  if (!session?.user) {
    redirect('/login');
  }
  return session;
}

export async function requireRole(role: string) {
  const session = await requireAuth();
  if (session.user.role !== role) {
    redirect('/unauthorized');
  }
  return session;
}
```

## Middleware Protection

Create `middleware.ts` at the project root:

```typescript
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

const protectedRoutes = ['/dashboard', '/settings', '/admin'];
const adminRoutes = ['/admin'];
const authRoutes = ['/login', '/register'];

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isLoggedIn = !!req.auth;
  const userRole = req.auth?.user?.role;

  // Redirect logged-in users away from auth pages
  if (isLoggedIn && authRoutes.some((route) => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }

  // Protect authenticated routes
  if (!isLoggedIn && protectedRoutes.some((route) => pathname.startsWith(route))) {
    const callbackUrl = encodeURIComponent(pathname);
    return NextResponse.redirect(new URL(`/login?callbackUrl=${callbackUrl}`, req.url));
  }

  // Protect admin routes
  if (adminRoutes.some((route) => pathname.startsWith(route)) && userRole !== 'ADMIN') {
    return NextResponse.redirect(new URL('/unauthorized', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api/auth|_next/static|_next/image|favicon.ico).*)'],
};
```

## Sign-In / Sign-Out Components

### Sign-In Button (Client Component)
```typescript
'use client';

import { signIn } from 'next-auth/react';

interface SignInButtonProps {
  provider: 'google' | 'github' | 'credentials';
  children: React.ReactNode;
  className?: string;
}

export function SignInButton({ provider, children, className }: SignInButtonProps) {
  return (
    <button
      onClick={() => signIn(provider, { callbackUrl: '/dashboard' })}
      className={className}
    >
      {children}
    </button>
  );
}
```

### Sign-Out Button (Client Component)
```typescript
'use client';

import { signOut } from 'next-auth/react';

interface SignOutButtonProps {
  children?: React.ReactNode;
  className?: string;
}

export function SignOutButton({ children = 'Sign out', className }: SignOutButtonProps) {
  return (
    <button
      onClick={() => signOut({ callbackUrl: '/' })}
      className={className}
    >
      {children}
    </button>
  );
}
```

### Session Provider (Layout)
Wrap the root layout to enable `useSession` in client components:

```typescript
import { SessionProvider } from 'next-auth/react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
```

## Session Access Patterns

### Server Component
```typescript
import { auth } from '@/lib/auth';

export default async function ProfilePage() {
  const session = await auth();
  if (!session?.user) return <p>Not authenticated</p>;

  return <p>Welcome, {session.user.name}</p>;
}
```

### Client Component
```typescript
'use client';

import { useSession } from 'next-auth/react';

export function UserMenu() {
  const { data: session, status } = useSession();

  if (status === 'loading') return <span aria-busy="true">Loading...</span>;
  if (!session) return null;

  return <span>{session.user?.name}</span>;
}
```

### API Route
```typescript
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export async function GET() {
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return NextResponse.json({ user: session.user });
}
```

### Server Action
```typescript
'use server';

import { auth } from '@/auth';

export async function updateProfile(formData: FormData) {
  const session = await auth();
  if (!session?.user) throw new Error('Unauthorized');

  // Proceed with update
}
```

## Environment Variables

Add to `.env.local`:

```bash
AUTH_SECRET=          # Generate with: npx auth secret
AUTH_GOOGLE_ID=       # Google OAuth client ID
AUTH_GOOGLE_SECRET=   # Google OAuth client secret
AUTH_GITHUB_ID=       # GitHub OAuth client ID
AUTH_GITHUB_SECRET=   # GitHub OAuth client secret
```

## Type Extension

Extend the Auth.js types in `types/next-auth.d.ts`:

```typescript
import { DefaultSession } from 'next-auth';

declare module 'next-auth' {
  interface User {
    role?: string;
  }

  interface Session {
    user: {
      id: string;
      role: string;
    } & DefaultSession['user'];
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    role?: string;
  }
}
```

## Integration Check

After generating the auth scaffold, verify that: the Prisma schema includes all four Auth.js models (User, Account, Session, VerificationToken), the route handler exports GET and POST from `handlers`, the middleware matcher excludes `api/auth` routes, the JWT callback passes the role to the session, and `AUTH_SECRET` is listed in `.env.local`. If using RBAC, verify the `requireRole` helper is used in protected server components and API routes.

## Asset

See `assets/auth-config/auth.ts` for a minimal starter Auth.js configuration.
