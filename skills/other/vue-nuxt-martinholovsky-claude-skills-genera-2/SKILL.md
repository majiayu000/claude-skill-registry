# Vue 3 & Nuxt 3 Expert

## Section 1: Overview

**Risk Level**: MEDIUM

**Expertise Areas**:
- Vue 3.4+ with Composition API and TypeScript
- Nuxt 3.10+ server-side rendering (SSR) and static site generation (SSG)
- State management with Pinia and composables
- Performance optimization and Core Web Vitals
- Client-side security (XSS, CSRF, injection attacks)
- Modern build tooling (Vite, Nitro)

**Target Users**: Frontend engineers building modern, performant, type-safe web applications

**Key Focus**: Type-safe component architecture, composable logic, SSR/SSG patterns, and client-side security

---

## Section 2: Core Principles

1. **TDD First** - Write tests before implementation using Vitest and Vue Test Utils
2. **Performance Aware** - Optimize reactivity, use computed over methods, implement lazy loading
3. **Type Safety** - Use TypeScript strict mode with proper component and composable typing
4. **Composable-First** - Extract reusable logic into composables for maximum reusability
5. **Security-Conscious** - Prevent XSS, validate inputs, configure CSP headers
6. **SSR-Compatible** - Always consider server-side rendering implications

---

## Section 3: Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```typescript
// tests/components/UserCard.test.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import UserCard from '~/components/UserCard.vue'

describe('UserCard', () => {
  it('displays user name and email', () => {
    const wrapper = mount(UserCard, {
      props: {
        user: {
          id: '1',
          name: 'John Doe',
          email: 'john@example.com'
        }
      },
      global: {
        plugins: [createTestingPinia()]
      }
    })

    expect(wrapper.text()).toContain('John Doe')
    expect(wrapper.text()).toContain('john@example.com')
  })

  it('emits select event when clicked', async () => {
    const wrapper = mount(UserCard, {
      props: {
        user: { id: '1', name: 'John', email: 'john@test.com' }
      }
    })

    await wrapper.trigger('click')
    expect(wrapper.emitted('select')).toBeTruthy()
    expect(wrapper.emitted('select')[0]).toEqual(['1'])
  })

  it('shows loading state', () => {
    const wrapper = mount(UserCard, {
      props: {
        user: null,
        loading: true
      }
    })

    expect(wrapper.find('[data-testid="loading-skeleton"]').exists()).toBe(true)
  })
})
```

### Step 2: Write Composable Tests

```typescript
// tests/composables/useAsyncData.test.ts
import { describe, it, expect, vi } from 'vitest'
import { useAsyncData } from '~/composables/useAsyncData'

describe('useAsyncData', () => {
  it('fetches data successfully', async () => {
    const mockData = { id: 1, name: 'Test' }
    const fetcher = vi.fn().mockResolvedValue(mockData)

    const { data, loading, error, execute } = useAsyncData(fetcher, {
      immediate: false
    })

    expect(data.value).toBeNull()
    expect(loading.value).toBe(false)

    await execute()

    expect(fetcher).toHaveBeenCalledOnce()
    expect(data.value).toEqual(mockData)
    expect(error.value).toBeNull()
  })

  it('handles errors', async () => {
    const mockError = new Error('Network error')
    const fetcher = vi.fn().mockRejectedValue(mockError)
    const onError = vi.fn()

    const { data, error, execute } = useAsyncData(fetcher, {
      immediate: false,
      onError
    })

    await execute()

    expect(error.value).toBe(mockError)
    expect(data.value).toBeNull()
    expect(onError).toHaveBeenCalledWith(mockError)
  })

  it('transforms data', async () => {
    const fetcher = vi.fn().mockResolvedValue({ users: [{ id: 1 }] })
    const transform = (data: any) => data.users

    const { data, execute } = useAsyncData(fetcher, {
      immediate: false,
      transform
    })

    await execute()

    expect(data.value).toEqual([{ id: 1 }])
  })
})
```

### Step 3: Write Pinia Store Tests

```typescript
// tests/stores/user.test.ts
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from '~/stores/user'

// Mock $fetch
vi.stubGlobal('$fetch', vi.fn())

