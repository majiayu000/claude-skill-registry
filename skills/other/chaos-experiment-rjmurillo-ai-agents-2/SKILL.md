---
name: chaos-experiment
version: 1.0.0
model: claude-sonnet-4-5
description: Design and document chaos engineering experiments. Guide steady state baseline, hypothesis formation, failure injection plans, and results analysis. Use for resilience testing, game days, failure injection experiments, and building confidence in system stability.
license: MIT
---

# Chaos Experiment Designer

Design rigorous chaos engineering experiments that build confidence in system resilience.

## Triggers

- `chaos experiment`
- `test resilience`
- `failure injection`
- `game day`
- `chaos engineering`

## Quick Reference

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Scope | Define system boundaries and objectives | System under test, success criteria |
| 2. Baseline | Establish steady state metrics | Quantified normal behavior |
| 3. Hypothesis | Form falsifiable hypothesis | Clear prediction statement |
| 4. Injection | Design failure scenarios | Injection plan with blast radius |
| 5. Execute | Run controlled experiment | Observation log |
| 6. Analyze | Compare actual vs expected | Findings and action items |

## When to Use

Use this skill when:

- Planning a game day or failure injection exercise
- Building confidence in system resilience before production launch
- Investigating whether auto-scaling, circuit breakers, or failover mechanisms work as designed
- After a real incident, to validate that fixes prevent recurrence

Use [threat-modeling](../threat-modeling/SKILL.md) instead when:

- Identifying security threats (not resilience)
- Evaluating attack surfaces rather than failure modes

Use [pre-mortem](../pre-mortem/SKILL.md) instead when:

- Identifying project risks (not infrastructure failures)
- Working at planning stage before any system exists

## Core Principles

Chaos engineering is the discipline of experimenting on a system to build confidence in its capability to withstand turbulent conditions in production.

### The Five Principles

1. **Steady State Focus**: Measure observable outputs (throughput, error rates, latency percentiles), not internal metrics
2. **Real-World Variables**: Introduce disruptions that simulate actual failure modes
3. **Production Testing**: Experiment on live systems with real traffic patterns
4. **Continuous Automation**: Build experiments into CI/CD pipelines
5. **Blast Radius Containment**: Minimize customer impact through careful scoping

## Process

### Phase 1: Scope Definition

Define the experiment boundaries.

**Inputs**: System architecture, historical incidents, monitoring data

**Questions to Answer**:

1. What system or subsystem will we test?
2. What is our business justification for this experiment?
3. Who are the stakeholders and who must approve?
4. What is the maximum acceptable customer impact?
5. What time window is safest for execution?

**Output**: Scoped experiment definition with stakeholder sign-off

### Phase 2: Establish Baseline

Quantify normal system behavior.

**Collect Steady State Metrics**:

| Metric Category | Examples | Collection Period |
|-----------------|----------|-------------------|
| Throughput | Requests/second, transactions/minute | 7-30 days |
| Error Rates | 4xx rate, 5xx rate, exception count | 7-30 days |
| Latency | P50, P95, P99 response times | 7-30 days |
| Resource | CPU%, Memory%, Disk I/O, Network I/O | 7-30 days |
| Business | Orders/hour, active sessions, conversion rate | 7-30 days |

**Define Tolerance Thresholds**:

- Green: Within normal variance (baseline +/- 1 standard deviation)
- Yellow: Elevated but acceptable (baseline +/- 2 standard deviations)
- Red: Unacceptable degradation (exceeds 2 standard deviations)

**Output**: Baseline document with metric values and thresholds

### Phase 3: Form Hypothesis

Create a falsifiable hypothesis.

**Hypothesis Template**:

```text
Given [system in steady state],
When [specific failure is injected],
Then [system behavior remains within tolerance]
Because [specific resilience mechanism exists].
```

**Example Hypotheses**:

- "Given our API gateway in steady state, when we terminate 50% of backend instances, then P99 latency remains under 500ms because auto-scaling will provision replacements within 60 seconds."
- "Given our payment service in steady state, when we introduce 500ms network latency to the database, then order completion rate remains above 99% because connection pooling and retry logic handle transient delays."

**Hypothesis Quality Checklist**:

- [ ] Specific failure mode identified
- [ ] Quantifiable success criteria defined
- [ ] Underlying resilience mechanism named
- [ ] Timeframe for expected recovery stated

**Output**: Documented hypothesis with measurable predictions

### Phase 4: Design Injection Plan

Plan the controlled failure injection.

**Common Failure Categories**:

| Category | Examples | Tools |
|----------|----------|-------|
| Instance Failure | Kill process, terminate VM, evict pod | chaos-monkey, kill, kubectl delete |
| Network | Partition, latency, packet loss, DNS failure | tc, iptables, toxiproxy, chaos-mesh |
| Resource Exhaustion | CPU spike, memory pressure, disk fill | stress-ng, dd, memory hogs |
| Dependency | External service unavailable, slow response | fault injection proxy, mock services |
| Time | Clock skew, NTP failure | faketime, chrony manipulation |
| State | Data corruption, cache invalidation | Custom scripts |

**Injection Plan Elements**:

1. **Failure Type**: Precise description of what will be broken
2. **Injection Method**: Tool and exact commands to use
3. **Scope**: Which instances/services/regions affected
4. **Duration**: How long the failure persists
5. **Ramp-up**: Gradual vs immediate injection
6. **Rollback**: How to instantly restore normal operation

