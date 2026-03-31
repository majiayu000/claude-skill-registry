---
name: generate-pr-description
description: Generate PR title and description
argument-hint: [parent-branch]
---

# Generate PR Description

Analyze the git diff between the parent branch and the current branch and create a pull request title and description.

**Parent branch:** Use "$1" if provided, otherwise default to "main"

## Instructions

1. Use `git diff <parent-branch>...HEAD` and `git log <parent-branch>..HEAD` to analyze changes
2. Generate a concise, descriptive PR title
3. Write a description summarizing what changed and why

### Guidelines

- Title should clearly describe what the PR accomplishes
- Description should provide context for reviewers
- List the key changes made
- Mention any breaking changes, migrations, or deployment considerations
- Be concise and direct

## Output Format

Print the title and description in code blocks so they can be easily copied:

---

**PR title:**

```
Add user notification preferences
```

**PR description:**

```
## Summary

Users can now configure how and when they receive notifications.

## Changes

- Added notification preferences model and API endpoints
- Created settings UI for managing preferences
- Implemented email digest options (immediate, daily, weekly)

## Notes

- Requires database migration
```

---
