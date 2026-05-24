---
name: pr-lifecycle
description: GitHub CLI commands and workflows for managing pull requests, CI checks, CodeRabbit reviews, and branch protection
version: 1.1.0
compatibility: All repositories with GitHub

metadata:
  category: workflow
  tags:
    - pull-requests
    - git
    - github-cli
    - code-review
    - branch-protection
    - stacked-prs
  triggers:
    - on-demand
  uses:
    - coderabbit-interactions
    - jira-workflow
    - stacked-prs
---

# PR Lifecycle Management

Comprehensive workflows for managing pull requests using GitHub CLI (`gh`), including CI checks, CodeRabbit reviews, stacked PRs, and branch protection.

## Core Principles

1. **Never Work on Main** - All work must happen on feature/fix/chore branches
2. **Auto-Assignment** - Always assign PRs to the current user after creation
3. **Prevent Terminal Buffering** - Use echo wrappers for `gh` commands
4. **Conventional Commits** - Follow conventional commit format for all commits

## Skill Contents

### Sections

- [Core Principles](#core-principles)
- [Workflow Overview](#workflow-overview)
- [Quick Reference](#quick-reference)
- [Stacked PRs](#stacked-prs)
- [CodeRabbit Integration](#coderabbit-integration)
- [References](#references)
- [Skill Dependencies](#skill-dependencies)

### Available Resources

**references/** - Detailed documentation
- [branch protection](references/branch-protection.md)
- [coderabbit integration](references/coderabbit-integration.md)
- [commit formats](references/commit-formats.md)
- [pr creation](references/pr-creation.md)
- [troubleshooting](references/troubleshooting.md)

---

## Workflow Overview

| Phase | Description | Reference |
|-------|-------------|-----------|
| **Branch Setup** | Create feature branches, never commit to main | `references/branch-protection.md` |
| **PR Creation** | Create draft PRs with proper formatting | `references/pr-creation.md` |
| **CI & Reviews** | Monitor CI, respond to CodeRabbit | `references/coderabbit-integration.md` |
| **Commits** | Use conventional commit format | `references/commit-formats.md` |

## Quick Reference

### Branch Naming Convention

```text
{type}/{JIRA-KEY}-{description}
```

- `feat/` - New features
- `fix/` - Bug fixes
- `chore/` - Maintenance
- `docs/` - Documentation
- `refactor/` - Code restructuring

### Prevent Terminal Buffering

```bash
# Always use echo wrapper for gh commands
echo "Checking..." ; gh pr checks 123 --repo owner/repo ; echo "Done"
```

### Create and Assign PR

```bash
CURRENT_USER=$(gh api user --jq '.login')

PR_URL=$(gh pr create --draft \
    --title "[JIRA-KEY] fix(security): description" \
    --body "## Summary..." \
    --repo owner/repo 2>&1)

PR_NUMBER=$(echo "$PR_URL" | grep -oE '[0-9]+$')
gh pr edit $PR_NUMBER --repo owner/repo --add-assignee "$CURRENT_USER"
```

## Stacked PRs

For dependent changes, use stacked PRs with proper visualization:

### PR Title Format

```text
[JIRA-KEY] type(scope): description (PR N/M)
```

### Stack Visualization (in PR Description)

```markdown
## PR Stack

| # | PR | Title | Status |
|---|-----|-------|--------|
| 1 | #78 | PNPM migration | Merged |
| 2 | **#79** | Shell to JS | This PR |
| 3 | #80 | Skills content | Depends on #79 |
```

### Merge Flow (Not Rebase)

```bash
# After fixing issues in PR #79
git checkout feat/pr-80-branch
git merge feat/pr-79-branch --no-edit
git push origin feat/pr-80-branch
# Repeat for subsequent PRs in stack
```

See `.claude/skills/stacked-prs` for complete stacked PR workflows.

## CodeRabbit Integration

### Key Requirements

1. All CI checks must pass before marking ready
2. Address all CodeRabbit comments including nitpicks
3. CodeRabbit approves automatically after addressing feedback

### Co-Author for CodeRabbit Fixes

```text
Co-authored-by: coderabbitai[bot] <136622811+coderabbitai[bot]@users.noreply.github.com>
```

See `.claude/skills/coderabbit-interactions` for detailed patterns.

## References

| Reference | Content |
|-----------|---------|
| `references/branch-protection.md` | Branch naming, never commit to main |
| `references/pr-creation.md` | PR creation with auto-assignment |
| `references/coderabbit-integration.md` | CodeRabbit status checks and thread replies |
| `references/commit-formats.md` | Commit message templates with attribution |
| `references/troubleshooting.md` | Common issues and solutions |

## Best Practices

1. **Auto-assign PRs** to current user using `gh api user --jq '.login'`
2. **Include Jira key** in branch names, commits, and PR titles
3. **Always use echo wrapper** for `gh` commands to prevent buffering
4. **Always specify `--repo owner/repo`** to avoid directory context issues
5. **Use GraphQL API** for review threads, comments, and replies
6. **Work on other tasks while CI runs** - Don't block on CodeRabbit reviews

## Skill Dependencies

| Skill | Purpose |
|-------|---------|
| `coderabbit-interactions` | Thread replies, comment export, local CLI reviews |
| `jira-workflow` | Ticket creation and Jira key integration |
| `stacked-prs` | Stacked PR management and merge workflows |

## Related

- `.claude/skills/coderabbit-interactions` - Detailed CodeRabbit interaction patterns
- `.claude/skills/jira-workflow` - Jira ticket workflow
- `.claude/skills/stacked-prs` - Stacked PR management
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/pr-lifecycle/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

