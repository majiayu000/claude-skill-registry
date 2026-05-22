---
name: frontend-development
description: "Multi-framework frontend development. Frameworks: React 18+ (Suspense, hooks, TanStack), Vue 3 (Composition API, Pinia, Nuxt), Svelte 5 (Runes, SvelteKit), Angular (Signals, standalone). Common: TypeScript, state management, routing, data fetching, performance optimization, component patterns. Actions: create, build, implement, style, optimize, refactor components/pages/features. Keywords: React, Vue, Svelte, Angular, component, TypeScript, hooks, Composition API, runes, signals, useSuspenseQuery, Pinia, stores, state management, routing, lazy loading, Suspense, performance, bundle size, code splitting, reactivity, props, events. Use when: creating components in any framework, building pages, fetching data, implementing routing, state management, optimizing performance, organizing frontend code, choosing between frameworks."
---

# Frontend Development Guidelines

## Purpose

Comprehensive guide for modern frontend development across React, Vue 3, Svelte 5, and Angular. Covers framework-specific patterns, common architectural principles, and cross-framework best practices.

## When to Use This Skill

- Creating components or pages in React, Vue, Svelte, or Angular
- Building new features with framework-specific patterns
- Implementing state management (Pinia, Zustand, stores, signals)
- Setting up routing (TanStack Router, Vue Router, SvelteKit, Angular Router)
- Data fetching patterns (TanStack Query, composables, SvelteKit load functions)
- Performance optimization across frameworks
- Component composition and reusability
- TypeScript integration and best practices
- Choosing the right framework for a project
- Migrating between frameworks

---

## Framework Selection Guide

Choose your framework based on project requirements:

| Framework | Best For | Learning Curve | Performance | Ecosystem |
|-----------|----------|----------------|-------------|-----------|
| **React** | Large apps, strong typing, enterprise | Medium | Good | Largest |
| **Vue 3** | Progressive adoption, approachable | Low | Excellent | Growing |
| **Svelte 5** | Small/medium apps, native feel | Low | Best | Smaller |
| **Angular** | Enterprise, full-featured | Steep | Good | Complete |

**Quick Decision:**
- **Existing codebase?** Use what's there or plan migration
- **Team experience?** Leverage existing knowledge
- **Project size?** Large → React/Angular, Medium → Vue/React, Small → Svelte/Vue
- **Performance critical?** Svelte > Vue > React ≈ Angular
- **TypeScript required?** All support it well (Angular best integrated)
- **Ecosystem needs?** React > Vue > Angular > Svelte

See framework-specific sections below for detailed patterns.

---

## Quick Framework Comparison

| Feature | React | Vue 3 | Svelte 5 | Angular |
|---------|-------|-------|----------|---------|
| **Reactivity** | Hooks (useState) | ref/reactive | Runes ($state) | Signals |
| **Components** | JSX/TSX | SFC (.vue) | SFC (.svelte) | Decorators/Class |
| **State Mgmt** | Zustand/Context | Pinia | Stores | Services |
| **Routing** | React Router/TanStack | Vue Router | SvelteKit | Angular Router |
| **Data Fetching** | TanStack Query | Composables/VueQuery | Load functions | HttpClient/RxJS |
| **Styling** | CSS-in-JS/Modules | Scoped CSS | Scoped CSS | Component styles |
| **Full-Stack** | Next.js | Nuxt | SvelteKit | Universal/SSR |
| **Bundle Size** | ~40KB | ~32KB | ~3KB | ~60KB |
| **Compiler** | Runtime | Runtime | Compile-time | AOT Compiler |

