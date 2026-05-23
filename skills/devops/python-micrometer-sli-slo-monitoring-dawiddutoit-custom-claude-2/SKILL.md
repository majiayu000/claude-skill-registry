---
name: python-micrometer-sli-slo-monitoring
description: |
  Define and monitor Service Level Indicators (SLIs) and Service Level Objectives (SLOs) using Micrometer histograms.
  Use when implementing availability and latency SLOs, creating SLO-aligned histogram buckets,
  monitoring error budgets, or validating compliance with defined service levels.
  Essential for reliability engineering and production SLO monitoring in microservices.
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
---

# Micrometer SLI/SLO Monitoring

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

Service Level Objectives (SLOs) define reliability targets (e.g., 99.9% availability, P95 latency < 500ms). Service Level Indicators (SLIs) measure whether SLOs are met. Micrometer's histogram buckets (Service Level Objectives in Micrometer) allow you to define thresholds aligned with business SLOs, enabling automatic error budget calculations and SLO compliance tracking.

## When to Use

Use this skill when you need to:

- **Define SLOs for services** - Set reliability targets (availability, latency, throughput) based on business requirements
- **Implement SLI measurement** - Configure metrics to track whether SLOs are being met
- **Create SLO-aligned histogram buckets** - Define buckets at SLO thresholds (e.g., 500ms for latency)
- **Monitor error budgets** - Track remaining error budget before SLO violation
- **Set up SLO-based alerting** - Alert when approaching or violating SLO thresholds
- **Calculate SLO compliance** - Query metrics to determine percentage of requests meeting SLO
- **Implement multi-tier SLOs** - Different reliability targets for different endpoints (P1/P2/P3)
- **Track burn rate** - Detect when error budget is consumed too quickly

**When NOT to use:**
- Before defining business SLOs (work with product/business teams first)
- For purely technical metrics without SLO targets (use `python-micrometer-core` instead)
- When Micrometer isn't set up (use `python-micrometer-metrics-setup` first)
- For high-cardinality metrics (use `python-python-micrometer-cardinality-control` to prevent metric explosion)

---

## Quick Start

Define SLOs as histogram buckets in configuration:

```yaml
management:
  metrics:
    distribution:
      # Histogram buckets aligned with business SLOs
      slo:
        http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s,2s,5s

      # Enable histogram export
      percentiles-histogram:
        http.server.requests: true
```

Then query SLO compliance in Prometheus/Stackdriver:

```promql
# Availability SLI: % requests without errors (non-5xx)
sum(rate(http_server_requests_seconds_count{status!~"5.."}[5m]))
/
sum(rate(http_server_requests_seconds_count[5m]))
* 100

# Latency SLI: % requests faster than 500ms SLO
sum(rate(http_server_requests_seconds_bucket{le="0.5"}[5m]))
/
sum(rate(http_server_requests_seconds_count[5m]))
* 100
```

## Instructions

### Step 1: Define Business SLOs

Start by identifying meaningful SLOs for your service:

**Typical SLO Categories:**

1. **Availability SLO**
   - Goal: 99.9% of requests succeed (no 5xx errors)
   - Period: 30 days rolling window
   - Error Budget: 0.1% errors = ~43 minutes downtime/month

2. **Latency SLO**
   - Goal: 95% of requests complete within 500ms
   - Measurement: p95 latency
   - SLI: percentage of requests faster than threshold

3. **Throughput SLO**
   - Goal: Handle 1000 requests/second peak
   - Measurement: request rate
   - SLI: achieved RPS vs. target

**Example SLOs for Supplier Charges API:**

```
Service: supplier-charges-api

Availability SLO:
  Target: 99.9%
  Window: 30 days
  Error Budget: 43 minutes/month
  SLI: (successful_requests / total_requests) >= 0.999

Latency SLO:
  Target: p95 < 500ms, p99 < 1s
  Window: 30 days
  SLI: percentage of requests meeting threshold >= 95%

Charge Processing SLO:
  Target: 99% of charges approved within 5 minutes
  Window: 7 days
  SLI: (charges_approved_within_5m / total_charges) >= 0.99
```

