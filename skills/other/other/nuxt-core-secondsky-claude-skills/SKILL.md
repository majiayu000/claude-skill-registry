---
name: nuxt-core
description: Nuxt 5 core framework with project setup, routing, SEO, error handling, and Vite 8/Nitro v3 configuration. Use when creating Nuxt 5 apps, setting up routing, or migrating config.
license: MIT
metadata:
  version: 5.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 5.x
  last-verified: 2026-03-30
---

# Nuxt 5 Core Fundamentals

Project setup, configuration, routing, SEO, and error handling for Nuxt 5 applications.

## Quick Reference

### Version Requirements

| Package | Minimum | Recommended |
|---------|---------|-------------|
| nuxt | 5.0.0 | 5.x |
| vue | 3.5.0 | 3.5.x |
| nitro | 3.0.0 | 3.x |
| vite | 8.0.0 | 8.x |
| typescript | 5.0.0 | 5.x |

### Key Commands

```bash
bunx nuxi@latest init my-app
bun run dev
bun run build
bun run preview
bun run postinstall
bunx nuxi typecheck
bunx nuxi add page about
bunx nuxi add component MyButton
bunx nuxi add composable useAuth
```

## Directory Structure (Nuxt v5)

```
my-nuxt-app/
├── app/                    # Default srcDir
│   ├── assets/             # Build-processed assets (CSS, images)
│   ├── components/         # Auto-imported Vue components
│   ├── composables/        # Auto-imported composables
│   ├── layouts/            # Layout components
│   ├── middleware/         # Route middleware
│   ├── pages/              # File-based routing
│   ├── plugins/            # Nuxt plugins
│   ├── utils/              # Auto-imported utility functions
│   ├── app.vue             # Main app component
│   ├── app.config.ts       # App-level runtime config
│   ├── error.vue           # Error page component
│   └── router.options.ts   # Router configuration
│
├── server/                 # Server-side code (Nitro v3)
│   ├── api/                # API endpoints
│   ├── middleware/         # Server middleware
│   ├── plugins/            # Nitro plugins
│   ├── routes/             # Server routes
│   └── utils/              # Server utilities
│
├── shared/                 # Shared code (app + server)
│   ├── utils/              # Auto-imported shared utils
│   └── types/              # Auto-imported shared types
│
├── public/                 # Static assets (served from root)
├── content/                # Nuxt Content files (if using)
├── layers/                 # Nuxt layers
├── modules/                # Local modules
├── .nuxt/                  # Generated files (git ignored)
├── .output/                # Build output (git ignored)
├── nuxt.config.ts          # Nuxt configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies
```

## What's New in Nuxt 5

| Area | Nuxt 4 | Nuxt 5 |
|------|--------|--------|
| Bundler | Vite 6 (esbuild + Rollup) | Vite 8 (Rolldown) |
| Server engine | Nitro v2 (h3 v1) | Nitro v3 (h3 v2, Web Standard APIs) |
| Vite config | Separate client/server configs | Vite Environment API |
| JS runtime | JSX plugin included by default | JSX plugin optional (on-demand) |
| Client-only placeholder | Empty `<div>` | HTML comment node |
| callHook | Always returns Promise | May return void (sync when possible) |
| clearNuxtState | Sets to `undefined` | Resets to initial default value |
| Page component names | Auto-generated | Normalized to match route names |
| `experimental.externalVue` | Available | Removed (always mocked) |

## Configuration

### Basic nuxt.config.ts

```typescript
export default defineNuxtConfig({
  future: {
    compatibilityVersion: 5
  },

  devtools: { enabled: true },

  modules: [
    '@nuxt/ui',
    '@nuxt/content',
    '@nuxt/image'
  ],

  runtimeConfig: {
    apiSecret: process.env.API_SECRET,
    databaseUrl: process.env.DATABASE_URL,

    public: {
      apiBase: process.env.API_BASE || 'https://api.example.com',
      appName: 'My App'
    }
  },

  app: {
    head: {
      title: 'My Nuxt App',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },

  nitro: {
    preset: 'cloudflare_pages'
  },

  typescript: {
    strict: true,
    typeCheck: true
  }
})
```

