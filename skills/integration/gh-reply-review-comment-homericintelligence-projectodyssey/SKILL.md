---
name: gh-reply-review-comment
description: "Reply to PR review comments using the correct GitHub API endpoint. Use when responding to inline code review feedback (not gh pr comment)."
category: github
agent: test-engineer
user-invocable: false
---

# Reply to Review Comments

Reply to PR review comments using the correct GitHub API.

## When to Use

- Responding to inline code review feedback
- Addressing specific review comments
- Confirming fixes have been implemented
- Updating reviewers on progress

## Critical: Two Types of Comments

**DO NOT confuse these**:

1. **PR-level comments** (general timeline): `gh pr comment`
2. **Review comment replies** (inline code): GitHub API (see below)

## Quick Reference

```bash
# 1. Get comment ID
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | {id: .id, path: .path, body: .body}'

# 2. Reply to comment
gh api repos/OWNER/REPO/pulls/PR/comments/COMMENT_ID/replies \
  --method POST -f body="✅ Fixed - brief description"

# 3. Verify reply posted
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.in_reply_to_id)'
```

## Workflow

1. **Get comment IDs**: List all review comments
2. **Apply fixes**: Make the requested changes
3. **Reply to EACH comment**: Respond individually to each
4. **Verify replies**: Check they all posted successfully
5. **Monitor CI**: Ensure changes pass CI

## Reply Format

Keep responses SHORT and CONCISE (1 line preferred):

**Good examples**:

- `✅ Fixed - Updated conftest.py to use real repository root`
- `✅ Fixed - Deleted test file as requested`
- `✅ Fixed - Removed markdown linting section`

**Bad examples**:

- Long explanations
- Defensive responses
- Multiple paragraphs

## Error Handling

| Problem | Solution |
|---------|----------|
| Comment ID invalid | Verify using API call |
| Permission denied | Check `gh auth status` |
| Reply fails | Verify PR and comment exist |
| Comment not found | Double-check ID format |

## Verification

After replying:

```bash
# Check replies appeared
gh api repos/OWNER/REPO/pulls/PR/comments \
  --jq '.[] | select(.in_reply_to_id) | {id: .id, body: .body}'

# Verify CI status
gh pr checks PR
```

## References

- See CLAUDE.md for complete PR workflow
- See `/agents/guides/github-review-comments.md` for detailed guide
