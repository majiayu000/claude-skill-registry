---
name: vue-reactivity-system
description: Use when Vue reactivity system with refs, reactive, computed, and watchers. Use when managing complex state in Vue applications.
allowed-tools:
  - Bash
  - Read
---

# Vue Reactivity System

Master Vue's reactivity system to build reactive, performant applications
with optimal state management and computed properties.

## Reactivity Fundamentals (Proxy-based)

Vue 3 uses JavaScript Proxies for reactivity:

```typescript
import { ref, reactive, isRef, isReactive, isProxy } from 'vue';

// ref creates reactive wrapper
const count = ref(0);
console.log(isRef(count)); // true
console.log(isProxy(count)); // false (ref itself isn't proxy)
console.log(isProxy(count.value)); // false for primitives

// reactive creates proxy
const state = reactive({ count: 0 });
console.log(isReactive(state)); // true
console.log(isProxy(state)); // true

// Proxies track access and mutations
state.count++; // Triggers reactivity
count.value++; // Triggers reactivity
```

## Ref - Reactive Primitives and Objects

### Basic Ref Usage

```typescript
import { ref } from 'vue';

// Primitives
const count = ref(0);
const name = ref('John');
const isActive = ref(true);

// Access via .value
console.log(count.value); // 0
count.value++; // Update triggers reactivity

// Objects (wrapped in proxy)
const user = ref({
  name: 'John',
  age: 30
});

// Nested properties are reactive
user.value.age++; // Triggers reactivity

// Can replace entire object
user.value = { name: 'Jane', age: 25 }; // Works!
```

### Shallow Ref

```typescript
import { shallowRef, triggerRef } from 'vue';

// Only .value is reactive, not nested properties
const state = shallowRef({
  count: 0,
  nested: { value: 0 }
});

// This triggers reactivity
state.value = { count: 1, nested: { value: 1 } };

// This does NOT trigger reactivity
state.value.count++; // No update!

// Manually trigger
state.value.count++;
triggerRef(state); // Force update
```

### Custom Ref

```typescript
import { customRef } from 'vue';

// Debounced ref
function useDebouncedRef<T>(value: T, delay = 200) {
  let timeout: ReturnType<typeof setTimeout>;

  return customRef((track, trigger) => ({
    get() {
      track(); // Tell Vue to track this
      return value;
    },
    set(newValue: T) {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        value = newValue;
        trigger(); // Tell Vue to re-render
      }, delay);
    }
  }));
}

// Usage
const searchQuery = useDebouncedRef('', 300);

// Updates are debounced
searchQuery.value = 'a'; // Doesn't trigger immediately
searchQuery.value = 'ab'; // Still waiting
searchQuery.value = 'abc'; // Triggers after 300ms
```

## Reactive - Deep Reactive Objects

### Basic Reactive Usage

```typescript
import { reactive } from 'vue';

// Create deep reactive object
const state = reactive({
  user: {
    name: 'John',
    profile: {
      email: 'john@example.com',
      settings: {
        theme: 'dark'
      }
    }
  },
  posts: []
});

// All nested properties are reactive
state.user.profile.settings.theme = 'light'; // Triggers reactivity
state.posts.push({ id: 1, title: 'Post' }); // Triggers reactivity
```

### Shallow Reactive

```typescript
import { shallowReactive } from 'vue';

// Only root-level properties are reactive
const state = shallowReactive({
  count: 0,
  nested: { value: 0 }
});

// This triggers reactivity
state.count++; // Works

// This does NOT trigger reactivity
state.nested.value++; // No update!

// But replacing works
state.nested = { value: 1 }; // Triggers reactivity
```

### Reactive Arrays

```typescript
import { reactive } from 'vue';

const list = reactive<number[]>([]);

// Mutating methods trigger reactivity
list.push(1); // Reactive
list.pop(); // Reactive
list.splice(0, 1); // Reactive
list.sort(); // Reactive
list.reverse(); // Reactive

// Replacement triggers reactivity
const newList = reactive([1, 2, 3]);
```

### Reactive Collections

```typescript
import { reactive } from 'vue';

// Map
const map = reactive(new Map<string, number>());
map.set('count', 0); // Reactive
map.delete('count'); // Reactive

// Set
const set = reactive(new Set<number>());
set.add(1); // Reactive
set.delete(1); // Reactive

// WeakMap and WeakSet
const weakMap = reactive(new WeakMap());
const weakSet = reactive(new WeakSet());
```

