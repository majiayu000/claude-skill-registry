---
name: error-boundary
description: React error boundary hierarchy, fallback UI patterns, offline-first fallback, retry mechanisms, and graceful degradation.
---

# Error Boundary Patterns

React error boundary hierarchy and graceful degradation patterns.

## Error Boundary Component

```typescript
// Class-based (React requirement for componentDidCatch)
interface ErrorBoundaryProps {
  children: React.ReactNode
  fallback?: React.ComponentType<FallbackProps>
  onError?: (error: Error, info: React.ErrorInfo) => void
}

interface ErrorBoundaryState {
  error: Error | null
}

export interface FallbackProps {
  error: Error
  reset: () => void
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('[ErrorBoundary]', error, info.componentStack)
    this.props.onError?.(error, info)
  }

  reset = () => this.setState({ error: null })

  render() {
    if (this.state.error) {
      const Fallback = this.props.fallback ?? DefaultFallback
      return <Fallback error={this.state.error} reset={this.reset} />
    }
    return this.props.children
  }
}

// react-error-boundary library (recommended — battle-tested)
// npm install react-error-boundary
import { ErrorBoundary } from 'react-error-boundary'

<ErrorBoundary
  FallbackComponent={MyFallback}
  onError={(error, info) => reportToSentry(error, info)}
  onReset={() => queryClient.clear()}
>
  <App />
</ErrorBoundary>
```

## Error Boundary Hierarchy

```
App (top-level — catches everything, shows full-page error)
├── Navigation (no boundary — nav errors bubble to app)
├── <ErrorBoundary fallback={PageError}>           ← page level
│   └── DashboardPage
│       ├── <ErrorBoundary fallback={SectionError}>  ← section level
│       │   └── StatsSection
│       └── <ErrorBoundary fallback={WidgetError}>   ← widget level
│           └── ChartWidget                           (one fails, others work)
└── Sidebar (separate boundary — sidebar error ≠ main content error)
```

```typescript
// Page-level boundary (reset on navigation)
import { usePathname } from 'next/navigation'
import { ErrorBoundary } from 'react-error-boundary'

export function PageErrorBoundary({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <ErrorBoundary
      key={pathname}              // reset boundary on route change
      FallbackComponent={PageErrorFallback}
      onError={reportError}
    >
      {children}
    </ErrorBoundary>
  )
}

// Widget-level boundary (isolated, inline fallback)
export function WidgetErrorBoundary({ children, name }: { children: React.ReactNode; name: string }) {
  return (
    <ErrorBoundary
      fallback={<WidgetErrorFallback name={name} />}
      onError={(err) => reportError(err, { widget: name })}
    >
      {children}
    </ErrorBoundary>
  )
}
```

## Fallback UI Design Patterns

```typescript
// Full-page fallback (app boundary)
function PageErrorFallback({ error, reset }: FallbackProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-2xl font-bold text-gray-900">Something went wrong</h1>
      <p className="max-w-md text-gray-500">
        {process.env.NODE_ENV === 'development'
          ? error.message
          : 'An unexpected error occurred. Our team has been notified.'}
      </p>
      <div className="flex gap-3">
        <button onClick={reset} className="btn btn-primary">Try again</button>
        <a href="/" className="btn btn-outline">Go home</a>
      </div>
      {process.env.NODE_ENV === 'development' && (
        <pre className="mt-4 max-w-2xl overflow-auto rounded bg-red-50 p-4 text-left text-sm text-red-800">
          {error.stack}
        </pre>
      )}
    </div>
  )
}

// Inline section fallback (section boundary)
function SectionErrorFallback({ error, reset }: FallbackProps) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center">
      <p className="text-red-700 font-medium">Failed to load this section</p>
      <button onClick={reset} className="mt-3 text-sm text-red-600 underline hover:no-underline">
        Retry
      </button>
    </div>
  )
}

// Toast-style fallback (non-critical widget)
function WidgetErrorFallback({ name }: { name: string }) {
  return (
    <div className="flex items-center gap-2 rounded border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-700">
      <span>⚠</span>
      <span>{name} unavailable</span>
    </div>
  )
}
```

