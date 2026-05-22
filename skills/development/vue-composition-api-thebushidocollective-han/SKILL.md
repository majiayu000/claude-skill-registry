---
name: vue-composition-api
description: Use when Vue 3 Composition API with reactive refs, computed, and composables. Use when building modern Vue 3 applications.
allowed-tools:
  - Bash
  - Read
---

# Vue Composition API

Master the Vue 3 Composition API for building scalable, maintainable
Vue applications with better code organization and reusability.

## Setup Function Fundamentals

The `setup()` function is the entry point for using the Composition API:

```typescript
import { ref, computed, onMounted } from 'vue';

export default {
  props: ['initialCount'],
  setup(props, context) {
    // props is reactive
    console.log(props.initialCount);

    // context provides attrs, slots, emit, expose
    const { attrs, slots, emit, expose } = context;

    const count = ref(0);
    const doubled = computed(() => count.value * 2);

    function increment() {
      count.value++;
      emit('update', count.value);
    }

    onMounted(() => {
      console.log('Component mounted');
    });

    // Expose public methods
    expose({ increment });

    // Return values to template
    return {
      count,
      doubled,
      increment
    };
  }
};
```

## Script Setup Syntax

Modern Vue 3 uses `<script setup>` for cleaner syntax:

```typescript
<script setup lang="ts">
import { ref, computed } from 'vue';

// Top-level bindings automatically exposed to template
const count = ref(0);
const doubled = computed(() => count.value * 2);

function increment() {
  count.value++;
}

// Props and emits use compiler macros
interface Props {
  initialCount?: number;
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 0
});

const emit = defineEmits<{
  update: [value: number];
}>();
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

## Ref vs Reactive - When to Use Each

### Use Ref For

```typescript
import { ref } from 'vue';

// Primitives
const count = ref(0);
const name = ref('John');
const isActive = ref(true);

// Single object that needs replacement
const user = ref({ name: 'John', age: 30 });
user.value = { name: 'Jane', age: 25 }; // Works

// Arrays that need replacement
const items = ref([1, 2, 3]);
items.value = [4, 5, 6]; // Works
```

### Use Reactive For

```typescript
import { reactive, toRefs } from 'vue';

// Complex nested objects
const state = reactive({
  user: { name: 'John', age: 30 },
  settings: { theme: 'dark', notifications: true },
  posts: []
});

// Group related state
const formState = reactive({
  name: '',
  email: '',
  password: '',
  errors: {}
});

// Convert to refs for destructuring
const { name, email } = toRefs(formState);
```

### Avoid Reactive For

```typescript
// DON'T: Replacing entire reactive object loses reactivity
let state = reactive({ count: 0 });
state = reactive({ count: 1 }); // Breaks reactivity!

// DO: Use ref instead
const state = ref({ count: 0 });
state.value = { count: 1 }; // Works
```

## Computed Properties Patterns

### Basic Computed

```typescript
import { ref, computed } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`;
});
```

### Writable Computed

```typescript
const fullName = computed({
  get() {
    return `${firstName.value} ${lastName.value}`;
  },
  set(value) {
    const names = value.split(' ');
    firstName.value = names[0] || '';
    lastName.value = names[1] || '';
  }
});

// Can now set
fullName.value = 'Jane Smith';
```

### Computed with Complex Logic

```typescript
interface Product {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

const cart = ref<Product[]>([]);

const cartSummary = computed(() => {
  const total = cart.value.reduce((sum, item) =>
    sum + (item.price * item.quantity), 0
  );

  const itemCount = cart.value.reduce((sum, item) =>
    sum + item.quantity, 0
  );

  const tax = total * 0.08;
  const grandTotal = total + tax;

  return {
    total,
    itemCount,
    tax,
    grandTotal
  };
});
```

## Watch and WatchEffect

### Watch - Explicit Dependencies

```typescript
import { ref, watch } from 'vue';

const count = ref(0);
const name = ref('');

// Watch single source
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`);
});

// Watch multiple sources
watch(
  [count, name],
  ([newCount, newName], [oldCount, oldName]) => {
    console.log('Multiple values changed');
  }
);

