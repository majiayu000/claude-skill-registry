---
name: web-framework-nuxt
description: Nuxt 3 patterns - file-based routing, data fetching (useFetch/useAsyncData), useState, server routes, middleware, auto-imports, layouts, SEO
---

# Nuxt 3 Framework Patterns

> **Quick Guide:** Use `useFetch` for API calls in components (SSR-safe), `useAsyncData` for custom data sources. Create server routes in `server/api/`. Auto-imports handle composables and components automatically. Use `useState` for SSR-friendly shared state.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `useFetch` or `useAsyncData` for data fetching in components - NEVER raw `$fetch` in setup which causes double-fetching)**

**(You MUST use `server/api/` for API routes - handlers export default with `defineEventHandler()`)**

**(You MUST use `definePageMeta` to attach middleware and configure page behavior)**

**(You MUST use `useHead` or `useSeoMeta` for SEO metadata - never manual `<head>` tags)**

**(You MUST ensure `useState` values are JSON-serializable for SSR hydration)**

</critical_requirements>

---

**Auto-detection:** Nuxt 3, nuxt.config.ts, useFetch, useAsyncData, useState, defineEventHandler, definePageMeta, defineNuxtRouteMiddleware, NuxtLayout, NuxtPage, NuxtLink, navigateTo, server/api, pages/, layouts/, middleware/, composables/, useHead, useSeoMeta

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
- Static sites without server-side logic (consider VitePress)
- Projects already committed to Next.js patterns (React ecosystem)

**Detailed Resources:**

- For code examples:
  - [data-fetching.md](examples/data-fetching.md) - useFetch, useAsyncData, $fetch patterns
  - [server-routes.md](examples/server-routes.md) - API routes with defineEventHandler
  - [middleware.md](examples/middleware.md) - Route middleware for auth and guards
  - [state-management.md](examples/state-management.md) - useState composables
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Nuxt 3 is a **meta-framework for Vue 3** that provides file-based routing, automatic code splitting, server-side rendering, and a powerful data-fetching system. Built on Nitro server engine, it enables full-stack development with API routes colocated with your frontend.

**Core Principles:**

1. **Universal rendering by default** - Pages render on server first, then hydrate on client
2. **Auto-imports everywhere** - Composables, components, and utilities are automatically available
3. **File-based conventions** - Directories define behavior (pages/, server/, layouts/, middleware/)
4. **SSR-safe data fetching** - Composables prevent double-fetching between server and client
5. **Zero-config TypeScript** - Full type safety with automatic type generation

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: File-Based Routing

Nuxt uses the `pages/` directory for file-based routing. File names become URL paths.

#### Routing Conventions

| File                        | URL                      | Description        |
| --------------------------- | ------------------------ | ------------------ |
| `pages/index.vue`           | `/`                      | Home page          |
| `pages/about.vue`           | `/about`                 | Static route       |
| `pages/blog/[slug].vue`     | `/blog/:slug`            | Dynamic parameter  |
| `pages/users/[...slug].vue` | `/users/*`               | Catch-all route    |
| `pages/posts/[[id]].vue`    | `/posts` or `/posts/:id` | Optional parameter |

#### Basic Page Structure

```vue
<!-- pages/index.vue -->
<script setup lang="ts">
// Auto-imported: no explicit imports needed for Nuxt composables

definePageMeta({
  title: "Home Page",
});

const { data: posts } = await useFetch("/api/posts");
</script>

<template>
  <div>
    <h1>Welcome</h1>
    <NuxtLink to="/about">About</NuxtLink>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <NuxtLink :to="`/blog/${post.slug}`">{{ post.title }}</NuxtLink>
      </li>
    </ul>
  </div>
</template>
```

**Why good:** File names map directly to URLs, NuxtLink provides prefetching, auto-imports eliminate boilerplate, definePageMeta configures page behavior

#### Dynamic Routes

