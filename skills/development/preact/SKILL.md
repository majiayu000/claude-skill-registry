---
name: preact
description: Builds fast, lightweight React-compatible applications with Preact's 3KB library and optional Signals for fine-grained reactivity. Use when optimizing bundle size, migrating from React, or when user mentions Preact, preact/compat, or lightweight React alternative.
---

# Preact

Fast 3KB React alternative with the same modern API and optional Signals for fine-grained reactivity.

## Quick Start

```bash
# Create new project
npm create preact my-app

# Or with Vite
npm create vite@latest my-app -- --template preact-ts

cd my-app
npm install
npm run dev
```

## Components

### Functional Components

```tsx
import { h } from 'preact';

// Basic component
function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}

// With default export
export default function App() {
  return (
    <div>
      <Greeting name="World" />
    </div>
  );
}
```

### Class Components

```tsx
import { Component, h } from 'preact';

interface CounterState {
  count: number;
}

interface CounterProps {
  initialCount?: number;
}

class Counter extends Component<CounterProps, CounterState> {
  state = { count: this.props.initialCount ?? 0 };

  increment = () => {
    this.setState(prev => ({ count: prev.count + 1 }));
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}
```

## Hooks

### useState

```tsx
import { useState } from 'preact/hooks';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}
```

### useEffect

```tsx
import { useState, useEffect } from 'preact/hooks';

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState(null);
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

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### useRef

```tsx
import { useRef } from 'preact/hooks';

function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  const focusInput = () => {
    inputRef.current?.focus();
  };

  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </div>
  );
}
```

### useMemo & useCallback

```tsx
import { useMemo, useCallback } from 'preact/hooks';

function ExpensiveList({ items, filter }: { items: Item[]; filter: string }) {
  // Memoize expensive computation
  const filteredItems = useMemo(() => {
    return items.filter(item =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  // Memoize callback
  const handleItemClick = useCallback((id: string) => {
    console.log('Clicked:', id);
  }, []);

  return (
    <ul>
      {filteredItems.map(item => (
        <li key={item.id} onClick={() => handleItemClick(item.id)}>
          {item.name}
        </li>
      ))}
    </ul>
  );
}
```

### useContext

```tsx
import { createContext } from 'preact';
import { useContext } from 'preact/hooks';

interface Theme {
  primary: string;
  secondary: string;
}

const ThemeContext = createContext<Theme>({
  primary: '#007bff',
  secondary: '#6c757d',
});

function ThemeProvider({ children }) {
  const theme = {
    primary: '#6366f1',
    secondary: '#8b5cf6',
  };

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}

function ThemedButton() {
  const theme = useContext(ThemeContext);

  return (
    <button style={{ backgroundColor: theme.primary, color: 'white' }}>
      Themed Button
    </button>
  );
}
```

### useReducer

```tsx
import { useReducer } from 'preact/hooks';

interface State {
  count: number;
  step: number;
}

type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'setStep'; payload: number }
  | { type: 'reset' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { ...state, count: state.count + state.step };
    case 'decrement':
      return { ...state, count: state.count - state.step };
    case 'setStep':
      return { ...state, step: action.payload };
    case 'reset':
      return { count: 0, step: 1 };
    default:
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({ type: 'setStep', payload: +e.currentTarget.value })}
      />
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <button onClick={() => dispatch({ type: 'reset' })}>Reset</button>
    </div>
  );
}
```

## Signals

Preact Signals provide fine-grained reactivity without re-rendering entire component trees.

### Basic Signals

```tsx
import { signal, computed } from '@preact/signals';

// Create signals (outside component = global state)
const count = signal(0);
const doubled = computed(() => count.value * 2);

function Counter() {
  // Signals auto-subscribe - only affected parts re-render
  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled: {doubled}</p>
      <button onClick={() => count.value++}>Increment</button>
    </div>
  );
}
```

### Signal Hooks

```tsx
import { useSignal, useComputed } from '@preact/signals';

function Counter() {
  // Component-scoped signals
  const count = useSignal(0);
  const doubled = useComputed(() => count.value * 2);

  return (
    <div>
      <p>Count: {count}</p>
      <p>Doubled: {doubled}</p>
      <button onClick={() => count.value++}>Increment</button>
    </div>
  );
}
```

### Signal Effects

```tsx
import { signal, effect, batch } from '@preact/signals';

const name = signal('');
const email = signal('');

// Runs whenever dependencies change
effect(() => {
  console.log(`User: ${name.value} <${email.value}>`);
});

// Batch multiple updates
function updateUser(newName: string, newEmail: string) {
  batch(() => {
    name.value = newName;
    email.value = newEmail;
  });
}
```

### Complex State with Signals

```tsx
import { signal, computed } from '@preact/signals';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

// State
const todos = signal<Todo[]>([]);
const filter = signal<'all' | 'active' | 'completed'>('all');

// Derived state
const filteredTodos = computed(() => {
  switch (filter.value) {
    case 'active':
      return todos.value.filter(t => !t.completed);
    case 'completed':
      return todos.value.filter(t => t.completed);
    default:
      return todos.value;
  }
});

