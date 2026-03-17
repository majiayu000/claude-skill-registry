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

## When to Use

- Add tags to metrics (ensure bounded cardinality)
- Normalize high-cardinality data (URIs, IDs)
- Prevent OutOfMemoryError from metric explosion
- Control monitoring costs
- Debug metric growth

**When NOT to use:**
- Truly unbounded data (use distributed tracing)
- Per-request details (use structured logging)

## Cardinality Rules

### Safe Tags (Low Cardinality)

```java
// ✅ HTTP method (4-10 values)
.tag("method", "GET")

// ✅ Status class (5 values)
.tag("status.class", "2xx")

// ✅ Environment (3-5 values)
.tag("env", "production")
```

### Dangerous Tags (High Cardinality)

```java
// ❌ User ID (millions) → Use tracing
.tag("user.id", userId)

// ❌ Request ID (infinite) → Use tracing
.tag("request.id", requestId)

// ❌ Full URI → Normalize!
.tag("uri", "/api/charges?supplier=123")
```

**Rule of Thumb:**
- Safe per metric: < 1,000 combinations
- Safe application-wide: < 10,000 active metrics

## Normalization Patterns

### URI Normalization

```java
@Bean
public MeterFilter uriNormalization() {
    return MeterFilter.replaceTagValues("uri", uri -> {
        // Strip query parameters
        int queryIndex = uri.indexOf('?');
        if (queryIndex > 0) uri = uri.substring(0, queryIndex);

        // Replace IDs: /charges/123 → /charges/{id}
        return uri.replaceAll("/\\d+", "/{id}")
                  .replaceAll("/[a-f0-9-]{36}", "/{uuid}");
    });
}
```

### Business Category Normalization

```java
private String normalizeSupplier(String supplierId) {
    Supplier supplier = supplierRepository.findById(supplierId);
    
    if (supplier.getAnnualVolume() > 1_000_000) return "enterprise";
    if (supplier.getAnnualVolume() > 100_000) return "mid-market";
    if (supplier.isDirect()) return "direct";
    return "standard";
}
```

## Cardinality Limits

```java
@Bean
public MeterFilter cardinalityLimiter() {
    // Limit unique URIs to 100
    return MeterFilter.maximumAllowableTags(
        "http.server.requests",
        "uri",
        100,
        MeterFilter.deny()  // Deny new meters after limit
    );
}
```

## Monitor Cardinality

```java
@Component
public class CardinalityMonitor {

    private final MeterRegistry registry;

    @Scheduled(fixedRate = 60_000)
    public void monitorMetricCount() {
        int meterCount = registry.getMeters().size();

        if (meterCount > 8000) {
            log.error("CRITICAL: {} metrics (threshold 8000)", meterCount);
        }

        Gauge.builder("micrometer.meter.count", () -> meterCount)
             .register(registry);
    }
}
```

## Alternatives to High-Cardinality Tags

### Use Distributed Tracing

```java
// Store user ID in span, NOT metrics
span.setAttribute("user.id", userId);

// Metrics use only bounded tags
Timer.builder("charge.processing")
    .tag("status", "processing")  // bounded
    .register(registry);
```

### Use Structured Logging

```java
// Add to MDC for logging, NOT metrics
MDC.put("user.id", userId);
```

## Requirements

- Spring Boot 2.1+
- spring-boot-starter-actuator
- Java 11+
- For tracing: micrometer-tracing-bridge-otel

## Anti-Patterns

```java
// ❌ NEVER add unbounded tags
.tag("user.id", userId)
.tag("request.id", requestId)
.tag("timestamp", Instant.now())

// ✅ DO normalize to bounded categories
.tag("customer.tier", normalizeCustomer(customer))
.tag("request.type", normalizeRequest(request))
```

## See Also

- [python-micrometer-core](../python-micrometer-core/SKILL.md) - Meter types
- [python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md) - Business KPIs
