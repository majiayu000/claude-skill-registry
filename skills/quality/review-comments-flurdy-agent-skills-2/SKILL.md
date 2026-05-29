---
name: review-comments
description: Address PR review comments from reviewers (amazon-q-developer, copilot, humans). Use when the user wants to see and respond to feedback on their pull request.
---

# Address Review Comments

Fetch and address review comments on the current PR.

## Usage

```
/review-comments
/review-comments 123    # Specific PR number
```

## Instructions

### 1. Find the PR

If no PR number provided, get it from the current branch:

```bash
gh pr view --json number,url,title --jq '{number, url, title}'
```

### 2. Fetch Review Comments

Get all review comments on the PR:

```bash
# Get PR reviews and comments
gh pr view {pr_number} --json reviews,comments

# Get inline code review comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

### 3. Categorize Comments

Group comments by:
- **Reviewer**: amazon-q-developer[bot], copilot[bot], human reviewers
- **Status**: Pending, Resolved, Outdated
- **Type**: Code suggestion, question, blocking issue

### 4. Present Summary

Show a summary of comments:

```
PR #123: feat(offers-cms): add caching

Reviews:
- amazon-q-developer: 3 comments (2 suggestions, 1 security concern)
- copilot: 1 comment (style suggestion)
- @username: 2 comments (1 question, 1 blocking)

Unresolved comments: 6
```

### 5. Address Comments

For each unresolved comment:

1. Read the comment and understand what's being asked
2. Check the file and line being referenced
3. Either:
   - Make the suggested change if appropriate, including an initially failing test if needed
   - Explain why the current code is correct
   - Ask the user for guidance on ambiguous feedback

### 6. After Making Changes

```bash
# Stage and commit fixes
git add {files_changed}
git commit -m "address review feedback"

# Push updates
git push
```

### 7. Respond to Comments (Optional)

If the user wants to reply to comments:

```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments/{comment_id}/replies \
  -f body="Done - fixed in latest commit"
```
