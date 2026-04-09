---
name: nuxt-data
description: Nuxt 5 data management with useFetch, useAsyncData, useState, and Pinia. Use when creating composables, fetching data, managing state, or debugging reactive/SSR data issues.
license: MIT
metadata:
  version: 5.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 5.x
  last-verified: 2026-03-30
---

# Nuxt 5 Data Management

Composables, data fetching, and state management patterns for Nuxt 5 applications.

**Use when**: creating custom composables, fetching data with useFetch or useAsyncData, managing global state with useState, integrating Pinia, debugging reactive data issues, or implementing SSR-safe state patterns.

## Quick Reference

### Data Fetching Methods

| Method | Use Case | SSR | Caching | Reactive |
|--------|----------|-----|---------|----------|
| `useFetch` | Simple API calls | Yes | Yes | Yes |
| `useAsyncData` | Custom async logic | Yes | Yes | Yes |
| `$fetch` | Client-side only, events | No | No | No |

## When to Load References

**Load `references/composables.md` when:**
- Writing custom composables with complex state
- Debugging state management issues or memory leaks
- Implementing SSR-safe patterns with browser APIs
- Building authentication or complex state composables

**Load `references/data-fetching.md` when:**
- Implementing API data fetching with reactive parameters
- Troubleshooting shallow vs deep reactivity issues
- Debugging data not refreshing when params change
- Implementing pagination, infinite scroll, or search

## Composables

### useState - The Foundation

`useState` creates SSR-safe, shared reactive state that persists across component instances.

```typescript
// composables/useCounter.ts
export const useCounter = () => {
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
  const user = useState('auth-user', () => null)
  return { user }
}

// WRONG: Creates new instance every call!
export const useAuth = () => {
  const user = ref(null)
  return { user }
}
```

**Rule**: Use `useState` for shared/global state. Use `ref` for local component state only.

### clearNuxtState Resets to Defaults (v5 Change)

```typescript
// Nuxt 5: clearNuxtState resets state to its initial value, not undefined
const count = useState('counter', () => 42)
count.value = 100

clearNuxtState('counter')
// count.value is now 42 (the initial default), not undefined
```

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
    if (import.meta.server) return
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

  if (import.meta.client) {
    const stored = localStorage.getItem(key)
    if (stored) {
      data.value = JSON.parse(stored)
    }

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
const { data, error, pending, refresh } = await useFetch('/api/users')

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

const { data: users, pending } = await useFetch('/api/users', {
  query: {
    page,
    search,
    limit: 10
  }
})
</script>
```

### Transform Data

```typescript
const { data: userNames } = await useFetch('/api/users', {
  transform: (users) => users.map(u => u.name)
})
```

### useAsyncData - Custom Logic

```typescript
const { data } = await useAsyncData('dashboard', async () => {
  const [users, posts, stats] = await Promise.all([
    $fetch('/api/users'),
    $fetch('/api/posts'),
    $fetch('/api/stats')
  ])
  return { users, posts, stats }
})
```

### Error Handling

```typescript
const { data, error, status } = await useFetch('/api/users')

if (error.value) {
  console.error('Error:', error.value.message)
  console.error('Status:', error.value.statusCode)
}

if (status.value === 'error') {
  showError(error.value)
}
```

### Manual Refresh

```typescript
const { data, refresh, execute } = await useFetch('/api/users', {
  immediate: false
})

await execute()
await refresh()
await refresh({ dedupe: true })
```

### Shallow vs Deep Reactivity

```typescript
// Nuxt 5 default: Shallow reactivity
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
await refresh()
```

### Caching and Deduplication

```typescript
const { data } = await useFetch('/api/users', {
  key: 'users-list',
  dedupe: 'cancel',
  getCachedData: (key, nuxtApp) => {
    return nuxtApp.payload.data[key]
  }
})
```

### Lazy Loading Data

```typescript
const { data, pending } = useLazyFetch('/api/users')
const { data: data2, pending: pending2 } = useLazyAsyncData('users', () => $fetch('/api/users'))
```

### $fetch - Client-Side Only

```typescript
const submitForm = async () => {
  const result = await $fetch('/api/submit', {
    method: 'POST',
    body: formData.value
  })
}
```

## State Management

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

  const clearCart = () => {
    items.value = []
  }

  return { items, total, addItem, removeItem, clearCart }
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
```

## Common Anti-Patterns

### Using ref Instead of useState

```typescript
// WRONG
export const useAuth = () => {
  const user = ref(null)
  return { user }
}

// CORRECT
export const useAuth = () => {
  const user = useState('auth-user', () => null)
  return { user }
}
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
// WRONG
const { data } = await useFetch('/api/user')
data.value.name = 'New Name'

// CORRECT - Enable deep
const { data } = await useFetch('/api/user', { deep: true })

// CORRECT - Replace entire value
data.value = { ...data.value, name: 'New Name' }

// CORRECT - Refresh after mutation
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

**clearNuxtState not working as expected:**
- v5 resets to initial default value, not `undefined`
- Check that the initial factory function returns the expected default

## Related Skills

- **nuxt-core**: Project setup, routing, configuration
- **nuxt-server**: Server routes, API patterns (Nitro v3)
- **nuxt-production**: Performance, testing, deployment

---

**Version**: 5.0.0 | **Last Updated**: 2026-03-30 | **License**: MIT
