---
name: nextjs
model: standard
description: Next.js App Router best practices — Server Components, data fetching, caching, routing, middleware, metadata, error handling, streaming, Server Actions, and performance optimization for Next.js 14-16+.
keywords: [next.js, nextjs, app router, server components, rsc, server actions, streaming, suspense, parallel routes, intercepting routes, metadata, middleware, caching, revalidation, image optimization, font optimization]
user-invocable: false
---

# Next.js App Router

Apply these patterns when building, reviewing, or debugging Next.js App Router applications.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install nextjs
```


## WHEN

- Building Next.js applications with App Router
- Migrating from Pages Router to App Router
- Implementing Server Components and streaming
- Setting up parallel and intercepting routes
- Optimizing data fetching and caching
- Building full-stack features with Server Actions
- Debugging hydration errors or RSC boundary issues

## Rendering Modes

| Mode | Where | When to Use |
|------|-------|-------------|
| **Server Components** | Server only | Data fetching, secrets, heavy computation |
| **Client Components** | Browser | Interactivity, hooks, browser APIs |
| **Static (SSG)** | Build time | Content that rarely changes |
| **Dynamic (SSR)** | Request time | Personalized or real-time data |
| **Streaming** | Progressive | Large pages, slow data sources |

### Server vs Client Decision Tree

```
Does it need...?
├── useState, useEffect, event handlers, browser APIs
│   └── Client Component ('use client')
├── Direct data fetching, no interactivity
│   └── Server Component (default)
└── Both?
    └── Split: Server parent fetches data → Client child handles UI
```

## File Conventions

See [file-conventions.md](references/file-conventions.md) for complete reference.

```
app/
├── layout.tsx          # Shared UI wrapper (persists across navigations)
├── page.tsx            # Route UI
├── loading.tsx         # Suspense fallback (automatic)
├── error.tsx           # Error boundary (must be 'use client')
├── not-found.tsx       # 404 UI
├── route.ts            # API endpoint (cannot coexist with page.tsx)
├── template.tsx        # Like layout but re-mounts on navigation
├── default.tsx         # Parallel route fallback
└── opengraph-image.tsx # OG image generation
```

Route segments: `[slug]` dynamic, `[...slug]` catch-all, `[[...slug]]` optional catch-all, `(group)` route group, `@slot` parallel route, `_folder` private (excluded from routing).

## Data Fetching Patterns

Choose the right pattern for each use case. See [data-patterns.md](references/data-patterns.md) for full decision tree.

| Pattern | Use Case | Caching |
|---------|----------|---------|
| Server Component fetch | Internal reads (preferred) | Full Next.js caching |
| Server Action | Mutations, form submissions | POST only, no cache |
| Route Handler | External APIs, webhooks, public REST | GET can be cached |
| Client fetch → API | Client-side reads (last resort) | HTTP cache headers |

### Server Component Data Fetching (Preferred)

```tsx
// app/products/page.tsx — Server Component by default
export default async function ProductsPage() {
  const products = await db.product.findMany() // Direct DB access, no API layer
  return <ProductGrid products={products} />
}
```

### Avoiding Data Waterfalls

```tsx
// BAD: Sequential — each awaits before the next starts
const user = await getUser()
const posts = await getPosts()

// GOOD: Parallel fetching
const [user, posts] = await Promise.all([getUser(), getPosts()])

// GOOD: Streaming with Suspense — each section loads independently
<Suspense fallback={<UserSkeleton />}><UserSection /></Suspense>
<Suspense fallback={<PostsSkeleton />}><PostsSection /></Suspense>
```

### Server Actions (Mutations)

```tsx
// app/actions.ts
'use server'
import { revalidateTag } from 'next/cache'

export async function addToCart(productId: string) {
  const cookieStore = await cookies()
  const sessionId = cookieStore.get('session')?.value
  if (!sessionId) redirect('/login')

  await db.cart.upsert({
    where: { sessionId_productId: { sessionId, productId } },
    update: { quantity: { increment: 1 } },
    create: { sessionId, productId, quantity: 1 },
  })
  revalidateTag('cart')
  return { success: true }
}
```

## Caching Strategy

| Method | Syntax | Use Case |
|--------|--------|----------|
| No cache | `fetch(url, { cache: 'no-store' })` | Always-fresh data |
| Static | `fetch(url, { cache: 'force-cache' })` | Rarely changes |
| ISR | `fetch(url, { next: { revalidate: 60 } })` | Time-based refresh |
| Tag-based | `fetch(url, { next: { tags: ['products'] } })` | On-demand invalidation |

Invalidate from Server Actions:

```tsx
'use server'
import { revalidateTag, revalidatePath } from 'next/cache'

