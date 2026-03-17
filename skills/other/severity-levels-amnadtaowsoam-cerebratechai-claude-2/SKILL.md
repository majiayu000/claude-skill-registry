---
name: Severity Levels
description: Comprehensive guide to incident severity classification and response requirements
---

# Incident Severity Levels

## Overview

Severity levels provide a standardized way to classify incidents based on their impact, enabling appropriate response, resource allocation, and communication. Consistent severity classification ensures the right people respond with the right urgency.

**Core Principle**: "Severity drives response - classify quickly, respond appropriately."

## 1. Why Severity Levels Matter

### Benefits of Clear Severity Definitions

```
✓ Appropriate resource allocation
  - Don't wake everyone for minor issues
  - Do mobilize all hands for critical outages

✓ Clear response expectations
  - Everyone knows what SEV1 means
  - Consistent response across teams

✓ Communication clarity
  - Stakeholders understand impact
  - Status page updates match severity

✓ Postmortem requirements
  - SEV0/1: Always postmortem
  - SEV3/4: Optional review

✓ SLA tracking
  - Measure response times by severity
  - Identify improvement areas

✓ Historical analysis
  - Trend severity over time
  - Identify systemic issues
```

### Cost of Inconsistent Severity

```
❌ Over-escalation:
- Alert fatigue
- Wasted resources
- Boy who cried wolf syndrome

❌ Under-escalation:
- Delayed response
- Increased customer impact
- Missed SLA targets
```

## 2. Standard Severity Definitions

### SEV0 / P0: Critical - Complete Outage

```
Definition:
Complete service outage affecting all or nearly all users with severe business impact.

Characteristics:
- 100% or near-100% of users affected
- Core functionality completely unavailable
- Significant revenue impact
- Data loss or security breach
- No workaround available

Examples:
✓ Entire website/app down (returns 500/503)
✓ Database completely unavailable
✓ Payment processing completely halted
✓ Data breach with customer data exposed
✓ Complete datacenter failure
✓ Critical security vulnerability being actively exploited

Response:
- Immediate all-hands response
- War room established
- Executive notification
- Status page: "Major outage"
- Customer communication: Immediate
```

### SEV1 / P1: High - Major Functionality Broken

```
Definition:
Major functionality unavailable or severely degraded, affecting significant portion of users.

Characteristics:
- 25-100% of users affected
- Critical feature unavailable
- Significant business impact
- Limited or no workaround
- Revenue impact

Examples:
✓ Login system down (can't authenticate)
✓ Checkout broken (can't complete purchases)
✓ API returning 50%+ errors
✓ Database in read-only mode
✓ Major feature completely broken
✓ Significant data corruption

Response:
- Immediate response (< 15 minutes)
- Senior engineer + team lead
- War room for extended incidents
- Status page: "Partial outage"
- Customer communication: Within 30 minutes
```

### SEV2 / P2: Medium - Important Feature Degraded

```
Definition:
Important functionality degraded or unavailable, affecting subset of users.

Characteristics:
- 5-25% of users affected
- Important (not critical) feature impacted
- Moderate business impact
- Workaround may exist
- Performance degradation

Examples:
✓ Search feature slow or returning poor results
✓ Email notifications delayed
✓ Dashboard loading slowly
✓ Some API endpoints timing out
✓ Single region experiencing issues
✓ Non-critical feature broken

Response:
- Response within 1 hour
- On-call engineer + escalation if needed
- Status page: "Degraded performance" (optional)
- Customer communication: If prolonged
```

### SEV3 / P3: Low - Minor Issue

```
Definition:
Minor functionality issue with minimal user impact, workaround available.

Characteristics:
- < 5% of users affected
- Minor feature impacted
- Minimal business impact
- Workaround available
- Cosmetic or edge case

Examples:
✓ UI element misaligned
✓ Minor data inconsistency
✓ Rare edge case bug
✓ Non-critical background job failing
✓ Internal tool slow
✓ Documentation outdated

Response:
- Response within 4 hours (business hours)
- On-call engineer (low priority)
- No status page update
- No customer communication
```

