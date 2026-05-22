---
name: solid-core-utilities
description: "SolidJS utilities: Context API, props manipulation (mergeProps/splitProps), JSX attributes (class/classList, events, refs), lifecycle (onMount/onCleanup), reactive utilities (batch/untrack/startTransition), store utilities."
---

# SolidJS Utilities

## Context API

Use `createContext` to create context. `Provider` component wraps children and passes `value`. `useContext` consumes context.

```tsx
import { createContext, useContext, createSignal } from "solid-js";

// Create context
const ThemeContext = createContext();

// Provider with signal
function ThemeProvider(props) {
  const [theme, setTheme] = createSignal("light");
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {props.children}
    </ThemeContext.Provider>
  );
}

// Custom hook with error handling
function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}

// Use in component
function Component() {
  const { theme, setTheme } = useTheme();
  return <div class={theme()}>Content</div>;
}
```

## Props

- Props are reactive - access properties directly
- Use `mergeProps` to combine props with defaults
- Use `splitProps` to separate props
- Props with `default` or `initial` prefix are common for one-time initialization; the linter allows this pattern without explicit `untrack`

```tsx
import { mergeProps, splitProps } from "solid-js";

// Merge props
function Button(props) {
  const merged = mergeProps({ type: "button" }, props);
  return <button {...merged}>Click</button>;
}

// Split props
function Component(props) {
  const [local, others] = splitProps(props, ["name", "age"]);
  return <div {...others}>{local.name}</div>;
}

// Default/initial props (no tracking needed)
function Input(props) {
  const [value, setValue] = createSignal(props.initialValue);
  return <input value={value()} onInput={e => setValue(e.target.value)} />;
}
```

## children Helper

Use `children` helper for complex child manipulation. Prevents duplicate DOM creation.

```tsx
import { children } from "solid-js";

function Wrapper(props) {
  // Resolve children once (prevents duplicate DOM)
  const resolved = children(() => props.children);
  
  // Reuse resolved children multiple times
  return (
    <div>
      {resolved()}
      <div>Duplicate: {resolved()}</div>
    </div>
  );
}
```

**When to use:**
- Accessing `props.children` multiple times
- Accessing `props.children` outside tracking scope
- Resolving/transforming children before use

**Important:** `children` helper evaluates immediately - use conditionally for conditional rendering:

```tsx
// ❌ Always evaluates
const resolved = children(() => props.children);
<Show when={visible()}>{resolved()}</Show>

// ✅ Conditional evaluation
const resolved = children(() => visible() && props.children);
```

**Array normalization:**
```tsx
const resolved = children(() => props.children);
const array = resolved.toArray(); // Normalize to array
```

## JSX Attributes

### class and classList

```tsx
// Static class
<div class="active" />

// Dynamic class
<div class={isActive() ? "active" : undefined} />

// classList object
<div
  classList={{
    active: isActive(),
    disabled: isDisabled(),
    "large-text": size() === "large"
  }}
/>

// Signal classList
const [classes, setClasses] = createSignal({});
<div classList={classes()} />
```

### Event Handlers

```tsx
// onClick, onInput, etc. (lowercase 'on')
<button onClick={handleClick}>Click</button>
<input onInput={e => console.log(e.target.value)} />

// Event delegation with on:eventName
<button on:click={handler} />
<div on:mousedown={handler} />
```

### Other Attributes

```tsx
// ref callback
let inputEl;
<input ref={inputEl} />

// style object (reactive)
<div style={{ color: color(), fontSize: "14px" }} />

// innerHTML (dangerous, use carefully)
<div innerHTML={htmlContent()} />

// use:* directives
<div use:someDirective={arg} />
```

### Refs and Directives

- Use `ref` attribute to access DOM elements directly
- `ref` can be a variable or a callback function
- In TypeScript, use `let myElement!: HTMLDivElement;` for definitive assignment
- Signal setters or callbacks can be used as refs for dynamic elements
- Forward refs by passing `props.ref` to child's element
- Directives (`use:`) attach reusable behaviors to DOM elements
  - Function signature: `(element: Element, accessor: () => any): void`
  - Can have multiple directives on an element
  - Can pass reactive data to accessor

```tsx
import { createSignal, Show } from "solid-js";

// Basic ref
let myInput!: HTMLInputElement;
<input ref={myInput} />;

// Callback ref
let myDiv;
<div ref={(el) => (myDiv = el)}>Content</div>;

// Signal as ref
const [show, setShow] = createSignal(false);
let element!: HTMLParagraphElement;
<Show when={show()}>
  <p ref={element}>This is the ref element</p>
</Show>;

// Forwarding refs
function ChildComponent(props) {
  return <input ref={props.ref} />;
}
function ParentComponent() {
  let inputRef;
  return <ChildComponent ref={inputRef} />;
}

// Custom directive
function myDirective(element: Element, accessor: () => any) {
  createEffect(() => {
    element.textContent = accessor();
  });
}
<div use:myDirective={mySignal()}></div>;
```

