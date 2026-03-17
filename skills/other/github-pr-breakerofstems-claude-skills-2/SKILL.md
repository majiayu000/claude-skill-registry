---
name: github-pr
description: Create and manage pull requests
---

# GitHub Pull Request Skill

Create pull requests with proper descriptions and link to issues.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Create well-documented pull requests that are easy to review.

## Commands

```bash
gh pr create
gh pr create --title "<title>" --body "<body>"
gh pr create --draft
gh pr view <number>
gh pr list
gh pr checks <number>
```

## PR Title Format

Include issue number in title:
```
[#123] Fix login validation bug
[#456] Add user authentication
```

## PR Body Template

```markdown
## Summary

<!-- Brief description of the changes -->

## Related Issue

Closes #<issue-number>

## Changes Made

- Change 1
- Change 2

## Testing

- [ ] Unit tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project conventions
- [ ] Self-review completed
```

## Workflow

1. **Verify branch is ready**
   ```bash
   git status
   git log origin/main..HEAD --oneline
   ```

2. **Push latest changes**
   ```bash
   git push
   ```

3. **Create PR**
   ```bash
   gh pr create --title "[#123] Fix login bug" --body "## Summary
   Fixes validation issue in login form.

   Closes #123"
   ```

4. **Verify PR created**
   ```bash
   gh pr view
   ```

## Policies

- PR title must include issue number
- PR body must reference the issue with "Closes #X" or "Fixes #X"
- Ensure all commits are pushed before creating PR
- Use draft PRs for work-in-progress
- Never push directly to main/master