// Watch reactive object property
const user = reactive({ name: 'John', age: 30 });

watch(
  () => user.name,
  (newName) => {
    console.log(`Name changed to ${newName}`);
  }
);

// Deep watch
watch(
  user,
  (newUser) => {
    console.log('User changed:', newUser);
  },
  { deep: true }
);
```

### WatchEffect - Auto Tracking

```typescript
import { ref, watchEffect } from 'vue';

const count = ref(0);
const multiplier = ref(2);

// Automatically tracks dependencies
watchEffect(() => {
  console.log(`Result: ${count.value * multiplier.value}`);
});

// Runs immediately and whenever dependencies change
```

### Advanced Watch Options

```typescript
const data = ref(null);

watch(
  source,
  (newValue, oldValue) => {
    // Callback logic
  },
  {
    immediate: true,      // Run immediately
    deep: true,           // Deep watch objects
    flush: 'post',        // Timing: 'pre' | 'post' | 'sync'
    onTrack(e) {          // Debug
      console.log('tracked', e);
    },
    onTrigger(e) {        // Debug
      console.log('triggered', e);
    }
  }
);

// Stop watching
const stop = watch(source, callback);
stop(); // Cleanup
```

## Lifecycle Hooks in Composition API

```typescript
import {
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured,
  onActivated,
  onDeactivated
} from 'vue';

export default {
  setup() {
    onBeforeMount(() => {
      console.log('Before mount');
    });

    onMounted(() => {
      console.log('Mounted');
      // DOM is available
      // Setup event listeners, fetch data
    });

    onBeforeUpdate(() => {
      console.log('Before update');
    });

    onUpdated(() => {
      console.log('Updated');
      // DOM has been updated
    });

    onBeforeUnmount(() => {
      console.log('Before unmount');
      // Cleanup before unmount
    });

    onUnmounted(() => {
      console.log('Unmounted');
      // Final cleanup
    });

    onErrorCaptured((err, instance, info) => {
      console.error('Error captured:', err, info);
      return false; // Stop propagation
    });

    // For components wrapped in <KeepAlive>
    onActivated(() => {
      console.log('Component activated');
    });

    onDeactivated(() => {
      console.log('Component deactivated');
    });
  }
};
```

## Composables - Reusable Composition Functions

### Simple Composable

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue';

export function useCounter(initialValue = 0) {
  const count = ref(initialValue);
  const doubled = computed(() => count.value * 2);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  function reset() {
    count.value = initialValue;
  }

  return {
    count: readonly(count),
    doubled,
    increment,
    decrement,
    reset
  };
}

// Usage
<script setup lang="ts">
import { useCounter } from '@/composables/useCounter';

const { count, doubled, increment, decrement } = useCounter(10);
</script>
```

### Advanced Composable with Side Effects

```typescript
// composables/useFetch.ts
import { ref, unref, watchEffect } from 'vue';
import type { Ref } from 'vue';

export function useFetch<T>(url: Ref<string> | string) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function fetchData() {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(unref(url));
      if (!response.ok) throw new Error('Fetch failed');
      data.value = await response.json();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  watchEffect(() => {
    fetchData();
  });

  return {
    data: readonly(data),
    error: readonly(error),
    loading: readonly(loading),
    refetch: fetchData
  };
}

// Usage
<script setup lang="ts">
import { ref } from 'vue';
import { useFetch } from '@/composables/useFetch';

const userId = ref('1');
const url = computed(() => `/api/users/${userId.value}`);
const { data, error, loading, refetch } = useFetch(url);
</script>
```

### Composable with Cleanup

```typescript
// composables/useEventListener.ts
import { onMounted, onUnmounted } from 'vue';

export function useEventListener(
  target: EventTarget,
  event: string,
  handler: (e: Event) => void
) {
  onMounted(() => {
    target.addEventListener(event, handler);
  });

  onUnmounted(() => {
    target.removeEventListener(event, handler);
  });
}

// Usage
<script setup lang="ts">
import { useEventListener } from '@/composables/useEventListener';

useEventListener(window, 'resize', () => {
  console.log('Window resized');
});
</script>
```