## Retry Mechanism in Error Boundaries

```typescript
import { ErrorBoundary } from 'react-error-boundary'
import { useState, useCallback } from 'react'

function RetryFallback({ error, reset }: FallbackProps) {
  const [retries, setRetries] = useState(0)
  const maxRetries = 3

  const handleRetry = useCallback(() => {
    if (retries < maxRetries) {
      setRetries(r => r + 1)
      reset()
    }
  }, [retries, reset])

  return (
    <div className="rounded-lg border bg-white p-6 text-center">
      <p className="font-medium text-gray-900">Failed to load</p>
      {retries < maxRetries ? (
        <button onClick={handleRetry} className="mt-4 btn btn-sm">
          Retry ({maxRetries - retries} left)
        </button>
      ) : (
        <p className="mt-4 text-sm text-gray-400">
          Please refresh the page or <a href="/support" className="underline">contact support</a>.
        </p>
      )}
    </div>
  )
}
```

## Error Reporting (Sentry Integration)

```typescript
import * as Sentry from '@sentry/nextjs'

export function reportError(
  error: Error,
  context?: Record<string, unknown>,
  info?: React.ErrorInfo
) {
  if (process.env.NODE_ENV === 'development') {
    console.error('[Error]', error, context)
    return
  }

  Sentry.withScope(scope => {
    if (context) scope.setExtras(context)
    if (info?.componentStack) scope.setExtra('componentStack', info.componentStack)
    Sentry.captureException(error)
  })
}
```

## Offline Detection and Fallback UI

```typescript
'use client'
import { useState, useEffect } from 'react'

function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof window !== 'undefined' ? navigator.onLine : true
  )
  useEffect(() => {
    const on  = () => setIsOnline(true)
    const off = () => setIsOnline(false)
    window.addEventListener('online',  on)
    window.addEventListener('offline', off)
    return () => { window.removeEventListener('online', on); window.removeEventListener('offline', off) }
  }, [])
  return isOnline
}

export function OfflineBanner() {
  const isOnline = useOnlineStatus()
  if (isOnline) return null
  return (
    <div role="status" className="fixed top-0 inset-x-0 z-50 bg-amber-500 py-2 text-center text-sm font-medium text-white">
      You are offline. Changes will sync when connection is restored.
    </div>
  )
}
```

## Partial Failure Handling

```typescript
// Multiple independent widgets — one fails, others keep working
export function Dashboard() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <WidgetErrorBoundary name="Revenue Chart"><RevenueChart /></WidgetErrorBoundary>
      <WidgetErrorBoundary name="User Stats"><UserStats /></WidgetErrorBoundary>
      <WidgetErrorBoundary name="Activity Feed"><ActivityFeed /></WidgetErrorBoundary>
      <WidgetErrorBoundary name="Notifications"><NotificationPanel /></WidgetErrorBoundary>
    </div>
  )
}

// Graceful degradation: show stale data when fetch fails
async function StatsWidget() {
  try {
    const stats = await fetchStats()
    return <StatsDisplay stats={stats} fresh />
  } catch {
    const cached = await getCachedStats()
    if (cached) return <StatsDisplay stats={cached} stale />
    throw new Error('Stats unavailable')   // let error boundary handle
  }
}
```

## Error Recovery (Reset on Navigation)

```typescript
import { usePathname } from 'next/navigation'
import { useEffect, useRef } from 'react'
import { useErrorBoundary } from 'react-error-boundary'

function NavigationErrorReset() {
  const pathname = usePathname()
  const { resetBoundary } = useErrorBoundary()
  const prevPath = useRef(pathname)

  useEffect(() => {
    if (prevPath.current !== pathname) {
      prevPath.current = pathname
      resetBoundary()
    }
  }, [pathname, resetBoundary])

  return null
}

// Place inside ErrorBoundary to auto-reset on navigation
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <NavigationErrorReset />
  {children}
</ErrorBoundary>
```

