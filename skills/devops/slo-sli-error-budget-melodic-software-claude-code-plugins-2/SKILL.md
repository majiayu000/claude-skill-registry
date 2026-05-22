---
name: slo-sli-error-budget
description: Use when defining SLOs, selecting SLIs, or implementing error budget policies. Covers reliability targets, SLI selection, and error budget management.
allowed-tools: Read, Glob, Grep
---

# SLOs, SLIs, and Error Budgets

Patterns and practices for defining service level objectives, selecting meaningful indicators, and managing reliability through error budgets.

## When to Use This Skill

- Defining SLOs for services
- Selecting appropriate SLIs
- Implementing error budget policies
- Balancing reliability and velocity
- Setting up SLO-based alerting

## Core Concepts

### SLI (Service Level Indicator)

```text
SLI = Quantitative measure of service level

What to measure:
- Availability: % of successful requests
- Latency: % of requests faster than threshold
- Throughput: Requests per second
- Error rate: % of failed requests

Formula:
SLI = (good events / total events) × 100%

Example:
Availability SLI = (successful requests / total requests) × 100%
             = (99,500 / 100,000) × 100%
             = 99.5%
```

### SLO (Service Level Objective)

```text
SLO = Target value for an SLI

Format: SLI >= Target over Time Window

Examples:
- 99.9% of requests successful over 30 days
- 95% of requests complete in <200ms over 7 days
- 99.95% availability measured monthly

Components:
┌─────────────────────────────────────────────────────┐
│ SLO = SLI + Target + Time Window                    │
│                                                      │
│ "99.9% of HTTP requests return non-5xx             │
│  over a rolling 30-day window"                      │
└─────────────────────────────────────────────────────┘
```

### Error Budget

```text
Error Budget = Allowed unreliability

If SLO = 99.9% availability:
Error Budget = 100% - 99.9% = 0.1%

Over 30 days:
Total minutes = 30 × 24 × 60 = 43,200
Error budget = 43,200 × 0.001 = 43.2 minutes

Or in requests (assuming 1M requests/month):
Error budget = 1,000,000 × 0.001 = 1,000 failed requests

Budget consumption:
┌────────────────────────────────────────────────────┐
│ Error Budget Remaining: 65%                        │
│ ████████████████████░░░░░░░░░░                    │
│ Consumed: 35% (15 min of 43.2 min)                │
│ Days remaining in window: 12                       │
└────────────────────────────────────────────────────┘
```

## Selecting SLIs

### SLI Categories

```text
1. Request-based SLIs:
   - Availability (success rate)
   - Latency (response time)
   - Quality (correct responses)

2. Processing-based SLIs:
   - Throughput
   - Freshness (data staleness)
   - Coverage (% of data processed)

3. Storage-based SLIs:
   - Durability
   - Availability of data
```

### SLI Selection Framework

```text
For each user journey:

1. Identify critical interactions
   └── What does the user care about?

2. Map to measurable signals
   └── What can we measure?

3. Define good vs bad
   └── What's acceptable?

4. Validate with users/stakeholders
   └── Does this match expectations?
```

### Good SLI Characteristics

```text
✅ Good SLIs:
- Directly reflect user experience
- Measurable and observable
- Simple to understand
- Actionable when violated

❌ Bad SLIs:
- Internal metrics (CPU, memory)
- Too complex to explain
- Can't be measured reliably
- No clear good/bad threshold
```

### SLI Examples by Service Type

```text
API Service:
- Availability: % non-5xx responses
- Latency: % requests < 200ms
- Quality: % valid responses

Data Pipeline:
- Freshness: % data < 10 min old
- Coverage: % records processed
- Correctness: % matching expected

Storage Service:
- Durability: % objects not lost
- Availability: % successful reads
- Latency: % reads < 50ms

Web Application:
- Page Load: % pages < 3 seconds
- Interactivity: % interactions < 100ms
- Core Web Vitals: LCP, FID, CLS
```

## Setting SLO Targets

### Target Selection Approach

```text
1. Measure current performance:
   What's the baseline?

2. Understand user expectations:
   What do users need?

3. Consider business constraints:
   What's the cost of reliability?

4. Start conservative:
   Better to exceed than miss

5. Iterate based on data:
   Adjust as you learn
```

### SLO Target Guidelines

```text
Service Type        | Availability | Latency (p99)
--------------------|--------------|---------------
Internal APIs       | 99.5%        | 500ms
External APIs       | 99.9%        | 200ms
Payment systems     | 99.99%       | 300ms
Static content      | 99.95%       | 100ms
Batch processing    | 99%          | -

The "nines" scale:
99%    = 7.2 hours/month downtime
99.9%  = 43.8 minutes/month
99.99% = 4.38 minutes/month
```

### Time Windows

```text
Rolling vs Calendar:

Rolling (recommended):
- 30-day rolling window
- Smooth, no cliff effects
- Always relevant

Calendar:
- Monthly reset
- Aligns with business cycles
- Creates "budget reset" behavior

Window selection:
Short (7 days): More sensitive, faster feedback
Long (30 days): More stable, smoother trends
```

## Error Budget Policies

### Policy Components

```text
Error Budget Policy defines:

1. When to take action
   └── Budget thresholds (75%, 50%, 25%, 0%)

2. What actions to take
   └── Freeze features, focus on reliability

3. Who decides
   └── Team, management, escalation path

4. How to recover
   └── Steps to restore budget
```

