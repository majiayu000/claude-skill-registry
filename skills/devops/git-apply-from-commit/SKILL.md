---
name: git-apply-from-commit
description: Carefully apply changes from a specific git commit to the current branch.
model: inherit
---
# git-apply-from-commit

Replay a commit from another PR onto the current branch, adapting for base branch changes and user-specified modifications.

## When to Use

Use this skill when the user wants to:

- Cherry-pick a commit but the base branch has diverged significantly
- Apply changes from another PR with modifications
- Replay work from a stale branch onto a fresh one
- Port a feature/fix from one branch to another with adjustments

## Required Input

1. **Commit reference** - One of:
   - PR number (e.g., `#123`)
   - Commit SHA (e.g., `abc1234`)
   - GitHub PR URL (e.g., `https://github.com/org/repo/pull/123`)

2. **User's modification notes** - What they want different from the original

## Approach

### Phase 1: Fetch and Understand the Original Commit

```bash
# If given a PR number, get the commits
gh pr view <PR_NUMBER> --json commits

# View the full diff of the PR
gh pr diff <PR_NUMBER>

# Or if given a commit SHA directly
git show <COMMIT_SHA>
```

Read and understand:

- What files were changed
- What the commit was trying to accomplish
- The context and intent behind the changes

### Phase 2: Analyze Current State

1. **Read the relevant files on the current branch** - Understand current implementations
2. **Identify base branch drift**:
   - Renamed files or moved code
   - Refactored patterns or abstractions
   - New dependencies or removed ones
   - Changed APIs or interfaces
3. **Note conflicts** - Where the original changes would clash with current state

### Phase 3: Gather User Requirements

Use `AskUserQuestion` to clarify:

- Specific modifications they want
- How to handle ambiguous conflicts
- Priority if there are trade-offs

DO NOT proceed with code changes until requirements are clear.

### Phase 4: Apply Changes Intelligently

**Do NOT use blind `git cherry-pick`** - it often fails with diverged branches and creates messy conflicts.

Instead:

1. Manually apply the **intent** of the commit, not just the diff
2. Adapt to current:
   - File locations and names
   - Code patterns and conventions
   - API signatures and interfaces
3. Incorporate user's requested modifications
4. Resolve conflicts based on context, not just syntax

### Phase 5: Review Before Committing

1. Show the user what changed using `git diff`
2. Explain any adaptations made due to base branch changes
3. Highlight where user's modifications were applied
4. Get approval before creating the commit

## Example Usage

**User:** "Replay commit abc123 from PR #456 onto this branch. But I want to use the new `ApiClient` instead of the old `HttpService`."

**Agent actions:**

1. `gh pr diff 456` - View the original changes
2. Read current files that would be affected
3. Note that `HttpService` was refactored to `ApiClient` in base
4. Apply the commit's logic using `ApiClient`
5. Show diff to user for approval
6. Commit with appropriate message

## Notes

- Always read files before modifying them
- Preserve the original commit's intent while adapting implementation
- When in doubt, ask the user
- Reference the original commit/PR in the new commit message for traceability
