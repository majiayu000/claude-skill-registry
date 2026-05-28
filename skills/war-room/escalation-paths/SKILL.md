---
name: Escalation Paths
description: Clear escalation procedures and paths for incident response
---

# Escalation Paths

## Overview

Escalation paths define when and how to escalate incidents to ensure the right expertise is engaged at the right time. Effective escalation prevents incidents from languishing while avoiding unnecessary wake-up calls.

**Core Principle**: "Escalate early for critical issues, but don't cry wolf for minor problems."

## 1. What is Escalation and When to Escalate

### Definition

```
Escalation: The process of engaging additional resources or higher-level expertise when:
- Current responder cannot resolve the issue
- Incident exceeds time/severity thresholds
- Specialized expertise is needed
- Executive visibility is required
```

### When to Escalate

```
✓ Escalate when:
- SEV0 incident (always, immediately)
- SEV1 not resolved in 30 minutes
- SEV2 not resolved in 2 hours
- You don't know how to fix it
- Issue affects multiple teams
- Requires specialized expertise (database, security, networking)
- Customer escalation (enterprise customer affected)
- Regulatory/legal implications

✗ Don't escalate when:
- You can fix it yourself in < 15 minutes
- It's a known issue with documented fix
- It's outside business hours for SEV3/4
- You haven't tried basic troubleshooting
```

## 2. Escalation Triggers

### 2.1 Severity Thresholds

```typescript
interface EscalationRule {
  severity: string;
  immediateEscalation: boolean;
  escalateAfter?: number; // minutes
  escalateTo: string[];
}

const escalationRules: EscalationRule[] = [
  {
    severity: 'SEV0',
    immediateEscalation: true,
    escalateTo: ['on-call-senior', 'team-lead', 'engineering-manager', 'cto']
  },
  {
    severity: 'SEV1',
    immediateEscalation: false,
    escalateAfter: 30,
    escalateTo: ['on-call-senior', 'team-lead']
  },
  {
    severity: 'SEV2',
    immediateEscalation: false,
    escalateAfter: 120,
    escalateTo: ['team-lead']
  },
  {
    severity: 'SEV3',
    immediateEscalation: false,
    escalateAfter: 480,
    escalateTo: ['team-lead']
  }
];
```

### 2.2 Time-Based Escalation

```
Automatic escalation based on duration:

SEV0:
- 0 minutes: Page on-call engineer
- 0 minutes: Page senior engineer (parallel)
- 0 minutes: Notify team lead
- 15 minutes: Escalate to engineering manager
- 30 minutes: Escalate to CTO

SEV1:
- 0 minutes: Page on-call engineer
- 30 minutes: Escalate to senior engineer
- 60 minutes: Escalate to team lead
- 120 minutes: Escalate to engineering manager

SEV2:
- 0 minutes: Notify on-call engineer
- 120 minutes: Escalate to team lead
- 240 minutes: Escalate to engineering manager

SEV3:
- 0 minutes: Create ticket
- 480 minutes: Notify team lead (business hours)
```

### 2.3 Expertise Needed

```
Escalate to subject matter expert (SME) when:

Database issues:
- Slow queries
- Connection pool exhaustion
- Replication lag
- Failover needed
→ Escalate to: @database-team

Security issues:
- Suspected breach
- DDoS attack
- Vulnerability exploitation
→ Escalate to: @security-team

Infrastructure issues:
- Kubernetes cluster problems
- Network issues
- Cloud provider outage
→ Escalate to: @platform-team

Application-specific:
- Payment processing
- Authentication
- Search functionality
→ Escalate to: @payments-team, @auth-team, @search-team
```

### 2.4 Cross-Team Dependencies

```
Escalate when issue spans multiple teams:

Example: Payment processing down
- Affects: Frontend, Backend, Payments, Database
- Escalate to: All affected teams
- Coordinate: Incident commander needed

Example: Database slow
- Affects: All services using database
- Escalate to: Database team (primary), all service teams (notify)
```

