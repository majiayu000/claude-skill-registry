---
name: data-fetching
description: Best practices and conventions for server-side data fetching, caching, and rendering in Next.js 16+ applications.
---

## Overview

This skill covers server-side data fetching and caching patterns using Next.js 16+ Cache Components approach with Partial Prerendering (PPR). It combines fine-grained caching control with server-side data fetching for optimal performance.

## Core Principles

### Data Access Rules
- **NEVER call Drizzle ORM directly** - Always use server actions defined in `lib/actions/`
- **Cache at the component level** - Use the `use cache` directive in pages/layouts, not in action files
- **Wrap dynamic content** - Use `Suspense` boundaries to separate static and dynamic content
- **Use lifetime profiles** - Always specify `cacheLife()` with appropriate profile

## Cache Components Workflow

### 1. Planning Data Fetching
Before implementing:
- Identify what data is needed for the page/component
- Determine what content should be instantly visible (cached) vs. what can stream (dynamic)
- Locate the appropriate server actions in `lib/actions/` or create new ones if needed
- Plan cache tags for data that needs manual invalidation

### 2. Implementing Cached Data Fetching
Follow this pattern in pages or layouts:

```typescript
import { cacheLife } from 'next/cache'
import { getModels } from '@/lib/actions/models'

export default async function ModelsPage() {
  'use cache'
  cacheLife('hours')

  const models = await getModels()

  return <div>{/* render models */}</div>
}
```

### 3. Handling Dynamic Content
For runtime-dependent data (cookies, headers, searchParams):

```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <>
      <h1>Static Content</h1>
      <Suspense fallback={<Skeleton />}>
        <DynamicUserContent />
      </Suspense>
    </>
  )
}

async function DynamicUserContent() {
  const session = await getSession() // uses cookies()
  return <div>{session.user.name}</div>
}
```

## Caching Configuration

### Cache Life Profiles
Use built-in lifetime profiles with `cacheLife()`:

| Profile | Use Case | Duration |
|---------|----------|----------|
| `'seconds'` | Highly volatile data | ~30 seconds |
| `'minutes'` | Frequently updated content | ~5 minutes |
| `'hours'` | Semi-static content | ~1 hour |
| `'days'` | Mostly static content | ~1 day |
| `'weeks'` | Rarely changing content | ~1 week |
| `'max'` | Static content | Maximum duration |

**Default Choice:** Use `'hours'` for most content unless you have specific requirements.

### Cache Tags and Revalidation

#### Using `cacheTag` for Manual Invalidation
Tag cached data that needs to be invalidated on specific events:

```typescript
import { cacheLife, cacheTag } from 'next/cache'
import { getModelById } from '@/lib/actions/models'

export default async function ModelPage({ params }: { params: { id: string } }) {
  'use cache'
  cacheLife('hours')
  cacheTag('models', `model-${params.id}`)

  const model = await getModelById(params.id)
  return <div>{/* render model */}</div>
}
```

#### Invalidating Cache with `updateTag`
Use in server actions for immediate cache expiration (read-your-own-writes):

```typescript
'use server'
import { updateTag } from 'next/cache'

export async function updateModel(id: string, data: ModelData) {
  // Update database via action
  await updateModelAction(id, data)

  // Immediately expire cache so user sees fresh data
  updateTag(`model-${id}`, 'models')
}
```

#### Using `revalidateTag` for Background Refresh
For stale-while-revalidate pattern:

```typescript
'use server'
import { revalidateTag } from 'next/cache'

export async function createModel(data: ModelData) {
  await createModelAction(data)

  // Stale-while-revalidate: serve stale, refresh in background
  revalidateTag('models', 'max')
}
```

## Best Practices

### Caching Strategy
- **Cache pages/layouts, not actions** - Add `use cache` directive in pages/layouts that consume actions, never in action files themselves
- **Wrap actions in cached functions** - The page/layout function itself becomes the caching boundary
- **Use Suspense boundaries** - Separate static shell from dynamic/streaming content
- **Tag strategically** - Use cache tags for content that changes infrequently but needs manual updates