```vue
<!-- pages/blog/[slug].vue -->
<script setup lang="ts">
const route = useRoute();
const slug = route.params.slug as string;

const { data: post, error } = await useFetch(`/api/posts/${slug}`);

if (error.value) {
  throw createError({
    statusCode: 404,
    statusMessage: "Post not found",
  });
}
</script>

<template>
  <article v-if="post">
    <h1>{{ post.title }}</h1>
    <div v-html="post.content" />
  </article>
</template>
```

**Why good:** Dynamic segments use bracket syntax, route params typed via useRoute, createError triggers error page

#### Catch-All Routes

```vue
<!-- pages/docs/[...slug].vue -->
<script setup lang="ts">
const route = useRoute();
// slug is an array: ['guide', 'getting-started'] for /docs/guide/getting-started
const slugArray = route.params.slug as string[];
const path = slugArray.join("/");

const { data: doc } = await useFetch(`/api/docs/${path}`);
</script>

<template>
  <div v-if="doc">
    <h1>{{ doc.title }}</h1>
    <div v-html="doc.content" />
  </div>
</template>
```

**Why good:** Catch-all routes handle nested paths, slug is array of segments, enables documentation-style hierarchies

---

### Pattern 2: Data Fetching with useFetch

`useFetch` is the primary composable for API calls. It prevents double-fetching by transferring server data to client during hydration.

#### Basic useFetch

```typescript
// In <script setup>
const API_ENDPOINT = "/api/users";

// Simple fetch - URL as cache key
const { data, error, status, refresh } = await useFetch(API_ENDPOINT);

// With query parameters
const page = ref(1);
const { data: users } = await useFetch(API_ENDPOINT, {
  query: { page, limit: 20 },
});

// Watch option - refetch when reactive values change
const { data: searchResults } = await useFetch("/api/search", {
  query: { q: searchQuery },
  watch: [searchQuery],
});
```

**Why good:** Automatic SSR hydration prevents double-fetch, reactive query params, watch option for auto-refetch

#### useFetch with Options

```vue
<script setup lang="ts">
interface User {
  id: number;
  name: string;
  email: string;
}

const USERS_ENDPOINT = "/api/users";

const {
  data: users,
  pending,
  error,
  refresh,
} = await useFetch<User[]>(USERS_ENDPOINT, {
  // Pick specific fields to reduce payload
  pick: ["id", "name"],

  // Transform response before returning
  transform: (response) => response.filter((user) => user.active),

  // Lazy loading - don't block navigation
  lazy: true,

  // Custom cache key
  key: "active-users",

  // Default value while loading
  default: () => [],
});
</script>

<template>
  <div>
    <div v-if="pending">Loading...</div>
    <div v-else-if="error">Error: {{ error.message }}</div>
    <ul v-else>
      <li v-for="user in users" :key="user.id">{{ user.name }}</li>
    </ul>
    <button @click="refresh()">Refresh</button>
  </div>
</template>
```

**Why good:** Type-safe with generics, pick reduces payload size, transform shapes data, lazy prevents navigation blocking, default provides fallback

#### POST Requests with useFetch

```vue
<script setup lang="ts">
interface CreateUserPayload {
  name: string;
  email: string;
}

const form = reactive<CreateUserPayload>({
  name: "",
  email: "",
});

const { execute, status, error } = useFetch("/api/users", {
  method: "POST",
  body: form,
  immediate: false, // Don't execute on mount
});

async function handleSubmit() {
  await execute();
  if (!error.value) {
    navigateTo("/users");
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="form.name" placeholder="Name" />
    <input v-model="form.email" type="email" placeholder="Email" />
    <button type="submit" :disabled="status === 'pending'">
      {{ status === "pending" ? "Creating..." : "Create User" }}
    </button>
    <p v-if="error" class="error">{{ error.message }}</p>
  </form>
</template>
```

**Why good:** immediate: false for user-triggered actions, reactive body auto-serializes, status for loading state, navigateTo for redirect

---

### Pattern 3: useAsyncData for Custom Data Sources

`useAsyncData` provides more control than `useFetch` - use it for non-HTTP data sources or when you need to combine multiple fetches.

