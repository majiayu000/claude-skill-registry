---
name: web-trpc-setup
description: Sets up tRPC queries and mutations in web components with proper typing, React Query integration, and error handling.
---

# Web tRPC Setup Skill

## When to Use

- User needs to add data fetching to a component
- User wants to create a new tRPC query or mutation
- User needs to set up React Query with tRPC
- User asks to add form submission with tRPC

## What This Skill Does

1. Determines if query or mutation is needed
2. Creates proper tRPC procedure calls
3. Handles loading, error, and success states
4. Sets up proper React Query options
5. Adds cache invalidation for mutations
6. Implements proper TypeScript typing

## Query Pattern

```typescript
"use client";

import { trpc } from "@/lib/trpc";

export function useActivities() {
  const { data, isLoading, error, refetch } = trpc.activities.list.useQuery(
    { limit: 20, offset: 0 },
    {
      staleTime: 5 * 60 * 1000,
      refetchOnWindowFocus: false,
    },
  );

  return { data, isLoading, error, refetch };
}
```

## Mutation Pattern

```typescript
"use client";

import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

export function useCreateActivity() {
  const utils = trpc.useUtils();

  const mutation = trpc.activities.create.useMutation({
    onSuccess: () => {
      utils.activities.list.invalidate();
      toast.success("Activity created");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  return mutation;
}
```

## Error Handling

```typescript
if (isLoading) return <Skeleton />;
if (error) return <ErrorAlert message={error.message} onRetry={refetch} />;
```

## Loading States

```typescript
import { Skeleton } from '@/components/ui/skeleton';

function ActivityList() {
  const { data, isLoading } = trpc.activities.list.useQuery();

  if (isLoading) {
    return (
      <View className="p-4">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-24 mb-4" />
        ))}
      </View>
    );
  }

  return <ActivityListView activities={data} />;
}
```

## Cache Invalidation

```typescript
// Invalidate after mutation
utils.activities.list.invalidate();

// Invalidate specific item
utils.activities.getById.invalidate({ id });
```
