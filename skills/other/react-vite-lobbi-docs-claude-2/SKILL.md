---
name: react-vite
description: React 18+ patterns with Vite bundler, TypeScript, hooks, component design, and state management. Activate for React apps, Vite configuration, TypeScript, frontend development, and modern React patterns.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# React Vite Skill

Provides comprehensive React 18+ development with Vite bundler, TypeScript integration, and modern frontend patterns.

## When to Use This Skill

Activate this skill when working with:
- React 18+ applications with Vite
- TypeScript component development
- React hooks and custom hooks
- State management (Context, Zustand, React Query)
- Component composition and patterns
- Vite configuration and optimization
- Build optimization and deployment

## Quick Reference

### Project Setup
```bash
# Create new Vite + React + TypeScript project
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Install common dependencies
npm install @tanstack/react-query zustand react-hook-form zod
npm install -D @types/node

# Development
npm run dev

# Build
npm run build
npm run preview

# Lint
npm run lint
```

## Project Structure

```
src/
├── main.tsx              # Application entry point
├── App.tsx              # Root component
├── vite-env.d.ts        # Vite TypeScript definitions
├── components/          # Reusable components
│   ├── ui/             # Base UI components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Input.tsx
│   └── features/       # Feature-specific components
│       ├── UserList.tsx
│       └── Dashboard.tsx
├── hooks/              # Custom hooks
│   ├── useAuth.ts
│   ├── useApi.ts
│   └── useLocalStorage.ts
├── stores/            # State management
│   ├── authStore.ts
│   └── userStore.ts
├── services/          # API and external services
│   ├── api.ts
│   └── auth.ts
├── types/            # TypeScript types
│   ├── index.ts
│   └── api.ts
├── utils/           # Utility functions
│   └── helpers.ts
└── styles/         # Global styles
    └── index.css
```

## Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],

  // Path aliases
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@stores': path.resolve(__dirname, './src/stores'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },

  // Server configuration
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },

  // Build optimization
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['@tanstack/react-query', 'zustand'],
        },
      },
    },
    sourcemap: true,
    minify: 'terser',
  },
})
```

## TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@hooks/*": ["./src/hooks/*"],
      "@stores/*": ["./src/stores/*"],
      "@types/*": ["./src/types/*"],
      "@utils/*": ["./src/utils/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Component Patterns

### Functional Component with TypeScript
```typescript
import { FC, ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: () => void
}

export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

### Component with Generic Types
```typescript
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => ReactNode
  keyExtractor: (item: T) => string | number
}

export function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item) => (
        <li key={keyExtractor(item)}>{renderItem(item)}</li>
      ))}
    </ul>
  )
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  keyExtractor={(user) => user.id}
/>
```

## Custom Hooks

### useLocalStorage Hook
```typescript
import { useState, useEffect } from 'react'

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T) => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.error(error)
      return initialValue
    }
  })

  const setValue = (value: T) => {
    try {
      setStoredValue(value)
      window.localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error(error)
    }
  }

  return [storedValue, setValue]
}
```

### useDebounce Hook
```typescript
import { useState, useEffect } from 'react'

export function useDebounce<T>(value: T, delay: number = 500): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => {
      clearTimeout(handler)
    }
  }, [value, delay])

  return debouncedValue
}
```

### useAsync Hook
```typescript
import { useState, useEffect, useCallback } from 'react'

interface AsyncState<T> {
  data: T | null
  loading: boolean
  error: Error | null
}

export function useAsync<T>(
  asyncFunction: () => Promise<T>,
  immediate = true
) {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    loading: immediate,
    error: null,
  })

  const execute = useCallback(async () => {
    setState({ data: null, loading: true, error: null })
    try {
      const response = await asyncFunction()
      setState({ data: response, loading: false, error: null })
    } catch (error) {
      setState({ data: null, loading: false, error: error as Error })
    }
  }, [asyncFunction])

  useEffect(() => {
    if (immediate) {
      execute()
    }
  }, [execute, immediate])

  return { ...state, execute }
}
```

## State Management with Zustand

```typescript
// stores/authStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  name: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: (user, token) =>
        set({ user, token, isAuthenticated: true }),

      logout: () =>
        set({ user: null, token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
)

// Usage in component
function Profile() {
  const { user, logout } = useAuthStore()

  return (
    <div>
      <h1>{user?.name}</h1>
      <button onClick={logout}>Logout</button>
    </div>
  )
}
```

