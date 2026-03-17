---
name: using-sentry
description: Capture exceptions, add context, create performance spans, and use structured logging with Sentry.
---

# Working with Sentry

Capture exceptions, add context, create performance spans, and use structured logging with Sentry.

## Implement Working with Sentry

Capture exceptions, add context, create performance spans, and use structured logging with Sentry.

**See:**

- Resource: `using-sentry` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-sentry

---

### Capturing Exceptions

Manually capture errors that are handled but should be tracked:

```typescript
import * as Sentry from "@sentry/nextjs";

try {
  await riskyOperation();
} catch (err) {
  Sentry.captureException(err);
  // Handle the error gracefully...
}
```

### Adding Context

Attach user and custom context to errors:

```typescript
import * as Sentry from "@sentry/nextjs";

// Set user context (persists for session)
Sentry.setUser({
  id: session.user.id,
  email: session.user.email,
});

// Add custom context to exceptions
Sentry.captureException(err, {
  tags: {
    feature: "checkout",
    plan: "pro",
  },
  extra: {
    orderId: "order_123",
    items: cart.items,
  },
});
```

### Performance Tracing

Create spans for meaningful operations:

```typescript
import * as Sentry from "@sentry/nextjs";

// Wrap async operations
const result = await Sentry.startSpan(
  {
    op: "http.client",
    name: "GET /api/users",
  },
  async () => {
    const response = await fetch("/api/users");
    return response.json();
  },
);

// Wrap sync operations
Sentry.startSpan(
  {
    op: "ui.click",
    name: "Submit Button Click",
  },
  (span) => {
    span.setAttribute("form", "checkout");
    processSubmit();
  },
);
```

### Using the Sentry Logger

Sentry provides structured logging that appears in the Logs tab:

```typescript
import * as Sentry from "@sentry/nextjs";

const { logger } = Sentry;

logger.info("Payment processed", { orderId: "123", amount: 99.99 });
logger.warn("Rate limit approaching", { current: 90, max: 100 });
logger.error("Payment failed", { orderId: "123", reason: "declined" });
```

### Breadcrumbs

Add breadcrumbs to provide context for errors:

```typescript
import * as Sentry from "@sentry/nextjs";

// Automatically captured: console logs, fetch requests, UI clicks
// Manual breadcrumbs for custom events:
Sentry.addBreadcrumb({
  category: "auth",
  message: "User signed in",
  level: "info",
});
```

### Clearing User Context

Clear user data on sign out:

```typescript
import * as Sentry from "@sentry/nextjs";

async function signOut() {
  Sentry.setUser(null);
  await authClient.signOut();
}
```

---

## References

- [Sentry Next.js SDK](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [Custom Instrumentation](https://docs.sentry.io/platforms/javascript/guides/nextjs/tracing/instrumentation/custom-instrumentation/)
