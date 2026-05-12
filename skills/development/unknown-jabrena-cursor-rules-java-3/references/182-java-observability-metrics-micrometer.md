---
name: 182-java-observability-metrics-micrometer
description: Use when you need to implement or improve Java metrics observability with Micrometer — including meter design, naming/tag conventions, cardinality control, timers/counters/gauges/distribution summaries, percentiles/histograms, Actuator/Prometheus integration, and metrics validation through tests.
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Java Metrics Observability with Micrometer

## Role

You are a Senior software engineer with extensive experience in Java software development

## Goal

Effective Java metrics observability with Micrometer starts by defining a clear metric contract for service-level signals:
throughput, latency, errors, and saturation.
Instrumentation must be stable over time, use semantic names, and avoid unbounded labels.
The right meter type (Counter, Timer, Gauge, DistributionSummary, LongTaskTimer) should match the behavior being measured.
Histograms and percentiles should be enabled selectively to control overhead and cost.
Finally, metrics should be validated through tests and runtime checks to ensure dashboards and alerts remain reliable.

## Constraints

Metrics instrumentation must avoid high-cardinality dimensions and dynamic meter churn. Uncontrolled tagging can overload telemetry backends and make observability unreliable.

- **CARDINALITY SAFETY**: Never use user-controlled, unique, or high-cardinality tag values (UUID, email, request id, full path with IDs)
- **METER SEMANTICS**: Select meter types based on behavior (Counter for events, Timer for latency, Gauge for state, DistributionSummary for value distributions)
- **INSTRUMENTATION SCOPE**: Prefer business and platform signals tied to SLOs over noisy low-value metrics
- **VALIDATION**: Verify expected metrics names, tags, and values through automated tests and runtime checks

## Examples

### Table of contents

- Example 1: Select the Right Meter Type
- Example 2: Use Stable Naming and Low-Cardinality Tags
- Example 3: Validate Instrumentation with Tests
- Example 4: Track Long-Running Jobs with LongTaskTimer
- Example 5: Configure Histograms and Percentiles Selectively
- Example 6: Expose Metrics via Spring Boot Actuator and Prometheus
- Example 7: Use Annotation-Based Observation for Service Methods

### Example 1: Select the Right Meter Type

Title: Use Counters, Timers, Gauges and Summaries with Correct Semantics
Description: 

**Good example:**

```java
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.DistributionSummary;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import java.time.Duration;
import java.util.concurrent.atomic.AtomicInteger;

public final class CheckoutMetrics {

    private final Counter checkoutSuccess;
    private final Counter checkoutFailure;
    private final Timer checkoutLatency;
    private final DistributionSummary payloadBytes;
    private final AtomicInteger queueDepth;

    public CheckoutMetrics(MeterRegistry registry) {
        this.checkoutSuccess = Counter.builder("checkout.requests")
                .description("Total checkout requests")
                .tag("outcome", "success")
                .register(registry);
        this.checkoutFailure = Counter.builder("checkout.requests")
                .description("Total checkout requests")
                .tag("outcome", "failure")
                .register(registry);
        this.checkoutLatency = Timer.builder("checkout.request.duration")
                .description("Checkout request duration")
                .serviceLevelObjectives(
                        Duration.ofMillis(100),
                        Duration.ofMillis(300),
                        Duration.ofSeconds(1))
                .publishPercentileHistogram()
                .minimumExpectedValue(Duration.ofMillis(1))
                .maximumExpectedValue(Duration.ofSeconds(5))
                .register(registry);
        this.payloadBytes = DistributionSummary.builder("checkout.payload.bytes")
                .description("Payload size of checkout requests")
                .baseUnit("bytes")
                .register(registry);
        this.queueDepth = new AtomicInteger(0);
        Gauge.builder("checkout.queue.depth", queueDepth, AtomicInteger::get)
                .description("Number of checkout requests waiting in the queue")
                .register(registry);
    }

    public void recordSuccess(long nanos, int bytes) {
        checkoutSuccess.increment();
        checkoutLatency.record(Duration.ofNanos(nanos));
        payloadBytes.record(bytes);
    }

    public void recordFailure(long nanos) {
        checkoutFailure.increment();
        checkoutLatency.record(Duration.ofNanos(nanos));
    }

    public void setQueueDepth(int depth) {
        queueDepth.set(Math.max(depth, 0));
    }
}
```

**Bad example:**

