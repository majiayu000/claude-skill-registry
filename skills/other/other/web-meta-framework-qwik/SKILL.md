---
name: web-meta-framework-qwik
description: Qwik resumable framework - zero hydration, $ lazy boundaries, signals, Qwik City file-based routing, routeLoader$, routeAction$, server$ RPC, serialization rules
---

# Qwik Framework Patterns

> **Quick Guide:** Qwik is resumable - it serializes application state on the server and resumes on the client without re-executing framework code (no hydration). Every `$` suffix marks a lazy-loading boundary where the optimizer splits code into separate chunks. Only the code for the interaction the user triggers gets downloaded. Use `component$` for all components, `useSignal`/`useStore` for state, `routeLoader$` for server data, `routeAction$` for mutations, and `server$` for ad-hoc server RPC. The critical mental model: anything crossing a `$` boundary must be serializable.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap every component in `component$()` - plain functions cannot be lazy-loaded, cannot use hooks, and cannot use `<Slot />`)**

**(You MUST ensure all values captured in a `$` closure are serializable - non-serializable captures pass type-checking but fail at runtime)**

**(You MUST use `routeLoader$` for initial server data instead of fetching in `useTask$` or `useResource$` - loaders run before render and integrate with SSR streaming)**

**(You MUST use `preventdefault:click` as a JSX attribute instead of calling `event.preventDefault()` - event handlers load asynchronously so synchronous Event APIs are unavailable)**

**(You MUST export `routeLoader$` and `routeAction$` from route files (`index.tsx` or `layout.tsx` in `src/routes/`) - unexported or misplaced loaders/actions silently do nothing)**

**(You MUST NOT destructure store properties at the top level - destructuring breaks reactivity because you lose the Proxy reference)**

</critical_requirements>

---

**Auto-detection:** Qwik, component$, useSignal, useStore, useTask$, useVisibleTask$, useComputed$, useResource$, routeLoader$, routeAction$, server$, sync$, QRL, noSerialize, @builder.io/qwik, @builder.io/qwik-city, Qwik City, $(), onClick$, onInput$, Slot, q:slot, preventdefault, stoppropagation, useStylesScoped$, resumable, resumability

**When to use:**

- Building web apps where instant interactivity matters (zero hydration delay)
- Apps with complex interactivity that would ship too much JS with traditional hydration
- Projects needing fine-grained lazy loading without manual code-splitting
- Full-stack apps with server loaders, actions, and RPC via `server$`
- Progressive enhancement where forms work without JavaScript

**When NOT to use:**

- Static content sites with minimal interactivity (use a static site generator)
- Projects where the team is deeply invested in React ecosystem libraries that have no Qwik equivalents
- Apps that rely heavily on non-serializable runtime state (class instances, closures with side effects)

**Key patterns covered:**

- Resumability mental model and the `$` suffix convention
- Component definition with `component$`, props, and `<Slot />`
- Reactive state: `useSignal`, `useStore`, `useComputed$`
- Lifecycle: `useTask$`, `useVisibleTask$`, `useResource$`
- Event handling: `onClick$`, `preventdefault:click`, `sync$`
- Qwik City routing: file-based routes, layouts, dynamic params
- Server data: `routeLoader$`, `routeAction$`, `server$`
- Serialization rules and the `$` boundary

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core patterns:**

- [examples/core.md](examples/core.md) - Components, signals, stores, tasks, events, slots
- [examples/routing.md](examples/routing.md) - File-based routing, routeLoader$, routeAction$, server$, middleware
- [examples/serialization.md](examples/serialization.md) - Serialization rules, $ boundary, non-serializable patterns

---

<philosophy>

## Philosophy

Qwik is built on **resumability** - the idea that the server can serialize the entire application state (component tree, listeners, state) into HTML, and the client can resume exactly where the server left off without re-executing any framework code.

**How it differs from hydration frameworks:**

Traditional SSR frameworks render HTML on the server, then **re-execute all component code on the client** to attach event listeners and rebuild the component tree. This is hydration - the client replays the server's work.

Qwik skips this entirely. The server serializes everything into the HTML. When a user clicks a button, only the click handler's code downloads and executes. The framework itself, the component tree, and all other handlers stay unloaded until needed.

