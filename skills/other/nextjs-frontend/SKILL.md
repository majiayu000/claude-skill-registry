---
name: nextjs-frontend
description: Frontend development skill for Next.js 14+ with App Router, TypeScript, React 18+, Material UI (primary), and Tailwind CSS (secondary). Use when creating or modifying React components, pages, layouts, hooks, API routes, forms, or state management. Covers Server/Client Components, data fetching, routing, and best practices.
---

# Next.js Frontend Development

## Technology Stack

- **Next.js 14+** - App Router with Server Components
- **TypeScript 5+** - Strict mode enabled
- **React 18+** - Server Components, Suspense, use() hook
- **Material UI 6** - Primary component library
- **Tailwind CSS 4** - Utility-first styling (secondary)
- **React Context** - Client state management
- **Nuqs** - URL state persistence

## Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Route group
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── layout.tsx
│   ├── dashboard/
│   │   ├── page.tsx
│   │   ├── loading.tsx           # Loading UI
│   │   └── error.tsx             # Error boundary
│   ├── api/                      # Route handlers
│   │   └── users/
│   │       └── route.ts
│   ├── layout.tsx                # Root layout
│   └── page.tsx
├── components/
│   ├── ui/                       # MUI-based components
│   │   ├── Button.tsx
│   │   └── index.ts
│   ├── forms/                    # Form components
│   │   └── UserForm.tsx
│   └── layout/                   # Layout components
│       ├── Header.tsx
│       └── Sidebar.tsx
├── hooks/                        # Custom hooks
│   ├── useUser.ts
│   └── useDebounce.ts
├── lib/                          # Utilities
│   ├── api.ts                    # Fetch wrapper
│   └── utils.ts                  # Helper functions
├── types/                        # TypeScript types
│   └── index.ts
└── context/                      # React Context providers
    └── UserContext.tsx
```

## Server vs Client Components

### Decision Guide

| Use Server Component | Use Client Component |
|---------------------|---------------------|
| Data fetching | Event handlers (onClick, etc.) |
| Direct database access | useState, useEffect, useRef |
| Sensitive tokens/keys | Browser-only APIs |
| Large bundles (reduce JS) | Custom hooks with state |
| SEO-critical content | Third-party non-RSC libs |

### Server Component (Default)

```tsx
// app/dashboard/page.tsx (Server Component)
import { Suspense } from 'react';
import { UserList } from '@/components/UserList';
import { UserListSkeleton } from '@/components/UserListSkeleton';

// Async data fetching directly in component
async function getUsers() {
  const res = await fetch('https://api.example.com/users', {
    next: { revalidate: 60 } // Cache for 60 seconds
  });
  if (!res.ok) throw new Error('Failed to fetch users');
  return res.json() as Promise<User[]>;
}

export default async function DashboardPage() {
  return (
    <main>
      <h1>Dashboard</h1>
      <Suspense fallback={<UserListSkeleton />}>
        <UserList />
      </Suspense>
    </main>
  );
}