### Vite 8 / Rolldown Configuration

Nuxt 5 uses Vite 8 with Rolldown as the bundler. Use `rolldownOptions` instead of `rollupOptions`:

```typescript
export default defineNuxtConfig({
  vite: {
    build: {
      rolldownOptions: {
        output: {
          manualChunks: {
            vendor: ['vue', 'vue-router']
          }
        }
      }
    },

    optimizeDeps: {
      include: []
    }
  }
})
```

### Vite Environment API

Nuxt 5 uses the Vite Environment API for environment-specific config. Use `configEnvironment` and `applyToEnvironment` instead of separate client/server configs:

```typescript
// Module/plugin authors - use Vite plugins instead of extendViteConfig
addVitePlugin(() => ({
  name: 'my-plugin',
  config(config) {
    // Global vite configuration
  },
  configEnvironment(name, config) {
    // Environment-specific config
    if (name === 'client') {
      config.optimizeDeps ||= {}
      config.optimizeDeps.include ||= []
      config.optimizeDeps.include.push('my-package')
    }
  },
  applyToEnvironment(environment) {
    return environment.name === 'client'
  },
}))
```

### Optional JSX Support

`@vitejs/plugin-vue-jsx` is no longer installed by default. Install it only if needed:

```bash
bun add -D @vitejs/plugin-vue-jsx
```

Nuxt will auto-detect `.jsx`/`.tsx` files and prompt installation.

### Runtime Config Usage

```typescript
const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const apiSecret = config.apiSecret
```

**In server routes (v5 change):** `useRuntimeConfig()` no longer accepts `event`:

```typescript
// Nuxt 4
export default defineEventHandler((event) => {
  const config = useRuntimeConfig(event)
})

// Nuxt 5
export default defineEventHandler(() => {
  const config = useRuntimeConfig()
})
```

### App Config vs Runtime Config

| Feature | App Config | Runtime Config |
|---------|------------|----------------|
| Location | `app.config.ts` | `nuxt.config.ts` |
| Hot reload | Yes | No |
| Secrets | No | Yes (server-only) |
| Use case | UI settings, themes | API keys, URLs |

## Routing

### File-Based Routing

```
app/pages/
├── index.vue              → /
├── about.vue              → /about
├── users/
│   ├── index.vue          → /users
│   └── [id].vue           → /users/:id
└── blog/
    ├── index.vue          → /blog
    ├── [slug].vue         → /blog/:slug
    └── [...slug].vue      → /blog/* (catch-all)
```

**v5 Change**: Page component names are now normalized to match their route names. This ensures consistent `<KeepAlive>` behavior.

### Dynamic Routes

```vue
<!-- app/pages/users/[id].vue -->
<script setup lang="ts">
const route = useRoute()
const userId = computed(() => route.params.id)
const { data: user } = await useFetch(`/api/users/${userId.value}`)
</script>

<template>
  <div>
    <h1>{{ user?.name }}</h1>
  </div>
</template>
```

### Navigation

```vue
<script setup>
const goToUser = (id: string) => {
  navigateTo(`/users/${id}`)
}
</script>

<template>
  <NuxtLink to="/about">About</NuxtLink>
  <NuxtLink :to="`/users/${user.id}`">View User</NuxtLink>
  <NuxtLink to="/dashboard" prefetch>Dashboard</NuxtLink>
</template>
```

### Route Middleware

```typescript
// app/middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
```

```vue
<!-- app/pages/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})
</script>
```

### Global Middleware

```typescript
// app/middleware/analytics.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  if (import.meta.client) {
    window.gtag?.('event', 'page_view', {
      page_path: to.path
    })
  }
})
```

