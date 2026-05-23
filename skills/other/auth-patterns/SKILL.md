---
name: auth-patterns
description: This skill should be used when the user asks about "authentication in Next.js", "NextAuth", "Auth.js", "middleware auth", "protected routes", "session management", "JWT", "login flow", or needs guidance on implementing authentication and authorization in Next.js applications.
version: 1.0.0
---

# Authentication Patterns in Next.js

## Overview

Next.js supports multiple authentication strategies. This skill covers common patterns including NextAuth.js (Auth.js), middleware-based protection, and session management.

## Authentication Libraries

| Library | Best For |
|---------|----------|
| NextAuth.js (Auth.js) | Full-featured auth with providers |
| Clerk | Managed auth service |
| Lucia | Lightweight, flexible auth |
| Supabase Auth | Supabase ecosystem |
| Custom JWT | Full control |

## NextAuth.js v5 Setup

### Installation

```bash
npm install next-auth@beta
```

### Configuration

```tsx
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        const user = await getUserByEmail(credentials.email)
        if (!user || !verifyPassword(credentials.password, user.password)) {
          return null
        }
        return user
      },
    }),
  ],
  callbacks: {
    authorized: async ({ auth }) => {
      return !!auth
    },
  },
})
```

### API Route Handler

```tsx
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'

export const { GET, POST } = handlers
```

### Middleware Protection

```tsx
// middleware.ts
export { auth as middleware } from '@/auth'

export const config = {
  matcher: ['/dashboard/:path*', '/api/protected/:path*'],
}
```

## Getting Session Data

### In Server Components

```tsx
// app/dashboard/page.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const session = await auth()

  if (!session) {
    redirect('/login')
  }

  return (
    <div>
      <h1>Welcome, {session.user?.name}</h1>
    </div>
  )
}
```

### In Client Components

```tsx
// components/user-menu.tsx
'use client'

import { useSession } from 'next-auth/react'

export function UserMenu() {
  const { data: session, status } = useSession()

  if (status === 'loading') {
    return <div>Loading...</div>
  }

  if (!session) {
    return <SignInButton />
  }

  return (
    <div>
      <span>{session.user?.name}</span>
      <SignOutButton />
    </div>
  )
}
```

### Session Provider Setup

```tsx
// app/providers.tsx
'use client'

import { SessionProvider } from 'next-auth/react'

export function Providers({ children }: { children: React.ReactNode }) {
  return <SessionProvider>{children}</SessionProvider>
}

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
```

## Sign In/Out Components

```tsx
// components/auth-buttons.tsx
import { signIn, signOut } from '@/auth'

export function SignInButton() {
  return (
    <form
      action={async () => {
        'use server'
        await signIn('github')
      }}
    >
      <button type="submit">Sign in with GitHub</button>
    </form>
  )
}

export function SignOutButton() {
  return (
    <form
      action={async () => {
        'use server'
        await signOut()
      }}
    >
      <button type="submit">Sign out</button>
    </form>
  )
}
```

## Middleware-Based Auth

### Basic Pattern

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const protectedRoutes = ['/dashboard', '/settings', '/api/protected']
const authRoutes = ['/login', '/signup']

export function middleware(request: NextRequest) {
  const token = request.cookies.get('session')?.value
  const { pathname } = request.nextUrl

  // Redirect authenticated users away from auth pages
  if (authRoutes.some(route => pathname.startsWith(route))) {
    if (token) {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  // Protect routes
  if (protectedRoutes.some(route => pathname.startsWith(route))) {
    if (!token) {
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('callbackUrl', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

### With JWT Verification

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import { jwtVerify } from 'jose'

const secret = new TextEncoder().encode(process.env.JWT_SECRET)

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  try {
    const { payload } = await jwtVerify(token, secret)
    // Token is valid, continue
    return NextResponse.next()
  } catch {
    // Token is invalid
    return NextResponse.redirect(new URL('/login', request.url))
  }
}
```

## Role-Based Access Control

### Extending Session Types

```tsx
// types/next-auth.d.ts
import { DefaultSession } from 'next-auth'

declare module 'next-auth' {
  interface Session {
    user: {
      role: 'user' | 'admin'
    } & DefaultSession['user']
  }
}

// auth.ts
export const { handlers, auth } = NextAuth({
  callbacks: {
    session: ({ session, token }) => ({
      ...session,
      user: {
        ...session.user,
        role: token.role,
      },
    }),
    jwt: ({ token, user }) => {
      if (user) {
        token.role = user.role
      }
      return token
    },
  },
})
```

### Role-Based Component

```tsx
// components/admin-only.tsx
import { auth } from '@/auth'
import { redirect } from 'next/navigation'

export async function AdminOnly({ children }: { children: React.ReactNode }) {
  const session = await auth()

  if (session?.user?.role !== 'admin') {
    redirect('/unauthorized')
  }

  return <>{children}</>
}

// Usage
export default async function AdminPage() {
  return (
    <AdminOnly>
      <AdminDashboard />
    </AdminOnly>
  )
}
```

## Session Storage Options

### JWT (Stateless)

```tsx
// auth.ts
export const { auth } = NextAuth({
  session: { strategy: 'jwt' },
  // JWT stored in cookies, no database needed
})
```

### Database Sessions

```tsx
// auth.ts
import { PrismaAdapter } from '@auth/prisma-adapter'
import { prisma } from '@/lib/prisma'

export const { auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'database' },
  // Sessions stored in database
})
```

## Custom Login Page

```tsx
// app/login/page.tsx
'use client'

import { signIn } from 'next-auth/react'
import { useSearchParams } from 'next/navigation'

export default function LoginPage() {
  const searchParams = useSearchParams()
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard'

  return (
    <div className="flex flex-col gap-4">
      <button
        onClick={() => signIn('github', { callbackUrl })}
        className="btn"
      >
        Sign in with GitHub
      </button>
      <button
        onClick={() => signIn('google', { callbackUrl })}
        className="btn"
      >
        Sign in with Google
      </button>
    </div>
  )
}
```

## Security Best Practices

1. **Use HTTPS** in production
2. **Set secure cookie flags** (HttpOnly, Secure, SameSite)
3. **Implement CSRF protection** (built into NextAuth)
4. **Validate redirect URLs** to prevent open redirects
5. **Use environment variables** for secrets
6. **Implement rate limiting** on auth endpoints
7. **Hash passwords** with bcrypt or argon2

## Resources

For detailed patterns, see:
- `references/middleware-auth.md` - Advanced middleware patterns
- `references/session-management.md` - Session strategies
- `examples/nextauth-setup.md` - Complete NextAuth.js setup
