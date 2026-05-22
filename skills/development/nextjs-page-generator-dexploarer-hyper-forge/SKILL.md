---
name: nextjs-page-generator
description: Generates Next.js 13+ pages with App Router, Server Components, Client Components, API routes, and proper data fetching. Use when building Next.js applications.
---

# Next.js Page Generator Skill

Expert at creating Next.js 13+ pages using App Router, Server/Client Components, and modern patterns.

## When to Activate

- "create Next.js page for [feature]"
- "generate Next.js app router page"
- "build Next.js component with data fetching"

## App Router Page Structure

### Server Component (Default)

```typescript
// app/users/page.tsx
import { Suspense } from 'react';
import { UserList } from './UserList';
import { LoadingSkeleton } from '@/components/LoadingSkeleton';

// Metadata
export const metadata = {
  title: 'Users | My App',
  description: 'Browse all users',
};

// Revalidate every hour
export const revalidate = 3600;

interface PageProps {
  searchParams: { page?: string; search?: string };
}

export default async function UsersPage({ searchParams }: PageProps) {
  const page = Number(searchParams.page) || 1;
  const search = searchParams.search || '';

  // Server-side data fetching
  const users = await fetchUsers({ page, search });

  return (
    <div className="container">
      <h1>Users</h1>

      <Suspense fallback={<LoadingSkeleton />}>
        <UserList users={users} />
      </Suspense>
    </div>
  );
}

// Data fetching function
async function fetchUsers({ page, search }: { page: number; search: string }) {
  const res = await fetch(
    `${process.env.API_URL}/users?page=${page}&search=${search}`,
    {
      next: { revalidate: 3600 }, // Cache for 1 hour
    }
  );

  if (!res.ok) {
    throw new Error('Failed to fetch users');
  }

  return res.json();
}
```

### Client Component (Interactive)

```typescript
// app/users/UserList.tsx
'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

interface User {
  id: number;
  name: string;
  email: string;
}

interface UserListProps {
  users: User[];
}

export function UserList({ users }: UserListProps) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [search, setSearch] = useState(searchParams.get('search') || '');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams(searchParams);
    params.set('search', search);
    params.set('page', '1');
    router.push(`/users?${params.toString()}`);
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search users..."
        />
        <button type="submit">Search</button>
      </form>

      <ul>
        {users.map((user) => (
          <li key={user.id}>
            <a href={`/users/${user.id}`}>
              {user.name} ({user.email})
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Dynamic Route

```typescript
// app/users/[id]/page.tsx
import { notFound } from 'next/navigation';
import { Metadata } from 'next';

interface PageProps {
  params: { id: string };
}

// Generate static params at build time
export async function generateStaticParams() {
  const users = await fetchAllUsers();

  return users.map((user) => ({
    id: user.id.toString(),
  }));
}

// Generate metadata
export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const user = await fetchUser(params.id);

  if (!user) {
    return {
      title: 'User Not Found',
    };
  }

  return {
    title: `${user.name} | My App`,
    description: `Profile page for ${user.name}`,
  };
}

export default async function UserPage({ params }: PageProps) {
  const user = await fetchUser(params.id);

  if (!user) {
    notFound();
  }

  return (
    <div>
      <h1>{user.name}</h1>
      <p>Email: {user.email}</p>
    </div>
  );
}

async function fetchUser(id: string) {
  const res = await fetch(`${process.env.API_URL}/users/${id}`, {
    next: { revalidate: 60 },
  });

  if (!res.ok) return null;

  return res.json();
}
```

### API Route

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
});

// GET /api/users
export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const page = Number(searchParams.get('page')) || 1;
  const limit = Number(searchParams.get('limit')) || 10;

  try {
    const users = await db.user.findMany({
      skip: (page - 1) * limit,
      take: limit,
    });

    return NextResponse.json({
      users,
      page,
      limit,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch users' },
      { status: 500 }
    );
  }
}

// POST /api/users
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate
    const validatedData = userSchema.parse(body);

    // Create user
    const user = await db.user.create({
      data: validatedData,
    });

    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: error.errors },
        { status: 400 }
      );
    }

    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    );
  }
}
```

### Loading & Error States

```typescript
// app/users/loading.tsx
export default function Loading() {
  return (
    <div className="container">
      <div className="skeleton">Loading users...</div>
    </div>
  );
}

// app/users/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="error">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// app/users/not-found.tsx
export default function NotFound() {
  return (
    <div>
      <h2>Users Not Found</h2>
      <p>Could not find the requested users page.</p>
    </div>
  );
}
```

## File Structure

```
app/
├── users/
│   ├── page.tsx           # Main page (Server Component)
│   ├── loading.tsx        # Loading state
│   ├── error.tsx          # Error boundary
│   ├── not-found.tsx      # 404 page
│   ├── UserList.tsx       # Client component
│   └── [id]/
│       ├── page.tsx       # Dynamic route
│       ├── loading.tsx
│       └── error.tsx
└── api/
    └── users/
        └── route.ts       # API route
```

## Best Practices

- Use Server Components by default
- Add 'use client' only when needed
- Implement proper loading states
- Handle errors with error boundaries
- Use metadata for SEO
- Implement ISR with revalidate
- Use TypeScript for type safety
- Validate API inputs with Zod
- Use proper status codes
- Implement pagination
- Add search functionality
- Cache API responses

## Output Checklist

- ✅ Page created with proper structure
- ✅ Server/Client components separated
- ✅ Metadata configured
- ✅ Loading states
- ✅ Error handling
- ✅ API routes (if needed)
- ✅ TypeScript types
- 📝 Usage instructions
