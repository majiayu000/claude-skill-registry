---
name: pinia
description: Manages Vue state with Pinia including stores, getters, actions, and plugins. Use when building Vue applications needing centralized state, sharing state between components, or replacing Vuex.
---

# Pinia

The intuitive, type safe, and flexible store for Vue.

## Quick Start

**Install:**
```bash
npm install pinia
```

**Setup (main.ts):**
```typescript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

const app = createApp(App);
app.use(createPinia());
app.mount('#app');
```

## Defining Stores

### Option Store (Vue Options API style)

```typescript
// stores/counter.ts
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Counter',
  }),

  getters: {
    doubleCount: (state) => state.count * 2,

    // Getter using other getters
    doubleCountPlusOne(): number {
      return this.doubleCount + 1;
    },
  },

  actions: {
    increment() {
      this.count++;
    },

    async fetchAndSet() {
      const response = await fetch('/api/count');
      const data = await response.json();
      this.count = data.count;
    },
  },
});
```

### Setup Store (Composition API style)

```typescript
// stores/counter.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCounterStore = defineStore('counter', () => {
  // State
  const count = ref(0);
  const name = ref('Counter');

  // Getters
  const doubleCount = computed(() => count.value * 2);

  // Actions
  function increment() {
    count.value++;
  }

  async function fetchAndSet() {
    const response = await fetch('/api/count');
    const data = await response.json();
    count.value = data.count;
  }

  return { count, name, doubleCount, increment, fetchAndSet };
});
```

## Using Stores

### Basic Usage

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter';

const counter = useCounterStore();

// Access state
console.log(counter.count);

// Access getters
console.log(counter.doubleCount);

// Call actions
counter.increment();
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double: {{ counter.doubleCount }}</p>
    <button @click="counter.increment">Increment</button>
  </div>
</template>
```

### Destructuring with storeToRefs

```vue
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useCounterStore } from '@/stores/counter';

const counter = useCounterStore();

// Destructure with reactivity preserved
const { count, doubleCount } = storeToRefs(counter);

// Actions can be destructured directly
const { increment } = counter;
</script>

<template>
  <div>
    <p>{{ count }}</p>
    <button @click="increment">+1</button>
  </div>
</template>
```

## State

### Accessing State

```typescript
const store = useCounterStore();

// Direct access
store.count;

// Via $state
store.$state.count;
```

### Modifying State

```typescript
const store = useCounterStore();

// Direct mutation
store.count++;

// Patch single property
store.$patch({ count: 10 });

// Patch multiple properties
store.$patch({
  count: 10,
  name: 'New Counter',
});

// Patch with function
store.$patch((state) => {
  state.count++;
  state.items.push({ id: 1 });
});

// Replace entire state
store.$state = { count: 0, name: 'Reset' };

// Reset to initial state
store.$reset();
```

## Getters

### Basic Getters

```typescript
export const useProductStore = defineStore('products', {
  state: () => ({
    items: [] as Product[],
  }),

  getters: {
    // Arrow function
    itemCount: (state) => state.items.length,

    // Using this for other getters
    hasItems(): boolean {
      return this.itemCount > 0;
    },

    // Getter with parameter (returns function)
    getById: (state) => {
      return (id: string) => state.items.find(item => item.id === id);
    },
  },
});
```

### Using Other Store Getters

```typescript
import { useUserStore } from './user';

export const useCartStore = defineStore('cart', {
  getters: {
    userCart(): CartItem[] {
      const userStore = useUserStore();
      return this.items.filter(item => item.userId === userStore.currentUserId);
    },
  },
});
```

## Actions

### Basic Actions

```typescript
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null,
  }),

  actions: {
    async login(email: string, password: string) {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });

        const data = await response.json();
        this.user = data.user;
        this.token = data.token;

        return data;
      } catch (error) {
        this.user = null;
        this.token = null;
        throw error;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.$reset();
    },
  },
});
```

### Using Other Stores in Actions

```typescript
import { useNotificationStore } from './notification';

export const useCartStore = defineStore('cart', {
  actions: {
    async checkout() {
      const notificationStore = useNotificationStore();

      try {
        await this.submitOrder();
        notificationStore.show('Order placed!');
      } catch (error) {
        notificationStore.show('Order failed', 'error');
      }
    },
  },
});
```

## Subscribing to Changes

### State Subscription

```typescript
const store = useCounterStore();

