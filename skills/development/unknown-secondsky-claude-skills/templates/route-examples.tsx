/**
 * TanStack Router - Complete Examples
 * File-based routing structure and patterns
 */

// ============================================
// Root Route (src/routes/__root.tsx)
// ============================================

import { createRootRoute, Link, Outlet } from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

export const Route = createRootRoute({
  component: () => (
    <>
      <nav>
        <Link to="/" activeProps={{ className: 'font-bold' }}>Home</Link>
        <Link to="/about">About</Link>
        <Link to="/posts">Posts</Link>
      </nav>
      <hr />
      <Outlet />
      <TanStackRouterDevtools />
    </>
  ),
})

// ============================================
// Index Route (src/routes/index.tsx)
// ============================================

import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({
  component: HomePage,
})

function HomePage() {
  return <h1>Home Page</h1>
}

// ============================================
// Route with Params (src/routes/posts.$postId.tsx)
// ============================================

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    // Fully typed params!
    const post = await fetch(`/api/posts/${params.postId}`).then(r => r.json())
    return { post }
  },
  component: PostPage,
})

function PostPage() {
  const { post } = Route.useLoaderData()
  const { postId } = Route.useParams()

  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  )
}

// ============================================
// Route with TanStack Query (src/routes/posts.index.tsx)
// ============================================

import { queryOptions, useQuery } from '@tanstack/react-query'

const postsQueryOptions = queryOptions({
  queryKey: ['posts'],
  queryFn: async () => fetch('/api/posts').then(r => r.json()),
})

export const Route = createFileRoute('/posts/')({
  loader: ({ context: { queryClient } }) =>
    queryClient.ensureQueryData(postsQueryOptions),
  component: PostsListPage,
})

function PostsListPage() {
  const { data: posts } = useQuery(postsQueryOptions)

  return (
    <div>
      <h1>Posts</h1>
      {posts.map(post => (
        <Link key={post.id} to="/posts/$postId" params={{ postId: post.id }}>
          {post.title}
        </Link>
      ))}
    </div>
  )
}

// ============================================
// Nested Layout (src/routes/dashboard.tsx)
// ============================================

export const Route = createFileRoute('/dashboard')({
  component: DashboardLayout,
})

function DashboardLayout() {
  return (
    <div>
      <aside>Dashboard Sidebar</aside>
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  )
}

// Child: src/routes/dashboard.index.tsx
export const Route = createFileRoute('/dashboard/')({
  component: () => <h2>Dashboard Home</h2>,
})

// Child: src/routes/dashboard.settings.tsx
export const Route = createFileRoute('/dashboard/settings')({
  component: () => <h2>Settings</h2>,
})