### SEV4 / P4: Minimal - Cosmetic Issue

```
Definition:
Cosmetic issue or very minor bug with no user impact.

Characteristics:
- No user impact
- Cosmetic only
- Internal tooling
- Nice-to-have improvement

Examples:
✓ Typo in UI text
✓ Color scheme inconsistency
✓ Internal dashboard formatting
✓ Log message formatting
✓ Code style issue

Response:
- Response next business day or later
- Regular development workflow
- No on-call response needed
- No communication required
```

## 3. Severity Assessment Criteria

### The Four Dimensions

```typescript
interface SeverityAssessment {
  scope: {
    usersAffected: number | string; // Absolute number or percentage
    servicesAffected: string[];
    regionsAffected: string[];
  };
  impact: {
    functionalityLost: 'complete' | 'major' | 'partial' | 'minor' | 'cosmetic';
    businessImpact: 'critical' | 'high' | 'medium' | 'low' | 'none';
    revenueImpact: number; // $ per hour
  };
  duration: {
    actual?: number; // minutes (if resolved)
    projected?: number; // minutes (if ongoing)
  };
  workaround: {
    available: boolean;
    difficulty: 'easy' | 'moderate' | 'difficult' | 'none';
  };
}

function calculateSeverity(assessment: SeverityAssessment): string {
  // Complete outage
  if (assessment.scope.usersAffected === '100%' && 
      assessment.impact.functionalityLost === 'complete') {
    return 'SEV0';
  }

  // Major functionality broken
  if (assessment.impact.functionalityLost === 'major' ||
      assessment.impact.businessImpact === 'critical' ||
      (typeof assessment.scope.usersAffected === 'number' && assessment.scope.usersAffected > 10000)) {
    return 'SEV1';
  }

  // Important feature degraded
  if (assessment.impact.functionalityLost === 'partial' ||
      assessment.impact.businessImpact === 'medium') {
    return 'SEV2';
  }

  // Minor issue
  if (assessment.impact.functionalityLost === 'minor') {
    return 'SEV3';
  }

  // Cosmetic
  return 'SEV4';
}
```

### Scope: How Many Users?

```
100% of users → SEV0 (if critical functionality)
50-100% of users → SEV1
10-50% of users → SEV2
1-10% of users → SEV3
< 1% of users → SEV3 or SEV4

Examples:
- All users can't login → SEV0
- Half of users seeing errors → SEV1
- 10% of users experiencing slow search → SEV2
- Single enterprise customer affected → SEV2 or SEV3 (depends on contract)
- One user reports UI glitch → SEV4
```

### Impact: How Severe?

```
Critical: Core business function unavailable
- Can't process payments → SEV0/1
- Can't access data → SEV0/1
- Security breach → SEV0

High: Important function degraded
- Slow checkout → SEV1/2
- Search not working → SEV1/2
- Email delays → SEV2

Medium: Nice-to-have function affected
- Recommendations not showing → SEV2/3
- Analytics dashboard slow → SEV3

Low: Cosmetic or edge case
- UI misalignment → SEV4
- Rare bug → SEV3
```

### Duration: How Long?

```
Duration affects severity escalation:

Initial classification:
- SEV2: Important feature degraded

After 4 hours:
- Escalate to SEV1 (prolonged impact)

After 8 hours:
- Consider SEV0 (major incident)

Example:
- Search slow for 30 minutes → SEV2
- Search slow for 6 hours → SEV1
- Search down for 12 hours → SEV0
```

### Workaround: Is There an Alternative?

```
No workaround → Higher severity
Easy workaround → Lower severity

Examples:
- Login broken, no alternative → SEV0
- Login broken, can use SSO → SEV1
- Feature A broken, can use Feature B → SEV2
- UI button broken, can use keyboard shortcut → SEV3
```

## 4. Examples for Each Severity Level

