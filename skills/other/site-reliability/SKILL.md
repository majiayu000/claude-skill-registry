---
name: site-reliability
version: 0.1.0
description: >
  Use this skill when implementing SRE practices, defining error budgets, reducing
  toil, planning capacity, or improving service reliability. Triggers on SRE,
  error budgets, SLOs, SLAs, toil automation, incident management, postmortems,
  on-call rotation, capacity planning, chaos engineering, and any task requiring
  reliability engineering decisions.
category: engineering
tags: [sre, reliability, error-budgets, toil, capacity, incident-management]
recommended_skills: [observability, incident-management, chaos-engineering, performance-engineering]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# Site Reliability Engineering

SRE is the discipline of applying software engineering to operations problems. It
replaces ad-hoc ops work with principled systems: reliability targets backed by error
budgets, toil replaced by automation, and incidents treated as system failures rather
than human ones. This skill covers the full SRE lifecycle - from defining SLOs through
capacity planning and progressive delivery - as practiced by teams operating
production systems at scale. Designed for engineers moving from "keep the lights on"
to systematic reliability ownership.

---

## When to use this skill

Trigger this skill when the user:
- Needs to define or revise SLOs, SLIs, or SLAs for a service
- Is calculating or acting on an error budget
- Wants to identify, measure, or automate toil
- Is running or writing a postmortem
- Is designing or improving an on-call rotation
- Is forecasting capacity needs or planning a load test
- Is designing a rollout strategy (canary, blue/green, progressive)

Do NOT trigger this skill for:
- Pure infrastructure provisioning without a reliability framing (use a Docker/K8s skill)
- Application performance optimization without an SLO context (use a performance-engineering skill)

---

## Key principles

1. **Embrace risk with error budgets** - 100% reliability is neither achievable nor
   desirable. Every extra nine of availability comes at a cost: slower feature velocity,
   more complex systems, higher operational burden. An error budget makes the
   trade-off explicit: spend budget on risk-taking (deploys, experiments), save it
   when reliability is threatened.

2. **Eliminate toil** - Toil is work that is manual, repetitive, automatable, reactive,
   and scales with service growth without producing lasting value. Every hour of toil is
   an hour not spent on reliability improvements. The goal is not zero toil (some is
   unavoidable) but continuous reduction.

3. **SLOs are the contract** - SLOs align engineering and business on what reliability
   is worth. They prevent both over-engineering ("five nines or nothing") and
   under-investing ("it mostly works"). Write SLOs before writing on-call runbooks;
   the SLO defines what warrants waking someone up.

4. **Blameless postmortems** - Systems fail, not people. Blaming individuals creates
   an environment where engineers hide problems and avoid risk. Blameless postmortems
   surface systemic issues and produce durable fixes. The goal is learning, not
   accountability theater.

5. **Automate yourself out of a job** - The SRE charter is to automate operations
   work until the team's operational load is below 50% of their time. The remaining
   capacity is reserved for reliability engineering that makes the next incident less
   likely or less severe.

---

## Core concepts

### SLI / SLO / SLA hierarchy

```
SLA (Service Level Agreement)
  - External contract with customers. Breach triggers penalties.
  - Set conservatively: your internal SLO must be tighter than your SLA.

  SLO (Service Level Objective)
    - Internal target. Drives alerting, error budgets, and engineering decisions.
    - Typically SLO = SLA - 0.5 to 1 percentage point headroom.

    SLI (Service Level Indicator)
      - The actual measurement. A ratio: good events / total events.
      - Example: (requests completing < 300ms) / (all requests)
```

**Rule of thumb**: Define one availability SLI and one latency SLI per user-facing
service. Add correctness SLIs for data pipelines or financial systems.

### Error budget mechanics

```
Error budget = 1 - SLO target
  99.9% SLO  -> 0.1% budget  -> 43.8 min/month at risk
  99.5% SLO  -> 0.5% budget  -> 3.65 hours/month at risk

Budget consumed = (bad events this window) / (total events this window)
Budget remaining = budget_total - budget_consumed
```