**The `$` suffix is the core mechanism.** Every function ending in `$` is a lazy-loading boundary. The Qwik optimizer splits code at each `$` marker into separate chunks. This means:

- `component$()` - the component's render function loads only when needed
- `onClick$()` - the click handler loads only when the user clicks
- `routeLoader$()` - the loader runs server-side only
- `useTask$()` - the task loads when its tracked dependencies change

**The tradeoff:** Because code must be serializable to cross `$` boundaries, you cannot capture non-serializable values (class instances, functions, DOM nodes) in `$` closures. This constraint is the price of instant interactivity.

**When to use Qwik:**

- Interactive apps where time-to-interactive matters
- Large apps where traditional hydration downloads too much JS upfront
- Full-stack apps leveraging `routeLoader$`/`routeAction$`/`server$` for server logic
- Progressive enhancement (Qwik forms work without JS)

**When NOT to use Qwik:**

- Static content sites with little interactivity
- Projects heavily dependent on React-specific libraries without Qwik equivalents
- Apps requiring extensive non-serializable runtime state

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Components with component$

Every Qwik component must be wrapped in `component$()`. This is not optional - it enables lazy loading, hooks, and `<Slot />`.

```tsx
import { component$, useSignal } from "@builder.io/qwik";

interface CounterProps {
  initial?: number;
  label: string;
}

export const Counter = component$<CounterProps>(({ initial = 0, label }) => {
  const count = useSignal(initial);

  return (
    <div>
      <span>
        {label}: {count.value}
      </span>
      <button onClick$={() => count.value++}>+</button>
    </div>
  );
});
```

**Why good:** `component$` enables the optimizer to split this into a lazy chunk, typed props via generic, `useSignal` for reactive state, `onClick$` handler loads only on click

```tsx
// BAD: Plain function component
export const Counter = (props: { label: string }) => {
  // Cannot use hooks here - useSignal will throw
  // Cannot use <Slot /> - only works inside component$
  return <div>{props.label}</div>;
};
```

**Why bad:** Without `component$` wrapper, hooks throw at runtime, `<Slot />` breaks, optimizer cannot split the code, component is not resumable

---

### Pattern 2: Reactive State - useSignal vs useStore

`useSignal` holds a single reactive value accessed via `.value`. `useStore` holds a reactive object with deep tracking by default.

```tsx
import { component$, useSignal, useStore } from "@builder.io/qwik";

export const UserProfile = component$(() => {
  // useSignal for primitives and flat values
  const isEditing = useSignal(false);
  const selectedTab = useSignal<"profile" | "settings">("profile");

  // useStore for objects/arrays - deep reactivity by default
  const user = useStore({
    name: "Alice",
    email: "alice@example.com",
    preferences: {
      theme: "dark",
      notifications: true,
    },
  });

  return (
    <div>
      <h1>{user.name}</h1>
      {isEditing.value ? (
        <input
          value={user.name}
          onInput$={(_, el) => {
            user.name = el.value;
          }}
        />
      ) : (
        <button
          onClick$={() => {
            isEditing.value = true;
          }}
        >
          Edit
        </button>
      )}
    </div>
  );
});
```

**Why good:** `useSignal` for simple toggles/selections (accessed via `.value`), `useStore` for structured data (mutate properties directly), deep reactivity tracks `user.preferences.theme` changes automatically

```tsx
// BAD: Destructuring a store
const { name, email } = useStore({ name: "Alice", email: "a@b.com" });
// name and email are now plain strings - NOT reactive
// Changing them does nothing to the UI
```

**Why bad:** Destructuring extracts primitive values from the Proxy, breaking reactivity - you must keep the store reference intact and access `store.name` directly

---

### Pattern 3: Computed Values with useComputed$

`useComputed$` derives values from signals/stores. It re-runs only when dependencies change. Synchronous only.

