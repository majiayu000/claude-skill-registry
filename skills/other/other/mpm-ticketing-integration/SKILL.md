---
name: pm-ticketing-integration
version: "1.0.0"
description: Ticket-driven development protocol
when_to_use: ticket IDs mentioned, issue URLs, work tracking
category: pm-workflow
tags: [tickets, integration, workflow, pm-required]
---

# Ticketing Integration Protocol

## Detection Rules

PM detects ticket context from:
- Ticket ID patterns: `PROJ-123`, `#123`, `MPM-456`, `JJF-62`
- Ticket URLs: `github.com/.../issues/123`, `linear.app/.../issue/XXX`
- Explicit references: "work on ticket", "implement issue", "fix bug #123"
- Session start context (first user message with ticket reference)

## CRITICAL ENFORCEMENT

**PM MUST NEVER use these tools directly - ALWAYS delegate to ticketing agent:**

- ❌ PM using WebFetch on ticket URLs → Delegate to ticketing
- ❌ PM using `mcp__mcp-ticketer__*` tools → Delegate to ticketing
- ❌ PM using ANY tools to access tickets → ONLY delegate to ticketing agent

**Delegation Rule**: ALL ticket operations must be delegated to ticketing agent.

## TICKET-DRIVEN DEVELOPMENT PROTOCOL (TkDD)

**When ticket detected** (PROJ-123, #123, ticket URLs, "work on ticket"):

### PM MUST Execute This Workflow

**1. Work Start** → Delegate to ticketing:
```
Task:
  agent: "ticketing"
  task: "Start work on ticket {ticket_id}"
  acceptance_criteria:
    - Transition ticket to 'in_progress'
    - Add comment: "Work started by Claude MPM"
    - Confirm state change
```

**2. Each Phase** → Comment with deliverables:
```
Task:
  agent: "ticketing"
  task: "Update ticket {ticket_id} with progress"
  context: |
    Phase completed: {phase_name}
    Deliverables: {deliverable_summary}
  acceptance_criteria:
    - Add comment with phase completion details
    - Include links to commits/PRs if applicable
```

**3. Work Complete** → Transition to done/closed:
```
Task:
  agent: "ticketing"
  task: "Complete ticket {ticket_id}"
  context: |
    Work summary: {summary}
    QA verification: {qa_evidence}
    Files changed: {file_list}
  acceptance_criteria:
    - Transition to 'done' or 'closed'
    - Add comprehensive completion comment
    - Link PR if created
```

**4. Blockers** → Comment blocker details:
```
Task:
  agent: "ticketing"
  task: "Report blocker on ticket {ticket_id}"
  context: |
    Blocker: {blocker_description}
    Impact: {impact}
    Waiting on: {dependency}
  acceptance_criteria:
    - Update ticket state to 'blocked'
    - Add blocker details in comment
    - Notify relevant stakeholders if applicable
```

## Documentation Routing with Ticket Context

### When Ticket Context Provided

When user starts session with ticket reference:
- PM delegates to ticketing agent to attach work products
- Research findings → Attached as comments to ticket
- Specifications → Attached as files or formatted comments
- Still create local docs as backup in `{docs_path}/`
- All agent delegations include ticket context

### When NO Ticket Context

- All documentation goes to `{docs_path}/` (default: `docs/research/`)
- No ticket attachment operations
- Named with pattern: `{topic}-{date}.md`

## Ticket Context Propagation

When ticket is detected, PM includes ticket context in all delegations:

```
Task:
  agent: "{any_agent}"
  task: "{task_description}"
  context: |
    Ticket: {ticket_id}
    Ticket summary: {summary_from_ticketing_agent}
    {other_context}
  acceptance_criteria:
    {criteria}
```

This ensures all agents know work is ticket-driven and can reference it.

## Example TkDD Workflow

```
User: "Work on ticket PROJ-123"
    ↓
PM delegates to ticketing: Get ticket details
    ↓
PM delegates to ticketing: Transition to 'in_progress', comment "Work started"
    ↓
PM delegates to research: Investigate approach (with ticket context)
    ↓
PM delegates to ticketing: Comment "Research phase complete: {findings}"
    ↓
PM delegates to engineer: Implement feature (with ticket context)
    ↓
PM delegates to ticketing: Comment "Implementation complete: {files}"
    ↓
PM delegates to QA: Verify implementation
    ↓
PM delegates to ticketing: Transition to 'done', comment "Work complete: {summary}"
```

## Violation Prevention

**Circuit Breaker**: PM using ticket tools directly triggers:
- Violation #1: ⚠️ WARNING - Must delegate immediately
- Violation #2: 🚨 ESCALATION - Session flagged for review
- Violation #3: ❌ FAILURE - Session non-compliant

This enforcement ensures PM maintains pure coordination role.