**Burn rate** = observed error rate / allowed error rate. A burn rate of 1 means you
are spending budget at exactly the expected pace. A burn rate of 14.4 on a 30-day
window means the budget is gone in 50 hours.

**Budget policy** (what to do when budget is threatened):

| Budget remaining | Action |
|---|---|
| > 50% | Normal feature velocity, deploys allowed |
| 25-50% | Review recent changes, increase monitoring |
| 10-25% | Freeze non-essential deploys, focus on stability |
| < 10% | Feature freeze, all hands on reliability work |

### Toil definition

Toil has all of these properties - if even one is missing, it may be legitimate work:

- **Manual**: A human is in the loop doing repetitive keystrokes
- **Repetitive**: Done more than once with the same steps
- **Automatable**: A script or system could do it
- **Reactive**: Triggered by a system event, not proactive engineering
- **No lasting value**: Executing it does not improve the system; it just holds it steady
- **Scales with load**: More traffic, more toil (a danger sign)

### Incident severity levels

| Severity | Customer impact | Response | Example |
|---|---|---|---|
| SEV1 | Complete outage or data loss | Immediate page, war room | Payment service down |
| SEV2 | Degraded core functionality | Page on-call | 20% of requests erroring |
| SEV3 | Minor degradation, workaround exists | Ticket, next business day | Slow dashboard loads |
| SEV4 | Cosmetic issue or internal tool | Backlog | Wrong label in admin UI |

### On-call best practices

- Rotate weekly; never longer than two weeks without a break
- Guarantee engineers sleep: no P1 pages between 10pm-8am without escalation
- Track on-call load: pages per shift, time-to-ack, total hours interrupted
- Every on-call shift ends with a handoff: active incidents, lingering alerts, context
- Budget 20-30% of the next sprint for on-call follow-up work

---

## Common tasks

### Define SLOs for a service

**Step 1: Choose the right SLIs.** Start from user journeys, not technical metrics.

| User journey | SLI type | Measurement |
|---|---|---|
| "Page loads fast" | Latency | requests_under_300ms / total_requests |
| "API calls succeed" | Availability | non_5xx_responses / total_responses |
| "Data is correct" | Correctness | correct_outputs / total_outputs |
| "Writes persist" | Durability | successful_writes_verified / total_writes |

**Step 2: Set targets using historical data.**

```
1. Pull 30 days of your current SLI measurements
2. Find your current actual performance (e.g., 99.85% availability)
3. Set SLO slightly below current performance (e.g., 99.7%)
4. Tighten over time as you improve reliability
```

Never set an SLO tighter than your best recent 30-day window without a
corresponding reliability investment plan.

**Step 3: Choose the window.** Rolling 30-day windows are standard. They smooth
spikes but respond to sustained degradation. Avoid calendar month windows - they reset
budgets on the 1st regardless of what happened on the 31st.

**Step 4: Define measurement exclusions.** Planned maintenance, dependencies outside
your control, and client errors (4xx) typically excluded from SLI calculations.

### Calculate and track error budgets

**Burn rate alerting (recommended over threshold alerting):**

```
Fast burn alert (page immediately):
  Condition: burn_rate > 14.4 for 5 minutes
  Meaning:   At this rate, 30-day budget exhausted in ~50 hours
  Severity:  SEV2, page on-call

Slow burn alert (ticket, investigate):
  Condition: burn_rate > 3 for 60 minutes
  Meaning:   Budget exhausted in ~10 days if trend continues
  Severity:  SEV3, create ticket

Budget depletion alert (SEV1 escalation trigger):
  Condition: budget_remaining < 10%
  Action:    Feature freeze, reliability sprint
```

**Multi-window alerting** catches both fast spikes and slow degradation:
- 5-minute window: catches fast burns (major incident)
- 1-hour window: catches slow burns (creeping degradation)
- Both windows alerting together = high-confidence page

**Budget depletion actions:**
1. Stop all non-essential deploys
2. Pull toil-reduction and reliability items from the backlog
3. Review the postmortem queue for unresolved action items
4. Document the decision with date and budget percentage in your incident tracker

### Identify and reduce toil

**Toil taxonomy** - classify before automating:

