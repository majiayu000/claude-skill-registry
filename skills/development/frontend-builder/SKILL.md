---
name: Frontend Builder
description: Build modern React/Next.js frontends. Use when creating web applications, choosing frontend stack, structuring components, or implementing UI/UX designs. Covers React, Next.js, Tailwind CSS, and component patterns.
version: 1.0.0
---

# Frontend Builder

Build maintainable, performant React and Next.js frontends.

## Core Principles

### 1. Component Composition

Break UI into small, reusable, single-purpose components

### 2. State Proximity

Keep state as close to where it's used as possible

### 3. Performance by Default

Optimize rendering, code splitting, and asset loading

### 4. Developer Experience

Clear naming, consistent patterns, helpful errors

## Framework Selection

### React (Vite) vs. Next.js

**Use React + Vite when**:

- Client-side only application
- No SEO requirements
- Simple deployment (static hosting)
- Faster initial setup

**Use Next.js when**:

- SEO important (marketing sites, blogs, e-commerce)
- Server-side rendering needed
- API routes required
- File-based routing preferred
- Image optimization critical

**Recommended for most projects**: Next.js (App Router)

---

## Component Architecture

### Component Types

**1. Page Components** (Route entry points):

```typescript
// app/users/page.tsx (Next.js App Router)
export default function UsersPage() {
  return (
    <div>
      <Header />
      <UserList />
      <Footer />
    </div>
  )
}
```

**2. Feature Components** (Business logic):

```typescript
// components/features/UserList.tsx
export function UserList() {
  const { data, isLoading } = useUsers()

  if (isLoading) return <LoadingSpinner />

  return (
    <div>
      {data.map(user => <UserCard key={user.id} user={user} />)}
    </div>
  )
}
```

**3. UI Components** (Reusable, no business logic):

```typescript
// components/ui/button.tsx
export function Button({ children, variant = 'primary', ...props }) {
  return (
    <button
      className={cn(buttonVariants[variant])}
      {...props}
    >
      {children}
    </button>
  )
}
```

### Component Best Practices

```typescript
// ✅ Good: Small, focused, typed
interface UserProfileProps {
  user: User
  onEdit?: () => void
}

export function UserProfile({ user, onEdit }: UserProfileProps) {
  return (
    <div className="flex gap-4">
      <Avatar src={user.avatar} alt={user.name} />
      <UserDetails user={user} />
      {onEdit && <Button onClick={onEdit}>Edit</Button>}
    </div>
  )
}

// ❌ Bad: Giant, untyped, unclear
export function UserProfile(props) {
  // 500 lines of JSX, multiple responsibilities
  return <div>...</div>
}
```

---

## State Management

### Decision Tree

```
How many components need this state?
│
├─ One component → useState
├─ Parent + children → Props or useState + props
├─ Siblings → Lift to common parent
├─ Widely used (theme, auth) → Context API
└─ Complex app state → Zustand or Redux
```

### Local State (useState)

```typescript
// For component-level state
function Counter() {
  const [count, setCount] = useState(0)
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>{count}</button>
    </div>
  )
}
```

### Context API

```typescript
// For app-wide state (theme, auth, user)
const UserContext = createContext<UserContextType | undefined>(undefined)

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  )
}

export function useUser() {
  const context = useContext(UserContext)
  if (!context) throw new Error('useUser must be within UserProvider')
  return context
}
```

### Zustand (Recommended for Complex State)

```typescript
import { create } from 'zustand'

interface CounterStore {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

export const useCounterStore = create<CounterStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 })
}))

// Usage
function Counter() {
  const { count, increment } = useCounterStore()
  return <button onClick={increment}>{count}</button>
}
```

---

## Data Fetching

### React Query (Recommended)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Query (GET)
function Users() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
    staleTime: 5 * 60 * 1000 // 5 minutes
  })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage error={error} />

  return <UserList users={data} />
}

// Mutation (POST, PUT, DELETE)
function CreateUser() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    }
  })

  return (
    <button onClick={() => mutation.mutate({ name: 'John' })}>
      Create User
    </button>
  )
}
```

### Next.js Server Components (App Router)

```typescript
// app/users/page.tsx
// Server Component - fetches on server
export default async function UsersPage() {
  const users = await fetchUsers() // Runs on server

  return <UserList users={users} />
}

// Client Component - for interactivity
'use client'

