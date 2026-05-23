---
name: gh-get-review-comments
description: "Retrieve all review comments from a pull request using the GitHub API. Use when you need to see what feedback has been provided on a PR."
category: github
agent: test-engineer
user-invocable: false
---

# Get PR Review Comments

Retrieve and analyze all review comments from a pull request.

## When to Use

- Checking for unresolved review feedback
- Analyzing reviewer feedback before fixing
- Verifying all comments have been addressed
- Getting comment IDs for replies

## Quick Reference

```bash
# Get all review comments
gh api repos/OWNER/REPO/pulls/PR/comments

# Get comments with formatting
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | {id: .id, path: .path, body: .body}'

# Filter by reviewer
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.user.login == "username")'

# Get only unresolved comments
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.in_reply_to_id == null)'
```

## Workflow

1. **Fetch comments**: Use API to list all comments
2. **Parse output**: Extract IDs and feedback
3. **Analyze feedback**: Understand what needs fixing
4. **Plan fixes**: Decide how to address each comment
5. **Apply fixes**: Make the requested changes

## Output Format

Comments include:

- `id` - Comment ID (use for replies)
- `path` - File where comment was made
- `line` - Line number of comment
- `body` - Comment text
- `user` - Reviewer username
- `in_reply_to_id` - Parent comment ID (null if top-level)

## Error Handling

| Problem | Solution |
|---------|----------|
| PR not found | Verify PR number |
| Auth failure | Check `gh auth status` |
| No comments | API returns empty array (not an error) |
| Permission denied | Check authentication scopes |

## Filtering Examples

**Comments on specific file**:

```bash
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.path == "src/file.mojo")'
```

**Comments by specific reviewer**:

```bash
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.user.login == "reviewer")'
```

**Only top-level comments** (not replies):

```bash
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.in_reply_to_id == null)'
```

## References

- See gh-reply-review-comment skill for replying to comments
- See gh-fix-pr-feedback skill for workflow to address feedback
- GitHub API docs: <https://docs.github.com/en/rest/pulls/comments>
