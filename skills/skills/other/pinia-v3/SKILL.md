---
name: pinia-v3
description: Pinia v3 Vue state management with defineStore, getters, actions. Use for Vue 3 stores, Nuxt SSR, Vuex migration, or encountering store composition, hydration, testing errors.

  Keywords: pinia, vue state management, pinia stores, defineStore, vue 3 state, state management, getters, actions, pinia plugins, pinia ssr, nuxt pinia, vuex migration, store composition, pinia testing, setup stores, option stores, storeToRefs, mapState, mapActions, state hydration, pinia nuxt module, createPinia, useStore, pinia devtools, pinia hmr, hot module replacement
license: MIT
---

# Pinia v3 - Vue State Management

**Status**: Production Ready ✅
**Last Updated**: 2025-11-11
**Dependencies**: Vue 3 (or Vue 2.7 with @vue/composition-api)
**Latest Versions**: pinia@^3.0.4, @pinia/nuxt@^0.11.2, @pinia/testing@^1.0.2

---

## Quick Start (5 Minutes)

### 1. Install Pinia

```bash
bun add pinia
# or
bun add pinia
# or
bun add pinia
```

**For Vue <2.7 users**: Also install `@vue/composition-api` with `bun add @vue/composition-api`

**Why this matters:**
- Pinia is the official Vue state management library
- Provides better TypeScript support than Vuex
- Eliminates mutations and namespacing complexity
- Full DevTools support with time-travel debugging

### 2. Create and Register Pinia Instance

```typescript
// main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)
app.mount('#app')
```

**CRITICAL:**
- Install Pinia BEFORE using any store
- Call `app.use(pinia)` before mounting the app
- Only one Pinia instance per application (unless SSR)

### 3. Define Your First Store

```typescript
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
    name: 'Eduardo'
  }),
  getters: {
    doubleCount: (state) => state.count * 2
  },
  actions: {
    increment() {
      this.count++
    }
  }
})
```

### 4. Use Store in Components

```vue
<script setup>
import { useCounterStore } from '@/stores/counter'

const counter = useCounterStore()
</script>

<template>
  <div>
    <p>Count: {{ counter.count }}</p>
    <p>Double: {{ counter.doubleCount }}</p>
    <button @click="counter.increment">Increment</button>
  </div>
</template>
```

---

## The Two Store Syntaxes

**Load `references/store-syntax-guide.md` for complete comparison of Option vs Setup stores.**

### Quick Overview

Pinia supports two store definition syntaxes:

**Option Stores:**
- Similar to Vue Options API
- Built-in `$reset()` method
- Best for: Simpler use cases, teams familiar with Vuex

**Setup Stores:**
- Uses Composition API pattern
- Full composables integration
- Best for: Advanced patterns, need watchers/VueUse integration

**→ Load `references/store-syntax-guide.md` for:** Complete syntax comparison, examples, choosing criteria

---

## State, Getters, and Actions

**Load `references/state-getters-actions.md` for complete API reference.**

### Quick Reference

**State:**
- Define in `state: () => ({...})` (option) or `ref()` (setup)
- Access directly: `store.count`
- Mutate directly: `store.count++` or `store.$patch({...})`
- Reset: `store.$reset()` (option stores only)

**Getters:**
- Computed properties: `getters: { double: (state) => state.count * 2 }`
- Access other getters with `this` (must type return value)

**Actions:**
- Business logic: `actions: { increment() { this.count++ } }`
- Can be async
- Access other stores directly

**Store Destructuring:**
```typescript
import { storeToRefs } from 'pinia'

// ✅ For reactivity
const { name, count } = storeToRefs(store)

// ✅ Actions can destructure directly
const { increment } = store
```

**→ Load `references/state-getters-actions.md` for:** Complete API, subscriptions, store composition patterns, Options API usage

---

## Plugins and Composables

**Load `references/plugins-composables.md` for complete plugin and composables guide.**

### Plugin Basics

```typescript
pinia.use(({ store, options }) => {
  // Add properties to every store
  return { customProperty: 'value' }
})
```

### Composables Integration

**Option Stores:** Limited to `useLocalStorage` style in `state()`
**Setup Stores:** Full VueUse/composables support

**→ Load `references/plugins-composables.md` for:** Complete plugin patterns, VueUse integration, TypeScript typing, common patterns (persistence, router, logger)

---

## Using Stores Outside Components

### The Problem

