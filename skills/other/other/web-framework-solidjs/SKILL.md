---
name: web-framework-solidjs
description: SolidJS fine-grained reactivity patterns - signals, effects, memos, stores, createResource, control flow components, Suspense, SolidStart
---

# SolidJS Patterns

> **Quick Guide:** Use `createSignal` for primitives, `createStore` for nested objects. Always call signals as functions (`count()` not `count`). Never destructure props. Use `<Show>`, `<For>`, `<Switch>` for control flow. Wrap async data in `createResource` and components in `<Suspense>`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call signals as functions to read values - `count()` NOT `count`)**

**(You MUST NEVER destructure props - use `props.name` or `splitProps()` to preserve reactivity)**

**(You MUST use `<Show>`, `<For>`, `<Switch>` control flow components instead of ternaries and `.map()`)**

**(You MUST clean up side effects with `onCleanup()` inside effects)**

**(You MUST wrap async data fetching in `createResource` and components in `<Suspense>`)**

</critical_requirements>

---

**Auto-detection:** SolidJS, createSignal, createEffect, createMemo, createStore, createResource, createAsync, query, action, Show, For, Switch, Match, splitProps, mergeProps, onCleanup, onMount, Suspense, ErrorBoundary, solid-js, @solidjs/router, SolidStart

**When to use:**

- Building reactive UIs with fine-grained reactivity (no virtual DOM)
- Managing state with signals (primitives) and stores (nested objects)
- Creating derived values with memos
- Fetching async data with createResource
- Building full-stack apps with SolidStart

**Key patterns covered:**

- Signals, effects, and memos (core reactivity)
- Component patterns (props, splitProps, mergeProps, refs)
- Control flow components (Show, For, Index, Switch, Match)
- Stores for complex nested state
- createResource for async data fetching (plain SolidJS)
- createAsync + query for data fetching (SolidStart, recommended for Solid 2.0)
- Context for dependency injection
- Suspense and ErrorBoundary for async handling
- SolidStart patterns (server functions, query, actions)

**When NOT to use:**

- When team is deeply invested in React ecosystem
- Projects requiring extensive third-party React component libraries
- When you need React-specific features (Server Components, concurrent mode)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Signals, effects, memos, batch
- [examples/components.md](examples/components.md) - Props handling, control flow, refs, component types
- [examples/stores.md](examples/stores.md) - createStore, produce, reconcile, Context
- [examples/resources.md](examples/resources.md) - createResource, createAsync, query/action (SolidStart)
- [reference.md](reference.md) - Decision frameworks, anti-patterns, checklists

---

<philosophy>

## Philosophy

SolidJS achieves exceptional performance through **fine-grained reactivity**: instead of re-rendering entire component trees like React, Solid tracks dependencies at the expression level and surgically updates only the specific DOM nodes that changed. Components run once during creation, not on every state change.

**Core principles:**

1. **Fine-grained reactivity** - Updates happen at the DOM node level, not component level
2. **Signals are functions** - Reading a signal (`count()`) subscribes to it, creating automatic dependency tracking
3. **Components run once** - The component function body executes only at creation time
4. **No virtual DOM** - Direct DOM manipulation eliminates diffing overhead
5. **Explicit reactivity** - State is explicitly reactive via `createSignal` and `createStore`

**Key mental model:**

```typescript
// React: Component re-renders, recalculates everything
function Counter() {
  const [count, setCount] = useState(0);
  console.log('This runs on EVERY update'); // Re-runs
  return <span>{count}</span>; // Re-renders span
}

// Solid: Component runs once, only expressions update
function Counter() {
  const [count, setCount] = createSignal(0);
  console.log('This runs ONCE'); // Only at creation
  return <span>{count()}</span>; // Only text node updates
}
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Signals - Reactive Primitives

Signals are the foundation of Solid's reactivity. They hold a value and notify subscribers when it changes.

#### Basic Signals

```typescript
import { createSignal } from "solid-js";

const MAX_COUNT = 100;
const INITIAL_COUNT = 0;

// createSignal returns [getter, setter]
const [count, setCount] = createSignal(INITIAL_COUNT);

// MUST call as function to read
console.log(count()); // 0

// Setting values
setCount(5);
setCount((prev) => prev + 1); // Functional update

// With TypeScript explicit types
const [user, setUser] = createSignal<User | null>(null);
```

**Why good:** Explicit reactivity through function calls, automatic dependency tracking, type-safe with generics, functional updates prevent stale closure bugs

#### Signals in Components

```typescript
import { createSignal, type Component } from 'solid-js';

