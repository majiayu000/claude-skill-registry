---
name: nextjs-app-router
description: >
  Next.js App Router patterns including server components, route handlers, middleware,
  parallel routes, intercepting routes, streaming, and caching strategies. Use when the user
  is building with Next.js 13+/14+/15+, asking about the App Router, server components vs
  client components, route handlers, Next.js middleware, or Next.js caching and revalidation.
  Trigger on any mention of Next.js, App Router, server components, or Next.js API routes.
---

# Next.js App Router Patterns

Patterns for building applications with the Next.js App Router architecture.

## When to Use
- User is building or migrating to Next.js App Router
- User asks about server vs client components
- User needs route handlers, middleware, or API routes
- User asks about parallel routes or intercepting routes
- User needs streaming, Suspense, or loading states
- User asks about Next.js caching or revalidation

## Core Patterns

### Server Components (Default)

All components in the App Router are server components by default. They run on the server, can access databases directly, and send zero JavaScript to the client.

```tsx
// app/products/page.tsx -- Server Component (no "use client" directive)
import { db } from '@/lib/db'

interface Product {
  id: string
  name: string
  price: number
}

export default async function ProductsPage() {
  const products: Product[] = await db.query('SELECT * FROM products ORDER BY name')

  return (
    <main>
      <h1>Products</h1>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            {p.name} -- ${p.price}
          </li>
        ))}
      </ul>
    </main>
  )
}
```

Use `"use client"` only when the component needs interactivity (event handlers, hooks, browser APIs).

```tsx
'use client'
// app/products/add-to-cart-button.tsx -- Client Component
import { useState } from 'react'

export function AddToCartButton({ productId }: { productId: string }) {
  const [isPending, setIsPending] = useState(false)

  const handleClick = async () => {
    setIsPending(true)
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    })
    setIsPending(false)
  }

  return (
    <button onClick={handleClick} disabled={isPending}>
      {isPending ? 'Adding...' : 'Add to Cart'}
    </button>
  )
}
```

### Route Handlers

Replace API routes from Pages Router. Define HTTP methods as named exports.

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'
import { db } from '@/lib/db'

const CreateUserSchema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
})

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl
  const page = parseInt(searchParams.get('page') || '1', 10)
  const limit = parseInt(searchParams.get('limit') || '20', 10)

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  })

  return NextResponse.json({ data: users, meta: { page, limit } })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const parsed = CreateUserSchema.safeParse(body)

  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 })
  }

  const user = await db.user.create({ data: parsed.data })
  return NextResponse.json({ data: user }, { status: 201 })
}
```

### Middleware

Runs before every request. Use for authentication, redirects, header injection, and geolocation.

```tsx
// middleware.ts (root of project)
import { NextRequest, NextResponse } from 'next/server'

const publicPaths = new Set(['/', '/login', '/signup', '/api/auth'])

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  if (publicPaths.has(pathname)) {
    return NextResponse.next()
  }

  const token = request.cookies.get('session')?.value
  if (!token) {
    const loginUrl = new URL('/login', request.url)
    loginUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(loginUrl)
  }

  const response = NextResponse.next()
  response.headers.set('x-request-id', crypto.randomUUID())
  return response
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
}
```

### Parallel Routes and Streaming

Use named slots (`@folder/`) to render multiple pages simultaneously in the same layout. The layout receives each slot as a prop.

```tsx
// app/layout.tsx -- @analytics and @feed are parallel route slots
export default function DashboardLayout({
  children, analytics, feed,
}: {
  children: React.ReactNode; analytics: React.ReactNode; feed: React.ReactNode
}) {
  return (
    <div className="grid grid-cols-3 gap-4">
      <main className="col-span-2">{children}</main>
      <aside>{analytics}{feed}</aside>
    </div>
  )
}
```

Wrap slow server components in Suspense to stream UI progressively.

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react'

export default function DashboardPage() {
  return (
    <main>
      <Suspense fallback={<ChartSkeleton />}><RevenueChart /></Suspense>
      <Suspense fallback={<TableSkeleton />}><RecentOrders /></Suspense>
    </main>
  )
}
```

### Caching and Revalidation

Control caching at the fetch level or route segment level.

```tsx
// Time-based revalidation: refetch every 60 seconds
const products = await fetch('https://api.example.com/products', {
  next: { revalidate: 60 },
})

// On-demand revalidation via Server Action
'use server'
import { revalidatePath, revalidateTag } from 'next/cache'

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data })
  revalidateTag('products')     // Invalidate by tag
  revalidatePath('/products')   // Invalidate by path
}

// Tag a fetch for on-demand revalidation
const products = await fetch('https://api.example.com/products', {
  next: { tags: ['products'] },
})
```

## Anti-Patterns

- **Marking everything "use client"** -- This defeats the purpose of server components. Only add the directive to components that genuinely need interactivity or browser APIs. Keep data fetching in server components.
- **Fetching data in client components when server components suffice** -- If the data is needed at render time and does not depend on user interaction, fetch it in a server component.
- **Using `getServerSideProps` or `getStaticProps`** -- These belong to the Pages Router. In App Router, fetch data directly in server components or use route handlers.
- **Ignoring loading.tsx and error.tsx** -- Every route segment should have loading and error boundaries. Without them, errors crash the entire page and loading states are absent.
- **Over-caching** -- Caching mutable data without revalidation leads to stale content. Always pair caching with an appropriate revalidation strategy.

## Quick Reference

| File | Purpose |
|------|---------|
| `page.tsx` | Route UI (required to make route accessible) |
| `layout.tsx` | Shared layout wrapping child routes |
| `loading.tsx` | Suspense fallback for the route segment |
| `error.tsx` | Error boundary for the route segment |
| `not-found.tsx` | 404 UI for the route segment |
| `route.ts` | API endpoint (GET, POST, PUT, DELETE) |
| `middleware.ts` | Runs before requests (auth, redirects) |
| `@folder/` | Named slot for parallel routes |
| `(group)/` | Route group (no URL segment) |
| `[param]/` | Dynamic route segment |

Default: server component. Add `"use client"` only for interactivity.
