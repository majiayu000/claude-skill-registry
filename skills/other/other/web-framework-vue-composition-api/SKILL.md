---
name: web-framework-vue-composition-api
description: Vue 3 Composition API patterns, reactivity primitives, composables, lifecycle hooks
---

# Vue 3 Composition API

> **Quick Guide:** Use `<script setup>` for cleaner components. `ref()` for primitives, `reactive()` for objects. Extract reusable logic into composables (`use*` functions). Clean up side effects in `onUnmounted`. Use `defineProps`, `defineEmits`, `defineExpose` for component interfaces.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `<script setup>` syntax for all new Vue components)**

**(You MUST clean up all side effects (timers, listeners, subscriptions) in `onUnmounted`)**

**(You MUST use `ref()` for primitives and `reactive()` for objects - access ref values via `.value`)**

**(You MUST prefix all composable functions with `use` following Vue conventions)**

**(You MUST use `defineExpose()` to expose methods/properties to parent components)**

</critical_requirements>

---

**Auto-detection:** Vue 3 Composition API, script setup, ref, reactive, computed, watch, watchEffect, composables, onMounted, onUnmounted, defineProps, defineEmits, defineExpose, defineModel, useTemplateRef, useId, onWatcherCleanup, provide, inject, Suspense

**When to use:**

- Building Vue 3 components using Composition API
- Creating reusable composables (use\* functions)
- Managing reactive state with ref/reactive
- Handling component lifecycle and side effects
- TypeScript integration with Vue components

**Key patterns covered:**

- Script setup syntax and compiler macros
- Reactivity primitives (ref, reactive, computed, watch, watchEffect)
- Lifecycle hooks (onMounted, onUnmounted, onUpdated)
- Composables pattern for logic reuse
- Template refs with useTemplateRef() (Vue 3.5+)
- defineModel() for v-model binding (Vue 3.4+)
- useId() for SSR-safe unique IDs (Vue 3.5+)
- Provide/Inject for dependency injection
- Async components and Suspense

**When NOT to use:**

- Simple components where Options API is cleaner
- Components that don't benefit from logic extraction
- When team has no Composition API experience (consider gradual adoption)

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

The Composition API enables organizing code by **logical concern** rather than by option type (data, methods, computed). This makes complex components more maintainable and enables powerful logic reuse through composables. Code is naturally TypeScript-friendly with minimal type annotations needed.

**Core principles:**

1. **Composition over configuration** - Group related logic together instead of splitting across options
2. **Explicit reactivity** - State is explicitly reactive via `ref()` and `reactive()`
3. **Logic reuse via composables** - Extract and share stateful logic between components
4. **TypeScript-first** - Types flow naturally without excessive annotations

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Script Setup Syntax

Use `<script setup>` for cleaner, more concise components. Variables and imports are automatically exposed to the template.

#### Basic Structure

```vue
<script setup lang="ts">
import { ref, computed } from "vue";
import type { User } from "@/types";

// Props and emits
const props = defineProps<{
  userId: string;
  initialCount?: number;
}>();

const emit = defineEmits<{
  update: [value: number];
  submit: [];
}>();

// Reactive state
const count = ref(props.initialCount ?? 0);
const user = ref<User | null>(null);

// Computed values
const doubleCount = computed(() => count.value * 2);

// Methods
function increment() {
  count.value++;
  emit("update", count.value);
}
</script>

<template>
  <div>
    <p>Count: {{ count }} (Double: {{ doubleCount }})</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

**Why good:** All variables/functions automatically available in template, no explicit return needed, cleaner syntax with less boilerplate, TypeScript types flow naturally, named exports from imports work directly

---

### Pattern 2: Reactivity Primitives

Use `ref()` for primitives and `reactive()` for objects. Access ref values via `.value` in script, automatic unwrapping in templates.

#### ref() for Primitives

```typescript
import { ref } from "vue";

const MAX_COUNT = 100;

// ✅ Good Example - ref for primitives
const count = ref(0);
const name = ref("");
const isLoading = ref(false);