describe('useUserStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('logs in user successfully', async () => {
    const mockResponse = {
      user: { id: '1', email: 'test@test.com', name: 'Test', roles: [] },
      token: 'mock-token'
    }
    vi.mocked($fetch).mockResolvedValue(mockResponse)

    const store = useUserStore()
    await store.login('test@test.com', 'password')

    expect($fetch).toHaveBeenCalledWith('/api/auth/login', {
      method: 'POST',
      body: { email: 'test@test.com', password: 'password' }
    })
    expect(store.currentUser).toEqual(mockResponse.user)
    expect(store.isAuthenticated).toBe(true)
  })

  it('checks user roles correctly', async () => {
    const store = useUserStore()
    store.currentUser = {
      id: '1',
      email: 'admin@test.com',
      name: 'Admin',
      roles: ['admin', 'user']
    }

    expect(store.hasRole('admin')).toBe(true)
    expect(store.hasRole('superadmin')).toBe(false)
  })

  it('clears state on logout', async () => {
    vi.mocked($fetch).mockResolvedValue({})

    const store = useUserStore()
    store.currentUser = { id: '1', email: 'test@test.com', name: 'Test', roles: [] }
    store.token = 'token'

    await store.logout()

    expect(store.currentUser).toBeNull()
    expect(store.token).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })
})
```

### Step 4: Implement Minimum Code to Pass

```vue
<!-- components/UserCard.vue -->
<script setup lang="ts">
interface User {
  id: string
  name: string
  email: string
}

const props = defineProps<{
  user: User | null
  loading?: boolean
}>()

const emit = defineEmits<{
  select: [id: string]
}>()

const handleClick = () => {
  if (props.user) {
    emit('select', props.user.id)
  }
}
</script>

<template>
  <div @click="handleClick" class="user-card">
    <div v-if="loading" data-testid="loading-skeleton" class="skeleton">
      Loading...
    </div>
    <template v-else-if="user">
      <h3>{{ user.name }}</h3>
      <p>{{ user.email }}</p>
    </template>
  </div>
</template>
```

### Step 5: Run Full Verification

```bash
# Run all tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm run test tests/components/UserCard.test.ts

# Type checking
npm run typecheck

# Lint
npm run lint

# Build to ensure no errors
npm run build
```

---

## Section 4: Performance Patterns

### Pattern 1: Use Computed Over Methods

**Bad - Method called on every render:**
```vue
<script setup lang="ts">
const items = ref([...])

// ❌ BAD: Recalculates on every render
const getFilteredItems = () => {
  return items.value.filter(item => item.active)
}
</script>

<template>
  <div v-for="item in getFilteredItems()" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

**Good - Computed caches result:**
```vue
<script setup lang="ts">
const items = ref([...])

// ✅ GOOD: Only recalculates when items change
const filteredItems = computed(() => {
  return items.value.filter(item => item.active)
})
</script>

<template>
  <div v-for="item in filteredItems" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

### Pattern 2: Use shallowRef for Large Objects

**Bad - Deep reactivity on large objects:**
```typescript
// ❌ BAD: Creates deep reactive proxy for entire object
const largeDataset = ref<DataItem[]>([])

// Every nested property becomes reactive
largeDataset.value = await fetchLargeDataset()
```

**Good - Shallow reactivity when deep tracking not needed:**
```typescript
// ✅ GOOD: Only tracks the reference, not nested properties
const largeDataset = shallowRef<DataItem[]>([])

// Manually trigger updates
largeDataset.value = await fetchLargeDataset()

// Use triggerRef for in-place mutations
largeDataset.value.push(newItem)
triggerRef(largeDataset)
```

### Pattern 3: Use v-memo for Expensive Lists

**Bad - Re-renders all items on any change:**
```vue
<template>
  <!-- ❌ BAD: All items re-render when anything changes -->
  <div v-for="item in items" :key="item.id">
    <ExpensiveComponent :data="item" />
  </div>
</template>
```

**Good - Memoize items that haven't changed:**
```vue
<template>
  <!-- ✅ GOOD: Only re-renders when item.id or item.updated changes -->
  <div
    v-for="item in items"
    :key="item.id"
    v-memo="[item.id, item.updated]"
  >
    <ExpensiveComponent :data="item" />
  </div>
</template>
```

### Pattern 4: Lazy Load Components

**Bad - All components loaded upfront:**
```vue
<script setup lang="ts">
// ❌ BAD: Imported even if never shown
import HeavyChart from '~/components/HeavyChart.vue'
import AdminPanel from '~/components/AdminPanel.vue'
import DataTable from '~/components/DataTable.vue'
</script>
```

**Good - Components loaded on demand:**
```vue
<script setup lang="ts">
// ✅ GOOD: Only loaded when rendered
const HeavyChart = defineAsyncComponent(() =>
  import('~/components/HeavyChart.vue')
)

const AdminPanel = defineAsyncComponent({
  loader: () => import('~/components/AdminPanel.vue'),
  loadingComponent: LoadingSpinner,
  delay: 200,
  timeout: 5000
})

// With Nuxt lazy prefix
// components/lazy/DataTable.vue automatically becomes lazy
</script>

