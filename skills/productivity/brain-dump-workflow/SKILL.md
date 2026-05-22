---
name: brain-dump-workflow
description: Enforces Brain Dump quality workflow for ticket implementation with automatic telemetry
---

# Brain Dump Workflow Skill

This skill guides you through the Brain Dump quality workflow, ensuring consistent code quality and proper tracking across all AI-assisted development.

## Overview

Brain Dump implements a structured quality workflow inspired by Dillon Mulroy's "tracer review" pattern:

```
ready → in_progress → ai_review → human_review → done
```

Each phase has specific requirements and MCP tools to use.

## Starting Work

When you begin working on a ticket:

```
// 1. Start the ticket work (creates git branch, updates status)
mcp__brain-dump__workflow "start-work"({ ticketId: "<ticket-id>" })

// 2. Create a session for state tracking
mcp__brain-dump__session "create"({ ticketId: "<ticket-id>" })
// Returns: { sessionId: "..." }

// 3. Update state as you progress
mcp__brain-dump__session "update-state"({
  sessionId: "<session-id>",
  state: "analyzing",
  metadata: { message: "Reading ticket requirements" }
})
```

## State Transitions

Update your state as you work through phases:

| State          | When to use                            |
| -------------- | -------------------------------------- |
| `analyzing`    | Reading and understanding requirements |
| `implementing` | Writing or modifying source code       |
| `testing`      | Running tests to verify behavior       |
| `committing`   | Creating git commits                   |
| `reviewing`    | Final self-review before completing    |

Example:

```
mcp__brain-dump__session "update-state"({
  sessionId: "<session-id>",
  state: "implementing",
  metadata: { message: "Adding new API endpoint" }
})
```

## Completing Work

When implementation is done:

```
// 1. Run validation
// pnpm type-check && pnpm lint && pnpm test

// 2. Complete the ticket work
mcp__brain-dump__workflow "complete-work"({
  ticketId: "<ticket-id>",
  summary: "Added new API endpoint with validation and tests"
})
// Status becomes: ai_review
```

## AI Review Phase

During AI review, run code review agents:

```
// Submit findings from review
mcp__brain-dump__review "submit-finding"({
  ticketId: "<ticket-id>",
  agent: "code-reviewer",
  severity: "major",
  category: "error-handling",
  description: "Missing error handling for null input"
})

// After fixing, mark as fixed
mcp__brain-dump__review "mark-fixed"({
  findingId: "<finding-id>",
  status: "fixed",
  fixDescription: "Added null check at line 45"
})

// Check if all critical/major issues are resolved
mcp__brain-dump__review "check-complete"({ ticketId: "<ticket-id>" })
// Returns: { canProceedToHumanReview: true/false }
```

## Demo Generation

When AI review passes (all critical/major findings fixed):

```
mcp__brain-dump__review "generate-demo"({
  ticketId: "<ticket-id>",
  steps: [
    { order: 1, description: "Navigate to /settings", expectedOutcome: "Settings page loads", type: "manual" },
    { order: 2, description: "Click 'Add User' button", expectedOutcome: "Modal appears", type: "visual" },
    { order: 3, description: "Submit form with valid data", expectedOutcome: "Success message shown", type: "manual" }
  ]
})
// Status becomes: human_review
```

## Important: Stop at Human Review

After generating the demo script, **STOP**. Do not attempt to auto-approve the ticket.

The human reviewer will:

1. Follow the demo steps
2. Call `mcp__brain-dump__review "submit-feedback"()` with their verdict
3. The ticket moves to `done` only after human approval

## Telemetry

All your tool usage is automatically captured by the telemetry hooks:

- Tool start/end times
- Correlation IDs for pairing events
- Session context

This provides full audit trails for enterprise compliance.

## Quick Reference

| Action         | MCP Tool                                                                        |
| -------------- | ------------------------------------------------------------------------------- |
| Start ticket   | `workflow "start-work"({ ticketId })`                                           |
| Create session | `session "create"({ ticketId })`                                                |
| Update state   | `session "update-state"({ sessionId, state })`                                  |
| Complete work  | `workflow "complete-work"({ ticketId, summary })`                               |
| Submit finding | `review "submit-finding"({ ticketId, agent, severity, category, description })` |
| Fix finding    | `review "mark-fixed"({ findingId, status })`                                    |
| Check review   | `review "check-complete"({ ticketId })`                                         |
| Generate demo  | `review "generate-demo"({ ticketId, steps })`                                   |
