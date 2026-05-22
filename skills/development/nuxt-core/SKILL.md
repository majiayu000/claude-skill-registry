---
name: nuxt-core
description: |
  Nuxt 4 core framework fundamentals: project setup, configuration, routing,
  SEO, error handling, and directory structure.

  Use when: creating new Nuxt 4 projects, configuring nuxt.config.ts,
  setting up routing and middleware, implementing SEO with useHead/useSeoMeta,
  handling errors with error.vue and NuxtErrorBoundary, or understanding
  Nuxt 4 directory structure.

  Keywords: Nuxt 4, nuxt.config.ts, file-based routing, pages directory,
  definePageMeta, useHead, useSeoMeta, error.vue, NuxtErrorBoundary,
  middleware, navigateTo, NuxtLink, app directory, runtime config
license: MIT
metadata:
  version: 4.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 4.x
  last-verified: 2025-12-28
---

# Nuxt 4 Core Fundamentals

Project setup, configuration, routing, SEO, and error handling for Nuxt 4 applications.

## Quick Reference

### Version Requirements

| Package | Minimum | Recommended |
|---------|---------|-------------|
| nuxt | 4.0.0 | 4.2.x |
| vue | 3.5.0 | 3.5.x |
| nitro | 2.10.0 | 2.12.x |
| vite | 6.0.0 | 6.2.x |
| typescript | 5.0.0 | 5.x |

### Key Commands

```bash
# Create new project
bunx nuxi@latest init my-app

# Development
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview

# Type checking
bun run postinstall  # Generates .nuxt directory
bunx nuxi typecheck

# Add a page/component/composable
bunx nuxi add page about
bunx nuxi add component MyButton
bunx nuxi add composable useAuth
```

## Directory Structure (Nuxt v4)

```
my-nuxt-app/
├── app/                    # Default srcDir in v4
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
├── server/                 # Server-side code (Nitro)
│   ├── api/                # API endpoints
│   ├── middleware/         # Server middleware
│   ├── plugins/            # Nitro plugins
│   ├── routes/             # Server routes
│   └── utils/              # Server utilities
│
├── public/                 # Static assets (served from root)
├── shared/                 # Shared code (app + server)
├── content/                # Nuxt Content files (if using)
├── layers/                 # Nuxt layers
├── modules/                # Local modules
├── .nuxt/                  # Generated files (git ignored)
├── .output/                # Build output (git ignored)
├── nuxt.config.ts          # Nuxt configuration
├── tsconfig.json           # TypeScript configuration
└── package.json            # Dependencies
```

**Key Change in v4**: The `app/` directory is now the default `srcDir`. All app code goes in `app/`, server code stays in `server/`.

## When to Load References

**Load `references/configuration-deep.md` when:**
- Configuring advanced nuxt.config.ts options
- Setting up modules and plugins
- Customizing Vite or Nitro configuration
- Configuring experimental features

**Load `references/routing-advanced.md` when:**
- Implementing complex routing patterns
- Creating route middleware with authentication
- Using catch-all routes or optional parameters
- Configuring router options

**Load `references/plugins-architecture.md` when:**
- Creating Nuxt plugins
- Injecting global utilities or composables
- Integrating third-party libraries
- Understanding plugin execution order

## Configuration

### Basic nuxt.config.ts

```typescript
export default defineNuxtConfig({
  // Enable Nuxt 4 features
  future: {
    compatibilityVersion: 4
  },

  // Development tools
  devtools: { enabled: true },

  // Modules
  modules: [
    '@nuxt/ui',
    '@nuxt/content',
    '@nuxt/image'
  ],

  // Runtime config (environment variables)
  runtimeConfig: {
    // Server-only (not exposed to client)
    apiSecret: process.env.API_SECRET,
    databaseUrl: process.env.DATABASE_URL,

    // Public (client + server)
    public: {
      apiBase: process.env.API_BASE || 'https://api.example.com',
      appName: 'My App'
    }
  },

  // App config
  app: {
    head: {
      title: 'My Nuxt App',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },

  // Nitro config (server)
  nitro: {
    preset: 'cloudflare-pages'
  },

  // TypeScript
  typescript: {
    strict: true,
    typeCheck: true
  }
})
```

### Runtime Config Usage

```typescript
// In composables or components
const config = useRuntimeConfig()

// Public values (client + server)
const apiBase = config.public.apiBase

// Server-only values (only in server/)
const apiSecret = config.apiSecret  // undefined on client!
```

**Critical Rule**: Always use `useRuntimeConfig()` instead of `process.env` for environment variables in production.

### App Config vs Runtime Config

| Feature | App Config | Runtime Config |
|---------|------------|----------------|
| Location | `app.config.ts` | `nuxt.config.ts` |
| Hot reload | Yes | No |
| Secrets | No | Yes (server-only) |
| Use case | UI settings, themes | API keys, URLs |

```typescript
// app/app.config.ts - UI settings (hot-reloadable)
export default defineAppConfig({
  theme: {
    primaryColor: '#3490dc'
  },
  ui: {
    rounded: 'lg'
  }
})

// Usage
const appConfig = useAppConfig()
const color = appConfig.theme.primaryColor
```

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

