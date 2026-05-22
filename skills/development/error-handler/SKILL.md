---
name: error-handler
description: Design robust error handling with boundaries, logging, and user-friendly messages. Use when implementing error handling, debugging crashes, setting up error tracking, or handling network failures.
---

# Error Handling Architect

## When to Use
- Implementing try/catch blocks
- Creating error boundaries
- Handling API failures
- Setting up error tracking (Sentry)
- Debugging crashes or unhandled exceptions
- Creating user-friendly error messages

## Quick Reference

### Error Boundary Pattern
```tsx
// components/error-boundary.tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
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
    // Log to error tracking service
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

### API Error Handling
```typescript
// lib/api-client.ts
interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}

interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

export async function apiCall<T>(
  url: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return {
        error: {
          code: `HTTP_${response.status}`,
          message: errorData.message || getHttpErrorMessage(response.status),
          details: errorData,
        },
      };
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      return {
        error: {
          code: 'NETWORK_ERROR',
          message: 'Unable to connect. Please check your internet connection.',
        },
      };
    }
    return {
      error: {
        code: 'UNKNOWN_ERROR',
        message: 'An unexpected error occurred. Please try again.',
        details: error,
      },
    };
  }
}

function getHttpErrorMessage(status: number): string {
  const messages: Record<number, string> = {
    400: 'Invalid request. Please check your input.',
    401: 'Please sign in to continue.',
    403: 'You don\'t have permission to do this.',
    404: 'The requested resource was not found.',
    429: 'Too many requests. Please wait a moment.',
    500: 'Server error. Please try again later.',
    502: 'Service temporarily unavailable.',
    503: 'Service is under maintenance.',
  };
  return messages[status] || 'Something went wrong.';
}
```

### Retry with Exponential Backoff
```typescript
// lib/retry.ts
interface RetryOptions {
  maxAttempts?: number;
  baseDelay?: number;
  maxDelay?: number;
  shouldRetry?: (error: unknown) => boolean;
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    baseDelay = 1000,
    maxDelay = 10000,
    shouldRetry = () => true,
  } = options;

  let lastError: unknown;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt === maxAttempts || !shouldRetry(error)) {
        throw error;
      }

      const delay = Math.min(baseDelay * Math.pow(2, attempt - 1), maxDelay);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

// Usage
const data = await withRetry(
  () => fetch('/api/data').then(r => r.json()),
  { maxAttempts: 3, shouldRetry: (e) => e instanceof TypeError }
);
```

### User-Friendly Error Messages
```typescript
// lib/error-messages.ts
const ERROR_MESSAGES: Record<string, string> = {
  // Auth errors
  'auth/invalid-email': 'Please enter a valid email address.',
  'auth/user-not-found': 'No account found with this email.',
  'auth/wrong-password': 'Incorrect password. Please try again.',
  'auth/email-already-in-use': 'An account with this email already exists.',
  'auth/weak-password': 'Password should be at least 6 characters.',
  'auth/too-many-requests': 'Too many attempts. Please try again later.',

  // Firestore errors
  'permission-denied': 'You don\'t have permission to access this.',
  'not-found': 'The requested item was not found.',
  'already-exists': 'This item already exists.',

  // Network errors
  'NETWORK_ERROR': 'Connection failed. Check your internet.',
  'TIMEOUT': 'Request timed out. Please try again.',

  // Default
  'UNKNOWN': 'Something went wrong. Please try again.',
};

export function getUserMessage(error: unknown): string {
  if (error instanceof Error) {
    // Firebase error codes
    const code = (error as { code?: string }).code;
    if (code && ERROR_MESSAGES[code]) {
      return ERROR_MESSAGES[code];
    }
    // Check message patterns
    if (error.message.includes('network')) {
      return ERROR_MESSAGES['NETWORK_ERROR'];
    }
  }
  return ERROR_MESSAGES['UNKNOWN'];
}
```

### Toast Integration
```typescript
// hooks/use-error-handler.ts
import { useToast } from '@ainexsuite/ui';
import { getUserMessage } from '@/lib/error-messages';

export function useErrorHandler() {
  const { toast } = useToast();

  const handleError = (error: unknown, context?: string) => {
    const message = getUserMessage(error);

    // Log for debugging (dev only)
    if (process.env.NODE_ENV === 'development') {
      console.error(`[${context || 'Error'}]`, error);
    }

    // Show user-friendly message
    toast({
      title: 'Error',
      description: message,
      variant: 'error',
    });

    // TODO: Send to error tracking in production
    // if (process.env.NODE_ENV === 'production') {
    //   Sentry.captureException(error, { extra: { context } });
    // }
  };

  return { handleError };
}

// Usage
const { handleError } = useErrorHandler();
try {
  await saveEntry(data);
} catch (error) {
  handleError(error, 'saveEntry');
}
```

## Error Handling Checklist

### API Routes
- [ ] Wrap handler in try/catch
- [ ] Return consistent error format `{ error: { code, message } }`
- [ ] Use appropriate HTTP status codes
- [ ] Don't leak sensitive error details to client
- [ ] Log full error server-side

### React Components
- [ ] Wrap risky components in ErrorBoundary
- [ ] Provide meaningful fallback UI
- [ ] Handle loading and error states
- [ ] Use error boundaries at route level

### Async Operations
- [ ] Handle promise rejections
- [ ] Implement retry for transient failures
- [ ] Show loading state during retries
- [ ] Set reasonable timeouts

### User Experience
- [ ] Show user-friendly messages (not stack traces)
- [ ] Provide recovery actions when possible
- [ ] Don't show same error multiple times
- [ ] Clear error state on retry

## Common Anti-Patterns

### Don't Do This
```typescript
// Silent failures
try {
  await riskyOperation();
} catch {
  // Error swallowed - user has no idea something failed
}

// Exposing internals
catch (error) {
  toast({ description: error.stack }); // Never show stack traces
}

// Generic messages everywhere
catch {
  alert('Error!'); // Not helpful
}
```

### Do This Instead
```typescript
// Proper handling
try {
  await riskyOperation();
} catch (error) {
  handleError(error, 'riskyOperation');
  // Optionally: set error state, show fallback, etc.
}
```

## See Also
- [patterns.md](patterns.md) - Advanced error patterns
- [examples.md](examples.md) - Real-world examples from this codebase
