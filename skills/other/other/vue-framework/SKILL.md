---
name: vue-framework
description: "Build reactive user interfaces with Vue 3 using Composition API, reactive state management, and component-based architecture. Master composables, provide/inject, Pinia state management, and Vue Router. Use for: creating interactive single-page applications, implementing reactive data binding and computed properties, building reusable component libraries, managing complex application state, integrating with TypeScript for type safety, optimizing performance with virtual DOM, and developing progressive web applications with Vue ecosystem tools."
---

# Vue Framework

Build reactive, component-based user interfaces with Vue 3 Composition API and modern tooling.

## Overview

Vue 3 is a progressive JavaScript framework for building user interfaces. The Composition API provides improved code organization, better TypeScript support, and enhanced reusability compared to the Options API. Vue 3 introduces performance improvements, better tree-shaking, and a more flexible reactivity system.

## Composition API Fundamentals

### Setup Function

```vue
<script setup>
import { ref, computed, onMounted } from 'vue';

// Reactive state
const count = ref(0);
const message = ref('Hello Vue!');

// Computed property
const doubleCount = computed(() => count.value * 2);

// Method
function increment() {
  count.value++;
}

// Lifecycle hook
onMounted(() => {
  console.log('Component mounted');
});
</script>

<template>
  <div>
    <p>{{ message }}</p>
    <p>Count: {{ count }}</p>
    <p>Double: {{ doubleCount }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

### Reactive State

```typescript
import { ref, reactive, readonly, shallowRef } from 'vue';

// ref - for primitives and objects
const count = ref(0);
const user = ref({ name: 'John', age: 30 });

// Access/modify with .value
count.value++;
user.value.name = 'Jane';

// reactive - for objects only
const state = reactive({
  count: 0,
  user: { name: 'John' }
});

// Direct access (no .value)
state.count++;
state.user.name = 'Jane';

// readonly - prevent mutations
const readonlyState = readonly(state);

// shallowRef - only top-level reactive
const shallowState = shallowRef({ nested: { value: 1 } });
```

### Computed Properties

```typescript
import { ref, computed } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

// Read-only computed
const fullName = computed(() => `${firstName.value} ${lastName.value}`);

// Writable computed
const fullNameWritable = computed({
  get() {
    return `${firstName.value} ${lastName.value}`;
  },
  set(value) {
    [firstName.value, lastName.value] = value.split(' ');
  }
});
```

### Watchers

```typescript
import { ref, watch, watchEffect } from 'vue';

const count = ref(0);
const user = ref({ name: 'John' });

// Watch single ref
watch(count, (newVal, oldVal) => {
  console.log(`Count changed from ${oldVal} to ${newVal}`);
});

// Watch multiple sources
watch([count, user], ([newCount, newUser], [oldCount, oldUser]) => {
  console.log('Multiple values changed');
});

// Watch object property
watch(
  () => user.value.name,
  (newName) => console.log(`Name: ${newName}`)
);

// watchEffect - auto-tracks dependencies
watchEffect(() => {
  console.log(`Count is ${count.value}`);
});

// Cleanup
const stop = watchEffect(() => {
  // ...
});
stop(); // Stop watching
```

## Component Design

### Props and Emits

```vue
<script setup lang="ts">
interface Props {
  title: string;
  count?: number;
  user: { name: string; age: number };
}

interface Emits {
  (e: 'update', value: number): void;
  (e: 'delete', id: string): void;
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
});

const emit = defineEmits<Emits>();

function handleUpdate() {
  emit('update', props.count + 1);
}
</script>

<template>
  <div>
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
    <button @click="handleUpdate">Update</button>
  </div>
</template>
```

### Slots

```vue
<!-- Parent Component -->
<template>
  <Card>
    <template #header>
      <h2>Card Title</h2>
    </template>
    
    <template #default>
      <p>Card content</p>
    </template>
    
    <template #footer>
      <button>Action</button>
    </template>
  </Card>
</template>

<!-- Card Component -->
<script setup>
defineSlots<{
  header?: () => any;
  default: () => any;
  footer?: () => any;
}>();
</script>

