---
name: managing-incidents
description: Guide incident response from detection to post-mortem using SRE principles, severity classification, on-call management, blameless culture, and communication protocols. Use when setting up incident processes, designing escalation policies, or conducting post-mortems.
---

# Incident Management

Provide end-to-end incident management guidance covering detection, response, communication, and learning. Emphasizes SRE culture, blameless post-mortems, and structured processes for high-reliability operations.

## When to Use This Skill

Apply this skill when:
- Setting up incident response processes for a team
- Designing on-call rotations and escalation policies
- Creating runbooks for common failure scenarios
- Conducting blameless post-mortems after incidents
- Implementing incident communication protocols (internal and external)
- Choosing incident management tooling and platforms
- Improving MTTR and incident frequency metrics

## Core Principles

### Incident Management Philosophy

**Declare Early and Often:** Do not wait for certainty. Declaring an incident enables coordination, can be downgraded if needed, and prevents delayed response.

**Mitigation First, Root Cause Later:** Stop customer impact immediately (rollback, disable feature, failover). Debug and fix root cause after stability restored.

**Blameless Culture:** Assume good intentions. Focus on how systems failed, not who failed. Create psychological safety for honest learning.

**Clear Command Structure:** Assign Incident Commander (IC) to own coordination. IC delegates tasks but does not do hands-on debugging.

**Communication is Critical:** Internal coordination via dedicated channels, external transparency via status pages. Update stakeholders every 15-30 minutes during critical incidents.

## Severity Classification

Standard severity levels with response times:

**SEV0 (P0) - Critical Outage:**
- Impact: Complete service outage, critical data loss, payment processing down
- Response: Page immediately 24/7, all hands on deck, executive notification
- Example: API completely down, entire customer base affected

**SEV1 (P1) - Major Degradation:**
- Impact: Major functionality degraded, significant customer subset affected
- Response: Page during business hours, escalate off-hours, IC assigned
- Example: 15% error rate, critical feature unavailable

**SEV2 (P2) - Minor Issues:**
- Impact: Minor functionality impaired, edge case bug, small user subset
- Response: Email/Slack alert, next business day response
- Example: UI glitch, non-critical feature slow

**SEV3 (P3) - Low Impact:**
- Impact: Cosmetic issues, no customer functionality affected
- Response: Ticket queue, planned sprint
- Example: Visual inconsistency, documentation error

For detailed severity decision framework and interactive classifier, see `references/severity-classification.md`.

## Incident Roles

**Incident Commander (IC):**
- Owns overall incident response and coordination
- Makes strategic decisions (rollback vs. debug, when to escalate)
- Delegates tasks to responders (does NOT do hands-on debugging)
- Declares incident resolved when stability confirmed

**Communications Lead:**
- Posts status updates to internal and external channels
- Coordinates with stakeholders (executives, product, support)
- Drafts post-incident customer communication
- Cadence: Every 15-30 minutes for SEV0/SEV1

**Subject Matter Experts (SMEs):**
- Hands-on debugging and mitigation
- Execute runbooks and implement fixes
- Provide technical context to IC

**Scribe:**
- Documents timeline, actions, decisions in real-time
- Records incident notes for post-mortem reconstruction

Assign roles based on severity:
- SEV2/SEV3: Single responder
- SEV1: IC + SME(s)
- SEV0: IC + Communications Lead + SME(s) + Scribe

For detailed role responsibilities, see `references/incident-roles.md`.

## On-Call Management

### Rotation Patterns

**Primary + Secondary:**
- Primary: First responder
- Secondary: Backup if primary doesn't ack within 5 minutes
- Rotation length: 1 week (optimal balance)

**Follow-the-Sun (24/7):**
- Team A: US hours, Team B: Europe hours, Team C: Asia hours
- Benefit: No night shifts, improved work-life balance
- Requires: Multiple global teams

**Tiered Escalation:**
- Tier 1: Junior on-call (common issues, runbook-driven)
- Tier 2: Senior on-call (complex troubleshooting)
- Tier 3: Team lead/architect (critical decisions)

### Best Practices

- Rotation length: 1 week per rotation
- Handoff ceremony: 30-minute call to discuss active issues
- Compensation: On-call stipend + time off after major incidents
- Tooling: PagerDuty, Opsgenie, or incident.io
- Limits: Max 2-3 pages per night; escalate if exceeded

## Incident Response Workflow

Standard incident lifecycle:

```
Detection → Triage → Declaration → Investigation
  ↓
Mitigation → Resolution → Monitoring → Closure
  ↓
Post-Mortem (within 48 hours)
```

### Key Decision Points

**When to Declare:** When in doubt, declare (can always downgrade severity)

