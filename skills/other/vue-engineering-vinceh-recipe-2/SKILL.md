---
name: vue-engineering
description: Comprehensive guide for Vue 3 application development using modern best practices (2025). Covers Composition API, script setup syntax, reactivity system, composables, component patterns, TypeScript integration, performance optimization, and testing with Vitest. Use when building Vue 3 applications, creating components, writing composables, optimizing performance, or implementing Vue best practices.
---

# Vue 3 Engineering

## Overview

To build modern Vue 3 applications, follow industry best practices based on the Composition API, `<script setup>` syntax, and the 2025 ecosystem (Vite, Vitest, TypeScript). This skill provides comprehensive guidance for Vue 3 development, from component creation to production optimization.

**Current Vue Version:** Vue 3.5.18 (as of 2025)
**Build Tool:** Vite (Vue CLI is legacy)
**Testing:** Vitest (Jest is legacy for Vue)
**Standard:** Composition API with `<script setup>` (Options API is legacy)

## Decision Tree

```
User Request → What are you building/fixing?
    |
    ├─ Creating a new component?
    │   └─ Use Quick Start: Creating Components (below)
    │
    ├─ Need reusable logic?
    │   ├─ Load references/composables-patterns.md
    │   └─ Use asset: composable-template.ts
    │
    ├─ State management question (ref vs reactive)?
    │   └─ Load references/reactivity-guide.md
    │
    ├─ Component communication (props/emits/slots)?
    │   └─ Load references/component-patterns.md
    │
    ├─ Performance issue or optimization?
    │   └─ Load references/performance-optimization.md
    │
    ├─ TypeScript setup or typing question?
    │   └─ Load references/typescript-integration.md
    │
    ├─ Writing tests?
    │   └─ Load references/testing-guide.md
    │
    ├─ Reviewing code or debugging?
    │   └─ Load references/anti-patterns.md
    │
    └─ Learning Composition API basics?
        └─ Load references/composition-api-guide.md
```

## Quick Start: Creating Components

### Basic Component with `<script setup>`

```vue
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const double = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <div>
    <p>Count: {{ count }}</p>
    <p>Double: {{ double }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<style scoped>
/* Component styles */
</style>
```

### Component with Props and Emits (TypeScript)

```vue
<script setup lang="ts">
// Props
const props = defineProps<{
  title: string
  count?: number
}>()

// Emits
const emit = defineEmits<{
  update: [value: number]
  close: []
}>()

// Local state
const localCount = ref(props.count ?? 0)

// Methods
function handleUpdate() {
  emit('update', localCount.value)
}
</script>

<template>
  <div>
    <h2>{{ title }}</h2>
    <button @click="handleUpdate">Update</button>
  </div>
</template>
```

For a complete component template, use [component-template.vue](assets/component-template.vue).

## Quick Start: Creating Composables

Composables are reusable functions that encapsulate stateful logic.

### Basic Composable Pattern

```typescript
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  const double = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  return {
    count,
    double,
    increment,
    decrement
  }
}
```

**Usage in component:**
```vue
<script setup>
import { useCounter } from '@/composables/useCounter'

const { count, double, increment } = useCounter(5)
</script>
```

For a complete composable template, use [composable-template.ts](assets/composable-template.ts).

## Core Workflows

### Workflow 1: Building a Component

1. **Create file** with `.vue` extension
2. **Add `<script setup lang="ts">`** at top
3. **Define props** with `defineProps<T>()`
4. **Define emits** with `defineEmits<T>()`
5. **Add reactive state** with `ref()` or `reactive()`
6. **Create computed values** for derived state
7. **Add methods** as regular functions
8. **Use lifecycle hooks** (`onMounted`, `onUnmounted`, etc.)
9. **Build template** using component state
10. **Add scoped styles**

### Workflow 2: Creating a Composable

1. **Create file** in `composables/` directory with `use*.ts` naming
2. **Accept options** as parameter (single object preferred)
3. **Create reactive state** with `ref()` or `reactive()`
4. **Add computed values** for derived state
5. **Define methods** that manipulate state
6. **Handle cleanup** with `onUnmounted` if needed
7. **Return refs and methods** as object
8. **Document with JSDoc** and TypeScript types

### Workflow 3: Optimizing Performance