Stores need the Pinia instance, which is auto-injected in components but not available in module scope.

### ❌ Wrong: Accessing Store at Module Level

```typescript
// router.ts
import { useUserStore } from '@/stores/user'

// ❌ Fails: Pinia not installed yet
const userStore = useUserStore()

router.beforeEach((to) => {
  if (userStore.isLoggedIn) { /* ... */ }
})
```

### ✅ Right: Accessing Store Inside Callbacks

```typescript
// router.ts
import { useUserStore } from '@/stores/user'

router.beforeEach((to) => {
  // ✅ Works: Called after Pinia is installed
  const userStore = useUserStore()

  if (userStore.isLoggedIn) { /* ... */ }
})
```

**Why it works**: Router guards execute AFTER `app.use(pinia)` completes.

### SSR: Explicit Pinia Instance

```typescript
// server-side
export function setupRouter(pinia) {
  router.beforeEach((to) => {
    const userStore = useUserStore(pinia) // Pass explicitly
  })
}
```

---

## Server-Side Rendering & Nuxt

**Load `references/ssr-and-nuxt.md` for complete SSR and Nuxt integration guide.**

### SSR Quick Reference

**State Hydration:**
- Server: Serialize with `devalue()` (not `JSON.stringify`)
- Client: Hydrate BEFORE calling `useStore()`
- Critical: Call all `useStore()` BEFORE `await` in actions

### Nuxt 3/4 Integration

```bash
bunx nuxi@latest module add pinia
```

**Auto-imports:** `defineStore`, `storeToRefs`, `usePinia`, `acceptHMRUpdate`, all stores

**→ Load `references/ssr-and-nuxt.md` for:** Complete SSR patterns, Nuxt configuration, server-side data fetching, SSR pitfalls, debugging

---

## Testing

**Load `references/testing-guide.md` for complete testing guide.**

### Testing Quick Start

```typescript
import { setActivePinia, createPinia } from 'pinia'

beforeEach(() => {
  setActivePinia(createPinia()) // Fresh Pinia for each test
})
```

### Component Testing

```bash
bun add -d @pinia/testing
```

```typescript
import { createTestingPinia } from '@pinia/testing'

mount(Component, {
  global: { plugins: [createTestingPinia()] }
})
```

**→ Load `references/testing-guide.md` for:** Complete test patterns, stubbing actions, mocking getters, async testing, SSR testing

---

## Hot Module Replacement (HMR)

### Vite Setup

```typescript
// stores/counter.ts
import { defineStore, acceptHMRUpdate } from 'pinia'

export const useCounterStore = defineStore('counter', {
  // store definition
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useCounterStore, import.meta.hot))
}
```

### Webpack Setup

```typescript
if (import.meta.webpackHot) {
  import.meta.webpackHot.accept(acceptHMRUpdate(useCounterStore, import.meta.webpackHot))
}
```

**Benefits:**
- Edit stores without full page reload
- Preserve application state during development
- Faster development iteration

---

## Options API Usage

For projects still using Options API, load complete mapper documentation.

**→ Load `references/state-getters-actions.md` for:** Complete Options API integration, all mappers (`mapStores`, `mapState`, `mapWritableState`, `mapActions`)

---

## Migrating from Vuex

**Load `references/vuex-migration.md` for complete migration guide.**

### Quick Conversion Overview

**Key Changes:**
1. Remove `namespaced` (automatic via store ID)
2. Eliminate `mutations` (direct state mutation)
3. Replace `commit()` with direct mutations
4. Replace `rootState`/`rootGetters` with store imports
5. Use `store.$reset()` instead of custom clear mutations

**Directory:** `store/modules/` → `stores/` (each module = separate store)

**→ Load `references/vuex-migration.md` for:** Complete conversion steps, component migration, checklist, gradual migration strategy

---

## Critical Rules

### Always Do

✅ Define all state properties in `state()` or return them from setup stores
✅ Use `storeToRefs()` when destructuring state/getters in components
✅ Call `app.use(pinia)` BEFORE mounting the app
✅ Return all state from setup stores (private state breaks SSR/DevTools)
✅ Call `useStore()` inside functions/callbacks when used outside components
✅ Use `acceptHMRUpdate()` for development HMR support
✅ Type return values when getters use `this` to access other getters
✅ Use `devalue` for SSR state serialization (prevents XSS)
✅ Hydrate state BEFORE calling any `useStore()` on the client (SSR)
✅ Call all `useStore()` BEFORE any `await` in async actions (SSR)

