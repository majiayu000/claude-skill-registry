---
name: react-frontend-patterns
description: Use when architecting or implementing React frontends with Zustand, TanStack Query, or component hierarchies. Symptoms - unclear where state lives, stores causing re-renders, no API caching strategy, inconsistent error handling.
---

# React Frontend Patterns

## Overview

**State flows down, events flow up. Colocate state with consumers. Fetch at route level.**

Patterns for React 19 + TypeScript + Zustand + TanStack Query + Tailwind v4. Use in Phase 1 (architecture decisions) and Phase 3 (implementation).

## Quick Reference

| Pattern | Rule |
|---------|------|
| Zustand stores | One per feature domain (`useCartStore`, `useUserStore`) |
| Selectors | Always: `useStore((s) => s.field)` — never bare `useStore()` |
| Multiple fields | `useShallow`: `useStore(useShallow((s) => ({ a: s.a, b: s.b })))` |
| Derived state | Compute in selector, never store computed values |
| Server data | TanStack Query — never Zustand for API data |
| Query keys | `[domain, action, params]`: `['products', 'list', { category }]` |
| Mutations | `useMutation` with `onSuccess` invalidation |
| Error boundaries | Page-level + feature-level |
| Loading states | Component-level via `isPending` |
| Test location | `__tests__/` subfolder |

## State Colocation

```
Where does this state live?
│
├── From server? ──────────► TanStack Query cache
│                            (products, user profile, orders)
│
├── Global UI? ────────────► Zustand store
│                            (theme, sidebar, notifications)
│
├── In URL? ───────────────► Router params/search
│                            (filters, pagination, selected tab)
│
├── Form input? ───────────► react-hook-form
│                            (field values, validation)
│
└── Local to component? ───► useState
                             (modal open, hover, dropdown)
```

**Rule:** Start with the most local option. Lift only when needed.

## Zustand Patterns

One store per feature domain. Actions own async logic. Reset for tests.

**The Selector Rule (Non-Negotiable):**

```tsx
// ✅ Always use selectors
const items = useCartStore((s) => s.items)
const addItem = useCartStore((s) => s.addItem)

// ✅ Multiple fields with useShallow
const { items, total } = useCartStore(
  useShallow((s) => ({ items: s.items, total: s.total }))
)

// ❌ NEVER bare — causes re-render on ANY state change
const store = useCartStore()
const { items, total } = useCartStore()  // Also bad!
```

**Create selector hooks** to enforce this pattern:

```tsx
// In store file — export selector hooks
export const useCartItems = () => useCartStore((s) => s.items)
export const useCartTotal = () => useCartStore((s) => s.items.reduce(...))
export const useCartActions = () => useCartStore(
  useShallow((s) => ({ addItem: s.addItem, removeItem: s.removeItem }))
)

// In components — impossible to use bare store
const items = useCartItems()  // ✅ Always correct
```

**Complete store template:** See [references/zustand-store-template.ts](references/zustand-store-template.ts)

## TanStack Query Patterns

Queries for reads. Mutations for writes. Custom hooks wrap both.

```tsx
// Query hook
export function useProducts(category: string) {
  return useQuery({
    queryKey: ['products', 'list', { category }],
    queryFn: () => api.products.list(category),
  })
}

// Mutation hook
export function useCreateProduct() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: api.products.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] })
    },
  })
}
```

**Complete patterns:** See [references/tanstack-query-patterns.tsx](references/tanstack-query-patterns.tsx)

## Error & Loading Strategy

| Layer | Error Handling | Loading |
|-------|---------------|---------|
| Page | Error boundary with fallback UI | Page skeleton |
| Feature | Error boundary isolates widget | Component skeleton |
| Mutation | Toast notification via `onError` | Button spinner |
| Form | Inline validation messages | Submit disabled |

```tsx
// Page-level boundary
<ErrorBoundary fallback={<PageError />}>
  <ProductsPage />
</ErrorBoundary>

// Feature-level boundary
<ErrorBoundary fallback={<WidgetError />}>
  <RecommendationsWidget />
</ErrorBoundary>
```

## Component Hierarchy

```
src/
├── components/
│   ├── ui/                    # shadcn/ui primitives
│   ├── [feature]/             # Feature components
│   │   ├── FeatureCard.tsx
│   │   └── __tests__/
│   │       └── FeatureCard.test.tsx
│   └── layout/                # Shell, nav, sidebar
├── stores/                    # Zustand stores
│   └── useCartStore.ts
├── hooks/                     # TanStack Query hooks
│   └── useProducts.ts
└── pages/                     # Route components
    └── ProductsPage.tsx
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Bare `useStore()` | Always use selector: `useStore((s) => s.field)` |
| Server data in Zustand | Use TanStack Query for API data |
| Storing derived state | Compute in selector: `(s) => s.items.length` |
| Missing query key params | Include all variables: `['products', { category, page }]` |
| No error boundary | Add page-level + feature-level boundaries |
| Mocking Zustand in tests | Use real stores, reset in `beforeEach` |

## Red Flags — STOP and Fix

If you catch yourself doing any of these, stop and apply the correct pattern:

- `const { x, y, z } = useStore()` — Bare destructuring. Use selectors or useShallow.
- `const store = useStore()` — Bare store. Always select specific fields.
- `useState` for data from API — Use TanStack Query.
- Storing `itemCount` when you have `items` — Derive in selector: `(s) => s.items.length`
- `vi.mock` on a Zustand store — Use real store, reset in beforeEach.
- Fetching in useEffect — Use TanStack Query's useQuery.
- "Just this once, time is tight" — Patterns take 10 seconds more. Do it right.

## Provider Setup

See [references/provider-setup.tsx](references/provider-setup.tsx) for the complete app provider stack.

## E2E Testing Support

**MANDATORY:** All interactive elements MUST have `data-testid` attributes.

Naming convention: `{component}-{element}-{action?}`

Examples:
```tsx
<button data-testid="recipe-form-submit">Save</button>
<input data-testid="recipe-form-title" />
<div data-testid="recipe-card-{id}">...</div>
```

For lists/collections, include the ID:
```tsx
data-testid="recipe-card-123"
data-testid="shopping-item-456"
```

**Interactive elements requiring `data-testid`:**
- All buttons, links, and clickable elements
- Form inputs (text, select, checkbox, radio)
- Cards and list items that can be interacted with
- Modals, dialogs, and their controls
- Navigation items
- Toast notifications and alerts