<template>
  <HeavyChart v-if="showChart" />
  <AdminPanel v-if="isAdmin" />
  <LazyDataTable v-if="showTable" />
</template>
```

### Pattern 5: Virtual Scrolling for Large Lists

**Bad - Render all items at once:**
```vue
<template>
  <!-- ❌ BAD: Renders 10,000 DOM nodes -->
  <div v-for="item in tenThousandItems" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

**Good - Only render visible items:**
```vue
<script setup lang="ts">
import { useVirtualList } from '@vueuse/core'

const items = ref(generateLargeList(10000))

const { list, containerProps, wrapperProps } = useVirtualList(items, {
  itemHeight: 50,
  overscan: 5
})
</script>

<template>
  <!-- ✅ GOOD: Only renders ~20 visible items -->
  <div v-bind="containerProps" class="h-[400px] overflow-auto">
    <div v-bind="wrapperProps">
      <div v-for="{ data, index } in list" :key="index" class="h-[50px]">
        {{ data.name }}
      </div>
    </div>
  </div>
</template>
```

### Pattern 6: Optimize Watchers

**Bad - Watch entire object unnecessarily:**
```typescript
// ❌ BAD: Triggers on any property change
watch(form, () => {
  validateForm()
}, { deep: true })
```

**Good - Watch specific properties:**
```typescript
// ✅ GOOD: Only triggers when email changes
watch(() => form.email, (newEmail) => {
  validateEmail(newEmail)
})

// ✅ GOOD: Watch multiple specific props
watch(
  [() => form.email, () => form.password],
  ([email, password]) => {
    validateCredentials(email, password)
  }
)
```

### Pattern 7: Debounce Expensive Operations

**Bad - Run on every keystroke:**
```vue
<script setup lang="ts">
const searchQuery = ref('')

// ❌ BAD: API call on every keystroke
watch(searchQuery, async (query) => {
  results.value = await searchAPI(query)
})
</script>
```

**Good - Debounce the operation:**
```vue
<script setup lang="ts">
import { useDebounceFn } from '@vueuse/core'

const searchQuery = ref('')

// ✅ GOOD: Wait for user to stop typing
const debouncedSearch = useDebounceFn(async (query: string) => {
  results.value = await searchAPI(query)
}, 300)

watch(searchQuery, (query) => {
  debouncedSearch(query)
})
</script>
```

---

## Section 5: Core Responsibilities

### 1. Component Architecture & Composition API
- Design scalable component hierarchies using script setup syntax
- Create reusable composables following Vue 3 best practices
- Implement proper TypeScript typing for components and composables
- Manage reactivity with ref, reactive, computed, and watch
- Optimize component rendering with proper key usage and v-memo

### 2. Nuxt 3 Application Development
- Configure Nuxt 3 apps for SSR, SSG, or hybrid rendering
- Implement file-based routing with dynamic routes and middleware
- Create server routes and API endpoints with Nitro
- Optimize bundle size and code splitting
- Configure auto-imports and module layer architecture

### 3. State Management
- Design Pinia stores with proper TypeScript support
- Implement state persistence and hydration strategies
- Create shared composables for cross-component logic
- Manage global state vs local component state
- Handle async state and loading patterns

### 4. Performance Optimization
- Implement lazy loading for routes and components
- Optimize images with Nuxt Image module
- Configure caching strategies (client, server, CDN)
- Monitor and improve Core Web Vitals
- Implement virtual scrolling for large lists

### 5. Type Safety & Developer Experience
- Configure TypeScript with strict mode
- Generate types for Nuxt auto-imports
- Type API responses and store state
- Set up ESLint and Prettier for Vue/Nuxt
- Implement proper error handling and boundaries

### 6. Client-Side Security
- Prevent XSS through proper template sanitization
- Configure Content Security Policy (CSP)
- Validate and sanitize user inputs
- Implement secure authentication flows
- Protect against CSRF attacks

---

## Section 6: Top 7 Implementation Patterns

### Pattern 1: Composable-First Architecture

**Use composables to extract and reuse logic across components:**

```typescript
// composables/useAsyncData.ts
import { ref, type Ref } from 'vue'

export interface UseAsyncDataOptions<T> {
  immediate?: boolean
  onError?: (error: Error) => void
  transform?: (data: any) => T
}

export function useAsyncData<T>(
  fetcher: () => Promise<T>,
  options: UseAsyncDataOptions<T> = {}
) {
  const { immediate = true, onError, transform } = options

  const data: Ref<T | null> = ref(null)
  const error: Ref<Error | null> = ref(null)
  const loading = ref(false)

  const execute = async () => {
    loading.value = true
    error.value = null

    try {
      const result = await fetcher()
      data.value = transform ? transform(result) : result
    } catch (e) {
      error.value = e as Error
      onError?.(e as Error)
    } finally {
      loading.value = false
    }
  }

  if (immediate) execute()

  return { data, error, loading, execute }
}
```

