---
name: nextjs-server-components
description: Use when next.js Server Components for optimal performance. Use when building data-intensive Next.js applications.
allowed-tools:
  - Bash
  - Read
---

# Next.js Server Components

Master Server Components in Next.js to build high-performance
applications with server-side rendering and data fetching.

## Server Components Basics

In Next.js App Router, all components are Server Components by default:

```typescript
// app/posts/page.tsx (Server Component by default)
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Cache for 1 hour
  });
  if (!res.ok) throw new Error('Failed to fetch posts');
  return res.json();
}

export default async function Posts() {
  const posts = await getPosts();

  return (
    <div>
      <h1>Blog Posts</h1>
      {posts.map((post: Post) => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
          <span>{new Date(post.date).toLocaleDateString()}</span>
        </article>
      ))}
    </div>
  );
}

// Direct database access (server-only)
import { db } from '@/lib/db';

export default async function Users() {
  const users = await db.user.findMany({
    select: {
      id: true,
      name: true,
      email: true
    }
  });

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>
          {user.name} - {user.email}
        </div>
      ))}
    </div>
  );
}
```

## Server vs Client Components Decision Tree

```typescript
// Use Server Components when:
// - Fetching data
// - Accessing backend resources directly
// - Keeping sensitive information on server
// - Keeping large dependencies on server

// Server Component (default)
export default async function ServerComp() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Use Client Components when:
// - Using interactivity (onClick, onChange, etc.)
// - Using state or lifecycle hooks (useState, useEffect)
// - Using browser-only APIs (localStorage, window, etc.)
// - Using custom hooks that depend on state/effects
// - Using React Context

// Client Component
'use client';
import { useState } from 'react';

export default function ClientComp() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}

// Composition: Server Component with Client Component
export default async function Page() {
  const data = await fetchData(); // Server-side

  return (
    <div>
      <ServerContent data={data} />
      <InteractiveButton /> {/* Client Component */}
    </div>
  );
}
```

## Server Actions for Mutations

```typescript
// app/actions.ts - Server Actions
'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const post = await db.post.create({
    data: { title, content }
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.id}`);
}

export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.post.update({
    where: { id },
    data: { title, content }
  });

  revalidatePath(`/posts/${id}`);
  return { success: true };
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } });
  revalidatePath('/posts');
}

// app/posts/new/page.tsx - Using Server Actions
export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}

// With client-side enhancement
'use client';
import { useFormStatus, useFormState } from 'react-dom';
import { createPost } from './actions';

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create Post'}
    </button>
  );
}

export default function NewPostForm() {
  const [state, formAction] = useFormState(createPost, null);

  return (
    <form action={formAction}>
      <input name="title" required />
      <textarea name="content" required />
      {state?.error && <p className="error">{state.error}</p>}
      <SubmitButton />
    </form>
  );
}
```

## Data Fetching Patterns

```typescript
// Parallel data fetching
async function getUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

async function getUserPosts(id: string) {
  const res = await fetch(`/api/users/${id}/posts`);
  return res.json();
}

export default async function UserProfile({ params }: {
  params: { id: string }
}) {
  // Fetch in parallel
  const [user, posts] = await Promise.all([
    getUser(params.id),
    getUserPosts(params.id)
  ]);

  return (
    <div>
      <UserInfo user={user} />
      <UserPosts posts={posts} />
    </div>
  );
}

// Sequential data fetching (when needed)
export default async function Dashboard() {
  // Fetch user first
  const user = await getUser();

  // Then fetch user-specific data
  const settings = await getUserSettings(user.id);
  const notifications = await getUserNotifications(user.id);

  return (
    <div>
      <UserHeader user={user} settings={settings} />
      <Notifications items={notifications} />
    </div>
  );
}