const Counter: Component = () => {
  const [count, setCount] = createSignal(0);

  // This console.log runs ONCE, not on every update
  console.log('Component created');

  return (
    <div>
      {/* Only this text node updates when count changes */}
      <span>Count: {count()}</span>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
};

export { Counter };
```

**Why good:** Component body runs once, only `{count()}` expression re-evaluates on update, minimal DOM manipulation

---

### Pattern 2: Effects - Side Effects on State Changes

Effects run automatically when their tracked dependencies change.

#### createEffect

```typescript
import { createSignal, createEffect, onCleanup } from "solid-js";

const [count, setCount] = createSignal(0);

// Automatically tracks count() as dependency
createEffect(() => {
  console.log("Count changed:", count());
});

// Effect with cleanup
createEffect(() => {
  const handler = () => console.log("Clicked, count:", count());
  window.addEventListener("click", handler);

  // MUST clean up to prevent memory leaks
  onCleanup(() => {
    window.removeEventListener("click", handler);
  });
});
```

**Why good:** Automatic dependency tracking (no dependency array), onCleanup runs before each re-execution and on disposal

#### Explicit Tracking with on()

```typescript
import { createSignal, createEffect, on } from "solid-js";

const [count, setCount] = createSignal(0);
const [name, setName] = createSignal("");

// Only tracks count, ignores name even if accessed
createEffect(
  on(count, (value, prev) => {
    console.log("Count went from", prev, "to", value);
    // name() here won't add a dependency
    console.log("Current name:", name());
  }),
);

// Multiple explicit dependencies
createEffect(
  on([count, name], ([c, n]) => {
    console.log("Either changed:", c, n);
  }),
);
```

**Why good:** Explicit control over what triggers the effect, access to previous value

---

### Pattern 3: Memos - Cached Derived Values

Memos cache computed values and only recalculate when dependencies change.

#### createMemo

```typescript
import { createSignal, createMemo } from "solid-js";

const [items, setItems] = createSignal<Item[]>([]);
const [filter, setFilter] = createSignal("");

// Only recalculates when items or filter changes
const filteredItems = createMemo(() => {
  console.log("Filtering..."); // Only runs when dependencies change
  return items().filter((item) =>
    item.name.toLowerCase().includes(filter().toLowerCase()),
  );
});

// Expensive computation - memoized automatically
const sortedItems = createMemo(() => {
  return [...items()].sort((a, b) => a.name.localeCompare(b.name));
});
```

**Why good:** Caches result until dependencies change, prevents unnecessary recalculations, clearer than inline expressions for complex logic

---

### Pattern 4: Component Props

Never destructure props in Solid - it breaks reactivity.

#### Props with splitProps and mergeProps

```typescript
import { splitProps, mergeProps, type Component, type JSX } from 'solid-js';

interface ButtonProps extends JSX.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  loading?: boolean;
}

const Button: Component<ButtonProps> = (rawProps) => {
  // Default props with mergeProps
  const props = mergeProps({ variant: 'primary' as const }, rawProps);

  // Split custom props from native HTML attributes
  const [local, buttonProps] = splitProps(props, ['variant', 'loading']);

  return (
    <button
      {...buttonProps}
      class={`btn btn-${local.variant}`}
      disabled={local.loading || buttonProps.disabled}
    >
      {local.loading ? 'Loading...' : props.children}
    </button>
  );
};

export { Button };
```

**Why good:** splitProps separates custom props from spread-able HTML props, mergeProps provides defaults while preserving reactivity, never destructure props

#### Component Types

Use `VoidComponent` (no children), `ParentComponent` (children required), or `Component` (children optional) for type-safe children handling.

```typescript
const Icon: VoidComponent<{ name: string }> = (props) => (/* ... */);
const Card: ParentComponent<{ title: string }> = (props) => (/* ... */);
```

See [examples/components.md](examples/components.md) for full component type examples.

---

### Pattern 5: Control Flow Components

Solid uses dedicated components for control flow instead of JavaScript expressions.

#### Show for Conditionals

```typescript
import { Show } from 'solid-js';

// Basic condition with fallback
<Show when={user()} fallback={<LoginForm />}>
  <Dashboard />
</Show>

// Keyed flow - access the truthy value safely
<Show when={user()} fallback={<LoginForm />}>
  {(user) => <Dashboard user={user()} />}
</Show>
```

**Why good:** Optimized for fine-grained updates, keyed flow provides narrowed type

#### For for Lists

```typescript
import { For } from 'solid-js';

