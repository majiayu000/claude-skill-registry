---
name: recover-branch-context
description: Get up to speed on the current branch's intent by analyzing commits, changes, and optionally a Linear ticket. Use when starting work on an existing branch.
user-invocable: true
---

# Recover Branch Context

You are tasked with understanding the intent and current state of an existing branch so you can resume or continue work effectively. The code state is your primary source of truth - it may have drifted from any associated Linear ticket.

## Initial Response

When this command is invoked, respond with:

```
I'll help you understand the context of this branch. Let me analyze the commits and changes.

Do you have a Linear ticket ID or URL for this work? (optional - I can proceed without it)
```

Then wait briefly for the user's response. If they provide a ticket, fetch it. If they say no or don't respond quickly, proceed with the analysis.

## Process Steps

### Step 1: Determine the Base Branch

1. **Check common base branch names**:
   ```bash
   git branch -a | grep -E "(main|master|dev|develop)" | head -5
   ```

2. **Find the merge base**:
   ```bash
   # Try dev first (common in this repo), then main/master
   git merge-base HEAD dev 2>/dev/null || git merge-base HEAD main 2>/dev/null || git merge-base HEAD master
   ```

3. **Get current branch name**:
   ```bash
   git branch --show-current
   ```

### Step 2: Gather Commit History Since Divergence

1. **Get all commits since diverging from base**:
   ```bash
   git log --oneline $(git merge-base HEAD dev)..HEAD
   ```

2. **Get detailed commit messages** for understanding intent:
   ```bash
   git log --format="%h %s%n%b" $(git merge-base HEAD dev)..HEAD
   ```

3. **Get files changed across all commits**:
   ```bash
   git diff --name-status $(git merge-base HEAD dev)..HEAD
   ```

### Step 3: Gather Uncommitted Changes

1. **Get staged changes**:
   ```bash
   git diff --name-status --cached
   ```

2. **Get unstaged changes**:
   ```bash
   git diff --name-status
   ```

3. **Get untracked files**:
   ```bash
   git ls-files --others --exclude-standard
   ```

4. **Full working tree status**:
   ```bash
   git status --short
   ```

### Step 4: Fetch Linear Ticket (If Provided)

If the user provides a Linear ticket:

1. Use the `mcp__linear__get_issue` tool to fetch the ticket details
2. Note: The ticket represents the **original requirements** but the code may have evolved

### Step 5: Analyze and Group Changes by Intent

**CRITICAL**: Do not just list files. Group them by logical feature area or intent.

1. **Read key changed files** to understand what they do
2. **Identify patterns** in the changes:
   - New feature additions
   - Bug fixes
   - Refactoring
   - Configuration changes
   - Test additions
3. **Group files by their purpose**, not by directory

### Step 6: Output Summary

Present findings in this structure:

```markdown
# Branch Context: [branch-name]

**Base branch**: [dev/main]
**Commits since divergence**: [count]
**Linear ticket**: [ID if provided, or "None provided"]

## Intent Summary

[1-3 sentences describing the overall goal of this branch based on commits and changes]

## Feature Areas

### [Feature/Intent Area 1]
**Purpose**: [What this group of changes accomplishes]
**Status**: [Complete/In Progress/Not Started]

**Committed changes**:
- `path/to/file.ext:lines` - [brief description]
- `path/to/another.ext` - [brief description]

**Uncommitted changes**:
- `path/to/wip.ext` - [brief description]

### [Feature/Intent Area 2]
...

## Uncommitted Work

**Staged** (ready to commit):
- [files]

**Modified** (not staged):
- [files]

**Untracked** (new files):
- [files]

## Code vs Ticket Drift

[If a Linear ticket was provided, note any discrepancies between what the ticket describes and what the code actually implements. The code is the source of truth.]

## Suggested Next Steps

[Based on the analysis, what appears to be remaining work or natural next actions]
```

## Important Guidelines

1. **Code is the source of truth**: The branch's commits and changes represent what's actually being built, which may differ from the original ticket description.

2. **Group by intent, not structure**: Don't just list files by directory. Understand what each change accomplishes and group related changes together.

3. **Include file:line references**: When describing changes, point to specific locations in files so the user can quickly navigate.

4. **Identify work-in-progress**: Distinguish between completed (committed) work and in-progress (uncommitted) work.

5. **Note drift from ticket**: If a Linear ticket was provided, explicitly call out where the implementation has evolved beyond or differs from the ticket description.

6. **Be concise but complete**: The summary should give someone enough context to immediately start working, without overwhelming them with every detail.

## Example Output

```markdown
# Branch Context: feat/comment-threads

**Base branch**: main
**Commits since divergence**: 3
**Linear ticket**: TASK-142

## Intent Summary

This branch adds threaded comments to tasks, allowing users to start discussion threads on individual tasks and reply to existing comments. The implementation includes a new database table, API routes for CRUD operations, and a collapsible thread UI in the task detail view.

## Feature Areas

### Comments Data Layer
**Purpose**: Database schema and API routes for storing and retrieving comment threads
**Status**: Complete

**Committed changes**:
- `src/db/schema/comments.ts` - New comments table with parent_id for threading
- `src/db/migrations/0012_add_comments.sql` - Migration file
- `src/api/routes/comments.ts` - CRUD endpoints for comments

### Thread UI Components
**Purpose**: Components for displaying and composing threaded comments on tasks
**Status**: In Progress

**Committed changes**:
- `src/components/tasks/CommentThread.tsx` - Recursive thread display component

**Uncommitted changes**:
- `src/components/tasks/CommentComposer.tsx` - Reply/new comment input box
- `src/hooks/useCommentThread.ts` - Data fetching hook for thread state

## Code vs Ticket Drift

The ticket scoped comments as flat (non-threaded), but the implementation adds full threading support with nested replies via a parent_id column.

## Suggested Next Steps

1. Complete the CommentComposer component and wire it into CommentThread
2. Add optimistic updates to useCommentThread for snappy UX
3. Add tests for the comment API routes
```