1. **Analyze bundle** with Vite plugins
2. **Implement lazy loading** for routes and components
3. **Use `v-show` vs `v-if`** appropriately
4. **Add keys to `v-for`** lists
5. **Use computed** instead of methods for derived data
6. **Implement virtual scrolling** for large lists
7. **Code split** vendor dependencies
8. **Monitor with Lighthouse** and Vue DevTools

### Workflow 4: Testing a Component

1. **Setup Vitest** in project
2. **Create `*.spec.ts`** file next to component
3. **Mount component** with `@vue/test-utils` or `@testing-library/vue`
4. **Test user interactions** (clicks, inputs, etc.)
5. **Assert rendered output** (not implementation details)
6. **Test props and emits**
7. **Mock external dependencies**
8. **Run tests** with `npm run test`

## Common Patterns

### Pattern 1: Form Handling

```vue
<script setup lang="ts">
import { reactive, computed } from 'vue'

interface FormData {
  email: string
  password: string
}

const form = reactive<FormData>({
  email: '',
  password: ''
})

const errors = reactive({
  email: '',
  password: ''
})

const isValid = computed(() => {
  return form.email.includes('@') && form.password.length >= 8
})

function validate() {
  errors.email = form.email.includes('@') ? '' : 'Invalid email'
  errors.password = form.password.length >= 8 ? '' : 'Password too short'
}

async function handleSubmit() {
  validate()
  if (!isValid.value) return

  // Submit form
  await api.submit(form)
}
</script>
```

### Pattern 2: API Integration

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const data = ref(null)
const loading = ref(false)
const error = ref(null)

