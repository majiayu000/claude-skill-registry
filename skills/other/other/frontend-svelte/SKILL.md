---
name: frontend-svelte
description: Professional frontend development skill covering Svelte, SvelteKit, shadcn-svelte, and Bun ecosystem. Use this skill when building modern web applications, creating UI components, implementing state management, handling forms, or working with TypeScript-based frontend architectures. Ideal for projects requiring reactive frameworks, server-side rendering, or type-safe component development.
---

# Frontend Development Skill

Comprehensive skill for modern frontend development with Svelte, SvelteKit, shadcn-svelte, and the Bun ecosystem.

## Technology Stack

### Core Framework: Svelte + SvelteKit

#### Svelte Fundamentals
- **Reactive Framework**: Compile-time framework that converts components into highly efficient imperative code
- **True Reactivity**: Automatic dependency tracking without virtual DOM
- **Small Bundle Size**: Minimal runtime overhead
- **Built-in Animations**: Transition and animation directives
- **Scoped Styles**: Component styles are scoped by default

#### SvelteKit Features
- **Full-Stack Framework**: Server-side rendering (SSR), static site generation (SSG), and client-side rendering (CSR)
- **File-Based Routing**: Routes defined by file system structure
- **API Routes**: Build API endpoints alongside frontend code
- **Form Actions**: Server-side form handling with progressive enhancement
- **Hooks**: Intercept and modify requests/responses
- **Adapters**: Deploy to any platform (Node, Vercel, Netlify, Cloudflare, etc.)

### UI Component Library: shadcn-svelte

#### Overview
- Port of shadcn/ui for Svelte
- Accessible, customizable components built on Radix Svelte (Melt UI)
- Copy-paste component approach (not an npm package)
- Built with Tailwind CSS
- TypeScript support

#### Key Components
- **Forms**: Input, Textarea, Select, Checkbox, Radio, Switch
- **Feedback**: Alert, Toast (Sonner), Dialog, Alert Dialog
- **Navigation**: Button, Dropdown Menu, Tabs, Command Menu
- **Layout**: Card, Separator, Accordion, Collapsible
- **Data Display**: Table, Badge, Avatar, Skeleton
- **Overlays**: Popover, Tooltip, Sheet, Drawer

#### Installation & Usage
```bash
# Initialize shadcn-svelte
bunx shadcn-svelte@latest init

# Add components as needed
bunx shadcn-svelte@latest add button
bunx shadcn-svelte@latest add card
bunx shadcn-svelte@latest add form
```

### Package Manager: Bun

#### Why Bun?
- **Performance**: 25x faster than npm, 4x faster than pnpm
- **All-in-One**: Runtime, bundler, test runner, package manager
- **Drop-in Replacement**: Compatible with npm/Node.js ecosystem
- **Built-in Testing**: Vitest-compatible test runner
- **TypeScript Native**: Native TypeScript support, no compilation needed

#### npm Compatibility
- Reads package.json and package-lock.json/bun.lockb
- Works with most npm packages
- Can run npm scripts via `bun run`
- Falls back to npm when needed for specific packages

## Project Architecture

### Recommended Directory Structure