## Readonly - Prevent Mutations

```typescript
import { reactive, readonly, isReadonly } from 'vue';

const state = reactive({ count: 0 });
const readonlyState = readonly(state);

console.log(isReadonly(readonlyState)); // true

// Cannot mutate
readonlyState.count++; // Warning in dev mode

// Original is still mutable
state.count++; // Works, updates readonly view too

// Deep readonly
const deepState = reactive({
  nested: { value: 0 }
});

const deepReadonly = readonly(deepState);
deepReadonly.nested.value++; // Warning! Deep readonly
```

## ToRef and ToRefs - Preserve Reactivity

### ToRefs - Convert Reactive to Refs

```typescript
import { reactive, toRefs } from 'vue';

const state = reactive({
  count: 0,
  name: 'John'
});

// Destructuring loses reactivity
const { count, name } = state; // NOT reactive!

// Use toRefs to preserve reactivity
const { count: countRef, name: nameRef } = toRefs(state);

// Now reactive
countRef.value++; // Updates state.count
console.log(state.count); // 1
```

### ToRef - Create Ref from Property

```typescript
import { reactive, toRef } from 'vue';

const state = reactive({
  count: 0
});

// Create ref to specific property
const countRef = toRef(state, 'count');

countRef.value++; // Updates state.count
console.log(state.count); // 1

// Non-existent properties
const missingRef = toRef(state, 'missing');
missingRef.value = 'now exists'; // Adds to state!
```

## Unref and IsRef - Ref Utilities

```typescript
import { ref, unref, isRef } from 'vue';

const count = ref(0);
const plain = 0;

// unref: unwrap if ref, return value otherwise
console.log(unref(count)); // 0
console.log(unref(plain)); // 0

// Useful for handling ref or value
function double(value: number | Ref<number>): number {
  return unref(value) * 2;
}

double(count); // 0
double(5); // 10

// isRef: check if value is ref
if (isRef(count)) {
  console.log(count.value);
} else {
  console.log(count);
}
```

## Computed - Derived State

### Basic Computed

```typescript
import { ref, computed } from 'vue';

const count = ref(0);

const doubled = computed(() => count.value * 2);

console.log(doubled.value); // 0
count.value = 5;
console.log(doubled.value); // 10

// Computed is cached
const expensive = computed(() => {
  console.log('Computing...');
  return count.value * 2;
});

console.log(expensive.value); // Computing... 0
console.log(expensive.value); // 0 (cached, no log)
count.value = 1;
console.log(expensive.value); // Computing... 2
```

### Writable Computed

```typescript
import { ref, computed } from 'vue';

const firstName = ref('John');
const lastName = ref('Doe');

const fullName = computed({
  get() {
    return `${firstName.value} ${lastName.value}`;
  },
  set(value) {
    [firstName.value, lastName.value] = value.split(' ');
  }
});

console.log(fullName.value); // John Doe
fullName.value = 'Jane Smith';
console.log(firstName.value); // Jane
console.log(lastName.value); // Smith
```

### Computed Debugging

```typescript
import { ref, computed } from 'vue';

const count = ref(0);

const doubled = computed(
  () => count.value * 2,
  {
    onTrack(e) {
      console.log('Tracked:', e);
    },
    onTrigger(e) {
      console.log('Triggered:', e);
    }
  }
);
```

## Watch - React to Changes

### Watch Single Source

```typescript
import { ref, watch } from 'vue';

const count = ref(0);

// Basic watch
watch(count, (newValue, oldValue) => {
  console.log(`Count: ${oldValue} -> ${newValue}`);
});

// With options
watch(
  count,
  (newValue, oldValue) => {
    console.log('Count changed');
  },
  {
    immediate: true, // Run immediately
    flush: 'post', // Timing: 'pre' | 'post' | 'sync'
    onTrack(e) { console.log('Tracked:', e); },
    onTrigger(e) { console.log('Triggered:', e); }
  }
);
```

### Watch Multiple Sources