export async function updateProduct(id: string, data: ProductData) {
  await db.product.update({ where: { id }, data })
  revalidateTag('products')   // Invalidate by tag
  revalidatePath('/products') // Invalidate by path
}
```

## RSC Boundaries

Props crossing Server → Client boundary **must be JSON-serializable**. See [rsc-boundaries.md](references/rsc-boundaries.md).

| Prop Type | Valid? | Fix |
|-----------|--------|-----|
| `string`, `number`, `boolean` | Yes | — |
| Plain object / array | Yes | — |
| Server Action (`'use server'`) | Yes | — |
| Function `() => {}` | **No** | Define inside client component |
| `Date` object | **No** | Use `.toISOString()` |
| `Map`, `Set`, class instance | **No** | Convert to plain object/array |

**Critical rule:** Client Components cannot be `async`. Fetch data in a Server Component parent and pass it down.

## Async APIs (Next.js 15+)

`params`, `searchParams`, `cookies()`, and `headers()` are all async. See [async-patterns.md](references/async-patterns.md).

```tsx
// Pages and layouts — always await params
type Props = { params: Promise<{ slug: string }> }

export default async function Page({ params }: Props) {
  const { slug } = await params
}

// Server functions
const cookieStore = await cookies()
const headersList = await headers()

// Non-async components — use React.use()
import { use } from 'react'
export default function Page({ params }: Props) {
  const { slug } = use(params)
}
```

## Routing Patterns

### Route Organization

| Pattern | Syntax | Purpose |
|---------|--------|---------|
| Route groups | `(marketing)/` | Organize without affecting URL |
| Parallel routes | `@analytics/` | Multiple independent sections in one layout |
| Intercepting routes | `(.)photos/[id]` | Modal overlays on soft navigation |
| Private folders | `_components/` | Exclude from routing |

### Parallel Routes & Modals

See [parallel-routes.md](references/parallel-routes.md) for complete modal pattern.

Key rules:
- Every `@slot` folder **must** have a `default.tsx` (returns `null`) or you get 404 on refresh
- Close modals with `router.back()`, **never** `router.push()` or `<Link>`
- Intercepting route matchers: `(.)` same level, `(..)` one level up, `(...)` from root

## Metadata & SEO

See [metadata.md](references/metadata.md) for OG images, sitemaps, and file conventions.

```tsx
// Static metadata (layout or page)
export const metadata: Metadata = {
  title: { default: 'My App', template: '%s | My App' },
  description: 'Built with Next.js',
}

// Dynamic metadata
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const post = await getPost(slug)
  return {
    title: post.title,
    description: post.description,
    openGraph: { images: [{ url: post.image, width: 1200, height: 630 }] },
  }
}
```

**Metadata is Server Components only.** If a page has `'use client'`, extract metadata to a parent layout.

## Error Handling

See [error-handling.md](references/error-handling.md) for full patterns including auth errors.

```tsx
// app/blog/error.tsx — must be 'use client'
'use client'
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

**Critical gotcha:** `redirect()`, `notFound()`, `forbidden()`, and `unauthorized()` throw special errors. Never catch them in try/catch:

```tsx
// BAD: redirect throw is caught — navigation fails!
try {
  await db.post.create({ data })
  redirect(`/posts/${post.id}`)
} catch (error) {
  return { error: 'Failed' } // Catches the redirect too!
}

// GOOD: Call redirect outside try-catch
let post
try { post = await db.post.create({ data }) }
catch (error) { return { error: 'Failed' } }
redirect(`/posts/${post.id}`)
```

## Streaming with Suspense

```tsx
export default async function ProductPage({ params }: Props) {
  const { id } = await params
  const product = await getProduct(id) // Blocking — loads first

  return (
    <div>
      <ProductHeader product={product} />
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={id} />       {/* Streams in independently */}
      </Suspense>
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations productId={id} /> {/* Streams in independently */}
      </Suspense>
    </div>
  )
}
```

### Hooks That Require Suspense Boundaries

| Hook | Suspense Required |
|------|-------------------|
| `useSearchParams()` | Always (or entire page becomes CSR) |
| `usePathname()` | In dynamic routes |
| `useParams()` | No |
| `useRouter()` | No |

## Performance