### 2.5 Executive Visibility Required

```
Escalate to executives when:

SEV0 incidents (always):
- Complete outage
- Data breach
- Major customer impact

Business impact:
- Revenue loss > $50k/hour
- SLA breach with penalties
- Regulatory violation
- PR/reputation risk

Customer escalation:
- Enterprise customer affected
- Customer threatening to churn
- Legal action threatened
```

## 3. Escalation Levels

### L1: First Responder (On-Call Engineer)

```
Role: Primary on-call engineer

Responsibilities:
- Acknowledge alerts within 5-15 minutes
- Perform initial triage
- Follow runbooks
- Resolve common issues
- Escalate when needed

Skills:
- General system knowledge
- Basic troubleshooting
- Runbook execution

Escalation criteria:
- Can't resolve in 30 minutes (SEV1)
- Needs specialized expertise
- SEV0 incident
```

### L2: Subject Matter Expert / Team Lead

```
Role: Senior engineer or team lead

Responsibilities:
- Deep technical investigation
- Complex troubleshooting
- Decision-making (rollback vs fix forward)
- Coordinate with other teams
- Guide L1 engineer

Skills:
- Deep system knowledge
- Advanced troubleshooting
- Architecture understanding

Escalation criteria:
- Can't resolve in 60 minutes (SEV1)
- Requires architectural decision
- Cross-team coordination needed
- SEV0 incident
```

### L3: Architect / Principal Engineer

```
Role: Principal engineer or architect

Responsibilities:
- Architectural decisions
- Complex system-wide issues
- Design emergency fixes
- Long-term solution planning

Skills:
- System architecture expertise
- Cross-system knowledge
- Strategic thinking

Escalation criteria:
- Architectural change needed
- System-wide impact
- Novel failure mode
- SEV0 lasting > 30 minutes
```

### L4: Director / VP / CTO

```
Role: Engineering leadership

Responsibilities:
- Executive decision-making
- Resource allocation
- Customer communication (enterprise)
- PR/legal coordination
- Post-incident accountability

Escalation criteria:
- SEV0 incident (always notified)
- Major business impact
- Customer escalation
- Regulatory/legal issues
- PR crisis
```

## 4. Escalation Paths by Service/Component

### Service-Specific Escalation Matrix

```typescript
interface ServiceEscalation {
  service: string;
  primary: string;
  secondary: string;
  sme: string[];
  executive: string;
}

const escalationMatrix: ServiceEscalation[] = [
  {
    service: 'api-gateway',
    primary: '@oncall-platform',
    secondary: '@platform-lead',
    sme: ['@platform-architect', '@networking-team'],
    executive: '@vp-engineering'
  },
  {
    service: 'user-service',
    primary: '@oncall-backend',
    secondary: '@backend-lead',
    sme: ['@auth-expert', '@database-team'],
    executive: '@vp-engineering'
  },
  {
    service: 'payment-service',
    primary: '@oncall-payments',
    secondary: '@payments-lead',
    sme: ['@payments-architect', '@security-team'],
    executive: '@cto' // High-stakes service
  },
  {
    service: 'database',
    primary: '@oncall-database',
    secondary: '@database-lead',
    sme: ['@dba-senior', '@platform-team'],
    executive: '@vp-engineering'
  }
];
```

### Escalation Flow Diagram

```
Incident Detected
      ↓
L1: On-Call Engineer
      ↓
Can resolve? ─YES→ Resolve & Document
      ↓ NO
      ↓
Needs expertise? ─YES→ L2: SME/Team Lead
      ↓ NO                    ↓
      ↓                  Can resolve? ─YES→ Resolve
      ↓                       ↓ NO
      ↓                       ↓
SEV0 or >30min? ─YES→ L3: Architect/Principal
      ↓ NO                    ↓
      ↓                  Can resolve? ─YES→ Resolve
      ↓                       ↓ NO
      ↓                       ↓
Continue investigation  L4: Executive
      ↓                       ↓
Escalate if not         Major decisions,
resolved in 2 hours     resource allocation
```

