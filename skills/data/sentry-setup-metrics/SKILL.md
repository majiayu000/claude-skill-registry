---
name: sentry-setup-metrics
description: Setup Sentry Metrics in any project. Use this when asked to add Sentry metrics, track custom metrics, setup counters/gauges/distributions, or instrument application performance metrics. Supports JavaScript, TypeScript, Python, React, Next.js, and Node.js.
---

# SOURCE: getsentry/sentry-for-claude
# PATH: skills/sentry-setup-metrics/SKILL.md


# Setup Sentry Metrics

This skill helps configure Sentry's custom metrics feature to track counters, gauges, and distributions across your applications.

## When to Use This Skill

Invoke this skill when:
- User asks to "setup Sentry metrics" or "add custom metrics"
- User wants to "track metrics in Sentry"
- User requests "counters", "gauges", or "distributions" with Sentry
- User mentions they want to track business KPIs or application health
- User asks about `Sentry.metrics` or `sentry_sdk.metrics`
- User wants to instrument performance metrics

## Platform Support

**Supported Platforms:**
- JavaScript/TypeScript (SDK 10.25.0+): Next.js, React, Node.js, Browser
- Python (SDK 2.44.0+): Django, Flask, FastAPI, general Python

**Note:** Ruby does not currently have dedicated metrics support in the Sentry SDK.

## Metric Types Overview

Before setup, explain the three metric types to the user:

| Type | Purpose | Use Cases | Aggregations |
|------|---------|-----------|--------------|
| **Counter** | Track cumulative occurrences | Button clicks, API calls, errors | sum, per_second, per_minute |
| **Gauge** | Point-in-time snapshots | Queue depth, memory usage, connections | min, max, avg |
| **Distribution** | Statistical analysis of values | Response times, cart amounts, query duration | p50, p75, p95, p99, avg, min, max |

## Platform Detection

### JavaScript/TypeScript Detection
Check for these files:
- `package.json` - Read to identify framework and Sentry SDK version
- Look for `@sentry/nextjs`, `@sentry/react`, `@sentry/node`, `@sentry/browser`
- Check if SDK version is 10.25.0+ (required for metrics)

### Python Detection
Check for:
- `requirements.txt`, `pyproject.toml`, `setup.py`, or `Pipfile`
- Look for `sentry-sdk` version 2.44.0+ (required for metrics)

## Required Information

Ask the user:

```
I'll help you set up Sentry Metrics. First, let me check your project setup.

After detecting the platform:

1. **What metrics do you want to track?**
   - Counters: Event counts (clicks, API calls, errors)
   - Gauges: Point-in-time values (queue depth, memory)
   - Distributions: Value analysis (response times, amounts)

2. **Do you need metric filtering?**
   - Yes: Configure beforeSendMetric to filter/modify metrics
   - No: Send all metrics as-is
```

---

## JavaScript/TypeScript Configuration

### Minimum SDK Version
- All JS platforms: `10.25.0+`

### Step 1: Verify SDK Version

```bash
grep -E '"@sentry/(nextjs|react|node|browser)"' package.json
```

If version is below 10.25.0, inform user to upgrade:
```bash
npm install @sentry/nextjs@latest  # or appropriate package
```

### Step 2: Verify Metrics Are Enabled

Metrics are **enabled by default** in SDK 10.25.0+. No changes to `Sentry.init()` are required unless user wants to disable or filter.

**Locate init files:**
- Next.js: `instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`
- React: `src/index.tsx`, `src/main.tsx`, or dedicated sentry config file
- Node.js: Entry point file or dedicated sentry config
- Browser: Entry point or config file

**Optional: Explicitly enable (not required):**

```javascript
import * as Sentry from "@sentry/nextjs"; // or @sentry/react, @sentry/node

Sentry.init({
  dsn: "YOUR_DSN_HERE",

  // Metrics enabled by default, but can be explicit
  enableMetrics: true,

  // ... other existing config
});
```

### Step 3: Add Metric Filtering (Optional)

If user wants to filter metrics before sending:

```javascript
Sentry.init({
  dsn: "YOUR_DSN_HERE",

  beforeSendMetric: (metric) => {
    // Drop metrics with sensitive attributes
    if (metric.attributes?.sensitive === true) {
      return null;
    }

    // Remove specific attribute before sending
    if (metric.attributes?.internal) {
      delete metric.attributes.internal;
    }

    return metric;
  },
});
```

### Step 4: Disable Metrics (If Requested)

