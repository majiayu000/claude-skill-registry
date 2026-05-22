---
name: solid-core-control-flow
description: "SolidJS control flow: Show for conditionals, Switch/Match for multiple conditions, For/Index for lists, Dynamic for dynamic components, Suspense for async data."
---

# SolidJS Control Flow

## Show Component

Renders children when `when` condition is true. Use `fallback` prop for false condition.

```tsx
import { Show } from "solid-js";

<Show when={data()} fallback={<div>Loading...</div>}>
  <div>{data().name}</div>
</Show>

// Nested Show
<Show when={user()}>
  <Show when={user().admin}>
    <AdminPanel />
  </Show>
</Show>
```

## Switch and Match

Use for multiple, mutually exclusive conditions:

```tsx
import { Switch, Match } from "solid-js";

<Switch fallback={<div>Default</div>}>
  <Match when={status() === "loading"}>
    <Loading />
  </Match>
  <Match when={status() === "error"}>
    <Error />
  </Match>
  <Match when={status() === "success"}>
    <Content />
  </Match>
</Switch>
```

- `<Switch>` wraps multiple `<Match>` components
- First `<Match when={condition}>` that is true renders its children
- `<Switch fallback={...}>` for no matching conditions

## For and Index

### For

Use when order/length may change frequently (complex data):
- `item` is value
- `index` is signal: `index()`

```tsx
import { For } from "solid-js";

<For each={items()}>
  {(item, index) => (
    <div>
      {item.name} - {index()} {/* index is signal */}
    </div>
  )}
</For>
```

### Index

Use when order/length is stable, content changes frequently (primitives, inputs):
- `item` is signal: `item()`
- `index` is number

```tsx
import { Index } from "solid-js";

<Index each={inputs()}>
  {(input, index) => (
    <input value={input()} onInput={...} />
    // input is signal, index is number
  )}
</Index>
```

**When to use:**
- `<For>`: Dynamic lists where items may be added/removed/reordered
- `<Index>`: Stable lists where content changes (e.g., form inputs, primitives)

## Dynamic Component

Render components dynamically:

```tsx
import { Dynamic } from "solid-js";

<Dynamic component={componentName()} props={props()} />
```

## Suspense

Handles async data and lazy-loaded components:

```tsx
import { Suspense } from "solid-js";

<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>

// Nested Suspense
<Suspense fallback={<PageSkeleton />}>
  <Suspense fallback={<TitleSkeleton />}>
    <Title />
  </Suspense>
  <Content />
</Suspense>
```

**Best practices:**
- Wrap async data fetching components
- Use nested Suspense for independent loading states
- Provide meaningful fallback UI

## Error Boundaries

Catch errors in component tree:

```tsx
import { ErrorBoundary } from "solid-js";

<ErrorBoundary fallback={(err, reset) => (
  <div>
    Error: {err.message}
    <button onClick={reset}>Retry</button>
  </div>
)}>
  <Component />
</ErrorBoundary>
```

- `fallback` prop renders UI on error
- `reset` function to retry rendering

## Best Practices

1. Use `<Show>` for simple conditionals
2. Use `<Switch>`/<`Match>` for multiple mutually exclusive conditions
3. Use `<For>` for dynamic lists (items may change)
4. Use `<Index>` for stable lists (content changes, not order)
5. Always wrap async components with `<Suspense>`
6. Use `<ErrorBoundary>` for error handling
7. Provide meaningful fallback UI