## Development vs Production Error Display

```typescript
function ErrorFallback({ error, reset }: FallbackProps) {
  const isDev = process.env.NODE_ENV === 'development'
  return (
    <div role="alert" className="rounded-lg border border-red-200 bg-red-50 p-6">
      <h2 className="font-semibold text-red-900">
        {isDev ? `Error: ${error.name}` : 'Something went wrong'}
      </h2>
      {isDev ? (
        <details className="mt-3">
          <summary className="cursor-pointer text-sm text-red-700">Stack trace</summary>
          <pre className="mt-2 overflow-auto text-xs text-red-800 whitespace-pre-wrap">{error.stack}</pre>
        </details>
      ) : (
        <p className="mt-2 text-sm text-red-700">An unexpected error occurred. Please try again.</p>
      )}
      <button onClick={reset} className="mt-4 text-sm font-medium text-red-700 underline">Try again</button>
    </div>
  )
}
```

## Testing Error Boundaries

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ErrorBoundary } from 'react-error-boundary'

function BrokenComponent({ shouldThrow }: { shouldThrow: boolean }) {
  if (shouldThrow) throw new Error('Test error')
  return <div>Working fine</div>
}

describe('ErrorBoundary', () => {
  beforeEach(() => vi.spyOn(console, 'error').mockImplementation(() => {}))
  afterEach(() => vi.mocked(console.error).mockRestore())

  it('shows fallback UI when child throws', () => {
    render(
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <BrokenComponent shouldThrow />
      </ErrorBoundary>
    )
    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument()
  })

  it('resets and shows content after retry', async () => {
    const user = userEvent.setup()
    let shouldThrow = true
    function Toggle() {
      if (shouldThrow) throw new Error('Test error')
      return <div>Recovered</div>
    }
    render(<ErrorBoundary FallbackComponent={ErrorFallback}><Toggle /></ErrorBoundary>)
    shouldThrow = false
    await user.click(screen.getByRole('button', { name: /try again/i }))
    expect(screen.getByText('Recovered')).toBeInTheDocument()
  })
})
```

## Decision Matrix

| Scope | Fallback Type | When |
|-------|--------------|------|
| Widget | Inline placeholder | Non-critical UI section |
| Section | Collapsed + retry button | Independent feature area |
| Page | Full page with retry | Page-level data failure |
| App | Full page with refresh | Unrecoverable state |
| Network | Toast + offline banner | Connectivity issues |

---

## Original Patterns (preserved for reference)

## Basic Error Boundary (react-error-boundary)

```tsx
import { ErrorBoundary, FallbackProps } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="p-4 bg-red-50 border border-red-200 rounded">
      <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
      <pre className="mt-2 text-sm text-red-600">{error.message}</pre>
      <button
        onClick={resetErrorBoundary}
        className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Try again
      </button>
    </div>
  );
}

// Usage
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <RiskyComponent />
</ErrorBoundary>
```

## Error Boundary Hierarchy

```
App Error Boundary (full page fallback)
├── Layout Error Boundary (layout-level recovery)
│   ├── Sidebar Error Boundary (sidebar collapses gracefully)
│   └── Main Content Error Boundary
│       ├── Widget A Error Boundary (individual widget fails)
│       ├── Widget B Error Boundary
│       └── Widget C Error Boundary
```

```tsx
// App-level: full page fallback with navigation
<ErrorBoundary FallbackComponent={FullPageError}>
  <Layout>
    {/* Section-level: isolated failures */}
    <ErrorBoundary FallbackComponent={SectionError}>
      <Dashboard />
    </ErrorBoundary>
    <ErrorBoundary FallbackComponent={SectionError}>
      <Analytics />
    </ErrorBoundary>
  </Layout>
