---
name: error-tracing
description: >
  Read stack traces, follow error chains, and trace errors to their root cause.
  Use when the user encounters an error message, stack trace, exception, or crash.
  Apply when debugging async errors, React error boundaries, source map issues,
  or when an error message is unclear.
---

# Error Tracing

Read stack traces and error chains to trace errors back to their root cause across synchronous, asynchronous, and distributed code paths.

## When to Use

- An error or stack trace appears in console, logs, or test output
- The user shares an exception and needs help understanding it
- Debugging async errors with incomplete stack traces
- Setting up error boundaries in React or similar frameworks
- Mapping minified production errors back to source code

## Core Patterns

### Reading Stack Traces

Stack traces read from top to bottom. The top frame is where the error was thrown; the bottom frame is the entry point:

```
Error: Cannot read properties of undefined (reading 'email')
    at formatUser (src/utils/format.ts:42:18)        <-- ERROR THROWN HERE
    at processUsers (src/services/user.ts:87:12)      <-- Called formatUser
    at handler (src/routes/users.ts:23:5)             <-- Called processUsers
    at Layer.handle (node_modules/express/lib/router/layer.js:95:5)
```

Reading strategy:
1. Read the error message first — it often tells you exactly what is wrong
2. Find the first frame in YOUR code (skip `node_modules`)
3. Go to that file and line — `src/utils/format.ts:42`
4. Understand what variable is `undefined` and trace where it came from
5. Walk up the stack to find where the bad data originated

```typescript
// The error says: Cannot read 'email' of undefined
// At format.ts:42: user.email  — so `user` is undefined
// At user.ts:87: formatUser(users[i])  — so users[i] is undefined
// Root cause: array has gaps or index is out of bounds
```

### Error Chains (Cause Property)

Wrap errors to add context while preserving the original cause:

```typescript
// Build error chains with the cause option (ES2022)
async function createOrder(data: OrderInput): Promise<Order> {
  let user: User;
  try {
    user = await fetchUser(data.userId);
  } catch (error) {
    throw new Error(`Failed to create order: user lookup failed`, {
      cause: error,
    });
  }

  try {
    return await insertOrder(user, data);
  } catch (error) {
    throw new Error(`Failed to create order: database insert failed`, {
      cause: error,
    });
  }
}

// Reading the error chain
function logErrorChain(error: Error): void {
  let current: Error | undefined = error;
  let depth = 0;
  while (current) {
    const indent = "  ".repeat(depth);
    console.error(`${indent}${current.message}`);
    if (current.stack) {
      console.error(`${indent}${current.stack.split("\n")[1]?.trim()}`);
    }
    current = current.cause instanceof Error ? current.cause : undefined;
    depth++;
  }
}

// Output:
// Failed to create order: database insert failed
//   at createOrder (src/services/order.ts:18:11)
//   ECONNREFUSED 127.0.0.1:5432
//     at Connection.connect (node_modules/pg/lib/connection.js:45:9)
```

```python
# Python: Exception chaining with raise ... from
def create_order(data: dict) -> Order:
    try:
        user = fetch_user(data["user_id"])
    except DatabaseError as e:
        raise OrderError(f"Failed to create order for user {data['user_id']}") from e
    # The __cause__ attribute preserves the original exception
```

### Async Stack Traces

Async operations can lose stack context. Use these techniques to preserve traceability:

```typescript
// Node.js: Enable async stack traces
// Run with: node --async-stack-traces app.js
// Or set in code:
Error.stackTraceLimit = 50; // Increase from default 10

// PROBLEM: Lost context in async callbacks
setTimeout(() => {
  throw new Error("What called setTimeout?");
  // Stack trace only shows the timer callback, not the caller
}, 1000);

// SOLUTION: Capture context before the async boundary
async function processWithContext(items: Item[]): Promise<void> {
  const callerStack = new Error("context").stack; // Capture before async

  await Promise.all(
    items.map(async (item) => {
      try {
        await processItem(item);
      } catch (error) {
        throw new Error(
          `Failed processing item ${item.id}. Caller: ${callerStack}`,
          { cause: error }
        );
      }
    })
  );
}

// SOLUTION: Named functions instead of anonymous callbacks
// BAD: Anonymous — shows as "<anonymous>" in stack
items.map(async (item) => { /* ... */ });

// GOOD: Named — shows as "processItem" in stack
items.map(async function processItem(item) { /* ... */ });
```

