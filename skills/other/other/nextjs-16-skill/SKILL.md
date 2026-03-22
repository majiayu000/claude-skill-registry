---
name: nextjs-16-skill
description: Expert guidance on Next.js 16 App Router development. Use when building or reviewing Next.js applications requiring: (1) App Router architecture and file-based routing, (2) Server Components vs Client Components decisions, (3) Server Actions for data mutations, (4) Better Auth authentication integration, (5) API route handlers, (6) React 19 patterns (useFormStatus, useActionState). Invoke when creating pages, components, authentication flows, or API endpoints in Next.js 16.
---

# Next.js 16 App Router

Expert guidance for building modern Next.js 16 applications with App Router.

## Quick Decision: Server or Client Component?

```
┌─────────────────────────────────────────────────────────────┐
│                    Component Decision Tree                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Does it need interactivity (onClick, onChange, etc.)?       │
│  ├── YES → Client Component ("use client")                   │
│  └── NO ↓                                                    │
│                                                              │
│  Does it use React hooks (useState, useEffect, etc.)?        │
│  ├── YES → Client Component ("use client")                   │
│  └── NO ↓                                                    │
│                                                              │
│  Does it need browser APIs (localStorage, window)?           │
│  ├── YES → Client Component ("use client")                   │
│  └── NO → Server Component (default, no directive needed)    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Server Component (Default)

```tsx
// app/tasks/page.tsx - NO "use client" directive
import { getTasks } from "@/lib/api";

export default async function TasksPage() {
  const tasks = await getTasks(); // Direct async data fetching

  return (
    <main>
      <h1>Tasks</h1>
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ul>
    </main>
  );
}
```

## Client Component

```tsx
"use client"; // Required directive at top of file

import { useState } from "react";

export function TaskForm({ onSubmit }: { onSubmit: (title: string) => void }) {
  const [title, setTitle] = useState("");

  return (
    <form onSubmit={(e) => { e.preventDefault(); onSubmit(title); }}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
      />
      <button type="submit">Add Task</button>
    </form>
  );
}
```

## Server Action (Mutation)

```tsx
// app/tasks/actions.ts
"use server";

import { revalidatePath } from "next/cache";

export async function createTask(formData: FormData) {
  const title = formData.get("title") as string;

  await fetch(`${process.env.API_URL}/tasks`, {
    method: "POST",
    body: JSON.stringify({ title }),
  });

  revalidatePath("/tasks"); // Refresh the page data
}
```

```tsx
// app/tasks/page.tsx - Using the action
import { createTask } from "./actions";

export default function TasksPage() {
  return (
    <form action={createTask}>
      <input name="title" placeholder="Task title" />
      <button type="submit">Add Task</button>
    </form>
  );
}
```

## Project Structure

```
app/
├── layout.tsx           # Root layout (Server Component)
├── page.tsx             # Home page
├── globals.css          # Global styles
├── tasks/
│   ├── page.tsx         # /tasks route
│   ├── actions.ts       # Server Actions
│   ├── [id]/
│   │   └── page.tsx     # /tasks/:id route
│   └── components/
│       └── TaskForm.tsx # Client Component
├── api/
│   └── tasks/
│       └── route.ts     # API route handler
└── auth/
    └── [...nextauth]/
        └── route.ts     # Better Auth handler
```

## Reference Guides

For detailed patterns, see:

- **App Router**: See [references/app-router.md](references/app-router.md) for routing, layouts, loading states, and error handling
- **Server/Client Components**: See [references/server-client-components.md](references/server-client-components.md) for composition patterns and data fetching
- **Server Actions**: See [references/server-actions.md](references/server-actions.md) for mutations, validation, and optimistic updates
- **Better Auth**: See [references/better-auth.md](references/better-auth.md) for authentication setup and protected routes
- **API Routes**: See [references/api-routes.md](references/api-routes.md) for route handlers and middleware
- **React 19 Patterns**: See [references/react-19-patterns.md](references/react-19-patterns.md) for useFormStatus, useActionState, and transitions
