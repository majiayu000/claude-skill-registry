---
name: nextjs-app-router
description: Next.js 16 App Router patterns including server components, client components, server actions, route handlers, layouts, metadata API, dynamic routes, file conventions, data fetching, caching strategies, and Next.js best practices for building modern React applications
model: sonnet
---

# Next.js App Router Patterns

## When to Use This Skill

Activate this skill when working on:

- Creating new pages, routes, or layouts
- Implementing server or client components
- Building server actions for data mutations
- Setting up route handlers (API endpoints)
- Configuring metadata and SEO
- Implementing dynamic routes
- Organizing app directory structure
- Data fetching and caching strategies

## Core Patterns

### Server vs Client Components Decision Tree

**Use Server Components (default) when:**

- Fetching data from databases or APIs
- Accessing backend resources directly
- Keeping sensitive information secure (API keys, tokens)
- Reducing client-side JavaScript bundle
- No interactivity required

**Use Client Components (`'use client'`) when:**

- Using React hooks (`useState`, `useEffect`, `useContext`)
- Handling browser events (onClick, onChange)
- Using browser-only APIs (localStorage, window)
- Using third-party libraries that depend on React hooks
- Implementing real-time features with Ably

**Example:**

```tsx
// app/board/[id]/page.tsx - Server Component (default)
import { getBoard } from "@/lib/actions/board/getBoard";

export default async function BoardPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const board = await getBoard(id);

  return <BoardView board={board} />;
}
```

```tsx
// components/board/BoardView.tsx - Client Component
"use client";

import { useState } from "react";
import { PostProvider } from "@/components/board/PostProvider";

export function BoardView({ board }) {
  const [filter, setFilter] = useState("all");

  return <PostProvider boardId={board.id}>{/* Interactive UI */}</PostProvider>;
}
```

### Server Actions with Authentication

**CRITICAL:** All server actions MUST use `actionWithAuth` or `rbacWithAuth` wrappers (see [rbac-security](../rbac-security/SKILL.md) skill).

**Pattern:**

```tsx
// lib/actions/post/createPost.ts
"use server";

import { rbacWithAuth } from "@/lib/actions/actionWithAuth";
import { db } from "@/db";
import { postTable } from "@/db/schema";

export const createPost = async (
  boardId: string,
  content: string,
  type: PostType
) =>
  rbacWithAuth(boardId, async (userId) => {
    const post = await db
      .insert(postTable)
      .values({
        id: nanoid(),
        boardId,
        userId,
        content,
        type,
        createdAt: new Date(),
      })
      .returning();

    return post[0];
  });
```

**Usage in Client Components:**

```tsx
"use client";

import { createPost } from "@/lib/actions/post/createPost";
import { useTransition } from "react";

export function CreatePostForm({ boardId }) {
  const [isPending, startTransition] = useTransition();

  const handleSubmit = async (formData: FormData) => {
    startTransition(async () => {
      await createPost(boardId, formData.get("content") as string, "went_well");
    });
  };

  return <form action={handleSubmit}>...</form>;
}
```

### File-Based Routing Conventions

**Special Files:**

- `page.tsx` - Unique UI for a route
- `layout.tsx` - Shared UI for segments and children
- `loading.tsx` - Loading UI (Suspense boundary)
- `error.tsx` - Error UI (Error boundary)
- `not-found.tsx` - Not found UI
- `route.ts` - API endpoint (Route Handler)

**Route Organization:**

```text
app/
├── layout.tsx                    # Root layout
├── page.tsx                      # Home page
├── board/
│   ├── layout.tsx               # Board layout
│   ├── page.tsx                 # Board list
│   └── [id]/
│       ├── page.tsx             # Board detail (dynamic route)
│       ├── loading.tsx          # Loading state
│       └── error.tsx            # Error handling
└── api/
    └── webhooks/
        └── route.ts             # API route handler
```

### Metadata API for SEO