#### Basic useAsyncData

```vue
<script setup lang="ts">
// For custom data sources or complex logic
const { data: user, pending } = await useAsyncData("user", async () => {
  // Can use any async operation
  const response = await $fetch("/api/user");
  return response;
});

// Multiple parallel requests
const { data } = await useAsyncData("dashboard", async () => {
  const [users, posts, stats] = await Promise.all([
    $fetch("/api/users"),
    $fetch("/api/posts"),
    $fetch("/api/stats"),
  ]);
  return { users, posts, stats };
});
</script>

<template>
  <div v-if="data">
    <UserList :users="data.users" />
    <PostList :posts="data.posts" />
    <StatsCard :stats="data.stats" />
  </div>
</template>
```

**Why good:** First argument is cache key (required for deduplication), Promise.all for parallel requests, $fetch inside useAsyncData is SSR-safe

#### Reactive useAsyncData

```vue
<script setup lang="ts">
const userId = ref("1");

// Re-fetches when userId changes
const { data: user } = await useAsyncData(
  () => `user-${userId.value}`, // Dynamic key
  () => $fetch(`/api/users/${userId.value}`),
  { watch: [userId] },
);
</script>
```

**Why good:** Dynamic key function, watch option for reactive dependencies, automatic refetch on change

---

### Pattern 4: Server Routes with defineEventHandler

Nuxt server routes live in `server/api/` (prefixed with `/api`) or `server/routes/` (no prefix).

#### Basic API Route

```typescript
// server/api/users.get.ts
import type { User } from "~/types";

export default defineEventHandler(async (event): Promise<User[]> => {
  // Access query parameters
  const query = getQuery(event);
  const page = Number(query.page) || 1;
  const limit = Number(query.limit) || 20;

  // Fetch from database or external API
  const users = await db.users.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return users;
});
```

**Why good:** File suffix `.get.ts` restricts to GET method, getQuery extracts query params, typed return value

#### POST Route with Body

```typescript
// server/api/users.post.ts
import { z } from "zod";

const CreateUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
});

export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  // Validate request body
  const result = CreateUserSchema.safeParse(body);
  if (!result.success) {
    throw createError({
      statusCode: 400,
      statusMessage: "Validation failed",
      data: result.error.flatten(),
    });
  }

  const user = await db.users.create({
    data: result.data,
  });

  setResponseStatus(event, 201);
  return user;
});
```

**Why good:** readBody parses request body, Zod validation for type safety, createError for typed errors, setResponseStatus for custom status codes

#### Dynamic Route Parameters

```typescript
// server/api/users/[id].ts
export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id");

  if (!id) {
    throw createError({
      statusCode: 400,
      statusMessage: "User ID required",
    });
  }

  const user = await db.users.findUnique({ where: { id } });

  if (!user) {
    throw createError({
      statusCode: 404,
      statusMessage: "User not found",
    });
  }

  return user;
});
```

**Why good:** getRouterParam extracts dynamic segments, early returns for validation, createError for HTTP errors

#### Catch-All Server Route

```typescript
// server/api/proxy/[...path].ts
export default defineEventHandler(async (event) => {
  const path = event.context.params?.path || "";

  // Forward request to external API
  const response = await $fetch(`https://external-api.com/${path}`, {
    method: event.method,
    headers: {
      Authorization: `Bearer ${process.env.API_KEY}`,
    },
  });

  return response;
});
```

**Why good:** Catch-all for proxying, context.params for path segments, server-side secrets safe

---

### Pattern 5: useState for Shared State

`useState` is an SSR-friendly composable for shared reactive state. Values transfer from server to client during hydration.

#### Basic useState

```vue
<script setup lang="ts">
// Shared state across components - key-based
const counter = useState("counter", () => 0);

function increment() {
  counter.value++;
}
</script>