| Category | Examples | Priority |
|---|---|---|
| Interrupt-driven | Restarting crashed pods, clearing queues | High - on-call tax |
| Regular manual ops | Weekly capacity checks, certificate renewals | Medium - scheduled work |
| Deploy ceremony | Manual release steps, environment promotion | High - blocks velocity |
| Data cleanup | Fixing bad records, reconciliation jobs | Medium - correctness risk |
| Access management | Provisioning accounts, rotating credentials | High - security risk |

**Automation prioritization matrix:**

```
                 HIGH FREQUENCY
                      |
  Quick to            |              Slow to
  automate            |              automate
                      |
 AUTOMATE FIRST  -----+-----  SCHEDULE: PLAN PROJECT
                      |
                      |
 AUTOMATE WHEN   -----+-----  ACCEPT OR ELIMINATE
  CONVENIENT          |
                      |
                 LOW FREQUENCY
```

Measure toil before and after automation: track hours/week per category per engineer.
If toil is growing, the automation is not keeping pace with service growth.

### Run a blameless postmortem

**When to hold one:** Every SEV1. Every SEV2 with customer-visible impact. Any
incident that consumed more than 4 hours of on-call time. Recurring SEV3s from the
same root cause.

**Timeline (24-48 hours after resolution):**

```
Day 0 (during incident): Designate incident commander, keep a timeline in a shared doc
Day 1 (next morning):    Assign postmortem owner, schedule meeting within 48 hours
Day 2 (postmortem):      60-90 min facilitated session
Day 3:                   Draft published internally for 24-hour comment period
Day 5:                   Final version published, action items entered in tracker
```

**The five questions that drive every postmortem:**

1. What happened and when? (timeline)
2. Why did it happen? (root cause - ask "why" five times)
3. Why did we not detect it sooner? (detection gap)
4. What slowed down the response? (mitigation gap)
5. What prevents recurrence? (action items)

**Action item rules:** Each item must have an owner, a due date, and a measurable
definition of done. "Improve monitoring" is not an action item. "Add burn-rate alert
for payments-api availability SLO by 2025-Q3" is.

See `references/postmortem-template.md` for the full template with example entries
and facilitation guide.

### Design on-call rotation

**Rotation structure:**

```
Primary on-call:   First responder. Acks within 15 min, mitigates or escalates.
Secondary on-call: Backup if primary misses ack within 15 min.
Escalation path:   Engineering manager -> Director -> Incident commander (for SEV1 only)
```

**Runbook requirements** (every alert must have one):

- Symptom: what the alert is telling you
- Impact: who is affected and how severely
- Steps: numbered investigation and mitigation steps
- Escalation: who to call if steps do not resolve it
- Context: links to dashboards, service documentation, past incidents

**Handoff process** (end of each on-call rotation):

1. Document any open or lingering issues
2. List any alerts that fired but did not page (worth reviewing)
3. Share known fragile areas or upcoming risky changes
4. Review toil hours and open action items with incoming on-call

**Health metrics for on-call load:**

| Metric | Target | Alert threshold |
|---|---|---|
| Pages per on-call week | < 5 | > 10 |
| Pages outside business hours | < 2/week | > 5/week |
| Time-to-ack (P1) | < 5 min | > 15 min |
| Toil percentage of on-call time | < 50% | > 70% |

### Plan capacity

**Demand forecasting approach:**

```
1. Baseline: measure current peak RPS, CPU, memory, storage
2. Growth rate: calculate month-over-month traffic growth (last 6 months)
3. Project forward: apply growth rate to 6-month and 12-month horizons
4. Add headroom: 30-50% above projected peak for burst capacity
5. Trigger threshold: the utilization level that kicks off provisioning
```

**Load testing before capacity decisions:**

- Define the traffic shape (ramp, steady state, spike)
- Test to 150% of expected peak - find the breaking point before users do
- Measure: latency distribution at load, error rate at load, resource utilization
- Identify the bottleneck (CPU, DB connections, memory) before scaling the wrong thing

**Headroom planning table:**

