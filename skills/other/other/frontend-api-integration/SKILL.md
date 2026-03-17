---
name: frontend-api-integration
description: Guide for building robust API integration layers in React/TypeScript applications. Use when implementing HTTP clients (axios/fetch), request/response interceptors, authentication token handling, error handling strategies, retry logic, request cancellation, or organizing API services. Triggers on questions about API client setup, custom hooks for data fetching, React Query/SWR integration, or service layer patterns.
---

# Frontend API Integration

## API Client Setup

### Axios Instance with Interceptors

```typescript
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor - auth token injection
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('accessToken');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor - error handling + token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await refreshAccessToken();
      originalRequest.headers.Authorization = `Bearer ${newToken}`;
      return api(originalRequest);
    }
    return Promise.reject(error);
  }
);
```

### Request Cancellation

```typescript
// Per-request cancellation
const controller = new AbortController();
api.get('/data', { signal: controller.signal });
controller.abort();

// Auto-timeout helper
function withTimeout(ms: number) {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), ms);
  return controller.signal;
}
```

### Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  retries = 3,
  delay = 1000
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries === 0) throw error;
    await new Promise(r => setTimeout(r, delay));
    return withRetry(fn, retries - 1, delay * 2);
  }
}
```

## Service Layer Pattern

```typescript
// services/userService.ts
export const userService = {
  getById: (id: string) => api.get<User>(`/users/${id}`).then(r => r.data),
  create: (data: CreateUserDTO) => api.post<User>('/users', data).then(r => r.data),
  update: (id: string, data: Partial<User>) => api.patch<User>(`/users/${id}`, data).then(r => r.data),
  delete: (id: string) => api.delete(`/users/${id}`)
};
```

## Error Handling

```typescript
// types/api.ts
interface ApiError {
  message: string;
  code: string;
  status: number;
}

function parseError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    return {
      message: error.response?.data?.message ?? error.message,
      code: error.response?.data?.code ?? 'UNKNOWN',
      status: error.response?.status ?? 500
    };
  }
  return { message: 'Unknown error', code: 'UNKNOWN', status: 500 };
}
```

## Reference Files

- **[axios-patterns.md](references/axios-patterns.md)**: Advanced interceptor patterns, request deduplication
- **[react-query-patterns.md](references/react-query-patterns.md)**: useQuery/useMutation setup, cache strategies
- **[swr-patterns.md](references/swr-patterns.md)**: SWR configuration, global mutate patterns
