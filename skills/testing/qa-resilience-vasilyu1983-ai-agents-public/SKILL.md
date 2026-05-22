---
name: qa-resilience
description: "Use when designing or testing resilience for distributed systems: timeouts/deadlines, retries (backoff + jitter, retry budgets), circuit breakers, bulkheads, backpressure/load shedding, graceful degradation, health checks, chaos experiments/game days/DR drills, and SLO-based reliability gates."
---

# QA Resilience (Jan 2026) - Failure Mode Testing & Production Hardening

This skill provides execution-ready patterns for building resilient, fault-tolerant systems that handle failures gracefully, and for validating those behaviors with tests.

Core sources: Principles of Chaos Engineering (https://principlesofchaos.org/), AWS Well-Architected Reliability Pillar (https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html), and Kubernetes probes (https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/). For additional curated sources, see `data/sources.json`.

---

## Common Requests

Use this skill when a user requests:

- Circuit breaker implementation
- Retry strategies and exponential backoff
- Bulkhead pattern for resource isolation
- Backpressure, load shedding, and overload protection
- Timeout policies for external dependencies
- Graceful degradation and fallback mechanisms
- Health check design (liveness vs readiness)
- Error handling best practices
- Chaos engineering setup
- Game days / DR / failover testing (with guardrails)
- Production hardening strategies
- Fault injection testing

**When NOT to use this skill:**

- Simple CRUD apps with no external dependencies — use basic error handling
- Single database, no network calls — standard connection pooling sufficient
- Pure batch jobs with manual retry — scheduled job frameworks handle this
- Frontend-only validation — see [software-frontend](../software-frontend/SKILL.md) instead

---

## Quick Start (Default Workflow)

If key context is missing, ask for: critical user journeys, dependency inventory (including third parties), SLO/SLI targets, current timeout/retry/circuit-breaker settings, idempotency/dedup strategy, and where fault injection is allowed (local/staging/prod).

1. Define scope: critical user journeys, top N dependencies, and SLOs/SLIs (latency, errors, saturation).
2. Build a dependency contract per dependency: timeout budget, retry policy (bounded + jitter), idempotency/dedup expectations, circuit breaker thresholds, and fallback/degraded behavior.
3. Choose a test harness: deterministic fault injection first (mocks/fakes, fault proxy, service mesh faults), then staged chaos experiments, then game day/DR drills if applicable.
4. Define pass/fail signals: error budget burn, p95/p99 budgets, fallback rates, queue backlog, circuit breaker state changes, and recovery time.
5. Produce artifacts (use templates): [Resilience Test Plan Template](assets/testing/template-resilience-test-plan.md), [Fault Injection Playbook](assets/testing/fault-injection-playbook.md), [Resilience Runbook Template](assets/runbooks/resilience-runbook-template.md).

---

## Core QA (Default)

### Failure Mode Testing (What to Validate)

- Timeouts: every network call and DB query has a bounded timeout; validate timeout budgets across chained calls and deadline/cancellation propagation.
- Retries: bounded retries with backoff + jitter; validate idempotency/dedup and retry storm safeguards (caps, budgets, and per-try timeouts).
- Dependency failure: partial outage, slow downstream, rate limiting, DNS failures, auth failures, and corrupted/invalid responses.
- Overload/saturation: connection pool exhaustion, queue backlog, thread pool starvation, and rate limiting; validate backpressure and load shedding.
- Degraded-mode UX: what the user sees/gets when dependencies fail (cached/stale/partial responses) and what consistency guarantees apply.
- Health checks: validate liveness/readiness/startup probe behavior (Kubernetes probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

### Right-Sized Chaos Engineering (Safe by Construction)

- Define steady state and hypothesis (Principles of Chaos Engineering: https://principlesofchaos.org/).
- Start in non-prod; in prod, use minimal blast radius, timeboxed runs, and explicit abort criteria.
- REQUIRED: rollback plan, owners, and observability signals before running experiments.
- REQUIRED (prod): change window + on-call aware, error budget healthy, and an explicit stop condition based on customer impact signals.

### Load/Perf + Production Guardrails

- Load tests validate capacity and tail latency; resilience tests validate behavior under failure.
- Guardrails:
  - Run heavy resilience/perf suites on schedule (nightly) and on canary deploys, not on every PR.
  - Gate releases on regression budgets (p99 latency, error rate, saturation) rather than on raw CPU/memory.

### Flake Control for Resilience Tests

- Chaos/fault injection can look "flaky" if the experiment is not deterministic.
- Stabilize the experiment first: fixed blast radius, controlled fault parameters, deterministic duration, strong observability.

### Debugging Ergonomics

- Every resilience test run should capture: experiment parameters, target scope, timestamps, and trace/log links for failures.
- Prefer tracing/metrics to confirm the failure is the expected one (not collateral damage).

### Do / Avoid

Do:
- Test degraded mode explicitly; document expected UX and API responses.
- Validate retries/timeouts in integration tests with fault injection.

Avoid:
- Unbounded retries and missing timeouts (amplifies incidents).
- "Happy-path only" testing that ignores downstream failure classes.

## Quick Reference

| Pattern | Mechanism / Tooling | When to Use | Configuration (Starting Point) |
|---------|--------------|-------------|---------------|
| Circuit Breaker | App-level breaker or service mesh; emit breaker state changes | Sustained downstream failures or timeouts | Open on sustained error/timeout rates; use half-open probes; tune windows to traffic + error budget |
| Retry with Backoff | Client retry libs; respect Retry-After for 429/503 | Transient failures and rate limiting | 2-3 retries max for user-facing paths; backoff + jitter; per-try timeouts; never exceed remaining deadline |
| Timeout Budgets | Deadlines/cancellation + DB statement timeouts | Any remote call or query | Budget per hop; fail fast; propagate deadlines; set DB query timeout and pool wait timeout |
| Bulkheads + Backpressure | Concurrency limiters, separate pools/queues, admission control | Overload/saturation risk | Separate pools per dependency; bound queues; reject early (429/503) over uncontrolled latency growth |
| Graceful Degradation | Feature flags, cached/stale fallback, partial responses | Non-critical features and partial outages | Define data freshness + UX; instrument fallback rate; avoid silent degradation |
| Health Checks | K8s liveness/readiness/startup probes | Orchestration and load balancing | Liveness shallow; readiness checks critical deps (bounded); startup for slow init; add graceful shutdown |
| Chaos / Fault Injection | Fault proxies, service-mesh faults, managed chaos tools | Validate behavior under real failure modes | Start in non-prod; control blast radius; timebox; predefine stop conditions; record experiment parameters |

---

## Decision Tree: Resilience Pattern Selection

```text
Failure scenario: [System Dependency Type]
    ├─ External API/Service?
    │   ├─ Transient errors? → Retry with exponential backoff + jitter
    │   ├─ Cascading failures? → Circuit breaker + fallback
    │   ├─ Rate limiting? → Retry with Retry-After header respect
    │   └─ Slow response? → Timeout + circuit breaker
    │
    ├─ Database Dependency?
    │   ├─ Connection pool exhaustion? → Bulkhead isolation + timeout
    │   ├─ Query timeout? → Statement timeout (5-10s)
    │   ├─ Replica lag? → Read from primary fallback
    │   └─ Connection failures? → Retry + circuit breaker
    │
    ├─ Overload/Saturation?
    │   ├─ Queue/pool growing? → Backpressure + bound queues + admission control
    │   ├─ Thundering herd? → Jitter + request coalescing + caching
    │   └─ Expensive paths? → Load shedding + feature flag degradation
    │
    ├─ Non-Critical Feature?
    │   ├─ ML recommendations? → Feature flag + default values fallback
    │   ├─ Search service? → Cached results or basic SQL fallback
    │   ├─ Email/notifications? → Log error, don't block main flow
    │   └─ Analytics? → Fire-and-forget, circuit breaker for protection
    │
    ├─ Kubernetes/Orchestration?
    │   ├─ Service discovery? → Liveness + readiness + startup probes
    │   ├─ Slow startup? → Startup probe (failureThreshold: 30)
    │   ├─ Load balancing? → Readiness probe (check dependencies)
    │   └─ Auto-restart? → Liveness probe (simple check)
    │
    └─ Testing Resilience?
        ├─ Pre-production? → Chaos Toolkit experiments
        ├─ Production (low risk)? → Feature flags + canary deployments
        ├─ Scheduled testing? → Game days (quarterly)
        └─ Continuous chaos? → Low-blast-radius fault injection with strong guardrails
```

---

## Navigation: Core Resilience Patterns

- **[Circuit Breaker Patterns](references/circuit-breaker-patterns.md)** - Prevent cascading failures
  - Classic circuit breaker implementation (Node.js, Python)
  - Tuning, alerting, and fallback strategies

- **[Retry Patterns](references/retry-patterns.md)** - Handle transient failures
  - Exponential backoff with jitter
  - Retry decision table (which errors to retry)
  - Idempotency patterns and Retry-After headers

- **[Bulkhead Isolation](references/bulkhead-isolation.md)** - Resource compartmentalization
  - Semaphore pattern for thread/connection pools
  - Database connection pooling strategies
  - Queue-based bulkheads with load shedding

- **[Timeout Policies](references/timeout-policies.md)** - Prevent resource exhaustion
  - Connection, request, and idle timeouts
  - Database query timeouts (PostgreSQL, MySQL)
  - Nested timeout budgets for chained operations

- **[Graceful Degradation](references/graceful-degradation.md)** - Maintain partial functionality
  - Cached fallback strategies
  - Default values and feature toggles
  - Partial responses with Promise.allSettled

- **[Health Check Patterns](references/health-check-patterns.md)** - Service availability monitoring
  - Liveness, readiness, and startup probes
  - Kubernetes probe configuration
  - Shallow vs deep health checks

---

## Navigation: Operational Resources

- **[Resilience Checklists](references/resilience-checklists.md)** - Production hardening checklists
  - Dependency resilience
  - Health and readiness probes
  - Observability for resilience
  - Failure testing

- **[Chaos Engineering Guide](references/chaos-engineering-guide.md)** - Safe reliability experiments
  - Planning chaos experiments
  - Common failure injection scenarios
  - Execution steps and debrief checklist

---

## Navigation: Templates

- **[Resilience Runbook Template](assets/runbooks/resilience-runbook-template.md)** - Service hardening profile
  - Dependencies and SLOs
  - Fallback strategies
  - Rollback procedures

- **[Fault Injection Playbook](assets/testing/fault-injection-playbook.md)** - Chaos testing script
  - Success signals
  - Rollback criteria
  - Post-experiment debrief

- **[Resilience Test Plan Template](assets/testing/template-resilience-test-plan.md)** - Failure mode test plan (timeouts/retries/degraded mode)
  - Scope and dependencies
  - Fault matrix and expected behavior
  - Observability signals and pass/fail criteria

---

## Quick Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| External API calls | Circuit breaker + retry with exponential backoff |
| Database queries | Timeout + connection pooling + circuit breaker |
| Slow dependency | Bulkhead isolation + timeout |
| Overload/saturation | Bulkheads + backpressure + load shedding |
| Non-critical feature | Feature flag + graceful degradation |
| Kubernetes deployment | Liveness + readiness + startup probes |
| Testing resilience | Chaos engineering experiments |
| Transient failures | Retry with exponential backoff + jitter |
| Cascading failures | Circuit breaker + bulkhead |

---

## Anti-Patterns to Avoid

- **No timeouts** - Infinite waits exhaust resources
- **Infinite retries** - Amplifies problems (thundering herd)
- **Retries without idempotency** - Duplicate side effects and data corruption
- **No circuit breakers** - Cascading failures
- **Tight coupling** - One failure breaks everything
- **Silent failures** - No observability into degraded state
- **No bulkheads** - Shared thread pools exhaust all resources
- **Failover never tested** - DR plan fails during a real incident
- **Testing only happy path** - Production reveals failures

---

## Optional: AI / Automation

Do:
- Use AI to propose failure-mode scenarios from an explicit risk register; keep only scenarios that map to known dependencies and business journeys.
- Use AI to summarize experiment results (metrics deltas, error clusters) and draft postmortem timelines; verify with telemetry.

Avoid:
- "Scenario generation" without a risk map (creates noise and wasted load).
- Letting AI relax timeouts/retries or remove guardrails.

---

## Related Skills

- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — Incident response, SLOs, and platform runbooks
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API error handling, retries, and database reliability patterns
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System decomposition and dependency design for reliability
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — Regression, load, and fault-injection testing strategies
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Security failure modes and guardrails
- [../qa-observability/SKILL.md](../qa-observability/SKILL.md) — Metrics, tracing, logging, and performance monitoring
- [../qa-debugging/SKILL.md](../qa-debugging/SKILL.md) — Production debugging and incident investigation
- [../data-sql-optimization/SKILL.md](../data-sql-optimization/SKILL.md) — Database resilience, connection pooling, and query timeouts
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) — API design patterns including error handling and retry semantics

---

## Usage Notes

**Pattern Selection:**

- Start with circuit breakers for external dependencies
- Add retries for transient failures (network, rate limits)
- Use bulkheads to prevent resource exhaustion
- Combine patterns for defense-in-depth

**Observability:**

- Track circuit breaker state changes
- Monitor retry attempts and success rates
- Alert on degraded mode duration
- Measure recovery time after failures

**Testing:**

- Start chaos experiments in non-production
- Define hypothesis before failure injection
- Set blast radius limits and auto-revert
- Document learnings and action items

---

> **Success Criteria:** Systems gracefully handle failures, recover automatically, maintain partial functionality during outages, and fail fast to prevent cascading failures. Resilience is tested proactively through chaos engineering.
