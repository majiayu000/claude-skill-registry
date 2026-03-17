---
name: shadcn-stack
description: Next.js 15 + shadcn/ui + Server Components patterns for server-rendered React applications
agents: [blaze, nova, tap, spark]
context7_libraries:
  - /vercel/next.js
  - /shadcn-ui/ui
  - /tanstack/query
  - /react-hook-form/react-hook-form
  - /effect-ts/effect
llm_docs:
  - shadcn
  - tanstack
  - effect
---

# shadcn Stack

Modern Next.js architecture optimized for server-side rendering, SEO, and progressive enhancement.

## Core Technologies

| Library | Purpose | Install |
|---------|---------|---------|
| Next.js 15 | Full-stack React framework | `next` |
| shadcn/ui | Accessible UI components | `npx shadcn@latest add [component]` |
| React Query | Client-side data caching | `@tanstack/react-query` |
| React Hook Form | Form state management | `react-hook-form` |
| Effect | Type-safe validation & errors | `effect`, `@hookform/resolvers` |
| Tailwind CSS | Utility-first styling | `tailwindcss` |

---

## Next.js App Router Patterns

### File-Based Routing

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page (/)
├── loading.tsx         # Loading UI
├── error.tsx           # Error boundary
├── dashboard/
│   ├── layout.tsx      # Dashboard layout
│   ├── page.tsx        # /dashboard
│   └── settings/
│       └── page.tsx    # /dashboard/settings
└── api/
    └── users/
        └── route.ts    # API route
```

### Server Components (Default)

```typescript
// app/users/page.tsx - Server Component by default
import { getUsers } from '@/lib/db';

export default async function UsersPage() {
  const users = await getUsers(); // Direct database access

  return (
    <div>
      <h1>Users</h1>
      <UserList users={users} />
    </div>
  );
}
```

### Client Components

```typescript
// components/user-search.tsx
'use client';

import { useState } from 'react';
import { Input } from '@/components/ui/input';

export function UserSearch({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
    onSearch(e.target.value);
  };

  return (
    <Input
      value={query}
      onChange={handleChange}
      placeholder="Search users..."
    />
  );
}
```

---

## Server Actions

### Define Server Actions

```typescript
// app/actions/users.ts
'use server';

import { revalidatePath } from 'next/cache';
import { Schema, Effect } from 'effect';
import { db } from '@/lib/db';

const CreateUserSchema = Schema.Struct({
  name: Schema.String.pipe(Schema.minLength(2)),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  role: Schema.Literal('admin', 'user', 'guest'),
});

export async function createUser(formData: FormData) {
  const validated = Schema.decodeUnknownSync(CreateUserSchema)({
    name: formData.get('name'),
    email: formData.get('email'),
    role: formData.get('role'),
  });

  await db.user.create({ data: validated });
  revalidatePath('/users');
}

export async function deleteUser(id: string) {
  await db.user.delete({ where: { id } });
  revalidatePath('/users');
}
```

### Use in Components

```typescript
// app/users/create/page.tsx
import { createUser } from '@/app/actions/users';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function CreateUserPage() {
  return (
    <form action={createUser}>
      <Input name="name" placeholder="Name" required />
      <Input name="email" type="email" placeholder="Email" required />
      <select name="role">
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <Button type="submit">Create User</Button>
    </form>
  );
}
```

### With useFormStatus for Loading States

```typescript
'use client';

import { useFormStatus } from 'react-dom';
import { Button } from '@/components/ui/button';

function SubmitButton() {
  const { pending } = useFormStatus();
  
  return (
    <Button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create User'}
    </Button>
  );
}
```

---

## shadcn/ui Components

### Installation

```bash
npx shadcn@latest init
npx shadcn@latest add button card input form table dialog
```

### Component Usage

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function UserCard({ user }: { user: User }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{user.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{user.email}</p>
      </CardContent>
      <CardFooter>
        <Button variant="outline">Edit</Button>
        <Button variant="destructive">Delete</Button>
      </CardFooter>
    </Card>
  );
}
```

