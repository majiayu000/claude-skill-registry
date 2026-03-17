---
name: web-state-pinia
description: Pinia stores, Vue 3 state patterns. Use when managing client state in Vue applications, choosing between Options/Setup stores, composing stores, or implementing persistence.
---

# Pinia State Management Patterns

> **Quick Guide:** Use Pinia for all shared client state in Vue 3. Options stores for simplicity, Setup stores for flexibility. Server data? Use your data fetching solution. Use `storeToRefs()` when destructuring state.

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Managing State with Pinia

**(You MUST use a data fetching solution for ALL server/API data - NEVER put API responses in Pinia stores)**

**(You MUST use `storeToRefs()` when destructuring state from stores - direct destructuring loses reactivity)**

**(You MUST return ALL state properties in Setup stores - private state breaks SSR and DevTools)**

**(You MUST use named exports ONLY - NO default exports in any store files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

</critical_requirements>

---

**Auto-detection:** Pinia, defineStore, Vue 3 state, storeToRefs, Vue state management, Options store, Setup store

**When to use:**

- Managing shared client state in Vue 3 applications
- Choosing between Options stores and Setup stores
- Composing stores that depend on each other
- Implementing state persistence across sessions
- Adding DevTools integration for debugging
- Setting up stores for SSR/Nuxt applications

**When NOT to use:**

- Server/API data (use a dedicated data fetching solution)
- Simple component-local state (use `ref()` or `reactive()`)
- URL-appropriate state like filters (use route query params)

---

<philosophy>

## Philosophy

Pinia is the official state management solution for Vue 3, designed to be intuitive, type-safe, and flexible. It eliminates the boilerplate of Vuex while maintaining powerful features like DevTools integration, plugin support, and SSR compatibility.

**Core Principles:**

1. **Modular by Default** - Each store is independent, no nested modules
2. **No Mutations** - Actions handle all state changes directly
3. **Full TypeScript Support** - Type inference works out of the box
4. **Composition API Friendly** - Works seamlessly with `<script setup>`

**State Ownership:**

| State Type            | Solution               | Reason                                   |
| --------------------- | ---------------------- | ---------------------------------------- |
| Server/API data       | Data fetching solution | Caching, synchronization, loading states |
| Shared client state   | Pinia                  | Reactivity, DevTools, persistence        |
| Component-local state | `ref()` / `reactive()` | Simpler, no overhead                     |
| URL state (filters)   | Route query params     | Shareable, bookmarkable                  |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Options Store vs Setup Store Decision

Pinia offers two store definition syntaxes. Choose based on your needs.

#### Decision Tree

```
Which store syntax should I use?

Need composables (useRoute, useI18n)?
├─ YES → Setup Store
└─ NO → Need watchers inside store?
    ├─ YES → Setup Store
    └─ NO → Prefer Vue Options API style?
        ├─ YES → Options Store
        └─ NO → Setup Store (more flexible)
```

**Options Store**: Simpler, familiar to Vuex users, built-in `$reset()` method
**Setup Store**: More flexible, supports composables, requires manual reset

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 2: Options Store Definition

Use Options stores for straightforward state management with familiar syntax.

#### When to Use

- Teams familiar with Vuex or Vue Options API
- Simple stores without composable dependencies
- When built-in `$reset()` method is needed
- Standard CRUD operations on client state

For implementation examples and good/bad comparisons, see [examples/core.md](examples/core.md).

---

### Pattern 3: Setup Store Definition

Use Setup stores when you need maximum flexibility and composable integration.

#### When to Use

- Using Vue Router composables (`useRoute`, `useRouter`)
- Using i18n composables (`useI18n`)
- Need watchers inside the store
- Complex computed dependencies
- Integrating with external composables

#### Critical Requirements for Setup Stores

- Return ALL state properties (no private state)
- Use `ref()` for state, `computed()` for getters
- Functions become actions automatically
- Must implement custom `$reset()` if needed

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 4: Accessing Store State in Components

Proper store access patterns prevent reactivity issues.

#### Key Rules

1. **Never destructure state directly** - loses reactivity
2. **Use `storeToRefs()` for state/getters** - preserves reactivity
3. **Destructure actions directly** - they don't need reactivity

For implementation examples with storeToRefs, see [examples/core.md](examples/core.md).

---

### Pattern 5: Composing Stores

Stores can use other stores, but follow rules to avoid circular dependencies.

#### Guidelines

- Import and use stores at the top of your store function
- Avoid circular dependencies through getters/actions
- If stores reference each other, ensure no infinite loops
- Use setup stores for complex composition patterns

For implementation examples, see [examples/core.md](examples/core.md).

---

### Pattern 6: State Persistence

Use plugins for persisting state across sessions.

#### Persistence Guidelines

- Use `pinia-plugin-persistedstate` for most cases
- Only persist user preferences and non-sensitive data
- Use `paths` option to persist specific properties only
- Never persist server data (refetch on load instead)
- Consider storage type: localStorage vs sessionStorage

For implementation examples, see [examples/persistence.md](examples/persistence.md).

---

### Pattern 7: Pinia Plugins

Extend all stores with shared functionality.

#### Common Plugin Use Cases

- Adding shared properties (router, analytics)
- Wrapping actions with logging/timing
- Adding custom options (debounce, throttle)
- Implementing side effects (localStorage)

For implementation examples, see [examples/plugins.md](examples/plugins.md).

---

### Pattern 8: Testing Stores

Test stores in isolation and within components.

#### Testing Approaches

1. **Unit tests**: Test store actions/getters directly with `setActivePinia()`
2. **Component tests**: Use `createTestingPinia()` for component mounting
3. **Mocking**: Actions are stubbed by default with `@pinia/testing`

For implementation examples, see [examples/testing.md](examples/testing.md).

---

### Pattern 9: SSR Considerations

Handle server-side rendering and hydration properly.

#### SSR Guidelines

- Use SSR-safe defaults (no browser APIs in initial state)
- Wrap client-only logic in `if (import.meta.client)` blocks
- Be careful with Setup stores - ensure all refs are returned
- Sanitize serialized state to prevent XSS

For implementation examples, see [examples/ssr.md](examples/ssr.md).

</patterns>

---

<integration>

## Integration Guide

**Vue Router Integration:**

Use Setup stores to access router composables:

```typescript
import { useRoute, useRouter } from "vue-router";

export const useFiltersStore = defineStore("filters", () => {
  const route = useRoute();
  const router = useRouter();
  // Access route.query, call router.push(), etc.
});
```

**DevTools:**

Pinia has full Vue DevTools support:

- Time-travel debugging
- State inspection and editing
- Action tracking
- Store timeline

**Nuxt Integration:**

Use `@pinia/nuxt` module for automatic SSR support and auto-imports.

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use a data fetching solution for ALL server/API data - NEVER put API responses in Pinia stores)**

**(You MUST use `storeToRefs()` when destructuring state from stores - direct destructuring loses reactivity)**

**(You MUST return ALL state properties in Setup stores - private state breaks SSR and DevTools)**

**(You MUST use named exports ONLY - NO default exports in any store files)**

**(You MUST use named constants for ALL numbers - NO magic numbers in state code)**

**Failure to follow these rules will cause reactivity bugs, SSR hydration errors, and DevTools failures.**

</critical_reminders>
