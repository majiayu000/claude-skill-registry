---
name: solid-core-secondary-primitives
description: "SolidJS secondary primitives: createComputed for immediate sync, createDeferred for idle updates, createReaction for one-time tracking, createRenderEffect for DOM operations, createSelector for optimized equality."
metadata:
  globs:
    - "**/*computed*"
    - "**/*deferred*"
    - "**/*reaction*"
    - "**/*selector*"
    - "**/*render-effect*"
---

# SolidJS Secondary Primitives

Complete guide to advanced reactive primitives in SolidJS. These primitives provide fine-grained control over reactivity timing and execution.

## createComputed - Immediate Synchronization

`createComputed` creates a reactive computation that runs **before** the rendering phase. Used to synchronize state before rendering begins.

```tsx
import { createComputed } from "solid-js";
import { createStore } from "solid-js/store";

function UserEditor(props: { user: User }) {
  const [formData, setFormData] = createStore({ name: "" });

  // Update store synchronously when props change
  // Prevents a second render cycle
  createComputed(() => {
    setFormData("name", props.user.name);
  });

  return (
    <form>
      <h1>Editing: {formData.name}</h1>
      <input
        value={formData.name}
        onInput={(e) => setFormData("name", e.currentTarget.value)}
      />
    </form>
  );
}
```

**Key characteristics:**
- Runs **before** rendering phase
- Synchronous execution
- Prevents extra render cycles
- Receives previous value as argument

**Use cases:**
- Synchronizing props to local state
- Building custom primitives
- Immediate reactive updates
- State normalization

**When to use vs createEffect:**
- `createComputed`: Need synchronous updates before render
- `createEffect`: Need side effects after render completes

## createDeferred - Idle Updates

`createDeferred` creates a readonly that only notifies downstream changes when the browser is idle. Optimizes performance by batching non-critical changes.

```tsx
import { createDeferred, createSignal } from "solid-js";

function SearchComponent() {
  const [searchTerm, setSearchTerm] = createSignal("");
  
  // Defer updates until browser is idle
  const deferredSearch = createDeferred(searchTerm, {
    timeoutMs: 500, // Max wait time
  });

  // This only updates when browser is idle
  return <div>Searching: {deferredSearch()}</div>;
}
```

**Options:**
- `timeoutMs`: Maximum time to wait before forcing update (default: no timeout)
- `equals`: Custom equality function
- `name`: Debug name

**Use cases:**
- Search input debouncing
- Non-critical UI updates
- Performance optimization
- Reducing render frequency

**Example with timeout:**

```tsx
const deferred = createDeferred(source, {
  timeoutMs: 1000, // Force update after 1 second even if not idle
});
```

## createReaction - One-Time Tracking

`createReaction` separates tracking from execution. Registers a side effect that runs the **first time** the tracked expression changes.

```tsx
import { createReaction, createSignal } from "solid-js";

function Component() {
  const [s, set] = createSignal("start");

  // Create reaction that runs once on first change
  const track = createReaction(() => {
    console.log("Something changed!");
  });

  // Track the signal
  track(() => s());

  // First change triggers reaction
  set("end"); // "Something changed!"

  // Second change doesn't trigger (reaction already ran)
  set("final"); // No output

  // Need to call track() again to re-enable
  track(() => s());
  set("again"); // "Something changed!"
}
```

**Key characteristics:**
- Runs **once** on first dependency change
- Separates tracking from execution
- Must call tracking function again to re-enable

**Use cases:**
- One-time initialization
- Custom tracking logic
- Advanced reactive patterns
- Separating concerns

**Pattern: Lazy initialization:**

```tsx
const track = createReaction(() => {
  initializeExpensiveOperation();
});

// Only initializes when first accessed
track(() => someSignal());
```

## createRenderEffect - DOM Operations

`createRenderEffect` creates a reactive computation that runs **synchronously during rendering**, before elements are mounted.

```tsx
import { createRenderEffect, createSignal } from "solid-js";

function Counter() {
  const [count, setCount] = createSignal(0);

  // Runs immediately during render phase
  // Before elements are mounted
  createRenderEffect(() => {
    console.log("Count:", count());
    // Can manipulate DOM here
  });

  return (
    <div>
      <p>Count: {count()}</p>
      <button onClick={() => setCount(count() + 1)}>Increment</button>
    </div>
  );
}
```

**Execution timing:**
- **Initial run**: Synchronously during render, before mount, refs not set
- **Subsequent runs**: After pure computations, once per batch
- **SSR**: Runs once on server, then on client after hydration

**Use cases:**
- DOM manipulation during render
- Immediate effects
- Ref-independent effects
- Custom rendering logic

**When to use vs createEffect:**
- `createRenderEffect`: Need immediate execution during render
- `createEffect`: Need execution after render completes

