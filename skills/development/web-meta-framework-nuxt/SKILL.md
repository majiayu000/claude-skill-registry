---
name: web-meta-framework-nuxt
description: Nuxt patterns - file-based routing, data fetching (useFetch/useAsyncData), useState, server routes, middleware, auto-imports, layouts, SEO
---

# Nuxt Framework Patterns

> **Quick Guide:** Use `useFetch` for API calls in components (SSR-safe), `useAsyncData` for custom data sources or parallel fetches. Create server routes in `server/api/`. Auto-imports handle composables and components automatically. Use `useState` for SSR-friendly shared state. Data is a `shallowRef` by default -- use `deep: true` if you need deep reactivity.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `useFetch` or `useAsyncData` for data fetching in components -- NEVER raw `$fetch` in setup which causes double-fetching)**

**(You MUST use `server/api/` for API routes -- handlers export default with `defineEventHandler()`)**

**(You MUST use `definePageMeta` to attach middleware and configure page behavior -- it is a macro, values must be statically analyzable)**

**(You MUST use `useHead` or `useSeoMeta` for SEO metadata -- never manual `<head>` tags)**

**(You MUST ensure `useState` values are JSON-serializable for SSR hydration -- no functions, classes, or Symbols)**

</critical_requirements>

---

**Auto-detection:** Nuxt, nuxt.config.ts, useFetch, useAsyncData, useState, defineEventHandler, definePageMeta, defineNuxtRouteMiddleware, NuxtLayout, NuxtPage, NuxtLink, navigateTo, server/api, pages/, layouts/, middleware/, composables/, useHead, useSeoMeta, app/ directory

**When to use:**

- Building Vue 3 applications with file-based routing and SSR/SSG
- Creating full-stack applications with server routes in the same project
- Implementing data fetching that works seamlessly across server and client
- Building SEO-optimized pages with automatic metadata handling
- Leveraging auto-imports for composables and components

**Key patterns covered:**

- File-based routing (pages/, dynamic routes, catch-all routes)
- Data fetching (useFetch, useAsyncData, $fetch)
- Server routes (server/api/, defineEventHandler)
- Shared state (useState composable)
- Route middleware (defineNuxtRouteMiddleware, navigateTo)
- Layouts (layouts/, NuxtLayout, setPageLayout)
- SEO (useHead, useSeoMeta)
- Plugins (plugins/, defineNuxtPlugin)
- Error handling (NuxtErrorBoundary, createError, showError)
- Auto-imports (composables, components, utils)

**When NOT to use:**

- Simple SPAs without SSR needs (consider Vue + Vite directly)
- Static documentation sites without server logic (consider a static-site generator)

---

<philosophy>

## Philosophy

Nuxt is a **meta-framework for Vue 3** that provides file-based routing, automatic code splitting, server-side rendering, and a powerful data-fetching system. Built on Nitro server engine, it enables full-stack development with API routes colocated with your frontend.

**Core Principles:**

1. **Universal rendering by default** -- Pages render on server first, then hydrate on client
2. **Auto-imports everywhere** -- Composables, components, and utilities are automatically available
3. **File-based conventions** -- Directories define behavior (pages/, server/, layouts/, middleware/)
4. **SSR-safe data fetching** -- Composables prevent double-fetching between server and client
5. **Zero-config TypeScript** -- Full type safety with automatic type generation
6. **Shallow reactivity for performance** -- `data` from `useFetch`/`useAsyncData` is a `shallowRef` by default

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: File-Based Routing

File names in `pages/` become URL paths. Dynamic segments use bracket syntax.

| File                        | URL                      | Description        |
| --------------------------- | ------------------------ | ------------------ |
| `pages/index.vue`           | `/`                      | Home page          |
| `pages/about.vue`           | `/about`                 | Static route       |
| `pages/blog/[slug].vue`     | `/blog/:slug`            | Dynamic parameter  |
| `pages/users/[...slug].vue` | `/users/*`               | Catch-all route    |
| `pages/posts/[[id]].vue`    | `/posts` or `/posts/:id` | Optional parameter |

```vue
<!-- pages/blog/[slug].vue -->
<script setup lang="ts">
const route = useRoute();
const slug = route.params.slug as string;
const { data: post, error } = await useFetch(`/api/posts/${slug}`);

if (error.value) {
  throw createError({ statusCode: 404, statusMessage: "Post not found" });
}
</script>
```

**Why good:** File names map to URLs, bracket syntax for dynamic params, createError triggers error page

See [examples/core.md](examples/core.md) for complete page examples with layouts and middleware.

---

### Pattern 2: Data Fetching (useFetch / useAsyncData)

