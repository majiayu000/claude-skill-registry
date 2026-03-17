# incident-triage

Rapid incident classification, severity assessment, and response coordination.

## Triggers

- "production incident"
- "system is down"
- "critical issue"
- "triage incident"
- "incident severity"
- "outage"
- "P0" / "P1" / "SEV1"

## Purpose

This skill provides rapid incident response coordination by:
- Classifying incident type and severity
- Assembling response team
- Coordinating initial response actions
- Tracking timeline and status
- Facilitating communication
- Preparing post-incident review

## Behavior

When triggered, this skill:

1. **Gathers incident details**:
   - What is happening?
   - When did it start?
   - Who/what is affected?
   - What changed recently?

2. **Classifies severity**:
   - Assess customer impact
   - Determine scope
   - Assign severity level
   - Calculate business impact

3. **Assembles response team**:
   - Identify required responders
   - Notify on-call personnel
   - Establish incident commander

4. **Initiates response**:
   - Create incident channel/bridge
   - Start timeline documentation
   - Coordinate initial diagnosis

5. **Manages communication**:
   - Internal status updates
   - Customer communication (if needed)
   - Executive notifications (for high severity)

6. **Tracks resolution**:
   - Document actions taken
   - Track mitigation progress
   - Confirm resolution
   - Schedule post-incident review

## Severity Levels

### SEV1 / P0 - Critical

```yaml
sev1:
  name: Critical
  alias: [P0, SEV1, Critical]

  criteria:
    - Complete service outage
    - Data loss or corruption
    - Security breach
    - >50% customers affected
    - Revenue-impacting

  response:
    response_time: 15 minutes
    update_frequency: 15 minutes
    executive_notification: immediate
    customer_communication: within 30 minutes

  escalation:
    - incident_commander: required
    - engineering_manager: required
    - vp_engineering: within 30 minutes
    - cto: within 1 hour (if unresolved)

  target_resolution: 4 hours
```

### SEV2 / P1 - High

```yaml
sev2:
  name: High
  alias: [P1, SEV2, High]

  criteria:
    - Major feature unavailable
    - Significant degradation
    - 10-50% customers affected
    - Workaround exists but painful

  response:
    response_time: 30 minutes
    update_frequency: 30 minutes
    executive_notification: within 1 hour
    customer_communication: within 2 hours (if extended)

  escalation:
    - incident_commander: required
    - engineering_manager: within 1 hour

  target_resolution: 8 hours
```

### SEV3 / P2 - Medium

```yaml
sev3:
  name: Medium
  alias: [P2, SEV3, Medium]

  criteria:
    - Feature partially degraded
    - <10% customers affected
    - Workaround available
    - Non-critical path affected

  response:
    response_time: 2 hours
    update_frequency: 2 hours
    executive_notification: daily summary
    customer_communication: as needed

  escalation:
    - team_lead: within 4 hours

  target_resolution: 24 hours
```

### SEV4 / P3 - Low

```yaml
sev4:
  name: Low
  alias: [P3, SEV4, Low]

  criteria:
    - Minor issue
    - Cosmetic problem
    - Edge case affected
    - Easy workaround

  response:
    response_time: next business day
    update_frequency: daily
    executive_notification: weekly summary

  escalation: standard ticket flow

  target_resolution: 1 week
```

## Incident Response Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DETECTION & TRIAGE                                       │
│    • Alert received or issue reported                       │
│    • Gather initial details                                 │
│    • Classify severity                                      │
│    • Create incident record                                 │
│    • Time: <15 minutes                                      │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. MOBILIZATION                                             │
│    • Page on-call responders                                │
│    • Establish incident commander                           │
│    • Create communication channel                           │
│    • Notify stakeholders per severity                       │
│    • Time: <5 minutes after triage                          │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. INVESTIGATION                                            │
│    • Review recent changes                                  │
│    • Check monitoring/logs                                  │
│    • Identify affected components                           │
│    • Form hypothesis                                        │
│    • Time: ongoing, status updates per SLA                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. MITIGATION                                               │
│    • Implement workaround if available                      │
│    • Rollback if change-related                             │
│    • Scale resources if capacity issue                      │
│    • Isolate affected components                            │
│    • Goal: Reduce customer impact                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RESOLUTION                                               │
│    • Implement permanent fix                                │
│    • Verify fix is effective                                │
│    • Monitor for recurrence                                 │
│    • Update status to resolved                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. POST-INCIDENT                                            │
│    • Schedule post-incident review                          │
│    • Document timeline and actions                          │
│    • Identify root cause                                    │
│    • Create follow-up action items                          │
│    • Update runbooks/documentation                          │
└─────────────────────────────────────────────────────────────┘
```

## Incident Record Format

```markdown
# Incident Report: INC-2025-001234

