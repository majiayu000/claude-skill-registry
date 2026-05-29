---
name: nanostores
description: Manages state with Nanostores using atoms, maps, computed stores, and framework integrations. Use when building framework-agnostic state, sharing state between islands/components, or needing tiny bundle size.
---

# Nanostores

Tiny state manager (265-797 bytes) for React, Vue, Svelte, Solid, Angular, and vanilla JS with atomic stores.

## Quick Start

**Install:**
```bash
npm install nanostores
# Framework integrations
npm install @nanostores/react    # React/Preact
npm install @nanostores/vue      # Vue 3
npm install @nanostores/solid    # Solid
```

**Create stores:**
```typescript
// stores/counter.ts
import { atom } from 'nanostores';

export const $counter = atom(0);

// stores/user.ts
import { map } from 'nanostores';

interface User {
  name: string;
  email: string;
  role: 'admin' | 'user';
}

export const $user = map<User>({
  name: 'Guest',
  email: '',
  role: 'user',
});
```

**Use in React:**
```tsx
import { useStore } from '@nanostores/react';
import { $counter, $user } from './stores';

function Counter() {
  const count = useStore($counter);

  return (
    <button onClick={() => $counter.set(count + 1)}>
      Count: {count}
    </button>
  );
}

function Profile() {
  const user = useStore($user);

  return (
    <div>
      <p>{user.name}</p>
      <button onClick={() => $user.setKey('name', 'John')}>
        Change Name
      </button>
    </div>
  );
}
```

## Store Types

### Atom - Primitive Values

```typescript
import { atom } from 'nanostores';

// Simple counter
export const $count = atom(0);

// With TypeScript type
export const $status = atom<'idle' | 'loading' | 'error'>('idle');

// Usage
$count.get();           // Read: 0
$count.set(5);          // Write
$count.set(n => n + 1); // Update function
```

### Map - Object State

```typescript
import { map } from 'nanostores';

interface Settings {
  theme: 'light' | 'dark';
  language: string;
  notifications: boolean;
}

export const $settings = map<Settings>({
  theme: 'light',
  language: 'en',
  notifications: true,
});

// Update single key (efficient)
$settings.setKey('theme', 'dark');

// Replace entire object
$settings.set({ theme: 'dark', language: 'fr', notifications: false });

// Listen to specific key changes
$settings.listenKeys(['theme'], (value, oldValue, changedKey) => {
  console.log(`${changedKey} changed to ${value[changedKey]}`);
});
```

### Computed - Derived State

```typescript
import { atom, computed } from 'nanostores';

export const $items = atom<Item[]>([]);
export const $filter = atom<'all' | 'active' | 'completed'>('all');

// Single dependency
export const $itemCount = computed($items, items => items.length);

// Multiple dependencies
export const $filteredItems = computed(
  [$items, $filter],
  (items, filter) => {
    if (filter === 'all') return items;
    return items.filter(item =>
      filter === 'completed' ? item.done : !item.done
    );
  }
);

// Chained computations
export const $activeCount = computed($filteredItems, items =>
  items.filter(i => !i.done).length
);
```

### Batched - Debounced Computed

```typescript
import { atom, batched } from 'nanostores';

const $page = atom(1);
const $sort = atom('date');
const $category = atom('all');

// Waits for event loop tick before recalculating
// Prevents multiple API calls when multiple deps change
export const $apiUrl = batched(
  [$page, $sort, $category],
  (page, sort, category) =>
    `/api/items?page=${page}&sort=${sort}&category=${category}`
);
```

## Framework Integration

### React/Preact

```tsx
import { useStore } from '@nanostores/react';

function Component() {
  const count = useStore($counter);
  const user = useStore($user);

  // Actions are just function calls - no dispatch needed
  const increment = () => $counter.set(count + 1);
  const updateName = (name: string) => $user.setKey('name', name);

  return <div>{count} - {user.name}</div>;
}
```

### Vue 3

```vue
<script setup>
import { useStore } from '@nanostores/vue';
import { $counter, $user } from './stores';

const counter = useStore($counter);
const user = useStore($user);
</script>

<template>
  <div>
    <p>{{ counter }}</p>
    <p>{{ user.name }}</p>
    <button @click="$counter.set(counter + 1)">Increment</button>
  </div>
</template>
```

### Svelte

```svelte
<script>
  import { $counter, $user } from './stores';
</script>

<!-- Use $ prefix for auto-subscription -->
<p>Count: {$counter}</p>
<p>User: {$user.name}</p>
<button on:click={() => $counter.set($counter + 1)}>
  Increment
</button>
```

### Solid

```tsx
import { useStore } from '@nanostores/solid';

function Component() {
  const counter = useStore($counter);
  const user = useStore($user);

  return (
    <div>
      <p>{counter()}</p>
      <p>{user().name}</p>
    </div>
  );
}
```

