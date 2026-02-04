---
name: tanstack-router
description: TanStack Router file-based routing patterns including route creation, navigation, loaders, type-safe routing, and lazy loading. Use when creating routes, implementing navigation, or working with TanStack Router.
---

# TanStack Router Patterns

## Purpose

File-based routing with TanStack Router, emphasizing type-safe navigation, route loaders, and lazy loading.

## When to Use This Skill

- Creating new routes
- Implementing navigation
- Using route loaders for data
- Type-safe routing with parameters
- Lazy loading routes

---

## Quick Start

### Basic Route

```typescript
// routes/posts/index.tsx
import { createFileRoute } from '@tanstack/react-router';
import { postsApi } from '~/features/posts/api/postsApi';

export const Route = createFileRoute('/posts')({
  loader: async () => {
    const posts = await postsApi.getAll();
    return { posts };
  },
  component: PostsPage,
});

function PostsPage() {
  const { posts } = Route.useLoaderData();

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

---

## File-Based Routing

### Directory Structure

```
routes/
├── __root.tsx          # Root route
├── index.tsx           # /
├── about.tsx           # /about
├── posts/
│   ├── index.tsx       # /posts
│   └── $postId.tsx     # /posts/:postId
└── users/
    ├── index.tsx       # /users
    └── $userId/
        ├── index.tsx   # /users/:userId
        └── posts.tsx   # /users/:userId/posts
```

### Route Mapping

```
File Path                        → URL Path
routes/index.tsx                 → /
routes/about.tsx                 → /about
routes/posts/index.tsx           → /posts
routes/posts/$postId.tsx         → /posts/:postId
routes/users/$userId/index.tsx   → /users/:userId
routes/users/$userId/posts.tsx   → /users/:userId/posts
```

---

## Route Parameters

### Dynamic Routes

```typescript
// routes/posts/$postId.tsx
import { createFileRoute } from '@tanstack/react-router';
import { postsApi } from '~/features/posts/api/postsApi';

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await postsApi.get(params.postId);
    return { post };
  },
  component: PostDetails,
});

function PostDetails() {
  const { post } = Route.useLoaderData();
  const { postId } = Route.useParams();

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  );
}
```

### Multiple Parameters

```typescript
// routes/users/$userId/posts/$postId.tsx
export const Route = createFileRoute('/users/$userId/posts/$postId')({
  loader: async ({ params }) => {
    const { userId, postId } = params;
    const post = await postsApi.getByUserAndId(userId, postId);
    return { post };
  },
  component: UserPostDetails,
});
```

---

## Route Loaders

### Basic Loader

```typescript
export const Route = createFileRoute('/posts')({
  loader: async () => {
    const posts = await postsApi.getAll();
    return { posts };
  },
  component: PostsPage,
});
```

### Loader with Dependencies

```typescript
export const Route = createFileRoute('/users/$userId/posts')({
  loader: async ({ params, context }) => {
    const [user, posts] = await Promise.all([
      userApi.get(params.userId),
      postsApi.getByUser(params.userId),
    ]);
    return { user, posts };
  },
  component: UserPosts,
});
```

### Loader Error Handling

```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    try {
      const post = await postsApi.get(params.postId);
      return { post, error: null };
    } catch (error) {
      return { post: null, error: 'Post not found' };
    }
  },
  component: PostDetails,
});

function PostDetails() {
  const { post, error } = Route.useLoaderData();

  if (error) return <Error message={error} />;
  return <div>{post.title}</div>;
}
```

---

## Navigation

```typescript
import { Link, useNavigate } from '@tanstack/react-router';

// Link component
<Link to="/posts/$postId" params={{ postId: '123' }}>View Post</Link>

// Programmatic navigation
const navigate = useNavigate();
navigate({ to: '/posts', search: { filter: 'published' } });
```

---

## Lazy Loading

### Lazy Route Component

```typescript
// routes/posts/index.tsx
import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

const PostsPage = lazy(() => import('~/features/posts/PostsPage'));

export const Route = createFileRoute('/posts')({
  component: PostsPage,
});
```

### Lazy Loader

```typescript
export const Route = createFileRoute('/posts')({
  loader: async () => {
    // Dynamically import heavy module only when route loads
    const { processData } = await import('~/lib/heavyModule');
    const posts = await postsApi.getAll();
    const processed = processData(posts);
    return { posts: processed };
  },
  component: PostsPage,
});
```

---

## Search Params

### Type-Safe Search Params

```typescript
import { z } from 'zod';