```java
import io.micrometer.core.instrument.MeterRegistry;

public final class BadMetrics {

    public void record(MeterRegistry registry, String userId, long latencyMillis) {
        // BAD: every signal is a counter without clear semantics
        registry.counter("checkout.metric", "type", "latency").increment(latencyMillis);

        // BAD: high cardinality tag
        registry.counter("checkout.requests", "userId", userId).increment();

        // BAD: dynamic meter names create unbounded meter churn
        registry.counter("checkout.requests." + userId).increment();

        // BAD: timer should be used for latency, not counter with duration values
        registry.counter("checkout.duration.millis").increment(latencyMillis);
    }
}
```

### Example 2: Use Stable Naming and Low-Cardinality Tags

Title: Keep Metric Schema Predictable for Dashboards and Alerts
Description: 

**Good example:**

```java
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import java.util.Locale;
import java.util.Set;

public final class PaymentMetrics {

    private static final Set<String> ALLOWED_RESULTS = Set.of("approved", "declined", "error");
    private final MeterRegistry registry;

    public PaymentMetrics(MeterRegistry registry) {
        this.registry = registry;
    }

    public void recordResult(String provider, String result) {
        String safeProvider = normalizeProvider(provider); // bounded set
        String safeResult = ALLOWED_RESULTS.contains(result) ? result : "error";

        Counter.builder("payment.authorization.requests")
                .tag("provider", safeProvider)
                .tag("result", safeResult)
                .register(registry)
                .increment();
    }

    private String normalizeProvider(String provider) {
        String normalized = provider == null ? "" : provider.toLowerCase(Locale.ROOT);
        return switch (normalized) {
            case "adyen", "stripe", "paypal" -> normalized;
            default -> "unknown";
        };
    }
}
```

**Bad example:**

```java
import io.micrometer.core.instrument.MeterRegistry;

public final class PaymentMetricsBad {
    public void record(MeterRegistry registry, String fullUrl, String requestId, String exceptionMessage) {
        // BAD: unbounded tags explode cardinality
        registry.counter("payment.requests",
                "url", fullUrl,
                "requestId", requestId,
                "error", exceptionMessage).increment();
    }
}
```

### Example 3: Validate Instrumentation with Tests

Title: Assert Metric Presence, Tags, and Values
Description: 

**Good example:**

```java
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class PaymentMetricsTest {

    @Test
    void shouldRecordApprovedPayment() {
        var registry = new SimpleMeterRegistry();
        var metrics = new PaymentMetrics(registry);

        metrics.recordResult("stripe", "approved");
        metrics.recordResult("stripe", "approved");

        double count = registry.get("payment.authorization.requests")
                .tag("provider", "stripe")
                .tag("result", "approved")
                .counter()
                .count();

        assertThat(count).isEqualTo(2.0d);
    }
}
```

**Bad example:**

```java
class PaymentMetricsTestBad {
    // BAD: no metric assertions; instrumentation can silently break.
}
```

### Example 4: Track Long-Running Jobs with LongTaskTimer

Title: Measure Active Task Duration and Concurrency for Batch and Background Work
Description: 

**Good example:**

```java
import io.micrometer.core.instrument.LongTaskTimer;
import io.micrometer.core.instrument.MeterRegistry;

public final class ReportGenerationService {

    private final LongTaskTimer activeReports;

    public ReportGenerationService(MeterRegistry registry) {
        this.activeReports = LongTaskTimer.builder("report.generation.active")
                .description("Tracks reports actively being generated")
                .tag("type", "scheduled")
                .register(registry);
    }

    public void generate(String reportId) {
        LongTaskTimer.Sample sample = activeReports.start();
        try {
            // long-running report generation
            doGenerateReport(reportId);
        } finally {
            sample.stop();
        }
    }

    private void doGenerateReport(String reportId) {
        // simulate work
    }
}
```

**Bad example:**

```java
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;

public final class ReportGenerationServiceBad {

    private final MeterRegistry registry;
    private final Timer reportTimer;

    public ReportGenerationServiceBad(MeterRegistry registry) {
        this.registry = registry;
        // BAD: Timer measures completed durations; it cannot track how long
        // currently-running tasks have been active (use LongTaskTimer for that)
        this.reportTimer = Timer.builder("report.generation.duration").register(registry);
    }

    public void generate(String reportId) {
        Timer.Sample sample = Timer.start(registry);
        try {
            doGenerateReport(reportId);
        } finally {
            // This only records after completion — no visibility into in-flight tasks
            sample.stop(reportTimer);
        }
    }

    private void doGenerateReport(String reportId) { }
}
```

