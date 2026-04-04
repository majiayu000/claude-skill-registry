---
name: nuxt-production
description: |
  Nuxt 5 production optimization: hydration, performance, testing with Vitest,
  deployment to Cloudflare/Vercel/Netlify, and migration from Nuxt 4.

  Use when: debugging hydration mismatches, optimizing performance and Core Web Vitals,
  writing tests with Vitest, deploying to Cloudflare Pages/Workers/Vercel/Netlify,
  or migrating from Nuxt 4 to Nuxt 5.

  Keywords: hydration, hydration mismatch, ClientOnly, SSR, performance,
  lazy loading, lazy hydration, Vitest, testing, deployment, Cloudflare Pages,
  Cloudflare Workers, Vercel, Netlify, NuxtHub, migration, Nuxt 4 to Nuxt 5,
  Rolldown, Vite 8, Nitro v3, comment placeholder
license: MIT
metadata:
  version: 5.0.0
  author: Claude Skills Maintainers
  category: Framework
  framework: Nuxt
  framework-version: 5.x
  last-verified: 2026-03-30
---

# Nuxt 5 Production Guide

Hydration, performance, testing, deployment, and migration patterns.

## What's New in Nuxt 5

### v5 Key Changes

| Change | Nuxt 4 | Nuxt 5 |
|--------|--------|--------|
| Bundler | Vite 6 (esbuild + Rollup) | Vite 8 (Rolldown) |
| Server engine | Nitro v2 | Nitro v3 (h3 v2) |
| Server errors | `createError({statusCode})` | `HTTPError({status})` |
| Client-only placeholder | Empty `<div>` | HTML comment node |
| callHook | Always returns Promise | May return void |
| clearNuxtState | Sets to `undefined` | Resets to initial default |
| Page names | Auto-generated | Normalized to route names |
| JSX support | Included by default | Optional (on-demand) |
| externalVue | Configurable | Removed (always mocked) |

### Client-Only Comment Placeholders (v5)

Client-only components (`.client.vue` files and `createClientOnly()` wrappers) now render an HTML comment on the server instead of an empty `<div>`. This fixes scoped styles hydration issues.

```vue
<!-- If you relied on the placeholder <div> for layout -->
<ClientOnly>
  <MyComponent />
  <template #fallback>
    <div class="placeholder" style="min-height: 200px"></div>
  </template>
</ClientOnly>
```

To revert to the old `<div>` behavior:

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  experimental: {
    clientNodePlaceholder: false
  }
})
```

### Non-Async callHook (v5)

`callHook` may now return `void` instead of always returning `Promise`. Always use `await`:

```typescript
// WRONG
nuxtApp.callHook('my:hook', data).then(() => { ... })

// CORRECT
await nuxtApp.callHook('my:hook', data)
```

## When to Load References

**Load `references/hydration.md` when:**
- Debugging "Hydration node mismatch" errors
- Implementing ClientOnly components
- Fixing non-deterministic rendering issues

**Load `references/performance.md` when:**
- Optimizing Core Web Vitals scores
- Implementing lazy loading and code splitting
- Reducing bundle size

**Load `references/testing-vitest.md` when:**
- Writing component tests with @nuxt/test-utils
- Testing composables with Nuxt context
- Mocking Nuxt APIs

**Load `references/deployment-cloudflare.md` when:**
- Deploying to Cloudflare Pages or Workers
- Configuring wrangler.toml
- Setting up NuxtHub integration

## Hydration Best Practices

### What Causes Hydration Mismatches

| Cause | Example | Fix |
|-------|---------|-----|
| Non-deterministic values | `Math.random()` | Use `useState` |
| Browser APIs on server | `window.innerWidth` | Use `onMounted` |
| Date/time on server | `new Date()` | Use `useState` or `ClientOnly` |
| Third-party scripts | Analytics | Use `ClientOnly` |

### Fix Patterns

```vue
<!-- Non-deterministic values -->
<script setup>
const id = useState('random-id', () => Math.random())
</script>

