---
name: tanstack-router
description: Expert guidance for TanStack Router file-based routing, loaders, actions, type-safe navigation, and React patterns. Use when user says "tanstack router", "/tanstack-router", "create route", "add page", "routing help", "loader", "route params", or asks about navigation, layouts, or route structure.
---

# TanStack Router Skill

Expert guidance for TanStack Router with file-based routing, type-safe navigation, and modern React patterns.

## Quick Reference

### File-Based Route Structure

```
src/routes/
├── __root.tsx          # Root layout (wraps everything)
├── index.tsx           # / (home page)
├── about.tsx           # /about
├── posts/
│   ├── index.tsx       # /posts
│   └── $postId.tsx     # /posts/:postId (dynamic)
├── _layout/            # Layout group (no URL segment)
│   ├── route.tsx       # Shared layout component
│   └── dashboard.tsx   # /_layout/dashboard -> /dashboard
└── settings.tsx        # /settings
```

### Route Naming Conventions

| Pattern | URL | Purpose |
|---------|-----|---------|
| `index.tsx` | `/parent` | Index route for directory |
| `$param.tsx` | `/:param` | Dynamic segment |
| `$param/` | `/:param/*` | Dynamic + nested routes |
| `_layout/` | (none) | Layout group, no URL segment |
| `_layout.tsx` | (none) | Pathless layout wrapper |
| `$.tsx` | `/*` | Splat/catch-all route |
| `route.tsx` | (parent) | Route config for directory |

## Creating Routes

### Basic Route

```tsx
// src/routes/about.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/about')({
  component: AboutPage,
})

function AboutPage() {
  return <div>About us</div>
}
```

### Route with Loader

```tsx
// src/routes/posts/$postId.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)
    return { post }
  },
  component: PostPage,
})

function PostPage() {
  const { post } = Route.useLoaderData()
  return <article>{post.title}</article>
}
```

### Route with Search Params

```tsx
// src/routes/search.tsx
import { createFileRoute } from '@tanstack/react-router'

// Define search param schema
type SearchParams = {
  q?: string
  page?: number
  sort?: 'asc' | 'desc'
}

export const Route = createFileRoute('/search')({
  validateSearch: (search: Record<string, unknown>): SearchParams => ({
    q: search.q as string,
    page: Number(search.page) || 1,
    sort: (search.sort as 'asc' | 'desc') || 'desc',
  }),
  component: SearchPage,
})

function SearchPage() {
  const { q, page, sort } = Route.useSearch()
  const navigate = Route.useNavigate()

  return (
    <div>
      <input
        value={q ?? ''}
        onChange={(e) =>
          navigate({ search: { q: e.target.value, page: 1 } })
        }
      />
    </div>
  )
}
```

### Root Layout

```tsx
// src/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router'

export const Route = createRootRoute({
  component: RootLayout,
})

function RootLayout() {
  return (
    <div className="min-h-screen">
      <header>
        <nav>...</nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>...</footer>
    </div>
  )
}
```

### Layout Routes (Pathless)

```tsx
// src/routes/_authenticated/route.tsx
import { createFileRoute, Outlet, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({ to: '/login' })
    }
  },
  component: AuthLayout,
})

function AuthLayout() {
  return (
    <div className="authenticated-layout">
      <Sidebar />
      <Outlet />
    </div>
  )
}

// src/routes/_authenticated/dashboard.tsx -> /dashboard
// src/routes/_authenticated/settings.tsx -> /settings
```

## Type-Safe Navigation

### Link Component

```tsx
import { Link } from '@tanstack/react-router'

// Basic link
<Link to="/about">About</Link>

// With params
<Link to="/posts/$postId" params={{ postId: '123' }}>
  View Post
</Link>

// With search params
<Link to="/search" search={{ q: 'react', page: 1 }}>
  Search
</Link>

// Active styling
<Link
  to="/dashboard"
  activeProps={{ className: 'text-blue-500 font-bold' }}
  inactiveProps={{ className: 'text-gray-500' }}
>
  Dashboard
</Link>
```

### Programmatic Navigation

```tsx
import { useNavigate, useRouter } from '@tanstack/react-router'

function MyComponent() {
  const navigate = useNavigate()
  const router = useRouter()

  // Navigate to route
  const goToPost = () => {
    navigate({ to: '/posts/$postId', params: { postId: '123' } })
  }

  // Navigate with search
  const search = () => {
    navigate({ to: '/search', search: { q: 'query' } })
  }

  // Replace history
  const replace = () => {
    navigate({ to: '/home', replace: true })
  }

  // Invalidate and refetch
  const refresh = () => {
    router.invalidate()
  }
}
```

## Loaders and Data Fetching

### Basic Loader