// Waterfall optimization with Suspense
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      {/* User loads first */}
      <Suspense fallback={<UserSkeleton />}>
        <User />
      </Suspense>

      {/* These load in parallel */}
      <div className="grid">
        <Suspense fallback={<SettingsSkeleton />}>
          <Settings />
        </Suspense>
        <Suspense fallback={<NotificationsSkeleton />}>
          <Notifications />
        </Suspense>
      </div>
    </div>
  );
}
```

## Streaming with Suspense

```typescript
// app/dashboard/page.tsx
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Fast component renders immediately */}
      <QuickStats />

      {/* Slow components stream in */}
      <Suspense fallback={<ChartSkeleton />}>
        <RevenueChart />
      </Suspense>

      <Suspense fallback={<TableSkeleton />}>
        <RecentOrders />
      </Suspense>

      <Suspense fallback={<ActivitySkeleton />}>
        <ActivityFeed />
      </Suspense>
    </div>
  );
}

async function RevenueChart() {
  // Slow data fetch
  const data = await fetchRevenueData();

  return <Chart data={data} />;
}

async function RecentOrders() {
  const orders = await fetchOrders({ limit: 10 });

  return (
    <table>
      {orders.map(order => (
        <tr key={order.id}>
          <td>{order.id}</td>
          <td>{order.total}</td>
        </tr>
      ))}
    </table>
  );
}

// Nested Suspense for granular streaming
async function ActivityFeed() {
  return (
    <div>
      <h2>Activity</h2>
      <Suspense fallback={<div>Loading comments...</div>}>
        <Comments />
      </Suspense>
      <Suspense fallback={<div>Loading likes...</div>}>
        <Likes />
      </Suspense>
    </div>
  );
}
```

## Server Component Patterns

```typescript
// Pattern 1: Data fetching in Server Component
async function fetchProduct(id: string) {
  const product = await db.product.findUnique({ where: { id } });
  return product;
}

export default async function ProductPage({ params }: {
  params: { id: string }
}) {
  const product = await fetchProduct(params.id);

  return (
    <div>
      <ProductDetails product={product} />
      <AddToCartButton productId={product.id} /> {/* Client Component */}
    </div>
  );
}

// Pattern 2: Server Component as data provider
async function ProductWithReviews({ id }: { id: string }) {
  const [product, reviews] = await Promise.all([
    fetchProduct(id),
    fetchReviews(id)
  ]);

  return (
    <>
      <ProductInfo product={product} />
      <ReviewList reviews={reviews} />
      <ReviewForm productId={id} /> {/* Client Component */}
    </>
  );
}

// Pattern 3: Composing Server and Client Components
export default async function Page() {
  const data = await fetchData();

  return (
    <ClientWrapper>
      {/* Server Component children work inside Client Components */}
      <ServerContent data={data} />
    </ClientWrapper>
  );
}

// Pattern 4: Props passing from Server to Client
export default async function Layout({
  children
}: {
  children: React.ReactNode
}) {
  const user = await getUser();

  return (
    <div>
      <ClientHeader user={user} /> {/* Pass server data to client */}
      <main>{children}</main>
    </div>
  );
}
```

## Client Component Patterns

```typescript
// Pattern 1: Minimal Client Component
'use client';
import { useState } from 'react';

export function Counter({ initialCount = 0 }: { initialCount?: number }) {
  const [count, setCount] = useState(initialCount);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}

// Pattern 2: Client Component with Server Component children
'use client';
import { useState } from 'react';

export function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <div>
      <div className="tabs">
        <button onClick={() => setActiveTab(0)}>Tab 1</button>
        <button onClick={() => setActiveTab(1)}>Tab 2</button>
      </div>
      <div>{children}</div>
    </div>
  );
}

// Usage: Server Component children work
export default async function Page() {
  const data = await fetchData();

  return (
    <Tabs>
      <ServerContent data={data} />
    </Tabs>
  );
}

