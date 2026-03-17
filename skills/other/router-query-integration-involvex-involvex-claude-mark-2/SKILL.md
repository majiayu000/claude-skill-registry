---
name: router-query-integration
description: Integrate TanStack Router with TanStack Query for optimal data fetching. Covers route loaders with query prefetching, ensuring instant navigation, and eliminating request waterfalls. Use when setting up route loaders or optimizing navigation performance.
---

# Router × Query Integration

Seamlessly integrate TanStack Router with TanStack Query for optimal SPA performance and instant navigation.

## Route Loader + Query Prefetch

The key pattern: Use route loaders to prefetch queries BEFORE navigation completes.

**Benefits:**
- Loaders run before render, eliminating waterfall
- Fast SPA navigations (instant perceived performance)
- Queries still benefit from cache deduplication
- Add Router & Query DevTools during development (auto-hide in production)

## Basic Pattern

```typescript
// src/routes/users/$id.tsx
import { createFileRoute } from '@tanstack/react-router'
import { queryClient } from '@/app/queryClient'
import { usersKeys, fetchUser } from '@/features/users/queries'

export const Route = createFileRoute('/users/$id')({
  loader: async ({ params }) => {
    const id = params.id

    return queryClient.ensureQueryData({
      queryKey: usersKeys.detail(id),
      queryFn: () => fetchUser(id),
      staleTime: 30_000, // Fresh for 30 seconds
    })
  },
  component: UserPage,
})

function UserPage() {
  const { id } = Route.useParams()
  const { data: user } = useQuery({
    queryKey: usersKeys.detail(id),
    queryFn: () => fetchUser(id),
  })

  // Data is already loaded from loader, so this returns instantly
  return <div>{user.name}</div>
}
```

## Using Query Options Pattern (Recommended)

**Query Options** provide maximum type safety and DRY:

```typescript
// features/users/queries.ts
import { queryOptions } from '@tanstack/react-query'

export function userQueryOptions(userId: string) {
  return queryOptions({
    queryKey: ['users', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 30_000,
  })
}

export function useUser(userId: string) {
  return useQuery(userQueryOptions(userId))
}

// src/routes/users/$userId.tsx
import { userQueryOptions } from '@/features/users/queries'
import { queryClient } from '@/app/queryClient'

export const Route = createFileRoute('/users/$userId')({
  loader: ({ params }) =>
    queryClient.ensureQueryData(userQueryOptions(params.userId)),
  component: UserPage,
})

function UserPage() {
  const { userId } = Route.useParams()
  const { data: user } = useUser(userId)

  return <div>{user.name}</div>
}
```

## Multiple Queries in Loader

```typescript
export const Route = createFileRoute('/dashboard')({
  loader: async () => {
    // Run in parallel
    await Promise.all([
      queryClient.ensureQueryData(userQueryOptions()),
      queryClient.ensureQueryData(statsQueryOptions()),
      queryClient.ensureQueryData(postsQueryOptions()),
    ])
  },
  component: Dashboard,
})

function Dashboard() {
  const { data: user } = useUser()
  const { data: stats } = useStats()
  const { data: posts } = usePosts()

  // All data pre-loaded, renders instantly
  return (
    <div>
      <UserHeader user={user} />
      <StatsPanel stats={stats} />
      <PostsList posts={posts} />
    </div>
  )
}
```

## Dependent Queries

```typescript
export const Route = createFileRoute('/users/$userId/posts')({
  loader: async ({ params }) => {
    // First ensure user data
    const user = await queryClient.ensureQueryData(
      userQueryOptions(params.userId)
    )

    // Then fetch user's posts
    return queryClient.ensureQueryData(
      userPostsQueryOptions(user.id)
    )
  },
  component: UserPostsPage,
})
```

## Query Client Setup

**Export the query client for use in loaders:**

```typescript
// src/app/queryClient.ts
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,
      gcTime: 5 * 60_000,
      retry: 1,
    },
  },
})

// src/main.tsx
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from './app/queryClient'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>
)
```

## Prefetch vs Ensure

**`prefetchQuery`** - Fire and forget, don't wait:
```typescript
loader: ({ params }) => {
  // Don't await - just start fetching
  queryClient.prefetchQuery(userQueryOptions(params.userId))
  // Navigation continues immediately
}
```

**`ensureQueryData`** - Wait for data (recommended):
```typescript
loader: async ({ params }) => {
  // Await - navigation waits until data is ready
  return await queryClient.ensureQueryData(userQueryOptions(params.userId))
}
```

**`fetchQuery`** - Always fetches fresh:
```typescript
loader: async ({ params }) => {
  // Ignores cache, always fetches
  return await queryClient.fetchQuery(userQueryOptions(params.userId))
}
```

**Recommendation:** Use `ensureQueryData` for most cases - respects cache and staleTime.

## Handling Errors in Loaders

