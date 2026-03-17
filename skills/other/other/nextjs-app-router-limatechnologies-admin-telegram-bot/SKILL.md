---
name: nextjs-app-router
description: Next.js 15 App Router patterns. Server/Client components, Server Actions, data fetching, caching, layouts, routing. Use when implementing Next.js features.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Next.js App Router - Modern Patterns

## Purpose

Expert guidance for Next.js 15 App Router:

- **Server Components** - Default rendering strategy
- **Client Components** - Interactive UI patterns
- **Server Actions** - Form mutations & data updates
- **Data Fetching** - Caching & revalidation strategies
- **Routing** - Layouts, loading, error boundaries

---

## Critical Rules

### 1. Server Components (Default)

> Components are Server Components by default. Only add `'use client'` when needed.

```tsx
// Server Component (default) - can access DB directly
async function UserProfile({ userId }: { userId: string }) {
	const user = await db.user.findUnique({ where: { id: userId } });
	return <div>{user.name}</div>;
}
```

### 2. Client Components (Interactive Only)

> Only use `'use client'` for interactivity (hooks, events, browser APIs).

```tsx
'use client';

import { useState } from 'react';

export function Counter() {
	const [count, setCount] = useState(0);
	return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### 3. Server Actions (Mutations)

> Use Server Actions for form submissions and data mutations.

```tsx
// app/actions.ts
'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const createUserSchema = z.object({
	name: z.string().min(2),
	email: z.string().email(),
});

export async function createUser(formData: FormData) {
	const data = createUserSchema.parse({
		name: formData.get('name'),
		email: formData.get('email'),
	});

	await db.user.create({ data });
	revalidatePath('/users');
}
```

---

## File Structure

```
app/
├── layout.tsx           # Root layout (required)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── not-found.tsx       # 404 page
├── (auth)/             # Route group (no URL segment)
│   ├── login/page.tsx
│   └── register/page.tsx
├── dashboard/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx
│   └── [id]/           # Dynamic route
│       └── page.tsx
└── api/
    └── trpc/[trpc]/route.ts
```

---

## Data Fetching Patterns

### Static Data (Default)

```tsx
// Cached at build time
async function getProducts() {
	const res = await fetch('https://api.example.com/products');
	return res.json();
}
```

### Dynamic Data

```tsx
// Always fresh
async function getUser(id: string) {
	const res = await fetch(`https://api.example.com/users/${id}`, {
		cache: 'no-store',
	});
	return res.json();
}
```

### Revalidate on Interval

```tsx
// Revalidate every 60 seconds
async function getPosts() {
	const res = await fetch('https://api.example.com/posts', {
		next: { revalidate: 60 },
	});
	return res.json();
}
```

### On-Demand Revalidation

```tsx
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function updatePost(id: string) {
  await db.post.update({ where: { id }, data: { ... } });

  revalidatePath('/posts');           // Revalidate path
  revalidateTag('posts');             // Revalidate tag
}
```

---

## Loading & Error States

### Loading UI

```tsx
// app/dashboard/loading.tsx
export default function Loading() {
	return <DashboardSkeleton />;
}
```

### Error Boundary

```tsx
// app/dashboard/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
	return (
		<div>
			<h2>Something went wrong!</h2>
			<button onClick={() => reset()}>Try again</button>
		</div>
	);
}
```

---

## Metadata & SEO

### Static Metadata

```tsx
// app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
	title: 'Home | MyApp',
	description: 'Welcome to MyApp',
};
```

### Dynamic Metadata

```tsx
// app/products/[id]/page.tsx
import type { Metadata } from 'next';

export async function generateMetadata({ params }: { params: { id: string } }): Promise<Metadata> {
	const product = await getProduct(params.id);
	return {
		title: product.name,
		description: product.description,
	};
}
```

---

## Route Handlers (API)

```tsx
// app/api/users/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
	const users = await db.user.findMany();
	return NextResponse.json(users);
}

export async function POST(request: Request) {
	const body = await request.json();
	const user = await db.user.create({ data: body });
	return NextResponse.json(user, { status: 201 });
}
```

---

## Middleware

```tsx
// middleware.ts (root)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
	// Check auth
	const token = request.cookies.get('token');

	if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
		return NextResponse.redirect(new URL('/login', request.url));
	}

	return NextResponse.next();
}

export const config = {
	matcher: ['/dashboard/:path*'],
};
```

---

## Common Patterns

### Parallel Data Fetching

```tsx
async function Dashboard() {
	// Fetch in parallel
	const [user, posts, notifications] = await Promise.all([
		getUser(),
		getPosts(),
		getNotifications(),
	]);

	return (
		<div>
			<UserCard user={user} />
			<PostList posts={posts} />
			<NotificationBell count={notifications.length} />
		</div>
	);
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

export default function Page() {
	return (
		<div>
			<h1>Dashboard</h1>
			<Suspense fallback={<UserSkeleton />}>
				<UserProfile />
			</Suspense>
			<Suspense fallback={<PostsSkeleton />}>
				<RecentPosts />
			</Suspense>
		</div>
	);
}
```

---

## Agent Integration

This skill is used by:

- **nextjs-expert** subagent
- **orchestrator** for routing Next.js tasks
- **ui-mobile/tablet/desktop** for platform-specific pages

---

## FORBIDDEN

1. **'use client' without reason** - Default is server
2. **useEffect for data fetching** - Use async components
3. **getServerSideProps/getStaticProps** - App Router uses async components
4. **API routes for internal data** - Use Server Components directly
5. **Client-side auth checks only** - Use middleware

---

## Version

- **v1.0.0** - Initial implementation based on Next.js 15 patterns
