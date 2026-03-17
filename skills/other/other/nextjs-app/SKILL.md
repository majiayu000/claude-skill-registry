---
name: nextjs-app
description: 生成Next.js 14+ App Router组件，包括服务端组件、客户端组件、API路由、中间件和数据获取模式。
metadata:
  short-description: 生成Next.js App Router代码
---

# Next.js App Skill

## Description
Generate Next.js 14+ App Router components with server/client patterns.

## Trigger
- `/nextjs` command
- User requests Next.js code
- User needs App Router patterns

## Prompt

You are a Next.js expert that creates modern App Router applications.

### Server Component with Data Fetching

```tsx
// app/users/page.tsx
import { Suspense } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

async function getUsers(): Promise<User[]> {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 }, // ISR: revalidate every 60 seconds
  });
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json();
}

async function UserList() {
  const users = await getUsers();
  
  return (
    <ul className="space-y-2">
      {users.map(user => (
        <li key={user.id} className="p-4 bg-white rounded-lg shadow">
          <h3 className="font-semibold">{user.name}</h3>
          <p className="text-gray-600">{user.email}</p>
        </li>
      ))}
    </ul>
  );
}

export default function UsersPage() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      <Suspense fallback={<div>Loading users...</div>}>
        <UserList />
      </Suspense>
    </main>
  );
}
```

### Client Component with Form

```tsx
'use client';

import { useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';
import { createUser } from './actions';

export function CreateUserForm() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(formData: FormData) {
    setError(null);
    startTransition(async () => {
      const result = await createUser(formData);
      if (result.error) {
        setError(result.error);
      } else {
        router.push('/users');
        router.refresh();
      }
    });
  }

  return (
    <form action={handleSubmit} className="space-y-4">
      {error && <div className="text-red-600">{error}</div>}
      
      <input
        name="name"
        placeholder="Name"
        required
        className="w-full p-2 border rounded"
      />
      <input
        name="email"
        type="email"
        placeholder="Email"
        required
        className="w-full p-2 border rounded"
      />
      
      <button
        type="submit"
        disabled={isPending}
        className="w-full p-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

### Server Action

```tsx
// app/users/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export async function createUser(formData: FormData) {
  const validated = CreateUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
  });

  if (!validated.success) {
    return { error: 'Invalid input' };
  }

  try {
    await fetch('https://api.example.com/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(validated.data),
    });
    
    revalidatePath('/users');
    return { success: true };
  } catch {
    return { error: 'Failed to create user' };
  }
}
```

### Middleware

```tsx
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;
  
  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith('/dashboard')) {
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

## Tags
`nextjs`, `react`, `app-router`, `server-components`, `fullstack`

## Compatibility
- Codex: ✅
- Claude Code: ✅
