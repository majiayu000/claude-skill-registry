---
name: jotai
description: Manages React state with Jotai including atoms, derived atoms, async atoms, and utilities. Use when building React applications needing atomic state, bottom-up state management, or fine-grained updates.
---

# Jotai

Primitive and flexible state management for React.

## Quick Start

**Install:**
```bash
npm install jotai
```

**Basic usage:**
```tsx
import { atom, useAtom } from 'jotai';

const countAtom = atom(0);

function Counter() {
  const [count, setCount] = useAtom(countAtom);

  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

## Atoms

### Primitive Atoms

```tsx
import { atom } from 'jotai';

// Number
const countAtom = atom(0);

// String
const nameAtom = atom('');

// Boolean
const isOpenAtom = atom(false);

// Object
const userAtom = atom({ name: '', email: '' });

// Array
const todosAtom = atom<Todo[]>([]);
```

### Using Atoms

```tsx
import { useAtom, useAtomValue, useSetAtom } from 'jotai';

function Component() {
  // Read and write
  const [count, setCount] = useAtom(countAtom);

  // Read only
  const count = useAtomValue(countAtom);

  // Write only (no re-render on change)
  const setCount = useSetAtom(countAtom);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
    </div>
  );
}
```

## Derived Atoms

### Read-Only Derived

```tsx
import { atom } from 'jotai';

const countAtom = atom(0);

// Simple derived
const doubledAtom = atom((get) => get(countAtom) * 2);

// Derived from multiple atoms
const firstNameAtom = atom('John');
const lastNameAtom = atom('Doe');
const fullNameAtom = atom((get) => {
  return `${get(firstNameAtom)} ${get(lastNameAtom)}`;
});

// Filtered list
const todosAtom = atom<Todo[]>([]);
const completedTodosAtom = atom((get) => {
  return get(todosAtom).filter(todo => todo.completed);
});
```

### Read-Write Derived

```tsx
const countAtom = atom(0);

// Derived with custom setter
const doubledAtom = atom(
  (get) => get(countAtom) * 2,
  (get, set, newValue: number) => {
    set(countAtom, newValue / 2);
  }
);

// Toggle atom
const isOpenAtom = atom(false);
const toggleAtom = atom(
  (get) => get(isOpenAtom),
  (get, set) => {
    set(isOpenAtom, !get(isOpenAtom));
  }
);
```

### Write-Only Atoms

```tsx
// Action atom (no read value)
const incrementAtom = atom(null, (get, set) => {
  set(countAtom, get(countAtom) + 1);
});

// Usage
const increment = useSetAtom(incrementAtom);
<button onClick={increment}>+1</button>

// Action with parameters
const addTodoAtom = atom(null, (get, set, text: string) => {
  const todos = get(todosAtom);
  set(todosAtom, [...todos, { id: Date.now(), text, completed: false }]);
});
```

## Async Atoms

### Basic Async Atom

```tsx
import { atom, useAtomValue } from 'jotai';
import { Suspense } from 'react';

const userIdAtom = atom(1);

const userAtom = atom(async (get) => {
  const id = get(userIdAtom);
  const response = await fetch(`/api/users/${id}`);
  return response.json();
});

function UserProfile() {
  const user = useAtomValue(userAtom);
  return <div>{user.name}</div>;
}

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile />
    </Suspense>
  );
}
```

### Async Atom with Error Handling

```tsx
import { atom, useAtom } from 'jotai';
import { loadable } from 'jotai/utils';

const userAtom = atom(async (get) => {
  const response = await fetch('/api/user');
  if (!response.ok) throw new Error('Failed to fetch');
  return response.json();
});

const loadableUserAtom = loadable(userAtom);

function UserProfile() {
  const [userLoadable] = useAtom(loadableUserAtom);

  if (userLoadable.state === 'loading') {
    return <div>Loading...</div>;
  }

  if (userLoadable.state === 'hasError') {
    return <div>Error: {userLoadable.error.message}</div>;
  }

  return <div>{userLoadable.data.name}</div>;
}
```

### Refreshable Async Atom

```tsx
import { atom, useAtom, useSetAtom } from 'jotai';

const fetchCountAtom = atom(0);

const dataAtom = atom(async (get) => {
  get(fetchCountAtom); // Dependency for refresh
  const response = await fetch('/api/data');
  return response.json();
});

const refreshAtom = atom(null, (get, set) => {
  set(fetchCountAtom, (c) => c + 1);
});

function DataComponent() {
  const data = useAtomValue(dataAtom);
  const refresh = useSetAtom(refreshAtom);

  return (
    <div>
      <pre>{JSON.stringify(data)}</pre>
      <button onClick={refresh}>Refresh</button>
    </div>
  );
}
```

## Jotai Utilities

### atomWithStorage

```tsx
import { atomWithStorage } from 'jotai/utils';

// Persists to localStorage
const themeAtom = atomWithStorage('theme', 'light');

// With sessionStorage
const sessionAtom = atomWithStorage('session', null, sessionStorage);

function ThemeToggle() {
  const [theme, setTheme] = useAtom(themeAtom);

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Theme: {theme}
    </button>
  );
}
```

### atomWithReset

```tsx
import { atomWithReset, useResetAtom } from 'jotai/utils';

const countAtom = atomWithReset(0);

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  const reset = useResetAtom(countAtom);

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(c => c + 1)}>+1</button>
      <button onClick={reset}>Reset</button>
    </div>
  );
}
```

### atomFamily

```tsx
import { atomFamily } from 'jotai/utils';