// Access/modify via .value
count.value++;
console.log(count.value); // 1

// Compare against named constants
if (count.value >= MAX_COUNT) {
  count.value = MAX_COUNT;
}
```

**Why good:** Reactivity is explicit and trackable, primitives can be passed by reference, `.value` makes reactive access obvious, template unwraps automatically

#### reactive() for Objects

```typescript
import { reactive } from "vue";

// ✅ Good Example - reactive for objects
const state = reactive({
  user: null as User | null,
  settings: {
    theme: "light",
    notifications: true,
  },
});

// Direct property access (no .value)
state.user = fetchedUser;
state.settings.theme = "dark";
```

**Why good:** Deep reactivity by default, no `.value` needed for property access, intuitive object manipulation, nested properties are reactive

#### computed() for Derived State

```typescript
import { ref, computed } from "vue";

const firstName = ref("John");
const lastName = ref("Doe");

// ✅ Read-only computed
const fullName = computed(() => `${firstName.value} ${lastName.value}`);

// ✅ Writable computed
const fullNameWritable = computed({
  get: () => `${firstName.value} ${lastName.value}`,
  set: (value: string) => {
    const [first, last] = value.split(" ");
    firstName.value = first;
    lastName.value = last ?? "";
  },
});
```

**Why good:** Cached until dependencies change, clearly expresses derived state, supports both read-only and writable patterns

---

### Pattern 3: Watch and WatchEffect

Use `watch()` when you need access to previous values or explicit sources. Use `watchEffect()` for automatic dependency tracking.

#### watch() Pattern

```typescript
import { ref, watch } from "vue";

const searchQuery = ref("");
const results = ref<SearchResult[]>([]);

const DEBOUNCE_DELAY_MS = 300;

// ✅ Watch specific source with old/new values
watch(
  searchQuery,
  async (newQuery, oldQuery) => {
    if (newQuery !== oldQuery && newQuery.length > 0) {
      results.value = await searchApi(newQuery);
    }
  },
  {
    immediate: false, // Don't run on mount (default)
  },
);

// ✅ Watch multiple sources
watch([firstName, lastName], ([newFirst, newLast], [oldFirst, oldLast]) => {
  console.log(
    `Name changed from ${oldFirst} ${oldLast} to ${newFirst} ${newLast}`,
  );
});

// ✅ Watch reactive object property (use getter)
const state = reactive({ count: 0 });
watch(
  () => state.count, // Getter required for reactive properties
  (newCount) => console.log(`Count is now ${newCount}`),
);
```

**Why good:** Explicit about what's being watched, access to old values for comparison, lazy by default (runs on change, not mount)

#### watchEffect() Pattern

```typescript
import { ref, watchEffect } from "vue";

const userId = ref<string | null>(null);
const userData = ref<User | null>(null);

// ✅ Automatic dependency tracking
watchEffect(async () => {
  if (userId.value) {
    userData.value = await fetchUser(userId.value);
  }
});
// Runs immediately, re-runs when userId changes
```

**Why good:** Automatically tracks reactive dependencies, runs immediately, simpler when you don't need old values

#### Cleanup in Watchers

```typescript
import { watch, onWatcherCleanup } from "vue";

const searchQuery = ref("");

watch(searchQuery, async (query) => {
  const controller = new AbortController();

  // ✅ Vue 3.5+ cleanup pattern
  onWatcherCleanup(() => controller.abort());

  try {
    const results = await fetch(`/api/search?q=${query}`, {
      signal: controller.signal,
    });
    // handle results
  } catch (e) {
    if (e.name !== "AbortError") throw e;
  }
});
```

**Why good:** Prevents race conditions, cancels in-flight requests when source changes, clean async handling

---

### Pattern 4: Lifecycle Hooks

Register lifecycle callbacks with `onMounted`, `onUnmounted`, etc. Always clean up side effects.

#### Basic Lifecycle Pattern

```typescript
import { ref, onMounted, onUnmounted } from "vue";

const POLL_INTERVAL_MS = 5000;

