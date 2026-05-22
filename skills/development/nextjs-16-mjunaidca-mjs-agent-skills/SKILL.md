---
name: nextjs-16
description: Build Next.js 16 applications with the correct patterns. Use this skill when creating pages, layouts, middleware (now proxy.ts), dynamic routes, or upgrading from Next.js 15. Covers breaking changes like async params/searchParams, Turbopack defaults, proxy.ts (replacing middleware.ts), and cacheComponents.
---

# Next.js 16

Build Next.js 16 applications correctly. This skill prevents common mistakes when working with Next.js 16's breaking changes.

## When to Use

- Creating new Next.js 16 projects
- Upgrading from Next.js 15 to 16
- Working with dynamic routes and params
- Implementing request proxying (formerly middleware)
- Configuring Turbopack builds
- Using cacheComponents (formerly dynamicIO)

## Critical Breaking Changes

### 1. params and searchParams are Now Promises

**THIS IS THE MOST COMMON MISTAKE.** In Next.js 16, `params` and `searchParams` are asynchronous.

```typescript
// WRONG - Next.js 15 pattern (WILL FAIL)
export default function Page({ params }: { params: { id: string } }) {
  return <div>ID: {params.id}</div>
}

// CORRECT - Next.js 16 pattern
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  return <div>ID: {id}</div>
}
```

**For searchParams:**

```typescript
// WRONG - Next.js 15 pattern
export default function Page({
  searchParams
}: {
  searchParams: { query: string }
}) {
  return <div>Query: {searchParams.query}</div>
}

// CORRECT - Next.js 16 pattern
export default async function Page({
  searchParams,
}: {
  searchParams: Promise<{ query?: string }>
}) {
  const { query } = await searchParams
  return <div>Query: {query}</div>
}
```

**In layouts:**

```typescript
// CORRECT - Layout with async params
export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  return (
    <div>
      <nav>Current: {slug}</nav>
      {children}
    </div>
  )
}
```

**In generateMetadata:**

```typescript
// CORRECT - Async params in metadata
export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params
  const product = await getProduct(id)
  return { title: product.name }
}
```

### 2. middleware.ts is Now proxy.ts

**DO NOT CREATE `middleware.ts` in Next.js 16.** Use `proxy.ts` instead.

```typescript
// File: proxy.ts (NOT middleware.ts)
// Location: project root (same level as app/)

import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'

// WRONG: export function middleware() {}
// CORRECT:
export function proxy(request: NextRequest) {
  // Check auth
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

// Matcher config remains the same
export const config = {
  matcher: ['/dashboard/:path*', '/api/:path*'],
}
```

**Key differences from middleware:**
- File renamed: `middleware.ts` → `proxy.ts`
- Function renamed: `middleware()` → `proxy()`
- Location: Still at project root
- Matcher config: Same syntax

### 3. Turbopack is Now Default

Turbopack is the default bundler. The `--turbopack` flag is no longer needed.

```bash
# Next.js 15
next dev --turbopack

# Next.js 16 (Turbopack is default)
next dev
```

**Configuration moved to top-level:**

```typescript
// next.config.ts

// WRONG - Next.js 15 pattern
const config = {
  experimental: {
    turbo: {
      rules: { /* ... */ }
    }
  }
}

// CORRECT - Next.js 16 pattern
const config = {
  turbopack: {
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },
}
```

### 4. cacheComponents Replaces dynamicIO

The `dynamicIO` experimental flag is now `cacheComponents`:

```typescript
// next.config.ts

// WRONG - Next.js 15 pattern
const config = {
  experimental: {
    dynamicIO: true,
  }
}

// CORRECT - Next.js 16 pattern
const config = {
  cacheComponents: true,
}
```

### 5. Parallel Routes Require default.js

**Parallel routes MUST have a `default.js` file** or you'll get 404 errors during soft navigation.

```
app/
├── @modal/
│   ├── default.tsx    ← REQUIRED
│   └── login/
│       └── page.tsx
├── layout.tsx
└── page.tsx
```

```typescript
// app/@modal/default.tsx
export default function Default() {
  return null
}
```

### 6. Image Component Changes

Several `next/image` props have changed:

```typescript
// WRONG - Next.js 15 patterns
<Image
  src="/photo.jpg"
  layout="fill"           // Removed
  objectFit="cover"       // Removed
  objectPosition="center" // Removed
  lazyBoundary="200px"    // Removed
  lazyRoot={ref}          // Removed
/>

// CORRECT - Next.js 16 patterns
<Image
  src="/photo.jpg"
  fill                    // Use fill prop
  style={{
    objectFit: 'cover',
    objectPosition: 'center'
  }}
/>
```

### 7. Route Handlers Async Context

Route handlers also need async params:

