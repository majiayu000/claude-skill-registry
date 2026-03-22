---
name: nuxt
description: >-
  You are an expert in Nuxt 3, the full-stack Vue framework with server-side
  rendering, auto-imports, file-based routing, API routes powered by Nitro,
  and 200+ modules. You help developers build production Vue applications with
  hybrid rendering (SSR/SSG/SPA per route), server components, middleware,
  state management with useState, data fetching with useFetch/useAsyncData,
  and deployment to 20+ platforms.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Frontend Development
  tags:
    - vue
    - framework
    - ssr
    - ssg
    - fullstack
    - nitro
    - auto-imports
---

# Nuxt — The Vue Framework

You are an expert in Nuxt 3, the full-stack Vue framework with server-side rendering, auto-imports, file-based routing, API routes powered by Nitro, and 200+ modules. You help developers build production Vue applications with hybrid rendering (SSR/SSG/SPA per route), server components, middleware, state management with useState, data fetching with useFetch/useAsyncData, and deployment to 20+ platforms.

## Core Capabilities

### Pages and Routing

```vue
<!-- pages/index.vue — Auto-routed to / -->
<script setup lang="ts">
const { data: posts } = await useFetch('/api/posts')
</script>

<template>
  <div>
    <h1>Blog</h1>
    <div v-for="post in posts" :key="post.id" class="post-card">
      <NuxtLink :to="`/posts/${post.slug}`">
        <h2>{{ post.title }}</h2>
        <p>{{ post.excerpt }}</p>
      </NuxtLink>
    </div>
  </div>
</template>
```

```vue
<!-- pages/posts/[slug].vue — Dynamic route -->
<script setup lang="ts">
const route = useRoute()
const { data: post, error } = await useAsyncData(
  `post-${route.params.slug}`,
  () => $fetch(`/api/posts/${route.params.slug}`)
)

if (error.value) {
  throw createError({ statusCode: 404, message: 'Post not found' })
}

// SEO
useHead({
  title: post.value?.title,
  meta: [{ name: 'description', content: post.value?.excerpt }],
})

useSeoMeta({
  ogTitle: post.value?.title,
  ogImage: post.value?.coverImage,
})
</script>

<template>
  <article v-if="post">
    <h1>{{ post.title }}</h1>
    <div v-html="post.content" />
  </article>
</template>
```

### Server API Routes

```typescript
// server/api/posts/index.get.ts
export default defineEventHandler(async () => {
  const posts = await db.posts.findMany({ orderBy: { createdAt: 'desc' } })
  return posts
})

// server/api/posts/[slug].get.ts
export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug')
  const post = await db.posts.findUnique({ where: { slug } })
  if (!post) throw createError({ statusCode: 404, message: 'Not found' })
  return post
})

// server/api/posts/index.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const session = await requireAuth(event)
  return db.posts.create({ data: { ...body, authorId: session.userId } })
})

// server/middleware/auth.ts
export default defineEventHandler(async (event) => {
  const path = getRequestURL(event).pathname
  if (!path.startsWith('/api/admin')) return
  const session = await getSession(event)
  if (!session) throw createError({ statusCode: 401 })
  event.context.user = session.user
})
```

### Composables and State

```typescript
// composables/useAuth.ts — Auto-imported everywhere
export function useAuth() {
  const user = useState<User | null>('user', () => null)
  const isLoggedIn = computed(() => !!user.value)

  async function login(email: string, password: string) {
    user.value = await $fetch('/api/auth/login', { method: 'POST', body: { email, password } })
  }

  async function logout() {
    await $fetch('/api/auth/logout', { method: 'POST' })
    user.value = null
    navigateTo('/login')
  }

  return { user, isLoggedIn, login, logout }
}
```

## Installation

```bash
npx nuxi@latest init my-app
cd my-app && npm install
npm run dev
```

## Best Practices

1. **Auto-imports** — Components, composables, utils auto-imported; no import statements needed
2. **useFetch for data** — SSR-safe data fetching; deduplicates requests, caches across navigation
3. **Hybrid rendering** — Set per-route rendering in `nuxt.config.ts`: SSR, SSG, SPA, or ISR
4. **useState** — SSR-safe reactive state; shared across components, serialized server→client
5. **Server routes** — `server/api/` directory; powered by Nitro; deploy to any platform
6. **SEO** — `useHead()` and `useSeoMeta()` for per-page meta tags; SSR-rendered for crawlers
7. **Modules** — 200+ modules: `@nuxtjs/tailwindcss`, `@sidebase/nuxt-auth`, `@nuxt/image`, etc.
8. **Nitro engine** — Universal server deploys to Node, Vercel, Netlify, Cloudflare, Deno, Bun
