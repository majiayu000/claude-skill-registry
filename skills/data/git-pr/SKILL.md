---
name: git-pr
description: >-
  Create pull requests following project conventions.
  Use when creating feature PRs, bug fix PRs, hotfix PRs, or release PRs.
  Invoked by: "create PR", "pull request", "open PR", "submit PR".
---

# Pull Request Creation SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
This SOP guides developers through creating pull requests that follow project conventions. It covers all PR types (feature, bug fix, hotfix, release) with proper documentation, branch flows, and templates.

### When to Use
**ALWAYS**: Creating any PR for the project
**SKIP**: Draft PRs, WIP PRs (use GitHub UI directly)

---

## Process Workflow

### Flow Diagram
```
[Identify Type] --> [Analyze Changes] --> [Create Summary] --> [Submit PR]
```

### Phase Summary
| Phase | Objective | Deliverable |
|-------|-----------|-------------|
| 1. Identify Type | Determine PR category | PR type selected |
| 2. Analyze Changes | Review commits and diffs | Change summary |
| 3. Create Summary | Draft title and description | PR documentation |
| 4. Submit PR | Execute `gh pr create` | Active GitHub PR |

---

## Quick Start

1. **Ensure branch is ready**: All changes committed, tests passing
2. **Determine PR type**: Feature, Bug Fix, Hotfix, or Release
3. **Create PR**: Use the appropriate template below
4. **Fill template**: Complete all sections
5. **Request review**: Assign reviewers

