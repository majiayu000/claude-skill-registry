---
name: react-hooks-complete
description: Complete React hooks reference system. PROACTIVELY activate for: (1) useState and useReducer patterns, (2) useEffect and lifecycle, (3) useRef for DOM and values, (4) useContext for shared state, (5) useMemo and useCallback optimization, (6) React 19 hooks (useTransition, useDeferredValue, useActionState, useOptimistic), (7) Custom hook development, (8) Hook rules and best practices. Provides: Hook syntax, effect cleanup patterns, performance optimization, custom hook patterns. Ensures correct hook usage following React best practices.
---

## Quick Reference

| Hook | Purpose | Example |
|------|---------|---------|
| `useState` | Local state | `const [count, setCount] = useState(0)` |
| `useReducer` | Complex state | `const [state, dispatch] = useReducer(reducer, init)` |
| `useEffect` | Side effects | `useEffect(() => { ... }, [deps])` |
| `useRef` | Mutable ref / DOM | `const ref = useRef<HTMLInputElement>(null)` |
| `useContext` | Consume context | `const value = useContext(MyContext)` |
| `useMemo` | Memoize value | `const computed = useMemo(() => calc(), [deps])` |
| `useCallback` | Stable function | `const fn = useCallback(() => {}, [deps])` |

| React 19 Hook | Purpose |
|---------------|---------|
| `useTransition` | Non-blocking updates |
| `useDeferredValue` | Defer expensive renders |
| `useActionState` | Server Action state |
| `useOptimistic` | Optimistic UI updates |
| `useFormStatus` | Form pending state |

## When to Use This Skill

Use for **React hooks implementation**:
- Choosing the right hook for your use case
- Managing component state with useState/useReducer
- Handling side effects and cleanup with useEffect
- Building custom reusable hooks
- Optimizing with useMemo and useCallback
- Using React 19 concurrent features

**For state management libraries**: see `react-state-management`

---

# React Hooks Complete Guide

## State Hooks

### useState

```tsx
import { useState } from 'react';

// Basic usage
const [count, setCount] = useState(0);

// With initial function (lazy initialization)
const [state, setState] = useState(() => {
  const initialValue = expensiveComputation();
  return initialValue;
});

// Object state
const [user, setUser] = useState<User | null>(null);

// Updating object state (always create new reference)
setUser((prev) => prev ? { ...prev, name: 'New Name' } : null);

// Array state
const [items, setItems] = useState<Item[]>([]);

// Add item
setItems((prev) => [...prev, newItem]);

// Remove item
setItems((prev) => prev.filter((item) => item.id !== id));

// Update item
setItems((prev) =>
  prev.map((item) => (item.id === id ? { ...item, ...updates } : item))
);
```

### useReducer

```tsx
import { useReducer } from 'react';

// Define state and action types
interface State {
  count: number;
  error: string | null;
  loading: boolean;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'reset'; payload: number }
  | { type: 'setError'; payload: string };

// Reducer function
function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + 1 };
    case 'decrement':
      return { ...state, count: state.count - 1 };
    case 'reset':
      return { ...state, count: action.payload };
    case 'setError':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

// Usage
function Counter() {
  const [state, dispatch] = useReducer(reducer, {
    count: 0,
    error: null,
    loading: false,
  });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset', payload: 0 })}>
        Reset
      </button>
    </div>
  );
}
```

### useReducer with Immer

```tsx
import { useReducer } from 'react';
import { produce } from 'immer';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

type Action =
  | { type: 'add'; text: string }
  | { type: 'toggle'; id: number }
  | { type: 'delete'; id: number };

function todosReducer(state: Todo[], action: Action): Todo[] {
  return produce(state, (draft) => {
    switch (action.type) {
      case 'add':
        draft.push({
          id: Date.now(),
          text: action.text,
          completed: false,
        });
        break;
      case 'toggle':
        const todo = draft.find((t) => t.id === action.id);
        if (todo) todo.completed = !todo.completed;
        break;
      case 'delete':
        const index = draft.findIndex((t) => t.id === action.id);
        if (index !== -1) draft.splice(index, 1);
        break;
    }
  });
}
```

## Effect Hooks

### useEffect

```tsx
import { useEffect, useState } from 'react';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function fetchUser() {
      setLoading(true);
      try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        if (!cancelled) {
          setUser(data);
        }
      } catch (error) {
        if (!cancelled) {
          console.error('Failed to fetch user:', error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchUser();

    // Cleanup function
    return () => {
      cancelled = true;
    };
  }, [userId]); // Re-run when userId changes

  if (loading) return <p>Loading...</p>;
  if (!user) return <p>User not found</p>;
  return <div>{user.name}</div>;
}
```

### useLayoutEffect

