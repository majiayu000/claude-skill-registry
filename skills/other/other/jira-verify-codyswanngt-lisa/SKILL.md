---
name: jira-verify
description: This skill should be used when verifying that a JIRA ticket meets organizational standards for epic relationships and description quality. It checks epic parent relationships and validates description completeness for coding assistants, developers, and stakeholders.
allowed-tools: ["mcp__atlassian__getJiraIssue", "mcp__atlassian__searchJiraIssuesUsingJql", "mcp__atlassian__getAccessibleAtlassianResources"]
---

# Verify JIRA Ticket: $ARGUMENTS

Fetch ticket $ARGUMENTS and verify it meets organizational standards.

## Verification Checks

### 1. Epic Parent Relationship

**Rule**: Non-bug, non-epic tickets MUST have an epic parent

- If missing: Search filter 10089 (Epic Backlog) and suggest appropriate epics

### 2. Description Quality

Verify description adequately addresses:

**Coding Assistants**: Acceptance criteria, requirements, constraints, I/O
**Developers**: Technical context, integration points, testing, edge cases
**Stakeholders**: Business value, user impact, success metrics, summary

### 3. Validation Journey (Frontend Tickets)

**Rule**: Tickets that touch UI (components, labels, or description mentioning frontend, UI, modal, layout, responsive, screen, page, button, form) MUST include a Validation Journey section.

Check by running:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID> 2>&1
```

- If the parser returns steps: PASS
- If the parser fails with "No 'Validation Journey' section found": FAIL — recommend using `/jira-add-journey <TICKET_ID>` to add one

This check is skipped for:
- Pure backend/API tickets (no UI surface)
- Config-only tickets (env vars, feature flags, CI/CD)
- Epic-level tickets (journeys belong on child stories/tasks)

## Execute Verification

Retrieve ticket details, run all checks, and provide specific improvement recommendations for any failures.