## 5. When NOT to Escalate (Avoid Alert Fatigue)

### Don't Escalate If

```
❌ You haven't tried basic troubleshooting
   - Check logs
   - Review recent changes
   - Follow runbook
   - Test critical paths

❌ It's a known issue with documented fix
   - Check runbook first
   - Search incident history
   - Review documentation

❌ You can fix it in < 15 minutes
   - Simple restart
   - Clear cache
   - Known configuration fix

❌ It's outside business hours for low severity
   - SEV3/4 can wait until morning
   - No customer impact
   - Non-urgent

❌ You're escalating just to cover yourself
   - Escalate because you need help, not to avoid responsibility
```

### Alert Fatigue Prevention

```typescript
// Track escalation patterns
interface EscalationMetrics {
  engineer: string;
  totalEscalations: number;
  appropriateEscalations: number;
  prematureEscalations: number;
  delayedEscalations: number;
}

// Flag concerning patterns
function analyzeEscalationPatterns(metrics: EscalationMetrics[]) {
  for (const m of metrics) {
    const prematureRate = m.prematureEscalations / m.totalEscalations;
    
    if (prematureRate > 0.5) {
      console.log(`⚠️ ${m.engineer} escalates too quickly (${prematureRate * 100}%)`);
      // Provide additional training
    }
    
    if (m.delayedEscalations > 5) {
      console.log(`⚠️ ${m.engineer} delays escalation too often`);
      // Review escalation criteria
    }
  }
}
```

## 6. Escalation Procedures

### 6.1 Who to Contact

```
Escalation Directory:

L1 (On-Call Engineer):
- PagerDuty: @oncall-primary
- Slack: #oncall-primary
- Phone: (from PagerDuty)

L2 (Team Lead):
- PagerDuty: @oncall-secondary
- Slack: @team-lead
- Phone: +1-555-0100

L3 (Architect):
- Slack: @principal-engineer
- Phone: +1-555-0200
- Email: architect@example.com

L4 (Executive):
- Slack: @vp-engineering
- Phone: +1-555-0300 (SEV0 only)
- Email: vp@example.com
```

### 6.2 How to Contact

```
Contact Methods by Severity:

SEV0:
1. PagerDuty (immediate page)
2. Phone call (if no response in 2 minutes)
3. Slack @mention + DM
4. Escalate to next level if no response in 5 minutes

SEV1:
1. PagerDuty (page)
2. Slack @mention in incident channel
3. Phone call if no response in 15 minutes

SEV2:
1. Slack @mention in incident channel
2. PagerDuty (low urgency)
3. Email (if outside business hours)

SEV3/4:
1. Slack message (no @mention)
2. Email
3. Create ticket
```

### 6.3 What Information to Provide

```markdown
## Escalation Message Template

**Escalating to**: @senior-engineer
**From**: @oncall-engineer
**Incident**: INC-2024-001
**Severity**: SEV1
**Time**: 10:45 UTC

**Summary**:
API Gateway returning 503 errors for 30 minutes. 50% of users affected.

**What I've Tried**:
- ✅ Checked logs (found database connection errors)
- ✅ Verified database is running
- ✅ Restarted API pods (no improvement)
- ✅ Reviewed recent deployments (none in last 24 hours)

**Current Status**:
- Error rate: 45%
- Users affected: ~25,000
- Duration: 30 minutes

**Why Escalating**:
- SEV1 not resolved in 30 minutes
- Database connection issue beyond my expertise
- Need database team involvement

**Next Steps I Recommend**:
- Check database connection pool
- Review database performance
- Consider database failover

**Links**:
- Incident channel: #inc-2024-001
- Dashboard: https://grafana.example.com/d/incident
- Runbook: https://wiki.example.com/runbooks/db-connection

**Questions?** Ask in #inc-2024-001
```

### 6.4 Handoff Checklist

