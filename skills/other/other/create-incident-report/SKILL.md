---
name: create-incident-report
description: Create an incident report when the user asks to document an outage, write an incident report, create a post-mortem, log an incident, or structure a real-time incident response
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[incident description, severity, or affected system]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: incident, postmortem, ops
---

# Create Incident Report

## Overview

Create a structured incident report that can be used during a live incident for coordination or after resolution for post-mortem analysis. The report separates what happened (timeline) from why it happened (root cause) and what to do about it (action items), with clear severity definitions and impact quantification.

## Workflow

1. **Read project context** — Check `.chalk/docs/engineering/` for:
   - Architecture docs (to identify affected systems and dependencies)
   - Previous incident reports (to match format and learn from patterns)
   - Monitoring and alerting docs (to reference dashboards)
   - On-call and escalation procedures

2. **Determine incident status** — From `$ARGUMENTS` and conversation:
   - **Active incident**: The incident is ongoing. Create the report in real-time coordination mode with fields to fill as information becomes available. Mark unknowns explicitly.
   - **Post-incident**: The incident is resolved. Create a complete retrospective report.
   - Identify what is known so far: symptoms, affected systems, timeline, actions taken

3. **Assign severity** — Using the severity matrix:
   - **SEV-1 (Critical)**: Complete service outage, data loss or corruption, security breach, revenue-impacting failure affecting all users
   - **SEV-2 (High)**: Major feature outage, significant degradation for most users, data integrity risk
   - **SEV-3 (Medium)**: Partial feature outage, degraded performance, affects subset of users, workaround available
   - **SEV-4 (Low)**: Minor issue, minimal user impact, cosmetic degradation, no data risk

4. **Construct the timeline** — Build a chronological sequence of events:
   - Use timestamps in UTC (or note the timezone)
   - Record: when the issue started, when it was detected, when each action was taken, when it was resolved
   - For active incidents: record events as they happen, leaving future entries as TBD
   - Distinguish between: detection time, response time, mitigation time, resolution time
   - Include automated alerts, human observations, and customer reports

5. **Quantify impact** — Be specific about:
   - Number of users affected (or percentage of total)
   - Duration of impact (from user perspective, not just internal detection)
   - Revenue impact (if measurable or estimable)
   - Data impact (records affected, data lost or corrupted)
   - SLA impact (was an SLA breached? which one?)
   - Downstream impact (did this affect other teams or services?)

6. **Document actions taken** — For each action during the incident:
   - What was done
   - Who did it
   - When it was done
   - What was the result (did it help, make it worse, or have no effect?)

7. **Identify root cause** — For post-incident reports:
   - Distinguish between the trigger (what caused the incident to start) and the root cause (why the system was vulnerable to that trigger)
   - Use the "5 Whys" technique to dig past symptoms
   - For active incidents: note preliminary root cause with confidence level

8. **Write action items** — Concrete, assigned, time-bound follow-ups:
   - Immediate: Prevent recurrence of this exact incident
   - Short-term: Address the systemic weakness that allowed it
   - Long-term: Architectural or process improvements
   - Each action item has an owner and a due date

9. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_incident_*`. Find the highest number and increment by 1.

10. **Write the report** — Save to `.chalk/docs/engineering/<n>_incident_<date>_<slug>.md`.

11. **Confirm** — Present the report with severity, impact summary, and key action items highlighted.

## Filename Convention

```
<number>_incident_<YYYY_MM_DD>_<slug>.md
```

Examples:
- `11_incident_2024_11_15_payment_outage.md`
- `14_incident_2024_12_03_database_failover.md`

## Incident Report Format

```markdown
# Incident Report: <Descriptive Title>

**Severity**: SEV-1 | SEV-2 | SEV-3 | SEV-4
**Status**: Active | Mitigated | Resolved
**Date**: <YYYY-MM-DD>
**Duration**: <total time from detection to resolution>
**Incident Commander**: <name or TBD>
**Report Author**: <name>

## Summary

<One paragraph: What happened, what was the impact, and how was it resolved. Written for a reader who needs to understand the incident in 30 seconds.>

## Impact

| Dimension | Measurement |
|-----------|-------------|
| Users Affected | <number or percentage> |
| Duration (user-facing) | <time from first user impact to resolution> |
| Duration (detection to resolution) | <internal response time> |
| Revenue Impact | <estimated dollar amount or "not applicable"> |
| Data Impact | <records affected, data lost, or "no data impact"> |
| SLA Breach | <Yes — SLA X breached by Y minutes / No> |
| Downstream Services | <list of affected dependent services or "none"> |

## Severity Justification

<Why this severity level was assigned. Reference the severity matrix.>

## Timeline

All times in <timezone>.