If user explicitly wants to disable metrics:

```javascript
Sentry.init({
  dsn: "YOUR_DSN_HERE",
  enableMetrics: false,
});
```

---

## JavaScript Metrics API Examples

Provide these examples to the user based on their use case:

### Counter Examples

```javascript
// Basic counter - increment by 1
Sentry.metrics.count("button_click", 1);

// Counter with attributes for filtering/grouping
Sentry.metrics.count("api_call", 1, {
  attributes: {
    endpoint: "/api/users",
    method: "GET",
    status_code: 200,
  },
});

// Counter for errors
Sentry.metrics.count("checkout_error", 1, {
  attributes: {
    error_type: "payment_declined",
    payment_provider: "stripe",
  },
});

// Counter for business events
Sentry.metrics.count("email_sent", 1, {
  attributes: {
    template: "welcome",
    recipient_type: "new_user",
  },
});
```

### Gauge Examples

```javascript
// Basic gauge
Sentry.metrics.gauge("queue_depth", 42);

// Memory usage gauge
Sentry.metrics.gauge("memory_usage", process.memoryUsage().heapUsed, {
  unit: "byte",
  attributes: {
    process: "main",
  },
});

// Connection pool gauge
Sentry.metrics.gauge("db_connections", 15, {
  attributes: {
    pool: "primary",
    max_connections: 100,
  },
});

// Active users gauge
Sentry.metrics.gauge("active_users", currentUserCount, {
  attributes: {
    region: "us-east",
  },
});
```

### Distribution Examples

```javascript
// Response time distribution
Sentry.metrics.distribution("response_time", 187.5, {
  unit: "millisecond",
  attributes: {
    endpoint: "/api/products",
    method: "GET",
  },
});

// Cart value distribution
Sentry.metrics.distribution("cart_value", 149.99, {
  unit: "usd",
  attributes: {
    customer_tier: "premium",
  },
});

// Query duration distribution
Sentry.metrics.distribution("db_query_duration", 45.2, {
  unit: "millisecond",
  attributes: {
    query_type: "select",
    table: "users",
  },
});

// File size distribution
Sentry.metrics.distribution("upload_size", 2048576, {
  unit: "byte",
  attributes: {
    file_type: "image",
  },
});
```

### Manual Flush

```javascript
// Force pending metrics to send immediately
await Sentry.flush();

// Useful before process exit or after critical operations
process.on("beforeExit", async () => {
  await Sentry.flush();
});
```

---

## Python Configuration

### Minimum SDK Version
- `sentry-sdk` version `2.44.0+`

### Step 1: Verify SDK Version

```bash
pip show sentry-sdk | grep Version
```

If version is below 2.44.0:
```bash
pip install --upgrade sentry-sdk
```

### Step 2: Verify Metrics Are Enabled

Metrics are **enabled by default** in SDK 2.44.0+. No changes required unless filtering is needed.

**Common init locations:**
- Django: `settings.py`
- Flask: `app.py` or `__init__.py`
- FastAPI: `main.py`
- General: Entry point or dedicated config file

### Step 3: Add Metric Filtering (Optional)

```python
import sentry_sdk

def before_send_metric(metric, hint):
    # Drop metrics with specific attributes
    if metric.get("attributes", {}).get("sensitive"):
        return None

    # Modify metric before sending
    if metric.get("attributes", {}).get("internal"):
        del metric["attributes"]["internal"]

    return metric

sentry_sdk.init(
    dsn="YOUR_DSN_HERE",
    before_send_metric=before_send_metric,
)
```

---

## Python Metrics API Examples

### Counter Examples

```python
import sentry_sdk

# Basic counter
sentry_sdk.metrics.count("button_click", 1)

# Counter with attributes
sentry_sdk.metrics.count(
    "api_call",
    1,
    attributes={
        "endpoint": "/api/users",
        "method": "GET",
        "status_code": 200,
    }
)

# Counter for errors
sentry_sdk.metrics.count(
    "checkout_error",
    1,
    attributes={
        "error_type": "payment_declined",
        "payment_provider": "stripe",
    }
)

# Business event counter
sentry_sdk.metrics.count(
    "email_sent",
    5,  # Can increment by more than 1
    attributes={
        "template": "newsletter",
        "batch_id": "batch_123",
    }
)
```

### Gauge Examples