async function fetchData() {
  loading.value = true
  error.value = null

  try {
    const response = await fetch('/api/data')
    data.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">Error: {{ error }}</div>
  <div v-else>{{ data }}</div>
</template>
```

### Pattern 3: Modal/Dialog Component

```vue
<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean
  title: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  confirm: []
}>()

function close() {
  emit('update:modelValue', false)
}

function confirm() {
  emit('confirm')
  close()
}
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click="close">
      <div class="modal-content" @click.stop>
        <h2>{{ title }}</h2>
        <slot />
        <div class="modal-actions">
          <button @click="close">Cancel</button>
          <button @click="confirm">Confirm</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
```

### Pattern 4: List with Virtual Scrolling

Use virtual scrolling for large lists (1000+ items):

```vue
<script setup>
// Use a virtual scrolling library like vue-virtual-scroller
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

const items = ref(Array.from({ length: 10000 }, (_, i) => ({
  id: i,
  name: `Item ${i}`
})))
</script>

<template>
  <RecycleScroller
    :items="items"
    :item-size="50"
    key-field="id"
    v-slot="{ item }"
  >
    <div class="item">{{ item.name }}</div>
  </RecycleScroller>
</template>
```

## Best Practices (2025)

### ✅ Do:
1. **Use `<script setup>` for all new components** - It's the 2025 standard
2. **Prefer `ref()` over `reactive()`** - More consistent and flexible
3. **Extract reusable logic into composables** - Keep components lean
4. **Use TypeScript for medium+ projects** - Better DX and fewer bugs
5. **Test with Vitest** - Modern, fast, Vite-integrated
6. **Lazy load routes and components** - Better performance
7. **Use computed for derived state** - Automatic caching
8. **Clean up side effects in `onUnmounted`** - Prevent memory leaks
9. **Use Vite for builds** - Faster than Webpack
10. **Follow naming conventions** - `use*` for composables, `PascalCase` for components

### ❌ Don't:
1. **Don't use Options API for new projects** - Legacy as of 2025
2. **Don't misuse `v-if`/`v-show`** - Wrong choice = 3x slower
3. **Don't prop drill** - Use provide/inject or Pinia
4. **Don't mutate props** - Props are read-only
5. **Don't forget keys in `v-for`** - Causes rendering bugs
6. **Don't create monolithic components** - Break them down
7. **Don't overuse watchers** - Use computed when possible
8. **Don't skip cleanup** - Always clean up in lifecycle hooks
9. **Don't use Vue CLI** - Use Vite + create-vue
10. **Don't use Jest** - Use Vitest for Vue 3

## Resources

This skill includes comprehensive reference guides and ready-to-use templates:

### references/composition-api-guide.md
Complete guide to Vue 3 Composition API and `<script setup>` syntax. Covers defineProps, defineEmits, lifecycle hooks, template refs, and combining with normal `<script>`.

**Load when:** Learning Composition API, understanding `<script setup>`, working with props/emits, using lifecycle hooks.

### references/reactivity-guide.md
Deep dive into Vue 3's reactivity system. Covers `ref()` vs `reactive()`, `toRefs()`, computed properties, `watch()` vs `watchEffect()`, and common reactivity pitfalls.

**Load when:** Choosing between ref and reactive, managing state, creating computed values, watching for changes, debugging reactivity issues.

### references/composables-patterns.md
Comprehensive guide to creating reusable composables. Covers naming conventions, structure patterns, common use cases (API fetching, event listeners), VueUse examples, and testing composables.

**Load when:** Creating composables, extracting reusable logic, learning from VueUse patterns, testing composables.

### references/component-patterns.md
Guide to Vue 3 component design patterns. Covers props (TypeScript + validation), emits (typed events), slots (default, named, scoped), provide/inject, and component composition strategies.

**Load when:** Designing component APIs, working with props/emits/slots, using provide/inject, composing components.

### references/performance-optimization.md
Performance optimization techniques for Vue 3. Covers lazy loading, code splitting, `v-show` vs `v-if`, virtual scrolling, computed caching, bundle optimization, and Vue 3.5 performance improvements (56% memory reduction).

**Load when:** Optimizing performance, reducing bundle size, implementing lazy loading, debugging slow renders, analyzing builds.

### references/typescript-integration.md
Complete TypeScript integration guide. Covers project setup with Vite, typing props/emits/refs, generic components, Volar extension setup, and migration from JavaScript.

**Load when:** Setting up TypeScript, typing components, using Volar, migrating from JavaScript, resolving type errors.

### references/testing-guide.md
Testing strategies with Vitest and Testing Library. Covers Vitest setup, component testing, testing props/emits/slots, testing composables, mocking, async testing, and E2E considerations.

**Load when:** Writing tests, setting up Vitest, testing components/composables, mocking dependencies, debugging tests.

### references/anti-patterns.md
Common Vue 3 mistakes and anti-patterns to avoid. Covers 14 anti-patterns including Options API usage, v-if/v-show misuse, prop drilling, reactivity pitfalls, memory leaks, and bundle size issues.

**Load when:** Reviewing code, debugging issues, learning what to avoid, code review feedback, performance problems.

### assets/component-template.vue
Production-ready Vue 3 component template with TypeScript, props, emits, reactive state, computed values, methods, and lifecycle hooks. Includes scoped styles and comprehensive examples.

**Use when:** Creating new components, need a starting template, teaching component structure.

### assets/composable-template.ts
Production-ready composable template with TypeScript, options object, reactive state, computed values, cleanup, and full JSDoc documentation. Includes useCounter example.

**Use when:** Creating new composables, need a starting template, learning composable structure.

### assets/vite.config.template.ts
Complete Vite configuration for Vue 3 projects. Includes Vue plugin setup, path aliases, dev server config, build optimization, chunk splitting, and CSS preprocessing.

**Use when:** Setting up new project, configuring Vite, optimizing build, adding aliases.

## Tips for Success

1. **Start with `<script setup>`** - Cleaner syntax, better performance, less boilerplate
2. **Think in composables** - Extract logic early, keep components focused on UI
3. **Use the template files** - Don't start from scratch, use provided templates
4. **Load references as needed** - Don't try to memorize everything, use references strategically
5. **Follow the decision tree** - It guides you to the right resource quickly
6. **Use TypeScript** - Even basic typing catches 80% of bugs
7. **Test with Vitest** - Fast feedback loop, great DX
8. **Optimize early** - Lazy load from the start, don't wait for problems
9. **Learn from VueUse** - Study well-written composables
10. **Keep up with Vue updates** - Vue 3.5+ brings significant improvements

## Version Notes

This skill is based on:
- **Vue 3.5.18** (current as of 2025)
- **Composition API** as standard (Options API is legacy)
- **Vite 6** as build tool (Vue CLI is deprecated)
- **Vitest 3** as test runner (Jest is legacy for Vue)
- **Volar** as IDE extension (Vetur is deprecated)
- **TypeScript 5** for type safety

The Vue ecosystem has matured significantly in 2025. The Composition API with `<script setup>` is now the standard approach for all new Vue development.