**When to Escalate:**
- No progress after 30 minutes
- Severity increases (SEV2 → SEV1)
- Specialized expertise needed

**When to Close:**
- Issue resolved and stable for 30+ minutes
- Monitoring shows all metrics at baseline
- No customer-reported issues

For complete workflow details, see `references/incident-workflow.md`.

## Communication Protocols

### Internal Communication

**Incident Slack Channel:**
- Format: `#incident-YYYY-MM-DD-topic-description`
- Pin: Severity, IC name, status update template, runbook links

**War Room:** Video call for SEV0/SEV1 requiring real-time voice coordination

**Status Update Cadence:**
- SEV0: Every 15 minutes
- SEV1: Every 30 minutes
- SEV2: Every 1-2 hours or at major milestones

### External Communication

**Status Page:**
- Tools: Statuspage.io, Instatus, custom
- Stages: Investigating → Identified → Monitoring → Resolved
- Transparency: Acknowledge issue publicly, provide ETAs when possible

**Customer Email:**
- When: SEV0/SEV1 affecting customers
- Timing: Within 1 hour (acknowledge), post-resolution (full details)
- Tone: Apologetic, transparent, action-oriented

**Regulatory Notifications:**
- Data Breach: GDPR requires notification within 72 hours
- Financial Services: Immediate notification to regulators
- Healthcare: HIPAA breach notification rules

For communication templates, see `examples/communication-templates.md`.

## Runbooks and Playbooks

### Runbook Structure

Every runbook should include:
1. **Trigger:** Alert conditions that activate this runbook
2. **Severity:** Expected severity level
3. **Prerequisites:** System state requirements
4. **Steps:** Numbered, executable commands (copy-pasteable)
5. **Verification:** How to confirm fix worked
6. **Rollback:** How to undo if steps fail
7. **Owner:** Team/person responsible
8. **Last Updated:** Date of last revision

### Best Practices

- **Executable:** Commands copy-pasteable, not just descriptions
- **Tested:** Run during disaster recovery drills
- **Versioned:** Track changes in Git
- **Linked:** Reference from alert definitions
- **Automated:** Convert manual steps to scripts over time

For runbook templates, see `examples/runbooks/` directory.

## Blameless Post-Mortems

### Blameless Culture Tenets

**Assume Good Intentions:** Everyone made the best decision with information available.

**Focus on Systems:** Investigate how processes failed, not who failed.

**Psychological Safety:** Create environment where honesty is rewarded.

**Learning Opportunity:** Incidents are gifts of organizational knowledge.

### Post-Mortem Process

**1. Schedule Review (Within 48 Hours):** While memory is fresh

**2. Pre-Work:** Reconstruct timeline, gather metrics/logs, draft document

**3. Meeting Facilitation:**
- Timeline walkthrough
- 5 Whys Analysis to identify systemic root causes
- What Went Well / What Went Wrong
- Define action items with owners and due dates

**4. Post-Mortem Document:**
- Sections: Summary, Timeline, Root Cause, Impact, What Went Well/Wrong, Action Items
- Distribution: Engineering, product, support, leadership
- Storage: Archive in searchable knowledge base

**5. Follow-Up:** Track action items in sprint planning

For detailed facilitation guide and template, see `references/blameless-postmortems.md` and `examples/postmortem-template.md`.

## Alert Design Principles

**Actionable Alerts Only:**
- Every alert requires human action
- Include graphs, runbook links, recent changes
- Deduplicate related alerts
- Route to appropriate team based on service ownership

**Preventing Alert Fatigue:**
- Audit alerts quarterly: Remove non-actionable alerts
- Increase thresholds for noisy metrics
- Use anomaly detection instead of static thresholds
- Limit: Max 2-3 pages per night

## Tool Selection

### Incident Management Platforms

**PagerDuty:**
- Best for: Established enterprises, complex escalation policies
- Cost: $19-41/user/month
- When: Team size 10+, budget $500+/month

**Opsgenie:**
- Best for: Atlassian ecosystem users, flexible routing
- Cost: $9-29/user/month
- When: Using Atlassian products, budget $200-500/month

**incident.io:**
- Best for: Modern teams, AI-powered response, Slack-native
- When: Team size 5-50, Slack-centric culture

For detailed tool comparison, see `references/tool-comparison.md`.

### Status Page Solutions

**Statuspage.io:** Most trusted, easy setup ($29-399/month)
**Instatus:** Budget-friendly, modern design ($19-99/month)

## Metrics and Continuous Improvement

### Key Incident Metrics

**MTTA (Mean Time To Acknowledge):**
- Target: < 5 minutes for SEV1
- Improvement: Better on-call coverage

