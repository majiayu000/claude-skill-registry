---
name: git-workflow
description: "Agent Skill: Git workflow best practices for teams and CI/CD. This skill should be used when establishing branching strategies, implementing Conventional Commits, creating or reviewing PRs, managing PR review threads, merging PRs with signed commits, handling merge conflicts, or integrating Git with CI/CD. By Netresearch."
---

# Git Workflow Skill

Expert patterns for Git version control: branching, commits, collaboration, and CI/CD.

## Expertise Areas

- **Branching**: Git Flow, GitHub Flow, Trunk-based development
- **Commits**: Conventional Commits, semantic versioning
- **Collaboration**: PR workflows, code review, merge strategies, thread resolution
- **CI/CD**: GitHub Actions, GitLab CI, branch protection

## Reference Files

Detailed documentation for each area:

| Reference | When to Load |
|-----------|--------------|
| `references/branching-strategies.md` | Managing branches, choosing branching model |
| `references/commit-conventions.md` | Writing commits, semantic versioning |
| `references/pull-request-workflow.md` | Creating/reviewing PRs, thread resolution, merging |
| `references/ci-cd-integration.md` | CI/CD automation, GitHub Actions |
| `references/advanced-git.md` | Rebasing, cherry-picking, bisecting |
| `references/github-releases.md` | Release management, immutable releases |

### Explicit Content Triggers

When creating pull requests, load `references/pull-request-workflow.md` for PR structure, size guidelines, and template patterns.

When reviewing PRs or responding to review comments, load `references/pull-request-workflow.md` for review comment levels (blocking/suggestion/nit) and the code review checklist.

When replying to PR review threads or resolving threads, load `references/pull-request-workflow.md` for the GraphQL API patterns for thread replies and resolution.

When merging PRs, load `references/pull-request-workflow.md` for the merge requirements checklist (resolved threads, Copilot review, rebased branch, CI checks).

When merging in repos requiring signed commits with rebase-only strategy, load `references/pull-request-workflow.md` for the local fast-forward merge workflow.

When handling merge conflicts, load `references/pull-request-workflow.md` for conflict resolution strategies.

When choosing a branching strategy, load `references/branching-strategies.md` for Git Flow, GitHub Flow, and Trunk-based patterns.

When writing commit messages, load `references/commit-conventions.md` for Conventional Commits format and semantic versioning rules.

When creating releases, load `references/github-releases.md` for immutable release warnings and recovery patterns.

## Conventional Commits (Quick Reference)

```
<type>[scope]: <description>
```

**Types**: `feat` (MINOR), `fix` (PATCH), `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

**Breaking change**: Add `!` after type or `BREAKING CHANGE:` in footer.

## Branch Naming

```bash
feature/TICKET-123-description
fix/TICKET-456-bug-name
release/1.2.0
hotfix/1.2.1-security-patch
```

## GitHub Flow (Default)

```bash
git checkout main && git pull
git checkout -b feature/my-feature
# ... work ...
git push -u origin HEAD
gh pr create && gh pr merge --squash
```

## Verification

```bash
./scripts/verify-git-workflow.sh /path/to/repository
```

## GitHub Immutable Releases

**CRITICAL**: Deleted releases block tag names PERMANENTLY. Get releases right first time.

See `references/github-releases.md` for prevention and recovery patterns.

---

> **Contributing:** https://github.com/netresearch/git-workflow-skill