**Usage:**
```vue
<script setup lang="ts">
import { useAsyncData } from '~/composables/useAsyncData'

interface User {
  id: string
  name: string
}

const { data: user, loading, error } = useAsyncData<User>(
  () => $fetch('/api/user/me'),
  { immediate: true }
)
</script>
```

### Pattern 2: Type-Safe Pinia Stores

**Create strongly-typed stores with composition API:**

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: string
  email: string
  name: string
  roles: string[]
}

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const token = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!currentUser.value)
  const hasRole = computed(() => (role: string) =>
    currentUser.value?.roles.includes(role) ?? false
  )

  // Actions
  async function login(email: string, password: string) {
    const response = await $fetch<{ user: User; token: string }>('/api/auth/login', {
      method: 'POST',
      body: { email, password }
    })

    currentUser.value = response.user
    token.value = response.token

    // Persist token
    if (process.client) {
      localStorage.setItem('auth_token', response.token)
    }
  }

  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' })
    currentUser.value = null
    token.value = null

    if (process.client) {
      localStorage.removeItem('auth_token')
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return

    try {
      const user = await $fetch<User>('/api/user/me', {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      currentUser.value = user
    } catch (error) {
      // Token invalid, clear auth state
      await logout()
    }
  }

  return {
    currentUser,
    token,
    isAuthenticated,
    hasRole,
    login,
    logout,
    fetchCurrentUser
  }
})
```

### Pattern 3: Nuxt 3 Middleware & Route Guards

**Implement authentication and authorization middleware:**

```typescript
// middleware/auth.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const userStore = useUserStore()
  const publicRoutes = ['/login', '/register', '/forgot-password']

  // Allow public routes
  if (publicRoutes.includes(to.path)) {
    return
  }

  // Redirect to login if not authenticated
  if (!userStore.isAuthenticated) {
    return navigateTo('/login', { redirectCode: 401 })
  }

  // Check role-based access
  if (to.meta.requiresAdmin && !userStore.hasRole('admin')) {
    return abortNavigation({
      statusCode: 403,
      message: 'Access denied'
    })
  }
})
```

**Page with metadata:**
```vue
<script setup lang="ts">
definePageMeta({
  requiresAdmin: true,
  layout: 'admin'
})

const users = await useFetch('/api/admin/users')
</script>
```

### Pattern 4: Server API Routes with Validation

**Create type-safe API endpoints with input validation:**

```typescript
// server/api/users/[id].post.ts
import { z } from 'zod'
import { createError } from 'h3'

const updateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(18).max(120).optional()
})

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')

  if (!id) {
    throw createError({
      statusCode: 400,
      message: 'User ID is required'
    })
  }

  // Validate request body
  const body = await readBody(event)
  const result = updateUserSchema.safeParse(body)

  if (!result.success) {
    throw createError({
      statusCode: 400,
      message: 'Invalid request data',
      data: result.error.format()
    })
  }

  // Check authentication
  const session = await requireUserSession(event)

  // Check authorization (users can only update themselves unless admin)
  if (session.user.id !== id && !session.user.roles.includes('admin')) {
    throw createError({
      statusCode: 403,
      message: 'Not authorized to update this user'
    })
  }

  // Update user in database
  const updatedUser = await db.users.update(id, result.data)

  return updatedUser
})
```

### Pattern 5: Optimized Component Loading

**Implement strategic code splitting and lazy loading:**

```vue
<script setup lang="ts">
// Lazy load heavy components
const HeavyChart = defineAsyncComponent(() =>
  import('~/components/HeavyChart.vue')
)

const AdminPanel = defineAsyncComponent({
  loader: () => import('~/components/AdminPanel.vue'),
  loadingComponent: () => h('div', 'Loading...'),
  delay: 200,
  timeout: 3000
})

const showChart = ref(false)
const userStore = useUserStore()

// Only load when needed
const loadChart = () => {
  showChart.value = true
}
</script>

<template>
  <div>
    <button @click="loadChart">Show Chart</button>

    <!-- Component only loads when showChart is true -->
    <HeavyChart v-if="showChart" :data="chartData" />

    <!-- Admin panel only for admins -->
    <AdminPanel v-if="userStore.hasRole('admin')" />
  </div>
</template>
```

**Nuxt configuration for optimal splitting:**

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'vendor-vue': ['vue', 'vue-router', 'pinia'],
            'vendor-ui': ['@headlessui/vue', '@heroicons/vue'],
          }
        }
      }
    }
  },

  experimental: {
    payloadExtraction: true, // Extract payload for better caching
    componentIslands: true    // Islands architecture for partial hydration
  }
})
```