```typescript
export const Route = createFileRoute('/users/$userId')({
  loader: async ({ params }) => {
    try {
      return await queryClient.ensureQueryData(userQueryOptions(params.userId))
    } catch (error) {
      // Let router error boundary handle it
      throw error
    }
  },
  errorComponent: ({ error }) => (
    <div>
      <h1>Failed to load user</h1>
      <p>{error.message}</p>
    </div>
  ),
  component: UserPage,
})
```

## Invalidating Queries After Mutations

```typescript
// features/users/mutations.ts
export function useUpdateUser() {
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  return useMutation({
    mutationFn: (user: UpdateUserDTO) => api.put(`/users/${user.id}`, user),
    onSuccess: (updatedUser) => {
      // Update cache immediately
      queryClient.setQueryData(
        userQueryOptions(updatedUser.id).queryKey,
        updatedUser
      )

      // Invalidate related queries
      queryClient.invalidateQueries({ queryKey: ['users', 'list'] })

      // Navigate to updated user page (will use cached data)
      navigate({ to: '/users/$userId', params: { userId: updatedUser.id } })
    },
  })
}
```

## Preloading on Link Hover

```typescript
import { Link, useRouter } from '@tanstack/react-router'

function UserLink({ userId }: { userId: string }) {
  const router = useRouter()

  const handleMouseEnter = () => {
    // Preload route (includes loader)
    router.preloadRoute({ to: '/users/$userId', params: { userId } })
  }

  return (
    <Link
      to="/users/$userId"
      params={{ userId }}
      onMouseEnter={handleMouseEnter}
    >
      View User
    </Link>
  )
}
```

Or use built-in preload:
```typescript
<Link
  to="/users/$userId"
  params={{ userId: '123' }}
  preload="intent" // Preload on hover/focus
>
  View User
</Link>
```

## Search Params + Queries

```typescript
// src/routes/users/index.tsx
import { z } from 'zod'

const searchSchema = z.object({
  page: z.number().default(1),
  filter: z.enum(['active', 'all']).default('all'),
})

export const Route = createFileRoute('/users/')({
  validateSearch: searchSchema,
  loader: ({ search }) => {
    return queryClient.ensureQueryData(
      usersListQueryOptions(search.page, search.filter)
    )
  },
  component: UsersPage,
})

function UsersPage() {
  const { page, filter } = Route.useSearch()
  const { data: users } = useUsersList(page, filter)

  return <UserTable users={users} page={page} filter={filter} />
}
```

## Suspense Mode

With Suspense, you don't need separate loading states:

```typescript
export const Route = createFileRoute('/users/$userId')({
  loader: ({ params }) =>
    queryClient.ensureQueryData(userQueryOptions(params.userId)),
  component: UserPage,
})

function UserPage() {
  const { userId } = Route.useParams()

  // Use Suspense hook - data is NEVER undefined
  const { data: user } = useSuspenseQuery(userQueryOptions(userId))

  return <div>{user.name}</div>
}

// Wrap route in Suspense boundary (in __root.tsx or layout)
<Suspense fallback={<Spinner />}>
  <Outlet />
</Suspense>
```

## Performance Best Practices

1. **Prefetch in Loaders** - Always use loaders to eliminate waterfalls
2. **Use Query Options** - Share configuration between loaders and components
3. **Set Appropriate staleTime** - Tune per query (30s for user data, 10min for static)
4. **Parallel Prefetching** - Use `Promise.all()` for independent queries
5. **Hover Preloading** - Enable `preload="intent"` on critical links
6. **Cache Invalidation** - Be specific with invalidation keys to avoid unnecessary refetches

## DevTools Setup

```typescript
// src/main.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

<QueryClientProvider client={queryClient}>
  <RouterProvider router={router} />
  <ReactQueryDevtools position="bottom-right" />
  <TanStackRouterDevtools position="bottom-left" />
</QueryClientProvider>
```

Both auto-hide in production.

## Common Patterns

**List + Detail Pattern:**
```typescript
// List route prefetches list
export const ListRoute = createFileRoute('/users/')({
  loader: () => queryClient.ensureQueryData(usersListQueryOptions()),
  component: UsersList,
})

// Detail route prefetches specific user
export const DetailRoute = createFileRoute('/users/$userId')({
  loader: ({ params }) =>
    queryClient.ensureQueryData(userQueryOptions(params.userId)),
  component: UserDetail,
})

// Clicking from list to detail uses cached data if available
```

**Edit Form Pattern:**
```typescript
export const EditRoute = createFileRoute('/users/$userId/edit')({
  loader: ({ params }) =>
    queryClient.ensureQueryData(userQueryOptions(params.userId)),
  component: UserEditForm,
})

function UserEditForm() {
  const { userId } = Route.useParams()
  const { data: user } = useUser(userId)
  const updateUser = useUpdateUser()

  // Form pre-populated with cached user data
  return <Form initialValues={user} onSubmit={updateUser.mutate} />
}
```

## Related Skills

- **tanstack-query** - Comprehensive Query v5 patterns
- **tanstack-router** - Router configuration and usage
- **api-integration** - OpenAPI + Apidog patterns
