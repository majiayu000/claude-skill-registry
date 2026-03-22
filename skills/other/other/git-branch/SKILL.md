---
name: git-branch
description: Use when creating a new branch in dd-sdk-ios for a JIRA ticket or feature. Use when choosing a branch name or base branch for development work.
---

# Branching in dd-sdk-ios

## Convention

Branch names follow: `<author>/<JIRA-TICKET>/<descriptive-slug>`

- `<author>`: your GitHub username or initials
- `<JIRA-TICKET>`: project shortname + ticket number (e.g. `RUM-9999`, `FFL-123`)
- `<descriptive-slug>`: short kebab-case description

**Examples from the repo:**
- `maxep/RUM-14622/visionos-integration-test`
- `bplasovska/RUM-14563/lowercase-header-keys`
- `kelvin/RUM-13420/cache-ddtags`

## Branch Model

The repo follows **git-flow**: `master` is production, `develop` is the integration branch.

For a single PR, branch from `develop`:

```bash
git checkout -b <author>/<JIRA-TICKET>/<slug> develop
```

For large contributions split across multiple PRs, create a shared feature branch first, then branch each PR from it:

```bash
git checkout -b feature/<feature-slug> develop          # shared target branch
git checkout -b <author>/<JIRA-TICKET>/<slug> feature/<feature-slug>  # per-PR branch
```

Each per-PR branch targets `feature/<feature-slug>`. Only the final feature branch is merged into `develop`.

## No JIRA Ticket?

For chores or external contributions without a ticket, use a descriptive slug only:

```bash
git checkout -b <author>/<slug> develop
```
