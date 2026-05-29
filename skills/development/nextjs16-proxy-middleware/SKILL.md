---
name: nextjs16-proxy-middleware
description: Comprehensive guide for implementing Next.js 16 proxy pattern for authentication and route protection. Covers the new proxy.ts API, protected route patterns, authentication middleware, and best practices for serverless environments. Use when implementing route protection, authentication middleware, or migrating from middleware.ts to proxy.ts.
---

# Next.js 16 Proxy Pattern & Middleware

This skill covers the new **proxy pattern** introduced in Next.js 16, which replaces the legacy `middleware.ts` approach. The proxy is optimized for Vercel's serverless environment and provides cleaner semantics.

## What Changed in Next.js 16

### Before (middleware.ts)

```typescript
// middleware.ts - Legacy (deprecated)
import { NextResponse } from "next/server";
export function middleware(request) {
  // Logic here
}
export const config = { matcher: [...] };
```

### After (proxy.ts) ✅

```typescript
// proxy.ts - New Convention (recommended)
import { NextResponse } from "next/server";
export async function proxy(request) {
  // Logic here
}
export const config = { matcher: [...] };
```

**Key differences:**

- Function name: `middleware()` → `proxy()`
- Clearer intent: "proxy between client and server"
- Better semantics for Next.js ecosystem
- Automatic loading without export naming conventions

## Project Implementation (The Simpsons API)

### Protected Routes

The [proxy.ts](../../../../proxy.ts) file implements authentication-based route protection:

**Protected Routes:**

- `/diary` - User personal diary
- `/collections` - User quote collections
- `/episodes` - Episode ratings and notes (list + detail pages)
- `/characters` - Comments and follows (list + detail pages)

**Accessible without authentication:**

- `/` - Home page
- `/guide` - Public guide
- `/login` - Sign-in page
- `/register` - Sign-up page
- `/api` - API routes (handled separately)

### Route Pattern Matching

**✅ CORRECT - Protects both variants:**

```typescript
const protectedPaths = [
  "/diary",
  "/collections",
  "/episodes", // Protects /episodes (list)
  "/episodes/", // Protects /episodes/ (with trailing)
  "/characters", // Protects /characters (list)
  "/characters/", // Protects /characters/ (with trailing)
];
```

**❌ WRONG - Only protects with trailing slash:**

```typescript
const protectedPaths = [
  "/episodes/", // Misses: /episodes
  "/characters/", // Misses: /characters
];
```

**Why both matter:**

- Next.js routing treats `/episodes` and `/episodes/` as potentially different
- Users may bookmark either URL variant
- Must protect both to ensure complete security

### Matcher Configuration

The `config.matcher` pattern determines which routes the proxy runs on:

```typescript
export const config = {
  matcher: [
    // Match all routes EXCEPT:
    "/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

**What this excludes:**

- `/api/*` - API routes handled separately
- `/_next/static/*` - Static assets
- `/_next/image/*` - Image optimization
- `/favicon.ico` - Favicon
- All image files (svg, png, jpg, etc.)

**What this includes:**

- `/` and all dynamic routes
- `/login` and `/register`
- `/diary`, `/episodes`, `/characters`, etc.

## Implementation Pattern

### 1. Session Validation

```typescript
export async function proxy(request: NextRequest) {
  // Validate session using Better Auth
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const isAuthenticated = !!session?.user;
  const { pathname } = request.nextUrl;

  // ... route protection logic
}
```

**Key points:**

- Extract session from request headers
- Check for presence of `session?.user`
- Use `pathname` from `request.nextUrl` (not `request.url`)

### 2. Protected Route Pattern

```typescript
const protectedPaths = ["/diary", "/collections", "/episodes", "/characters"];

const isProtectedRoute = protectedPaths.some((path) =>
  pathname.startsWith(path)
);

if (isProtectedRoute && !isAuthenticated) {
  const loginUrl = new URL("/login", request.url);
  loginUrl.searchParams.set("callbackUrl", pathname);
  return NextResponse.redirect(loginUrl);
}
```

**Important:**

- Use `pathname.startsWith()` for prefix matching
- Include root path (e.g., `/episodes` not just `/episodes/`)
- Set `callbackUrl` for post-login redirect
- Must handle both authenticated and unauthenticated states

### 3. Callback URL Implementation

After redirecting to login, the login page must use the `callbackUrl`:

```typescript
// app/login/page.tsx
import { useSearchParams, useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/";

  const handleSignIn = async (email, password) => {
    await authClient.signIn.email({
      email,
      password,
      onSuccess: () => {
        // Redirect to original page or home
        router.push(callbackUrl);
      },
    });
  };

  return (
    // Login form...
  );
}
```

### 4. Redirect Authenticated Users Away

```typescript
// Prevent authenticated users from visiting auth pages
if (isAuthenticated && (pathname === "/login" || pathname === "/register")) {
  return NextResponse.redirect(new URL("/", request.url));
}

return NextResponse.next();
```

## Common Patterns

### A. Simple Path Protection

```typescript
const protectedPaths = ["/admin", "/dashboard"];
const isProtected = protectedPaths.includes(pathname);

if (isProtected && !isAuthenticated) {
  return NextResponse.redirect(new URL("/login", request.url));
}
```

### B. Role-Based Protection (Future Enhancement)

```typescript
const adminPaths = ["/admin"];
const isAdmin = session?.user?.role === "admin";

if (adminPaths.some((p) => pathname.startsWith(p)) && !isAdmin) {
  return NextResponse.redirect(new URL("/unauthorized", request.url));
}
```

### C. Public Routes with Optional Auth

Some routes should work with OR without authentication:

```typescript
// e.g., Character detail page can show comments if authenticated
const publicButEnhanced = ["/characters", "/episodes"];
const isPublicRoute = publicButEnhanced.some((p) => pathname.startsWith(p));

if (isPublicRoute) {
  // Allow access but provide user data in response headers if authenticated
  if (isAuthenticated) {
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set("x-user-id", session.user.id);
    return NextResponse.next({ request: { headers: requestHeaders } });
  }
}
```

## Debugging

### Enable Logging

```typescript
const DEBUG = process.env.NODE_ENV === "development";

export async function proxy(request: NextRequest) {
  if (DEBUG) {
    console.log(`[PROXY] ${request.method} ${request.nextUrl.pathname}`);
    console.log(`[AUTH] Authenticated: ${!!session?.user}`);
  }

  // ... rest of logic
}
```

### Test with curl

```bash
# Without authentication
curl -i http://localhost:3000/diary

# Should redirect to login with callbackUrl parameter
# Location: http://localhost:3000/login?callbackUrl=/diary

# With session cookie
curl -i -b "session=..." http://localhost:3000/diary
# Should return 200
```

## Performance Considerations

### ⚠️ Session Validation Overhead

Each proxy invocation validates the session:

```typescript
const session = await auth.api.getSession({ headers: request.headers });
```

**Optimization strategies:**

1. **Cache session in headers** (already done in Better Auth)

   ```typescript
   // Better Auth caches in JWT
   // Minimal overhead per request
   ```

2. **Skip validation for public routes**

   ```typescript
   const publicRoutes = ["/", "/api", "/_next"];
   if (publicRoutes.some((p) => pathname.startsWith(p))) {
     return NextResponse.next();
   }
   ```

3. **Use regional compute** (handled by Vercel)
   - Proxy runs in same region as user
   - Reduces latency

## Security Best Practices

### 1. Always Validate Session State

```typescript
// ✅ CORRECT
const isAuthenticated = !!session?.user && session.user.id;

// ❌ WRONG
const isAuthenticated = !!session; // Doesn't check user
```

### 2. Use Secure Headers

```typescript
if (isAuthenticated) {
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-user-id", session.user.id);
  return NextResponse.next({ request: { headers: requestHeaders } });
}
```

### 3. Never Log Sensitive Data

```typescript
// ❌ DON'T DO THIS
console.log("Session:", session); // Could expose tokens

// ✅ DO THIS
console.log("Authenticated user:", session?.user?.id);
```

### 4. Validate Redirect URLs

```typescript
const callbackUrl = searchParams.get("callbackUrl");

// ❌ WRONG - Open redirect vulnerability
router.push(callbackUrl);

// ✅ CORRECT - Whitelist or validate
const validRedirects = ["/", "/diary", "/collections"];
router.push(validRedirects.includes(callbackUrl) ? callbackUrl : "/");
```

## Migration from middleware.ts

### Step 1: Rename the function

```typescript
// BEFORE
export function middleware(request) {}

// AFTER
export async function proxy(request) {}
```

### Step 2: Rename the file

```bash
mv middleware.ts proxy.ts
```

### Step 3: Update imports (if any)

Most cases don't need imports to change - they're framework-level.

### Step 4: Verify config

```typescript
// This stays the same
export const config = {
  matcher: [
    // ...
  ],
};
```

### Step 5: Test thoroughly

```bash
# Run locally
pnpm dev

# Test protected route
curl http://localhost:3000/diary
# Should redirect to login

# Test public route
curl http://localhost:3000/
# Should return 200
```

## Testing Protected Routes

### Manual Testing

```bash
# 1. Test redirect to login
curl -i http://localhost:3000/diary
# Expect: 307 redirect to /login?callbackUrl=/diary

# 2. Test public route still works
curl -i http://localhost:3000/
# Expect: 200

# 3. Test authenticated access
# First login in browser, then:
curl -i -b "cookie: ..." http://localhost:3000/diary
# Expect: 200 (or redirect to login page content)
```

### E2E Testing (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("protected routes redirect to login", async ({ page }) => {
  // Try to access protected route without auth
  await page.goto("/diary");

  // Should redirect to login with callbackUrl
  expect(page.url()).toContain("/login");
  expect(page.url()).toContain("callbackUrl=%2Fdiary");
});

test("authenticated users can access protected routes", async ({
  page,
  context,
}) => {
  // Login first (set session cookie)
  // Then access protected route
  await context.addCookies([
    {
      name: "session",
      value: "...", // valid session token
      domain: "localhost",
      path: "/",
    },
  ]);

  await page.goto("/diary");

  // Should show diary page, not login
  expect(page.url()).toBe("http://localhost:3000/diary");
});
```

## Troubleshooting

### Problem: Routes Not Protected

**Cause:** Matcher pattern doesn't include the route

**Solution:**

```typescript
// Check that route is in matcher and not excluded
export const config = {
  matcher: [
    // Should match your protected routes
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

### Problem: Session Always Null

**Cause:** Session not properly passed in headers

**Solution:**

```typescript
// Ensure Better Auth is properly configured
const session = await auth.api.getSession({
  headers: request.headers, // Must pass request headers
});
```

### Problem: Infinite Redirect Loop

**Cause:** Login page also protected or callbackUrl not handled

**Solution:**

```typescript
// Exclude login from protection
if (pathname === "/login" || pathname === "/register") {
  return NextResponse.next();
}

// Handle callbackUrl in login page
const callbackUrl = searchParams.get("callbackUrl") || "/";
// Use it after successful auth
```

## Resources

- [Next.js 16 Upgrade Guide](https://nextjs.org/docs/getting-started/upgrading)
- [Better Auth Documentation](https://better-auth.com)
- [Vercel Edge Middleware](https://vercel.com/docs/concepts/functions/edge-middleware)
- [The Simpsons API - proxy.ts](../../../../proxy.ts)

## See Also

- [Better Auth Migration Guide](../../../../docs/BETTER_AUTH_MIGRATION.md)
- [Vercel Environment Sync](../../../../docs/VERCEL_ENV_SYNC.md)
- [Project Architecture](../../../../docs/ARCHITECTURE.md)

```typescript
// proxy.ts
import { NextResponse, NextRequest } from "next/server";

/**
 * Función proxy - debe exportarse como default o named export "proxy"
 */
