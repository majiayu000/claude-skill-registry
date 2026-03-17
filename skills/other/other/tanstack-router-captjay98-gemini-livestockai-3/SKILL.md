---
name: TanStack Router
description: File-based routing, loaders, and navigation patterns in LivestockAI
---

# TanStack Router

LivestockAI uses [TanStack Router](https://tanstack.com/router) for type-safe, file-based routing with SSR support.

## Route Structure

Routes are in `app/routes/`:

```
app/routes/
├── __root.tsx           # Root layout
├── index.tsx            # Public landing (/)
├── _auth.tsx            # Auth layout wrapper
└── _auth/               # Protected routes
    ├── dashboard.tsx    # /dashboard
    ├── batches/
    │   ├── index.tsx    # /batches
    │   └── $batchId.tsx # /batches/:batchId
    ├── farms/
    │   ├── index.tsx    # /farms
    │   └── $farmId.tsx  # /farms/:farmId
    └── settings.tsx     # /settings
```

## Route Definition Pattern

**Use loaders for data fetching**, not `useEffect`:

```typescript
import { createFileRoute } from '@tanstack/react-router'
import { getBatchesForFarmFn } from '~/features/batches/server'
import { BatchesSkeleton } from '~/components/batches/batches-skeleton'

export const Route = createFileRoute('/_auth/batches/')({
  // 1. Validate search params
  validateSearch: (search) => ({
    farmId: search.farmId as string | undefined,
    page: Number(search.page) || 1,
    status: search.status as string | undefined,
  }),

  // 2. Define loader dependencies
  loaderDeps: ({ search }) => ({
    farmId: search.farmId,
    page: search.page,
    status: search.status,
  }),

  // 3. Loader - fetches data on server
  loader: async ({ deps }) => {
    return getBatchesForFarmFn({ data: deps })
  },

  // 4. Loading state
  pendingComponent: BatchesSkeleton,

  // 5. Error state
  errorComponent: ({ error }) => (
    <div className="p-4 text-red-600">
      Error: {error.message}
    </div>
  ),

  // 6. Main component
  component: BatchesPage,
})

function BatchesPage() {
  // Access loader data with full type safety
  const { paginatedBatches, summary } = Route.useLoaderData()

  return (
    <div>
      <h1>Batches</h1>
      {/* Render data */}
    </div>
  )
}
```

## Anti-Pattern: useEffect for Data

```typescript
// ❌ WRONG - Don't do this
function BatchesPage() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getBatchesForFarmFn({ data: {} }).then(setData)
  }, [])

  if (loading) return <div>Loading...</div>
  return <div>{/* render */}</div>
}
```

## Dynamic Routes

Use `$paramName` for dynamic segments:

```typescript
// app/routes/_auth/batches/$batchId.tsx
export const Route = createFileRoute('/_auth/batches/$batchId')({
  loader: async ({ params }) => {
    return getBatchDetailsFn({ data: { batchId: params.batchId } })
  },
  component: BatchDetailPage,
})

function BatchDetailPage() {
  const { batch, stats } = Route.useLoaderData()
  const { batchId } = Route.useParams()
  // ...
}
```

## Navigation

```typescript
import { Link, useNavigate } from '@tanstack/react-router'

// Declarative navigation
<Link to="/batches/$batchId" params={{ batchId: '123' }}>
  View Batch
</Link>

// Programmatic navigation
const navigate = useNavigate()
navigate({ to: '/batches', search: { status: 'active' } })
```

## Search Params

```typescript
// Reading search params
const { farmId, status } = Route.useSearch()

// Updating search params
<Link
  to="."
  search={(prev) => ({ ...prev, status: 'active' })}
>
  Active Only
</Link>
```

## Skeleton Components

Create skeleton components for `pendingComponent`:

```typescript
// app/components/batches/batches-skeleton.tsx
import { Skeleton } from '~/components/ui/skeleton'

export function BatchesSkeleton() {
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <Skeleton key={i} className="h-32 w-full" />
        ))}
      </div>
      <Skeleton className="h-64 w-full" />
    </div>
  )
}
```

## Auth Layout

The `_auth.tsx` layout wraps protected routes:

```typescript
// app/routes/_auth.tsx
export const Route = createFileRoute('/_auth')({
  beforeLoad: async () => {
    const session = await getSession()
    if (!session) {
      throw redirect({ to: '/login' })
    }
  },
  component: AuthLayout,
})

function AuthLayout() {
  return (
    <AppShell>
      <Outlet />
    </AppShell>
  )
}
```

## Related Skills

- `tanstack-start` - Server functions
- `tanstack-query` - Client-side mutations
- `rugged-utility` - UI patterns for loading states