### Never Do

❌ Add state properties dynamically after store creation
❌ Destructure store directly without `storeToRefs()` (loses reactivity)
❌ Use arrow functions for actions (need `this` context)
❌ Return private state in setup stores (breaks SSR/DevTools/plugins)
❌ Call `useStore()` at module top-level (before Pinia installed)
❌ Create circular dependencies between stores (both reading each other's state)
❌ Use `JSON.stringify()` for SSR serialization (vulnerable to XSS)
❌ Call `useStore()` after `await` in actions (breaks SSR)
❌ Forget to type getter return values when using `this`
❌ Skip `beforeEach(() => setActivePinia(createPinia()))` in unit tests

---

## Known Issues Prevention

This skill prevents **12** documented issues:

### Issue #1: Lost Reactivity from Direct Destructuring
**Error**: State changes don't update in template after destructuring
**Why It Happens**: JavaScript destructuring breaks Vue reactivity
**Prevention**: Always use `storeToRefs()` for state/getters

### Issue #2: Cannot Add State Properties Dynamically
**Error**: New properties added after store creation aren't reactive
**Why It Happens**: Pinia needs all properties defined upfront for reactivity
**Prevention**: Declare all properties in `state()`, even if initially `undefined`

### Issue #3: Store Not Found Before Pinia Install
**Error**: `getActivePinia()` returns undefined
**Why It Happens**: Calling `useStore()` before `app.use(pinia)`
**Prevention**: Call `app.use(pinia)` before mounting or accessing stores

### Issue #4: Setup Store Private State Breaks SSR
**Error**: State not serialized/hydrated correctly in SSR
**Why It Happens**: Properties not returned from setup aren't tracked
**Prevention**: Return ALL state properties from setup stores

### Issue #5: Getters with `this` Don't Infer Types
**Error**: TypeScript can't infer return type when getter uses `this`
**Source**: Known TypeScript limitation with Pinia
**Prevention**: Explicitly type return value: `getterName(): ReturnType { ... }`

### Issue #6: Options API Store Suffix Confusion
**Error**: Can't find `this.counterStore` in component
**Why It Happens**: `mapStores()` automatically adds 'Store' suffix
**Prevention**: Use store name + 'Store' or call `setMapStoreSuffix()`

### Issue #7: Actions Called After `await` Break SSR
**Error**: Wrong Pinia instance used in SSR, causing state pollution
**Why It Happens**: `await` changes execution context in async functions
**Prevention**: Call all `useStore()` before any `await` statements

### Issue #8: Circular Store Dependencies Crash App
**Error**: Maximum call stack exceeded
**Why It Happens**: Both stores read each other's state during initialization
**Prevention**: Use getters/actions for cross-store access, not setup-time reads

### Issue #9: XSS Vulnerability in SSR State Serialization
**Error**: User input in state can execute malicious scripts
**Why It Happens**: `JSON.stringify()` doesn't escape executable code
**Prevention**: Use `devalue` library for safe serialization

### Issue #10: HMR Doesn't Work in Development
**Error**: Changes to store require full page reload
**Why It Happens**: Vite/webpack HMR not configured for store
**Prevention**: Add `acceptHMRUpdate()` block to each store file

### Issue #11: Composables Return Functions Break Option Stores
**Error**: Store state contains non-serializable functions
**Why It Happens**: Option stores `state()` can only return writable refs
**Prevention**: Use setup stores for complex composables, or extract only writable state

### Issue #12: State Not Reset Between Unit Tests
**Error**: Tests affect each other, sporadic failures
**Why It Happens**: Single Pinia instance shared across tests
**Prevention**: `beforeEach(() => setActivePinia(createPinia()))` in test suites

---

## Package Versions (Verified 2025-11-21)

**Core:** `pinia@^3.0.4`, `vue@^3.5.24`
**Nuxt:** `@pinia/nuxt@^0.11.2`, `nuxt@^3.13.0`
**Testing:** `@pinia/testing@^1.0.2`, `vitest@^1.0.0`
**SSR:** `devalue@^5.3.2` (for safe serialization)

---

## Common Patterns

See reference files for complete pattern examples:
- **Authentication stores** → `references/state-getters-actions.md`
- **Persistence plugins** → `references/plugins-composables.md`
- **Form stores** → `references/store-syntax-guide.md` (setup store examples)
- **Router integration** → `references/state-getters-actions.md` (accessing stores outside components)

---

## Official Documentation

- **Pinia**: https://pinia.vuejs.org/
- **Getting Started**: https://pinia.vuejs.org/getting-started.html
- **Core Concepts**: https://pinia.vuejs.org/core-concepts/
- **SSR Guide**: https://pinia.vuejs.org/ssr/
- **Nuxt Integration**: https://pinia.vuejs.org/ssr/nuxt.html
- **Testing**: https://pinia.vuejs.org/cookbook/testing.html
- **Vuex Migration**: https://pinia.vuejs.org/cookbook/migration-vuex.html
- **GitHub**: https://github.com/vuejs/pinia

---

## Troubleshooting

### Problem: "getActivePinia() was called with no active Pinia"
**Solution**:
1. Ensure `app.use(pinia)` is called before mounting
2. If outside component, call `useStore()` inside callback/function
3. For SSR, pass pinia instance explicitly: `useStore(pinia)`

### Problem: State changes don't update in template
**Solution**: Use `storeToRefs()` instead of direct destructuring

### Problem: Getter using `this` has TypeScript errors
**Solution**: Explicitly type the return value: `myGetter(): ReturnType { return this.otherGetter }`

### Problem: $reset() not available in setup store
**Solution**: Implement custom reset manually:
```typescript
function $reset() {
  count.value = 0
  name.value = ''
}
return { count, name, $reset }
```

### Problem: HMR not working for stores
**Solution**: Add HMR acceptance block:
```typescript
if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useMyStore, import.meta.hot))
}
```

### Problem: Tests fail intermittently
**Solution**: Create fresh Pinia in `beforeEach()`:
```typescript
beforeEach(() => {
  setActivePinia(createPinia())
})
```

---

## When to Load References

**Load `references/store-syntax-guide.md` when:**
- Need detailed comparison between Option and Setup store syntaxes
- Deciding which syntax to use for a new store
- Questions about Option vs Setup stores trade-offs
- Need complete examples of both syntaxes

**Load `references/state-getters-actions.md` when:**
- Need complete API reference for state, getters, or actions
- Questions about `$patch`, `$subscribe`, or `$onAction`
- Implementing store composition patterns
- Using Options API mappers (`mapStores`, `mapState`, `mapActions`)
- Accessing stores outside components (router, plugins)

**Load `references/plugins-composables.md` when:**
- Creating custom Pinia plugins
- Integrating VueUse or other composables into stores
- Need persistence, routing, or logging plugin patterns
- Questions about TypeScript typing for plugins
- Advanced composables integration

**Load `references/ssr-and-nuxt.md` when:**
- Setting up server-side rendering
- Integrating with Nuxt 3/4
- Questions about state hydration or serialization
- SSR-related errors (wrong Pinia instance, hydration mismatch)
- Nuxt auto-imports or configuration
- Server-side data fetching patterns

**Load `references/testing-guide.md` when:**
- Setting up unit tests for stores
- Testing components that use Pinia stores
- Need to stub actions or mock getters
- Questions about `createTestingPinia`
- Testing SSR stores
- Vitest or testing framework integration

**Load `references/vuex-migration.md` when:**
- Migrating existing Vuex codebase to Pinia
- Questions about Vuex→Pinia conversion
- Need migration checklist or examples
- Gradual migration strategy needed

---

## Complete Setup Checklist

- [ ] Installed `pinia` package
- [ ] Created Pinia instance with `createPinia()`
- [ ] Registered with `app.use(pinia)` before mounting
- [ ] Created stores directory (e.g., `src/stores/`)
- [ ] Defined at least one store with `defineStore()`
- [ ] Used `storeToRefs()` when destructuring in components
- [ ] Typed getter return values when using `this`
- [ ] Added HMR support with `acceptHMRUpdate()` (development)
- [ ] Configured SSR hydration (if using SSR)
- [ ] Configured `@pinia/nuxt` (if using Nuxt)
- [ ] Set up testing with `createTestingPinia()` (if testing)
- [ ] All stores follow consistent naming: `use[Name]Store`
- [ ] Verified DevTools integration works

---

**Questions? Issues?**

1. Check official docs: https://pinia.vuejs.org/
2. Review "Known Issues Prevention" section above
3. Verify setup checklist is complete
4. Check for TypeScript configuration issues
5. Ensure Pinia is installed before using stores