```typescript
// WRONG
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  return Response.json({ id: params.id })
}

// CORRECT
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params
  return Response.json({ id })
}
```

## Quick Start

```bash
# Create new Next.js 16 project
npx create-next-app@latest my-app

# Or upgrade existing project
npm install next@16 react@latest react-dom@latest
```

## Project Structure (Next.js 16)

```
my-app/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   ├── globals.css
│   ├── @modal/              # Parallel route
│   │   ├── default.tsx      # REQUIRED default
│   │   └── login/
│   │       └── page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   └── [id]/            # Dynamic route
│   │       └── page.tsx     # Uses async params
│   └── api/
│       └── tasks/
│           └── [id]/
│               └── route.ts # Uses async params
├── proxy.ts                 # NOT middleware.ts
├── next.config.ts           # Turbopack at top-level
├── package.json
└── tsconfig.json
```

## Common Patterns

### httpOnly Cookie Proxy (Auth Token Forwarding)

When using Better Auth or similar with httpOnly cookies, JavaScript cannot access the token. Create a server-side API route to forward requests with the token:

```typescript
// app/api/proxy/[...path]/route.ts
import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  const cookieStore = await cookies();

  // Read httpOnly cookie (only accessible server-side)
  const idToken = cookieStore.get("auth_token")?.value;

  if (!idToken) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  // Build target URL
  const targetPath = "/" + path.join("/");
  const url = new URL(targetPath, BACKEND_URL);

  // Forward query params
  request.nextUrl.searchParams.forEach((value, key) => {
    url.searchParams.set(key, value);
  });

  try {
    const body = await request.text();

    const response = await fetch(url.toString(), {
      method: "POST",
      headers: {
        Authorization: `Bearer ${idToken}`,
        "Content-Type": "application/json",
      },
      body: body || undefined,
    });

    // Handle SSE streaming responses
    if (response.headers.get("content-type")?.includes("text/event-stream")) {
      return new Response(response.body, {
        status: response.status,
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          "Connection": "keep-alive",
        },
      });
    }

    const data = await response.json().catch(() => null);
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("[Proxy] Error:", error);
    return NextResponse.json({ error: "Proxy request failed" }, { status: 500 });
  }
}

// Add GET, PUT, DELETE as needed with same pattern
```

**Key points:**
- httpOnly cookies are a security feature - JavaScript cannot read them
- Server-side API routes CAN read all cookies via `cookies()` from `next/headers`
- Always handle SSE streaming by passing through `response.body`
- Use `credentials: "include"` on client fetch to send cookies to the proxy

**Evidence**: `web-dashboard/src/app/api/chatkit/route.ts`

### Script Loading for Web Components (beforeInteractive)

External web component scripts must load before React hydration. Use `beforeInteractive` in root layout:

```tsx
// app/layout.tsx
import Script from "next/script";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        {/* MUST be in <head> with beforeInteractive for web components */}
        <Script
          src="https://cdn.example.com/web-component.js"
          strategy="beforeInteractive"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

**Script strategies:**
| Strategy | When It Loads | Use Case |
|----------|---------------|----------|
| `beforeInteractive` | Before hydration, in `<head>` | Web components, critical JS |
| `afterInteractive` | After page interactive | Analytics, non-critical |
| `lazyOnload` | During idle time | Low priority |

**Evidence**: `web-dashboard/src/app/layout.tsx`

### Dynamic Route with Data Fetching

```typescript
// app/tasks/[id]/page.tsx
import { notFound } from 'next/navigation'

interface Props {
  params: Promise<{ id: string }>
}

async function getTask(id: string) {
  const res = await fetch(`${process.env.API_URL}/api/tasks/${id}`)
  if (!res.ok) return null
  return res.json()
}

export async function generateMetadata({ params }: Props) {
  const { id } = await params
  const task = await getTask(id)
  return { title: task?.title ?? 'Task Not Found' }
}

export default async function TaskPage({ params }: Props) {
  const { id } = await params
  const task = await getTask(id)

  if (!task) notFound()

  return (
    <div>
      <h1>{task.title}</h1>
      <p>Status: {task.status}</p>
    </div>
  )
}
```

### Search Page with Filters

```typescript
// app/search/page.tsx
interface Props {
  searchParams: Promise<{
    query?: string
    status?: string
    page?: string
  }>
}

export default async function SearchPage({ searchParams }: Props) {
  const { query, status, page = '1' } = await searchParams

  const results = await fetch(
    `${process.env.API_URL}/api/search?` +
    new URLSearchParams({
      ...(query && { query }),
      ...(status && { status }),
      page,
    })
  ).then(r => r.json())

  return (
    <div>
      <h1>Search Results for: {query}</h1>
      {results.map(r => <div key={r.id}>{r.title}</div>)}
    </div>
  )
}
```

### Proxy with Auth Check

```typescript
// proxy.ts
import { NextRequest, NextResponse } from 'next/server'

