---
name: tanstack-hook
description: Generates TanStack Query hooks following project patterns with useQuery. Creates hooks in src/hooks/ with typed return values. Use when creating data fetching logic.
---

# TanStack Hook Generator Skill

Creates data-fetching hooks using TanStack Query patterns.

## File Pattern

```text
src/hooks/use{Feature}.ts
```

## Hook Template

```typescript
// src/hooks/use{Feature}.ts

import { useQuery } from "@tanstack/react-query";
import { mock{Feature}Data, {Feature}Data } from "../data/mock-{feature}";

async function fetch{Feature}Data(): Promise<{Feature}Data> {
    // Replace with actual API call in production
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mock{Feature}Data;
}

export function use{Feature}() {
    return useQuery({
        queryKey: ["{feature}"],
        queryFn: fetch{Feature}Data,
        staleTime: 1000 * 60 * 5, // 5 minutes
    });
}
```

## Return Pattern (for complex hooks)

```typescript
export function use{Feature}() {
    const [filter, setFilter] = useState("");
    
    const query = useQuery({
        queryKey: ["{feature}", filter],
        queryFn: () => fetch{Feature}Data(filter),
    });

    const handleAction = useCallback(() => {
        // Action logic
    }, []);

    return {
        state: {
            data: query.data,
            isLoading: query.isLoading,
            error: query.error,
            filter,
        },
        actions: {
            setFilter,
            handleAction,
            refetch: query.refetch,
        },
    };
}
```

## Usage in Component

```tsx
export function {Feature}Component() {
    const { data, isLoading, error } = use{Feature}();

    if (isLoading) return <Skeleton />;
    if (error) return <Alert status="danger">Error loading data</Alert>;

    return <div>{data.name}</div>;
}
```

## Conventions

1. **Filename**: `use{Feature}.ts` in camelCase
2. **Named export**: `export function use{Feature}()`
3. **Query keys**: Descriptive arrays like `["{feature}"]`
4. **Stale time**: Set appropriate cache duration
5. **Error handling**: Let components handle loading/error states

## Examples

See these files for reference:

- `src/hooks/useOrder.ts`
- `src/hooks/useProjectPage.ts`
- `src/hooks/useUnmatchedItems.ts`
