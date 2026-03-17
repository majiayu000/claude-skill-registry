---
name: nuxt-data
description: |
  Nuxt 4 data management: composables, data fetching with useFetch/useAsyncData,
  and state management with useState and Pinia.

  Use when: creating custom composables, fetching data with useFetch or useAsyncData,
  managing global state with useState, integrating Pinia, debugging reactive data issues,
  or implementing SSR-safe state patterns.

  Keywords: useFetch, useAsyncData, $fetch, useState, composables, Pinia,
  data fetching, state management, reactive, shallow reactivity, reactive keys,
  transform, pending, error, refresh, dedupe, caching
license: MIT
metadata:
  version: 4.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 4.x
  last-verified: 2025-12-28
---

# Nuxt 4 Data Management

Composables, data fetching, and state management patterns for Nuxt 4 applications.

## Quick Reference

### Data Fetching Methods

| Method | Use Case | SSR | Caching | Reactive |
|--------|----------|-----|---------|----------|
| `useFetch` | Simple API calls | Yes | Yes | Yes |
| `useAsyncData` | Custom async logic | Yes | Yes | Yes |
| `$fetch` | Client-side only, events | No | No | No |

### Composable Naming

| Prefix | Purpose | Example |
|--------|---------|---------|
| `use` | State/logic composable | `useAuth`, `useCart` |
| `fetch` | Data fetching only | `fetchUsers` (rare) |

## When to Load References

**Load `references/composables.md` when:**
- Writing custom composables with complex state
- Debugging state management issues or memory leaks
- Implementing SSR-safe patterns with browser APIs
- Building authentication or complex state composables
- Understanding singleton vs per-call composable patterns

**Load `references/data-fetching.md` when:**
- Implementing API data fetching with reactive parameters
- Troubleshooting shallow vs deep reactivity issues
- Debugging data not refreshing when params change
- Implementing pagination, infinite scroll, or search
- Understanding transform functions, caching, or error handling

**Load `references/pinia-integration.md` when:**
- Setting up Pinia for complex state management
- Creating stores with getters and actions
- Integrating Pinia with SSR
- Persisting state across page reloads

## Composables

### useState - The Foundation

`useState` creates SSR-safe, shared reactive state that persists across component instances.

```typescript
// composables/useCounter.ts
export const useCounter = () => {
  // Singleton - shared across all components
  const count = useState('counter', () => 0)

  const increment = () => count.value++
  const decrement = () => count.value--
  const reset = () => count.value = 0

  return { count, increment, decrement, reset }
}
```

### useState vs ref - Critical Distinction

```typescript
// CORRECT: Shared state (singleton pattern)
export const useAuth = () => {
  const user = useState('auth-user', () => null)  // Shared!
  return { user }
}

// WRONG: Creates new instance every call!
export const useAuth = () => {
  const user = ref(null)  // Not shared!
  return { user }
}
```

**Rule**: Use `useState` for shared/global state. Use `ref` for local component state only.

### Complete Authentication Composable

```typescript
// composables/useAuth.ts
export const useAuth = () => {
  const user = useState<User | null>('auth-user', () => null)
  const isAuthenticated = computed(() => !!user.value)
  const isLoading = useState('auth-loading', () => false)

  const login = async (email: string, password: string) => {
    isLoading.value = true
    try {
      const data = await $fetch('/api/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      user.value = data.user
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
    navigateTo('/login')
  }

  const checkSession = async () => {
    if (import.meta.server) return  // Skip on server
    try {
      const data = await $fetch('/api/auth/session')
      user.value = data.user
    } catch {
      user.value = null
    }
  }

  return { user, isAuthenticated, isLoading, login, logout, checkSession }
}
```

### SSR-Safe Browser APIs

```typescript
// composables/useLocalStorage.ts
export const useLocalStorage = <T>(key: string, defaultValue: T) => {
  const data = useState<T>(key, () => defaultValue)

  // Only access localStorage on client
  if (import.meta.client) {
    const stored = localStorage.getItem(key)
    if (stored) {
      data.value = JSON.parse(stored)
    }

    // Watch and persist changes
    watch(data, (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue))
    }, { deep: true })
  }

  return data
}
```