### React Error Boundaries

Catch rendering errors and prevent full-app crashes:

```tsx
import { Component, ErrorInfo, ReactNode } from "react";

interface ErrorBoundaryProps {
  fallback: ReactNode;
  children: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log the error with component stack
    console.error("Component error:", {
      message: error.message,
      componentStack: errorInfo.componentStack,
      stack: error.stack,
    });
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage: Wrap sections of the UI independently
function App() {
  return (
    <div>
      <ErrorBoundary fallback={<p>Navigation error</p>}>
        <Navigation />
      </ErrorBoundary>
      <ErrorBoundary fallback={<p>Content failed to load</p>}>
        <MainContent />
      </ErrorBoundary>
    </div>
  );
}
```

### Source Maps for Production Errors

Map minified stack traces back to original source:

```bash
# Generate source maps during build
# webpack: devtool: "source-map"
# vite: build.sourcemap: true
# tsc: "sourceMap": true in tsconfig.json

# Decode a minified stack trace
npx source-map-cli resolve bundle.js.map 1 2345
# Output: src/services/order.ts:42:18

# Upload source maps to error tracking service
npx sentry-cli releases files v1.0.0 upload-sourcemaps ./dist
```

```typescript
// In error tracking setup (Sentry example)
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  release: process.env.APP_VERSION,
  environment: process.env.NODE_ENV,
});

// Errors automatically include deminified stack traces
```

## Anti-Patterns

### What NOT to Do

- **Swallowing errors**: `catch (e) {}` — silent failures hide bugs. Always log or re-throw.
- **Losing the original error**: `throw new Error("failed")` without `{ cause: originalError }` — the root cause is lost.
- **Catching too broadly**: A single try/catch around 200 lines of code. Wrap specific operations individually.
- **Ignoring stack trace frames**: Jumping to conclusions without reading where the error actually occurred.
- **String errors**: `throw "something failed"` — always throw Error objects for stack traces.

```typescript
// BAD: Swallowed error
try {
  await saveOrder(order);
} catch (e) {
  // Silently fails — order is lost, user thinks it succeeded
}

// BAD: Original cause lost
try {
  await saveOrder(order);
} catch (e) {
  throw new Error("Order save failed");  // What was the actual error?
}

// GOOD: Error chained with context
try {
  await saveOrder(order);
} catch (error) {
  throw new Error(`Order ${order.id} save failed`, { cause: error });
}
```

## Quick Reference

```
Reading Stack Traces:
  1. Read the error message first
  2. Find the first frame in YOUR code (skip node_modules)
  3. Go to that file:line
  4. Trace the undefined/null value up the call stack

Error Chaining:
  throw new Error("context message", { cause: originalError })
  Python: raise NewError("message") from original_error

Async Debugging:
  - node --async-stack-traces
  - Error.stackTraceLimit = 50
  - Capture caller stack before async boundaries
  - Use named functions, not anonymous callbacks

React Error Boundaries:
  - Catch rendering errors per UI section
  - Log componentStack from ErrorInfo
  - Show fallback UI, not a white screen

Production Errors:
  - Generate source maps at build time
  - Upload to error tracking (Sentry, Datadog)
  - Never expose source maps publicly
  - Include release version in error reports

Rules:
  - Never swallow errors silently
  - Always chain errors with cause
  - Always throw Error objects, not strings
  - Wrap specific operations, not entire functions
```
