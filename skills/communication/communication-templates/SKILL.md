---
name: Communication Templates
description: Pre-written message templates for incident communication across different channels and severity levels.
---

# Communication Templates

## Overview

Communication Templates are pre-written, customizable messages designed for rapid, consistent incident communication. During high-stress incidents, having templates ensures clarity, reduces errors, and speeds up stakeholder notification.

**Core Principle**: "In a crisis, clear communication is as important as technical resolution."

## Best Practices

- Use one source of truth: link every message to the incident doc/war-room.
- Separate audiences: internal can be technical; external must be plain-language and empathetic.
- Communicate facts: explicitly state **what’s known**, **what’s unknown**, and **what’s next**.
- Timebox updates: commit to an update cadence for SEV0/1; update sooner when status changes.
- Protect sensitive details: avoid customer-identifiable data, security details, and internal hostnames.

## Quick Start

1. Pick the correct template (internal/external, severity, channel).
2. Fill variables consistently (use UTC timestamps).
3. Post internal first (Slack/Teams + incident doc), then external (status page/social/email) if needed.
4. Set the next-update time and stick to the cadence.
5. At resolution, publish a clear summary + next steps (postmortem link/timeframe).

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from string import Template


class Severity(str, Enum):
    SEV0 = "SEV0"
    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"


@dataclass(frozen=True)
class IncidentContext:
    service_name: str
    impact: str
    started_utc: str
    incident_id: str
    incident_commander: str
    severity: Severity


INTERNAL_INITIAL_ALERT = Template(
    """🚨 **INCIDENT DETECTED** - $severity

**Service**: $service_name
**Impact**: $impact
**Started**: $started_utc
**Incident Commander**: @$incident_commander
**War Room**: #incident-$incident_id

**Current Status**: Investigating

**Next Update**: in 30 minutes or when status changes
"""
)


def render_internal_initial_alert(ctx: IncidentContext) -> str:
    return INTERNAL_INITIAL_ALERT.substitute(
        severity=ctx.severity.value,
        service_name=ctx.service_name,
        impact=ctx.impact,
        started_utc=ctx.started_utc,
        incident_commander=ctx.incident_commander,
        incident_id=ctx.incident_id,
    )
```

## Production Checklist

- [ ] Templates stored in a single, searchable location (wiki/repo/Slack workflow).
- [ ] Variables standardized (UTC timestamps, incident ID format, severity scale).
- [ ] Update cadence defined per severity (and enforced by the IC).
- [ ] External comms have an approval/ownership path (on-call comms owner).
- [ ] Post-incident: publish customer-facing summary + internal postmortem process.

## Anti-patterns

1. **Speculating publicly**: creates trust debt and complicates follow-up messaging.
2. **Overpromising ETAs**: use time-bounded updates (“next update at…”) instead.
3. **Inconsistent wording across channels**: stakeholders lose confidence; keep a canonical update.
4. **Leaking sensitive details**: never include PII or security-relevant specifics in external posts.

---

## 1. Initial Incident Notification

### Internal Alert (Slack/Teams)
```markdown
🚨 **INCIDENT DETECTED** - SEV[X]

**Service**: [Service Name]
**Impact**: [Brief description of user impact]
**Started**: [Timestamp UTC]
**Incident Commander**: @[Name]
**War Room**: #incident-[ID]

**Current Status**: Investigating

**Next Update**: [Time] or when status changes
```

### External Status Page (Initial)
```markdown
⚠️ **Investigating** - [Service Name]

We are currently investigating reports of [brief issue description]. 
Users may experience [specific impact].

We will provide an update within [timeframe].

Posted: [Timestamp UTC]
```

---

## 2. Progress Updates

### Internal Update (Every 15-30 min for SEV0/1)
```markdown
📊 **INCIDENT UPDATE** - SEV[X] - [Time Elapsed]

**What we know**:
- [Finding 1]
- [Finding 2]

**What we're doing**:
- [Action 1] - @[Owner]
- [Action 2] - @[Owner]

**Blockers**: [None / List blockers]

**Next Update**: [Time]
```

### External Status Page (Update)
```markdown
🔍 **Identified** - [Service Name]

We have identified the issue as [root cause description].
Our team is actively working on a fix.

**Impact**: [Updated impact statement]
**Workaround**: [If available]

Next update: [Timeframe]

Updated: [Timestamp UTC]
```

---

## 3. Resolution Notification

### Internal Resolution
```markdown
✅ **INCIDENT RESOLVED** - SEV[X]

**Duration**: [Start] - [End] ([Total time])
**Root Cause**: [Brief technical explanation]
**Resolution**: [What fixed it]

**Impact Summary**:
- Users affected: [Number/Percentage]
- Revenue impact: [Estimate if known]
- Data loss: [Yes/No]

**Next Steps**:
- [ ] Postmortem scheduled: [Date/Time]
- [ ] Customer communication: [Owner]
- [ ] Monitoring validation: [Owner]

**Incident Commander**: @[Name]
```

### External Status Page (Resolved)
```markdown
✅ **Resolved** - [Service Name]

This incident has been resolved. All systems are operating normally.

**Summary**: [What happened]
**Duration**: [Total time]
**Impact**: [Who was affected]

We apologize for any inconvenience. A detailed postmortem will be published within [timeframe].

Resolved: [Timestamp UTC]
```

---

## 4. Customer Email Templates

### SEV0/1 - Direct Customer Email
```markdown
Subject: [Service Name] Incident Update - [Date]