<!-- Browser APIs -->
<script setup>
const width = ref(0)
onMounted(() => {
  width.value = window.innerWidth
})
</script>

<!-- ClientOnly component -->
<template>
  <ClientOnly>
    <MyMapComponent />
    <template #fallback>
      <div class="skeleton">Loading map...</div>
    </template>
  </ClientOnly>
</template>
```

## Performance Optimization

### Lazy Loading Components

```vue
<script setup>
const HeavyChart = defineAsyncComponent(() =>
  import('~/components/HeavyChart.vue')
)
</script>
```

### Lazy Hydration

```vue
<script setup>
const LazyComponent = defineLazyHydrationComponent(
  'visible',
  () => import('./HeavyComponent.vue')
)

const InteractiveComponent = defineLazyHydrationComponent(
  'interaction',
  () => import('./InteractiveComponent.vue')
)

const IdleComponent = defineLazyHydrationComponent(
  'idle',
  () => import('./IdleComponent.vue')
)
</script>
```

### Route Caching

```typescript
export default defineNuxtConfig({
  routeRules: {
    '/': { prerender: true },
    '/about': { prerender: true },
    '/blog/**': { swr: 3600 },
    '/products/**': { isr: 3600 },
    '/dashboard/**': { ssr: false },
    '/static/**': {
      headers: { 'Cache-Control': 'public, max-age=31536000' }
    }
  }
})
```

### Image Optimization

```vue
<template>
  <NuxtImg
    src="/images/hero.jpg"
    alt="Hero image"
    width="800"
    height="400"
    loading="lazy"
    placeholder
    format="webp"
  />

  <NuxtPicture
    src="/images/product.jpg"
    alt="Product"
    sizes="sm:100vw md:50vw lg:400px"
    :modifiers="{ quality: 80 }"
  />
</template>
```

## Testing with Vitest

### Setup

```bash
bun add -d @nuxt/test-utils vitest @vue/test-utils happy-dom
```

```typescript
// vitest.config.ts
import { defineVitestConfig } from '@nuxt/test-utils/config'

export default defineVitestConfig({
  test: {
    environment: 'nuxt',
    environmentOptions: {
      nuxt: {
        domEnvironment: 'happy-dom'
      }
    }
  }
})
```

### Component Testing

```typescript
import { describe, it, expect } from 'vitest'
import { mountSuspended } from '@nuxt/test-utils/runtime'
import UserCard from '~/components/UserCard.vue'

describe('UserCard', () => {
  it('renders user name', async () => {
    const wrapper = await mountSuspended(UserCard, {
      props: {
        user: { id: 1, name: 'John Doe', email: 'john@example.com' }
      }
    })

    expect(wrapper.text()).toContain('John Doe')
  })
})
```

### Mocking Composables

```typescript
import { mockNuxtImport } from '@nuxt/test-utils/runtime'

mockNuxtImport('useFetch', () => {
  return () => ({
    data: ref({ users: [{ id: 1, name: 'John' }] }),
    pending: ref(false),
    error: ref(null)
  })
})
```

## Deployment

### Cloudflare Pages (Recommended)

```bash
bun run build
bunx wrangler pages deploy .output/public
```

```typescript
export default defineNuxtConfig({
  nitro: { preset: 'cloudflare_pages' }
})
```

### Cloudflare Workers

```typescript
export default defineNuxtConfig({
  nitro: { preset: 'cloudflare_module' }
})
```

### Vercel / Netlify

```typescript
// Vercel
export default defineNuxtConfig({
  nitro: { preset: 'vercel' }
})

// Netlify
export default defineNuxtConfig({
  nitro: { preset: 'netlify' }
})
```

### NuxtHub (Cloudflare All-in-One)

```bash
bun add @nuxthub/core
```

```typescript
export default defineNuxtConfig({
  modules: ['@nuxthub/core'],
  hub: {
    database: true,
    kv: true,
    blob: true,
    cache: true
  }
})
```

## Migration from Nuxt 4

### Step 1: Update package.json

```json
{
  "devDependencies": {
    "nuxt": "^5.0.0"
  }
}
```

### Step 2: Enable Compatibility Mode

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  future: {
    compatibilityVersion: 5
  }
})
```

