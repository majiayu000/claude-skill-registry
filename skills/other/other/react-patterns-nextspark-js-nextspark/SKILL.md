---
name: react-patterns
description: |
  Modern React patterns for this Next.js 15 application.
  Covers Server/Client Components, Context API, TanStack Query, Suspense, Error Boundaries, and performance patterns.
  Use this skill when implementing React components or understanding component architecture.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# React Patterns Skill

Patterns for working with React 19 and Next.js 15 App Router in this application.

## Architecture Overview

```
REACT COMPONENT ARCHITECTURE:

Server Components (Default):
├── app/layout.tsx           # Root layout with providers
├── app/page.tsx             # Pages (default server)
└── app/dashboard/layout.tsx # Nested layouts

Client Components ('use client'):
├── core/components/         # Interactive UI components
├── core/contexts/           # React Context providers
├── core/hooks/              # Custom hooks
└── core/providers/          # Provider wrappers

Data Fetching Strategy:
├── TanStack Query           # Client-side data fetching
├── Server Actions           # Server mutations
└── Route Handlers           # API endpoints
```

## When to Use This Skill

- Deciding between Server and Client Components
- Implementing Context API patterns
- Using TanStack Query for data fetching
- Adding Suspense boundaries
- Implementing error handling
- Performance optimization with useCallback/useMemo

## Server Components vs Client Components

### Server Components (Default)

All components in the `app/` directory are Server Components by default.

```typescript
// app/layout.tsx - Server Component
export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Can use async/await directly
  const locale = await getUserLocale()
  const messages = await getMessages({ locale })
  const defaultTheme = await getDefaultThemeMode()

  return (
    <html lang={locale} suppressHydrationWarning>
      <body>
        {/* Wrap client components in providers */}
        <NextIntlClientProvider messages={messages}>
          <NextThemeProvider defaultTheme={defaultTheme}>
            <QueryProvider>
              <TeamProvider>
                {children}
              </TeamProvider>
            </QueryProvider>
          </NextThemeProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  )
}
```

**When to use Server Components:**
- Fetching data from database
- Accessing backend resources
- Keeping sensitive data on server
- Reducing client JavaScript bundle
- Pages that don't need interactivity

### Client Components

Mark with `'use client'` directive at the top of the file.

```typescript
'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/core/hooks/useAuth'

export function LoginForm() {
  const [error, setError] = useState<string | null>(null)
  const { signIn } = useAuth()
  const router = useRouter()

  const handleSubmit = useCallback(async (data: LoginData) => {
    try {
      await signIn(data)
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed')
    }
  }, [signIn, router])

  return (
    <form onSubmit={handleSubmit}>
      {/* Form content */}
    </form>
  )
}
```

**When to use Client Components:**
- Using React hooks (useState, useEffect, etc.)
- Adding event listeners (onClick, onChange, etc.)
- Using browser APIs
- Using third-party libraries that use hooks
- Components that need interactivity

## Context API Pattern

### Creating Context with Custom Hook

```typescript
// core/contexts/TeamContext.tsx
'use client'

import { createContext, useContext, useState, useCallback, ReactNode } from 'react'

interface TeamContextValue {
  currentTeam: Team | null
  userTeams: UserTeamMembership[]
  isLoading: boolean
  switchTeam: (teamId: string) => Promise<void>
  refreshTeams: () => Promise<void>
}

const TeamContext = createContext<TeamContextValue | undefined>(undefined)

export function TeamProvider({ children }: { children: ReactNode }) {
  const [currentTeam, setCurrentTeam] = useState<Team | null>(null)
  const [userTeams, setUserTeams] = useState<UserTeamMembership[]>([])
  const [isLoading, setIsLoading] = useState(true)

  const switchTeam = useCallback(async (teamId: string) => {
    // Implementation
  }, [])

  const refreshTeams = useCallback(async () => {
    // Implementation
  }, [])

  return (
    <TeamContext.Provider value={{
      currentTeam,
      userTeams,
      isLoading,
      switchTeam,
      refreshTeams,
    }}>
      {children}
    </TeamContext.Provider>
  )
}

// Custom hook with error boundary
export function useTeamContext() {
  const context = useContext(TeamContext)
  if (context === undefined) {
    throw new Error('useTeamContext must be used within TeamProvider')
  }
  return context
}
```

### Provider Nesting Pattern

```typescript
// app/layout.tsx
<NextIntlClientProvider messages={messages}>
  <NextThemeProvider>
    <QueryProvider>
      <TeamProvider>
        <SubscriptionProvider>
          {children}
        </SubscriptionProvider>
      </TeamProvider>
    </QueryProvider>
  </NextThemeProvider>
</NextIntlClientProvider>
```

**Order matters:** Providers that depend on others must be nested inside them.

## TanStack Query for Data Fetching

### Provider Setup

```typescript
// core/providers/query-provider.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { useState } from 'react'

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () => new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 60 * 1000,        // 1 minute
          refetchOnWindowFocus: false,
        },
      },
    })
  )

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NEXT_PUBLIC_RQ_DEVTOOLS === 'true' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  )
}
```

