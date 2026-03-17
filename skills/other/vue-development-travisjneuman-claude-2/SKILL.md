---
name: vue-development
description: Vue.js 3 development with Composition API, TypeScript, Pinia state management, and Nuxt 3 full-stack. Use when building Vue applications, implementing reactive patterns, creating composables, or working with the Vue ecosystem.
---

# Vue.js 3 Development

Comprehensive guide for building modern Vue.js applications with the Composition API.

## Stack Overview

| Tool       | Purpose              | Version |
| ---------- | -------------------- | ------- |
| Vue 3      | Core framework       | 3.4+    |
| TypeScript | Type safety          | 5.0+    |
| Vite       | Build tool           | 5.0+    |
| Pinia      | State management     | 2.1+    |
| Vue Router | Routing              | 4.2+    |
| Nuxt 3     | Full-stack framework | 3.10+   |
| Vitest     | Testing              | 1.0+    |

---

## Composition API with Script Setup

### Basic Component Structure

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

// Props with TypeScript
interface Props {
  title: string;
  count?: number;
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
});

// Emits with TypeScript
const emit = defineEmits<{
  update: [value: number];
  submit: [];
}>();

// Reactive state
const localCount = ref(props.count);
const items = ref<string[]>([]);

// Computed
const doubleCount = computed(() => localCount.value * 2);

// Methods
function increment() {
  localCount.value++;
  emit("update", localCount.value);
}

// Lifecycle
onMounted(() => {
  console.log("Component mounted");
});
</script>

<template>
  <div class="component">
    <h1>{{ title }}</h1>
    <p>Count: {{ localCount }} (Double: {{ doubleCount }})</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<style scoped>
.component {
  padding: 1rem;
}
</style>
```

### Reactivity Patterns

```typescript
import { ref, reactive, computed, watch, watchEffect } from "vue";

// Primitives: use ref()
const count = ref(0);
const name = ref("");
count.value++; // Access via .value

// Objects/Arrays: use reactive()
const state = reactive({
  items: [] as Item[],
  loading: false,
  error: null as Error | null,
});
state.items.push(item); // Direct access, no .value

// Computed values
const total = computed(() => state.items.reduce((sum, i) => sum + i.price, 0));

// Watch specific values
watch(count, (newVal, oldVal) => {
  console.log(`Count changed: ${oldVal} -> ${newVal}`);
});

// Watch with options
watch(
  () => state.items,
  (newItems) => saveToStorage(newItems),
  { deep: true, immediate: true },
);

// Automatic dependency tracking
watchEffect(() => {
  console.log(`Count is now: ${count.value}`);
});
```

---

## Composables (Reusable Logic)

### Naming & Structure

```
src/
└── composables/
    ├── useFetch.ts
    ├── useLocalStorage.ts
    ├── useDebounce.ts
    └── useAuth.ts
```

**Convention:** Always prefix with `use` (e.g., `useFetch`, `useAuth`)

### Creating Composables

```typescript
// composables/useFetch.ts
import { ref, toValue, watchEffect, type MaybeRefOrGetter } from "vue";

export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function fetchData() {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(toValue(url));
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
    } finally {
      loading.value = false;
    }
  }

  // Auto-refetch when URL changes
  watchEffect(() => {
    fetchData();
  });

  return { data, error, loading, refetch: fetchData };
}

// Usage in component
const { data, error, loading } = useFetch<User[]>("/api/users");

// With reactive URL
const userId = ref(1);
const { data: user } = useFetch(() => `/api/users/${userId.value}`);
```

### Composable Best Practices

```typescript
// composables/useLocalStorage.ts
import { ref, watch, type Ref } from "vue";

export function useLocalStorage<T>(key: string, defaultValue: T): Ref<T> {
  // Read initial value
  const stored = localStorage.getItem(key);
  const value = ref<T>(stored ? JSON.parse(stored) : defaultValue) as Ref<T>;

  // Sync to storage
  watch(
    value,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true },
  );

  return value;
}