### Dialog Pattern

```typescript
'use client';

import { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export function CreateUserDialog() {
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Create User</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New User</DialogTitle>
          <DialogDescription>
            Add a new user to the system.
          </DialogDescription>
        </DialogHeader>
        <CreateUserForm onSuccess={() => setOpen(false)} />
      </DialogContent>
    </Dialog>
  );
}
```

---

## React Hook Form + Effect Schema

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { effectTsResolver } from '@hookform/resolvers/effect-ts';
import { Schema } from 'effect';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';

const formSchema = Schema.Struct({
  name: Schema.String.pipe(Schema.minLength(2, { message: () => 'Name must be at least 2 characters' })),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/, { message: () => 'Invalid email address' })),
});

type FormValues = Schema.Schema.Type<typeof formSchema>;

export function CreateUserForm({ onSuccess }: { onSuccess: () => void }) {
  const form = useForm<FormValues>({
    resolver: effectTsResolver(formSchema),
    defaultValues: { name: '', email: '' },
  });

  async function onSubmit(values: FormValues) {
    const response = await fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(values),
    });
    if (response.ok) {
      onSuccess();
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="john@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Creating...' : 'Create'}
        </Button>
      </form>
    </Form>
  );
}
```

---

## React Query for Client-Side Data

```typescript
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      return response.json();
    },
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (newUser: CreateUserInput) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Query Provider Setup

```typescript
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## shadcn Table with Server Data

```typescript
// app/users/page.tsx
import { getUsers } from '@/lib/db';
import { UsersTable } from './users-table';

export default async function UsersPage() {
  const users = await getUsers();
  return <UsersTable data={users} />;
}

// app/users/users-table.tsx
'use client';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { deleteUser } from '@/app/actions/users';

export function UsersTable({ data }: { data: User[] }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Role</TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {data.map((user) => (
          <TableRow key={user.id}>
            <TableCell>{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
            <TableCell>
              <Badge variant={user.role === 'admin' ? 'default' : 'secondary'}>
                {user.role}
              </Badge>
            </TableCell>
            <TableCell>
              <form action={deleteUser.bind(null, user.id)}>
                <Button variant="destructive" size="sm" type="submit">
                  Delete
                </Button>
              </form>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
```

---

## Loading & Error States

### Loading UI

```typescript
// app/users/loading.tsx
import { Skeleton } from '@/components/ui/skeleton';

export default function Loading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-64 w-full" />
    </div>
  );
}
```

### Error Boundary

```typescript
// app/users/error.tsx
'use client';

import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center gap-4 py-16">
      <h2 className="text-xl font-semibold">Something went wrong!</h2>
      <p className="text-muted-foreground">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```

---

## SEO & Metadata

```typescript
// app/users/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Users | My App',
  description: 'Manage users in the system',
  openGraph: {
    title: 'Users',
    description: 'Manage users in the system',
  },
};

export default async function UsersPage() {
  // ...
}
```

### Dynamic Metadata

```typescript
// app/users/[id]/page.tsx
import { Metadata } from 'next';
import { getUser } from '@/lib/db';

type Props = { params: Promise<{ id: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { id } = await params;
  const user = await getUser(id);

  return {
    title: `${user.name} | My App`,
    description: `Profile for ${user.name}`,
  };
}
```

---

## Best Practices

1. **Server Components by default** - Only add 'use client' when needed
2. **Server Actions for mutations** - Avoid API routes for form submissions
3. **Co-locate components** - Keep page-specific components in route folders
4. **Use shadcn primitives** - Build on top of existing components
5. **Effect Schema everywhere** - Validate on both client and server
6. **Streaming with Suspense** - Wrap slow components for progressive loading
7. **Revalidate strategically** - Use revalidatePath/revalidateTag after mutations

## Documentation

- https://nextjs.org/docs
- https://ui.shadcn.com
- https://effect.website/docs
- https://react-hook-form.com
- https://tanstack.com/query/latest