| Time | Event | Actor |
|------|-------|-------|
| <HH:MM> | <First symptom or trigger event> | System |
| <HH:MM> | Alert fired: <alert name> | Monitoring |
| <HH:MM> | Incident acknowledged by <name> | <name> |
| <HH:MM> | Investigation began: <what was checked first> | <name> |
| <HH:MM> | Root cause identified: <brief description> | <name> |
| <HH:MM> | Mitigation applied: <what was done> | <name> |
| <HH:MM> | Service restored, monitoring for stability | <name> |
| <HH:MM> | Incident declared resolved | <name> |

## Current Status

<For active incidents: What is the current state? What is being worked on? What is the next expected update?>

<For resolved incidents: Confirmation that the service is fully restored and stable.>

## Detection

| Method | Detail |
|--------|--------|
| How detected | Alert / Customer report / Internal observation |
| Time to detect | <minutes from incident start to first detection> |
| Alert name | <name of the alert that fired, or "no alert — detected manually"> |

**Detection gap analysis**: <Was detection fast enough? If not, what alert should be added?>

## Immediate Actions Taken

| Action | Result | Who | When |
|--------|--------|-----|------|
| <Action description> | Helped / No effect / Made worse | <name> | <HH:MM> |
| <Action description> | <result> | <name> | <HH:MM> |

## Root Cause

### Trigger
<What specific event started the incident? E.g., "A deployment at 14:00 introduced a database query without an index.">

### Root Cause
<Why was the system vulnerable to that trigger? E.g., "No query performance review in the PR process. No slow-query alerting in production.">

### Contributing Factors
- <Factor 1: e.g., "Staging database is too small to reproduce production performance issues">
- <Factor 2: e.g., "No load testing for new database queries">

### 5 Whys

1. **Why** did the service go down? → <answer>
2. **Why** did <answer>? → <deeper answer>
3. **Why** did <deeper answer>? → <even deeper>
4. **Why** did <even deeper>? → <systemic issue>
5. **Why** did <systemic issue exist>? → <root cause>

## Lessons Learned

### What went well
- <Things that worked during the response>

### What went poorly
- <Things that did not work or were missing>

### Where we got lucky
- <Things that could have been worse but were not, by chance>

## Action Items

### Immediate (this week)

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-1 | <Prevent exact recurrence> | <name> | <date> | Open |

### Short-Term (this month)

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-2 | <Address systemic weakness> | <name> | <date> | Open |

### Long-Term (this quarter)

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-3 | <Architectural improvement> | <name> | <date> | Open |
```

## Severity Matrix

| Severity | User Impact | Data Impact | Revenue Impact | Response Time |
|----------|------------|-------------|----------------|---------------|
| SEV-1 | Complete outage for all users | Data loss or corruption | Significant revenue loss | Immediate — all hands |
| SEV-2 | Major feature down for most users | Data integrity risk | Moderate revenue impact | Within 30 minutes |
| SEV-3 | Feature degraded for some users | No data impact | Minimal revenue impact | Within 2 hours |
| SEV-4 | Minor issue for few users | No data impact | No revenue impact | Next business day |

## Active Incident Mode

When creating a report during an active incident, use these conventions:

- Mark unknown fields as `TBD` or `Under investigation`
- Update the timeline as events occur
- Keep the Summary section current with the latest status
- Use the Current Status section for real-time coordination
- Root Cause section should say "Preliminary: <hypothesis>" with a confidence level
- Action Items should focus on immediate mitigation, not long-term improvements (those come after resolution)

## Anti-patterns

- **Blame language** — "Engineer X caused the outage by deploying bad code" is blame. "A deployment introduced a query without an index" is a factual description. Incident reports describe systems and events, not assign personal fault. Blame discourages reporting and transparency.
- **No timeline** — An incident report without a timeline is a narrative, not an investigation tool. Timestamps reveal detection gaps, response delays, and coordination failures. Every significant event needs a timestamp.
- **No impact quantification** — "Some users were affected" is not useful. How many? For how long? What was the revenue impact? Quantified impact drives priority for prevention investments and provides accountability.
- **Mixing "what happened" with "why"** — The timeline records what happened and when. The root cause section explains why. Mixing them creates a confusing narrative. Keep them separate: timeline is facts, root cause is analysis.
- **Action items without owners or dates** — "We should add monitoring" is not an action item. "Add slow-query alerting for queries exceeding 500ms — Owner: Backend Team — Due: 2024-12-15" is an action item. Without ownership and deadlines, action items are wishes.
- **Skipping "what went well"** — Incident reports that only list failures demoralize teams. Acknowledging fast detection, effective communication, or successful rollback reinforces good practices.
- **One-time reports for recurring incidents** — If the same type of incident keeps happening, the action items from previous reports are not being completed. Reference previous incidents and escalate the systemic issue.
- **Post-mortem theater** — Writing a detailed report and then never following up on action items is worse than not writing the report. Track action item completion and hold regular reviews.