export function useDataPolling(fetchFn: () => Promise<void>) {
  const isPolling = ref(false);
  let intervalId: ReturnType<typeof setInterval> | null = null;

  onMounted(() => {
    isPolling.value = true;
    // Initial fetch
    fetchFn();
    // Start polling
    intervalId = setInterval(fetchFn, POLL_INTERVAL_MS);
  });

  onUnmounted(() => {
    // ✅ Always clean up
    isPolling.value = false;
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  });

  return { isPolling };
}
```

**Why good:** Clear setup/teardown pairing, prevents memory leaks, cleanup always runs on unmount

#### Event Listener Pattern

```typescript
import { onMounted, onUnmounted } from "vue";

// ✅ Good Example - Reusable event listener composable
export function useEventListener<K extends keyof WindowEventMap>(
  target: Window,
  event: K,
  callback: (e: WindowEventMap[K]) => void,
) {
  onMounted(() => target.addEventListener(event, callback));
  onUnmounted(() => target.removeEventListener(event, callback));
}

// Usage
const { width, height } = useWindowSize();

export function useWindowSize() {
  const width = ref(window.innerWidth);
  const height = ref(window.innerHeight);

  useEventListener(window, "resize", () => {
    width.value = window.innerWidth;
    height.value = window.innerHeight;
  });

  return { width, height };
}
```

**Why good:** Encapsulates setup/cleanup logic, reusable across components, prevents listener leaks

---

### Pattern 5: Composables

Extract reusable stateful logic into composable functions prefixed with `use`.

#### Composable Structure

```typescript
// composables/use-counter.ts
import { ref, computed } from "vue";

const DEFAULT_INITIAL_VALUE = 0;
const DEFAULT_STEP = 1;

interface UseCounterOptions {
  initialValue?: number;
  step?: number;
  min?: number;
  max?: number;
}

export function useCounter(options: UseCounterOptions = {}) {
  const {
    initialValue = DEFAULT_INITIAL_VALUE,
    step = DEFAULT_STEP,
    min = -Infinity,
    max = Infinity,
  } = options;

  const count = ref(initialValue);

  const isAtMin = computed(() => count.value <= min);
  const isAtMax = computed(() => count.value >= max);

  function increment() {
    if (count.value + step <= max) {
      count.value += step;
    }
  }

  function decrement() {
    if (count.value - step >= min) {
      count.value -= step;
    }
  }

  function reset() {
    count.value = initialValue;
  }

  // ✅ Return object with refs (enables destructuring while keeping reactivity)
  return {
    count,
    isAtMin,
    isAtMax,
    increment,
    decrement,
    reset,
  };
}
```

**Why good:** Encapsulates related state and logic, returns refs for reactivity preservation, configurable via options object, named constants for defaults

#### Composable Usage

```vue
<script setup lang="ts">
import { useCounter } from "@/composables/use-counter";

const MAX_QUANTITY = 99;
const MIN_QUANTITY = 1;

const {
  count: quantity,
  increment,
  decrement,
  isAtMax,
} = useCounter({
  initialValue: 1,
  min: MIN_QUANTITY,
  max: MAX_QUANTITY,
  step: 1,
});
</script>

<template>
  <div>
    <button @click="decrement">-</button>
    <span>{{ quantity }}</span>
    <button @click="increment" :disabled="isAtMax">+</button>
  </div>
</template>
```

**Why good:** Destructuring renames avoid conflicts, reactivity preserved through refs, logic completely encapsulated

#### Async Composable Pattern

```typescript
// composables/use-fetch.ts
import {
  ref,
  toValue,
  watchEffect,
  type MaybeRefOrGetter,
  type Ref,
} from "vue";

interface UseFetchReturn<T> {
  data: Ref<T | null>;
  error: Ref<Error | null>;
  isLoading: Ref<boolean>;
  refetch: () => Promise<void>;
}

