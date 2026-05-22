---
name: vue-composables
description: >-
  Develops Vue 3 Composition API patterns and custom composables. Activates when creating composables,
  using ref/reactive/computed, working with watchers, lifecycle hooks, provide/inject, or when user
  mentions composable, reactive, ref, computed, watch, Vue composition, or state management.
---

# Vue Composables Development

## When to Apply

Activate this skill when:

- Creating custom composables
- Using Composition API features (ref, reactive, computed)
- Working with watchers and lifecycle hooks
- Implementing provide/inject patterns
- Managing component state with Composition API

## Documentation

Use `search-docs` for detailed Vue 3 Composition API patterns and documentation.

## Basic Usage

### Refs and Reactive

<code-snippet name="Refs and Reactive" lang="typescript">
import { ref, reactive, computed } from 'vue';

// Ref for primitives
const count = ref(0);
count.value++; // Access with .value

// Reactive for objects
const state = reactive({
    name: '',
    items: [],
});
state.name = 'Updated'; // Direct access

// Computed
const doubled = computed(() => count.value * 2);
</code-snippet>

### Custom Composables

Create reusable logic with composables:

<code-snippet name="Custom Composable" lang="typescript">
// composables/useCounter.ts
import { ref, computed } from 'vue';

export function useCounter(initial = 0) {
    const count = ref(initial);

    const doubled = computed(() => count.value * 2);

    function increment() {
        count.value++;
    }

    function decrement() {
        count.value--;
    }

    return {
        count,
        doubled,
        increment,
        decrement,
    };
}
</code-snippet>

### Watchers

<code-snippet name="Watchers" lang="typescript">
import { ref, watch, watchEffect } from 'vue';

const search = ref('');

// Watch specific ref
watch(search, (newValue, oldValue) => {
    console.log(`Search changed from ${oldValue} to ${newValue}`);
});

// Watch with options
watch(search, (value) => {
    fetchResults(value);
}, { immediate: true, debounce: 300 });

// Watch multiple sources
watch([firstName, lastName], ([first, last]) => {
    fullName.value = `${first} ${last}`;
});

// watchEffect - auto-tracks dependencies
watchEffect(() => {
    console.log(`Count is: ${count.value}`);
});
</code-snippet>

### Lifecycle Hooks

<code-snippet name="Lifecycle Hooks" lang="typescript">
import { onMounted, onUnmounted, onBeforeMount } from 'vue';

onBeforeMount(() => {
    // Before component mounts
});

onMounted(() => {
    // Component mounted - DOM available
    window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
    // Cleanup
    window.removeEventListener('resize', handleResize);
});
</code-snippet>

### Async Composables

<code-snippet name="Async Composable" lang="typescript">
// composables/useFetch.ts
import { ref, watchEffect } from 'vue';

export function useFetch<T>(url: string) {
    const data = ref<T | null>(null);
    const error = ref<Error | null>(null);
    const loading = ref(false);

    async function execute() {
        loading.value = true;
        error.value = null;

        try {
            const response = await fetch(url);
            data.value = await response.json();
        } catch (e) {
            error.value = e as Error;
        } finally {
            loading.value = false;
        }
    }

    execute();

    return { data, error, loading, refetch: execute };
}
</code-snippet>

### Provide/Inject

<code-snippet name="Provide Inject" lang="typescript">
// Parent component
import { provide, ref } from 'vue';

const theme = ref('dark');
provide('theme', theme);

// Child component (any depth)
import { inject } from 'vue';

const theme = inject('theme', ref('light')); // With default
</code-snippet>

### Type-Safe Composables

<code-snippet name="Typed Composables" lang="typescript">
import { ref, type Ref } from 'vue';

interface UseModalReturn {
    isOpen: Ref<boolean>;
    open: () => void;
    close: () => void;
    toggle: () => void;
}

export function useModal(): UseModalReturn {
    const isOpen = ref(false);

    return {
        isOpen,
        open: () => (isOpen.value = true),
        close: () => (isOpen.value = false),
        toggle: () => (isOpen.value = !isOpen.value),
    };
}
</code-snippet>

## Composable Conventions

- Name composables with `use` prefix: `useCounter`, `useFetch`
- Place in `composables/` directory
- Return refs, not raw values (maintains reactivity)
- Document parameters and return types
- Clean up side effects in `onUnmounted`

## Common Pitfalls

- Destructuring reactive objects (loses reactivity) - use `toRefs()`
- Forgetting `.value` when accessing refs in script
- Not cleaning up event listeners or intervals in `onUnmounted`
- Creating composables that don't return reactive references
- Using `ref` when `reactive` is more appropriate for complex objects
