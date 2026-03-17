---
name: tanstack-router
description: Build type-safe React applications with TanStack Router. Covers file-based routing, type-safe params, search params, loaders, and code splitting. Use for React SPAs requiring type-safe navigation, nested layouts, and data loading patterns.
---

# TanStack Router

Type-safe routing for React applications with first-class search params, loaders, and code splitting.

## Instructions

1. **Leverage type safety** - Define route params and search params with full TypeScript inference
2. **Use loaders** - Fetch data before route renders
3. **Structure routes** - Use file-based routing or code-first approach
4. **Handle errors** - Define error boundaries per route
5. **Lazy load** - Code split with lazy route imports

## Setup

```bash
npm install @tanstack/react-router
# For file-based routing
npm install -D @tanstack/router-vite-plugin
```

### Vite Configuration

```ts
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { TanStackRouterVite } from '@tanstack/router-vite-plugin';

export default defineConfig({
  plugins: [react(), TanStackRouterVite()],
});
```

## File-Based Routing

### Route Structure

```
src/
├── routes/
│   ├── __root.tsx          # Root layout
│   ├── index.tsx           # / (home)
│   ├── about.tsx           # /about
│   ├── posts/
│   │   ├── index.tsx       # /posts
│   │   └── $postId.tsx     # /posts/:postId
│   ├── _layout.tsx         # Layout route (no URL segment)
│   └── _layout/
│       └── settings.tsx    # /settings (uses _layout)
├── routeTree.gen.ts        # Auto-generated
└── main.tsx
```

### Root Route

```tsx
// routes/__root.tsx
import { createRootRoute, Link, Outlet } from '@tanstack/react-router';
import { TanStackRouterDevtools } from '@tanstack/router-devtools';

export const Route = createRootRoute({
  component: () => (
    <>
      <nav className="flex gap-4 p-4 border-b">
        <Link to="/" className="[&.active]:font-bold">
          Home
        </Link>
        <Link to="/about" className="[&.active]:font-bold">
          About
        </Link>
        <Link to="/posts" className="[&.active]:font-bold">
          Posts
        </Link>
      </nav>
      <main className="p-4">
        <Outlet />
      </main>
      <TanStackRouterDevtools />
    </>
  ),
});
```

### Index Route

```tsx
// routes/index.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  component: HomePage,
});

function HomePage() {
  return (
    <div>
      <h1>Welcome Home</h1>
    </div>
  );
}
```

### Dynamic Route with Loader

```tsx
// routes/posts/$postId.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const response = await fetch(`/api/posts/${params.postId}`);
    if (!response.ok) throw new Error('Post not found');
    return response.json();
  },
  component: PostPage,
});

function PostPage() {
  const post = Route.useLoaderData();

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

## Search Params

### Type-Safe Search Params

```tsx
// routes/posts/index.tsx
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';

const postsSearchSchema = z.object({
  page: z.number().catch(1),
  filter: z.enum(['all', 'published', 'draft']).catch('all'),
  search: z.string().optional(),
});

export const Route = createFileRoute('/posts/')({
  validateSearch: postsSearchSchema,
  loaderDeps: ({ search: { page, filter } }) => ({ page, filter }),
  loader: async ({ deps: { page, filter } }) => {
    return fetchPosts({ page, filter });
  },
  component: PostsPage,
});

function PostsPage() {
  const { page, filter, search } = Route.useSearch();
  const posts = Route.useLoaderData();
  const navigate = Route.useNavigate();

  return (
    <div>
      <input
        value={search ?? ''}
        onChange={(e) =>
          navigate({
            search: (prev) => ({ ...prev, search: e.target.value }),
          })
        }
        placeholder="Search..."
      />

      <select
        value={filter}
        onChange={(e) =>
          navigate({
            search: (prev) => ({ ...prev, filter: e.target.value }),
          })
        }
      >
        <option value="all">All</option>
        <option value="published">Published</option>
        <option value="draft">Draft</option>
      </select>

      <PostsList posts={posts} />

      <Pagination
        page={page}
        onPageChange={(newPage) =>
          navigate({
            search: (prev) => ({ ...prev, page: newPage }),
          })
        }
      />
    </div>
  );
}
```

## Navigation

### Link Component

```tsx
import { Link } from '@tanstack/react-router';

