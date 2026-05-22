---
name: tanstack-stack
description: TanStack ecosystem for client-first, real-time applications with type-safe routing and reactive data
agents: [blaze, nova, tap, spark]
context7_libraries:
  - /tanstack/db
  - /tanstack/router
  - /tanstack/query
  - /tanstack/table
  - /tanstack/form
  - /tanstack/virtual
  - /effect-ts/effect
---

# TanStack Stack

Type-safe, high-performance libraries optimized for client-first, real-time applications.

## Core Libraries

| Library | Purpose | Install |
|---------|---------|---------|
| TanStack Router | Type-safe routing with search params | `@tanstack/react-router` |
| TanStack Query | Server-state management & caching | `@tanstack/react-query` |
| TanStack DB | Reactive client store with live queries | `@tanstack/db` |
| TanStack Table | Headless table with sorting/filtering | `@tanstack/react-table` |
| TanStack Form | Type-safe form state management | `@tanstack/react-form` |
| TanStack Virtual | Virtualization for large lists | `@tanstack/react-virtual` |

---

## TanStack DB: Collections & Live Queries

TanStack DB provides sub-millisecond reactive queries over normalized collections.

### Create a Collection

```typescript
import { createCollection } from '@tanstack/db';
import { Schema } from 'effect';

// Define schema with Effect Schema
const UserSchema = Schema.Struct({
  id: Schema.String,
  name: Schema.String,
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/)),
  role: Schema.Literal('admin', 'user', 'guest'),
  createdAt: Schema.Date,
});
type User = Schema.Schema.Type<typeof UserSchema>;

// Create collection with QueryCollection (TanStack Query backend)
export const usersCollection = createCollection({
  id: 'users',
  schema: UserSchema,
  backend: new QueryCollection({
    queryFn: () => fetch('/api/users').then(r => r.json()),
    getId: (user) => user.id,
  }),
});
```

### Live Queries with useLiveQuery

```typescript
import { useLiveQuery } from '@tanstack/db';

function ActiveUsersList() {
  // Live query - re-renders automatically when data changes (~0.7ms for 100k items)
  const activeUsers = useLiveQuery({
    collection: usersCollection,
    query: {
      where: { role: { $ne: 'guest' } },
      orderBy: { createdAt: 'desc' },
      limit: 50,
    },
  });

  return (
    <ul>
      {activeUsers.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Optimistic Mutations

```typescript
import { useMutation } from '@tanstack/db';

function CreateUserButton() {
  const mutation = useMutation({
    collection: usersCollection,
    mutationFn: async (newUser) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        body: JSON.stringify(newUser),
      });
      return response.json();
    },
    // Optimistic update - UI updates immediately
    onMutate: (newUser) => {
      return { ...newUser, id: crypto.randomUUID() };
    },
    // Rollback on error
    onError: (error, newUser, context) => {
      console.error('Failed to create user:', error);
    },
  });

  return (
    <button onClick={() => mutation.mutate({ name: 'New User', email: 'new@example.com', role: 'user' })}>
      Create User
    </button>
  );
}
```

### Sync Modes

```typescript
// Eager sync - load all data upfront
const collection = createCollection({
  backend: new QueryCollection({ ... }),
  syncMode: 'eager',
});

// On-demand sync - fetch when queried
const collection = createCollection({
  backend: new QueryCollection({ ... }),
  syncMode: 'on-demand',
});

// Progressive sync - hybrid approach
const collection = createCollection({
  backend: new QueryCollection({ ... }),
  syncMode: 'progressive',
});
```

---

## TanStack Router: Type-Safe Routing

### File-Based Routes (recommended with Vite plugin)

```typescript
// routes/dashboard.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/dashboard')({
  component: DashboardPage,
  // Type-safe loader
  loader: async () => {
    const stats = await fetchDashboardStats();
    return { stats };
  },
});

function DashboardPage() {
  const { stats } = Route.useLoaderData();
  return <Dashboard stats={stats} />;
}
```

### Search Params with Validation

```typescript
import { createFileRoute } from '@tanstack/react-router';
import { z } from 'zod';

const searchSchema = z.object({
  page: z.number().default(1),
  sort: z.enum(['name', 'date', 'status']).default('date'),
  filter: z.string().optional(),
});

export const Route = createFileRoute('/users')({
  validateSearch: searchSchema,
  component: UsersPage,
});

function UsersPage() {
  const { page, sort, filter } = Route.useSearch();
  const navigate = Route.useNavigate();

  // Type-safe navigation
  const goToPage = (newPage: number) => {
    navigate({ search: { page: newPage, sort, filter } });
  };

  return <UserList page={page} sort={sort} filter={filter} onPageChange={goToPage} />;
}
```

### Nested Layouts

```typescript
// routes/_layout.tsx (layout route)
export const Route = createFileRoute('/_layout')({
  component: LayoutComponent,
});

