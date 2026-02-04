---
name: svelte
description: Builds UIs with Svelte 5 including runes, components, reactivity, and stores. Use when creating Svelte applications, building reactive interfaces, or working with compile-time frameworks.
---

# Svelte 5

A framework that compiles components to efficient JavaScript at build time.

## Quick Start

**Create project:**
```bash
npx sv create my-app
cd my-app
npm install
npm run dev
```

## Component Basics

```svelte
<script lang="ts">
  let count = $state(0);

  function increment() {
    count++;
  }
</script>

<button onclick={increment}>
  Count: {count}
</button>

<style>
  button {
    font-weight: bold;
  }
</style>
```

## Runes (Svelte 5)

### $state - Reactive State

```svelte
<script lang="ts">
  // Primitive state
  let count = $state(0);
  let name = $state('');

  // Object state (deeply reactive)
  let user = $state({
    name: 'John',
    email: 'john@example.com',
  });

  // Array state
  let items = $state<string[]>([]);

  function addItem(item: string) {
    items.push(item); // Mutations work!
  }
</script>

<p>{count}</p>
<p>{user.name}</p>
```

### $derived - Computed Values

```svelte
<script lang="ts">
  let count = $state(0);
  let items = $state([1, 2, 3]);

  // Simple derived
  let doubled = $derived(count * 2);

  // Complex derived
  let total = $derived(items.reduce((a, b) => a + b, 0));

  // Derived with function
  let expensive = $derived.by(() => {
    // Complex computation
    return items.filter(x => x > count).length;
  });
</script>

<p>Count: {count}, Doubled: {doubled}</p>
```

### $effect - Side Effects

```svelte
<script lang="ts">
  let count = $state(0);

  // Runs when dependencies change
  $effect(() => {
    console.log(`Count is now ${count}`);
  });

  // With cleanup
  $effect(() => {
    const interval = setInterval(() => count++, 1000);

    return () => {
      clearInterval(interval);
    };
  });

  // Pre-effect (runs before DOM update)
  $effect.pre(() => {
    console.log('Before DOM update');
  });
</script>
```

### $props - Component Props

```svelte
<!-- Button.svelte -->
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
    children: import('svelte').Snippet;
  }

  let { variant = 'primary', disabled = false, children }: Props = $props();
</script>

<button class={variant} {disabled}>
  {@render children()}
</button>
```

```svelte
<!-- Usage -->
<Button variant="primary">
  Click me
</Button>
```

### $bindable - Two-way Binding Props

```svelte
<!-- Input.svelte -->
<script lang="ts">
  let { value = $bindable('') }: { value: string } = $props();
</script>

<input bind:value />
```

```svelte
<!-- Usage -->
<script lang="ts">
  let name = $state('');
</script>

<Input bind:value={name} />
```

## Events

### DOM Events

```svelte
<script lang="ts">
  function handleClick(event: MouseEvent) {
    console.log('Clicked', event.target);
  }

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    console.log(target.value);
  }
</script>

<button onclick={handleClick}>Click</button>
<input oninput={handleInput} />

<!-- Inline handlers -->
<button onclick={() => count++}>Increment</button>

<!-- Modifiers -->
<form onsubmit|preventDefault={handleSubmit}>
  <button>Submit</button>
</form>
```

### Component Events (Callbacks)

```svelte
<!-- Child.svelte -->
<script lang="ts">
  let { onchange }: { onchange: (value: string) => void } = $props();
</script>

<input oninput={(e) => onchange(e.target.value)} />
```

```svelte
<!-- Parent.svelte -->
<script lang="ts">
  function handleChange(value: string) {
    console.log(value);
  }
</script>

<Child onchange={handleChange} />
```

## Control Flow

### Conditionals

```svelte
{#if condition}
  <p>True</p>
{:else if otherCondition}
  <p>Other</p>
{:else}
  <p>False</p>
{/if}
```

### Loops

```svelte
{#each items as item, index (item.id)}
  <li>{index}: {item.name}</li>
{:else}
  <p>No items</p>
{/each}
```

### Await

```svelte
{#await promise}
  <p>Loading...</p>
{:then data}
  <p>{data}</p>
{:catch error}
  <p>Error: {error.message}</p>
{/await}

<!-- Short form -->
{#await promise then data}
  <p>{data}</p>
{/await}
```

### Key Block

```svelte
{#key value}
  <!-- Recreates component when value changes -->
  <Component />
{/key}
```

## Snippets (Svelte 5)

```svelte
<script lang="ts">
  let items = $state(['a', 'b', 'c']);
</script>

{#snippet listItem(item: string, index: number)}
  <li>{index}: {item}</li>
{/snippet}

<ul>
  {#each items as item, i}
    {@render listItem(item, i)}
  {/each}
</ul>
```

### Passing Snippets as Props

```svelte
<!-- List.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    items: string[];
    row: Snippet<[string, number]>;
  }

  let { items, row }: Props = $props();
</script>

<ul>
  {#each items as item, i}
    {@render row(item, i)}
  {/each}
</ul>
```

