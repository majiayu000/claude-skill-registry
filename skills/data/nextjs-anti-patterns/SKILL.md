---
name: nextjs-anti-patterns
description: Identify and fix common Next.js App Router anti-patterns and mistakes.
  Use when reviewing code for Next.js best practices, debugging performance issues,
  migrating from Pages Router patterns, or preven
---

---
name: nextjs-anti-patterns
description: Identify and fix common Next.js App Router anti-patterns and mistakes. Use when reviewing code for Next.js best practices, debugging performance issues, migrating from Pages Router patterns, or preventing common pitfalls. Activates for code review, performance optimization, or detecting inappropriate useEffect/useState usage. CRITICAL: For browser detection, keep the logic in the user-facing component (or a composed helper that it renders) rather than isolating it in unused files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js Anti-Patterns

## Overview

Identify and correct common anti-patterns in Next.js App Router applications, focusing on misuse of useEffect, improper data fetching, unnecessary client-side state, and incorrect component boundaries.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**
```typescript
function handleSubmit(e: any) { ... }
const data: any[] = [];
```

**✅ CORRECT:**
```typescript
function handleSubmit(e: React.FormEvent<HTMLFormElement>) { ... }
const data: string[] = [];
```

### Common Next.js Type Patterns

```typescript
// Page props
function Page({ params }: { params: { slug: string } }) { ... }
function Page({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) { ... }

// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { ... }
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { ... }

// Server actions
async function myAction(formData: FormData) { ... }
```

## When to Use This Skill

Use this skill when:
- Reviewing Next.js code for best practices
- Debugging performance issues in App Router apps
- Migrating from Pages Router with legacy patterns
- Code shows excessive client-side JavaScript
- Components are using useEffect unnecessarily
- Detecting waterfall data fetching patterns
- Identifying incorrect Server/Client component usage

## Rendering Responsibilities

When requirements call for a page or component to present specific UI (e.g., display a banner or guard message), place that rendering responsibility in the exported component that callers actually use. Helper components are fine, but make sure they are composed so the main entry point still outputs the expected elements.

### Recommended Pattern

```typescript
// page.tsx
'use client';

import { BrowserGuard } from './BrowserGuard';

export default function Page() {
  return <BrowserGuard />;
}

// BrowserGuard.tsx
'use client';

export function BrowserGuard() {
  const isSafari = typeof navigator !== 'undefined' &&
    /Safari/.test(navigator.userAgent) &&
    !/Chrome/.test(navigator.userAgent);

  if (isSafari) {
    return <h1>Unsupported Browser</h1>;
  }

  return <h1>Welcome</h1>;
}
```

This keeps the logic modular while ensuring the visible component still renders the appropriate message. Apply the same principle to other requirements—compose helpers, but never leave the primary component without the mandated UI.

## Anti-Pattern Categories

### Category 1: Inappropriate useEffect Usage

#### Anti-Pattern 1.1: Using useEffect for Browser Detection

**❌ WRONG - useEffect with useState:**
```typescript
'use client';

import { useEffect, useState } from 'react';

export default function BrowserCheck() {
  const [isSafari, setIsSafari] = useState(false);

  useEffect(() => {
    setIsSafari(/Safari/.test(navigator.userAgent));
  }, []);

  return <div>{isSafari ? 'Unsupported' : 'Welcome'}</div>;
}
```

**Why it's wrong:**
- Causes flash of wrong content (renders default, then updates)
- Unnecessary client-side state management
- Can be detected directly in component body
- Creates hydration mismatch

**✅ CORRECT - Direct browser detection in component body:**
```typescript
'use client';

export default function BrowserCheck() {
  // Direct detection without useState or useEffect
  const isSafari = typeof navigator !== 'undefined' &&
    /Safari/.test(navigator.userAgent) &&
    !/Chrome/.test(navigator.userAgent);

  const isFirefox = typeof navigator !== 'undefined' &&
    /Firefox/.test(navigator.userAgent);

  if (isSafari || isFirefox) {
    return <h1>Unsupported Browser</h1>;
  }

  return <h1>Welcome</h1>;
}
```

**Key points:**
- Use `typeof navigator !== 'undefined'` for SSR safety
- Direct detection in component body (no hooks)
- Use conditional rendering, not useState
- Safari detection should exclude Chrome (`!/Chrome/.test(...)`)
- Implement directly in the component OR create a helper and import it into the exported entry point
- Ensure the logic is accessible from the component that consumers will render

