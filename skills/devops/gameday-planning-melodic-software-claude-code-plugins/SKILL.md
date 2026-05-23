---
name: gameday-planning
description: Use when planning GameDay exercises, designing failure scenarios, or conducting chaos drills. Covers GameDay preparation, execution, and follow-up.
allowed-tools: Read, Glob, Grep
---

# GameDay Planning

Comprehensive guide for planning and executing GameDay exercises - organized chaos drills that test system resilience and incident response.

## When to Use This Skill

- Planning GameDay exercises
- Designing failure scenarios
- Preparing teams for chaos experiments
- Running disaster recovery drills
- Improving incident response readiness

## What is a GameDay?

```text
GameDay = Planned chaos exercise for your systems

Like a fire drill, but for infrastructure:
- Scheduled in advance
- Controlled environment
- Practice for real incidents
- Learn and improve

Not chaos engineering:
- GameDay: Scheduled team exercise
- Chaos engineering: Continuous experiments

GameDays include:
- Failure injection
- Incident response practice
- Team coordination
- Runbook validation
```

## GameDay Types

### By Scope

```text
1. Component GameDay
   └── Single service or component
   └── Focused scenarios
   └── 2-4 hours

2. Service GameDay
   └── Multiple related services
   └── Integration scenarios
   └── Half day

3. Full System GameDay
   └── Complete system
   └── Disaster scenarios
   └── Full day

4. Cross-Team GameDay
   └── Multiple teams involved
   └── Complex scenarios
   └── 1-2 days
```

### By Objective

```text
1. Resilience validation
   └── Does the system handle failures?

2. Recovery practice
   └── Can we restore from backup?

3. Incident response training
   └── How well do we coordinate?

4. Runbook validation
   └── Do our runbooks work?

5. Capacity testing
   └── What happens under load?
```

## Planning Phase

### Timeline Overview

```text
Week -4: Initial planning
├── Define objectives
├── Identify stakeholders
└── Draft scenario ideas

Week -3: Scenario design
├── Detail failure scenarios
├── Define success criteria
└── Identify risks

Week -2: Preparation
├── Review with stakeholders
├── Prepare monitoring
├── Update runbooks
└── Brief participants

Week -1: Final prep
├── Confirm participants
├── Test monitoring
├── Walkthrough scenarios
└── Prepare rollback plans

Day of: Execute
├── Pre-GameDay briefing
├── Run scenarios
├── Document observations
└── Hot debrief
```

### Objective Setting

```text
Good objectives:
- "Validate failover to secondary region works < 5 minutes"
- "Confirm team can diagnose database issues using runbooks"
- "Test load balancer behavior when 50% of nodes fail"

Bad objectives:
- "See what breaks" (too vague)
- "Test everything" (too broad)
- "Find all bugs" (unrealistic)

SMART objectives:
Specific: Clear scenario
Measurable: Defined success criteria
Achievable: Within team capability
Relevant: Tests real risks
Time-bound: Fits in GameDay
```

### Scenario Design

```text
Scenario template:

Name: [Descriptive name]
Type: [Infrastructure/Application/Data/Process]
Duration: [Expected time]

Objective:
What are we testing?

Hypothesis:
"When [fault], the system will [expected behavior]"

Setup:
1. [Pre-condition 1]
2. [Pre-condition 2]

Execution:
1. [Injection step 1]
2. [Injection step 2]

Expected Outcome:
- [Metric] should [behavior]
- [Alert] should [fire/not fire]
- [Recovery] should [happen]

Success Criteria:
□ [Criterion 1]
□ [Criterion 2]

Abort Conditions:
- [Condition] → Stop immediately
- [Condition] → Pause and assess

Rollback Steps:
1. [Rollback step 1]
2. [Rollback step 2]
```

### Common Scenarios

```text
Infrastructure:
□ Kill primary database instance
□ Network partition between zones
□ Full disk on critical service
□ Memory exhaustion
□ Certificate expiration

Application:
□ Deploy bad configuration
□ Overwhelm with traffic
□ Corrupt cache entries
□ Exhaust connection pool
□ API dependency failure

Data:
□ Restore from backup
□ Data corruption detection
□ Replication lag
□ Schema migration failure

Process:
□ Key team member unavailable
□ Credentials rotation
□ Access revocation
□ Runbook-only resolution
```

