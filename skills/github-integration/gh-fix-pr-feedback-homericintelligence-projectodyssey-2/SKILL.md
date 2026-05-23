---
name: gh-fix-pr-feedback
description: "Address PR review feedback by making changes and replying to comments. Use when a PR has open review comments needing responses."
category: github
agent: implementation-engineer
---

# Fix PR Review Feedback

Address PR review comments by implementing fixes and responding to each comment.

## When to Use

- PR has open review comments requiring responses
- Ready to implement reviewer's requested changes
- Need to notify reviewers of fixes
- PR is blocked on feedback

## Quick Reference

```bash
# 1. Get all review comments
gh api repos/OWNER/REPO/pulls/PR/comments --jq '.[] | {id: .id, path: .path, body: .body}'

# 2. Make fixes to code
# [edit files, test, format]

# 3. Commit changes
git add . && git commit -m "fix: address PR review feedback"

# 4. Reply to EACH comment
gh api repos/OWNER/REPO/pulls/PR/comments/COMMENT_ID/replies \
  --method POST -f body="✅ Fixed - [brief description]"

# 5. Push and verify
git push
gh pr checks PR
```

## Workflow

1. **Fetch review comments**: List all comments requiring response
2. **Analyze feedback**: Understand all requested changes
3. **Make changes**: Edit code to address each comment
4. **Run tests**: Verify fixes pass locally
5. **Commit changes**: Create single focused commit
6. **Reply to comments**: Reply to EACH comment individually (critical!)
7. **Push and verify**: Push changes and check CI status

## Reply Format

Keep responses SHORT and CONCISE (1 line preferred):

- `✅ Fixed - Updated conftest.py to use real repository root`
- `✅ Fixed - Removed duplicate test file`
- `✅ Fixed - Added error handling for edge case`

## Critical: Two Types of Comments

**PR-level comments** (general timeline):

```bash
gh pr comment <pr> --body "Response"
```

**Review comment replies** (inline code feedback):

```bash
gh api repos/OWNER/REPO/pulls/PR/comments/COMMENT_ID/replies \
  --method POST -f body="✅ Fixed - description"
```

NEVER confuse these - use the correct API for review comments.

## Error Handling

| Problem | Solution |
|---------|----------|
| Comment ID invalid | Verify ID using API |
| Auth failure | Run `gh auth status` |
| Reply not appearing | Check API endpoint syntax |
| CI fails after push | Review logs and fix issues |

## Verification

After addressing feedback:

- [ ] All review comments have replies
- [ ] Changes committed and pushed
- [ ] CI checks passing
- [ ] No new issues introduced

## References

- See CLAUDE.md for complete PR workflow
- See `/agents/guides/github-review-comments.md` for detailed guide
