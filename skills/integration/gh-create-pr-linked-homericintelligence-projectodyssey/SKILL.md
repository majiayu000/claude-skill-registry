---
name: gh-create-pr-linked
description: "Create a pull request properly linked to a GitHub issue using gh pr create --issue. Use when creating a PR that implements or addresses a specific issue."
category: github
agent: implementation-engineer
---

# Create PR Linked to Issue

Create a pull request with automatic issue linking.

## When to Use

- After completing implementation work
- Ready to submit changes for review
- Need to link PR to GitHub issue
- Starting from a feature branch

## Quick Reference

```bash
# Create PR linked to issue (preferred)
gh pr create --issue <issue-number>

# With custom title and body
gh pr create --title "Title" --body "Closes #<issue-number>"

# Verify link appears
gh issue view <issue-number>  # Check Development section
```

## Workflow

1. **Verify changes committed**: `git status` shows clean
2. **Push branch**: `git push -u origin branch-name`
3. **Create PR**: `gh pr create --issue <number>`
4. **Verify link**: Check issue's Development section on GitHub
5. **Monitor CI**: Watch checks with `gh pr checks`

## PR Requirements

- ✅ PR must be linked to GitHub issue
- ✅ All changes committed and pushed
- ✅ Branch has upstream tracking
- ✅ Clear, descriptive title
- ✅ Summary in description
- ❌ Do NOT create PR without issue link

## Error Handling

| Problem | Solution |
|---------|----------|
| No upstream branch | `git push -u origin branch-name` |
| Issue not found | Verify issue number exists |
| Auth failure | Run `gh auth status` |
| Link not appearing | Add "Closes #ISSUE-NUMBER" to body |

## Verification

After creating PR:

```bash
# View PR details
gh pr view <pr-number>

# Check CI status
gh pr checks <pr-number>

# Verify issue link
gh issue view <issue-number>  # Look for "Development" section
```

## Branch Naming Convention

Format: `<issue-number>-<description>`

Examples:

- `42-add-tensor-ops`
- `73-fix-memory-leak`
- `105-update-docs`

## References

- See CLAUDE.md for complete git workflow
- See CLAUDE.md for PR submission requirements