### Step 2: Configure SLO Histogram Buckets

Map SLO thresholds to histogram buckets in Micrometer:

```yaml
# application.yml
management:
  metrics:
    distribution:
      # Define buckets matching your SLOs
      slo:
        # HTTP request latencies: include SLO thresholds
        http.server.requests: |
          10ms,50ms,100ms,200ms,500ms,1s,2s,5s

        # Client request latencies
        http.client.requests: |
          100ms,500ms,1s,5s

        # Custom business metrics (milliseconds)
        charge.approval.duration: |
          1000,5000,10000,30000,60000

        # Invoice generation time
        invoice.generation.duration: |
          100,500,1000,5000,10000

      # Enable histogram export (required for Prometheus/Stackdriver)
      percentiles-histogram:
        http.server.requests: true
        http.client.requests: true
        charge.approval.duration: true
        invoice.generation.duration: true
```

**Bucket Strategy:**
- Include SLO threshold (500ms for availability)
- Add boundaries above and below for tail analysis
- Keep 5-10 buckets (too many = cardinality explosion)
- Use powers of 2 or multiples for readability

```java
// Alternative: programmatic configuration
@Configuration
public class SLOMetricsConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> sloHistograms() {
        return registry -> {
            registry.config().meterFilter(
                new MeterFilter() {
                    @Override
                    public DistributionStatisticConfig configure(
                            Meter.Id id,
                            DistributionStatisticConfig config) {

                        // HTTP request SLOs
                        if (id.getName().equals("http.server.requests")) {
                            return DistributionStatisticConfig.builder()
                                .percentilesHistogram(true)
                                .serviceLevelObjectives(
                                    Duration.ofMillis(10).toNanos(),
                                    Duration.ofMillis(50).toNanos(),
                                    Duration.ofMillis(100).toNanos(),
                                    Duration.ofMillis(200).toNanos(),
                                    Duration.ofMillis(500).toNanos(),  // SLO threshold
                                    Duration.ofSeconds(1).toNanos(),
                                    Duration.ofSeconds(2).toNanos(),
                                    Duration.ofSeconds(5).toNanos()
                                )
                                .build()
                                .merge(config);
                        }

                        // Charge approval SLOs (5 minute target)
                        if (id.getName().equals("charge.approval.duration")) {
                            return DistributionStatisticConfig.builder()
                                .percentilesHistogram(true)
                                .serviceLevelObjectives(
                                    Duration.ofSeconds(10).toNanos(),
                                    Duration.ofSeconds(60).toNanos(),
                                    Duration.ofMinutes(5).toNanos(),     // SLO threshold
                                    Duration.ofMinutes(10).toNanos()
                                )
                                .build()
                                .merge(config);
                        }

                        return config;
                    }
                }
            );
        };
    }
}
```

### Step 3: Implement SLI Calculation Queries

Create monitoring queries to measure SLI compliance:

**Prometheus Queries:**