## Preparation Phase

### Stakeholder Communication

```text
Communication plan:

Leadership:
- What: GameDay overview, risks, benefits
- When: Week -3 (approval)
- How: Meeting + document

Participating teams:
- What: Detailed plan, roles, expectations
- When: Week -2 (kickoff)
- How: Meeting + documentation

Adjacent teams:
- What: Notification, potential impact
- When: Week -1
- How: Email + calendar block

On-call:
- What: Extra vigilance, escalation paths
- When: Day before
- How: Briefing + runbook
```

### Participant Briefing

```text
Briefing contents:

1. Objectives
   What are we testing and why?

2. Roles
   Who does what during GameDay?

3. Schedule
   Timeline and scenario order

4. Ground rules
   What's allowed, what's not

5. Safety
   Kill switches, abort conditions

6. Communication
   Channels, updates, escalation

7. Questions
   Clear up any confusion
```

### Monitoring Preparation

```text
Before GameDay:

1. Verify dashboards work
   - All relevant metrics visible
   - Baselines understood

2. Configure extra alerting
   - GameDay-specific alerts
   - Lower thresholds if needed

3. Prepare queries
   - Log queries ready
   - Trace searches prepared

4. Test recording
   - Screen recording if needed
   - Metrics export configured

5. Clear noise
   - Suppress known alerts
   - Reduce background chatter
```

### Safety Measures

```text
Required safety measures:

Kill switches:
- Immediate stop for each scenario
- Multiple people can trigger
- Tested before GameDay

Blast radius limits:
- Maximum affected users/traffic
- Automatic enforcement
- Clear escalation if exceeded

Rollback plans:
- Documented for each scenario
- Tested rollback procedures
- Time-limited scenarios

Communication:
- Dedicated channel
- Clear "STOP" command
- Status page ready to update

Customer protection:
- Synthetic traffic if possible
- Canary approach
- Quick customer comm ready
```

## Execution Phase

### Day-of Structure

```text
Typical GameDay schedule:

08:00 - Pre-GameDay briefing
        └── Review objectives, roles, safety

08:30 - Monitoring baseline
        └── Capture normal state

09:00 - Scenario 1
        └── Execute, observe, document

10:30 - Break + quick debrief

11:00 - Scenario 2
        └── Execute, observe, document

12:30 - Lunch break

13:30 - Scenario 3
        └── Execute, observe, document

15:00 - Scenario 4 (if time)

16:00 - Hot debrief
        └── Initial observations

16:30 - Cleanup
        └── Ensure all reverted
```

### Roles During Execution

```text
GameDay Lead:
- Runs the overall exercise
- Makes go/no-go decisions
- Controls pacing
- Manages safety

Scenario Executor:
- Injects faults
- Monitors injection
- Has kill switch
- Reports status

Observers:
- Watch system behavior
- Document findings
- Note unexpected events
- Track metrics

Incident Responders:
- Act as if real incident
- Follow runbooks
- Practice coordination
- Don't know scenarios in advance (optional)

Scribe:
- Records timeline
- Documents decisions
- Captures quotes
- Notes action items
```

### Documentation During

```text
Timeline template:

[TIME] [ACTOR] [ACTION/OBSERVATION]

09:00 GameDay Lead: Starting Scenario 1 - DB failover
09:01 Executor: Triggered primary DB shutdown
09:02 Observer: Alert fired: DB connection errors
09:03 Observer: Failover initiated automatically
09:05 Observer: Secondary promoted to primary
09:07 Responder: Services reconnected
09:10 Observer: Error rate returning to normal
09:12 GameDay Lead: Scenario 1 complete - success

Capture:
- Exact times
- Who did what
- System responses
- Deviations from expected
- Interesting observations
```

### Handling Real Incidents

