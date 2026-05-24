---
name: fix-pr-comments
description: This skill should be used when the user asks to "fix PR comments", "address PR feedback", "resolve PR threads", mentions "PR review", or discusses GitHub pull request comments.
version: 1.0.0
---

# Fix PR Comments

Handle PR review comments by choosing the appropriate response for each comment.

## Response Types

For each PR comment, choose one of these responses:

1. **Address and resolve**: Fix the issue, push the changes, and resolve the thread
2. **Explain**: If the comment doesn't make sense, leave a comment explaining why. Only resolve the thread if the comment is from a bot user.
3. **Ask for clarification**: If unclear, leave a question asking for clarification

## Comment Prefix

When leaving comments on PRs, always prefix with "Claude Code: " to make it clear the comment came from Claude.

## Comment Guidelines

**Never leave top-level comments on the PR** (via `gh pr comment` or the issues comments API). Only reply directly within review comment threads using the replies API. Top-level comments like "Addressed all feedback" are not helpful and clutter the PR.

## Workflow

1. Read all PR comments to understand the feedback
2. For each comment, determine the appropriate response type
3. Make code changes where needed
4. Push all changes
5. Resolve threads that have been addressed
6. Request re-review from reviewers whose comments have all been addressed
7. Leave explanatory comments or clarification questions as needed

## Re-requesting Review

Only request re-review from reviewers who have **not** already approved the PR. If a reviewer has approved, their approval still stands even after addressing their comments.

To check review states before requesting re-review:
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --jq '.[] | "\(.user.login): \(.state)"' | sort -u
```

To request re-review (only for reviewers with CHANGES_REQUESTED or COMMENTED state, not APPROVED):
```bash
gh pr edit --add-reviewer <reviewer-username>
```