```markdown
## Escalation Handoff Checklist

### Context
- [ ] Incident ID and severity
- [ ] What's broken (specific symptoms)
- [ ] Impact (users, revenue, services)
- [ ] Timeline (when started, key events)
- [ ] What's been tried
- [ ] Current hypothesis
- [ ] Relevant links

### Communication
- [ ] Incident channel ownership transferred
- [ ] Status page update responsibility
- [ ] Stakeholder notification
- [ ] Next update timing

### Access
- [ ] Necessary permissions granted
- [ ] VPN/SSH access confirmed
- [ ] Tool access verified

### Actions
- [ ] Current action in progress
- [ ] Next steps documented
- [ ] Blockers identified
```

## 7. Escalation SLAs

### Response Time SLAs

```
Escalation Level | Acknowledgement | Join Incident
-----------------|-----------------|---------------
L1 (On-Call)     | 5 min (SEV0)    | Immediate
                 | 15 min (SEV1)   | Immediate
L2 (Team Lead)   | 10 min (SEV0)   | 5 min
                 | 30 min (SEV1)   | 15 min
L3 (Architect)   | 15 min (SEV0)   | 10 min
                 | 60 min (SEV1)   | 30 min
L4 (Executive)   | 30 min (SEV0)   | As needed
```

### Escalation Timeout

```typescript
// Auto-escalate if no response
async function escalateWithTimeout(
  level: string,
  contact: string,
  timeoutMinutes: number
) {
  const escalation = await sendEscalation(level, contact);
  
  // Wait for acknowledgement
  const acknowledged = await waitForAck(escalation.id, timeoutMinutes);
  
  if (!acknowledged) {
    console.log(`No response from ${contact}, escalating to next level`);
    await escalateToNextLevel(level);
  }
}
```

## 8. On-Call Rotation Tiers

### Tier Structure

```
Tier 1 (Primary On-Call):
- Role: First responder
- Rotation: Weekly
- Compensation: On-call pay + overtime
- Responsibilities:
  - Respond to all alerts
  - Initial triage
  - Resolve common issues
  - Escalate when needed

Tier 2 (Secondary On-Call):
- Role: Backup and escalation
- Rotation: Weekly (offset from Tier 1)
- Compensation: On-call pay
- Responsibilities:
  - Backup if Tier 1 unavailable
  - Escalation for complex issues
  - Subject matter expertise

Tier 3 (Management On-Call):
- Role: Executive escalation
- Rotation: Monthly
- Compensation: Included in salary
- Responsibilities:
  - SEV0 incidents
  - Executive decisions
  - Customer communication
```

### Rotation Schedule

```
Week 1:
- Tier 1: Alice
- Tier 2: Bob
- Tier 3: Charlie (Manager)

Week 2:
- Tier 1: Bob
- Tier 2: Charlie
- Tier 3: Charlie (Manager)

Week 3:
- Tier 1: Charlie
- Tier 2: Alice
- Tier 3: David (Manager)
```

## 9. Subject Matter Expert (SME) Registry

### SME Directory

```typescript
interface SME {
  name: string;
  expertise: string[];
  contact: {
    slack: string;
    phone: string;
    email: string;
  };
  availability: string;
  escalationCriteria: string;
}

const smeRegistry: SME[] = [
  {
    name: 'Alice Chen',
    expertise: ['PostgreSQL', 'Database Performance', 'Replication'],
    contact: {
      slack: '@alice',
      phone: '+1-555-0101',
      email: 'alice@example.com'
    },
    availability: '24/7 for SEV0/1',
    escalationCriteria: 'Database issues, slow queries, failover needed'
  },
  {
    name: 'Bob Smith',
    expertise: ['Kubernetes', 'Infrastructure', 'Networking'],
    contact: {
      slack: '@bob',
      phone: '+1-555-0102',
      email: 'bob@example.com'
    },
    availability: 'Business hours + SEV0',
    escalationCriteria: 'K8s cluster issues, networking, infrastructure'
  },
  {
    name: 'Carol Johnson',
    expertise: ['Security', 'Authentication', 'Compliance'],
    contact: {
      slack: '@carol',
      phone: '+1-555-0103',
      email: 'carol@example.com'
    },
    availability: '24/7 for security incidents',
    escalationCriteria: 'Security breaches, auth issues, compliance'
  }
];
```

