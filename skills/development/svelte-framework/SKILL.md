---
name: svelte-framework
description: "Master Svelte and SvelteKit for building reactive, high-performance web applications with compile-time optimization. Use for: creating reactive UIs, implementing SvelteKit applications, understanding Svelte 5 runes ($state, $derived, $effect), file-based routing, server-side rendering, building SPAs and hybrid apps, component development, state management, and optimizing performance with compiler-based reactivity."
---

# Svelte Framework

Build reactive, high-performance web applications with Svelte's compile-time approach and SvelteKit's full-stack framework.

## Overview

Svelte is a radical approach to building user interfaces that shifts work from the browser to compile time. Unlike frameworks that use a virtual DOM, Svelte compiles components into highly efficient JavaScript that surgically updates the DOM. SvelteKit builds on Svelte to provide a full-featured framework with routing, SSR, SSG, and API endpoints. Svelte 5 introduces "Runes" for a more explicit signal-based reactivity model.

## When to Use Svelte/SvelteKit

| Scenario | Reason | Key Feature |
|----------|--------|-------------|
| Performance-critical apps | No virtual DOM overhead | Compile-time optimization |
| Small bundle size requirements | Minimal runtime | Compiled output |
| Simple, readable code | Less boilerplate | Reactive by default |
| Full-stack applications | Built-in SSR and API routes | SvelteKit framework |
| Static sites | Pre-rendering support | SSG capabilities |
| Progressive web apps | Service worker integration | SvelteKit adapters |
| Real-time applications | Efficient reactivity | Signal-based updates |

## Core Concepts

### Reactivity Model

Svelte's reactivity is based on **assignments**. When you assign a value to a variable, Svelte automatically updates the DOM.

**Basic Reactivity:**
```svelte
<script>
  let count = 0
  
  function increment() {
    count += 1 // Assignment triggers update
  }
</script>

<button on:click={increment}>
  Count: {count}
</button>
```

**Reactive Declarations (Svelte 4 and earlier):**
```svelte
<script>
  let count = 0
  $: doubled = count * 2 // Re-runs when count changes
  $: console.log('Count is', count) // Side effect
</script>
```

### Svelte 5 Runes

Svelte 5 introduces **Runes** for more explicit reactivity:

**`$state`** — Declare reactive variables:
```svelte
<script>
  let count = $state(0)
  let user = $state({ name: 'John', age: 30 })
</script>
```

**`$derived`** — Computed values:
```svelte
<script>
  let numbers = $state([1, 2, 3, 4])
  let total = $derived(numbers.reduce((sum, n) => sum + n, 0))
</script>
```

**`$effect`** — Side effects:
```svelte
<script>
  let count = $state(0)
  
  $effect(() => {
    console.log('Count changed:', count)
  })
</script>
```

**`$props`** — Component props:
```svelte
<script>
  let { title, count = 0 } = $props()
</script>
```

**`$bindable`** — Two-way binding:
```svelte
<script>
  let { value = $bindable() } = $props()
</script>
```

## SvelteKit Features

### File-Based Routing

Routes are automatically created based on file structure:

```
src/routes/
  +page.svelte          # /
  about/
    +page.svelte        # /about
  blog/
    +page.svelte        # /blog
    [slug]/
      +page.svelte      # /blog/:slug
  api/
    users/
      +server.js        # API endpoint
```

### Data Loading

**`+page.js` or `+page.server.js`:**
```javascript
export const load = async ({ fetch, params }) => {
  const response = await fetch(`/api/posts/${params.slug}`)
  const post = await response.json()
  
  return {
    post
  }
}
```

**`+page.svelte`:**
```svelte
<script>
  export let data
</script>

<h1>{data.post.title}</h1>
<p>{data.post.content}</p>
```

### Layouts

**`+layout.svelte`** defines shared UI:
```svelte
<script>
  import Header from '$lib/Header.svelte'
  import Footer from '$lib/Footer.svelte'
</script>

<Header />
<slot /> <!-- Page content -->
<Footer />
```

### Server-Side Rendering (SSR)

SvelteKit renders pages on the server by default:
- Improved SEO
- Faster initial page load
- Progressive enhancement

**Disable SSR per page:**
```javascript
// +page.js
export const ssr = false
```

### API Routes

**`+server.js`:**
```javascript
import { json } from '@sveltejs/kit'

export async function GET({ url }) {
  const data = await fetchData()
  return json(data)
}

export async function POST({ request }) {
  const body = await request.json()
  // Process data
  return json({ success: true })
}
```

## Component Patterns

### Props and Events

**Parent Component:**
```svelte
<script>
  import Child from './Child.svelte'
  
  function handleEvent(event) {
    console.log('Received:', event.detail)
  }
</script>

<Child name="John" on:custom={handleEvent} />
```

**Child Component:**
```svelte
<script>
  import { createEventDispatcher } from 'svelte'
  
  export let name
  const dispatch = createEventDispatcher()
  
  function notify() {
    dispatch('custom', { message: 'Hello' })
  }
</script>

<button on:click={notify}>Notify Parent</button>
```

### Slots

```svelte
<!-- Card.svelte -->
<div class="card">
  <slot name="header" />
  <slot /> <!-- Default slot -->
  <slot name="footer" />
</div>

<!-- Usage -->
<Card>
  <h2 slot="header">Title</h2>
  <p>Content</p>
  <button slot="footer">Action</button>
</Card>
```

