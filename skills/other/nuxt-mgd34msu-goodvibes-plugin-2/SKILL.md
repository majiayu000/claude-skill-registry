---
name: nuxt
description: Builds applications with Nuxt 3 including pages, layouts, composables, server routes, and data fetching. Use when creating Vue applications with SSR, building full-stack Vue apps, or needing file-based routing with Vue.
---

# Nuxt 3

The intuitive Vue framework for building full-stack web applications.

## Quick Start

**Create project:**
```bash
npx nuxi@latest init my-app
cd my-app
npm install
npm run dev
```

## Project Structure

```
my-app/
  app.vue           # Root component
  nuxt.config.ts    # Configuration
  pages/            # File-based routing
  components/       # Auto-imported components
  composables/      # Auto-imported composables
  layouts/          # Page layouts
  server/           # Server routes & API
  middleware/       # Route middleware
  plugins/          # Vue plugins
  public/           # Static assets
  assets/           # Processed assets
```

## Pages & Routing

### Basic Pages

```vue
<!-- pages/index.vue -->
<template>
  <div>
    <h1>Home Page</h1>
    <NuxtLink to="/about">About</NuxtLink>
  </div>
</template>
```

### Dynamic Routes

```vue
<!-- pages/users/[id].vue -->
<script setup lang="ts">
const route = useRoute();
const userId = route.params.id;
</script>

<template>
  <div>User ID: {{ userId }}</div>
</template>
```

### Catch-All Routes

```vue
<!-- pages/[...slug].vue -->
<script setup lang="ts">
const route = useRoute();
// /a/b/c -> slug = ['a', 'b', 'c']
const segments = route.params.slug;
</script>
```

### Nested Routes

```
pages/
  users/
    [id]/
      index.vue      # /users/:id
      profile.vue    # /users/:id/profile
      settings.vue   # /users/:id/settings
```

## Layouts

### Default Layout

```vue
<!-- layouts/default.vue -->
<template>
  <div>
    <AppHeader />
    <main>
      <slot />
    </main>
    <AppFooter />
  </div>
</template>
```

### Custom Layout

```vue
<!-- layouts/admin.vue -->
<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <slot />
    </div>
  </div>
</template>
```

```vue
<!-- pages/admin/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  layout: 'admin',
});
</script>

<template>
  <div>Admin Dashboard</div>
</template>
```

## Data Fetching

### useFetch

```vue
<script setup lang="ts">
// Automatic caching and deduplication
const { data, pending, error, refresh } = await useFetch('/api/users');

// With options
const { data: posts } = await useFetch('/api/posts', {
  query: { limit: 10 },
  pick: ['id', 'title'], // Only pick specific fields
  transform: (data) => data.map(post => post.title),
});
</script>

<template>
  <div v-if="pending">Loading...</div>
  <div v-else-if="error">Error: {{ error.message }}</div>
  <ul v-else>
    <li v-for="user in data" :key="user.id">{{ user.name }}</li>
  </ul>
</template>
```

### useAsyncData

```vue
<script setup lang="ts">
// For custom async operations
const { data, pending } = await useAsyncData('users', () => {
  return $fetch('/api/users');
});

// With lazy loading
const { data: lazyData } = await useAsyncData(
  'lazy-users',
  () => $fetch('/api/users'),
  { lazy: true }
);
</script>
```

### $fetch

```vue
<script setup lang="ts">
// Direct fetch (no SSR hydration)
async function createUser(userData: User) {
  const newUser = await $fetch('/api/users', {
    method: 'POST',
    body: userData,
  });
  return newUser;
}
</script>
```

## State Management

### useState

```vue
<script setup lang="ts">
// Shared reactive state across components
const counter = useState('counter', () => 0);

function increment() {
  counter.value++;
}
</script>
```

### Composables

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = useState('counter', () => initial);

  function increment() {
    count.value++;
  }

  function decrement() {
    count.value--;
  }

  return { count, increment, decrement };
}
```

```vue
<!-- Any component - auto-imported -->
<script setup lang="ts">
const { count, increment } = useCounter(10);
</script>
```

## Server Routes

### API Endpoints

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const users = await prisma.user.findMany();
  return users;
});

// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const user = await prisma.user.create({ data: body });
  return user;
});
```