### SEV0 Examples

```
1. Complete Service Outage
   Symptom: Website returns 503 for all requests
   Impact: 100% of users can't access service
   Revenue: $50k/hour
   Severity: SEV0

2. Data Breach
   Symptom: Customer data exposed publicly
   Impact: All customers' PII at risk
   Legal: GDPR violation, regulatory fines
   Severity: SEV0

3. Payment Processing Halted
   Symptom: All payment transactions failing
   Impact: Can't process any orders
   Revenue: $100k/hour
   Severity: SEV0

4. Database Deleted
   Symptom: Production database dropped
   Impact: All data lost, service unusable
   Recovery: Hours to restore from backup
   Severity: SEV0

5. Critical Security Vulnerability Exploited
   Symptom: SQL injection being actively exploited
   Impact: Data exfiltration in progress
   Risk: Complete data compromise
   Severity: SEV0
```

### SEV1 Examples

```
1. Login System Down
   Symptom: Authentication service returning errors
   Impact: Users can't login (existing sessions work)
   Affected: ~30% of users (those not logged in)
   Severity: SEV1

2. Checkout Broken
   Symptom: Payment submission fails
   Impact: Can't complete purchases
   Revenue: $20k/hour
   Severity: SEV1

3. Database Read-Only Mode
   Symptom: All write operations failing
   Impact: Can view data, can't create/update
   Affected: 100% of users (partial functionality)
   Severity: SEV1

4. API 50% Error Rate
   Symptom: Half of API requests failing
   Impact: Mobile app intermittently broken
   Affected: 50% of mobile users
   Severity: SEV1

5. Major Feature Completely Broken
   Symptom: Search returns no results
   Impact: Can't find products
   Business: Significant conversion impact
   Severity: SEV1
```

### SEV2 Examples

```
1. Search Slow
   Symptom: Search takes 10s instead of 1s
   Impact: Poor user experience, some users give up
   Affected: All users (degraded, not broken)
   Severity: SEV2

2. Email Notifications Delayed
   Symptom: Emails sent 2 hours late
   Impact: Users don't get timely notifications
   Workaround: Check in-app notifications
   Severity: SEV2

3. Single Region Degraded
   Symptom: US-West region slow
   Impact: 20% of users (in that region)
   Workaround: None for those users
   Severity: SEV2

4. Admin Dashboard Unavailable
   Symptom: Internal admin tool down
   Impact: Support team can't access user data
   Affected: Internal users only
   Severity: SEV2

5. Some API Endpoints Timing Out
   Symptom: /api/recommendations timing out
   Impact: Recommendations not showing
   Workaround: Users can still browse/purchase
   Severity: SEV2
```

### SEV3 Examples

```
1. UI Glitch
   Symptom: Button overlaps text on mobile
   Impact: Looks bad, but still functional
   Affected: Mobile users
   Severity: SEV3

2. Minor Data Inconsistency
   Symptom: User's last login time incorrect
   Impact: Cosmetic, doesn't affect functionality
   Affected: All users (minor)
   Severity: SEV3

3. Rare Edge Case Bug
   Symptom: Error when user has exactly 100 items
   Impact: Very few users affected
   Workaround: Remove one item
   Severity: SEV3

4. Non-Critical Background Job Failing
   Symptom: Daily analytics aggregation not running
   Impact: Internal reports outdated
   Workaround: Run manually
   Severity: SEV3

5. Internal Tool Slow
   Symptom: Developer dashboard takes 5s to load
   Impact: Internal productivity slightly reduced
   Affected: Engineering team only
   Severity: SEV3
```

### SEV4 Examples

