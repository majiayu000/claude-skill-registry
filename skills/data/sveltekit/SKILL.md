---
name: sveltekit
description: Builds applications with SvelteKit including routing, load functions, form actions, hooks, and adapters. Use when creating Svelte applications with SSR, building full-stack apps, or needing file-based routing with Svelte.
---

# SvelteKit

The official application framework for Svelte with routing, SSR, and more.

## Quick Start

**Create project:**
```bash
npx sv create my-app
cd my-app
npm install
npm run dev
```

## Project Structure

```
my-app/
  src/
    routes/           # File-based routing
      +page.svelte    # Page components
      +page.server.ts # Server load functions
      +layout.svelte  # Layouts
    lib/              # Shared code ($lib alias)
    app.html          # HTML template
    hooks.server.ts   # Server hooks
  static/             # Static assets
  svelte.config.js    # SvelteKit config
  vite.config.ts      # Vite config
```

## Routing

### Basic Pages

```svelte
<!-- src/routes/+page.svelte -->
<h1>Home Page</h1>
<a href="/about">About</a>
```

### Dynamic Routes

```svelte
<!-- src/routes/users/[id]/+page.svelte -->
<script lang="ts">
  let { data } = $props();
</script>

<h1>User: {data.user.name}</h1>
```

```typescript
// src/routes/users/[id]/+page.server.ts
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
  const user = await getUser(params.id);
  return { user };
};
```

### Optional Parameters

```
src/routes/[[lang]]/about/+page.svelte
// Matches /about and /en/about
```

### Rest Parameters

```
src/routes/files/[...path]/+page.svelte
// Matches /files/a/b/c -> params.path = 'a/b/c'
```

### Route Groups

```
src/routes/
  (auth)/
    login/+page.svelte
    register/+page.svelte
  (app)/
    dashboard/+page.svelte
```

## Load Functions

### Server Load

```typescript
// src/routes/posts/+page.server.ts
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ params, locals, fetch }) => {
  const response = await fetch('/api/posts');

  if (!response.ok) {
    throw error(404, 'Posts not found');
  }

  const posts = await response.json();
  return { posts };
};
```

### Universal Load

```typescript
// src/routes/posts/+page.ts
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, data }) => {
  // Runs on server and client
  const response = await fetch('/api/posts');
  return { posts: await response.json() };
};
```

### Layout Load

```typescript
// src/routes/+layout.server.ts
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  return {
    user: locals.user,
  };
};
```

### Using Data in Components

```svelte
<!-- src/routes/posts/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<h1>Posts</h1>
{#each data.posts as post}
  <article>
    <h2>{post.title}</h2>
    <p>{post.excerpt}</p>
  </article>
{/each}
```

## Form Actions

### Basic Action

```typescript
// src/routes/login/+page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email') as string;
    const password = data.get('password') as string;

    const user = await login(email, password);

    if (!user) {
      return fail(400, { email, error: 'Invalid credentials' });
    }

    cookies.set('session', user.token, { path: '/' });
    throw redirect(303, '/dashboard');
  },
};
```

```svelte
<!-- src/routes/login/+page.svelte -->
<script lang="ts">
  import type { ActionData } from './$types';

  let { form }: { form: ActionData } = $props();
</script>

<form method="POST">
  <input name="email" value={form?.email ?? ''} />
  <input name="password" type="password" />
  <button>Login</button>

  {#if form?.error}
    <p class="error">{form.error}</p>
  {/if}
</form>
```

### Named Actions

```typescript
// src/routes/todo/+page.server.ts
export const actions: Actions = {
  create: async ({ request }) => {
    const data = await request.formData();
    await createTodo(data.get('text'));
  },
  delete: async ({ request }) => {
    const data = await request.formData();
    await deleteTodo(data.get('id'));
  },
};
```

```svelte
<form method="POST" action="?/create">
  <input name="text" />
  <button>Add</button>
</form>

<form method="POST" action="?/delete">
  <input type="hidden" name="id" value={todo.id} />
  <button>Delete</button>
</form>
```

### Progressive Enhancement

```svelte
<script lang="ts">
  import { enhance } from '$app/forms';
</script>

<form method="POST" use:enhance>
  <!-- Form content -->
</form>

<!-- Custom enhance -->
<form
  method="POST"
  use:enhance={() => {
    return async ({ result, update }) => {
      if (result.type === 'success') {
        // Handle success
      }
      await update();
    };
  }}
>
```

## Layouts

