---
name: api-client
description: Centralized TypeScript API client with typed namespaces, automatic token refresh with request deduplication, TanStack Query integration, and consistent error handling.
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: api
  time: 5h
  source: drift-masterguide
---

# TypeScript API Client

Centralized API client with typed namespaces, automatic token refresh, and TanStack Query integration.

## When to Use This Skill

- Building frontend applications that call backend APIs
- Need type safety on requests and responses
- Want automatic token refresh without duplicated logic
- Using TanStack Query for caching and state management

## Core Concepts

The pattern provides:
- Typed namespaces (auth, users, billing, etc.)
- Automatic token refresh with request deduplication
- TanStack Query integration for caching
- Consistent error handling with custom error class

Architecture:
```
Component → useQuery/useMutation → API Client → Fetch
                                       ↓
                                  401? → Refresh → Retry
```

## Implementation

### TypeScript

```typescript
// lib/api/types.ts
export class APIClientError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number,
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'APIClientError';
  }
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
  expiresAt: string;
}

// lib/api/client.ts
interface RequestOptions {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  body?: Record<string, unknown>;
  params?: Record<string, string | number | boolean | undefined>;
  skipRefresh?: boolean;
}

export class APIClient {
  private baseUrl: string;
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  private onUnauthorized: () => void;
  
  // Refresh deduplication
  private isRefreshing = false;
  private refreshPromise: Promise<boolean> | null = null;

  constructor(options: { baseUrl: string; onUnauthorized?: () => void }) {
    this.baseUrl = options.baseUrl.replace(/\/$/, '');
    this.onUnauthorized = options.onUnauthorized || (() => {});
  }

  setTokens(accessToken: string, refreshToken: string): void {
    this.accessToken = accessToken;
    this.refreshToken = refreshToken;
  }

  clearTokens(): void {
    this.accessToken = null;
    this.refreshToken = null;
  }

  // Typed namespaces
  auth = {
    login: (data: { email: string; password: string }) =>
      this.request<{ tokens: TokenPair; user: User }>('/auth/login', {
        method: 'POST',
        body: data,
      }),

    refresh: () =>
      this.request<TokenPair>('/auth/refresh', {
        method: 'POST',
        body: { refreshToken: this.refreshToken },
        skipRefresh: true, // Prevent infinite loop
      }),

    me: () =>
      this.request<User>('/auth/me', { method: 'GET' }),
  };

  users = {
    get: (id: string) =>
      this.request<User>(`/users/${id}`, { method: 'GET' }),

    update: (id: string, data: Partial<User>) =>
      this.request<User>(`/users/${id}`, { method: 'PATCH', body: data }),
  };

  private async request<T>(endpoint: string, options: RequestOptions): Promise<T> {
    const url = this.buildUrl(endpoint, options.params);
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.accessToken) {
      headers['Authorization'] = `Bearer ${this.accessToken}`;
    }

    const response = await fetch(url, {
      method: options.method,
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
    });

    // Handle 401 - attempt refresh
    if (response.status === 401 && !options.skipRefresh) {
      const refreshed = await this.attemptTokenRefresh();
      if (refreshed) {
        return this.request<T>(endpoint, { ...options, skipRefresh: true });
      }
      this.onUnauthorized();
      throw new APIClientError('Unauthorized', 'UNAUTHORIZED', 401);
    }

    if (!response.ok) {
      throw await this.parseError(response);
    }

    if (response.status === 204) return undefined as T;
    return this.transformResponse<T>(await response.json());
  }

  private async attemptTokenRefresh(): Promise<boolean> {
    if (!this.refreshToken) return false;

    // Deduplicate concurrent refresh attempts
    if (this.isRefreshing) {
      return this.refreshPromise!;
    }

    this.isRefreshing = true;
    this.refreshPromise = this.doRefresh();

    try {
      return await this.refreshPromise;
    } finally {
      this.isRefreshing = false;
      this.refreshPromise = null;
    }
  }

  private async doRefresh(): Promise<boolean> {
    try {
      const tokens = await this.auth.refresh();
      this.setTokens(tokens.accessToken, tokens.refreshToken);
      return true;
    } catch {
      this.clearTokens();
      return false;
    }
  }

  private buildUrl(endpoint: string, params?: Record<string, any>): string {
    const url = new URL(`${this.baseUrl}${endpoint}`);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) url.searchParams.set(key, String(value));
      });
    }
    return url.toString();
  }

  private transformResponse<T>(data: unknown): T {
    // Convert snake_case to camelCase
    return this.snakeToCamel(data) as T;
  }

  private snakeToCamel(obj: unknown): unknown {
    if (Array.isArray(obj)) return obj.map(item => this.snakeToCamel(item));
    if (obj !== null && typeof obj === 'object') {
      return Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [
          key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase()),
          this.snakeToCamel(value),
        ])
      );
    }
    return obj;
  }

  private async parseError(response: Response): Promise<APIClientError> {
    try {
      const data = await response.json();
      return new APIClientError(
        data.message || 'Request failed',
        data.code || 'UNKNOWN_ERROR',
        response.status,
        data.details
      );
    } catch {
      return new APIClientError('Request failed', 'UNKNOWN_ERROR', response.status);
    }
  }
}

// Singleton export
export const apiClient = new APIClient({
  baseUrl: process.env.NEXT_PUBLIC_API_URL || '/api',
  onUnauthorized: () => {
    if (typeof window !== 'undefined') window.location.href = '/login';
  },
});
```

### TanStack Query Integration

```typescript
// lib/api/query-keys.ts
export const queryKeys = {
  auth: {
    all: ['auth'] as const,
    me: () => [...queryKeys.auth.all, 'me'] as const,
  },
  users: {
    all: ['users'] as const,
    detail: (id: string) => [...queryKeys.users.all, id] as const,
  },
} as const;

// lib/api/hooks/use-auth.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

export function useCurrentUser() {
  return useQuery({
    queryKey: queryKeys.auth.me(),
    queryFn: () => apiClient.auth.me(),
    staleTime: 5 * 60 * 1000,
    retry: false,
  });
}

export function useLogin() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: { email: string; password: string }) =>
      apiClient.auth.login(data),
    onSuccess: (response) => {
      apiClient.setTokens(response.tokens.accessToken, response.tokens.refreshToken);
      queryClient.setQueryData(queryKeys.auth.me(), response.user);
    },
  });
}
```

## Usage Examples

### Component Usage

```tsx
function UserProfile() {
  const { data: user, isLoading } = useCurrentUser();
  const logout = useLogout();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{user?.displayName}</h2>
      <button onClick={() => logout.mutate()}>Logout</button>
    </div>
  );
}
```

## Best Practices

1. Typed namespaces - Group related endpoints for discoverability
2. Token refresh deduplication - Prevent multiple concurrent refresh requests
3. Query key factory - Consistent cache key management
4. Response transformation - Convert snake_case to camelCase automatically
5. Singleton export - Single instance for consistent token state

## Common Mistakes

- Not deduplicating token refresh (causes race conditions)
- Forgetting skipRefresh on refresh endpoint (infinite loop)
- Scattered fetch calls without centralized error handling
- No response transformation (inconsistent casing)
- Creating multiple client instances (token state mismatch)

## Related Patterns

- jwt-auth - JWT authentication implementation
- rate-limiting - Client-side rate limiting
- error-handling - Error handling patterns
