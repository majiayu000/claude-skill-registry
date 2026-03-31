---
name: review-pr
description: "Review a pull request by fetching PR comments and running a comprehensive code review with evaluation. Use when the user asks to \"review PR\", \"review pull request\", \"review this PR\", \"check PR before merging\", or \"full PR review\"."
---

# Review PR

Fetch PR context, run a comprehensive code review, and evaluate findings.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Run `/fetch-pr-comments` skill
2. Detect base branch
3. Run `/review-code` skill
4. Run `/evaluate-findings` skill

## Step 1: Run `/fetch-pr-comments` Skill

Run the `/fetch-pr-comments` skill to get unresolved review comments.

## Step 2: Detect Base Branch

Detect the PR's base branch via `gh pr view --json baseRefName --jq '.baseRefName'`.

## Step 3: Run `/review-code` Skill

Run the `/review-code` skill. The diff command is `git diff <base-branch>...HEAD`.

## Step 4: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the combined results from Step 3. Include any unresolved PR comments from Step 1 as additional findings for evaluation.

If zero actionable findings survive evaluation, report that the code looks clean and stop. Otherwise, present the evaluated findings to the user.

## Rules

- If fetching PR comments fails, proceed with code review only.