export function useFetch<T>(url: MaybeRefOrGetter<string>): UseFetchReturn<T> {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(false);

  async function fetchData() {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(toValue(url));
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      data.value = await response.json();
    } catch (e) {
      error.value = e instanceof Error ? e : new Error(String(e));
    } finally {
      isLoading.value = false;
    }
  }

  // Re-fetch when URL changes
  watchEffect(() => {
    fetchData();
  });

  return {
    data,
    error,
    isLoading,
    refetch: fetchData,
  };
}
```

**Why good:** Accepts refs/getters for reactive URLs, automatic refetch on dependency change, complete loading/error state, explicit refetch capability

---

### Pattern 6: defineModel for v-model (Vue 3.4+)

Use `defineModel()` macro to simplify two-way binding on custom components. Replaces manual `defineProps` + `defineEmits` pattern.

#### Basic defineModel

```vue
<!-- ✅ Good Example - Child component with defineModel -->
<script setup lang="ts">
// defineModel creates both the prop and emit automatically
const model = defineModel<string>();
</script>

<template>
  <input v-model="model" type="text" />
</template>
```

```vue
<!-- Parent component -->
<script setup lang="ts">
import { ref } from "vue";
import TextInput from "./TextInput.vue";

const text = ref("");
</script>

<template>
  <TextInput v-model="text" />
</template>
```

**Why good:** Single line replaces defineProps + defineEmits + manual emit, ref-like API for direct mutation, works directly with native v-model

#### Named Models (Multiple v-models)

```vue
<!-- ✅ Good Example - Multiple v-model bindings -->
<script setup lang="ts">
const firstName = defineModel<string>("firstName");
const lastName = defineModel<string>("lastName");
</script>

<template>
  <input v-model="firstName" placeholder="First name" />
  <input v-model="lastName" placeholder="Last name" />
</template>
```

```vue
<!-- Parent usage -->
<template>
  <UserName v-model:first-name="first" v-model:last-name="last" />
</template>
```

**Why good:** Cleaner than manual prop/emit for multiple bindings, kebab-case in template maps to camelCase in script

#### defineModel with Options

```vue
<script setup lang="ts">
// Required model
const title = defineModel<string>("title", { required: true });

// Model with default
const count = defineModel<number>({ default: 0 });
</script>
```

#### defineModel with Modifiers

```vue
<!-- ✅ Good Example - Handling v-model modifiers -->
<script setup lang="ts">
const [model, modifiers] = defineModel<string>({
  set(value) {
    // Transform value on set based on modifiers
    if (modifiers.capitalize && value) {
      return value.charAt(0).toUpperCase() + value.slice(1);
    }
    return value;
  },
});
</script>

<template>
  <input v-model="model" type="text" />
</template>
```

```vue
<!-- Parent with modifier -->
<template>
  <TextInput v-model.capitalize="text" />
</template>
```

**Why good:** Access to modifiers via destructure, setter transforms value before emit, clean handling of custom modifiers

---

### Pattern 7: Template Refs with useTemplateRef (Vue 3.5+)

Use `useTemplateRef()` for template references, especially for dynamic refs. Falls back to `ref()` pattern for simple static refs.

#### useTemplateRef (Vue 3.5+)

```vue
<script setup lang="ts">
import { useTemplateRef, onMounted } from "vue";

// ✅ Good Example - useTemplateRef for template refs
const inputRef = useTemplateRef<HTMLInputElement>("input");

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<template>
  <input ref="input" type="text" />
</template>
```

**Why good:** String-based ref binding, works with dynamic ref IDs, clearer separation between reactive refs and template refs

#### Traditional ref() Pattern (All Vue 3 versions)

```vue
<script setup lang="ts">
import { ref, onMounted } from "vue";

// ✅ Still valid - ref name matches template ref attribute
const inputRef = ref<HTMLInputElement | null>(null);

onMounted(() => {
  // Focus input on mount
  inputRef.value?.focus();
});

function selectAll() {
  inputRef.value?.select();
}
</script>

<template>
  <input ref="inputRef" type="text" />
  <button @click="selectAll">Select All</button>
</template>
```

**Why good:** Type-safe DOM access, null safety with optional chaining, ref name matches template attribute

#### Component Refs with defineExpose

```vue
<!-- ChildComponent.vue -->
<script setup lang="ts">
import { ref } from "vue";