// Basic list rendering
<For each={items()} fallback={<p>No items</p>}>
  {(item, index) => (
    <li>
      {index()}: {item.name}
    </li>
  )}
</For>
```

**Why good:** Automatically handles keying by reference, index() is a signal, optimized list diffing

#### Switch/Match for Multiple Conditions

```typescript
import { Switch, Match } from 'solid-js';

<Switch fallback={<p>Unknown status</p>}>
  <Match when={status() === 'loading'}>
    <Spinner />
  </Match>
  <Match when={status() === 'error'}>
    <ErrorMessage error={error()} />
  </Match>
  <Match when={status() === 'success'}>
    <SuccessView data={data()} />
  </Match>
</Switch>
```

**Why good:** First matching condition renders, cleaner than nested Shows

---

### Pattern 6: Refs

Refs work differently in Solid - no `forwardRef` needed.

#### DOM and Component Refs

```typescript
import { onMount, type Component } from 'solid-js';

const Form: Component = () => {
  let inputRef: HTMLInputElement;

  onMount(() => {
    // Ref is available after mount
    inputRef.focus();
  });

  return (
    <form>
      {/* Ref callback or assignment */}
      <input ref={inputRef!} type="text" />
      <input ref={(el) => console.log('Element:', el)} type="email" />
    </form>
  );
};

export { Form };
```

**Why good:** No forwardRef wrapper needed, refs are just props, works with components and DOM elements

---

### Pattern 7: Context

Share data across component tree without prop drilling. Create a typed context, wrap in Provider with a Store, and expose a hook with error handling.

```typescript
const AuthContext = createContext<AuthContextValue>();

const AuthProvider: ParentComponent = (props) => {
  const [store, setStore] = createStore<{ user: User | null }>({ user: null });
  const value = { get user() { return store.user; }, /* actions */ };
  return <AuthContext.Provider value={value}>{props.children}</AuthContext.Provider>;
};

function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
```

**Why good:** Getter on store field preserves reactivity in context, throws on missing provider

See [examples/stores.md](examples/stores.md) for complete Store + Context implementation.

</patterns>

---

<integration>

## Integration Guide

**SolidJS is framework-agnostic for styling and tooling.** Components receive props and emit events, fitting any styling or state management approach.

**Ecosystem:**

- **SolidStart** for full-stack applications with file-based routing
- **@solidjs/router** for client-side routing
- **solid-primitives** community library for common utilities
- Any CSS solution via `class` attribute binding

**State decisions:**

- Simple values: `createSignal`
- Nested objects/arrays: `createStore`
- Shared across components: Context + Store
- Async data: `createResource` or `createAsync` (SolidStart)

**Component communication:**

- Props down, callbacks up (like React)
- Context for deeply nested sharing
- No prop drilling thanks to fine-grained reactivity

</integration>

---

<red_flags>

## RED FLAGS

- **Reading signal without parentheses** - `count` instead of `count()` doesn't read the value or track dependencies
- **Destructuring props** - `const { name } = props` breaks reactivity; use `props.name` or `splitProps()`
- **Using ternary instead of Show** - `{condition ? <A /> : <B />}` bypasses Solid's optimizations
- **Using .map() instead of For** - `{items().map(...)}` doesn't get fine-grained list updates
- **Missing onCleanup in effects** - Event listeners, timers, subscriptions will leak memory
- **Async operations inside createEffect tracking scope** - Code after `await` loses tracking context
- **Side effects in createMemo** - Memos should be pure; use createEffect for side effects
- **Using createEffect for data fetching** - Use createResource or createAsync instead
- **Direct mutation of store** - `store.field = x` bypasses proxy tracking; use setStore path syntax

**Gotchas:**

- Signals read outside reactive context (event handlers) aren't tracked
- Stores only track property access (`store.field`), not the store object itself
- Code after `await` in effects runs outside the tracking scope
- `children` is a getter in Solid - use `children()` helper when iterating
- Index provides values as signals - call `item()` inside Index, not in For

See [reference.md](reference.md) for full anti-pattern examples and decision frameworks.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call signals as functions to read values - `count()` NOT `count`)**

**(You MUST NEVER destructure props - use `props.name` or `splitProps()` to preserve reactivity)**

**(You MUST use `<Show>`, `<For>`, `<Switch>` control flow components instead of ternaries and `.map()`)**

**(You MUST clean up side effects with `onCleanup()` inside effects)**

**(You MUST wrap async data fetching in `createResource` and components in `<Suspense>`)**

**Failure to follow these rules will break reactivity, cause memory leaks, or result in stale UI.**

</critical_reminders>
