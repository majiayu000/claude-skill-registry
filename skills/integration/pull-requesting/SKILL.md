---
name: 'pull-requesting'
description: 'Creates well-structured pull requests with clear descriptions. Use when creating PRs, preparing changes for review, or when asked to open a pull request.'
---

# Pull Requesting

## PR Structure

```markdown
## Summary

Brief description of what this PR does (1-3 sentences).

## Changes

- Bullet point of each significant change
- Group related changes together
- Link to relevant issues: Fixes #123

## Test Plan

- [ ] How to verify this works
- [ ] Edge cases tested
- [ ] Manual testing steps if applicable

## Screenshots

(If UI changes, before/after screenshots)
```

## Workflow

1. **Check branch status**

   ```bash
   git status
   git log main..HEAD --oneline
   git diff main...HEAD --stat
   ```

2. **Review all commits** (not just the latest)

   ```bash
   git log main..HEAD
   ```

3. **Create PR**

   ```bash
   gh pr create --title "type(scope): description" --body "$(cat <<'EOF'
   ## Summary
   Brief description.

   ## Changes
   - Change 1
   - Change 2

   ## Test Plan
   - [ ] Test step 1
   - [ ] Test step 2
   EOF
   )"
   ```

## Best Practices

### Size

- **Small PRs**: Easier to review, faster to merge
- **Single concern**: One feature or fix per PR
- **< 400 lines**: Ideal for thorough review

### Title

- Use conventional commit format: `type(scope): description`
- Be specific: "fix(auth): handle expired tokens" not "fix bug"

### Description

- Explain **why**, not just **what**
- Link related issues
- Include testing instructions
- Add screenshots for UI changes

### Before Submitting

- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Self-reviewed the diff
- [ ] Documentation updated if needed
- [ ] No secrets or credentials included