// Pattern 3: Client wrapper with context
'use client';
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext<{
  theme: string;
  setTheme: (theme: string) => void;
} | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// Pattern 4: Optimistic updates with Server Actions
'use client';
import { useOptimistic } from 'react';
import { addTodo } from './actions';

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: string) => [
      ...state,
      { id: Date.now(), text: newTodo, pending: true }
    ]
  );

  async function formAction(formData: FormData) {
    const text = formData.get('text') as string;
    addOptimisticTodo(text);
    await addTodo(text);
  }

  return (
    <div>
      {optimisticTodos.map(todo => (
        <div key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>
          {todo.text}
        </div>
      ))}
      <form action={formAction}>
        <input name="text" />
        <button type="submit">Add</button>
      </form>
    </div>
  );
}
```

## Composition Strategies

```typescript
// Strategy 1: Server Component as layout
export default async function Layout({
  children
}: {
  children: React.ReactNode
}) {
  const user = await getUser();

  return (
    <div>
      <ServerNav user={user} />
      <Sidebar>
        <ClientSidebarContent /> {/* Interactive sidebar */}
      </Sidebar>
      <main>{children}</main>
    </div>
  );
}

// Strategy 2: Passing Server Components as props
export default async function Page() {
  const posts = await getPosts();

  return (
    <ClientLayout
      sidebar={<ServerSidebar posts={posts} />}
      main={<ServerContent posts={posts} />}
    />
  );
}

// Strategy 3: Server Component with multiple Client Components
export default async function Dashboard() {
  const data = await fetchDashboardData();

  return (
    <div>
      <ClientHeader />
      <ServerStats data={data.stats} />
      <ClientChart data={data.chartData} />
      <ServerTable data={data.tableData} />
      <ClientFilters />
    </div>
  );
}

// Strategy 4: Conditional Client Components
export default async function Page() {
  const user = await getUser();

  return (
    <div>
      {user.isAdmin ? (
        <AdminClientPanel />
      ) : (
        <UserServerContent user={user} />
      )}
    </div>
  );
}
```

## Server-Only Code

```typescript
// lib/server-only-utils.ts
import 'server-only'; // Ensures this file is never bundled for client

export async function getSecretData() {
  const apiKey = process.env.SECRET_API_KEY;
  // This code only runs on server
  const res = await fetch('https://api.example.com/secret', {
    headers: {
      Authorization: `Bearer ${apiKey}`
    }
  });
  return res.json();
}

export function decryptData(encrypted: string) {
  // Encryption logic that should never reach client
  return decrypt(encrypted, process.env.ENCRYPTION_KEY);
}

// app/dashboard/page.tsx
import { getSecretData } from '@/lib/server-only-utils';

export default async function Dashboard() {
  const data = await getSecretData();

  return <div>{data.publicInfo}</div>;
}

// Type-safe environment variables
// env.ts
import 'server-only';

export const env = {
  DATABASE_URL: process.env.DATABASE_URL!,
  API_KEY: process.env.API_KEY!,
  SECRET_KEY: process.env.SECRET_KEY!
} as const;

// Usage in Server Components
import { env } from '@/lib/env';

export default async function Page() {
  const data = await fetch('https://api.example.com', {
    headers: { 'X-API-Key': env.API_KEY }
  });

  return <div>Data fetched</div>;
}
```

## Performance Implications

```typescript
// Heavy dependency only loaded on server
import { marked } from 'marked'; // Markdown parser (large library)

export default async function MarkdownPage({ content }: {
  content: string
}) {
  // This runs only on server, keeping bundle small
  const html = marked(content);

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}

// Image optimization on server
import sharp from 'sharp'; // Image processing library

export default async function OptimizedImage({ src }: { src: string }) {
  // Process on server
  const buffer = await fetch(src).then(r => r.arrayBuffer());
  const optimized = await sharp(buffer)
    .resize(800, 600)
    .webp()
    .toBuffer();

  const base64 = optimized.toString('base64');

  return <img src={`data:image/webp;base64,${base64}`} />;
}