```python
import sentry_sdk
import psutil

# Basic gauge
sentry_sdk.metrics.gauge("queue_depth", 42)

# Memory usage gauge
sentry_sdk.metrics.gauge(
    "memory_usage",
    psutil.virtual_memory().used,
    unit="byte",
    attributes={"host": "web-01"}
)

# Database connection gauge
sentry_sdk.metrics.gauge(
    "db_connections",
    connection_pool.size(),
    attributes={
        "pool": "primary",
        "max": connection_pool.max_size,
    }
)

# Cache hit rate gauge
sentry_sdk.metrics.gauge(
    "cache_hit_rate",
    0.85,
    attributes={"cache": "redis"}
)
```

### Distribution Examples

```python
import sentry_sdk
import time

# Response time distribution
start = time.time()
# ... do work ...
duration_ms = (time.time() - start) * 1000

sentry_sdk.metrics.distribution(
    "response_time",
    duration_ms,
    unit="millisecond",
    attributes={
        "endpoint": "/api/products",
        "method": "GET",
    }
)

# Order value distribution
sentry_sdk.metrics.distribution(
    "order_value",
    order.total,
    unit="usd",
    attributes={
        "customer_tier": customer.tier,
        "payment_method": order.payment_method,
    }
)

# Query duration distribution
sentry_sdk.metrics.distribution(
    "db_query_duration",
    query_time_ms,
    unit="millisecond",
    attributes={
        "query_type": "select",
        "table": "orders",
    }
)
```

---

## Framework-Specific Notes

### Next.js
- Metrics work on both client and server
- Consider tracking in API routes and server components
- Use attributes to distinguish client vs server metrics

### React (Browser)
- Track user interactions (clicks, form submissions)
- Monitor component render performance
- Be mindful of metric volume from client-side

### Node.js
- Track API response times, queue depths, background job metrics
- Use gauges for resource monitoring
- Flush metrics before process exit

### Django
- Track view response times
- Monitor database query performance
- Use middleware for automatic request metrics

### Flask/FastAPI
- Track endpoint performance
- Monitor external API call durations
- Use decorators or middleware for automatic instrumentation

---

## Common Units

Use these units for better readability in Sentry dashboard:

| Category | Units |
|----------|-------|
| **Time** | `nanosecond`, `microsecond`, `millisecond`, `second`, `minute`, `hour`, `day`, `week` |
| **Size** | `bit`, `byte`, `kilobyte`, `megabyte`, `gigabyte`, `terabyte` |
| **Currency** | `usd`, `eur`, `gbp` (or any ISO currency code) |
| **Rate** | `ratio`, `percent` |
| **Other** | `none` (default), or custom string |

---

## Best Practices

### DO Use Metrics For:
- Business KPIs (orders, signups, revenue)
- Application health (error rates, latency)
- Resource utilization (queue depth, connections)
- User actions (clicks, page views, feature usage)

### DON'T Use Metrics For:
- Infrastructure monitoring (use dedicated tools)
- Log aggregation (use Sentry Logs instead)
- Full request tracing (use Sentry Tracing)
- High-cardinality data in attributes

### Naming Conventions:
```
# Good - descriptive, namespaced
api.request.duration
checkout.cart.value
user.signup.completed

# Avoid - vague, inconsistent
duration
value1
myMetric
```

### Attribute Guidelines:
- Keep cardinality low (avoid user IDs, request IDs)
- Use consistent attribute names across metrics
- Include relevant context for filtering
- Avoid sensitive data in attributes

---

## Instrumentation Patterns

### Timing Helper (JavaScript)

```javascript
async function withTiming(name, fn, attributes = {}) {
  const start = performance.now();
  try {
    return await fn();
  } finally {
    const duration = performance.now() - start;
    Sentry.metrics.distribution(name, duration, {
      unit: "millisecond",
      attributes,
    });
  }
}

// Usage
const result = await withTiming(
  "api.external.duration",
  () => fetch("https://api.example.com/data"),
  { service: "example-api" }
);
```

### Timing Decorator (Python)

```python
import functools
import time
import sentry_sdk

def track_duration(metric_name, **extra_attrs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                duration_ms = (time.time() - start) * 1000
                sentry_sdk.metrics.distribution(
                    metric_name,
                    duration_ms,
                    unit="millisecond",
                    attributes=extra_attrs,
                )
        return wrapper
    return decorator

# Usage
@track_duration("db.query.duration", query_type="user_lookup")
def get_user_by_id(user_id):
    return db.query(User).filter(User.id == user_id).first()
```

### Request Middleware (Express/Node.js)

