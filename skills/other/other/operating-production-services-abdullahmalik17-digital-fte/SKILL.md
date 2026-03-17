---
name: operating-production-services
description: |
  SRE patterns for production service reliability: SLOs, error budgets, postmortems, and incident response.
  Use when defining reliability targets, writing postmortems, implementing SLO alerting, or establishing
  on-call practices. NOT for initial service development (use scaffolding skills instead).
---

# Operating Production Services

Production reliability patterns: measure what matters, learn from failures, improve systematically.

## Quick Reference

| Need | Go To |
|------|-------|
| Define reliability targets | [SLOs & Error Budgets](#slos--error-budgets) |
| Write incident report | [Postmortem Templates](#postmortem-templates) |
| Set up SLO alerting | [references/slo-alerting.md](references/slo-alerting.md) |

---

## SLOs & Error Budgets

### The Hierarchy

```
SLA (Contract) → SLO (Target) → SLI (Measurement)
```

### Common SLIs

```promql
# Availability: successful requests / total requests
sum(rate(http_requests_total{status!~"5.."}[28d]))
/
sum(rate(http_requests_total[28d]))

# Latency: requests below threshold / total requests
sum(rate(http_request_duration_seconds_bucket{le="0.5"}[28d]))
/
sum(rate(http_request_duration_seconds_count[28d]))
```

### SLO Targets Reality Check

| SLO % | Downtime/Month | Downtime/Year |
|-------|----------------|---------------|
| 99% | 7.2 hours | 3.65 days |
| 99.9% | 43 minutes | 8.76 hours |
| 99.95% | 22 minutes | 4.38 hours |
| 99.99% | 4.3 minutes | 52 minutes |

**Don't aim for 100%.** Each nine costs exponentially more.

### Error Budget

```
Error Budget = 1 - SLO Target
```

**Example:** 99.9% SLO = 0.1% error budget = 43 minutes/month

**Policy:**
| Budget Remaining | Action |
|------------------|--------|
| > 50% | Normal velocity |
| 10-50% | Postpone risky changes |
| < 10% | Freeze non-critical changes |
| 0% | Feature freeze, fix reliability |

See [references/slo-alerting.md](references/slo-alerting.md) for Prometheus recording rules and multi-window burn rate alerts.

---

## Postmortem Templates

### The Blameless Principle

| Blame-Focused | Blameless |
|---------------|-----------|
| "Who caused this?" | "What conditions allowed this?" |
| Punish individuals | Improve systems |
| Hide information | Share learnings |

### When to Write Postmortems

- SEV1/SEV2 incidents
- Customer-facing outages > 15 minutes
- Data loss or security incidents
- Near-misses that could have been severe
- Novel failure modes

### Standard Template

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD | **Duration**: X min | **Severity**: SEVX

## Executive Summary
One paragraph: what happened, impact, root cause, resolution.

## Timeline (UTC)
| Time | Event |
|------|-------|
| HH:MM | First alert fired |
| HH:MM | On-call acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Fix deployed |
| HH:MM | Service recovered |

## Root Cause Analysis

### 5 Whys
1. Why did service fail? → [Answer]
2. Why did [1] happen? → [Answer]
3. Why did [2] happen? → [Answer]
4. Why did [3] happen? → [Answer]
5. Why did [4] happen? → [Root cause]

## Impact
- Customers affected: X
- Duration: X minutes
- Revenue impact: $X
- Support tickets: X

## Action Items
| Priority | Action | Owner | Due | Ticket |
|----------|--------|-------|-----|--------|
| P0 | [Immediate fix] | @name | Date | XXX-123 |
| P1 | [Prevent recurrence] | @name | Date | XXX-124 |
| P2 | [Improve detection] | @name | Date | XXX-125 |
```

### Quick Template (Minor Incidents)

```markdown
# Quick Postmortem: [Title]

**Date**: YYYY-MM-DD | **Duration**: X min | **Severity**: SEV3

## What Happened
One sentence description.

## Timeline
- HH:MM - Trigger
- HH:MM - Detection
- HH:MM - Resolution

## Root Cause
One sentence.

## Fix
- Immediate: [What was done]
- Long-term: [Ticket XXX-123]
```

---

## Postmortem Meeting Guide

### Structure (60 min)

1. **Opening (5 min)** - Remind: "We're here to learn, not blame"
2. **Timeline (15 min)** - Walk through events chronologically
3. **Analysis (20 min)** - What failed? Why? What allowed it?
4. **Action Items (15 min)** - Prioritize, assign owners, set dates
5. **Closing (5 min)** - Summarize learnings, confirm owners

### Facilitation Tips

- Redirect blame to systems: "What made this mistake possible?"
- Time-box tangents
- Document dissenting views
- Encourage quiet participants

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Aim for 100% SLO | Accept error budget exists |
| Skip small incidents | Small incidents reveal patterns |
| Orphan action items | Every item needs owner + date + ticket |
| Blame individuals | Ask "what conditions allowed this?" |
| Create busywork actions | Actions should prevent recurrence |

---

## Verification

Run: `python scripts/verify.py`

## References

- [references/slo-alerting.md](references/slo-alerting.md) - Prometheus rules, burn rate alerts, Grafana dashboards
