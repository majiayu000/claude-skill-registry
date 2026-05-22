---
name: developing-with-react
description: React 18+ development with hooks, state management, component patterns, and Next.js integration. Use when building React applications or working with JSX/TSX components.
---

# React Framework - Quick Reference

**Version**: 1.0.0 | **Framework**: React 18+ | **Use Case**: Fast lookups during active development

---

## When to Use

Load this skill when:
- `package.json` contains `"react"` dependency (>=18.0.0)
- Project has `.jsx` or `.tsx` files in `src/`
- Next.js, Vite, or Create React App detected
- User mentions "React" in task description

**Minimum Detection Confidence**: 0.8 (80%)

---

## Quick Start

```tsx
import { FC, useState } from 'react';

interface Props {
  title: string;
  onAction?: () => void;
}

export const MyComponent: FC<Props> = ({ title, onAction }) => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>{title}</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
      <button onClick={onAction}>Action</button>
    </div>
  );
};
```

---

## Component Design

### Functional Component Structure

```tsx
// 1. Imports (grouped and sorted)
import { useState, useEffect } from 'react';
import type { FC, ReactNode } from 'react';

// 2. Types/Interfaces
interface Props {
  children: ReactNode;
  className?: string;
}

// 3. Component
export const Component: FC<Props> = ({ children, className }) => {
  // 4. Hooks (state, effects, context)
  const [state, setState] = useState<string>('');

  useEffect(() => {
    // Side effects
  }, []);

  // 5. Event handlers
  const handleClick = () => setState('clicked');

  // 6. Early returns (error states, loading)
  if (!children) return null;

  // 7. Main render
  return <div className={className}>{children}</div>;
};
```

### Container/Presentational Pattern

```tsx
// Container: Logic and data fetching
export const UserProfileContainer: FC<{ userId: number }> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser)
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <LoadingSpinner />;
  if (!user) return <ErrorMessage />;

  return <UserProfile user={user} />;
};

// Presentational: Pure UI
export const UserProfile: FC<{ user: User }> = ({ user }) => (
  <div>
    <h2>{user.name}</h2>
    <p>{user.email}</p>
  </div>
);
```

---

## Core Hooks

### useState - Local State

```tsx
// Basic usage
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);

// Functional updates (when new state depends on old)
setCount(prevCount => prevCount + 1);

// Lazy initialization (expensive computation)
const [data, setData] = useState(() => expensiveComputation());

// Object state updates (always spread)
setForm(prev => ({ ...prev, email: 'new@email.com' }));
```

### useEffect - Side Effects

```tsx
// Run once on mount
useEffect(() => {
  fetchData();
}, []);

// Run when dependencies change
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// Cleanup function
useEffect(() => {
  const subscription = api.subscribe();
  return () => subscription.unsubscribe();
}, []);

// Abort fetch on unmount
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal });
  return () => controller.abort();
}, [url]);
```

### useContext - Consume Context

```tsx
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Provider
export const ThemeProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light');

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook (always validate context exists)
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

### useReducer - Complex State

```tsx
type Action = { type: 'increment' } | { type: 'decrement' } | { type: 'reset' };

const reducer = (state: number, action: Action): number => {
  switch (action.type) {
    case 'increment': return state + 1;
    case 'decrement': return state - 1;
    case 'reset': return 0;
    default: return state;
  }
};

const Counter = () => {
  const [count, dispatch] = useReducer(reducer, 0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
    </div>
  );
};
```

### Custom Hooks

```tsx
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(url, { signal: controller.signal })
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}

// Usage
const { data: user, loading, error } = useFetch<User>(`/api/users/${userId}`);
```

---

## Performance Optimization

### React.memo - Prevent Re-renders

```tsx
// Memoize component - only re-renders when props change
export const ExpensiveComponent = memo(({ data }: { data: Data }) => {
  return <div>{/* expensive rendering */}</div>;
});

// With custom comparison
export const CustomMemo = memo(
  ({ user }: { user: User }) => <div>{user.name}</div>,
  (prev, next) => prev.user.id === next.user.id
);
```

### useMemo & useCallback

```tsx
// useMemo: Memoize expensive computations
const filteredItems = useMemo(() => {
  return items.filter(item => item.includes(filter));
}, [items, filter]);

// useCallback: Memoize function references
const handleClick = useCallback(() => {
  setCount(c => c + 1);
}, []);

