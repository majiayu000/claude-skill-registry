---
name: python-micrometer-cardinality-control
description: |
  Prevent OutOfMemoryError from unbounded metric tags by implementing cardinality limits.
  Use when adding tags to Micrometer metrics, normalizing URIs or IDs to bounded categories,
  monitoring metric explosion, or avoiding high-cardinality fields like user IDs and request IDs.
  Critical for production microservices in GKE with cost-sensitive monitoring backends.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer Cardinality Control

## Table of Contents

1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [Quick Start](#quick-start)
4. [Instructions](#instructions)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
8. [See Also](#see-also)

---

## Purpose

Metric cardinality (number of unique tag combinations) directly impacts memory usage and monitoring costs. Unbounded tags like user IDs, request IDs, or full URIs create millions of unique metrics, causing memory exhaustion and expensive billing. This skill provides patterns to detect, prevent, and remediate cardinality issues.

## When to Use

Use this skill when you need to:

- **Add tags to metrics** - Ensure tags have bounded cardinality before adding to counters, timers, or gauges
- **Normalize high-cardinality data** - Convert unbounded values (user IDs, URIs) to bounded categories
- **Prevent OutOfMemoryError** - Limit metric explosion that crashes JVM with heap exhaustion
- **Control monitoring costs** - Reduce metric volume to avoid expensive billing from monitoring backends
- **Monitor metric growth** - Detect cardinality explosions before they impact production
- **Implement MeterFilter limits** - Configure hard limits on tag values per metric
- **Debug metric explosion** - Investigate why metric count is growing unexpectedly

**When NOT to use:**
- For truly unbounded data like user IDs (use distributed tracing instead)
- When you need per-request details (use structured logging with correlation IDs)
- Before understanding basic Micrometer setup (use `python-micrometer-metrics-setup` first)

---

## Quick Start

For any metric with dynamic tags, apply this pattern:

```java
// ❌ Dangerous: unbounded cardinality
.tag("supplier.id", supplierId) // 10,000+ unique values

// ✅ Safe: normalized to bounded categories
.tag("supplier.category", normalizeSupplier(supplier)) // 5-10 values

private String normalizeSupplier(Supplier s) {
    if (s.isTopTier()) return "tier1";
    if (s.isDirectSupplier()) return "direct";
    return "standard";
}
```

## Instructions

### Step 1: Identify Dangerous Tag Values

Before adding any tag, ask: "How many unique values could this tag have?"

**High-cardinality tags (AVOID):**
- User IDs, Customer IDs, Supplier IDs (unbounded)
- Request IDs, Transaction IDs (infinite unique values)
- Full URIs with query parameters (`/api/charges?supplier=123&date=2025-01-01`)
- Timestamps, email addresses, UUIDs
- Full exception class names (can vary with stack traces)

**Low-cardinality tags (SAFE):**
- HTTP methods: GET, POST, PUT, DELETE (4-10 values)
- HTTP status codes: 200, 201, 400, 404, 500 (≤20 values)
- Status class: 1xx, 2xx, 3xx, 4xx, 5xx (5 values)
- Environment: dev, staging, production (3-5 values)
- Supplier category: tier1, direct, international, standard (5-10 values)
- Feature flags: enabled, disabled (2 values)

**Cardinality Rule of Thumb:**
- Safe per metric family: < 1,000 unique tag combinations
- Safe application-wide: < 10,000 active metrics
- Monitor via: `/actuator/metrics` endpoint

### Step 2: Normalize to Bounded Categories

For naturally high-cardinality data, create a normalization function:

```java
// Example: Normalize supplier ID to category
private String normalizeSupplierCategory(String supplierId) {
    Supplier supplier = supplierRepository.findById(supplierId);

    // Business logic: categorize suppliers
    if (supplier.getAnnualVolume() > 1_000_000) return "enterprise";
    if (supplier.getAnnualVolume() > 100_000) return "mid-market";
    if (supplier.isDirect()) return "direct";
    return "standard";
}

// Usage in metrics
Counter.builder("supplier.charges")
    .tag("supplier.category", normalizeSupplierCategory(supplierId))
    .register(registry)
    .increment();
```

**Normalization Examples:**
- Supplier ID → Supplier category (tier1, direct, standard)
- Full URI → Template URI (`/charges/123` → `/charges/{id}`)
- Exception class → Exception type (validation, timeout, auth, other)
- HTTP status → Status class (2xx, 4xx, 5xx)

### Step 3: Implement MeterFilter Cardinality Limits

Use Spring's `MeterFilter` to enforce hard limits:

```java
@Configuration
public class CardinalityLimitConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> cardinalityLimiter() {
        return registry -> {
            // Limit unique URIs to 100
            registry.config().meterFilter(
                MeterFilter.maximumAllowableTags(
                    "http.server.requests",
                    "uri",
                    100,
                    MeterFilter.deny()  // Deny new meters after limit
                )
            );

            // Limit unique supplier categories to 20
            registry.config().meterFilter(
                MeterFilter.maximumAllowableTags(
                    "supplier.charges",
                    "supplier.category",
                    20,
                    MeterFilter.deny()
                )
            );
        };
    }
}
```

**MeterFilter.deny() behaviors:**
- New meters exceeding limit are rejected
- No metric is recorded for exceeded values
- Application continues normally (fails gracefully)

### Step 4: Monitor Cardinality

Create a scheduled task to detect cardinality explosions:

```java
@Component
public class CardinalityMonitor {

    private final MeterRegistry registry;
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    public CardinalityMonitor(MeterRegistry registry) {
        this.registry = registry;
    }

    @Scheduled(fixedRate = 60_000) // Every minute
    public void monitorMetricCount() {
        int meterCount = registry.getMeters().size();

        // Alert thresholds
        if (meterCount > 8000) {
            log.error("CRITICAL: Metric count {} exceeds 8000 threshold", meterCount);
        } else if (meterCount > 5000) {
            log.warn("WARNING: Metric count {} exceeds 5000 threshold", meterCount);
        }

        // Record cardinality as a metric itself
        Gauge.builder("micrometer.meter.count",
                      () -> meterCount)
             .description("Total number of metrics in registry")
             .register(registry);
    }
}
```

### Step 5: Handle User/Request-Specific Data

For truly unbounded data (user IDs, request IDs), use these alternatives:

**Option A: Use Distributed Tracing (Recommended)**
```java
@Service
public class ChargeService {

    private final Tracer tracer;
    private final MeterRegistry registry;

    public void processCharge(String userId, Charge charge) {
        Span span = tracer.currentSpan();

        // Store user ID in span attributes, NOT metrics
        span.setAttribute("user.id", userId);
        span.setAttribute("supplier.id", charge.getSupplierId());

        // Metrics use only bounded tags
        Timer.builder("charge.processing")
            .tag("status", "processing") // bounded
            .register(registry)
            .record(() -> {
                // Processing logic
            });
    }
}
```

**Option B: Store in Logs (with correlation)**
```java
@Component
public class CorrelationFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain chain) throws ServletException, IOException {

        String userId = extractUserId(request);

        // Add to logging context, NOT metrics
        MDC.put("user.id", userId);

        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();
        }
    }
}
```

**Option C: Separate Time-Series Database**
```java
// For detailed per-user analytics, use separate backend
@Service
public class UserAnalyticsService {

    private final AnalyticsDatabase analyticsDb;

    public void recordUserAction(String userId, Action action) {
        // Record in analytics DB, not Micrometer
        analyticsDb.insert(userId, action.getTimestamp(), action.getType());
    }
}
```

## Examples

### Example 1: URI Normalization Filter

Automatically replace path parameters with placeholders:

```java
@Configuration
public class URINormalizationConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> uriNormalizationFilter() {
        return registry -> {
            registry.config().meterFilter(
                MeterFilter.replaceTagValues("uri", uri -> {
                    // Strip query parameters
                    int queryIndex = uri.indexOf('?');
                    if (queryIndex > 0) {
                        uri = uri.substring(0, queryIndex);
                    }

                    // Replace numeric IDs with {id}
                    uri = uri.replaceAll("/\\d+", "/{id}");

                    // Replace UUIDs with {uuid}
                    uri = uri.replaceAll(
                        "/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}",
                        "/{uuid}"
                    );

                    return uri;
                })
            );
        };
    }
}
```

**Before:** `/charges/12345`, `/charges/67890`, `/charges/11111` = 3 metrics
**After:** `/charges/{id}` = 1 metric

### Example 2: Exception Type Normalization

Normalize exception classes to categories:

```java
@Configuration
public class ExceptionNormalizationConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> exceptionNormalization() {
        return registry -> {
            registry.config().meterFilter(
                MeterFilter.replaceTagValues("exception", exception -> {
                    if (exception.contains("ValidationException")) {
                        return "validation";
                    } else if (exception.contains("TimeoutException")) {
                        return "timeout";
                    } else if (exception.contains("AuthenticationException")) {
                        return "auth";
                    } else if (exception.contains("SQLException")) {
                        return "database";
                    }
                    return "other";
                })
            );
        };
    }
}
```

### Example 3: Detect Cardinality Explosion

Automatically alert when cardinality exceeds thresholds:

```java
@Component
public class CardinalityGuardian {

    private final MeterRegistry registry;
    private final AlertService alertService;
    private int previousCount = 0;

    @Scheduled(fixedRate = 30_000) // Every 30 seconds
    public void checkCardinalityGrowth() {
        int currentCount = registry.getMeters().size();

        // Spike detection: +500 meters in 30 seconds
        if (currentCount - previousCount > 500) {
            alertService.alert(
                "CARDINALITY_SPIKE",
                String.format(
                    "Metric count jumped from %d to %d (added %d in 30s)",
                    previousCount, currentCount, currentCount - previousCount
                )
            );
        }

        previousCount = currentCount;
    }
}
```

## Requirements

- Spring Boot 2.1+ (auto-configures `MeterRegistry`)
- `spring-boot-starter-actuator` dependency
- Java 11+
- For distributed tracing: `micrometer-tracing-bridge-otel`

## Anti-Patterns to Avoid

```java
// ❌ NEVER add unbounded tags
.tag("user.id", userId)              // Millions of unique values
.tag("request.id", requestId)        // Infinite unique values
.tag("full.uri", fullUriWithParams)  // Dynamic query strings
.tag("timestamp", Instant.now())     // Time-based explosion

// ❌ NEVER use exception names directly
.tag("exception", e.getClass().getName()) // Can vary with stack traces

// ❌ NEVER trust external IDs
.tag("customer.id", externalCustomerId)  // No control over cardinality

// ✅ DO normalize everything to bounded categories
.tag("customer.tier", normalizeCustomerTier(customer))  // 3-5 values
.tag("request.type", normalizeRequestType(request))    // 5-10 values
.tag("error.type", normalizeException(e))              // 10-15 values
```

## See Also

- [micrometer-metrics-setup](../micrometer-metrics-setup/SKILL.md) - Initial Micrometer configuration
- [micrometer-business-metrics](../micrometer-business-metrics/SKILL.md) - Domain-specific KPI metrics
- [micrometer-testing-metrics](../micrometer-testing-metrics/SKILL.md) - Testing custom metrics