### Stores (State Management)

**Writable Store:**
```javascript
// stores.js
import { writable } from 'svelte/store'

export const count = writable(0)
```

**Usage:**
```svelte
<script>
  import { count } from './stores.js'
  
  function increment() {
    count.update(n => n + 1)
  }
</script>

<button on:click={increment}>
  Count: {$count}
</button>
```

**Derived Store:**
```javascript
import { derived } from 'svelte/store'

export const doubled = derived(count, $count => $count * 2)
```

**Custom Store:**
```javascript
function createCounter() {
  const { subscribe, set, update } = writable(0)
  
  return {
    subscribe,
    increment: () => update(n => n + 1),
    decrement: () => update(n => n - 1),
    reset: () => set(0)
  }
}

export const counter = createCounter()
```

## Reactivity Patterns

### Array and Object Updates

**Problem:** Mutations don't trigger reactivity:
```svelte
<script>
  let items = [1, 2, 3]
  
  function addItem() {
    items.push(4) // ❌ Won't trigger update
  }
</script>
```

**Solution:** Reassign the variable:
```svelte
<script>
  let items = [1, 2, 3]
  
  function addItem() {
    items = [...items, 4] // ✅ Triggers update
  }
</script>
```

### Reactive Statements

```svelte
<script>
  let firstName = 'John'
  let lastName = 'Doe'
  
  $: fullName = `${firstName} ${lastName}`
  $: console.log('Name changed:', fullName)
  
  $: if (fullName.length > 20) {
    console.log('Name is too long')
  }
</script>
```

## Performance Optimization

### Compile-Time Advantages

- **No virtual DOM**: Direct DOM manipulation
- **Smaller bundles**: Only ship what you use
- **Faster updates**: Surgical DOM updates
- **Static analysis**: Compiler optimizations

### Lazy Loading

```svelte
<script>
  let HeavyComponent
  
  async function loadComponent() {
    const module = await import('./HeavyComponent.svelte')
    HeavyComponent = module.default
  }
</script>

<button on:click={loadComponent}>Load</button>

{#if HeavyComponent}
  <svelte:component this={HeavyComponent} />
{/if}
```

### Immutable Data

```svelte
<svelte:options immutable={true} />

<script>
  export let data
</script>
```

Tells Svelte that data won't be mutated, enabling faster equality checks.

## Common Patterns

### Conditional Rendering

```svelte
{#if condition}
  <p>Condition is true</p>
{:else if otherCondition}
  <p>Other condition is true</p>
{:else}
  <p>All conditions are false</p>
{/if}
```

### Lists

```svelte
{#each items as item, index (item.id)}
  <div>{index}: {item.name}</div>
{:else}
  <p>No items</p>
{/each}
```

### Await Blocks

```svelte
{#await promise}
  <p>Loading...</p>
{:then data}
  <p>Data: {data}</p>
{:catch error}
  <p>Error: {error.message}</p>
{/await}
```

## Lifecycle Functions

```svelte
<script>
  import { onMount, onDestroy, beforeUpdate, afterUpdate } from 'svelte'
  
  onMount(() => {
    console.log('Component mounted')
    return () => console.log('Cleanup')
  })
  
  onDestroy(() => {
    console.log('Component destroyed')
  })
  
  beforeUpdate(() => {
    console.log('Before DOM update')
  })
  
  afterUpdate(() => {
    console.log('After DOM update')
  })
</script>
```

## Actions (Custom Directives)

```svelte
<script>
  function tooltip(node, text) {
    const tooltip = document.createElement('div')
    tooltip.textContent = text
    
    function handleMouseEnter() {
      document.body.appendChild(tooltip)
    }
    
    function handleMouseLeave() {
      tooltip.remove()
    }
    
    node.addEventListener('mouseenter', handleMouseEnter)
    node.addEventListener('mouseleave', handleMouseLeave)
    
    return {
      destroy() {
        node.removeEventListener('mouseenter', handleMouseEnter)
        node.removeEventListener('mouseleave', handleMouseLeave)
      }
    }
  }
</script>

<button use:tooltip="Click me">Hover</button>
```

## Deployment

SvelteKit supports multiple adapters:

- **`@sveltejs/adapter-auto`**: Auto-detect platform
- **`@sveltejs/adapter-node`**: Node.js server
- **`@sveltejs/adapter-static`**: Static site generation
- **`@sveltejs/adapter-vercel`**: Vercel
- **`@sveltejs/adapter-netlify`**: Netlify
- **`@sveltejs/adapter-cloudflare`**: Cloudflare Workers

## Common Pitfalls

1. **Forgetting to reassign**: Mutations don't trigger reactivity
2. **Reactive statement order**: `$:` statements run in order
3. **Component key**: Use `{#key}` to force re-creation
4. **Store subscriptions**: Auto-unsubscribe with `$` prefix
5. **SSR compatibility**: Avoid browser-only APIs in SSR context

## Using the Reference Files

### When to Read Each Reference

**`/references/sveltekit-routing.md`** — Read when implementing complex routing, nested layouts, route parameters, or API endpoints.

**`/references/reactivity-patterns.md`** — Read when debugging reactivity issues, working with complex state, or migrating from Svelte 4 to Svelte 5 runes.

**`/references/stores-state-management.md`** — Read when implementing global state, creating custom stores, or managing complex application state.
