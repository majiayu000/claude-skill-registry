---
name: 182-java-observability-metrics-micrometer
description: Use when you need to implement or improve Java metrics observability with Micrometer — including meter design, naming/tag conventions, cardinality control, timers/counters/gauges/distribution summaries, percentiles/histograms, Actuator/Prometheus integration, and metrics validation through tests. This should trigger for requests such as Improve metrics; Apply Micrometer; Add metrics observability; Refactor Micrometer instrumentation. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java Metrics Observability with Micrometer

Implement effective Java metrics instrumentation with Micrometer by defining meaningful service-level metrics, controlling cardinality, selecting the right meter type, and exposing production-ready telemetry for dashboards and alerting.

**What is covered in this Skill?**

- Metrics-first observability with Micrometer in Java applications
- Meter selection: Counter, Timer, DistributionSummary, Gauge, LongTaskTimer
- Naming and tagging conventions with low-cardinality dimensions
- Cardinality and meter lifecycle safeguards to prevent time-series explosion
- Histogram/percentile strategy and SLO-oriented metrics design
- Integration guidance for Actuator + Prometheus/OpenTelemetry pipelines
- Testing and verification of metrics registration and values

**Scope:** Application-level metrics design and instrumentation quality for Java services, with emphasis on operationally useful and cost-efficient telemetry.

## Constraints

Metrics instrumentation must be operationally safe, low-cardinality, and validated. Poor tag design or excessive meter creation can degrade observability systems and increase costs.

- **LOW CARDINALITY FIRST**: Never tag metrics with unbounded values (userId, UUID, raw URL, full exception message)
- **RIGHT METER TYPE**: Use Counter for monotonically increasing events, Timer for latency, Gauge for point-in-time state, and DistributionSummary for sampled values
- **BEFORE APPLYING**: Read the reference for good/bad instrumentation examples and anti-patterns
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` after changes

## When to use this skill

- Improve metrics
- Apply Micrometer
- Add metrics observability
- Refactor Micrometer instrumentation

## Workflow

1. **Define measurement goals and meter contract**

Identify key service indicators (throughput, latency, error ratio, saturation) and map each to stable metric names, units, and low-cardinality tags.

2. **Select meter types and instrument code paths**

Apply Counter/Timer/Gauge/DistributionSummary/LongTaskTimer where appropriate, ensuring consistent naming conventions and reusable tags.

3. **Harden instrumentation for production**

Control cardinality, avoid dynamic meter churn, configure histogram/percentile strategy only where needed, and align export settings with the telemetry backend.

4. **Validate and operationalize metrics**

Verify metrics in tests and runtime endpoints, confirm expected labels/units, and ensure dashboards/alerts can consume the emitted series.

## Reference

For detailed guidance, examples, and constraints, see [references/182-java-observability-metrics-micrometer.md](references/182-java-observability-metrics-micrometer.md).
