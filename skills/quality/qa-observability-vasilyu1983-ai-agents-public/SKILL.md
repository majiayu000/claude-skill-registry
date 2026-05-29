---
name: qa-observability
description: "Observability for quality engineering: using logs, metrics, and traces as test signals; SLI/SLO quality gates; trace-based debugging of failures; and cost-aware instrumentation with OpenTelemetry."
---

# QA Observability & Performance Engineering (Dec 2025)

This skill provides execution-ready patterns for building observable, performant systems and using telemetry as part of QA workflows.

Core references: OpenTelemetry ([Docs](https://opentelemetry.io/docs/)) and W3C Trace Context ([Spec](https://www.w3.org/TR/trace-context/)) for correlation; SLO/error budget guidance from the Google SRE Book ([Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)).

---

## When to Use This Skill

Claude should invoke this skill when a user requests:

- OpenTelemetry instrumentation and setup
- Distributed tracing implementation (Jaeger, Tempo, Zipkin)
- Metrics collection and dashboarding (Prometheus, Grafana)
- Structured logging setup (Pino, Winston, structlog)
- SLO/SLI definition and error budgets
- Performance profiling and optimization
- Capacity planning and resource forecasting
- APM integration (Datadog, New Relic, Dynatrace)
- Observability maturity assessment
- Alert design and on-call runbooks
- Performance budgeting (frontend and backend)
- Cost-performance optimization
- Production performance debugging

---

## Core QA (Default)

### What “Observability for QA” Means

- Treat telemetry as a first-class test oracle and debugging substrate, not an ops-only concern.
- Make every failure diagnosable by default: logs + metrics + traces with correlation IDs ([OpenTelemetry](https://opentelemetry.io/docs/), [W3C Trace Context](https://www.w3.org/TR/trace-context/)).

### QA Signals (Use in CI and in Prod)

- Logs: structured, redacted, correlated with request/trace IDs (avoid PII).
- Metrics: SLIs for latency, availability, error rate, saturation; track tail latency (p95/p99).
- Traces: end-to-end request paths; use traces to localize failures across services.

### Synthetic vs RUM (How QA Uses Both)

- Synthetic monitoring: deterministic probes that validate availability and critical flows from the outside.
- RUM (real user monitoring): validates real-world performance and regressions; use as a feedback loop for test coverage and performance budgets.

### SLIs/SLOs as Quality Gates

- Use SLOs and error budgets to set reliability expectations and release gates ([Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)).
- Example release gates [Inference]:
  - Block deploy when error budget burn is above policy (fast + slow windows).
  - Block deploy on sustained p99 regression beyond a defined budget.

### Trace-Based Debugging for Test Failures

- Every integration/E2E test should emit a correlation ID and capture a trace link on failure.
- Prefer “find the failing span” over grepping logs; use logs to enrich the span narrative.

### CI Economics (Telemetry Cost Control)

- Sampling is a quality lever: keep 100% for errors, sample successes as needed [Inference].
- Keep dashboards high-signal; alert on symptoms (SLO burn) not raw resource metrics.

### Do / Avoid

Do:
- Define an “observability readiness” bar before E2E and chaos tests.
- Make test tooling attach IDs (request/trace) to failures for fast triage.

Avoid:
- Logging secrets/PII or writing dashboards with no owners.
- Alerting on “everything”; alert fatigue is a quality failure mode.

## Quick Reference

| Task | Tool/Framework | Command/Setup | When to Use |
|------|----------------|---------------|-------------|
| Distributed tracing | OpenTelemetry + Jaeger | Auto-instrumentation, manual spans | Microservices, debugging request flow |
| Metrics collection | Prometheus + Grafana | Expose /metrics endpoint, scrape config | Track latency, error rate, throughput |
| Structured logging | Pino (Node.js), structlog (Python) | JSON logs with trace ID | Production debugging, log aggregation |
| SLO/SLI definition | Prometheus queries, SLO YAML | Availability, latency, error rate SLIs | Reliability targets, error budgets |
| Performance profiling | Clinic.js, Chrome DevTools, cProfile | CPU/memory flamegraphs | Slow application, high resource usage |
| Load testing | k6, Artillery | Ramp-up, spike, soak tests | Capacity planning, performance validation |
| APM integration | Datadog, New Relic, Dynatrace | Agent installation, instrumentation | Full observability stack |
| Web performance | Lighthouse CI, Web Vitals | Performance budgets in CI/CD | Frontend optimization |

---

## Decision Tree: Observability Strategy

```text
User needs: [Observability Task Type]
    ├─ Starting New Service?
    │   ├─ Microservices? → OpenTelemetry auto-instrumentation + Jaeger
    │   ├─ Monolith? → Structured logging (Pino/structlog) + Prometheus
    │   ├─ Frontend? → Web Vitals + performance budgets
    │   └─ All services? → Full stack (logs + metrics + traces)
    │
    ├─ Debugging Issues?
    │   ├─ Distributed system? → Distributed tracing (search by trace ID)
    │   ├─ Single service? → Structured logs (search by request ID)
    │   ├─ Performance problem? → CPU/memory profiling
    │   └─ Database slow? → Query profiling (EXPLAIN ANALYZE)
    │
    ├─ Reliability Targets?
    │   ├─ Define SLOs? → Availability, latency, error rate SLIs
    │   ├─ Error budgets? → Calculate allowed downtime per SLO
    │   ├─ Alerting? → Burn rate alerts (fast: 1h, slow: 6h)
    │   └─ Dashboard? → Grafana SLO dashboard with error budget
    │
    ├─ Performance Optimization?
    │   ├─ Find bottlenecks? → CPU/memory profiling
    │   ├─ Database queries? → EXPLAIN ANALYZE, indexing
    │   ├─ Frontend slow? → Lighthouse, Web Vitals analysis
    │   └─ Load testing? → k6 scenarios (ramp, spike, soak)
    │
    └─ Capacity Planning?
        ├─ Baseline metrics? → Collect 30 days of traffic data
        ├─ Load testing? → Test at 2x expected peak
        ├─ Forecasting? → Time series analysis (Prophet, ARIMA)
        └─ Cost optimization? → Right-size instances, spot instances
```

---

## Navigation: Core Implementation Patterns

See [resources/core-observability-patterns.md](resources/core-observability-patterns.md) for detailed implementation guides:

- **OpenTelemetry End-to-End Setup** - Complete instrumentation with Node.js/Python examples
  - Three pillars of observability (logs, metrics, traces)
  - Auto-instrumentation and manual spans
  - OTLP exporters and collectors
  - Production checklist

- **Distributed Tracing Strategy** - Service-to-service trace propagation
  - W3C Trace Context standard
  - Sampling strategies (always-on, probabilistic, parent-based, adaptive)
  - Cross-service correlation
  - Trace backend configuration

- **SLO/SLI Design & Error Budgets** - Reliability targets and alerting
  - SLI definitions (availability, latency, error rate)
  - Prometheus queries for SLIs
  - Error budget calculation and policies
  - Burn rate alerts (fast: 1h, slow: 6h)

- **Structured Logging** - Production-ready JSON logs
  - Log format with trace correlation
  - Pino (Node.js) and structlog (Python) setup
  - Log levels and what NOT to log
  - Centralized aggregation (ELK, Loki, Datadog)

- **Performance Profiling** - CPU, memory, database, frontend optimization
  - Node.js profiling (Chrome DevTools, Clinic.js)
  - Memory leak detection (heap snapshots)
  - Database query profiling (EXPLAIN ANALYZE)
  - Web Vitals and performance budgets

- **Capacity Planning** - Scale planning and cost optimization
  - Capacity formula and calculations
  - Load testing with k6
  - Resource forecasting (Prophet, ARIMA)
  - Cost per request optimization

---

## Navigation: Observability Maturity

See [resources/observability-maturity-model.md](resources/observability-maturity-model.md) for maturity assessment:

- **Level 1: Reactive (Firefighting)** - Manual log grepping, hours to resolve
  - Basic logging to files
  - No structured logging or distributed tracing
  - Progression: Centralize logs, add metrics

- **Level 2: Proactive (Monitoring)** - Centralized logs, application alerts
  - Structured JSON logs with ELK/Splunk
  - Prometheus metrics and Grafana dashboards
  - Progression: Add distributed tracing, define SLOs

- **Level 3: Predictive (Observability)** - Unified telemetry, SLO-driven
  - Distributed tracing (Jaeger, Tempo)
  - Automatic trace-log-metric correlation
  - SLO/SLI-based alerting with error budgets
  - Progression: automated anomaly detection, automated remediation

- **Level 4: Automated Operations** - Automation-driven, self-healing systems
  - Automated anomaly detection and assisted root cause analysis
  - Automated remediation with safe guards (feature flags, circuit breakers, rollbacks)
  - Continuous optimization (performance budgets, capacity tuning)
  - Chaos engineering for resilience (right-sized blast radius)

**Maturity Assessment Tool** - Rate your organization (0-5 per category):

- Logging, metrics, tracing, alerting, incident response
- MTTR/MTTD benchmarks by level
- Recommended next steps

---

## Navigation: Anti-Patterns & Best Practices

See [resources/anti-patterns-best-practices.md](resources/anti-patterns-best-practices.md) for common mistakes:

**Critical Anti-Patterns:**

1. **Logging Everything** - Log bloat and high costs
2. **No Sampling** - 100% trace collection is expensive
3. **Alert Fatigue** - Too many noisy alerts
4. **Ignoring Tail Latency** - P99 matters more than average
5. **No Error Budgets** - Teams move too slow or too fast
6. **Metrics Without Context** - Dashboard mysteries
7. **No Cost Tracking** - Observability can cost 20% of infrastructure
8. **Point-in-Time Profiling** - Missing intermittent issues

**Best Practices Summary:**

- Sample traces intelligently (100% errors, 1-10% success)
- Alert on SLO burn rate, not infrastructure metrics
- Track tail latency (P99, P999), not just averages
- Use error budgets to balance velocity vs reliability
- Add context to dashboards (baselines, annotations, SLOs)
- Track observability costs, optimize aggressively
- Continuous profiling for intermittent issues

---

## Templates

See [templates/](templates/) for copy-paste ready examples organized by domain and tech stack:

**QA Checklists:**

- [Observability Readiness Checklist](templates/checklists/template-observability-readiness-checklist.md) - Logs/metrics/traces readiness for QA and fast debugging

**OpenTelemetry Instrumentation:**

- [Node.js/Express Setup](templates/opentelemetry/nodejs/opentelemetry-nodejs-setup.md) - Auto-instrumentation, manual spans, Docker, K8s
- [Python/Flask Setup](templates/opentelemetry/python/opentelemetry-python-setup.md) - Flask instrumentation, SQLAlchemy, deployment

**Monitoring & SLO:**

- [SLO YAML Template](templates/monitoring/slo/slo-definition.yaml) - Complete SLO definitions with error budgets
- [Prometheus Alert Rules](templates/monitoring/slo/prometheus-alert-rules.yaml) - Burn rate alerts, multi-window monitoring
- [SLO Dashboard](templates/monitoring/grafana/grafana-dashboard-slo.json) - SLI tracking, error budget visualization
- [Unified Observability Dashboard](templates/monitoring/grafana/template-grafana-dashboard-observability.json) - Logs, metrics, traces in one view

**Load Testing:**

- [k6 Load Test Template](templates/load-testing/load-testing-k6.js) - Ramp-up, spike, soak test scenarios
- [Artillery Load Test](templates/load-testing/template-load-test-artillery.yaml) - YAML configuration, multiple scenarios

**Performance Optimization:**

- [Lighthouse CI Configuration](templates/performance/frontend/template-lighthouse-ci.json) - Performance budgets, CI/CD integration
- [Node.js Profiling Config](templates/performance/backend/template-nodejs-profiling-config.js) - CPU/memory profiling, leak detection

---

## Resources

See [resources/](resources/) for deep-dive operational guides:

- [Core Observability Patterns](resources/core-observability-patterns.md) - 6 implementation patterns with code examples
- [Observability Maturity Model](resources/observability-maturity-model.md) - 4-level maturity framework with assessment
- [Anti-Patterns & Best Practices](resources/anti-patterns-best-practices.md) - 8 critical anti-patterns with solutions
- [OpenTelemetry Best Practices](resources/opentelemetry-best-practices.md) - Setup, sampling, attributes, context propagation
- [Distributed Tracing Patterns](resources/distributed-tracing-patterns.md) - Trace propagation, span design, debugging workflows
- [SLO Design Guide](resources/slo-design-guide.md) - SLI/SLO/SLA, error budgets, burn rate alerts
- [Performance Profiling Guide](resources/performance-profiling-guide.md) - CPU/memory profiling, database optimization, frontend performance

---

## Optional: AI / Automation

Use AI assistance to reduce toil, not to replace the fundamentals of instrumentation, SLOs, and debugging.

Do:
- Cluster similar alerts/incidents and propose likely suspects; verify via traces/logs/metrics.
- Summarize incident timelines from telemetry to speed up postmortems.

Avoid:
- “Black box” anomaly detection without explainability and a rollback plan.
- Auto-remediation without guardrails and human review for high-severity actions.

---

## External Resources

See [data/sources.json](data/sources.json) for curated sources:

- OpenTelemetry documentation and specifications
- APM platforms (Datadog, New Relic, Dynatrace, Honeycomb)
- Observability tools (Prometheus, Grafana, Jaeger, Tempo, Loki)
- SRE books (Google SRE, Site Reliability Workbook)
- Performance tooling (Lighthouse, k6, Clinic.js)
- Web Vitals and Core Web Vitals

---

## Related Skills

**DevOps & Infrastructure:**

- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) - Kubernetes, Docker, CI/CD pipelines
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) - Database performance and optimization

**Backend Development:**

- [../software-backend/SKILL.md](../software-backend/SKILL.md) - Backend architecture and API design
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) - System design patterns

**Quality & Reliability:**

- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) - Circuit breakers, retries, graceful degradation
- [../qa-debugging/SKILL.md](../qa-debugging/SKILL.md) - Production debugging techniques
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) - Testing strategies and automation

