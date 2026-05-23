---
name: svelte-5
description: Svelte 5 patterns, gotchas, and solutions. Use when working with Svelte 5/SvelteKit, especially for reactivity, SSR, and state management issues.
---

# Svelte 5 Patterns and Gotchas

Svelte 5 introduces runes (`$state`, `$derived`, `$effect`) as the primary reactivity system. This skill documents patterns and solutions for common issues.

## Quick Reference

| Scenario | Use This | Not This |
|----------|----------|----------|
| Component state | `let x = $state(value)` | `let x = writable(value)` |
| Derived values | `let y = $derived(x * 2)` | `$: y = x * 2` |
| Side effects | `$effect(() => { ... })` | `$: { ... }` |
| Shared state | Context API or `.svelte.ts` modules | Module-level writable stores |
| Client-only rendering | `export const ssr = false` in +page.ts | `{#if browser}` wrappers |

## SSR + Hydration Issues

### Problem: Conditional Blocks Don't Re-render After Hydration

**Symptoms:**
- State updates correctly (confirmed via console.log)
- But `{#if condition}` blocks don't show/hide
- Works in dev, breaks in production build with adapter-static

**Root Cause:**
With `adapter-static`, pages are pre-rendered with initial state. After hydration, writable stores from `svelte/store` may not properly reconnect their reactive subscriptions.

**Solutions (in order of preference):**

#### 1. Disable SSR for Interactive Pages (Simplest)

If your page is purely client-side interactive with no SEO requirements:

```typescript
// +page.ts
export const ssr = false;
```

This makes the page client-only, eliminating all hydration issues.

#### 2. Use $state Runes with Mounted Guard

If you need SSR for the page shell but have client-only interactive sections:

```svelte
<script lang="ts">
  import { onMount } from 'svelte';

  let detailOpen = $state(false);
  let selectedItem = $state<Item | null>(null);
  let mounted = $state(false);

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted && detailOpen && selectedItem}
  <!-- Renders only after hydration -->
{/if}
```

#### 3. Context API for Shared State

For state shared across components in SSR context:

```svelte
<!-- +layout.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';

  const panelState = $state({ open: false, item: null });
  setContext('panel', panelState);
</script>
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  const panel = getContext('panel');
</script>

{#if panel.open && panel.item}
  <!-- Works because context creates fresh state per request -->
{/if}
```

## Migrating from Stores to Runes

### Before (Svelte 4 / Legacy)

```svelte
<script>
  import { writable } from 'svelte/store';

  const count = writable(0);
  const doubled = derived(count, $c => $c * 2);

  function increment() {
    count.update(n => n + 1);
  }
</script>

<p>{$count} doubled is {$doubled}</p>
```

### After (Svelte 5)

```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);

  function increment() {
    count++;
  }
</script>

<p>{count} doubled is {doubled}</p>
```

**Key Changes:**
- `writable()` → `$state()`
- `derived()` → `$derived()`
- `$storeName` → `stateName` (no $ prefix needed)
- `.set()` / `.update()` → direct assignment

## State in .svelte.ts Modules

For shared reactive state across components:

```typescript
// lib/stores/panel.svelte.ts
import type { Item } from '$lib/types';

let _open = $state(false);
let _item = $state<Item | null>(null);

export const panelState = {
  get open() { return _open; },
  set open(v: boolean) { _open = v; },

  get item() { return _item; },
  set item(v: Item | null) { _item = v; },

  close() {
    _open = false;
    _item = null;
  }
};
```

Usage:
```svelte
<script>
  import { panelState } from '$lib/stores/panel.svelte';
</script>

{#if panelState.open && panelState.item}
  <Panel item={panelState.item} />
{/if}
```

## $effect Gotchas

### Effects Don't Run During SSR

```svelte
<script>
  $effect(() => {
    // This only runs on client, never during SSR
    console.log('This won\'t appear in server logs');
  });
</script>
```

### Cleanup Pattern

```svelte
<script>
  $effect(() => {
    const subscription = subscribe();

    return () => {
      subscription.unsubscribe();
    };
  });
</script>
```

### Avoid Infinite Loops

```svelte
<script>
  let count = $state(0);

  // BAD - infinite loop
  $effect(() => {
    count = count + 1;
  });

  // GOOD - explicit dependencies
  $effect(() => {
    console.log('Count changed:', count);
  });
</script>
```

## bits-ui Component Patterns

### Migrating `let:builder` to Child Snippets

In Svelte 4, bits-ui components used `let:builder` to expose builder props for composition:

```svelte
<!-- Svelte 4 - BROKEN in Svelte 5 -->
<Tooltip.Trigger asChild let:builder>
  <Button builders={[builder]} disabled={true}>
    Hover me
  </Button>
</Tooltip.Trigger>
```

In Svelte 5, this pattern causes `invalid_default_snippet` errors because `let:` directives conflict with default snippet rendering.

**Fix: Use the `child` snippet pattern:**

```svelte
<!-- Svelte 5 - Correct -->
<Tooltip.Trigger>
  {#snippet child({ props })}
    <Button {...props} disabled={true}>
      Hover me
    </Button>
  {/snippet}
</Tooltip.Trigger>
```

**Key differences:**
- Remove `asChild` attribute
- Remove `let:builder` directive
- Use `{#snippet child({ props })}` instead
- Spread `{...props}` onto the child element instead of `builders={[builder]}`

This applies to all bits-ui trigger components:
- `Tooltip.Trigger`
- `Dialog.Trigger`
- `Popover.Trigger`
- `DropdownMenu.Trigger`
- etc.

### Why This Breaks

The bits-ui trigger components support two rendering modes:
1. **Default children**: `{@render children?.()}` - renders child content directly
2. **Child snippet**: `{@render child({ props })}` - passes builder props to child

Using `let:builder` expects mode 2 but the component tries to render mode 1, causing Svelte 5 to throw `invalid_default_snippet`.

## Common Mistakes

### 1. Mixing Stores and Runes

Don't mix `writable()` stores with `$state` in the same component for related state. Pick one approach:

```svelte
<!-- BAD -->
<script>
  const open = writable(false);  // Store
  let item = $state(null);       // Rune
</script>

<!-- GOOD -->
<script>
  let open = $state(false);
  let item = $state(null);
</script>
```

### 2. Using $ Prefix with $state

```svelte
<!-- BAD -->
<script>
  let count = $state(0);
</script>
<p>{$count}</p>  <!-- Wrong! -->

<!-- GOOD -->
<script>
  let count = $state(0);
</script>
<p>{count}</p>
```

### 3. Module-Level $state in Regular .ts Files

`$state` only works in `.svelte` and `.svelte.ts` files:

```typescript
// lib/state.ts - BAD
let count = $state(0);  // Won't work!

// lib/state.svelte.ts - GOOD
let count = $state(0);  // Works
```

## When to Use SSR vs Client-Only

| Use SSR (`ssr: true`) | Use Client-Only (`ssr: false`) |
|----------------------|-------------------------------|
| Content pages (SEO matters) | Dashboards |
| Landing pages | Admin panels |
| Blog posts | Interactive tools |
| Static marketing | Real-time data views |

## References

- [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide)
- [SvelteKit State Management](https://svelte.dev/docs/kit/state-management)
- [Svelte $state](https://svelte.dev/docs/svelte/$state)
- [Svelte $effect](https://svelte.dev/docs/svelte/$effect)
- [SvelteKit Page Options](https://svelte.dev/docs/kit/page-options)
