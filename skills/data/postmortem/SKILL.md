---
name: optimization.postmortem
phase: optimization
roles:
  - Engineering Lead
  - SRE
  - QA Lead
description: Produce a post-incident analysis capturing timeline, root causes, impact, and corrective actions.
variables:
  required:
    - name: incident_summary
      description: High-level summary of the incident.
    - name: impact_scope
      description: Systems, users, or KPIs impacted.
  optional:
    - name: duration
      description: Incident duration or timestamps.
    - name: mitigation_steps
      description: Steps taken during mitigation.
outputs:
  - Incident timeline and contributing factors.
  - Root cause analysis with classification and detection gaps.
  - Corrective and preventive actions with owners.
---

# Purpose
Standardize postmortem creation so engineering and reliability teams can rapidly document learnings and accountability.

# Pre-run Checklist
- ✅ Gather incident alerts, logs, and chat transcripts.
- ✅ Confirm timeline with responders.
- ✅ Align on severity classification and stakeholders.

# Invocation Guidance
```bash
codex run --skill optimization.postmortem \
  --vars "incident_summary={{incident_summary}}" \
         "impact_scope={{impact_scope}}" \
         "duration={{duration}}" \
         "mitigation_steps={{mitigation_steps}}"
```

# Recommended Input Attachments
- Incident timeline exports (PagerDuty, Opsgenie, Slack).
- Monitoring dashboards or screenshots.
- Customer communications sent during the incident.

# Claude Workflow Outline
1. Summarize incident context, severity, impact, and timeline.
2. Detail sequence of events with timestamps and decision points.
3. Perform root cause analysis using techniques like 5 Whys or fishbone.
4. Document detection gaps and monitoring improvements.
5. Provide corrective and preventive actions with owners and deadlines.

# Output Template
```
# Postmortem — {{incident_summary}}

## Impact & Timeline
- Severity:
- Impact Scope:
- Duration:
| Time | Event | Owner | Notes |
| --- | --- | --- | --- |

## Root Cause Analysis
- Primary Cause:
- Contributing Factors:
- Detection Gaps:

## Corrective Actions
| Action | Owner | Due Date | Status |
| --- | --- | --- | --- |

## Preventive Measures
- Monitoring Updates:
- Process Improvements:
- Follow-up Reviews:
```

# Follow-up Actions
- Review postmortem in reliability or engineering forums.
- Track actions in the incident management system.
- Schedule follow-up to verify preventive measures are in place.