// Pass to memoized children to prevent re-renders
<MemoizedChild onClick={handleClick} />
```

### Code Splitting

```tsx
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

const App = () => (
  <Suspense fallback={<div>Loading...</div>}>
    <HeavyComponent />
  </Suspense>
);
```

---

## Accessibility (WCAG 2.1 AA)

### Essential Patterns

```tsx
// Use semantic HTML
<button onClick={handleClick}>Click me</button>  // Good
<div onClick={handleClick}>Click me</div>        // Bad

// ARIA labels for screen readers
<button aria-label="Close dialog">X</button>

// ARIA descriptions
<input type="email" aria-describedby="email-hint" />
<span id="email-hint">We'll never share your email</span>

// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">{statusMessage}</div>

// Keyboard navigation
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') onClose();
  if (e.key === 'Enter') onSubmit();
};
```

### Form Accessibility

```tsx
<form onSubmit={handleSubmit}>
  <label htmlFor="email">Email</label>
  <input
    id="email"
    type="email"
    aria-invalid={!!errors.email}
    aria-describedby={errors.email ? 'email-error' : undefined}
  />
  {errors.email && <span id="email-error" role="alert">{errors.email}</span>}
</form>
```

---

## TypeScript Quick Reference

### Component Props

```tsx
interface Props {
  title: string;               // Required
  subtitle?: string;           // Optional
  variant: 'primary' | 'secondary';  // Union types
  onClick?: () => void;        // Optional function
  onSubmit: (data: FormData) => void;  // Required function
  children: ReactNode;         // Children
  user: User;                  // Complex type
}

export const Component: FC<Props> = ({ title, onClick }) => (
  <div onClick={onClick}>{title}</div>
);
```

### Event Handlers

```tsx
const handleClick = (e: MouseEvent<HTMLButtonElement>) => {};
const handleChange = (e: ChangeEvent<HTMLInputElement>) => {};
const handleSubmit = (e: FormEvent<HTMLFormElement>) => { e.preventDefault(); };
const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {};
```

### Refs

```tsx
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => { inputRef.current?.focus(); }, []);
<input ref={inputRef} />
```

---

## Anti-Patterns (Avoid These)

```tsx
// DON'T: Mutate state directly
user.name = 'Jane'; setUser(user);  // Bad
setUser({ ...user, name: 'Jane' }); // Good

// DON'T: Use index as key
{items.map((item, i) => <div key={i}>{item}</div>)}  // Bad
{items.map(item => <div key={item.id}>{item}</div>)} // Good

// DON'T: Call hooks conditionally
if (condition) { useState(0); }  // Bad - hooks must be top-level

// DON'T: Miss useEffect dependencies
useEffect(() => { fetchUser(userId); }, []);     // Bad
useEffect(() => { fetchUser(userId); }, [userId]); // Good

// DON'T: Inline functions in JSX (when performance matters)
<Button onClick={() => handleClick(id)}>Click</Button>  // Bad
<Button onClick={handleClickWithId}>Click</Button>      // Good (with useCallback)
```

---

## Testing Quick Reference

```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);
    await userEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click</Button>);
    expect(await axe(container)).toHaveNoViolations();
  });
});
```

---

## Integration Checklist

When using this skill, ensure:

- [ ] Components use TypeScript with strict types
- [ ] Interactive elements are keyboard accessible
- [ ] ARIA attributes added where semantic HTML insufficient
- [ ] Performance optimization applied (memo, useMemo, useCallback)
- [ ] Unit tests written with React Testing Library
- [ ] Accessibility tests with jest-axe
- [ ] Custom hooks extracted for reusable logic
- [ ] Error boundaries implemented for error handling

---

## See Also

- **[REFERENCE.md](REFERENCE.md)** - Comprehensive React guide with:
  - Advanced component patterns (compound components, render props, HOCs)
  - Complete hooks deep dive
  - State management architectures (Context optimization, Redux, Zustand)
  - Full WCAG 2.1 AA accessibility guide
  - Performance profiling and optimization
  - Testing strategies and patterns
  - TypeScript advanced patterns
  - Styling approaches (CSS Modules, styled-components, Tailwind)
- **[templates/](templates/)** - Code generation templates
- **[examples/](examples/)** - Real-world implementation examples

---

**Version**: 1.0.0 | **Last Updated**: 2025-01-01 | **Status**: Production Ready
