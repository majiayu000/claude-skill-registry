---
name: web-error-handling-error-boundaries
description: Error boundary patterns, fallback UI, reset/retry functionality, react-error-boundary library
---

# React Error Boundaries

> **Quick Guide:** Error boundaries catch JavaScript errors in component trees and display fallback UI. Use `react-error-boundary` library for production apps. Place boundaries strategically around features (not just root). Boundaries do NOT catch event handler, async, or SSR errors. **React 19+**: Use `createRoot` options (`onCaughtError`, `onUncaughtError`, `onRecoverableError`) for centralized error logging.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `getDerivedStateFromError` for rendering fallback UI - it runs during render phase)**

**(You MUST use `componentDidCatch` for side effects like logging - it runs during commit phase)**

**(You MUST wrap error boundaries around feature sections, not just the app root)**

**(You MUST provide reset/retry functionality for recoverable errors)**

**(You MUST use `role="alert"` on fallback UI for accessibility)**

**(You MUST use `createRoot` error options (`onCaughtError`, `onUncaughtError`, `onRecoverableError`) for centralized error logging in React 19+)**

</critical_requirements>

---

**Auto-detection:** error boundary, ErrorBoundary, getDerivedStateFromError, componentDidCatch, fallback UI, react-error-boundary, useErrorBoundary, error recovery, error fallback, onCaughtError, onUncaughtError, onRecoverableError, captureOwnerStack

**When to use:**

- Catching and displaying fallback UI for render errors
- Implementing retry/reset functionality after errors
- Preventing entire app crashes from component failures
- Creating isolated failure domains for different features

**Key patterns covered:**

- Class-based error boundary implementation
- `react-error-boundary` library patterns
- `useErrorBoundary` hook for async error handling
- Fallback UI with reset functionality
- Strategic boundary placement (granular vs coarse)
- TypeScript error boundary patterns
- **React 19+**: `createRoot` error options (`onCaughtError`, `onUncaughtError`, `onRecoverableError`)
- **React 19+**: `captureOwnerStack()` for enhanced debugging

**When NOT to use:**

