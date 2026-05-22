---
name: bellog-rsc
description: Provides guidance on React Server Components vs Client Components decision-making in Bellog. Triggers when creating new components.
---

# Bellog Server/Client Components

This skill defines when to use Server Components vs Client Components in the Bellog blog project.

## Core Principle

**Default to Server Components.** Only use Client Components when necessary.

## Decision Tree

```
Does the component need interactivity or browser APIs?
│
├─ NO (static rendering)
│  └─ ✅ Server Component
│     - Fast initial load
│     - Zero client JavaScript
│     - Can use async/await directly
│     - Can access server-only APIs
│     - Better SEO
│
└─ YES (hooks, events, browser APIs)
   └─ 🔴 Client Component ("use client")
      - Can use hooks (useState, useEffect, etc.)
      - Can attach event handlers
      - Can access browser APIs
      - Can use framer-motion
      - Can use next-themes
```

## Server Components (Default)

### When to Use

✅ Use Server Components when:
- Rendering static content
- Fetching data from APIs or databases
- Reading from the filesystem
- No interactivity needed
- Pure presentation components
- SEO is critical

### Characteristics

```typescript
// ✅ Server Component (no "use client")

import { getAllPosts } from '@/lib/posts';

export default async function PostList() {
  // Can use async/await directly
  const posts = await getAllPosts();

  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

### Benefits

- **Performance:** No JavaScript sent to client
- **SEO:** Fully rendered HTML
- **Data fetching:** Direct database/API access
- **Security:** Can use secrets safely
- **Caching:** Automatic request memoization

### Examples in Bellog

**Server Components:**
- `app/page.tsx` - Home page (fetches recent posts)
- `app/posts/page.tsx` - Posts list (fetches all posts)
- `app/posts/[slug]/page.tsx` - Post detail (fetches single post)
- `PostList` component - Renders static post grid
- `PostCard` component - Static card rendering

## Client Components

### When to Use

🔴 Use Client Components when you need:

**1. React Hooks:**
- `useState`, `useEffect`, `useContext`
- `useRef`, `useCallback`, `useMemo`
- Custom hooks (`useScrollSpy`, etc.)

**2. Event Handlers:**
- `onClick`, `onChange`, `onSubmit`
- `onScroll`, `onMouseEnter`, `onMouseLeave`
- Form interactions

**3. Browser APIs:**
- `window`, `document`, `localStorage`
- `IntersectionObserver`, `ResizeObserver`
- `navigator`, `location`

**4. Third-Party Libraries:**
- **framer-motion** - Requires client
- **next-themes** - Theme toggle requires client
- Any library that uses browser APIs

### Characteristics

```typescript
"use client"; // Required at top of file

import { useState } from 'react';
import { motion } from 'framer-motion';

export function InteractiveCard() {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      whileHover={{ scale: 1.02 }}
    >
      {/* Interactive content */}
    </motion.div>
  );
}
```

### Examples in Bellog

**Client Components:**
- `Navbar.tsx` - Scroll detection, theme toggle
- `Intro.tsx` - TypeAnimation, framer-motion
- `NotionToc.tsx` - Scroll spy, active section tracking
- `template.tsx` - Page transition animations
- `ThemeToggle.tsx` - next-themes integration
- `ProgressBar.tsx` - Scroll progress tracking
- `GiscusComments.tsx` - Comment system (requires client JS)

## Common Patterns

### Pattern 1: Server Component with Client Island

**Best Practice:** Keep most as Server, wrap interactive parts as Client.

```typescript
// app/posts/[slug]/page.tsx (Server Component)
import { getPostBySlug } from '@/lib/posts';
import { NotionToc } from '@/components/posts/NotionToc'; // Client
import { PostNavigation } from '@/components/posts/PostNavigation'; // Client
import { PostRenderer } from '@/components/posts/PostRenderer'; // Server

export default async function PostPage({ params }) {
  const post = await getPostBySlug(params.slug);

  return (
    <div>
      <NotionToc headings={post.headings} /> {/* Client island */}
      <PostRenderer content={post.content} /> {/* Server */}
      <PostNavigation prev={post.prev} next={post.next} /> {/* Client */}
    </div>
  );
}
```

### Pattern 2: Passing Data from Server to Client

```typescript
// Server Component
async function ParentServer() {
  const data = await fetchData(); // Server-side fetch

  return <ChildClient data={data} />; // Pass as props
}

// Client Component
"use client";

function ChildClient({ data }) {
  const [selected, setSelected] = useState(data[0]);
  // Use data in client component
}
```

**Important:** Don't pass functions or Date objects - serialize data!

```typescript
// ❌ Wrong
<ClientComponent date={new Date()} />

// ✅ Correct
<ClientComponent date={new Date().toISOString()} />
```

### Pattern 3: Composition Pattern

**Wrap Client Component to Reduce Bundle:**

```typescript
// Layout (Server Component)
import { ClientHeader } from './ClientHeader';

export function Layout({ children }) {
  return (
    <>
      <ClientHeader /> {/* Only this is client */}
      <main>{children}</main> {/* Can be server */}
    </>
  );
}
```

## Caching Patterns (Server Components)

### React cache()

```typescript
import { cache } from 'react';