## Data Fetching

### useFetch - Basic Usage

```typescript
// Simple GET request
const { data, error, pending, refresh } = await useFetch('/api/users')

// With options
const { data: users } = await useFetch('/api/users', {
  method: 'GET',
  query: { limit: 10, offset: 0 },
  headers: { 'X-Custom-Header': 'value' }
})
```

### Reactive Parameters

```vue
<script setup lang="ts">
const page = ref(1)
const search = ref('')

// Auto-refetches when page or search changes
const { data: users, pending } = await useFetch('/api/users', {
  query: {
    page,
    search,
    limit: 10
  }
})

// Or with computed
const query = computed(() => ({
  page: page.value,
  search: search.value,
  limit: 10
}))

const { data } = await useFetch('/api/users', { query })
</script>
```

### Transform Data

```typescript
const { data: userNames } = await useFetch('/api/users', {
  transform: (users) => users.map(u => u.name)
})

// data.value is now string[] instead of User[]
```

### Pick Specific Fields

```typescript
const { data } = await useFetch('/api/user', {
  pick: ['id', 'name', 'email']  // Only these fields in payload
})
```

### useAsyncData - Custom Logic

```typescript
// Multiple parallel requests
const { data } = await useAsyncData('dashboard', async () => {
  const [users, posts, stats] = await Promise.all([
    $fetch('/api/users'),
    $fetch('/api/posts'),
    $fetch('/api/stats')
  ])
  return { users, posts, stats }
})

// Access: data.value.users, data.value.posts, data.value.stats
```

### Error Handling

```typescript
const { data, error, status } = await useFetch('/api/users')

// Check error
if (error.value) {
  console.error('Error:', error.value.message)
  console.error('Status:', error.value.statusCode)
}

// Status values: 'idle' | 'pending' | 'success' | 'error'
if (status.value === 'error') {
  showError(error.value)
}
```

### Manual Refresh

```typescript
const { data, refresh, execute } = await useFetch('/api/users', {
  immediate: false  // Don't fetch on mount
})

// Fetch manually
await execute()

// Refresh (re-fetch)
await refresh()

// Refresh with new params
await refresh({ dedupe: true })
```

### Shallow vs Deep Reactivity (v4 Change)

```typescript
// Nuxt 4 default: Shallow reactivity
const { data } = await useFetch('/api/user')
data.value.name = 'New Name'  // Won't trigger reactivity!

// Enable deep reactivity for mutations
const { data } = await useFetch('/api/user', {
  deep: true
})
data.value.name = 'New Name'  // Now works!

// Or refresh instead of mutating
const { data, refresh } = await useFetch('/api/user')
await $fetch('/api/user', { method: 'PATCH', body: { name: 'New Name' } })
await refresh()  // Re-fetch updated data
```

### Caching and Deduplication

```typescript
const { data } = await useFetch('/api/users', {
  key: 'users-list',           // Custom cache key
  dedupe: 'cancel',            // Cancel duplicate requests
  getCachedData: (key, nuxtApp) => {
    // Return cached data if valid
    return nuxtApp.payload.data[key]
  }
})
```

### Lazy Loading Data

```typescript
// useLazyFetch - Navigation happens immediately, data loads in background
const { data, pending } = useLazyFetch('/api/users')

// useLazyAsyncData
const { data, pending } = useLazyAsyncData('users', () => $fetch('/api/users'))
```

### $fetch - Client-Side Only

```typescript
// In event handlers (not during SSR)
const submitForm = async () => {
  const result = await $fetch('/api/submit', {
    method: 'POST',
    body: formData.value
  })
}

// In server routes
export default defineEventHandler(async (event) => {
  const externalData = await $fetch('https://api.example.com/data')
  return externalData
})
```

## State Management

### useState Patterns

```typescript
// Simple counter
const count = useState('count', () => 0)

// Complex object
const settings = useState('settings', () => ({
  theme: 'light',
  notifications: true,
  language: 'en'
}))

// Typed state
interface User {
  id: string
  name: string
  email: string
}
const user = useState<User | null>('user', () => null)
```

