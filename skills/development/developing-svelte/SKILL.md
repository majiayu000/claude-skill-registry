---
name: developing-svelte
description: Use when working with .svelte files, SvelteKit projects, or Svelte reactivity. Covers component structure, stores, routing, Svelte 5 runes, and testing patterns.
---

# Svelte Development

Apply these patterns when working with Svelte components and SvelteKit applications.

## Component Structure

```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import Component from './Component.svelte';

  export let propName: string;
  export let optionalProp: number = 0;

  let count = 0;

  $: doubled = count * 2;

  function increment() {
    count += 1;
  }

  onMount(() => {
    return () => { /* cleanup */ };
  });
</script>

<div class="container">
  <h1>{propName}</h1>
  <button on:click={increment}>Count: {count}</button>
</div>

<style>
  .container { padding: 1rem; }
</style>
```

## Reactivity

```svelte
<script>
  let count = 0;
  $: doubled = count * 2;
  $: if (count > 10) alert('High count!');
</script>
```

### Store Subscriptions

```svelte
<script>
  import { writable, derived } from 'svelte/store';

  const count = writable(0);
  const doubled = derived(count, $count => $count * 2);

  function increment() {
    $count += 1;
  }
</script>

<p>Count: {$count}, Doubled: {$doubled}</p>
```

## Stores

### Writable Store

```typescript
import { writable } from 'svelte/store';

function createCounter() {
  const { subscribe, set, update } = writable(0);
  return {
    subscribe,
    increment: () => update(n => n + 1),
    reset: () => set(0)
  };
}

export const counter = createCounter();
```

### Derived Store

```typescript
import { derived } from 'svelte/store';
import { items } from './items';

export const totalPrice = derived(items, $items =>
  $items.reduce((sum, item) => sum + item.price, 0)
);
```

### Context vs Stores

Use stores for state shared across unrelated components. Use context for state scoped to a component tree.

```svelte
<script>
  import { setContext, getContext } from 'svelte';
  setContext('theme', { color: 'dark' });
  const theme = getContext('theme');
</script>
```

## SvelteKit

### File-based Routing

```
src/routes/
├── +page.svelte           # /
├── +layout.svelte
├── about/+page.svelte     # /about
├── blog/[slug]/+page.svelte  # /blog/:slug
└── api/users/+server.ts   # /api/users
```

### Page Load

```typescript
// +page.server.ts
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
  const res = await fetch(`/api/posts/${params.slug}`);
  return { post: await res.json() };
};
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';
  export let data: PageData;
</script>

<h1>{data.post.title}</h1>
```

### Form Actions

```typescript
// +page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request }) => {
    const data = await request.formData();
    const email = data.get('email');
    if (!email) return fail(400, { email, missing: true });
    throw redirect(303, '/success');
  }
};
```

```svelte
<script>
  import { enhance } from '$app/forms';
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" />
  <button>Submit</button>
</form>
```

## Svelte 5 Runes

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);

  $effect(() => {
    console.log('count changed:', count);
  });

  let { name, value = 0 }: { name: string; value?: number } = $props();
</script>
```

| Svelte 4 | Svelte 5 |
|----------|----------|
| `let count = 0` | `let count = $state(0)` |
| `$: doubled = count * 2` | `let doubled = $derived(count * 2)` |
| `$: { ... }` | `$effect(() => { ... })` |
| `export let prop` | `let { prop } = $props()` |

## Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect } from 'vitest';
import Counter from './Counter.svelte';

describe('Counter', () => {
  it('increments count on click', async () => {
    render(Counter);
    const button = screen.getByRole('button');
    expect(button).toHaveTextContent('Count: 0');
    await fireEvent.click(button);
    expect(button).toHaveTextContent('Count: 1');
  });
});
```

## Requirements

1. Keep components small; split large ones
2. Use TypeScript with `lang="ts"`
3. Prefer `$:` over `onMount` for derived state
4. Use `{#each items as item (item.id)}` with keys
5. Use scoped component styles
6. Use `use:enhance` for progressive form enhancement
7. Colocate load functions with pages
