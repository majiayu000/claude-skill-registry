---
name: git-workflow
description: Follow git conventions for commits, branches, and PRs.
  Auto-activated during git operations.
---

# Git Workflow Skill

## Purpose
Ensure consistent git practices across all phases.

## Commit Message Convention
Reference: [conventions/commit-messages.md](conventions/commit-messages.md)

### Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types
| Type | Use For |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| refactor | Code restructuring |
| docs | Documentation |
| test | Test changes |
| chore | Maintenance |
| perf | Performance improvement |
| style | Formatting, no code change |
| ci | CI/CD changes |

### Examples
```
feat(auth): implement JWT token refresh

- Add refresh token endpoint
- Update token validation logic
- Add integration tests

Closes #123
```

## Branch Naming
Reference: [conventions/branch-naming.md](conventions/branch-naming.md)

Format: `<type>/<ticket>-<description>`

Examples:
- `feat/AUTH-123-jwt-refresh`
- `fix/BUG-456-login-error`
- `refactor/TECH-789-user-service`

## PR Template
Reference: [conventions/pr-template.md](conventions/pr-template.md)

## Workflow Best Practices

### Commit Frequency
- Commit after each logical unit of work
- Each commit should be independently buildable
- Don't commit broken code

### Branch Strategy
- Create feature branch from main/develop
- Keep branches short-lived
- Rebase before merge when appropriate

### PR Guidelines
- Keep PRs focused and reviewable
- Include context in description
- Link to related issues
- Request appropriate reviewers

## Quality Checklist
Before committing:
- [ ] Code compiles/builds
- [ ] Tests pass
- [ ] Lint passes
- [ ] Commit message follows convention
- [ ] No sensitive data included

Before creating PR:
- [ ] Branch is up to date
- [ ] All commits are meaningful
- [ ] PR description is complete
- [ ] Tests are included
- [ ] Documentation updated