### Vanilla JS

```typescript
// Subscribe with immediate callback
const unsubscribe = $counter.subscribe(value => {
  document.getElementById('count').textContent = String(value);
});

// Listen only to changes (no immediate callback)
const unlisten = $counter.listen(value => {
  console.log('Changed to:', value);
});

// Cleanup
unsubscribe();
unlisten();
```

## Lifecycle & Async

### onMount - Lazy Initialization

```typescript
import { atom, onMount } from 'nanostores';

export const $users = atom<User[]>([]);

// Only runs when first subscriber attaches
onMount($users, () => {
  // Fetch data
  fetchUsers().then(users => $users.set(users));

  // Return cleanup function
  return () => {
    // Runs when last subscriber detaches
    console.log('Store disabled');
  };
});
```

### Task Tracking

```typescript
import { atom, onMount, task, allTasks } from 'nanostores';

export const $data = atom<Data | null>(null);

onMount($data, () => {
  // Mark async operation for tracking
  task(async () => {
    const data = await fetchData();
    $data.set(data);
  });
});

// Wait for all tasks (useful in SSR)
await allTasks();
```

### Effect - Side Effects

```typescript
import { atom, effect } from 'nanostores';

const $enabled = atom(false);
const $interval = atom(1000);

// Runs when dependencies change, with cleanup
const cleanup = effect([$enabled, $interval], (enabled, ms) => {
  if (!enabled) return;

  const id = setInterval(() => console.log('tick'), ms);
  return () => clearInterval(id);
});

// Later: cleanup();
```

## Events & Interception

### onSet - Validate/Transform

```typescript
import { atom, onSet } from 'nanostores';

const $email = atom('');

onSet($email, ({ newValue, abort }) => {
  // Validate
  if (!newValue.includes('@')) {
    abort(); // Prevent update
    return;
  }

  // Can't modify, but can abort
});
```

### onNotify - Control Notifications

```typescript
import { atom, onNotify } from 'nanostores';

const $data = atom(null);

onNotify($data, ({ abort }) => {
  // Prevent subscriber notifications
  if (shouldSkip()) abort();
});
```

## Astro Islands

Nanostores is the recommended solution for sharing state between Astro islands.

```typescript
// stores/cart.ts
import { atom, map } from 'nanostores';

export const $isCartOpen = atom(false);
export const $cartItems = map<Record<string, CartItem>>({});

export function addToCart(item: CartItem) {
  $cartItems.setKey(item.id, {
    ...item,
    quantity: ($cartItems.get()[item.id]?.quantity || 0) + 1,
  });
}
```

```astro
---
// React island
import AddToCartButton from './AddToCartButton';
// Vue island
import CartFlyout from './CartFlyout.vue';
---

<AddToCartButton client:load item={product} />
<CartFlyout client:load />
```

## Testing

```typescript
import { keepMount, cleanStores } from 'nanostores';
import { $user, $settings } from './stores';

afterEach(() => {
  cleanStores($user, $settings);
});

it('updates user name', () => {
  keepMount($user); // Force mount without subscribers

  $user.setKey('name', 'Alice');

  expect($user.get().name).toBe('Alice');
});

it('computes derived state', async () => {
  keepMount($items);
  keepMount($filteredItems);

  $items.set([{ id: 1, done: false }]);
  $filter.set('active');

  expect($filteredItems.get()).toHaveLength(1);
});
```

## Best Practices

1. **Naming convention** - Prefix stores with `$` for clarity
2. **Keep stores small** - Many small atoms > one large store
3. **Use computed** - Derive state instead of duplicating
4. **Lazy loading** - Use onMount for async initialization
5. **Framework agnostic** - Define stores outside components

## Common Patterns

### Action Functions

```typescript
// stores/todos.ts
export const $todos = atom<Todo[]>([]);

export function addTodo(text: string) {
  $todos.set([
    ...$todos.get(),
    { id: crypto.randomUUID(), text, done: false }
  ]);
}

export function toggleTodo(id: string) {
  $todos.set(
    $todos.get().map(todo =>
      todo.id === id ? { ...todo, done: !todo.done } : todo
    )
  );
}
```

### Store Factory

```typescript
import { atom, onMount } from 'nanostores';

function createResourceStore<T>(fetcher: () => Promise<T>) {
  const $data = atom<T | null>(null);
  const $loading = atom(false);
  const $error = atom<Error | null>(null);

  onMount($data, () => {
    $loading.set(true);
    fetcher()
      .then(data => $data.set(data))
      .catch(err => $error.set(err))
      .finally(() => $loading.set(false));
  });

  return { $data, $loading, $error };
}

export const users = createResourceStore(() => fetch('/api/users').then(r => r.json()));
```

## Reference Files

- [references/persistent.md](references/persistent.md) - localStorage persistence
- [references/router.md](references/router.md) - SPA routing