```text
If real incident occurs during GameDay:

1. STOP GameDay immediately
   "GameDay paused - real incident"

2. Assess the real incident
   Is it related to GameDay?

3. Revert any GameDay changes
   If potentially contributing

4. Handle real incident
   Normal incident process

5. Decide on continuation
   Resume or reschedule GameDay?

Always prioritize real incidents over GameDay.
```

## Follow-Up Phase

### Hot Debrief

```text
Immediately after GameDay:

Duration: 30-60 minutes
Participants: All GameDay participants

Agenda:
1. What happened? (5 min per scenario)
   - Timeline walk-through
   - Key observations

2. What worked well?
   - Celebrate successes
   - Note effective practices

3. What didn't work?
   - Issues discovered
   - Gaps in tools/process

4. Initial action items
   - Quick fixes
   - Further investigation needed

5. Next steps
   - Postmortem schedule
   - Owner assignments
```

### Formal Postmortem

```text
Within 1 week of GameDay:

GameDay Postmortem

Executive Summary
Brief overview of objectives, execution, outcomes

Scenarios Executed
| Scenario | Outcome | Key Findings |
|----------|---------|--------------|
| DB failover | Success | 3 min recovery |
| Network partition | Partial | Manual intervention needed |

Detailed Findings

Scenario 1: Database Failover
- Hypothesis: Automatic failover < 5 min
- Result: CONFIRMED (3 min actual)
- Observations: [Details]

Scenario 2: Network Partition
- Hypothesis: Services continue with degraded mode
- Result: PARTIALLY CONFIRMED
- Gap: Service X didn't handle gracefully
- Observations: [Details]

Action Items
| Action | Owner | Priority | Due Date |
|--------|-------|----------|----------|
| Fix Service X partition handling | @engineer | P1 | 2024-02-01 |
| Update runbook for DB failover | @oncall | P2 | 2024-02-15 |

Recommendations for Next GameDay
- [Suggestion 1]
- [Suggestion 2]
```

### Action Item Tracking

```text
Every action item needs:
- Clear description
- Single owner
- Priority level
- Due date
- Definition of done

Track in:
- Issue tracker
- Dedicated dashboard
- Regular review meetings

Don't let action items languish.
The point is to improve.
```

## Best Practices

### Planning

```text
1. Start small
   First GameDay should be simple

2. Clear objectives
   Know what you're testing

3. Stakeholder buy-in
   Get approval and support

4. Thorough preparation
   Don't rush the prep work

5. Documented scenarios
   Written plans, not in heads
```

### Execution

```text
1. Safety first
   Kill switches ready

2. Communicate constantly
   Everyone knows what's happening

3. Document everything
   You'll forget otherwise

4. Stay on schedule
   Don't let scenarios run over

5. Be flexible
   Adapt to unexpected situations
```

### Follow-Up

```text
1. Debrief immediately
   Hot debrief same day

2. Formal postmortem
   Within a week

3. Track action items
   Don't let them die

4. Share learnings
   Spread knowledge broadly

5. Plan the next one
   Make it a regular practice
```

## Common Pitfalls

```text
Pitfall: Scope creep
Fix: Strict scenario limits, time boxes

Pitfall: Insufficient preparation
Fix: Checklists, dry runs

Pitfall: No safety measures
Fix: Required kill switches, abort criteria

Pitfall: Skipping documentation
Fix: Dedicated scribe, templates

Pitfall: Orphaned action items
Fix: Tracked, owned, reviewed

Pitfall: Infrequent GameDays
Fix: Quarterly schedule, smaller scope
```

## Maturity Progression

```text
Level 1: Ad-hoc
- First GameDay
- Simple scenarios
- Manual execution

Level 2: Regular
- Quarterly GameDays
- Multiple scenarios
- Basic automation

Level 3: Integrated
- Monthly GameDays
- Complex scenarios
- Good documentation
- Action item tracking

Level 4: Continuous
- Weekly smaller drills
- Quarterly large GameDays
- Automated scenarios
- Metrics-driven improvement
```

## Related Skills

- `chaos-engineering-fundamentals` - Continuous chaos experiments
- `incident-response` - Handling real incidents
- `resilience-patterns` - Building resilient systems