// components/UserList.tsx (Server Component)
async function UserList() {
  const users = await getUsers();

  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Client Component

```tsx
'use client';

import { useState } from 'react';
import { Button, TextField } from '@mui/material';

interface UserFormProps {
  initialData?: User;
  onSubmit: (data: User) => Promise<void>;
}

export function UserForm({ initialData, onSubmit }: UserFormProps) {
  const [name, setName] = useState(initialData?.name ?? '');
  const [email, setEmail] = useState(initialData?.email ?? '');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmit({ name, email });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <TextField
        label="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button
        type="submit"
        variant="contained"
        loading={isSubmitting}
      >
        Save
      </Button>
    </form>
  );
}
```

## TypeScript Patterns

### Type Definitions

```tsx
// types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: string;
}

export interface ApiResponse<T> {
  data: T;
  meta?: {
    page: number;
    total: number;
    hasMore: boolean;
  };
}

export type Status = 'idle' | 'loading' | 'success' | 'error';

// Component props with generics
export interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}
```

### Strict Component Props

```tsx
import type { ButtonProps as MuiButtonProps } from '@mui/material/Button';

// Extend MUI props
interface CustomButtonProps extends MuiButtonProps {
  loading?: boolean;
  icon?: React.ReactNode;
}

export function Button({
  loading,
  icon,
  children,
  disabled,
  ...props
}: CustomButtonProps) {
  return (
    <MuiButton disabled={disabled || loading} {...props}>
      {loading ? <CircularProgress size={20} /> : icon}
      {children}
    </MuiButton>
  );
}
```

### API Response Typing

```tsx
// lib/api.ts
class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
  }
}

export async function api<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(endpoint, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!res.ok) {
    throw new ApiError(res.status, await res.text());
  }

  return res.json();
}

// Usage
const users = await api<ApiResponse<User[]>>('/api/users');
```

## Material UI + Tailwind

### MUI Theme Configuration

```tsx
// app/theme.ts
import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: '8px',
        },
      },
    },
  },
});
```

### Combined Styling Pattern

```tsx
'use client';

import { Box, Card, Typography } from '@mui/material';
import clsx from 'clsx';

interface FeatureCardProps {
  title: string;
  description: string;
  variant?: 'default' | 'highlighted';
}

export function FeatureCard({
  title,
  description,
  variant = 'default'
}: FeatureCardProps) {
  return (
    <Card
      className={clsx(
        'p-4 transition-shadow hover:shadow-lg',
        variant === 'highlighted' && 'ring-2 ring-primary-500'
      )}
    >
      <Typography variant="h6" className="mb-2 text-gray-900">
        {title}
      </Typography>
      <Typography variant="body2" className="text-gray-600">
        {description}
      </Typography>
    </Card>
  );
}
```

## State Management

### React Context Pattern

```tsx
// context/UserContext.tsx
'use client';

import {
  createContext,
  useContext,
  useOptimistic,
  type ReactNode
} from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserState {
  user: User | null;
  isLoading: boolean;
}

interface UserContextValue extends UserState {
  setUser: (user: User | null) => void;
  updateUser: (updates: Partial<User>) => void;
}

const UserContext = createContext<UserContextValue | null>(null);

export function UserProvider({
  children,
  initialUser
}: {
  children: ReactNode;
  initialUser?: User;
}) {
  const [state, setState] = useOptimistic<UserState>({
    user: initialUser ?? null,
    isLoading: false,
  });

  const setUser = (user: User | null) => {
    setState({ user, isLoading: false });
  };

  const updateUser = (updates: Partial<User>) => {
    if (!state.user) return;
    setState({
      user: { ...state.user, ...updates },
      isLoading: false,
    });
  };

  return (
    <UserContext.Provider value={{ ...state, setUser, updateUser }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}
```

### URL State with Nuqs

```tsx
'use client';

import { useQueryState, parseAsInteger, parseAsString } from 'nuqs';

export function useUserFilters() {
  const [search, setSearch] = useQueryState(
    'search',
    parseAsString.withDefault('')
  );
  const [page, setPage] = useQueryState(
    'page',
    parseAsInteger.withDefault(1)
  );
  const [status, setStatus] = useQueryState(
    'status',
    parseAsString.withDefault('all')
  );

  return {
    filters: { search, page, status },
    setFilters: { setSearch, setPage, setStatus },
    resetFilters: () => {
      setSearch(null);
      setPage(null);
      setStatus(null);
    },
  };
}

// Usage in component
function UserList() {
  const { filters, setFilters } = useUserFilters();

  const { data, isLoading } = useQuery({
    queryKey: ['users', filters],
    queryFn: () => fetchUsers(filters),
  });

  return (
    <div>
      <TextField
        value={filters.search}
        onChange={(e) => setFilters.setSearch(e.target.value || null)}
        placeholder="Search users..."
      />
      {/* ... */}
    </div>
  );
}
```

## Routing Patterns

### Dynamic Routes

```tsx
// app/users/[id]/page.tsx
interface PageProps {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ tab?: string }>;
}

export default async function UserPage({
  params,
  searchParams
}: PageProps) {
  const { id } = await params;
  const { tab } = await searchParams;

  const user = await getUser(id);

  return (
    <div>
      <h1>{user.name}</h1>
      <UserTabs activeTab={tab ?? 'overview'} />
    </div>
  );
}

// Generate static pages for known users
export async function generateStaticParams() {
  const users = await getUsers();
  return users.map((user) => ({ id: user.id }));
}
```

### Loading and Error States

```tsx
// app/dashboard/loading.tsx
import { Skeleton } from '@mui/material';

export default function DashboardLoading() {
  return (
    <div className="space-y-4">
      <Skeleton variant="text" width={200} height={40} />
      <Skeleton variant="rectangular" height={200} />
    </div>
  );
}

// app/dashboard/error.tsx
'use client';

import { Button } from '@mui/material';

export default function DashboardError({
  error,
  reset
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <h2 className="text-xl font-semibold mb-4">Something went wrong!</h2>
      <Button onClick={reset} variant="contained">
        Try again
      </Button>
    </div>
  );
}
```

## Custom Hooks

See [references/hooks.md](references/hooks.md) for detailed hook patterns.

```tsx
// hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

// hooks/useMediaQuery.ts
import { useMediaQuery as useMuiMediaQuery, useTheme } from '@mui/material';

export function useMediaQuery(query: string): boolean {
  const theme = useTheme();
  return useMuiMediaQuery(theme.breakpoints.down(query));
}
```

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Component | PascalCase | `UserCard`, `Navbar` |
| Hook | camelCase with `use` prefix | `useUser`, `useDebounce` |
| Utility | camelCase | `formatDate`, `cn` |
| Type/Interface | PascalCase | `User`, `ApiResponse` |
| File (component) | PascalCase | `UserCard.tsx` |
| File (hook) | camelCase with `use` | `useUser.ts` |
| File (util) | camelCase | `api.ts`, `utils.ts` |
| Folder | camelCase or kebab-case | `components/`, `user-profile/` |

## UI Design Collaboration

When implementing designs from the UI Designer skill:

1. **Receive design specs** - Colors, typography, spacing from MUI theme
2. **Use provided code snippets** - Component code from design specs
3. **Match design tokens** - Use MUI theme values, not hardcoded colors
4. **Implement responsive behavior** - Follow breakpoint guidance from specs

Common handoff artifacts:
- Component code snippets with MUI sx props
- Design specifications with spacing/typography values
- Interactive mockup files for reference

For creating wireframes, mockups, or design specifications, use the **ui-designer** skill.

## References

- **Custom Hooks**: See [references/hooks.md](references/hooks.md) for data fetching, forms, and media hooks
- **Forms**: See [references/forms.md](references/forms.md) for form validation with React Hook Form + Zod
- **Testing**: See [references/testing.md](references/testing.md) for Jest, Testing Library, and E2E patterns
- **UI Design**: Use the `ui-designer` skill for wireframes, mockups, and design specifications
