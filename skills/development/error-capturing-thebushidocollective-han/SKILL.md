---
name: sentry-error-capturing
description: Use when capturing and reporting errors to Sentry, adding context, or handling exceptions. Covers error boundaries, context enrichment, and fingerprinting.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Sentry - Error Capturing & Context

Capture errors and enrich them with context for better debugging.

## Capturing Errors

### Manual Error Capture

```typescript
import * as Sentry from "@sentry/browser";

try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error);
}
```

### Capture with Extra Context

```typescript
Sentry.captureException(error, {
  tags: {
    section: "checkout",
    feature: "payment",
  },
  extra: {
    orderId: order.id,
    cartItems: cart.items.length,
  },
  level: "error",
});
```

### Capture Messages

```typescript
Sentry.captureMessage("User exceeded rate limit", {
  level: "warning",
  tags: { userId: user.id },
});
```

## Adding Context

### User Context

```typescript
Sentry.setUser({
  id: user.id,
  email: user.email,
  username: user.username,
  ip_address: "{{auto}}",
});

// Clear on logout
Sentry.setUser(null);
```

### Tags

```typescript
// Global tags
Sentry.setTag("app.version", "1.2.3");
Sentry.setTag("tenant", customer.tenantId);

// Per-event tags
Sentry.captureException(error, {
  tags: { operation: "database_query" },
});
```

### Extra Data

```typescript
Sentry.setExtra("orderDetails", {
  items: order.items,
  total: order.total,
});
```

### Context Objects

```typescript
Sentry.setContext("order", {
  id: order.id,
  status: order.status,
  items: order.items.length,
});

Sentry.setContext("customer", {
  plan: customer.plan,
  region: customer.region,
});
```

## Breadcrumbs

### Automatic Breadcrumbs

```typescript
// Most integrations add breadcrumbs automatically
// Console, fetch, XHR, DOM events, navigation
```

### Manual Breadcrumbs

```typescript
Sentry.addBreadcrumb({
  category: "auth",
  message: "User logged in",
  level: "info",
  data: {
    userId: user.id,
    method: "oauth",
  },
});
```

### Configure Breadcrumbs

```typescript
Sentry.init({
  beforeBreadcrumb(breadcrumb, hint) {
    // Filter or modify breadcrumbs
    if (breadcrumb.category === "console") {
      return null; // Don't capture console logs
    }
    return breadcrumb;
  },
  maxBreadcrumbs: 50,
});
```

## Error Boundaries (React)

```tsx
import * as Sentry from "@sentry/react";

// Basic error boundary
const App = () => (
  <Sentry.ErrorBoundary fallback={<ErrorPage />}>
    <YourApp />
  </Sentry.ErrorBoundary>
);

// With custom fallback and onError
<Sentry.ErrorBoundary
  fallback={({ error, resetError }) => (
    <div>
      <p>Something went wrong: {error.message}</p>
      <button onClick={resetError}>Try again</button>
    </div>
  )}
  onError={(error, componentStack) => {
    console.error("Caught by Sentry boundary:", error);
  }}
  beforeCapture={(scope) => {
    scope.setTag("location", "checkout");
  }}
>
  <CheckoutFlow />
</Sentry.ErrorBoundary>
```

## Fingerprinting

### Custom Grouping

```typescript
Sentry.captureException(error, {
  fingerprint: ["{{ default }}", user.id],
});
```

### Override Default Grouping

```typescript
Sentry.init({
  beforeSend(event) {
    if (event.exception?.values?.[0]?.type === "ChunkLoadError") {
      event.fingerprint = ["chunk-load-error"];
    }
    return event;
  },
});
```

## Scopes

### Configure Scope

```typescript
Sentry.configureScope((scope) => {
  scope.setUser({ id: user.id });
  scope.setTag("theme", "dark");
  scope.setLevel("warning");
});
```

### With Scope (Isolated)

```typescript
Sentry.withScope((scope) => {
  scope.setTag("operation", "batch_import");
  scope.setExtra("batchSize", items.length);
  Sentry.captureException(error);
});
// Tags/extra only apply within this scope
```

## Best Practices

1. Set user context on login, clear on logout
2. Add relevant business context (order ID, tenant, etc.)
3. Use tags for filterable, indexable data
4. Use extra for detailed debugging data
5. Implement error boundaries at feature boundaries
6. Use fingerprinting to group related errors
7. Add breadcrumbs for critical user actions
