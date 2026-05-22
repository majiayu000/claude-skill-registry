---
name: solid-core-advanced-utilities
description: "SolidJS advanced utilities: createRoot for manual disposal, createUniqueId for SSR-safe IDs, useTransition for batching async updates, observable for RxJS interop, modifyMutable for batch updates."
---

# Advanced Utilities

## createRoot

Creates a new owned context requiring explicit disposal. Essential for manual memory management and testing.

```tsx
import { createRoot } from "solid-js";

createRoot((dispose) => {
  const [count, setCount] = createSignal(0);
  
  createEffect(() => {
    console.log(count());
  });
  
  // Explicitly dispose when done
  dispose();
});
```

**Use cases:**
- Testing (ensures cleanup)
- Manual memory management
- Nested tracking scopes
- Top-level code wrapping

**Example in tests:**
```tsx
test("counter works", () => {
  createRoot((dispose) => {
    const { count, increment } = createCounter();
    expect(count()).toBe(0);
    increment();
    expect(count()).toBe(1);
    dispose(); // Clean up
  });
});
```

**Returning values:**
```tsx
const counter = createRoot((dispose) => {
  const [count, setCount] = createSignal(0);
  return {
    value: count,
    increment: () => setCount(c => c + 1),
    dispose
  };
});
```

## createUniqueId

Generates SSR-safe unique IDs. Stable across server and client renders.

```tsx
import { createUniqueId } from "solid-js";

function Input(props: { id?: string }) {
  const id = props.id ?? createUniqueId();
  return (
    <>
      <label for={id}>Name</label>
      <input id={id} />
    </>
  );
}
```

**Requirements:**
- Must be called same number of times on server and client
- Cannot use conditionally with `isServer` or inside `<NoHydration>`
- Not cryptographically secure
- Not suitable for distributed systems

**Use cases:**
- Form element IDs
- Accessibility (aria-labelledby, etc.)
- SSR-compatible unique identifiers

## useTransition

Batches async updates, deferring commit until all async processes complete. Tied to Suspense.

```tsx
import { useTransition } from "solid-js";

const [isPending, start] = useTransition();

// Check if transitioning
isPending();

// Wrap in transition
start(() => {
  setSignal(newValue);
  // transition is done
});
```

**Features:**
- Batches async updates in transaction
- Tracks resources read under Suspense boundaries
- `isPending()` indicates transition state
- Returns promise when transition completes

**Use case:** Smooth UI transitions with async data loading.

## observable

Converts signals to Observables for RxJS integration.

```tsx
import { observable } from "solid-js";
import { from } from "rxjs";

const [s, set] = createSignal(0);
const obsv$ = from(observable(s));

obsv$.subscribe((v) => console.log(v));
```

**Use case:** Integrating with RxJS or other Observable libraries.

## modifyMutable

Batches multiple mutable store changes. Updates multiple fields in one render cycle.

```tsx
import { modifyMutable, reconcile, produce } from "solid-js/store";

const state = createMutable({
  user: {
    firstName: "John",
    lastName: "Smith",
  },
});

// Multiple updates trigger multiple renders
state.user.firstName = "Jane";
state.user.lastName = "Doe";

// Batch updates with modifyMutable
modifyMutable(state.user, reconcile({
  firstName: "Jane",
  lastName: "Doe",
}));

// Or with produce
modifyMutable(state, produce((state) => {
  state.user.firstName = "Jane";
  state.user.lastName = "Doe";
}));
```

**Benefits:**
- Single render cycle for multiple changes
- Works with `reconcile` and `produce`
- Better performance for complex updates

## getOwner / runWithOwner

Advanced ownership patterns for nested contexts.

```tsx
import { getOwner, runWithOwner } from "solid-js";

const owner = getOwner();

// Run code with specific owner
runWithOwner(owner, () => {
  // Code runs in owner's context
});
```

**Use case:** Advanced scenarios requiring specific owner context (rare).

## Best Practices

1. **createRoot:**
   - Always use in tests for proper cleanup
   - Use for manual memory management
   - Return dispose function when creating reusable primitives

2. **createUniqueId:**
   - Use for form elements and accessibility
   - Call same number of times on server/client
   - Don't use conditionally based on server/client

3. **useTransition:**
   - Use with Suspense boundaries
   - Check `isPending()` for loading states
   - Batch related async updates

4. **modifyMutable:**
   - Use for batch updates to mutable stores
   - Combine with `reconcile` or `produce`
   - Prefer over multiple direct mutations

