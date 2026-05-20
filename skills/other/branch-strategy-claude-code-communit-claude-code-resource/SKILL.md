---
name: branch-strategy
description: Branch naming conventions, Git Flow vs trunk-based development, feature branch lifecycle, and release strategies. Reference when creating branches, planning releases, or choosing a branching model.
---

# Branch Strategy

## Branch Naming Conventions

Every branch name must follow a structured prefix convention. This keeps the repository navigable, enables CI/CD automation, and makes intent immediately clear.

### Required Prefixes

| Prefix | Purpose | Example |
|---|---|---|
| `feature/` | New functionality or capability | `feature/user-avatar-upload` |
| `fix/` | Bug fixes for existing behavior | `fix/login-redirect-loop` |
| `hotfix/` | Urgent production fixes | `hotfix/payment-null-pointer` |
| `release/` | Release preparation and stabilization | `release/2.4.0` |
| `chore/` | Maintenance, dependencies, tooling | `chore/upgrade-eslint-9` |
| `docs/` | Documentation-only changes | `docs/api-authentication-guide` |
| `refactor/` | Code restructuring without behavior change | `refactor/extract-billing-service` |
| `test/` | Adding or fixing tests only | `test/payment-edge-cases` |
| `experiment/` | Exploratory work, not intended for merge | `experiment/graphql-federation` |

### Naming Rules

1. Use lowercase with hyphens as separators: `feature/add-user-search` not `feature/Add_User_Search`
2. Keep names concise but descriptive: `fix/cart-total` not `fix/the-bug-where-cart-total-shows-wrong-amount`
3. Include a ticket or issue number when one exists: `feature/PROJ-1234-user-avatar-upload`
4. Never use personal names: `feature/search-api` not `feature/anthonys-search-work`
5. Avoid generic names: `fix/login-redirect-loop` not `fix/bug` or `fix/stuff`
6. Maximum length: aim for under 50 characters after the prefix

### Ticket Number Placement

When integrating with issue trackers, place the ticket number immediately after the prefix:

```
feature/PROJ-1234-user-avatar-upload
fix/GH-567-null-pointer-on-empty-cart
hotfix/INC-89-payment-gateway-timeout
```

This enables automated linking between branches, PRs, and issues.

## Branching Models

### Trunk-Based Development

The simplest model. All developers work on short-lived branches off `main` and merge back frequently.

```
main ─────●─────●─────●─────●─────●─────●─────
           \   /       \   /       \   /
            ●─●         ●─●         ●
          (feature)   (fix)     (feature)
```

**When to Use Trunk-Based Development:**

- Teams with strong CI/CD pipelines and automated testing
- Continuous deployment environments
- Small to medium teams (2-15 developers)
- Products that ship continuously (SaaS, web applications)
- Teams practicing feature flags for incomplete work

**Rules:**

1. Branches live no longer than 1-2 days
2. Every commit to `main` must pass all tests
3. Use feature flags to hide incomplete functionality
4. No long-lived branches except `main`
5. Deploy from `main` on every merge (or at minimum daily)
6. Keep changes small and incremental

**Branch Lifecycle:**

```bash
# Create branch from main
git checkout main && git pull
git checkout -b feature/PROJ-123-add-search

# Work in small increments, commit frequently
git add -p && git commit -m "Add search index configuration"
git add -p && git commit -m "Implement basic search query endpoint"

# Rebase onto main before merging
git fetch origin && git rebase origin/main

# Merge via PR (squash or merge commit per team convention)
# Delete branch immediately after merge
```

### Git Flow

A structured model with multiple long-lived branches for teams that need formal release management.

```
main     ─────●──────────────────●──────────────
              |                  |
develop  ─────●────●────●────●───●────●─────────
               \  / \  /    |       /
feature         ●●   ●●   release ●
                            \   /
                             ●─●
```

**When to Use Git Flow:**

- Products with scheduled releases (mobile apps, installed software)
- Teams that maintain multiple versions simultaneously
- Regulated industries requiring release audit trails
- Larger teams (15+ developers) needing coordination
- Projects with dedicated QA phases

**Branch Structure:**

| Branch | Lifetime | Merges Into | Purpose |
|---|---|---|---|
| `main` | Permanent | -- | Production-ready code, tagged releases |
| `develop` | Permanent | `main` (via release) | Integration branch for features |
| `feature/*` | Temporary | `develop` | New work in progress |
| `release/*` | Temporary | `main` and `develop` | Release stabilization |
| `hotfix/*` | Temporary | `main` and `develop` | Urgent production fixes |

**Release Workflow:**

```bash
# 1. Create release branch from develop
git checkout develop && git pull
git checkout -b release/2.4.0

# 2. Only bug fixes, documentation, and release prep on this branch
# No new features allowed

# 3. When stable, merge to main and tag
git checkout main && git merge --no-ff release/2.4.0
git tag -a v2.4.0 -m "Release 2.4.0"

# 4. Back-merge to develop
git checkout develop && git merge --no-ff release/2.4.0

# 5. Delete release branch
git branch -d release/2.4.0
```

**Hotfix Workflow:**

```bash
# 1. Branch from main
git checkout main && git pull
git checkout -b hotfix/payment-null-pointer

# 2. Fix the issue, commit

# 3. Merge to both main and develop
git checkout main && git merge --no-ff hotfix/payment-null-pointer
git tag -a v2.4.1 -m "Hotfix: payment null pointer"
git checkout develop && git merge --no-ff hotfix/payment-null-pointer

# 4. Delete hotfix branch
git branch -d hotfix/payment-null-pointer
```