### Example Policy

```text
Error Budget Policy for OrderService

Budget Remaining | Actions Required
-----------------|------------------------------------------
> 50%            | Normal development, deploy freely
25-50%           | Review deployments, increase testing
10-25%           | Freeze non-critical features
< 10%            | All hands on reliability, no new features
0% (exhausted)   | Postmortem required, leadership review

Escalation:
- Budget < 25%: Alert team lead
- Budget < 10%: Alert engineering manager
- Budget exhausted: Incident declared
```

### Budget Recovery

```text
When budget exhausted:

1. Stop non-critical deployments
2. Focus on stability improvements
3. Conduct thorough postmortems
4. Implement preventive measures
5. Resume normal work when budget recovers

Budget recovers through:
- Time passing (rolling window)
- Improved reliability
- SLO adjustment (if appropriate)
```

## Multi-Window SLOs

### Why Multiple Windows?

```text
Single window problems:
- Long window: Slow to detect issues
- Short window: Too sensitive to spikes

Solution: Multiple windows

Fast burn: Short window (1 hour)
- Detects major outages quickly
- High urgency alerts

Slow burn: Long window (30 days)
- Detects gradual degradation
- Lower urgency, more context
```

### Multi-Window Configuration

```text
Alert configuration:

Fast burn (page immediately):
- 2% of 30-day budget burned in 1 hour
- 5% of 30-day budget burned in 6 hours

Slow burn (ticket):
- 10% of 30-day budget burned in 3 days
- 20% of 30-day budget burned in 7 days

Calculation:
If 30-day budget = 43.2 minutes
2% in 1 hour = 0.864 minutes = 52 seconds of errors
→ Significant outage, page immediately
```

## SLO-Based Alerting

### Alert Design

```text
Traditional alerting:
- CPU > 80% → Alert
- Error rate > 1% → Alert
- Latency > 500ms → Alert
→ Often noisy, may not reflect user impact

SLO-based alerting:
- Error budget burn rate too high → Alert
→ Directly tied to user impact
→ Fewer, more meaningful alerts
```

### Burn Rate Calculation

```text
Burn rate = Rate of budget consumption

If budget should last 30 days:
Normal burn rate = 1x (consuming 3.33%/day)

Fast burn rate = 14.4x
→ Burning 48%/day → 0 in 2 days
→ PAGE: Major incident

Slow burn rate = 3x
→ Burning 10%/day → 0 in 10 days
→ TICKET: Needs attention
```

## Dashboard Design

### Key Metrics to Display

```text
SLO Dashboard Components:

1. Current SLI value
   └── "99.85% availability (target: 99.9%)"

2. Error budget remaining
   └── Bar chart with thresholds

3. Burn rate trend
   └── Line chart over time

4. Time to budget exhaustion
   └── "At current rate: 15 days"

5. Historical SLO compliance
   └── How often have we met SLO?

6. Key error contributors
   └── What's consuming budget?
```

### Visualization Example

```text
┌─────────────────────────────────────────────────────┐
│ OrderService SLO Dashboard                          │
├─────────────────────────────────────────────────────┤
│ Availability SLI: 99.87%     Target: 99.9%    ⚠️   │
│ ██████████████████████████████████████░░░░ 99.87%  │
│                                                     │
│ Error Budget (30 day):                              │
│ ████████████████░░░░░░░░░░░░░░ 55% remaining       │
│ Consumed: 19.4 min / 43.2 min                       │
│                                                     │
│ Burn Rate: 1.3x (slight overage)                   │
│ ────────────────────────────────                   │
│                      ↑ now                          │
│                                                     │
│ Top Budget Consumers:                               │
│ 1. Database timeouts (8.2 min)                      │
│ 2. Payment gateway errors (5.1 min)                 │
│ 3. Rate limiting (3.8 min)                          │
└─────────────────────────────────────────────────────┘
```

## Implementation Checklist

### Getting Started

```text
1. [ ] Identify critical user journeys
2. [ ] Define SLIs for each journey
3. [ ] Set initial SLO targets (conservative)
4. [ ] Implement SLI measurement
5. [ ] Create error budget tracking
6. [ ] Set up burn rate alerts
7. [ ] Create SLO dashboard
8. [ ] Define error budget policy
9. [ ] Socialize with stakeholders
10. [ ] Iterate based on learnings
```

### Common Pitfalls

```text
1. Too many SLOs
   → Focus on 3-5 critical SLOs

2. Unrealistic targets
   → Start achievable, tighten over time

3. Internal metrics as SLIs
   → Use user-facing metrics

4. No error budget policy
   → Policy makes SLOs actionable

5. Alert on SLI directly
   → Alert on burn rate instead
```

## Best Practices

```text
1. User-centric SLIs
   Measure what users experience

2. Conservative initial targets
   Better to exceed than miss

3. Documented error budget policy
   Everyone knows the rules

4. Regular SLO reviews
   Quarterly review and adjustment

5. Blameless culture
   Focus on learning, not blame

6. Automated tracking
   SLI/SLO calculation must be reliable
```

## Related Skills

- `observability-patterns` - Metrics and monitoring
- `distributed-tracing` - Trace-based SLIs
- `incident-response` - Using SLOs in incidents