### Step 3: Update Server Error Handling

```typescript
// Before (Nuxt 4)
import { createError } from 'h3'
throw createError({ statusCode: 404, statusMessage: 'Not Found' })

// After (Nuxt 5)
import { HTTPError } from 'nitro/h3'
throw new HTTPError({ status: 404, statusText: 'Not Found' })
```

### Step 4: Update Server Event API

```typescript
// Before (Nuxt 4)
const path = event.path
event.node.res.statusCode = 200
setResponseHeader(event, 'x-custom', 'value')
const config = useRuntimeConfig(event)

// After (Nuxt 5)
const path = event.url.pathname
event.res.status = 200
event.res.headers.set('x-custom', 'value')
const config = useRuntimeConfig()
```

### Step 5: Update Vite Config

```typescript
// Before (Nuxt 4)
export default defineNuxtConfig({
  vite: {
    build: {
      rollupOptions: { ... }
    }
  }
})

// After (Nuxt 5) - use rolldownOptions
export default defineNuxtConfig({
  vite: {
    build: {
      rolldownOptions: { ... }
    }
  }
})
```

### Step 6: Update Route Rules

```typescript
// Before
routeRules: {
  '/old': { redirect: { to: '/new', statusCode: 302 } }
}

// After
routeRules: {
  '/old': { redirect: { to: '/new', status: 302 } }
}
```

### Step 7: Update Import Paths

```typescript
// Before
import { defineEventHandler, getQuery } from 'h3'

// After
import { defineEventHandler, getQuery } from 'nitro/h3'
// Or rely on auto-imports (no import needed)
```

### Step 8: Remove Deprecated Options

```typescript
// Remove these from nuxt.config.ts
export default defineNuxtConfig({
  experimental: {
    externalVue: false,  // REMOVED - delete this
    viteEnvironmentApi: true,  // REMOVED - always enabled
  }
})
```

### Step 9: Install JSX Plugin (If Needed)

```bash
# Only if your project uses .jsx/.tsx files
bun add -D @vitejs/plugin-vue-jsx
```

### Step 10: Update callHook Usage

```typescript
// Before
nuxtApp.callHook('my:hook', data).then(() => { ... })

// After
await nuxtApp.callHook('my:hook', data)
```

## Common Anti-Patterns

### Client-Only Code on Server

```typescript
// WRONG
const width = window.innerWidth

// CORRECT
if (import.meta.client) {
  const width = window.innerWidth
}

// Or use onMounted
onMounted(() => {
  const width = window.innerWidth
})
```

### Non-Deterministic SSR

```typescript
// WRONG
const id = Math.random()
const time = Date.now()

// CORRECT
const id = useState('id', () => Math.random())
const time = useState('time', () => Date.now())
```

## Troubleshooting

**Hydration Mismatch:**
- Check for `window`, `document`, `localStorage` usage
- Wrap in `ClientOnly` or use `onMounted`
- Look for `Math.random()`, `Date.now()`
- Check if relying on `<div>` placeholder for client-only components

**Build Errors:**
```bash
rm -rf .nuxt .output node_modules/.vite && bun install
```

**Vite Plugin Warnings:**
- Migrate from `extendViteConfig({ server })` to `configEnvironment`
- Use `applyToEnvironment` instead of `server: false` / `client: false`

**Rolldown Build Issues:**
- Replace `rollupOptions` with `rolldownOptions`
- Replace `vite.esbuild` with `vite.oxc`
- Check CJS interop changes in Vite 8

## Related Skills

- **nuxt-core**: Project setup, routing, configuration
- **nuxt-data**: Composables, data fetching, state
- **nuxt-server**: Server routes, API patterns (Nitro v3)
- **cloudflare-d1**: D1 database patterns

---

**Version**: 5.0.0 | **Last Updated**: 2026-03-30 | **License**: MIT