function Navigation() {
  return (
    <nav>
      {/* Basic link */}
      <Link to="/">Home</Link>

      {/* With params */}
      <Link to="/posts/$postId" params={{ postId: '123' }}>
        Post 123
      </Link>

      {/* With search params */}
      <Link to="/posts" search={{ page: 1, filter: 'published' }}>
        Published Posts
      </Link>

      {/* Active styling */}
      <Link
        to="/about"
        activeProps={{ className: 'font-bold text-blue-600' }}
        inactiveProps={{ className: 'text-gray-600' }}
      >
        About
      </Link>
    </nav>
  );
}
```

### Programmatic Navigation

```tsx
import { useNavigate, useRouter } from '@tanstack/react-router';

function PostActions({ postId }: { postId: string }) {
  const navigate = useNavigate();
  const router = useRouter();

  const handleDelete = async () => {
    await deletePost(postId);
    // Navigate to posts list
    navigate({ to: '/posts' });
  };

  const handleEdit = () => {
    // Navigate with params
    navigate({
      to: '/posts/$postId/edit',
      params: { postId },
    });
  };

  const goBack = () => {
    router.history.back();
  };

  return (
    <div className="flex gap-2">
      <button onClick={goBack}>Back</button>
      <button onClick={handleEdit}>Edit</button>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
```

## Error Handling

```tsx
// routes/posts/$postId.tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId);
    if (!post) {
      throw new Error('Post not found');
    }
    return post;
  },
  errorComponent: PostErrorComponent,
  component: PostPage,
});

function PostErrorComponent({ error }: { error: Error }) {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
      <h2 className="text-red-800 font-semibold">Error Loading Post</h2>
      <p className="text-red-600">{error.message}</p>
      <Link to="/posts" className="text-blue-600 underline">
        Back to Posts
      </Link>
    </div>
  );
}
```

## Pending States

```tsx
// routes/posts/$postId.tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => fetchPost(params.postId),
  pendingComponent: () => <PostSkeleton />,
  component: PostPage,
});

// Or in the component
function PostPage() {
  const { isLoading } = Route.useMatch();
  const post = Route.useLoaderData();

  if (isLoading) return <PostSkeleton />;

  return <article>{/* ... */}</article>;
}
```

## Layouts

### Layout Routes

```tsx
// routes/_authenticated.tsx
import { createFileRoute, Outlet, redirect } from '@tanstack/react-router';

export const Route = createFileRoute('/_authenticated')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: { redirect: location.href },
      });
    }
  },
  component: () => (
    <div className="authenticated-layout">
      <Sidebar />
      <Outlet />
    </div>
  ),
});
```

```tsx
// routes/_authenticated/dashboard.tsx
// This route requires authentication
export const Route = createFileRoute('/_authenticated/dashboard')({
  component: DashboardPage,
});
```

## Context

```tsx
// main.tsx
import { RouterProvider, createRouter } from '@tanstack/react-router';
import { routeTree } from './routeTree.gen';

interface RouterContext {
  auth: {
    isAuthenticated: boolean;
    user: User | null;
  };
}

const router = createRouter({
  routeTree,
  context: {
    auth: undefined!, // Will be set by provider
  },
});

function App() {
  const auth = useAuth(); // Your auth hook

  return (
    <RouterProvider
      router={router}
      context={{ auth }}
    />
  );
}
```

## Code Splitting

```tsx
// routes/admin.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/admin')({
  component: () => import('./AdminPage').then(m => <m.AdminPage />),
});

// Or with lazy
import { lazy } from 'react';

const AdminPage = lazy(() => import('./AdminPage'));

export const Route = createFileRoute('/admin')({
  component: AdminPage,
});
```

## Best Practices

| Practice | Recommendation |
|----------|----------------|
| **Search Params** | Always validate with Zod schema |
| **Loaders** | Fetch data before render, not in components |
| **Type Safety** | Let TypeScript infer from route definitions |
| **Error Handling** | Define errorComponent per route |
| **Code Splitting** | Lazy load route components |
| **Layouts** | Use layout routes for shared UI |

## When to Use

- React SPAs requiring type-safe routing
- Applications with complex search params
- Projects needing route-level data loading
- Teams wanting compile-time route validation
- Apps with nested layouts and auth guards

## Notes

- Full TypeScript inference for params and search
- File-based or code-first routing
- Built-in devtools for debugging
- Integrates with TanStack Query
- 12kb gzipped bundle size