// ✅ Good: Accept refs, getters, or plain values
// ✅ Good: Return plain object with refs (not reactive)
// ✅ Good: Clean up in onUnmounted
// ✅ Good: Use toValue() for flexible inputs
```

---

## Pinia State Management

### Store Definition (Composition Style)

```typescript
// stores/user.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface User {
  id: number;
  name: string;
  email: string;
}

export const useUserStore = defineStore("user", () => {
  // State
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters (computed)
  const isLoggedIn = computed(() => !!user.value);
  const displayName = computed(() => user.value?.name ?? "Guest");

  // Actions
  async function login(email: string, password: string) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) throw new Error("Login failed");

      user.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Unknown error";
      throw e;
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    user.value = null;
  }

  return {
    // State
    user,
    loading,
    error,
    // Getters
    isLoggedIn,
    displayName,
    // Actions
    login,
    logout,
  };
});
```

### Using Stores in Components

```vue
<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

// Use storeToRefs for destructuring state/getters
const { user, isLoggedIn, loading } = storeToRefs(userStore);

// Actions can be destructured directly
const { login, logout } = userStore;

async function handleLogin() {
  try {
    await login(email.value, password.value);
    router.push("/dashboard");
  } catch {
    // Error handled in store
  }
}
</script>
```

### Store with Persistence

```typescript
// stores/settings.ts
import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  const theme = ref<"light" | "dark">("light");
  const locale = ref("en");

  // Load from storage on init
  const stored = localStorage.getItem("settings");
  if (stored) {
    const parsed = JSON.parse(stored);
    theme.value = parsed.theme ?? "light";
    locale.value = parsed.locale ?? "en";
  }

  // Persist changes
  watch([theme, locale], () => {
    localStorage.setItem(
      "settings",
      JSON.stringify({
        theme: theme.value,
        locale: locale.value,
      }),
    );
  });

  function toggleTheme() {
    theme.value = theme.value === "light" ? "dark" : "light";
  }

  return { theme, locale, toggleTheme };
});
```

---

## Component Patterns

### Provider/Inject Pattern

```typescript
// context/auth.ts
import { provide, inject, type InjectionKey } from "vue";

interface AuthContext {
  user: Ref<User | null>;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthKey: InjectionKey<AuthContext> = Symbol("auth");

// Provider component
export function provideAuth() {
  const user = ref<User | null>(null);

  async function login(email: string, password: string) {
    // Implementation
  }

  function logout() {
    user.value = null;
  }

  const context = { user, login, logout };
  provide(AuthKey, context);
  return context;
}

// Consumer hook
export function useAuth(): AuthContext {
  const context = inject(AuthKey);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
```

### Smart/Dumb Components

```vue
<!-- components/UserCard.vue (Dumb - Presentational) -->
<script setup lang="ts">
interface Props {
  name: string;
  email: string;
  avatar?: string;
}

defineProps<Props>();
defineEmits<{ click: [] }>();
</script>

<template>
  <div class="user-card" @click="$emit('click')">
    <img :src="avatar ?? '/default-avatar.png'" :alt="name" />
    <h3>{{ name }}</h3>
    <p>{{ email }}</p>
  </div>
</template>
```

```vue
<!-- views/UserList.vue (Smart - Container) -->
<script setup lang="ts">
import { useFetch } from "@/composables/useFetch";
import UserCard from "@/components/UserCard.vue";

const { data: users, loading, error } = useFetch<User[]>("/api/users");

function handleUserClick(user: User) {
  router.push(`/users/${user.id}`);
}
</script>

<template>
  <div class="user-list">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <template v-else>
      <UserCard
        v-for="user in users"
        :key="user.id"
        :name="user.name"
        :email="user.email"
        :avatar="user.avatar"
        @click="handleUserClick(user)"
      />
    </template>
  </div>
</template>
```

---

## Nuxt 3 (Full-Stack)

### Project Structure

```
nuxt-app/
├── pages/              # File-based routing
│   ├── index.vue       # /
│   ├── about.vue       # /about
│   └── users/
│       ├── index.vue   # /users
│       └── [id].vue    # /users/:id
├── components/         # Auto-imported components
├── composables/        # Auto-imported composables
├── server/             # API routes (Nitro)
│   ├── api/
│   │   └── users.ts    # /api/users
│   └── middleware/
├── layouts/            # Page layouts
├── middleware/         # Route middleware
└── nuxt.config.ts
```

### API Routes

```typescript
// server/api/users.ts
export default defineEventHandler(async (event) => {
  const method = getMethod(event);

  if (method === "GET") {
    return await prisma.user.findMany();
  }

  if (method === "POST") {
    const body = await readBody(event);
    return await prisma.user.create({ data: body });
  }
});

// server/api/users/[id].ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");
  return await prisma.user.findUnique({ where: { id: Number(id) } });
});
```

### Data Fetching

```vue
<script setup lang="ts">
// Server-side fetch (SSR)
const { data: users } = await useFetch("/api/users");

