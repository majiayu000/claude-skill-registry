---
name: solidjs
description: Builds UIs with SolidJS including signals, effects, memos, and fine-grained reactivity. Use when creating high-performance reactive applications, building without virtual DOM, or needing granular updates.
---

# SolidJS

A declarative JavaScript library for building UIs with fine-grained reactivity.

## Quick Start

**Create project:**
```bash
npx degit solidjs/templates/ts my-app
cd my-app
npm install
npm run dev
```

## Signals

### Basic Signal

```tsx
import { createSignal } from 'solid-js';

function Counter() {
  const [count, setCount] = createSignal(0);

  return (
    <button onClick={() => setCount(count() + 1)}>
      Count: {count()}
    </button>
  );
}
```

### Signal Patterns

```tsx
import { createSignal } from 'solid-js';

function App() {
  // Primitive signal
  const [name, setName] = createSignal('');

  // Object signal
  const [user, setUser] = createSignal({ name: 'John', age: 30 });

  // Update primitives
  setName('Jane');

  // Update objects (replace entire object)
  setUser({ ...user(), age: 31 });

  // Functional update
  setCount(prev => prev + 1);

  return (
    <div>
      <p>Name: {name()}</p>
      <p>User: {user().name}</p>
    </div>
  );
}
```

## Effects

### createEffect

```tsx
import { createSignal, createEffect } from 'solid-js';

function Logger() {
  const [count, setCount] = createSignal(0);

  // Runs on initial render and when count changes
  createEffect(() => {
    console.log('Count changed:', count());
  });

  // With cleanup
  createEffect(() => {
    const handler = () => console.log('clicked');
    document.addEventListener('click', handler);

    // Cleanup function
    onCleanup(() => {
      document.removeEventListener('click', handler);
    });
  });

  return <button onClick={() => setCount(c => c + 1)}>Increment</button>;
}
```

### onMount and onCleanup

```tsx
import { onMount, onCleanup } from 'solid-js';

function Timer() {
  const [time, setTime] = createSignal(0);

  onMount(() => {
    const interval = setInterval(() => {
      setTime(t => t + 1);
    }, 1000);

    onCleanup(() => clearInterval(interval));
  });

  return <p>Time: {time()}s</p>;
}
```

## Memos (Derived State)

```tsx
import { createSignal, createMemo } from 'solid-js';

function App() {
  const [count, setCount] = createSignal(0);
  const [multiplier, setMultiplier] = createSignal(2);

  // Computed value - only recalculates when dependencies change
  const doubled = createMemo(() => count() * multiplier());

  // Expensive computation
  const filtered = createMemo(() => {
    console.log('Computing filtered list...');
    return items().filter(item => item.active);
  });

  return (
    <div>
      <p>Count: {count()}</p>
      <p>Doubled: {doubled()}</p>
    </div>
  );
}
```

## Components

### Basic Component

```tsx
import { Component } from 'solid-js';

interface Props {
  name: string;
  age?: number;
}

const Greeting: Component<Props> = (props) => {
  return (
    <div>
      <h1>Hello, {props.name}!</h1>
      {props.age && <p>Age: {props.age}</p>}
    </div>
  );
};

// Usage
<Greeting name="John" age={30} />
```

### Props with Defaults

```tsx
import { mergeProps } from 'solid-js';

interface Props {
  count?: number;
  label?: string;
}

function Counter(props: Props) {
  const merged = mergeProps({ count: 0, label: 'Count' }, props);

  return (
    <p>{merged.label}: {merged.count}</p>
  );
}
```

### Splitting Props

```tsx
import { splitProps } from 'solid-js';

interface Props {
  name: string;
  class?: string;
  style?: string;
}

function Button(props: Props) {
  const [local, others] = splitProps(props, ['name']);

  return (
    <button {...others}>
      {local.name}
    </button>
  );
}
```

## Children

```tsx
import { ParentComponent, children } from 'solid-js';

const Card: ParentComponent<{ title: string }> = (props) => {
  return (
    <div class="card">
      <h2>{props.title}</h2>
      <div class="content">
        {props.children}
      </div>
    </div>
  );
};

// With resolved children
const List: ParentComponent = (props) => {
  const resolved = children(() => props.children);

  createEffect(() => {
    console.log('Children:', resolved());
  });

  return <ul>{resolved()}</ul>;
};
```

## Control Flow

### Show

```tsx
import { Show } from 'solid-js';

function App() {
  const [loggedIn, setLoggedIn] = createSignal(false);

  return (
    <Show
      when={loggedIn()}
      fallback={<button onClick={() => setLoggedIn(true)}>Log in</button>}
    >
      <button onClick={() => setLoggedIn(false)}>Log out</button>
    </Show>
  );
}
```

### For

```tsx
import { For } from 'solid-js';

function TodoList() {
  const [todos, setTodos] = createSignal([
    { id: 1, text: 'Learn Solid' },
    { id: 2, text: 'Build app' },
  ]);

  return (
    <ul>
      <For each={todos()}>
        {(todo, index) => (
          <li>
            {index() + 1}. {todo.text}
          </li>
        )}
      </For>
    </ul>
  );
}
```

### Index

