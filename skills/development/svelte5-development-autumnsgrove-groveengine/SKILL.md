---
name: svelte5-development
description: Build web applications with Svelte 5 runes, SvelteKit routing, form actions, and component patterns. Use when working with Svelte, SvelteKit, or building reactive web interfaces.
---

# Svelte 5 Development Skill

## When to Activate

Activate this skill when:
- Creating Svelte 5 components
- Working with SvelteKit routing
- Implementing runes ($state, $derived, $effect)
- Building forms with actions
- Setting up SvelteKit projects

## Quick Commands

```bash
npx sv create my-app      # Create SvelteKit project
cd my-app && pnpm install
pnpm dev               # Start dev server (localhost:5173)
pnpm build             # Build for production
```

## Runes Quick Reference

| Rune | Purpose | Example |
|------|---------|---------|
| `$state` | Reactive state | `let count = $state(0)` |
| `$derived` | Computed values | `let doubled = $derived(count * 2)` |
| `$effect` | Side effects | `$effect(() => console.log(count))` |
| `$props` | Component props | `let { name } = $props()` |
| `$bindable` | Two-way binding | `let { value = $bindable() } = $props()` |

## Reactive State ($state)

```svelte
<script>
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 30 });
  let items = $state(['apple', 'banana']);
</script>

<button onclick={() => count++}>
  Clicked {count} times
</button>

<button onclick={() => user.age++}>
  {user.name} is {user.age}
</button>
```

**Deep reactivity**: Objects and arrays update automatically on mutation.

## Computed Values ($derived)

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);

  // For complex computations
  let summary = $derived.by(() => {
    const total = items.length;
    const done = items.filter(i => i.done).length;
    return `${done}/${total}`;
  });
</script>
```

## Side Effects ($effect)

```svelte
<script>
  let count = $state(0);

  $effect(() => {
    console.log(`Count is ${count}`);
    document.title = `Count: ${count}`;

    // Cleanup function
    return () => {
      console.log('Cleanup');
    };
  });
</script>
```

## Component Props ($props)

```svelte
<!-- Button.svelte -->
<script>
  let { label, disabled = false, onclick } = $props();
</script>

<button {disabled} {onclick}>{label}</button>
```

### TypeScript Props

```svelte
<script lang="ts">
  interface Props {
    label: string;
    disabled?: boolean;
    onclick?: () => void;
  }

  let { label, disabled = false, onclick }: Props = $props();
</script>
```

## SvelteKit File Conventions

| File | Purpose |
|------|---------|
| `+page.svelte` | Page component |
| `+page.server.js` | Server-only load/actions |
| `+layout.svelte` | Shared layout |
| `+server.js` | API endpoints |
| `+error.svelte` | Error boundary |

## Data Loading

```javascript
// src/routes/posts/+page.server.js
export async function load({ fetch }) {
  const response = await fetch('/api/posts');
  return { posts: await response.json() };
}
```

```svelte
<!-- src/routes/posts/+page.svelte -->
<script>
  let { data } = $props();
</script>

{#each data.posts as post}
  <article>
    <h2>{post.title}</h2>
  </article>
{/each}
```

## Form Actions

```javascript
// src/routes/login/+page.server.js
import { fail, redirect } from '@sveltejs/kit';

export const actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = data.get('email');

    if (!email) {
      return fail(400, { missing: true });
    }

    cookies.set('session', token, { path: '/' });
    throw redirect(303, '/dashboard');
  }
};
```

```svelte
<!-- +page.svelte -->
<script>
  import { enhance } from '$app/forms';
  let { form } = $props();
</script>

<form method="POST" use:enhance>
  <input name="email" value={form?.email ?? ''} />
  {#if form?.missing}
    <p class="error">Email required</p>
  {/if}
  <button>Submit</button>
</form>
```

## API Routes

```javascript
// src/routes/api/posts/+server.js
import { json } from '@sveltejs/kit';

export async function GET({ url }) {
  const posts = await getPosts();
  return json(posts);
}

export async function POST({ request }) {
  const data = await request.json();
  const post = await createPost(data);
  return json(post, { status: 201 });
}
```

## Common Pitfalls

### Destructuring Breaks Reactivity
```javascript
// ❌ Bad
let { count } = $state({ count: 0 });

// ✅ Good
let state = $state({ count: 0 });
state.count++;
```

### Missing Keys in Each
```svelte
<!-- ❌ Bad -->
{#each items as item}

<!-- ✅ Good -->
{#each items as item (item.id)}
```

### Use Progressive Enhancement
```svelte
<script>
  import { enhance } from '$app/forms';
</script>

<form method="POST" use:enhance>
```

## Project Structure

```
src/
├── lib/
│   ├── components/
│   └── server/
├── routes/
│   ├── +layout.svelte
│   ├── +page.svelte
│   └── api/
├── app.html
└── hooks.server.js
```

## Related Resources

See `AgentUsage/svelte5_guide.md` for complete documentation including:
- Advanced rune patterns
- Snippets for reusable markup
- Performance optimization
- TypeScript integration
