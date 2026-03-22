---
name: web-framework-svelte
description: Svelte 5 Runes reactivity - $state, $derived, $effect, $props, $bindable, components, snippets, event handling, context API
---

# Svelte 5 Patterns

> **Quick Guide:** Svelte 5 uses Runes for explicit reactivity. Use `$state` for reactive variables, `$derived` for computed values, `$effect` only as an escape hatch. Use snippets instead of slots. Use callback props instead of event dispatchers. Keep components small and composable.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use Svelte 5 Runes syntax — NOT Svelte 4 patterns like `export let`, `$:`, or stores for component state)**

**(You MUST use `$derived` for computed values — NEVER use `$effect` to synchronize state)**

**(You MUST use snippets (`{#snippet}` / `{@render}`) instead of slots (`<slot>`))**

**(You MUST use callback props (`onclick`, `onsomething`) instead of `createEventDispatcher`)**

**(You MUST use `$state.raw()` for large objects/arrays that are replaced, not mutated)**

**(You MUST use `createContext` for type-safe context instead of raw `setContext`/`getContext` with string keys)**

</critical_requirements>

---

**Auto-detection:** Svelte 5, Runes, $state, $derived, $effect, $props, $bindable, $inspect, .svelte, snippet, @render, createContext, getContext, setContext, $state.raw, $state.eager, $derived.by, $effect.pre, ClassValue

**When to use:**

- Building Svelte 5 components with Runes reactivity
- Managing component state with `$state` and computed values with `$derived`
- Creating reusable markup with snippets (replacing slots)
- Handling events with native event attributes and callback props
- Sharing state across components with context API
- Two-way binding with `$bindable` props

**Key patterns covered:**

- Runes: `$state`, `$derived`, `$effect`, `$props`, `$bindable`, `$inspect`
- Component composition with snippets and `{@render}`
- Event handling with native attributes and callback props
- Context API with `createContext` for type-safe cross-component state
- Class-based reactive state with `$state` fields
- Deep vs shallow reactivity (`$state` vs `$state.raw`)

**When NOT to use:**

