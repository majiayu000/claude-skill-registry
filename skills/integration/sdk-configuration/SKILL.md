---
name: sentry-sdk-configuration
description: Use when initializing Sentry in applications, configuring SDK options, or setting up integrations across different frameworks and platforms.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Sentry - SDK Configuration

Initialize and configure Sentry SDKs across different platforms and frameworks.

## JavaScript/TypeScript

### Browser SDK

```typescript
import * as Sentry from "@sentry/browser";

Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
  environment: process.env.NODE_ENV,
  release: process.env.RELEASE_VERSION,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration(),
  ],
});
```

### Node.js SDK

```typescript
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
  environment: process.env.NODE_ENV,
  release: process.env.RELEASE_VERSION,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.httpIntegration(),
    Sentry.expressIntegration(),
  ],
});
```

### Next.js SDK

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
});
```

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

## React SDK

```tsx
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.reactRouterV6BrowserTracingIntegration({
      useEffect,
      useLocation,
      useNavigationType,
      createRoutesFromChildren,
      matchRoutes,
    }),
  ],
  tracesSampleRate: 1.0,
});

// Wrap your app
const App = () => (
  <Sentry.ErrorBoundary fallback={<ErrorFallback />}>
    <YourApp />
  </Sentry.ErrorBoundary>
);
```

## Python SDK

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    environment=os.getenv("ENVIRONMENT"),
    release=os.getenv("RELEASE_VERSION"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
```

### Django Integration

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    integrations=[
        sentry_sdk.integrations.django.DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
```

## Go SDK

```go
import "github.com/getsentry/sentry-go"

func main() {
    err := sentry.Init(sentry.ClientOptions{
        Dsn:              "https://examplePublicKey@o0.ingest.sentry.io/0",
        Environment:      os.Getenv("ENVIRONMENT"),
        Release:          os.Getenv("RELEASE_VERSION"),
        TracesSampleRate: 1.0,
    })
    if err != nil {
        log.Fatalf("sentry.Init: %s", err)
    }
    defer sentry.Flush(2 * time.Second)
}
```

## Configuration Options

### Sample Rates

```typescript
Sentry.init({
  // Error sampling (1.0 = 100%)
  sampleRate: 1.0,

  // Transaction/trace sampling
  tracesSampleRate: 0.2,

  // Or use a sampler function
  tracesSampler: (samplingContext) => {
    if (samplingContext.name.includes("/health")) {
      return 0; // Don't trace health checks
    }
    return 0.2;
  },
});
```

### Filtering Events

```typescript
Sentry.init({
  beforeSend(event, hint) {
    // Filter out specific errors
    if (event.exception?.values?.[0]?.type === "NetworkError") {
      return null;
    }
    return event;
  },
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    /^Script error\.?$/,
  ],
  denyUrls: [
    /extensions\//i,
    /^chrome:\/\//i,
  ],
});
```

## Best Practices

1. Always set `environment` and `release`
2. Use environment variables for DSN
3. Configure appropriate sample rates for production
4. Filter noisy or irrelevant errors
5. Use framework-specific integrations
6. Initialize Sentry as early as possible