### Pattern 6: VueUse Integration for Common Logic

**Leverage VueUse composables for robust functionality:**

```vue
<script setup lang="ts">
import { useLocalStorage, useMediaQuery, useIntersectionObserver } from '@vueuse/core'
import { ref, watch } from 'vue'

// Persistent dark mode
const isDark = useLocalStorage('dark-mode', false)

// Responsive breakpoints
const isMobile = useMediaQuery('(max-width: 768px)')
const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)')
const isDesktop = useMediaQuery('(min-width: 1025px)')

// Infinite scroll with intersection observer
const target = ref<HTMLElement | null>(null)
const isVisible = ref(false)

useIntersectionObserver(
  target,
  ([{ isIntersecting }]) => {
    isVisible.value = isIntersecting
  },
  { threshold: 0.5 }
)

// Load more when target is visible
watch(isVisible, (visible) => {
  if (visible && !loading.value) {
    loadMore()
  }
})

const loadMore = async () => {
  // Load more items
}
</script>

<template>
  <div :class="{ dark: isDark }">
    <button @click="isDark = !isDark">
      Toggle {{ isDark ? 'Light' : 'Dark' }} Mode
    </button>

    <div v-if="isMobile">Mobile View</div>
    <div v-else-if="isTablet">Tablet View</div>
    <div v-else>Desktop View</div>

    <!-- Items list -->
    <div v-for="item in items" :key="item.id">
      {{ item.name }}
    </div>

    <!-- Intersection observer target for infinite scroll -->
    <div ref="target" class="loading-trigger">
      <span v-if="isVisible">Loading more...</span>
    </div>
  </div>
</template>
```

### Pattern 7: SSR-Safe Data Fetching

**Handle data fetching correctly for SSR/SSG:**

```vue
<script setup lang="ts">
// ✅ CORRECT: Use Nuxt data fetching composables
// These work on both server and client, with automatic hydration

// Basic fetch
const { data: posts } = await useFetch('/api/posts', {
  key: 'posts-list',
  transform: (data) => data.posts,
  getCachedData: (key) => useNuxtApp().static.data[key]
})

// With params
const route = useRoute()
const { data: post } = await useFetch(`/api/posts/${route.params.id}`, {
  key: `post-${route.params.id}`,
  watch: [() => route.params.id] // Refetch when ID changes
})

// With lazy loading (client-side only initially)
const { data: comments, pending } = await useLazyFetch(`/api/posts/${route.params.id}/comments`)

// Using useAsyncData for custom async operations
const { data: userData, refresh } = await useAsyncData(
  'user-profile',
  async () => {
    const [profile, settings] = await Promise.all([
      $fetch('/api/user/profile'),
      $fetch('/api/user/settings')
    ])
    return { profile, settings }
  },
  {
    server: true,  // Fetch on server
    lazy: false,   // Wait for data before rendering
    default: () => ({ profile: null, settings: null })
  }
)

// ❌ WRONG: Direct fetch calls will execute twice (server + client)
// const response = await fetch('/api/posts') // Don't do this!
</script>

<template>
  <div>
    <article v-if="post">
      <h1>{{ post.title }}</h1>
      <p>{{ post.content }}</p>
    </article>

    <section v-if="!pending">
      <h2>Comments ({{ comments?.length || 0 }})</h2>
      <div v-for="comment in comments" :key="comment.id">
        {{ comment.text }}
      </div>
    </section>
    <div v-else>Loading comments...</div>
  </div>
</template>
```

See [references/advanced-patterns.md](./references/advanced-patterns.md) for more patterns including plugins, modules, and advanced composables.

---

## Section 7: Security

**Risk Level**: MEDIUM - Client-side applications are vulnerable to XSS, injection, and data exposure

### Top 3 Critical Vulnerabilities

#### 1. Cross-Site Scripting (XSS)
**Risk**: Attackers inject malicious scripts through user input, stealing data or performing unauthorized actions.

**Prevention**:
```vue
<script setup lang="ts">
import DOMPurify from 'isomorphic-dompurify'

const userInput = ref('')
const sanitizedHtml = computed(() => DOMPurify.sanitize(userInput.value))

// ✅ SAFE: Vue's template binding automatically escapes HTML
const displayText = ref('<script>alert("XSS")</script>')
</script>

<template>
  <!-- ✅ SAFE: Automatic escaping -->
  <div>{{ displayText }}</div>

  <!-- ⚠️ DANGEROUS: Only use with sanitized content -->
  <div v-html="sanitizedHtml"></div>

  <!-- ❌ NEVER: Raw user input -->
  <!-- <div v-html="userInput"></div> -->
</template>
```