// Compute-intensive operations on server
export default async function AnalyticsPage() {
  // Heavy computation runs on server
  const rawData = await fetchRawData();
  const processed = processLargeDataset(rawData); // CPU-intensive
  const stats = calculateStatistics(processed); // More computation

  return <StatsDisplay stats={stats} />;
}

// Multiple data sources aggregation
export default async function AggregatedDashboard() {
  const [analytics, sales, inventory] = await Promise.all([
    fetchAnalytics(),
    fetchSales(),
    fetchInventory()
  ]);

  const report = generateReport(analytics, sales, inventory);

  return <ReportView report={report} />;
}
```

## Error Handling in Server Components

```typescript
// Throwing errors in Server Components
export default async function PostPage({ params }: {
  params: { id: string }
}) {
  const post = await db.post.findUnique({
    where: { id: params.id }
  });

  if (!post) {
    throw new Error('Post not found');
  }

  return <Article post={post} />;
}

// Using notFound() for 404s
import { notFound } from 'next/navigation';

export default async function UserPage({ params }: {
  params: { id: string }
}) {
  const user = await db.user.findUnique({
    where: { id: params.id }
  });

  if (!user) {
    notFound(); // Renders not-found.tsx
  }

  return <UserProfile user={user} />;
}

// Handling errors with try-catch
export default async function Page() {
  try {
    const data = await fetchData();
    return <Content data={data} />;
  } catch (error) {
    console.error('Failed to fetch data:', error);
    return <ErrorMessage />;
  }
}

// Error boundaries for Server Components
// Caught by nearest error.tsx
export default async function RiskyComponent() {
  const data = await riskyOperation(); // May throw

  return <Display data={data} />;
}
```

## When to Use This Skill

Use nextjs-server-components when you need to:

- Fetch data on the server
- Access backend resources directly
- Keep sensitive data server-side
- Reduce client bundle size
- Improve initial page load
- Build SEO-optimized pages
- Stream content to the client
- Implement zero-JS pages
- Optimize for performance
- Access databases directly
- Use server-only libraries
- Perform heavy computations

## Best Practices

1. **Use server components by default** - Only add 'use client' when you need
   interactivity, state, or browser APIs.

2. **Fetch data close to where it's used** - Colocate data fetching with the
   components that use the data.

3. **Leverage parallel data fetching** - Use Promise.all to fetch independent
   data sources simultaneously.

4. **Use streaming for better UX** - Wrap slow components in Suspense to show
   content as it loads.

5. **Keep sensitive logic server-side** - Database queries, API keys, and
   business logic should stay on server.

6. **Minimize client components** - Each 'use client' boundary increases
   JavaScript bundle size.

7. **Cache data appropriately** - Use Next.js caching strategies (revalidate,
   no-store) based on data freshness needs.

8. **Handle errors gracefully** - Use error boundaries and not-found pages for
   better error handling.

9. **Use TypeScript for type safety** - Define proper types for props and data
   to catch errors early.

10. **Test server component behavior** - Verify data fetching, error handling,
    and rendering in tests.

## Common Pitfalls

1. **Using client-only APIs in server components** - window, localStorage,
   document are not available on server.

2. **Not handling async errors properly** - Unhandled promise rejections crash
   the entire page.

3. **Mixing server and client state** - State management libraries don't work
   in server components.

4. **Overusing client components** - Adding 'use client' unnecessarily increases
   bundle size and reduces performance.

5. **Not leveraging data streaming** - Missing Suspense boundaries cause slow
   page loads instead of progressive rendering.

6. **Ignoring caching strategies** - Not setting revalidate times leads to stale
   data or unnecessary requests.

7. **Not optimizing data fetching** - Sequential fetches cause waterfalls;
   use parallel fetching when possible.

8. **Exposing sensitive data** - Accidentally passing secrets or API keys to
   client components.

9. **Not handling loading states** - Missing loading UI during data fetching
   creates poor user experience.

10. **Misunderstanding component boundaries** - Server components can't be
    imported into client components directly.

## Resources

- [Next.js Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [Composition Patterns](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns)
- [Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components)
