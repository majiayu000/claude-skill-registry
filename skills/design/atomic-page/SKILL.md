---
name: atomic-page
description: Create a React PAGE that binds templates/organisms to real app data and routing. Use for route-level components. Pages handle data loading, orchestration, and side effects.
argument-hint: "[PageName] [optional: route/intent]"
---

# Atomic Design: PAGE (React Functional Components)

You are creating a **PAGE**: a route-level component that binds UI to real data and app concerns.

## Hard rules

1. **Functional components only**.
2. **Orchestration lives here**:
   - Data fetching (via the project’s standard: loaders, query libs, server components, etc.)
   - Side effects (analytics, navigation, subscriptions) in `useEffect` or framework equivalents
3. **Keep UI reusable**:
   - Prefer pushing rendering into templates/organisms; keep pages thin.
4. **Error/loading states**:
   - Must have consistent handling aligned with the repo’s conventions.
5. **Performance**:
   - Avoid waterfall fetching; colocate queries where the project expects.
   - Memoize expensive derived data with `useMemo` when justified.

## Output expectations

- Provide:
  1. `Page.tsx`
  2. `Page.test.tsx` (routing + async states, if applicable)
  3. A brief note explaining which layer owns which responsibility (page vs template vs organism).

## Recommended folder conventions

- `src/pages/<PageName>/...` (or framework equivalent)
