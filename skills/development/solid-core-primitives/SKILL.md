---
name: solid-core-primitives
description: "Core SolidJS primitives: signals use getter functions count(), components run once (no re-renders), effects track automatically, stores use direct property access, memos for computed values. Fine-grained reactivity means targeted DOM updates."
---

# Core SolidJS Primitives

## Fine-Grained Reactivity

Solid uses **fine-grained reactivity** - only the specific DOM nodes that depend on changed signals are updated. Unlike React, components don't re-execute on state changes.

**Key concepts:**
- Components run **once** on initialization
- Only DOM elements directly associated with changed signals update
- No component re-renders
- Targeted, specific updates for better performance

**Example:**
```tsx
function Counter() {
  const [count, setCount] = createSignal(0);
  const [name, setName] = createSignal("John");
  
  return (
    <div>
      <span>{count()}</span> {/* Only this updates when count changes */}
      <span>{name()}</span>   {/* Only this updates when name changes */}
    </div>
  );
}
```

When `count` changes, only the first `<span>` updates, not the entire component.

## Signals

- Always call the getter function: `count()` not `count`
- Setters accept value or function: `setCount(5)` or `setCount(prev => prev + 1)`
- Signals only track when accessed within a tracking scope (JSX, effects, memos)
- Initialization doesn't cause tracking - access must be in reactive context
- Use `equals` option for custom equality checking
- Use `name` option for debugging (dev mode only)

```tsx
import { createSignal } from "solid-js";

// Basic signal
const [count, setCount] = createSignal(0);
console.log(count()); // ✅ Correct - call getter
console.log(count);   // ❌ Wrong - returns function

// Setter with function
setCount(prev => prev + 1);

// Custom equality
const [data, setData] = createSignal({ value: 1 }, { 
  equals: (prev, next) => prev.value === next.value 
});

// Named signal for debugging
const [user, setUser] = createSignal(null, { name: "user" });
```

## Components

- Components run **once** on initialization - setup happens in function body
- Component functions don't re-run on state changes - Solid uses fine-grained reactivity
- Reactive updates happen automatically through signals/stores accessed in JSX
- Component names must start with capital letter
- Conditional rendering should live in JSX or a reactive scope, not in the component body

```tsx
function Counter() {
  const [count, setCount] = createSignal(0);
  
  // This runs ONCE on mount - not reactive
  console.log("Component rendered");
  
  // Conditional rendering must be in JSX
  return (
    <div>
      <span>{count()}</span>
      <button onClick={() => setCount(prev => prev + 1)}>Increment</button>
    </div>
  );
}
```

## Effects

- Use `createEffect` for side effects (DOM manipulation, API calls, subscriptions)
- Effects run once initially, then whenever dependencies change
- Avoid setting signals that are read in the same effect unless guarded to prevent loops
- Use `createMemo` for computed values instead
- No manual dependency arrays - tracking is automatic
- Nested effects track independently

```tsx
import { createEffect, onCleanup, createSignal } from "solid-js";

// Basic effect
createEffect(() => {
  console.log("Count:", count());
});

// Effect with cleanup
createEffect(() => {
  const timer = setInterval(() => console.log("tick"), 1000);
  onCleanup(() => clearInterval(timer));
});

// Nested effects
createEffect(() => {
  console.log("Outer");
  createEffect(() => {
    console.log("Inner", count()); // Only inner tracks count
  });
});
```

## Stores

- Access properties directly: `store.user` not `store.user()`
- Use path syntax for updates: `setStore("key", value)`
- Signals created lazily when accessed in tracking scope
- Fine-grained reactivity - only updated properties trigger updates
- Use `produce` for complex mutations
- Use `reconcile` for merging new data efficiently
- Use `unwrap` to get plain object snapshot

```tsx
import { createStore, produce, reconcile, unwrap } from "solid-js/store";

const [store, setStore] = createStore({ 
  user: { name: "John", age: 30 },
  items: [1, 2, 3]
});

// Direct access
console.log(store.user.name); // ✅ Direct access

// Path syntax updates
setStore("user", "name", "Jane");
setStore("items", 0, 10); // Update array item
setStore("items", store.items.length, 4); // Append

// Multiple updates with produce
setStore("user", produce(user => {
  user.name = "Bob";
  user.age = 31;
}));

// Merge with reconcile
setStore("items", reconcile([1, 2, 3, 4])); // Only adds 4

// Get plain object
const plain = unwrap(store);
```

## Memos and Computed Values

- Use `createMemo` for computed values that depend on other reactive values
- Memos cache results and only recompute when dependencies change
- Prefer memos over effects for derived state
- `createComputed` runs synchronously before render (advanced use)

```tsx
import { createMemo, createSignal, createComputed } from "solid-js";

const [count, setCount] = createSignal(0);
const doubled = createMemo(() => count() * 2);

// Computed with initial value
const sum = createComputed((prev) => {
  const current = count();
  return (prev || 0) + current;
}, 0);
```

## Advanced Primitives

### createComputed

Runs synchronously before render (use sparingly):

```tsx
import { createComputed } from "solid-js";

function UserEditor(props: { user: User }) {
  const [formData, setFormData] = createStore({ name: "" });
  
  // Sync store with props before render
  createComputed(() => {
    setFormData("name", props.user.name);
  });
  
  return <input value={formData.name} />;
}
```

### createRenderEffect

Like `createEffect` but runs during render phase:

```tsx
import { createRenderEffect } from "solid-js";

createRenderEffect(() => {
  // Runs during render, before DOM updates
  console.log("Render effect:", count());
});
```

### createSelector

Efficiently track specific values in arrays:

```tsx
import { createSelector } from "solid-js";

const isSelected = createSelector(() => selectedId());
<For each={items()}>
  {(item) => (
    <div class={isSelected(item.id) ? "selected" : ""}>
      {item.name}
    </div>
  )}
</For>
```

### createDeferred

Defer updates for smooth animations:

```tsx
import { createDeferred } from "solid-js";

const deferred = createDeferred(() => searchQuery(), { timeoutMs: 200 });

// deferred() updates after user stops typing
```

### createReaction

Track dependencies without re-executing immediately:

```tsx
import { createReaction } from "solid-js";

const track = createReaction(() => {
  // Runs when dependencies change, but doesn't track on creation
});

track(() => {
  // Track these signals
  count();
  name();
});
```

## Key Differences from React

1. **No re-renders**: Components run once, updates are fine-grained
2. **No hooks**: Use primitives like `createSignal`, `createEffect` (not `useState`, `useEffect`)
3. **Accessor functions**: Signals must be called: `count()` not `count`
4. **Direct store access**: `store.user` not `store.user()`
5. **Automatic tracking**: No dependency arrays needed