- Meta-framework-specific patterns (routing, load functions, form actions) — use the corresponding meta-framework skill
- Svelte 4 patterns (`export let`, `$:` reactive statements, `<slot>`, `createEventDispatcher`)
- Server-side logic (use your meta-framework's server hooks and routes)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Runes & Reactivity:**

- [examples/core.md](examples/core.md) - `$state`, `$derived`, `$effect`, `$props`, `$bindable`, component patterns

**Component Patterns:**

- [examples/snippets.md](examples/snippets.md) - Snippet blocks, `{@render}`, passing snippets as props, replacing slots
- [examples/events.md](examples/events.md) - Event handling, component events via callback props, event modifiers

**Advanced:**

- [examples/advanced.md](examples/advanced.md) - `$inspect`, context API, `$state.raw`, `$state.eager`, class-based state, shared state modules

---

<philosophy>

## Philosophy

Svelte 5 introduces **Runes** — a set of primitives that bring explicit, fine-grained reactivity to Svelte. Unlike Svelte 4's compiler magic (`$:`, `export let`), Runes make reactivity visible and portable across `.svelte` files, `.ts` files, and class definitions.

**Core principles:**

1. **Explicit reactivity** — Runes (`$state`, `$derived`, `$effect`) make reactive declarations visible. No hidden compiler transformations.
2. **Derived over effects** — Compute values with `$derived`, not `$effect`. Effects are escape hatches, not primary tools.
3. **Deep reactivity by default** — `$state` creates deeply reactive proxies for objects/arrays. Mutations are tracked automatically.
4. **Snippets replace slots** — `{#snippet}` blocks are more powerful, typed, and composable than `<slot>` elements.
5. **Callback props replace event dispatchers** — Pass `onsomething` callback props instead of using `createEventDispatcher`.
6. **Compile-time optimization** — Svelte compiles components to efficient imperative code. No virtual DOM diffing at runtime.

**When to use Svelte 5 Runes:**

- All new Svelte components (Runes are the default in Svelte 5)
- Reactive state in `.svelte.ts` or `.svelte.js` files
- Class-based state with reactive fields
- Any computed value that depends on reactive state

**When NOT to use:**

- Non-reactive constants (use plain `const` or `let`)
- Server-side code that doesn't need reactivity
- Meta-framework concerns (routing, load functions, server hooks) — use the corresponding meta-framework skill
- Svelte 4 patterns — `export let`, `$:`, stores for component state, `<slot>`, `createEventDispatcher`

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Reactive State with $state

Use `$state` to declare reactive variables. Updates to `$state` variables automatically trigger UI re-renders.

```svelte
<!-- counter.svelte -->
<script lang="ts">
  let count = $state(0);
  const STEP = 5;

  function increment() {
    count += 1;
  }

  function incrementByStep() {
    count += STEP;
  }
</script>

<button onclick={increment}>
  Count: {count}
</button>
<button onclick={incrementByStep}>
  +{STEP}
</button>
```

**Why good:** Explicit reactive declaration, named constants for magic numbers, plain function event handlers

```svelte
<!-- BAD: Svelte 4 style -->
<script>
  let count = 0; // Not explicitly reactive in Svelte 5 mode
  $: doubled = count * 2; // Svelte 4 reactive statement
</script>
```

**Why bad:** `$:` is Svelte 4 syntax deprecated in Svelte 5, implicit reactivity is confusing and non-portable

#### Deep Reactivity

`$state` creates deep proxies for objects and arrays — mutations are tracked automatically:

```svelte
<script lang="ts">
  interface Todo {
    done: boolean;
    text: string;
  }

  let todos = $state<Todo[]>([
    { done: false, text: 'Learn Svelte 5' }
  ]);

  function addTodo(text: string) {
    todos.push({ done: false, text }); // Mutation tracked!
  }

  function toggleTodo(index: number) {
    todos[index].done = !todos[index].done; // Deep mutation tracked!
  }
</script>
```

**Why good:** No need for immutable update patterns, array methods like `.push()` trigger reactivity, property mutations tracked deeply

---

### Pattern 2: Computed Values with $derived

Use `$derived` for values that depend on other reactive state. Never use `$effect` to synchronize state.

```svelte
<script lang="ts">
  let count = $state(0);

  // Simple expression
  let doubled = $derived(count * 2);

  // Complex computation with $derived.by
  let stats = $derived.by(() => {
    const isEven = count % 2 === 0;
    const isPositive = count > 0;
    return { isEven, isPositive };
  });
</script>

<p>{count} doubled is {doubled}</p>
<p>Even: {stats.isEven}, Positive: {stats.isPositive}</p>
```

**Why good:** Automatically recalculates when dependencies change, no side effects, push-pull reactivity avoids unnecessary recalculations

```svelte
<!-- BAD: Using $effect to synchronize state -->
<script lang="ts">
  let count = $state(0);
  let doubled = $state(0);

  $effect(() => {
    doubled = count * 2; // WRONG: Use $derived instead
  });
</script>
```

**Why bad:** `$effect` for derived state creates unnecessary reactive subscriptions, runs after DOM update (timing issues), harder to reason about data flow

---

### Pattern 3: Component Props with $props

Use `$props` to declare component inputs. Supports destructuring, defaults, rest props, and TypeScript.

```svelte
<!-- user-card.svelte -->
<script lang="ts">
  interface Props {
    name: string;
    email: string;
    role?: string;
    class?: string;
  }

  let { name, email, role = 'member', ...rest }: Props = $props();

  // Derived from props — updates when props change
  let initials = $derived(
    name.split(' ').map(n => n[0]).join('').toUpperCase()
  );
</script>

<div class="user-card" {...rest}>
  <span class="avatar">{initials}</span>
  <h3>{name}</h3>
  <p>{email}</p>
  <span class="badge">{role}</span>
</div>
```

**Why good:** Type-safe props with interface, destructuring with defaults, rest props for pass-through, derived values update with prop changes

```svelte
<!-- BAD: Svelte 4 style -->
<script>
  export let name; // Svelte 4 prop declaration
  export let email;
  export let role = 'member';
</script>
```

**Why bad:** `export let` is Svelte 4 syntax deprecated in Svelte 5, no type safety, no rest props

---

### Pattern 4: Two-Way Binding with $bindable

Use `$bindable` to declare props that support two-way binding with `bind:`. Use sparingly — prefer one-way data flow.

```svelte
<!-- text-input.svelte -->
<script lang="ts">
  interface Props {
    value: string;
    placeholder?: string;
  }

  let { value = $bindable(''), placeholder = '' }: Props = $props();
</script>

<input
  bind:value={value}
  {placeholder}
  class="text-input"
/>
```

```svelte
<!-- parent.svelte -->
<script lang="ts">
  import TextInput from './text-input.svelte';

  let searchQuery = $state('');
</script>

<TextInput bind:value={searchQuery} placeholder="Search..." />
<p>Searching for: {searchQuery}</p>
```

**Why good:** Explicit two-way binding declaration, parent controls the state, child can modify via `bind:`, TypeScript-safe

**When to use:** Form inputs, UI primitives (sliders, toggles) where two-way binding simplifies the API

**When not to use:** Most component communication — prefer callback props for explicit data flow

---

### Pattern 5: Side Effects with $effect

Use `$effect` for side effects that need to run when reactive state changes. This is an **escape hatch** — prefer `$derived` for computed values and event handlers for user-triggered actions.

```svelte
<script lang="ts">
  let searchQuery = $state('');
  let results = $state<string[]>([]);
  const DEBOUNCE_MS = 300;

  // Good: Side effect for external API calls
  $effect(() => {
    const query = searchQuery;

    if (!query) {
      results = [];
      return;
    }

    const timer = setTimeout(async () => {
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      results = await response.json();
    }, DEBOUNCE_MS);

    // Cleanup function runs before next effect and on unmount
    return () => clearTimeout(timer);
  });
</script>

<input bind:value={searchQuery} placeholder="Search..." />

{#each results as result}
  <p>{result}</p>
{/each}
```

**Why good:** External API call is a legitimate side effect, cleanup prevents stale requests, named constant for debounce

#### When NOT to Use $effect

```svelte
<script lang="ts">
  let count = $state(0);

  // BAD: Synchronizing state — use $derived
  // $effect(() => { doubled = count * 2; });

  // BAD: Logging in effect — use $inspect for debugging
  // $effect(() => { console.log(count); });

  // BAD: Calling functions on change — use event handlers
  // $effect(() => { if (count > 10) showAlert(); });

  // GOOD: Use $derived for computed values
  let doubled = $derived(count * 2);
</script>
```

---

### Pattern 6: Snippets (Replacing Slots)

Snippets are reusable markup blocks declared with `{#snippet}` and rendered with `{@render}`. They replace Svelte 4's `<slot>` elements.

```svelte
<!-- card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title: string;
    children: Snippet;
    footer?: Snippet;
  }

  let { title, children, footer }: Props = $props();
</script>

<div class="card">
  <h2>{title}</h2>
  <div class="card-body">
    {@render children()}
  </div>
  {#if footer}
    <div class="card-footer">
      {@render footer()}
    </div>
  {/if}
</div>
```

```svelte
<!-- usage -->
<script lang="ts">
  import Card from './card.svelte';
</script>

<Card title="Welcome">
  <p>This becomes the children snippet automatically.</p>

  {#snippet footer()}
    <button>Learn More</button>
  {/snippet}
</Card>
```

**Why good:** Type-safe with `Snippet` type, optional snippets with conditional rendering, `children` is implicit for content between tags

```svelte
<!-- BAD: Svelte 4 slots -->
<div class="card">
  <slot /> <!-- Deprecated in Svelte 5 -->
  <slot name="footer" /> <!-- Use snippets instead -->
</div>
```

**Why bad:** `<slot>` is deprecated in Svelte 5, no type safety, less composable than snippets

---

### Pattern 7: Event Handling

Svelte 5 uses native event attributes (`onclick`, `onsubmit`) instead of Svelte 4's `on:click` directive. Component events use callback props.

#### Element Events

```svelte
<script lang="ts">
  let count = $state(0);

  function handleClick(event: MouseEvent) {
    count += 1;
  }

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    // handle form
  }
</script>

<button onclick={handleClick}>Clicked {count} times</button>

<!-- Inline handlers are fine for simple logic -->
<button onclick={() => count = 0}>Reset</button>

<form onsubmit={handleSubmit}>
  <input name="query" />
  <button type="submit">Search</button>
</form>
```

#### Component Events via Callback Props

```svelte
<!-- color-picker.svelte -->
<script lang="ts">
  interface Props {
    color: string;
    onchange?: (color: string) => void;
    onreset?: () => void;
  }

  let { color, onchange, onreset }: Props = $props();

  const COLORS = ['red', 'green', 'blue', 'purple'] as const;
</script>

{#each COLORS as c}
  <button
    onclick={() => onchange?.(c)}
    class={{ selected: color === c }}
  >
    {c}
  </button>
{/each}

{#if onreset}
  <button onclick={onreset}>Reset</button>
{/if}
```

```svelte
<!-- parent.svelte -->
<script lang="ts">
  import ColorPicker from './color-picker.svelte';

  let selectedColor = $state('red');
</script>

<ColorPicker
  color={selectedColor}
  onchange={(c) => selectedColor = c}
  onreset={() => selectedColor = 'red'}
/>
```

**Why good:** Type-safe callback props, optional with `?.` call, parent controls event handling, no indirection through dispatcher

```svelte
<!-- BAD: Svelte 4 event dispatcher -->
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch('change', { color: 'red' }); // Deprecated pattern
  }
</script>
```

**Why bad:** `createEventDispatcher` is deprecated in Svelte 5, no type safety, requires manual event typing

</patterns>

---

<integration>

## Integration Guide

**Styling integration:**

- Scoped `<style>` blocks are the default — styles don't leak to other components
- Use `:global()` for global styles or CSS custom properties for parent-to-child styling
- Any CSS approach (CSS Modules, utility-first, preprocessors) works with Svelte

**State management:**

- `$state` for component-local state
- Context API (`createContext`) for subtree-scoped state
- Reactive classes with `$state` fields for shared state modules (`.svelte.ts`)
- Meta-framework load functions for server state

**TypeScript integration:**

- Full TypeScript support in `<script lang="ts">` blocks
- `Snippet<[ParamType]>` for typed snippet props
- Interface-based prop typing with `$props()`
- `ClassValue` type from `svelte/elements` for type-safe class props (Svelte 5.19+)

</integration>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Using `export let` for props — use `$props()` instead
- Using `$:` reactive statements — use `$derived` or `$effect`
- Using `<slot>` or `<slot name="x">` — use `{#snippet}` and `{@render}`
- Using `createEventDispatcher` — use callback props
- Using `$effect` to sync state — use `$derived` for computed values
- Destructuring `$state` objects — breaks reactivity (values captured at destructure time)

**Medium Priority:**

- Using `on:click` directive — use `onclick` attribute
- Not using `$state.raw()` for large API responses — unnecessary proxy overhead
- Using `setContext`/`getContext` with string keys — use `createContext` for type safety
- Using `class:name={condition}` — use built-in `class` attribute object/array syntax (since 5.16)

**Gotchas:**

- `$state` proxies are not the original object — use `$state.snapshot()` to get a plain copy
- Destructuring `$state` captures values, not references — access properties directly instead
- `$derived` return values are NOT deeply reactive — only `$state` creates deep proxies
- `$effect` runs after DOM update — use `$effect.pre()` for pre-update timing
- Dependencies after `await` in `$effect` are not tracked
- Context must be set during component init — cannot call `setContext` in event handlers or `$effect`

> For complete decision frameworks and the full anti-patterns list, see [reference.md](reference.md).

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use Svelte 5 Runes syntax — NOT Svelte 4 patterns like `export let`, `$:`, or stores for component state)**

**(You MUST use `$derived` for computed values — NEVER use `$effect` to synchronize state)**

**(You MUST use snippets (`{#snippet}` / `{@render}`) instead of slots (`<slot>`))**

**(You MUST use callback props (`onclick`, `onsomething`) instead of `createEventDispatcher`)**

**(You MUST use `$state.raw()` for large objects/arrays that are replaced, not mutated)**

**(You MUST use `createContext` for type-safe context instead of raw `setContext`/`getContext` with string keys)**

**Failure to follow these rules will produce outdated Svelte 4 code that is deprecated and will break in future versions.**

</critical_reminders>
