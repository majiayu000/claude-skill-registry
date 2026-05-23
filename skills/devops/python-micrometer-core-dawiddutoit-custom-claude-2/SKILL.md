---
name: python-micrometer-core
description: |
  Instrument Java/Spring Boot applications with observability metrics. Use when adding metrics to microservices,
  integrating with monitoring systems (Prometheus, Cloud Monitoring), managing metric cardinality, or implementing
  SLI/SLO monitoring. Works with Spring Boot Actuator, GCP Cloud Monitoring, and dimensional metrics.
---

# Micrometer Skill

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

## Table of Contents

1. [When to Use](#when-to-use)
2. [Setup](#setup)
3. [Meter Types](#meter-types)
4. [Tags and Cardinality](#tags-and-cardinality)
5. [Common Patterns](#common-patterns)
6. [Supporting Files](#supporting-files)
7. [Requirements](#requirements)

## When to Use

Use this skill when you need to:

- Add metrics to microservices (counters, timers, gauges, distributions)
- Integrate with monitoring systems (Prometheus, GCP Cloud Monitoring, Datadog)
- Implement dimensional metrics with tags for filtering
- Configure Spring Boot Actuator auto-metrics
- Create custom application-specific measurements

**When NOT to use:**
- For initial Micrometer setup (use `python-micrometer-metrics-setup`)
- For business KPI metrics (use `python-micrometer-business-metrics`)
- For cardinality management (use `python-micrometer-cardinality-control`)
- For GCP export (use `python-micrometer-gcp-cloud-monitoring`)

## Setup

### Dependencies

```kotlin
dependencies {
    // Spring Boot Actuator (includes Micrometer)
    implementation("org.springframework.boot:spring-boot-starter-actuator")

    // Backend registries
    implementation("io.micrometer:micrometer-registry-prometheus")  // Prometheus
    implementation("io.micrometer:micrometer-registry-stackdriver")  // GCP
}
```

### Configuration

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus

  metrics:
    enable:
      jvm: true
      process: true
      system: true

    distribution:
      percentiles-histogram:
        http.server.requests: true  # Create histogram buckets

      slo:
        http.server.requests: 10ms,50ms,100ms,500ms,1s  # SLO thresholds

    tags:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:local}
```

## Meter Types

### Counter - Monotonically Increasing

```java
Counter counter = Counter.builder("api.requests")
    .tag("endpoint", "/charges")
    .register(registry);

counter.increment();    // +1
counter.increment(5);   // +5
```

### Gauge - Point-in-Time Value

```java
// Function-based (recommended)
Gauge.builder("queue.size", queue, Queue::size)
    .register(registry);
```

### Timer - Duration and Frequency

```java
Timer timer = Timer.builder("database.query")
    .register(registry);

timer.record(() -> {
    // database operation
});

// Or with Sample
Timer.Sample sample = Timer.start(registry);
// ... perform operation
sample.stop(Timer.builder("api.latency").register(registry));
```

### DistributionSummary - Non-Time Distributions

```java
DistributionSummary summary = DistributionSummary.builder("request.size")
    .baseUnit("bytes")
    .register(registry);

summary.record(fileSize);
```

See [references/meter-types-reference.md](references/meter-types-reference.md) for comprehensive meter type guide and decision trees.

## Tags and Cardinality

### Safe Tags (Bounded, Low Cardinality)

```java
// ✅ HTTP method (4-10 values)
.tag("method", "GET")

// ✅ Status class (5 values)
.tag("status.class", "2xx")

// ✅ Environment (3-5 values)
.tag("env", "production")
```

### Dangerous Tags (Unbounded, High Cardinality)

```java
// ❌ User ID (millions of values) → Use tracing instead
.tag("user.id", userId)

// ❌ Request ID (infinite values) → Use tracing instead
.tag("request.id", requestId)

// ❌ Full URI with parameters → Normalize!
.tag("uri", "/api/charges?supplier=123&date=2025-01-01")
```

### Cardinality Limits

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
```

See [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) for comprehensive cardinality management.

## Common Patterns

### Service Metrics

```java
@Service
public class OrderService {

    private final Counter ordersCreated;
    private final Timer orderLookup;

    public OrderService(MeterRegistry registry) {
        this.ordersCreated = Counter.builder("order.created")
            .description("Orders created")
            .register(registry);

        this.orderLookup = Timer.builder("order.lookup.duration")
            .description("Time to lookup order")
            .register(registry);
    }

    public Order createOrder(OrderRequest request) {
        Timer.Sample sample = Timer.start();
        try {
            Order order = new Order(request);
            ordersCreated.increment();
            return order;
        } finally {
            sample.stop(orderLookup);
        }
    }
}
```

### @Timed Annotation

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

### Common Tags Organization-Wide

```java
@Configuration
public class MetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> commonTags(
            @Value("${spring.application.name}") String appName,
            @Value("${environment}") String environment) {

        return registry -> registry.config()
            .commonTags(
                "application", appName,
                "environment", environment,
                "region", "europe-west2"
            );
    }
}
```

## Supporting Files

| File | Purpose |
|------|---------|
| [references/meter-types-reference.md](references/meter-types-reference.md) | Comprehensive meter types guide with decision trees |

## Requirements

- Spring Boot 2.2+ (Micrometer included)
- Micrometer core library (auto-included with Actuator)
- JVM application with Spring Boot
- Monitoring system backend (Prometheus, Cloud Monitoring)

**Dependencies:**
```gradle
implementation("org.springframework.boot:spring-boot-starter-actuator")
implementation("io.micrometer:micrometer-registry-prometheus")  // Choose backend
```

## See Also

- **[python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md)** - High cardinality prevention
- **[python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md)** - Business KPIs
- **[python-micrometer-gcp-cloud-monitoring](../python-micrometer-gcp-cloud-monitoring/SKILL.md)** - GCP export
- **[python-micrometer-metrics-setup](../python-micrometer-metrics-setup/SKILL.md)** - Initial setup