```tsx
import { useLayoutEffect, useRef, useState } from 'react';

function Tooltip({ text, children }: { text: string; children: ReactNode }) {
  const [tooltipHeight, setTooltipHeight] = useState(0);
  const tooltipRef = useRef<HTMLDivElement>(null);

  // Runs synchronously after DOM mutations but before paint
  useLayoutEffect(() => {
    if (tooltipRef.current) {
      setTooltipHeight(tooltipRef.current.getBoundingClientRect().height);
    }
  }, [text]);

  return (
    <div className="tooltip-container">
      {children}
      <div
        ref={tooltipRef}
        className="tooltip"
        style={{ top: -tooltipHeight - 10 }}
      >
        {text}
      </div>
    </div>
  );
}
```

### useInsertionEffect (for CSS-in-JS libraries)

```tsx
import { useInsertionEffect } from 'react';

// For CSS-in-JS library authors
function useCSS(rule: string) {
  useInsertionEffect(() => {
    const style = document.createElement('style');
    style.textContent = rule;
    document.head.appendChild(style);
    return () => {
      document.head.removeChild(style);
    };
  }, [rule]);
}
```

## Context Hook

### useContext

```tsx
import { createContext, useContext, useState, ReactNode } from 'react';

// Define context type
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Create context with default value
const AuthContext = createContext<AuthContextType | null>(null);

// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const userData = await response.json();
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

// Usage
function LoginButton() {
  const { isAuthenticated, logout, user } = useAuth();

  if (isAuthenticated) {
    return (
      <div>
        <span>Welcome, {user?.name}</span>
        <button onClick={logout}>Logout</button>
      </div>
    );
  }

  return <Link href="/login">Login</Link>;
}
```

## Ref Hooks

### useRef

```tsx
import { useRef, useEffect } from 'react';

// DOM reference
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return <input ref={inputRef} type="text" />;
}

// Mutable value (doesn't trigger re-render)
function Timer() {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const [count, setCount] = useState(0);

  const startTimer = () => {
    if (intervalRef.current) return;
    intervalRef.current = setInterval(() => {
      setCount((c) => c + 1);
    }, 1000);
  };

  const stopTimer = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={startTimer}>Start</button>
      <button onClick={stopTimer}>Stop</button>
    </div>
  );
}
```

### useImperativeHandle

```tsx
import { forwardRef, useImperativeHandle, useRef } from 'react';

interface VideoPlayerHandle {
  play: () => void;
  pause: () => void;
  seek: (time: number) => void;
}

const VideoPlayer = forwardRef<VideoPlayerHandle, { src: string }>(
  ({ src }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);

    useImperativeHandle(ref, () => ({
      play() {
        videoRef.current?.play();
      },
      pause() {
        videoRef.current?.pause();
      },
      seek(time: number) {
        if (videoRef.current) {
          videoRef.current.currentTime = time;
        }
      },
    }));

    return <video ref={videoRef} src={src} />;
  }
);

// Usage
function App() {
  const playerRef = useRef<VideoPlayerHandle>(null);

  return (
    <div>
      <VideoPlayer ref={playerRef} src="/video.mp4" />
      <button onClick={() => playerRef.current?.play()}>Play</button>
      <button onClick={() => playerRef.current?.pause()}>Pause</button>
      <button onClick={() => playerRef.current?.seek(30)}>Skip to 30s</button>
    </div>
  );
}
```

## Performance Hooks

### useMemo

```tsx
import { useMemo, useState } from 'react';

function ProductList({ products, filter }: Props) {
  // Memoize expensive computation
  const filteredProducts = useMemo(() => {
    console.log('Filtering products...');
    return products.filter((product) => {
      if (filter.category && product.category !== filter.category) {
        return false;
      }
      if (filter.minPrice && product.price < filter.minPrice) {
        return false;
      }
      if (filter.maxPrice && product.price > filter.maxPrice) {
        return false;
      }
      return true;
    });
  }, [products, filter]);

  // Memoize derived data
  const stats = useMemo(
    () => ({
      total: filteredProducts.length,
      avgPrice:
        filteredProducts.reduce((sum, p) => sum + p.price, 0) /
        filteredProducts.length,
    }),
    [filteredProducts]
  );

  return (
    <div>
      <p>
        Showing {stats.total} products (avg: ${stats.avgPrice.toFixed(2)})
      </p>
      {filteredProducts.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}
```

### useCallback

```tsx
import { useCallback, useState, memo } from 'react';

// Memoized child component
const TodoItem = memo(function TodoItem({
  todo,
  onToggle,
  onDelete,
}: {
  todo: Todo;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}) {
  console.log('Rendering todo:', todo.id);
  return (
    <li>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
      />
      <span>{todo.text}</span>
      <button onClick={() => onDelete(todo.id)}>Delete</button>
    </li>
  );
});

function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([]);

  // Stable callback reference
  const handleToggle = useCallback((id: number) => {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  }, []);

  const handleDelete = useCallback((id: number) => {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }, []);

  return (
    <ul>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={handleToggle}
          onDelete={handleDelete}
        />
      ))}
    </ul>
  );
}
```

