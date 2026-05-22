---
name: nextjs-middleware-generator
description: Generate Next.js middleware for authentication, authorization, redirects, CORS, rate limiting, and internationalization. Use when asked to create middleware, protect routes, add CORS, handle redirects, or set up i18n routing.
---

# Next.js Middleware Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Generation Process

1. Determine middleware requirements (auth, CORS, rate limiting, i18n, redirects)
2. Generate `middleware.ts` at the project root
3. Configure route matchers
4. Add helper functions as needed

## Base Middleware Structure

Create `middleware.ts` at the project root. Next.js only supports a single middleware file:

```typescript
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // Middleware logic here
  return NextResponse.next();
}

export const config = {
  matcher: [
    // Match all routes except static files and Next.js internals
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

## Auth Middleware

Protect routes by checking for a valid session:

```typescript
import { NextRequest, NextResponse } from 'next/server';

const protectedRoutes = ['/dashboard', '/settings', '/profile'];
const authRoutes = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionToken = request.cookies.get('authjs.session-token')?.value;
  const isLoggedIn = !!sessionToken;

  // Redirect logged-in users away from auth pages
  if (isLoggedIn && authRoutes.some((route) => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users to login
  if (!isLoggedIn && protectedRoutes.some((route) => pathname.startsWith(route))) {
    const callbackUrl = encodeURIComponent(pathname);
    return NextResponse.redirect(new URL(`/login?callbackUrl=${callbackUrl}`, request.url));
  }

  return NextResponse.next();
}
```

### Auth.js Integration

When using Auth.js, use its built-in middleware wrapper:

```typescript
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isLoggedIn = !!req.auth;

  if (!isLoggedIn && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ['/((?!api/auth|_next/static|_next/image|favicon.ico).*)'],
};
```

## Role-Based Access

Check user role from JWT or session and restrict routes:

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { jwtVerify } from 'jose';

const roleRoutes: Record<string, string[]> = {
  '/admin': ['ADMIN'],
  '/dashboard/billing': ['ADMIN', 'BILLING'],
  '/dashboard': ['ADMIN', 'USER'],
};

async function getUserRole(request: NextRequest): Promise<string | null> {
  const token = request.cookies.get('authjs.session-token')?.value;
  if (!token) return null;

  try {
    const secret = new TextEncoder().encode(process.env.AUTH_SECRET);
    const { payload } = await jwtVerify(token, secret);
    return (payload.role as string) ?? null;
  } catch {
    return null;
  }
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  for (const [route, allowedRoles] of Object.entries(roleRoutes)) {
    if (pathname.startsWith(route)) {
      const role = await getUserRole(request);

      if (!role) {
        return NextResponse.redirect(new URL('/login', request.url));
      }

      if (!allowedRoles.includes(role)) {
        return NextResponse.redirect(new URL('/unauthorized', request.url));
      }

      break;
    }
  }

  return NextResponse.next();
}
```

## CORS Middleware

Add CORS headers for API routes:

```typescript
import { NextRequest, NextResponse } from 'next/server';

const allowedOrigins = [
  'https://your-frontend.com',
  'http://localhost:3000',
];

function corsHeaders(origin: string | null) {
  const headers = new Headers();
  if (origin && allowedOrigins.includes(origin)) {
    headers.set('Access-Control-Allow-Origin', origin);
  }
  headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  headers.set('Access-Control-Max-Age', '86400');
  return headers;
}

export function middleware(request: NextRequest) {
  const origin = request.headers.get('origin');

  // Handle preflight OPTIONS requests
  if (request.method === 'OPTIONS') {
    return new NextResponse(null, {
      status: 204,
      headers: corsHeaders(origin),
    });
  }

  const response = NextResponse.next();

  // Add CORS headers to the response
  if (origin && allowedOrigins.includes(origin)) {
    response.headers.set('Access-Control-Allow-Origin', origin);
  }
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  return response;
}

export const config = {
  matcher: '/api/:path*',
};
```

## Rate Limiting

Header-based rate limiting without external store (suitable for edge runtime):

```typescript
import { NextRequest, NextResponse } from 'next/server';

const rateLimit = new Map<string, { count: number; resetTime: number }>();

const WINDOW_MS = 60_000; // 1 minute
const MAX_REQUESTS = 60;

function getRateLimitKey(request: NextRequest): string {
  return request.headers.get('x-forwarded-for')
    ?? request.headers.get('x-real-ip')
    ?? 'anonymous';
}

function checkRateLimit(key: string): { allowed: boolean; remaining: number } {
  const now = Date.now();
  const entry = rateLimit.get(key);

  if (!entry || now > entry.resetTime) {
    rateLimit.set(key, { count: 1, resetTime: now + WINDOW_MS });
    return { allowed: true, remaining: MAX_REQUESTS - 1 };
  }

  entry.count++;

  if (entry.count > MAX_REQUESTS) {
    return { allowed: false, remaining: 0 };
  }

  return { allowed: true, remaining: MAX_REQUESTS - entry.count };
}

export function middleware(request: NextRequest) {
  const key = getRateLimitKey(request);
  const { allowed, remaining } = checkRateLimit(key);

  if (!allowed) {
    return NextResponse.json(
      { error: 'Too many requests' },
      {
        status: 429,
        headers: {
          'Retry-After': '60',
          'X-RateLimit-Limit': String(MAX_REQUESTS),
          'X-RateLimit-Remaining': '0',
        },
      }
    );
  }

  const response = NextResponse.next();
  response.headers.set('X-RateLimit-Limit', String(MAX_REQUESTS));
  response.headers.set('X-RateLimit-Remaining', String(remaining));
  return response;
}

export const config = {
  matcher: '/api/:path*',
};
```

## Redirect / Rewrite Rules

### Permanent and Temporary Redirects

```typescript
import { NextRequest, NextResponse } from 'next/server';

const permanentRedirects: Record<string, string> = {
  '/old-blog': '/blog',
  '/legacy-docs': '/docs',
};

const temporaryRedirects: Record<string, string> = {
  '/promo': '/campaigns/summer-2025',
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname in permanentRedirects) {
    return NextResponse.redirect(new URL(permanentRedirects[pathname], request.url), 308);
  }

  if (pathname in temporaryRedirects) {
    return NextResponse.redirect(new URL(temporaryRedirects[pathname], request.url), 307);
  }

  return NextResponse.next();
}
```

### A/B Testing with Rewrites

```typescript
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname === '/pricing') {
    const bucket = request.cookies.get('ab-bucket')?.value;
    const variant = bucket ?? (Math.random() < 0.5 ? 'a' : 'b');

    const response = NextResponse.rewrite(
      new URL(`/pricing/${variant}`, request.url)
    );

    if (!bucket) {
      response.cookies.set('ab-bucket', variant, {
        maxAge: 60 * 60 * 24 * 30, // 30 days
        httpOnly: true,
      });
    }

    return response;
  }

  return NextResponse.next();
}
```

## i18n Routing

Detect locale from `Accept-Language` header and redirect:

```typescript
import { NextRequest, NextResponse } from 'next/server';

const locales = ['en', 'it', 'de', 'fr', 'es'];
const defaultLocale = 'en';

function getPreferredLocale(request: NextRequest): string {
  const acceptLanguage = request.headers.get('accept-language') ?? '';
  const preferred = acceptLanguage
    .split(',')
    .map((lang) => lang.split(';')[0].trim().substring(0, 2))
    .find((lang) => locales.includes(lang));

  return preferred ?? defaultLocale;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Skip if path already has a locale prefix
  const hasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (hasLocale) return NextResponse.next();

  // Check for stored locale preference
  const cookieLocale = request.cookies.get('NEXT_LOCALE')?.value;
  const locale = cookieLocale && locales.includes(cookieLocale)
    ? cookieLocale
    : getPreferredLocale(request);

  const response = NextResponse.redirect(
    new URL(`/${locale}${pathname}`, request.url)
  );

  response.cookies.set('NEXT_LOCALE', locale, {
    maxAge: 60 * 60 * 24 * 365,
    httpOnly: true,
  });

  return response;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api).*)'],
};
```

## Composing Multiple Middlewares

Chain multiple middleware functions in a single `middleware.ts`:

```typescript
import { NextRequest, NextResponse } from 'next/server';

type MiddlewareFn = (
  request: NextRequest,
  response: NextResponse
) => NextResponse | Response | undefined;

function composeMiddleware(...fns: MiddlewareFn[]) {
  return function middleware(request: NextRequest) {
    let response = NextResponse.next();

    for (const fn of fns) {
      const result = fn(request, response);

      // If middleware returns a redirect or error, stop the chain
      if (result instanceof Response && result !== response) {
        return result;
      }

      if (result) {
        response = result as NextResponse;
      }
    }

    return response;
  };
}

// Individual middleware functions
function withCors(request: NextRequest, response: NextResponse) {
  const origin = request.headers.get('origin');
  if (origin) {
    response.headers.set('Access-Control-Allow-Origin', origin);
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  }
  return response;
}

function withAuth(request: NextRequest, response: NextResponse) {
  const token = request.cookies.get('authjs.session-token')?.value;

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}

function withHeaders(request: NextRequest, response: NextResponse) {
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'origin-when-cross-origin');
  return response;
}

// Compose and export
export const middleware = composeMiddleware(withHeaders, withCors, withAuth);

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

## Matcher Configuration

The `config.matcher` controls which routes the middleware runs on:

```typescript
export const config = {
  // Single path
  matcher: '/dashboard/:path*',

  // Multiple paths
  matcher: ['/dashboard/:path*', '/api/:path*'],

  // Regex — exclude static files and Next.js internals
  matcher: ['/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)'],

  // Only API routes
  matcher: '/api/:path*',
};
```

Key rules:
- Matchers must be string literals (no variables) for static analysis
- Use `:path*` for wildcard segments
- Always exclude `_next/static`, `_next/image`, and static assets to avoid unnecessary middleware execution

## Completeness Check

After generating middleware, verify that: the middleware file is at the project root (not inside `app/` or `src/`), the `config.matcher` excludes static files and `_next` internals, redirects use `307` (temporary) or `308` (permanent) status codes, CORS middleware handles both preflight OPTIONS and regular requests, auth middleware does not block the login page itself, and composed middlewares short-circuit correctly on redirects. If using Auth.js, verify the matcher excludes `api/auth` routes.

## Asset

See `assets/middleware-template/middleware.ts` for a composable middleware starter template.
