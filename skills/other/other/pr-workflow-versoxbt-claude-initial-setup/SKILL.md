---
name: pr-workflow
description: >
  Guide pull request creation, review process, CI gates, and merge strategies.
  Use when the user creates a PR, asks about PR templates, review workflows,
  CODEOWNERS setup, or merge strategies. Apply when running gh pr create.
---

# Pull Request Workflow

Structure PRs for effective code review, automated CI validation, and clean merge history.

## When to Use

- Creating a pull request with `gh pr create` or GitHub UI
- Setting up PR templates for a repository
- Configuring CODEOWNERS for automatic review assignment
- Choosing between squash, merge, and rebase merge strategies
- Reviewing or improving an existing PR workflow

## Core Patterns

### PR Creation with gh CLI

Always analyze changes before creating a PR:

```bash
# 1. Check what will be in the PR
git log main..HEAD --oneline
git diff main...HEAD --stat

# 2. Push branch with upstream tracking
git push -u origin feature/AUTH-123-add-sso

# 3. Create PR with structured body
gh pr create --title "feat(auth): add SSO login via SAML" --body "$(cat <<'EOF'
## Summary
- Add SAML-based SSO authentication flow
- Integrate with identity provider discovery endpoint
- Store SSO sessions with configurable TTL

## Changes
- `src/auth/sso.ts` — SAML assertion parsing and validation
- `src/auth/routes.ts` — New `/auth/sso/callback` endpoint
- `src/config/sso.ts` — SSO provider configuration schema

## Test Plan
- [ ] Unit tests for SAML assertion parsing
- [ ] Integration test with mock IdP
- [ ] Manual test with Okta sandbox
- [ ] Verify session expiration behavior

Closes #142
EOF
)"
```

### PR Template

Create `.github/pull_request_template.md` in the repository:

```markdown
## Summary
<!-- 1-3 bullet points describing WHAT changed and WHY -->

## Changes
<!-- List key files changed and what was modified -->

## Test Plan
<!-- How to verify this works correctly -->
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing steps documented

## Screenshots
<!-- If UI changes, include before/after screenshots -->

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or noted in description)
- [ ] Self-reviewed the diff
```

### CODEOWNERS Setup

Create `.github/CODEOWNERS` to auto-assign reviewers:

```bash
# Default owners for everything
* @org/engineering-leads

# Frontend owned by frontend team
src/components/     @org/frontend
src/pages/          @org/frontend
src/styles/         @org/frontend

# API and backend
src/api/            @org/backend
src/services/       @org/backend
src/models/         @org/backend

# Infrastructure
Dockerfile          @org/devops
docker-compose.yml  @org/devops
.github/workflows/  @org/devops
terraform/          @org/devops

# Security-sensitive files require security review
src/auth/           @org/security @org/backend
src/crypto/         @org/security
```

### Merge Strategy Selection

```bash
# SQUASH MERGE: Default for feature PRs
# Produces one clean commit on main
gh pr merge 123 --squash

# MERGE COMMIT: For release branches or when history matters
# Preserves all individual commits
gh pr merge 123 --merge

# REBASE MERGE: For clean, linear history
# Replays commits on top of base branch
gh pr merge 123 --rebase
```

| Strategy | Best For | Result |
|----------|----------|--------|
| Squash   | Feature PRs, messy history | Single commit on main |
| Merge    | Release branches, audit trails | Merge commit + all commits |
| Rebase   | Clean PRs with good commits | Linear history, no merge commit |

### Draft PRs and Review Process

```bash
# Create draft PR for early feedback
gh pr create --draft --title "WIP: refactor auth module"

# Mark ready for review when done
gh pr ready 123

# Request specific reviewers
gh pr create --reviewer "alice,bob" --title "feat: add caching layer"

# Add reviewers to existing PR
gh pr edit 123 --add-reviewer "alice"

# Check CI status before merging
gh pr checks 123

# View review status
gh pr view 123
```

Review workflow stages:
1. **Draft PR** — Open early for visibility, not ready for review
2. **Ready for Review** — All CI passing, self-reviewed, description complete
3. **Changes Requested** — Address feedback, push new commits (do not force-push)
4. **Approved** — Merge when CI is green and approvals are met
5. **Merged** — Delete the source branch

### CI Gates Configuration

Example GitHub Actions workflow for PR validation:

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks
on:
  pull_request:
    branches: [main, develop]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
      - run: npm run build
```

Configure branch protection to require these checks before merging.

## Anti-Patterns

### What NOT to Do

- **Giant PRs**: PRs over 400 lines are hard to review and likely to hide bugs. Split into smaller, focused PRs.
- **No description**: A PR with just a title gives reviewers no context. Always include summary, changes, and test plan.
- **Force-pushing during review**: Reviewers lose context of what changed between review rounds. Push new commits instead.
- **Merging with failing CI**: Never override CI checks to merge faster. Fix the failures.
- **Self-approving**: Even solo developers benefit from CI gates. Do not bypass required reviews.

```bash
# BAD: No description
gh pr create --title "updates"

# BAD: Force push during review
git rebase -i HEAD~5
git push --force  # Reviewer comments now point to nonexistent commits

# GOOD: Push fixup commits during review
git commit -m "fix: address review feedback on input validation"
git push
```

## Quick Reference

```
PR Creation Checklist:
  1. git log main..HEAD — review all commits
  2. git diff main...HEAD --stat — verify changed files
  3. git push -u origin <branch> — push with tracking
  4. gh pr create — with title, body, reviewers

PR Title Format:
  <type>(<scope>): <description>    (matches commit conventions)

PR Body Sections:
  ## Summary         — WHAT and WHY (1-3 bullets)
  ## Changes         — Key files and modifications
  ## Test Plan       — How to verify correctness
  ## Screenshots     — Before/after for UI changes

Merge Strategy:
  Feature PRs        -> squash merge
  Release branches   -> merge commit
  Clean linear PRs   -> rebase merge

Files to Set Up:
  .github/pull_request_template.md  — PR template
  .github/CODEOWNERS                — Auto-assign reviewers
  .github/workflows/pr-checks.yml  — CI gates

Commands:
  gh pr create --draft              — Early visibility
  gh pr ready 123                   — Mark ready for review
  gh pr checks 123                  — Verify CI status
  gh pr merge 123 --squash          — Squash merge
```