**Jump to:**
- [React Development](#react-development) - Hooks, Suspense, TanStack ecosystem
- [Vue 3 Development](#vue-3-development) - Composition API, Pinia, Nuxt
- [Svelte 5 Development](#svelte-5-development) - Runes, SvelteKit, minimal runtime
- [Angular Development](#angular-development) - Signals, standalone components, RxJS
- [Framework-Agnostic Patterns](#framework-agnostic-patterns) - Universal concepts

---

## React Development

### New Component Checklist

Creating a component? Follow this checklist:

- [ ] Use `React.FC<Props>` pattern with TypeScript
- [ ] Lazy load if heavy component: `React.lazy(() => import())`
- [ ] Wrap in `<SuspenseLoader>` for loading states
- [ ] Use `useSuspenseQuery` for data fetching
- [ ] Import aliases: `@/`, `~types`, `~components`, `~features`
- [ ] Styles: Inline if <100 lines, separate file if >100 lines
- [ ] Use `useCallback` for event handlers passed to children
- [ ] Default export at bottom
- [ ] No early returns with loading spinners
- [ ] Use `useMuiSnackbar` for user notifications

### New Feature Checklist

Creating a feature? Set up this structure:

- [ ] Create `features/{feature-name}/` directory
- [ ] Create subdirectories: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] Create API service file: `api/{feature}Api.ts`
- [ ] Set up TypeScript types in `types/`
- [ ] Create route in `routes/{feature-name}/index.tsx`
- [ ] Lazy load feature components
- [ ] Use Suspense boundaries
- [ ] Export public API from feature `index.ts`

---

## Import Aliases Quick Reference

| Alias | Resolves To | Example |
|-------|-------------|---------|
| `@/` | `src/` | `import { apiClient } from '@/lib/apiClient'` |
| `~types` | `src/types` | `import type { User } from '~types/user'` |
| `~components` | `src/components` | `import { SuspenseLoader } from '~components/SuspenseLoader'` |
| `~features` | `src/features` | `import { authApi } from '~features/auth'` |

Defined in: [vite.config.ts](../../vite.config.ts) lines 180-185

---

## Common Imports Cheatsheet

```typescript
// React & Lazy Loading
import React, { useState, useCallback, useMemo } from 'react';
const Heavy = React.lazy(() => import('./Heavy'));

// MUI Components
import { Box, Paper, Typography, Button, Grid } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';

// TanStack Query (Suspense)
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';

// TanStack Router
import { createFileRoute } from '@tanstack/react-router';

// Project Components
import { SuspenseLoader } from '~components/SuspenseLoader';

// Hooks
import { useAuth } from '@/hooks/useAuth';
import { useMuiSnackbar } from '@/hooks/useMuiSnackbar';

// Types
import type { Post } from '~types/post';
```

---

## Topic Guides

### 🎨 Component Patterns

**Modern React components use:**
- `React.FC<Props>` for type safety
- `React.lazy()` for code splitting
- `SuspenseLoader` for loading states
- Named const + default export pattern

**Key Concepts:**
- Lazy load heavy components (DataGrid, charts, editors)
- Always wrap lazy components in Suspense
- Use SuspenseLoader component (with fade animation)
- Component structure: Props → Hooks → Handlers → Render → Export

**[📖 Complete Guide: resources/component-patterns.md](resources/component-patterns.md)**

---

### 📊 Data Fetching

**PRIMARY PATTERN: useSuspenseQuery**
- Use with Suspense boundaries
- Cache-first strategy (check grid cache before API)
- Replaces `isLoading` checks
- Type-safe with generics

**API Service Layer:**
- Create `features/{feature}/api/{feature}Api.ts`
- Use `apiClient` axios instance
- Centralized methods per feature
- Route format: `/form/route` (NOT `/api/form/route`)

**[📖 Complete Guide: resources/data-fetching.md](resources/data-fetching.md)**

---

### 📁 File Organization

**features/ vs components/:**
- `features/`: Domain-specific (posts, comments, auth)
- `components/`: Truly reusable (SuspenseLoader, CustomAppBar)

**Feature Subdirectories:**
```
features/
  my-feature/
    api/          # API service layer
    components/   # Feature components
    hooks/        # Custom hooks
    helpers/      # Utility functions
    types/        # TypeScript types
```

**[📖 Complete Guide: resources/file-organization.md](resources/file-organization.md)**

---

### 🎨 Styling

**Inline vs Separate:**
- <100 lines: Inline `const styles: Record<string, SxProps<Theme>>`
- >100 lines: Separate `.styles.ts` file

**Primary Method:**
- Use `sx` prop for MUI components
- Type-safe with `SxProps<Theme>`
- Theme access: `(theme) => theme.palette.primary.main`

**MUI v7 Grid:**
```typescript
<Grid size={{ xs: 12, md: 6 }}>  // ✅ v7 syntax
<Grid xs={12} md={6}>             // ❌ Old syntax
```

**[📖 Complete Guide: resources/styling-guide.md](resources/styling-guide.md)**

---

### 🛣️ Routing

**TanStack Router - Folder-Based:**
- Directory: `routes/my-route/index.tsx`
- Lazy load components
- Use `createFileRoute`
- Breadcrumb data in loader

**Example:**
```typescript
import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

const MyPage = lazy(() => import('@/features/my-feature/components/MyPage'));

export const Route = createFileRoute('/my-route/')({
    component: MyPage,
    loader: () => ({ crumb: 'My Route' }),
});
```

**[📖 Complete Guide: resources/routing-guide.md](resources/routing-guide.md)**

---

### ⏳ Loading & Error States

**CRITICAL RULE: No Early Returns**

```typescript
// ❌ NEVER - Causes layout shift
if (isLoading) {
    return <LoadingSpinner />;
}

// ✅ ALWAYS - Consistent layout
<SuspenseLoader>
    <Content />
</SuspenseLoader>
```

**Why:** Prevents Cumulative Layout Shift (CLS), better UX

**Error Handling:**
- Use `useMuiSnackbar` for user feedback
- NEVER `react-toastify`
- TanStack Query `onError` callbacks

**[📖 Complete Guide: resources/loading-and-error-states.md](resources/loading-and-error-states.md)**

---

### ⚡ Performance

**Optimization Patterns:**
- `useMemo`: Expensive computations (filter, sort, map)
- `useCallback`: Event handlers passed to children
- `React.memo`: Expensive components
- Debounced search (300-500ms)
- Memory leak prevention (cleanup in useEffect)

**[📖 Complete Guide: resources/performance.md](resources/performance.md)**

---

### 📘 TypeScript

**Standards:**
- Strict mode, no `any` type
- Explicit return types on functions
- Type imports: `import type { User } from '~types/user'`
- Component prop interfaces with JSDoc

**[📖 Complete Guide: resources/typescript-standards.md](resources/typescript-standards.md)**

---

### 🔧 Common Patterns

**Covered Topics:**
- React Hook Form with Zod validation
- DataGrid wrapper contracts
- Dialog component standards
- `useAuth` hook for current user
- Mutation patterns with cache invalidation

**[📖 Complete Guide: resources/common-patterns.md](resources/common-patterns.md)**

---

### 📚 Complete Examples

**Full working examples:**
- Modern component with all patterns
- Complete feature structure
- API service layer
- Route with lazy loading
- Suspense + useSuspenseQuery
- Form with validation

**[📖 Complete Guide: resources/complete-examples.md](resources/complete-examples.md)**

---

## React-Specific Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Create a React component | [component-patterns.md](resources/component-patterns.md) |
| Fetch data with TanStack Query | [data-fetching.md](resources/data-fetching.md) |
| Organize files/folders | [file-organization.md](resources/file-organization.md) |
| Style with MUI v7 | [styling-guide.md](resources/styling-guide.md) |
| Set up TanStack Router | [routing-guide.md](resources/routing-guide.md) |
| Handle loading/errors | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Optimize React performance | [performance.md](resources/performance.md) |
| TypeScript types | [typescript-standards.md](resources/typescript-standards.md) |
| Forms/Auth/DataGrid | [common-patterns.md](resources/common-patterns.md) |
| See full React examples | [complete-examples.md](resources/complete-examples.md) |

**Note:** Resources above are React-specific. For Vue/Svelte/Angular, see framework sections in this document.

---

## Core Principles (All Frameworks)

1. **Lazy Load Heavy Components**: Routes, data grids, charts, editors, modals
2. **Consistent Loading States**: Avoid layout shift with proper loading UI
3. **Type Safety**: Use TypeScript for all components and APIs
4. **Component Composition**: Small, focused components with clear responsibilities
5. **Unidirectional Data Flow**: Props down, events up
6. **Performance First**: Memoize expensive computations, virtual scrolling for lists
7. **Organized Features**: Group related code (components, state, types, utilities)
8. **Framework Idioms**: Use framework-specific patterns (hooks, composables, runes, services)

### React-Specific Principles

1. **useSuspenseQuery**: Primary data fetching pattern for new code
2. **No Early Returns**: Prevents layout shift (use Suspense boundaries)
3. **Import Aliases**: Use @/, ~types, ~components, ~features
4. **Styles Based on Size**: <100 inline, >100 separate file

### Vue-Specific Principles

1. **Composition API**: Prefer over Options API for reusability
2. **Script Setup**: Use for cleaner syntax and better performance
3. **Composables**: Extract reusable logic like React hooks
4. **Pinia for State**: Modern Vuex alternative with TypeScript support

### Svelte-Specific Principles

1. **Runes for Reactivity**: Use $state, $derived, $effect (Svelte 5+)
2. **SvelteKit for Apps**: Leverage file-based routing and server functions
3. **Minimal Stores**: Runes reduce need for stores in components
4. **Progressive Enhancement**: Build for no-JS, enhance with JS

### Angular-Specific Principles

1. **Standalone Components**: Default since v17 (avoid NgModules)
2. **Signals for State**: Prefer over RxJS for simple reactivity
3. **OnPush Detection**: Optimize change detection
4. **Dependency Injection**: Use inject() for modern DI

---

## Quick Reference: File Structure

```
src/
  features/
    my-feature/
      api/
        myFeatureApi.ts       # API service
      components/
        MyFeature.tsx         # Main component
        SubComponent.tsx      # Related components
      hooks/
        useMyFeature.ts       # Custom hooks
        useSuspenseMyFeature.ts  # Suspense hooks
      helpers/
        myFeatureHelpers.ts   # Utilities
      types/
        index.ts              # TypeScript types
      index.ts                # Public exports

  components/
    SuspenseLoader/
      SuspenseLoader.tsx      # Reusable loader
    CustomAppBar/
      CustomAppBar.tsx        # Reusable app bar

  routes/
    my-route/
      index.tsx               # Route component
      create/
        index.tsx             # Nested route
```

---

## Modern Component Template (Quick Copy)

```typescript
import React, { useState, useCallback } from 'react';
import { Box, Paper } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '~types/feature';

interface MyComponentProps {
    id: number;
    onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
    const [state, setState] = useState<string>('');

    const { data } = useSuspenseQuery({
        queryKey: ['feature', id],
        queryFn: () => featureApi.getFeature(id),
    });

    const handleAction = useCallback(() => {
        setState('updated');
        onAction?.();
    }, [onAction]);

    return (
        <Box sx={{ p: 2 }}>
            <Paper sx={{ p: 3 }}>
                {/* Content */}
            </Paper>
        </Box>
    );
};

export default MyComponent;
```

For complete examples, see [resources/complete-examples.md](resources/complete-examples.md)

---

## Vue 3 Development

### Component Patterns

**Composition API** - Modern Vue 3 approach with `<script setup>`:

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types/user'

interface Props {
  userId: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  update: [user: User]
}>()

const user = ref<User | null>(null)
const isLoading = ref(true)
const displayName = computed(() => user.value?.name ?? 'Unknown')

onMounted(async () => {
  user.value = await fetchUser(props.userId)
  isLoading.value = false
})

function handleUpdate() {
  if (user.value) emit('update', user.value)
}
</script>

<template>
  <div class="user-profile">
    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <h2>{{ displayName }}</h2>
      <button @click="handleUpdate">Update</button>
    </div>
  </div>
</template>

<style scoped>
.user-profile {
  padding: 1rem;
}
</style>
```

**Key Patterns:**
- `<script setup>` - Concise composition API syntax
- `defineProps<T>()` - Type-safe props with generics
- `defineEmits<T>()` - Type-safe events
- `ref()`, `reactive()` - Reactivity primitives
- `computed()` - Derived state
- `watch()`, `watchEffect()` - Side effects
- `onMounted`, `onUnmounted` - Lifecycle hooks

### State Management (Pinia)

```typescript
// stores/userStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const users = ref<User[]>([])
  const currentUser = ref<User | null>(null)

  // Getters
  const userCount = computed(() => users.value.length)
  const isAuthenticated = computed(() => currentUser.value !== null)

  // Actions
  async function fetchUsers() {
    users.value = await api.getUsers()
  }

  function setCurrentUser(user: User) {
    currentUser.value = user
  }

  return { users, currentUser, userCount, isAuthenticated, fetchUsers, setCurrentUser }
})

// Component usage
<script setup lang="ts">
import { useUserStore } from '@/stores/userStore'
const userStore = useUserStore()
</script>
```

### Routing (Vue Router)

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/users/:id',
      component: () => import('@/views/UserView.vue'),
      props: true
    }
  ]
})

// Component with route params
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const userId = route.params.id

function goBack() {
  router.push('/')
}
</script>
```

### Data Fetching Patterns

**Composables** - Reusable logic:

```typescript
// composables/useUser.ts
import { ref, type Ref } from 'vue'

export function useUser(id: Ref<number>) {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<Error | null>(null)

  async function fetchUser() {
    loading.value = true
    try {
      user.value = await api.getUser(id.value)
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  watchEffect(() => {
    fetchUser()
  })

  return { user, loading, error, refetch: fetchUser }
}

// Usage in component
<script setup lang="ts">
const props = defineProps<{ userId: number }>()
const { user, loading, error } = useUser(toRef(props, 'userId'))
</script>
```

**Nuxt.js Server-Side:**

```vue
<script setup lang="ts">
// Nuxt auto-imports composables
const { data: user, pending, error } = await useFetch(`/api/users/${route.params.id}`)
</script>
```

### Vue 3 Best Practices

- **Composition API over Options API** - Better TypeScript support, reusability
- **Script setup** - Reduces boilerplate, automatic registration
- **Pinia over Vuex** - Simpler API, better TypeScript, composition API compatible
- **Composables** - Extract reusable logic (like React hooks)
- **v-memo** - Optimize expensive renders (similar to React.memo)
- **defineOptions** - Set component options in script setup
- **Shallow reactive** - Use `shallowRef()` for large objects

---

## Svelte 5 Development

### Runes-Based Reactivity

**Svelte 5 Runes** - New reactivity system:

```svelte
<script lang="ts">
import type { User } from '$lib/types/user'

interface Props {
  userId: number
  onUpdate?: (user: User) => void
}

let { userId, onUpdate }: Props = $props()

// Reactive state with $state
let user = $state<User | null>(null)
let isLoading = $state(true)

// Derived state with $derived
let displayName = $derived(user?.name ?? 'Unknown')
let userAge = $derived.by(() => {
  if (!user?.birthDate) return null
  return calculateAge(user.birthDate)
})

// Effects with $effect
$effect(() => {
  // Runs when userId changes
  loadUser(userId)
})

async function loadUser(id: number) {
  isLoading = true
  user = await fetchUser(id)
  isLoading = false
}

function handleUpdate() {
  if (user) onUpdate?.(user)
}
</script>

{#if isLoading}
  <div>Loading...</div>
{:else if user}
  <div class="user-profile">
    <h2>{displayName}</h2>
    {#if userAge}
      <p>Age: {userAge}</p>
    {/if}
    <button onclick={handleUpdate}>Update</button>
  </div>
{/if}

<style>
.user-profile {
  padding: 1rem;
}
</style>
```

**Svelte 5 Runes:**
- `$state()` - Reactive state (replaces `let` for reactivity)
- `$derived` - Computed values (replaces `$:`)
- `$derived.by()` - Complex derived state
- `$effect()` - Side effects (replaces `$:` statements)
- `$props()` - Component props with destructuring
- `$bindable()` - Two-way binding for props
- `$inspect()` - Debugging reactive values

### State Management (Svelte Stores)

```typescript
// stores/user.ts
import { writable, derived, readonly } from 'svelte/store'

function createUserStore() {
  const { subscribe, set, update } = writable<User[]>([])

  return {
    subscribe,
    setUsers: (users: User[]) => set(users),
    addUser: (user: User) => update(users => [...users, user]),
    removeUser: (id: number) => update(users => users.filter(u => u.id !== id)),
    reset: () => set([])
  }
}

export const users = createUserStore()
export const userCount = derived(users, $users => $users.length)

// Component usage (Svelte 4 style)
<script>
import { users } from '$lib/stores/user'
</script>

<p>Total users: {$users.length}</p>

// Or with runes (Svelte 5)
<script>
import { users } from '$lib/stores/user'
let currentUsers = $state($users)
</script>
```

### SvelteKit Routing & Data Loading

```typescript
// src/routes/users/[id]/+page.ts
import type { PageLoad } from './$types'

export const load: PageLoad = async ({ params, fetch }) => {
  const user = await fetch(`/api/users/${params.id}`).then(r => r.json())

  return {
    user
  }
}

// src/routes/users/[id]/+page.svelte
<script lang="ts">
import type { PageData } from './$types'

let { data }: { data: PageData } = $props()
let { user } = $derived(data)
</script>

<h1>{user.name}</h1>
```

**SvelteKit Patterns:**
- `+page.svelte` - Page component
- `+page.ts` - Page data loading (runs on server and client)
- `+page.server.ts` - Server-only load functions
- `+layout.svelte` - Shared layouts
- `+server.ts` - API endpoints
- Form actions - Progressive enhancement

### Svelte 5 Best Practices

- **Use Runes** - Modern reactivity (Svelte 5+)
- **Explicit reactivity** - Use `$state()` instead of implicit `let`
- **$derived over $:** - Clearer intent, better optimization
- **Component composition** - Use slots and snippets
- **SvelteKit for apps** - Full-stack framework with routing, SSR
- **Minimize stores** - Runes reduce need for stores in components
- **Progressive enhancement** - Use form actions for better UX

---

## Angular Development

### Standalone Components (Modern)

```typescript
// user-profile.component.ts
import { Component, Input, Output, EventEmitter, signal, computed } from '@angular/core'
import { CommonModule } from '@angular/common'
import type { User } from '@/types/user'

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="user-profile" *ngIf="!isLoading(); else loading">
      <h2>{{ displayName() }}</h2>
      <p>Age: {{ userAge() }}</p>
      <button (click)="handleUpdate()">Update</button>
    </div>
    <ng-template #loading>
      <div>Loading...</div>
    </ng-template>
  `,
  styles: [`
    .user-profile {
      padding: 1rem;
    }
  `]
})
export class UserProfileComponent {
  @Input({ required: true }) userId!: number
  @Output() userUpdate = new EventEmitter<User>()