```promql
# === AVAILABILITY SLI ===
# Goal: 99.9% success rate (non-5xx responses)

# Current availability (5-minute window)
(
  sum(rate(http_server_requests_seconds_count{status!~"5.."}[5m]))
  /
  sum(rate(http_server_requests_seconds_count[5m]))
) * 100

# 30-day rolling availability (error budget)
(
  sum(rate(http_server_requests_seconds_count{status!~"5.."}[30d]))
  /
  sum(rate(http_server_requests_seconds_count[30d]))
) * 100

# Remaining error budget (if SLO is 99.9%)
(
  (
    sum(rate(http_server_requests_seconds_count{status!~"5.."}[30d]))
    /
    sum(rate(http_server_requests_seconds_count[30d]))
  ) - 0.999
) * 100

# === LATENCY SLI ===
# Goal: 95% of requests faster than 500ms

# P95 latency
histogram_quantile(0.95, sum(rate(http_server_requests_seconds_bucket[5m])) by (le))

# Percentage of requests meeting SLO (faster than 500ms)
(
  sum(rate(http_server_requests_seconds_bucket{le="0.5"}[5m]))
  /
  sum(rate(http_server_requests_seconds_count[5m]))
) * 100

# === CHARGE PROCESSING SLI ===
# Goal: 99% approved within 5 minutes

# Percentage meeting SLO
(
  sum(rate(charge_approval_duration_seconds_bucket{le="300"}[7d]))
  /
  sum(rate(charge_approval_duration_seconds_count[7d]))
) * 100

# === ERROR RATE SLI ===
# Goal: < 1% error rate

(
  sum(rate(http_server_requests_seconds_count{status=~"5.."}[5m]))
  /
  sum(rate(http_server_requests_seconds_count[5m]))
) * 100
```

**Cloud Monitoring Queries (GCP):**

```
# Availability SLI
fetch k8s_container
| metric 'custom.googleapis.com/http/server/requests'
| filter metric.status != '5*'
| group_by 1m, [value_rate: rate(value.requests)]
| every 1m
| value [sli: mean(value_rate)]

# Latency SLI (p95 < 500ms)
fetch k8s_container
| metric 'custom.googleapis.com/http/server/requests'
| group_by 1m, [value_percentile_95: percentile_cont(value.latency, 0.95)]
| condition value_percentile_95 < 500 'ms'
| ratio_by_bucket(bucket.latency)
```

### Step 4: Set Up SLO Alerting

Create alerts when SLOs are at risk:

**Prometheus AlertManager:**

```yaml
# alerting-rules.yml
groups:
  - name: slo_alerts
    interval: 30s
    rules:
      # Alert: Availability SLO at risk
      - alert: AvailabilitySLOAtRisk
        expr: |
          (
            sum(rate(http_server_requests_seconds_count{status!~"5.."}[5m]))
            /
            sum(rate(http_server_requests_seconds_count[5m]))
          ) < 0.999
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Availability SLO violated ({{ $value | humanizePercentage }})"
          dashboard: "https://grafana.example.com/d/slo"

      # Alert: Latency SLO at risk
      - alert: LatencySLOAtRisk
        expr: |
          histogram_quantile(0.95, sum(rate(http_server_requests_seconds_bucket[5m])) by (le)) > 0.5
        for: 10m
        labels:
          severity: warning
          slo: latency
        annotations:
          summary: "P95 latency exceeds 500ms SLO"
          value: "{{ $value }}s"

      # Alert: Error budget exceeded
      - alert: ErrorBudgetExhausted
        expr: |
          (
            sum(rate(http_server_requests_seconds_count{status=~"5.."}[30d]))
            /
            sum(rate(http_server_requests_seconds_count[30d]))
          ) > 0.001  # > 0.1% error rate
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Error budget consumed ({{ $value | humanizePercentage }})"
```

**GCP Cloud Monitoring:**

```yaml
# Terraform: SLO alert policy
resource "google_monitoring_alert_policy" "availability_slo" {
  display_name = "Supplier Charges - Availability SLO"
  combiner     = "OR"

  conditions {
    display_name = "Availability < 99.9%"

    condition_threshold {
      filter = <<-EOT
        resource.type = "k8s_container"
        AND metric.type = "custom.googleapis.com/http/server/requests"
        AND metric.response_code_class != "5xx"
      EOT

      comparison      = "COMPARISON_LT"
      threshold_value = 0.999
      duration        = "300s"

      aggregations {
        alignment_period   = "60s"
        per_series_aligner = "ALIGN_RATE"
      }
    }
  }

  notification_channels = [google_monitoring_notification_channel.pagerduty.id]
}
```

