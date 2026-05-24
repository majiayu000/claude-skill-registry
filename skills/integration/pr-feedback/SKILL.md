---
name: pr-feedback
description: Review and address PR feedback. Use when asked to "check PR comments", "review PR feedback", "address PR comments", or respond to code review.
---

# PR Feedback

Review and respond to pull request comments.

## Process

1. **Get PR context**
   ```bash
   gh pr view --json number,title,url --jq '"PR #\(.number): \(.title)\n\(.url)"'
   ```

2. **Fetch comments**
   ```bash
   gh pr view --comments
   ```
   For full thread details:
   ```bash
   gh api repos/{owner}/{repo}/pulls/{number}/comments --paginate
   ```

3. **Review each comment** — understand the feedback before responding

4. **Address in code** — make the fix, cite file:line in your response

5. **Reply to thread** — summarize fix + reference commit/line

6. **Resolve threads** — only after fix lands and is pushed

## Guidelines

- Read all comments before starting fixes — some may conflict or overlap
- Don't resolve threads until the fix is committed and pushed
- Cite specific file:line when replying (e.g., "Fixed in `src/foo.ts:42`")
- If feedback is unclear, ask for clarification rather than guessing
- Group related fixes into logical commits