</ErrorBoundary>
```

## Next.js App Router (error.tsx)

```tsx
// app/dashboard/error.tsx
'use client';

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log to error reporting service
    reportError(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2>Dashboard could not load</h2>
      <p className="text-gray-500">{error.message}</p>
      <button onClick={reset} className="mt-4 btn-primary">
        Retry
      </button>
    </div>
  );
}
```

## Fallback UI Patterns

```tsx
// 1. Inline fallback (widget level)
function InlineFallback({ error }: { error: Error }) {
  return (
    <div className="p-3 text-sm text-gray-500 bg-gray-50 rounded">
      Unable to load this section
    </div>
  );
}

// 2. Toast notification (non-critical)
function ToastFallback({ error, resetErrorBoundary }: FallbackProps) {
  useEffect(() => {
    toast.error(error.message, {
      action: { label: 'Retry', onClick: resetErrorBoundary },
    });
  }, [error]);
  return null; // renders nothing, shows toast instead
}

// 3. Full page (critical)
function FullPageFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold">Something went wrong</h1>
      <p className="mt-2 text-gray-600">Please try refreshing the page</p>
      <div className="mt-4 space-x-3">
        <button onClick={resetErrorBoundary}>Retry</button>
        <button onClick={() => window.location.reload()}>Refresh</button>
      </div>
    </div>
  );
}
```

## Retry with Error Boundary

```tsx
import { ErrorBoundary } from 'react-error-boundary';
import { QueryErrorResetBoundary } from '@tanstack/react-query';

// Auto-reset on navigation
<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onReset={() => {
    // Clear any cached state that caused the error
    queryClient.invalidateQueries();
  }}
  resetKeys={[pathname]} // auto-reset when URL changes
>
  <Outlet />
</ErrorBoundary>

// With TanStack Query
<QueryErrorResetBoundary>
  {({ reset }) => (
    <ErrorBoundary onReset={reset} FallbackComponent={ErrorFallback}>
      <SuspenseComponent />
    </ErrorBoundary>
  )}
</QueryErrorResetBoundary>
```

## Error Reporting

```tsx
function logError(error: Error, info: { componentStack?: string }) {
  // Send to Sentry/monitoring
  if (typeof window !== 'undefined' && process.env.NODE_ENV === 'production') {
    Sentry.captureException(error, {
      extra: { componentStack: info.componentStack },
    });
  }
}

<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onError={logError}
>
  <App />
</ErrorBoundary>
```

## Offline Detection

```tsx
function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

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

// Offline banner
function OfflineBanner() {
  const isOnline = useOnlineStatus();
  if (isOnline) return null;

  return (
    <div className="fixed top-0 inset-x-0 bg-yellow-500 text-center py-2 z-50">
      You are offline. Some features may be unavailable.
    </div>
  );
}
```

## Testing Error Boundaries

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

function ThrowError() {
  throw new Error('Test error');
}

test('renders fallback on error', () => {
  const spy = vi.spyOn(console, 'error').mockImplementation(() => {});

  render(
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <ThrowError />
    </ErrorBoundary>
  );

  expect(screen.getByRole('alert')).toBeInTheDocument();
  expect(screen.getByText(/test error/i)).toBeInTheDocument();

  spy.mockRestore();
});

test('resets on retry click', async () => {
  let shouldThrow = true;
  function MaybeThrow() {
    if (shouldThrow) throw new Error('Boom');
    return <div>Recovered</div>;
  }

  render(
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <MaybeThrow />
    </ErrorBoundary>
  );

  shouldThrow = false;
  await userEvent.click(screen.getByText('Try again'));
  expect(screen.getByText('Recovered')).toBeInTheDocument();
});
```

## Decision Matrix

| Scope | Fallback Type | When |
|-------|--------------|------|
| Widget | Inline placeholder | Non-critical UI section |
| Section | Collapsed + retry button | Independent feature area |
| Page | Full page with retry | Page-level data failure |
| App | Full page with refresh | Unrecoverable state |
| Network | Toast + offline banner | Connectivity issues |