```
1. Typo in UI
   Symptom: "Sumbit" instead of "Submit"
   Impact: None (users understand)
   Affected: All users (cosmetic only)
   Severity: SEV4

2. Color Scheme Issue
   Symptom: Button color doesn't match design
   Impact: Purely aesthetic
   Affected: All users (cosmetic)
   Severity: SEV4

3. Documentation Outdated
   Symptom: API docs show old endpoint
   Impact: Developers might be confused
   Workaround: Check code or ask
   Severity: SEV4

4. Log Message Formatting
   Symptom: Logs missing timestamp
   Impact: Slightly harder to debug
   Affected: Engineers only
   Severity: SEV4

5. Code Style Inconsistency
   Symptom: Some files use tabs, others spaces
   Impact: None (linter catches it)
   Affected: Developers only
   Severity: SEV4
```

## 5. Severity and Response SLAs

### Response Time SLAs

```typescript
interface SeveritySLA {
  severity: string;
  acknowledgement: number; // minutes
  initialResponse: number; // minutes
  updateFrequency: number; // minutes
  resolutionTarget: number; // hours
}

const severitySLAs: SeveritySLA[] = [
  {
    severity: 'SEV0',
    acknowledgement: 5,
    initialResponse: 10,
    updateFrequency: 15,
    resolutionTarget: 1
  },
  {
    severity: 'SEV1',
    acknowledgement: 15,
    initialResponse: 30,
    updateFrequency: 30,
    resolutionTarget: 4
  },
  {
    severity: 'SEV2',
    acknowledgement: 60,
    initialResponse: 120,
    updateFrequency: 120,
    resolutionTarget: 24
  },
  {
    severity: 'SEV3',
    acknowledgement: 240,
    initialResponse: 480,
    updateFrequency: 480,
    resolutionTarget: 168 // 1 week
  },
  {
    severity: 'SEV4',
    acknowledgement: 1440, // 1 day
    initialResponse: 2880, // 2 days
    updateFrequency: 0, // No updates needed
    resolutionTarget: 720 // 30 days
  }
];
```

### SLA Table

| Severity | Acknowledge | Initial Response | Update Frequency | Resolution Target |
|----------|-------------|------------------|------------------|-------------------|
| SEV0     | 5 min       | 10 min           | Every 15 min     | 1 hour            |
| SEV1     | 15 min      | 30 min           | Every 30 min     | 4 hours           |
| SEV2     | 1 hour      | 2 hours          | Every 2 hours    | 24 hours          |
| SEV3     | 4 hours     | 8 hours          | Daily            | 1 week            |
| SEV4     | 1 day       | 2 days           | None             | 30 days           |

## 6. Severity Escalation and De-escalation

### When to Escalate Severity

```
Escalation Triggers:

1. Duration
   - SEV2 lasting > 4 hours → SEV1
   - SEV1 lasting > 8 hours → SEV0

2. Scope Expansion
   - Initially 10% users → Now 50% users
   - Single region → Multiple regions

3. New Information
   - Thought it was cosmetic → Actually breaking functionality
   - Discovered data loss

4. Business Impact
   - Revenue impact higher than estimated
   - Major customer affected

5. Cascading Failures
   - One service down → Multiple services affected
```

```typescript
// Auto-escalation logic
function checkEscalation(incident: Incident): boolean {
  const duration = Date.now() - incident.startTime.getTime();
  const durationHours = duration / (1000 * 60 * 60);

  // SEV2 for > 4 hours → SEV1
  if (incident.severity === 'SEV2' && durationHours > 4) {
    escalateIncident(incident, 'SEV1', 'Duration exceeded 4 hours');
    return true;
  }

  // SEV1 for > 8 hours → SEV0
  if (incident.severity === 'SEV1' && durationHours > 8) {
    escalateIncident(incident, 'SEV0', 'Duration exceeded 8 hours');
    return true;
  }

  return false;
}
```

### When to De-escalate Severity

```
De-escalation Triggers:

1. Partial Mitigation
   - SEV0 → SEV1: Core functionality restored, some features degraded
   - SEV1 → SEV2: Workaround implemented

2. Scope Reduction
   - 100% users → 10% users
   - All regions → Single region

3. Better Understanding
   - Thought 100% affected → Actually 10%
   - Thought critical → Actually non-critical

4. Temporary Workaround
   - SEV1 → SEV2: Manual workaround available
```