### Query Pattern

```typescript
// ✅ CORRECT - Use TanStack Query for data fetching
import { useQuery } from '@tanstack/react-query'

function CustomerList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['customers'],
    queryFn: () => fetch('/api/v1/customers').then(res => res.json()),
  })

  if (isLoading) return <Skeleton />
  if (error) return <ErrorMessage error={error} />

  return <DataTable data={data} />
}

// ❌ WRONG - Don't use useEffect for data fetching
function CustomerList() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/v1/customers')
      .then(res => res.json())
      .then(setData)
      .finally(() => setLoading(false))
  }, [])
}
```

### Mutation Pattern

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function CreateCustomerForm() {
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: CreateCustomer) =>
      fetch('/api/v1/customers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      }).then(res => res.json()),
    onSuccess: () => {
      // Invalidate queries to refetch
      queryClient.invalidateQueries({ queryKey: ['customers'] })
    },
  })

  return (
    <form onSubmit={(e) => {
      e.preventDefault()
      mutation.mutate(formData)
    }}>
      {/* Form fields */}
    </form>
  )
}
```

## Suspense Boundaries

### Basic Usage

```typescript
import { Suspense } from 'react'

function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Suspense fallback={<NavSkeleton />}>
        <Navigation />
      </Suspense>

      <main>
        <Suspense fallback={<ContentSkeleton />}>
          {children}
        </Suspense>
      </main>
    </div>
  )
}
```

### With Async Components

```typescript
// app/dashboard/layout.tsx
'use client'

import { Suspense } from 'react'

function AuthMethodDetectorWrapper() {
  useAuthMethodDetector()  // Hook that reads URL params
  return null
}

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {/* Wrap async detection in Suspense */}
      <Suspense fallback={null}>
        <AuthMethodDetectorWrapper />
      </Suspense>

      <div data-cy="dashboard-container">
        {children}
      </div>
    </>
  )
}
```

### Block Renderer with Suspense

```typescript
// app/components/page-renderer.tsx
import { Suspense } from 'react'

function BlockSkeleton() {
  return (
    <div className="w-full py-12 px-4 animate-pulse">
      <div className="h-8 bg-muted rounded w-1/3 mb-4" />
      <div className="h-4 bg-muted rounded w-2/3" />
    </div>
  )
}

function BlockRenderer({ block }: { block: BlockInstance }) {
  const BlockComponent = getBlockComponent(block.blockSlug)

  return (
    <Suspense fallback={<BlockSkeleton />}>
      <BlockComponent {...block.props} />
    </Suspense>
  )
}
```

## Error Boundaries

### Next.js Error Boundary

```typescript
// app/dashboard/(main)/[entity]/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/core/components/ui/button'
import { AlertCircle } from 'lucide-react'

export default function EntityError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error('Entity page error:', error)
  }, [error])

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4 p-6">
      <AlertCircle className="h-12 w-12 text-destructive" />
      <h2 className="text-xl font-semibold">Something went wrong!</h2>
      <p className="text-sm text-muted-foreground max-w-md text-center">
        {error.message || 'An error occurred while loading this page.'}
      </p>

      <div className="flex items-center gap-2">
        <Button variant="outline" onClick={() => window.history.back()}>
          Go Back
        </Button>
        <Button onClick={() => reset()}>
          Try Again
        </Button>
      </div>

      {/* Development error details */}
      {process.env.NODE_ENV === 'development' && error.stack && (
        <details className="mt-4 p-4 bg-muted rounded-lg text-xs max-w-2xl w-full">
          <summary className="cursor-pointer font-medium">Error Details</summary>
          <pre className="mt-2 overflow-auto">{error.stack}</pre>
        </details>
      )}
    </div>
  )
}
```

### Custom Error Component

```typescript
// Block error fallback
function BlockError({ blockSlug }: { blockSlug: string }) {
  return (
    <div className="w-full py-12 px-4 bg-destructive/10 border border-destructive/20 rounded">
      <div className="max-w-7xl mx-auto text-center">
        <p className="text-destructive">
          Failed to load block: <code className="font-mono">{blockSlug}</code>
        </p>
        <p className="text-sm text-muted-foreground mt-2">
          This block may not be available or there was an error rendering it.
        </p>
      </div>
    </div>
  )
}
```

## Performance Patterns

### useCallback for Event Handlers

```typescript
'use client'

import { useCallback, useState } from 'react'

function ThemeToggle() {
  const { setTheme, theme } = useTheme()
  const { user } = useAuth()

  // Memoize callback to prevent unnecessary re-renders
  const handleThemeChange = useCallback(async (newTheme: string) => {
    setTheme(newTheme)

    // Persist preference if logged in
    if (user?.id) {
      try {
        await fetch('/api/user/profile', {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            meta: { uiPreferences: { theme: newTheme } }
          }),
        })
      } catch (error) {
        console.error('Failed to save theme preference:', error)
      }
    }
  }, [setTheme, user])

  return (
    <DropdownMenu>
      <DropdownMenuItem onClick={() => handleThemeChange('light')}>
        Light
      </DropdownMenuItem>
      <DropdownMenuItem onClick={() => handleThemeChange('dark')}>
        Dark
      </DropdownMenuItem>
    </DropdownMenu>
  )
}
```

### Avoiding Unnecessary Re-renders

```typescript
// ✅ CORRECT - useState with initializer function
const [queryClient] = useState(() => new QueryClient())