```tsx
export const Route = createFileRoute('/users')({
  loader: async () => {
    const users = await fetchUsers()
    return { users }
  },
})
```

### Loader with Context

```tsx
// src/routes/__root.tsx
export const Route = createRootRoute({
  beforeLoad: async () => {
    return {
      auth: await getAuthState(),
      queryClient: getQueryClient(),
    }
  },
})

// src/routes/profile.tsx
export const Route = createFileRoute('/profile')({
  loader: async ({ context }) => {
    // Access context from parent routes
    const { auth, queryClient } = context
    return queryClient.fetchQuery({
      queryKey: ['profile', auth.userId],
      queryFn: () => fetchProfile(auth.userId),
    })
  },
})
```

### Loader with Params and Search

```tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params, search }) => {
    const { postId } = params
    const { includeComments } = search

    const [post, comments] = await Promise.all([
      fetchPost(postId),
      includeComments ? fetchComments(postId) : null,
    ])

    return { post, comments }
  },
})
```

### Pending/Error States

```tsx
export const Route = createFileRoute('/posts')({
  loader: fetchPosts,
  pendingComponent: () => <div>Loading posts...</div>,
  errorComponent: ({ error }) => <div>Error: {error.message}</div>,
})
```

## Error Handling

### Route-Level Error Boundary

```tsx
export const Route = createFileRoute('/risky')({
  loader: riskyLoader,
  errorComponent: ({ error, reset }) => (
    <div>
      <h1>Something went wrong</h1>
      <pre>{error.message}</pre>
      <button onClick={reset}>Try again</button>
    </div>
  ),
})
```

### Not Found Handling

```tsx
// src/routes/__root.tsx
export const Route = createRootRoute({
  notFoundComponent: () => (
    <div>
      <h1>404 - Page Not Found</h1>
      <Link to="/">Go Home</Link>
    </div>
  ),
})
```

## Authentication Patterns

### Protected Routes

```tsx
// src/routes/_auth/route.tsx
export const Route = createFileRoute('/_auth')({
  beforeLoad: async ({ context, location }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: { redirect: location.href },
      })
    }
  },
})
```

### Login with Redirect

```tsx
// src/routes/login.tsx
export const Route = createFileRoute('/login')({
  validateSearch: (search) => ({
    redirect: search.redirect as string | undefined,
  }),
  component: LoginPage,
})

function LoginPage() {
  const { redirect } = Route.useSearch()
  const navigate = useNavigate()

  const handleLogin = async () => {
    await performLogin()
    navigate({ to: redirect ?? '/' })
  }
}
```

## Common Patterns

### Route Preloading

```tsx
<Link to="/posts/$postId" params={{ postId }} preload="intent">
  Preload on hover
</Link>

<Link to="/heavy-page" preload="viewport">
  Preload when visible
</Link>
```

### Search Param Persistence

```tsx
// Keep search params when navigating
navigate({
  to: '/posts/$postId',
  params: { postId },
  search: (prev) => ({ ...prev, tab: 'comments' }),
})
```

### Route Masking

```tsx
// Show different URL than actual route
navigate({
  to: '/posts/$postId',
  params: { postId: '123' },
  mask: { to: '/p/123' },
})
```

## Router Configuration

### Basic Setup

```tsx
// src/router.tsx
import { createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

export const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
  defaultPreloadStaleTime: 0,
  context: {
    auth: undefined!, // Will be set by provider
  },
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### With TanStack Query

```tsx
import { QueryClient } from '@tanstack/react-query'

const queryClient = new QueryClient()

const router = createRouter({
  routeTree,
  context: { queryClient },
  defaultPreload: 'intent',
  defaultPreloadStaleTime: 0,
})
```

## Gotchas and Tips

1. **File naming matters**: `$param.tsx` creates dynamic routes, `_prefix` creates layout groups
2. **Loader runs on every navigation**: Use TanStack Query inside loaders for caching
3. **Context flows down**: Set context in parent routes, access in children
4. **Type safety is automatic**: Route params and search are fully typed from file names
5. **Outlet is required**: Layout routes need `<Outlet />` to render children
6. **beforeLoad vs loader**: Use `beforeLoad` for auth checks, `loader` for data
7. **Search params are serialized**: Complex objects need custom serializers

## Migration from React Router

| React Router | TanStack Router |
|--------------|-----------------|
| `useParams()` | `Route.useParams()` |
| `useSearchParams()` | `Route.useSearch()` |
| `useLoaderData()` | `Route.useLoaderData()` |
| `useNavigate()` | `useNavigate()` or `Route.useNavigate()` |
| `<Outlet />` | `<Outlet />` (same) |
| `loader` in route config | `loader` in `createFileRoute` |
