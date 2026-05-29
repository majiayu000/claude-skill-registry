---
name: ai-support
description: "Use when investigating a customer support ticket, reproducing a reported issue, or documenting support findings."
effort: high
argument-hint: "start <ticket-id>|find [query]"
---


# Support

## Purpose

Structured customer support investigation. Organizes findings by ticket, links to relevant code and PRs, and builds a searchable knowledge base of resolved issues.

## Trigger

- Command: `/ai-support start <ticket-id>` or `/ai-support find [query]`
- Context: customer-reported issue, support ticket investigation, escalation from support team.

## When to Use

- Investigating a customer-reported bug or behavior
- Reproducing an issue from a support ticket
- Documenting resolution for future reference
- Escalation requiring code-level investigation

## When NOT to Use

- **Production incidents** -- use `/ai-postmortem`
- **Internal bugs found during development** -- use `/ai-debug`
- **Feature requests** -- use `/ai-triage`

## Modes

### start <ticket-id> -- New investigation

1. **Create structure** -- create `.ai-engineering/support/{date}/{ticket-id}/` directory.
2. **Scaffold investigation** -- create `investigation.md` from template:

```markdown
# {ticket-id}: {title}

**Date**: YYYY-MM-DD
**Customer**: {name/org if known}
**Status**: investigating | resolved | escalated
**Priority**: p1 | p2 | p3

## Issue
{Customer's description -- verbatim or summarized}

## Environment
- Product version:
- OS/Platform:
- Configuration:

## Steps to Reproduce
1. {Step}
2. {Step}
3. {Expected vs actual behavior}

## Findings
{Investigation results, root cause analysis}

## Resolution
{Fix applied, workaround provided, or escalation path}

## Related
- Code: {file paths}
- PR: {links}
- Notes: {links to /ai-note entries}
```

3. **Investigate** -- explore codebase for relevant code paths, check recent changes to affected areas, review error patterns.
4. **Update** -- keep `investigation.md` current as findings emerge.

### find [query] -- Search investigations

1. **Search** -- scan `.ai-engineering/support/` directories for matching content.
2. **Rank** -- prioritize by recency, then relevance.
3. **Present** -- list ticket-id, date, title, status, and resolution summary.

## Procedure for Investigation

1. **Reproduce** -- attempt to reproduce the issue locally using the reported steps.
2. **Isolate** -- narrow down to the specific code path, configuration, or data condition.
3. **Root cause** -- identify why the behavior occurs (bug, misconfiguration, edge case, expected behavior).
4. **Resolve** -- one of:
   - **Fix**: create a PR via `/ai-pr` and link it in the investigation
   - **Workaround**: document the workaround steps
   - **Escalate**: mark as `escalated` with reason and target team
   - **Won't fix**: document rationale

## Quick Reference

```
/ai-support start TICKET-4521         # start investigation
/ai-support start SUP-123             # any ticket ID format works
/ai-support find timeout              # search past investigations
/ai-support find                      # list all investigations
```

## Storage

- Location: `.ai-engineering/support/{YYYY-MM-DD}/{ticket-id}/investigation.md`
- Organized by date for natural chronological browsing

$ARGUMENTS
