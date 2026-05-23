---
name: workleap-telemetry
description: |
  Guide for Workleap's telemetry solution (@workleap/telemetry) that unifies Honeycomb, LogRocket, and Mixpanel with consistent correlation IDs.

  Use this skill when:
  (1) Initializing wl-telemetry in a frontend application
  (2) Working with correlation values (Telemetry Id, Device Id) and their lifecycle
  (3) Using Honeycomb for distributed tracing and performance analysis
  (4) Creating and enriching Honeycomb traces/spans using OpenTelemetry
  (5) Using LogRocket for session replay and frontend debugging
  (6) Using Mixpanel for product analytics and event tracking
  (7) Understanding Honeycomb, LogRocket, and Mixpanel roles in wl-telemetry
  (8) Correlating data across Honeycomb, LogRocket, and Mixpanel
  (9) Configuring loggers for wl-telemetry diagnostics
  (10) Using Noop telemetry clients to disable/mock telemetry
  (11) Reviewing PRs that add or modify telemetry instrumentation
  (12) Troubleshooting missing or inconsistent telemetry across tools
---

# Workleap Telemetry (wl-telemetry)

`@workleap/telemetry` is an umbrella package that integrates Honeycomb, LogRocket, and Mixpanel with consistent correlation IDs for unified debugging and analysis.

## Core Concepts

### Correlation Values

Two automatic correlation IDs unify all telemetry platforms:

| ID | Purpose | Honeycomb | LogRocket/Mixpanel |
|---|---|---|---|
| **Telemetry Id** | Single app load | `app.telemetry_id` | `Telemetry Id` |
| **Device Id** | Device across sessions | `app.device_id` | `Device Id` |

If LogRocket is enabled, Honeycomb and Mixpanel automatically receive `app.logrocket_session_url` / `LogRocket Session URL`.

### Platform Roles

- **Honeycomb**: Distributed traces, performance monitoring, RUM metrics (LCP, CLS, INP)
- **LogRocket**: Session replay, frontend debugging, user experience investigation
- **Mixpanel**: Product analytics, event tracking, user behavior insights

## Quick Start

```typescript
import { initializeTelemetry, TelemetryProvider } from "@workleap/telemetry/react";

const telemetryClient = initializeTelemetry({
  logRocket: { appId: "your-app-id" },
  honeycomb: {
    namespace: "your-namespace",
    serviceName: "your-service",
    apiServiceUrls: [/.+/g],
    options: { proxy: "https://your-otel-proxy" }
  },
  mixpanel: {
    productId: "wlp",
    envOrTrackingApiBaseUrl: "production"
  }
});

// Wrap application
<TelemetryProvider client={telemetryClient}>
  <App />
</TelemetryProvider>
```

## Using Platform Clients

```typescript
// Access via hooks
const telemetryClient = useTelemetryClient();
const honeycombClient = useHoneycombInstrumentationClient();
const logRocketClient = useLogRocketInstrumentationClient();
const mixpanelClient = useMixpanelClient();
const track = useMixpanelTrackingFunction();
```

## Storybook/Testing (Noop Clients)

```typescript
import { NoopTelemetryClient, TelemetryProvider } from "@workleap/telemetry/react";

const telemetryClient = new NoopTelemetryClient();

<TelemetryProvider client={telemetryClient}>
  <Story />
</TelemetryProvider>
```

## Detailed References

- **Full API Reference**: See [references/api.md](references/api.md) for complete APIs
- **Integration Patterns**: See [references/integrations.md](references/integrations.md) for platform-specific patterns
- **Usage Examples**: See [references/examples.md](references/examples.md) for common patterns

## Critical Rules

1. **Use umbrella package** - Always use `@workleap/telemetry`, not standalone packages
2. **Do not invent APIs** - Only use documented APIs from references
3. **Correlation is automatic** - Never manually set Telemetry Id or Device Id
4. **Noop for non-production** - Use `NoopTelemetryClient` in Storybook/tests
5. **Privacy matters** - Never log PII to LogRocket; use `data-public`/`data-private` attributes