### SME Lookup Tool

```typescript
// Find SME for specific issue
function findSME(issue: string): SME[] {
  return smeRegistry.filter(sme =>
    sme.expertise.some(exp =>
      issue.toLowerCase().includes(exp.toLowerCase())
    )
  );
}

// Usage
const databaseSMEs = findSME('PostgreSQL slow queries');
console.log(`Contact: ${databaseSMEs[0].contact.slack}`);
```

## 10. Cross-Team Escalation

### Cross-Team Escalation Matrix

```
Issue Type          | Primary Team  | Secondary Team | Coordinator
--------------------|---------------|----------------|-------------
API Gateway Down    | Platform      | Backend        | Platform Lead
Database Slow       | Database      | All Services   | Database Lead
Payment Failing     | Payments      | Backend        | Payments Lead
Security Breach     | Security      | All Teams      | CISO
Network Issues      | Platform      | Infrastructure | Platform Lead
```

### Cross-Team Communication

```markdown
## Cross-Team Escalation Template

**To**: @backend-team, @frontend-team
**From**: @platform-team
**Incident**: INC-2024-001 (SEV1)
**Impact**: API Gateway down, affecting all services

**What We Know**:
- API Gateway returning 503 errors
- Started at 10:13 UTC
- All services affected
- Root cause: Under investigation

**What We Need From You**:
- Backend: Check if your services are receiving traffic
- Frontend: Enable fallback UI for offline mode
- All: Monitor your error rates

**Coordination**:
- War room: https://zoom.us/j/123456
- Incident channel: #inc-2024-001
- Next update: 10:30 UTC (15 minutes)

**Point of Contact**: @platform-lead
```

## 11. Vendor Escalation (AWS Support, etc.)

### When to Escalate to Vendor

```
Escalate to cloud provider when:
✓ Suspected provider outage
✓ Infrastructure issue beyond your control
✓ Need architectural guidance
✓ Performance issue with managed service
✓ Billing/quota issues

Don't escalate when:
✗ It's your application code
✗ You haven't checked status page
✗ It's a known limitation
```

### AWS Support Escalation

```bash
# Check AWS Service Health
aws health describe-events --filter eventTypeCategories=issue

# Open support case
aws support create-case \
  --subject "RDS instance unresponsive" \
  --service-code "amazon-rds" \
  --severity-code "urgent" \
  --category-code "performance" \
  --communication-body "Production RDS instance db-prod-01 is unresponsive. All queries timing out. Started at 10:13 UTC. Affecting 100% of users."

# Escalate existing case
aws support add-communication-to-case \
  --case-id "case-123456" \
  --communication-body "Issue is SEV0, please escalate to senior support engineer"
```

### Vendor Escalation Tiers

```
AWS Support Tiers:
- Developer: Business hours, general guidance
- Business: 24/7, < 1 hour response for production down
- Enterprise: 24/7, < 15 min response for business-critical down, TAM

GCP Support Tiers:
- Basic: Community support only
- Standard: 4-hour response for P2
- Enhanced: 1-hour response for P1
- Premium: 15-minute response for P1, TAM

Azure Support Tiers:
- Basic: Billing and subscription support
- Developer: Business hours
- Standard: 24/7, < 1 hour for critical
- Professional Direct: < 1 hour for critical, TAM
```

## 12. Executive Escalation (When to Wake the CTO)

### When to Escalate to Executives

