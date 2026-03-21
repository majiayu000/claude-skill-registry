---
name: server-components
description: React Server Components, Suspense boundaries, streaming SSR, partial prerendering patterns for Next.js App Router.
---

# React Server Components

RSC + Next.js App Router patterns for streaming, caching, and minimal client JS.

## RSC vs Client Components Decision Matrix

```
Use Server Component (default) when:
  - Fetching data from DB / API
  - Accessing backend resources (filesystem, secrets)
  - No interactivity (useState, useEffect, event listeners)
  - Heavy dependencies (no bundle cost)

Use Client Component ("use client") when:
  - useState / useReducer / useRef
  - useEffect / lifecycle hooks
  - Browser APIs (window, navigator, IntersectionObserver)
  - Event listeners (onClick, onChange)
  - Third-party client libraries (charts, drag-drop)

Rule: Push "use client" as LOW in the tree as possible.
```

## "use client" / "use server" Directives

```typescript
// app/dashboard/page.tsx — Server Component (no directive needed)
import { db } from '@/lib/db'
import { StatsCounter } from './stats-counter' // client component

export default async function DashboardPage() {
  const stats = await db.query.stats.findMany()
  // Can pass serializable props to client components
  return <StatsCounter initialCount={stats.length} />
}

// app/dashboard/stats-counter.tsx — Client Component
'use client'
import { useState } from 'react'

export function StatsCounter({ initialCount }: { initialCount: number }) {
  const [count, setCount] = useState(initialCount)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// Server Action in separate file
// app/actions.ts
'use server'
export async function createItem(formData: FormData) {
  // runs on server, called from client
}
```

## Suspense Boundary Placement Strategy

```typescript
// Place Suspense around slow data — fast data renders immediately
export default async function Page() {
  const fastData = await db.query.config.findFirst()   // fast: cached

  return (
    <div>
      <Header config={fastData} />                      {/* instant */}

      <Suspense fallback={<StatsSkeleton />}>
        <SlowStats />                                   {/* streams in */}
      </Suspense>

      <Suspense fallback={<FeedSkeleton rows={5} />}>
        <ActivityFeed />                                {/* streams in */}
      </Suspense>
    </div>
  )
}

async function SlowStats() {
  const stats = await fetch('/api/stats', { cache: 'no-store' })
    .then(r => r.json())
  return <StatsGrid stats={stats} />
}
```

## Streaming SSR with loading.tsx

```
app/
  dashboard/
    page.tsx        ← async server component (data fetching)
    loading.tsx     ← shown while page.tsx is streaming
    error.tsx       ← shown if page.tsx throws
    layout.tsx      ← wraps all, always renders immediately
```

```typescript
// app/dashboard/loading.tsx — instant skeleton, no async needed
export default function Loading() {
  return (
    <div className="animate-pulse space-y-4">
      <div className="h-8 bg-gray-200 rounded w-1/3" />
      <div className="grid grid-cols-3 gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-24 bg-gray-200 rounded" />
        ))}
      </div>
    </div>
  )
}
```

## Partial Prerendering (PPR)

```typescript
// next.config.ts — enable PPR (Next.js 14+)
export default {
  experimental: { ppr: true },
}

// page.tsx — static shell + dynamic holes
import { Suspense } from 'react'
import { unstable_noStore as noStore } from 'next/cache'

export default function ProductPage({ params }: { params: { id: string } }) {
  return (
    <div>
      {/* Static: prerendered at build time */}
      <ProductShell id={params.id} />

      {/* Dynamic hole: streams in per request */}
      <Suspense fallback={<PriceSkeleton />}>
        <LivePrice id={params.id} />
      </Suspense>
    </div>
  )
}

async function LivePrice({ id }: { id: string }) {
  noStore()  // opt out of caching — always fresh
  const price = await fetchLivePrice(id)
  return <span>${price}</span>
}
```

## Server Actions Patterns

