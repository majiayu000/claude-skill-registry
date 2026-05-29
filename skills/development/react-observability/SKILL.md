---
name: react-observability
description: Logging, error messages, and debugging patterns for React. Use when adding logging, designing error messages, debugging production issues, or improving code observability. Works for both React web and React Native.
---

# React Observability

## Problem Statement

Silent failures are debugging nightmares. Code that returns early without logging, error messages that lack context, and missing observability make production issues impossible to diagnose. Write code as if you'll debug it at 3am with only logs.

---

## Pattern: No Silent Early Returns

**Problem:** Early returns without logging create invisible failure paths.

```typescript
// WRONG - silent death
const saveData = (id: string, value: number) => {
  if (!validIds.has(id)) {
    return;  // ❌ Why did we return? No one knows.
  }
  // ... save logic
};

// CORRECT - observable
const saveData = (id: string, value: number) => {
  if (!validIds.has(id)) {
    logger.warn('[saveData] Dropping save - invalid ID', {
      id,
      value,
      validIds: Array.from(validIds),
    });
    return;
  }
  // ... save logic
};
```

**Rule:** Every early return should log why it's returning, with enough context to diagnose.

---

## Pattern: Error Message Design

**Problem:** Error messages that don't help diagnose the issue.

```typescript
// BAD - no context
throw new Error('Data not found');

// BAD - slightly better but still useless at 3am
throw new Error('Data not found. Please try again.');

// GOOD - diagnostic context included
throw new Error(
  `Data not found. ID: ${id}, ` +
  `Available: ${Object.keys(data).length} items, ` +
  `Last fetch: ${lastFetchTime}. This may indicate a caching issue.`
);
```

**Error message template:**

```typescript
throw new Error(
  `[${functionName}] ${whatFailed}. ` +
  `Context: ${relevantState}. ` +
  `Possible cause: ${hypothesis}.`
);
```

**What to include:**

| Element | Why |
|---------|-----|
| Function/location | Where the error occurred |
| What failed | The specific condition that wasn't met |
| Relevant state | Values that help diagnose |
| Possible cause | Your best guess for the fix |

---

## Pattern: Structured Logging

**Problem:** Console.log statements that are hard to parse and search.

```typescript
// BAD - unstructured
console.log('saving data', id, value);
console.log('current state', data);

// GOOD - structured with context object
logger.info('[saveData] Saving data', {
  id,
  value,
  existingCount: Object.keys(data).length,
});
```

**Logging levels:**

| Level | Use for |
|-------|---------|
| `error` | Exceptions, failures that need immediate attention |
| `warn` | Unexpected conditions that didn't fail but might indicate problems |
| `info` | Important business events (user actions, flow milestones) |
| `debug` | Detailed diagnostic info (state dumps, timing) |

**Wrapper for consistent logging:**

```typescript
// utils/logger.ts
const LOG_LEVELS = ['debug', 'info', 'warn', 'error'] as const;
type LogLevel = typeof LOG_LEVELS[number];

const currentLevel: LogLevel = process.env.NODE_ENV === 'development' ? 'debug' : 'warn';

function shouldLog(level: LogLevel): boolean {
  return LOG_LEVELS.indexOf(level) >= LOG_LEVELS.indexOf(currentLevel);
}

export const logger = {
  debug: (message: string, context?: object) => {
    if (shouldLog('debug')) {
      console.log(`[DEBUG] ${message}`, context ?? '');
    }
  },
  info: (message: string, context?: object) => {
    if (shouldLog('info')) {
      console.log(`[INFO] ${message}`, context ?? '');
    }
  },
  warn: (message: string, context?: object) => {
    if (shouldLog('warn')) {
      console.warn(`[WARN] ${message}`, context ?? '');
    }
  },
  error: (message: string, context?: object) => {
    if (shouldLog('error')) {
      console.error(`[ERROR] ${message}`, context ?? '');
    }
  },
};
```

---

## Pattern: Sensitive Data Handling

**Problem:** Logging sensitive data to console or error reporting.

```typescript
// utils/secureLogger.ts
const SENSITIVE_KEYS = ['password', 'token', 'ssn', 'creditCard', 'apiKey', 'secret'];

function redactSensitive(obj: object): object {
  const redacted = { ...obj };
  for (const key of Object.keys(redacted)) {
    if (SENSITIVE_KEYS.some(s => key.toLowerCase().includes(s))) {
      redacted[key] = '[REDACTED]';
    } else if (typeof redacted[key] === 'object' && redacted[key] !== null) {
      redacted[key] = redactSensitive(redacted[key]);
    }
  }
  return redacted;
}

export const secureLogger = {
  info: (message: string, context?: object) => {
    const safeContext = context ? redactSensitive(context) : undefined;
    logger.info(message, safeContext);
  },
  // ... other levels
};
```