## Props and Emits in Composition API

### TypeScript Props

```typescript
<script setup lang="ts">
interface Props {
  title: string;
  count?: number;
  items: string[];
  user: {
    name: string;
    email: string;
  };
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
});

// Access props
console.log(props.title);
console.log(props.count);

// Destructuring loses reactivity - use toRefs
import { toRefs } from 'vue';
const { title, count } = toRefs(props);
</script>
```

### TypeScript Emits

```typescript
<script setup lang="ts">
// Type-safe emits
const emit = defineEmits<{
  update: [value: number];
  delete: [];
  change: [id: string, value: string];
}>();

function handleUpdate() {
  emit('update', 42);
}

function handleChange(id: string, value: string) {
  emit('change', id, value);
}
</script>
```

### Runtime Props Validation

```typescript
<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0,
    validator: (value: number) => value >= 0
  },
  status: {
    type: String as PropType<'active' | 'inactive'>,
    default: 'active'
  }
});
</script>
```

## Provide and Inject Patterns

### Basic Provide/Inject

```typescript
<!-- Parent Component -->
<script setup lang="ts">
import { provide, ref } from 'vue';

const theme = ref('dark');
const updateTheme = (newTheme: string) => {
  theme.value = newTheme;
};

provide('theme', { theme, updateTheme });
</script>

<!-- Child Component (any depth) -->
<script setup lang="ts">
import { inject } from 'vue';

const themeContext = inject('theme');
// themeContext.theme
// themeContext.updateTheme('light')
</script>
```

### Type-Safe Provide/Inject

```typescript
// keys.ts
import type { InjectionKey, Ref } from 'vue';

export interface ThemeContext {
  theme: Ref<string>;
  updateTheme: (theme: string) => void;
}

export const ThemeKey: InjectionKey<ThemeContext> =
  Symbol('theme');

// Provider
<script setup lang="ts">
import { provide, ref } from 'vue';
import { ThemeKey } from './keys';

const theme = ref('dark');
const updateTheme = (newTheme: string) => {
  theme.value = newTheme;
};

provide(ThemeKey, { theme, updateTheme });
</script>

// Consumer
<script setup lang="ts">
import { inject } from 'vue';
import { ThemeKey } from './keys';

const theme = inject(ThemeKey);
// Fully typed!
</script>
```

### Provide with Default Values

```typescript
<script setup lang="ts">
import { inject } from 'vue';

const theme = inject('theme', {
  theme: ref('light'),
  updateTheme: () => {}
});

// Or use factory function for reactive defaults
const config = inject('config', () => reactive({
  locale: 'en',
  timezone: 'UTC'
}), true); // true = treat as factory
</script>
```

## TypeScript with Composition API

### Component with Full Types

```typescript
<script setup lang="ts">
import { ref, computed, type Ref, type ComputedRef } from 'vue';

interface User {
  id: number;
  name: string;
  email: string;
}

interface Props {
  userId: number;
}

interface Emits {
  (e: 'update', user: User): void;
  (e: 'delete', id: number): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const user: Ref<User | null> = ref(null);
const isLoading = ref(false);

const userName: ComputedRef<string> = computed(() =>
  user.value?.name ?? 'Unknown'
);

async function loadUser() {
  isLoading.value = true;
  try {
    const response = await fetch(`/api/users/${props.userId}`);
    user.value = await response.json();
  } finally {
    isLoading.value = false;
  }
}

function updateUser(updates: Partial<User>) {
  if (user.value) {
    user.value = { ...user.value, ...updates };
    emit('update', user.value);
  }
}
</script>
```

### Generic Composables

```typescript
// composables/useLocalStorage.ts
import { ref, watch, type Ref } from 'vue';

export function useLocalStorage<T>(
  key: string,
  defaultValue: T
): Ref<T> {
  const data = ref<T>(defaultValue) as Ref<T>;

  // Load from localStorage
  const stored = localStorage.getItem(key);
  if (stored) {
    try {
      data.value = JSON.parse(stored);
    } catch (e) {
      console.error('Failed to parse localStorage', e);
    }
  }

  // Save to localStorage on change
  watch(
    data,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue));
    },
    { deep: true }
  );

  return data;
}

// Usage
const user = useLocalStorage<User>('user', { id: 0, name: '' });
```