function LayoutComponent() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}
```

---

## TanStack Table: Data Grids

### Basic Table Setup

```typescript
import { useReactTable, getCoreRowModel, getSortedRowModel, getFilteredRowModel, flexRender } from '@tanstack/react-table';

function UsersTable({ data }: { data: User[] }) {
  const columns = useMemo(() => [
    { accessorKey: 'name', header: 'Name' },
    { accessorKey: 'email', header: 'Email' },
    { 
      accessorKey: 'role', 
      header: 'Role',
      cell: ({ getValue }) => <Badge>{getValue()}</Badge>,
    },
    {
      accessorKey: 'createdAt',
      header: 'Created',
      cell: ({ getValue }) => formatDate(getValue()),
    },
  ], []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(headerGroup => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map(header => (
              <th key={header.id} onClick={header.column.getToggleSortingHandler()}>
                {flexRender(header.column.columnDef.header, header.getContext())}
                {header.column.getIsSorted() && (header.column.getIsSorted() === 'asc' ? ' ↑' : ' ↓')}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### With TanStack DB Live Queries

```typescript
function LiveUsersTable() {
  const users = useLiveQuery({
    collection: usersCollection,
    query: { orderBy: { createdAt: 'desc' } },
  });

  return <UsersTable data={users} />;
}
```

---

## TanStack Form: Type-Safe Forms

```typescript
import { useForm } from '@tanstack/react-form';
import { effectValidator } from '@tanstack/effect-form-adapter';
import { Schema } from 'effect';

const UserSchema = Schema.Struct({
  name: Schema.String.pipe(Schema.minLength(2, { message: () => 'Name must be at least 2 characters' })),
  email: Schema.String.pipe(Schema.pattern(/^[^@]+@[^@]+\.[^@]+$/, { message: () => 'Invalid email address' })),
  role: Schema.Literal('admin', 'user', 'guest'),
});

function CreateUserForm() {
  const form = useForm({
    defaultValues: { name: '', email: '', role: 'user' as const },
    validatorAdapter: effectValidator(),
    validators: {
      onChange: UserSchema,
    },
    onSubmit: async ({ value }) => {
      await createUser(value);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    form.handleSubmit();
  };

  return (
    <form onSubmit={handleSubmit}>
      <form.Field name="name">
        {(field) => (
          <div>
            <label>Name</label>
            <input
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.errors && <span className="error">{field.state.meta.errors}</span>}
          </div>
        )}
      </form.Field>

      <form.Field name="email">
        {(field) => (
          <div>
            <label>Email</label>
            <input
              type="email"
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              onBlur={field.handleBlur}
            />
            {field.state.meta.errors && <span className="error">{field.state.meta.errors}</span>}
          </div>
        )}
      </form.Field>

      <form.Field name="role">
        {(field) => (
          <div>
            <label>Role</label>
            <select value={field.state.value} onChange={(e) => field.handleChange(e.target.value as any)}>
              <option value="user">User</option>
              <option value="admin">Admin</option>
              <option value="guest">Guest</option>
            </select>
          </div>
        )}
      </form.Field>

      <button type="submit" disabled={form.state.isSubmitting}>
        {form.state.isSubmitting ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

---

## TanStack Virtual: Large Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualizedList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Estimated row height
    overscan: 5, // Render 5 extra items above/below viewport
  });

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`,
            }}
          >
            {items[virtualRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Project Setup

### Vite + TanStack Router

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install @tanstack/react-router @tanstack/react-query @tanstack/db @tanstack/react-table @tanstack/react-form @tanstack/zod-form-adapter @tanstack/react-virtual zod
npm install -D @tanstack/router-plugin
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { TanStackRouterVite } from '@tanstack/router-plugin/vite';

export default defineConfig({
  plugins: [
    TanStackRouterVite(),
    react(),
  ],
});
```

---

## TanStack Start (Full-Stack Option)

For greenfield projects, TanStack Start provides a full-stack framework:

```bash
npm create @tanstack/start@latest
```

Start includes:
- File-based routing with TanStack Router
- Server functions (like Server Actions)
- SSR/SSG capabilities
- Built-in TanStack Query integration
- Vite-powered development

---

## Best Practices

1. **Use collections for all server data** - Normalize at the collection level
2. **Leverage live queries** - Let TanStack DB handle reactivity, don't poll
3. **Optimistic by default** - Use onMutate for instant UI feedback
4. **Type everything** - Use Effect Schema for runtime + TypeScript validation
5. **Virtualize large lists** - TanStack Virtual for 1000+ items
6. **Search params as state** - Use TanStack Router search params for shareable UI state
7. **Co-locate loaders** - Keep data fetching close to route components

## Documentation

- https://tanstack.com/db/latest
- https://tanstack.com/router/latest
- https://tanstack.com/query/latest
- https://tanstack.com/table/latest
- https://tanstack.com/form/latest
- https://tanstack.com/virtual/latest
- https://effect.website/docs
