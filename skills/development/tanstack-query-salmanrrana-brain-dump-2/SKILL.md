---
name: TanStack Query Core
description: Use when asking about "TanStack Query", "React Query", "useQuery", "query keys", "staleTime", "query client setup", "query factories", or "queryOptions"
version: 1.0.0
---

# TanStack Query Core

## Core Mental Model

TanStack Query is an **async state manager**, not a data fetching library.

- Manages async state through Promises
- Data fetching happens in `queryFn` (axios, fetch, etc.)
- Synchronizes data using unique `QueryKey` identifiers

**Critical rule**: Use exclusively for async/server state. Use local state for UI state.

## Query Options API (v5+)

Use `queryOptions()` for type safety and reusability:

```typescript
import { queryOptions, useQuery } from "@tanstack/react-query";

// Define reusable query options
const todoQueryOptions = (id: string) =>
  queryOptions({
    queryKey: ["todos", id],
    queryFn: () => fetchTodo(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

// Usage
const { data } = useQuery(todoQueryOptions(id));
```

### Query Factories

Organize related queries:

```typescript
export const todoQueries = {
  all: () => queryOptions({ queryKey: ["todos"], queryFn: fetchAllTodos }),
  detail: (id: string) =>
    queryOptions({
      queryKey: ["todos", id],
      queryFn: () => fetchTodo(id),
      staleTime: 5 * 60 * 1000,
    }),
};

// Usage
const { data } = useQuery(todoQueries.detail(id));
```

## staleTime Configuration

`staleTime` is the most important option:

- **Fresh data** (within staleTime): Cache only, no refetch
- **Stale data** (beyond staleTime): Cache + background refetch

```typescript
// Recommended defaults
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute default
      gcTime: 5 * 60 * 1000, // 5 minutes cleanup
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
    },
  },
});
```

## Query Keys as Dependencies

**Always include parameters in queryKey**:

```typescript
// CORRECT: Parameters in queryKey
const todoQuery = (id: string) =>
  queryOptions({
    queryKey: ["todos", id], // ✅ id included
    queryFn: () => fetchTodo(id),
  });

// INCORRECT: Missing id in queryKey
const todoQuery = (id: string) =>
  queryOptions({
    queryKey: ["todos"], // ❌ id missing
    queryFn: () => fetchTodo(id),
  });
```

## Common Anti-Patterns

### 1. Parameters to refetch()

```typescript
// WRONG: refetch({ id: newId }) - doesn't work
// CORRECT: Use state to trigger new query
const [todoId, setTodoId] = useState(id);
const { data } = useQuery(todoQuery(todoId));
setTodoId(newId); // Triggers new query
```

### 2. Client State in RQ

```typescript
// WRONG: UI state in RQ
// CORRECT: Use React state, Zustand, etc.
const [isOpen, setIsOpen] = useState(false); // ✅
```

### 3. QueryClient in Component

```typescript
// WRONG: New client every render
function App() {
  const queryClient = new QueryClient(); // ❌
}

// CORRECT: Create once
const queryClient = new QueryClient(); // ✅
```

## Selectors & Suspense

```typescript
// Fine-grained updates with select
const { data: title } = useQuery({
  ...productQuery(id),
  select: (data) => data.title,
});

// Suspense for guaranteed data
const { data } = useSuspenseQuery(todoQuery(id)); // data is Todo, not undefined

// Wrap with boundary
<Suspense fallback={<Loading />}>
  <TodoDetail id={id} />
</Suspense>
```

## Quick Reference

| Concept          | Recommendation     |
| ---------------- | ------------------ |
| Query definition | `queryOptions()`   |
| Organization     | Query factories    |
| staleTime        | Start with 60s     |
| Parameters       | Always in queryKey |
| Client state     | Separate from RQ   |
| Refetch control  | Adjust staleTime   |

### Related Skills

- **tanstack-mutations** - Mutations, invalidation
- **tanstack-types** - Type safety with Zod
- **tanstack-errors** - Error handling
- **tanstack-forms** - Forms integration
