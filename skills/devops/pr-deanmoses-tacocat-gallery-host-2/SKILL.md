---
name: pr
description: Creates pull requests with proper formatting. Use when creating PRs, opening pull requests, or preparing changes for review.
---

# Pull Requests

## PR Title

Use the [Conventional Commit Format](https://www.conventionalcommits.org/), same as commit messages:

```text
<type>(<scope>): <description>
```

## Types

- `feat`: User-facing features or behavior changes (must change production code)
- `fix`: Bug fixes (must change production code)
- `docs`: Documentation only
- `style`: Code style/formatting (no logic changes)
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `chore`: CI/CD, tooling, dependency bumps, configs (no production code)

## PR Description Template

```markdown
## Summary
One sentence describing the overall change.

- Optional supporting details
- If needed

## Test plan
- [ ] How to verify it works
```

## Labels

Apply labels using `gh pr create --label <label>` or `gh pr edit --add-label <label>`:

- `enhancement` - User-facing features or improvements (must change production code behavior)
- `refactor` - Production code changes that don't alter behavior
- `bug` - Fixes broken production code functionality
- `test` - Changes to tests
- `documentation` - Documentation changes

**No label needed** for dependency bumps, CI/CD, tooling, or infrastructure changes.

## Branch Naming

Use `type/short-description`:

```text
feat/cache-policy
fix/robots-txt-503
chore/pre-commit-hooks
```

## Instructions

1. Run `git log main..HEAD` to see commits for this branch
2. Run `git diff main...HEAD` to see all changes
3. Summarize the changes in 1-2 sentences
4. Create a test plan with verification steps
5. Apply appropriate labels