### Dynamic Routes

```typescript
// server/api/users/[id].get.ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id');
  const user = await prisma.user.findUnique({ where: { id } });

  if (!user) {
    throw createError({
      statusCode: 404,
      message: 'User not found',
    });
  }

  return user;
});
```

### Query Parameters

```typescript
// server/api/search.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  // /api/search?q=test&limit=10
  const { q, limit = 10 } = query;

  return await search(q, Number(limit));
});
```

## Middleware

### Route Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { loggedIn } = useUserSession();

  if (!loggedIn.value) {
    return navigateTo('/login');
  }
});
```

```vue
<!-- pages/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
});
</script>
```

### Global Middleware

```typescript
// middleware/logger.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  console.log(`Navigating from ${from.path} to ${to.path}`);
});
```

### Server Middleware

```typescript
// server/middleware/log.ts
export default defineEventHandler((event) => {
  console.log('Request:', event.path);
});
```

## Components

### Auto-imports

```vue
<!-- components/AppHeader.vue -->
<template>
  <header>
    <NuxtLink to="/">Home</NuxtLink>
  </header>
</template>

<!-- Automatically available in any page/component -->
<template>
  <div>
    <AppHeader />
  </div>
</template>
```

### Nested Components

```
components/
  base/
    Button.vue    # <BaseButton />
    Input.vue     # <BaseInput />
  user/
    Avatar.vue    # <UserAvatar />
```

## SEO & Meta

```vue
<script setup lang="ts">
useHead({
  title: 'My Page',
  meta: [
    { name: 'description', content: 'Page description' },
    { property: 'og:title', content: 'My Page' },
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/page' },
  ],
});

// Or use useSeoMeta
useSeoMeta({
  title: 'My Page',
  description: 'Page description',
  ogTitle: 'My Page',
  ogDescription: 'Page description',
  ogImage: 'https://example.com/image.png',
});
</script>
```

## Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
  ],

  runtimeConfig: {
    // Server-only
    apiSecret: process.env.API_SECRET,
    // Public (exposed to client)
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:3000',
    },
  },

  app: {
    head: {
      title: 'My App',
      meta: [
        { name: 'description', content: 'My app description' },
      ],
    },
  },

  routeRules: {
    '/': { prerender: true },
    '/api/**': { cors: true },
    '/admin/**': { ssr: false },
  },
});
```

## Rendering Modes

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  // Global SSR setting
  ssr: true,

  // Per-route rules
  routeRules: {
    '/': { prerender: true },           // Static at build
    '/blog/**': { isr: 3600 },          // ISR with 1hr revalidation
    '/admin/**': { ssr: false },        // Client-only SPA
    '/api/**': { cors: true },          // API routes
  },
});
```

## Plugins

```typescript
// plugins/my-plugin.ts
export default defineNuxtPlugin((nuxtApp) => {
  return {
    provide: {
      hello: (name: string) => `Hello ${name}!`,
    },
  };
});
```

```vue
<script setup lang="ts">
const { $hello } = useNuxtApp();
const greeting = $hello('World'); // "Hello World!"
</script>
```

## Error Handling

```vue
<!-- error.vue -->
<script setup lang="ts">
const props = defineProps<{
  error: {
    statusCode: number;
    message: string;
  };
}>();

const handleError = () => clearError({ redirect: '/' });
</script>

<template>
  <div>
    <h1>{{ error.statusCode }}</h1>
    <p>{{ error.message }}</p>
    <button @click="handleError">Go Home</button>
  </div>
</template>
```

## Best Practices

1. **Use composables** - Extract reusable logic
2. **Leverage auto-imports** - Components, composables, utils
3. **Use server routes** - API endpoints in same project
4. **Configure rendering** - SSR, SSG, ISR per route
5. **Use TypeScript** - Full type safety

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling composables outside setup | Only use in setup or other composables |
| Using reactive in server routes | Server routes are stateless |
| Missing await on useFetch | Always await data fetching |
| Not handling loading states | Check pending before data |
| Hardcoding env variables | Use runtimeConfig |

## Reference Files

- [references/data-fetching.md](references/data-fetching.md) - Data fetching patterns
- [references/server.md](references/server.md) - Server routes
- [references/modules.md](references/modules.md) - Popular modules