<template>
  <div>
    <p>Count: {{ counter }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>
```

**Why good:** Key ensures state sharing across components, initializer function runs once, SSR-safe hydration

#### Composable with useState

```typescript
// composables/use-user.ts
interface User {
  id: string;
  name: string;
  email: string;
}

export function useUser() {
  const user = useState<User | null>("user", () => null);
  const isLoggedIn = computed(() => user.value !== null);

  async function login(credentials: { email: string; password: string }) {
    const response = await $fetch<User>("/api/auth/login", {
      method: "POST",
      body: credentials,
    });
    user.value = response;
  }

  async function logout() {
    await $fetch("/api/auth/logout", { method: "POST" });
    user.value = null;
  }

  return {
    user: readonly(user),
    isLoggedIn,
    login,
    logout,
  };
}
```

```vue
<!-- Using the composable -->
<script setup lang="ts">
const { user, isLoggedIn, logout } = useUser();
</script>

<template>
  <div v-if="isLoggedIn">
    <p>Welcome, {{ user?.name }}</p>
    <button @click="logout">Logout</button>
  </div>
</template>
```

**Why good:** Composable encapsulates state logic, useState key ensures singleton, readonly prevents external mutation, computed for derived state

#### useState Limitations

```typescript
// CRITICAL: useState values must be JSON-serializable

// WRONG - Functions not serializable
const state = useState("fn", () => ({
  callback: () => console.log("hi"), // Error during hydration
}));

// WRONG - Classes not serializable
const state = useState("class", () => new MyClass());

// CORRECT - Plain objects and primitives
const state = useState("data", () => ({
  count: 0,
  items: [],
  settings: { theme: "dark" },
}));
```

**Why good:** Clear constraint - JSON-serializable only, prevents hydration mismatches

---

### Pattern 6: Route Middleware

Middleware runs before navigating to a route. Use for authentication, authorization, and redirects.

#### Named Middleware

```typescript
// middleware/auth.ts
export default defineNuxtRouteMiddleware((to, from) => {
  const { isLoggedIn } = useUser();

  if (!isLoggedIn.value) {
    return navigateTo("/login");
  }
});
```

```vue
<!-- pages/dashboard.vue -->
<script setup lang="ts">
definePageMeta({
  middleware: "auth",
});
</script>

<template>
  <div>Dashboard content (protected)</div>
</template>
```

**Why good:** Named middleware reusable across pages, navigateTo for redirects, definePageMeta attaches middleware

#### Global Middleware

```typescript
// middleware/analytics.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
  // .global suffix runs on every route
  if (import.meta.client) {
    // Track page view (client-side only)
    trackPageView(to.fullPath);
  }
});
```

**Why good:** .global suffix for automatic execution, import.meta.client for client-only code

#### Inline Middleware

```vue
<script setup lang="ts">
definePageMeta({
  middleware: [
    // Inline middleware for page-specific logic
    function (to, from) {
      const hasPermission = checkPermission(to.params.id as string);
      if (!hasPermission) {
        return abortNavigation();
      }
    },
    "auth", // Can mix with named middleware
  ],
});
</script>
```

**Why good:** Inline for one-off logic, array for multiple middleware, abortNavigation cancels navigation

---

### Pattern 7: Layouts

Layouts wrap pages with shared UI. Use for navigation, footers, and page structure.

#### Default Layout

```vue
<!-- layouts/default.vue -->
<script setup lang="ts">
const { isLoggedIn, user } = useUser();
</script>

<template>
  <div class="layout">
    <header>
      <nav>
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/about">About</NuxtLink>
        <template v-if="isLoggedIn">
          <span>{{ user?.name }}</span>
          <NuxtLink to="/dashboard">Dashboard</NuxtLink>
        </template>
        <NuxtLink v-else to="/login">Login</NuxtLink>
      </nav>
    </header>

    <main>
      <slot />
      <!-- Page content renders here -->
    </main>

    <footer>
      <p>&copy; 2024 My App</p>
    </footer>
  </div>
