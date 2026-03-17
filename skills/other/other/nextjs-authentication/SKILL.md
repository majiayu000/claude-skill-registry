---
name: nextjs-authentication
description: Complete Next.js authentication system. PROACTIVELY activate for: (1) NextAuth.js (Auth.js) setup, (2) OAuth providers (GitHub, Google), (3) Credentials provider, (4) Session management (JWT/database), (5) Protected routes with middleware, (6) Role-based access control (RBAC), (7) Login/registration forms, (8) Authorization patterns, (9) Type augmentation for sessions. Provides: Auth.js configuration, middleware protection, session hooks, RBAC patterns, login forms. Ensures secure authentication with proper session handling.
---

## Quick Reference

| Auth.js Export | Purpose | Usage |
|----------------|---------|-------|
| `auth` | Get session (server) | `const session = await auth()` |
| `signIn` | Trigger sign in | `await signIn('github')` |
| `signOut` | Trigger sign out | `await signOut()` |
| `handlers` | API route handlers | `export const { GET, POST } = handlers` |

| Session Access | Location | Code |
|----------------|----------|------|
| Server Component | Server | `const session = await auth()` |
| Client Component | Client | `const { data: session } = useSession()` |
| Middleware | Edge | `req.auth` |
| Server Action | Server | `const session = await auth()` |

| Protection Pattern | Location | Method |
|--------------------|----------|--------|
| Route-level | `middleware.ts` | Check `req.auth` |
| Page-level | Server Component | `if (!session) redirect()` |
| Component-level | Client | `useSession()` + guard |
| Action-level | Server Action | `await auth()` check |

## When to Use This Skill

Use for **authentication and authorization**:
- Setting up NextAuth.js (Auth.js v5)
- Adding OAuth providers (GitHub, Google, etc.)
- Implementing credentials-based login
- Protecting routes with middleware
- Role-based access control

**Related skills:**
- For middleware patterns: see `nextjs-middleware`
- For Server Actions: see `nextjs-server-actions`
- For form handling: see `nextjs-server-actions`

---

# Next.js Authentication

## NextAuth.js (Auth.js)

### Installation and Setup

```bash
npm install next-auth@beta
```

```tsx
// auth.ts
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import bcrypt from 'bcryptjs';

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    Google({
      clientId: process.env.GOOGLE_ID,
      clientSecret: process.env.GOOGLE_SECRET,
    }),
    Credentials({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });

        if (!user || !user.password) {
          return null;
        }

        const isValid = await bcrypt.compare(
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
        };
      },
    }),
  ],
  session: {
    strategy: 'jwt',
  },
  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
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
    },
  },
});
```

### Route Handler

```tsx
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';

export const { GET, POST } = handlers;
```

### Environment Variables

```bash
# .env
AUTH_SECRET=your-secret-key-generate-with-openssl-rand-base64-32
GITHUB_ID=your-github-oauth-id
GITHUB_SECRET=your-github-oauth-secret
GOOGLE_ID=your-google-oauth-id
GOOGLE_SECRET=your-google-oauth-secret
```

## Session Management

### Server-Side Session Access

```tsx
// app/dashboard/page.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return (
    <div>
      <h1>Welcome, {session.user?.name}</h1>
      <p>Email: {session.user?.email}</p>
    </div>
  );
}
```

### Client-Side Session Access

```tsx
// components/UserMenu.tsx
'use client';

import { useSession, signIn, signOut } from 'next-auth/react';

export function UserMenu() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <button onClick={() => signIn()}>Sign In</button>;
  }

  return (
    <div>
      <span>{session.user?.name}</span>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}
```

### Session Provider

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
  children,
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

## Protected Routes

### Middleware Protection

```tsx
// middleware.ts
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

const publicPaths = ['/', '/login', '/register', '/api/auth'];

export default auth((req) => {
  const { nextUrl } = req;
  const isLoggedIn = !!req.auth;

  const isPublicPath = publicPaths.some((path) =>
    nextUrl.pathname.startsWith(path)
  );

  if (!isPublicPath && !isLoggedIn) {
    const loginUrl = new URL('/login', nextUrl);
    loginUrl.searchParams.set('callbackUrl', nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Role-based access
  if (nextUrl.pathname.startsWith('/admin')) {
    if (req.auth?.user?.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', nextUrl));
    }
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

### Component-Level Protection

```tsx
// components/ProtectedContent.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function ProtectedContent({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  return <>{children}</>;
}
```

### Client-Side Route Guard

```tsx
'use client';

import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/login');
    }
  }, [status, router]);

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  if (status === 'unauthenticated') {
    return null;
  }

  return <>{children}</>;
}
```

## Login and Registration Forms

### Login Form

```tsx
// app/login/page.tsx
import { signIn } from '@/auth';
import { redirect } from 'next/navigation';

