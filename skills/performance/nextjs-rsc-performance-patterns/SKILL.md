---
name: nextjs-rsc-performance-patterns
version: "1.0"
description: >
  Performance optimization patterns for Next.js 14+ React Server Components.
  PROACTIVELY activate for: (1) Optimizing RSC data fetching, (2) Implementing streaming with Suspense,
  (3) Configuring caching and revalidation, (4) Parallel data fetching, (5) Partial Prerendering.
  Triggers: "rsc", "server component", "nextjs performance", "data fetching", "caching", "revalidate", "suspense", "streaming", "partial prerendering"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Next.js RSC Performance Patterns

This skill provides expert knowledge on optimizing Next.js 14+ applications using the App Router, focusing on React Server Components (RSC), data fetching strategies, and rendering optimizations to improve Core Web Vitals.

## RSC Data Fetching

React Server Components enable you to fetch data directly on the server, eliminating client-server request waterfalls and reducing JavaScript bundle size.

### Parallel Data Fetching

Fetch independent data sources in parallel to minimize total wait time:

```tsx
// app/product/[id]/page.tsx - GOOD
async function ProductPage({ params }: { params: { id: string } }) {
  // These fetches happen in parallel - Next.js automatically deduplicates
  const productPromise = fetch(`https://api.example.com/products/${params.id}`)
  const reviewsPromise = fetch(`https://api.example.com/reviews?product=${params.id}`)

  // Wait for both to complete
  const [productRes, reviewsRes] = await Promise.all([productPromise, reviewsPromise])
  const product = await productRes.json()
  const reviews = await reviewsRes.json()

  return <ProductDetails product={product} reviews={reviews} />
}
```

### Sequential vs Parallel Pattern

**Sequential (when data depends on previous result):**
```tsx
async function UserDashboard({ userId }: { userId: string }) {
  const user = await fetchUser(userId)
  // This depends on user data, so must be sequential
  const preferences = await fetchPreferences(user.preferencesId)
  return <Dashboard user={user} preferences={preferences} />
}
```

**Parallel (when data is independent):**
```tsx
async function UserDashboard({ userId }: { userId: string }) {
  // Fetch independent data in parallel
  const [user, notifications, activity] = await Promise.all([
    fetchUser(userId),
    fetchNotifications(userId),
    fetchActivity(userId)
  ])
  return <Dashboard user={user} notifications={notifications} activity={activity} />
}
```

### Next.js Extended fetch API

Next.js extends the native fetch API with automatic request deduplication and granular caching control:

```tsx
// Cached for 1 hour (3600 seconds)
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
})

// Revalidate on-demand using tags
const data = await fetch('https://api.example.com/products', {
  next: { tags: ['products'] }
})
// Later, trigger revalidation: revalidateTag('products')

// Force fresh data on every request (opt out of caching)
const data = await fetch('https://api.example.com/realtime', {
  cache: 'no-store'
})
```

## Streaming and Suspense

Streaming enables progressive loading, improving Time to First Byte (TTFB) and perceived performance by sending HTML to the browser incrementally.

### Basic Suspense Pattern

```tsx
// app/dashboard/page.tsx - GOOD
import { Suspense } from 'react'

async function RecentOrders() {
  // Slow data fetch
  const orders = await fetch('https://api.example.com/orders').then(r => r.json())
  return <OrdersList orders={orders} />
}

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading orders...</div>}>
        <RecentOrders />
      </Suspense>
    </div>
  )
}
```

The static content (h1) is sent immediately, while `RecentOrders` streams in when ready.

### Multiple Suspense Boundaries

```tsx
export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* These load independently and stream in as ready */}
      <Suspense fallback={<Skeleton />}>
        <RecentOrders />
      </Suspense>

      <Suspense fallback={<Skeleton />}>
        <Analytics />
      </Suspense>

      <Suspense fallback={<Skeleton />}>
        <Notifications />
      </Suspense>
    </div>
  )
}
```

### loading.js Convention

Next.js automatically wraps page content in a Suspense boundary when you provide a `loading.js` file:

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <div>Loading dashboard...</div>
}

// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchDashboardData() // Suspense boundary is automatic
  return <DashboardView data={data} />
}
```

## Partial Prerendering (PPR)

Partial Prerendering (Next.js 14.1+) combines static and dynamic rendering within a single route, serving a static shell immediately while streaming dynamic content.

### Enable PPR

```js
// next.config.js
module.exports = {
  experimental: {
    ppr: true,
  },
}
```

### PPR Pattern

```tsx
// app/product/[id]/page.tsx
import { Suspense } from 'react'

export const experimental_ppr = true

async function Reviews({ productId }: { productId: string }) {
  // Dynamic content - will be streamed
  const reviews = await fetch(`https://api.example.com/reviews/${productId}`, {
    cache: 'no-store'
  }).then(r => r.json())

  return <ReviewList reviews={reviews} />
}

