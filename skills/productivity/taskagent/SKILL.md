---
name: taskagent
description: >-
  IMMEDIATELY load this skill if you read ANY file containing "taskagent"
  (PLAN.md, org/projects, docs, etc). Also load for multi-session work
  or when user mentions agent tasks. For simple single-session tasks
  without taskagent references, use TodoWrite instead.
---

# Taskagent - Agent Work Tracking

## CRITICAL: Command Name

**Always use `taskagent`, NEVER use `task` directly.**

`taskagent` is a wrapper that uses a separate taskwarrior configuration for agent work.
Using `task` directly will access the human's personal task list, not the agent task tracking system.

**`taskagent` is globally available** - no need to `cd` to any directory. It works from anywhere.

## CRITICAL: Use Partial UUIDs, Not Short IDs

**Always use partial UUIDs (first 8 characters) instead of short numeric IDs.**

Short IDs (1, 2, 3...) renumber whenever tasks are completed, deleted, or modified. This makes them unreliable for persistent references. UUIDs are permanent.

```bash
# BAD - short ID may change
taskagent 3 info

# GOOD - partial UUID is stable
taskagent abc1234d info
```

All reports (`list`, `ready`, `next`) now display `uuid.short` instead of numeric IDs. Use these partial UUIDs in all commands.

When creating tasks or linking dependencies, always capture and use UUIDs:
```bash
taskagent add "New task" project:foo
# Note the UUID from output, use it for future references
```

## Overview

taskagent is a taskwarrior-based tracker for persistent agent memory across sessions. Use for multi-session work with complex context; use TodoWrite for simple single-session tasks.

## When to Use taskagent vs TodoWrite

### Use taskagent when:
- **Multi-session work** - Tasks spanning multiple compaction cycles or days
- **Complex context** - Work needing detailed background or discovered subtasks
- **Project work** - Tasks tied to a specific project with a PLAN.md
- **Side quests** - Exploratory work that might pause the main task
- **Handoff needed** - Work that another session (or human) needs to pick up

### Use TodoWrite when:
- **Single-session tasks** - Work that completes within current session
- **Linear execution** - Straightforward step-by-step tasks with no branching
- **Immediate context** - All information already in conversation
- **Simple tracking** - Just need a checklist to show progress

**Key insight**: If resuming work after 2 weeks would be difficult without taskagent, use taskagent.

## Surviving Compaction Events

**What survives compaction:**
- All taskagent data (tasks, annotations, details, dependencies)
- PLAN.md in project root
- org/projects wiki files

**What doesn't survive:**
- Conversation history
- TodoWrite lists

**Writing annotations for post-compaction recovery:**

Write annotations as if explaining to a future agent with zero conversation context:

```
COMPLETED: Specific deliverables
IN PROGRESS: Current state + next immediate step
BLOCKERS: What's preventing progress
KEY DECISIONS: Important context or user guidance
```

## Recording Learnings and Misalignments

**During the session**, annotate tasks with learnings and misalignments as they occur. These are critical for future sessions and handoff.

**LEARNING** = New information acquired (user preference, codebase pattern, correct approach discovered)
```bash
taskagent <uuid> annotate "LEARNING: User prefers fd over find for file searches."
taskagent <uuid> annotate "LEARNING: Deploy pipeline is in .github/workflows/deploy.yml, not CircleCI."
```

**MISALIGNMENT** = Agent went wrong direction, was corrected (implies wasted effort or wrong output)
```bash
taskagent <uuid> annotate "MISALIGNMENT: Assumed React class components, codebase uses functional only."
taskagent <uuid> annotate "MISALIGNMENT: Put config in src/, should have been lib/ per project convention."
```

**When to record:**
- **LEARNING**: When you discover something useful about the codebase, user preferences, or correct approach
- **MISALIGNMENT**: When the user corrects you or you realize you went the wrong direction

A misalignment often produces a learning - record both:
```bash
taskagent <uuid> annotate "MISALIGNMENT: Used grep, user corrected to use ugrep."
taskagent <uuid> annotate "LEARNING: User prefers ugrep (ug) over grep."
```

These annotations are retrieved during `/handoff` and written to the plan file's `## Learnings` section for future sessions.

## Session Start Protocol

**At session start, always:**

1. Check for ready work:
   ```bash
   taskagent ready
   ```

2. Check for active (in-progress) work:
   ```bash
   taskagent +ACTIVE list
   ```

3. If active work exists, read the task details and annotations:
   ```bash
   taskagent <uuid> agentinfo    # minimal info for agents (preferred)
   taskagent <uuid> info         # full details (shorthand for 'information')
   ```

4. Ask user which project/context if unclear, then check for org/projects file:
   - Look for `~/org/projects/<project>.md` (vimwiki)
   - Read the `## Agent` section for:
     - `taskagent project`: project name (defaults to filename)
     - `plan file`: path to PLAN.md (defaults to repo root)

5. Read the PLAN.md if it exists for additional context

6. Report to user: "X tasks ready, Y in progress. [Summary]. Should I continue with Z?"

## Progress Checkpointing

Update taskagent annotations at these checkpoints:

**Critical triggers:**
- Context running low - User mentions compaction/token limit
- Token budget > 70% - Proactively checkpoint
- Major milestone reached - Completed significant work
- Hit a blocker - Can't proceed, capture what was tried
- Task transition - Switching tasks or closing one

**Checkpoint command:**
```bash
taskagent <uuid> annotate "COMPLETED: X. IN PROGRESS: Y. NEXT: Z."
```