// Create a family of atoms with parameter
const todoAtomFamily = atomFamily((id: string) =>
  atom({ id, text: '', completed: false })
);

function TodoItem({ id }: { id: string }) {
  const [todo, setTodo] = useAtom(todoAtomFamily(id));

  return (
    <div>
      <input
        value={todo.text}
        onChange={(e) => setTodo({ ...todo, text: e.target.value })}
      />
    </div>
  );
}
```

### selectAtom

```tsx
import { selectAtom } from 'jotai/utils';

const userAtom = atom({ name: 'John', age: 30, email: 'john@example.com' });

// Only re-renders when name changes
const nameAtom = selectAtom(userAtom, (user) => user.name);

// With equality function
const ageAtom = selectAtom(
  userAtom,
  (user) => user.age,
  (a, b) => a === b
);
```

### splitAtom

```tsx
import { splitAtom } from 'jotai/utils';

const todosAtom = atom<Todo[]>([]);
const todoAtomsAtom = splitAtom(todosAtom);

function TodoList() {
  const [todoAtoms, dispatch] = useAtom(todoAtomsAtom);

  return (
    <ul>
      {todoAtoms.map((todoAtom) => (
        <TodoItem
          key={`${todoAtom}`}
          todoAtom={todoAtom}
          onRemove={() => dispatch({ type: 'remove', atom: todoAtom })}
        />
      ))}
    </ul>
  );
}

function TodoItem({ todoAtom, onRemove }) {
  const [todo, setTodo] = useAtom(todoAtom);

  return (
    <li>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={(e) => setTodo({ ...todo, completed: e.target.checked })}
      />
      {todo.text}
      <button onClick={onRemove}>Delete</button>
    </li>
  );
}
```

### focusAtom

```tsx
import { focusAtom } from 'jotai-optics';

const userAtom = atom({ name: 'John', address: { city: 'NYC', zip: '10001' } });

// Focus on nested property
const cityAtom = focusAtom(userAtom, (optic) => optic.prop('address').prop('city'));

function CityInput() {
  const [city, setCity] = useAtom(cityAtom);
  return <input value={city} onChange={(e) => setCity(e.target.value)} />;
}
```

## Provider

### Scoped State

```tsx
import { Provider, createStore } from 'jotai';

const myStore = createStore();

function App() {
  return (
    <Provider store={myStore}>
      <Counter />
    </Provider>
  );
}
```

### Multiple Providers

```tsx
function App() {
  return (
    <Provider>
      <Counter /> {/* Uses Provider 1 */}
      <Provider>
        <Counter /> {/* Uses Provider 2 - isolated state */}
      </Provider>
    </Provider>
  );
}
```

### Store API

```tsx
import { createStore } from 'jotai';

const store = createStore();

// Get value outside React
const count = store.get(countAtom);

// Set value outside React
store.set(countAtom, 10);

// Subscribe to changes
const unsub = store.sub(countAtom, () => {
  console.log('Count changed:', store.get(countAtom));
});
```

## DevTools

```tsx
import { useAtomsDebugValue } from 'jotai-devtools';

function DebugAtoms() {
  useAtomsDebugValue();
  return null;
}

function App() {
  return (
    <>
      <DebugAtoms />
      <Counter />
    </>
  );
}
```

## Patterns

### Form State

```tsx
const formAtom = atom({
  name: '',
  email: '',
  message: '',
});

const nameAtom = focusAtom(formAtom, (o) => o.prop('name'));
const emailAtom = focusAtom(formAtom, (o) => o.prop('email'));
const messageAtom = focusAtom(formAtom, (o) => o.prop('message'));

const isValidAtom = atom((get) => {
  const form = get(formAtom);
  return form.name.length > 0 && form.email.includes('@');
});
```

### Optimistic Updates

```tsx
const todosAtom = atom<Todo[]>([]);

const addTodoAtom = atom(null, async (get, set, text: string) => {
  const tempId = Date.now();
  const newTodo = { id: tempId, text, completed: false, pending: true };

  // Optimistic update
  set(todosAtom, [...get(todosAtom), newTodo]);

  try {
    const response = await fetch('/api/todos', {
      method: 'POST',
      body: JSON.stringify({ text }),
    });
    const savedTodo = await response.json();

    // Replace temp with saved
    set(todosAtom, get(todosAtom).map(t =>
      t.id === tempId ? { ...savedTodo, pending: false } : t
    ));
  } catch (error) {
    // Rollback
    set(todosAtom, get(todosAtom).filter(t => t.id !== tempId));
  }
});
```

## Best Practices

1. **Define atoms outside components** - Avoid recreating atoms
2. **Use derived atoms** - Compose complex state from primitives
3. **Use utilities** - atomWithStorage, atomFamily, splitAtom
4. **Keep atoms small** - One piece of state per atom
5. **Use Suspense for async** - Or loadable for manual handling

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Creating atoms in components | Define atoms outside components |
| Not wrapping async in Suspense | Add Suspense boundary |
| Mutating objects directly | Return new objects |
| Overusing derived atoms | Keep derivation tree shallow |
| Missing equality functions | Use selectAtom with comparator |

## Reference Files

- [references/utilities.md](references/utilities.md) - Jotai utilities
- [references/async.md](references/async.md) - Async patterns
- [references/integration.md](references/integration.md) - Framework integration