### Shared Cart Example

```typescript
// composables/useCart.ts
interface CartItem {
  id: string
  name: string
  price: number
  quantity: number
}

export const useCart = () => {
  const items = useState<CartItem[]>('cart-items', () => [])

  const total = computed(() =>
    items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  const itemCount = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const addItem = (product: Omit<CartItem, 'quantity'>) => {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({ ...product, quantity: 1 })
    }
  }

  const removeItem = (id: string) => {
    items.value = items.value.filter(i => i.id !== id)
  }

  const updateQuantity = (id: string, quantity: number) => {
    const item = items.value.find(i => i.id === id)
    if (item) {
      item.quantity = Math.max(0, quantity)
      if (item.quantity === 0) removeItem(id)
    }
  }

  const clearCart = () => {
    items.value = []
  }

  return { items, total, itemCount, addItem, removeItem, updateQuantity, clearCart }
}
```

### Pinia Integration

```bash
bun add pinia @pinia/nuxt
```

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@pinia/nuxt']
})

// stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    userName: (state) => state.user?.name ?? 'Guest'
  },

  actions: {
    async login(email: string, password: string) {
      const { user, token } = await $fetch('/api/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      this.user = user
      this.token = token
    },

    logout() {
      this.user = null
      this.token = null
    }
  }
})

// Usage in components
const authStore = useAuthStore()
await authStore.login('user@example.com', 'password')
console.log(authStore.userName)
```

## Common Anti-Patterns

### Using ref Instead of useState

```typescript
// WRONG - Creates new instance every time!
export const useAuth = () => {
  const user = ref(null)  // Not shared
  return { user }
}

// CORRECT
export const useAuth = () => {
  const user = useState('auth-user', () => null)
  return { user }
}
```

### Missing Error Handling

```typescript
// WRONG
const { data } = await useFetch('/api/users')
console.log(data.value.length)  // Crashes if error!

// CORRECT
const { data, error } = await useFetch('/api/users')
if (error.value) {
  showToast({ type: 'error', message: error.value.message })
  return
}
console.log(data.value.length)
```

### Non-Deterministic Transform

```typescript
// WRONG - Causes hydration mismatch!
const { data } = await useFetch('/api/users', {
  transform: (users) => users.sort(() => Math.random() - 0.5)
})

// CORRECT
const { data } = await useFetch('/api/users', {
  transform: (users) => users.sort((a, b) => a.name.localeCompare(b.name))
})
```

### Mutating Shallow Refs

```typescript
// WRONG - v4 uses shallow refs by default
const { data } = await useFetch('/api/user')
data.value.name = 'New Name'  // Won't trigger reactivity!

// CORRECT - Option 1: Enable deep
const { data } = await useFetch('/api/user', { deep: true })
data.value.name = 'New Name'

// CORRECT - Option 2: Replace entire value
data.value = { ...data.value, name: 'New Name' }

// CORRECT - Option 3: Refresh after mutation
await $fetch('/api/user', { method: 'PATCH', body: { name: 'New Name' } })
await refresh()
```

## Troubleshooting

**Data Not Refreshing When Params Change:**
- Ensure params are reactive: `{ query: { page } }` where `page = ref(1)`
- Check you're using the ref itself, not `.value`

**Hydration Mismatch with useState:**
- Ensure key is unique: `useState('unique-key', () => value)`
- Avoid `Math.random()` or `Date.now()` in initial values

**State Lost on Navigation:**
- Use `useState` instead of `ref` for persistent state
- Check you're using the same key across components

**Infinite Refetch Loop:**
- Check for reactive dependencies in transform function
- Use `watch` with `{ immediate: false }` for side effects

## Related Skills

- **nuxt-core**: Project setup, routing, configuration
- **nuxt-server**: Server routes, API patterns
- **nuxt-production**: Performance, testing, deployment

---

**Version**: 4.0.0 | **Last Updated**: 2025-12-28 | **License**: MIT
