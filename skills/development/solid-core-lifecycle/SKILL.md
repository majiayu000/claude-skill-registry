---
name: solid-core-lifecycle
description: "SolidJS lifecycle: onMount for DOM access after mount, onCleanup for resource disposal, effect lifecycle management, component vs effect cleanup."
metadata:
  globs:
    - "**/*lifecycle*"
    - "**/*mount*"
    - "**/*cleanup*"
---

# SolidJS Lifecycle Management

Complete guide to managing component and effect lifecycle in SolidJS. Understanding lifecycle is essential for proper resource cleanup and avoiding memory leaks.

## onMount - Component Mounting

`onMount` runs code after components mount to the DOM. Perfect for accessing refs, setting up third-party libraries, and one-time initializations.

```tsx
import { onMount } from "solid-js";

function MyComponent() {
  let ref: HTMLButtonElement;

  // Runs after component mounts to DOM
  onMount(() => {
    ref.disabled = true;
    // Access DOM elements safely
    // Initialize third-party libraries
    // Set up one-time event listeners
  });

  return <button ref={ref}>Focus me!</button>;
}
```

**Key characteristics:**
- Runs **once** after initial render
- Non-tracking (equivalent to `createEffect` with no dependencies)
- Perfect for DOM access via refs
- Ideal for third-party library initialization

**Use cases:**
- Accessing DOM refs
- Initializing libraries (charts, maps, etc.)
- Setting up one-time event listeners
- Fetching initial data

## onCleanup - Resource Disposal

`onCleanup` registers cleanup methods that execute when components unmount or tracking scopes dispose. Essential for preventing memory leaks.

```tsx
import { createSignal, onCleanup } from "solid-js";

function Component() {
  const [count, setCount] = createSignal(0);

  const handleClick = () => setCount((value) => value + 1);

  // Add event listener
  document.addEventListener("click", handleClick);

  // Cleanup when component unmounts
  onCleanup(() => {
    document.removeEventListener("click", handleClick);
  });

  return <main>Document has been clicked {count()} times</main>;
}
```

**When cleanup runs:**
- **In components**: When component unmounts
- **In effects**: When effect is disposed or recalculated
- **In memos**: When memo is disposed
- **In roots**: When root is disposed

## Effect Lifecycle

Effects have their own lifecycle. Cleanup runs before effect re-executes:

```tsx
import { createEffect, onCleanup, createSignal } from "solid-js";

function Component() {
  const [id, setId] = createSignal(1);

  createEffect(() => {
    const currentId = id();
    
    // Setup
    const subscription = subscribeToData(currentId);
    
    // Cleanup runs:
    // 1. Before effect re-executes (when id changes)
    // 2. When effect is disposed (component unmounts)
    onCleanup(() => {
      subscription.unsubscribe();
    });
  });

  return <button onClick={() => setId(id() + 1)}>Next</button>;
}
```

**Cleanup execution order:**
1. Previous cleanup runs (if effect re-executes)
2. Effect body runs
3. New cleanup registered

## Component Lifecycle vs Effect Lifecycle

**Component lifecycle:**
- Component function runs once on initialization
- `onMount` runs after DOM mount
- `onCleanup` runs on unmount
- No re-execution on state changes (fine-grained reactivity)

**Effect lifecycle:**
- Effect runs initially, then on dependency changes
- Cleanup runs before re-execution
- Cleanup runs on disposal

```tsx
function Component() {
  const [count, setCount] = createSignal(0);

  // Component body runs ONCE
  console.log("Component initialized");

  // Runs after mount
  onMount(() => {
    console.log("Component mounted");
  });

  // Runs on unmount
  onCleanup(() => {
    console.log("Component cleanup");
  });

  // Effect runs when count changes
  createEffect(() => {
    console.log("Effect runs:", count());
    
    onCleanup(() => {
      console.log("Effect cleanup");
    });
  });

  return <button onClick={() => setCount(count() + 1)}>Count: {count()}</button>;
}
```

## Cleanup Best Practices

### 1. Always Clean Up Event Listeners

```tsx
function Component() {
  const handleResize = () => {
    // Handle resize
  };

  window.addEventListener("resize", handleResize);
  
  onCleanup(() => {
    window.removeEventListener("resize", handleResize);
  });
}
```

