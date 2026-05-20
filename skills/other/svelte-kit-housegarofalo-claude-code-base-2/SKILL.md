---
name: svelte-kit
description: Expert guidance for SvelteKit 2 with Svelte 5 runes, server-side rendering, and modern patterns. Covers $state, $derived, $effect, form actions, load functions, and API routes. Use for SvelteKit applications, Svelte 5 runes, and full-stack Svelte development.
---

# SvelteKit Development

Expert guidance for SvelteKit 2 with Svelte 5 runes, server-side rendering, and modern patterns.

## Svelte 5 Runes

### Basic Reactivity

```svelte
<script lang="ts">
  // Reactive state (replaces let)
  let count = $state(0);

  // Derived values (replaces $:)
  let doubled = $derived(count * 2);

  // Complex derived
  let summary = $derived.by(() => {
    if (count === 0) return 'Zero';
    if (count < 10) return 'Small';
    return 'Large';
  });

  // Side effects (replaces $:)
  $effect(() => {
    console.log(`Count is now ${count}`);

    // Cleanup function
    return () => console.log('Cleaning up');
  });

  function increment() {
    count++;
  }
</script>

<button onclick={increment}>
  Count: {count} (doubled: {doubled})
</button>
<p>{summary}</p>
```

### Props with TypeScript

```svelte
<script lang="ts">
  import type { User } from '$lib/types';

  interface Props {
    user: User;
    isEditable?: boolean;
    onUpdate?: (user: User) => void;
  }

  let { user, isEditable = false, onUpdate }: Props = $props();

  // Bindable props
  let { value = $bindable() }: { value: string } = $props();
</script>

<div class="user-card">
  <h2>{user.name}</h2>
  {#if isEditable}
    <button onclick={() => onUpdate?.(user)}>Edit</button>
  {/if}
</div>
```

### State Classes

```typescript
// lib/stores/counter.svelte.ts
export class Counter {
  value = $state(0);
  doubled = $derived(this.value * 2);

  increment() {
    this.value++;
  }

  decrement() {
    this.value--;
  }

  reset() {
    this.value = 0;
  }
}

// Usage in component
<script>
  import { Counter } from '$lib/stores/counter.svelte';

  const counter = new Counter();
</script>

<button onclick={() => counter.increment()}>
  {counter.value} x 2 = {counter.doubled}
</button>
```

## SvelteKit Routing

### File Structure

```
src/
├── routes/
│   ├── +page.svelte          # /
│   ├── +layout.svelte        # Shared layout
│   ├── +error.svelte         # Error page
│   ├── about/
│   │   └── +page.svelte      # /about
│   ├── blog/
│   │   ├── +page.svelte      # /blog
│   │   └── [slug]/
│   │       ├── +page.svelte  # /blog/:slug
│   │       └── +page.ts      # Load function
│   └── api/
│       └── users/
│           └── +server.ts    # API endpoint
├── lib/
│   ├── components/
│   ├── stores/
│   └── utils/
└── app.html
```

### Load Functions

```typescript
// routes/blog/[slug]/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, fetch }) => {
  const response = await fetch(`/api/posts/${params.slug}`);

  if (!response.ok) {
    throw error(404, 'Post not found');
  }

  const post = await response.json();

  return {
    post,
    meta: {
      title: post.title,
      description: post.excerpt,
    },
  };
};

// In +page.svelte
<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<article>
  <h1>{data.post.title}</h1>
  {@html data.post.content}
</article>
```

### Server Load (Database Access)

```typescript
// routes/dashboard/+page.server.ts
import type { PageServerLoad } from './$types';
import { db } from '$lib/server/database';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.user) {
    throw redirect(303, '/login');
  }

  const [stats, recentOrders] = await Promise.all([
    db.stats.get(locals.user.id),
    db.orders.findRecent(locals.user.id, 10),
  ]);

  return {
    stats,
    recentOrders,
  };
};
```

### Form Actions

```typescript
// routes/login/+page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { auth } from '$lib/server/auth';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData();
    const email = formData.get('email') as string;
    const password = formData.get('password') as string;

    // Validation
    if (!email || !password) {
      return fail(400, {
        email,
        error: 'Email and password required'
      });
    }

    try {
      const session = await auth.login(email, password);
      cookies.set('session', session.id, { path: '/' });
    } catch {
      return fail(401, {
        email,
        error: 'Invalid credentials'
      });
    }

    throw redirect(303, '/dashboard');
  },
};
```

```svelte
<!-- routes/login/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  let { form }: { form: ActionData } = $props();
</script>

<form method="POST" use:enhance>
  <input
    name="email"
    type="email"
    value={form?.email ?? ''}
    required
  />
  <input name="password" type="password" required />

  {#if form?.error}
    <p class="error">{form.error}</p>
  {/if}

  <button type="submit">Log In</button>
</form>
```

### API Routes

```typescript
// routes/api/users/+server.ts
import type { RequestHandler } from './$types';
import { json, error } from '@sveltejs/kit';
import { db } from '$lib/server/database';

export const GET: RequestHandler = async ({ url }) => {
  const page = Number(url.searchParams.get('page') ?? '1');
  const limit = Number(url.searchParams.get('limit') ?? '10');

  const users = await db.users.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return json({ users, page, limit });
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();

  if (!body.email || !body.name) {
    throw error(400, 'Email and name required');
  }

  const user = await db.users.create(body);

  return json(user, { status: 201 });
};
```

## Hooks

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { auth } from '$lib/server/auth';

export const handle: Handle = async ({ event, resolve }) => {
  // Get session from cookie
  const sessionId = event.cookies.get('session');

  if (sessionId) {
    const user = await auth.validateSession(sessionId);
    event.locals.user = user;
  }

  // Add security headers
  const response = await resolve(event);
  response.headers.set('X-Frame-Options', 'DENY');

  return response;
};
```

## Best Practices

| Pattern | Implementation |
|---------|----------------|
| **State** | Use `$state()` for reactive values |
| **Derived** | Use `$derived()` for computed values |
| **Effects** | Use `$effect()` sparingly, prefer derived |
| **Server data** | Use `+page.server.ts` for DB/auth |
| **Client data** | Use `+page.ts` for public APIs |
| **Forms** | Use form actions with `use:enhance` |

## When to Use

- Building full-stack web applications
- Projects requiring fast performance
- Applications needing SSR/SSG
- Teams preferring minimal boilerplate
- Interactive data-driven dashboards

## Notes

- Svelte 5 runes are the recommended approach
- SvelteKit provides file-based routing
- Server-side code is automatically separated
- Forms work without JavaScript enabled