## Summary

| Field | Value |
|-------|-------|
| Title | Database connection pool exhaustion |
| Severity | SEV1 (Critical) |
| Status | Resolved |
| Start Time | 2025-12-08 14:32 UTC |
| Detected | 2025-12-08 14:35 UTC |
| Resolved | 2025-12-08 15:47 UTC |
| Duration | 1h 15m |
| Impact | 100% of API requests failing |
| Customers Affected | ~45,000 |

## Incident Commander

**Name**: Sarah Chen
**Role**: Senior SRE

## Response Team

| Role | Name | Joined |
|------|------|--------|
| Incident Commander | Sarah Chen | 14:38 |
| Backend Lead | David Kim | 14:40 |
| DBA | Elena Rodriguez | 14:45 |
| Comms Lead | James Wilson | 14:50 |

## Impact Assessment

### Customer Impact
- **Scope**: All customers using web and mobile apps
- **Severity**: Complete service outage
- **Duration**: 1h 15m
- **Affected Features**: All authenticated features

### Business Impact
- **Revenue Loss**: Estimated $XX,XXX
- **SLA Breach**: Yes (99.9% monthly target affected)
- **Customer Complaints**: 127 support tickets

## Timeline

| Time (UTC) | Event |
|------------|-------|
| 14:32 | First customer reports of errors |
| 14:35 | PagerDuty alert for 5xx spike |
| 14:38 | Incident declared, Sarah Chen IC |
| 14:40 | Investigation begins |
| 14:45 | Identified: DB connection pool exhausted |
| 14:52 | Root cause: Runaway query from batch job |
| 15:00 | Mitigation: Batch job killed |
| 15:10 | Connection pool recovering |
| 15:30 | 50% traffic restored |
| 15:47 | Full service restored |
| 15:50 | Monitoring confirms stable |
| 16:00 | Incident closed |

## Root Cause

**Summary**: A scheduled batch job contained an inefficient query that held database connections indefinitely, exhausting the connection pool.

**Details**:
- Batch job deployed at 14:00 with new query
- Query had missing index, causing full table scan
- Each scan held connection for 30+ seconds
- 100 concurrent requests × 30s = pool exhausted
- New requests could not get connections → 5xx errors

**Contributing Factors**:
1. Missing index migration in batch job deploy
2. No query timeout configured
3. Connection pool size not tuned for load
4. Batch job ran during peak hours

## Resolution

**Immediate Actions**:
1. Killed runaway batch job
2. Restarted application servers to reset connections
3. Verified service restoration

**Permanent Fixes** (follow-ups):
- [ ] Add missing index (INC-001-01)
- [ ] Configure query timeouts (INC-001-02)
- [ ] Increase connection pool size (INC-001-03)
- [ ] Move batch jobs to off-peak hours (INC-001-04)
- [ ] Add connection pool monitoring alerts (INC-001-05)

## Communication Log

| Time | Channel | Message |
|------|---------|---------|
| 14:45 | #incident-2025-001234 | Incident declared, investigating API failures |
| 15:00 | Status Page | Investigating service disruption |
| 15:15 | Status Page | Identified cause, implementing fix |
| 15:30 | #incident-2025-001234 | Service recovering, 50% restored |
| 15:50 | Status Page | Service fully restored |
| 16:00 | Email to customers | Incident resolved, apology + explanation |

## Post-Incident Review

**Scheduled**: 2025-12-10 10:00 UTC
**Attendees**: Response team + Engineering Manager
**Document**: .aiwg/incidents/INC-2025-001234-pir.md

## Lessons Learned

### What Went Well
- Fast detection (3 minutes)
- Clear incident commander
- Good team coordination

### What Could Improve
- Batch job should have been tested with prod-like data
- Missing connection pool alerts
- No query timeout safety net

## Action Items

