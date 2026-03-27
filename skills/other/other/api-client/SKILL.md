---
name: api-client
description: |
  Use when setting up API clients - TanStack Query, Axios, JWT token management, error handling, or response parsing.
  NOT when plain fetch calls, non-API data handling, or unrelated UI logic.
  Triggers: "API client", "data fetching", "JWT token", "error handling", "paginated list", "TanStack Query".
---

# API Client Skill

## Overview

Expert guidance for API client implementation using TanStack Query/Axios, including JWT token attachment via interceptors, global error handling with toasts, type-safe response parsing with Zod, and offline detection for robust data fetching.

## When This Skill Applies

This skill triggers when users request:
- **API Setup**: "Setup API client", "Configure TanStack Query", "Axios instance"
- **Data Fetching**: "Fetch student data", "Get attendance", "API calls"
- **JWT/Token**: "Attach JWT token", "Bearer token headers", "Token refresh"
- **Error Handling**: "API error toast", "Handle 401", "Retry failed requests"
- **Response Parsing**: "Type-safe responses", "Zod validation", "Parse API data"
- **Pagination**: "Paginated list", "Infinite query", "Load more data"

## Core Rules

### 1. Setup: TanStack Query Configuration

```typescript
// lib/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 1,
    },
  },
});

// app/layout.tsx or app/providers.tsx
'use client';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/queryClient';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

**Requirements:**
- Use TanStack Query v5 for data fetching
- Configure appropriate staleTime and gcTime
- Set retry strategy with exponential backoff
- Wrap app with QueryClientProvider
- Use Axios as fallback for complex scenarios

### 2. JWT: Interceptors Auto-Attach

```typescript
// lib/apiClient.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { useAuthStore } from '@/lib/auth-store';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001/api',
      timeout: 10000, // 10 seconds
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - attach JWT token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const { session } = useAuthStore.getState();
        if (session?.token && config.headers) {
          config.headers.Authorization = `Bearer ${session.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors and 401
    this.client.interceptors.response.use(
      (response: AxiosResponse) => response,
      async (error) => {
        if (error.response?.status === 401) {
          const { refresh } = useAuthStore.getState();
          try {
            const newToken = await refresh();
            if (newToken) {
              error.config!.headers!.Authorization = `Bearer ${newToken}`;
              return this.client(error.config!);
            }
          } catch (refreshError) {
            useAuthStore.getState().signOut();
            window.location.href = '/auth/login';
          }
        }
        return Promise.reject(error);
      }
    );
  }

  get<T>(url: string, config?: AxiosRequestConfig) {
    return this.client.get<T>(url, config);
  }

  post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.client.post<T>(url, data, config);
  }

  put<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.client.put<T>(url, data, config);
  }

  delete<T>(url: string, config?: AxiosRequestConfig) {
    return this.client.delete<T>(url, config);
  }
}

export const apiClient = new ApiClient();
```

**Requirements:**
- Create Axios instance with baseURL and timeout
- Request interceptor attaches JWT from auth store
- Response interceptor handles 401 and token refresh
- Automatic redirect to login on refresh failure
- Type-safe methods with TypeScript generics

### 3. Errors: Global Handler

```typescript
// lib/errorHandler.ts
import axios from 'axios';
import { toast } from 'sonner';

export const handleApiError = (error: any) => {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.message || error.message;

    switch (error.response?.status) {
      case 400:
        toast.error('Bad Request', { description: message });
        break;
      case 401:
        toast.error('Unauthorized', { description: 'Please log in again' });
        break;
      case 403:
        toast.error('Forbidden', { description: 'You do not have permission' });
        break;
      case 404:
        toast.error('Not Found', { description: message });
        break;
      case 429:
        toast.error('Too Many Requests', { description: 'Please try again later' });
        break;
      case 500:
        toast.error('Server Error', { description: message });
        break;
      default:
        toast.error('Error', { description: message || 'Something went wrong' });
    }
  } else {
    toast.error('Network Error', { description: error.message || 'Something went wrong' });
  }
};
```

```typescript
// hooks/useApi.ts
import { useQuery, useMutation, UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';
import { apiClient } from '@/lib/apiClient';
import { handleApiError } from '@/lib/errorHandler';
import { z } from 'zod';

export function useApi<T>(
  queryKey: any[],
  url: string,
  options?: Omit<UseQueryOptions<T>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey,
    queryFn: async () => {
      const response = await apiClient.get<T>(url);
      return response.data;
    },
    ...options,
  });
}

export function useApiMutation<T, V = any>(
  url: string,
  options?: Omit<UseMutationOptions<T, V, void>, 'mutationFn'>,
  schema?: z.ZodSchema<T>
) {
  return useMutation({
    mutationFn: async (variables: V) => {
      const response = await apiClient.post<T>(url, variables);

      // Zod validation if schema provided
      if (schema) {
        try {
          const parsed = schema.parse(response.data);
          return parsed;
        } catch (error) {
          if (error instanceof z.ZodError) {
            toast.error('Validation Error', { description: error.errors[0].message });
            throw new Error(`Response validation failed: ${error.errors[0].message}`);
          }
        }
      }

      return response.data;
    },
    onError: (error) => {
      options?.onError?.(error);
      handleApiError(error);
    },
    onSuccess: (data, variables) => {
      options?.onSuccess?.(data, variables);
      if (options?.context?.successMessage) {
        toast.success('Success', { description: options.context.successMessage });
      }
    },
  });
}
```

**Requirements:**
- Global error handler with toast notifications
- Handle all HTTP status codes appropriately
- Zod schema validation for response parsing
- Automatic error display in toasts
- Success message handling for mutations

### 4. Parsing: Typed Responses, Optimistic Updates

```typescript
// lib/api/types.ts
import { z } from 'zod';

// Student type with Zod schema
export const StudentSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  role: z.enum(['student', 'teacher', 'admin']),
  classId: z.string().nullable(),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export type Student = z.infer<typeof StudentSchema>;

// Attendance type
export const AttendanceSchema = z.object({
  id: z.string(),
  studentId: z.string(),
  date: z.string(),
  status: z.enum(['present', 'absent', 'late']),
  notes: z.string().optional(),
});

export type Attendance = z.infer<typeof AttendanceSchema>;

// Paginated response type
export function PaginatedResponseSchema<T extends z.ZodTypeAny>(itemSchema: T) {
  return z.object({
    data: z.array(itemSchema),
    meta: z.object({
      total: z.number(),
      page: z.number(),
      pageSize: z.number(),
      totalPages: z.number(),
    }),
  });
}

// hooks/useStudents.ts
import { useApi } from './useApi';
import { StudentSchema, PaginatedResponseSchema } from '@/lib/api/types';

export function useStudents(page = 1, pageSize = 20) {
  return useApi(
    ['students', 'page', page],
    `/students?page=${page}&pageSize=${pageSize}`,
    {
      select: (data) => {
        const parsed = PaginatedResponseSchema(StudentSchema).parse(data);
        return parsed;
      },
    }
  );
}

// hooks/useUpdateStudent.ts
export function useUpdateStudent() {
  const queryClient = useQueryClient();

  return useApiMutation(
    (variables: { id: string; data: Partial<Student> }) =>
      `/students/${variables.id}`,
    {
      onSuccess: (_, variables) => {
        // Invalidate and refetch
        queryClient.invalidateQueries({ queryKey: ['students'] });
        queryClient.invalidateQueries({ queryKey: ['student', variables.id] });
      },
      context: { successMessage: 'Student updated successfully' },
    }
  );
}

// hooks/useDeleteStudent.ts
export function useDeleteStudent() {
  const queryClient = useQueryClient();

  return useApiMutation(
    (id: string) => `/students/${id}`,
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['students'] });
      },
      context: { successMessage: 'Student deleted successfully' },
    }
  );
}
```

```typescript
// Infinite queries for pagination
import { useInfiniteQuery } from '@tanstack/react-query';
import { StudentSchema } from '@/lib/api/types';

export function useInfiniteStudents() {
  return useInfiniteQuery({
    queryKey: ['students', 'infinite'],
    queryFn: async ({ pageParam = 1 }) => {
      const response = await apiClient.get(`/students?page=${pageParam}&pageSize=20`);
      const data = response.data.map((item: any) => StudentSchema.parse(item));
      return {
        data,
        nextPage: data.length === 20 ? pageParam + 1 : null,
      };
    },
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage,
  });
}

// Optimistic updates with rollback
export function useUpdateAttendance() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ studentId, date, status }: { studentId: string; date: string; status: string }) => {
      return apiClient.put(`/attendance/${studentId}/${date}`, { status });
    },
    onMutate: async ({ studentId, date, status }) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['attendance', studentId] });

      // Snapshot previous value
      const previousAttendance = queryClient.getQueryData(['attendance', studentId]);

      // Optimistically update
      queryClient.setQueryData(['attendance', studentId], (old: any) => ({
        ...old,
        data: old.data.map((item: any) =>
          item.date === date ? { ...item, status } : item
        ),
      }));

      return { previousAttendance };
    },
    onError: (error, variables, context) => {
      // Rollback on error
      if (context?.previousAttendance) {
        queryClient.setQueryData(['attendance', variables.studentId], context.previousAttendance);
      }
    },
    onSettled: (_, __, variables) => {
      // Refetch on success or error
      queryClient.invalidateQueries({ queryKey: ['attendance', variables.studentId] });
    },
  });
}

// Offline detection
export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

// AbortController for cancelable requests
export function useFetchWithAbort<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  const fetchData = useCallback(async () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    abortControllerRef.current = new AbortController();
    setLoading(true);
    setError(null);

    try {
      const response = await apiClient.get<T>(url, {
        signal: abortControllerRef.current.signal,
      });
      setData(response.data);
    } catch (err) {
      if (err instanceof Error && err.name !== 'AbortError') {
        setError(err);
      }
    } finally {
      setLoading(false);
    }
  }, [url]);

  return { data, error, loading, refetch: fetchData, abort: () => abortControllerRef.current?.abort() };
}
```

**Requirements:**
- Infinite queries for paginated lists
- Optimistic updates for immediate feedback
- Rollback on error
- Offline detection and handling
- AbortController for cancelable requests

## Output Requirements

### Code Files

1. **API Client**:
   - `lib/apiClient.ts` - Axios instance with interceptors
   - `lib/queryClient.ts` - TanStack Query configuration

2. **Error Handling**:
   - `lib/errorHandler.ts` - Global error handler
   - `hooks/useApi.ts` - Type-safe API hooks

3. **Type Definitions**:
   - `lib/api/types.ts` - Zod schemas and types

4. **Feature Hooks**:
   - `hooks/useStudents.ts` - Student-specific hooks
   - `hooks/useAttendance.ts` - Attendance-specific hooks

### Integration Requirements

- **@auth-integration**: Use JWT tokens from auth store
- **@react-component**: Functional components with hooks
- **@tailwind-css**: Responsive UI with mobile support

### Documentation

- **PHR**: Create Prompt History Record for API decisions
- **ADR**: Document caching strategy, retry policy
- **Comments**: Document API endpoints and data flow

## Workflow

1. **Setup API Client**
   - Configure TanStack Query
   - Create Axios instance
   - Setup JWT interceptors

2. **Define Types**
   - Create Zod schemas
   - Export TypeScript types

3. **Create Hooks**
   - Build useApi and useApiMutation
   - Add feature-specific hooks
   - Implement error handling

4. **Integrate with Auth**
   - Attach JWT tokens automatically
   - Handle 401 responses
   - Refresh tokens on expiry

5. **Implement Features**
   - Query hooks for data fetching
   - Mutation hooks with optimistic updates
   - Infinite queries for pagination

6. **Test and Optimize**
   - Test error scenarios
   - Verify offline behavior
   - Optimize caching strategy

## Quality Checklist

Before completing any API client implementation:

- [ ] **Typesafe Requests/Responses**: Zod schemas for all data
- [ ] **Retry on Fail**: Exponential backoff for retries
- [ ] **Offline Detection**: Handle network disconnections
- [ ] **AbortController**: Support cancelable requests
- [ ] **JWT Auto-Attach**: Headers with Authorization Bearer
- [ ] **Error Handling**: Global error handler with toasts
- [ ] **401 Logout**: Automatic redirect on token expiry
- [ ] **Zod Validation**: Response schema validation
- [ ] **Optimistic Updates**: Immediate UI feedback
- [ ] **Query Invalidation**: Automatic cache updates

## Common Patterns

### Fetch Student Data

```typescript
// hooks/useStudent.ts
export function useStudent(id: string) {
  return useApi(
    ['student', id],
    `/students/${id}`,
    {
      enabled: !!id, // Only fetch if id exists
    }
  );
}

// Usage
function StudentProfile({ studentId }: { studentId: string }) {
  const { data: student, isLoading, error } = useStudent(studentId);

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <h1>{student?.name}</h1>
      <p>{student?.email}</p>
    </div>
  );
}
```

### API Error Toast with Zod Parse

```typescript
// hooks/useCreateStudent.ts
export function useCreateStudent() {
  const queryClient = useQueryClient();

  return useApiMutation(
    async (data: { name: string; email: string }) => {
      const response = await apiClient.post('/students', data);
      // Zod validation
      const parsed = StudentSchema.parse(response.data);
      return parsed;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['students'] });
      },
      context: { successMessage: 'Student created successfully' },
    }
  );
}

// Usage
function CreateStudentForm() {
  const { mutate: createStudent, isPending } = useCreateStudent();

  const handleSubmit = (data: FormData) => {
    createStudent(data);
  };

  return <form onSubmit={handleSubmit}>{/* form fields */}</form>;
}
```

### Paginated List with Infinite Query

```typescript
// hooks/useInfiniteStudents.ts
export function useInfiniteStudents() {
  return useInfiniteQuery({
    queryKey: ['students', 'infinite'],
    queryFn: async ({ pageParam = 1 }) => {
      const response = await apiClient.get(`/students?page=${pageParam}&pageSize=20`);
      const parsed = z.array(StudentSchema).parse(response.data);
      return {
        data: parsed,
        nextPage: parsed.length === 20 ? pageParam + 1 : null,
      };
    },
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage,
  });
}

// Usage
function StudentList() {
  const { data, isLoading, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteStudents();

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.data.map((student) => (
            <StudentCard key={student.id} student={student} />
          ))}
        </div>
      ))}
      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

### Attendance Fetch with Offline Support

```typescript
// hooks/useAttendance.ts
export function useAttendance(studentId: string, date: string) {
  const isOnline = useOnlineStatus();

  return useApi(
    ['attendance', studentId, date],
    `/attendance/${studentId}/${date}`,
    {
      enabled: !!studentId && !!date && isOnline,
      staleTime: 5 * 60 * 1000,
    }
  );
}

// Usage
function AttendanceCard({ studentId, date }: { studentId: string; date: string }) {
  const { data: attendance, isLoading, error } = useAttendance(studentId, date);
  const isOnline = useOnlineStatus();

  if (!isOnline) {
    return <OfflineMessage />;
  }

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div>
      <p>Status: {attendance?.status}</p>
    </div>
  );
}
```

## Caching Strategy

```typescript
// lib/queryClient.ts
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Fresh data is considered stale after 5 minutes
      staleTime: 5 * 60 * 1000,
      // Garbage collect unused queries after 10 minutes
      gcTime: 10 * 60 * 1000,
      // Retry failed requests 3 times
      retry: 3,
      // Exponential backoff: 1s, 2s, 4s (max 30s)
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      // Refetch on window focus (optional)
      refetchOnWindowFocus: false,
      // Refetch on reconnect
      refetchOnReconnect: true,
    },
  },
});
```

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:3001/api
# For production
NEXT_PUBLIC_API_URL=https://api.yourapp.com
```

## References

- TanStack Query: https://tanstack.com/query/latest
- Axios: https://axios-http.com
- Zod: https://zod.dev
- React Query Examples: https://tanstack.com/query/latest/docs/react/examples
