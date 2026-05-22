---
name: branching-strategy
description: >
  Guide git branching strategies, branch naming, and merge/rebase decisions.
  Use when the user creates branches, asks about Git Flow vs trunk-based development,
  discusses merge vs rebase, or is setting up a new repository's branching model.
---

# Branching Strategy

Choose and apply the right branching model for the project's size, team, and release cadence.

## When to Use

- Creating a new branch for a feature, fix, or release
- Deciding between merge and rebase
- Setting up a new repository's branching conventions
- Discussing release management and deployment strategies
- Resolving merge conflicts or untangling branch history

## Core Patterns

### Branch Naming Conventions

Use a consistent prefix/slug format:

```bash
# Format: <type>/<ticket-id>-<short-description>
feature/AUTH-123-add-sso-login
fix/BUG-456-null-pointer-on-logout
refactor/TECH-789-extract-auth-service
hotfix/SEC-101-patch-xss-vulnerability
release/v2.3.0
chore/TECH-202-upgrade-node-20

# Without ticket system
feature/add-user-registration
fix/prevent-race-condition-in-cache
```

Rules:
- Lowercase with hyphens (kebab-case)
- Keep under 50 characters after the prefix
- Include ticket ID when available
- Use descriptive slugs, not cryptic abbreviations

### Git Flow (Structured Releases)

Best for: projects with scheduled releases, multiple environments, or compliance requirements.

```
main ────────●────────────────●──────────── (production)
              \              /
release/v2.1   ●────●──────●               (stabilization)
              /      \
develop ────●────●────●────●────●────────── (integration)
            \        /          \
feature/x    ●──●──●            \
                                 \
feature/y                         ●──●──●
```

```bash
# Start a feature
git checkout develop
git checkout -b feature/AUTH-123-add-sso

# Complete a feature — merge back to develop
git checkout develop
git merge --no-ff feature/AUTH-123-add-sso
git branch -d feature/AUTH-123-add-sso

# Create a release branch
git checkout develop
git checkout -b release/v2.1.0

# Finalize release
git checkout main
git merge --no-ff release/v2.1.0
git tag -a v2.1.0 -m "Release v2.1.0"
git checkout develop
git merge --no-ff release/v2.1.0

# Hotfix from production
git checkout main
git checkout -b hotfix/SEC-101-patch-xss
# ... fix applied ...
git checkout main
git merge --no-ff hotfix/SEC-101-patch-xss
git tag -a v2.1.1 -m "Hotfix v2.1.1"
git checkout develop
git merge --no-ff hotfix/SEC-101-patch-xss
```

### Trunk-Based Development (Continuous Delivery)

Best for: small teams, CI/CD pipelines, frequent deployments.

```
main ──●──●──●──●──●──●──●──●──●── (always deployable)
        \   /  \   /      \   /
         ●─●    ●─●        ●─●     (short-lived branches, <2 days)
```

```bash
# Short-lived feature branch
git checkout main
git pull --rebase origin main
git checkout -b feature/add-search

# Keep branch fresh (daily)
git fetch origin
git rebase origin/main

# Merge back quickly (within 1-2 days)
git checkout main
git merge --no-ff feature/add-search
git push origin main
```

Key rules for trunk-based:
- Branches live less than 2 days
- Feature flags for incomplete work
- Main is always deployable
- No long-lived branches except main

### Merge vs Rebase Decision

```bash
# REBASE: Use for local branch cleanup before merging
# Produces linear history, easier to read
git checkout feature/my-work
git rebase main
git checkout main
git merge --no-ff feature/my-work

# MERGE: Use for integrating shared/public branches
# Preserves full history and merge points
git checkout main
git merge --no-ff feature/my-work

# SQUASH MERGE: Use for PRs with messy intermediate commits
# Produces single clean commit on target branch
git checkout main
git merge --squash feature/my-work
git commit -m "feat: add search functionality"
```

| Strategy     | When to Use                           | Trade-off                    |
|-------------|---------------------------------------|------------------------------|
| Merge       | Shared branches, preserving history   | Noisy log, but full context  |
| Rebase      | Local cleanup, linear history         | Clean log, rewrites history  |
| Squash      | Messy PR history, single logical unit | Cleanest log, loses details  |

**Golden rule**: Never rebase commits that have been pushed to a shared branch.

## Anti-Patterns

### What NOT to Do

- **Long-lived feature branches**: Branches open for weeks accumulate merge conflicts and drift from main. Keep branches short-lived.
- **Committing directly to main**: Even solo developers benefit from branch-based workflow for rollback safety.
- **Rebasing shared branches**: Rewriting history on branches others work on causes lost commits and confusion.
- **Inconsistent naming**: Mixing `feature/`, `feat/`, `Feature/`, and no prefix makes automation and filtering impossible.
- **No branch protection**: Main/develop should require PR reviews and CI checks. Never force-push to protected branches.

```bash
# BAD: Direct commit to main
git checkout main
git commit -m "feat: add new feature"
git push

# BAD: Rebase a shared branch
git checkout develop
git rebase main  # Others are also working on develop!

# GOOD: Feature branch with PR
git checkout -b feature/add-search
# ... work ...
# Open PR, get review, merge via PR
```

## Quick Reference

```
Branch Naming:
  feature/<ticket>-<description>
  fix/<ticket>-<description>
  hotfix/<ticket>-<description>
  release/v<semver>
  chore/<ticket>-<description>

Strategy Selection:
  Scheduled releases + multiple envs  -> Git Flow
  Continuous delivery + small team    -> Trunk-based
  Open source + many contributors     -> GitHub Flow (fork + PR)

Merge Strategy:
  Local cleanup         -> rebase then merge --no-ff
  Shared branch         -> merge --no-ff (never rebase)
  Messy PR commits      -> squash merge

Rules:
  - Never rebase public/shared branches
  - Never force-push to main or develop
  - Keep feature branches under 2 days (trunk-based)
  - Always use --no-ff for merge commits (preserves branch history)
  - Delete branches after merging
```