- **Always use `next/image`** over `<img>` — see [image-optimization.md](references/image-optimization.md)
- **Always use `next/link`** over `<a>` — client-side navigation with prefetching
- **Always use `next/font`** — see [font-optimization.md](references/font-optimization.md)
- **Always use `next/script`** — see [scripts.md](references/scripts.md)
- **Set `priority`** on above-the-fold images (LCP)
- **Add `sizes`** when using `fill` — without it, the largest image variant downloads
- **Dynamic imports** for heavy client components: `const Chart = dynamic(() => import('./Chart'))`
- **Use `generateStaticParams`** to pre-render dynamic routes at build time

## Route Handlers

See [route-handlers.md](references/route-handlers.md) for API endpoint patterns.

## Bundling

See [bundling.md](references/bundling.md) for fixing third-party package issues, server-incompatible packages, and ESM/CommonJS problems.

## Hydration Errors

See [hydration-errors.md](references/hydration-errors.md) for all causes and fixes.

| Cause | Fix |
|-------|-----|
| Browser APIs (`window`, `localStorage`) | Client component with `useEffect` mount check |
| `new Date().toLocaleString()` | Render on client with `useEffect` |
| `Math.random()` for IDs | Use `useId()` hook |
| `<p><div>...</div></p>` | Fix invalid HTML nesting |
| Third-party scripts modifying DOM | Use `next/script` with `afterInteractive` |

## Self-Hosting

See [self-hosting.md](references/self-hosting.md) for Docker, PM2, cache handlers, and deployment checklist.

Key points:
- Use `output: 'standalone'` for Docker — creates minimal production bundle
- Copy `public/` and `.next/static/` separately (not included in standalone)
- Set `HOSTNAME="0.0.0.0"` for containers
- Multi-instance ISR requires a custom cache handler (Redis/S3) — filesystem cache breaks
- Set health check endpoint at `/api/health`

## NEVER Do

| Never | Why | Instead |
|-------|-----|---------|
| Add `'use client'` by default | Bloats client bundle, loses Server Component benefits | Server Components are default — add `'use client'` only for interactivity |
| Make client components `async` | Not supported — will crash | Fetch in Server Component parent, pass data as props |
| Pass `Date`/`Map`/functions to client | Not serializable across RSC boundary | Serialize to string/plain object, or use Server Actions |
| Fetch from own API in Server Components | Unnecessary round-trip — you're already on the server | Access DB/service directly |
| Wrap `redirect()`/`notFound()` in try-catch | They throw special errors that get swallowed | Call outside try-catch or use `unstable_rethrow()` |
| Skip `loading.tsx` or Suspense fallbacks | Users see blank page during data loading | Always provide loading states |
| Use `useSearchParams` without Suspense | Entire page silently falls back to CSR | Wrap in `<Suspense>` boundary |
| Use `router.push()` to close modals | Breaks history, modal can flash/persist | Use `router.back()` |
| Use `@vercel/og` for OG images | Built into Next.js already | Import from `next/og` |
| Omit `default.tsx` in parallel route slots | Hard navigation (refresh) returns 404 | Add `default.tsx` returning `null` |
| Use Edge runtime unless required | Limited APIs, most npm packages break | Default Node.js runtime covers 95% of cases |
| Skip `sizes` prop on `fill` images | Downloads largest image variant always | Add `sizes="100vw"` or appropriate breakpoints |
| Import fonts in multiple components | Creates duplicate instances | Import once in layout, use CSS variable |
| Use `<link>` for Google Fonts | No optimization, blocks rendering | Use `next/font` |

## Reference Files

| File | Topic |
|------|-------|
| [rsc-boundaries.md](references/rsc-boundaries.md) | Server/Client boundary rules, serialization |
| [data-patterns.md](references/data-patterns.md) | Fetching decision tree, waterfall avoidance |
| [error-handling.md](references/error-handling.md) | Error boundaries, redirect gotcha, auth errors |
| [async-patterns.md](references/async-patterns.md) | Next.js 15+ async params/cookies/headers |
| [metadata.md](references/metadata.md) | SEO, OG images, sitemaps, file conventions |
| [parallel-routes.md](references/parallel-routes.md) | Modal pattern, intercepting routes, gotchas |
| [hydration-errors.md](references/hydration-errors.md) | Causes, debugging, fixes |
| [self-hosting.md](references/self-hosting.md) | Docker, PM2, cache handlers, deployment |
| [file-conventions.md](references/file-conventions.md) | Project structure, special files, middleware |
| [bundling.md](references/bundling.md) | Third-party packages, SSR issues, Turbopack |
| [image-optimization.md](references/image-optimization.md) | next/image best practices |
| [font-optimization.md](references/font-optimization.md) | next/font best practices |
| [scripts.md](references/scripts.md) | next/script, third-party loading |
| [route-handlers.md](references/route-handlers.md) | API endpoints, request/response helpers |
