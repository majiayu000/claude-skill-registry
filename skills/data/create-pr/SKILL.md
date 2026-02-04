---
name: create-pr
allowed-tools: Task, Bash(gh:*), Bash(git:*)
description: Create comprehensive GitHub pull requests with quality validation
argument-hint: [optional description or issue reference]
user-invocable: true
---

## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Unpushed commits: !`git log @{u}..HEAD --oneline 2>/dev/null || git log --oneline -5`
- GitHub authentication: !`gh auth status`
- Repository changes: !`git diff --stat HEAD~1..HEAD 2>/dev/null || echo "No recent changes"`

## Requirements

- Ensure the repository is clean, authenticated, and ready for PR submission.
- Complete lint, test, build, and security checks before creating the PR.
- Link related issues and apply accurate labels for traceability.
- **Use atomic commits for logical units of work**: Each commit should represent one complete, cohesive change.
- Title: entirely lowercase, <50 chars, imperative mood (e.g., "add", "fix", "update"), conventional commits format (feat:, fix:, docs:, refactor:, test:, chore:)
  - Scope (optional): lowercase noun, 1-2 words. Must match existing scopes in git history.
- Body: blank line after title, ≤72 chars per line, must start with uppercase letter, standard capitalization and punctuation. Describe what changed and why, not how.
- Footer (optional): Must start with uppercase letter, standard capitalization. Reference issues/PRs (Closes #123, Fixes #456, Linked to PR #789). Use BREAKING CHANGE: prefix for breaking changes.

### Examples

```
feat(auth): add google oauth login flow

- Introduce Google OAuth 2.0 for user sign-in
- Add backend callback endpoint `/auth/google/callback`
- Update login UI with Google button and loading state

Add a new authentication option improving cross-platform
sign-in.

Closes #42. Linked to #38 and PR #45
```

```
fix(api): handle null payload in session refresh

- Validate payload before accessing `user.id`
- Return proper 400 response instead of 500
- Add regression test for null input

Prevents session refresh crash when token expires.

Fixes #105
```

```
feat(auth): migrate to oauth 2.0

- Replace basic auth with OAuth 2.0 flow
- Update authentication middleware
- Add token refresh endpoint

BREAKING CHANGE: Authentication API now requires OAuth 2.0 tokens. Basic auth is no longer supported.

Closes #120. Linked to #115 and PR #122
```

## Your Task

**IMPORTANT: You MUST use the Task tool to complete ALL tasks.**

1. Validate repository readiness, analyse change scope, and detect any blockers.
2. Run the necessary quality and security checks; resolve failures by collaborating with specialized agents when required.
3. Assemble the pull request with the prescribed structure, link issues, apply labels, and report the final status to the team.

### Workflow Steps

1. **Repository Validation** - Check authentication and branch status
2. **Change Analysis** - Analyze commits and file changes
3. **Quality Validation** - Run project-specific quality checks
4. **Security Scanning** - Check for sensitive data exposure
5. **Issue Discovery** - Find and link related issues
6. **PR Creation** - Generate and create pull request with proper metadata

### Quality Validation Process

**Node.js Projects:**

- Run lint, test, build, and type-check commands
- Validate package.json changes
- Check for security vulnerabilities

**Python Projects:**

- Run ruff, black, pytest, and mypy
- Validate requirements and dependencies
- Check for security issues

### Security Validation

- Scan for sensitive files (.env, .key, .pem)
- Check for hardcoded secrets, passwords, tokens
- Validate input sanitization in changed files
- Ensure no credentials in commit history

### Pre-Creation Requirements

- Repository state validated and clean
- All quality checks passed (lint, test, build)
- Security scan completed without issues
- Related issues identified and linked
- Proper branch naming and commit messages following standards

### Failure Resolution Process

When quality checks fail:

1. Use TodoWrite to create specific task list for failures
2. Use Task tool with specialized agents:
   - **@code-reviewer** — logic correctness, tests, error handling.
   - **@security-reviewer** — authentication, data protection, validation.
3. Fix issues systematically with validation after each fix
4. Mark tasks completed immediately after resolution
5. Re-run quality checks until all pass

### PR Structure Requirements

**Title Guidelines:**

- Maximum 70 characters
- Use imperative mood
- No emojis
- Clear and descriptive

**Body Template:**

```markdown
## Summary
Brief description of changes and business impact

## Changes
- List of key modifications
- Technical details and rationale

## Related Issues
Fixes #123, Closes #456

## Testing
- [ ] Unit tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] Edge cases covered

## Security & Quality
- [ ] No sensitive data exposed
- [ ] Input validation implemented
- [ ] Linting and type checking passed
- [ ] Build successful

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
```

### Automated Labeling

- `testing` - Test file modifications
- `documentation` - Documentation updates
- `dependencies` - Package file changes
- `security` - Security-related modifications

### Commit Message Validation

- **Use atomic commits for logical units of work**: Each commit should represent one complete, cohesive change.
- Title: entirely lowercase, <50 chars, imperative mood (e.g., "add", "fix", "update"), conventional commits format (feat:, fix:, docs:, refactor:, test:, chore:)
  - Scope (optional): lowercase noun, 1-2 words. Must match existing scopes in git history.
- Body: blank line after title, ≤72 chars per line, must start with uppercase letter, standard capitalization and punctuation. Describe what changed and why, not how.
- Footer (optional): Must start with uppercase letter, standard capitalization. Reference issues/PRs (Closes #123, Fixes #456, Linked to PR #789). Use BREAKING CHANGE: prefix for breaking changes.

### Examples

```
feat(auth): add google oauth login flow

- Introduce Google OAuth 2.0 for user sign-in
- Add backend callback endpoint `/auth/google/callback`
- Update login UI with Google button and loading state

Add a new authentication option improving cross-platform
sign-in.

Closes #42. Linked to #38 and PR #45
```

```
fix(api): handle null payload in session refresh

- Validate payload before accessing `user.id`
- Return proper 400 response instead of 500
- Add regression test for null input

Prevents session refresh crash when token expires.

Fixes #105
```

```
feat(auth): migrate to oauth 2.0

- Replace basic auth with OAuth 2.0 flow
- Update authentication middleware
- Add token refresh endpoint

BREAKING CHANGE: Authentication API now requires OAuth 2.0 tokens. Basic auth is no longer supported.

Closes #120. Linked to #115 and PR #122
```

- Review all commits in branch for compliance
- Handle non-standard commits by documenting in PR description or interactive rebase if safe

### Best Practices

- **Quality-first**: All checks must pass before PR creation
- **Security validation**: Comprehensive scanning for vulnerabilities
- **Issue linking**: Connect PRs to related issues with auto-closing keywords
- **Small, focused changes**: Easier to review and merge
