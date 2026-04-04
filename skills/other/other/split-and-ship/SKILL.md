---
name: split-and-ship
description: "Execute an approved split plan by creating separate branches, commits, and PRs for each change group. Use when the user asks to \"split and ship\", \"ship the split plan\", \"create separate PRs\", or \"split changes into branches\"."
---

# Split and Ship

Ship an approved split plan as separate branches, commits, and PRs.

## Context

A split plan must exist in the conversation. The plan specifies an ordered list of groups, each with a name, file list, and branch topology (stacked or independent).

## Step 1: Prepare Working Tree

1. Detect the default branch: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
2. Check the current branch and whether a PR already exists for it using `gh pr view`
3. Save all staged changes, then unstage everything (`git reset`)
4. Stash all changes including untracked files (`git stash --include-untracked`) so files can be selectively restored per group

Verify `git stash list` shows the saved changes before proceeding.

## Step 2: Ship Each Group

Use `TaskCreate` to create a task for each group. Process groups in order.

For each group:

1. **Determine branch**: If the current branch already has a PR and this group's changes align with the PR's purpose, stay on the current branch. Otherwise, use `AskUserQuestion` to confirm the proposed branch name and create it from the appropriate base:
   - Independent group: branch from the default branch
   - Stacked group: branch from the previous group's branch
2. **Restore and stage** this group's files from the stash (`git checkout stash -- <files>` restores and stages in one operation). For files with hunks belonging to different groups, restore the file, then use Edit to remove the hunks that belong to later groups before staging. After committing, reset the working tree (`git checkout -- .`) to clean up before the next group.
3. **Run `/commit-staged-push` Skill**
4. **Create or update PR**:
   - Staying on existing branch with a PR: run the `/update-pr` skill
   - New branch: run the `/create-pr` skill targeting the appropriate base (default branch for independent groups, previous group's branch for stacked groups)

## Step 3: Clean Up and Summarize

1. Drop the stash
2. Check out the last created branch
3. Output a summary table: group name, branch, PR URL, and base branch

## Rules

- Never lose uncommitted work. If any step fails (commit hook, push, PR creation), stop and report the failure, which groups have been shipped, and that the stash still contains all changes for recovery.
- Stacked PRs target the previous group's branch. Independent PRs target the default branch.
- For stacked groups, the PR description should note the dependency chain.