export async function proxy(request: NextRequest) {
  // Lógica de proxy
  return NextResponse.next();
}

/**
 * Config opcional - define rutas donde se ejecuta el proxy
 */
export const config = {
  matcher: ["/about/:path*", "/dashboard/:path*"],
};
```

## Configuración de Matcher

### Tipos de Matcher

#### 1. Path Simple

```typescript
export const config = {
  matcher: "/about",
};
```

#### 2. Múltiples Paths

```typescript
export const config = {
  matcher: ["/about", "/contact", "/dashboard/:path*"],
};
```

#### 3. Negative Lookahead (Excluir Rutas)

```typescript
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization)
     * - favicon.ico, sitemap.xml, robots.txt (metadata)
     */
    "/((?!api|_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt).*)",
  ],
};
```

#### 4. Matcher con Condiciones

```typescript
export const config = {
  matcher: [
    {
      source: "/api/:path*",
      locale: false, // Ignora locale-based routing
      has: [
        { type: "header", key: "Authorization", value: "Bearer Token" },
        { type: "query", key: "userId", value: "123" },
      ],
      missing: [{ type: "cookie", key: "session", value: "active" }],
    },
  ],
};
```

### Reglas de Matcher

1. **DEBE** empezar con `/`
2. Puede incluir parámetros nombrados: `/about/:path` (exacto) vs `/about/:path*` (wildcard)
3. Modificadores disponibles:
   - `*` = cero o más
   - `?` = cero o uno
   - `+` = uno o más
4. Puede usar regex: `/about/(.*)` es igual a `/about/:path*`
5. Los valores deben ser **constantes** (analizados en build-time)

## Patrones Comunes

### 1. Autenticación y Protección de Rutas

```typescript
import { NextResponse, NextRequest } from "next/server";
import { auth } from "@/lib/auth";

