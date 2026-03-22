---
name: incident-response-patterns
description: "Production incident response patterns: severity classification (SEV1-4), incident roles, SLO/SLI framework, error budget policy, and blameless culture principles. Use when designing incident response processes, writing runbooks, defining SLOs, creating post-mortems, or reviewing incident readiness. Do NOT use for code bug investigation (use bug-investigation instead)."
durability: encoded-preference
---

# Incident Response Patterns

## Scope

This skill covers production incident management principles. For code-level bug investigation, see `bug-investigation`. For operational reliability in code reviews (observability, retry, circuit breakers, health checks, timeouts, blast radius), see `sre-reviewer`.

## Severity Classification Matrix

| Level | Name | Criteria | Response Time | Update Cadence |
|-------|------|----------|---------------|----------------|
| SEV1 | Critical | Full service outage, data loss risk, security breach | Immediate | Every 15 min |
| SEV2 | Major | Degraded service for >25% users, key feature down | Within minutes | Every 30 min |
| SEV3 | Moderate | Minor feature broken, workaround available | Within hours | Every 2 hours |
| SEV4 | Low | Cosmetic issue, no user impact, tech debt trigger | Next business day | Daily |

## Incident Response Roles

| Role | Responsibility |
|------|---------------|
| Incident Commander (IC) | Owns timeline, decision-making, severity calls. Single point of coordination |
| Communications Lead | Sends stakeholder updates per severity cadence. Manages status page |
| Technical Lead | Drives diagnosis using runbooks and observability. Owns remediation execution |
| Scribe | Logs every action and finding in real-time with timestamps. Source of truth for timeline |

Assign all four roles before beginning troubleshooting. Chaos multiplies without explicit coordination.

## SLO/SLI Definition Framework

### SLI Types

| SLI | Definition | Good Event | Metric Pattern |
|-----|-----------|------------|----------------|
| Availability | Proportion of successful requests | HTTP status < 500 | success_total / request_total |
| Latency | Proportion of requests within threshold | Response time < threshold at target percentile | histogram_quantile |
| Correctness | Proportion of correct results | No business logic error | 1 - (error_total / request_total) |

### SLO Structure

Each SLO specifies:
- Which SLI it targets
- Target percentage (e.g., 99.95%)
- Measurement window (typically 30 days rolling)
- Error budget (derived from target and window)

### Error Budget Policy

| Budget Remaining | Action |
|-----------------|--------|
| > 50% | Normal feature development |
| 25-50% | Feature freeze review with Eng Manager |
| < 25% | All hands on reliability work until budget recovers |
| Exhausted (0%) | Freeze all non-critical deploys, review with VP Eng |

SLOs must have teeth: when the error budget is burned, feature work pauses for reliability work.

## Blameless Culture Principles

- Frame findings as "the system allowed this failure mode" -- never as "X person caused the outage"
- Focus on what the system lacked (guardrails, alerts, tests) rather than what a human did wrong
- Treat every incident as a learning opportunity that strengthens organizational resilience
- Protect psychological safety -- engineers who fear blame will hide issues instead of escalating
- On-call engineers must have authority to take emergency actions without multi-level approval chains

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Skipping severity classification | Always classify -- it determines escalation, communication, and resources |
| Diving into troubleshooting without assigning roles | Assign IC, Comms, Tech Lead, Scribe first |
| Untested runbooks | Test quarterly -- validate remediation steps actually work |
| Post-mortem without tracked action items | Every action item needs owner, priority, due date, status tracking |
| Repeated incidents from known root causes | Indicates post-mortem action items are not being completed |
| Single person's tribal knowledge as the runbook | Document into persistent, shared runbooks |

For runbook template, post-mortem template, burn rate thresholds, and communication cadence, see references/templates.md.
