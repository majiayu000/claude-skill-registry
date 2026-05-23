---
name: react-nextjs-component-guardian
description: Offensive React/Next.js component quality enforcement. Triggered when creating components, reviewing client/server patterns, debugging hook dependencies, optimizing re-renders, or preparing frontend for production. App Router-aware. Scans for performance bottlenecks, accessibility gaps, state management issues, and TypeScript safety. Produces auto-scan reports with optimization paths.
---

# React/Next.js Component Guardian

**Mission:** Prevent React component bugs and optimize frontend performance through proactive pattern enforcement and evidence-based best practices. This skill operates in **offensive mode** - finding optimization opportunities and pattern violations before they cause issues.

## Activation Triggers

- Creating new React components
- "Why is my component re-rendering?"
- Next.js App Router vs Pages Router questions
- "Should this be a Server or Client Component?"
- Hook dependency warnings
- Performance optimization requests
- Accessibility audit requests
- State management architecture review
- TypeScript prop type errors
- Production frontend deployment prep

## Framework Awareness

This skill is specialized for **Next.js 14+ App Router** with React 18+:

- **Server Components** (default in App Router)
- **Client Components** (`'use client'` directive)
- **Server Actions** (async functions with `'use server'`)
- **Route Handlers** (app/api/)
- **Middleware** (middleware.ts)
- **Layouts and Templates**

For Pages Router projects, ask: "Are you using App Router or Pages Router?"

## Scan Methodology

### 1. Initial Context Gathering

**Ask if not provided:**
- "Show me the component code"
- "Is this a Server or Client Component?"
- "What's the component's purpose?" (layout, page, UI element, form)
- "Are you seeing performance issues?" (slow renders, memory leaks)
- "Is this component accessible?" (keyboard nav, screen readers)

### 2. Critical Component Patterns Scan

Execute ALL checks in this section. Each is based on real production incidents.

#### 🔴 CRITICAL: Server vs Client Component Mistakes

**Historical Failure:** Using client-only APIs in Server Components causes hydration errors

**Scan for:**
- [ ] `'use client'` directive placement (must be first line, before imports)
- [ ] Client-only APIs in Server Components (useState, useEffect, window, localStorage)
- [ ] Server-only APIs in Client Components (database queries, fs module)
- [ ] Unnecessary Client Components (could be Server Components)
- [ ] Props passed from Server to Client (must be serializable)

**Red flags:**
```tsx
// ❌ Missing 'use client' with hooks
import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)  // Error!
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}

// ❌ 'use client' not first line
import { useState } from 'react'
'use client'  // Error! Must be before imports

// ❌ Non-serializable props
// app/page.tsx (Server Component)
<ClientComponent user={new User()} />  // Error! Classes not serializable

// ❌ Server-only code in Client Component
'use client'
import { db } from '@/lib/database'  // Error! Database in client bundle
```

**Optimization:**
```tsx
// ✅ Proper Client Component
'use client'  // First line

import { useState } from 'react'

export default function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(count + 1)}>{count}</button>
}

// ✅ Server Component (no directive needed)
import { db } from '@/lib/database'

export default async function UserList() {
  const users = await db.user.findMany()  // Server-side query
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}

// ✅ Serializable props
// app/page.tsx
const user = await getUser()
<ClientComponent userId={user.id} userName={user.name} />  // Plain objects OK

// ✅ Minimize Client Components
// Only mark interactive parts as 'use client'
export default async function Page() {
  const data = await fetchData()  // Server Component
  return (
    <div>
      <StaticContent data={data} />  {/* Server Component */}
      <InteractiveButton />  {/* Client Component */}
    </div>
  )
}
```

**Decision matrix:**
- **Use Server Component when**: Fetching data, rendering static content, SEO important
- **Use Client Component when**: User interaction, browser APIs, state/effects needed

#### 🔴 CRITICAL: Hook Dependency Arrays

**Historical Failure:** Missing dependencies cause stale closures and infinite loops

**Scan for:**
- [ ] useEffect with missing dependencies (ESLint warnings)
- [ ] useCallback/useMemo with incorrect dependencies
- [ ] Functions in dependencies (should be wrapped in useCallback)
- [ ] Infinite loops (dependency triggers its own update)
- [ ] Object/array dependencies (reference equality issues)

**Red flags:**
```tsx
// ❌ Missing dependency
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [])  // Error! Missing userId dependency

  return <div>{user?.name}</div>
}

// ❌ Function in dependency (creates new reference every render)
useEffect(() => {
  const handler = () => console.log(count)
  window.addEventListener('click', handler)
  return () => window.removeEventListener('click', handler)
}, [handler])  // Error! handler recreated every render

// ❌ Object dependency (reference changes every render)
const options = { filter: 'active', sort: 'name' }
useEffect(() => {
  fetchData(options)
}, [options])  // Error! Infinite loop

// ❌ Dependency triggers its own update
useEffect(() => {
  setCount(count + 1)
}, [count])  // Error! Infinite loop
```

