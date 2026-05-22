---
name: qa-debugging
description: Systematic debugging methodologies, troubleshooting workflows, logging strategies, error tracking, performance profiling, stack trace analysis, and debugging tools across languages and environments. Covers local debugging, distributed systems, production issues, and root cause analysis.
---

# Debugging & Troubleshooting (Dec 2025) — Quick Reference

This skill provides execution-ready debugging strategies, troubleshooting workflows, and root cause analysis techniques.

Core references: Google SRE troubleshooting patterns ([Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)) and SLO-driven reliability/triage ([Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)); observability standards via OpenTelemetry ([Docs](https://opentelemetry.io/docs/)) and W3C Trace Context ([Spec](https://www.w3.org/TR/trace-context/)).

---

## Core QA (Default)

### Workflow (Reproduce → Isolate → Instrument → Fix → Verify → Regress)

Reproduce:
- Capture exact failure signature: error message, stack trace, request ID/trace ID, timestamp, build SHA, environment, user/tenant, seed/test data IDs.
- Quantify reproducibility: “fails 3/20 runs” is different from “fails 20/20”.

Isolate:
- Reduce scope: minimal input, minimal config, smallest component boundary.
- Bisect changes (git bisect / feature flags) when it started “recently”.

Instrument:
- Prefer structured logs + correlation IDs and traces over ad-hoc print statements ([OpenTelemetry](https://opentelemetry.io/docs/), [W3C Trace Context](https://www.w3.org/TR/trace-context/)).
- Add assertions/guards to fail fast at the true boundary.

Fix:
- Fix root cause, not symptoms; avoid “papering over” with retries/sleeps.

Verify:
- Add regression test at the lowest effective layer; validate in CI-like conditions.

Regress:
- Record the narrative: trigger, root cause, fix, prevention, and what signal would have caught it earlier ([Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)).

### Debugging Ergonomics (Make Failures Cheap)

- Standardize a failure bundle:
  - Logs (structured), trace links, key metrics snapshot, and repro steps.
  - Test artifacts (screenshots/trace/video for UI; core dumps/crash reports where relevant).
- REQUIRED: every automated suite defines what artifacts are produced on failure and where they live.

### Flaky/Intermittent Failures (Test and Prod)

- Treat flakes as reliability debt, not “noise”.
- First action: classify the flake type:
  - Timing/race: missing waits, async hazards, eventual consistency.
  - Environment: CPU/memory pressure, timezones/locales, throttling.
  - Data: shared state, ordering dependency, non-deterministic fixtures.
- Use controlled repetition: run the test N times with tracing enabled; correlate failures via request/trace IDs.

### Do / Avoid

Do:
- Start with the smallest reliable reproducer.
- Use evidence to support hypotheses (logs, traces, metrics, stack traces).
- Add guardrails and regression tests as part of the fix.

Avoid:
- Adding sleeps to “stabilize” tests without proving the underlying race.
- Disabling tests or lowering assertions to make CI green.
- Debugging directly in production without a safe, scoped plan (feature flags, sampling, read-only probes).

## Quick Reference

| Symptom | Tool/Technique | Command/Approach | When to Use |
|---------|----------------|------------------|-------------|
| Application crashes | Stack trace analysis | Check error logs, identify first line in your code | Unhandled exceptions |
| Slow performance | Profiling (CPU/memory) | `node --prof`, Chrome DevTools, cProfile | High CPU, latency issues |
| Memory leak | Heap snapshots | `node --inspect`, compare snapshots over time | Memory usage grows |
| Database slow | Query profiling | `EXPLAIN ANALYZE`, slow query log | Slow queries, high DB CPU |
| Production-only bug | Log analysis + feature flags | `grep "ERROR"`, enable verbose logging for user | Can't reproduce locally |
| Distributed system issue | Distributed tracing | OpenTelemetry, Jaeger, trace request ID | Microservices, async workflows |
| Intermittent failures | Logging + monitoring | Add detailed logs, monitor metrics | Race conditions, timeouts |
| Network timeout | Network debugging | `curl`, Postman, check firewall/DNS | External API failures |

---

## Decision Tree: Debugging Strategy

```text
Issue type: [Problem Scenario]
    ├─ Application Behavior?
    │   ├─ Crashes immediately? → Check stack trace, error logs
    │   ├─ Slow/hanging? → CPU/memory profiling
    │   ├─ Intermittent failures? → Add logging, reproduce consistently
    │   └─ Unexpected output? → Binary search (add logs to narrow down)
    │
    ├─ Performance Issues?
    │   ├─ High CPU? → CPU profiler to find hot functions
    │   ├─ Memory leak? → Heap snapshots, track over time
    │   ├─ Slow database? → EXPLAIN ANALYZE, check indexes
    │   ├─ Network latency? → Trace external API calls
    │   └─ Frontend slow? → Lighthouse, Web Vitals profiling
    │
    ├─ Production-Only?
    │   ├─ Can't reproduce? → Analyze logs for patterns
    │   ├─ Environment difference? → Compare configs, data volume
    │   ├─ Need safe debugging? → Feature flags for verbose logging
    │   └─ Recent deployment? → Git bisect to find regression
    │
    ├─ Distributed Systems?
    │   ├─ Multiple services involved? → Distributed tracing (Jaeger)
    │   ├─ Request lost? → Search logs by request ID
    │   ├─ Service dependency? → Check health checks, circuit breakers
    │   └─ Async workflow? → Trace message queue, event logs
    │
    └─ Error Type?
        ├─ TypeError/NullPointer? → Check object existence, defensive coding
        ├─ Network timeout? → Check external service health, retry logic
        ├─ Database error? → Check connection pool, query syntax
        └─ Unknown error? → Systematic debugging workflow (observe, hypothesize, test)
```

---

## When to Use This Skill

Use this skill when a user reports:

- Application crashes or errors
- Unexpected behavior or bugs
- Performance issues (slow queries, memory leaks, high CPU)
- Production incidents requiring root cause analysis
- Stack trace or error message interpretation
- Debugging strategies for specific scenarios
- Log analysis and pattern detection
- Distributed system debugging (microservices, async workflows)
- Memory leaks and resource exhaustion
- Race conditions and concurrency issues
- Network connectivity problems
- Database query optimization
- Third-party API integration issues

---

## Operational Deep Dives

See [resources/operational-patterns.md](resources/operational-patterns.md) for systematic debugging workflows, logging strategy details, stack trace and performance profiling guides, and language-specific tooling checklists.

---

## Templates (Copy-Paste Ready)

Production templates organized by workflow type:

- **Debugging Workflow**: [templates/debugging/template-debugging-checklist.md](templates/debugging/template-debugging-checklist.md) - Universal debugging checklist with specialized checklists for performance, memory leaks, distributed systems, and production incidents
- **Debugging Worksheet**: [templates/debugging/template-debugging-worksheet.md](templates/debugging/template-debugging-worksheet.md) - One-page worksheet (repro → isolate → instrument → verify) for fast, consistent triage
- **Incident Response**: [templates/incidents/template-incident-response.md](templates/incidents/template-incident-response.md) - Complete incident response playbook with severity levels, communication templates, and postmortem format
- **Logging Setup**: [templates/observability/template-logging-setup.md](templates/observability/template-logging-setup.md) - Production logging configurations for Node.js (Pino), Python (structlog), Go (zap), with Docker and CloudWatch integration

---

## Resources (Deep-Dive Guides)

Operational best practices by domain:

- **Operational Patterns**: [resources/operational-patterns.md](resources/operational-patterns.md) - Core debugging workflows, stack trace triage, profiling guides, and tool selection
- **Debugging Methodologies**: [resources/debugging-methodologies.md](resources/debugging-methodologies.md) - Scientific method, binary search, delta debugging, rubber duck, time-travel debugging, observability-first approaches
- **Logging Best Practices**: [resources/logging-best-practices.md](resources/logging-best-practices.md) - Structured logging, log levels, what to log/not log, implementations by language, request ID propagation, performance optimization
- **Production Debugging**: [resources/production-debugging-patterns.md](resources/production-debugging-patterns.md) - Safe production debugging techniques, log analysis, metrics, distributed tracing, feature flags, incident response workflow

---

## Navigation

**Resources**
- [resources/operational-patterns.md](resources/operational-patterns.md)
- [resources/debugging-methodologies.md](resources/debugging-methodologies.md)
- [resources/logging-best-practices.md](resources/logging-best-practices.md)
- [resources/production-debugging-patterns.md](resources/production-debugging-patterns.md)

**Templates**
- [templates/debugging/template-debugging-checklist.md](templates/debugging/template-debugging-checklist.md)
- [templates/debugging/template-debugging-worksheet.md](templates/debugging/template-debugging-worksheet.md)
- [templates/incidents/template-incident-response.md](templates/incidents/template-incident-response.md)
- [templates/observability/template-logging-setup.md](templates/observability/template-logging-setup.md)

**Data**
- [data/sources.json](data/sources.json) — Curated external references

---

## Optional: AI / Automation

Use AI assistance to accelerate triage, not to replace evidence-based debugging.

Do:
- Summarize logs/traces and cluster failures; always include “evidence snippets” (IDs, timestamps, top errors) that can be independently verified.
- Generate hypotheses, then test them with targeted instrumentation.

Avoid:
- Letting AI decide root cause without corroborating evidence.
- Copying suggested fixes without adding regression tests.

---

## External Resources

See `data/sources.json` for:
- Debugging tool documentation
- Error tracking platforms (Sentry, Rollbar, Bugsnag)
- Observability platforms (Datadog, New Relic, Honeycomb)
- Profiling tutorials and guides
- Production debugging best practices

---

## Quick Decision Matrix

| Symptom | Likely Cause | First Action |
|---------|-------------|-------------|
| Application crashes | Unhandled exception | Check error logs and stack trace |
| Slow performance | Database/network/CPU bottleneck | Profile with performance tools |
| Memory usage grows | Memory leak | Take heap snapshots over time |
| Intermittent failures | Race condition, network timeout | Add detailed logging around failure |
| Production-only bug | Environment difference, data volume | Compare prod vs dev config/data |
| High CPU usage | Infinite loop, inefficient algorithm | CPU profiler to find hot functions |
| Database slow | Missing index, N+1 queries | Run EXPLAIN ANALYZE on slow queries |

---

## Anti-Patterns to Avoid

- **Random changes** - Making changes without hypothesis
- **Inadequate logging** - Can't debug what you can't see
- **Debugging in production** - Always reproduce locally when possible
- **Ignoring stack traces** - Stack trace tells you exactly where error occurred
- **Not writing tests** - Fix today, break tomorrow
- **Symptom fixing** - Treating symptoms instead of root cause
- **No monitoring** - Flying blind in production
- **Skipping postmortems** - Not learning from incidents

---

## Related Skills

This skill works with other skills in the framework:

**Development & Operations**:

- [git-workflow](../git-workflow/SKILL.md) - Git bisect for finding regressions, version control workflows
- [dev-api-design](../dev-api-design/SKILL.md) - API debugging, error handling, REST patterns, status codes

**Infrastructure & Platform**:

- [ops-devops-platform](../ops-devops-platform/SKILL.md) - CI/CD pipelines, monitoring, incident response, SRE practices, Kubernetes ops
- [data-sql-optimization](../data-sql-optimization/SKILL.md) - Database query optimization, EXPLAIN ANALYZE, index tuning, slow query debugging

---

> **Success Criteria:** Issues are diagnosed systematically, root causes are identified accurately, fixes include regression tests, and debugging knowledge is documented for future reference.