---

## Quick Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Starting new service | OpenTelemetry auto-instrumentation + structured logging |
| Debugging microservices | Distributed tracing with Jaeger/Tempo |
| Setting reliability targets | Define SLOs for availability, latency, error rate |
| Application is slow | CPU/memory profiling + database query analysis |
| Planning for scale | Load testing + capacity forecasting |
| High infrastructure costs | Cost per request analysis + right-sizing |
| Improving observability | Assess maturity level + 6-month roadmap |
| Frontend performance issues | Web Vitals monitoring + performance budgets |

---

## Usage Notes

**When to Apply Patterns:**

- New service setup → Start with OpenTelemetry + structured logging + basic metrics
- Microservices debugging → Use distributed tracing for full request visibility
- Reliability requirements → Define SLOs first, then implement monitoring
- Performance issues → Profile first, optimize second (measure before optimizing)
- Capacity planning → Collect baseline metrics for 30 days before load testing
- Observability maturity → Assess current level, plan 6-month progression

**Common Workflows:**

1. **New Service**: OpenTelemetry → Prometheus → Grafana → Define SLOs
2. **Debugging**: Search logs by trace ID → Click trace → See full request flow
3. **Performance**: Profile CPU/memory → Identify bottleneck → Optimize → Validate
4. **Capacity Planning**: Baseline metrics → Load test 2x peak → Forecast growth → Scale proactively

**Optimization Priorities:**

1. Correctness (logs, traces, metrics actually help debug)
2. Cost (optimize sampling, retention, cardinality)
3. Performance (observability overhead <5% latency)

---

> **Success Criteria:** Systems are fully observable with unified telemetry (logs+metrics+traces), SLOs drive alerting and feature velocity, performance is proactively optimized, and capacity is planned ahead of demand.