```typescript
import { ref, watch } from 'vue';

const x = ref(0);
const y = ref(0);

// Watch array of sources
watch(
  [x, y],
  ([newX, newY], [oldX, oldY]) => {
    console.log(`x: ${oldX} -> ${newX}`);
    console.log(`y: ${oldY} -> ${newY}`);
  }
);

// Trigger when any changes
x.value++; // Logs
y.value++; // Logs
```

### Watch Reactive Object

```typescript
import { reactive, watch } from 'vue';

const state = reactive({
  count: 0,
  user: { name: 'John' }
});

// Watch getter
watch(
  () => state.count,
  (newValue, oldValue) => {
    console.log('Count changed');
  }
);

// Deep watch entire object
watch(
  state,
  (newValue, oldValue) => {
    console.log('State changed');
  },
  { deep: true }
);

// Watch specific nested property
watch(
  () => state.user.name,
  (newValue, oldValue) => {
    console.log('Name changed');
  }
);
```

### Stop Watching

```typescript
import { ref, watch } from 'vue';

const count = ref(0);

const stop = watch(count, (value) => {
  console.log(`Count: ${value}`);

  // Stop watching when count reaches 5
  if (value >= 5) {
    stop();
  }
});

// Or stop externally
stop();
```

## WatchEffect - Automatic Dependency Tracking

```typescript
import { ref, watchEffect } from 'vue';

const count = ref(0);
const name = ref('John');

// Automatically tracks dependencies
watchEffect(() => {
  console.log(`${name.value}: ${count.value}`);
});
// Logs: John: 0

count.value++; // Logs: John: 1
name.value = 'Jane'; // Logs: Jane: 1

// Cleanup
const stop = watchEffect((onCleanup) => {
  const timer = setTimeout(() => {
    console.log(count.value);
  }, 1000);

  // Register cleanup
  onCleanup(() => {
    clearTimeout(timer);
  });
});

// Stop watching
stop();
```

### WatchEffect Timing

```typescript
import { ref, watchEffect, watchPostEffect, watchSyncEffect } from 'vue';

const count = ref(0);

// Default: 'pre' - before component update
watchEffect(() => {
  console.log('Pre:', count.value);
}, { flush: 'pre' });

// 'post' - after component update (access updated DOM)
watchPostEffect(() => {
  console.log('Post:', count.value);
  // Can access updated DOM
});

// 'sync' - synchronous (use sparingly!)
watchSyncEffect(() => {
  console.log('Sync:', count.value);
});
```

## Effect Scope - Group Effects

```typescript
import { effectScope, ref, watch } from 'vue';

const scope = effectScope();

scope.run(() => {
  const count = ref(0);

  watch(count, () => {
    console.log('Count changed');
  });

  watchEffect(() => {
    console.log('Effect');
  });
});

// Stop all effects in scope
scope.stop();

// Nested scopes
const parent = effectScope();

parent.run(() => {
  const child = effectScope();

  child.run(() => {
    // Child effects
  });

  // Stop child only
  child.stop();
});

// Stop parent (and all children)
parent.stop();
```

## Reactivity Utilities

### Trigger and Scheduler

```typescript
import { ref, triggerRef } from 'vue';

const count = ref(0);

// Manually trigger updates
count.value = 1;
triggerRef(count); // Force update even if value didn't change
```

### Reactive Unwrapping

```typescript
import { reactive, ref } from 'vue';

const count = ref(0);
const state = reactive({
  // Refs are auto-unwrapped in reactive
  count
});

// No .value needed
console.log(state.count); // 0 (not state.count.value)
state.count++; // Works

// But in arrays, not unwrapped
const list = reactive([ref(0)]);
console.log(list[0].value); // Must use .value
```

## When to Use This Skill

Use vue-reactivity-system when building modern, production-ready
applications that require:

- Complex state management patterns
- Fine-grained reactivity control
- Performance optimization through computed properties
- Advanced watching and effect patterns
- Understanding of Vue's reactive internals
- Debugging reactivity issues
- Building reactive composables
- Large-scale applications with complex data flows

## Reactivity Best Practices