  // Signals - reactive primitives
  user = signal<User | null>(null)
  isLoading = signal(true)

  // Computed signals
  displayName = computed(() => this.user()?.name ?? 'Unknown')
  userAge = computed(() => {
    const birthDate = this.user()?.birthDate
    return birthDate ? this.calculateAge(birthDate) : null
  })

  async ngOnInit() {
    this.user.set(await this.fetchUser(this.userId))
    this.isLoading.set(false)
  }

  handleUpdate() {
    const currentUser = this.user()
    if (currentUser) this.userUpdate.emit(currentUser)
  }
}
```

**Angular Signals** - New reactivity system (v16+):
- `signal()` - Writable reactive value
- `computed()` - Derived state
- `effect()` - Side effects
- `.set()`, `.update()` - Modify signal values
- `()` - Read signal value (call as function)

### State Management (Services + Signals)

```typescript
// services/user.service.ts
import { Injectable, signal, computed } from '@angular/core'
import { HttpClient } from '@angular/common/http'

@Injectable({ providedIn: 'root' })
export class UserService {
  private users = signal<User[]>([])
  private currentUser = signal<User | null>(null)

  // Public computed signals
  readonly userCount = computed(() => this.users().length)
  readonly isAuthenticated = computed(() => this.currentUser() !== null)

