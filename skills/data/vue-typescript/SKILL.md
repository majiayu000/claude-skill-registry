---
name: vue-typescript
description: Expert guidance for Vue 3 with TypeScript, Composition API, Pinia state management, and VueUse utilities. Covers typed props, emits, composables, and Vue Router. Use for Vue 3 development, TypeScript integration, and Pinia state management.
---

# Vue + TypeScript Development

Expert guidance for Vue 3 with TypeScript, Composition API, Pinia state management, and VueUse utilities.

## Core Patterns

### Component with TypeScript

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { User } from '@/types';

// Props with TypeScript
interface Props {
  userId: string;
  initialData?: User;
}

const props = withDefaults(defineProps<Props>(), {
  initialData: undefined,
});

// Emits with TypeScript
interface Emits {
  (e: 'update', user: User): void;
  (e: 'delete', id: string): void;
}

const emit = defineEmits<Emits>();

// Reactive state
const user = ref<User | null>(props.initialData ?? null);
const isLoading = ref(false);
const error = ref<string | null>(null);

// Computed
const displayName = computed(() =>
  user.value ? `${user.value.firstName} ${user.value.lastName}` : 'Unknown'
);

// Methods
async function fetchUser() {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await fetch(`/api/users/${props.userId}`);
    user.value = await response.json();
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to fetch user';
  } finally {
    isLoading.value = false;
  }
}

function handleUpdate() {
  if (user.value) {
    emit('update', user.value);
  }
}

// Lifecycle
onMounted(() => {
  if (!props.initialData) {
    fetchUser();
  }
});

// Expose for template refs
defineExpose({ fetchUser });
</script>

<template>
  <div class="user-card">
    <div v-if="isLoading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="user" class="content">
      <h2>{{ displayName }}</h2>
      <p>{{ user.email }}</p>
      <button @click="handleUpdate">Update</button>
      <button @click="emit('delete', user.id)">Delete</button>
    </div>
  </div>
</template>
```

### Pinia Store with TypeScript

```typescript
// stores/user.ts
import { defineStore } from 'pinia';
import type { User } from '@/types';

interface UserState {
  currentUser: User | null;
  users: User[];
  isLoading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    currentUser: null,
    users: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => state.currentUser !== null,
    getUserById: (state) => {
      return (id: string) => state.users.find(u => u.id === id);
    },
    activeUsers: (state) => state.users.filter(u => u.isActive),
  },

  actions: {
    async fetchUsers() {
      this.isLoading = true;
      this.error = null;

      try {
        const response = await fetch('/api/users');
        this.users = await response.json();
      } catch (e) {
        this.error = e instanceof Error ? e.message : 'Failed to fetch';
      } finally {
        this.isLoading = false;
      }
    },

    async login(email: string, password: string) {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) throw new Error('Login failed');

      this.currentUser = await response.json();
    },

    logout() {
      this.currentUser = null;
    },
  },
});

// Setup store syntax (alternative)
export const useUserStoreSetup = defineStore('user-setup', () => {
  const currentUser = ref<User | null>(null);
  const isAuthenticated = computed(() => currentUser.value !== null);

  async function login(email: string, password: string) {
    // ... implementation
  }

  return { currentUser, isAuthenticated, login };
});
```

### Composables with TypeScript

```typescript
// composables/useFetch.ts
import { ref, unref, watchEffect } from 'vue';
import type { Ref, MaybeRef } from 'vue';

interface UseFetchOptions<T> {
  immediate?: boolean;
  initialData?: T;
  onError?: (error: Error) => void;
}

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  isLoading: Ref<boolean>;
  execute: () => Promise<void>;
}

export function useFetch<T>(
  url: MaybeRef<string>,
  options: UseFetchOptions<T> = {}
): UseFetchReturn<T> {
  const { immediate = true, initialData = null, onError } = options;

  const data = ref<T | null>(initialData) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(false);

  async function execute() {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(unref(url));
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
      onError?.(error.value);
    } finally {
      isLoading.value = false;
    }
  }

  if (immediate) {
    watchEffect(() => {
      execute();
    });
  }

  return { data, error, isLoading, execute };
}

// Usage in component
const { data: users, isLoading, error, execute: refetch } = useFetch<User[]>('/api/users');
```

### VueUse Integration

```typescript
import {
  useLocalStorage,
  useDark,
  useToggle,
  useDebounce,
  onClickOutside,
  useIntersectionObserver,
} from '@vueuse/core';

// Persistent state
const preferences = useLocalStorage('user-prefs', {
  theme: 'light',
  language: 'en',
});

// Dark mode
const isDark = useDark();
const toggleDark = useToggle(isDark);

// Debounced search
const searchQuery = ref('');
const debouncedQuery = useDebounce(searchQuery, 300);

// Click outside
const dropdownRef = ref<HTMLElement | null>(null);
onClickOutside(dropdownRef, () => {
  isOpen.value = false;
});

// Infinite scroll
const loadMoreRef = ref<HTMLElement | null>(null);
useIntersectionObserver(loadMoreRef, ([{ isIntersecting }]) => {
  if (isIntersecting) {
    loadMoreItems();
  }
});
```

## Vue Router with TypeScript

```typescript
// router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/users/:id',
    name: 'user',
    component: () => import('@/views/UserDetail.vue'),
    props: true,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else {
    next();
  }
});
```

## Type Definitions

```typescript
// types/index.ts
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  isActive: boolean;
  createdAt: string;
}

export interface ApiResponse<T> {
  data: T;
  meta: {
    page: number;
    total: number;
  };
}

// Typed provide/inject
import type { InjectionKey } from 'vue';

export const UserServiceKey: InjectionKey<UserService> = Symbol('UserService');

// In parent
provide(UserServiceKey, userService);

// In child
const userService = inject(UserServiceKey)!;
```

## Best Practices

| Practice | Implementation |
|----------|----------------|
| **Props typing** | Use `defineProps<Props>()` with interface |
| **Emits typing** | Use `defineEmits<Emits>()` with interface |
| **Ref typing** | `ref<Type>(initialValue)` |
| **Composables** | Return typed objects, use `MaybeRef` for flexibility |
| **Store typing** | Define state interface, use typed getters |

## When to Use

- Building Vue 3 applications with TypeScript
- Creating composable libraries
- Implementing complex state management with Pinia
- Projects requiring type safety
- Teams familiar with Vue ecosystem

## Notes

- Vue 3 Composition API is recommended
- Pinia is the official state management solution
- VueUse provides 200+ composables
- Script setup syntax reduces boilerplate