const count = ref(0);

function increment() {
  count.value++;
}

function reset() {
  count.value = 0;
}

// ✅ Explicitly expose what parent can access
defineExpose({
  count,
  increment,
  reset,
});
</script>
```

```vue
<!-- ParentComponent.vue -->
<script setup lang="ts">
import { ref } from "vue";
import ChildComponent from "./ChildComponent.vue";

const childRef = ref<InstanceType<typeof ChildComponent> | null>(null);

function resetChild() {
  childRef.value?.reset();
}
</script>

<template>
  <ChildComponent ref="childRef" />
  <button @click="resetChild">Reset Child</button>
</template>
```

**Why good:** Script setup components are private by default, explicit public API via defineExpose, type-safe parent access with InstanceType

---

### Pattern 8: useId for Accessible IDs (Vue 3.5+)

Use `useId()` to generate unique IDs for form elements and ARIA attributes. IDs are stable across SSR and client renders.

```vue
<script setup lang="ts">
import { useId } from "vue";

// ✅ Good Example - SSR-safe unique ID for form accessibility
const id = useId();
</script>

<template>
  <div>
    <label :for="id">Email address</label>
    <input :id="id" type="email" />
  </div>
</template>
```

**Why good:** SSR-safe (no hydration mismatch), unique per component instance, multiple calls generate different IDs, replaces manual ID generation

#### Multiple IDs in One Component

```vue
<script setup lang="ts">
import { useId } from "vue";

// Each call generates a different ID
const nameId = useId();
const emailId = useId();
const passwordId = useId();
</script>

<template>
  <form>
    <div>
      <label :for="nameId">Name</label>
      <input :id="nameId" type="text" />
    </div>
    <div>
      <label :for="emailId">Email</label>
      <input :id="emailId" type="email" />
    </div>
    <div>
      <label :for="passwordId">Password</label>
      <input :id="passwordId" type="password" />
    </div>
  </form>
</template>
```

**Why good:** Each call produces unique ID, stable across server/client, no need for uuid libraries

---

### Pattern 10: Provide/Inject Dependency Injection

Share data between ancestor and descendant components without prop drilling.

#### Type-Safe Provide/Inject

```typescript
// injection-keys.ts
import type { InjectionKey, Ref } from "vue";

export interface ThemeContext {
  theme: Ref<"light" | "dark">;
  toggleTheme: () => void;
}

// ✅ Symbol key with type information
export const THEME_KEY: InjectionKey<ThemeContext> = Symbol("theme");
```

```vue
<!-- ThemeProvider.vue -->
<script setup lang="ts">
import { ref, provide } from "vue";
import { THEME_KEY, type ThemeContext } from "@/injection-keys";

const theme = ref<"light" | "dark">("light");

function toggleTheme() {
  theme.value = theme.value === "light" ? "dark" : "light";
}

// ✅ Provide with typed key
provide(THEME_KEY, {
  theme,
  toggleTheme,
});
</script>

<template>
  <div :data-theme="theme">
    <slot />
  </div>
</template>
```

```vue
<!-- ConsumerComponent.vue -->
<script setup lang="ts">
import { inject } from "vue";
import { THEME_KEY } from "@/injection-keys";

// ✅ Type-safe injection with fallback
const themeContext = inject(THEME_KEY);

if (!themeContext) {
  throw new Error("ConsumerComponent must be used within ThemeProvider");
}

const { theme, toggleTheme } = themeContext;
</script>

<template>
  <button @click="toggleTheme">Current: {{ theme }}</button>
</template>
```

**Why good:** InjectionKey provides type safety, Symbol prevents key collisions, explicit error handling for missing providers

---

### Pattern 11: Props and Emits with TypeScript

Use defineProps and defineEmits with TypeScript for type-safe component interfaces.

#### Props with Reactive Destructure (Vue 3.5+) - Recommended

```vue
<script setup lang="ts">
// ✅ Reactive destructure with defaults (Vue 3.5+)
// Props are automatically reactive - no .value needed
const {
  title,
  count = 0,
  items = () => [], // Factory for non-primitive defaults
} = defineProps<{
  title: string;
  count?: number;
  items?: string[];
}>();

