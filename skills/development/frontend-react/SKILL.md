---
name: frontend-react
description: |
  Modern React stack: React 19, TypeScript, Tailwind CSS, Vite, TanStack Query.
  Use when: building React apps, components, state management, or UI.
  Triggers: "react", "frontend", "tailwind", "vite", "typescript react",
  "component", "useState", "tanstack", "react query".
---

# React Frontend Stack

> **Live docs:** Add `use context7` to prompt for up-to-date React, TanStack Query, Tailwind documentation.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Components | [components.md](references/components.md) — Button, Input, Modal, patterns |
| State | [state.md](references/state.md) — useState, Zustand, Context, URL state |

## Tooling (2025)

| Tool | Purpose | Why |
|------|---------|-----|
| **Vite** | Build tool | Fast HMR, ESM native |
| **React 19** | UI library | RSC, Actions, use() |
| **TypeScript** | Type safety | Strict mode |
| **Tailwind v4** | Styling | Utility-first, Vite plugin |
| **TanStack Query** | Data fetching | Caching, mutations |
| **Zustand** | State | Simple, no boilerplate |
| **React Router 7** | Routing | Data loading, actions |

**Notes:**
- Tailwind v4: new config via Vite plugin, no `tailwind.config.js`
- TanStack Router may require React 18.3.1 (use `--legacy-peer-deps` if needed)

## Project Setup

```bash
pnpm create vite@latest my-app --template react-ts
cd my-app
pnpm add @tanstack/react-query zustand
pnpm add -D tailwindcss @tailwindcss/vite
```

### Vite Config

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { '@': '/src' },
  },
});
```

### Tailwind v4

```css
/* src/index.css */
@import "tailwindcss";
```

## Project Structure

```
src/
├── main.tsx             # Entry point
├── App.tsx              # Root component
├── index.css            # Tailwind imports
├── components/
│   ├── ui/              # Reusable UI (Button, Input, Card)
│   └── features/        # Feature components
├── pages/               # Route components
├── hooks/               # Custom hooks
├── stores/              # Zustand stores
├── api/                 # API client, queries
├── types/               # TypeScript types
└── lib/                 # Utilities
```

## Component Patterns

### Functional Component

```tsx
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
}

export function UserCard({ user, onEdit }: UserCardProps) {
  return (
    <div className="rounded-lg border p-4">
      <h3 className="font-semibold">{user.name}</h3>
      <p className="text-sm text-gray-600">{user.email}</p>
      {onEdit && (
        <button
          onClick={() => onEdit(user.id)}
          className="mt-2 text-blue-600 hover:underline"
        >
          Edit
        </button>
      )}
    </div>
  );
}
```

### Component with Children

```tsx
interface CardProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export function Card({ title, children, className }: CardProps) {
  return (
    <div className={cn("rounded-lg border bg-white p-6", className)}>
      <h2 className="mb-4 text-lg font-semibold">{title}</h2>
      {children}
    </div>
  );
}
```

### Polymorphic Component

```tsx
type ButtonProps<T extends React.ElementType = 'button'> = {
  as?: T;
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
} & React.ComponentPropsWithoutRef<T>;

export function Button<T extends React.ElementType = 'button'>({
  as,
  variant = 'primary',
  children,
  className,
  ...props
}: ButtonProps<T>) {
  const Component = as || 'button';
  return (
    <Component
      className={cn(
        'px-4 py-2 rounded-md font-medium',
        variant === 'primary' && 'bg-blue-600 text-white',
        variant === 'secondary' && 'bg-gray-200 text-gray-800',
        className
      )}
      {...props}
    >
      {children}
    </Component>
  );
}

// Usage
<Button>Click me</Button>
<Button as="a" href="/about">Link</Button>
```

## Hooks

### Custom Hook Example

```tsx
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### useDebounce

```tsx
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
```

## TanStack Query

### Setup

```tsx
// main.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 1,
    },
  },
});

<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

### Query Hook

```tsx
// api/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUser) =>
      fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).then(r => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

### Usage in Component

```tsx
function UserList() {
  const { data: users, isLoading, error } = useUsers();
  const createUser = useCreateUser();

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;

  return (
    <div>
      {users.map(user => <UserCard key={user.id} user={user} />)}
      <button onClick={() => createUser.mutate({ name: 'New' })}>
        Add User
      </button>
    </div>
  );
}
```

## Zustand State

```tsx
// stores/auth.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
    }),
    { name: 'auth-storage' }
  )
);

// Usage
const { user, login, logout } = useAuthStore();
```

## Forms

```tsx
import { useState, FormEvent } from 'react';

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrors({});

    if (!email) {
      setErrors(prev => ({ ...prev, email: 'Required' }));
      return;
    }

    // Submit...
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full rounded border px-3 py-2"
          placeholder="Email"
        />
        {errors.email && <p className="text-sm text-red-500">{errors.email}</p>}
      </div>
      <button type="submit" className="w-full rounded bg-blue-600 py-2 text-white">
        Login
      </button>
    </form>
  );
}
```

## Anti-patterns

| Don't | Do Instead |
|-------|------------|
| CRA (Create React App) | Vite |
| CSS Modules / styled-components | Tailwind |
| Redux (complex) | Zustand (simple) |
| useEffect for data fetching | TanStack Query |
| Prop drilling | Context or Zustand |
| `any` types | Proper TypeScript types |
| Index as key | Unique ID as key |
| Inline object props | useMemo or extract |
