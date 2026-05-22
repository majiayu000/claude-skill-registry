---
name: nextjs-skill
description: Reusable Next.js 16+ skill with App Router, Server Components, Client Components, and API routes. Use with context7 MCP server.
---

# Next.js Skill

Use this skill when building React applications with Next.js 16+ App Router.

## Project Structure

```
app/
├── layout.tsx           # Root layout (HTML, body, providers)
├── page.tsx             # Home page (/)
├── globals.css          # Global styles (Tailwind)
├── not-found.tsx        # 404 page
├── loading.tsx          # Loading UI
├── error.tsx            # Error boundary
└── tasks/
    ├── page.tsx         # /tasks
    ├── layout.tsx       # Tasks layout
    └── [id]/
        └── page.tsx     # /tasks/:id
```

## Server vs Client Components

### Server Component (Default)
```typescript
// app/tasks/page.tsx
import { db } from "@/lib/db";

export default async function TasksPage() {
  const tasks = await db.getTasks();
  return (
    <div>
      <h1>Tasks</h1>
      <ul>
        {tasks.map(task => (
          <li key={task.id}>{task.title}</li>
        ))}
      </ul>
    </div>
  );
}
```

### Client Component
```typescript
// components/TaskForm.tsx
"use client";

import { useState } from "react";

export function TaskForm() {
  const [title, setTitle] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Form logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button type="submit">Add Task</button>
    </form>
  );
}
```

## Routing

### Dynamic Routes
```typescript
// app/tasks/[id]/page.tsx
interface PageProps {
  params: { id: string };
}

export default function TaskPage({ params }: PageProps) {
  const taskId = params.id;
  // Fetch and display task
}
```

### Route Groups
```typescript
// app/(auth)/login/page.tsx     // URL: /login
// app/(auth)/signup/page.tsx    // URL: /signup
// app/(dashboard)/tasks/page.tsx // URL: /tasks
```

### Parallel Routes
```typescript
// @modal/page.tsx
// @slot/page.tsx
```

## Data Fetching

### Direct Database Query (Server Component)
```typescript
// app/tasks/page.tsx
import { db } from "@/lib/db";

export default async function TasksPage({
  searchParams,
}: {
  searchParams: { status?: string };
}) {
  const status = searchParams.status || "all";
  const tasks = await db.getTasks(status);

  return (
    <div>
      <TaskList tasks={tasks} />
    </div>
  );
}
```

### With Suspense
```typescript
import { Suspense } from "react";
import { TaskList } from "@/components/TaskList";

export default function Page() {
  return (
    <Suspense fallback={<TaskListSkeleton />}>
      <TaskList />
    </Suspense>
  );
}
```

## Navigation

### Link Component
```typescript
import Link from "next/link";

<Link href="/tasks">View Tasks</Link>
<Link href={`/tasks/${task.id}`}>Edit</Link>
```

### Programmatic Navigation
```typescript
"use client";
import { useRouter } from "next/navigation";

export function CreateButton() {
  const router = useRouter();

  const handleClick = () => {
    router.push("/tasks/new");
    // or
    router.replace("/tasks");
    // or
    router.refresh(); // Refresh server data
  };

  return <button onClick={handleClick}>Go</button>;
}
```

## Forms

### Server Action Form
```typescript
// actions/create-task.ts
"use server";

import { redirect } from "next/navigation";

export async function createTask(formData: FormData) {
  const title = formData.get("title");
  // Validate and save to database
  redirect("/tasks");
}
```

```typescript
// app/tasks/new/page.tsx
import { createTask } from "@/actions/create-task";

export default function NewTaskPage() {
  return (
    <form action={createTask}>
      <input name="title" placeholder="Task title" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

## API Routes (Backend for Frontend)

```typescript
// app/api/tasks/route.ts
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");

  const tasks = await db.getTasks(status);
  return NextResponse.json(tasks);
}

export async function POST(request: Request) {
  const data = await request.json();
  const task = await db.createTask(data);
  return NextResponse.json(task, { status: 201 });
}
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Styling with Tailwind

```typescript
// app/page.tsx
export default function Page() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            Dashboard
          </h1>
        </div>
      </header>
      <main>
        <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {/* Content */}
        </div>
      </main>
    </div>
  );
}
```

## Best Practices

1. Use Server Components by default
2. Use `"use client"` only when needed (hooks, event handlers)
3. Fetch data directly in Server Components
4. Use Suspense for streaming UI
5. Use Link for client-side navigation
6. Use server actions for form submissions
7. Keep client-side state minimal
8. Use TypeScript for type safety
9. Organize by feature, not by file type