## Data Fetching with React Query

```typescript
// services/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface User {
  id: number
  name: string
  email: string
}

export const userApi = {
  getAll: () => api.get<User[]>('/users').then((res) => res.data),
  getById: (id: number) => api.get<User>(`/users/${id}`).then((res) => res.data),
  create: (data: Omit<User, 'id'>) => api.post<User>('/users', data).then((res) => res.data),
  update: (id: number, data: Partial<User>) => api.patch<User>(`/users/${id}`, data).then((res) => res.data),
  delete: (id: number) => api.delete(`/users/${id}`),
}

// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { userApi, User } from '@/services/api'

export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: userApi.getAll,
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useUser(id: number) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: () => userApi.getById(id),
    enabled: !!id,
  })
}

export function useCreateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: userApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<User> }) =>
      userApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
      queryClient.invalidateQueries({ queryKey: ['users', variables.id] })
    },
  })
}
```

## Form Handling with React Hook Form

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const userSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
  age: z.number().min(18, 'Must be at least 18'),
})

type UserFormData = z.infer<typeof userSchema>

export function UserForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: {
      name: '',
      email: '',
      age: 18,
    },
  })

  const { mutate: createUser } = useCreateUser()

  const onSubmit = (data: UserFormData) => {
    createUser(data, {
      onSuccess: () => {
        reset()
      },
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input {...register('name')} id="name" />
        {errors.name && <span>{errors.name.message}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input {...register('email')} type="email" id="email" />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="age">Age</label>
        <input {...register('age', { valueAsNumber: true })} type="number" id="age" />
        {errors.age && <span>{errors.age.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating...' : 'Create User'}
      </button>
    </form>
  )
}
```

## Performance Optimization

### Code Splitting with Lazy Loading
```typescript
import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Users = lazy(() => import('./pages/Users'))
const Settings = lazy(() => import('./pages/Settings'))

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/users" element={<Users />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
```

### Memoization
```typescript
import { memo, useMemo, useCallback } from 'react'

interface UserListProps {
  users: User[]
  onUserClick: (id: number) => void
}

export const UserList = memo<UserListProps>(({ users, onUserClick }) => {
  const sortedUsers = useMemo(
    () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  )

  const handleClick = useCallback(
    (id: number) => {
      console.log('Clicked user:', id)
      onUserClick(id)
    },
    [onUserClick]
  )

  return (
    <ul>
      {sortedUsers.map((user) => (
        <li key={user.id} onClick={() => handleClick(user.id)}>
          {user.name}
        </li>
      ))}
    </ul>
  )
})
```

## Environment Variables

```bash
# .env
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Zenith
VITE_ENABLE_ANALYTICS=true
```

```typescript
// Access in code
const apiUrl = import.meta.env.VITE_API_URL
const appName = import.meta.env.VITE_APP_NAME
const isDev = import.meta.env.DEV
const isProd = import.meta.env.PROD
```

## Testing Setup

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})

// src/test/setup.ts
import { expect, afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'
import * as matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

afterEach(() => {
  cleanup()
})
```

## Best Practices

1. **TypeScript**: Use strict mode and avoid `any` types
2. **Component Structure**: Keep components small and focused
3. **Custom Hooks**: Extract reusable logic into custom hooks
4. **State Management**: Use appropriate tools (Context for simple, Zustand/Redux for complex)
5. **Data Fetching**: Use React Query for server state management
6. **Forms**: Leverage React Hook Form with Zod validation
7. **Performance**: Use `memo`, `useMemo`, `useCallback` judiciously
8. **Code Splitting**: Implement lazy loading for routes and heavy components
9. **Error Boundaries**: Implement error boundaries for graceful error handling
10. **Accessibility**: Use semantic HTML and ARIA attributes

## Build and Deployment

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Analyze bundle size
npm run build -- --mode analyze

# Type checking
npx tsc --noEmit
```

## Vite Plugins

```bash
# Common Vite plugins
npm install -D vite-plugin-pwa
npm install -D vite-plugin-compression
npm install -D @vitejs/plugin-react-swc  # Faster than default
```