export function UserList({ users }: { users: User[] }) {
  const [selected, setSelected] = useState<string | null>(null)

  return (
    <div>
      {users.map(user => (
        <UserCard
          key={user.id}
          user={user}
          onClick={() => setSelected(user.id)}
        />
      ))}
    </div>
  )
}
```

---

## Form Handling

### React Hook Form (Recommended)

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters')
})

type LoginForm = z.infer<typeof loginSchema>

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema)
  })

  const onSubmit = async (data: LoginForm) => {
    await login(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <input
          {...register('email')}
          type="email"
          placeholder="Email"
          className="border p-2"
        />
        {errors.email && (
          <span className="text-red-500">{errors.email.message}</span>
        )}
      </div>

      <div>
        <input
          {...register('password')}
          type="password"
          placeholder="Password"
          className="border p-2"
        />
        {errors.password && (
          <span className="text-red-500">{errors.password.message}</span>
        )}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

---

## Styling

### Tailwind CSS (Recommended)

```typescript
// Install: @shadcn/ui for component library
function Button({ variant = 'primary', children, ...props }) {
  return (
    <button
      className={cn(
        'px-4 py-2 rounded font-medium transition-colors',
        {
          'bg-blue-500 text-white hover:bg-blue-600': variant === 'primary',
          'bg-gray-200 text-gray-900 hover:bg-gray-300': variant === 'secondary',
          'bg-red-500 text-white hover:bg-red-600': variant === 'danger'
        }
      )}
      {...props}
    >
      {children}
    </button>
  )
}
```

### CSS Modules (Alternative)

```typescript
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
}

.primary {
  background-color: blue;
  color: white;
}

// Button.tsx
import styles from './Button.module.css'

export function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  )
}
```

---

## Performance Optimization

### React Optimization

```typescript
import { memo, useMemo, useCallback } from 'react'

// 1. Memoize expensive calculations
function DataTable({ data }) {
  const sortedData = useMemo(
    () => data.sort((a, b) => a.name.localeCompare(b.name)),
    [data]
  )

  return <Table data={sortedData} />
}

// 2. Memoize callbacks
function Parent() {
  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])

  return <ExpensiveChild onClick={handleClick} />
}

// 3. Memoize components
const ExpensiveChild = memo(function ExpensiveChild({ onClick }) {
  return <button onClick={onClick}>Click</button>
})
```

### Next.js Optimization

```typescript
// 1. Image optimization
import Image from 'next/image'

<Image
  src="/photo.jpg"
  alt="Photo"
  width={500}
  height={300}
  priority // Above the fold
/>

// 2. Font optimization
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return (
    <html className={inter.className}>
      <body>{children}</body>
    </html>
  )
}

// 3. Dynamic imports (code splitting)
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <LoadingSpinner />
})
```

---

## Error Handling

### Error Boundary

```typescript
'use client'

import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-50 border border-red-200">
          <h2 className="text-red-800">Something went wrong</h2>
          <p className="text-red-600">{this.state.error?.message}</p>
        </div>
      )
    }

    return this.props.children
  }
}
```

### Next.js Error Handling

```typescript
// app/error.tsx
'use client'

export default function Error({
  error,
  reset
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

---

## Folder Structure

### Next.js App Router

```
app/
├── (auth)/              # Route group (auth pages)
│   ├── login/
│   └── signup/
├── (dashboard)/         # Route group (dashboard)
│   ├── layout.tsx
│   ├── page.tsx
│   └── settings/
├── api/                 # API routes
│   └── users/
│       └── route.ts
└── layout.tsx           # Root layout

components/
├── ui/                  # shadcn/ui components
│   ├── button.tsx
│   ├── input.tsx
│   └── dialog.tsx
├── features/            # Feature components
│   ├── UserList.tsx
│   └── UserProfile.tsx
└── layouts/             # Layout components
    ├── Header.tsx
    └── Footer.tsx

lib/
├── utils.ts             # Utility functions
├── api.ts               # API client
└── validation.ts        # Zod schemas

hooks/
├── useUser.ts
└── useDebounce.ts

stores/
└── userStore.ts         # Zustand stores
```

---

## TypeScript Best Practices

```typescript
// 1. Type component props
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  children: ReactNode
  onClick?: () => void
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return <button onClick={onClick}>{children}</button>
}

// 2. Type API responses
interface User {
  id: string
  name: string
  email: string
}

async function fetchUsers(): Promise<User[]> {
  const res = await fetch('/api/users')
  return res.json()
}

// 3. Type state
const [user, setUser] = useState<User | null>(null)
const [isLoading, setIsLoading] = useState<boolean>(false)
```

---

## Summary

Great frontends:

- ✅ Use Next.js for most projects (SEO, performance, DX)
- ✅ Break UI into small, typed components
- ✅ Choose appropriate state management (useState → Context → Zustand)
- ✅ Use React Query for server state
- ✅ Style with Tailwind CSS + shadcn/ui
- ✅ Optimize with memoization and code splitting
- ✅ Handle errors gracefully with Error Boundaries
- ✅ Follow consistent folder structure

---

## Related Resources

**Related Skills**:

- `api-designer` - For designing backend APIs to consume
- `ux-designer` - For creating UX designs to implement
- `deployment-advisor` - For hosting Next.js/React apps

**Related Patterns**:

- `META/DECISION-FRAMEWORK.md` - Frontend framework selection
- `STANDARDS/architecture-patterns/component-patterns.md` - Component design patterns (when created)

**Related Playbooks**:

- `PLAYBOOKS/setup-nextjs-project.md` - Next.js project setup (when created)
- `PLAYBOOKS/optimize-frontend-performance.md` - Performance optimization (when created)