### Performance Optimization
- **Minimize dynamic APIs** - Avoid using `cookies()`, `headers()`, or `searchParams` in cached functions
- **Parallel data fetching** - Multiple server actions can be called in parallel within a cached component
- **Appropriate cache lifetimes** - Balance freshness needs with server load

### Data Mutation Patterns
- **Use `updateTag` for user mutations** - When users need to see their changes immediately
- **Use `revalidateTag` for background updates** - When serving slightly stale data is acceptable
- **Tag hierarchies** - Use multiple tags (e.g., `'models'` and `'model-123'`) for flexible invalidation

## Common Patterns

### Pattern 1: Cached List Page
```typescript
import { cacheLife, cacheTag } from 'next/cache'
import { getModels } from '@/lib/actions/models'

export default async function ModelsPage() {
  'use cache'
  cacheLife('hours')
  cacheTag('models')

  const models = await getModels()
  return <div>{/* render list */}</div>
}
```

### Pattern 2: Cached Detail Page with Params
```typescript
import { cacheLife, cacheTag } from 'next/cache'
import { getModelById } from '@/lib/actions/models'

export default async function ModelPage({ params }: { params: { id: string } }) {
  'use cache'
  cacheLife('hours')
  cacheTag('models', `model-${params.id}`)

  const model = await getModelById(params.id)
  return <div>{/* render detail */}</div>
}
```

### Pattern 3: Mixed Static and Dynamic Content
```typescript
import { Suspense } from 'react'
import { cacheLife } from 'next/cache'

export default function Page() {
  return (
    <>
      <StaticContent />
      <Suspense fallback={<LoadingSkeleton />}>
        <DynamicContent />
      </Suspense>
    </>
  )
}

async function StaticContent() {
  'use cache'
  cacheLife('hours')

  const data = await getStaticData()
  return <div>{/* render */}</div>
}

async function DynamicContent() {
  const session = await getSession() // uses cookies
  const userData = await getUserData(session.userId)
  return <div>{/* render */}</div>
}
```

### Pattern 4: Server Action with Cache Invalidation
```typescript
'use server'
import { updateTag } from 'next/cache'
import { updateModelAction } from '@/lib/actions/models'

export async function updateModel(id: string, data: FormData) {
  const result = await updateModelAction(id, data)

  if (result.status === 'success') {
    // Immediately expire cache for this specific model and all models
    updateTag(`model-${id}`, 'models')
  }

  return result
}
```

## Important Constraints

### Serialization Requirements
- **Arguments must be serializable** - Pass primitives, plain objects, and arrays only
- **No class instances or functions** - Cannot pass non-serializable values as arguments to cached functions
- **Unserializable return values are OK** - Can return React components or other unserializable values if you don't introspect them

### What NOT to Cache
- **Functions using runtime APIs** - `cookies()`, `headers()`, `searchParams` should not be in cached functions
- **Server Actions** - Never add `use cache` to server action files; cache at the consumption point
- **Highly personalized content** - User-specific data that varies per request

## Configuration

Enable Cache Components in `next.config.ts`:

```typescript
const nextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

## Troubleshooting

### Cache Not Working
- Verify `cacheComponents: true` is set in `next.config.ts`
- Check that `use cache` is at the top of the function body
- Ensure you're using Node.js runtime (Edge Runtime not supported)
- Verify function arguments are serializable

### Stale Data Issues
- Check cache lifetime profile - may need shorter duration
- Use `updateTag` instead of `revalidateTag` for immediate updates
- Verify cache tags match between caching and invalidation

### Performance Issues
- Profile which content needs to be cached vs. dynamic
- Use more `Suspense` boundaries to improve streaming
- Consider longer cache lifetimes for stable content
- Review database query performance in server actions


