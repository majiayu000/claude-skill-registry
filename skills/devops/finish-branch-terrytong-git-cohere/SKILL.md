---
name: finish-branch
description: "Clean up after a feature branch or experiment is complete. This skill deletes the git worktree and branch ONLY AFTER the associated PR has been merged. It also closes any related GitHub issues. Use this after your PR has been merged to keep the repository clean."
user_invocable: true
---

# Finish Branch - Post-Merge Cleanup

## Overview

This skill handles the cleanup after a PR has been merged. It will:
1. Verify the PR is actually merged (REQUIRED before any cleanup)
2. Delete the git worktree
3. Delete the local and remote branch
4. Close any related GitHub issues

**IMPORTANT**: This skill will NOT delete anything unless the PR is confirmed merged.

## Usage

Invoke this skill when:
- Your PR has been merged and you want to clean up
- You finished an experiment and the results are merged to main
- You need to remove an old worktree after successful merge

## Workflow

### Step 1: Identify the Branch and PR

First, ask the user which branch to clean up:

```
Which branch would you like to finish?

Please provide:
1. Branch name (e.g., exp/cot-faithfulness or feature/add-dark-mode)
2. PR number (if known) or I can find it
```

### Step 2: Verify PR is Merged

**CRITICAL**: Before any deletion, verify the PR is merged:

```bash
# Find PR for the branch
gh pr list --head {branch-name} --state merged

# Or check specific PR
gh pr view {pr-number} --json state,mergedAt

# The PR MUST have state: "MERGED" before proceeding
```

If the PR is NOT merged:
```
## Cannot Proceed

The PR for branch '{branch-name}' is not yet merged.
Current state: {state}

Options:
1. Wait for the PR to be merged, then run /finish-branch again
2. Merge the PR now (if you have permissions)
3. Cancel cleanup

What would you like to do?
```

### Step 3: Find Related Issues

```bash
# Get the PR body and look for issue references
gh pr view {pr-number} --json body,closingIssuesReferences

# Common patterns to find:
# - "Closes #123"
# - "Fixes #123"
# - "Resolves #123"
# - Issue links in PR body
```

### Step 4: Delete Worktree (if exists)

```bash
# List worktrees to find the one for this branch
git worktree list

# Remove the worktree
# The worktree path is usually ../worktree-{name} or ../experiment-{name}
git worktree remove ../worktree-{name}

# If the worktree has uncommitted changes, force removal (after user confirmation)
git worktree remove --force ../worktree-{name}
```

### Step 5: Delete Local and Remote Branch

```bash
# Delete local branch
git branch -d {branch-name}

# If the branch wasn't fully merged (shouldn't happen if PR is merged)
# Ask user before force deleting
git branch -D {branch-name}

# Delete remote branch
git push origin --delete {branch-name}
```

### Step 6: Close Related Issues

```bash
# Close each related issue
gh issue close {issue-number} --comment "Closed via merged PR #{pr-number}"
```

### Step 7: Report Results

```
## Branch Cleanup Complete

**Branch**: {branch-name}
**PR**: #{pr-number} (merged at {merged-at})

### Cleanup Actions
- [x] PR verified as merged
- [x] Worktree removed: ../worktree-{name}
- [x] Local branch deleted: {branch-name}
- [x] Remote branch deleted: origin/{branch-name}
- [x] Related issues closed: #{issue-1}, #{issue-2}

### Notes
{any-warnings-or-notes}
```

## Error Handling

### PR Not Found
```
Could not find a PR for branch '{branch-name}'.

Options:
1. Provide the PR number manually
2. Check if the branch was pushed to remote
3. Cancel cleanup
```

### Worktree Not Found
```
No worktree found for branch '{branch-name}'.
This is fine if you were working in the main repository.

Proceeding with branch deletion...
```

### Branch Has Unmerged Commits
```
WARNING: Branch '{branch-name}' has commits not in the merged PR.

Unmerged commits:
- {commit-hash}: {commit-message}

Options:
1. Force delete anyway (lose these commits)
2. Cherry-pick commits to a new branch first
3. Cancel cleanup
```

### Issue Close Failed
```
Could not close issue #{issue-number}: {error}

This might be because:
- Issue doesn't exist
- Issue is already closed
- Insufficient permissions

Proceeding with other cleanup tasks...
```

## Safety Checks

This skill includes several safety measures:

1. **PR merge verification is mandatory** - Will not proceed without confirmed merge
2. **User confirmation for force operations** - Always asks before force deleting
3. **Unmerged commit detection** - Warns if local branch has extra commits
4. **Detailed reporting** - Shows exactly what was deleted

## Examples

### Basic Usage
```
User: /finish-branch
Assistant: Which branch would you like to finish? Please provide the branch name or PR number.

User: exp/mi-estimation, PR #42
Assistant: Let me verify PR #42 is merged...
[Checks PR status]
PR #42 is merged. Proceeding with cleanup...
[Performs cleanup]
Branch cleanup complete!
```

### With Related Issues
```
User: /finish-branch feature/add-auth
Assistant: Found PR #55 for branch feature/add-auth.
PR is merged (merged 2 hours ago).
Found related issues: #50 (Closes), #51 (Fixes)

Proceeding with cleanup...
- Removed worktree: ../worktree-add-auth
- Deleted branch: feature/add-auth
- Closed issue #50
- Closed issue #51

All done!
```

## Integration with Research Executor

The **research-executor** agent MUST use this skill for cleanup. The workflow is:

1. Research executor creates worktree using **/using-git-worktrees** skill
2. Experiment is implemented with TDD methodology
3. PR is created and submitted for review
4. **ONLY AFTER PR is merged**, invoke `/finish-branch` for cleanup

The research-executor will prompt:
```
Experiment complete and PR merged!
Would you like me to clean up the worktree and branch?
```

Upon confirmation, invoke `/finish-branch` with the experiment branch name.

**Critical Rules:**
- NEVER delete worktrees before PR is merged
- NEVER delete worktrees manually - always use this skill
- This is the ONLY approved cleanup method for experiment branches

This ensures experimental worktrees don't accumulate and the repository stays clean.

## Related Skills and Agents

- **/using-git-worktrees** - Creates the worktree (this skill cleans it up)
- **research-executor** agent - The primary user of this skill for experiment cleanup
- **/google-docs-formatter** - Used by research-executor for documentation
