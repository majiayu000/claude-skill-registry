---
name: sre-patterns
description: Provides Site Reliability Engineering best practices for SLOs, SLIs, SLAs, error budgets, toil reduction, reliability reviews, and capacity planning. Use when defining service objectives, measuring reliability, reducing toil, planning capacity, or when user mentions 'SRE', 'SLO', 'SLI', 'SLA', 'error budget', 'toil', 'reliability', 'on-call', 'capacity planning'.
---

# SRE Patterns

Best practices for building and operating reliable systems using Site Reliability Engineering principles.

## SLO / SLI / SLA Definitions

These three concepts form the foundation of SRE. They are distinct and frequently confused.

| Concept | Definition | Owner | Example |
|---------|-----------|-------|---------|
| **SLI** (Service Level Indicator) | A quantitative measurement of a service attribute | Engineering | 99.2% of requests completed in < 300ms |
| **SLO** (Service Level Objective) | A target value or range for an SLI | Engineering + Product | 99.5% of requests must complete in < 300ms |
| **SLA** (Service Level Agreement) | A contract with consequences for missing an SLO | Business + Legal | 99.9% uptime or customer receives service credits |

### Relationship

```
SLI (what you measure)
 --> SLO (what you target, always stricter than SLA)
  --> SLA (what you promise externally, with penalties)
```

**Key rule:** SLO must be stricter than SLA. If your SLA promises 99.9% uptime, your internal SLO should target 99.95%. The gap is your safety margin.

## SLI Specification

SLIs must be precise, measurable, and tied to user experience. Vague indicators lead to meaningless objectives.

### SLI Types by Service Category

| Service Type | SLI Category | Good Event | Valid Event |
|-------------|-------------|------------|-------------|
| Request-driven | Availability | Response status < 500 | All HTTP requests |
| Request-driven | Latency | Response time < 300ms | All HTTP requests |
| Data pipeline | Freshness | Data age < 10 minutes | All data records |
| Data pipeline | Correctness | Records with no processing errors | All processed records |
| Storage system | Durability | Objects retrievable after write | All stored objects |
| Storage system | Throughput | Read operations < 50ms | All read operations |

### SLI Specification Example

```yaml
# sli-specification.yaml
service: payment-api
slis:
  - name: availability
    description: Proportion of successful requests
    specification:
      good_event: "HTTP response status code is not 5xx"
      valid_event: "All HTTP requests to /api/v1/payments/*"
      measurement_source: load_balancer_logs
      measurement_window: rolling_28_days
    implementation:
      numerator: "count(status < 500)"
      denominator: "count(all requests)"
      exclude:
        - health_check_endpoints
        - synthetic_monitoring_requests

  - name: latency
    description: Proportion of requests served within threshold
    specification:
      good_event: "HTTP response completes within 300ms"
      valid_event: "All non-background HTTP requests"
      measurement_source: server_side_metrics
      measurement_window: rolling_28_days
    implementation:
      numerator: "count(duration_ms <= 300)"
      denominator: "count(all requests)"
      percentile_targets:
        p50: 100ms
        p95: 250ms
        p99: 500ms
```

## Error Budget Calculation

The error budget is the inverse of your SLO -- the amount of unreliability you can tolerate.

### Formula

```
Error Budget = 1 - SLO target

Example:
  SLO = 99.9% availability
  Error Budget = 1 - 0.999 = 0.1%

  In a 30-day month (43,200 minutes):
  Budget = 43,200 * 0.001 = 43.2 minutes of downtime allowed
```

### Error Budget by SLO Level

| SLO Target | Error Budget (30 days) | Error Budget (per quarter) | Practical Meaning |
|-----------|----------------------|--------------------------|-------------------|
| 99.0% | 7 hours 12 min | 21 hours 36 min | Tolerates significant outages |
| 99.5% | 3 hours 36 min | 10 hours 48 min | Weekly maintenance window feasible |
| 99.9% | 43 minutes 12 sec | 2 hours 9 min | No room for long outages |
| 99.95% | 21 minutes 36 sec | 1 hour 5 min | Requires high automation |
| 99.99% | 4 minutes 19 sec | 12 min 58 sec | Requires redundancy at every layer |

