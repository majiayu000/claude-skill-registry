---
name: react
description: Core React 19 patterns including hooks, Suspense, lazy loading, component structure, TypeScript best practices, and performance optimization. Use when working with React components, hooks, lazy loading, Suspense boundaries, or React-specific TypeScript patterns.
---

# React Core Patterns

## Purpose

Essential React 19 patterns for building modern applications with hooks, Suspense, lazy loading, and TypeScript.

**Note**: React 19 (released December 2024) breaking changes:
- `forwardRef` no longer needed - pass `ref` as a prop directly
- `propTypes` removed (silently ignored)
- New JSX transform required
- `React.FC` type discouraged - use direct function components instead

## When to Use This Skill

- Creating React components
- Using React hooks (useState, useEffect, useCallback, useMemo)
- Implementing lazy loading and code splitting
- Working with Suspense boundaries
- React-specific TypeScript patterns
- Performance optimization with React

---

## Quick Start

### Component Structure Template

```typescript
import { useState, useCallback } from 'react';

interface Props {
  userId: string;
  onUpdate?: (data: UserData) => void;
}

interface UserData {
  name: string;
  email: string;
}

function UserProfile({ userId, onUpdate }: Props) {
  const [data, setData] = useState<UserData | null>(null);

  const handleUpdate = useCallback((newData: UserData) => {
    setData(newData);
    onUpdate?.(newData);
  }, [onUpdate]);

  return (
    <div>
      {/* Component content */}
    </div>
  );
}

export default UserProfile;
```

### Component Checklist

Creating a React component? Follow this:

- [ ] Use function components with typed props (not `React.FC`)
- [ ] Define interfaces for Props and local state
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Use `useMemo` for expensive computations
- [ ] Lazy load if heavy component: `lazy(() => import())`
- [ ] Wrap lazy components in `<Suspense>` with fallback
- [ ] Default export at bottom
- [ ] No conditional hooks (hooks must be called in same order)
- [ ] Pass `ref` as a prop (no `forwardRef` needed in React 19)

---

## Core Hooks Patterns

### useState

```typescript
// Simple state
const [count, setCount] = useState<number>(0);

// Object state
const [user, setUser] = useState<User | null>(null);

// Array state
const [items, setItems] = useState<Item[]>([]);

// Functional updates when depending on previous state
setCount(prev => prev + 1);
setItems(prev => [...prev, newItem]);
```

### useCallback

```typescript
// Wrap functions passed to child components
const handleClick = useCallback((id: string) => {
  console.log('Clicked:', id);
}, []); // Empty deps if no dependencies

// With dependencies
const handleUpdate = useCallback((data: FormData) => {
  apiCall(userId, data);
}, [userId]); // Re-create when userId changes
```

### useMemo

```typescript
// Expensive computation
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.score - b.score);
}, [items]);

// Derived state
const totalPrice = useMemo(() => {
  return cart.reduce((sum, item) => sum + item.price, 0);
}, [cart]);
```

### useEffect

```typescript
// Run once on mount
useEffect(() => {
  fetchData();
}, []);

// Run when dependency changes
useEffect(() => {
  if (userId) {
    loadUserData(userId);
  }
}, [userId]);

// Cleanup
useEffect(() => {
  const subscription = subscribe(userId);
  return () => subscription.unsubscribe();
}, [userId]);
```

---

## Lazy Loading & Code Splitting

### Basic Lazy Loading

```typescript
import React, { Suspense } from 'react';

// Lazy load heavy component
const HeavyChart = React.lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart />
      </Suspense>
    </div>
  );
}
```

### Multiple Lazy Components

```typescript
const AdminPanel = React.lazy(() => import('./AdminPanel'));
const UserSettings = React.lazy(() => import('./UserSettings'));
const Reports = React.lazy(() => import('./Reports'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/settings" element={<UserSettings />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Suspense>
  );
}
```

### Feature-Based Code Splitting

```typescript
// features/auth/index.tsx
export { default } from './AuthFeature';

// Lazy load entire feature
const AuthFeature = React.lazy(() => import('~/features/auth'));

<Suspense fallback={<FeatureLoader />}>
  <AuthFeature />
</Suspense>
```

---

## Suspense Patterns

### Suspense Boundaries

```typescript
// Wrap data-fetching components
<Suspense fallback={<Skeleton />}>
  <UserProfile userId={id} />
</Suspense>

// Nested Suspense for granular loading
<Suspense fallback={<PageLoader />}>
  <Header />
  <Suspense fallback={<ContentSkeleton />}>
    <MainContent />
  </Suspense>
  <Footer />
</Suspense>
```