**Optimization:**
```tsx
// ✅ Correct dependencies
function UserProfile({ userId }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])  // ✅ userId included

  return <div>{user?.name}</div>
}

// ✅ useCallback for function dependencies
const handleClick = useCallback(() => {
  console.log(count)
}, [count])

useEffect(() => {
  window.addEventListener('click', handleClick)
  return () => window.removeEventListener('click', handleClick)
}, [handleClick])  // ✅ Stable reference

// ✅ useMemo for object dependencies
const options = useMemo(() => ({
  filter: 'active',
  sort: 'name'
}), [])  // Only created once

useEffect(() => {
  fetchData(options)
}, [options])  // ✅ Stable reference

// ✅ Functional updates (no dependency needed)
useEffect(() => {
  const timer = setInterval(() => {
    setCount(c => c + 1)  // Functional update
  }, 1000)
  return () => clearInterval(timer)
}, [])  // ✅ No count dependency needed
```

**ESLint rule enforcement:**
```json
// .eslintrc.json
{
  "rules": {
    "react-hooks/exhaustive-deps": "error"  // Enforce dependency arrays
  }
}
```

#### 🟡 HIGH: Performance Optimization

**Historical Issue:** Unnecessary re-renders causing UI lag

**Scan for:**
- [ ] Expensive computations without useMemo
- [ ] Event handlers without useCallback
- [ ] Large lists without virtualization
- [ ] Components without React.memo (when appropriate)
- [ ] Prop drilling (should use context or composition)

**Red flags:**
```tsx
// ❌ Expensive computation on every render
function DataTable({ data }) {
  const sortedData = data.sort((a, b) => a.name.localeCompare(b.name))
  return <table>{/* ... */}</table>
}

// ❌ New function reference every render
function Parent() {
  const [count, setCount] = useState(0)
  return <Child onClick={() => setCount(count + 1)} />
}

// ❌ Long list without virtualization (1000+ items)
function UserList({ users }) {
  return (
    <ul>
      {users.map(u => <UserItem key={u.id} user={u} />)}  {/* 10,000 DOM nodes */}
    </ul>
  )
}

// ❌ Prop drilling through 3+ levels
<Parent>
  <Child1 user={user}>
    <Child2 user={user}>
      <Child3 user={user}>
        {/* Finally uses user */}
      </Child3>
    </Child2>
  </Child1>
</Parent>
```

**Optimization:**
```tsx
// ✅ useMemo for expensive computations
function DataTable({ data }) {
  const sortedData = useMemo(() => {
    return data.sort((a, b) => a.name.localeCompare(b.name))
  }, [data])
  return <table>{/* ... */}</table>
}

// ✅ useCallback for event handlers
function Parent() {
  const [count, setCount] = useState(0)
  const handleClick = useCallback(() => {
    setCount(c => c + 1)
  }, [])
  return <Child onClick={handleClick} />
}

// ✅ React.memo to prevent unnecessary re-renders
const Child = React.memo(function Child({ onClick }) {
  return <button onClick={onClick}>Click me</button>
})

// ✅ Virtualization for long lists
import { FixedSizeList } from 'react-window'

function UserList({ users }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={users.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>
          <UserItem user={users[index]} />
        </div>
      )}
    </FixedSizeList>
  )
}

// ✅ Context instead of prop drilling
const UserContext = createContext<User | null>(null)

function Parent() {
  const user = useUser()
  return (
    <UserContext.Provider value={user}>
      <Child1>
        <Child2>
          <Child3 />  {/* Uses useContext(UserContext) */}
        </Child2>
      </Child1>
    </UserContext.Provider>
  )
}
```

**Performance budget:**
- Component render time: <16ms (60fps target)
- useEffect execution: <50ms
- Event handler response: <100ms
- Initial page load: <3s

Use React DevTools Profiler to measure.

#### 🟡 HIGH: TypeScript Prop Safety

**Historical Failure:** Runtime prop errors in production due to weak typing

**Scan for:**
- [ ] Components without prop type definitions
- [ ] `any` types for props
- [ ] Optional props without default values
- [ ] Event handler types (use React.MouseEvent, etc.)
- [ ] Generic component types (React.FC vs function components)

**Red flags:**
```tsx
// ❌ No prop types
export default function Button(props) {
  return <button onClick={props.onClick}>{props.children}</button>
}

// ❌ any types
interface Props {
  data: any  // Error! No type safety
  onClick: any
}

// ❌ Wrong event type
function handleClick(e: Event) {  // Error! Should be React.MouseEvent
  e.preventDefault()
}

// ❌ React.FC (deprecated pattern)
const Button: React.FC<Props> = ({ children }) => {
  return <button>{children}</button>
}
```

