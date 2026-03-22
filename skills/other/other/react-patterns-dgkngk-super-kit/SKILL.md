---
name: react-patterns
description: Modern React patterns, hooks, and state management principles. Use when structuring React components, managing state, optimizing re-renders, or choosing state management libraries.
---

# React Patterns Skill

## Overview
Modern React patterns, hooks, and state management principles.

## Core Principles

### 1. Component Composition
- Prefer composition over inheritance
- Use children prop for flexibility
- Create compound components for related UI

### 2. Hooks Best Practices
```tsx
// Custom hook pattern
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}
```

### 3. State Management
- **Local state:** useState for component-level
- **Shared state:** Context + useReducer
- **Server state:** React Query, SWR
- **Global state:** Zustand, Jotai

### 4. Performance Patterns
```tsx
// Memoization
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data.name}</div>;
});

// useMemo for expensive computations
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// useCallback for stable references
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

### 5. Error Boundaries
```tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    logError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <FallbackUI />;
    }
    return this.props.children;
  }
}
```

## Anti-Patterns to Avoid
- ❌ Prop drilling (use Context instead)
- ❌ Mutating state directly
- ❌ Missing dependency arrays
- ❌ Over-using useEffect
- ❌ Inline function definitions in render
