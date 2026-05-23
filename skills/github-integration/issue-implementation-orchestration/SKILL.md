---
name: issue-implementation-orchestration
description: Orchestrates issue implementation with automatic review and commits. Use when asked to "implement feature", "implement epic", "implement project", "execute feature", "execute epic", "execute project", or when you want implementations automatically reviewed and committed.
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
  - TaskOutput
  - Glob
  - Grep
  - Read
  - Bash
  - AskUserQuestion
---

# Orchestrate Issue Implementation

Orchestrate the implementation of a parent issue (project, epic, or feature) by executing its child issues sequentially, reviewing each implementation, and committing approved changes.

## Goal

Complete all planned child issues within a parent by:
1. Spawning task implementations via the `issue-implementation` skill
2. Reviewing completed work via the `issue-implementation-review` skill
3. Committing approved changes
4. Updating documentation when all children are complete

## Issue Hierarchy

| Parent Type | Child Type | Child's Children |
| ----------- | ---------- | ---------------- |
| Project     | Epics      | Features → Tasks |
| Epic        | Features   | Tasks            |
| Feature     | Tasks      | (none)           |

## Process

### 1. Identify Parent Issue

#### Input

`$ARGUMENTS` - Can specify:

- **Issue ID**: Specific issue to implement (e.g., "P-xxx", "E-xxx", or "F-xxx")
- **Scope**: Limit search to issues within a parent scope

Use `get_issue` to retrieve the issue details. If no ID is specified, use `get_next_available_issue` with the appropriate `issueType` to find the next available issue.

### 2. Create Feature Branch

Before starting implementation, ensure work is on a feature branch.

#### Check Current Branch

Use Bash to check the current branch:

```bash
git branch --show-current
```

#### Branch Logic

- **If on `main`**: Create and checkout a feature branch:
  ```bash
  git checkout -b feature/{ISSUE_ID}
  ```
  Example: `feature/F-add-user-auth` or `feature/E-auth-system`

- **If already on a non-main branch**: Continue without branching

#### Log Branch Status

Use `append_issue_log` to record:
- Branch created: "Created feature branch feature/{ISSUE_ID}"
- Existing branch: "Continuing on existing branch {BRANCH_NAME}"

### 3. Verify Planned Work Exists

**CRITICAL**: Before starting, verify all work is planned.

1. Use `list_issues` to get all direct children of this issue
2. For each child, recursively verify its children exist (down to tasks)
3. Review the complete work breakdown for completeness

**Verification depth by parent type:**

- **Feature**: Verify tasks exist
- **Epic**: Verify features exist, and each feature has tasks
- **Project**: Verify epics exist, each epic has features, and each feature has tasks

**If children are missing:**

- **STOP immediately**
- Inform the user that the issue has unplanned work
- List what appears to be missing:
  - Children that have no sub-children
  - Functionality from the description not covered
- Ask the user to complete the planning before proceeding
- **Do NOT create issues yourself** - implementation does not include planning

### 4. Evaluate Complexity and Plan (Optional)

Before executing children, evaluate whether the work would benefit from upfront planning.

#### Complexity Signals

Consider spawning a planner for issues with:

- **Multiple tasks** (more than 3-4 tasks)
- **Refactoring or migration** language in task descriptions
- **Architectural changes** mentioned
- **Multiple integration points** or subsystems involved
- **Cross-cutting concerns** that affect multiple areas

This is a judgment call—no hard threshold required.

#### Spawn Implementation Planner

If judged sufficiently complex:

1. Use the `Task` tool to spawn `issue-implementation-planner` as an async subagent:
   ```
   Task tool parameters:
   - subagent_type: "general-purpose"
   - description: "Plan implementation for {ISSUE_ID}"
   - run_in_background: true
   - prompt: |
       Use the /issue-implementation-planner skill to create an implementation plan for {ISSUE_ID}.

       Issue: {ISSUE_ID} - {ISSUE_TITLE}
       Description: {ISSUE_DESCRIPTION}

       Children to implement:
       {LIST_OF_CHILDREN_WITH_DESCRIPTIONS}

       Create a comprehensive plan that identifies key files, patterns, and implementation approach.
   ```

2. Use `TaskOutput` to wait for the planner to complete
3. Store the planner's output as context for implementation agents
4. Include relevant plan context when spawning child implementations

### 5. Determine Execution Order

Analyze the direct children to determine the correct execution order:

1. **Check prerequisites**: Each child may have `prerequisites` listing IDs that must complete first
2. **Check status**: Skip children that are already `done` or `wont-do`
3. **Build execution queue**: Order children so all prerequisites are satisfied before each runs

**Execution Rules:**

- A child can only start when ALL its prerequisite issues are `done`
- If a child has no prerequisites, it can start immediately (after any currently running child)
- Execute children **sequentially** - wait for each to complete before starting the next

