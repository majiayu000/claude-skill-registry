---
name: route-generator
description: Adds new routes to TanStack Router in src/router.tsx. Creates route definitions following project patterns. Use when adding new pages or sections.
---

# Route Generator Skill

Adds new routes to `src/router.tsx` following TanStack Router patterns.

## Route Definition Pattern

```typescript
const {name}Route = createRoute({
    getParentRoute: () => {parentRoute},
    path: "/{path}",
    component: {ComponentName},
});
```

## Parent Route Selection

| Parent | Use For |
|--------|---------|
| `rootRoute` | Top-level pages (like `/project`) |
| `orderLayoutRoute` | Order-related pages with shared layout |
| `projectRoute` | Project sub-pages under `/project/...` |

## Adding a New Route

1. **Import the component** at the top of `router.tsx`
2. **Create the route definition** with appropriate parent
3. **Add to routeTree** in the correct children array

### Example: Adding a New Order Page

```typescript
// 1. Import
import { NewFeature } from "./components/NewFeature";

// 2. Create route
const newFeatureRoute = createRoute({
    getParentRoute: () => orderLayoutRoute,
    path: "/new-feature",
    component: NewFeature,
});

// 3. Add to routeTree
const routeTree = rootRoute.addChildren([
    orderLayoutRoute.addChildren([
        // ... existing routes
        newFeatureRoute, // Add here
    ]),
    // ...
]);
```

### Example: Adding a Project Sub-Page

```typescript
const projectAnalyticsRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/analytics",
    component: ProjectAnalytics,
});

// Add to projectRoute's children in routeTree
```

## Placeholder Component Pattern

For pages not yet implemented:

```typescript
const comingSoonRoute = createRoute({
    getParentRoute: () => projectRoute,
    path: "/coming-soon",
    component: () => (
        <div className="p-8 text-center text-default-500">
            Coming Soon
        </div>
    ),
});
```

## Navigation

Use TanStack Router's `Link` component:

```tsx
import { Link } from "@tanstack/react-router";

<Link to="/new-feature">Go to Feature</Link>
```

## Reference

See `src/router.tsx` for current route structure.
