---
name: issue-tracking-with-beans-and-linear
description: Use when starting work, tracking tasks, or deciding where to record discovered work - clarifies when to use Beans vs Linear
---

# Task Tracking Hierarchy

Two systems serve different purposes. Use the right tool for the job.

| System        | Purpose                    | Persistence  | Audience                |
| ------------- | -------------------------- | ------------ | ----------------------- |
| **Beans**     | Agent memory & audit trail | Git-tracked  | Agents, future sessions |
| **Linear**    | Project tracking           | External     | Humans                  |

Linear is for human-visible project tracking. Beans is for agent implementation memory. Both systems work together with bidirectional linking.

## When to Use Each System

**Beans** — Persistent agent memory (only if the project uses Beans):

- All non-trivial work (3+ steps)
- Work that may span sessions or context boundaries
- Discovered work during implementation
- Anything needing an audit trail
- Skip for trivial single-step tasks (typo fixes, quick lookups)

**Linear** — Human-level tracking:

- Epics and milestones
- User-facing features
- Scope/timeline changes
- Decisions requiring human input
- Security concerns

## Starting Work on a Linear Ticket

When beginning work on a Linear ticket (e.g., ZCO-123):

1. Run `beans query '{ beans(filter: { type: ["epic"], search: "\"<linear-ticket-id>\"" }) { id title status } }'` to find an existing related Beans epic
2. If none exists, create one automatically:
   ```
   beans create "<linear-ticket-id>: <design-name>" --type epic --body "<description>"
   ```
3. All implementation sub-tasks go under this epic as child issues using `--parent <epic-id>`

## Git Commit Messages

All commits related to a Linear ticket MUST reference it:

```
<descriptive message>

Part of ZCO-123.
```

When also closing a Beans issue:

```
<message>

Part of ZCO-123. Closes beans-1234.
```

This ensures Linear ticket traceability in git history even after Beans cleanup.

## Rule: Discovered Work Goes to Beans First

When you discover work during implementation:

1. Create a bean immediately (`--tag discovered`), add a line that explains that it was created while working on current bean, and name the current bean.
2. Assess if it needs Linear escalation
3. Never ignore discovered work due to context pressure

## Rule: Escalate Discovered Work to Linear

Create a Linear ticket for discovered work IF it:

- Affects scope or timeline of current work
- Requires human decision or approval
- Represents user-facing changes
- Is a security concern
- Is significant enough to track at project level

For purely technical implementation details (refactoring, test fixes, code cleanup), keep them in Beans only with `--tag implementation-detail`.

When Beans work reveals an epic-level concern:

1. Create the bean with `--type epic`
2. Immediately create a corresponding Linear ticket, tag it as "Epic"
3. Cross-reference both directions

## Querying Work

- `beans list --status backlog` — Find unblocked work to do next
- `beans list --search "<linear-ticket-id>"` — All Beans issues for a Linear ticket
- `beans show <id>` — View issue details including dependencies

## Provenance for Context

When revisiting a Linear ticket that seems vague, use Beans to trace its origin:

- Find the Beans epic: `beans list --type epic | rg --fixed-strings '<linear-ticket-id>'`
- Use `--tag discovered --link:<epic-ticket-id>` to understand why work was filed
- This provides context that Linear alone cannot

## Completing a Linear Ticket

When all Beans issues under an epic are closed:

1. [ ] Update the Linear ticket with a summary:
   - What was implemented
   - Any discovered work filed as separate Linear tickets
   - Notable decisions or deviations from original scope
2. [ ] Move the Linear ticket to appropriate status

The Linear ticket becomes the permanent record; Beans issues are ephemeral working memory.