### 6. Execute Children

For each child in the execution queue:

#### 6.1 Verify Child is Ready

- Check all prerequisites are `done`
- Check child status is `open` or `draft` (not already `in-progress` or `done`)
- If not ready, skip and check next child

#### 6.2 Launch Child Implementation

Use the `Task` tool to spawn a subagent that implements the child:

**For Tasks** - spawn the `issue-implementation` skill:
```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Implement task [TASK_ID]"
- prompt: |
    Use the /issue-implementation skill to implement task [TASK_ID].

    Context:
    - Parent: [PARENT_ID] - [PARENT_TITLE]
    - Task: [TASK_ID] - [TASK_TITLE]

    [INCLUDE_PLAN_CONTEXT_IF_AVAILABLE]

    Implement this task following the task implementation workflow.
    Do NOT commit your changes - leave them uncommitted for review.

    If you encounter any errors or blockers, STOP and report back.
```

**For Features/Epics/Projects** - spawn the `issue-implementation-orchestration` skill (recursive):
```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Orchestrate [CHILD_TYPE] [CHILD_ID]"
- prompt: |
    Use the /issue-implementation-orchestration skill to implement [CHILD_TYPE] [CHILD_ID].

    Context:
    - Parent: [PARENT_ID] - [PARENT_TITLE]
    - [CHILD_TYPE]: [CHILD_ID] - [CHILD_TITLE]

    [INCLUDE_PLAN_CONTEXT_IF_AVAILABLE]

    Orchestrate the implementation of this issue and its children.

    If you encounter any errors or blockers, STOP and report back.
```

**Wait for the subagent to complete** before proceeding.

#### 6.3 Verify Child Completion

After the subagent returns:

1. Use `get_issue` to check the child's status
2. If status is `done`: Continue to review step (for tasks) or next child (for orchestrated children)
3. If status is NOT `done`: **STOP** and handle the error (see Section 7)

#### 6.4 Review Task Implementation

After a task completes successfully, evaluate if a review is warranted.

**Skip review for trivial tasks** (judgment call):
- Single configuration change
- One-line fix
- Simple rename or move

**For non-trivial tasks**, spawn `issue-implementation-review`:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Review implementation of [TASK_ID]"
- run_in_background: true
- prompt: |
    Use the /issue-implementation-review skill to review task [TASK_ID].

    Task: [TASK_ID] - [TASK_TITLE]
    Parent Feature: [PARENT_ID] - [PARENT_TITLE]

    Review the implementation for correctness, completeness, and simplicity.