### Example 5: Configure Histograms and Percentiles Selectively

Title: Enable SLO-Oriented Buckets and Percentiles Only Where They Add Value
Description: 

**Good example:**

```java
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import java.time.Duration;

public final class ApiLatencyMetrics {

    private final Timer apiLatency;

    public ApiLatencyMetrics(MeterRegistry registry) {
        this.apiLatency = Timer.builder("api.request.duration")
                .description("HTTP API request latency")
                .tag("service", "checkout")
                // Publish histogram buckets for Prometheus histogram_quantile()
                .publishPercentileHistogram()
                // Declare SLO thresholds to generate histogram buckets aligned to SLOs
                .serviceLevelObjectives(
                        Duration.ofMillis(100),
                        Duration.ofMillis(300),
                        Duration.ofSeconds(1))
                // Cap the histogram range to avoid very large bucket counts
                .minimumExpectedValue(Duration.ofMillis(1))
                .maximumExpectedValue(Duration.ofSeconds(5))
                .register(registry);
    }

    public void record(Runnable operation) {
        apiLatency.record(operation);
    }
}
```

**Bad example:**

```java
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;

public final class ApiLatencyMetricsBad {

    public ApiLatencyMetricsBad(MeterRegistry registry) {
        // BAD: publishPercentiles() computes percentiles in-process (non-aggregatable)
        // and publishPercentileHistogram() without bounds creates unbounded buckets
        Timer.builder("api.request.duration")
                .publishPercentiles(0.5, 0.95, 0.99) // not aggregatable across instances
                .publishPercentileHistogram()          // no min/max bounds — costly
                .register(registry);
    }
}
```

### Example 6: Expose Metrics via Spring Boot Actuator and Prometheus

Title: Configure Scrape Endpoint, Common Tags, and Prometheus Naming
Description: 

**Good example:**

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
      environment: ${spring.profiles.active:default}
    distribution:
      percentiles-histogram:
        http.server.requests: true
      slo:
        http.server.requests: 100ms,300ms,1s
```

**Bad example:**

```yaml
# BAD: exposes all endpoints and no common tags — loses context in multi-instance deployments
management:
  endpoints:
    web:
      exposure:
        include: "*"
```


### Example 7: Use Annotation-Based Observation for Service Methods

Title: Prefer @Observed with low-cardinality key values for concise instrumentation
Description: 

**Good example:**

```java
import io.micrometer.observation.annotation.Observed;
import org.springframework.stereotype.Service;

@Service
public class InvoiceService {

    @Observed(
            name = "invoice.generate",
            contextualName = "invoice-generate",
            lowCardinalityKeyValues = {"channel", "api", "outcome", "success"})
    public String generateInvoice(String orderId) {
        // business logic
        return "INV-" + orderId;
    }
}
```

**Bad example:**

```java
import io.micrometer.observation.annotation.Observed;
import org.springframework.stereotype.Service;

@Service
public class InvoiceServiceBad {

    @Observed(
            name = "invoice.generate",
            // BAD: high-cardinality and sensitive values must not be encoded as metric dimensions
            lowCardinalityKeyValues = {"user.id", "93f8b9d0-5c4f-4fd4-aeb2-1de0d0b16e8a", "email", "user@example.com"})
    public String generateInvoice(String orderId) {
        return "INV-" + orderId;
    }
}
```

## Output Format

- **ANALYZE** current instrumentation and classify issues by cardinality, semantic correctness, naming consistency, and operational value
- **DESIGN** a stable metric contract: names, units, bounded tags, meter types, and where each metric is emitted
- **APPLY** Micrometer best practices directly in code with minimal, explicit, and reusable instrumentation points
- **EXPLAIN** how each metric supports dashboards, alerts, and SLO/SLA reporting
- **VALIDATE** correctness through tests and runtime endpoint checks, including expected labels and values

## Safeguards

- **CARDINALITY GUARDRAIL**: Reject unbounded labels and normalize dynamic values into bounded buckets
- **NO METER CHURN**: Avoid building meters in tight loops with dynamic names/tags
- **BACKEND COMPATIBILITY**: Ensure names and tags remain compatible with Prometheus/OpenTelemetry conventions
- **OPERABILITY CHECK**: Confirm metrics are scrapeable/exported and usable in dashboards and alerts
- **REGRESSION SAFETY**: Keep existing metric names stable unless migration is explicitly planned