```
Always escalate to CTO/VP for:
✓ SEV0 incidents
✓ Data breach or security incident
✓ Revenue loss > $100k
✓ Major customer threatening to churn
✓ Regulatory violation
✓ PR crisis / media attention
✓ Legal action threatened

Consider escalating for:
✓ SEV1 lasting > 2 hours
✓ Multiple SEV1 incidents in short time
✓ Pattern of recurring issues
✓ Team morale crisis
```

### Executive Escalation Template

```markdown
## Executive Escalation

**To**: @cto
**From**: @engineering-manager
**Urgency**: High
**Time**: 11:00 UTC

**Situation**:
SEV0 incident: Complete service outage for 45 minutes

**Impact**:
- Users affected: 100% (~50,000 active users)
- Revenue loss: ~$75,000
- SLA breach: Yes (99.9% uptime)
- Customer complaints: 237 support tickets

**Root Cause**:
Database connection pool exhausted due to connection leak in v2.5.0 deployment

**Current Status**:
- Rolled back to v2.4.9 at 10:40 UTC
- Service recovering
- Error rate dropping (currently 5%, target < 1%)

**Next Steps**:
- Monitor for 30 minutes
- Investigate connection leak offline
- Postmortem scheduled for tomorrow 10:00 AM

**Customer Communication**:
- Status page updated
- Email sent to affected users
- Enterprise customers notified directly

**What We Need From You**:
- Approval for postmortem resources
- Customer communication review
- Decision on compensation for affected customers
```

## 13. De-Escalation Procedures

### When to De-Escalate

```
De-escalate when:
✓ Issue resolved
✓ Severity downgraded (SEV0 → SEV1)
✓ Handoff to regular business hours team
✓ Specialized expertise no longer needed
```

### De-Escalation Checklist

```markdown
## De-Escalation Checklist

### Before De-Escalating
- [ ] Issue resolved or significantly mitigated
- [ ] Monitoring shows stable state
- [ ] Root cause identified (or investigation plan in place)
- [ ] Documentation updated
- [ ] Stakeholders notified

### De-Escalation Communication
- [ ] Thank escalated team members
- [ ] Summarize resolution
- [ ] Document learnings
- [ ] Schedule postmortem (if needed)
- [ ] Update incident status

### Handoff
- [ ] Transfer ownership to business hours team (if applicable)
- [ ] Document remaining work
- [ ] Create follow-up tickets
```

### De-Escalation Message

```markdown
## De-Escalation Notice

**Incident**: INC-2024-001 (SEV1 → Resolved)
**Time**: 11:30 UTC
**Duration**: 77 minutes

**Resolution**:
Rolled back deployment to v2.4.9. Service fully restored.

**Thanks To**:
- @alice (database expertise)
- @bob (deployment rollback)
- @charlie (customer communication)

**Next Steps**:
- Postmortem scheduled: Tomorrow 10:00 AM
- Follow-up ticket: JIRA-1234 (investigate connection leak)
- Monitoring: Continue for 24 hours

**Status**:
- Incident: Resolved
- War room: Closed
- On-call: Returned to normal rotation
```

## 14. Tools: PagerDuty Schedules, Opsgenie Escalation Policies

### PagerDuty Escalation Policy

```json
{
  "escalation_policy": {
    "name": "Engineering Escalation",
    "escalation_rules": [
      {
        "escalation_delay_in_minutes": 0,
        "targets": [
          {
            "type": "schedule_reference",
            "id": "ONCALL_PRIMARY"
          }
        ]
      },
      {
        "escalation_delay_in_minutes": 15,
        "targets": [
          {
            "type": "schedule_reference",
            "id": "ONCALL_SECONDARY"
          }
        ]
      },
      {
        "escalation_delay_in_minutes": 30,
        "targets": [
          {
            "type": "user_reference",
            "id": "ENGINEERING_MANAGER"
          }
        ]
      }
    ]
  }
}
```

### Opsgenie Escalation

```yaml
# Opsgenie escalation policy
name: "Production Escalation"
rules:
  - condition: "match-all"
    notify:
      - type: "schedule"
        name: "Primary On-Call"
        delay: 0
      - type: "schedule"
        name: "Secondary On-Call"
        delay: 15m
      - type: "team"
        name: "Engineering Managers"
        delay: 30m
```