```tsx
import { component$, useSignal, useComputed$ } from "@builder.io/qwik";

const TAX_RATE = 0.08;
const FREE_SHIPPING_THRESHOLD = 100;

export const CartSummary = component$(() => {
  const subtotal = useSignal(85);

  const tax = useComputed$(() => subtotal.value * TAX_RATE);
  const shipping = useComputed$(() =>
    subtotal.value >= FREE_SHIPPING_THRESHOLD ? 0 : 9.99,
  );
  const total = useComputed$(() => subtotal.value + tax.value + shipping.value);

  return (
    <div>
      <p>Subtotal: ${subtotal.value.toFixed(2)}</p>
      <p>Tax: ${tax.value.toFixed(2)}</p>
      <p>Shipping: ${shipping.value.toFixed(2)}</p>
      <p>Total: ${total.value.toFixed(2)}</p>
    </div>
  );
});
```

**Why good:** Automatic dependency tracking (no dependency arrays), read-only signal prevents accidental mutation, recomputes only when `subtotal` changes, named constants for magic numbers

---

### Pattern 4: Tasks and Lifecycle

`useTask$` runs before render (server + client). `useVisibleTask$` runs after render (browser only). Use `track()` to declare reactive dependencies.

```tsx
import {
  component$,
  useSignal,
  useTask$,
  useVisibleTask$,
} from "@builder.io/qwik";
import { server$ } from "@builder.io/qwik-city";

const DEBOUNCE_MS = 300;

export const SearchBox = component$(() => {
  const query = useSignal("");
  const results = useSignal<string[]>([]);

  // Runs before render, re-runs when query changes
  useTask$(({ track, cleanup }) => {
    const searchTerm = track(() => query.value);
    if (!searchTerm) {
      results.value = [];
      return;
    }

    const debounceTimer = setTimeout(async () => {
      const data = await fetchResults(searchTerm);
      results.value = data;
    }, DEBOUNCE_MS);

    cleanup(() => clearTimeout(debounceTimer));
  });

  return (
    <div>
      <input
        value={query.value}
        onInput$={(_, el) => {
          query.value = el.value;
        }}
      />
      <ul>
        {results.value.map((r) => (
          <li key={r}>{r}</li>
        ))}
      </ul>
    </div>
  );
});

const fetchResults = server$(async function (term: string) {
  // Runs on server only - safe to access DB, env vars, etc.
  const db = this.env.get("DATABASE_URL");
  // ... query database
  return ["result1", "result2"];
});
```

**Why good:** `track()` explicitly declares what triggers re-runs, `cleanup()` prevents timer leaks, `server$` keeps the fetch server-side

**When to use each:**

| Hook              | Runs                           | Use for                                    |
| ----------------- | ------------------------------ | ------------------------------------------ |
| `useTask$`        | Server + client, before render | Data init, side effects on state change    |
| `useVisibleTask$` | Browser only, after render     | DOM manipulation, browser APIs, animations |
| `useComputed$`    | Synchronous, auto-tracked      | Derived values (formatting, filtering)     |
| `useResource$`    | Server + client, non-blocking  | Async data that shouldn't block render     |

---

### Pattern 5: Event Handling

Event handlers use the `on{Event}$` convention. Because handlers load asynchronously, synchronous Event APIs (`preventDefault`, `stopPropagation`, `currentTarget`) are NOT available - use declarative attributes instead.

```tsx
import { component$, useSignal, $ } from "@builder.io/qwik";

export const LoginForm = component$(() => {
  const email = useSignal("");

  // Extracted handler - wrap with $() for reuse
  const handleSubmit = $((e: SubmitEvent) => {
    // Submit email.value to server
  });

  return (
    <form preventdefault:submit onSubmit$={handleSubmit}>
      <input
        type="email"
        value={email.value}
        onInput$={(_, el) => {
          email.value = el.value;
        }}
      />
      <button type="submit">Login</button>
    </form>
  );
});
```

**Why good:** `preventdefault:submit` replaces `e.preventDefault()` declaratively, second parameter of `onInput$` gives the element directly (avoiding async `currentTarget` issues), extracted handler uses `$()` wrapper

```tsx
// BAD: Calling synchronous Event APIs
<form onSubmit$={(e) => {
  e.preventDefault(); // WRONG - handler is async, this is a no-op
  e.stopPropagation(); // WRONG - same reason
}}>
```