export async function proxy(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const isAuthenticated = !!session?.user;
  const { pathname } = request.nextUrl;

  // Rutas protegidas
  const protectedPaths = ["/dashboard", "/profile", "/admin"];
  const isProtected = protectedPaths.some((path) => pathname.startsWith(path));

  if (isProtected && !isAuthenticated) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/profile/:path*", "/admin/:path*"],
};
```

### 2. CORS Headers

```typescript
import { NextRequest, NextResponse } from "next/server";

const allowedOrigins = ["https://example.com", "https://app.example.com"];

const corsOptions = {
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export function proxy(request: NextRequest) {
  const origin = request.headers.get("origin") ?? "";
  const isAllowedOrigin = allowedOrigins.includes(origin);

  // Handle preflight requests
  if (request.method === "OPTIONS") {
    const preflightHeaders = {
      ...(isAllowedOrigin && { "Access-Control-Allow-Origin": origin }),
      ...corsOptions,
    };
    return NextResponse.json({}, { headers: preflightHeaders });
  }

  // Handle simple requests
  const response = NextResponse.next();

  if (isAllowedOrigin) {
    response.headers.set("Access-Control-Allow-Origin", origin);
  }

  Object.entries(corsOptions).forEach(([key, value]) => {
    response.headers.set(key, value);
  });

  return response;
}

export const config = {
  matcher: "/api/:path*",
};
```

### 3. Reescribir URLs (A/B Testing, Internationalization)

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  // A/B Testing con cookies
  const bucket = request.cookies.get("bucket")?.value;

  if (bucket === "b") {
    return NextResponse.rewrite(new URL("/variant-b", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: "/product/:path*",
};
```

### 4. Manejo de Cookies

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  // Leer cookies
  const sessionCookie = request.cookies.get("session");
  console.log(sessionCookie); // { name: 'session', value: 'abc123', Path: '/' }

  // Verificar existencia
  const hasSession = request.cookies.has("session");

  // Crear respuesta con cookies
  const response = NextResponse.next();

  // Establecer cookies
  response.cookies.set("theme", "dark");
  response.cookies.set({
    name: "user-id",
    value: "123",
    path: "/",
    httpOnly: true,
    secure: true,
    sameSite: "strict",
  });

  // Eliminar cookies
  response.cookies.delete("old-cookie");

  return response;
}
```

### 5. Request/Response Headers

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  // Clonar y modificar request headers
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-custom-header", "my-value");
  requestHeaders.set("x-pathname", request.nextUrl.pathname);

  // Pasar headers modificados a la app
  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });

  // Establecer response headers
  response.headers.set("x-response-header", "value");
  response.headers.set("Cache-Control", "public, max-age=3600");

  return response;
}
```

### 6. Responder Directamente (Sin Pasar a la App)

```typescript
import { NextRequest } from "next/server";
import { isAuthenticated } from "@/lib/auth";

export const config = {
  matcher: "/api/:function*",
};

export function proxy(request: NextRequest) {
  if (!isAuthenticated(request)) {
    return Response.json(
      { success: false, message: "authentication failed" },
      { status: 401 }
    );
  }

  // Continuar con la request
  return NextResponse.next();
}
```

### 7. Rate Limiting

```typescript
import { NextRequest, NextResponse } from "next/server";
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, "10 s"),
});

export async function proxy(request: NextRequest) {
  const ip = request.ip ?? "127.0.0.1";
  const { success } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }

  return NextResponse.next();
}

export const config = {
  matcher: "/api/:path*",
};
```

## Orden de Ejecución

El proxy se invoca para **cada ruta** en tu proyecto. Orden de ejecución:

1. `headers` de `next.config.js`
2. `redirects` de `next.config.js`
3. **Proxy** (`rewrites`, `redirects`, etc.)
4. `beforeFiles` (`rewrites`) de `next.config.js`
5. Filesystem routes (`public/`, `_next/static/`, `pages/`, `app/`)
6. `afterFiles` (`rewrites`) de `next.config.js`
7. Dynamic Routes (`/blog/[slug]`)
8. `fallback` (`rewrites`) de `next.config.js`

## Runtime

- Proxy usa por defecto **Node.js runtime**
- La opción de config `runtime` **NO** está disponible en archivos proxy
- Para Edge Runtime específico, considera usar Route Handlers en su lugar

## Flags Avanzados (next.config.js)

### skipTrailingSlashRedirect

Desactiva redirecciones automáticas de trailing slashes:

```javascript
// next.config.js
module.exports = {
  skipTrailingSlashRedirect: true,
};
```

```typescript
// proxy.ts
const legacyPrefixes = ["/docs", "/blog"];

export default async function proxy(req) {
  const { pathname } = req.nextUrl;

  if (legacyPrefixes.some((prefix) => pathname.startsWith(prefix))) {
    return NextResponse.next();
  }

  // Aplicar manejo personalizado de trailing slash
  if (!pathname.endsWith("/") && !pathname.match(/\.\w+$/)) {
    return NextResponse.redirect(
      new URL(`${req.nextUrl.pathname}/`, req.nextUrl)
    );
  }
}
```

### skipMiddlewareUrlNormalize

Desactiva normalización de URL para control total:

```javascript
// next.config.js
module.exports = {
  skipMiddlewareUrlNormalize: true,
};
```

## Mejores Prácticas

### ✅ HACER

1. **Usar matchers específicos** para limitar ejecución innecesaria
2. **Mantener la lógica ligera** - proxy se ejecuta en cada request
3. **Usar proxy como último recurso** - considera alternativas primero:
   - Server Components para lógica de servidor
   - Route Handlers para endpoints API
   - Server Actions para mutations
4. **Evitar módulos compartidos o globals** - proxy puede deployarse a CDN separadamente
5. **Pasar datos vía headers, cookies, rewrites o URL** - no confíes en estado compartido

### ❌ EVITAR

1. **No realizar operaciones pesadas** - impacta todos los requests
2. **No confiar en módulos compartidos** con el resto de la app
3. **No usar para lógica que puede ir en Server Components**
4. **No hacer queries a DB directamente** (si es posible evitarlo)
5. **No establecer headers grandes** - puede causar error 431

## Testing (Experimental)

Next.js 15.1+ incluye utilidades de testing:

```javascript
import { unstable_doesProxyMatch } from "next/experimental/testing/server";

// Verificar si proxy ejecuta en una URL
expect(
  unstable_doesProxyMatch({
    config,
    nextConfig,
    url: "/test",
  })
).toEqual(false);

// Testear función completa
import { isRewrite, getRewrittenUrl } from "next/experimental/testing/server";

const request = new NextRequest("https://nextjs.org/docs");
const response = await proxy(request);
expect(isRewrite(response)).toEqual(true);
expect(getRewrittenUrl(response)).toEqual("https://other-domain.com/docs");
```

## Soporte de Plataforma

| Opción de Deploy | Soportado                |
| ---------------- | ------------------------ |
| Node.js server   | ✅ Sí                    |
| Docker container | ✅ Sí                    |
| Static export    | ❌ No                    |
| Adapters         | Específico de plataforma |

## Troubleshooting

### Problema: Proxy no se ejecuta

**Solución**: Verificar matcher configuration

```typescript
// Antes (incorrecto)
export const config = {
  matcher: "about", // ❌ Falta el /
};

// Después (correcto)
export const config = {
  matcher: "/about", // ✅ Empieza con /
};
```

### Problema: Proxy se ejecuta en rutas estáticas

**Solución**: Excluir rutas estáticas con negative lookahead

```typescript
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

### Problema: Sesión/Auth no funciona

**Solución**: Verificar que Better Auth/NextAuth obtiene headers correctamente

```typescript
export async function proxy(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers, // ✅ Pasar headers
  });

  // Resto de la lógica
}
```

## Recursos

- [Documentación oficial de Proxy](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [NextRequest API](https://nextjs.org/docs/app/api-reference/functions/next-request)
- [NextResponse API](https://nextjs.org/docs/app/api-reference/functions/next-response)
- [path-to-regexp documentation](https://github.com/pillarjs/path-to-regexp)

## Versión

Esta skill está basada en **Next.js 16.1.1** (Enero 2026).