const activeCount = computed(() =>
  todos.value.filter(t => !t.completed).length
);

// Actions
function addTodo(text: string) {
  todos.value = [
    ...todos.value,
    { id: Date.now(), text, completed: false }
  ];
}

function toggleTodo(id: number) {
  todos.value = todos.value.map(todo =>
    todo.id === id ? { ...todo, completed: !todo.completed } : todo
  );
}

function removeTodo(id: number) {
  todos.value = todos.value.filter(t => t.id !== id);
}

// Component
function TodoApp() {
  return (
    <div>
      <h1>Todos ({activeCount} active)</h1>

      <div>
        <button onClick={() => filter.value = 'all'}>All</button>
        <button onClick={() => filter.value = 'active'}>Active</button>
        <button onClick={() => filter.value = 'completed'}>Completed</button>
      </div>

      <ul>
        {filteredTodos.value.map(todo => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}>
              {todo.text}
            </span>
            <button onClick={() => removeTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## preact/compat

Drop-in React replacement for using React libraries with Preact.

### Configuration

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  resolve: {
    alias: {
      'react': 'preact/compat',
      'react-dom': 'preact/compat',
      'react-dom/test-utils': 'preact/test-utils',
      'react/jsx-runtime': 'preact/jsx-runtime',
    },
  },
});
```

```javascript
// webpack.config.js
module.exports = {
  resolve: {
    alias: {
      'react': 'preact/compat',
      'react-dom': 'preact/compat',
      'react-dom/test-utils': 'preact/test-utils',
      'react/jsx-runtime': 'preact/jsx-runtime',
    },
  },
};
```

### Using React Libraries

```tsx
// React libraries work with preact/compat
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
      >
        <UserList />
      </motion.div>
    </QueryClientProvider>
  );
}

function UserList() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => fetch('/api/users').then(r => r.json()),
  });

  if (isLoading) return <p>Loading...</p>;

  return (
    <ul>
      {data.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

## Rendering

### Render to DOM

```tsx
import { render } from 'preact';
import App from './App';

render(<App />, document.getElementById('app')!);
```

### Hydration (SSR)

```tsx
import { hydrate } from 'preact';
import App from './App';

hydrate(<App />, document.getElementById('app')!);
```

### Server-Side Rendering

```tsx
import { render } from 'preact-render-to-string';
import App from './App';

const html = render(<App />);

// Full page
const page = `
<!DOCTYPE html>
<html>
  <head>
    <title>My App</title>
  </head>
  <body>
    <div id="app">${html}</div>
    <script src="/bundle.js"></script>
  </body>
</html>
`;
```

## Optimizations

### Avoiding Re-renders

```tsx
import { memo } from 'preact/compat';

// Only re-renders when props change (shallow comparison)
const MemoizedItem = memo(function Item({ item }) {
  return <li>{item.name}</li>;
});

// Custom comparison
const MemoizedUser = memo(
  function User({ user }) {
    return <div>{user.name}</div>;
  },
  (prevProps, nextProps) => prevProps.user.id === nextProps.user.id
);
```

### Lazy Loading

```tsx
import { lazy, Suspense } from 'preact/compat';

const Dashboard = lazy(() => import('./Dashboard'));
const Settings = lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Router>
        <Dashboard path="/dashboard" />
        <Settings path="/settings" />
      </Router>
    </Suspense>
  );
}
```

### Error Boundaries

```tsx
import { Component } from 'preact';

class ErrorBoundary extends Component {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div>
          <h1>Something went wrong</h1>
          <pre>{this.state.error?.message}</pre>
          <button onClick={() => this.setState({ hasError: false })}>
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Routing

```tsx
import { Router, Route, Link } from 'preact-router';

function App() {
  return (
    <div>
      <nav>
        <Link href="/">Home</Link>
        <Link href="/about">About</Link>
        <Link href="/users/123">User 123</Link>
      </nav>

      <Router>
        <Home path="/" />
        <About path="/about" />
        <User path="/users/:id" />
        <NotFound default />
      </Router>
    </div>
  );
}

function Home() {
  return <h1>Home</h1>;
}

function About() {
  return <h1>About</h1>;
}

function User({ id }: { id: string }) {
  return <h1>User: {id}</h1>;
}

function NotFound() {
  return <h1>404 - Not Found</h1>;
}
```

## Testing

```tsx
// Using @testing-library/preact
import { render, fireEvent, screen } from '@testing-library/preact';
import Counter from './Counter';

test('increments counter', async () => {
  render(<Counter />);

  const button = screen.getByRole('button', { name: /increment/i });
  const count = screen.getByText(/count:/i);

  expect(count).toHaveTextContent('Count: 0');

  await fireEvent.click(button);

  expect(count).toHaveTextContent('Count: 1');
});
```

## Reference Files

- [signals-patterns.md](references/signals-patterns.md) - Advanced Signals patterns
- [migration.md](references/migration.md) - Migrating from React to Preact
