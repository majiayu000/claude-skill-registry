---
name: prc
description: >-
  Review and address code review comments on PR. Use when asked to
  'address review comments', 'fix PR feedback', 'handle review comments',
  'respond to PR comments', or 'address CR comments'.
  NOT for initiating code review (use /sr),
  NOT for task-based implementation with CR mode (use /si).
argument-hint: [pr-number]
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion, TodoWrite
---

# PR Review Comments Handler

## PRIMARY OBJECTIVE

Fetch, analyze, and address code review comments on the current PR. Present an action plan for user approval before implementing fixes, then commit and reply to reviewers.

## Related Skills

- `/sr` — Initiate a code review (before merge). Use that skill to start a review, this skill to address the results.
- `/si` — Task-based implementation with "Address CR" mode. Use `/si` when review feedback requires structured task-driven changes; use `/prc` for direct, ad-hoc PR comment handling.

---

## GATE 1: Identify PR & Fetch Comments

### Step 1: Resolve PR

If `$ARGUMENTS` contains a PR number, use it. Otherwise:

1. Run `git branch --show-current` to get the current branch
2. Run `gh pr view --json number,title,url` to find the open PR

**Error — no PR found:**
Inform user: "No open PR found for branch `{branch}`. Verify the branch is pushed and the PR is open." Stop execution.

### Step 2: Fetch Comments

1. Run `gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews` to get reviews
2. Run `gh api repos/{owner}/{repo}/pulls/{pr_number}/comments` to get inline comments
3. Also check `gh pr view {pr_number} --json comments` for general PR comments

**Error — no comments found:**
Inform user: "No review comments found on PR #{number}. Nothing to address." Stop execution.

---

## GATE 2: Analyze & Present Plan

### Step 1: Categorize Comments

For each review comment, evaluate:
- Is the feedback valid and technically correct?
- Is it applicable to the current code?
- Does it align with project conventions and architecture?
- Is it a blocker or a nice-to-have suggestion?

Classify each comment into one of:
- **Address** — Valid feedback, will fix
- **Skip** — Not applicable or already handled (provide reason)
- **Discuss** — Ambiguous or disagreed, needs user input

### Step 2: Present Action Plan

Display a table:

```
| # | File:Line | Comment Summary | Action | Complexity |
|---|-----------|-----------------|--------|------------|
| 1 | src/foo.ts:42 | Missing null check | Address | Simple |
| 2 | src/bar.ts:15 | Rename variable | Address | Simple |
| 3 | src/baz.ts:88 | Architecture concern | Discuss | Significant |
```

**STOP** — Use AskUserQuestion to confirm the plan. Ask user to approve, modify, or flag any items they disagree with. Do not proceed until user approves.

---

## GATE 3: Implement & Verify

### Step 1: Apply Fixes

For each approved "Address" item:
1. Read the target file
2. Make the necessary code change using Edit
3. Track progress with TodoWrite

For "Discuss" items the user resolved: apply the agreed-upon fix.

### Step 2: Run Verification

1. Run project tests (`npm test` or equivalent)
2. Run lint checks (`npm run lint` or equivalent)
3. Run type checks if applicable (`tsc --noEmit`)

**Error — tests or lint fail:**
Present failures to user. Do not proceed to GATE 4. Work with user to resolve, or revert changes if needed.

---

## GATE 4: Commit, Push & Reply

### Step 1: Commit & Push

1. Stage changed files with `git add` (specific files only)
2. **Ask user permission** before committing
3. Create a focused commit: `fix: address PR review feedback`
4. Push to update the PR

### Step 2: Reply to Comments

For each addressed comment:
- Reply with a brief description of what was done (1-2 sentences)
- Use `gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/replies -f body="..."` to reply

For skipped comments:
- Reply explaining why respectfully

**Error — gh API reply fails:**
Report the error and suggest manual reply via GitHub UI.

---

## Output Format

Provide a final summary:

```
## PR Review Summary

**PR**: #XX - Title
**Reviewer(s)**: @username

### Comments Addressed:
1. [file:line] - Brief description of fix
2. [file:line] - Brief description of fix

### Comments Skipped (if any):
1. [file:line] - Reason why not applicable

### Changes Made:
- List of files modified
- New commit: {hash}
```
