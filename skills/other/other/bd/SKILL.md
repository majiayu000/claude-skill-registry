---
name: bd
description: Backlog management with the bd (beads) utility for issue tracking. Use when creating issues, claiming work, updating task status, closing completed work, or syncing the backlog with git.
---

# bd (Beads) Skill

This skill covers using **bd** for issue tracking and backlog management.

Run `bd onboard` to get started.

## Core Principle: The Backlog Is Everything

**Every task MUST be a bd issue.** No exceptions.

### Why Everything Goes Through bd

- **Visibility**: The human can see all planned and in-progress work
- **Context Management**: Subagents get focused, scoped tasks instead of sprawling conversations
- **Continuity**: If a session ends, the backlog preserves state
- **Auditability**: Every change traces back to an issue

## Recommended: Use task-design Skill

When creating issues, use the [task-design](../task-design/SKILL.md) skill for well-structured tasks.

Well-designed tasks have:
- **Context**: Why this matters
- **Scope**: What to touch (and what NOT to)
- **Requirements**: Verifiable MUST/SHOULD statements
- **Acceptance Criteria**: Checkboxes for completion
- **Validation**: How to verify the work

## Workflow

When asked to do something:

1. **Decompose** the request into discrete, actionable tasks
2. **Author issues** for each task using `bd create`
3. **Delegate** each issue to a subagent for execution
4. **Review** the subagent's work
5. **Close** the issue when complete

## Commands

```bash
bd onboard                              # Get oriented (run once)
bd ready                                # Find available work
bd create "<title>"                     # Create a new issue
bd show <id>                            # View issue details
bd update <id> --status in_progress     # Claim work
bd close <id>                           # Complete work
bd sync                                 # Sync issues with git
bd list                                 # List all issues
```

## Session Management

### Starting a Session

```bash
bd ready                                # See what's available
bd update <id> --status in_progress     # Claim an issue
```

### Completing Work

```bash
bd close <id>                           # Mark issue complete
bd sync                                 # Sync with git
```

### Ending a Session

File issues for any remaining work:

```bash
bd create "Continue section X"
bd create "Review feedback from Y"
```

Update statuses:

```bash
bd close <completed-ids>
bd update <partial-id> --status in_progress
```

Sync everything:

```bash
bd sync
```
