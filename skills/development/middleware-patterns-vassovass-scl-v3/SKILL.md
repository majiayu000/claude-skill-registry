---
name: middleware-patterns
description: Next.js middleware patterns for protected routes, auth redirects, and URL handling. Use when working with middleware.ts, protected routes, or auth redirects. Keywords: middleware, protected routes, redirect, auth check, URL, searchParams.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
---

# Middleware Patterns Skill

## Overview

Next.js middleware runs before every request. StepLeague uses it for auth protection and redirects.

---

## Middleware Location

```
src/
└── middleware.ts   ← Runs on every request matching config
```

---

## Protected Routes Configuration

```typescript
// src/middleware.ts

export const config = {
  matcher: [
    // Protected routes - require auth
    '/dashboard/:path*',
    '/league/:path*',
    '/settings/:path*',
    '/submit-steps/:path*',
    '/claim/:path*',
    
    // Admin routes
    '/admin/:path*',
  ],
};
```

---

## Pattern 1: Auth Redirect with Full URL Preservation

**Problem:** Users lose query params after sign-in redirect.

```typescript
// ❌ WRONG - Loses query params
const redirectUrl = new URL('/sign-in', request.url);
redirectUrl.searchParams.set('redirect', pathname);

// ✅ CORRECT - Preserves full URL
const redirectUrl = new URL('/sign-in', request.url);
const fullOriginalUrl = pathname + (request.nextUrl.search || '');
redirectUrl.searchParams.set('redirect', fullOriginalUrl);
```

**Full Implementation:**

```typescript
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Check for auth token in cookies
  const hasAuthToken = request.cookies.has('sb-access-token') ||
                       request.cookies.getAll().some(c => c.name.includes('-auth-token'));
  
  if (!hasAuthToken) {
    // Preserve full URL including query params
    const signInUrl = new URL('/sign-in', request.url);
    const fullPath = pathname + (request.nextUrl.search || '');
    signInUrl.searchParams.set('redirect', fullPath);
    
    return NextResponse.redirect(signInUrl);
  }
  
  return NextResponse.next();
}
```

---

## Pattern 2: Edge Runtime Compatibility

**Critical:** Don't use `@supabase/supabase-js` in middleware - it's not Edge-compatible.

```typescript
// ❌ WRONG - Breaks Edge runtime
import { createServerSupabaseClient } from '@/lib/supabase/server';

export async function middleware(request: NextRequest) {
  const supabase = await createServerSupabaseClient();  // Crashes!
}

// ✅ CORRECT - Check cookies directly
export async function middleware(request: NextRequest) {
  const hasAuth = request.cookies.has('sb-access-token');
  // Simple check, no Supabase import
}
```

---

## Pattern 3: Route-Based Logic

```typescript
export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Public routes - skip auth
  if (pathname.startsWith('/api/public') || 
      pathname === '/sign-in' ||
      pathname === '/sign-up') {
    return NextResponse.next();
  }
  
  // Admin routes - require superadmin
  if (pathname.startsWith('/admin')) {
    // Note: Full superadmin check happens in API/page
    // Middleware just ensures auth exists
    if (!hasAuth) {
      return NextResponse.redirect(new URL('/sign-in', request.url));
    }
  }
  
  // Protected routes - require any auth
  if (!hasAuth) {
    return redirectToSignIn(request);
  }
  
  return NextResponse.next();
}
```

---

## Pattern 4: Header Injection

Add custom headers for downstream use:

```typescript
export async function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Add pathname for layouts
  response.headers.set('x-pathname', request.nextUrl.pathname);
  
  // Add timestamp for debugging
  response.headers.set('x-middleware-ts', Date.now().toString());
  
  return response;
}
```

---

## StepLeague Middleware Structure

```typescript
// src/middleware.ts

import { NextResponse, type NextRequest } from 'next/server';

const PROTECTED_PATHS = [
  '/dashboard',
  '/league',
  '/settings',
  '/submit-steps',
  '/claim',
  '/admin',
];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  // Check if route needs protection
  const isProtected = PROTECTED_PATHS.some(p => pathname.startsWith(p));
  
  if (!isProtected) {
    return NextResponse.next();
  }
  
  // Check for auth cookie
  const authCookie = request.cookies.getAll()
    .find(c => c.name.includes('-auth-token'));
  
  if (!authCookie) {
    const signInUrl = new URL('/sign-in', request.url);
    const fullPath = pathname + (request.nextUrl.search || '');
    signInUrl.searchParams.set('redirect', fullPath);
    return NextResponse.redirect(signInUrl);
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

## Debugging Middleware

### Check if middleware runs:

```typescript
export async function middleware(request: NextRequest) {
  console.log('[Middleware]', request.nextUrl.pathname);
  // ...
}
```

### Check matcher config:

```typescript
// Test your matcher at: https://nextjs.org/docs/app/building-your-application/routing/middleware#matcher
```

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Middleware not running | Matcher excludes path | Update config.matcher |
| Redirect loops | Signin page matched | Add signin to public paths |
| Missing query params | Not preserving search | Use `pathname + search` |
| Edge runtime error | Using Node.js APIs | Use only Edge-compatible code |

---

## Key File

**File:** `src/middleware.ts`

This is the actual middleware implementation. See this file for the current protected paths and auth logic.

---

## Related Skills

- `auth-patterns` - Auth handling after middleware check
- `supabase-patterns` - Database operations (not in middleware)
- `testing-patterns` - Auth middleware tests in `auth-middleware.test.ts`