```tsx
import { Index } from 'solid-js';

// For non-keyed lists where items may change but indices stay stable
function Grid() {
  const [cells, setCells] = createSignal(['A', 'B', 'C']);

  return (
    <div>
      <Index each={cells()}>
        {(cell, index) => (
          <div>{index}: {cell()}</div>
        )}
      </Index>
    </div>
  );
}
```

### Switch/Match

```tsx
import { Switch, Match } from 'solid-js';

function StatusMessage() {
  const [status, setStatus] = createSignal('loading');

  return (
    <Switch fallback={<p>Unknown status</p>}>
      <Match when={status() === 'loading'}>
        <p>Loading...</p>
      </Match>
      <Match when={status() === 'success'}>
        <p>Success!</p>
      </Match>
      <Match when={status() === 'error'}>
        <p>Error occurred</p>
      </Match>
    </Switch>
  );
}
```

### Dynamic

```tsx
import { Dynamic } from 'solid-js/web';

function App() {
  const [component, setComponent] = createSignal('div');

  return (
    <Dynamic component={component()} class="container">
      Content
    </Dynamic>
  );
}
```

## Stores (Complex State)

```tsx
import { createStore, produce } from 'solid-js/store';

interface Todo {
  id: number;
  text: string;
  completed: boolean;
}

function TodoApp() {
  const [todos, setTodos] = createStore<Todo[]>([]);

  const addTodo = (text: string) => {
    setTodos(todos.length, {
      id: Date.now(),
      text,
      completed: false,
    });
  };

  const toggleTodo = (id: number) => {
    setTodos(
      todo => todo.id === id,
      'completed',
      completed => !completed
    );
  };

  // Using produce for complex updates
  const removeTodo = (id: number) => {
    setTodos(produce(todos => {
      const index = todos.findIndex(t => t.id === id);
      if (index !== -1) todos.splice(index, 1);
    }));
  };

  return (
    <For each={todos}>
      {todo => (
        <div>
          <span style={{ 'text-decoration': todo.completed ? 'line-through' : 'none' }}>
            {todo.text}
          </span>
          <button onClick={() => toggleTodo(todo.id)}>Toggle</button>
        </div>
      )}
    </For>
  );
}
```

## Context

```tsx
import { createContext, useContext, ParentComponent } from 'solid-js';

interface ThemeContext {
  theme: () => string;
  setTheme: (theme: string) => void;
}

const ThemeContext = createContext<ThemeContext>();

const ThemeProvider: ParentComponent = (props) => {
  const [theme, setTheme] = createSignal('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {props.children}
    </ThemeContext.Provider>
  );
};

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function ThemedButton() {
  const { theme, setTheme } = useTheme();

  return (
    <button onClick={() => setTheme(theme() === 'light' ? 'dark' : 'light')}>
      Theme: {theme()}
    </button>
  );
}
```

## Resources (Async Data)

```tsx
import { createResource, Suspense, ErrorBoundary } from 'solid-js';

async function fetchUser(id: string) {
  const res = await fetch(`/api/users/${id}`);
  return res.json();
}

function UserProfile() {
  const [userId, setUserId] = createSignal('1');
  const [user, { refetch, mutate }] = createResource(userId, fetchUser);

  return (
    <ErrorBoundary fallback={<p>Error loading user</p>}>
      <Suspense fallback={<p>Loading...</p>}>
        <Show when={user()}>
          <div>
            <h1>{user().name}</h1>
            <button onClick={refetch}>Refresh</button>
          </div>
        </Show>
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Refs

```tsx
function TextInput() {
  let inputRef: HTMLInputElement | undefined;

  onMount(() => {
    inputRef?.focus();
  });

  return <input ref={inputRef} />;
}

// Callback ref
function CallbackRef() {
  return (
    <input ref={(el) => {
      // Called when element is created
      el.focus();
    }} />
  );
}
```

## Directives

```tsx
// Define directive
function clickOutside(el: Element, accessor: () => () => void) {
  const onClick = (e: MouseEvent) => {
    if (!el.contains(e.target as Node)) {
      accessor()?.();
    }
  };

  document.addEventListener('click', onClick);
  onCleanup(() => document.removeEventListener('click', onClick));
}

// Use directive
function Dropdown() {
  const [open, setOpen] = createSignal(false);

  return (
    <div use:clickOutside={() => setOpen(false)}>
      <button onClick={() => setOpen(true)}>Open</button>
      <Show when={open()}>
        <div>Dropdown content</div>
      </Show>
    </div>
  );
}
```

## Best Practices

1. **Call signals as functions** - Always use `count()` not `count`
2. **Use For for keyed lists** - More efficient than map
3. **Use stores for complex state** - Nested reactivity
4. **Avoid destructuring props** - Breaks reactivity
5. **Use createMemo for expensive computations** - Caches results

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Destructuring props | Access props.x directly |
| Forgetting to call signal | Use count() not count |
| Using map instead of For | Use For component |
| Mutating signal objects | Replace entire object |
| Missing Suspense for resources | Wrap in Suspense |

## Reference Files

- [references/reactivity.md](references/reactivity.md) - Reactivity deep dive
- [references/stores.md](references/stores.md) - Store patterns
- [references/router.md](references/router.md) - Solid Router