### GitHub Flow

A simplified model that sits between trunk-based and Git Flow.

**When to Use GitHub Flow:**

- Web applications with continuous deployment
- Open source projects
- Teams that want simplicity but still use pull requests
- When Git Flow feels too heavy but you want PR-based review

**Rules:**

1. `main` is always deployable
2. Branch from `main` for any work
3. Open a PR when you want feedback or are ready to merge
4. Merge to `main` after review and CI passes
5. Deploy immediately after merge

## Branch Protection Rules

### Recommended Protection for `main`

```yaml
branch_protection:
  main:
    required_reviews: 1           # At least one approval
    dismiss_stale_reviews: true   # Re-review after new pushes
    require_status_checks: true   # CI must pass
    required_checks:
      - build
      - test
      - lint
    restrict_pushes: true         # No direct pushes
    require_linear_history: true  # Squash or rebase only
    include_administrators: true  # Rules apply to everyone
```

### Protection by Branch Type

| Rule | `main` | `develop` | `release/*` | `feature/*` |
|---|---|---|---|---|
| Require PR | Yes | Yes | Yes | No |
| Required reviewers | 1-2 | 1 | 1-2 | 0 |
| Require CI pass | Yes | Yes | Yes | Optional |
| Allow force push | No | No | No | Yes (owner) |
| Allow deletion | No | No | After merge | Yes |
| Require signed commits | Recommended | Optional | Optional | No |

## Release Tagging and Semantic Versioning

### Semver Format

```
MAJOR.MINOR.PATCH
  |     |     |
  |     |     └── Bug fixes, no API changes
  |     └──────── New features, backward compatible
  └────────────── Breaking changes
```

### When to Bump Each Number

**MAJOR (breaking):** Removing an API endpoint. Changing a response format. Renaming a public function. Dropping support for a platform.

**MINOR (feature):** Adding a new endpoint. Adding optional parameters. New configuration options. New UI features.

**PATCH (fix):** Bug fixes. Security patches. Performance improvements. Documentation corrections.

### Pre-release and Build Metadata

```
2.4.0-alpha.1      # Alpha pre-release
2.4.0-beta.2       # Beta pre-release
2.4.0-rc.1         # Release candidate
2.4.0+build.1234   # Build metadata (ignored in precedence)
```

### Tagging Checklist

Before creating a release tag:

- [ ] All tests pass on the release branch or main
- [ ] CHANGELOG has been updated with all changes since last release
- [ ] Version numbers updated in package files (package.json, pyproject.toml, etc.)
- [ ] Migration scripts tested if applicable
- [ ] Release notes drafted with user-facing summary
- [ ] Breaking changes documented with migration guide
- [ ] Dependencies audited for known vulnerabilities

### Creating Tags

```bash
# Annotated tag (preferred for releases)
git tag -a v2.4.0 -m "Release 2.4.0: Add user search, fix cart totals"

# Push tags to remote
git push origin v2.4.0

# Or push all tags
git push origin --tags
```

### Tag Naming Convention

- Always prefix with `v`: `v2.4.0` not `2.4.0`
- Match the version in your package files exactly
- Use annotated tags (not lightweight) for releases

## Feature Branch Lifecycle

### Standard Lifecycle

```
1. CREATE    ──  Branch from main/develop with proper prefix
2. DEVELOP   ──  Commit regularly, push daily
3. SYNC      ──  Rebase/merge from upstream regularly
4. REVIEW    ──  Open PR, request review
5. REVISE    ──  Address feedback, push updates
6. MERGE     ──  Squash or merge commit per convention
7. CLEANUP   ──  Delete branch locally and remotely
```

### Keeping Branches Current

```bash
# Option A: Rebase (cleaner history, use for personal branches)
git fetch origin
git rebase origin/main

# Option B: Merge (preserves history, use for shared branches)
git fetch origin
git merge origin/main
```

### Stale Branch Policy

- Branches with no commits for 14+ days should be reviewed
- Branches with no commits for 30+ days should be closed or archived
- Automate stale branch notifications via CI/CD

## Decision Guide

Use this flowchart to choose your branching model:

```
Do you deploy continuously to production?
├── Yes: Do you need PR-based code review?
│   ├── Yes ──► GitHub Flow
│   └── No  ──► Trunk-Based Development
└── No: Do you maintain multiple release versions?
    ├── Yes ──► Git Flow
    └── No: Do you have scheduled release cycles?
        ├── Yes ──► Git Flow (simplified)
        └── No  ──► GitHub Flow
```

## Anti-Patterns to Avoid

1. **Long-lived feature branches** -- Branches open for weeks accumulate merge conflicts and drift from main. Break work into smaller increments.
2. **Merging main into feature branches repeatedly** -- Creates a tangled history. Prefer rebasing for personal branches.
3. **Skipping branch protection** -- Even solo developers benefit from CI checks on main.
4. **Inconsistent naming** -- Mixed conventions make automation impossible. Enforce via CI hooks.
5. **Forgetting to delete merged branches** -- Stale branches clutter the repository. Configure auto-delete on merge.
6. **Direct commits to main** -- Bypasses review and CI. Always use PRs except for truly trivial changes on solo projects.
7. **Release branches without version bumps** -- Every release branch must update version numbers as its first commit.
8. **Cherry-picking without tracking** -- If you cherry-pick a fix to multiple branches, document which branches received the fix.