  constructor(private http: HttpClient) {}

  async fetchUsers() {
    const users = await this.http.get<User[]>('/api/users').toPromise()
    this.users.set(users)
  }

  setCurrentUser(user: User) {
    this.currentUser.set(user)
  }
}

// Component usage
export class MyComponent {
  constructor(public userService: UserService) {}

  // Access in template
  // {{ userService.userCount() }}
}
```

### Routing (Angular Router)

```typescript
// app.routes.ts
import { Routes } from '@angular/router'

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'users/:id',
    loadComponent: () => import('./users/user-detail.component').then(m => m.UserDetailComponent)
  }
]

// Component with route params
import { Component } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'

export class UserDetailComponent {
  userId = signal<string>('')

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {
    this.userId.set(this.route.snapshot.paramMap.get('id') ?? '')
  }

  goBack() {
    this.router.navigate(['/'])
  }
}
```

### Data Fetching (RxJS + Signals)

```typescript
import { Component, signal } from '@angular/core'
import { HttpClient } from '@angular/common/http'
import { toSignal } from '@angular/core/rxjs-interop'

export class UserListComponent {
  private http = inject(HttpClient)

  // Convert Observable to Signal
  users = toSignal(this.http.get<User[]>('/api/users'), { initialValue: [] })

  // Or manual signal management
  manualUsers = signal<User[]>([])