export default function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ callbackUrl?: string; error?: string }>;
}) {
  return (
    <div className="login-page">
      <h1>Sign In</h1>

      {searchParams.error && (
        <p className="error">Invalid credentials</p>
      )}

      <form
        action={async (formData) => {
          'use server';
          await signIn('credentials', {
            email: formData.get('email'),
            password: formData.get('password'),
            redirectTo: searchParams.callbackUrl || '/dashboard',
          });
        }}
      >
        <input name="email" type="email" placeholder="Email" required />
        <input name="password" type="password" placeholder="Password" required />
        <button type="submit">Sign In</button>
      </form>

      <div className="divider">or</div>

      <form
        action={async () => {
          'use server';
          await signIn('github', {
            redirectTo: searchParams.callbackUrl || '/dashboard',
          });
        }}
      >
        <button type="submit">Sign in with GitHub</button>
      </form>

      <form
        action={async () => {
          'use server';
          await signIn('google', {
            redirectTo: searchParams.callbackUrl || '/dashboard',
          });
        }}
      >
        <button type="submit">Sign in with Google</button>
      </form>
    </div>
  );
}
```

### Registration Form

```tsx
// app/register/page.tsx
import { register } from './actions';

export default function RegisterPage() {
  return (
    <div className="register-page">
      <h1>Create Account</h1>

      <form action={register}>
        <input name="name" placeholder="Name" required />
        <input name="email" type="email" placeholder="Email" required />
        <input
          name="password"
          type="password"
          placeholder="Password"
          minLength={8}
          required
        />
        <input
          name="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}
```

```tsx
// app/register/actions.ts
'use server';

import { redirect } from 'next/navigation';
import bcrypt from 'bcryptjs';
import { prisma } from '@/lib/prisma';
import { z } from 'zod';

const RegisterSchema = z
  .object({
    name: z.string().min(2),
    email: z.string().email(),
    password: z.string().min(8),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

export async function register(formData: FormData) {
  const validatedFields = RegisterSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    password: formData.get('password'),
    confirmPassword: formData.get('confirmPassword'),
  });

  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten().fieldErrors };
  }

  const { name, email, password } = validatedFields.data;

  const existingUser = await prisma.user.findUnique({ where: { email } });
  if (existingUser) {
    return { error: { email: ['Email already in use'] } };
  }

  const hashedPassword = await bcrypt.hash(password, 10);

  await prisma.user.create({
    data: {
      name,
      email,
      password: hashedPassword,
    },
  });

  redirect('/login?registered=true');
}
```

## Authorization

### Role-Based Access Control

```tsx
// lib/auth-utils.ts
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export async function requireRole(allowedRoles: string[]) {
  const session = await auth();

  if (!session) {
    redirect('/login');
  }

  if (!allowedRoles.includes(session.user?.role || '')) {
    redirect('/unauthorized');
  }

  return session;
}
```

```tsx
// app/admin/page.tsx
import { requireRole } from '@/lib/auth-utils';

export default async function AdminPage() {
  const session = await requireRole(['admin']);

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome, {session.user?.name}</p>
    </div>
  );
}
```

### Permission-Based Access

```tsx
// lib/permissions.ts
type Permission = 'read:users' | 'write:users' | 'delete:users' | 'admin';

const rolePermissions: Record<string, Permission[]> = {
  admin: ['read:users', 'write:users', 'delete:users', 'admin'],
  editor: ['read:users', 'write:users'],
  viewer: ['read:users'],
};

export function hasPermission(
  userRole: string,
  permission: Permission
): boolean {
  return rolePermissions[userRole]?.includes(permission) || false;
}
```

```tsx
// components/PermissionGuard.tsx
import { auth } from '@/auth';
import { hasPermission, Permission } from '@/lib/permissions';

export async function PermissionGuard({
  permission,
  children,
  fallback = null,
}: {
  permission: Permission;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}) {
  const session = await auth();

  if (!session || !hasPermission(session.user?.role || '', permission)) {
    return fallback;
  }

  return <>{children}</>;
}

// Usage
<PermissionGuard permission="delete:users" fallback={<span>No access</span>}>
  <DeleteUserButton userId={user.id} />
</PermissionGuard>
```

## JWT Tokens

### Custom JWT Content

```tsx
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  // ...
  callbacks: {
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
        token.permissions = user.permissions;
      }

      if (account) {
        token.accessToken = account.access_token;
      }

      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id as string;
      session.user.role = token.role as string;
      session.accessToken = token.accessToken as string;
      return session;
    },
  },
});
```

### Type Augmentation

```tsx
// types/next-auth.d.ts
import { DefaultSession, DefaultUser } from 'next-auth';
import { JWT, DefaultJWT } from 'next-auth/jwt';

declare module 'next-auth' {
  interface Session {
    user: {
      id: string;
      role: string;
    } & DefaultSession['user'];
    accessToken?: string;
  }

  interface User extends DefaultUser {
    role: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT extends DefaultJWT {
    id: string;
    role: string;
    accessToken?: string;
  }
}
```

## Logout

### Sign Out Action

```tsx
// components/SignOutButton.tsx
import { signOut } from '@/auth';

export function SignOutButton() {
  return (
    <form
      action={async () => {
        'use server';
        await signOut({ redirectTo: '/' });
      }}
    >
      <button type="submit">Sign Out</button>
    </form>
  );
}
```

### Client-Side Sign Out

```tsx
'use client';

import { signOut } from 'next-auth/react';

export function SignOutButton() {
  return (
    <button onClick={() => signOut({ callbackUrl: '/' })}>
      Sign Out
    </button>
  );
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use middleware for protection | Global route protection |
| Store minimal data in JWT | Keep tokens small |
| Use secure cookies | httpOnly, secure, sameSite |
| Implement CSRF protection | Built into NextAuth |
| Hash passwords | Use bcrypt or argon2 |
| Validate on server | Never trust client input |
| Use refresh tokens | For long sessions |
| Log auth events | For security auditing |
