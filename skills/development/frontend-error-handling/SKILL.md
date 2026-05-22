---
name: frontend-error-handling
description: Provides error handling patterns for React applications. This skill should be used when implementing error boundaries, API error interceptors, error tracking, or user-friendly error messages.
---

# Frontend Error Handling

This skill provides patterns for handling errors in React applications.

## Canonical Examples

Study these real implementations:
- **API Client Interceptor**: [client.ts](../../../apps/erify_studios/src/lib/api/client.ts)
- **Error Boundary**: [error-boundary.tsx](../../../apps/erify_studios/src/components/error-boundary.tsx)

---

## Error Handling Layers

### 1. API Client Interceptor (Global)

Handle auth errors and network errors globally:

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
    
    if (error.response?.status === 403) {
      toast.error('You do not have permission to perform this action');
    }
    
    if (!error.response) {
      toast.error('Network error. Please check your connection.');
    }
    
    return Promise.reject(error);
  }
);
```

### 2. Error Boundaries (Component Tree)

Catch rendering errors:

```tsx
import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="flex flex-col items-center justify-center h-screen">
          <h2>Something went wrong</h2>
          <button onClick={() => window.location.reload()}>Reload page</button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 3. TanStack Query Error Handling

Handle query/mutation errors:

```typescript
// Global error handler
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error) => {
        if (error instanceof AxiosError) {
          toast.error(error.response?.data?.message || 'Failed to fetch data');
        }
      },
    },
    mutations: {
      onError: (error) => {
        if (error instanceof AxiosError) {
          toast.error(error.response?.data?.message || 'Operation failed');
        }
      },
    },
  },
});

// Per-query error handling
const { data, error, isError } = useQuery({
  queryKey: ['tasks'],
  queryFn: fetchTasks,
});

if (isError) {
  return <ErrorState message={error.message} />;
}
```

### 4. Form Validation Errors

Handle validation errors from Zod:

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const form = useForm({
  resolver: zodResolver(createTaskSchema),
});

// Errors automatically shown via form.formState.errors
<FormField
  control={form.control}
  name="name"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Name</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />  {/* Shows validation error */}
    </FormItem>
  )}
/>
```

---

## Error Display Patterns

### Toast Notifications (Transient Errors)

```typescript
import { toast } from 'sonner';

// Success
toast.success('Task created successfully');

// Error
toast.error('Failed to create task');

// Warning
toast.warning('This action cannot be undone');
```

### Inline Error Messages (Form Errors)

```tsx
{error && <p className="text-sm text-destructive">{error.message}</p>}
```

### Error States (Component-level)

```tsx
if (isError) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <AlertCircle className="h-12 w-12 text-destructive mb-4" />
      <h3 className="text-lg font-semibold">Failed to load data</h3>
      <p className="text-sm text-muted-foreground">{error.message}</p>
      <Button onClick={() => refetch()} className="mt-4">Try again</Button>
    </div>
  );
}
```

---

## Best Practices Checklist

- [ ] API client has response interceptor for auth/network errors
- [ ] Error boundaries wrap route components
- [ ] TanStack Query has global error handlers
- [ ] Form validation uses Zod with react-hook-form
- [ ] Toast notifications for transient errors
- [ ] Inline error messages for form fields
- [ ] Error states for failed queries
- [ ] Retry buttons for recoverable errors
- [ ] User-friendly error messages (no stack traces)

---

## Related Skills

- [frontend-api-layer](../frontend-api-layer/SKILL.md) - API client setup
- [data-validation](../data-validation/SKILL.md) - Validation patterns