## React 19 Hooks

### useTransition

```tsx
import { useState, useTransition } from 'react';

function TabContainer() {
  const [tab, setTab] = useState('about');
  const [isPending, startTransition] = useTransition();

  function selectTab(nextTab: string) {
    // Mark state update as non-urgent
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <div>
      <nav>
        {['about', 'posts', 'contact'].map((t) => (
          <button
            key={t}
            onClick={() => selectTab(t)}
            className={tab === t ? 'active' : ''}
          >
            {t}
          </button>
        ))}
      </nav>

      <div className={isPending ? 'pending' : ''}>
        {tab === 'about' && <AboutTab />}
        {tab === 'posts' && <PostsTab />}
        {tab === 'contact' && <ContactTab />}
      </div>
    </div>
  );
}
```

### useDeferredValue

```tsx
import { useState, useDeferredValue, memo } from 'react';

const SlowList = memo(function SlowList({ text }: { text: string }) {
  // Expensive rendering
  const items = [];
  for (let i = 0; i < 20000; i++) {
    items.push(<li key={i}>{text}</li>);
  }
  return <ul>{items}</ul>;
});

function App() {
  const [text, setText] = useState('');
  const deferredText = useDeferredValue(text);

  return (
    <div>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type here..."
      />
      {/* Input stays responsive while list updates are deferred */}
      <SlowList text={deferredText} />
    </div>
  );
}
```

### useActionState

```tsx
'use client';

import { useActionState } from 'react';

async function submitForm(
  prevState: { message: string } | null,
  formData: FormData
) {
  'use server';

  const email = formData.get('email') as string;

  if (!email.includes('@')) {
    return { message: 'Invalid email address' };
  }

  await subscribeToNewsletter(email);
  return { message: 'Subscribed successfully!' };
}

function NewsletterForm() {
  const [state, formAction, isPending] = useActionState(submitForm, null);

  return (
    <form action={formAction}>
      <input type="email" name="email" placeholder="Enter email" required />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Subscribing...' : 'Subscribe'}
      </button>
      {state?.message && <p>{state.message}</p>}
    </form>
  );
}
```

### useOptimistic

```tsx
'use client';

import { useOptimistic, useState } from 'react';
import { likePost } from './actions';

function LikeButton({ postId, initialLikes }: Props) {
  const [likes, setLikes] = useState(initialLikes);
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (state, _) => state + 1
  );

  async function handleLike() {
    addOptimisticLike(null); // Optimistically update
    const newLikes = await likePost(postId); // Server action
    setLikes(newLikes); // Update with actual value
  }

  return (
    <button onClick={handleLike}>
      Like ({optimisticLikes})
    </button>
  );
}
```

### useFormStatus

```tsx
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function Form() {
  return (
    <form action={submitAction}>
      <input type="text" name="name" />
      <SubmitButton />
    </form>
  );
}
```

## Custom Hooks

### useLocalStorage

```tsx
import { useState, useEffect } from 'react';

function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue;

    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
    }
  }, [key, value]);

  return [value, setValue] as const;
}

// Usage
function App() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  return <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>Toggle</button>;
}
```

### useDebounce

```tsx
import { useState, useEffect } from 'react';

function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Usage
function SearchInput() {
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery);
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={(e) => setQuery(e.target.value)} />;
}
```

### useFetch

```tsx
import { useState, useEffect } from 'react';

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}

function useFetch<T>(url: string): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    let cancelled = false;

    const fetchData = async () => {
      setState({ data: null, loading: true, error: null });

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (!cancelled) {
          setState({ data, loading: false, error: null });
        }
      } catch (error) {
        if (!cancelled) {
          setState({
            data: null,
            loading: false,
            error: error instanceof Error ? error : new Error('Unknown error'),
          });
        }
      }
    };

    fetchData();

    return () => {
      cancelled = true;
    };
  }, [url]);

  return state;
}
```

### useMediaQuery

```tsx
import { useState, useEffect } from 'react';

function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Usage
function App() {
  const isMobile = useMediaQuery('(max-width: 768px)');
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)');

  return (
    <div className={prefersDark ? 'dark' : 'light'}>
      {isMobile ? <MobileNav /> : <DesktopNav />}
    </div>
  );
}
```

## Rules of Hooks

1. **Only call hooks at the top level** - Don't call in loops, conditions, or nested functions
2. **Only call hooks from React functions** - Call from components or custom hooks
3. **Start custom hook names with "use"** - Convention that enables linting

```tsx
// Bad - conditional hook call
function Bad({ condition }) {
  if (condition) {
    const [state, setState] = useState(0); // Error!
  }
}

// Good - call hook unconditionally
function Good({ condition }) {
  const [state, setState] = useState(0);
  if (condition) {
    // Use state here
  }
}
```

## Additional References

For production-ready custom hook implementations, see:

- `references/custom-hooks-library.md` - Complete library of reusable custom hooks
