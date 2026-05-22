---
name: nextjs-middleware
description: When you need to run code before a request completes: auth checks, redirects, headers, A/B testing. **Version Context**: Next.js 16.0+ uses `proxy.ts` (replaces `middleware.ts` from v15 and earlier).
version: 1.1.0
tokens: ~550
confidence: high
sources:
  - https://nextjs.org/docs/app/building-your-application/routing/middleware
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [nextjs, middleware, proxy, auth, routing, frontend]
---

## When to Use
When you need to run code before a request completes: auth checks, redirects, headers, A/B testing.

**Version Context**: Next.js 16.0+ uses `proxy.ts` (replaces `middleware.ts` from v15 and earlier).

## Patterns

### Basic Proxy (Next.js 16+)
```typescript
// proxy.ts (root of project)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  // Runs on EVERY matched route
  return NextResponse.next();
}

// Match specific routes
export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*']
};
```

### Legacy Middleware (Next.js 15 and earlier)
```typescript
// middleware.ts (root of project)
export function middleware(request: NextRequest) {
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*']
};
```

**Migration**: Run `npx @next/codemod@canary middleware-to-proxy .` to auto-migrate.

### Auth Redirect
```typescript
export function proxy(request: NextRequest) {
  const token = request.cookies.get('session');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}
```

### Add Headers
```typescript
export function proxy(request: NextRequest) {
  const response = NextResponse.next();

  // Add security headers
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');

  return response;
}
```

### Matcher Patterns
```typescript
export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
    // Match specific paths
    '/dashboard/:path*',
    '/api/:path*',
  ]
};
```

### Advanced Matcher with Conditions
```typescript
export const config = {
  matcher: [
    {
      source: '/api/:path*',
      locale: false,
      has: [{ type: 'header', key: 'Authorization' }],
      missing: [{ type: 'cookie', key: 'session' }],
    },
  ],
};
```

## Anti-Patterns
- Heavy computation in proxy (runs on every request)
- Database queries (use Edge-compatible clients only)
- Large dependencies (bundle size matters at edge)
- Forgetting matcher (runs on ALL routes by default)
- Using `middleware.ts` in Next.js 16+ (use `proxy.ts` instead)

## Verification Checklist
- [ ] Matcher configured (not running on static files)
- [ ] No heavy computation or DB calls
- [ ] Auth redirects tested
- [ ] Headers properly set
- [ ] Using `proxy.ts` for Next.js 16+, `middleware.ts` for v15 and earlier