</template>
```

**Why good:** slot for page content, composables work in layouts, NuxtLink for navigation

#### Custom Layouts

```vue
<!-- layouts/admin.vue -->
<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <NuxtLink to="/admin">Dashboard</NuxtLink>
      <NuxtLink to="/admin/users">Users</NuxtLink>
      <NuxtLink to="/admin/settings">Settings</NuxtLink>
    </aside>
    <main class="content">
      <slot />
    </main>
  </div>
</template>
```

```vue
<!-- pages/admin/index.vue -->
<script setup lang="ts">
definePageMeta({
  layout: "admin",
  middleware: "auth",
});
</script>

<template>
  <div>Admin Dashboard</div>
</template>
```

**Why good:** definePageMeta selects layout, layouts can be combined with middleware

#### Dynamic Layout

```vue
<script setup lang="ts">
const route = useRoute();

// Change layout based on condition
const layout = computed(() => {
  return route.query.print ? "print" : "default";
});
</script>

<template>
  <NuxtLayout :name="layout">
    <NuxtPage />
  </NuxtLayout>
</template>
```

**Why good:** NuxtLayout with dynamic name, reactive layout switching

---

### Pattern 8: SEO with useHead and useSeoMeta

Nuxt provides composables for managing document head and SEO metadata.

#### useHead for Page Metadata

```vue
<script setup lang="ts">
const SITE_NAME = "My Awesome Site";

useHead({
  title: "About Us",
  titleTemplate: (title) => `${title} | ${SITE_NAME}`,
  meta: [
    { name: "description", content: "Learn about our company and mission" },
  ],
  link: [{ rel: "canonical", href: "https://example.com/about" }],
});
</script>

<template>
  <div>
    <h1>About Us</h1>
    <!-- Page content -->
  </div>
</template>
```

**Why good:** titleTemplate for consistent formatting, composable API, SSR-rendered

#### useSeoMeta for SEO

```vue
<script setup lang="ts">
const { data: post } = await useFetch(`/api/posts/${route.params.slug}`);

useSeoMeta({
  title: () => post.value?.title ?? "Blog Post",
  description: () => post.value?.excerpt ?? "",
  ogTitle: () => post.value?.title ?? "Blog Post",
  ogDescription: () => post.value?.excerpt ?? "",
  ogImage: () => post.value?.coverImage ?? "/default-og.png",
  ogType: "article",
  twitterCard: "summary_large_image",
});
</script>

<template>
  <article v-if="post">
    <h1>{{ post.title }}</h1>
    <img :src="post.coverImage" :alt="post.title" />
    <div v-html="post.content" />
  </article>
</template>
```

**Why good:** Reactive values with functions, type-safe property names, automatic Open Graph and Twitter cards

#### Global Head Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  app: {
    head: {
      charset: "utf-8",
      viewport: "width=device-width, initial-scale=1",
      title: "My App",
      meta: [{ name: "theme-color", content: "#ffffff" }],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    },
  },
});
```

**Why good:** Global defaults in config, page-level overrides with composables

---

### Pattern 9: Error Handling

Nuxt provides error boundaries and utilities for graceful error handling.

#### Creating Errors

```typescript
// In server routes
export default defineEventHandler(async (event) => {
  const user = await getUser(event);

  if (!user) {
    throw createError({
      statusCode: 404,
      statusMessage: "User not found",
      message: "The requested user does not exist",
      data: { userId: getRouterParam(event, "id") },
    });
  }

  return user;
});
```

```vue
<!-- In pages -->
<script setup lang="ts">
const { data, error } = await useFetch("/api/protected");

if (error.value) {
  throw createError({
    statusCode: error.value.statusCode,
    statusMessage: error.value.statusMessage,
  });
}
</script>
```

**Why good:** createError works in both server and client, typed error structure, data for additional context

#### Error Page

```vue
<!-- error.vue (root level, not in pages/) -->
<script setup lang="ts">
import type { NuxtError } from "#app";

const props = defineProps<{
  error: NuxtError;
}>();

const handleError = () => clearError({ redirect: "/" });

const HTTP_NOT_FOUND = 404;
</script>

<template>
  <div class="error-page">
    <h1>
      {{ error.statusCode === HTTP_NOT_FOUND ? "Page Not Found" : "Error" }}
    </h1>
    <p>{{ error.message }}</p>
    <button @click="handleError">Go Home</button>
  </div>
</template>
```