### Error Boundaries with Suspense

```typescript
import { ErrorBoundary } from 'react-error-boundary';

<ErrorBoundary fallback={<ErrorFallback />}>
  <Suspense fallback={<Loading />}>
    <DataComponent />
  </Suspense>
</ErrorBoundary>
```

---

## TypeScript Patterns

### Component Props

```typescript
// Basic props
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

// Props with children
interface CardProps {
  title: string;
  children: React.ReactNode;
}

// Props with specific child types
interface ListProps {
  children: React.ReactElement<ItemProps> | React.ReactElement<ItemProps>[];
}

// Props with event handlers
interface FormProps {
  onSubmit: (data: FormData) => void;
  onChange?: (field: string, value: unknown) => void;
}
```

### Hooks TypeScript

```typescript
// useState with type
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<Item[]>([]);

// useRef with type
const inputRef = useRef<HTMLInputElement>(null);
const timerRef = useRef<number | null>(null);

// Custom hook with return type
function useUser(id: string): { user: User | null; loading: boolean } {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // ... implementation

  return { user, loading };
}
```

---

## Performance Optimization

### React.memo

```typescript
// Memoize component to prevent unnecessary re-renders
const UserCard = React.memo<UserCardProps>(({ user, onUpdate }) => {
  return (
    <div>
      <h3>{user.name}</h3>
      <button onClick={() => onUpdate(user.id)}>Update</button>
    </div>
  );
});

// Custom comparison function
const UserCard = React.memo(UserCardComponent, (prevProps, nextProps) => {
  return prevProps.user.id === nextProps.user.id;
});
```

### Avoiding Re-renders

```typescript
// ❌ Bad: Creates new function on every render
function Parent() {
  return <Child onClick={() => console.log('clicked')} />;
}

// ✅ Good: Stable function reference
function Parent() {
  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return <Child onClick={handleClick} />;
}
```

---

## Common Patterns

### Conditional Rendering

```typescript
// Ternary operator
{isLoading ? <Spinner /> : <Content />}

// Logical AND
{error && <ErrorMessage error={error} />}

// Nullish coalescing
{user ?? <GuestView />}

// Early return for loading states
function Component() {
  const { data } = useSomeHook();

  // ❌ Avoid early returns for loading - breaks hooks rules
  // Use Suspense instead

  return <div>{data.map(...)}</div>;
}
```

### Lists and Keys

```typescript
// Always use stable keys
{items.map(item => (
  <ItemCard key={item.id} item={item} />
))}

// Never use index as key if list can reorder
// ❌ Bad
{items.map((item, index) => (
  <ItemCard key={index} item={item} />
))}
```

---

## File Organization

### Feature-Based Structure

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── types/
│   │   └── index.tsx
│   └── posts/
│       ├── components/
│       ├── hooks/
│       ├── types/
│       └── index.tsx
├── components/  # Shared components
├── hooks/       # Shared hooks
└── types/       # Shared types
```

### Component Co-location

```
features/posts/
├── components/
│   ├── PostCard.tsx
│   ├── PostList.tsx
│   └── PostForm.tsx
├── hooks/
│   ├── usePost.ts
│   └── usePosts.ts
├── types/
│   └── post.ts
└── index.tsx  # Public API
```

---

## Common Mistakes to Avoid

### 1. Conditional Hooks

```typescript
// ❌ Never do this
function Component({ condition }) {
  if (condition) {
    const [state, setState] = useState(0); // Breaks rules of hooks
  }
}

// ✅ Do this
function Component({ condition }) {
  const [state, setState] = useState(0);
  // Use state conditionally, not the hook
}
```

### 2. Missing Dependencies

```typescript
// ❌ Bad: Missing dependency
useEffect(() => {
  fetchUser(userId);
}, []); // userId should be in deps

// ✅ Good: All dependencies listed
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

### 3. Mutating State

```typescript
// ❌ Bad: Mutating state directly
const handleAdd = () => {
  items.push(newItem); // Don't mutate
  setItems(items);
};

// ✅ Good: Create new array
const handleAdd = () => {
  setItems([...items, newItem]);
};
```

---

## Additional Resources

For more detailed patterns, see:
- [component-patterns.md](resources/component-patterns.md) - Advanced component patterns
- [performance.md](resources/performance.md) - Performance optimization techniques
- [typescript-patterns.md](resources/typescript-patterns.md) - TypeScript best practices
- [hooks-patterns.md](resources/hooks-patterns.md) - Custom hooks and advanced patterns
