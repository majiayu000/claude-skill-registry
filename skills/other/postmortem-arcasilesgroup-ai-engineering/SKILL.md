---
name: postmortem
description: Use when documenting an incident, outage, or production failure using the structured DERP model (Detection, Escalation, Recovery, Prevention).
effort: high
argument-hint: "start|continue <id>|find [query]|generate"
---



# Postmortem

## Purpose

Structured incident postmortem using the DERP model. Guides through Detection, Escalation, Recovery, and Prevention phases with targeted questions. Produces blameless, actionable postmortem documents.

## Trigger

- Command: `/ai-postmortem start|continue|find|generate`
- Context: incident occurred, production failure, outage resolution, near-miss analysis.

## Modes

### start -- New postmortem

1. **Assign ID** -- generate `PM-YYYY-NNN` (sequential within year).
2. **Set status** -- `draft`.
3. **Scaffold** -- create `.ai-engineering/postmortems/{id}.md` with DERP template.
4. **Interview -- Detection**:
   - When was the incident first detected?
   - How was it detected? (monitoring, user report, manual discovery)
   - What was the time between incident start and detection?
   - What monitoring should have caught it earlier?
5. **Interview -- Escalation**:
   - Who was notified and when?
   - Was the escalation path appropriate?
   - Were the right people involved at the right time?
6. **Interview -- Recovery**:
   - What actions were taken to restore service?
   - What was the total downtime/impact duration?
   - Was there a rollback? What was the rollback procedure?
7. **Interview -- Prevention**:
   - Root cause (use 5-Whys if needed)
   - What changes prevent recurrence?
   - Action items with owners and deadlines

Ask ONE section at a time. Wait for answers before proceeding to the next DERP phase.

### continue <id> -- Resume postmortem

1. **Load** -- read `.ai-engineering/postmortems/{id}.md`.
2. **Find gap** -- identify the first incomplete DERP section.
3. **Resume interview** -- continue from the incomplete section.

### find [query] -- Search postmortems

1. **Search** -- scan `.ai-engineering/postmortems/*.md` for matching content.
2. **List** -- show ID, title, date, status, and root cause summary.

### generate -- Create from existing notes

1. **Collect** -- gather incident-related commits, PRs, Slack threads, and notes from context.
2. **Draft** -- populate DERP sections from available data, mark gaps as `[NEEDS INPUT]`.
3. **Review** -- present draft for user validation before saving.

## Document Template

```markdown
# {id}: {title}

**Date**: YYYY-MM-DD
**Status**: draft | in-review | complete
**Severity**: SEV-1 | SEV-2 | SEV-3
**Duration**: {total impact time}

## Detection
{How and when the incident was discovered}

## Escalation
{Notification chain and response timeline}

## Recovery
{Steps taken to restore service}

## Prevention
### Root Cause
{5-Whys analysis}

### Action Items
| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|

## Timeline
| Time | Event |
|------|-------|
```

## Status Progression

`draft` -> `in-review` (all DERP sections complete) -> `complete` (action items assigned)

## Quick Reference

```
/ai-postmortem start                  # begin new postmortem
/ai-postmortem continue PM-2026-001   # resume in-progress postmortem
/ai-postmortem find database           # search past postmortems
/ai-postmortem generate               # generate from existing context
```

## Storage

- Location: `.ai-engineering/postmortems/{id}.md`
- ID format: `PM-YYYY-NNN`

$ARGUMENTS
