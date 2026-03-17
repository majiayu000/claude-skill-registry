---
name: error-boundary-generator
description: Analyze a React application and generate error boundaries with appropriate fallback UIs where they're missing. Use when asked to add error boundaries, handle errors in React, create fallback UIs, add error.tsx files, or improve error handling in a React/Next.js app.
---

# Error Boundary Generator

Before generating any output, read `config/defaults.md` and adapt all patterns, imports, and code examples to the user's configured stack.

## Process

1. Scan the React component tree and identify components that need error boundaries.
2. For each gap, generate an error boundary with a typed fallback component.
3. For Next.js App Router, generate `error.tsx` and `loading.tsx` files where missing.

## Identification Rules

Scan for components that:
- **Fetch data**: contain `fetch()`, `useQuery`, `useSWR`, server component `async` functions, or Prisma calls
- **Use external services**: Stripe, auth providers, third-party SDKs
- **Have complex state logic**: `useReducer` with many cases, complex `useEffect` chains
- **Render user-generated content**: `dangerouslySetInnerHTML`, rich text renderers, markdown parsers
- **Are page-level route components**: `page.tsx` files in Next.js App Router

## Error Types

Generate different fallback UIs based on error type:

### Recoverable Errors (retry button)

For data fetching failures, network errors, timeout errors:

```tsx
"use client";

import { useEffect } from "react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>We couldn't load this content. Please try again.</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

### Auth Errors (redirect to login)

For 401/403 responses detected in the error:

```tsx
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Error({ error }: { error: Error }) {
  const router = useRouter();

  useEffect(() => {
    if (error.message.includes("401") || error.message.includes("Unauthorized")) {
      router.push("/login");
    }
  }, [error, router]);

  return (
    <div role="alert">
      <h2>Access denied</h2>
      <p>Please sign in to view this page.</p>
      <button onClick={() => router.push("/login")}>Sign in</button>
    </div>
  );
}
```

### Not Found (404 UI)

Generate `not-found.tsx` for dynamic routes:

```tsx
import Link from "next/link";

export default function NotFound() {
  return (
    <div>
      <h2>Not found</h2>
      <p>The requested resource doesn't exist.</p>
      <Link href="/">Go home</Link>
    </div>
  );
}
```

### Server Errors (500 UI)

For `global-error.tsx` at the app root:

```tsx
"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div role="alert">
          <h2>Something went wrong</h2>
          <p>An unexpected error occurred. Please try again or contact support.</p>
          {error.digest && <p>Error reference: {error.digest}</p>}
          <button onClick={reset}>Try again</button>
        </div>
      </body>
    </html>
  );
}
```

## Component-Level Error Boundaries

For non-Next.js or for wrapping specific components within a page:

```tsx
"use client";

import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert">
          <p>Something went wrong.</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## Loading States

Generate `loading.tsx` alongside `error.tsx` where missing:

```tsx
export default function Loading() {
  return (
    <div role="status" aria-busy="true">
      <span>Loading...</span>
    </div>
  );
}
```

## Output Format

```
## Error Boundary Report

### Gaps Found
| Location | Risk | Reason | Generated |
|----------|------|--------|-----------|
| app/dashboard/page.tsx | High | Fetches data, no error.tsx | error.tsx + loading.tsx |
| components/PaymentForm.tsx | High | Stripe integration | ErrorBoundary wrapper |
| app/posts/[id]/page.tsx | Medium | Dynamic route | not-found.tsx + error.tsx |

### Files Generated
[List of all generated files with their contents]
```

## Reference

See [references/error-patterns.md](references/error-patterns.md) for error boundary placement strategy, Next.js error hierarchy, and logging integration patterns.