| ID | Action | Owner | Due | Status |
|----|--------|-------|-----|--------|
| INC-001-01 | Add missing index | Elena | 2025-12-09 | Done |
| INC-001-02 | Configure query timeouts | David | 2025-12-10 | In Progress |
| INC-001-03 | Tune connection pool | Sarah | 2025-12-12 | Planned |
| INC-001-04 | Reschedule batch jobs | David | 2025-12-15 | Planned |
| INC-001-05 | Add pool monitoring | Sarah | 2025-12-12 | Planned |
```

## Usage Examples

### Declare Incident

```
User: "Production is down, API returning 500 errors"

Skill initiates:
1. Gather details
2. Classify severity
3. Create incident record
4. Notify responders

Output:
"🚨 INCIDENT DECLARED: INC-2025-001234

Severity: SEV1 (Critical) - Complete API failure
Impact: All customers affected

Immediate Actions:
1. ✅ Incident record created
2. ✅ Paging on-call: Sarah Chen (SRE)
3. ✅ Slack channel: #incident-2025-001234
4. ⏳ Assembling response team

You are Incident Commander until relieved.

Quick Checklist:
- [ ] What changed in last 2 hours?
- [ ] Check: logs, metrics, recent deploys
- [ ] Status page update needed?

Update command: 'incident update <message>'"
```

### Severity Assessment

```
User: "Is this SEV1 or SEV2? Users can't checkout but browsing works"

Skill evaluates:
- Core function affected: Yes (checkout = revenue)
- Workaround: No (can't complete purchase)
- Customer %: All attempting checkout
- Revenue impact: Direct

Output:
"Severity Assessment: SEV1 (Critical)

Rationale:
✓ Revenue-impacting feature down
✓ No workaround for affected flow
✓ Checkout is business-critical path
✓ Affects all customers attempting purchase

SEV1 Criteria Met:
- Complete feature outage: checkout
- Revenue impact: direct
- No workaround: cannot complete purchases

Response Requirements:
- 15-minute update cadence
- Executive notification: immediate
- Customer communication: within 30 minutes
- Target resolution: 4 hours"
```

### Status Update

```
User: "Incident update: found the issue, deploying fix"

Skill logs:
1. Add to timeline
2. Update status
3. Notify stakeholders

Output:
"Incident Update: INC-2025-001234

Status: Mitigating
Time: 15:15 UTC

Update Logged:
'Found root cause, deploying fix'

Next Actions:
- [ ] Update status page
- [ ] Notify executive stakeholders
- [ ] Continue timeline documentation

Time Since Start: 43 minutes
Next Update Due: 15:30 UTC"
```

## Integration

This skill uses:
- `project-awareness`: Context for system topology
- `artifact-metadata`: Track incident artifacts

## Agent Orchestration

```yaml
agents:
  incident_commander:
    agent: incident-responder
    focus: Overall coordination and decisions

  technical_lead:
    agent: debugger
    focus: Root cause investigation

  reliability:
    agent: reliability-engineer
    focus: System stability and monitoring

  communications:
    agent: support-lead
    focus: Customer and stakeholder communication
```

## Configuration

### Notification Channels

```yaml
notifications:
  sev1:
    pagerduty: true
    slack: "#incidents-critical"
    email: [engineering-leads, on-call-manager]
    sms: [incident-commander, vp-engineering]

  sev2:
    pagerduty: true
    slack: "#incidents"
    email: [engineering-leads]

  sev3:
    slack: "#incidents"
    email: [team-lead]

  sev4:
    slack: "#incidents-low"
```

### Escalation Paths

```yaml
escalation:
  sev1:
    - {time: 0, to: on-call-engineer}
    - {time: 15m, to: engineering-manager}
    - {time: 30m, to: vp-engineering}
    - {time: 1h, to: cto}

  sev2:
    - {time: 0, to: on-call-engineer}
    - {time: 1h, to: engineering-manager}
    - {time: 4h, to: vp-engineering}
```

## Output Locations

- Incident records: `.aiwg/incidents/INC-{year}-{id}.md`
- Post-incident reviews: `.aiwg/incidents/INC-{year}-{id}-pir.md`
- Action items: `.aiwg/incidents/action-items.md`
- Metrics: `.aiwg/incidents/metrics/`

## References

- Incident response template: templates/operations/incident-template.md
- Post-incident review template: templates/operations/pir-template.md
- On-call schedule: .aiwg/team/on-call.yaml
- Runbooks: .aiwg/deployment/runbooks/