## Core Operations

> **Note**: All commands below use `taskagent`, not `task`. The `taskagent` command is specifically configured for agent work tracking and is separate from the human's personal taskwarrior.

> **Direct execution**: Basic taskagent operations (add, annotate, modify, start, stop, list, info) should be run directly - no subagent needed. Only invoke subagents for reviews (@task-reviewer, @code-reviewer) and complex queries (@taskagent-reader).

### Check ready work (built-in report)
```bash
taskagent ready                    # built-in taskwarrior report, shows unblocked tasks
taskagent project:<name> ready
taskagent blocked                  # show tasks blocked by dependencies
taskagent blocking                 # show tasks that are blocking others
```

### Create new task
```bash
taskagent add "Task title" project:<name>
taskagent add "Task title" project:<name> details:"Longer explanation of context and why"
taskagent add "Task title" project:<name> +side_quest
```

### Link discovered work
```bash
# Use the parent's UUID for discovered_from
taskagent add "Found issue" project:<name> discovered_from:<parent_uuid>
```

### Update task status
```bash
taskagent <uuid> start        # marks in progress
taskagent <uuid> stop         # pauses work
taskagent <uuid> done         # REQUIRES @task-reviewer first! See "Task Completion Review"
```

⚠️ **NEVER mark a task done without invoking @task-reviewer first.**

### Add session notes (annotations)
```bash
taskagent <uuid> annotate "COMPLETED: auth endpoint. IN PROGRESS: tests. NEXT: integration."
```

### View task details
```bash
taskagent <uuid> agentinfo    # minimal info for agents (preferred)
taskagent <uuid> info         # full details (shorthand for 'information')
taskagent project:<name> list
```

### Dependencies
```bash
taskagent <uuid> modify depends:<other_uuid>
```

## Task Fields Reference

| Field | Purpose | When to Set |
|-------|---------|-------------|
| **description** | Short task title | At creation |
| **details** | Initial context, the "why" | At creation |
| **project** | Links to org/projects | At creation |
| **annotations** | Session handoff notes | During work, at checkpoints |
| **discovered_from** | Parent task UUID (not short ID) | When discovered during other work |
| **+side_quest** | Tag for exploratory work | At creation if applicable |
| **+bug** | Tag: something broken | At creation |
| **+feature** | Tag: new functionality | At creation |
| **+task** | Tag: work item (tests, docs, refactoring) | At creation |
| **+chore** | Tag: maintenance (dependencies, tooling) | At creation |
| **+epic** | Tag: large feature, group of related tasks | At creation |

## PLAN.md Convention

**Optional**: Projects can have a `PLAN.md` in the repo root. This can be used independently of org/projects files, or together with them.

```markdown
# Project Plan

## Current Focus
What the agent should prioritize right now.

## Context
Background information helpful for the agent.

## Notes
Human-agent collaborative notes, session summaries.
```

The agent should:
- Read PLAN.md at session start for context
- Update the `## Notes` section with significant progress/decisions (ask first)
- Never modify `## Current Focus` without asking

## Task Completion Review

**MANDATORY**: Before marking ANY task done, you MUST invoke @task-reviewer. There are NO exceptions.

This applies to ALL task types:
- Code tasks
- Verification tasks (reviewer confirms the verification was actually performed)
- Research tasks (reviewer confirms findings were documented)
- Documentation tasks
- ANY task type

### External Ticket Integration

For tasks linked to external tickets (Jira, GitHub Issues):

1. **Before PR/merge**: Invoke `@code-reviewer` with the ticket ID
2. **Before `taskagent done`**: Invoke `@task-reviewer` as usual

Code-reviewer checks ticket alignment; task-reviewer checks task completion. Both are required for externally-tracked work.

Then invoke the reviewer with the UUID (from the report output):

```
@task-reviewer Review task <uuid>
- Project: <project-name>
- PLAN.md: <path or "none">
- org/projects file: <path or "none">
- Summary: <what you did in 1-2 sentences>
- Key files changed: <list main files touched, or "none" for non-code tasks>
```

**Always pass the UUID**, not the short ID or description. The reviewer needs the UUID to look up the task.

Include whichever other fields you have - the reviewer can work with partial context.

**After receiving the review verdict:**
- **PASS**: You may mark the task done with `taskagent <uuid> done`
- **PASS WITH RESERVATIONS**: Do NOT mark done automatically. Ask the human to review and decide.
- **NEEDS WORK**: Address the feedback, then request another review before closing.

## Integration with TodoWrite

**Temporal layering:**

- **TodoWrite** (this hour): Tactical execution, immediate steps
- **taskagent** (this week/month): Strategic objectives, persistent context

**Handoff pattern:**
1. Session start: Read taskagent task -> Create TodoWrite for immediate actions
2. During work: Mark TodoWrite items completed
3. Reach milestone: Update taskagent annotations
4. Session end: TodoWrite disappears, taskagent survives

## org/projects File Format

**Optional**: The org/projects vimwiki file (`~/org/projects/<project>.md`) can be used independently of PLAN.md, or together with it. Format:

```markdown
# Project Name

## Overview
High-level description.

## Resources
- Links, repos, docs

## Tasks
- [ ] Human tasks

## Agent
- **taskagent project**: `project-name`
- **plan file**: `~/path/to/repo/PLAN.md`
```

If `taskagent project` is omitted, defaults to the filename.
If `plan file` is omitted, defaults to `PLAN.md` in repo root.