## When to Use This Skill

Use vue-composition-api when building modern, production-ready
applications that require:

- Complex component logic that benefits from better organization
- Reusable logic across multiple components (composables)
- Better TypeScript integration and type inference
- Fine-grained reactivity control
- Large-scale applications requiring maintainability
- Migration from Vue 2 Options API to Vue 3
- Sharing stateful logic without mixins

## Vue-Specific Best Practices

1. **Prefer `<script setup>` syntax** - Cleaner, better performance, better types
2. **Use composables for reusable logic** - Extract to `composables/` directory
3. **Use `ref` for primitives, `reactive` for objects** - Unless you need to
   replace objects
4. **Always use TypeScript** - Better DX and fewer runtime errors
5. **Destructure reactive objects with `toRefs`** - Preserve reactivity
6. **Use computed for derived state** - Not methods in templates
7. **Cleanup side effects** - Use `onUnmounted` for event listeners, timers
8. **Keep components focused** - Extract complex logic to composables
9. **Use provide/inject for deep prop passing** - Avoid prop drilling
10. **Name composables with `use` prefix** - Follow convention (useCounter, useFetch)

## Vue-Specific Pitfalls

1. **Destructuring props directly** - Loses reactivity, use `toRefs(props)`
2. **Forgetting `.value` on refs** - Common source of bugs
3. **Mutating props** - Props are readonly, emit events instead
4. **Using reactive() for entire state** - Can't replace, use ref for root
5. **Not cleaning up watchers** - Memory leaks, store stop handle
6. **Accessing refs before mount** - DOM refs are null in setup
7. **Overusing reactive()** - Use ref for simple values
8. **Not using computed for derived state** - Recalculates on every render
9. **Forgetting to return from setup()** - Without `<script setup>`
10. **Mixing Options API and Composition API** - Confusing, pick one

## Common Patterns

### Form Handling

```typescript
<script setup lang="ts">
import { reactive, computed } from 'vue';

interface FormData {
  name: string;
  email: string;
  password: string;
}

interface FormErrors {
  name?: string;
  email?: string;
  password?: string;
}

const form = reactive<FormData>({
  name: '',
  email: '',
  password: ''
});

const errors = reactive<FormErrors>({});

const isValid = computed(() =>
  Object.keys(errors).length === 0 &&
  form.name && form.email && form.password
);

function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validate() {
  if (!form.name) {
    errors.name = 'Name is required';
  } else {
    delete errors.name;
  }

  if (!validateEmail(form.email)) {
    errors.email = 'Invalid email';
  } else {
    delete errors.email;
  }

  if (form.password.length < 8) {
    errors.password = 'Password must be 8+ characters';
  } else {
    delete errors.password;
  }
}

async function submit() {
  validate();
  if (!isValid.value) return;

  // Submit form
  await fetch('/api/register', {
    method: 'POST',
    body: JSON.stringify(form)
  });
}
</script>
```

### Async Data Loading

```typescript
<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface Data {
  id: number;
  title: string;
}

const data = ref<Data[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

async function fetchData() {
  loading.value = true;
  error.value = null;

  try {
    const response = await fetch('/api/data');
    if (!response.ok) throw new Error('Failed to fetch');
    data.value = await response.json();
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">Error: {{ error }}</div>
    <div v-else>
      <div v-for="item in data" :key="item.id">
        {{ item.title }}
      </div>
    </div>
  </div>
</template>
```

## Resources

- [Vue 3 Composition API Documentation](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Composition API RFC](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0013-composition-api.md)
- [VueUse - Collection of Composables](https://vueuse.org/)
- [Vue 3 TypeScript Guide](https://vuejs.org/guide/typescript/overview.html)
- [Composables Best Practices](https://vuejs.org/guide/reusability/composables.html)
