---
name: create-pr
description: Create a pull request — collect diff, generate PR description with context, apply checklist, and push. Use when ready to submit code for review.
disable-model-invocation: true
---

# Create Pull Request

Structured workflow for creating a well-documented pull request. Collects changes, generates description, applies quality checklist.

## 1. Verify Branch State

```
// turbo
git branch --show-current
```

```
// turbo
git status --short
```

**Check:**
- Current branch is NOT `main` or `master` (never create PRs from default branch)
- Working directory is clean (all changes committed)
- Branch is up to date with remote

If uncommitted changes exist, suggest running `/pre-commit` first.

## 2. Collect Diff

```
// turbo
git log main..HEAD --oneline
```

```
// turbo
git diff main..HEAD --stat
```

Analyze the changes to understand:
- **What** changed (files, modules, functions)
- **Why** it changed (feature, bugfix, refactor, chore)
- **Scope** (how many files, which areas of the codebase)
- **Risk** (breaking changes, migration, infra changes)

## 3. Generate PR Description

Produce a structured PR description:

```markdown
## Summary

[1-2 sentence summary of what this PR does and why]

## Changes

- [Bullet list of key changes, grouped by area]
- [Focus on WHAT and WHY, not HOW]

## Type

- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Chore (deps, CI, docs)
- [ ] Breaking change

## Testing

- [How was this tested?]
- [Which test suites were run?]
- [Manual testing steps if applicable]

## Screenshots / Evidence

[If UI changes — before/after screenshots]
[If performance — benchmark results]

## Checklist

- [ ] Code follows project conventions
- [ ] Tests added/updated for new logic
- [ ] Documentation updated if needed
- [ ] No secrets or PII in code
- [ ] Breaking changes documented
- [ ] Migration steps documented (if applicable)
```

## 4. Determine PR Title

Format: `<type>(<scope>): <description>`

**Types**: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `perf`, `ci`

Examples:
- `feat(auth): add OAuth2 login with Google`
- `fix(api): handle null response from payment gateway`
- `refactor(db): migrate from raw SQL to ORM queries`

## 5. Push and Create

Present the PR description to the user for review.

After approval:

```
git push -u origin <branch-name>
```

**⚠️ Do NOT run `git push` without user confirmation.**

Provide the link format for creating the PR in the browser:
```
https://github.com/<owner>/<repo>/compare/main...<branch-name>
```

Or if using GitHub CLI:
```
gh pr create --title "<title>" --body "<description>" --base main
```

## 6. Post-Create

Suggest next steps:
- Share PR link with reviewers
- Add labels (feature, bugfix, priority)
- Link to related issues
- Request specific reviewers based on changed files
- Run `/code-review` for self-review before requesting others

## Integration

- **Preceded by**: `/pre-commit` (quality gate passed)
- **Followed by**: `/code-review`