// Deduplicates requests within a single render
export const getPost = cache(async (id: string) => {
  return await fetchPost(id);
});
```

### Next.js unstable_cache()

```typescript
import { cache } from 'react';
import { unstable_cache } from 'next/cache';

export const getAllPosts = cache(
  unstable_cache(
    async () => {
      return await getAllPostsFromNotion();
    },
    ['all-posts'], // Cache key
    {
      revalidate: 3600, // 1 hour
      tags: ['posts', 'notion']
    }
  )
);
```

**Example from `/src/lib/posts.ts`:**

```typescript
export const getAllPosts = cache(
  unstable_cache(
    async () => {
      const posts = await getAllPostsFromNotion();
      return posts.sort((a, b) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
      );
    },
    ["all-posts"],
    {
      revalidate: 3600, // Revalidate every hour
      tags: ["posts", "notion"]
    }
  )
);
```

### On-Demand Revalidation

```typescript
// app/api/revalidate/route.ts
import { revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  const secret = request.nextUrl.searchParams.get('secret');

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ message: 'Invalid' }, { status: 401 });
  }

  revalidateTag('notion'); // Invalidate all Notion caches

  return Response.json({ revalidated: true });
}
```

## Common Mistakes

### Mistake 1: Unnecessary "use client"

```typescript
// ❌ Wrong (doesn't need "use client")
"use client";

export function StaticCard({ title, description }) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

// ✅ Correct (Server Component)
export function StaticCard({ title, description }) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}
```

### Mistake 2: Missing "use client"

```typescript
// ❌ Wrong (needs "use client" because of useState)
import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0); // Error!
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}

// ✅ Correct
"use client";

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Mistake 3: Async Client Component

```typescript
// ❌ Wrong (Client Components can't be async)
"use client";

export default async function Page() {
  const data = await fetchData(); // Error!
  return <div>{data}</div>;
}

// ✅ Correct (Server Component)
export default async function Page() {
  const data = await fetchData();
  return <ClientChild data={data} />;
}
```

### Mistake 4: Passing Functions as Props

```typescript
// ❌ Wrong (functions can't be serialized)
async function ServerComponent() {
  const handler = () => console.log('click');
  return <ClientComponent onClick={handler} />; // Error!
}

// ✅ Correct (define handler in client component)
"use client";

function ClientComponent() {
  const handler = () => console.log('click');
  return <button onClick={handler}>Click</button>;
}
```

## Component Type Checklist

When creating a component, ask:

- [ ] Does it use hooks? → Client
- [ ] Does it have event handlers? → Client
- [ ] Does it use framer-motion? → Client
- [ ] Does it use next-themes? → Client
- [ ] Does it access window/document? → Client
- [ ] Does it need browser APIs? → Client
- [ ] Otherwise → Server

If any checkbox is true, use "use client". Otherwise, keep as Server Component.

## Performance Impact

### Server Components

**Bundle Size:** 0 KB (no client JavaScript)
**Initial Load:** Fast (pre-rendered HTML)
**Hydration:** None needed
**SEO:** Excellent (fully rendered)

### Client Components

**Bundle Size:** Adds JavaScript to bundle
**Initial Load:** Slower (needs hydration)
**Hydration:** Required
**SEO:** Good (but requires hydration)

**Example:**
- `Navbar.tsx` (Client): ~5 KB
- `Intro.tsx` with framer-motion (Client): ~30 KB
- `PostList` (Server): 0 KB

## Best Practices

### 1. Start with Server

```typescript
// Always start here
export function Component() {
  // ...
}

// Only add "use client" when needed
```

### 2. Minimize Client Boundaries

```typescript
// ✅ Good - Only button is client
function Page() {
  return (
    <div>
      <StaticContent /> {/* Server */}
      <InteractiveButton /> {/* Client */}
    </div>
  );
}

// ❌ Bad - Everything is client
"use client";

function Page() {
  return (
    <div>
      <StaticContent /> {/* Unnecessary client */}
      <InteractiveButton />
    </div>
  );
}
```

### 3. Extract Client Logic

```typescript
// ✅ Extract interactive part
function ServerCard({ data }) {
  return (
    <div>
      <StaticHeader data={data} /> {/* Server */}
      <InteractiveActions id={data.id} /> {/* Client */}
    </div>
  );
}

"use client";

function InteractiveActions({ id }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}
```

### 4. Use Composition

```typescript
// Layout stays Server
function Layout({ children }) {
  return (
    <>
      <Header /> {/* Client component */}
      <main>{children}</main> {/* Can be Server */}
      <Footer /> {/* Server component */}
    </>
  );
}
```

## Quick Reference

```typescript
// Server Component (default)
export async function Component() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Client Component (when needed)
"use client";

import { useState } from 'react';

export function Component() {
  const [state, setState] = useState();
  return <button onClick={() => setState(...)}>Click</button>;
}

// Client with framer-motion
"use client";

import { motion } from 'framer-motion';

export function Component() {
  return <motion.div animate={{ opacity: 1 }}>...</motion.div>;
}

// Pass data Server → Client
function Server() {
  const data = await fetch();
  return <Client data={data} />; // Serialize data
}
```

Remember: Every "use client" adds to bundle size. Be intentional about where you place client boundaries.