// ⚠️ IMPORTANT: Wrap destructured props in getter for watch/composables
watch(
  () => count,
  (newCount) => {
    console.log("Count changed:", newCount);
  },
);
</script>
```

**Why good:** Native JavaScript default syntax, cleaner than withDefaults, automatically reactive in Vue 3.5+

#### Props with withDefaults (Vue 3.4 and below)

```vue
<script setup lang="ts">
interface Props {
  title: string;
  count?: number;
  items?: string[];
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  items: () => [], // Factory function for non-primitives
});
</script>
```

**Why good:** Still works in Vue 3.5+, explicit about defaults, familiar pattern

#### Emits with Validation

```vue
<script setup lang="ts">
// ✅ Named tuple syntax (Vue 3.3+)
const emit = defineEmits<{
  update: [id: string, value: number];
  delete: [id: string];
  submit: [];
}>();

function handleUpdate(id: string, value: number) {
  emit("update", id, value);
}

function handleDelete(id: string) {
  emit("delete", id);
}
</script>
```

**Why good:** Type-safe props and emits, autocomplete in consumers, compile-time validation, self-documenting component API

---

### Pattern 12: Async Components and Suspense

Lazy-load components and handle async operations gracefully.

#### defineAsyncComponent

```typescript
import { defineAsyncComponent } from "vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";
import ErrorDisplay from "@/components/ErrorDisplay.vue";

const LOADING_DELAY_MS = 200;
const LOAD_TIMEOUT_MS = 10000;

// ✅ Async component with loading/error handling
const HeavyChart = defineAsyncComponent({
  loader: () => import("@/components/HeavyChart.vue"),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorDisplay,
  delay: LOADING_DELAY_MS, // Delay before showing loading
  timeout: LOAD_TIMEOUT_MS, // Timeout before showing error
});
```

**Why good:** Code splitting for better initial load, graceful loading states, error handling built-in, prevents loading flicker with delay

#### Suspense with Async Setup

```vue
<!-- AsyncUserProfile.vue -->
<script setup lang="ts">
// Top-level await makes this an async component
const user = await fetchUser(props.userId);
const posts = await fetchUserPosts(props.userId);
</script>

<template>
  <div>
    <h1>{{ user.name }}</h1>
    <PostList :posts="posts" />
  </div>
</template>
```

```vue
<!-- ParentComponent.vue -->
<script setup lang="ts">
import { ref } from "vue";
import AsyncUserProfile from "./AsyncUserProfile.vue";

const userId = ref("123");
</script>

<template>
  <Suspense>
    <template #default>
      <AsyncUserProfile :user-id="userId" />
    </template>
    <template #fallback>
      <LoadingSpinner />
    </template>
  </Suspense>
</template>
```

**Why good:** Declarative loading states, coordinates multiple async dependencies, cleaner than manual loading state management

</patterns>

---

<integration>

## Integration Guide

**Vue Composition API is state and styling agnostic.** Components should accept props for data and emit events for communication. Use `class` attribute for styling.

**Works with:**

- **Vue Router**: Composables like `useRoute()`, `useRouter()` follow same patterns
- **Any CSS solution** via class binding and scoped styles
- **Any HTTP client** via composables wrapping fetch logic

**Component Communication:**

- Props down, events up for parent-child
- Provide/Inject for deep nesting
- External state management decisions are separate from component architecture

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `<script setup>` syntax for all new Vue components)**

**(You MUST clean up all side effects (timers, listeners, subscriptions) in `onUnmounted`)**

**(You MUST use `ref()` for primitives and `reactive()` for objects - access ref values via `.value`)**

**(You MUST prefix all composable functions with `use` following Vue conventions)**

**(You MUST use `defineExpose()` to expose methods/properties to parent components)**

**Failure to follow these rules will cause memory leaks, broken reactivity, and unmaintainable component APIs.**

</critical_reminders>
