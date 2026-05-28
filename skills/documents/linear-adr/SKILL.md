---
name: linear-adr
description: Create and manage Architecture Decision Records (ADRs) as Linear issues and documents. Use when asked to record a decision, document architecture, or create an ADR.
user-invocable: true
argument-hint: "<decision title>"
allowed-tools:
  - mcp__linear-server__save_issue
  - mcp__linear-server__save_comment
  - mcp__linear-server__create_document
  - mcp__linear-server__update_document
  - mcp__linear-server__list_documents
  - mcp__linear-server__get_document
  - mcp__linear-server__list_issues
  - mcp__linear-server__list_issue_labels
  - mcp__linear-server__list_projects
---

# Linear ADR Manager

You create and manage Architecture Decision Records (ADRs) tracked as Linear issues with the ADR label and companion Linear documents.

## Workspace Context

- **Team:** Lsdippo
- **ADR Label:** ADR (yellow, #F2C94C)

## ADR Creation Flow

1. **Gather the decision context** from the user
2. **Create a Linear issue** with the ADR label as the tracking ticket
3. **Create a Linear document** with the full ADR content, linked to the issue
4. **Report back** with both the issue ID and document link

## ADR Issue Format

**Title:** `ADR: <Decision Title>`
**Labels:** ADR
**Priority:** Normal (3) unless specified
**Description:**

```markdown
## Decision
[What was decided]

## Status
Proposed | Accepted | Deprecated | Superseded

## Document
[Link to full ADR document will be attached]
```

## ADR Document Template

Create the Linear document with this structure:

```markdown
# ADR: <Decision Title>

## Status
**Proposed** — <date>

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences

### Positive
- [Benefits of this decision]

### Negative
- [Tradeoffs and costs]

### Neutral
- [Other impacts]

## Alternatives Considered
1. **[Alternative A]** — Why it was rejected
2. **[Alternative B]** — Why it was rejected

## References
- [Links to relevant resources, discussions, or prior art]
```

## Managing ADRs

When asked to list or review ADRs:
- List issues with label=ADR
- Show their status (Proposed/Accepted/Deprecated)
- Fetch the linked document for full details if requested

When asked to update an ADR:
- Update both the issue and the document
- Add a comment on the issue noting the change
