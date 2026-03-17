---
name: frontend-vue
description: Professional Vue.js development skill covering Nuxt 3, Vue 3 Composition API, Tailwind CSS, and the Vue ecosystem. Use this skill when building Vue applications, implementing Nuxt features, using Pinia for state management, or component libraries like shadcn-vue.
---

# Vue Development Skill

Comprehensive skill for modern Vue.js development, focusing on Nuxt 3, Vue 3 Composition API, Tailwind CSS, and the Vue ecosystem.

## Technology Stack

### Core Framework: Vue 3 + Nuxt 3

#### Vue 3 Features
- **Composition API**: Logic reuse with `<script setup>`
- **Reactivity System**: `ref`, `reactive`, `computed`, `watch`
- **Teleport**: Rendering content outside the component DOM hierarchy
- **Fragments**: Multiple root nodes support
- **Suspense**: Handling async dependencies

#### Nuxt 3 Features
- **Auto-imports**: Automatically imports Vue APIs and component components
- **File-based Routing**: Pages in `pages/` directory create routes
- **Server Engine (Nitro)**: Universal deployment
- **Data Fetching**: `useFetch`, `useAsyncData`
- **Server Routes**: API endpoints in `server/api/`
- **SEO/Meta**: `useHead`, `useSeoMeta`

### UI Framework: Tailwind CSS + shadcn-vue

#### Tailwind CSS
- Utility-first architecture
- Configured via `tailwind.config.ts`
- Optimized with PostCSS

#### shadcn-vue (or similar)
- Vue port of shadcn/ui
- Accessible components based on Radix Vue
- **Key Components**: Button, Input, Select, Dialog, Toast

### State Management
- **Pinia**: The official state management library for Vue
  - Modular stores
  - TypeScript support
  - DevTools integration
  - No mutations (only actions)

## Project Architecture

### Recommend Directory Structure (Nuxt 3)
```
project-root/
├── app.vue            # Root component
├── nuxt.config.ts     # Configuration
├── components/        # Auto-imported components
│   ├── ui/            # UI library components
│   │   ├── button/
│   │   └── ...
│   └── Header.vue
├── pages/             # Routes
│   ├── index.vue
│   └── about.vue
├── layouts/           # Layout wrappers
│   └── default.vue
├── composables/       # Auto-imported logic
│   └── useUser.ts
├── server/            # Server API
│   └── api/
│       └── hello.ts
├── stores/            # Pinia stores
│   └── counter.ts
└── assets/            # CSS, images
    └── main.css
```

## Best Practices

### Composition API with `<script setup>`
- Use `const` for reactive variables.
- Keep logic organized by feature.
- Extract complex logic into composables (`composables/`).

### Performance
- **Async Components**: Use `defineAsyncComponent` for lazy loading.
- **Lazy Fetching**: Use `lazy: true` option in `useFetch` for non-critical data.
- **Asset Optimization**: Use Nuxt Image for image optimization.

### Nuxt Specifics
- **Hydration Mismatch**: Ensure HTML rendered on server matches client. Avoid random IDs or dates during initial render.
- **Middleware**: Use Route Middleware for auth guards (`middleware/auth.ts`).

## Common Code Patterns

### Nuxt Page with Data Fetching
```vue
<script setup lang="ts">
const { data: user, error } = await useFetch('/api/user/1')

if (error.value) {
  console.error(error.value)
}
</script>

<template>
  <div v-if="user" class="p-4">
    <h1 class="text-2xl font-bold">{{ user.name }}</h1>
    <p>{{ user.email }}</p>
  </div>
  <div v-else>Loading...</div>
</template>
```

### Pinia Store
```ts
// stores/counter.ts
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }

  return { count, doubleCount, increment }
})
```

### Composable
```ts
// composables/useMouse.ts
export function useMouse() {
  const x = ref(0)
  const y = ref(0)

  function update(event) {
    x.value = event.pageX
    y.value = event.pageY
  }

  onMounted(() => window.addEventListener('mousemove', update))
  onUnmounted(() => window.removeEventListener('mousemove', update))

  return { x, y }
}
```