### Step 5: Calculate and Track Error Budget

Monitor remaining error budget throughout the measurement window:

```java
@Component
public class ErrorBudgetMonitor {

    private final MeterRegistry registry;
    private final Logger log = LoggerFactory.getLogger(this.getClass());

    // SLO thresholds
    private static final double AVAILABILITY_SLO = 0.999;  // 99.9%
    private static final int MEASUREMENT_WINDOW_DAYS = 30;

    @Scheduled(fixedRate = 60_000) // Every minute
    public void monitorErrorBudget() {
        // In real implementation, fetch from Prometheus/Cloud Monitoring
        // This is pseudo-code showing the concept

        double currentAvailability = getCurrentAvailability();
        double errorBudgetRemaining = calculateErrorBudgetRemaining(currentAvailability);

        Gauge.builder("slo.error.budget.remaining",
                      () -> errorBudgetRemaining)
             .description("Error budget remaining for availability SLO")
             .register(registry);

        if (errorBudgetRemaining < 0.002) { // Less than 0.2% remaining
            log.warn("ERROR_BUDGET_LOW: Only {:.2f}% error budget remaining",
                     errorBudgetRemaining * 100);
        }

        if (errorBudgetRemaining < 0) {
            log.error("ERROR_BUDGET_EXCEEDED: SLO violation in progress");
        }
    }

    private double calculateErrorBudgetRemaining(double currentAvailability) {
        // Error budget = (SLO - current availability) / (1 - SLO)
        // Example: SLO 99.9%, current 99.8%
        // Remaining = (0.999 - 0.998) / (1 - 0.999) = 10% of budget
        return (currentAvailability - AVAILABILITY_SLO) / (1 - AVAILABILITY_SLO);
    }

    private double getCurrentAvailability() {
        // Would fetch from actual metrics in production
        return 0.9989; // Example: 99.89%
    }
}
```

### Step 6: Create SLO Dashboard

Visualize SLI metrics and error budget:

```json
{
  "dashboard": {
    "title": "Supplier Charges - SLO Dashboard",
    "panels": [
      {
        "title": "Availability SLI (30-day rolling)",
        "targets": [
          {
            "expr": "sum(rate(http_server_requests_seconds_count{status!~\"5..\"}[30d])) / sum(rate(http_server_requests_seconds_count[30d])) * 100"
          }
        ],
        "thresholds": [
          { "value": 99.9, "color": "green", "op": "gt" },
          { "value": 99.0, "color": "yellow", "op": "gt" },
          { "value": 99.0, "color": "red", "op": "lt" }
        ]
      },
      {
        "title": "Latency SLI (% requests < 500ms)",
        "targets": [
          {
            "expr": "sum(rate(http_server_requests_seconds_bucket{le=\"0.5\"}[5m])) / sum(rate(http_server_requests_seconds_count[5m])) * 100"
          }
        ],
        "thresholds": [
          { "value": 95, "color": "green", "op": "gt" },
          { "value": 90, "color": "yellow", "op": "gt" },
          { "value": 90, "color": "red", "op": "lt" }
        ]
      },
      {
        "title": "Error Budget Remaining",
        "targets": [
          {
            "expr": "(sum(rate(http_server_requests_seconds_count{status!~\"5..\"}[30d])) / sum(rate(http_server_requests_seconds_count[30d])) - 0.999) / (1 - 0.999) * 100"
          }
        ],
        "gauge": true,
        "thresholds": [
          { "value": 0, "color": "red" },
          { "value": 50, "color": "yellow" },
          { "value": 100, "color": "green" }
        ]
      }
    ]
  }
}
```

## Examples

### Example 1: Multi-Tier SLO Configuration