**Alternative: Use CSS media queries for responsive:**
```typescript
export default function ResponsiveComponent() {
  return (
    <div>
      <div className="block md:hidden"><MobileView /></div>
      <div className="hidden md:block"><DesktopView /></div>
    </div>
  );
}
```

#### Anti-Pattern 1.2: Using useEffect for Data Fetching

**Wrong:**
```typescript
'use client';

import { useEffect, useState } from 'react';

export default function BlogPosts() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/posts')
      .then(res => res.json())
      .then(data => {
        setPosts(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

**Why it's wrong:**
- Adds unnecessary client-side JavaScript
- Creates loading states that could be avoided
- Slower initial render (client-side fetch)
- Complicates error handling
- Breaks without JavaScript enabled

**Correct:**
```typescript
// Server Component (no 'use client')
export default async function BlogPosts() {
  const response = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 } // Cache for 1 hour
  });

  if (!response.ok) {
    throw new Error('Failed to fetch posts');
  }

  const posts = await response.json();

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

**Benefits:**
- Zero client-side JavaScript for this component
- No loading state needed
- Faster initial render (server-side)
- Automatic error boundary support
- Works without JavaScript

#### Anti-Pattern 1.3: Using useEffect for URL Detection

**Wrong:**
```typescript
'use client';

import { useEffect, useState } from 'react';

export default function ShareButton() {
  const [url, setUrl] = useState('');

  useEffect(() => {
    setUrl(window.location.href);
  }, []);

  const handleShare = () => {
    navigator.share({ url });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

**Correct:**
```typescript
'use client';

export default function ShareButton() {
  const handleShare = () => {
    // Access URL directly when needed
    const url = window.location.href;
    navigator.share({ url });
  };

  return <button onClick={handleShare}>Share</button>;
}
```

### Category 2: Inappropriate useState Usage

#### Anti-Pattern 2.1: Using useState for Server Data

**Wrong:**
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(r => r.json())
      .then(setUser);
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return <div>{user.name}</div>;
}
```

**Correct:**
```typescript
// Server Component
export default async function UserProfile({ userId }: { userId: string }) {
  const response = await fetch(`https://api.example.com/users/${userId}`);
  const user = await response.json();

  return <div>{user.name}</div>;
}
```

#### Anti-Pattern 2.2: Using useState for Derived Values

**Wrong:**
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function ProductList({ products }: { products: Product[] }) {
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setTotal(products.reduce((sum, p) => sum + p.price, 0));
  }, [products]);

  return <div>Total: ${total}</div>;
}
```

**Correct:**
```typescript
'use client';

export default function ProductList({ products }: { products: Product[] }) {
  // Calculate directly - no state needed
  const total = products.reduce((sum, p) => sum + p.price, 0);

  return <div>Total: ${total}</div>;
}
```

**Or, if truly expensive calculation:**
```typescript
'use client';

import { useMemo } from 'react';

export default function ProductList({ products }: { products: Product[] }) {
  const total = useMemo(
    () => products.reduce((sum, p) => sum + p.price, 0),
    [products]
  );

  return <div>Total: ${total}</div>;
}
```

### Category 3: Pages Router Patterns in App Router

#### Anti-Pattern 3.1: Using getServerSideProps

**Wrong:**
```typescript
// This doesn't work in App Router!
export async function getServerSideProps() {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();

  return { props: { data } };
}

export default function Page({ data }) {
  return <div>{data.title}</div>;
}
```

**Correct:**
```typescript
// App Router: Server Component with async
export default async function Page() {
  const res = await fetch('https://api.example.com/data', {
    cache: 'no-store' // Equivalent to getServerSideProps
  });
  const data = await res.json();

  return <div>{data.title}</div>;
}
```

#### Anti-Pattern 3.2: Using getStaticProps

**Wrong:**
```typescript
// This doesn't work in App Router!
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();

  return { props: { data }, revalidate: 60 };
}
```

**Correct:**
```typescript
// App Router: Server Component with revalidation
export default async function Page() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 } // Revalidate every 60 seconds
  });
  const data = await res.json();

  return <div>{data.title}</div>;
}
```

#### Anti-Pattern 3.3: Using next/head in App Router

**Wrong:**
```typescript
import Head from 'next/head';

export default function Page() {
  return (
    <>
      <Head>
        <title>My Page</title>
        <meta name="description" content="Description" />
      </Head>
      <main>Content</main>
    </>
  );
}
```

**Correct:**
```typescript
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Page',
  description: 'Description',
};

export default function Page() {
  return <main>Content</main>;
}
```

### Category 4: Performance Anti-Patterns