**Blast Radius Containment**:

- Start with smallest possible scope (single instance)
- Use canary deployment pattern for experiments
- Define automatic abort criteria
- Have rollback ready before starting
- Notify on-call before and after

**Output**: Detailed injection plan with rollback procedures

### Phase 5: Execute Experiment

Run the controlled experiment.

**Pre-Execution Checklist**:

- [ ] Stakeholders notified
- [ ] On-call team aware
- [ ] Monitoring dashboards ready
- [ ] Rollback procedure tested
- [ ] Customer support briefed (for production)
- [ ] Automatic abort criteria configured

**During Execution**:

1. Record experiment start timestamp
2. Monitor all baseline metrics in real-time
3. Log observations with timestamps
4. If abort criteria met, execute rollback immediately
5. Record experiment end timestamp

**Observation Log Format**:

```text
[HH:MM:SS] - [Metric/Event]: [Value/Description]
[00:00:00] - Experiment started: Injected 500ms latency to database connection
[00:00:15] - P99 latency: 450ms -> 650ms
[00:00:30] - Circuit breaker: OPEN on database connection pool
[00:01:00] - Retry queue depth: 0 -> 247
[00:01:30] - Auto-recovery initiated
[00:02:00] - P99 latency: 650ms -> 480ms
[00:02:30] - Circuit breaker: CLOSED
[00:03:00] - Experiment ended: Removed latency injection
```

**Output**: Timestamped observation log

### Phase 6: Analyze Results

Compare actual behavior against hypothesis.

**Analysis Questions**:

1. Did system behavior stay within tolerance thresholds?
2. Did resilience mechanisms activate as expected?
3. What was the actual recovery time?
4. Were there any unexpected cascading effects?
5. Did monitoring and alerting work correctly?

**Verdict Options**:

| Verdict | Meaning | Action |
|---------|---------|--------|
| VALIDATED | Hypothesis confirmed | Document and expand scope |
| INVALIDATED | Hypothesis falsified | File bugs, prioritize fixes |
| INCONCLUSIVE | Unable to determine | Refine experiment design |

**Finding Categories**:

- **Resilience Strengths**: Mechanisms that worked as designed
- **Weaknesses Discovered**: Gaps in resilience that need fixing
- **Monitoring Gaps**: Missing visibility during incident
- **Documentation Gaps**: Runbooks or procedures that need updating
- **Unexpected Behaviors**: System responses not predicted

**Output**: Analysis document with prioritized action items

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `generate_experiment.py` | Create experiment document from inputs | `python scripts/generate_experiment.py --name "API Gateway Resilience"` |
| `validate_experiment.py` | Validate experiment document completeness | `python scripts/validate_experiment.py path/to/experiment.md` |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General failure |
| 2 | Invalid arguments |
| 10 | Validation failure (missing required sections) |

## Output Directory

Experiments are saved to: `.agents/chaos/`

```text
.agents/chaos/
  YYYY-MM-DD-experiment-name.md
  YYYY-MM-DD-experiment-name-results.md
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Testing in staging only | Production has different traffic patterns | Start small in production |
| No rollback plan | Cannot recover if things go wrong | Define rollback before starting |
| Vague hypothesis | Cannot determine success | Use quantifiable predictions |
| Measuring internal metrics only | Do not reflect customer experience | Focus on observable outputs |
| Big bang experiments | Blast radius too large | Start with smallest scope |
| No baseline | Cannot compare results | Collect 7+ days of metrics first |
| Skipping stakeholder buy-in | Creates political problems | Get approval before execution |

## Templates

### Experiment Document Template

Use `templates/experiment-template.md` or generate with:

```bash
python scripts/generate_experiment.py \
  --name "Database Failover Resilience" \
  --system "Payment Service" \
  --owner "Jane Smith" \
  --output .agents/chaos/
```

## Verification Checklist

Before executing any chaos experiment:

- [ ] Scope clearly defined with business justification
- [ ] Baseline metrics collected (minimum 7 days)
- [ ] Hypothesis is falsifiable with quantifiable criteria
- [ ] Injection plan includes specific tools and commands
- [ ] Blast radius is contained to acceptable scope
- [ ] Rollback procedure is documented and tested
- [ ] Stakeholders have approved the experiment
- [ ] On-call team is aware of timing
- [ ] Monitoring dashboards are ready
- [ ] Results template is prepared

## Extension Points

1. **Failure Categories**: Add new failure types to Phase 4 table
2. **Tools Integration**: Extend scripts to integrate with chaos-mesh, Gremlin, LitmusChaos
3. **Automation**: Integrate with CI/CD for continuous chaos testing
4. **Metrics Sources**: Add integrations for Prometheus, Datadog, New Relic
5. **Scheduling**: Add calendar integration for recurring game days

## Related Resources

- [Principles of Chaos Engineering](https://principlesofchaos.org/)
- Chaos Monkey (Netflix)
- Chaos Mesh (CNCF)
- LitmusChaos (CNCF)
- Gremlin (Commercial)

## Related Skills

| Skill | Relationship |
|-------|--------------|
| security | Security review for production experiments |
| devops | CI/CD integration for automated chaos |
| qa | Test strategy alignment |
| analyst | Root cause analysis of findings |