  async loadUsers() {
    const users = await this.http.get<User[]>('/api/users').toPromise()
    this.manualUsers.set(users)
  }
}
```

### Angular Best Practices

- **Standalone components** - Default since v17 (no NgModules)
- **Signals over RxJS** - Simpler reactivity for state
- **toSignal** - Convert Observables to Signals when needed
- **inject()** - Modern dependency injection (no constructor)
- **Lazy loading** - Use `loadComponent` for routes
- **OnPush change detection** - Optimize rendering
- **Typed forms** - Use `FormGroup<T>` for type safety

---

## Framework-Agnostic Patterns

### State Management Comparison

| Pattern | React | Vue 3 | Svelte 5 | Angular |
|---------|-------|-------|----------|---------|
| **Local State** | `useState` | `ref()` | `$state()` | `signal()` |
| **Derived State** | `useMemo` | `computed()` | `$derived` | `computed()` |
| **Side Effects** | `useEffect` | `watch/watchEffect` | `$effect()` | `effect()` |
| **Global State** | Zustand/Context | Pinia | Stores | Services |
| **Async State** | TanStack Query | VueQuery/Composables | Stores | RxJS/Signals |

### Component Composition Patterns

**Props/Events Pattern** (All frameworks):
- Parent passes data down via props
- Child emits events upward
- Unidirectional data flow

**Slots/Children Pattern:**

```typescript
// React
<Layout>
  <Header />
  <Content />