#### Anti-Pattern 4.1: Serial Await (Waterfall Requests)

**Wrong:**
```typescript
export default async function Dashboard() {
  // This takes 3 seconds total if each request takes 1 second
  const user = await fetchUser();
  const posts = await fetchPosts();      // Waits for user
  const comments = await fetchComments(); // Waits for posts

  return (
    <div>
      <UserInfo user={user} />
      <Posts posts={posts} />
      <Comments comments={comments} />
    </div>
  );
}
```

**Correct:**
```typescript
export default async function Dashboard() {
  // This takes 1 second total (parallel fetching)
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ]);

  return (
    <div>
      <UserInfo user={user} />
      <Posts posts={posts} />
      <Comments comments={comments} />
    </div>
  );
}
```

**Even Better: Use Suspense for progressive rendering:**
```typescript
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<UserSkeleton />}>
        <UserInfo />
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
      <Suspense fallback={<CommentsSkeleton />}>
        <Comments />
      </Suspense>
    </div>
  );
}

async function UserInfo() {
  const user = await fetchUser();
  return <div>{user.name}</div>;
}

async function Posts() {
  const posts = await fetchPosts();
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}

async function Comments() {
  const comments = await fetchComments();
  return <ul>{comments.map(c => <li key={c.id}>{c.text}</li>)}</ul>;
}
```

#### Anti-Pattern 4.2: Over-using 'use client'

**Wrong:**
```typescript
// app/layout.tsx
'use client'; // Unnecessary - makes entire app client-side!

export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

**Correct:**
```typescript
// app/layout.tsx
// No 'use client' - keep as Server Component
export default function RootLayout({ children }) {
  return (
    <html>
      <body>{children}</body>
    </html>
  );
}
```

**Rule:** Only add `'use client'` to the lowest level component that needs it.

**Wrong:**
```typescript
// app/page.tsx
'use client'; // Entire page becomes client component

export default function Page() {
  return (
    <div>
      <Header />
      <StaticContent />
      <InteractiveButton />
    </div>
  );
}
```

**Correct:**
```typescript
// app/page.tsx - Server Component
export default function Page() {
  return (
    <div>
      <Header />
      <StaticContent />
      <InteractiveButton /> {/* Only this needs 'use client' */}
    </div>
  );
}

// InteractiveButton.tsx
'use client';

export default function InteractiveButton() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>;
}
```

#### Anti-Pattern 4.3: Importing Server Components into Client Components

**Wrong:**
```typescript
// ClientComponent.tsx
'use client';

import ServerComponent from './ServerComponent'; // Becomes client component!

export default function ClientComponent() {
  return <div><ServerComponent /></div>;
}
```

**Correct:**
```typescript
// ParentComponent.tsx (Server Component)
import ClientComponent from './ClientComponent';
import ServerComponent from './ServerComponent';

export default function ParentComponent() {
  return (
    <ClientComponent>
      <ServerComponent /> {/* Stays as Server Component */}
    </ClientComponent>
  );
}

// ClientComponent.tsx
'use client';

export default function ClientComponent({ children }) {
  return <div className="wrapper">{children}</div>;
}
```

### Category 5: Router and Navigation Anti-Patterns

#### Anti-Pattern 5.1: Using window.location for Navigation

**Wrong:**
```typescript
'use client';

export default function NavButton() {
  const handleClick = () => {
    window.location.href = '/dashboard'; // Full page reload!
  };

  return <button onClick={handleClick}>Go to Dashboard</button>;
}
```

**Correct:**
```typescript
'use client';

import { useRouter } from 'next/navigation';

export default function NavButton() {
  const router = useRouter();

  const handleClick = () => {
    router.push('/dashboard'); // Client-side navigation
  };

  return <button onClick={handleClick}>Go to Dashboard</button>;
}
```

**Even Better: Use Link component:**
```typescript
import Link from 'next/link';

export default function NavButton() {
  return <Link href="/dashboard">Go to Dashboard</Link>;
}
```

#### Anti-Pattern 5.2: Using useRouter in Server Components

**Wrong:**
```typescript
// Server Component
import { useRouter } from 'next/navigation'; // ERROR!

export default function Page() {
  const router = useRouter(); // This will fail
  return <div>...</div>;
}
```

**Correct for Server Components:**
```typescript
// Server Component - use redirect
import { redirect } from 'next/navigation';

export default async function Page() {
  const user = await getUser();

  if (!user) {
    redirect('/login');
  }

  return <div>Welcome, {user.name}</div>;
}
```

**Correct for Client Components:**
```typescript
// Client Component
'use client';