Dear [Customer Name],

We want to inform you about a service disruption that occurred on [Date] affecting [Service Name].

**What Happened**:
Between [Start Time] and [End Time] UTC, [brief description of issue].

**Impact to You**:
[Specific impact to this customer]

**Resolution**:
Our engineering team [what we did to fix it].

**What We're Doing**:
To prevent this from happening again, we are:
- [Action 1]
- [Action 2]

We sincerely apologize for any inconvenience this may have caused. If you have any questions or concerns, please contact [support email/phone].

Thank you for your patience and understanding.

Best regards,
[Team Name]
```

### SEV2 - General Customer Notice
```markdown
Subject: Service Update - [Service Name]

Hello,

We experienced a brief service disruption on [Date] that may have affected your use of [Service Name].

**Timeline**: [Start] - [End] UTC
**Impact**: [Brief description]
**Status**: Fully resolved

Our team has implemented additional monitoring to prevent similar issues.

If you experienced any data inconsistencies or have questions, please reach out to our support team.

Thank you,
[Team Name]
```

---

## 5. Executive Summary Template

```markdown
# Incident Executive Summary
**Incident ID**: INC-[YYYY-MM-DD-XXX]
**Severity**: SEV[X]
**Date**: [Date]

## TL;DR
[One-sentence summary of what happened and impact]

## Business Impact
- **Duration**: [X hours Y minutes]
- **Users Affected**: [Number/Percentage]
- **Revenue Impact**: $[Amount] (estimated)
- **SLA Breach**: [Yes/No - Details]

## What Happened
[2-3 paragraph non-technical explanation]

## Root Cause
[Simple explanation without jargon]

## Immediate Actions Taken
1. [Action 1]
2. [Action 2]

## Prevention Measures
1. [Long-term fix 1] - Owner: [Name] - ETA: [Date]
2. [Long-term fix 2] - Owner: [Name] - ETA: [Date]

## Customer Communication
- Status page updates: [X] times
- Direct emails sent: [Yes/No]
- Support tickets opened: [Number]

**Prepared by**: [Name]
**Date**: [Date]
```

---

## 6. Social Media Templates

### Twitter/X
```
We're currently experiencing issues with [Service]. Our team is investigating and we'll share updates here and at [status page link]. We apologize for the inconvenience.
```

### LinkedIn (Post-Resolution)
```
Earlier today, we experienced a service disruption affecting [Service]. Our team responded quickly and service has been fully restored.

We take reliability seriously and are implementing additional safeguards to prevent similar issues.

Thank you to our customers for your patience.

Full details: [link to postmortem]
```

---

## 7. Severity-Specific Templates

### SEV0 - All Hands on Deck
```markdown
🔴 **SEV0 CRITICAL INCIDENT** 🔴

**IMMEDIATE ACTION REQUIRED**

Service: [Name]
Impact: COMPLETE OUTAGE - All users affected
Started: [Time]

**War Room**: [Link/Channel]
**Bridge**: [Conference call number]

**All hands**: Please join war room immediately if you can assist with:
- [Service A] expertise
- [Service B] expertise
- Customer communication

IC: @[Name]
```

### SEV3 - Minor Issue
```markdown
⚠️ **SEV3 - Minor Issue**

Service: [Name]
Impact: [Small subset of users / Degraded performance]
Started: [Time]

**Status**: Monitoring
**Owner**: @[Name]

No immediate action required. Updates in #incidents if escalates.
```

---

## 8. Handoff Template

```markdown
🔄 **INCIDENT HANDOFF** - SEV[X]

**From**: @[Current IC]
**To**: @[New IC]
**Time**: [Timestamp]

**Current Status**: [Investigating/Mitigating/Monitoring]

**What's Been Done**:
- [Action 1] ✅
- [Action 2] ✅
- [Action 3] ⏳ In progress

**Active Blockers**:
- [Blocker 1] - Waiting on [Team/Person]

**Next Steps**:
1. [Action to take]
2. [Action to take]

**Key Contacts**:
- SME: @[Name]
- Customer Comms: @[Name]

**Documentation**: [Link to incident doc]

@[New IC] - You have the helm. Good luck! 🫡
```

---

## 9. Template Customization Guidelines

### Variables to Replace
- `[Service Name]`: The affected service
- `[Timestamp UTC]`: Always use UTC for clarity
- `[Impact]`: Specific user-facing impact
- `[Root Cause]`: Technical or simplified explanation
- `@[Name]`: Tag specific people
- `[X]`: Severity level (0-4)

### Tone Guidelines
- **Internal**: Direct, technical, action-oriented
- **External**: Empathetic, clear, non-technical
- **Executive**: Business-focused, concise, forward-looking
- **Social**: Brief, transparent, reassuring

---

## 10. Template Storage and Access

### Recommended Tools
- **Confluence/Notion**: Centralized wiki with search
- **Slack Workflows**: Auto-populate templates with `/incident` command
- **PagerDuty**: Built-in status page integration
- **Statuspage.io**: Template library for status updates

### Template Versioning
```
communication-templates/
├── v1.0-initial-alert.md
├── v1.0-progress-update.md
├── v1.0-resolution.md
├── v2.0-initial-alert.md (updated 2024-01-15)
└── README.md (changelog)
```

---

## Related Skills
- `41-incident-management/stakeholder-communication`
- `41-incident-management/severity-levels`
- `41-incident-management/escalation-paths`