const publicPaths = ['/', '/login', '/register', '/api/auth']

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Allow public paths
  if (publicPaths.some(p => pathname.startsWith(p))) {
    return NextResponse.next()
  }

  // Check for auth token
  const token = request.cookies.get('session')?.value

  if (!token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('callbackUrl', pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Add user header for API routes
  const response = NextResponse.next()
  response.headers.set('x-user-token', token)
  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

### API Route with Validation

```typescript
// app/api/tasks/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'

interface Props {
  params: Promise<{ id: string }>
}

export async function GET(request: NextRequest, { params }: Props) {
  const { id } = await params

  // Fetch from backend
  const res = await fetch(`${process.env.BACKEND_URL}/api/tasks/${id}`, {
    headers: {
      Authorization: request.headers.get('Authorization') ?? '',
    },
  })

  if (!res.ok) {
    return NextResponse.json(
      { error: 'Task not found' },
      { status: 404 }
    )
  }

  return NextResponse.json(await res.json())
}

export async function PATCH(request: NextRequest, { params }: Props) {
  const { id } = await params
  const body = await request.json()

  const res = await fetch(`${process.env.BACKEND_URL}/api/tasks/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: request.headers.get('Authorization') ?? '',
    },
    body: JSON.stringify(body),
  })

  return NextResponse.json(await res.json(), { status: res.status })
}
```

## next.config.ts Template

```typescript
import type { NextConfig } from 'next'

const config: NextConfig = {
  // Turbopack config (was experimental.turbo)
  turbopack: {
    rules: {
      '*.svg': {
        loaders: ['@svgr/webpack'],
        as: '*.js',
      },
    },
  },

  // Cache components (was experimental.dynamicIO)
  cacheComponents: true,

  // Environment variables (public)
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  // Images
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },

  // Rewrites for API proxy
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL}/api/:path*`,
      },
    ]
  },
}

export default config
```

## Migration Checklist

When upgrading from Next.js 15:

- [ ] Rename `middleware.ts` to `proxy.ts`
- [ ] Rename `middleware()` function to `proxy()`
- [ ] Update all page components with async `params`
- [ ] Update all page components with async `searchParams`
- [ ] Update all route handlers with async `params`
- [ ] Update `generateMetadata` with async `params`
- [ ] Move `turbo` config from `experimental.turbo` to `turbopack`
- [ ] Replace `dynamicIO` with `cacheComponents`
- [ ] Add `default.tsx` to all parallel routes
- [ ] Update `next/image` usage (remove layout, objectFit props)
- [ ] Remove `--turbopack` flag from dev scripts

## Common Pitfalls

### 1. Forgetting to await params

```typescript
// WRONG - Results in Promise object, not value
export default async function Page({ params }) {
  return <div>ID: {params.id}</div>  // Shows [object Promise]
}

// CORRECT
export default async function Page({ params }) {
  const { id } = await params
  return <div>ID: {id}</div>
}
```

### 2. Using middleware.ts

```typescript
// WRONG - File will be ignored
// middleware.ts

// CORRECT - Use proxy.ts
// proxy.ts
export function proxy(request) { ... }
```

### 3. Missing default.tsx in parallel routes

```
// WRONG - 404 during soft navigation
app/@sidebar/page.tsx

// CORRECT - Include default
app/@sidebar/default.tsx
app/@sidebar/page.tsx
```

### 4. Old turbo config location

```typescript
// WRONG
experimental: { turbo: {} }

// CORRECT
turbopack: {}
```

### 5. Reading httpOnly cookies from JavaScript

```typescript
// WRONG - httpOnly cookies cannot be read from JavaScript
const token = document.cookie.split('; ')
  .find(row => row.startsWith('auth_token='));
// Returns undefined even if cookie exists

// CORRECT - Use server-side API route proxy
// app/api/proxy/route.ts reads cookies via next/headers
const cookieStore = await cookies();
const token = cookieStore.get("auth_token")?.value;
```

### 6. Script afterInteractive for web components

```typescript
// WRONG - Web component not defined when React renders
<Script src="https://cdn.example.com/component.js" strategy="afterInteractive" />

// CORRECT - Load before React hydration
<head>
  <Script src="https://cdn.example.com/component.js" strategy="beforeInteractive" />
</head>
```

## References

For additional documentation, use Next.js DevTools MCP:
```
mcp__next-devtools__nextjs_docs with action="get" and path="/docs/app/guides/upgrading/version-16"
```

Or Context7:
```
mcp__context7__get-library-docs with context7CompatibleLibraryID="/vercel/next.js" and topic="app router"
```