```java
@Configuration
public class MultiTierSLOConfig {

    @Bean
    public MeterRegistryCustomizer<MeterRegistry> sloForAllEndpoints() {
        return registry -> {
            // P1 endpoints (critical): strict SLO
            configureP1SLO(registry);

            // P2 endpoints (important): moderate SLO
            configureP2SLO(registry);

            // P3 endpoints (nice-to-have): relaxed SLO
            configureP3SLO(registry);
        };
    }

    private void configureP1SLO(MeterRegistry registry) {
        // P1: charge processing endpoints (99.9% availability, p95 < 500ms)
        registry.config().meterFilter(
            MeterFilter.maximumAllowableTags(
                "http.server.requests",
                "uri",
                10, // Limit P1 URIs to track
                MeterFilter.deny()
            )
        );
    }

    private void configureP2SLO(MeterRegistry registry) {
        // P2: supplier management endpoints (99% availability, p95 < 1s)
        // Standard configuration
    }

    private void configureP3SLO(MeterRegistry registry) {
        // P3: admin endpoints (95% availability, p95 < 5s)
        // Less strict monitoring
    }
}
```

### Example 2: SLO Burn Rate Detection

Alert when error budget is consumed too quickly:

```java
@Component
public class SLOBurnRateMonitor {

    private final MeterRegistry registry;
    private double previousAvailability = 1.0;
    private long previousMeasurementTime = System.currentTimeMillis();

    @Scheduled(fixedRate = 300_000) // Every 5 minutes
    public void detectHighBurnRate() {
        double currentAvailability = getCurrentAvailability();
        long currentTime = System.currentTimeMillis();

        double timeDeltaHours = (currentTime - previousMeasurementTime) / (1000.0 * 60 * 60);

        // Calculate availability drop rate (percentage points per hour)
        double dropPerHour = (previousAvailability - currentAvailability) / timeDeltaHours;

        // If losing > 0.01% per hour, alert
        if (dropPerHour > 0.0001) {
            log.error("HIGH_BURN_RATE: Losing {:.4f}% availability per hour",
                      dropPerHour * 100);
        }

        previousAvailability = currentAvailability;
        previousMeasurementTime = currentTime;
    }

    private double getCurrentAvailability() {
        // Fetch from actual metrics
        return 0.9989;
    }
}
```

## Requirements

- Spring Boot 2.1+ with Actuator
- Micrometer core
- Prometheus or GCP Cloud Monitoring for query execution
- Grafana (optional, for SLO dashboard visualization)
- Java 11+

## Anti-Patterns to Avoid

```yaml
# ❌ Wrong: SLO buckets too coarse
slo:
  http.server.requests: 1s,10s

# ✅ Right: SLO buckets fine-grained around threshold
slo:
  http.server.requests: 10ms,50ms,100ms,200ms,500ms,1s,2s,5s

# ❌ Wrong: Forgetting percentiles-histogram
slo:
  http.server.requests: 500ms,1s

# ✅ Right: Enable histogram export
percentiles-histogram:
  http.server.requests: true

# ❌ Wrong: SLO thresholds without business context
slo:
  http.server.requests: 1ms,10ms,100ms,1s

# ✅ Right: SLO thresholds tied to business requirements
slo:
  http.server.requests: 500ms  # What users actually expect
  charge.approval.duration: 300s  # 5 minute business SLO

# ❌ Wrong: Single SLO for all operations
slo:
  http.server.requests: 500ms

# ✅ Right: Different SLOs per operation tier
slo:
  http.server.requests: 500ms    # P1: charge operations
  supplier.lookup: 2s            # P2: supplier lookups
  admin.report.generation: 30s   # P3: batch operations
```

## See Also

- [python-micrometer-cardinality-control](../python-micrometer-cardinality-control/SKILL.md) - Manage metric cardinality
- [python-micrometer-gcp-cloud-monitoring](../python-micrometer-gcp-cloud-monitoring/SKILL.md) - Export metrics to GCP
- [python-micrometer-business-metrics](../python-micrometer-business-metrics/SKILL.md) - Create business metrics