See [Process Workflow](#process-workflow) for detailed steps.

---

## PR Types & Decision Tree

### Decision Tree

```
What are you merging?
  |-- Production release? (development -> main) -> [RELEASE PR]
  |-- Critical production fix? (urgent) -> [HOTFIX PR] (hotfix -> main)
  |-- Bug fix? (non-urgent) -> [BUG FIX PR] (bugfix -> development)
  |-- New functionality? -> [FEATURE PR] (feature -> development)
```

### Quick Reference

| PR Type | From -> To | Urgency | Title Format | Duration |
|---------|------------|---------|--------------|----------|
| **Feature** | feature -> development | Normal | `feat: <description>` | 5-10 min |
| **Bug Fix** | bugfix -> development | Normal | `fix: <description>` | 3-7 min |
| **Hotfix** | hotfix -> main | **URGENT** | `hotfix: <description>` | 3-7 min |
| **Release** | development -> main | Scheduled | `Release: <version>` | 15-30 min |

### Branch Naming Convention

- `development` or `develop` - Development branch (target for feature/bugfix PRs)
- `main` or `master` - Production branch (target for hotfix/release PRs)

> Note: Verify your project's branch naming convention before creating PRs.

---

## Phase 1: Analyze Changes

### Step 1.1: Review Commit History

```bash
# Generic format
git log BASE..HEAD --oneline --no-merges

# Examples by PR type:
git log development..feature/my-feature --oneline --no-merges  # Feature PR
git log development..bugfix/my-fix --oneline --no-merges       # Bug Fix PR
git log main..hotfix/critical-fix --oneline --no-merges        # Hotfix PR
git log main..development --oneline --no-merges                # Release PR

# Get detailed commit messages
git log BASE..HEAD --pretty=format:"%s" --no-merges

# Count commits
git rev-list --count BASE..HEAD
```

### Step 1.2: Analyze Code Differences

```bash
# View diff statistics
git diff BASE...HEAD --stat
git diff BASE...HEAD --shortstat
git diff BASE...HEAD --name-only

# Area-specific diffs (adjust paths to your project structure)
git diff BASE...HEAD --stat -- src/components/
git diff BASE...HEAD --stat -- src/pages/
git diff BASE...HEAD --stat -- src/store/
```

### Step 1.3: Categorize Changes

Group changes by type:
- **Features**: New functionality
- **Fixes**: Bug corrections
- **Refactors**: Code improvements
- **Infrastructure**: Dependencies, config
- **Tests**: Test coverage
- **Documentation**: Docs updates

---

## Phase 2: Create PR Summary

### Step 2.1: Draft PR Title

**Feature PR**:
```
feat: Add AI assistant chat interface
Feature: Dark mode support
```

**Bug Fix PR**:
```
fix: Resolve navigation issue on page load
```

**Hotfix PR**:
```
hotfix: Prevent critical crash on startup
```

**Release PR**:
```
Release: v4.1.0 - AI Assistant & Dark Mode
```

### Step 2.2: Draft PR Description

Use the appropriate template below.

---

## PR Templates

### Feature PR Template

```markdown
## Summary
[Brief overview of feature]

## Changes
- Change 1
- Change 2

## Affected Areas
- [ ] Components/UI
- [ ] Pages/Views
- [ ] State Management
- [ ] Routing/Navigation
- [ ] Utils/Types
- [ ] API/Services

## Testing
[Describe testing performed]

## Related
- Issue: #XXX
- Ticket: XXX

Generated with [Claude Code](https://claude.com/claude-code)
```

### Bug Fix / Hotfix PR Template

```markdown
## Issue
[What was broken]

## Fix
[What was fixed]

## Root Cause
[If known and relevant]

## Affected Areas
- [ ] Components/UI
- [ ] Pages/Views
- [ ] State Management
- [ ] Routing/Navigation
- [ ] Utils/Types
- [ ] API/Services

## Verification
[How to verify the fix]

## Related
- Incident: #XXX
- Issue: #XXX

Generated with [Claude Code](https://claude.com/claude-code)
```

### Release PR Template

```markdown
## Release: v{version}

### Overview
[High-level summary of release]

### Features
- Feature 1 - [Brief description]
- Feature 2 - [Brief description]

### Fixes
- Fix 1 - [Brief description]
- Fix 2 - [Brief description]

### Improvements
- Improvement 1
- Improvement 2

### Affected Areas
- [ ] Components/UI
- [ ] Pages/Views
- [ ] State Management
- [ ] Routing/Navigation
- [ ] Utils/Types
- [ ] API/Services

### Testing Summary
[Summary of testing performed]

### Deployment Notes
[Any special deployment considerations]

### Breaking Changes
[If any, list here]

Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Phase 3: Create Pull Request

### Step 3.1: Verify Prerequisites

Before creating PR:

```bash
# Run tests (use your project's test command)
npm test

# Type check (if TypeScript project)
npx tsc --noEmit

# Lint (use your project's lint command)
npm run lint
```

### Step 3.2: Push Branch (if needed)

```bash
git push origin <branch-name>
```

### Step 3.3: Execute PR Creation

**Feature PR Example**:
```bash
gh pr create \
  --base development \
  --head feature/user-settings \
  --title "feat: Add user settings page" \
  --body "$(cat <<'EOF'
## Summary
Implemented user settings page with preferences management.

## Changes
- Added UserSettings component
- Created settings state slice
- Added settings route

## Affected Areas
- [x] Components/UI
- [x] Pages/Views
- [x] State Management

## Testing
Verified settings page loads correctly and saves preferences.

## Related
- Ticket: #12345

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Bug Fix PR Example**:
```bash
gh pr create \
  --base development \
  --head bugfix/routing-issue \
  --title "fix: Resolve routing issue on page navigation" \
  --body "$(cat <<'EOF'
## Issue
Page navigation fails when accessing certain routes.

## Fix
Updated route parameter handling.

## Root Cause
Type mismatch between route params and page props.

## Verification
Navigate to affected page -> Should load correctly.

## Related
- Issue: #456

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Release PR Example**:
```bash
gh pr create \
  --base main \
  --head development \
  --title "Release: v2.1.0 - User Settings & Performance Improvements" \
  --body "$(cat <<'EOF'
## Release: v2.1.0

### Overview
Release adding user settings and performance improvements.

### Features
- User settings page
- Dark mode support

### Fixes
- Routing issue on page navigation
- State persistence fix

### Testing Summary
- All unit tests passing
- Manual testing completed

### Deployment Notes
[Any deployment-specific notes]

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## Quick Reference

### Git Commands

```bash
# Review commits
git log BASE..HEAD --oneline --no-merges

# Review diffs
git diff BASE...HEAD --stat

# Push branch
git push origin <branch-name>
```

### GitHub CLI Commands

```bash
# Install (macOS)
brew install gh

# Authenticate
gh auth login

# Create PR
gh pr create --base <target> --head <source> --title "<title>" --body "<body>"

# List PRs
gh pr list

# View PR
gh pr view <number>
```

### Common Branch Flows

| From | To | PR Type |
|------|----|---------|
| feature/* | development | Feature |
| bugfix/* | development | Bug Fix |
| hotfix/* | main | Hotfix |
| development | main | Release |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `gh` not found | Install: `brew install gh` (macOS) or see [GitHub CLI docs](https://cli.github.com/) |
| Auth required | Run `gh auth login` |
| Branch not found | Push first: `git push origin <branch>` |
| Invalid base branch | Verify target exists: `git branch -r` |
| Tests failing | Run tests, fix failures |
| Type errors | Run type check, fix errors |
| Linting errors | Run linter, fix violations |
| Description too long | Use `--body-file` instead of inline |

---

## Success Checklist

### All PR Types
- [ ] PR type identified correctly
- [ ] Commit history reviewed
- [ ] Code diffs analyzed
- [ ] Affected areas identified
- [ ] PR title follows format
- [ ] PR description uses template
- [ ] Tests passing
- [ ] TypeScript passes
- [ ] Linting passes
- [ ] PR created successfully

### Additional for Release PRs
- [ ] Version number verified
- [ ] All changes categorized
- [ ] Breaking changes noted
- [ ] Deployment notes included

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/dev-feature` | Feature development workflow | Before creating PR |
| `/review-code` | Code review process | Before creating PR |
| `/test` | Testing workflow | Before creating PR |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