// Subscribe to state changes
store.$subscribe((mutation, state) => {
  console.log('State changed:', mutation.type);
  console.log('New state:', state);

  // Persist to localStorage
  localStorage.setItem('counter', JSON.stringify(state));
});

// With options
store.$subscribe(
  (mutation, state) => {
    // ...
  },
  { detached: true } // Survives component unmount
);
```

### Action Subscription

```typescript
const store = useAuthStore();

// Subscribe to actions
store.$onAction(({ name, args, after, onError }) => {
  console.log(`Action ${name} called with:`, args);

  after((result) => {
    console.log(`Action ${name} finished with:`, result);
  });

  onError((error) => {
    console.error(`Action ${name} failed:`, error);
  });
});
```

## Plugins

### Creating a Plugin

```typescript
// plugins/persistedState.ts
import { PiniaPluginContext } from 'pinia';

export function piniaPersistedState({ store }: PiniaPluginContext) {
  // Restore state from localStorage
  const savedState = localStorage.getItem(store.$id);
  if (savedState) {
    store.$patch(JSON.parse(savedState));
  }

  // Subscribe to changes
  store.$subscribe((mutation, state) => {
    localStorage.setItem(store.$id, JSON.stringify(state));
  });
}

// main.ts
const pinia = createPinia();
pinia.use(piniaPersistedState);
```

### Adding Properties to Stores

```typescript
import { markRaw } from 'vue';
import { Router } from 'vue-router';

declare module 'pinia' {
  export interface PiniaCustomProperties {
    router: Router;
  }
}

const pinia = createPinia();
pinia.use(({ store }) => {
  store.router = markRaw(router);
});
```

## TypeScript

### Typed Store

```typescript
interface UserState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isLoading: false,
    error: null,
  }),

  getters: {
    isLoggedIn: (state): boolean => !!state.user,
    fullName(): string {
      return this.user ? `${this.user.firstName} ${this.user.lastName}` : '';
    },
  },

  actions: {
    async fetchUser(id: string): Promise<void> {
      this.isLoading = true;
      try {
        const response = await fetch(`/api/users/${id}`);
        this.user = await response.json();
      } catch (e) {
        this.error = (e as Error).message;
      } finally {
        this.isLoading = false;
      }
    },
  },
});
```

## Testing

```typescript
import { setActivePinia, createPinia } from 'pinia';
import { useCounterStore } from '@/stores/counter';
import { describe, it, expect, beforeEach } from 'vitest';

describe('Counter Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('increments count', () => {
    const counter = useCounterStore();
    expect(counter.count).toBe(0);

    counter.increment();
    expect(counter.count).toBe(1);
  });

  it('computes double count', () => {
    const counter = useCounterStore();
    counter.count = 5;
    expect(counter.doubleCount).toBe(10);
  });
});
```

## Composing Stores

```typescript
// stores/cart.ts
import { useProductStore } from './products';
import { useUserStore } from './user';

export const useCartStore = defineStore('cart', () => {
  const productStore = useProductStore();
  const userStore = useUserStore();

  const items = ref<CartItem[]>([]);

  const total = computed(() => {
    return items.value.reduce((sum, item) => {
      const product = productStore.getById(item.productId);
      return sum + (product?.price ?? 0) * item.quantity;
    }, 0);
  });

  const discountedTotal = computed(() => {
    const discount = userStore.user?.discount ?? 0;
    return total.value * (1 - discount);
  });

  return { items, total, discountedTotal };
});
```

## Best Practices

1. **One store per domain** - User store, cart store, etc.
2. **Use Setup Stores for complex logic** - Better composition
3. **Use storeToRefs for destructuring** - Maintains reactivity
4. **Keep actions async-aware** - Return promises
5. **Use plugins for cross-cutting concerns** - Persistence, logging

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Destructuring state directly | Use storeToRefs() |
| Calling useStore outside setup | Call inside setup or actions |
| Mutating state in getters | Keep getters pure |
| Circular store dependencies | Refactor to avoid cycles |
| Not using $reset | Use it to reset to initial |

## Reference Files

- [references/plugins.md](references/plugins.md) - Plugin patterns
- [references/testing.md](references/testing.md) - Testing stores
- [references/composition.md](references/composition.md) - Store composition