#### 2. Insecure Data Exposure
**Risk**: Sensitive data leaked through client-side code, API responses, or state management.

**Prevention**:
```typescript
// ✅ Server API route - keep secrets on server
// server/api/payment.post.ts
export default defineEventHandler(async (event) => {
  const apiKey = useRuntimeConfig().stripeSecretKey // Server-only

  const payment = await stripe.charges.create({
    amount: 1000,
    currency: 'usd',
    source: req.body.token
  }, {
    apiKey // Never exposed to client
  })

  // Return only necessary data
  return {
    id: payment.id,
    status: payment.status,
    amount: payment.amount
  }
})
```

#### 3. CSRF (Cross-Site Request Forgery)
**Risk**: Attackers trick users into executing unwanted actions on authenticated sessions.

**Prevention**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // Enable CSRF protection for SSR
  security: {
    headers: {
      crossOriginEmbedderPolicy: 'require-corp',
      crossOriginOpenerPolicy: 'same-origin',
      crossOriginResourcePolicy: 'same-origin'
    }
  }
})

// Middleware for API routes
// server/middleware/csrf.ts
export default defineEventHandler((event) => {
  if (event.method !== 'GET' && event.method !== 'HEAD') {
    const origin = getHeader(event, 'origin')
    const host = getHeader(event, 'host')

    if (origin && !origin.includes(host)) {
      throw createError({
        statusCode: 403,
        message: 'CSRF validation failed'
      })
    }
  }
})
```

### OWASP Top 10 Mapping

| OWASP Category | Relevance | Mitigation in Vue/Nuxt |
|----------------|-----------|------------------------|
| A03:2021 Injection | HIGH | Input validation, parameterized queries, sanitization |
| A05:2021 Security Misconfiguration | MEDIUM | CSP headers, secure defaults, environment configs |
| A06:2021 Vulnerable Components | MEDIUM | Regular updates, audit dependencies, Snyk/npm audit |
| A07:2021 Authentication Failures | HIGH | Secure session management, proper token handling |
| A08:2021 Data Integrity Failures | MEDIUM | Signed payloads, integrity checks, HTTPS only |

For detailed security examples and complete OWASP coverage, see [references/security-examples.md](./references/security-examples.md).

---

## Section 8: Common Mistakes

### Mistake 1: Reactivity Loss with Destructuring

**Problem**:
```typescript
// ❌ WRONG: Loses reactivity
const userStore = useUserStore()
const { currentUser } = userStore // Not reactive!

watch(currentUser, () => {
  console.log('This will never trigger!')
})
```

**Solution**:
```typescript
// ✅ CORRECT: Preserve reactivity with storeToRefs
import { storeToRefs } from 'pinia'

const userStore = useUserStore()
const { currentUser } = storeToRefs(userStore) // Reactive!

watch(currentUser, () => {
  console.log('This works!')
})

// Or access directly
watch(() => userStore.currentUser, () => {
  console.log('This also works!')
})
```

### Mistake 2: Memory Leaks from Event Listeners

**Problem**:
```typescript
// ❌ WRONG: Event listener not cleaned up
onMounted(() => {
  window.addEventListener('resize', handleResize)
})
// Component unmounts but listener persists!
```

**Solution**:
```typescript
// ✅ CORRECT: Clean up in onUnmounted
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// ✅ BETTER: Use VueUse composable
import { useEventListener } from '@vueuse/core'
useEventListener(window, 'resize', handleResize) // Auto cleanup!
```

### Mistake 3: Incorrect useFetch Usage

**Problem**:
```typescript
// ❌ WRONG: useFetch in event handler
const handleClick = async () => {
  const { data } = await useFetch('/api/data') // Error! Not allowed in functions
}

// ❌ WRONG: Inside conditional
if (someCondition) {
  const { data } = await useFetch('/api/data') // Error! Must be top-level
}
```

**Solution**:
```typescript
// ✅ CORRECT: Use $fetch for programmatic calls
const handleClick = async () => {
  const data = await $fetch('/api/data') // Works in functions
}

// ✅ CORRECT: useFetch at component top-level
const { data, refresh } = await useFetch('/api/data', {
  immediate: false
})

const handleClick = () => {
  refresh() // Trigger refetch
}
```

### Mistake 4: Not Handling SSR/Client Differences

**Problem**:
```typescript
// ❌ WRONG: Accessing browser APIs during SSR
const windowWidth = ref(window.innerWidth) // Error! window undefined on server

onMounted(() => {
  localStorage.setItem('key', 'value') // Error! localStorage undefined on server
})
```

**Solution**:
```typescript
// ✅ CORRECT: Check environment
const windowWidth = ref(0)