```typescript
// De-escalation example
async function deEscalateIncident(
  incident: Incident,
  newSeverity: string,
  reason: string
) {
  await updateIncident(incident.id, {
    severity: newSeverity,
    timeline: [
      ...incident.timeline,
      {
        timestamp: new Date(),
        event: `De-escalated from ${incident.severity} to ${newSeverity}`,
        reason
      }
    ]
  });

  await notifyStakeholders({
    incident: incident.id,
    message: `Incident de-escalated to ${newSeverity}: ${reason}`
  });
}
```

## 7. Communication Requirements by Severity

### SEV0/1: Maximum Communication

```
Internal:
✓ Create dedicated Slack channel (#inc-YYYY-NNN)
✓ Establish war room (video call)
✓ Page on-call team + escalation
✓ Notify executives (CTO, CEO for SEV0)
✓ Update every 15-30 minutes

External:
✓ Update status page immediately
✓ Post on social media (if appropriate)
✓ Email affected customers
✓ Prepare customer-facing postmortem

Status Page Updates:
- Initial: "Investigating major outage affecting [service]"
- Progress: "Identified issue, implementing fix"
- Resolution: "Issue resolved, monitoring for stability"
- Follow-up: "Postmortem available at [link]"
```

### SEV2: Moderate Communication

```
Internal:
✓ Create incident channel (optional)
✓ Notify team lead
✓ Update every 2 hours
✓ No executive notification (unless prolonged)

External:
✓ Update status page (if customer-facing)
✓ Email enterprise customers (if affected)
✓ No social media posts

Status Page Updates:
- "Experiencing degraded performance on [service]"
- "Issue resolved"
```

### SEV3/4: Minimal Communication

```
Internal:
✓ Create ticket in issue tracker
✓ Assign to engineer
✓ No real-time updates

External:
✗ No status page update
✗ No customer communication
✗ Fix in regular release cycle
```

## 8. Post-Incident Requirements by Severity

### SEV0/1: Mandatory Postmortem

```
Requirements:
✓ Full postmortem within 48 hours
✓ Root cause analysis (5 Whys)
✓ Timeline of events
✓ Action items with owners
✓ Executive review
✓ Share with entire engineering org
✓ Optional: Public postmortem

Template:
- Executive summary
- Impact (users, revenue, duration)
- Timeline
- Root cause
- What went well / wrong
- Action items
- Lessons learned
```

### SEV2: Recommended Postmortem

```
Requirements:
✓ Lightweight postmortem (if prolonged or interesting)
✓ Brief root cause analysis
✓ Key learnings
✓ Action items
✓ Share with team

Optional:
- Full postmortem if valuable learnings
- Skip if straightforward fix
```

### SEV3/4: Optional Review

```
Requirements:
✓ Document fix in ticket
✓ Update runbook (if applicable)

Optional:
- Team discussion if pattern emerges
- No formal postmortem
```

## 9. Resource Allocation by Severity

### SEV0: All Hands

```
Mobilization:
- Incident Commander (senior engineer or manager)
- Technical Lead (architect or principal engineer)
- On-call team (all available)
- Subject matter experts (database, networking, etc.)
- Communications Lead
- Executive sponsor (CTO)

War Room:
- Video call (Zoom/Meet)
- Dedicated Slack channel
- Shared incident doc

Duration:
- Until resolved
- Rotate responders if > 4 hours
```

### SEV1: Core Team

```
Mobilization:
- On-call engineer (primary)
- Team lead or senior engineer
- Subject matter expert (if needed)
- Communications (if customer-facing)

War Room:
- Slack channel
- Video call (if needed)

Duration:
- Until resolved or de-escalated
```

### SEV2: On-Call + Backup

```
Mobilization:
- On-call engineer
- Escalate to team lead if not resolved in 2 hours

Communication:
- Slack thread or channel

Duration:
- Business hours response
```

### SEV3/4: Single Engineer

