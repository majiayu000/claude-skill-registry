---
name: github-project
description: "GitHub repository setup and configuration. This skill should be used when creating new GitHub repositories, configuring branch protection or rulesets, setting up CODEOWNERS, or troubleshooting PR merge issues. By Netresearch."
---

# GitHub Project Skill

GitHub repository setup, configuration, and best practices for collaboration workflows.

## Core Workflow

To set up or configure a GitHub repository, follow these steps:

1. Consult the appropriate reference for your task
2. Copy and customize the relevant asset templates
3. Run `scripts/verify-github-project.sh` to validate configuration
4. Apply settings via GitHub UI or `gh` CLI

## Using Reference Documentation

### Repository Setup

When setting up repository structure, consult `references/repository-structure.md` for standard file layout, required documentation files, and directory conventions.

When migrating from master to main branch, consult `references/branch-migration.md` for step-by-step migration commands and branch protection updates.

### Dependency Management

When configuring automated dependency updates, consult `references/dependency-management.md` for Dependabot and Renovate configuration patterns, auto-merge workflows, and update strategies.

### GitHub Features

When working with sub-issues, consult `references/sub-issues.md` for GraphQL API usage, parent-child relationships, and issue hierarchy patterns.

When setting up automatic release labeling, consult `references/release-labeling.md` for PR labeling workflows, release categorization, and changelog automation.

## Running Scripts

### Repository Verification

To verify GitHub project configuration against best practices:

```bash
scripts/verify-github-project.sh /path/to/repository
```

This script checks:
- Repository documentation (README, LICENSE, SECURITY.md)
- Collaboration setup (CODEOWNERS, issue/PR templates)
- Dependency automation (Dependabot/Renovate, auto-merge)
- Release configuration

## Using Asset Templates

### Repository Documentation

To set up CODEOWNERS for code review assignments, copy `assets/CODEOWNERS.template` to `.github/CODEOWNERS`.

To add contribution guidelines, copy `assets/CONTRIBUTING.md.template` to `CONTRIBUTING.md`.

To configure security vulnerability reporting, copy `assets/SECURITY.md.template` to `SECURITY.md`.

### Issue and PR Templates

To add a bug report template, copy `assets/bug_report.md.template` to `.github/ISSUE_TEMPLATE/bug_report.md`.

To add a feature request template, copy `assets/feature_request.md.template` to `.github/ISSUE_TEMPLATE/feature_request.md`.

To standardize PR descriptions, copy `assets/PULL_REQUEST_TEMPLATE.md.template` to `.github/PULL_REQUEST_TEMPLATE.md`.

### Dependency Automation

To configure Dependabot, copy `assets/dependabot.yml.template` to `.github/dependabot.yml`.

To configure Renovate, copy `assets/renovate.json.template` to `renovate.json`.

### Auto-Merge Workflows

To enable basic auto-merge for dependency updates, copy `assets/auto-merge.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with direct commits (no merge queue), copy `assets/auto-merge-direct.yml.template` to `.github/workflows/auto-merge.yml`.

To enable auto-merge with merge queue support, copy `assets/auto-merge-queue.yml.template` to `.github/workflows/auto-merge.yml`.

### Release Automation

To set up automatic release labeling for PRs, copy `assets/release-labeler.yml.template` to `.github/workflows/release-labeler.yml`.

## Go Project CI Checklist

When setting up CI for Go projects, ensure these GitHub configurations:

| Setting | Purpose | How |
|---------|---------|-----|
| Branch protection | Require tests pass before merge | Branch settings or Rulesets |
| Dependabot/Renovate | Automated dependency updates | `.github/dependabot.yml` or `renovate.json` |
| Auto-merge workflow | Merge minor/patch updates automatically | `assets/auto-merge*.yml` templates |
| Required checks | CI workflow names in branch protection | Match exact workflow job names |

## Merge Strategy & Signed Commits

When configuring repositories that require signed commits with clean history, consult `references/merge-strategy.md` for the recommended settings.

### Quick Reference

For signed commits workflow (rebase locally + merge commit):

| Repository Setting | Value | Why |
|--------------------|-------|-----|
| `allow_merge_commit` | **true** | Preserves signatures on feature branch commits |
| `allow_rebase_merge` | true | GitHub requires at least one of squash/rebase |
| `allow_squash_merge` | false | Destroys individual commit signatures |

| Branch Protection | Value | Why |
|-------------------|-------|-----|
| `required_signatures` | true | Enforces GPG/SSH signed commits |
| `required_linear_history` | **false** | Must be false - conflicts with merge commits |

### Workflow

```bash
# 1. Developer rebases PR branch locally (signs commits)
git fetch origin && git rebase origin/main
git push --force-with-lease

# 2. Merge via merge commit (preserves signatures)
gh pr merge <number> --merge
```

### Auto-Merge Compatibility

| Merge Strategy | Works with `required_signatures`? |
|----------------|-----------------------------------|
| Merge commit | ✅ Yes - GitHub signs the merge commit |
| Rebase merge | ❌ No - GitHub cannot sign rewritten commits |
| Squash merge | ❌ No - GitHub cannot sign squashed commit |

**Important:** When enabling auto-merge, select "Create a merge commit" strategy.

## Related Skills

When implementing Go code patterns and CI/CD workflows, use the `go-development` skill.

When implementing OpenSSF Scorecard, SLSA provenance, or signed releases, use the `enterprise-readiness` skill.

When establishing Git branching strategies or conventional commits, use the `git-workflow` skill.

When conducting deep security audits (OWASP, CVE analysis), use the `security-audit` skill.

## External Resources

When understanding GitHub Actions syntax, consult the [GitHub Actions Documentation](https://docs.github.com/en/actions).

When configuring branch protection, consult the [GitHub Branch Protection Guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches).

When setting up Dependabot, consult the [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot).

---

> **Contributing:** https://github.com/netresearch/github-project-skill