### 2. Clean Up Subscriptions

```tsx
function Component() {
  const [data, setData] = createSignal(null);

  createEffect(() => {
    const subscription = observable.subscribe((value) => {
      setData(value);
    });

    onCleanup(() => {
      subscription.unsubscribe();
    });
  });
}
```

### 3. Clean Up Intervals/Timeouts

```tsx
function Component() {
  createEffect(() => {
    const interval = setInterval(() => {
      // Do something
    }, 1000);

    onCleanup(() => {
      clearInterval(interval);
    });
  });
}
```

### 4. Clean Up AbortControllers

```tsx
function Component() {
  createEffect(() => {
    const controller = new AbortController();

    fetch("/api/data", { signal: controller.signal })
      .then((res) => res.json())
      .then(setData);

    onCleanup(() => {
      controller.abort();
    });
  });
}
```

### 5. Multiple Cleanups

You can register multiple cleanups - they all run in reverse order:

```tsx
function Component() {
  onMount(() => {
    const listener1 = setupListener1();
    const listener2 = setupListener2();

    onCleanup(() => {
      listener2.cleanup();
    });

    onCleanup(() => {
      listener1.cleanup();
    });
    // Cleanup order: listener1, then listener2 (reverse registration)
  });
}
```

## Common Patterns

### Accessing Refs After Mount

```tsx
function Component() {
  let inputRef: HTMLInputElement;

  onMount(() => {
    // Safe to access ref after mount
    inputRef.focus();
    inputRef.select();
  });

  return <input ref={inputRef} />;
}
```

### Third-Party Library Initialization

```tsx
function ChartComponent() {
  let chartContainer: HTMLDivElement;
  let chartInstance: Chart;

  onMount(() => {
    // Initialize chart library
    chartInstance = new Chart(chartContainer, {
      // config
    });
  });

  onCleanup(() => {
    // Cleanup chart instance
    if (chartInstance) {
      chartInstance.destroy();
    }
  });

  return <div ref={chartContainer} />;
}
```

### Conditional Cleanup

```tsx
function Component() {
  createEffect(() => {
    let cleanup: (() => void) | undefined;

    if (someCondition()) {
      cleanup = setupSomething();
    }

    onCleanup(() => {
      if (cleanup) {
        cleanup();
      }
    });
  });
}
```

### Async Operations Cleanup

```tsx
function Component() {
  createEffect(() => {
    let cancelled = false;

    fetchData().then((data) => {
      if (!cancelled) {
        setData(data);
      }
    });

    onCleanup(() => {
      cancelled = true;
    });
  });
}
```

## Anti-Patterns to Avoid

### ❌ Don't Access Refs Outside onMount

```tsx
// ❌ Wrong - ref may not be attached yet
function Component() {
  let ref: HTMLDivElement;
  ref.focus(); // Error!
  return <div ref={ref} />;
}

// ✅ Correct
function Component() {
  let ref: HTMLDivElement;
  onMount(() => {
    ref.focus(); // Safe
  });
  return <div ref={ref} />;
}
```

### ❌ Don't Forget to Clean Up

```tsx
// ❌ Wrong - memory leak
function Component() {
  document.addEventListener("click", handleClick);
  // No cleanup!
}

// ✅ Correct
function Component() {
  document.addEventListener("click", handleClick);
  onCleanup(() => {
    document.removeEventListener("click", handleClick);
  });
}
```

### ❌ Don't Use onMount for Reactive Code

```tsx
// ❌ Wrong - onMount doesn't track
function Component() {
  const [count, setCount] = createSignal(0);
  
  onMount(() => {
    // This only runs once, won't react to count changes
    console.log(count());
  });
}

// ✅ Correct - use createEffect
function Component() {
  const [count, setCount] = createSignal(0);
  
  createEffect(() => {
    // This tracks count and runs when it changes
    console.log(count());
  });
}
```

## Summary

- **onMount**: One-time setup after DOM mount
- **onCleanup**: Resource disposal on unmount/disposal
- **Effect cleanup**: Runs before effect re-executes
- **Always clean up**: Event listeners, subscriptions, intervals, timeouts
- **Component runs once**: Use effects for reactive code, not component body