**Why good:** Root-level error.vue catches all errors, clearError for recovery, typed error props

#### NuxtErrorBoundary for Component Errors

```vue
<template>
  <NuxtErrorBoundary @error="handleError">
    <!-- Content that might error -->
    <RiskyComponent />

    <template #error="{ error, clearError }">
      <div class="error-boundary">
        <p>Component failed: {{ error.message }}</p>
        <button @click="clearError">Retry</button>
      </div>
    </template>
  </NuxtErrorBoundary>
</template>

<script setup lang="ts">
function handleError(error: Error) {
  console.error("Caught error:", error);
  // Report to error tracking service
}
</script>
```

**Why good:** Component-level isolation, clearError for retry, @error event for logging

---

### Pattern 10: Plugins

Plugins run before Vue app creation. Use for registering global components, directives, or external libraries.

#### Basic Plugin

```typescript
// plugins/my-plugin.ts
export default defineNuxtPlugin((nuxtApp) => {
  // Available everywhere via useNuxtApp()
  return {
    provide: {
      hello: (name: string) => `Hello, ${name}!`,
    },
  };
});
```

```vue
<script setup lang="ts">
const { $hello } = useNuxtApp();
const greeting = $hello("World"); // "Hello, World!"
</script>
```

**Why good:** provide for global utilities, useNuxtApp for access, auto-loaded from plugins/

#### Client-Only Plugin

```typescript
// plugins/analytics.client.ts
export default defineNuxtPlugin(() => {
  // .client suffix = runs only in browser

  // Initialize analytics
  const analytics = initializeAnalytics();

  return {
    provide: {
      analytics,
    },
  };
});
```

**Why good:** .client suffix for browser-only code, server-only with .server suffix

#### Plugin with Dependencies

```typescript
// plugins/api.ts
export default defineNuxtPlugin(async (nuxtApp) => {
  const config = useRuntimeConfig();

  const api = $fetch.create({
    baseURL: config.public.apiBase,
    onRequest({ options }) {
      // Add auth header
      const token = useCookie("token");
      if (token.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`,
        };
      }
    },
  });

  return {
    provide: { api },
  };
});
```

```vue
<script setup lang="ts">
const { $api } = useNuxtApp();

// Uses configured $fetch instance
const { data } = await useAsyncData("users", () => $api("/users"));
</script>
```

**Why good:** $fetch.create for configured client, useRuntimeConfig for environment values, useCookie for auth tokens

</patterns>

---

<integration>

## Integration Guide

**Nuxt 3 is a full-stack Vue framework.** It handles routing, rendering, data fetching, and server-side logic. Other tools integrate through composables and plugins.

**Styling integration:**

- Apply styles via `class` attribute on components
- Supports CSS, SCSS, CSS Modules, or any PostCSS-compatible solution
- Global styles in `assets/` directory
- Scoped styles in component `<style scoped>` blocks

**Data fetching integration:**

- Server data: `useFetch` and `useAsyncData` (built-in SSR support)
- Real-time: WebSocket connections via client-only plugins

**State management:**

- Simple state: `useState` composable (SSR-safe)
- Complex state: External state libraries via plugins with SSR considerations

**Form handling:**

- Native form submission with server routes
- Client-side validation via composables

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `useFetch` or `useAsyncData` for data fetching in components - NEVER raw `$fetch` in setup which causes double-fetching)**

**(You MUST use `server/api/` for API routes - handlers export default with `defineEventHandler()`)**

**(You MUST use `definePageMeta` to attach middleware and configure page behavior)**

**(You MUST use `useHead` or `useSeoMeta` for SEO metadata - never manual `<head>` tags)**

**(You MUST ensure `useState` values are JSON-serializable for SSR hydration)**

**Failure to follow these rules will cause SSR hydration mismatches, double-fetching, and broken page metadata.**

</critical_reminders>
