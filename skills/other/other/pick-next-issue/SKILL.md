---
name: pick-next-issue
description: "Fetch and rank open GitHub issues by community engagement, present the top 3 candidates, and plan implementation for the selected issue. Use when the user asks to \"pick next issue\", \"next issue\", \"which issue should I work on\", \"top issues\", \"most popular issues\", \"prioritize issues\", or \"what should I work on next\"."
---

# Pick Next Issue

Rank open GitHub issues by engagement and plan the selected issue.

## Step 1: Run `/plan-style` Skill

Run the `/plan-style` skill to load planning conventions.

## Step 2: Fetch and Rank Issues

Run `gh issue list` to fetch open issues with engagement data:

```bash
gh issue list --state open --json number,title,url,reactionGroups,comments,labels,createdAt --limit 50
```

Calculate an engagement score for each issue:

- **Reactions score**: Sum all reaction counts from `reactionGroups` (thumbs up, heart, hooray, etc.). Weight thumbs-up (`THUMBS_UP`) reactions 2x since they signal explicit demand.
- **Comments score**: Count of comments on the issue.
- **Engagement score**: `(weighted reactions) + comments`

Sort issues by engagement score descending.

## Step 3: Present Top 3

Present the top 3 issues in a numbered list. For each issue, show:

1. **Title** with issue number and link
2. **Labels** (if any)
3. **Engagement**: reaction breakdown and comment count
4. **Created**: date
5. **First paragraph** of the issue body (truncate if long)

If fewer than 3 open issues exist, present all of them.

If no open issues exist, inform the user and stop.

## Step 4: User Picks an Issue

Ask the user to pick one of the presented issues (or request to see more).

If the user asks to **see more**, present the next 3 issues from the ranked list.

## Step 5: Read the Full Issue

Fetch the complete issue details for the selected issue:

```bash
gh issue view <number> --json number,title,body,url,labels,comments,reactionGroups,assignees,milestone
```

Read the full issue body and comments to understand the requirements and any discussion context.

## Step 6: Plan

Using the issue as the requirements, explore the codebase, design the implementation, and write a detailed plan (exact file paths, function signatures, data flow, test cases).

The plan's final step must instruct: "Close issue #N or reference it in the PR with `Closes #N`."

## Rules

- Requires `gh` CLI authenticated with access to the current repo
- If `gh` fails (not in a repo, not authenticated), inform the user and stop
- Never modify issues. This skill is read-only until the implementation is committed.
