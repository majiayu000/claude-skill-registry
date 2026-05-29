---
name: python-micrometer-core
description: |
  Instrument Java/Spring Boot applications with observability metrics. Use when adding metrics to microservices,
  integrating with monitoring systems (Prometheus, Cloud Monitoring), managing metric cardinality, or implementing
  SLI/SLO monitoring. Works with Spring Boot Actuator, GCP Cloud Monitoring, and dimensional metrics.
---

# Micrometer Skill

## Table of Contents

1. [Purpose](#purpose)
2. [When to Use](#when-to-use)
3. [Quick Start](#quick-start)
4. [Instructions](#instructions)
5. [Examples](#examples)
6. [Requirements](#requirements)
7. [See Also](#see-also)

---

## Purpose

Master Micrometer for comprehensive metrics instrumentation in Java/Spring Boot microservices. This skill covers meter types, dimensional metrics with tags, cardinality management, Spring Boot integration, and monitoring system backends.

## When to Use

Use this skill when you need to:

- **Add metrics to microservices** - Instrument application code with counters, timers, gauges, and distribution summaries
- **Integrate with monitoring systems** - Export metrics to Prometheus, GCP Cloud Monitoring, Datadog, or other backends
- **Understand meter types** - Choose the right meter type (Counter, Gauge, Timer, DistributionSummary) for your use case
- **Implement dimensional metrics** - Use tags to add context to metrics for filtering and aggregation
- **Manage metric cardinality** - Prevent memory issues from unbounded tag values
- **Configure Spring Boot Actuator** - Enable and customize auto-configured metrics
- **Create custom metrics** - Instrument business logic with application-specific measurements
- **Set up histogram buckets** - Configure SLO-aligned buckets for latency percentiles

**When NOT to use:**
- For initial Micrometer setup (use `python-micrometer-metrics-setup` instead)
- For business-specific KPI metrics (use `python-micrometer-business-metrics` instead)
- For high-cardinality tag management (use `python-micrometer-cardinality-control` instead)
- For GCP-specific export configuration (use `python-micrometer-gcp-cloud-monitoring` instead)

---

## Quick Start

Add metrics to a Spring Boot service in 2 minutes:

```java
@Service
public class ChargeProcessingService {

    private final Counter chargesProcessed;
    private final Timer processingTimer;

    public ChargeProcessingService(MeterRegistry registry) {
        // Counter - monotonically increasing
        this.chargesProcessed = Counter.builder("charge.processed")
            .tag("type", "supplier")
            .register(registry);

        // Timer - measures duration and frequency
        this.processingTimer = Timer.builder("charge.processing.duration")
            .serviceLevelObjectives(
                Duration.ofMillis(100),
                Duration.ofMillis(500),
                Duration.ofSeconds(1)
            )
            .register(registry);
    }

    public void processCharge(Charge charge) {
        Timer.Sample sample = Timer.start();

        try {
            // Process charge...
            chargesProcessed.increment();
        } finally {
            sample.stop(processingTimer);
        }
    }
}
```

Expose metrics:

```bash
# View all metrics
curl http://localhost:8080/actuator/metrics

# View specific metric
curl http://localhost:8080/actuator/metrics/charge.processed

# Prometheus scrape endpoint (add micrometer-registry-prometheus)
curl http://localhost:8080/actuator/prometheus
```

## Instructions

### Step 1: Add Dependencies

Add Micrometer to your Gradle build:

```kotlin
dependencies {
    // Spring Boot Actuator (includes Micrometer)
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    // Backend registries (choose based on monitoring system)
    implementation("io.micrometer:micrometer-registry-prometheus")  // For Prometheus
    implementation("io.micrometer:micrometer-registry-stackdriver")  // For GCP Cloud Monitoring

    // OpenTelemetry bridge for tracing
    implementation("io.micrometer:micrometer-tracing-bridge-otel")
}
```

### Step 2: Configure Actuator & Metrics

Update `application.yml`:

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
      base-path: /actuator

  endpoint:
    metrics:
      enabled: true
    prometheus:
      enabled: true

  metrics:
    enable:
      jvm: true
      process: true
      system: true
      logback: true

    distribution:
      percentiles-histogram:
        http.server.requests: true  # Create histogram buckets

      slo:
        http.server.requests: 10ms,50ms,100ms,500ms,1s  # SLO thresholds

    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:local}
```

### Step 3: Understand Meter Types

**Counter** - Monotonically increasing value:
```java
Counter counter = Counter.builder("api.requests")
    .tag("endpoint", "/charges")
    .register(registry);

counter.increment();    // +1
counter.increment(5);   // +5
```

**Gauge** - Point-in-time value (up or down):
```java
// Function-based (recommended)
Gauge.builder("queue.size", queue, Queue::size)
    .register(registry);

// AtomicInteger
AtomicInteger depth = new AtomicInteger(0);
Gauge.builder("queue.depth", depth, AtomicInteger::get)
    .register(registry);
```

**Timer** - Measures duration and frequency:
```java
// Record operation duration
Timer timer = Timer.builder("database.query")
    .register(registry);

timer.record(() -> {
    // database operation
});

// Or with Sample
Timer.Sample sample = Timer.start(registry);
// ... perform operation
sample.stop(Timer.builder("api.latency")
    .register(registry));
```

**DistributionSummary** - Tracks distribution of non-time values:
```java
DistributionSummary summary = DistributionSummary.builder("request.size")
    .baseUnit("bytes")
    .register(registry);

summary.record(fileSize);
```

### Step 4: Master Tag Cardinality (CRITICAL!)

**Safe Tags** (bounded, low cardinality):
```java
// ✅ HTTP method (4-10 values)
.tag("method", "GET")

// ✅ Status class (5 values)
.tag("status.class", "2xx")

// ✅ Environment (3-5 values)
.tag("env", "production")
```

**Dangerous Tags** (unbounded, high cardinality):
```java
// ❌ User ID (millions of values) → Use tracing instead
.tag("user.id", userId)

// ❌ Request ID (infinite values) → Use tracing instead
.tag("request.id", requestId)

// ❌ Full URI with parameters → Normalize!
.tag("uri", "/api/charges?supplier=123&date=2025-01-01")
```

**Prevent OOM from High Cardinality**:
```java
@Bean
public MeterFilter cardinalityLimiter() {
    // Limit unique URIs to 100
    return MeterFilter.maximumAllowableTags(
        "http.requests",
        "uri",
        100,
        MeterFilter.deny()  // Deny new meters after limit
    );
}

// OR normalize tags to bounded categories
@Bean
public MeterFilter uriNormalization() {
    return MeterFilter.replaceTagValues("uri", uri -> {
        // /api/charges/12345 → /api/charges/{id}
        return uri.replaceAll("/\\d+", "/{id}");
    });
}
```

### Step 5: Create Custom Metrics

**Method 1: Direct Registry (Recommended)**
```java
@Service
public class SupplierService {

    private final Counter suppliersCreated;
    private final Timer supplierLookup;
    private final DistributionSummary supplierWeight;

    public SupplierService(MeterRegistry registry) {
        this.suppliersCreated = Counter.builder("supplier.created")
            .description("New suppliers created")
            .register(registry);

        this.supplierLookup = Timer.builder("supplier.lookup.duration")
            .description("Time to lookup supplier")
            .register(registry);

        this.supplierWeight = DistributionSummary.builder("supplier.weight")
            .baseUnit("kg")
            .description("Supplier shipment weight")
            .register(registry);
    }

    public Supplier createSupplier(String name) {
        Timer.Sample sample = Timer.start();
        try {
            Supplier supplier = new Supplier(name);
            suppliersCreated.increment();
            return supplier;
        } finally {
            sample.stop(supplierLookup);
        }
    }
}
```

**Method 2: @Timed Annotation**
```java
@Configuration
public class MetricsConfig {
    @Bean
    public TimedAspect timedAspect(MeterRegistry registry) {
        return new TimedAspect(registry);
    }
}

@Service
public class InvoiceService {

    @Timed(
        value = "invoice.generation",
        description = "Time to generate invoice",
        percentiles = {0.95, 0.99}
    )
    public Invoice generateInvoice(String supplierId) {
        // Implementation
        return invoice;
    }
}
```

### Step 6: Apply Common Tags Organization-Wide

```java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> commonTags(
            @Value("${spring.application.name}") String appName,
            @Value("${environment}") String environment) {

        return registry -> registry.config()
            .commonTags(
                "application", appName,           // "supplier-charges-api"
                "environment", environment,        // "production"
                "region", "europe-west2",         // GKE region
                "cluster", "supplier-charges-gke" // Cluster name
            );
    }
}
```

## Examples

### Example 1: Comprehensive Service Metrics

```java
@Service
public class ChargeProcessingService {

    private final Counter chargesProcessed;
    private final Counter chargesFailed;
    private final Timer processingTimer;
    private final DistributionSummary chargeAmount;
    private final Gauge queueDepth;

    public ChargeProcessingService(MeterRegistry registry) {
        this.chargesProcessed = Counter.builder("charge.processed")
            .tag("type", "supplier")
            .description("Total charges processed successfully")
            .register(registry);

        this.chargesFailed = Counter.builder("charge.failed")
            .tag("type", "supplier")
            .description("Failed charge processing attempts")
            .register(registry);

        this.processingTimer = Timer.builder("charge.processing.duration")
            .description("Time to process a charge")
            .serviceLevelObjectives(
                Duration.ofMillis(100),
                Duration.ofMillis(500),
                Duration.ofMillis(1000)
            )
            .register(registry);

        this.chargeAmount = DistributionSummary.builder("charge.amount")
            .baseUnit("GBP")
            .description("Charge amount distribution")
            .register(registry);

        this.queueDepth = Gauge.builder("charge.queue.depth",
                this::getCurrentQueueDepth)
            .description("Current charge processing queue size")
            .register(registry);
    }

    public void processCharge(Charge charge) {
        Timer.Sample sample = Timer.start();

        try {
            validateCharge(charge);
            persistCharge(charge);

            chargeAmount.record(charge.getAmount().doubleValue());
            chargesProcessed.increment();

        } catch (ValidationException e) {
            chargesFailed.increment();
            throw e;
        } finally {
            sample.stop(processingTimer);
        }
    }

    private int getCurrentQueueDepth() {
        // Return queue size at observation time
        return chargingQueue.size();
    }
}
```

### Example 2: Actuator Integration with Spring Boot

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus

  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true

      slo:
        http.server.requests: 50ms,100ms,500ms,1s

    enable:
      jvm: true
      process: true
      system: true
      logback: true

    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:labs}
      region: europe-west2

  endpoint:
    health:
      show-details: always
    prometheus:
      enabled: true
```

**Endpoints**:
- `/actuator/metrics` - List all metrics
- `/actuator/metrics/charge.processed` - View specific metric
- `/actuator/prometheus` - Prometheus scrape endpoint
- `/actuator/health` - Application health

### Example 3: GCP Cloud Monitoring Integration

```yaml
# application.yml
spring:
  cloud:
    gcp:
      project-id: ecp-wtr-supplier-charges-labs

management:
  metrics:
    export:
      stackdriver:
        enabled: true
        project-id: ecp-wtr-supplier-charges-labs
        step: 1m
        use-semantic-metric-names: true
```

With Gradle dependency:
```kotlin
implementation("io.micrometer:micrometer-registry-stackdriver")
```

Metrics automatically exported to Cloud Monitoring!

### Example 4: Prevent High Cardinality OOM

```java
@Configuration
public class MetricsConfig {

    /**
     * Limits metric cardinality to prevent OutOfMemoryError.
     * Each unique URI creates a separate metric, so we cap at 100.
     */
    @Bean
    public MeterFilter cardinalityDefense() {
        return MeterFilter.maximumAllowableTags(
            "http.server.requests",
            "uri",
            100,  // Max 100 unique URIs
            MeterFilter.deny()  // Reject new meters after limit
        );
    }

    /**
     * Normalize URIs to bounded categories.
     * /api/charges/12345 → /api/charges/{id}
     * /api/charges/67890 → /api/charges/{id}
     */
    @Bean
    public MeterFilter uriNormalization() {
        return MeterFilter.replaceTagValues("uri", uri -> {
            // Strip query parameters
            int queryIndex = uri.indexOf('?');
            if (queryIndex > 0) {
                uri = uri.substring(0, queryIndex);
            }

            // Replace IDs with placeholders
            return uri.replaceAll("/\\d+", "/{id}")
                     .replaceAll("/[a-f0-9-]{36}", "/{uuid}");
        });
    }

    /**
     * Monitor metric cardinality itself.
     */
    @Bean
    public MeterBinder cardinalityMonitor(MeterRegistry registry) {
        return (r) -> Gauge.builder("micrometer.meter.count",
                registry, MeterRegistry::getMeters,
                Collection::size)
            .description("Number of meters in registry")
            .register(r);
    }
}
```

## Requirements

- Spring Boot 2.2+ (Micrometer included)
- Micrometer core library (auto-included with Actuator)
- JVM application with Spring Boot
- Monitoring system backend (Prometheus, Cloud Monitoring, etc.)

**Dependencies**:
```gradle
implementation("org.springframework.boot:spring-boot-starter-actuator")

// Choose one or more backends:
implementation("io.micrometer:micrometer-registry-prometheus")
implementation("io.micrometer:micrometer-registry-stackdriver")
implementation("io.micrometer:micrometer-tracing-bridge-otel")
```

## See Also

- **Meter Types**: Counter, Gauge, Timer, DistributionSummary
- **Dimensional Metrics**: Tags, Cardinality Management, Tag Normalization
- **Spring Boot Integration**: Actuator, Auto-configuration, Common Metrics
- **Monitoring Backends**: Prometheus, Cloud Monitoring, Datadog, New Relic
- **Performance**: Percentiles, Histograms, SLO Buckets
- **Troubleshooting**: High Cardinality, Memory Usage, Metric Naming