// Lazy fetch (client-side)
const { data: posts, pending } = await useLazyFetch("/api/posts");

// With parameters
const route = useRoute();
const { data: user } = await useFetch(`/api/users/${route.params.id}`);
</script>
```

---

## Testing with Vitest

### Setup

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
  },
});

// tests/setup.ts
import { vi } from "vitest";
import "@testing-library/jest-dom/vitest";
```

### Component Testing

```typescript
// tests/components/UserCard.test.ts
import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/vue";
import UserCard from "@/components/UserCard.vue";

describe("UserCard", () => {
  it("renders user information", () => {
    render(UserCard, {
      props: {
        name: "John Doe",
        email: "john@example.com",
      },
    });

    expect(screen.getByText("John Doe")).toBeInTheDocument();
    expect(screen.getByText("john@example.com")).toBeInTheDocument();
  });

  it("emits click event", async () => {
    const { emitted } = render(UserCard, {
      props: { name: "John", email: "john@test.com" },
    });

    await fireEvent.click(screen.getByRole("article"));
    expect(emitted().click).toHaveLength(1);
  });
});
```

### Composable Testing

```typescript
// tests/composables/useFetch.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useFetch } from "@/composables/useFetch";
import { flushPromises } from "@vue/test-utils";

describe("useFetch", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  it("fetches data successfully", async () => {
    const mockData = [{ id: 1, name: "Test" }];
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockData),
    } as Response);

    const { data, loading, error } = useFetch("/api/test");

    expect(loading.value).toBe(true);
    await flushPromises();

    expect(loading.value).toBe(false);
    expect(data.value).toEqual(mockData);
    expect(error.value).toBeNull();
  });

  it("handles errors", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("Network error"));

    const { data, error } = useFetch("/api/test");
    await flushPromises();

    expect(data.value).toBeNull();
    expect(error.value?.message).toBe("Network error");
  });
});
```

---

## Anti-Patterns to Avoid

| Anti-Pattern                             | Problem                         | Solution                 |
| ---------------------------------------- | ------------------------------- | ------------------------ |
| Using Options API for complex components | Poor code organization          | Use Composition API      |
| Mutating props directly                  | Breaks one-way data flow        | Emit events to parent    |
| Using `$refs` for state                  | Not reactive                    | Use `ref()` and props    |
| Deeply nested watchers                   | Performance issues              | Use `computed()` instead |
| Using mixins                             | Name collisions, unclear source | Use composables          |
| Not using `storeToRefs()`                | Loses reactivity on destructure | Always use with Pinia    |

---

## Related Resources

- [Vue.js Official Docs](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Nuxt 3 Documentation](https://nuxt.com/)
- [VueUse Composables](https://vueuse.org/)
- [Vue Test Utils](https://test-utils.vuejs.org/)

---

## When to Use This Skill

- Building new Vue.js 3 applications
- Migrating from Vue 2 Options API to Composition API
- Implementing Pinia state management
- Creating reusable composables
- Full-stack development with Nuxt 3
- Testing Vue components with Vitest