```
project-root/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── ui/              # shadcn-svelte components
│   │   │   │   ├── button/
│   │   │   │   ├── card/
│   │   │   │   └── ...
│   │   │   ├── layout/          # Layout components
│   │   │   │   ├── Header.svelte
│   │   │   │   ├── Footer.svelte
│   │   │   │   └── Sidebar.svelte
│   │   │   └── features/        # Feature-specific components
│   │   │       ├── auth/
│   │   │       ├── dashboard/
│   │   │       └── ...
│   │   ├── stores/              # Svelte stores
│   │   │   ├── user.ts
│   │   │   ├── theme.ts
│   │   │   └── notifications.ts
│   │   ├── utils/               # Utility functions
│   │   │   ├── api.ts
│   │   │   ├── validation.ts
│   │   │   └── formatting.ts
│   │   ├── types/               # TypeScript types
│   │   │   ├── api.ts
│   │   │   └── models.ts
│   │   ├── server/              # Server-side utilities
│   │   │   ├── db.ts
│   │   │   └── auth.ts
│   │   └── config/              # Configuration
│   │       ├── constants.ts
│   │       └── env.ts
│   ├── routes/                  # SvelteKit routes
│   │   ├── +page.svelte         # Home page
│   │   ├── +layout.svelte       # Root layout
│   │   ├── +error.svelte        # Error page
│   │   ├── api/                 # API routes
│   │   │   └── users/
│   │   │       └── +server.ts
│   │   ├── (auth)/              # Route group
│   │   │   ├── login/
│   │   │   └── register/
│   │   └── dashboard/
│   │       ├── +page.svelte
│   │       └── +page.server.ts
│   ├── app.html                 # HTML template
│   ├── app.css                  # Global styles
│   └── hooks.server.ts          # Server hooks
├── static/                      # Static assets
│   ├── images/
│   └── fonts/
├── tests/                       # Tests
│   ├── unit/
│   └── integration/
├── bun.lockb                    # Bun lockfile
├── package.json
├── svelte.config.js
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Core Patterns & Best Practices

### 1. Component Development

#### Component Structure Best Practices
```svelte
<script lang="ts">
  // 1. Imports (external, then internal)
  import { onMount, createEventDispatcher } from 'svelte';
  import { fade } from 'svelte/transition';
  import type { User } from '$lib/types';
  import { Button } from '$lib/components/ui/button';

  // 2. Type definitions (if not in separate file)
  interface $$Props {
    user: User;
    variant?: 'default' | 'compact';
  }

  // 3. Props with defaults
  export let user: User;
  export let variant: $$Props['variant'] = 'default';

  // 4. Event dispatcher
  const dispatch = createEventDispatcher<{
    edit: { userId: string };
    delete: { userId: string };
  }>();

  // 5. Local state
  let isEditing = false;
  let formData = { ...user };

  // 6. Reactive declarations
  $: fullName = `${user.firstName} ${user.lastName}`;
  $: hasChanges = JSON.stringify(formData) !== JSON.stringify(user);

  // 7. Functions
  function handleEdit() {
    isEditing = true;
  }

  function handleSave() {
    dispatch('edit', { userId: user.id });
    isEditing = false;
  }

  // 8. Lifecycle hooks
  onMount(() => {
    console.log('Component mounted');

    return () => {
      console.log('Component will unmount');
    };
  });
</script>

<!-- Template with clear hierarchy -->
<div class="user-card" class:compact={variant === 'compact'}>
  {#if isEditing}
    <form on:submit|preventDefault={handleSave}>
      <!-- Edit mode -->
    </form>
  {:else}
    <!-- View mode -->
    <div class="user-info" transition:fade>
      <h3>{fullName}</h3>
      <p>{user.email}</p>
    </div>
    <Button on:click={handleEdit}>Edit</Button>
  {/if}
</div>

<!-- Scoped styles -->
<style lang="postcss">
  .user-card {
    @apply rounded-lg border p-4;

    &.compact {
      @apply p-2;
    }
  }

  .user-info {
    @apply space-y-2;
  }
</style>
```

#### TypeScript Props Pattern
```typescript
// For complex props, use interface
interface $$Props {
  items: Item[];
  selectedId?: string;
  onSelect?: (item: Item) => void;
  class?: string;
}

export let items: $$Props['items'];
export let selectedId: $$Props['selectedId'] = undefined;
export let onSelect: $$Props['onSelect'] = undefined;

// For class prop forwarding
let className: $$Props['class'] = '';
export { className as class };
```

### 2. State Management

#### Svelte Stores

**Writable Store**
```typescript
// stores/user.ts
import { writable } from 'svelte/store';
import type { User } from '$lib/types';

function createUserStore() {
  const { subscribe, set, update } = writable<User | null>(null);

  return {
    subscribe,
    set,
    login: (user: User) => set(user),
    logout: () => set(null),
    updateProfile: (updates: Partial<User>) =>
      update(user => user ? { ...user, ...updates } : null)
  };
}

export const user = createUserStore();
```

**Derived Store**
```typescript
// stores/user.ts (continued)
import { derived } from 'svelte/store';

export const isAuthenticated = derived(
  user,
  $user => $user !== null
);

export const userPermissions = derived(
  user,
  $user => $user?.roles.flatMap(role => role.permissions) ?? []
);
```

**Readable Store (for external data)**
```typescript
import { readable } from 'svelte/store';

export const time = readable(new Date(), (set) => {
  const interval = setInterval(() => {
    set(new Date());
  }, 1000);

  return () => clearInterval(interval);
});
```

**Custom Store with Persistence**
```typescript
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export function persistedStore<T>(key: string, initialValue: T) {
  const stored = browser ? localStorage.getItem(key) : null;
  const initial = stored ? JSON.parse(stored) : initialValue;

  const store = writable<T>(initial);

  if (browser) {
    store.subscribe(value => {
      localStorage.setItem(key, JSON.stringify(value));
    });
  }

  return store;
}

// Usage
export const theme = persistedStore<'light' | 'dark'>('theme', 'light');
```

#### Context API (Component Tree State)
```svelte
<!-- Parent.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';
  import type { Writable } from 'svelte/store';
  import { writable } from 'svelte/store';

  const formData = writable({ name: '', email: '' });
  setContext('form', formData);
</script>

<!-- Child.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  import type { Writable } from 'svelte/store';

  const formData = getContext<Writable<FormData>>('form');
</script>

<input bind:value={$formData.name} />
```

### 3. SvelteKit Routing & Data Loading

#### Page Structure
```typescript
// routes/blog/[slug]/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch, parent }) => {
  // Access parent layout data
  const parentData = await parent();

  // Fetch data
  const response = await fetch(`/api/posts/${params.slug}`);
  const post = await response.json();

  return {
    post,
    meta: {
      title: post.title,
      description: post.excerpt
    }
  };
};
```

```svelte
<!-- routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.meta.title}</title>
  <meta name="description" content={data.meta.description} />
