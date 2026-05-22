---
name: frontend-api-layer
description: Provides patterns for structuring the API layer in React applications. This skill should be used when setting up API clients, defining API request declarations, or integrating with TanStack Query for data fetching.
---

# Frontend API Layer

This skill provides patterns for structuring the API layer in React applications using TanStack Query and type-safe API clients.

## Canonical Examples

Study these real implementations:
- **API Client with Better Auth**: [client.ts](../../../apps/erify_studios/src/lib/api/client.ts)
- **Token Store**: [token-store.ts](../../../apps/erify_studios/src/lib/api/token-store.ts)
- **API Declarations**: [task-templates.api.ts](../../../apps/erify_studios/src/features/task-templates/api/task-templates.api.ts)

**Detailed Code Examples**: See [references/api-layer-examples.md](references/api-layer-examples.md)

---

## Architecture

```
Component
  ↓
TanStack Query Hook (useQuery/useMutation)
  ↓
API Declaration (getTaskTemplates, createTaskTemplate)
  ↓
API Client (apiClient.get/post/put/delete)
  ↓
Backend API
```

---

## Core Principles

1. **API Declarations**: Define all API requests in `{feature}/api/*.api.ts` files
2. **Type Safety**: Use shared types from `@eridu/api-types`
3. **Error Handling**: API client handles auth errors, API declarations handle business errors
4. **Query Keys**: Centralize query keys in API declaration files

---

## API Client Setup

**⚠️ Important**: This project uses **Better Auth** for authentication with sophisticated token management. See [references/api-layer-examples.md](references/api-layer-examples.md) for the full implementation.

**Key Features**:
- Token caching with JWT expiration checking (`jose` library)
- Automatic token refresh on 401 with retry logic
- Better Auth integration via `authClient.client.token()`
- Distinguishes expired tokens (refresh) vs insufficient permissions (no redirect)
- In-memory token store (no localStorage for security)

**Simplified Overview**:

```typescript
// lib/api/client.ts
import axios from 'axios';
import { decodeJwt } from 'jose';
import { getCachedToken, setCachedToken } from '@/lib/api/token-store';
import { authClient } from '@/lib/auth';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

// Request: Check cached token, fetch if expired
apiClient.interceptors.request.use(async (config) => {
  let token = getCachedToken();
  if (!token || isTokenExpired(token)) {
    const session = await authClient.client.token();
    token = session?.data?.token;
    setCachedToken(token);
  }
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response: Refresh on 401 if expired, retry once
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      // Refresh token and retry (see references for full logic)
    }
    return Promise.reject(error);
  }
);
```

**📖 See [references/api-layer-examples.md](references/api-layer-examples.md) for the complete implementation with step-by-step code.**

---

## API Declarations Pattern

**Pattern**: `features/{feature}/api/{feature}.api.ts`

```typescript
import { apiClient } from '@/lib/api-client';
import type { TaskTemplateDto, CreateTaskTemplateDto } from '@eridu/api-types';

// Query Keys
export const taskTemplateKeys = {
  all: ['task-templates'] as const,
  lists: () => [...taskTemplateKeys.all, 'list'] as const,
  list: (studioId: string, filters: string) => [...taskTemplateKeys.lists(), studioId, filters] as const,
  details: () => [...taskTemplateKeys.all, 'detail'] as const,
  detail: (id: string) => [...taskTemplateKeys.details(), id] as const,
};

// API Functions
export async function getTaskTemplates(studioId: string, params?: { name?: string; cursor?: string; limit?: number }) {
  const { data } = await apiClient.get<{ data: TaskTemplateDto[]; meta: { total: number; nextCursor?: string } }>(
    `/studios/${studioId}/task-templates`,
    { params }
  );
  return data;
}

export async function createTaskTemplate(studioId: string, payload: CreateTaskTemplateDto) {
  const { data } = await apiClient.post<TaskTemplateDto>(`/studios/${studioId}/task-templates`, payload);
  return data;
}
```

**Key Points**:
- ✅ Centralize query keys using factory pattern
- ✅ Use shared types from `@eridu/api-types`
- ✅ Return typed responses
- ✅ Handle params and payload transformation

---

## TanStack Query Integration

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getTaskTemplates, createTaskTemplate, taskTemplateKeys } from '../api/task-templates.api';

export function useTaskTemplates(studioId: string, filters: { name?: string }) {
  return useQuery({
    queryKey: taskTemplateKeys.list(studioId, JSON.stringify(filters)),
    queryFn: () => getTaskTemplates(studioId, filters),
  });
}

export function useCreateTaskTemplate(studioId: string) {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (payload: CreateTaskTemplateDto) => createTaskTemplate(studioId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: taskTemplateKeys.lists() });
    },
  });
}
```

---

## Best Practices Checklist

- [ ] API client configured with Better Auth token management (see references)
- [ ] Token caching with JWT expiration checking implemented
- [ ] Automatic token refresh on 401 with retry logic
- [ ] All API requests defined in `{feature}/api/*.api.ts` files
- [ ] Query keys centralized using factory pattern
- [ ] Shared types from `@eridu/api-types` used for requests/responses
- [ ] TanStack Query hooks use query keys from API declarations
- [ ] Mutations invalidate relevant queries on success
- [ ] Error handling: API client (auth), components (business logic)

---

## Related Skills

- [frontend-state-management](../frontend-state-management/SKILL.md) - State management patterns
- [frontend-error-handling](../frontend-error-handling/SKILL.md) - Error handling patterns
- [shared-api-types](../shared-api-types/SKILL.md) - Shared API types