**Why bad:** Event handlers are lazy-loaded asynchronously, so `preventDefault()` and `stopPropagation()` execute too late to have any effect - use `preventdefault:submit` and `stoppropagation:submit` attributes instead

---

### Pattern 6: Content Projection with Slot

`<Slot />` projects child content. Named slots use the `q:slot` attribute. Only works inside `component$()`.

```tsx
import { component$, Slot } from "@builder.io/qwik";

export const Card = component$<{ variant?: "default" | "outlined" }>(
  ({ variant = "default" }) => {
    return (
      <div class={`card card-${variant}`}>
        <header class="card-header">
          <Slot name="header" />
        </header>
        <div class="card-body">
          <Slot /> {/* Default slot */}
        </div>
        <footer class="card-footer">
          <Slot name="footer" />
        </footer>
      </div>
    );
  },
);

// Usage
export const Page = component$(() => {
  return (
    <Card variant="outlined">
      <h2 q:slot="header">Card Title</h2>
      <p>This goes in the default slot.</p>
      <div q:slot="footer">
        <button>Action</button>
      </div>
    </Card>
  );
});
```

**Why good:** Named slots via `q:slot` attribute, default slot for main content, parent and child render independently

**Gotcha:** `q:slot` must be on a direct child of the component. Wrapping slotted content in an intermediate element breaks projection.

---

### Pattern 7: routeLoader$ for Server Data

`routeLoader$` runs on the server before the page renders. It must be exported from a route file. Returns a read-only signal.

```tsx
// src/routes/products/[id]/index.tsx
import { component$ } from "@builder.io/qwik";
import { routeLoader$ } from "@builder.io/qwik-city";

export const useProduct = routeLoader$(async (requestEvent) => {
  const productId = requestEvent.params.id;
  const product = await db.products.findById(productId);

  if (!product) {
    return requestEvent.fail(404, {
      errorMessage: `Product ${productId} not found`,
    });
  }

  return product;
});

export default component$(() => {
  const product = useProduct(); // ReadonlySignal

  return product.value.failed ? (
    <p>{product.value.errorMessage}</p>
  ) : (
    <div>
      <h1>{product.value.name}</h1>
      <p>${product.value.price}</p>
    </div>
  );
});
```

**Why good:** Server-only execution, runs before render (no loading states during SSR), type-safe error handling with `fail()`, read-only signal prevents accidental client-side mutation

---

### Pattern 8: routeAction$ for Mutations

`routeAction$` handles form submissions and mutations. Supports Zod validation. Must be exported from route files.

```tsx
// src/routes/contact/index.tsx
import { component$ } from "@builder.io/qwik";
import { routeAction$, Form, zod$, z } from "@builder.io/qwik-city";

export const useContactAction = routeAction$(
  async (data, requestEvent) => {
    // data is validated and typed: { name: string; email: string; message: string }
    await sendEmail(data);
    return { success: true };
  },
  zod$({
    name: z.string().min(1),
    email: z.string().email(),
    message: z.string().min(10),
  }),
);

export default component$(() => {
  const action = useContactAction();

  return (
    <Form action={action}>
      <input name="name" />
      <input name="email" type="email" />
      <textarea name="message" />

      {action.value?.fieldErrors?.email && (
        <p class="error">{action.value.fieldErrors.email}</p>
      )}

      {action.value?.failed && <p class="error">{action.value.message}</p>}

      {action.value?.success && <p>Message sent!</p>}

      <button type="submit" disabled={action.isRunning}>
        {action.isRunning ? "Sending..." : "Send"}
      </button>
    </Form>
  );
});
```

**Why good:** `<Form>` works without JS (progressive enhancement), Zod validation runs server-side with typed errors, `action.isRunning` for loading state, `action.value.failed` discriminates success/failure

</patterns>

---

<red_flags>

## RED FLAGS

### High Priority Issues

