---
name: better-auth-skill
description: Expert Better Auth skill with production best practices, session management, security hardening, and deployment optimization. Use with Better Auth MCP server.
---

# Better Auth Skill

Expert skill for implementing Better Auth in Next.js applications with production best practices, security hardening, and deployment optimization.

## Production-Ready Configuration

Use this configuration for production deployments (especially on Vercel):

```typescript
// lib/auth.ts - Production Ready
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg"; // or your database client

// Create a singleton pool to prevent multiple connections during dev
const globalForPool = globalThis as unknown as { pool: Pool | undefined };

export const pool = globalForPool.pool ?? new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === "production" ? {
    rejectUnauthorized: false
  } : undefined // No SSL in development unless required
});

if (process.env.NODE_ENV !== "production") globalForPool.pool = pool;

// Ensure the secret is properly set - fail loudly if missing
const authSecret = process.env.BETTER_AUTH_SECRET;
if (!authSecret) {
  console.error("BETTER_AUTH_SECRET is not set! This will cause authentication to fail.");
  if (process.env.NODE_ENV === "production") {
    throw new Error("BETTER_AUTH_SECRET environment variable is required in production");
  }
}

export const auth = betterAuth({
  secret: authSecret || "dev-secret-for-development-only-change-in-production",
  baseURL: process.env.BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` :
           process.env.VERCEL_BRANCH_URL ? `https://${process.env.VERCEL_BRANCH_URL}` :
           "http://localhost:3000"),
  database: pool, // or your database configuration
  trustedOrigins: [
    "https://your-production-domain.vercel.app",  // Production Vercel URL
    `https://your-project-git-*vercel.app`,       // Vercel preview URLs
    "http://localhost:3000",                    // Local development
    "http://127.0.0.1:3000",                   // Alternative local address
  ],
  advanced: {
    useSecureCookies: process.env.NODE_ENV === "production", // Force secure cookies in production
    cookiePrefix: "yourapp", // Reduce fingerprinting
    session: {
      expiresIn: 7 * 24 * 60 * 60, // 7 days in seconds
      updateAge: 24 * 60 * 60,      // Update session every 24 hours
      freshAge: 15 * 60,            // 15 minutes for sensitive operations
      cookieCache: {
        enabled: true,
        maxAge: 300,                // 5 minutes cache
        strategy: "compact",         // smallest and fastest
        refreshCache: true          // Refresh when updateAge threshold reached
      }
    },
    defaultCookieAttributes: {
      // Set default attributes for all cookies
      httpOnly: true,
      secure: process.env.NODE_ENV === "production", // Secure in production
      sameSite: process.env.NODE_ENV === "production" ? "none" : "lax", // "none" for cross-site in production with secure
      path: "/",
    },
    ipAddress: {
      ipAddressHeaders: ["cf-connecting-ip"] // Cloudflare header, adjust for your proxy
    }
  },
  account: {
    encryptOAuthTokens: true, // Encrypt OAuth tokens at rest
    storeStateStrategy: "database" // Default safe strategy
  },
  rateLimit: {
    enabled: process.env.NODE_ENV === "production" // Enable in production
  },
  logger: {
    level: process.env.NODE_ENV === "production" ? "error" : "debug"
  },
  plugins: [
    nextCookies() // Install this plugin last to ensure Set-Cookie is applied correctly
  ],
});
```

## Environment Variables

```bash
# .env.local
BETTER_AUTH_SECRET="your-32-character-secret-key-minimum"
BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
DATABASE_URL="postgresql://username:password@host:port/database"

# For Vercel deployment
VERCEL_ENV="production" # Will be set automatically by Vercel
VERCEL_URL="your-project-name.vercel.app" # Set automatically by Vercel
```

## Client-Side Configuration

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

// Determine the correct base URL based on environment
const getBaseURL = () => {
  if (typeof window !== "undefined") {
    // Browser environment
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");
  } else {
    // Server environment
    return process.env.BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");
  }
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
  plugins: [
    jwtClient()
  ]
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

## API Route Handler (App Router)

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth.handler);
```

## Server Component Session Validation

```typescript
// app/dashboard/page.tsx
import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";

// Force this page to be dynamic to prevent static generation
export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(), // Always pass headers from server components
  });

  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Dashboard - Welcome {session.user.name}</h1>
      {/* Your protected content */}
    </div>
  );
}
```

## Server Actions with Session Validation

```typescript
// lib/actions.ts
"use server";

import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function getUserProfile() {
  const session = await auth.api.getSession({
    headers: await headers(), // Always pass headers from server actions
  });

  if (!session) {
    throw new Error("Unauthorized");
  }

  return session.user;
}
```

## Next.js 16+ Proxy for Authentication (Recommended for Next 16+)

```typescript
// proxy.ts (Next.js 16+)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { auth } from "@/lib/auth";

// Public routes that don't require authentication
const publicRoutes = ["/", "/login", "/register"];

export async function middleware(req: NextRequest) {
  // For full validation, use Node.js runtime
  // For optimistic redirects, use presence-only check
  const session = await auth.api.getSession({
    headers: {
      cookie: req.headers.get("cookie") || "",
    },
  });

  const isLoggedIn = !!session?.user;
  const isOnPublicRoute = publicRoutes.includes(req.nextUrl.pathname);

  // If on a protected route without being logged in, redirect to login
  if (!isOnPublicRoute && !isLoggedIn) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  // If logged in and trying to access login/register, redirect to dashboard
  if ((req.nextUrl.pathname === "/login" || req.nextUrl.pathname === "/register") && isLoggedIn) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
}

// Use Node.js runtime for full session validation
export const config = {
  runtime: "nodejs",
  matcher: [
    /*
     * Match all request paths except for:
     * - api routes (handled by Better Auth API)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!api|_next/static|_next/image|favicon.ico|public).*)",
  ],
};
```

