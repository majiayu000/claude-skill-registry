---
name: react
description: |
  Manages React components, hooks, and lazy loading patterns for the SPA.
  Use when: creating components, writing hooks, implementing data fetching, managing state, or optimizing performance.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# React Skill

Bookkeep uses React 18 with TanStack Query for server state, React Router for navigation, and aggressive code splitting via `React.lazy()`. All pages except Login are lazy-loaded. The frontend uses the `@/` path alias for `./src/`.

## Quick Start

### Component with Query

```tsx
import { memo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { requestsApi } from '@/lib/api';

export const BookCard = memo(function BookCard({ book }: BookCardProps) {
  const { data: requests } = useQuery({
    queryKey: ['book-requests', book.hardcoverId],
    queryFn: () => requestsApi.getByHardcoverId(book.hardcoverId),
    enabled: !!book.hardcoverId,
    staleTime: 60_000,
  });

  return <div>{/* Component JSX */}</div>;
});
```

### Custom Hook with Chained Queries

```tsx
export function useTrendingBooks(limit = 12) {
  const booksQuery = useQuery({
    queryKey: ['hardcover', 'trending', limit],
    queryFn: () => getTrendingBooks(limit),
    staleTime: 24 * 60 * 60 * 1000,
  });

  const enrichedQuery = useQuery({
    queryKey: ['hardcover', 'trending', limit, 'availability'],
    queryFn: () => enrichAvailability(booksQuery.data!),
    enabled: !!booksQuery.data?.length,  // Chain to first query
  });

  return { ...booksQuery, data: enrichedQuery.data ?? booksQuery.data };
}
```

## Key Concepts

| Concept | Pattern | Location |
|---------|---------|----------|
| Lazy loading | `lazy(() => import('@/pages/X'))` | `src/App.tsx` |
| Server state | TanStack Query `useQuery`/`useMutation` | All components |
| Global state | React Context + Query | `src/contexts/` |
| Memoization | `memo()` for card grids | `BookCard.tsx` |
| Polling | Chained `setTimeout` with backoff | `useAvailabilityPolling.ts` |

## Common Patterns

### Conditional Query (Gate on Dependencies)

```tsx
const { data } = useQuery({
  queryKey: ['requests', hardcoverId],
  queryFn: () => requestsApi.getByHardcoverId(hardcoverId),
  enabled: open && !!hardcoverId,  // Only fetch when dialog open AND ID exists
});
```

### Query Invalidation After Mutation

```tsx
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: (data) => requestsApi.create(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['requests'] });
    queryClient.invalidateQueries({ queryKey: ['book-requests', hardcoverId] });
  },
});
```

## See Also

- [hooks](references/hooks.md)
- [components](references/components.md)
- [data-fetching](references/data-fetching.md)
- [state](references/state.md)
- [forms](references/forms.md)
- [performance](references/performance.md)

## Related Skills

- See the **tanstack-query** skill for advanced query patterns
- See the **typescript** skill for type definitions and interfaces
- See the **shadcn-ui** skill for UI primitives
- See the **tailwind** skill for styling patterns
- See the **vite** skill for build configuration