---
name: solid-core-advanced-components
description: "SolidJS advanced components: SuspenseList for coordinating multiple Suspense boundaries, NoHydration for skipping hydration of static content."
---

# Advanced Components

## SuspenseList

Coordinates multiple parallel Suspense and SuspenseList components. Controls reveal order to reduce layout thrashing.

```tsx
import { SuspenseList } from "solid-js";

<SuspenseList revealOrder="forwards" tail="collapsed">
  <ProfileDetails user={resource.user} />
  <Suspense fallback={<h2>Loading posts...</h2>}>
    <ProfileTimeline posts={resource.posts} />
  </Suspense>
  <Suspense fallback={<h2>Loading fun facts...</h2>}>
    <ProfileTrivia trivia={resource.trivia} />
  </Suspense>
</SuspenseList>
```

### Props

**revealOrder**: `"forwards" | "backwards" | "together"`

- `"forwards"` (default): Reveals each item once previous item finished rendering
- `"backwards"`: Reveals each item once next item finished rendering
- `"together"`: Reveals all items at the same time

**tail**: `"collapsed" | "hidden"` (optional)

- Controls fallback display behavior

### Use Cases

- Coordinating multiple async sections
- Preventing layout shift
- Controlling loading sequence
- Managing parallel data fetching

**Note:** SuspenseList is experimental and doesn't have full SSR support yet.

## NoHydration

Prevents client-side hydration for its children. Useful for static content that doesn't need reactivity.

```tsx
import { NoHydration } from "solid-js/web";

function Example() {
  return (
    <div>
      <InteractiveComponent />
      <NoHydration>
        <StaticContent />
      </NoHydration>
    </div>
  );
}
```

**Behavior:**
- Renders normally on server (contributes to HTML)
- Skips hydration on client (no event listeners, no reactive state)
- Reduces bundle size and improves performance

**Use cases:**
- Static content (markdown, documentation)
- Server-only rendered sections
- Performance optimization for non-interactive content
- Reducing client-side JavaScript

**Important:**
- Content inside `<NoHydration>` is not hydrated on the client
- Reactive updates and event handlers won't run in that subtree on the client
- Use `<Hydration>` to resume hydration for interactive islands when needed

## Best Practices

1. **SuspenseList:**
   - Use to coordinate multiple Suspense boundaries
   - Choose `revealOrder` based on UX needs
   - Consider layout stability when choosing order

2. **NoHydration:**
   - Use for truly static content
   - Don't use for interactive components
   - Reduces client-side overhead significantly