### Basic Layout

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from './$types';
  import { Snippet } from 'svelte';

  let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<nav>
  <a href="/">Home</a>
  {#if data.user}
    <span>{data.user.name}</span>
  {/if}
</nav>

<main>
  {@render children()}
</main>

<footer>Footer</footer>
```

### Nested Layouts

```
src/routes/
  +layout.svelte          # Root layout
  (app)/
    +layout.svelte        # App layout
    dashboard/+page.svelte
```

### Reset Layout

```svelte
<!-- src/routes/special/+page@.svelte -->
<!-- Uses root layout, skipping intermediate layouts -->
```

## Hooks

### Server Hooks

```typescript
// src/hooks.server.ts
import type { Handle, HandleFetch } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Run before every request
  const session = event.cookies.get('session');

  if (session) {
    event.locals.user = await getUser(session);
  }

  const response = await resolve(event);
  return response;
};

export const handleFetch: HandleFetch = async ({ request, fetch }) => {
  // Intercept fetch calls
  return fetch(request);
};

export const handleError = async ({ error, event }) => {
  console.error(error);
  return {
    message: 'Internal Error',
  };
};
```

### Sequence Multiple Hooks

```typescript
import { sequence } from '@sveltejs/kit/hooks';

export const handle = sequence(
  authHandle,
  loggingHandle,
  corsHandle
);
```

## API Routes

```typescript
// src/routes/api/users/+server.ts
import type { RequestHandler } from './$types';
import { json, error } from '@sveltejs/kit';

export const GET: RequestHandler = async ({ url }) => {
  const limit = Number(url.searchParams.get('limit') ?? 10);
  const users = await getUsers(limit);
  return json(users);
};

export const POST: RequestHandler = async ({ request }) => {
  const data = await request.json();
  const user = await createUser(data);
  return json(user, { status: 201 });
};

export const DELETE: RequestHandler = async ({ params }) => {
  await deleteUser(params.id);
  return new Response(null, { status: 204 });
};
```

## Navigation

```svelte
<script lang="ts">
  import { goto, invalidate, invalidateAll } from '$app/navigation';
  import { page } from '$app/stores';

  async function navigate() {
    await goto('/dashboard');
  }

  async function refresh() {
    await invalidate('/api/data');
    // or invalidateAll() for all data
  }
</script>

<p>Current path: {$page.url.pathname}</p>
```

## Error Handling

### Error Pages

```svelte
<!-- src/routes/+error.svelte -->
<script lang="ts">
  import { page } from '$app/stores';
</script>

<h1>{$page.status}</h1>
<p>{$page.error?.message}</p>
```

### Throwing Errors

```typescript
import { error } from '@sveltejs/kit';

export const load = async ({ params }) => {
  const post = await getPost(params.id);

  if (!post) {
    throw error(404, {
      message: 'Post not found',
    });
  }

  return { post };
};
```

## Environment Variables

```typescript
// .env
PUBLIC_API_URL=https://api.example.com
DATABASE_URL=postgres://...

// Access in server code
import { DATABASE_URL } from '$env/static/private';
import { env } from '$env/dynamic/private';

// Access in client code
import { PUBLIC_API_URL } from '$env/static/public';
```

## Adapters

```javascript
// svelte.config.js
import adapter from '@sveltejs/adapter-auto';
// Or specific adapter:
// import adapter from '@sveltejs/adapter-node';
// import adapter from '@sveltejs/adapter-vercel';
// import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter(),
  },
};
```

### Static Adapter

```javascript
import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: '404.html',
    }),
    prerender: {
      entries: ['*'],
    },
  },
};
```

## Page Options

```typescript
// src/routes/+page.ts
export const prerender = true;  // Static generation
export const ssr = false;       // Client-only
export const csr = true;        // Enable client JS
```

## Best Practices

1. **Use form actions** - Progressive enhancement built-in
2. **Leverage load functions** - Data loading before render
3. **Use +server.ts for APIs** - Clean API separation
4. **Type everything** - Use generated types
5. **Choose right adapter** - Match deployment target

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| fetch in component | Move to load function |
| Not using $props | Use $props for Svelte 5 |
| Missing $types imports | Generate types with `npm run check` |
| Wrong action method | Forms need method="POST" |
| Forgetting await | await goto() and invalidate() |

## Reference Files

- [references/routing.md](references/routing.md) - Advanced routing
- [references/forms.md](references/forms.md) - Form patterns
- [references/deployment.md](references/deployment.md) - Deployment guides