- Event handler errors (use try/catch)
- Async code errors outside components (use try/catch)
- Server-side rendering errors (handle at framework level)
- API request errors (handle in data fetching layer)

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For React 19 error hooks, see [examples/react-19-hooks.md](examples/react-19-hooks.md)
- For testing patterns, see [examples/testing.md](examples/testing.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Error boundaries provide **graceful degradation** - when one component fails, the rest of the application continues working. The key principle is **isolation**: wrap distinct features in separate boundaries so failures are contained. Error boundaries are the ONLY way to catch errors during React rendering; they don't replace try/catch for imperative code but complement it for declarative UI.

**Core principles:**

1. **Isolation over global handling** - Multiple granular boundaries beat one root boundary
2. **Recovery over failure** - Provide reset/retry when possible
3. **User feedback over silent failure** - Show meaningful fallback UI
4. **Logging integration** - Pass errors to monitoring via `onError` callback
5. **Centralized observability (React 19+)** - Use `createRoot` error options for unified error tracking across all boundaries

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Class-Based Error Boundary (Native React)

Error boundaries MUST be class components because `getDerivedStateFromError` and `componentDidCatch` have no hook equivalents.

#### Two Lifecycle Methods

| Method                     | Phase  | Purpose                       | Side Effects |
| -------------------------- | ------ | ----------------------------- | ------------ |
| `getDerivedStateFromError` | Render | Update state to show fallback | NOT allowed  |
| `componentDidCatch`        | Commit | Log errors, call callbacks    | Allowed      |

#### Implementation

```typescript
// ✅ Good Example - Complete error boundary with reset
import { Component } from "react";
import type { ErrorInfo, ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
  onReset?: () => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    // Update state so next render shows fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Side effects allowed here - call logging callback
    this.props.onError?.(error, errorInfo);
  }

  handleReset = (): void => {
    this.props.onReset?.();
    this.setState({ hasError: false, error: null });
  };

  render(): ReactNode {
    const { hasError, error } = this.state;
    const { children, fallback } = this.props;

    if (hasError && error) {
      // Support both static and function fallback
      if (typeof fallback === "function") {
        return fallback(error, this.handleReset);
      }
      if (fallback) {
        return fallback;
      }
      // Default fallback
      return (
        <div role="alert">
          <h2>Something went wrong</h2>
          <button onClick={this.handleReset}>Try again</button>
        </div>
      );
    }

    return children;
  }
}
```

**Why good:** Separates render-phase logic (getDerivedStateFromError) from commit-phase side effects (componentDidCatch), provides reset capability for recovery, flexible fallback API supports both static and function patterns, onError callback enables logging integration without coupling to specific tools

---

### Pattern 2: react-error-boundary Library

The `react-error-boundary` library provides a production-ready error boundary with hooks support and additional features.

#### Installation

```bash
npm install react-error-boundary
```

#### ErrorBoundary Component Props

| Prop                | Type                    | Purpose                         |
| ------------------- | ----------------------- | ------------------------------- |
| `fallback`          | `ReactNode`             | Static fallback UI              |
| `FallbackComponent` | `ComponentType`         | Component that renders fallback |
| `fallbackRender`    | `(props) => ReactNode`  | Render prop for fallback        |
| `onError`           | `(error, info) => void` | Error logging callback          |
| `onReset`           | `(details) => void`     | Called when boundary resets     |
| `resetKeys`         | `unknown[]`             | Dependencies that trigger reset |

#### Basic Usage

```typescript
// ✅ Good Example - react-error-boundary with FallbackComponent
import { ErrorBoundary } from "react-error-boundary";
import type { FallbackProps } from "react-error-boundary";

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onError={(error, info) => {
        // Send to your error tracking service
        console.error("Boundary caught:", error, info);
      }}
      onReset={() => {
        // Reset app state if needed
      }}
    >
      <Dashboard />
    </ErrorBoundary>
  );
}
```

**Why good:** FallbackComponent pattern enables reusable fallback UI, onError callback decouples error handling from logging implementation, onReset allows cleaning up state before retry

---

### Pattern 3: useErrorBoundary Hook (Async Errors)

Error boundaries don't catch async errors by default. Use `useErrorBoundary` hook to manually trigger the nearest error boundary.

#### The Problem

```typescript
// ❌ This error is NOT caught by error boundary
async function handleClick() {
  const response = await fetch("/api/data");
  if (!response.ok) {
    throw new Error("API failed"); // Lost - boundary doesn't see it
  }
}
```

#### The Solution

```typescript
// ✅ Good Example - useErrorBoundary for async errors
import { useState } from "react";
import { useErrorBoundary } from "react-error-boundary";

function DataLoader() {
  const { showBoundary } = useErrorBoundary();
  const [data, setData] = useState<unknown>(null);

  const handleLoadData = async () => {
    try {
      const response = await fetch("/api/data");
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (error) {
      // Manually trigger nearest error boundary
      showBoundary(error);
    }
  };

  return (
    <div>
      <button onClick={handleLoadData}>Load Data</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}

// Wrap with ErrorBoundary
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <DataLoader />
</ErrorBoundary>
```

**Why good:** showBoundary manually propagates async errors to the nearest boundary, maintains consistent error handling UX across sync and async failures, keeps error handling logic in the error boundary system

#### When to Use showBoundary

- Async operations that should show fallback UI on failure
- Event handlers where errors should propagate to boundary
- Effects that should trigger error UI on failure

#### When NOT to Use showBoundary

- Errors that should be handled locally with inline UI
- Recoverable errors that don't need full fallback UI
- Validation errors that need field-level feedback

---

### Pattern 4: resetKeys for Automatic Reset

Use `resetKeys` to automatically reset the error boundary when certain values change.

```typescript
// ✅ Good Example - Reset boundary when route changes
import { ErrorBoundary } from "react-error-boundary";
import { useLocation } from "react-router-dom";

function AppWithRouteReset() {
  const location = useLocation();

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      resetKeys={[location.pathname]}
      onResetKeysChange={() => {
        // Optionally track resets
      }}
    >
      <Routes />
    </ErrorBoundary>
  );
}
```

**Why good:** Automatic reset when navigation occurs prevents stale error states, users don't need to manually retry after navigating away and back

#### Common resetKeys Patterns

| Pattern        | Use Case                          |
| -------------- | --------------------------------- |
| `[pathname]`   | Reset on route change             |
| `[selectedId]` | Reset when viewing different item |
| `[retryCount]` | Reset after programmatic retry    |
| `[queryKey]`   | Reset when data source changes    |

---

### Pattern 5: Granular Boundary Placement

Place error boundaries strategically to isolate failures.

#### Placement Strategy

```
App
├─ ErrorBoundary (root - catches unhandled errors)
│   ├─ Header
│   ├─ ErrorBoundary (sidebar - isolated)
│   │   └─ Sidebar
│   ├─ ErrorBoundary (main content - isolated)
│   │   └─ MainContent
│   │       ├─ ErrorBoundary (widget A)
│   │       │   └─ ChartWidget
│   │       └─ ErrorBoundary (widget B)
│   │           └─ TableWidget
│   └─ Footer
```

```typescript
// ✅ Good Example - Granular boundaries around features
function Dashboard() {
  return (
    <div>
      <ErrorBoundary
        fallback={<div>Chart unavailable</div>}
        onError={logError}
      >
        <ChartWidget />
      </ErrorBoundary>

      <ErrorBoundary
        fallback={<div>Table unavailable</div>}
        onError={logError}
      >
        <DataTable />
      </ErrorBoundary>

      <ErrorBoundary
        fallback={<div>Stats unavailable</div>}
        onError={logError}
      >
        <StatsPanel />
      </ErrorBoundary>
    </div>
  );
}
```

**Why good:** One widget failing doesn't crash the entire dashboard, each feature has contextual fallback UI, errors are isolated to their domain

```typescript
// ❌ Bad Example - Single boundary for everything
function Dashboard() {
  return (
    <ErrorBoundary fallback={<div>Dashboard error</div>}>
      <ChartWidget />
      <DataTable />
      <StatsPanel />
    </ErrorBoundary>
  );
}
```

**Why bad:** One failing widget crashes the entire dashboard, users lose access to working features, poor user experience

---

### Pattern 6: Fallback UI Patterns

Design fallback UI that provides context and recovery options.

#### Minimal Fallback

```typescript
// ✅ Good Example - Minimal fallback with retry
function MinimalFallback({ resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert">
      <p>Failed to load</p>
      <button onClick={resetErrorBoundary}>Retry</button>
    </div>
  );
}
```

#### Detailed Fallback

```typescript
// ✅ Good Example - Detailed fallback with error info
function DetailedFallback({ error, resetErrorBoundary }: FallbackProps) {
  const isDev = process.env.NODE_ENV === "development";

  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <p>We're working on fixing this issue.</p>

      {isDev && (
        <details>
          <summary>Error details</summary>
          <pre>{error.message}</pre>
          <pre>{error.stack}</pre>
        </details>
      )}

      <div>
        <button onClick={resetErrorBoundary}>Try again</button>
        <button onClick={() => window.location.reload()}>
          Refresh page
        </button>
      </div>
    </div>
  );
}
```

**Why good:** role="alert" announces error to screen readers, error details in development aid debugging, production users see friendly message without technical details, multiple recovery options

#### Feature-Specific Fallback

```typescript
// ✅ Good Example - Contextual fallback
function ChartFallback({ resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="chart-fallback">
      <span aria-hidden="true">📊</span>
      <p>Chart could not be displayed</p>
      <button onClick={resetErrorBoundary}>Reload chart</button>
    </div>
  );
}

// Usage
<ErrorBoundary FallbackComponent={ChartFallback}>
  <RevenueChart />
</ErrorBoundary>
```

**Why good:** Fallback UI matches the context of the failed component, users understand what feature is unavailable

---

### Pattern 7: React 19+ Error Hooks (createRoot Options)

React 19 introduces three new root-level error handlers that complement error boundaries. These run at the `createRoot` level and provide centralized error logging.

#### Three Error Handlers

| Handler              | When Called                       | Use Case                                  |
| -------------------- | --------------------------------- | ----------------------------------------- |
| `onCaughtError`      | Error caught by an Error Boundary | Log errors that are handled by boundaries |
| `onUncaughtError`    | Error NOT caught by any boundary  | Log/report fatal errors                   |
| `onRecoverableError` | React auto-recovers from error    | Log hydration mismatches, suspense errors |

#### Basic Setup

```typescript
// ✅ Good Example - React 19 createRoot with error handlers
import { createRoot } from "react-dom/client";

const ROOT_ELEMENT_ID = "root";

function logError(
  error: Error,
  errorInfo: { componentStack?: string | null }
) {
  // Send to your error tracking service
  console.error("React error:", error);
  console.error("Component stack:", errorInfo.componentStack);
}

const container = document.getElementById(ROOT_ELEMENT_ID);
if (!container) throw new Error("Root element not found");

const root = createRoot(container, {
  onCaughtError: (error, errorInfo) => {
    // Error caught by an Error Boundary
    logError(error, errorInfo);
  },
  onUncaughtError: (error, errorInfo) => {
    // Error NOT caught - fatal
    logError(error, errorInfo);
  },
  onRecoverableError: (error, errorInfo) => {
    // React auto-recovered (e.g., hydration mismatch)
    logError(error, errorInfo);
  },
});

root.render(<App />);
```

**Why good:** Centralized error logging for ALL React errors, captures errors even when no boundary catches them, provides component stack for debugging

#### With Error Monitoring Service

```typescript
// ✅ Good Example - Integration with error monitoring
import { createRoot } from "react-dom/client";
import * as Sentry from "@sentry/react";

const ROOT_ELEMENT_ID = "root";

const container = document.getElementById(ROOT_ELEMENT_ID);
if (!container) throw new Error("Root element not found");

const root = createRoot(container, {
  onCaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
    // Custom handling for caught errors (optional)
    console.warn("Caught error:", error.message);
  }),
  onUncaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
    // Custom handling for uncaught errors (optional)
    console.error("Uncaught error:", error.message);
  }),
  onRecoverableError: Sentry.reactErrorHandler(),
});

root.render(<App />);
```

**Why good:** Error monitoring integration at root level, single point of configuration, `Sentry.reactErrorHandler()` adds proper React context to reports

> **See [examples/react-19-hooks.md](examples/react-19-hooks.md) for complete examples including `captureOwnerStack()` and advanced patterns.**

</patterns>

---

<integration>

## Integration Points

**Error boundaries integrate with your application through callbacks:**

- **`onError`**: Pass errors to your logging/monitoring system
- **`onReset`**: Clean up application state before retry
- **`resetKeys`**: Sync boundary state with application state (routes, selections)

**Error boundaries work alongside:**

- **Try/catch**: For event handlers, async code, imperative operations
- **Data fetching error states**: For API-level errors with retry logic
- **Form validation**: For field-level error display

**Boundaries do NOT replace these patterns - they complement them for rendering errors.**

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `getDerivedStateFromError` for rendering fallback UI - it runs during render phase)**

**(You MUST use `componentDidCatch` for side effects like logging - it runs during commit phase)**

**(You MUST wrap error boundaries around feature sections, not just the app root)**

**(You MUST provide reset/retry functionality for recoverable errors)**

**(You MUST use `role="alert"` on fallback UI for accessibility)**

**(You MUST use `createRoot` error options (`onCaughtError`, `onUncaughtError`, `onRecoverableError`) for centralized error logging in React 19+)**

**Failure to follow these rules will result in poor error handling, inaccessible UIs, or unrecoverable error states.**

</critical_reminders>