**MTTR (Mean Time To Recovery):**
- Target: < 1 hour for SEV1
- Improvement: Runbooks, automation

**MTBF (Mean Time Between Failures):**
- Target: > 30 days for critical services
- Improvement: Root cause fixes

**Incident Frequency:**
- Track: SEV0, SEV1, SEV2 counts per month
- Target: Downward trend

**Action Item Completion Rate:**
- Target: > 90%
- Improvement: Sprint integration, ownership clarity

### Continuous Improvement Loop

```
Incident → Post-Mortem → Action Items → Prevention
   ↑                                          ↓
   └──────────── Fewer Incidents ─────────────┘
```

## Decision Frameworks

### Severity Classification Decision Tree

```
Is production completely down or critical data at risk?
├─ YES → SEV0
└─ NO  → Is major functionality degraded?
          ├─ YES → Is there a workaround?
          │        ├─ YES → SEV1
          │        └─ NO  → SEV0
          └─ NO  → Are customers impacted?
                   ├─ YES → SEV2
                   └─ NO  → SEV3
```

Use interactive classifier: `python scripts/classify-severity.py`

### Escalation Matrix

For detailed escalation guidance, see `references/escalation-matrix.md`.

### Mitigation vs. Root Cause

**Prioritize Mitigation When:**
- Active customer impact ongoing
- Quick fix available (rollback, disable feature)

**Prioritize Root Cause When:**
- Customer impact already mitigated
- Fix requires careful analysis

**Default:** Mitigation first (99% of cases)

## Anti-Patterns to Avoid

- **Delayed Declaration:** Waiting for certainty before declaring incident
- **Skipping Post-Mortems:** "Small" incidents still provide learning
- **Blame Culture:** Punishing individuals prevents systemic learning
- **Ignoring Action Items:** Post-mortems without follow-through waste time
- **No Clear IC:** Multiple people leading creates confusion
- **Alert Fatigue:** Noisy, non-actionable alerts cause on-call to ignore pages
- **Hands-On IC:** IC should delegate debugging, not do it themselves

## Implementation Checklist

### Phase 1: Foundation (Week 1)
- [ ] Define severity levels (SEV0-SEV3)
- [ ] Choose incident management platform
- [ ] Set up basic on-call rotation
- [ ] Create incident Slack channel template

### Phase 2: Processes (Weeks 2-3)
- [ ] Create first 5 runbooks for common incidents
- [ ] Set up status page
- [ ] Train team on incident response
- [ ] Conduct tabletop exercise

### Phase 3: Culture (Weeks 4+)
- [ ] Conduct first blameless post-mortem
- [ ] Establish post-mortem cadence
- [ ] Implement MTTA/MTTR dashboards
- [ ] Track action items in sprint planning

### Phase 4: Optimization (Months 3-6)
- [ ] Automate incident declaration
- [ ] Implement runbook automation
- [ ] Monthly disaster recovery drills
- [ ] Quarterly incident trend reviews

## Integration with Other Skills

**Observability:** Monitoring alerts trigger incidents → Use incident-management for response

**Disaster Recovery:** DR provides recovery procedures → Incident-management provides operational response

**Security Incident Response:** Similar process with added compliance/forensics

**Infrastructure-as-Code:** IaC enables fast recovery via automated rebuild

**Performance Engineering:** Performance incidents trigger response → Performance team investigates post-mitigation

## Examples and Templates

**Runbook Templates:**
- `examples/runbooks/database-failover.md`
- `examples/runbooks/cache-invalidation.md`
- `examples/runbooks/ddos-mitigation.md`

**Post-Mortem Template:**
- `examples/postmortem-template.md` - Complete blameless post-mortem structure

**Communication Templates:**
- `examples/communication-templates.md` - Status updates, customer emails

**On-Call Handoff:**
- `examples/oncall-handoff-template.md` - Weekly handoff format

**Integration Scripts:**
- `examples/integrations/pagerduty-slack.py`
- `examples/integrations/statuspage-auto-update.py`
- `examples/integrations/postmortem-generator.py`

## Scripts

**Interactive Severity Classifier:**
```bash
python scripts/classify-severity.py
```
Asks questions to determine appropriate severity level based on impact and urgency.

## Further Reading

**Books:**
- Google SRE Book: "Postmortem Culture" (Chapter 15)
- "The Phoenix Project" by Gene Kim
- "Site Reliability Engineering" (Full book)

**Online Resources:**
- Atlassian: "How to Run a Blameless Postmortem"
- PagerDuty: "Incident Response Guide"
- Google SRE: "Postmortem Culture: Learning from Failure"

**Standards:**
- Incident Command System (ICS) - FEMA standard adapted for tech
- ITIL Incident Management - Traditional IT service management
