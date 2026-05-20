---
name: production-readiness
model: reasoning
description: Meta-skill that orchestrates logging, monitoring, error handling, performance, security, deployment, and testing skills to ensure a service is fully production-ready before launch. Use before first deploy, major releases, quarterly reviews, or after incidents.
---

# Production Readiness (Meta-Skill)

Coordinates all operational concerns into a single readiness review. Instead of duplicating domain expertise, this skill routes to specialized skills and agents for each area, then synthesizes results into a unified go/no-go assessment.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install production-readiness
```


---

## Purpose

Ensure a service is production-ready by systematically checking every operational concern — logging, error handling, performance, security, deployment, testing, and documentation — before traffic hits it.

A production-ready service:

- **Fails gracefully** under load and partial outages
- **Observes itself** with structured logs, metrics, and traces
- **Recovers automatically** from transient failures
- **Communicates health** to orchestrators and operators
- **Documents operations** so on-call engineers can respond without tribal knowledge

---

## When to Use

| Trigger | Context |
|---------|---------|
| **Before first deploy** | New service going to production for the first time |
| **Before major release** | Significant feature or architectural change shipping |
| **Quarterly production review** | Scheduled audit of existing services |
| **After incident** | Post-incident hardening to prevent recurrence |
| **Dependency upgrade** | Major framework, runtime, or infrastructure change |
| **Team handoff** | Transferring ownership of a service to another team |

---

## Orchestration Flow

Run each area sequentially or in parallel. Each step delegates to a specialized skill or agent — this skill does not re-implement their logic.

```
┌─────────────────────────────────────────────────┐
│              Production Readiness Review         │
├─────────────────────────────────────────────────┤
│                                                  │
│  1. Logging & Observability ──► logging-observability skill
│  2. Error Handling ───────────► error-handling-patterns skill
│  3. Performance ──────────────► performance-agent
│  4. Security ─────────────────► security-review meta-skill
│  5. Deployment ───────────────► deployment-agent + docker-expert skill
│  6. Testing ──────────────────► testing-workflow meta-skill
│  7. Documentation ────────────► /generate-docs command
│                                                  │
│  ──► Synthesize results into go/no-go report     │
└─────────────────────────────────────────────────┘
```

### Step Details

1. **Logging & Observability** — Structured logging, log levels, correlation IDs, metrics endpoints, distributed tracing, alerting rules
2. **Error Handling** — Global error boundaries, retry policies, dead-letter queues, error classification, user-facing error messages
3. **Performance** — Load testing results, P95/P99 latency baselines, memory/CPU profiling, database query analysis, caching strategy
4. **Security** — Auth/authz verification, input validation, dependency audit, secrets management, OWASP top-10 review
5. **Deployment** — Container hardening, rollback strategy, blue-green/canary configuration, infrastructure-as-code review
6. **Testing** — Unit/integration/e2e coverage, contract tests, chaos/failure injection, smoke tests in staging
7. **Documentation** — API docs, runbooks, architecture diagrams, on-call playbooks, ADRs for key decisions

---

## Skill Routing Table

| Concern | Skill / Agent | Path |
|---------|--------------|------|
| Logging & Observability | `logging-observability` | `ai/skills/tools/logging-observability/SKILL.md` |
| Error Handling | `error-handling-patterns` | `ai/skills/backend/error-handling-patterns/SKILL.md` |
| Performance | `performance-agent` | `ai/agents/performance/` |
| Security | `security-review` | `ai/skills/meta/security-review/SKILL.md` |
| Deployment (containers) | `docker-expert` | `ai/skills/devops/docker/SKILL.md` |
| Deployment (pipelines) | `deployment-agent` | `ai/agents/deployment/` |
| Testing | `testing-workflow` | `ai/skills/testing/testing-workflow/SKILL.md` |
| Rate Limiting | `rate-limiting-patterns` | `ai/skills/backend/rate-limiting-patterns/SKILL.md` |
| Documentation | `/generate-docs` | `ai/commands/documentation/` |

> **Routing rule:** Read the target skill first, follow its instructions, then return results here for synthesis.

---

## Production Readiness Checklist

### Health & Lifecycle

- [ ] Health check endpoint (`/healthz` or `/health`) returns dependency status
- [ ] Readiness probe distinguishes "starting" from "ready to serve"
- [ ] Liveness probe detects deadlocks and unrecoverable states
- [ ] Graceful shutdown drains in-flight requests before exit
- [ ] Startup probe allows for slow initialization without false restarts

### Resilience

- [ ] Circuit breakers on all external service calls
- [ ] Retry with exponential backoff and jitter on transient failures
- [ ] Rate limiting configured per endpoint and per client
- [ ] Backpressure mechanisms prevent cascade failures under load
- [ ] Timeouts set on every outbound call (HTTP, DB, queue)
- [ ] Bulkhead isolation separates critical from non-critical paths

### Configuration & Secrets

- [ ] All configuration externalized (env vars, config service, or feature flags)
- [ ] No secrets in code, images, or environment variable defaults
- [ ] Secrets loaded from a vault (e.g., AWS Secrets Manager, HashiCorp Vault)
- [ ] Configuration changes do not require redeployment
- [ ] Feature flags in place for high-risk changes

### Data Safety

- [ ] Backup strategy defined and tested (RPO/RTO documented)
- [ ] Restore procedure verified in a non-production environment
- [ ] Database migrations are backward-compatible and reversible
- [ ] Data retention policies implemented and enforced

### Operational Readiness

- [ ] Runbooks exist for top 5 most likely failure scenarios
- [ ] SLOs defined (availability, latency, error rate) with error budgets
- [ ] SLAs communicated to dependent teams or customers
- [ ] On-call rotation staffed and escalation path documented
- [ ] Dashboards show golden signals (latency, traffic, errors, saturation)
- [ ] Alerting rules configured with appropriate thresholds and severity

---

## Maturity Levels

| Level | Name | Requirements |
|-------|------|-------------|
| **L1** | **MVP** | Health check, basic logging, error handling, manual deploy, unit tests, README |
| **L2** | **Stable** | Structured logging, metrics, graceful shutdown, CI/CD pipeline, integration tests, runbooks |
| **L3** | **Resilient** | Distributed tracing, circuit breakers, auto-scaling, chaos testing, SLOs, on-call rotation |
| **L4** | **Optimized** | Adaptive rate limiting, predictive alerting, canary deploys, full observability, error budgets, postmortem culture |

### Progression Guidance

- **L1 → L2:** Add structured logging, metrics endpoint, and a CI/CD pipeline. Write runbooks for known failure modes.
- **L2 → L3:** Instrument distributed tracing. Add circuit breakers to external calls. Define SLOs and set up on-call.
- **L3 → L4:** Implement canary deployments. Adopt error budgets. Run regular game days. Build predictive alerting.

---

## Incident Response

### On-Call Rotation

- Minimum two engineers per rotation (primary + secondary)
- Handoff includes review of recent deploys, open issues, and known risks
- Escalation targets defined: primary → secondary → engineering lead → VP Eng

### Escalation Matrix

| Severity | Response Time | Escalation After | Stakeholder Notification |
|----------|--------------|-------------------|--------------------------|
| **SEV-1** (outage) | 15 min | 30 min | Immediate — exec + customers |
| **SEV-2** (degraded) | 30 min | 1 hour | Within 1 hour — eng lead |
| **SEV-3** (minor) | 4 hours | Next business day | Daily standup |
| **SEV-4** (cosmetic) | Next sprint | N/A | Backlog |

### Postmortem Template

```markdown
## Incident: [Title]
**Date:** YYYY-MM-DD | **Duration:** X hours | **Severity:** SEV-N

### Summary
One-paragraph description of what happened and impact.

### Timeline
- HH:MM — First alert fired
- HH:MM — Engineer paged, investigation started
- HH:MM — Root cause identified
- HH:MM — Mitigation applied
- HH:MM — Full resolution confirmed

### Root Cause
What broke and why. Link to code/config change if applicable.

### Impact
- Users affected: N
- Revenue impact: $X (if applicable)
- SLO budget consumed: X%

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Fix X  | @eng  | YYYY-MM-DD | Open |

### Lessons Learned
- What went well
- What went poorly
- Where we got lucky
```

---

## NEVER Do

1. **NEVER skip health checks** — every service must expose health endpoints; no exceptions for "simple" services
2. **NEVER store secrets in code or container images** — use a secrets manager; never default env vars with real values
3. **NEVER deploy without a rollback plan** — if you cannot roll back in under 5 minutes, you are not ready to deploy
4. **NEVER ignore error budget violations** — when the error budget is exhausted, freeze feature work and fix reliability
5. **NEVER treat logging as optional** — a service without structured logging is a service you cannot debug at 3 AM
6. **NEVER go to production without runbooks** — if on-call cannot resolve the top 5 failure modes without the original author, the service is not production-ready