</svelte:head>

<article>
  <h1>{data.post.title}</h1>
  <div>{@html data.post.content}</div>
</article>
```

#### Server-Side Data Loading
```typescript
// routes/dashboard/+page.server.ts
import type { PageServerLoad, Actions } from './$types';
import { error, fail, redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, depends }) => {
  // depends() creates a dependency for invalidation
  depends('app:dashboard');

  if (!locals.user) {
    throw redirect(307, '/login');
  }

  try {
    const stats = await fetchUserStats(locals.user.id);
    return { stats };
  } catch (err) {
    throw error(500, 'Failed to load dashboard data');
  }
};

export const actions: Actions = {
  updateProfile: async ({ request, locals }) => {
    const formData = await request.formData();
    const name = formData.get('name');

    if (!name) {
      return fail(400, { name, missing: true });
    }

    await updateUser(locals.user.id, { name });
    return { success: true };
  }
};
```

#### Form Actions with Progressive Enhancement
```svelte
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  export let form: ActionData;

  let loading = false;
</script>

<form
  method="POST"
  action="?/updateProfile"
  use:enhance={() => {
    loading = true;

    return async ({ result, update }) => {
      await update();
      loading = false;

      if (result.type === 'success') {
        // Handle success
      }
    };
  }}
>
  <input
    name="name"
    value={form?.name ?? ''}
    aria-invalid={form?.missing}
  />

  {#if form?.missing}
    <p class="error">Name is required</p>
  {/if}

  <button disabled={loading}>
    {loading ? 'Saving...' : 'Save'}
  </button>
</form>
```


> **REST API endpoints** (GET/POST handlers, pagination) and **type-safe API client**: see [references/api-patterns.md](references/api-patterns.md)
> **Form handling & validation** (shadcn-svelte forms, sveltekit-superforms, Zod): see [references/forms-styling.md](references/forms-styling.md)
> **Tailwind CSS configuration** and component styling patterns: see [references/forms-styling.md](references/forms-styling.md)
> **Testing** (Vitest, integration), **performance** (code splitting, lazy loading), **accessibility** (Melt UI, ARIA): see [references/testing-performance-a11y.md](references/testing-performance-a11y.md)
> **Deployment** (Bun build, env vars), **common patterns** (dark mode, toast, auth, SSE), **troubleshooting**, and **resources**: see [references/deployment-patterns.md](references/deployment-patterns.md)
