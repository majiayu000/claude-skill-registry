---
name: middleware-protection
description: Protect routes with Next.js middleware. Check authentication once, protect routes declaratively. Supports public routes, protected routes, and role-based access.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: auth
  time: 2h
  source: drift-masterguide
---

# Middleware Route Protection

Check auth once, protect routes declaratively.

## When to Use This Skill

- Need to protect multiple routes
- Want centralized auth checking
- Tired of repeating auth logic in every route
- Need role-based access control

## Core Concepts

1. **Middleware intercepts** - All requests pass through middleware
2. **Declarative routes** - Define protected/public routes in config
3. **Session refresh** - Keep sessions alive automatically
4. **Consistent errors** - API routes get JSON, pages get redirects

## TypeScript Implementation

### middleware.ts

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

// Routes that require authentication
const PROTECTED_ROUTES = [
  '/dashboard',
  '/settings',
  '/api/user',
  '/api/predictions',
];

// Routes that are always public
const PUBLIC_ROUTES = [
  '/',
  '/login',
  '/signup',
  '/api/health',
  '/api/public',
];

export async function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // Skip static files and Next.js internals
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/favicon') ||
    pathname.match(/\.(svg|png|jpg|jpeg|gif|webp|ico)$/)
  ) {
    return NextResponse.next();
  }

  // Skip explicitly public routes
  if (PUBLIC_ROUTES.some(route => pathname === route || pathname.startsWith(route + '/'))) {
    return NextResponse.next();
  }

  // Create response that we'll modify
  let response = NextResponse.next({ request });

  // Create Supabase client with cookie handling
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          response = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            response.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session (important for SSR)
  const { data: { user } } = await supabase.auth.getUser();

  // Check if route requires auth
  const requiresAuth = PROTECTED_ROUTES.some(route => 
    pathname === route || pathname.startsWith(route + '/')
  );

  if (requiresAuth && !user) {
    // API routes: return 401 JSON
    if (pathname.startsWith('/api/')) {
      return NextResponse.json(
        {
          error: 'Authentication required',
          code: 'AUTH_REQUIRED',
          loginUrl: '/login',
        },
        { status: 401 }
      );
    }
    
    // Pages: redirect to login with return URL
    const url = request.nextUrl.clone();
    url.pathname = '/login';
    url.searchParams.set('redirectTo', pathname);
    return NextResponse.redirect(url);
  }

  // Add user ID to headers for downstream use
  if (user) {
    response.headers.set('x-user-id', user.id);
  }

  return response;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

### Using User ID in API Routes

```typescript
// app/api/user/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET(request: NextRequest) {
  // User ID was added by middleware
  const userId = request.headers.get('x-user-id');
  
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const supabase = await createServerSupabaseClient();
  
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('*')
    .eq('id', userId)
    .single();

  return NextResponse.json({ profile });
}
```

### Role-Based Protection

```typescript
// middleware.ts (extended)

const ROUTE_ROLES: Record<string, string[]> = {
  '/admin': ['admin'],
  '/dashboard': ['user', 'admin'],
  '/api/admin': ['admin'],
};

// After getting user, check role
if (user) {
  const userRole = user.user_metadata?.role || 'user';
  
  const requiredRoles = Object.entries(ROUTE_ROLES)
    .find(([route]) => pathname.startsWith(route))?.[1];

  if (requiredRoles && !requiredRoles.includes(userRole)) {
    if (pathname.startsWith('/api/')) {
      return NextResponse.json(
        { error: 'Forbidden', code: 'FORBIDDEN' },
        { status: 403 }
      );
    }
    return NextResponse.redirect(new URL('/unauthorized', request.url));
  }
}
```

### Pattern-Based Routes

```typescript
// For more complex route matching
const PROTECTED_PATTERNS = [
  /^\/dashboard(\/.*)?$/,
  /^\/api\/user\/.*$/,
  /^\/settings$/,
  /^\/api\/v\d+\/private\/.*/,  // /api/v1/private/*, /api/v2/private/*
];

const requiresAuth = PROTECTED_PATTERNS.some(pattern => 
  pattern.test(pathname)
);
```

## Python Implementation (FastAPI)

```python
# middleware/auth.py
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Set

PROTECTED_ROUTES: Set[str] = {
    "/dashboard",
    "/settings",
    "/api/user",
}

PUBLIC_ROUTES: Set[str] = {
    "/",
    "/login",
    "/signup",
    "/api/health",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Skip public routes
        if path in PUBLIC_ROUTES or any(path.startswith(r + "/") for r in PUBLIC_ROUTES):
            return await call_next(request)
        
        # Check if route requires auth
        requires_auth = path in PROTECTED_ROUTES or any(
            path.startswith(r + "/") for r in PROTECTED_ROUTES
        )
        
        if not requires_auth:
            return await call_next(request)
        
        # Get user from session/token
        user = await get_user_from_request(request)
        
        if not user:
            if path.startswith("/api/"):
                raise HTTPException(
                    status_code=401,
                    detail={
                        "error": "Authentication required",
                        "code": "AUTH_REQUIRED",
                        "login_url": "/login",
                    }
                )
            return RedirectResponse(f"/login?redirectTo={path}")
        
        # Add user to request state
        request.state.user = user
        request.state.user_id = user.id
        
        return await call_next(request)


async def get_user_from_request(request: Request):
    """Extract and validate user from request."""
    token = request.cookies.get("session") or request.headers.get("Authorization")
    if not token:
        return None
    # Validate token and return user
    return await validate_session(token)
```

```python
# Using in routes
from fastapi import Request, Depends

@app.get("/api/user/profile")
async def get_profile(request: Request):
    user_id = request.state.user_id
    profile = await db.get_profile(user_id)
    return {"profile": profile}
```

## Error Response Format

```typescript
// Consistent error format for API routes
interface AuthError {
  error: string;
  code: 'AUTH_REQUIRED' | 'SESSION_EXPIRED' | 'FORBIDDEN';
  message?: string;
  loginUrl: string;
}

// 401 - Not authenticated
{
  "error": "Authentication required",
  "code": "AUTH_REQUIRED",
  "loginUrl": "/login"
}

// 403 - Authenticated but not authorized
{
  "error": "Forbidden",
  "code": "FORBIDDEN",
  "message": "Admin access required"
}
```

## Best Practices

1. **Refresh sessions** - Call `getUser()` in middleware to refresh
2. **Pass user ID** - Add to headers for downstream routes
3. **JSON for APIs** - Never redirect API routes
4. **Return URL** - Include `redirectTo` param for login redirects
5. **Skip static** - Don't process static files

## Common Mistakes

- Redirecting API routes (should return 401 JSON)
- Not refreshing session in middleware
- Processing static files through auth
- Missing return URL on login redirect
- Not handling role-based access

## Related Skills

- [Supabase Auth](../supabase-auth/)
- [JWT Auth](../jwt-auth/)
- [Row Level Security](../row-level-security/)