1. **Use `ref` for primitives** - Always wrap primitives in ref
2. **Use `reactive` for objects** - Deep reactivity for complex state
3. **Use `computed` for derived state** - Cached and reactive
4. **Use `watch` for side effects** - API calls, localStorage, etc.
5. **Use `watchEffect` for simple effects** - Auto-tracks dependencies
6. **Don't destructure reactive** - Use `toRefs` to preserve reactivity
7. **Use `readonly` to prevent mutations** - Protect shared state
8. **Cleanup effects properly** - Return cleanup function or use `onCleanup`
9. **Avoid deep watching everything** - Performance impact
10. **Use `shallowRef`/`shallowReactive` for large data** - Better performance

## Common Reactivity Pitfalls

1. **Destructuring reactive objects** - Loses reactivity without `toRefs`
2. **Forgetting `.value` on refs** - Common source of bugs
3. **Replacing reactive object** - Breaks reactivity, use `ref` instead
4. **Deep watching performance** - Can be slow with large objects
5. **Not cleaning up watchers** - Memory leaks
6. **Accessing refs before initialization** - Can be undefined
7. **Mutating props** - Props are readonly
8. **Unnecessary computed** - Use regular refs if not derived
9. **Synchronous effects** - Usually should be async
10. **Not understanding proxy limitations** - Some operations don't track

## Advanced Patterns

### Reactive State Pattern

```typescript
import { reactive, readonly, computed } from 'vue';

interface State {
  count: number;
  items: string[];
}

function createStore() {
  const state = reactive<State>({
    count: 0,
    items: []
  });

  // Computed
  const doubled = computed(() => state.count * 2);

  // Actions
  function increment() {
    state.count++;
  }

  function addItem(item: string) {
    state.items.push(item);
  }

  // Expose readonly state
  return {
    state: readonly(state),
    doubled,
    increment,
    addItem
  };
}

const store = createStore();
```

### Reactive Form State

```typescript
import { reactive, computed, watch } from 'vue';

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

function useForm() {
  const data = reactive<FormData>({
    email: '',
    password: ''
  });

  const errors = reactive<FormErrors>({});

  const isValid = computed(() =>
    !errors.email && !errors.password &&
    data.email && data.password
  );

  // Validate on change
  watch(
    () => data.email,
    (email) => {
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errors.email = 'Invalid email';
      } else {
        delete errors.email;
      }
    }
  );

  watch(
    () => data.password,
    (password) => {
      if (password.length < 8) {
        errors.password = 'Must be 8+ characters';
      } else {
        delete errors.password;
      }
    }
  );

  return {
    data,
    errors,
    isValid
  };
}
```

### Async Reactive State

```typescript
import { ref, watchEffect } from 'vue';

interface User {
  id: number;
  name: string;
}

function useAsyncData<T>(
  fetcher: () => Promise<T>
) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  async function execute() {
    loading.value = true;
    error.value = null;

    try {
      data.value = await fetcher();
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  watchEffect((onCleanup) => {
    let cancelled = false;

    execute().then(() => {
      if (cancelled) {
        data.value = null;
      }
    });

    onCleanup(() => {
      cancelled = true;
    });
  });

  return { data, error, loading, refetch: execute };
}
```

## Reactivity Caveats and Limitations

### Property Addition/Deletion

```typescript
import { reactive } from 'vue';

const state = reactive<{ count?: number }>({});

// Adding new property is reactive
state.count = 1; // Reactive

// But TypeScript won't know about it unless typed
// Solution: Define all properties upfront or use proper types
```

### Ref Unwrapping in Templates

```vue
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
  <!-- Auto-unwrapped in templates -->
  <p>{{ count }}</p>  <!-- Not count.value -->

  <!-- But not in JavaScript expressions -->
  <p>{{ count + 1 }}</p>  <!-- Won't work! -->
  <p>{{ count.value + 1 }}</p>  <!-- Correct -->
</template>
```

### Non-Reactive Values

```typescript
import { reactive } from 'vue';

// Primitive values in reactive are still reactive
const state = reactive({
  count: 0 // Reactive
});

// But extracting loses reactivity
let count = state.count; // Not reactive
count++; // Doesn't update state
```

## Resources

- [Vue 3 Reactivity Documentation](https://vuejs.org/guide/essentials/reactivity-fundamentals.html)
- [Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html)
- [Reactivity API Reference](https://vuejs.org/api/reactivity-core.html)
- [Reactivity Transform (Experimental)](https://vuejs.org/guide/extras/reactivity-transform.html)
- [Composition API FAQ](https://vuejs.org/guide/extras/composition-api-faq.html)