### Error Budget Burn Rate

Burn rate measures how fast you are consuming your error budget relative to the budget period.

```python
# error_budget_tracking.py

def calculate_burn_rate(
    error_count: int,
    total_requests: int,
    slo_target: float,
    budget_period_hours: float,
    elapsed_hours: float
) -> dict:
    """Calculate error budget consumption and burn rate."""
    error_budget = 1.0 - slo_target
    current_error_rate = error_count / total_requests if total_requests > 0 else 0
    budget_consumed = current_error_rate / error_budget if error_budget > 0 else float('inf')

    # Burn rate: 1.0 means consuming budget exactly on pace
    # > 1.0 means burning faster than sustainable
    expected_consumed = elapsed_hours / budget_period_hours
    burn_rate = budget_consumed / expected_consumed if expected_consumed > 0 else 0

    remaining_budget = max(0, error_budget - current_error_rate)
    hours_remaining = (
        (remaining_budget / current_error_rate) * elapsed_hours
        if current_error_rate > 0 else float('inf')
    )

    return {
        "slo_target": slo_target,
        "error_budget_total": error_budget,
        "current_error_rate": current_error_rate,
        "budget_consumed_pct": budget_consumed * 100,
        "burn_rate": burn_rate,
        "hours_until_exhausted": hours_remaining,
    }

# Example usage:
# 99.9% SLO, 720-hour budget period (30 days), 168 hours elapsed (1 week)
result = calculate_burn_rate(
    error_count=150,
    total_requests=500_000,
    slo_target=0.999,
    budget_period_hours=720,
    elapsed_hours=168
)
# burn_rate > 1.0 --> alerting threshold
```

## Error Budget Policy

An error budget policy defines what happens when the budget is consumed. Without a policy, the budget is just a number.

```yaml
# error-budget-policy.yaml
service: payment-api
slo: 99.9% availability (rolling 28 days)
policy_owner: payments-team-lead
approved_by: vp-engineering
effective_date: 2025-01-15

budget_thresholds:
  - level: normal
    condition: "budget_consumed < 50%"
    actions:
      - Continue normal feature development
      - Standard deployment cadence (daily)
      - Routine reliability improvements as scheduled

  - level: caution
    condition: "budget_consumed >= 50% AND < 75%"
    actions:
      - Review recent deployments for reliability impact
      - Increase monitoring alert sensitivity
      - Prioritize known reliability-related bugs
      - Reduce deployment frequency to twice per week

  - level: critical
    condition: "budget_consumed >= 75% AND < 100%"
    actions:
      - Halt all non-reliability feature work
      - Require SRE approval for every deployment
      - Deploy only bug fixes and reliability improvements
      - Conduct focused reliability review within 48 hours
      - Notify stakeholders of SLO risk

  - level: exhausted
    condition: "budget_consumed >= 100%"
    actions:
      - Feature freeze until budget replenishes or root cause resolved
      - Emergency reliability review within 24 hours
      - Postmortem required for each new incident
      - All deployments require SRE sign-off and canary phase
      - Weekly status report to VP Engineering

escalation:
  budget_dispute: "Escalate to VP Engineering for arbitration"
  exemptions: "Launch exemptions require VP+ approval with risk acceptance"
```

## Toil Measurement and Reduction

Toil is work that is manual, repetitive, automatable, reactive, and scales linearly with service growth. Toil is the enemy of reliability engineering.

### Toil Characteristics

| Characteristic | Description | Example |
|---------------|-------------|---------|
| Manual | Requires a human to perform | SSH into server to restart service |
| Repetitive | Done more than once or twice | Weekly cert rotation by hand |
| Automatable | A machine could do it | Copying logs to analysis bucket |
| Reactive | Triggered by an event, not proactive | Responding to disk full alerts |
| No enduring value | Does not improve the service | Re-running failed batch jobs |
| Scales with service | More instances = more work | Manually updating configs per server |

### Toil Measurement Framework