const postsSearchSchema = z.object({
  filter: z.enum(['all', 'published', 'draft']).default('all'),
  sort: z.enum(['date', 'title']).default('date'),
  page: z.number().default(1),
});

export const Route = createFileRoute('/posts')({
  validateSearch: postsSearchSchema,
  loader: async ({ search }) => {
    const posts = await postsApi.getAll(search);
    return { posts };
  },
  component: PostsPage,
});

function PostsPage() {
  const { posts } = Route.useLoaderData();
  const search = Route.useSearch();

  return (
    <div>
      <p>Filter: {search.filter}</p>
      <p>Sort: {search.sort}</p>
      <p>Page: {search.page}</p>
    </div>
  );
}
```

### Updating Search Params

```typescript
import { useNavigate } from '@tanstack/react-router';

function FilterButtons() {
  const navigate = useNavigate();
  const search = Route.useSearch();

  const setFilter = (filter: string) => {
    navigate({
      to: '.',
      search: (prev) => ({ ...prev, filter }),
    });
  };

  return (
    <div>
      <button onClick={() => setFilter('all')}>All</button>
      <button onClick={() => setFilter('published')}>Published</button>
      <button onClick={() => setFilter('draft')}>Draft</button>
    </div>
  );
}
```

---

## Layouts

### Root Layout

```typescript
// routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router';

export const Route = createRootRoute({
  component: RootLayout,
});

function RootLayout() {
  return (
    <div>
      <Header />
      <main>
        <Outlet />  {/* Child routes render here */}
      </main>
      <Footer />
    </div>
  );
}
```

### Nested Layouts

```typescript
// routes/dashboard.tsx
export const Route = createFileRoute('/dashboard')({
  component: DashboardLayout,
});

function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <div className="content">
        <Outlet />  {/* Dashboard child routes */}
      </div>
    </div>
  );
}

// routes/dashboard/index.tsx
export const Route = createFileRoute('/dashboard')({
  component: DashboardHome,
});

// routes/dashboard/analytics.tsx
export const Route = createFileRoute('/dashboard/analytics')({
  component: Analytics,
});
```

---

## Route Guards

### Authentication Guard

```typescript
export const Route = createFileRoute('/admin')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: { redirect: '/admin' },
      });
    }
  },
  component: AdminPage,
});
```

### Permission Guard

```typescript
export const Route = createFileRoute('/admin/users')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.hasPermission('users:manage')) {
      throw redirect({ to: '/unauthorized' });
    }
  },
  component: UsersPage,
});
```

---

## Breadcrumbs

### Route Breadcrumbs

```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await postsApi.get(params.postId);
    return { post };
  },
  meta: ({ loaderData }) => [
    { title: 'Home', path: '/' },
    { title: 'Posts', path: '/posts' },
    { title: loaderData.post.title, path: `/posts/${loaderData.post.id}` },
  ],
  component: PostDetails,
});
```

---

## Best Practices

### 1. Use Loaders for Data

```typescript
// ✅ Good: Loader fetches data
export const Route = createFileRoute('/posts')({
  loader: async () => {
    const posts = await postsApi.getAll();
    return { posts };
  },
  component: PostsPage,
});

// ❌ Avoid: Fetching in component
function PostsPage() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    postsApi.getAll().then(setPosts);
  }, []);

  return <div>...</div>;
}
```

### 2. Lazy Load Heavy Routes

```typescript
// ✅ Good: Lazy load admin panel
const AdminPanel = lazy(() => import('~/features/admin/AdminPanel'));

export const Route = createFileRoute('/admin')({
  component: AdminPanel,
});
```

### 3. Type-Safe Navigation

```typescript
// ✅ Good: Type-safe Link
<Link to="/posts/$postId" params={{ postId: post.id }}>
  View Post
</Link>

// ❌ Avoid: String concatenation
<a href={`/posts/${post.id}`}>View Post</a>
```

---

## Additional Resources

For more patterns, see:
- [routing-guide.md](resources/routing-guide.md) - Advanced routing
- [navigation-patterns.md](resources/navigation-patterns.md) - Navigation strategies
- [route-loaders.md](resources/route-loaders.md) - Complex loaders