**Static Metadata:**

```tsx
// app/board/[id]/page.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Board Details",
  description: "View and manage your retrospective board",
};
```

**Dynamic Metadata:**

```tsx
// app/board/[id]/page.tsx
import { getBoard } from "@/lib/actions/board/getBoard";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const board = await getBoard(id);

  return {
    title: `${board.name} - Ree Board`,
    description: board.description,
    openGraph: {
      title: board.name,
      description: board.description,
    },
  };
}
```

### Dynamic Imports for Code Splitting

**Lazy Load Heavy Components:**

```tsx
import dynamic from "next/dynamic";

// Drag-and-drop is lazy loaded in the project
const PostDragDrop = dynamic(() => import("@/components/board/PostDragDrop"), {
  ssr: false,
  loading: () => <LoadingSkeleton />,
});
```

## Anti-Patterns

### ❌ Using 'use client' at the Top Level Unnecessarily

**Bad:**

```tsx
"use client"; // ❌ Unnecessary - no hooks or interactivity

export default function Page() {
  return <div>Static content</div>;
}
```

**Good:**

```tsx
// ✅ Server component by default
export default function Page() {
  return <div>Static content</div>;
}
```

### ❌ Fetching Data in Client Components

**Bad:**

```tsx
"use client";

export default function Page() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/api/data")
      .then((r) => r.json())
      .then(setData); // ❌
  }, []);
}
```

**Good:**

```tsx
// ✅ Server component fetches data
export default async function Page() {
  const data = await getData();
  return <ClientView data={data} />;
}
```

### ❌ Server Actions Without Authentication

**Bad:**

```tsx
"use server";

export async function deleteBoard(id: string) {
  // ❌ No auth check - security vulnerability
  await db.delete(boardTable).where(eq(boardTable.id, id));
}
```

**Good:**

```tsx
"use server";

export const deleteBoard = async (id: string) =>
  rbacWithAuth(id, async (userId) => {
    // ✅ Authentication and RBAC enforced
    await db.delete(boardTable).where(eq(boardTable.id, id));
  });
```

### ❌ Not Using Suspense Boundaries

**Bad:**

```tsx
export default async function Page() {
  const data = await slowDataFetch(); // ❌ Blocks entire page
  return <div>{data}</div>;
}
```

**Good:**

```tsx
import { Suspense } from "react";

export default function Page() {
  return (
    <Suspense fallback={<Loading />}>
      <DataComponent />
    </Suspense>
  );
}

async function DataComponent() {
  const data = await slowDataFetch();
  return <div>{data}</div>;
}
```

## Integration with Other Skills

- **[rbac-security](../rbac-security/SKILL.md):** Server actions require authentication wrappers
- **[drizzle-patterns](../drizzle-patterns/SKILL.md):** Data fetching in server components
- **[signal-state-management](../signal-state-management/SKILL.md):** Client-side state in 'use client' components
- **[ably-realtime](../ably-realtime/SKILL.md):** Real-time features require client components
- **[testing-patterns](../testing-patterns/SKILL.md):** Test both server and client components

## Project-Specific Context

### Key Files

- `app/` - Next.js App Router directory
- `app/layout.tsx` - Root layout with providers
- `app/board/[id]/page.tsx` - Dynamic board page
- `lib/actions/` - Server actions by domain
- `proxy.ts` - Supabase authentication proxy (Next.js 16)
- `next.config.js` - Next.js configuration

### Project Conventions

1. Server actions live in `lib/actions/[entity]/`
2. All server actions use `actionWithAuth` or `rbacWithAuth`
3. Client components prefixed with 'use client'
4. Heavy components lazy-loaded (drag-and-drop)
5. Metadata configured for all public pages

### Environment-Specific Behavior

- Development: Local Turso database
- Production: Turso Cloud with auth tokens
- Both: Supabase authentication required

---

**Last Updated:** 2026-01-10