**Optimization:**
```tsx
// ✅ Explicit interface with proper types
interface ButtonProps {
  variant?: 'primary' | 'secondary'  // Literal union type
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void
  children: React.ReactNode
}

// ✅ Function component with typed props
export default function Button({
  variant = 'primary',  // Default value
  size = 'md',
  disabled = false,
  onClick,
  children
}: ButtonProps) {
  return (
    <button
      className={`btn-${variant} btn-${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// ✅ Generic component
interface ListProps<T> {
  items: T[]
  renderItem: (item: T) => React.ReactNode
  keyExtractor: (item: T) => string
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={keyExtractor(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  )
}

// Usage with type inference
<List
  items={users}  // TypeScript infers T = User
  renderItem={u => <span>{u.name}</span>}
  keyExtractor={u => u.id}
/>
```

#### 🟠 MEDIUM: Accessibility (a11y)

**Historical Issue:** Keyboard navigation broken, screen readers fail

**Scan for:**
- [ ] Interactive elements without keyboard support
- [ ] Missing ARIA labels
- [ ] Form inputs without labels
- [ ] Low contrast text
- [ ] Images without alt text
- [ ] Focus indicators removed

**Red flags:**
```tsx
// ❌ div as button (not keyboard accessible)
<div onClick={handleClick}>Click me</div>

// ❌ Missing label
<input type="text" placeholder="Enter name" />

// ❌ Image without alt
<img src="/logo.png" />

// ❌ Custom focus removal
button:focus { outline: none; }  /* Error! */
```

**Optimization:**
```tsx
// ✅ Semantic HTML
<button onClick={handleClick}>Click me</button>

// ✅ Proper labels
<label htmlFor="name">Name:</label>
<input id="name" type="text" />

// ✅ Alt text for images
<img src="/logo.png" alt="PDFLab Logo" />

// ✅ ARIA labels for icon buttons
<button aria-label="Close modal" onClick={onClose}>
  <XIcon />
</button>

// ✅ Keyboard navigation
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick()
    }
  }}
>
  Custom button
</div>

// ✅ Custom focus styles
button:focus-visible {
  outline: 2px solid oklch(0.72 0.15 250);
  outline-offset: 2px;
}
```

**WCAG 2.1 Level AA checklist:**
- Contrast ratio: 4.5:1 for normal text, 3:1 for large text
- All functionality available via keyboard
- Focus order logical
- Error messages descriptive

#### 🟠 MEDIUM: State Management Architecture

**Historical Issue:** State scattered across components, causing sync bugs

**Scan for:**
- [ ] Lifting state too high (context overuse)
- [ ] Duplicate state (same data in multiple places)
- [ ] Derived state stored (should be computed)
- [ ] Local storage abuse (should use server state)
- [ ] Missing loading/error states

**Red flags:**
```tsx
// ❌ Duplicate state
function Parent() {
  const [users, setUsers] = useState([])
  return <Child1 users={users} /><Child2 users={users} />
}
// Both children update users separately → out of sync

// ❌ Derived state stored
const [items, setItems] = useState([])
const [itemCount, setItemCount] = useState(0)  // Error! Duplicate source of truth

// ❌ Missing loading state
function Users() {
  const [users, setUsers] = useState([])
  useEffect(() => { fetchUsers().then(setUsers) }, [])
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
  // No loading indicator!
}
```

**Optimization:**
```tsx
// ✅ Single source of truth
const [items, setItems] = useState([])
const itemCount = items.length  // Derived, not stored

// ✅ Proper loading/error states
function Users() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchUsers()
      .then(setUsers)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  if (error) return <ErrorMessage message={error} />
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>
}

// ✅ Context for shared state (not prop drilling)
const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth().then(setUser).finally(() => setLoading(false))
  }, [])

  return (
    <AuthContext.Provider value={{ user, setUser, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

// ✅ Custom hook for cleaner access
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

// Usage
function Profile() {
  const { user, loading } = useAuth()
  if (loading) return <Spinner />
  return <div>{user?.name}</div>
}
```

**State management decision tree:**
1. **Local component state**: Single component uses it → `useState`
2. **Shared state (2-3 components)**: Lift to nearest parent → `useState` + props
3. **Shared state (3+ components, deep tree)**: Use context → `createContext`
4. **Server state (API data)**: Use React Query or SWR
5. **Complex client state**: Consider Zustand or Jotai

#### 🟢 LOW: Error Boundaries

**Not failure-critical but improves UX**

**Scan for:**
- [ ] Error boundaries around async components
- [ ] Fallback UI for errors
- [ ] Error reporting (Sentry integration)

**Optimization:**
```tsx
// ✅ Error boundary component
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

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
    // Send to Sentry
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false })}>
            Try again
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