## Lifecycle

```tsx
import { onMount, onCleanup, createSignal } from "solid-js";

function Component() {
  const [data, setData] = createSignal(null);

  // Runs once when component mounts
  onMount(async () => {
    const fetchedData = await fetchData();
    setData(fetchedData);
  });

  // Runs when component unmounts or effect re-runs
  onCleanup(() => {
    // Cleanup subscriptions, timers, etc.
    subscription.unsubscribe();
  });
}
```

## Reactive Utilities

### batch

Batch multiple updates - effects run once at the end:

```tsx
import { batch } from "solid-js";

const [up1, setUp1] = createSignal(1);
const [up2, setUp2] = createSignal(2);
const [up3, setUp3] = createSignal(3);
const down = createMemo(() => up1() + up2() + up3());
createEffect(() => console.log("Downstream:", down()));

// Batch multiple updates
batch(() => {
  setUp1(10);
  setUp2(10);
  setUp3(10);
  // All updates processed together, 'down' recomputes once
});
```

### untrack

Access signal without tracking:

```tsx
import { untrack } from "solid-js";

// Access signal without tracking
const value = untrack(() => props.staticValue);

// Props with default/initial prefix are auto-untracked
function MyComponent(props: { initialName: string }) {
  const [name, setName] = createSignal(props.initialName); // ✅ OK
  return <div>{name()}</div>;
}
```

### startTransition

Mark non-urgent updates:

```tsx
import { startTransition } from "solid-js";

const [filter, setFilter] = createSignal("");
const [search, setSearch] = createSignal("");

startTransition(() => {
  // Non-urgent updates
  setFilter(filterValue);
  setSearch(searchValue);
});
```

### from

Convert promises/observables to signals:

```tsx
import { from } from "solid-js";

const data = from(fetch("/api/data").then(r => r.json()));
```

### mapArray / indexArray

Transform arrays with fine-grained reactivity:

```tsx
import { mapArray, indexArray } from "solid-js";

// Map by item identity
const mapped = mapArray(items, item => item.id);

// Map by index
const indexed = indexArray(items, item => item.id);
```

### on

Execute effect when specific signal changes:

```tsx
import { on } from "solid-js";

createEffect(on(count, (value) => {
  console.log("Count changed to:", value);
}, { defer: true }));
```

### catchError

Catch errors in reactive contexts:

```tsx
import { catchError } from "solid-js";

const data = catchError(() => {
  return riskyOperation();
}, (err) => {
  console.error("Error:", err);
  return defaultValue;
});
```

## Store Utilities

### produce

Mutate store data imperatively:

```tsx
import { produce } from "solid-js/store";

setStore("user", produce(user => {
  user.name = "New Name";
  user.age = 31;
}));
```

### reconcile

Merge new data efficiently (only updates changed fields):

```tsx
import { reconcile } from "solid-js/store";

const newData = fetchNewData();
setStore("items", reconcile(newData)); // Only updates changed items
```

### unwrap

Get plain object snapshot:

```tsx
import { unwrap } from "solid-js/store";

const plainData = unwrap(store); // Plain JS object
// Use for serialization, API calls, etc.
```

### createMutable

Create mutable store (use sparingly):

```tsx
import { createMutable } from "solid-js/store";

const state = createMutable({ count: 0 });

// Direct mutation
state.count++;

// No setter needed, but less reactive control
```

## Advanced Patterns

### createResource

Manages asynchronous data fetching:

```tsx
import { createResource, Suspense } from "solid-js";

async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

function DataComponent(props: { userId: string }) {
  const [data, { mutate, refetch }] = createResource(
    () => props.userId,
    fetchUser,
    {
      initialValue: null,
      name: "user"
    }
  );

  return (
    <Suspense fallback={<div>Loading user...</div>}>
      <div>{data()?.name}</div>
      <button onClick={() => refetch()}>Refetch</button>
    </Suspense>
  );
}
```

### Portals

Renders children into a different DOM node:

```tsx
import { Portal } from "solid-js/web";

<Portal mount={document.body}>
  <Modal>Content</Modal>
</Portal>
```

### Lazy Components

```tsx
import { lazy, Suspense } from "solid-js";

const LazyComponent = lazy(() => import("./Component"));

<Suspense fallback={<Loading />}>
  <LazyComponent />
</Suspense>
```

## Best Practices

1. Create custom context hooks for type safety and error handling
2. Use `mergeProps` for default props
3. Use `splitProps` to separate local and forwarded props
4. Use `batch` when making multiple related updates
5. Use `untrack` to read values without tracking
6. Use `produce` for complex store mutations
7. Use `reconcile` when merging fetched data
8. Use `unwrap` when serializing or sending to API