## Next.js Edge Middleware (For older Next.js versions or when Node runtime not available)

```typescript
// middleware.ts (Edge runtime)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getSessionCookie } from "better-auth/cookies";

// Public routes that don't require authentication
const publicRoutes = ["/", "/login", "/register"];

export function middleware(req: NextRequest) {
  // Edge runtime cannot make database calls
  // Use presence-only check for optimistic redirects
  const sessionToken = getSessionCookie(req);
  const hasSessionCookie = !!sessionToken;

  const isOnPublicRoute = publicRoutes.includes(req.nextUrl.pathname);

  // If on a protected route without any session cookie, redirect to login
  // NOTE: This is NOT a security check, only for UX
  if (!isOnPublicRoute && !hasSessionCookie) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  // If logged in (has cookie) and trying to access login/register, redirect to dashboard
  if ((req.nextUrl.pathname === "/login" || req.nextUrl.pathname === "/register") && hasSessionCookie) {
    return NextResponse.redirect(new URL("/dashboard", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for:
     * - api routes (handled by Better Auth API)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!api|_next/static|_next/image|favicon.ico|public).*)",
  ],
};
```

## Session Management Best Practices

```typescript
// lib/session-utils.ts
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

// Get session with strict validation (forces DB lookup)
export async function getStrictSession() {
  const session = await auth.api.getSession({
    headers: await headers(),
    query: {
      disableCookieCache: true // Forces database validation
    }
  });

  return session;
}

// Revoke session (for logout, security operations)
export async function revokeCurrentSession() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (session) {
    await auth.api.revokeSession({
      sessionId: session.session.id,
      headers: await headers(),
    });
  }
}

// Revoke all other sessions (for password change, security)
export async function revokeOtherSessions() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (session) {
    await auth.api.revokeOtherSessions({
      userId: session.user.id,
      headers: await headers(),
    });
  }
}
```

## Security Hardening

```typescript
// Additional security measures in auth configuration
advanced: {
  // Disable CSRF and origin checks only if you know exactly why (NEVER in production)
  // disableCSRFCheck: false, // Default and recommended
  // disableOriginCheck: false, // Default and recommended

  // Additional security settings
  useSecureCookies: process.env.NODE_ENV === "production",
  cookiePrefix: "yourapp",
  defaultCookieAttributes: {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: process.env.NODE_ENV === "production" ? "none" : "lax",
    path: "/",
  }
},
rateLimit: {
  enabled: process.env.NODE_ENV === "production",
  window: 60 * 1000, // 1 minute window
  max: 10, // 10 attempts per window
  // Stricter limits for sensitive routes
  overrides: {
    signIn: { max: 5 },
    forgotPassword: { max: 3 },
  }
},
logger: {
  level: process.env.NODE_ENV === "production" ? "warn" : "debug"
}
```

## Better Auth MCP Usage

Use `@better-auth:list_files` to see available documentation:
```typescript
// List all knowledge base files
@better-auth:list_files
```

Use `@better-auth:search` to find specific topics:
```typescript
// Search for session configuration
@better-auth:search query="session management configuration"
```

## Production Deployment Best Practices

1. **Set Environment Variables**: Ensure `BETTER_AUTH_SECRET` is set in your hosting platform (Vercel, Netlify, etc.)
2. **Database Indexes**: Create indexes on `sessions.token`, `sessions.userId`, `users.email` for performance
3. **Dynamic Pages**: Add `export const dynamic = 'force-dynamic';` to protected pages to prevent static generation
4. **Cookie Configuration**: Use appropriate cookie settings for production (secure, sameSite, httpOnly)
5. **Base URL Configuration**: Set correct baseURL for your production environment
6. **Secret Validation**: Ensure the same secret is used across all runtimes (Edge, Serverless)
7. **Trusted Origins**: Include all domains where your app will be hosted
8. **Session Validation**: Always validate sessions server-side for protected routes
9. **Rate Limiting**: Enable rate limiting in production to prevent abuse
10. **Logging**: Set appropriate log levels for production (error/warn)

## Common Production Issues and Fixes

1. **Dashboard redirects to login despite valid session**: Add `dynamic = 'force-dynamic'` to the page
2. **Sign-in works but session not persisted**: Check that `BETTER_AUTH_SECRET` is the same in all environments
3. **Cookies not working in production**: Verify cookie attributes (secure, sameSite) are appropriate for HTTPS
4. **Middleware blocking access**: Use Node.js runtime for full validation or presence-only check for Edge
5. **Static generation issues**: Mark protected routes as dynamic to prevent pre-rendering
6. **Slow session lookups**: Add database indexes on session and user tables
7. **Session validation fails in middleware**: Pass headers correctly to auth.api.getSession()

## Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_sessions_token ON sessions(token);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
CREATE INDEX idx_verifications_identifier ON verifications(identifier);
```

## Troubleshooting Checklist

- [ ] BETTER_AUTH_SECRET is set in production environment
- [ ] Page is marked as dynamic if it checks for session
- [ ] Cookie attributes are configured for production (secure, sameSite, httpOnly)
- [ ] Trusted origins include production domain
- [ ] BaseURL is configured correctly for production
- [ ] Middleware passes headers correctly to auth.api.getSession()
- [ ] nextCookies plugin is installed and positioned last in plugins
- [ ] Database indexes are created for performance
- [ ] Redeploy after environment variable changes
- [ ] Runtime is set to "nodejs" in middleware if full validation is needed
- [ ] CSRF and origin checks are enabled in production
- [ ] Rate limiting is enabled in production