```svelte
<!-- Usage -->
<List {items}>
  {#snippet row(item, index)}
    <li class="custom">{index}: {item}</li>
  {/snippet}
</List>
```

## Bindings

### Form Bindings

```svelte
<script lang="ts">
  let text = $state('');
  let checked = $state(false);
  let selected = $state('');
  let group = $state<string[]>([]);
</script>

<input bind:value={text} />
<input type="checkbox" bind:checked />
<select bind:value={selected}>
  <option value="a">A</option>
  <option value="b">B</option>
</select>

<!-- Checkbox group -->
<input type="checkbox" bind:group value="one" />
<input type="checkbox" bind:group value="two" />

<!-- Radio group -->
<input type="radio" bind:group={selected} value="a" />
<input type="radio" bind:group={selected} value="b" />
```

### Element Bindings

```svelte
<script lang="ts">
  let div: HTMLDivElement;
  let width = $state(0);
  let height = $state(0);
</script>

<div bind:this={div} bind:clientWidth={width} bind:clientHeight={height}>
  {width} x {height}
</div>
```

## Lifecycle

```svelte
<script lang="ts">
  import { onMount, onDestroy, beforeUpdate, afterUpdate } from 'svelte';

  onMount(() => {
    console.log('Mounted');

    return () => {
      console.log('Cleanup on unmount');
    };
  });

  onDestroy(() => {
    console.log('Destroyed');
  });

  beforeUpdate(() => {
    console.log('Before update');
  });

  afterUpdate(() => {
    console.log('After update');
  });
</script>
```

## Stores

```typescript
// stores/count.ts
import { writable, derived, readable } from 'svelte/store';

// Writable store
export const count = writable(0);

// Derived store
export const doubled = derived(count, ($count) => $count * 2);

// Readable store
export const time = readable(new Date(), (set) => {
  const interval = setInterval(() => set(new Date()), 1000);
  return () => clearInterval(interval);
});

// Custom store
function createCounter() {
  const { subscribe, set, update } = writable(0);

  return {
    subscribe,
    increment: () => update((n) => n + 1),
    decrement: () => update((n) => n - 1),
    reset: () => set(0),
  };
}

export const counter = createCounter();
```

```svelte
<script lang="ts">
  import { count, doubled, counter } from './stores/count';
</script>

<!-- Auto-subscribe with $ prefix -->
<p>Count: {$count}</p>
<p>Doubled: {$doubled}</p>

<button onclick={() => $count++}>Increment</button>
<button onclick={counter.increment}>Counter++</button>
```

## Context

```svelte
<!-- Parent.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';

  setContext('theme', {
    color: 'dark',
    toggle: () => { /* ... */ },
  });
</script>
```

```svelte
<!-- Child.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';

  interface ThemeContext {
    color: string;
    toggle: () => void;
  }

  const { color, toggle } = getContext<ThemeContext>('theme');
</script>
```

## Actions

```typescript
// actions/clickOutside.ts
export function clickOutside(node: HTMLElement, callback: () => void) {
  function handleClick(event: MouseEvent) {
    if (!node.contains(event.target as Node)) {
      callback();
    }
  }

  document.addEventListener('click', handleClick, true);

  return {
    destroy() {
      document.removeEventListener('click', handleClick, true);
    },
  };
}
```

```svelte
<script lang="ts">
  import { clickOutside } from './actions/clickOutside';

  let open = $state(false);
</script>

{#if open}
  <div use:clickOutside={() => open = false}>
    Dropdown content
  </div>
{/if}
```

## Transitions

```svelte
<script lang="ts">
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  let visible = $state(true);
</script>

{#if visible}
  <div transition:fade={{ duration: 300 }}>
    Fades in and out
  </div>

  <div in:fly={{ y: 200 }} out:fade>
    Different in/out
  </div>

  <div transition:slide={{ duration: 500, easing: quintOut }}>
    Slides
  </div>
{/if}
```

## Class and Style

```svelte
<script lang="ts">
  let active = $state(false);
  let color = $state('red');
</script>

<!-- Class shortcuts -->
<div class:active>...</div>
<div class:active={isActive}>...</div>
<div class={active ? 'active' : ''}>...</div>

<!-- Style shortcuts -->
<div style:color>...</div>
<div style:color={color}>...</div>
<div style:--custom-property={value}>...</div>
```

## Best Practices

1. **Use runes** - $state, $derived, $effect for Svelte 5
2. **Extract logic** - Use stores or modules for shared state
3. **Type props** - Use TypeScript interfaces
4. **Use actions** - Reusable DOM behaviors
5. **Prefer snippets** - Over slots for typed templates

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using $: in Svelte 5 | Use $derived or $effect |
| Forgetting $state | Primitives need $state() |
| Wrong event syntax | Use onclick not on:click (Svelte 5) |
| Store without $ | Use $store for auto-subscribe |
| Missing key in each | Add (item.id) for keyed each |

## Reference Files

- [references/runes.md](references/runes.md) - Complete runes guide
- [references/stores.md](references/stores.md) - Store patterns
- [references/transitions.md](references/transitions.md) - Animation guide
