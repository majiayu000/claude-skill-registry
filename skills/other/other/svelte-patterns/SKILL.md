---
name: svelte-patterns
description: "Use when building Svelte 5 or SvelteKit applications. Covers runes, SvelteKit routing and SSR, component patterns, stores, transitions, and migration from Svelte 4."
---

# Svelte Patterns

## Svelte 5 Runes

Runes replace Svelte 4's `let` reactivity and `$:` labels with explicit primitives.

```svelte
<script lang="ts">
  // Reactive state
  let count = $state(0)
  let items = $state<string[]>([])

  // Derived values (replaces $: derived = ...)
  let doubled = $derived(count * 2)
  let total = $derived.by(() => {
    return items.reduce((sum, item) => sum + item.length, 0)
  })

  // Side effects (replaces $: { ... })
  $effect(() => {
    console.log(`count is ${count}`)
    return () => console.log('cleanup')  // cleanup function
  })
</script>

<button onclick={() => count++}>{count} (doubled: {doubled})</button>
```

## Component Props (Svelte 5)

`$props()` replaces `export let`. Use `Snippet` type for children (replaces `<slot>`). Named snippets take typed args.

## SvelteKit Routing

```
src/routes/
  +page.svelte          # /
  +layout.svelte        # shared layout
  +page.server.ts       # server load function
  blog/
    +page.svelte        # /blog
    [slug]/
      +page.svelte      # /blog/:slug
      +page.ts           # universal load
      +page.server.ts    # server-only load
  api/
    posts/
      +server.ts         # API route: GET, POST, etc.
```

### Load Functions

Server load (`+page.server.ts`) has DB/secret access. Universal load (`+page.ts`) runs both sides. Return typed data props.

### Form Actions

Define named actions in `+page.server.ts`. Use `fail()` for validation errors, `throw redirect()` for redirects. Client-side `use:enhance` for progressive enhancement.

## Stores

Svelte 5 runes preferred. Stores (`writable`, `derived`) still useful for cross-component shared state. Access with `$` prefix.

## Transitions

Built-in `transition:fade`, `in:fly`, `out:slide`. Use `animate:flip` for list reordering within `{#each}`.

## Gotchas

- **Svelte 5 migration**: `let x = 0` is no longer reactive at top level -- must use `$state(0)`. `$:` labels are deprecated; use `$derived` and `$effect`
- **`$effect` vs `$derived`**: use `$derived` for computed values, `$effect` only for side effects. `$effect` does NOT return a value
- **Object/array reactivity**: `$state` uses proxies; direct property mutation works (`obj.key = val`), but reassigning nested arrays needs care: `items = [...items, newItem]` or mutate in place
- **Stores to runes**: Svelte 5 still supports stores but runes are preferred. `$state` replaces `writable` for component-local state; stores still useful for cross-component shared state
- **Hydration mismatch**: SvelteKit SSR means server/client must render identically. Guard browser APIs with `browser` from `$app/environment` or `onMount`
- **Form action gotcha**: `throw redirect()` (not `return redirect()`) -- redirect is implemented as a thrown response in SvelteKit
- **`use:enhance`**: without it, form submissions trigger full page reload. With it, SvelteKit progressively enhances to fetch

## Cross-References

- **frontend:form-patterns** -- advanced form validation and multi-step wizard patterns
- **frontend:react-state-management** -- compare Svelte stores/runes with React state solutions
