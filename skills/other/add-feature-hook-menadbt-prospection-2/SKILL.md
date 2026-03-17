---
name: add-feature-hook
description: Creates TanStack Query hooks for API features with authentication. Use when connecting frontend to backend endpoints, creating data fetching hooks.
allowed-tools: Read, Write, Edit, Glob, Bash(pnpm run generate:api)
---

# Add Feature Hook

Creates TanStack Query hooks for API features with automatic authentication.

## Prerequisites

Generate latest API types (backend must be running):
```bash
cd front && pnpm run generate:api
```

## 3-Layer API Pattern

**NEVER call API directly in components!**

```
Feature Hooks (use-items.ts)
  ↓ uses
Base Auth Hooks (use-api.ts: useAuthenticatedQuery/Mutation)
  ↓ uses
Generated SDK (lib/api/*.gen.ts from OpenAPI)
```

## Workflow

### 1. Create Hook File

```typescript
// lib/hooks/use-my-feature.ts
import { useSuspenseQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuthenticatedQuery, useAuthenticatedMutation } from './use-api';
import {
  getMyFeatures,
  createMyFeature,
  updateMyFeature,
  deleteMyFeature,
} from '@/lib/api/sdk.gen';
import type { CreateMyFeatureRequest, MyFeatureResponse } from '@/lib/api/types.gen';

// Query key factory - prevents cache bugs
export const myFeatureKeys = {
  all: ['my-feature'] as const,
  list: (userId?: string) => [...myFeatureKeys.all, 'list', userId] as const,
  detail: (id: string) => [...myFeatureKeys.all, 'detail', id] as const,
};
```

### 2. Add Query Hook

```typescript
// Regular query (for optional data)
export function useMyFeatures(userId?: string) {
  return useAuthenticatedQuery({
    queryKey: myFeatureKeys.list(userId),
    queryFn: async (token) => {
      const response = await getMyFeatures({
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data ?? [];
    },
    enabled: !!userId,
  });
}

// Suspense query (for required data - use in content components)
export function useMyFeaturesSuspense(userId: string) {
  return useAuthenticatedQuery({
    queryKey: myFeatureKeys.list(userId),
    queryFn: async (token) => {
      const response = await getMyFeatures({
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data ?? [];
    },
    suspense: true, // Enables Suspense mode
  });
}
```

### 3. Add Mutation Hooks

```typescript
export function useCreateMyFeature() {
  const queryClient = useQueryClient();

  return useAuthenticatedMutation({
    mutationFn: async (data: CreateMyFeatureRequest, token) => {
      const response = await createMyFeature({
        headers: { Authorization: `Bearer ${token}` },
        body: data,
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: myFeatureKeys.all });
    },
    showSuccessToast: 'Created successfully!',
    showErrorToast: true, // Default error handling
  });
}

export function useDeleteMyFeature() {
  const queryClient = useQueryClient();

  return useAuthenticatedMutation({
    mutationFn: async (id: string, token) => {
      await deleteMyFeature({
        headers: { Authorization: `Bearer ${token}` },
        path: { id },
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: myFeatureKeys.all });
    },
    showSuccessToast: 'Deleted successfully!',
  });
}
```

## Query Key Factory

**Always use query key factories** to prevent cache bugs:

```typescript
export const myFeatureKeys = {
  all: ['my-feature'] as const,
  list: (userId?: string) => [...myFeatureKeys.all, 'list', userId] as const,
  detail: (id: string) => [...myFeatureKeys.all, 'detail', id] as const,
  filtered: (filters: Filters) => [...myFeatureKeys.all, 'filtered', filters] as const,
};
```

## Usage in Components

```typescript
// Content component (with Suspense)
function MyFeatureContent({ userId }: { userId: string }) {
  const { data } = useMyFeaturesSuspense(userId);
  const createMutation = useCreateMyFeature();

  const handleCreate = async (data: CreateMyFeatureRequest) => {
    await createMutation.mutateAsync(data);
  };

  return (
    <div>
      {data.map((item) => <div key={item.id}>{item.name}</div>)}
      <button onClick={() => handleCreate({ name: 'New' })}>
        Create
      </button>
    </div>
  );
}
```

## Toast Notifications

**Automatic** via `useAuthenticatedMutation`:
- Success: Green toast with custom message
- Error: Automatic error handling with red toast
- 401: Auto-redirect to login

**DO NOT** add manual error handling in components.

## Generated API Types

Types are auto-generated from backend OpenAPI:

```typescript
// Import from generated types
import type { CreateMyFeatureRequest, MyFeatureResponse } from '@/lib/api/types.gen';

// Import API functions
import { getMyFeatures, createMyFeature } from '@/lib/api/sdk.gen';
```

**DO NOT** edit files in `lib/api/` - regenerate instead.
