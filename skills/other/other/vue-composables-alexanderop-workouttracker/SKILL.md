---
name: vue-composables
description: Write high-quality Vue 3 composables following established patterns and best practices. Use when creating new composables, refactoring existing ones, or reviewing composable code. Triggers include requests to "create a composable", "write a use* function", "extract logic into a composable", or any Vue Composition API reusable logic task.
---

# Vue 3 Composables Style Guide

## Naming Conventions

### Files
- Prefix with `use` and use PascalCase: `useCounter.ts`, `useApiRequest.ts`
- Place in `src/composables/` directory

### Functions
- Use descriptive names: `useUserData()` not `useData()`
- Export as named function: `export function useCounter() {}`

## Structure Template

Follow this order consistently:

```ts
import { computed, onMounted, ref, watch } from 'vue'

export function useExample() {
  // 1. Initializing - setup logic, router, external dependencies

  // 2. Primary State - main reactive state
  const data = ref<Data | null>(null)

  // 3. State Metadata - status, errors, loading
  const status = ref<'idle' | 'loading' | 'success' | 'error'>('idle')
  const error = ref<Error | null>(null)

  // 4. Computed - derived state
  const isLoading = computed(() => status.value === 'loading')

  // 5. Methods - state manipulation
  const fetchData = async () => {
    status.value = 'loading'
    try {
      // fetch logic
      status.value = 'success'
    }
    catch (e) {
      status.value = 'error'
      error.value = e instanceof Error ? e : new Error(String(e))
    }
  }

  // 6. Lifecycle Hooks
  onMounted(() => {
    // initialization logic
  })

  // 7. Watchers
  watch(data, (newValue) => {
    // react to changes
  })

  return { data, status, error, isLoading, fetchData }
}
```

## Core Rules

### Single Responsibility
One composable = one purpose. Avoid mixing unrelated concerns.

```ts
// GOOD - focused on one task
export function useCounter() {
  const count = ref(0)
  const increment = () => {
    count.value++
  }
  const decrement = () => {
    count.value--
  }
  return { count, increment, decrement }
}

// BAD - mixing user data and counter
export function useUserAndCounter() {
  const user = ref(null)
  const count = ref(0)
  // ... mixed concerns
}
```

### Expose Error State
Return errors for component handling. Never swallow errors or show UI directly.

```ts
// GOOD
const error = ref<Error | null>(null)
try {
  await fetchData()
}
catch (e) {
  error.value = e instanceof Error ? e : new Error(String(e))
}
return { error }

// BAD - swallowing errors or showing UI
try {
  await fetchData()
}
catch (e) {
  console.error(e) // swallowed
  showToast('Error!') // UI in composable
}
```

### No UI Logic in Composables
Keep composables focused on state/logic. Handle UI in components.

```ts
// GOOD - composable returns state
export function useUserData(userId: string) {
  const user = ref<User | null>(null)
  const error = ref<Error | null>(null)
  const fetchUser = async () => { /* ... */ }
  return { user, error, fetchUser }
}

// Component handles UI
const { error } = useUserData(userId)
watch(error, (e) => {
  if (e)
    showToast('Error occurred')
})
```

### Object Arguments for 4+ Parameters

```ts
// GOOD - object for many params
useUserData({ id: 1, fetchOnMount: true, token: 'abc', locale: 'en' })

// GOOD - positional for few params
useCounter(initialValue, step)

// BAD - too many positional args
useUserData(1, true, 'abc', 'en', false, 'default')
```

### Group Related State into Objects

When a composable has 4+ related state properties, group them into a single `ref` object instead of separate refs.

```ts
// GOOD - grouped state for 4+ related properties
interface FormState {
  name: string
  email: string
  phone: string
  address: string
}

export function useContactForm() {
  const form = ref<FormState>({
    name: '',
    email: '',
    phone: '',
    address: '',
  })

  function reset() {
    form.value = { name: '', email: '', phone: '', address: '' }
  }

  return { form, reset }
}

// GOOD - separate refs for 1-3 unrelated properties
export function useToggle() {
  const isOpen = ref(false)
  const isLoading = ref(false)
  return { isOpen, isLoading }
}

// BAD - many separate refs for related state
export function useContactForm() {
  const name = ref('')
  const email = ref('')
  const phone = ref('')
  const address = ref('')
  // ... becomes unwieldy to manage and reset
}
```

### Functional Core, Imperative Shell
Extract pure logic from Vue reactivity when beneficial.

```ts
// Pure function (testable, no side effects)
function calculateTotal(items: ReadonlyArray<Item>) {
  return items.reduce((sum, item) => sum + item.price, 0)
}

// Composable uses the pure function
export function useCart() {
  const items = ref<Array<Item>>([])
  const total = computed(() => calculateTotal(items.value))
  return { items, total }
}
```

## Quick Reference

| Aspect | Do | Don't |
|--------|-----|-------|
| Naming | `useUserData`, `useFetchApi` | `useData`, `getData` |
| File | `useCounter.ts` in `composables/` | `counter.ts` anywhere |
| Errors | Return `error` ref | `console.error()` or toast |
| UI | Return state, handle UI in component | `showModal()` in composable |
| Params | Object for 4+ params | Long positional arg lists |
| State | `ref` object for 4+ related properties | Many separate refs |
| Focus | Single responsibility | Mixed concerns |
