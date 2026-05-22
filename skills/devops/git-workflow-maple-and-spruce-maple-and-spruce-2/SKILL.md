---
name: git-workflow
description: Branch naming, commit conventions, PR process, and issue tracking workflow. Use when creating branches, commits, or PRs.
---

# Git Workflow

## When to Use

Use this skill when creating branches, making commits, creating pull requests, or working with GitHub issues.

## Branch Protection

`main` branch is protected. All changes must go through pull requests.
- Direct pushes to `main` are blocked
- All work happens on feature branches
- PRs required even for solo development

## Branch Naming

```bash
git checkout main
git pull origin main
git checkout -b feature/{issue-number}-{short-description}
```

Patterns:
- `feature/[issue-number]-[short-description]`
- `fix/[issue-number]-[short-description]`
- `chore/[description]`

## Commit Conventions

**Format:**
```
<type>: <short description>

[optional body]

[Fixes #123]
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `chore`, `test`

**Rules:**
1. Commit frequently with small, focused commits
2. Describe what and why
3. Reference issues with `#issue-number`

**Examples:**
```bash
git commit -m "feat: add artist creation form (#2)"
git commit -m "fix: correct commission calculation (#5)"
```

## Pull Request Process

```bash
git push -u origin feature/{branch-name}
gh pr create --title "feat: description (#issue)" --body "..."
```

**PR template:**
```markdown
## Summary
[Brief description]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Tested locally

Closes #[issue-number]
```

## Working with Issues

### Before Starting Work
1. Check GitHub issues: `gh issue list`
2. Create or find an existing issue
3. Create feature branch referencing the issue
4. Reference issue in commits and PR (`Closes #XX`)

### Creating Issues
```bash
gh issue create \
  --title "Bug: description" \
  --label "bug,phase-X" \
  --body "## Description..."
```

### Issue Labels
- `phase-1` through `phase-5`: Phase-specific work
- `epic`: Large feature area

## Checklists

### Before Committing
- [ ] On feature branch (not main)
- [ ] Code follows patterns doc
- [ ] No credentials committed
- [ ] TypeScript compiles
- [ ] Commit references issue

### Before PR
- [ ] Commits pushed
- [ ] PR description complete
- [ ] Issue referenced
- [ ] Self-reviewed diff

### Before Merge
- [ ] PR approved (or self-reviewed)
- [ ] No conflicts
- [ ] CI passes