---

## Pattern: Flow Tracing

**Problem:** Multi-step operations where it's unclear how far execution got.

```typescript
async function checkoutFlow(cartId: string) {
  const flowId = `checkout-${Date.now()}`;

  logger.info(`[checkoutFlow:${flowId}] Starting`, { cartId });

  try {
    logger.debug(`[checkoutFlow:${flowId}] Step 1: Validating cart`);
    await validateCart(cartId);

    logger.debug(`[checkoutFlow:${flowId}] Step 2: Processing payment`);
    await processPayment(cartId);

    logger.debug(`[checkoutFlow:${flowId}] Step 3: Confirming order`);
    await confirmOrder(cartId);

    logger.info(`[checkoutFlow:${flowId}] Completed successfully`);
  } catch (error) {
    logger.error(`[checkoutFlow:${flowId}] Failed`, {
      error: error.message,
      stack: error.stack,
      cartId,
    });
    throw error;
  }
}
```

**Benefits:**
- Can search logs by flowId to see entire flow
- Know exactly which step failed
- Timing visible via timestamps

---

## Pattern: State Snapshots for Debugging

**Problem:** Need to understand state at specific points in complex flows.

```typescript
function snapshotState(label: string) {
  const state = useStore.getState();
  logger.debug(`[StateSnapshot] ${label}`, {
    itemCount: Object.keys(state.items).length,
    activeFeatures: Array.from(state.features),
    loading: state.loading,
  });
}

// Usage in flow
async function complexFlow() {
  snapshotState('Before load');
  await loadData(id);
  snapshotState('After load');
  await processData();
  snapshotState('After process');
}
```

---

## Pattern: Assertion Helpers

**Problem:** Conditions that "should never happen" but need visibility when they do.

```typescript
// utils/assertions.ts
export function assertDefined<T>(
  value: T | null | undefined,
  context: string
): asserts value is T {
  if (value === null || value === undefined) {
    const message = `[Assertion Failed] Expected defined value: ${context}`;
    logger.error(message, { value });
    throw new Error(message);
  }
}

export function assertCondition(
  condition: boolean,
  context: string,
  debugInfo?: object
): asserts condition {
  if (!condition) {
    const message = `[Assertion Failed] ${context}`;
    logger.error(message, debugInfo);
    throw new Error(message);
  }
}

// Usage
assertDefined(user, `User not found: ${userId}`);
assertCondition(
  items.length > 0,
  `No items found`,
  { searchQuery, filters }
);
```

---

## Pattern: Production Error Reporting

**Problem:** Errors in production with no visibility.

```typescript
// Integration with error reporting service (Sentry example)
import * as Sentry from '@sentry/react';

export function captureError(
  error: Error,
  context?: Record<string, unknown>
) {
  logger.error(error.message, { ...context, stack: error.stack });

  if (process.env.NODE_ENV === 'production') {
    Sentry.captureException(error, {
      extra: context,
    });
  }
}

// Usage
try {
  await riskyOperation();
} catch (error) {
  captureError(error, {
    userId,
    action: 'checkout',
    cartItems: cart.items.length,
  });
  throw error;
}
```

---

## Pattern: React Error Boundaries

**Problem:** Unhandled errors crash the entire app.

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logger.error('[ErrorBoundary] Caught error', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });

    captureError(error, { componentStack: errorInfo.componentStack });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <DefaultErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

---

## Checklist: Adding Observability

When writing new code:

- [ ] All early returns have logging with context
- [ ] Error messages include diagnostic information
- [ ] Multi-step operations have flow tracing
- [ ] Sensitive data is redacted before logging
- [ ] State snapshots available for debugging complex flows
- [ ] Production errors are captured with context

When debugging existing code:

- [ ] Add logging to suspect early returns
- [ ] Add state snapshots before and after async operations
- [ ] Check for silent catches that swallow errors
- [ ] Verify error messages have enough context

---

## Quick Debugging Template

Add this temporarily when debugging async/state issues:

```typescript
const DEBUG = true;

function debugLog(label: string, data?: object) {
  if (DEBUG) {
    console.log(`[DEBUG ${Date.now()}] ${label}`, data ?? '');
  }
}

// In your flow
debugLog('Flow start', { inputs });
debugLog('After step 1', { state: getState() });
debugLog('After step 2', { state: getState() });
debugLog('Flow end', { result });
```

Remove before committing, or gate behind a flag.