```

Use `TaskOutput` to wait for the review to complete.

**Handle review outcomes:**

- **No findings / empty output**: Proceed to commit
- **Findings identified**: You MUST address ALL findings before proceeding:
  1. **Review each finding** - Evaluate whether it's valid
  2. **Fix valid findings** - Make the necessary changes, including minor ones (documentation, style, small improvements)
  3. **Challenge incorrect findings** - If you believe a finding is wrong, explain your reasoning in the issue log. You are not required to blindly follow incorrect recommendations, but you must justify skipping any finding.
  4. **Re-run review** after making fixes to verify they were addressed
  5. **Proceed to commit** only when all valid findings are resolved
- **Questions requiring answers**:
  - **STOP** orchestration
  - Use `AskUserQuestion` to get answers from the user
  - Re-run review with the answers provided

**CRITICAL**: Do not categorize findings as "minor" and skip them. Every finding from a review must be either fixed or explicitly challenged with reasoning. Ignoring feedback is not acceptable.

#### 6.5 Commit Task Changes

After implementation and review pass, commit the changes.

**CRITICAL - Update Trellis BEFORE committing:**

The `.trellis/` directory contains issue state that must be included in commits. Always update Trellis issues first, then commit.

1. **Update Trellis state** (if not already done):
   - Ensure task is marked complete via `complete_task`
   - Append any final log entries via `append_issue_log`

2. **Commit the changes** using the `/git:commit` skill (if available) or manually:

   **Using the skill** (preferred):
   ```
   /git:commit [TASK_ID] Summary of changes
   ```

   **Manual fallback** (if skill unavailable):
   ```bash
   git add .
   git commit -m "[TASK_ID] Summary of changes"
   ```
   Example: `[T-add-user-validation] Add email validation to user registration`

3. **Verify commit succeeded** and no `.trellis/` changes remain uncommitted

4. **Log the commit** using `append_issue_log` on the parent issue

### 7. Handle Errors

<rules>
  <critical>If you encounter a permission error, STOP IMMEDIATELY and report to the user. Do NOT attempt workarounds.</critical>
  <critical>If a hook returns any unexpected errors or fails, STOP IMMEDIATELY and report to the user. Hook errors indicate important validation failures.</critical>
  <critical>NEVER work around errors by skipping steps, using alternative approaches, or ignoring validation failures.</critical>
  <critical>When blocked by any unexpected error - even if you think it doesn't apply to you - your only options are: (1) ask the user for help, or (2) stop completely.</critical>
  <critical>Do NOT assume an error is irrelevant or a false positive. Report any unexpected errors to the user and let them decide.</critical>
</rules>

If a child fails or the subagent reports an error:

1. **Stop execution** - Do not proceed to other children
2. **Log the failure** - Use `append_issue_log` on the parent to record what happened
3. **Ask the user** - Use AskUserQuestion to report the failure and ask how to proceed:
   - Retry the failed child
   - Skip the failed child and continue
   - Stop orchestration entirely
4. **Follow user direction** - Do what the user decides

**Common error scenarios that require stopping:**

- Permission denied when running commands
- Unexpected hook failures (pre-commit, post-edit, quality checks)
- Subagent returning errors or incomplete results
- Git commit failures

**Why this matters**: Hooks are configured to enforce quality checks and validation rules. When they fail, it usually means something is misconfigured or you lack necessary permissions. Working around these errors masks important problems and can lead to broken code being committed.

### 8. Update Documentation

When all children are done (before marking the parent as complete):

#### Spawn Documentation Updater

Use the `Task` tool to spawn `docs-updater`:

```
Task tool parameters:
- subagent_type: "general-purpose"
- description: "Update documentation for [ISSUE_ID]"
- run_in_background: true
- prompt: |
    Use the /docs-updater skill to review and update documentation.

    Issue: [ISSUE_ID] - [ISSUE_TITLE]

    Review the changes made during this implementation and update any relevant
    documentation files (CLAUDE.md, README.md, docs/**).
```

Use `TaskOutput` to wait for the docs-updater to complete.

#### Commit Documentation Changes

If the docs-updater made changes:

**CRITICAL - Update Trellis BEFORE committing:**

1. **Update Trellis first**:
   - Log the documentation update using `append_issue_log`
   - Make any other Trellis updates needed

2. **Commit the changes** using the `/git:commit` skill (if available) or manually:

   **Using the skill** (preferred):
   ```
   /git:commit docs: update documentation for [ISSUE_ID]
   ```

   **Manual fallback** (if skill unavailable):
   ```bash
   git add .
   git commit -m "docs: update documentation for [ISSUE_ID]"
   ```

3. **Verify no `.trellis/` changes remain uncommitted**

### 9. Complete Parent Issue

When all children are done and documentation is updated:

1. Verify all children have status `done` (or `wont-do` if skipped by user direction)
2. Update the parent status to `done` using `update_issue`
3. Log completion using `append_issue_log`
4. **If any uncommitted changes exist** (including `.trellis/`), commit them using the `/git:commit` skill (if available) or manually:

   **Using the skill** (preferred):
   ```
   /git:commit chore: complete [ISSUE_ID]
   ```

   **Manual fallback** (if skill unavailable):
   ```bash
   git add .
   git commit -m "chore: complete [ISSUE_ID]"
   ```
5. **Verify no uncommitted changes remain** - especially in `.trellis/`
6. Report summary to user:
   - Total direct children completed
   - Total descendants completed (all levels)
   - Any issues skipped
   - Commits created
   - Documentation updates made
   - Overall outcome

## Progress Tracking

Throughout orchestration:

- Use `append_issue_log` on the parent to record progress
- Report status to user after each child completes
- Keep user informed of which child is currently running

## Important Constraints

- **No parallel execution**: Run only one child at a time
- **No creating work**: Do not create new issues; only execute planned work
- **Respect dependencies**: Never start a child before its prerequisites are done
- **Stop on failure**: Always stop and ask user when something goes wrong
- **Ask questions**: Use AskUserQuestion when uncertain about anything
- **Trellis before commits**: Always update Trellis issues BEFORE making git commits
- **Commit after each task**: Ensure changes are committed before moving to the next task
- **Update docs before completing**: Always run docs-updater before marking parent as done
- **No uncommitted Trellis state**: Never finish with uncommitted `.trellis/` changes

<rules>
  <critical>STOP on ANY error - permission errors, hook failures, or unexpected results</critical>
  <critical>NEVER work around errors or assume they don't apply</critical>
  <critical>Do NOT proceed to next child if current child encountered errors</critical>
  <critical>Report ALL errors to the user, even if you think they're false positives</critical>
  <critical>Update Trellis issues BEFORE git commits so .trellis/ changes are included</critical>
  <critical>Never leave .trellis/ changes uncommitted when finishing work</critical>
  <critical>Address ALL review findings - do not ignore feedback because it seems minor</critical>
  <critical>If you skip a review finding, you MUST explain why you believe it is incorrect</critical>
</rules>