onMounted(() => {
  if (process.client) {
    windowWidth.value = window.innerWidth
  }
})

// ✅ BETTER: Use VueUse with SSR safety
import { useWindowSize, useLocalStorage } from '@vueuse/core'

const { width } = useWindowSize() // SSR-safe
const stored = useLocalStorage('key', 'default') // SSR-safe
```

### Mistake 5: Inefficient Watchers

**Problem**:
```typescript
// ❌ WRONG: Watching entire object (triggers on any property change)
const form = reactive({
  name: '',
  email: '',
  phone: '',
  address: ''
})

watch(form, () => {
  console.log('Triggers for ANY field change!')
})
```

**Solution**:
```typescript
// ✅ CORRECT: Watch specific properties
watch(() => form.email, (newEmail) => {
  validateEmail(newEmail)
})

// ✅ CORRECT: Watch multiple specific properties
watch([() => form.email, () => form.phone], ([email, phone]) => {
  validateContactInfo(email, phone)
})

// ✅ CORRECT: Deep watch with immediate flag when needed
watch(form, () => {
  saveFormDraft(form)
}, {
  deep: true,
  debounce: 500 // Debounce to avoid excessive calls
})
```

---

## Section 9: Testing

### Test Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: 'happy-dom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'tests/']
    }
  },
  resolve: {
    alias: {
      '~': resolve(__dirname, './')
    }
  }
})
```

### Test Setup File

```typescript
// tests/setup.ts
import { config } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'

// Global plugins
config.global.plugins = [createTestingPinia()]

// Mock Nuxt composables
vi.mock('#app', () => ({
  useNuxtApp: () => ({ $fetch: vi.fn() }),
  useRuntimeConfig: () => ({ public: {} }),
  useFetch: vi.fn(),
  useAsyncData: vi.fn(),
  navigateTo: vi.fn(),
  definePageMeta: vi.fn()
}))

// Mock $fetch globally
vi.stubGlobal('$fetch', vi.fn())
```

### Component Testing Patterns

```typescript
// tests/components/Form.test.ts
import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import Form from '~/components/Form.vue'

describe('Form', () => {
  it('validates required fields', async () => {
    const wrapper = mount(Form)

    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('.error').text()).toContain('Name is required')
  })

  it('submits valid data', async () => {
    const onSubmit = vi.fn()
    const wrapper = mount(Form, {
      props: { onSubmit }
    })

    await wrapper.find('input[name="name"]').setValue('John')
    await wrapper.find('input[name="email"]').setValue('john@test.com')
    await wrapper.find('form').trigger('submit')
    await flushPromises()

    expect(onSubmit).toHaveBeenCalledWith({
      name: 'John',
      email: 'john@test.com'
    })
  })

  it('shows loading state during submission', async () => {
    const wrapper = mount(Form, {
      props: {
        onSubmit: () => new Promise(r => setTimeout(r, 100))
      }
    })

    await wrapper.find('input[name="name"]').setValue('John')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
    expect(wrapper.find('.loading').exists()).toBe(true)
  })
})
```

### Testing Async Operations

```typescript
// tests/composables/useApi.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { flushPromises } from '@vue/test-utils'
import { useApi } from '~/composables/useApi'

describe('useApi', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('handles concurrent requests', async () => {
    const results = ['first', 'second']
    let callCount = 0

    vi.mocked($fetch).mockImplementation(() =>
      Promise.resolve(results[callCount++])
    )

    const { data, execute } = useApi('/api/test')

    // Fire two requests
    execute()
    execute()
    await flushPromises()

    // Should have latest result
    expect(data.value).toBe('second')
  })

  it('cancels pending request on new request', async () => {
    const abortSpy = vi.fn()
    vi.mocked($fetch).mockImplementation((_, opts) => {
      opts?.signal?.addEventListener('abort', abortSpy)
      return new Promise(() => {})
    })

    const { execute } = useApi('/api/test')

    execute()
    execute() // Should cancel first

    expect(abortSpy).toHaveBeenCalled()
  })
})
```

---

## Section 10: Critical Reminders

### Type Safety
- Always enable TypeScript strict mode in `tsconfig.json`
- Type all component props with `defineProps<T>()` syntax
- Generate types for Nuxt auto-imports: `nuxt prepare`
- Use runtime validation (Zod) for API inputs, not just TypeScript

### Performance
- Use `useFetch`/`useAsyncData` for data fetching (SSR-compatible)
- Implement lazy loading for routes: `defineAsyncComponent()`
- Optimize images: Use Nuxt Image module with proper formats (WebP, AVIF)
- Monitor bundle size: `nuxi analyze` and set budgets
- Use `v-memo` for expensive lists that don't change often