```yaml
# toil-tracking.yaml
team: platform-sre
measurement_period: 2025-Q1
target_toil_budget: 30%  # Max 30% of team time on toil

categories:
  - name: incident_response
    hours_per_week: 8
    toil_percentage: 60%    # 60% of incident response is toil
    toil_hours: 4.8
    examples:
      - Manually restarting crashed services
      - Clearing stuck queue items
      - Responding to known-cause alerts without automation

  - name: deployment_support
    hours_per_week: 6
    toil_percentage: 40%
    toil_hours: 2.4
    examples:
      - Manual pre-deploy checklist verification
      - Running migration scripts by hand
      - Monitoring dashboards during every deploy

  - name: capacity_management
    hours_per_week: 4
    toil_percentage: 75%
    toil_hours: 3.0
    examples:
      - Manually resizing instances
      - Tracking disk usage via spreadsheets
      - Filing tickets to request quota increases

  - name: access_provisioning
    hours_per_week: 3
    toil_percentage: 90%
    toil_hours: 2.7
    examples:
      - Creating accounts across multiple systems
      - Rotating credentials manually
      - Revoking access for departing employees

summary:
  total_team_hours_per_week: 200  # 5 engineers * 40 hours
  total_toil_hours_per_week: 12.9
  toil_percentage: 6.45%
  status: within_budget
  top_reduction_targets:
    - access_provisioning   # 90% toil -- automate with IaC/SCIM
    - capacity_management   # 75% toil -- autoscaling policies
    - incident_response     # 60% toil -- self-healing automation
```

## Capacity Planning

Capacity planning ensures services can handle expected and unexpected load without degradation.

### Capacity Planning Model

```python
# capacity_model.py

from dataclasses import dataclass
from typing import Optional

@dataclass
class CapacityPlan:
    service: str
    current_peak_rps: float
    growth_rate_monthly: float       # e.g., 0.05 for 5% per month
    headroom_target: float           # e.g., 0.30 for 30% headroom
    max_rps_per_instance: float
    current_instances: int
    burst_multiplier: float = 2.0    # Expected burst over peak

    def projected_peak(self, months_ahead: int) -> float:
        """Project peak RPS N months from now."""
        return self.current_peak_rps * (1 + self.growth_rate_monthly) ** months_ahead

    def required_capacity(self, months_ahead: int) -> float:
        """Required RPS capacity including headroom and burst tolerance."""
        projected = self.projected_peak(months_ahead)
        with_burst = projected * self.burst_multiplier
        with_headroom = with_burst / (1 - self.headroom_target)
        return with_headroom

    def required_instances(self, months_ahead: int) -> int:
        """Number of instances needed."""
        import math
        capacity = self.required_capacity(months_ahead)
        return math.ceil(capacity / self.max_rps_per_instance)

    def months_until_scaling_needed(self) -> Optional[int]:
        """Months until current instance count is insufficient."""
        current_max = self.current_instances * self.max_rps_per_instance
        for month in range(1, 37):
            if self.required_capacity(month) > current_max:
                return month
        return None  # Sufficient for 3+ years

    def report(self, horizon_months: int = 6) -> str:
        lines = [f"Capacity Plan: {self.service}", "=" * 40]
        lines.append(f"Current peak: {self.current_peak_rps:.0f} RPS")
        lines.append(f"Current instances: {self.current_instances}")
        lines.append(f"Growth rate: {self.growth_rate_monthly*100:.1f}%/month")
        lines.append("")

        for m in [1, 3, 6, 12]:
            if m <= horizon_months:
                needed = self.required_instances(m)
                delta = needed - self.current_instances
                flag = " ** SCALE NEEDED **" if delta > 0 else ""
                lines.append(f"  +{m:2d} months: {needed} instances (delta: {delta:+d}){flag}")

        scaling_month = self.months_until_scaling_needed()
        if scaling_month:
            lines.append(f"\nScaling needed in: {scaling_month} month(s)")
        else:
            lines.append("\nCapacity sufficient for 3+ years")
        return "\n".join(lines)


# Example:
plan = CapacityPlan(
    service="payment-api",
    current_peak_rps=1200,
    growth_rate_monthly=0.08,
    headroom_target=0.30,
    max_rps_per_instance=500,
    current_instances=10,
    burst_multiplier=2.0
)
print(plan.report(horizon_months=12))
```

## Reliability Review Process

Reliability reviews are structured evaluations of a service's production readiness and ongoing operational health.

### Pre-Launch Review

