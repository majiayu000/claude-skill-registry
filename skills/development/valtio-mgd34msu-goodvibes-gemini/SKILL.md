---
name: valtio
description: Manages state with Valtio using proxy-based reactivity, direct mutations, and automatic re-renders. Use when wanting mutable state syntax, fine-grained reactivity, or state management outside React components.
---

# Valtio

Proxy-based state management that makes React state feel like plain JavaScript.

## Quick Start

**Install:**
```bash
npm install valtio
```

**Create state:**
```typescript
// store.ts
import { proxy } from 'valtio';

interface Store {
  count: number;
  users: User[];
  filter: 'all' | 'active' | 'completed';
}

export const store = proxy<Store>({
  count: 0,
  users: [],
  filter: 'all',
});

// Actions - mutate directly
export const increment = () => {
  store.count++;
};

export const addUser = (user: User) => {
  store.users.push(user);
};
```

**Use in React:**
```tsx
import { useSnapshot } from 'valtio';
import { store, increment } from './store';

function Counter() {
  // Only re-renders when count changes
  const snap = useSnapshot(store);

  return (
    <div>
      <p>Count: {snap.count}</p>
      <button onClick={increment}>+1</button>
      {/* Or mutate directly */}
      <button onClick={() => store.count++}>+1</button>
    </div>
  );
}
```

## Core Concepts

### proxy() - Create Reactive State

```typescript
import { proxy } from 'valtio';

// Simple state
const state = proxy({ count: 0, text: '' });

// Nested objects are automatically proxied
const store = proxy({
  user: {
    name: 'John',
    settings: {
      theme: 'dark',
      notifications: true,
    },
  },
  todos: [],
});

// Mutations work at any depth
store.user.settings.theme = 'light';
store.todos.push({ id: 1, text: 'Learn Valtio' });
```

### useSnapshot() - Read in React

Returns a frozen, read-only snapshot that triggers re-renders only when accessed properties change.

```tsx
import { useSnapshot } from 'valtio';

function UserProfile() {
  const snap = useSnapshot(store);

  // Only re-renders when user.name changes
  return <p>{snap.user.name}</p>;
}

function TodoList() {
  const snap = useSnapshot(store);

  // Only re-renders when todos array changes
  return (
    <ul>
      {snap.todos.map(todo => (
        <li key={todo.id}>{todo.text}</li>
      ))}
    </ul>
  );
}
```

**Synchronous updates:**
```tsx
// For immediate renders (useful in tests)
const snap = useSnapshot(store, { sync: true });
```

### Mutations - Write to Proxy

Always mutate the proxy, never the snapshot.

```typescript
// Direct mutations
store.count++;
store.user.name = 'Jane';

// Array mutations
store.items.push(newItem);
store.items.splice(index, 1);
store.items[0].done = true;

// Object replacement
store.user = { ...store.user, name: 'Jane' };

// Delete properties
delete store.user.email;
```

## Actions Pattern

```typescript
// store/todos.ts
import { proxy } from 'valtio';

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

interface TodoStore {
  todos: Todo[];
  filter: 'all' | 'active' | 'completed';
}

export const todoStore = proxy<TodoStore>({
  todos: [],
  filter: 'all',
});

// Actions - define alongside store
export const actions = {
  addTodo(text: string) {
    todoStore.todos.push({
      id: crypto.randomUUID(),
      text,
      completed: false,
    });
  },

  toggleTodo(id: string) {
    const todo = todoStore.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
    }
  },

  removeTodo(id: string) {
    const index = todoStore.todos.findIndex(t => t.id === id);
    if (index >= 0) {
      todoStore.todos.splice(index, 1);
    }
  },

  clearCompleted() {
    todoStore.todos = todoStore.todos.filter(t => !t.completed);
  },

  setFilter(filter: TodoStore['filter']) {
    todoStore.filter = filter;
  },
};
```

## Computed Properties

### Getters

```typescript
const store = proxy({
  firstName: 'John',
  lastName: 'Doe',

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  },

  todos: [] as Todo[],

  get completedCount() {
    return this.todos.filter(t => t.completed).length;
  },

  get activeCount() {
    return this.todos.length - this.completedCount;
  },
});

// Usage
console.log(store.fullName); // 'John Doe'
```

### derive() - Cross-Store Computations

```typescript
import { proxy } from 'valtio';
import { derive } from 'derive-valtio';

const userStore = proxy({ name: 'John', role: 'admin' });
const settingsStore = proxy({ theme: 'dark' });

// Create derived state from multiple stores
const derived = derive({
  greeting: (get) => `Hello, ${get(userStore).name}!`,
  canEdit: (get) => get(userStore).role === 'admin',
});

// Attach derived properties to existing proxy
derive(
  {
    isDark: (get) => get(settingsStore).theme === 'dark',
  },
  { proxy: userStore }
);
```

## Subscriptions

### subscribe() - React to Changes

```typescript
import { subscribe } from 'valtio';

// Subscribe to all changes
const unsubscribe = subscribe(store, () => {
  console.log('Store changed:', store);
});

// Subscribe to nested object
subscribe(store.user, () => {
  console.log('User changed');
});

// Persist to localStorage
subscribe(store, () => {
  localStorage.setItem('store', JSON.stringify(store));
});

// Cleanup
unsubscribe();
```