### Dynamic Routes

```vue
<!-- app/pages/users/[id].vue -->
<script setup lang="ts">
const route = useRoute()

// Get route params
const userId = route.params.id

// Reactive (updates when route changes)
const userId = computed(() => route.params.id)

// Fetch user data
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

const goBack = () => {
  navigateTo(-1)  // Go back in history
}

// With options
const goToLogin = () => {
  navigateTo('/login', {
    replace: true,  // Replace current history entry
    external: false // Internal navigation
  })
}
</script>

<template>
  <!-- Declarative navigation -->
  <NuxtLink to="/about">About</NuxtLink>
  <NuxtLink :to="`/users/${user.id}`">View User</NuxtLink>

  <!-- Prefetching (default: on hover) -->
  <NuxtLink to="/dashboard" prefetch>Dashboard</NuxtLink>

  <!-- No prefetch -->
  <NuxtLink to="/admin" :prefetch="false">Admin</NuxtLink>
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
  // Runs on every route change
  if (import.meta.client) {
    window.gtag?.('event', 'page_view', {
      page_path: to.path
    })
  }
})
```

### Page Meta

```vue
<script setup lang="ts">
definePageMeta({
  title: 'Dashboard',
  middleware: ['auth'],
  layout: 'admin',
  pageTransition: { name: 'fade' },
  keepalive: true
})
</script>
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
  twitterCard: 'summary_large_image',
  twitterTitle: 'My Page Title',
  twitterDescription: 'Page description',
  twitterImage: 'https://example.com/og-image.jpg'
})
</script>
```

### useHead (More Control)

```vue
<script setup lang="ts">
useHead({
  title: 'My Page Title',
  meta: [
    { name: 'description', content: 'Page description' },
    { property: 'og:title', content: 'My Page Title' }
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/my-page' }
  ],
  script: [
    { src: 'https://example.com/script.js', defer: true }
  ]
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

### Title Template

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      titleTemplate: '%s | My App'  // "Page Title | My App"
    }
  }
})
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

### Error Boundaries (Component-Level)

```vue
<template>
  <NuxtErrorBoundary @error="handleError">
    <template #error="{ error, clearError }">
      <div class="error-container">
        <h2>Something went wrong</h2>
        <p>{{ error.message }}</p>
        <button @click="clearError">Try again</button>
      </div>
    </template>

    <!-- Your component content -->
    <MyComponent />
  </NuxtErrorBoundary>
</template>

<script setup>
const handleError = (error: Error) => {
  console.error('Component error:', error)
  // Send to error tracking service
}
</script>
```

### Throwing Errors

```typescript
// In pages or components
throw createError({
  statusCode: 404,
  statusMessage: 'Page Not Found',
  fatal: true  // Shows error page, stops rendering
})

// Non-fatal error (shows inline)
throw createError({
  statusCode: 400,
  message: 'Invalid input'
})
```

### API Error Handling

```typescript
const { data, error } = await useFetch('/api/users')

if (error.value) {
  // Handle error gracefully
  showError({
    statusCode: error.value.statusCode,
    message: error.value.message
  })
}
```

## Common Anti-Patterns

### Using process.env Instead of Runtime Config

```typescript
// WRONG - Won't work in production!
const apiUrl = process.env.API_URL

// CORRECT
const config = useRuntimeConfig()
const apiUrl = config.public.apiBase
```

### Missing Middleware Guards

```typescript
// WRONG - No return, middleware continues
export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated.value) {
    navigateTo('/login')  // Missing return!
  }
})

// CORRECT
export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated.value) {
    return navigateTo('/login')  // Return stops middleware chain
  }
})
```

### Non-Reactive Route Params

```typescript
// WRONG - Not reactive
const userId = route.params.id

// CORRECT - Reactive
const userId = computed(() => route.params.id)
```

## Troubleshooting

**Build Errors / Type Errors:**
```bash
rm -rf .nuxt .output node_modules/.vite && bun install && bun run dev
```

**Route Not Found:**
- Check file is in `app/pages/` (not root `pages/`)
- Verify file extension is `.vue`
- Check for typos in dynamic params `[id].vue`

**Middleware Not Running:**
- Ensure file has `.global.ts` suffix for global middleware
- Check `definePageMeta({ middleware: 'name' })` matches filename
- Verify middleware returns `navigateTo()` or nothing

**Meta Tags Not Updating:**
- Use reactive values: `title: () => post.value?.title`
- Ensure `useSeoMeta` is called in `<script setup>`

## Related Skills

- **nuxt-data**: Composables, data fetching, state management
- **nuxt-server**: Server routes, API patterns, database integration
- **nuxt-production**: Performance, testing, deployment
- **nuxt-ui-v4**: Nuxt UI component library

## Templates Available

See `templates/` directory for:
- Production-ready `nuxt.config.ts`
- `app.vue` with proper structure
- Middleware examples

---

**Version**: 4.0.0 | **Last Updated**: 2025-12-28 | **License**: MIT
