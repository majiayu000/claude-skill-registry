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

## Execute Verification

Retrieve ticket details, run both checks, and provide specific improvement recommendations for any failures.