<template>
  <div class="card">
    <div class="card-header">
      <slot name="header" />
    </div>
    <div class="card-body">
      <slot />
    </div>
    <div class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>
```

### Provide/Inject

```typescript
// Parent component
import { provide, ref } from 'vue';

const theme = ref('dark');
provide('theme', theme);

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
}
provide('toggleTheme', toggleTheme);

// Child component (any level deep)
import { inject } from 'vue';

const theme = inject('theme');
const toggleTheme = inject('toggleTheme');
```

## Composables

### Creating Composables

```typescript
// composables/useMouse.ts
import { ref, onMounted, onUnmounted } from 'vue';

export function useMouse() {
  const x = ref(0);
  const y = ref(0);

  function update(event: MouseEvent) {
    x.value = event.pageX;
    y.value = event.pageY;
  }

  onMounted(() => window.addEventListener('mousemove', update));
  onUnmounted(() => window.removeEventListener('mousemove', update));

  return { x, y };
}

// Usage
import { useMouse } from '@/composables/useMouse';

const { x, y } = useMouse();
```

### Composable Patterns

```typescript
// composables/useFetch.ts
import { ref, watchEffect, toValue } from 'vue';

export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  watchEffect(async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await fetch(toValue(url));
      data.value = await response.json();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  });

  return { data, error, loading };
}

// Usage
const { data, error, loading } = useFetch<User>('/api/user');
```

## State Management with Pinia

### Defining Stores

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null);
  const isAuthenticated = ref(false);

  // Getters
  const userName = computed(() => user.value?.name ?? 'Guest');

  // Actions
  async function login(email: string, password: string) {
    const response = await api.login(email, password);
    user.value = response.user;
    isAuthenticated.value = true;
  }

  function logout() {
    user.value = null;
    isAuthenticated.value = false;
  }

  return { user, isAuthenticated, userName, login, logout };
});

// Usage in component
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
userStore.login('email@example.com', 'password');
```

### Store Composition

```typescript
// stores/cart.ts
import { defineStore } from 'pinia';
import { useUserStore } from './user';

export const useCartStore = defineStore('cart', () => {
  const userStore = useUserStore();
  
  const items = ref([]);
  
  async function checkout() {
    if (!userStore.isAuthenticated) {
      throw new Error('Must be logged in');
    }
    // ... checkout logic
  }
  
  return { items, checkout };
});
```

## Vue Router

### Route Configuration

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/users/:id',
      component: () => import('@/views/UserProfile.vue'),
      props: true
    },
    {
      path: '/dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    }
  ]
});

// Navigation guard
router.beforeEach((to, from) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    return { path: '/login' };
  }
});

export default router;
```

### Using Router in Components

```vue
<script setup>
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

// Access params
const userId = route.params.id;

// Navigate
function goToUser(id: string) {
  router.push(`/users/${id}`);
}

// Navigate with query
router.push({ path: '/search', query: { q: 'vue' } });
</script>
```

## Performance Optimization

### v-memo

```vue
<template>
  <div v-for="item in list" :key="item.id" v-memo="[item.id, item.selected]">
    <!-- Only re-renders if id or selected changes -->
    <p>{{ item.name }}</p>
  </div>
</template>
```

### Lazy Loading

```typescript
// Lazy load components
const AsyncComponent = defineAsyncComponent(() =>
  import('./components/Heavy.vue')
);

// With loading/error states
const AsyncComponent = defineAsyncComponent({
  loader: () => import('./Heavy.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: 200,
  timeout: 3000
});
```

### KeepAlive

```vue
<template>
  <KeepAlive :max="10">
    <component :is="currentView" />
  </KeepAlive>
</template>
```

## Using the Reference Files

### When to Read Each Reference

**`/references/composition-api-patterns.md`** — Read when implementing advanced composables, reactive patterns, or complex state logic.

**`/references/pinia-guide.md`** — Read when setting up global state management, store composition, or persistence.

**`/references/performance-optimization.md`** — Read when optimizing rendering, implementing virtual scrolling, or reducing bundle size.

**`/references/testing-guide.md`** — Read when writing component tests, testing composables, or setting up E2E tests.