</Layout>

// Vue
<Layout>
  <template #header><Header /></template>
  <template #content><Content /></template>
</Layout>

// Svelte
<Layout>
  <Header slot="header" />
  <Content slot="content" />
</Layout>

// Angular
<app-layout>
  <app-header header></app-header>
  <app-content content></app-content>
</app-layout>
```

### Routing Patterns

**File-Based Routing:**
- Next.js (React), Nuxt (Vue), SvelteKit (Svelte)
- Folder structure defines routes
- `[id]` for dynamic segments

**Programmatic Routing:**
- React Router, Vue Router, Angular Router
- Define routes in config
- More flexible but more verbose

### Performance Optimization

**Universal Techniques:**
1. **Code splitting** - Lazy load routes and heavy components
2. **Memoization** - Cache expensive computations
3. **Virtual scrolling** - Render only visible items
4. **Debouncing** - Throttle expensive operations (search, resize)
5. **Image optimization** - Lazy load, responsive images, modern formats
6. **Bundle analysis** - Identify and remove large dependencies

**Framework-Specific:**
- **React:** `React.memo`, `useMemo`, `useCallback`, Suspense
- **Vue:** `v-memo`, `shallowRef`, `markRaw`, KeepAlive
- **Svelte:** Automatic optimization, `$derived`, minimal runtime
- **Angular:** OnPush, signals, trackBy, pure pipes

---

## Related Skills

**IMPORTANT: For UI/UX design work, invoke the specialized skill:**
```
Skill("ui-ux-pro-max")  → UI/UX design, visual hierarchy, color theory, spacing, typography
```

**UI/Design:**
- **ui-ux-pro-max**: UI/UX design principles, visual hierarchy, color theory, spacing systems, typography. **USE THIS** for design decisions, beautifying UIs, choosing colors/fonts, layout design.
- **ui-design-system**: Component design systems, accessibility, design tokens
- **ui-styling**: Tailwind CSS, styling patterns for all frameworks

**Backend Integration:**
- **backend-development**: API patterns that frontend consumes
- **better-auth**: Authentication implementation (works with all frameworks)

**Full-Stack Frameworks:**
- **web-frameworks**: Next.js (React), Nuxt (Vue), SvelteKit (Svelte) deep dive

**Development:**
- **debugging**: Framework-agnostic debugging strategies
- **refactoring-expert**: Code quality and refactoring patterns
- **chrome-devtools**: Browser debugging, performance profiling

## When to Invoke ui-ux-pro-max

Call `Skill("ui-ux-pro-max")` when:
- Designing new UI components or pages
- Choosing color palettes, typography, or spacing
- Improving visual hierarchy or layout
- Making interfaces look professional/modern/clean
- User mentions: ugly, inconsistent, cluttered, needs design help
- Building dashboards, admin panels, or SaaS interfaces

---

**Skill Status**: Multi-framework coverage with progressive disclosure