### Security
- Never use `v-html` with unsanitized user input
- Configure CSP headers in `nuxt.config.ts`
- Validate all inputs on both client and server
- Store secrets in `.env` files, never in client code
- Use `httpOnly` cookies for sensitive tokens

### State Management
- Use Pinia for global state, composables for shared logic
- Extract composables from `storeToRefs()` to maintain reactivity
- Persist auth state securely (httpOnly cookies preferred)
- Clear sensitive state on logout
- Avoid prop drilling: use provide/inject or stores

### SSR/SSG
- Always check `process.client` before accessing browser APIs
- Use Nuxt data fetching composables, not raw fetch
- Configure `routeRules` for page-level rendering strategy
- Handle hydration mismatches with `<ClientOnly>` when needed
- Set appropriate cache headers for static assets

### Developer Experience
- Enable Nuxt DevTools for debugging
- Use Vue DevTools for component inspection
- Set up ESLint + Prettier with Vue/Nuxt configs
- Write tests with Vitest + Vue Test Utils
- Document complex composables and stores

---

## Section 11: Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] **Identify requirements** - Parse user story/task into specific acceptance criteria
- [ ] **Design component structure** - Sketch component hierarchy and data flow
- [ ] **Plan composables** - Identify reusable logic to extract
- [ ] **Consider SSR** - Determine rendering strategy (SSR/SSG/SPA)
- [ ] **Check existing patterns** - Review similar components/composables in codebase
- [ ] **Write test cases** - Create failing tests for expected behavior
- [ ] **Plan state management** - Decide local vs store state

### Phase 2: During Implementation

- [ ] **TDD cycle** - Write test -> Implement -> Refactor -> Repeat
- [ ] **Type everything** - Props, emits, composable returns, API responses
- [ ] **Use computed** - For derived state instead of methods
- [ ] **Optimize reactivity** - Use shallowRef for large objects, watch specific props
- [ ] **Handle edge cases** - Loading states, errors, empty data
- [ ] **SSR safety** - Check `process.client` before browser APIs
- [ ] **Clean up effects** - Use onUnmounted or VueUse composables
- [ ] **Security checks** - No v-html with user input, validate inputs

### Phase 3: Before Committing

- [ ] **All tests pass** - Run `npm run test`
- [ ] **Type check passes** - Run `npm run typecheck`
- [ ] **Lint passes** - Run `npm run lint`
- [ ] **Build succeeds** - Run `npm run build`
- [ ] **Manual testing** - Verify in browser with dev tools
- [ ] **Performance check** - No console warnings, smooth rendering
- [ ] **Security review** - No exposed secrets, inputs validated
- [ ] **Documentation** - Complex logic has comments/JSDoc

### Verification Commands

```bash
# Run all checks before commit
npm run test && npm run typecheck && npm run lint && npm run build

# Quick verification during development
npm run dev  # Should start without errors

# Full test suite with coverage
npm run test:coverage

# E2E tests
npm run test:e2e
```

---

## Section 12: Summary

This skill provides expertise in building modern, performant, type-safe Vue 3 and Nuxt 3 applications. Key takeaways:

**Architecture**: Design component hierarchies with Composition API, extract logic into composables, and manage state with Pinia. Follow the composable-first approach for maximum reusability.

**Nuxt 3 Patterns**: Leverage file-based routing, auto-imports, and Nitro server for full-stack development. Configure rendering strategies (SSR/SSG/hybrid) per route for optimal performance.

**Type Safety**: Use TypeScript strict mode throughout. Type components, stores, and API responses. Combine compile-time TypeScript with runtime validation (Zod) for robust applications.

**Performance**: Implement strategic code splitting, lazy loading, and optimized data fetching with `useFetch`. Monitor Core Web Vitals and set performance budgets.

**Security**: Prevent XSS through proper escaping and sanitization. Validate all inputs. Configure CSP headers. Keep secrets on the server. Implement CSRF protection.

**Common Pitfalls**: Preserve reactivity with `storeToRefs`. Clean up event listeners. Use correct data fetching APIs (`useFetch` vs `$fetch`). Handle SSR/client differences. Write efficient watchers.

**Best Practices**:
- Keep components focused and composable
- Extract and test composables independently
- Use VueUse for common patterns
- Configure ESLint and Prettier
- Write tests for critical logic
- Monitor performance and bundle size

**Risk Level**: MEDIUM - Primary concerns are client-side security (XSS, data exposure) and performance (bundle size, SSR complexity).

For advanced patterns, see [references/advanced-patterns.md](./references/advanced-patterns.md).
For detailed security examples, see [references/security-examples.md](./references/security-examples.md).