export default async function ProductPage({ params }: { params: { id: string } }) {
  // Static content - prerendered
  const product = await fetch(`https://api.example.com/products/${params.id}`, {
    next: { revalidate: 3600 }
  }).then(r => r.json())

  return (
    <div>
      <ProductInfo product={product} />

      {/* Suspense boundary marks the dynamic "hole" */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />
      </Suspense>
    </div>
  )
}
```

The static shell (product info) is instantly served, while reviews stream in dynamically.

## Caching and Revalidation

Next.js provides multiple caching layers: Request Memoization, Data Cache, Full Route Cache, and Router Cache.

### Time-Based Revalidation

```tsx
// Revalidate every hour
async function BlogPosts() {
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }
  }).then(r => r.json())

  return <PostList posts={posts} />
}
```

### On-Demand Revalidation (Tag-Based)

```tsx
// app/products/page.tsx
async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { tags: ['products'] }
  }).then(r => r.json())

  return <ProductGrid products={products} />
}

// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const tag = request.nextUrl.searchParams.get('tag')

  if (tag) {
    revalidateTag(tag) // Purges all fetches tagged with 'products'
    return NextResponse.json({ revalidated: true, now: Date.now() })
  }

  return NextResponse.json({ revalidated: false }, { status: 400 })
}
```

### On-Demand Revalidation (Path-Based)

```tsx
// app/api/revalidate/route.ts
import { revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const path = request.nextUrl.searchParams.get('path')

  if (path) {
    revalidatePath(path) // Purges cache for specific route
    return NextResponse.json({ revalidated: true })
  }

  return NextResponse.json({ revalidated: false }, { status: 400 })
}
```

### Caching Decision Tree

1. **Dynamic, real-time data** (stock prices, user sessions): `cache: 'no-store'`
2. **Frequently changing data** (social feeds, news): Short revalidate (60-300s)
3. **Periodically updated data** (blog posts, product catalogs): Medium revalidate (3600s) + on-demand revalidation
4. **Rarely changing data** (legal pages, documentation): Long revalidate (86400s) or static

## Anti-Patterns

### Client-Side Data Fetching in useEffect

```tsx
// BAD - Creates request waterfall
'use client'
import { useState, useEffect } from 'react'

export default function ProductInfo({ id }) {
  const [product, setProduct] = useState(null)

  useEffect(() => {
    // Fetch only starts after JS loads and executes
    fetch(`/api/products/${id}`)
      .then(r => r.json())
      .then(setProduct)
  }, [id])

  return product ? <Display data={product} /> : <Loading />
}

// GOOD - Server Component fetches immediately
async function ProductInfo({ id }: { id: string }) {
  const product = await fetch(`https://api.example.com/products/${id}`, {
    next: { revalidate: 3600 }
  }).then(r => r.json())

  return <Display data={product} />
}
```

### Missing Suspense Boundaries

```tsx
// BAD - Entire page waits for slow fetch
export default async function Dashboard() {
  const slowData = await fetchSlowData() // Blocks entire page
  const fastData = await fetchFastData()

  return (
    <div>
      <FastSection data={fastData} />
      <SlowSection data={slowData} />
    </div>
  )
}

// GOOD - Suspense enables progressive loading
export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<FastSkeleton />}>
        <FastSection />
      </Suspense>

      <Suspense fallback={<SlowSkeleton />}>
        <SlowSection />
      </Suspense>
    </div>
  )
}
```

### Sequential Fetching When Parallel is Possible

```tsx
// BAD - Sequential fetching
async function UserProfile({ userId }) {
  const user = await fetchUser(userId)      // Wait
  const posts = await fetchPosts(userId)    // Then wait
  const friends = await fetchFriends(userId) // Then wait

  return <Profile user={user} posts={posts} friends={friends} />
}

// GOOD - Parallel fetching
async function UserProfile({ userId }) {
  const [user, posts, friends] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchFriends(userId)
  ])

  return <Profile user={user} posts={posts} friends={friends} />
}
```

### Over-Caching Dynamic Content

```tsx
// BAD - User-specific data cached globally
async function UserDashboard({ userId }) {
  const userData = await fetch(`https://api.example.com/users/${userId}`, {
    next: { revalidate: 3600 } // Wrong! This data is user-specific
  }).then(r => r.json())

  return <Dashboard data={userData} />
}

// GOOD - User-specific data not cached
async function UserDashboard({ userId }) {
  const userData = await fetch(`https://api.example.com/users/${userId}`, {
    cache: 'no-store' // Correct for user-specific data
  }).then(r => r.json())

  return <Dashboard data={userData} />
}
```

### Using img Instead of Image

```tsx
// BAD - Unoptimized images
<img src="/hero.jpg" alt="Hero" />

// GOOD - Optimized with next/image
import Image from 'next/image'

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // For LCP images
  sizes="100vw" // Responsive sizing
/>
```

## Performance Checklist

- [ ] Server Components used for all non-interactive UI
- [ ] Data fetching co-located with components that use it
- [ ] Independent data fetched in parallel with Promise.all()
- [ ] Suspense boundaries around slow data fetches
- [ ] loading.js files for automatic Suspense fallbacks
- [ ] Appropriate caching strategy for each data source
- [ ] On-demand revalidation for frequently changing content
- [ ] next/image used for all images
- [ ] Priority hint on LCP images
- [ ] No client-side data fetching in useEffect for initial render

## Core Web Vitals Impact

- **LCP (Largest Contentful Paint)**: Improved by streaming static content immediately, optimizing images with next/image
- **FID (First Input Delay)**: Improved by reducing client-side JavaScript through Server Components
- **CLS (Cumulative Layout Shift)**: Improved by proper image sizing, Suspense fallbacks with reserved space