**Example: DOM manipulation:**

```tsx
function Component() {
  const [value, setValue] = createSignal(0);

  createRenderEffect(() => {
    // Manipulate DOM immediately
    document.title = `Count: ${value()}`;
  });

  return <div>{value()}</div>;
}
```

## createSelector - Optimized Equality

`createSelector` creates a parameterized derived boolean signal optimized for selection states. Reduces updates from *n* to 2.

```tsx
import { createSelector, For } from "solid-js";

function List() {
  const [selectedId, setSelectedId] = createSignal<number>();
  const isSelected = createSelector(selectedId);

  return (
    <For each={list()}>
      {(item) => (
        <li
          classList={{ active: isSelected(item.id) }}
          onClick={() => setSelectedId(item.id)}
        >
          {item.name}
        </li>
      )}
    </For>
  );
}
```

**Performance benefit:**
- Without selector: *n* DOM updates (one per item)
- With selector: 2 DOM updates (previous + current)

**Custom equality:**

```tsx
const isSelected = createSelector(selectedId, (key, value) => {
  // Custom comparison
  return key === value.id;
});
```

**Use cases:**
- Selection states
- Active items
- Dropdown menus
- Tab navigation
- List highlighting

**Example: Tab navigation:**

```tsx
function Tabs() {
  const [activeTab, setActiveTab] = createSignal("home");
  const isActive = createSelector(activeTab);

  return (
    <nav>
      <For each={tabs}>
        {(tab) => (
          <button
            classList={{ active: isActive(tab.id) }}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
          </button>
        )}
      </For>
    </nav>
  );
}
```

## Comparison Table

| Primitive | Timing | Use Case |
|-----------|--------|----------|
| `createComputed` | Before render | Synchronize state before render |
| `createDeferred` | Browser idle | Defer non-critical updates |
| `createReaction` | First change only | One-time side effects |
| `createRenderEffect` | During render | Immediate DOM operations |
| `createSelector` | On change | Optimized selection state |

## When to Use Each

### createComputed
- ✅ Synchronizing props to local state
- ✅ Building custom primitives
- ✅ Immediate state updates

### createDeferred
- ✅ Search input debouncing
- ✅ Non-critical UI updates
- ✅ Performance optimization

### createReaction
- ✅ One-time initialization
- ✅ Custom tracking patterns
- ✅ Lazy loading

### createRenderEffect
- ✅ DOM manipulation during render
- ✅ Immediate effects
- ✅ Ref-independent operations

### createSelector
- ✅ Selection states
- ✅ Active item tracking
- ✅ Performance-critical lists

## Common Patterns

### Synchronizing Props

```tsx
function Editor(props: { data: Data }) {
  const [local, setLocal] = createStore({});

  // Sync props to local state before render
  createComputed(() => {
    setLocal(reconcile(props.data));
  });

  return <form>...</form>;
}
```

### Debounced Search

```tsx
function Search() {
  const [query, setQuery] = createSignal("");
  const deferredQuery = createDeferred(query, { timeoutMs: 300 });

  // Only search when deferred updates
  createEffect(() => {
    search(deferredQuery());
  });

  return <input onInput={(e) => setQuery(e.target.value)} />;
}
```

### Optimized List Selection

```tsx
function ItemList() {
  const [selected, setSelected] = createSignal<number>();
  const isSelected = createSelector(selected);

  return (
    <For each={items()}>
      {(item) => (
        <div
          classList={{ selected: isSelected(item.id) }}
          onClick={() => setSelected(item.id)}
        >
          {item.name}
        </div>
      )}
    </For>
  );
}
```

### One-Time Initialization

```tsx
function Component() {
  const [ready, setReady] = createSignal(false);
  
  const track = createReaction(() => {
    initializeExpensiveOperation();
    setReady(true);
  });

  // Only initializes when first accessed
  track(() => someCondition());
  
  return <Show when={ready()}>Content</Show>;
}
```

## Best Practices

1. **Use createComputed for sync:**
   - When you need state synchronized before render
   - Prevents extra render cycles

2. **Use createDeferred for performance:**
   - Non-critical UI updates
   - Search/filter inputs
   - Large list rendering

3. **Use createReaction sparingly:**
   - One-time side effects only
   - Custom tracking patterns
   - Advanced use cases

4. **Use createRenderEffect for DOM:**
   - Immediate DOM operations
   - Before mount effects
   - Ref-independent code

5. **Use createSelector for lists:**
   - Selection states
   - Active items
   - Performance-critical UI

## Summary

- **createComputed**: Immediate sync before render
- **createDeferred**: Idle-time updates for performance
- **createReaction**: One-time tracking and execution
- **createRenderEffect**: Immediate effects during render
- **createSelector**: Optimized selection state (n → 2 updates)