| Review Area | Key Questions | Pass Criteria |
|------------|---------------|---------------|
| SLOs defined | Are SLIs and SLOs documented? | At least availability + latency SLOs |
| Monitoring | Are dashboards and alerts configured? | SLO-based alerts with multi-window burn rate |
| Incident response | Is there a runbook? | Documented runbook with escalation paths |
| Capacity | Can it handle 2x current load? | Load test results proving headroom |
| Dependencies | Are failure modes mapped? | Dependency map with fallback behavior |
| Rollback | Can you revert within 5 minutes? | Tested rollback procedure |
| Data integrity | Are backups tested? | Backup restore tested within last 30 days |
| Security | Has threat modeling been done? | Threat model documented, critical items resolved |

### Ongoing Review Cadence

```
Weekly:  Error budget review (automated dashboard)
Monthly: Service health review (SRE + dev team, 30 min)
Quarterly: Full reliability review (cross-functional, 2 hours)
Annually: Architecture review (principal engineers + SRE, half day)
```

### Monthly Service Health Review Template

```markdown
## Service Health Review: [service-name]
Date: [date]
Attendees: [list]

### SLO Performance
- Availability SLO: [target] | Actual: [value] | Budget remaining: [%]
- Latency SLO: [target] | Actual: [value] | Budget remaining: [%]

### Incidents This Period
| Date | Severity | Duration | Budget Impact | Postmortem |
|------|----------|----------|--------------|------------|

### Toil Report
- Toil hours this period: [X]
- Top toil sources: [list]
- Automation tickets filed: [count]

### Action Items
| Item | Owner | Due Date | Status |
|------|-------|----------|--------|

### Capacity Outlook
- Current utilization: [%]
- Scaling needed by: [date or N/A]
```

## On-Call Best Practices

### On-Call Structure

| Practice | Recommendation | Rationale |
|----------|---------------|-----------|
| Rotation length | 1 week | Long enough for context, short enough to avoid burnout |
| Team size | Minimum 6-8 engineers | Ensures no one is on-call more than 1 in 6 weeks |
| Handoff | 30-minute overlap meeting | Transfer context on active issues |
| Escalation | Primary -> Secondary -> Team Lead -> Manager | Clear chain prevents ambiguity |
| Response time | 5 min acknowledge, 15 min start investigation | Documented in on-call agreement |
| Compensation | Time off in lieu or pay differential | On-call without compensation causes attrition |

### Alert Quality

```
Good alert:
  - Actionable (something a human must do NOW)
  - Tied to an SLO (not a system metric)
  - Has a runbook link
  - Fires infrequently (< 2 per shift)

Bad alert:
  - Informational (log it, don't page)
  - Fires often and gets ignored (alert fatigue)
  - No runbook (engineer wastes time figuring out what to do)
  - Not tied to user impact
```

### Multi-Window Burn Rate Alerting

Alert on error budget burn rate rather than raw error counts. Use multiple windows to balance sensitivity with false positive rate.

| Alert Severity | Burn Rate | Long Window | Short Window | Action |
|---------------|-----------|-------------|-------------|--------|
| Page (urgent) | 14.4x | 1 hour | 5 minutes | Immediate investigation |
| Page (less urgent) | 6x | 6 hours | 30 minutes | Investigate within 30 min |
| Ticket | 3x | 3 days | 6 hours | Fix within 1 business day |
| Log | 1x | 28 days | 3 days | Review at next planning |

## Incident Management

### Severity Levels

| Severity | Definition | Response | Example |
|----------|-----------|----------|---------|
| SEV1 | Service down, all users affected | Immediate, all-hands | Total outage of payment processing |
| SEV2 | Significant degradation, many users affected | Immediate, on-call team | Latency 10x normal, 30% errors |
| SEV3 | Partial degradation, some users affected | Within 1 hour | One region experiencing failures |
| SEV4 | Minor issue, few users affected | Next business day | Cosmetic issue in dashboard |

### Postmortem Structure

Every SEV1 and SEV2 incident gets a blameless postmortem within 72 hours.