## 15. Common Escalation Mistakes

### Mistake 1: Too Slow Escalation

```
❌ Problem:
Spending 2 hours trying to fix SEV1 alone

✓ Solution:
- Escalate SEV1 after 30 minutes
- Don't be a hero
- It's better to escalate early than late
```

### Mistake 2: Premature Escalation

```
❌ Problem:
Escalating before trying basic troubleshooting

✓ Solution:
- Check runbook first
- Try basic fixes (restart, check logs)
- Escalate if still stuck after 15 minutes
```

### Mistake 3: Unclear Handoff

```
❌ Problem:
"Hey @senior-engineer, there's an issue, can you help?"

✓ Solution:
Use escalation template with:
- What's broken
- What you've tried
- Current status
- Why escalating
```

### Mistake 4: Escalating to Wrong Person

```
❌ Problem:
Escalating database issue to frontend team

✓ Solution:
- Check SME registry
- Escalate to relevant expertise
- Use escalation matrix
```

### Mistake 5: No Follow-Up

```
❌ Problem:
Escalating and disappearing

✓ Solution:
- Stay engaged after escalating
- Provide context as needed
- Help with resolution
- Document outcome
```

## 16. Real Escalation Scenarios

### Scenario 1: Database Slow → Escalation to DBA

```
10:00 UTC - Alert: Database slow
10:02 UTC - L1 engineer investigates
10:05 UTC - Finds long-running queries
10:10 UTC - Attempts to kill queries (no improvement)
10:15 UTC - Escalates to L2 (database team)
10:20 UTC - DBA identifies missing index
10:25 UTC - Creates index
10:30 UTC - Performance restored

Escalation: Appropriate (specialized expertise needed)
Time to escalate: 15 minutes (good)
```

### Scenario 2: API Down → Immediate Escalation

```
14:00 UTC - Alert: API returning 100% errors (SEV0)
14:01 UTC - L1 engineer confirms outage
14:02 UTC - Immediately escalates to L2, L3, and management (parallel)
14:05 UTC - War room established
14:10 UTC - Root cause identified (bad deployment)
14:15 UTC - Rollback initiated
14:20 UTC - Service restored

Escalation: Appropriate (SEV0 requires immediate all-hands)
Time to escalate: 2 minutes (excellent)
```

### Scenario 3: Slow Search → Delayed Escalation

```
09:00 UTC - Alert: Search latency high (SEV2)
09:05 UTC - L1 engineer investigates
09:30 UTC - Tries various fixes (no improvement)
10:00 UTC - Still investigating alone
11:00 UTC - Finally escalates to search team
11:15 UTC - Search team identifies Elasticsearch issue
11:30 UTC - Issue resolved

Escalation: Too slow (should have escalated at 10:00 UTC)
Time to escalate: 2 hours (should be 1 hour for SEV2)
```

## Summary

Key takeaways for Escalation Paths:

1. **Know when to escalate** - Severity, time, expertise triggers
2. **Escalate early for critical issues** - SEV0 immediately, SEV1 after 30 min
3. **Use clear escalation paths** - L1 → L2 → L3 → L4
4. **Provide context** - What, tried, status, why escalating
5. **Don't be a hero** - Ask for help when stuck
6. **Use SME registry** - Escalate to right expertise
7. **Follow SLAs** - Response times by level
8. **Avoid alert fatigue** - Don't escalate unnecessarily
9. **Document everything** - Escalation reasons and outcomes
10. **De-escalate properly** - Thank people, document resolution

## Related Skills

- `41-incident-management/incident-triage` - Initial assessment before escalation
- `41-incident-management/severity-levels` - Severity determines escalation urgency
- `41-incident-management/oncall-playbooks` - Runbooks to try before escalating
- `41-incident-management/stakeholder-communication` - Communicating escalations