// Usage
<ErrorBoundary fallback={<ErrorPage />}>
  <ConversionInterface />
</ErrorBoundary>
```

### 3. Next.js App Router Specific Patterns

#### Loading States
```tsx
// app/dashboard/loading.tsx
export default function Loading() {
  return <Spinner />  // Shown while page.tsx loads
}
```

#### Error Handling
```tsx
// app/dashboard/error.tsx
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
      <h2>Error: {error.message}</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )
}
```

#### Server Actions
```tsx
// app/actions.ts
'use server'

import { db } from '@/lib/database'
import { revalidatePath } from 'next/cache'

export async function createUser(formData: FormData) {
  const name = formData.get('name') as string
  const user = await db.user.create({ data: { name } })
  revalidatePath('/users')  // Revalidate cache
  return { success: true, user }
}

// app/page.tsx (Server Component)
import { createUser } from './actions'

export default function Page() {
  return (
    <form action={createUser}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  )
}
```

### 4. Production Readiness Checklist

Generate this checklist in the auto-scan report:

```
REACT COMPONENT READINESS SCORE: X/10

✅ Server/Client components correctly separated
✅ All hooks have correct dependency arrays
✅ Performance optimizations applied (memo, useMemo, useCallback)
✅ TypeScript prop types defined
✅ Accessibility standards met (WCAG 2.1 AA)
⚠️  State management could be improved (context recommended)
⚠️  Missing error boundary
❌ Critical: useEffect infinite loop in ConversionStatus.tsx
❌ Performance: 10,000 item list without virtualization

RISK LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]
BLOCKERS: X critical issues must be resolved
OPTIMIZATIONS: Y performance wins available
```

## Output Format: Auto-Scan Report

```
═══════════════════════════════════════════════
🛡️ REACT/NEXT.JS COMPONENT GUARDIAN - SCAN RESULTS
═══════════════════════════════════════════════

📊 SCAN SCOPE
• Framework: Next.js 14 (App Router)
• React: 18.2.0
• Component type: Client Component
• Lines of code: 150

🚨 CRITICAL FINDINGS: [count]
[List each critical issue with:
 - What's wrong
 - Why it's dangerous (stale closures, infinite loops, etc.)
 - How to fix (code example)]

⚠️  HIGH PRIORITY: [count]
[Performance issues, TypeScript gaps]

💡 OPTIMIZATIONS: [count]
[useMemo opportunities, React.memo candidates]

🎯 ACCESSIBILITY AUDIT:
✅ Keyboard navigation: Fully accessible
✅ Screen reader: ARIA labels present
❌ Missing: Alt text for 3 images
⚠️  Contrast ratio: 3.2:1 (should be 4.5:1)

⚡ PERFORMANCE ANALYSIS:
Current render time: 45ms
With useMemo: ~25ms (44% faster)
With React.memo: ~15ms (67% faster)
With virtualization: ~8ms (82% faster)

═══════════════════════════════════════════════
FINAL VERDICT
═══════════════════════════════════════════════
Production Ready: [YES/NO/BLOCKED]
Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]
Estimated Fix Time: [X hours]

NEXT ACTIONS:
1. [Most critical fix]
2. [Second priority]
3. [Optional optimization]

═══════════════════════════════════════════════
```

## Key Principles

1. **Server-first mindset:** Default to Server Components, only use Client when necessary
2. **Hook dependency discipline:** Trust ESLint, fix all warnings
3. **Performance budget:** 16ms render target, measure with Profiler
4. **Accessibility mandatory:** WCAG 2.1 AA minimum
5. **TypeScript strict:** No `any`, explicit prop types
6. **Error handling:** Loading states, error boundaries, fallback UI

## Quick Reference: Common Fixes

```bash
# Install React DevTools (Chrome)
# Use Profiler to find slow components

# Install accessibility checker
npm install --save-dev eslint-plugin-jsx-a11y

# .eslintrc.json
{
  "extends": ["plugin:jsx-a11y/recommended"],
  "rules": {
    "react-hooks/exhaustive-deps": "error"
  }
}

# Check for unused dependencies
npm install --save-dev depcheck
npx depcheck

# Analyze bundle size
npm run build
# Check .next/analyze/
```

## PDFLab-Specific Patterns

**UnifiedConversionInterface.tsx** - Main conversion UI component:
- Should be Client Component (uses useState, useEffect)
- File upload requires browser APIs
- Progress tracking needs polling with useEffect
- Apply React.memo to FilePreview sub-component

**AuthContext.tsx** - Authentication state:
- Use context to avoid prop drilling
- Persist to localStorage for session restoration
- Implement loading state during auth check

**Navigation.tsx** - Main navigation:
- Can be Server Component if no client interactivity
- Use Next.js Link for client-side routing
- Apply proper ARIA labels for accessibility