```
Mobilization:
- On-call engineer (low priority)
- Or regular development workflow

Communication:
- Ticket comments

Duration:
- Fix in next sprint
```

## 10. On-Call Rotation Intensity

### Severity-Based On-Call Tiers

```
Tier 1 (Primary On-Call):
- Responds to all SEV0-SEV3
- 24/7 availability
- 15-minute response SLA

Tier 2 (Secondary On-Call):
- Escalation from Tier 1
- Subject matter experts
- 30-minute response SLA

Tier 3 (Management):
- SEV0 incidents only
- Executive visibility
- 1-hour response SLA
```

### On-Call Compensation by Severity

```
SEV0:
- Immediate response required
- Compensation: On-call pay + overtime
- Time off in lieu (TOIL)

SEV1:
- Urgent response required
- Compensation: On-call pay
- TOIL for extended incidents

SEV2-4:
- Business hours response acceptable
- Compensation: Standard on-call pay
```

## 11. Severity Level Confusion (Common Mistakes)

### Mistake 1: Confusing Impact with Effort

```
❌ Wrong:
"This will take 2 weeks to fix → SEV0"

✓ Right:
"100% of users can't login → SEV0"
"UI typo affecting 0 users → SEV4 (even if 2-week fix)"

Severity = User Impact, not Engineering Effort
```

### Mistake 2: Internal vs External Impact

```
❌ Wrong:
"Internal dashboard down → SEV1"

✓ Right:
"Internal dashboard down → SEV2 or SEV3"
(Unless it blocks customer support)

Customer-facing > Internal tools
```

### Mistake 3: Potential vs Actual Impact

```
❌ Wrong:
"Security vulnerability discovered → SEV0"

✓ Right:
"Security vulnerability being exploited → SEV0"
"Security vulnerability discovered (not exploited) → SEV1 or SEV2"

Actual impact > Potential impact
```

### Mistake 4: Over-Escalation

```
❌ Wrong:
"Single user reports UI glitch → SEV1"

✓ Right:
"Single user reports UI glitch → SEV3 or SEV4"

Don't cry wolf - save SEV0/1 for real emergencies
```

### Mistake 5: Under-Escalation

```
❌ Wrong:
"50% error rate for 2 hours → SEV2"

✓ Right:
"50% error rate for 2 hours → SEV1"

Don't minimize serious issues
```

## 12. Industry Standards Comparison

### Tech Company Standards

```
Google:
P0 = SEV0 (complete outage)
P1 = SEV1 (major impact)
P2 = SEV2 (moderate impact)
P3 = SEV3 (minor impact)
P4 = SEV4 (trivial)

Amazon:
SEV1 = Critical (customer-facing outage)
SEV2 = High (significant degradation)
SEV3 = Medium (minor degradation)
SEV4 = Low (cosmetic)
SEV5 = Trivial

Microsoft:
Sev A = Critical
Sev B = High
Sev C = Medium
Sev D = Low

Atlassian:
P1 = Critical (system down)
P2 = High (major feature broken)
P3 = Medium (minor feature broken)
P4 = Low (cosmetic)
```

### ITIL Standards

```
Priority 1: Critical
- Complete service outage
- Response: Immediate
- Resolution: 4 hours

Priority 2: High
- Significant degradation
- Response: 1 hour
- Resolution: 24 hours

Priority 3: Medium
- Minor degradation
- Response: 4 hours
- Resolution: 1 week

Priority 4: Low
- Cosmetic issue
- Response: 1 day
- Resolution: 1 month
```

## 13. Customizing Severity for Your Organization

### Factors to Consider

```
1. Company Size
   - Startup: 3 levels (Critical, High, Low)
   - Enterprise: 5 levels (SEV0-SEV4)

2. Industry
   - Healthcare: Stricter (patient safety)
   - Gaming: More lenient (entertainment)
   - Finance: Stricter (regulatory)

3. Customer Base
   - B2C: User count matters
   - B2B: Contract SLAs matter
   - Enterprise: Single customer = high severity

4. Business Model
   - E-commerce: Revenue impact critical
   - SaaS: Uptime critical
   - Freemium: Paying users > free users
```