- **Using plain functions instead of `component$()`** - Hooks throw, `<Slot />` breaks, optimizer cannot split code, component is not resumable
- **Destructuring store properties** - `const { name } = store` extracts a plain value, breaking reactivity. Always access `store.name` directly
- **Calling `event.preventDefault()` inside `onClick$`** - Handler loads asynchronously, so `preventDefault()` is a no-op. Use `preventdefault:click` attribute
- **Putting `routeLoader$`/`routeAction$` in non-route files without re-exporting** - They silently do nothing unless exported from `src/routes/**/index.tsx` or `layout.tsx`
- **Capturing non-serializable values in `$` closures** - Class instances, functions, DOM nodes pass type-checking but fail at runtime with serialization errors

### Medium Priority Issues

- **Using `useVisibleTask$` when `useTask$` would work** - `useVisibleTask$` is browser-only and runs after render; prefer `useTask$` by default for better SSR
- **Fetching data in `useTask$` instead of `routeLoader$`** - Loaders integrate with SSR streaming and run before render; `useTask$` blocks rendering
- **Using `client:load`-style thinking** - Qwik is not an islands framework. Every component is already lazy-loaded at the interaction level. You do not choose what to hydrate.
- **Over-capturing in `$` closures** - Closing over an entire store when you only need one property forces Qwik to serialize the whole store

### Common Mistakes

- **Using `useStore({ deep: true })` explicitly** - Deep is already the default. Passing it is redundant. Pass `{ deep: false }` only when you need shallow tracking
- **Using arrow functions for store methods** - Arrow functions lose `this` binding. Use regular `function(){}` syntax for methods on stores
- **Confusing `@builder.io/qwik` vs `@builder.io/qwik-city` imports** - Components, signals, tasks from `@builder.io/qwik`. Routing, loaders, actions, `server$` from `@builder.io/qwik-city`
- **Inline `<style>` tags in components** - Causes double-loading (SSR + client). Use `useStylesScoped$()` or CSS modules instead

### Gotchas & Edge Cases

- **`useTask$` without `track()` runs once on mount** - Without tracking any signal, it behaves like an initialization hook, not a reactive effect
- **`useTask$` blocks rendering** - Long async operations in `useTask$` delay the component render. Use `useResource$` for non-blocking async
- **`onInput$` second parameter** - The callback receives `(event, element)` where `element` is the target. Use `el.value` instead of `event.currentTarget.value` (currentTarget is null in async handlers)
- **Middleware does NOT run for `server$` calls** - Layout-level `onRequest`/`onGet` handlers are skipped for `server$` RPC. Use `plugin.ts` for middleware that must run on `server$` requests
- **Version skew with `server$`** - Client and server must run the same code version. Stale client deployments cause undefined behavior
- **`useStylesScoped$` uses emoji-based class hashing** - Scoped styles apply via emoji characters in selectors. Use `:global()` to break out when styling `<Slot />` content
- **Props are shallowly immutable** - Reassigning a primitive prop from a child does nothing. Pass a `Signal` instead if the child needs to write back
- **Deep store mutations may not trigger updates** - Tracking `store[key].nested` requires tracking the specific property, not just the key. `useStore` with `{ deep: false }` disables deep tracking
- **`<Slot />` does not work in inline components** - Only `component$()` functions support `<Slot />`. Arrow functions or plain functions will silently fail

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap every component in `component$()` - plain functions cannot be lazy-loaded, cannot use hooks, and cannot use `<Slot />`)**

**(You MUST ensure all values captured in a `$` closure are serializable - non-serializable captures pass type-checking but fail at runtime)**

**(You MUST use `routeLoader$` for initial server data instead of fetching in `useTask$` or `useResource$` - loaders run before render and integrate with SSR streaming)**

**(You MUST use `preventdefault:click` as a JSX attribute instead of calling `event.preventDefault()` - event handlers load asynchronously so synchronous Event APIs are unavailable)**

**(You MUST export `routeLoader$` and `routeAction$` from route files (`index.tsx` or `layout.tsx` in `src/routes/`) - unexported or misplaced loaders/actions silently do nothing)**

**(You MUST NOT destructure store properties at the top level - destructuring breaks reactivity because you lose the Proxy reference)**

**Failure to follow these rules will cause silent runtime failures, broken reactivity, serialization errors, or loaders/actions that never execute.**

</critical_reminders>
