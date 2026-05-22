---
name: solid-router-preloading
description: "Solid Router preloading: preload function for routes, usePreloadRoute hook, hover/focus intent detection, lazy component preloading, performance optimization."
metadata:
  globs:
    - "**/routes/**/*"
    - "**/*preload*"
---

# Solid Router Preloading

Complete guide to preloading routes and components in Solid Router. Optimize navigation performance by loading code and data before user commits to navigation.

## Automatic Preloading

Solid Router automatically preloads routes based on user intent signals.

### Intent Detection

| User Action | Behavior |
|------------|----------|
| **Hover** | Waits ~20ms before preloading |
| **Focus** | Preloads immediately |

**How it works:**
- Router listens for hover/focus on `<A>` components
- Debounces hover for 20ms to ignore accidental passes
- Loads route module and runs preload function
- Caches result for instant navigation

## Route Preload Function

Export a `preload` function in route modules to seed caches and prepare data.

### Basic Preload

```tsx
// routes/users/[id].tsx
import type { RouteDefinition } from "@solidjs/router";

export const route = {
  preload({ params, location }) {
    // Preload user data
    void getUserQuery(params.id);
    // Preload related data
    void getUserPostsQuery(params.id);
  },
} satisfies RouteDefinition;

export default function UserProfile() {
  // Data already cached from preload
  const user = createAsync(() => getUserQuery(params.id));
  return <div>{user()?.name}</div>;
}
```

### Preload with Search Params

```tsx
export const route = {
  preload({ params, location, search }) {
    const filters = search.filters;
    void getProductsQuery({ category: params.category, filters });
  },
} satisfies RouteDefinition;
```

**Preload function receives:**
- `params`: Route parameters
- `location`: Location object
- `search`: Search params (if using search API)

## usePreloadRoute Hook

Imperatively preload routes for custom interactions.

### Basic Usage

```tsx
import { usePreloadRoute } from "@solidjs/router";

function ProductCard({ productId }) {
  const preload = usePreloadRoute();

  const handleMouseEnter = () => {
    // Preload product detail route
    preload(`/products/${productId}`);
  };

  return (
    <div onMouseEnter={handleMouseEnter}>
      Product Card
    </div>
  );
}
```

### With Delay

```tsx
function ProductCard({ productId }) {
  const preload = usePreloadRoute();

  const handleMouseEnter = () => {
    // Custom delay before preloading
    setTimeout(() => {
      preload(`/products/${productId}`);
    }, 100);
  };

  return <div onMouseEnter={handleMouseEnter}>Product Card</div>;
}
```

## Lazy Component Preloading

Preload nested lazy components that aren't part of route hierarchy.

### Lazy Component with Preload

```tsx
import { lazy } from "solid-js";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

// Preload component
HeavyComponent.preload();

// Later, render it
return <HeavyComponent />;
```

### Coordinating Route and Component Preload

```tsx
// Route preload
export const route = {
  preload({ params }) {
    // Preload route data
    void getUserQuery(params.id);
    
    // Preload nested lazy component
    UserDetails.preload();
  },
} satisfies RouteDefinition;

const UserDetails = lazy(() => import("./UserDetails"));

export default function UserProfile() {
  return (
    <Suspense>
      <UserDetails />
    </Suspense>
  );
}
```

## Performance Optimization

### When to Preload

**Good candidates:**
- High-intent interactions (hover, focus)
- Likely next routes
- Critical data for navigation

**Avoid preloading:**
- Low-probability routes
- Very large bundles
- Expensive operations

### Measuring Impact

Use profiling tools to measure:
- Reduced long tasks
- Faster navigation
- Network usage trade-offs

### Custom Preload Strategy

```tsx
function SmartPreload({ route, delay = 20 }) {
  const preload = usePreloadRoute();
  let timeout: number;

  const handleIntent = () => {
    timeout = setTimeout(() => {
      preload(route);
    }, delay);
  };

  const cancelPreload = () => {
    clearTimeout(timeout);
  };

  return (
    <div
      onMouseEnter={handleIntent}
      onMouseLeave={cancelPreload}
    >
      <A href={route}>Link</A>
    </div>
  );
}
```

## Common Patterns

### Preload on Hover

```tsx
function NavigationLink({ href, children }) {
  const preload = usePreloadRoute();

  return (
    <A
      href={href}
      onMouseEnter={() => preload(href)}
    >
      {children}
    </A>
  );
}
```

### Preload with Query

```tsx
export const route = {
  preload({ params }) {
    // Preload multiple queries
    void Promise.all([
      getUserQuery(params.id),
      getUserPostsQuery(params.id),
      getUserFollowersQuery(params.id),
    ]);
  },
} satisfies RouteDefinition;
```

### Conditional Preload

```tsx
export const route = {
  preload({ params, location }) {
    // Only preload if authenticated
    if (isAuthenticated()) {
      void getUserQuery(params.id);
    }
  },
} satisfies RouteDefinition;
```

## SSR Considerations

**Important:** Preload functions run during SSR initial render and resume on client hydration.

**Best practices:**
- Keep preload functions **pure**
- Avoid side effects
- Use for data fetching only
- Don't mutate global state

```tsx
// ✅ Good - pure function
export const route = {
  preload({ params }) {
    void getUserQuery(params.id); // Just fetch data
  },
} satisfies RouteDefinition;

// ❌ Bad - side effects
export const route = {
  preload({ params }) {
    setGlobalState(params.id); // Mutates global state
    void getUserQuery(params.id);
  },
} satisfies RouteDefinition;
```

## Best Practices

1. **Use route preload for data:**
   - Seed query caches
   - Prepare route data
   - Warm computations

2. **Use usePreloadRoute for custom:**
   - Custom interactions
   - Timers
   - Observer-driven experiences

3. **Preload lazy components separately:**
   - Not automatically preloaded
   - Call `.preload()` manually
   - Coordinate with route preload

4. **Measure performance:**
   - Profile real user flows
   - Avoid over-preloading
   - Balance network cost

5. **Keep preload functions pure:**
   - No side effects
   - SSR-safe
   - Idempotent

## Summary

- **Automatic**: Hover (20ms delay) and focus trigger preload
- **Route preload**: Export preload function in route
- **usePreloadRoute**: Imperative preloading hook
- **Lazy components**: Call `.preload()` method
- **SSR**: Keep preload functions pure
- **Performance**: Measure and optimize