### Customization Template

```typescript
interface CustomSeverityDefinition {
  level: string;
  name: string;
  description: string;
  criteria: {
    usersAffected: string;
    businessImpact: string;
    examples: string[];
  };
  response: {
    acknowledgement: number;
    initialResponse: number;
    updateFrequency: number;
    resolutionTarget: number;
  };
  communication: {
    internal: string[];
    external: string[];
  };
  postIncident: {
    postmortemRequired: boolean;
    executiveReview: boolean;
  };
}

// Example: E-commerce company
const customSeverities: CustomSeverityDefinition[] = [
  {
    level: 'SEV0',
    name: 'Critical - Revenue Impacting',
    description: 'Complete inability to process orders',
    criteria: {
      usersAffected: '100% or major revenue impact',
      businessImpact: '> $50k/hour revenue loss',
      examples: [
        'Checkout completely broken',
        'Payment processing down',
        'Website completely unavailable'
      ]
    },
    response: {
      acknowledgement: 5,
      initialResponse: 10,
      updateFrequency: 15,
      resolutionTarget: 1
    },
    communication: {
      internal: ['All hands', 'Executive notification', 'War room'],
      external: ['Status page', 'Email to all customers', 'Social media']
    },
    postIncident: {
      postmortemRequired: true,
      executiveReview: true
    }
  }
];
```

## 14. Real Incident Severity Examples

### Example 1: GitLab Database Incident (2017)

```
Incident: Accidental database deletion

Initial Classification: SEV0
Reasoning:
- 100% of users affected
- 6 hours of data lost
- Service completely unavailable
- No workaround

Response:
- All hands on deck
- 18 hours to full recovery
- Public postmortem published

Correct severity: SEV0 ✓
```

### Example 2: AWS S3 Outage (2017)

```
Incident: S3 US-EAST-1 outage

Initial Classification: SEV0
Reasoning:
- Thousands of websites affected
- Complete S3 unavailability
- 4-hour duration
- Massive business impact

Response:
- All AWS teams mobilized
- Detailed postmortem
- Process changes implemented

Correct severity: SEV0 ✓
```

### Example 3: Slack Outage (2021)

```
Incident: Slack service disruption

Initial Classification: SEV1
Reasoning:
- Most users could still access (degraded)
- Some features unavailable
- Intermittent issues
- Workarounds available

Response:
- Core team response
- Status page updates
- Resolved in 2 hours

Correct severity: SEV1 ✓
```

### Example 4: GitHub Actions Slow (2022)

```
Incident: GitHub Actions experiencing delays

Initial Classification: SEV2
Reasoning:
- Service still functional
- Delays but not failures
- Subset of users affected
- Non-critical feature

Response:
- Engineering team investigation
- Status page update
- Resolved in 4 hours

Correct severity: SEV2 ✓
```

## Summary

Key takeaways for Severity Levels:

1. **Classify based on user impact** - Not engineering effort
2. **Use consistent definitions** - Everyone should agree what SEV1 means
3. **Escalate when needed** - Duration and scope changes matter
4. **Communicate appropriately** - SEV0 needs more communication than SEV4
5. **Allocate resources correctly** - Don't wake everyone for SEV3
6. **Follow SLAs** - Response times should match severity
7. **Require postmortems for SEV0/1** - Learn from major incidents
8. **Customize for your org** - But stay close to industry standards
9. **Avoid common mistakes** - Don't over or under-escalate
10. **Document everything** - Severity classification reasoning

## Related Skills

- `41-incident-management/incident-triage` - Initial assessment and classification
- `41-incident-management/escalation-paths` - When and how to escalate
- `41-incident-management/stakeholder-communication` - Communication by severity
- `40-system-resilience/postmortem-analysis` - Post-incident learning