```markdown
## Postmortem: [Incident Title]
Date: [incident date]
Duration: [start time] to [end time] ([total duration])
Severity: [SEV level]
Author: [name]
Reviewers: [names]

### Summary
[1-2 sentence description of what happened and impact]

### Impact
- Users affected: [number or percentage]
- Revenue impact: [if applicable]
- Error budget consumed: [percentage]
- SLO status: [still within / breached]

### Timeline
| Time (UTC) | Event |
|-----------|-------|
| HH:MM | First alert fired |
| HH:MM | On-call acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Full recovery confirmed |

### Root Cause
[Technical description of what caused the incident]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### What Went Well
- [Thing 1]
- [Thing 2]

### What Could Be Improved
- [Thing 1]
- [Thing 2]

### Action Items
| Action | Type | Owner | Bug/Ticket | Due |
|--------|------|-------|-----------|-----|
| [action] | prevent | [name] | [link] | [date] |
| [action] | detect | [name] | [link] | [date] |
| [action] | mitigate | [name] | [link] | [date] |
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| SLOs set by management without engineering input | Unrealistic targets that create constant fire-fighting | SLOs must be data-driven and jointly owned by eng + product |
| 100% availability SLO | Impossible to maintain, blocks all deployments | Highest practical target is 99.999%; most services need 99.9% |
| SLIs measured at the server, not at the user | Misses network issues, CDN failures, client-side errors | Measure SLIs at the load balancer or client where possible |
| Error budget without a policy | Budget is tracked but nothing changes when it is consumed | Write and enforce a formal error budget policy document |
| Alerting on raw metrics instead of SLOs | Alert fatigue from non-user-impacting events | Use multi-window burn rate alerting tied to SLOs |
| Treating all toil as unavoidable | Team spends 60%+ time on repetitive manual work | Measure toil, set a budget (< 50%), automate top sources |
| No postmortems or blame-focused postmortems | Same incidents recur; engineers hide mistakes | Blameless postmortems with tracked action items |
| Capacity planning by gut feel | Over-provisioning wastes money; under-provisioning causes outages | Model growth, load test regularly, maintain 30% headroom |
| On-call without runbooks | Engineers waste time investigating known issues | Every alert must link to a runbook with diagnosis steps |
| On-call hero culture | One person handles everything, burns out, leaves with all context | Minimum team size of 6-8, mandatory rotation, no opt-out |
| Monitoring everything, alerting on nothing useful | Thousands of metrics, dashboards no one looks at | Focus on the 3-5 SLIs that represent user experience |
| SLAs more aggressive than SLOs | No safety margin; internal failures immediately become contract breaches | SLOs must be stricter than SLAs by a meaningful margin |
| Skipping reliability reviews before launch | Production issues discovered by users, not engineers | Mandatory pre-launch review with documented pass criteria |

## SRE Maturity Checklist

### Level 1: Foundations

- [ ] SLIs defined for every user-facing service
- [ ] SLOs documented and published to stakeholders
- [ ] Basic monitoring and dashboards in place
- [ ] On-call rotation established with at least 6 engineers
- [ ] Incident response process documented
- [ ] Postmortem process established (blameless)

### Level 2: Operational

- [ ] Error budgets calculated and tracked automatically
- [ ] Error budget policy written and enforced
- [ ] Multi-window burn rate alerting configured
- [ ] Toil measured and tracked quarterly
- [ ] Runbooks exist for every on-call alert
- [ ] Monthly service health reviews conducted
- [ ] Capacity planning done quarterly with growth projections

### Level 3: Proactive

- [ ] Toil consistently below 30% of team time
- [ ] Automated remediation for top 5 incident categories
- [ ] Chaos engineering practiced regularly
- [ ] Load testing integrated into release pipeline
- [ ] Dependency failure modes mapped and tested
- [ ] SLO-informed release decisions (feature freeze when budget low)
- [ ] Cross-team reliability standards established

### Level 4: Optimized

- [ ] SLO performance consistently within target for 4+ quarters
- [ ] Error budget rarely exhausted (< 1 per quarter)
- [ ] Toil below 15% of team time
- [ ] Automated capacity planning with autoscaling
- [ ] Proactive reliability improvements outpace reactive work
- [ ] Reliability culture embedded across all engineering teams
- [ ] Regular architecture reviews with reliability as primary lens
