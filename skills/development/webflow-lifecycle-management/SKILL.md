---
name: webflow-lifecycle-management
description: Manage module lifecycles, cleanup, and page transitions. Use when handling component initialization, destruction, or animating page entrances and exits.
---

# Webflow Lifecycle Management

This skill covers the usage of lifecycle hooks to ensure proper resource management and smooth page transitions.

## Lifecycle Hooks

Import these from `@/modules/_`:

- `onMount(fn)`: Runs once when the module is initialized and added to the DOM.
- `onDestroy(fn)`: Runs when the module is removed from the DOM. **CRITICAL** for preventing memory leaks.
- `onPageIn(fn)`: Runs during the page entrance transition. Usually used for animations.
- `onPageOut(fn, options)`: Runs during the page exit transition.

## Example Pattern

```typescript
import { onMount, onDestroy, onPageIn, onPageOut } from "@/modules/_";
import gsap from "@lib/gsap";

export default function (element: HTMLElement, dataset: DOMStringMap) {
  onMount(() => {
    // Initialize: add event listeners, start observers
  });

  onPageIn(async () => {
    // Animate in
    await gsap.from(element, { opacity: 0, y: 20, duration: 0.8 });
  });

  onPageOut(async () => {
    // Animate out
    await gsap.to(element, { opacity: 0, duration: 0.4 });
  }, { element }); // Pass { element } to only animate if visible

  onDestroy(() => {
    // Cleanup: remove listeners, destroy GSAP instances, stop observers
  });
}
```