import { useRouter } from 'next/navigation';

export default function Page() {
  const router = useRouter();

  const handleLogout = () => {
    router.push('/login');
  };

  return <button onClick={handleLogout}>Logout</button>;
}
```

### Category 6: Data Fetching Anti-Patterns

#### Anti-Pattern 6.1: Creating Unnecessary API Routes

**Wrong:**
```typescript
// app/api/posts/route.ts
export async function GET() {
  const posts = await db.posts.findMany();
  return Response.json(posts);
}

// app/posts/page.tsx
'use client';

import { useEffect, useState } from 'react';

export default function Posts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch('/api/posts')
      .then(r => r.json())
      .then(setPosts);
  }, []);

  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

**Correct:**
```typescript
// app/posts/page.tsx - Direct database access
import { db } from '@/lib/db';

export default async function Posts() {
  const posts = await db.posts.findMany();

  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

**When API routes ARE appropriate:**
- External webhooks
- Client-side mutations
- Third-party integrations
- Public API endpoints

#### Anti-Pattern 6.2: Not Handling Loading States Properly

**Wrong:**
```typescript
// No loading UI - page blocks until all data loads
export default async function Dashboard() {
  const data = await fetchSlowData(); // Takes 5 seconds

  return <div>{data.content}</div>;
}
```

**Correct:**
```typescript
import { Suspense } from 'react';

export default function Dashboard() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <DashboardContent />
    </Suspense>
  );
}

async function DashboardContent() {
  const data = await fetchSlowData();
  return <div>{data.content}</div>;
}
```

## When Client Components ARE Appropriate

Despite all these anti-patterns, Client Components are still necessary and correct for:

### 1. Event Handlers and Interactivity

```typescript
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Clicks: {count}
    </button>
  );
}
```

### 2. Form State Management

```typescript
'use client';

import { useState } from 'react';

export default function SearchForm() {
  const [query, setQuery] = useState('');

  return (
    <form>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
    </form>
  );
}
```

### 3. Browser APIs

```typescript
'use client';

import { useEffect } from 'react';

export default function ScrollTracker() {
  useEffect(() => {
    const handleScroll = () => {
      console.log('Scroll position:', window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return <div>Scroll tracker active</div>;
}
```

### 4. Third-Party Client Libraries

```typescript
'use client';

import { useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';

export default function Map() {
  const mapContainer = useRef(null);

  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/streets-v11',
    });

    return () => map.remove();
  }, []);

  return <div ref={mapContainer} />;
}
```

### 5. React Context Consumers

```typescript
'use client';

import { useContext } from 'react';
import { ThemeContext } from './ThemeContext';

export default function ThemedButton() {
  const { theme, setTheme } = useContext(ThemeContext);

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle Theme
    </button>
  );
}
```

## Detection Checklist

When reviewing Next.js App Router code, check for:

- [ ] `useEffect` used for data fetching → Replace with Server Component
- [ ] `useEffect` used for browser detection → Do it directly or use CSS
- [ ] `useState` used for server data → Replace with Server Component
- [ ] `getServerSideProps` or `getStaticProps` → Migrate to async Server Components
- [ ] `next/head` imports → Replace with metadata exports
- [ ] Serial `await` statements → Use Promise.all or Suspense
- [ ] `'use client'` on static components → Remove directive
- [ ] Client Component importing Server Component → Use composition pattern
- [ ] API routes for simple data fetching → Access database directly in Server Component
- [ ] `window.location.href` for navigation → Use Link or useRouter
- [ ] Missing Suspense boundaries for slow data → Add Suspense

## Migration Strategy

When migrating code with anti-patterns:

1. **Identify data fetching** - Look for useEffect with fetch/axios
2. **Convert to Server Components** - Remove 'use client', make async
3. **Separate interactivity** - Extract interactive parts to small Client Components
4. **Update metadata** - Replace next/head with metadata exports
5. **Parallelize fetching** - Use Promise.all for independent requests
6. **Add Suspense** - Wrap slow components in Suspense boundaries
7. **Test thoroughly** - Ensure functionality preserved

## Summary

- **Default to Server Components** - add 'use client' only when needed
- **Never use useEffect for data fetching** - use async Server Components
- **Never use useState for server data** - fetch in Server Components
- **Avoid serial await** - use Promise.all for parallel fetching
- **Keep 'use client' boundary low** - only on components that need it
- **Use Suspense for loading states** - better UX than blocking
- **Access data directly** - avoid unnecessary API routes
- **Use metadata exports** - not next/head in App Router
