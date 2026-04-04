---
name: create-issues
allowed-tools: Task, Bash(gh:*), Bash(git:*)
description: Create GitHub issues with TDD principles and proper labels
argument-hint: [description]
user-invocable: true
---

## Context

- Current git status: !`git status`
- Current branch: !`git branch --show-current`
- Open issues: !`gh issue list --state open --limit 10`
- GitHub authentication: !`gh auth status`

## Requirements

- Follow TDD principles and Conventional Commits.
- Use proper labels, scope, and auto-closing keywords.
- Protected branches require PR + review + CI; no direct pushes to main/develop.
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

1. Assess the repository context and select an issue scope that fits `$ARGUMENTS`.
2. Create or update labels as needed, then draft the issue with the required structure and links.
3. Document decisions (including branch strategy) and share follow-up actions with the team.

### Decision Logic

**Branch-based decision tree**:

- **On main/develop**: Create issue directly.
- **On PR branch**: Ask "Must this be fixed before merge?"
  - **Yes**: Comment in PR with detailed context and reasoning, don't create issue.
  - **No**: Create new issue for later with clear justification for scope separation.

### Issue Types

1. **Epic issues**: Multi-PR initiatives (no auto-close keywords).
2. **PR-scoped issues**: Single PR resolution (use auto-close keywords).
3. **Review issues**: Non-blocking feedback from PR reviews.

### Issue Creation Process

1. **Analyze context** from current repository state and existing issues.
2. **Determine issue type** based on scope and complexity.
3. **Create proper labels** if they don't exist:
   ```bash
   gh label create "priority:high" --description "High priority - this sprint" --color "d73a4a" || true
   gh label create "priority:medium" --description "Medium priority - next sprint" --color "fbca04" || true
   gh label create "priority:low" --description "Low priority - backlog" --color "0075ca" || true
   ```
4. **Create issue** with proper structure and labels.
5. **Link related items** if applicable.

### Issue Structure Requirements

- **Title**: ≤70 chars, imperative, no emojis.
- **Labels**: Include priority and type labels.
- **Body**: Problem description, acceptance criteria, context.
- **Auto-closing**: Use keywords (`fixes`, `closes`, `resolves`) for PR-scoped issues.

### Key Principles

- Follow TDD: issue → test → code → PR → merge.
- Epic issues: manual linking, no auto-close keywords.
- PR-scoped issues: designed for auto-close keywords.
- Clear, actionable descriptions with proper context.
