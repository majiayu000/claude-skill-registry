---
name: writing-svelte5
description: Svelte 5 syntax reference. Use when writing ANY Svelte component. Svelte 5 uses runes ($state, $derived, $effect, $props) instead of Svelte 4 patterns. Training data is heavily Svelte 4—this skill prevents outdated syntax.
---

# Svelte 5 Syntax

Always use Svelte 5 runes. Never use Svelte 4 patterns.

## Svelte 4 → Svelte 5

| Svelte 4 ❌                    | Svelte 5 ✅                                            |
| ------------------------------ | ------------------------------------------------------ |
| `export let foo`               | `let { foo } = $props()`                               |
| `export let foo = 'default'`   | `let { foo = 'default' } = $props()`                   |
| `$: doubled = x * 2`           | `let doubled = $derived(x * 2)`                        |
| `$: { sideEffect() }`          | `$effect(() => { sideEffect() })`                      |
| `on:click={handler}`           | `onclick={handler}`                                    |
| `on:input={handler}`           | `oninput={handler}`                                    |
| `on:click\|preventDefault={h}` | `onclick={e => { e.preventDefault(); h(e) }}`          |
| `<slot />`                     | `{@render children()}`                                 |
| `<slot name="x" />`            | `{@render x?.()}`                                      |
| `$$props`                      | Use `$props()` with rest: `let { ...rest } = $props()` |
| `$$restProps`                  | `let { known, ...rest } = $props()`                    |
| `createEventDispatcher()`      | Pass callback props: `let { onchange } = $props()`     |

## Stores → Runes

| Svelte 4 ❌                               | Svelte 5 ✅             |
| ----------------------------------------- | ----------------------- |
| `import { writable } from 'svelte/store'` | Remove import           |
| `const count = writable(0)`               | `let count = $state(0)` |
| `$count` (auto-subscribe)                 | `count` (direct access) |
| `count.set(1)`                            | `count = 1`             |
| `count.update(n => n + 1)`                | `count += 1`            |

## Quick Reference

```svelte
<script>
  // Props (with defaults and rest)
  let { required, optional = 'default', ...rest } = $props();

  // Two-way bindable prop
  let { value = $bindable() } = $props();

  // Reactive state
  let count = $state(0);
  let items = $state([]);      // arrays are deeply reactive
  let user = $state({ name: '' }); // objects too

  // Derived values
  let doubled = $derived(count * 2);
  let complex = $derived.by(() => {
    // multi-line logic here
    return expensiveCalc(count);
  });

  // Side effects
  $effect(() => {
    console.log(count);
    return () => cleanup(); // optional cleanup
  });
</script>

<!-- Events: native names, no colon -->
<button onclick={() => count++}>Click</button>
<input oninput={e => value = e.target.value} />

<!-- Render snippets (replaces slots) -->
{@render children?.()}
```

## Snippets (Replace Slots)

```svelte
<!-- Parent passes snippets -->
<Dialog>
  {#snippet header()}
    <h1>Title</h1>
  {/snippet}

  {#snippet footer(close)}
    <button onclick={close}>Done</button>
  {/snippet}
</Dialog>

<!-- Child renders them -->
<script>
  let { header, footer, children } = $props();
</script>
{@render header?.()}
{@render children?.()}
{@render footer?.(() => open = false)}
```

## References

Load these when needed:

- **[references/typescript.md](references/typescript.md)** — Typing props, state, derived, snippets, events, context
- **[references/patterns.md](references/patterns.md)** — Context API, controlled inputs, forwarding props, async data, debouncing
- **[references/gotchas.md](references/gotchas.md)** — Reactivity edge cases, effect pitfalls, binding quirks