```javascript
function metricsMiddleware(req, res, next) {
  const start = performance.now();

  res.on("finish", () => {
    const duration = performance.now() - start;

    Sentry.metrics.distribution("http.request.duration", duration, {
      unit: "millisecond",
      attributes: {
        method: req.method,
        route: req.route?.path || req.path,
        status_code: res.statusCode,
      },
    });

    Sentry.metrics.count("http.request.count", 1, {
      attributes: {
        method: req.method,
        status_code: res.statusCode,
      },
    });
  });

  next();
}

app.use(metricsMiddleware);
```

### Django Middleware

```python
import time
import sentry_sdk

class SentryMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration_ms = (time.time() - start) * 1000

        sentry_sdk.metrics.distribution(
            "http.request.duration",
            duration_ms,
            unit="millisecond",
            attributes={
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
            },
        )

        return response

# Add to MIDDLEWARE in settings.py
```

---

## Verification Steps

After setup, provide these verification instructions:

### JavaScript Verification
```javascript
// Add this temporarily to test
Sentry.metrics.count("test_metric", 1, {
  attributes: { test: true },
});

Sentry.metrics.gauge("test_gauge", 42);

Sentry.metrics.distribution("test_distribution", 100, {
  unit: "millisecond",
});

// Force flush to send immediately
await Sentry.flush();
```

### Python Verification
```python
import sentry_sdk

sentry_sdk.metrics.count("test_metric", 1, attributes={"test": True})
sentry_sdk.metrics.gauge("test_gauge", 42)
sentry_sdk.metrics.distribution("test_distribution", 100, unit="millisecond")
```

Tell user to check their Sentry dashboard under **Metrics** section to verify metrics are arriving.

---

## Common Issues and Solutions

### Issue: Metrics not appearing in Sentry
**Solutions:**
1. Verify SDK version meets minimum requirements (JS: 10.25.0+, Python: 2.44.0+)
2. Ensure metrics aren't disabled (`enableMetrics: false`)
3. Check DSN is correct
4. Wait a few minutes - metrics are buffered before sending
5. Try manual flush: `await Sentry.flush()` or check aggregation window

### Issue: Too many metrics being sent
**Solutions:**
1. Use `beforeSendMetric` to filter unnecessary metrics
2. Reduce attribute cardinality
3. Sample metrics on high-traffic paths
4. Aggregate client-side before sending

### Issue: High cardinality warnings
**Solutions:**
1. Avoid user IDs, request IDs, timestamps in attributes
2. Use categories instead of specific values
3. Limit unique attribute value combinations

### Issue: Metrics not linked to traces
**Solutions:**
1. Ensure tracing is enabled alongside metrics
2. Emit metrics within traced spans
3. Check that trace sampling isn't dropping related traces

---

## Summary Checklist

Provide this checklist after setup:

```markdown
## Sentry Metrics Setup Complete

### Configuration Applied:
- [ ] SDK version verified (JS: 10.25.0+, Python: 2.44.0+)
- [ ] Metrics enabled (default) or explicitly configured
- [ ] Metric filtering configured (if requested)

### Instrumentation Added:
- [ ] Counter metrics for events/actions
- [ ] Gauge metrics for point-in-time values
- [ ] Distribution metrics for timing/values
- [ ] Appropriate units specified
- [ ] Meaningful attributes added

### Next Steps:
1. Run your application
2. Trigger actions that emit metrics
3. Check Sentry dashboard > Metrics section
4. Create dashboards and alerts based on metrics
```

---

## Quick Reference

| Platform | SDK Version | API Namespace |
|----------|-------------|---------------|
| JavaScript | 10.25.0+ | `Sentry.metrics.*` |
| Python | 2.44.0+ | `sentry_sdk.metrics.*` |

| Method | JavaScript | Python |
|--------|------------|--------|
| Counter | `Sentry.metrics.count(name, value, options)` | `sentry_sdk.metrics.count(name, value, **kwargs)` |
| Gauge | `Sentry.metrics.gauge(name, value, options)` | `sentry_sdk.metrics.gauge(name, value, **kwargs)` |
| Distribution | `Sentry.metrics.distribution(name, value, options)` | `sentry_sdk.metrics.distribution(name, value, **kwargs)` |

| Option | JavaScript | Python |
|--------|------------|--------|
| Unit | `{ unit: "millisecond" }` | `unit="millisecond"` |
| Attributes | `{ attributes: { key: "value" } }` | `attributes={"key": "value"}` |