| Component | Trigger utilization | Target utilization | Action |
|---|---|---|---|
| Compute (CPU) | > 70% sustained | 40-60% | Horizontal scale |
| Memory | > 80% | 50-70% | Vertical scale or tune GC |
| Database (connections) | > 80% pool use | 50-70% | Connection pooler, scale up |
| Storage | > 75% | < 60% | Provision more, archive old data |
| Network throughput | > 70% | < 50% | Scale or upgrade links |

**Cost vs reliability trade-off:** Headroom is expensive. Justify each component's
target with an SLO - a 99.9% availability SLO for a stateless service does not
require the same headroom as a 99.99% SLO for a payment processor.

### Implement progressive rollouts

**Rollout ladder:**

```
0.1% canary (10 min)
  -> 1% (30 min, review metrics)
  -> 5% (1 hour)
  -> 25% (1 hour)
  -> 50% (1 hour)
  -> 100%
```

**Canary analysis - automatic promotion/rollback criteria:**

| Signal | Rollback if | Promote if |
|---|---|---|
| Error rate | Canary > baseline + 0.5% | Canary <= baseline + 0.1% |
| p99 latency | Canary > baseline * 1.2 | Canary <= baseline * 1.05 |
| SLO burn rate | Canary burn rate > 5x | Canary burn rate <= 2x |
| CPU/Memory | Canary > baseline * 1.3 | Within 10% of baseline |

**Automated rollback triggers:** Instrument your CD pipeline to roll back
automatically when error rate or latency breaches the canary threshold. Do not
rely on humans to catch canary regressions - the whole point is to automate the
decision. If your deployment tool does not support automated rollback, treat that
as a toil item to fix.

**Feature flags vs canary:** Canary deploys test infrastructure changes (binary,
container, config). Feature flags test product changes (code paths). Use both.
Separate the risk of deploying new infrastructure from the risk of activating new
behavior.

---

## Gotchas

1. **SLO window reset on the 1st creates budget gaming** - Calendar month windows reset error budget on the 1st regardless of what happened on the 31st. Teams learn to push risky deploys right after reset. Use rolling 30-day windows which are always live and cannot be gamed.

2. **Burn rate alerts with a single window produce too much noise** - A 5-minute burn rate alert alone generates pages for transient spikes that self-recover. Multi-window alerting (5-minute AND 1-hour both elevated) dramatically reduces false positives while keeping sensitivity to real incidents.

3. **Toil metrics without a reduction target are just bookkeeping** - Measuring toil hours without committing to a reduction target and a sprint allocation to address it creates awareness without action. The measure only has value if it gates a quarterly automation investment.

4. **Canary rollout with no automated rollback is manual canary** - A canary that requires a human to notice the error rate spike and manually roll back is not a canary - it is a staged rollout with extra steps. Automated rollback on threshold breach is the defining property; without it, the safety benefit is largely absent.

5. **On-call runbooks that say "escalate to engineering"** - A runbook whose resolution step is "page someone else" does not reduce on-call burden; it just shifts it. Every runbook must include at least one concrete mitigation step the on-call can take before escalating.

---

## Anti-patterns / common mistakes

| Mistake | Why it is wrong | What to do instead |
|---|---|---|
| Setting SLOs without historical data | Targets become aspirational fiction, not engineering constraints | Measure current performance first, set SLO at or slightly below it |
| Alerting on resource utilization not SLOs | CPU at 90% may not affect users; 1% error rate definitely does | Alert on SLO burn rate; use resource metrics for capacity planning only |
| Blameful postmortems | Engineers hide problems, avoid risky-but-necessary changes | Explicitly state "no blame" in the template; focus every question on systems |
| Counting toil in hours but not automating it | Creates awareness without action | Budget one sprint per quarter specifically for toil reduction |
| Infinite error budget freezes | Teams freeze deploys forever, killing velocity | Define explicit budget policy with percentage thresholds and time-bounded freezes |
| On-call without runbooks | Every incident requires heroics; knowledge stays in individuals | Treat "alert without runbook" as a blocker; write the runbook during the incident |

---

## References

For detailed guidance on specific domains, load the relevant file from `references/`:

- `references/postmortem-template.md` - full postmortem template with example entries, facilitation guide, and action item tracker

Only load a references file when the current task requires it.

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