## SEO & Meta Tags

### useSeoMeta (Recommended)

```vue
<script setup lang="ts">
useSeoMeta({
  title: 'My Page Title',
  description: 'Page description for search engines',
  ogTitle: 'My Page Title',
  ogDescription: 'Page description',
  ogImage: 'https://example.com/og-image.jpg',
  ogUrl: 'https://example.com/my-page',
  twitterCard: 'summary_large_image'
})
</script>
```

### Dynamic Meta Tags

```vue
<script setup lang="ts">
const { data: post } = await useFetch(`/api/posts/${route.params.slug}`)

useSeoMeta({
  title: () => post.value?.title,
  description: () => post.value?.excerpt,
  ogImage: () => post.value?.image
})
</script>
```

## Error Handling

### Error Page

```vue
<!-- app/error.vue -->
<script setup lang="ts">
import type { NuxtError } from '#app'

const props = defineProps<{
  error: NuxtError
}>()

const handleError = () => {
  clearError({ redirect: '/' })
}
</script>

<template>
  <div class="error-page">
    <h1>{{ error.statusCode }}</h1>
    <p>{{ error.message }}</p>
    <button @click="handleError">Go Home</button>
  </div>
</template>
```

### Throwing Errors (App-side)

In the Vue part of your app (the `app/` directory), `createError` continues to work:

```typescript
throw createError({
  statusCode: 404,
  statusMessage: 'Page Not Found',
  fatal: true
})
```

### Error Boundaries (Component-Level)

```vue
<template>
  <NuxtErrorBoundary @error="handleError">
    <template #error="{ error, clearError }">
      <div>
        <h2>Something went wrong</h2>
        <p>{{ error.message }}</p>
        <button @click="clearError">Try again</button>
      </div>
    </template>
    <MyComponent />
  </NuxtErrorBoundary>
</template>
```

### clearNuxtState Resets to Defaults (v5 Change)

```typescript
// Nuxt 4: clearNuxtState sets state to undefined
// Nuxt 5: clearNuxtState resets state to its initial value

const count = useState('counter', () => 42)
count.value = 100

clearNuxtState('counter')
// Nuxt 5: count.value is now 42 (the default), not undefined
```

## Common Anti-Patterns

### Using process.env Instead of Runtime Config

```typescript
// WRONG
const apiUrl = process.env.API_URL

// CORRECT
const config = useRuntimeConfig()
const apiUrl = config.public.apiBase
```

### Missing Middleware Return

```typescript
// WRONG
export default defineNuxtRouteMiddleware((to) => {
  if (!isAuthenticated.value) {
    navigateTo('/login')  // Missing return!
  }
})

// CORRECT
export default defineNuxtRouteMiddleware((to) => {
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
```

### Non-Reactive Route Params

```typescript
// WRONG
const userId = route.params.id

// CORRECT
const userId = computed(() => route.params.id)
```

## Troubleshooting

**Build Errors / Type Errors:**
```bash
rm -rf .nuxt .output node_modules/.vite && bun install && bun run dev
```

**Route Not Found:**
- Check file is in `app/pages/`
- Verify file extension is `.vue`
- Check for typos in dynamic params `[id].vue`

**Vite Plugin Warnings:**
- Use `configEnvironment` + `applyToEnvironment` instead of `server`/`client` options
- Deprecated `extendViteConfig({ server })` will show warnings

**JSX Not Working:**
- Install `@vitejs/plugin-vue-jsx` if using `.jsx`/`.tsx` files

## Related Skills

- **nuxt-data**: Composables, data fetching, state management
- **nuxt-server**: Server routes, API patterns (Nitro v3)
- **nuxt-production**: Performance, testing, deployment, migration

## Templates Available

See `templates/` directory for:
- Production-ready `nuxt.config.ts`
- `app.vue` with proper structure

---

**Version**: 5.0.0 | **Last Updated**: 2026-03-30 | **License**: MIT