### subscribeKey() - Watch Single Property

```typescript
import { subscribeKey } from 'valtio/utils';

subscribeKey(store, 'count', (value) => {
  console.log('Count is now:', value);
  document.title = `Count: ${value}`;
});
```

### watch() - Auto-tracking

```typescript
import { watch } from 'valtio/utils';

const stop = watch((get) => {
  // Automatically subscribes to accessed properties
  console.log('User:', get(store).user.name);
  console.log('Count:', get(store).count);
});

// Later
stop();
```

## Utilities

### ref() - Escape Proxy

Wrap values that shouldn't be proxied (DOM nodes, class instances, large data).

```typescript
import { proxy, ref } from 'valtio';

const store = proxy({
  // DOM node - don't proxy
  canvas: ref(document.createElement('canvas')),

  // Large dataset - don't proxy for performance
  bigData: ref(hugeArray),

  // Class instance - preserve prototype
  date: ref(new Date()),
});
```

### snapshot() - Get Immutable Copy

```typescript
import { snapshot } from 'valtio';

const snap = snapshot(store);

// Useful for:
// - Sending to API
// - Logging
// - Comparison
console.log(JSON.stringify(snap));

// Deep equality check
if (snapshot(store) !== previousSnap) {
  // State changed
}
```

### proxySet() and proxyMap()

```typescript
import { proxySet, proxyMap } from 'valtio/utils';

// Reactive Set
const selectedIds = proxySet<string>(['id1', 'id2']);
selectedIds.add('id3');
selectedIds.delete('id1');
selectedIds.has('id2'); // true

// Reactive Map
const users = proxyMap<string, User>([
  ['user1', { name: 'John' }],
]);
users.set('user2', { name: 'Jane' });
users.get('user1'); // { name: 'John' }
users.delete('user1');
```

### devtools()

```typescript
import { devtools } from 'valtio/utils';

// Connect to Redux DevTools
const unsub = devtools(store, {
  name: 'MyApp Store',
  enabled: process.env.NODE_ENV === 'development',
});
```

## Async Actions

```typescript
const store = proxy({
  users: [] as User[],
  loading: false,
  error: null as string | null,
});

export async function fetchUsers() {
  store.loading = true;
  store.error = null;

  try {
    const response = await fetch('/api/users');
    store.users = await response.json();
  } catch (e) {
    store.error = e instanceof Error ? e.message : 'Unknown error';
  } finally {
    store.loading = false;
  }
}

// Can call from anywhere - not just React
fetchUsers();
```

## Outside React

Valtio works without React.

```typescript
import { proxy, subscribe, snapshot } from 'valtio/vanilla';

const state = proxy({ count: 0 });

// Subscribe to changes
subscribe(state, () => {
  const snap = snapshot(state);
  document.getElementById('count')!.textContent = String(snap.count);
});

// Update from anywhere
document.getElementById('btn')!.onclick = () => {
  state.count++;
};
```

## Testing

```typescript
import { proxy, snapshot } from 'valtio';
import { store, actions } from './store';

describe('todoStore', () => {
  beforeEach(() => {
    // Reset state
    store.todos = [];
    store.filter = 'all';
  });

  it('adds todo', () => {
    actions.addTodo('Test todo');

    expect(store.todos).toHaveLength(1);
    expect(store.todos[0].text).toBe('Test todo');
  });

  it('toggles todo', () => {
    actions.addTodo('Test');
    const id = store.todos[0].id;

    actions.toggleTodo(id);

    expect(store.todos[0].completed).toBe(true);
  });

  it('creates immutable snapshot', () => {
    store.count = 5;
    const snap = snapshot(store);

    expect(snap.count).toBe(5);
    expect(() => {
      (snap as any).count = 10;
    }).toThrow();
  });
});
```

## Common Patterns

### Store Slices

```typescript
// stores/user.ts
export const userStore = proxy({
  user: null as User | null,
  login(user: User) {
    this.user = user;
  },
  logout() {
    this.user = null;
  },
});

// stores/cart.ts
export const cartStore = proxy({
  items: [] as CartItem[],
  add(item: CartItem) {
    this.items.push(item);
  },
});

// stores/index.ts - combine if needed
export { userStore } from './user';
export { cartStore } from './cart';
```

### Form State

```typescript
const formStore = proxy({
  values: {
    email: '',
    password: '',
  },
  errors: {} as Record<string, string>,
  touched: {} as Record<string, boolean>,

  setField(field: string, value: string) {
    this.values[field] = value;
    this.touched[field] = true;
    this.validate(field);
  },

  validate(field?: string) {
    // Validation logic
  },
});
```

## Best Practices

1. **Read from snapshot, write to proxy** - Never mutate snap
2. **Define actions as functions** - Keep mutations organized
3. **Use ref() for non-reactive data** - DOM nodes, large arrays
4. **Keep stores small** - Split by domain/feature
5. **TypeScript interfaces** - Define types for store shape

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mutating snapshot | Mutate proxy instead |
| Spreading proxy in render | Use snapshot values |
| Large objects without ref() | Wrap with ref() |
| Async in render | Move to action function |

## Reference Files

- [references/utils.md](references/utils.md) - Utility functions
- [references/patterns.md](references/patterns.md) - Advanced patterns