`useFetch` wraps `useAsyncData` + `$fetch`. It prevents double-fetching by transferring server data to client during hydration. Data is a `shallowRef` -- replace the whole object to trigger reactivity, or use `deep: true`.

```typescript
// Simple fetch -- URL is cache key
const { data, error, status, refresh, clear } = await useFetch("/api/users");

// With reactive query params and auto-refetch
const page = ref(1);
const { data: users } = await useFetch("/api/users", {
  query: { page, limit: 20 },
  watch: [page],
});

// POST with immediate: false for user-triggered actions
const { execute, status } = useFetch("/api/users", {
  method: "POST",
  body: form,
  immediate: false,
  watch: false,
});
```

Use `useAsyncData` when combining multiple fetches or using non-HTTP sources:

```typescript
const { data } = await useAsyncData("dashboard", async () => {
  const [users, stats] = await Promise.all([
    $fetch("/api/users"),
    $fetch("/api/stats"),
  ]);
  return { users, stats };
});
```

**Critical:** `$fetch` in `<script setup>` (outside useFetch/useAsyncData) runs on **both** server and client, causing double-fetching. Always wrap in a composable.

See [examples/data-fetching.md](examples/data-fetching.md) for typed responses, transforms, lazy loading, and server-only fetch patterns.

---

### Pattern 3: Server Routes

Server routes live in `server/api/` (prefixed with `/api`) or `server/routes/` (no prefix). File suffix restricts HTTP method.

```typescript
// server/api/users.get.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const page = Number(query.page) || 1;
  return db.users.findMany({ skip: (page - 1) * 20, take: 20 });
});

// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  // Validate body with Zod or similar
  setResponseStatus(event, 201);
  return db.users.create({ data: body });
});
```

| Pattern   | File                       | URL               |
| --------- | -------------------------- | ----------------- |
| GET       | `server/api/users.get.ts`  | `GET /api/users`  |
| POST      | `server/api/users.post.ts` | `POST /api/users` |
| Dynamic   | `server/api/users/[id].ts` | `/api/users/:id`  |
| Catch-all | `server/api/[...path].ts`  | `/api/*`          |
| No prefix | `server/routes/health.ts`  | `/health`         |

See [examples/server-routes.md](examples/server-routes.md) for validation, error handling, server middleware, and CRUD patterns.

---

### Pattern 4: useState for Shared State

`useState` is an SSR-friendly composable for shared reactive state. Values transfer from server to client during hydration and **must be JSON-serializable**.

```typescript
// composables/use-user.ts
export function useUser() {
  const user = useState<User | null>("user", () => null);
  const isLoggedIn = computed(() => user.value !== null);

  async function login(credentials: { email: string; password: string }) {
    user.value = await $fetch<User>("/api/auth/login", {
      method: "POST",
      body: credentials,
    });
  }

  return { user: readonly(user), isLoggedIn, login };
}
```

**Key constraints:** Values must be JSON-serializable (no functions, classes). Key ensures singleton sharing across components. Wrap mutations in composable functions.

See [examples/state-management.md](examples/state-management.md) for cart state, UI state, cookie persistence, and server-initialized patterns.

---

### Pattern 5: Route Middleware

Middleware runs before navigation. Use for auth, authorization, and redirects.

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn } = useUser();
  if (!isLoggedIn.value) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`);
  }
});
```

| Type   | File Pattern                | Behavior                  |
| ------ | --------------------------- | ------------------------- |
| Named  | `middleware/auth.ts`        | Opt-in via definePageMeta |
| Global | `middleware/auth.global.ts` | Runs on every navigation  |
| Inline | Function in definePageMeta  | Page-specific logic       |

Attach via `definePageMeta({ middleware: "auth" })` or `definePageMeta({ middleware: ["auth", "admin"] })`.

**Critical:** Use `to` and `from` parameters -- never `useRoute()` in middleware (may have stale values).

See [examples/middleware.md](examples/middleware.md) for role-based auth, feature flags, guest guards, and global middleware patterns.

---

### Pattern 6: Layouts

Layouts wrap pages with shared UI (navigation, footers). Default layout applies automatically.

```vue
<!-- layouts/default.vue -->
<template>
  <div class="layout">
    <header>
      <nav><!-- Navigation --></nav>
    </header>
    <main><slot /></main>
    <footer><!-- Footer --></footer>
  </div>
</template>
```

Select layout per page: `definePageMeta({ layout: "admin" })`. Dynamic layout: `<NuxtLayout :name="computedLayout">`.

See [examples/core.md](examples/core.md) for layout examples with auth-aware navigation.

---

### Pattern 7: SEO with useHead and useSeoMeta