```typescript
// app/actions.ts
'use server'

import { revalidatePath, revalidateTag } from 'next/cache'
import { redirect } from 'next/navigation'
import { z } from 'zod'

const Schema = z.object({
  title: z.string().min(1).max(200),
  priority: z.enum(['low', 'medium', 'high']),
})

// Form submission action
export async function createTask(prevState: unknown, formData: FormData) {
  const parsed = Schema.safeParse({
    title: formData.get('title'),
    priority: formData.get('priority'),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors }
  }

  await db.insert(tasks).values(parsed.data)
  revalidatePath('/tasks')        // invalidate cached page
  revalidateTag('tasks')          // invalidate tagged fetches
  redirect('/tasks')
}

// Mutation action (called programmatically)
export async function deleteTask(id: string) {
  await db.delete(tasks).where(eq(tasks.id, id))
  revalidatePath('/tasks')
}

// Usage in client component
'use client'
import { useFormState, useFormStatus } from 'react-dom'
import { createTask } from './actions'

function SubmitButton() {
  const { pending } = useFormStatus()
  return <button disabled={pending}>{pending ? 'Saving...' : 'Save'}</button>
}

export function TaskForm() {
  const [state, action] = useFormState(createTask, null)
  return (
    <form action={action}>
      <input name="title" />
      {state?.error?.title && <p>{state.error.title}</p>}
      <SubmitButton />
    </form>
  )
}
```

## Data Fetching in RSC (async components)

```typescript
// Fetch with Next.js extended fetch (auto deduplication + caching)
async function UserProfile({ id }: { id: string }) {
  const user = await fetch(`/api/users/${id}`, {
    next: { revalidate: 60, tags: ['users', `user-${id}`] },  // ISR: 60s
  }).then(r => r.json())

  return <div>{user.name}</div>
}

// Direct DB query (server only — no API round-trip)
import { db } from '@/lib/db'
async function TaskList() {
  const tasks = await db.query.tasks.findMany({
    where: (t, { eq }) => eq(t.userId, await getCurrentUserId()),
    orderBy: (t, { desc }) => [desc(t.createdAt)],
  })
  return <ul>{tasks.map(t => <li key={t.id}>{t.title}</li>)}</ul>
}
```

## Cache and Revalidation

```typescript
import { unstable_cache } from 'next/cache'
import { cache } from 'react'

// React cache — deduplicate within a single request
const getUser = cache(async (id: string) => {
  return db.query.users.findFirst({ where: (u, { eq }) => eq(u.id, id) })
})

// Next.js unstable_cache — persist across requests (like ISR)
const getCachedStats = unstable_cache(
  async () => db.query.stats.findMany(),
  ['global-stats'],
  { revalidate: 300, tags: ['stats'] }   // 5 min TTL
)

// Manual revalidation from Server Action
import { revalidateTag, revalidatePath } from 'next/cache'
export async function updateUser(id: string, data: unknown) {
  await db.update(users).set(data).where(eq(users.id, id))
  revalidateTag(`user-${id}`)            // targeted cache bust
  revalidatePath('/dashboard')           // page cache bust
}
```

## Parallel Data Fetching in Layouts

```typescript
// Parallel: both requests fire simultaneously
export default async function Layout({ children }: { children: React.ReactNode }) {
  const [user, notifications] = await Promise.all([
    getUser(),
    getNotifications(),
  ])

  return (
    <div>
      <Header user={user} notificationCount={notifications.length} />
      <main>{children}</main>
    </div>
  )
}
```

## Error Boundary with error.tsx

```typescript
// app/dashboard/error.tsx — must be "use client"
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div role="alert" className="p-6 border border-red-200 rounded-lg">
      <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
      <p className="text-red-600 mt-1 text-sm">
        {process.env.NODE_ENV === 'development' ? error.message : 'An error occurred'}
      </p>
      <button onClick={reset} className="mt-4 btn btn-sm">Try again</button>
    </div>
  )
}
```

## Common Pitfalls

```typescript
// PITFALL 1: Non-serializable props RSC → Client
// WRONG: passing functions, class instances, Dates
<ClientComp handler={someFunction} />     // functions not serializable
<ClientComp date={new Date()} />          // Date not serializable

// RIGHT: serialize before passing
<ClientComp dateString={date.toISOString()} />
<ClientComp timestamp={date.getTime()} />

// PITFALL 2: Importing server-only code into client component
// Add 'server-only' package to throw at build time
import 'server-only'  // add to lib/db.ts, lib/auth.ts

// PITFALL 3: Hydration mismatch (browser extensions, dynamic dates)
// WRONG:
<span>{new Date().toLocaleString()}</span>  // server/client differ

// RIGHT: suppress or use useEffect
'use client'
const [time, setTime] = useState<string>('')
useEffect(() => setTime(new Date().toLocaleString()), [])
```