// ❌ WRONG - Creates new instance on every render
const queryClient = new QueryClient()
```

## Custom Hooks Pattern

### useAuth Hook

```typescript
// core/hooks/useAuth.ts
'use client'

import { useRouter } from 'next/navigation'
import { authClient } from '@/core/lib/auth-client'

export function useAuth() {
  const router = useRouter()
  const session = authClient.useSession()

  const handleSignIn = async ({ email, password, redirectTo }: SignInParams) => {
    const { data, error } = await authClient.signIn.email({ email, password })

    if (error) {
      throw new Error(error.message || 'Error signing in')
    }

    if (data) {
      router.push(redirectTo || '/dashboard')
    }

    return data
  }

  const handleSignOut = async () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('activeTeamId')
    }
    await authClient.signOut()
    router.push('/login')
  }

  return {
    user: session.data?.user,
    session: session.data,
    isLoading: session.isPending,
    signIn: handleSignIn,
    signOut: handleSignOut,
    // ... other auth methods
  }
}
```

## React 19 Patterns (Available but Not Used)

These patterns are documented in `.rules/components.md` but not currently used in the codebase:

### use() Hook

```typescript
// Pattern available in React 19
import { use } from 'react'

function TodoList({ todosPromise }: { todosPromise: Promise<Todo[]> }) {
  const todos = use(todosPromise)  // Suspends until resolved
  return (
    <ul>
      {todos.map(todo => <li key={todo.id}>{todo.title}</li>)}
    </ul>
  )
}
```

**Current approach:** Use TanStack Query instead.

### useActionState

```typescript
// Pattern available in React 19
import { useActionState } from 'react'

function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null)

  return (
    <form action={formAction}>
      {state?.error && <p className="text-destructive">{state.error}</p>}
      <input name="email" type="email" />
      <input name="password" type="password" />
      <button disabled={isPending}>Sign In</button>
    </form>
  )
}
```

**Current approach:** Use React Hook Form with Zod validation.

## Anti-Patterns

```typescript
// ❌ NEVER: Use namespace import for React
import * as React from 'react'
React.useState()
React.useCallback()
React.memo()

// ✅ CORRECT: Use named imports (project convention)
import { useState, useCallback, memo } from 'react'
// For types: import { type MouseEvent, type DragEvent } from 'react'

// ❌ NEVER: Use useEffect for data fetching
useEffect(() => {
  fetch('/api/data').then(setData)
}, [])

// ✅ CORRECT: Use TanStack Query
const { data } = useQuery({ queryKey: ['data'], queryFn: fetchData })

// ❌ NEVER: Create objects/functions in render without memoization
<Button onClick={() => handleClick(id)} />  // New function each render

// ✅ CORRECT: Use useCallback for stable references
const handleButtonClick = useCallback(() => handleClick(id), [id])
<Button onClick={handleButtonClick} />

// ❌ NEVER: Access hooks conditionally
if (condition) {
  const value = useContext(MyContext)  // Breaks Rules of Hooks
}

// ✅ CORRECT: Always call hooks at top level
const value = useContext(MyContext)
if (condition) {
  // use value
}

// ❌ NEVER: Forget 'use client' directive for client components
export function InteractiveComponent() {
  const [state, setState] = useState()  // Error: useState is not defined
}

// ✅ CORRECT: Add directive at top of file
'use client'
export function InteractiveComponent() {
  const [state, setState] = useState()
}

// ❌ NEVER: Use client-side hooks in Server Components
// app/page.tsx (Server Component)
export default function Page() {
  const [count, setCount] = useState(0)  // Error!
}

// ✅ CORRECT: Extract to Client Component
// app/page.tsx
import { Counter } from './Counter'
export default function Page() {
  return <Counter />  // Client Component handles state
}
```

## Checklist

Before finalizing React component implementation:

- [ ] Correct component type (Server vs Client)
- [ ] Named imports from 'react' (never `import * as React`)
- [ ] 'use client' directive if using hooks
- [ ] TanStack Query for data fetching (not useEffect)
- [ ] Context with custom hook for state sharing
- [ ] Suspense boundaries for async operations
- [ ] Error boundaries for error handling
- [ ] useCallback for event handlers passed as props
- [ ] data-cy attributes on interactive elements
- [ ] Proper TypeScript types for props
- [ ] Loading states handled

## Related Skills

- `tanstack-query` - Data fetching patterns
- `shadcn-components` - UI component patterns
- `accessibility` - ARIA and keyboard patterns
- `cypress-selectors` - Testing selectors