```vue
<script setup lang="ts">
const { data: post } = await useFetch(`/api/posts/${route.params.slug}`);

useSeoMeta({
  title: () => post.value?.title ?? "Blog Post",
  description: () => post.value?.excerpt ?? "",
  ogTitle: () => post.value?.title ?? "Blog Post",
  ogImage: () => post.value?.coverImage ?? "/default-og.png",
  twitterCard: "summary_large_image",
});
</script>
```

**Why good:** Reactive values with getter functions, type-safe property names, automatic Open Graph and Twitter cards, SSR-rendered

Global defaults in `nuxt.config.ts` via `app.head`. Page-level overrides via composables.

---

### Pattern 8: Plugins

Plugins run before Vue app creation. Use for registering global utilities or external libraries.

```typescript
// plugins/api.client.ts  -- .client suffix = browser only
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const api = $fetch.create({
    baseURL: config.public.apiBase,
    onRequest({ options }) {
      const token = useCookie("token");
      if (token.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`,
        };
      }
    },
  });
  return { provide: { api } };
});
```

Access via `useNuxtApp().$api`. Suffixes: `.client.ts` (browser), `.server.ts` (server), no suffix (both).

---

### Pattern 9: Error Handling

```typescript
// Server route errors
throw createError({
  statusCode: 404,
  statusMessage: "Not found",
  data: { id },
});

// Page-level: check useFetch error, throw createError
// Component-level: NuxtErrorBoundary with #error slot
// Global: error.vue at root level with clearError({ redirect: "/" })
```

`createError` works in both server and client. `NuxtErrorBoundary` isolates component failures. Root `error.vue` catches unhandled errors.

See [examples/core.md](examples/core.md) for error page and boundary examples.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Routing, layouts, error handling, auto-imports
- [examples/data-fetching.md](examples/data-fetching.md) - useFetch, useAsyncData, $fetch patterns
- [examples/server-routes.md](examples/server-routes.md) - API routes, validation, server middleware
- [examples/middleware.md](examples/middleware.md) - Auth guards, role-based access, global middleware
- [examples/state-management.md](examples/state-management.md) - useState composables, persistence
- [reference.md](reference.md) - Decision frameworks, checklists, anti-patterns

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `$fetch` directly in `<script setup>` for initial data -- causes double-fetching (server + client)
- Non-serializable values in `useState` -- functions, classes, Symbols cause hydration errors
- Missing `key` in `useAsyncData` for dynamic data -- leads to stale data and caching issues
- `useRoute()` in middleware -- use `to` and `from` parameters instead; useRoute may have stale values
- Secrets in client-side code -- use `runtimeConfig` private keys for server-only secrets

**Medium Priority Issues:**

- Blocking data fetches without `lazy: true` -- slows navigation; use lazy for non-critical data
- Not handling error state from useFetch -- always check and display `error.value`
- Using `onMounted` for data that should be in useFetch -- misses SSR benefits
- Forgetting `await` before `useFetch` in setup -- component renders before data is ready

**Gotchas & Edge Cases:**

- `useFetch` URL is the cache key -- same URL = same cached data; use `key` option to differentiate
- `useState` runs initializer only once per key -- subsequent calls return existing state
- Middleware runs on both server and client -- use `import.meta.server`/`import.meta.client` to split
- `server/api/` routes auto-prefix with `/api` -- `server/api/users.ts` becomes `/api/users`
- `definePageMeta` is a macro, not runtime -- values must be statically analyzable
- `NuxtLink` with external URLs needs `external` prop or use `<a>` instead
- Composables must be called synchronously in setup -- no `await` before first composable call
- `watch` in `useFetch` requires reactive values -- plain variables won't trigger refetch
- `data` from `useFetch`/`useAsyncData` is a `shallowRef` -- mutating nested properties won't trigger reactivity; replace the whole object or use `deep: true`
- `data` and `error` default to `undefined` (not `null`) -- adjust null checks accordingly

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `useFetch` or `useAsyncData` for data fetching in components -- NEVER raw `$fetch` in setup which causes double-fetching)**

**(You MUST use `server/api/` for API routes -- handlers export default with `defineEventHandler()`)**

**(You MUST use `definePageMeta` to attach middleware and configure page behavior -- it is a macro, values must be statically analyzable)**

**(You MUST use `useHead` or `useSeoMeta` for SEO metadata -- never manual `<head>` tags)**

**(You MUST ensure `useState` values are JSON-serializable for SSR hydration -- no functions, classes, or Symbols)**

**Failure to follow these rules will cause SSR hydration mismatches, double-fetching, and broken page metadata.**

</critical_reminders>
