---
name: issue-implementation
description: This skill should be used when the user asks to "implement task", "claim task", "work on task", or mentions implementing a single task in Trellis. For features, epics, or projects, use issue-implementation-orchestration instead.
allowed-tools:
  - mcp__task-trellis__claim_task
  - mcp__task-trellis__get_issue
  - mcp__task-trellis__get_next_available_issue
  - mcp__task-trellis__complete_task
  - mcp__task-trellis__append_issue_log
  - mcp__task-trellis__append_modified_files
  - mcp__task-trellis__update_issue
  - mcp__task-trellis__list_issues
  - mcp__perplexity-ask__perplexity_ask
  - Task
  - Glob
  - Grep
  - Read
  - Edit
  - Write
  - Bash
  - AskUserQuestion
---

# Implement Trellis Task

Implement a single task from the Trellis task management system. This skill handles direct task implementation only.

**Note**: For implementing features, epics, or projects (which orchestrate multiple tasks), use the `issue-implementation-orchestration` skill instead.

## Task Implementation

Tasks are atomic units of work (1-2 hours) that are implemented directly. Follow the detailed process in [task.md](task.md).

## Input

`$ARGUMENTS` (optional) - Can specify:

- **Task ID**: Specific task ID to claim (e.g., "T-create-user-model")
- **Scope**: Hierarchical scope for task filtering (P-, E-, F- prefixed)
- **Force**: Bypass validation when claiming specific task (only with task ID)

**If no task ID specified**: Claims the next available task based on priority and readiness (prerequisites satisfied).

## Instructions

Read and follow the detailed implementation process in [task.md](task.md).

## Key Constraints

- **Do NOT commit changes** - Leave all changes uncommitted for review by the orchestration skill or another agent
- **Only implement planned work** - Do not create new tasks during implementation
- **Respect dependencies** - Only start work when all prerequisites are completed
- **Stop on errors** - When encountering failures, stop and ask the user how to proceed
- **Track progress** - Update issue logs to track what's been done

## Critical: Error and Failure Handling

<rules>
  <critical>If you encounter a permission error, STOP IMMEDIATELY and report to the user. Do NOT attempt workarounds.</critical>
  <critical>If a hook returns any unexpected errors or fails, STOP IMMEDIATELY and report to the user. Hook errors indicate important validation failures that must be addressed.</critical>
  <critical>NEVER work around errors by skipping steps, using alternative approaches, or ignoring validation failures.</critical>
  <critical>When blocked by any unexpected error - even if you think it doesn't apply to you - your only options are: (1) ask the user for help, or (2) stop completely.</critical>
  <critical>Do NOT assume an error is irrelevant or a false positive. Report any unexpected errors to the user and let them decide.</critical>
  <critical>NEVER mark a task as complete if any unexpected errors occurred during implementation, even if you think the core work succeeded.</critical>
  <critical>NEVER commit changes - leave all changes uncommitted for review by another agent or developer</critical>
</rules>

**Why this matters**: Hooks are configured to enforce quality checks, permissions, and validation rules. When they fail, it usually means something is misconfigured or you lack necessary permissions. Working around these errors masks important problems and can lead to broken or invalid code being committed.
