---
name: commit
description: Standardized git commit, push, and PR creation workflow.
triggers:
  - commit
  - push
  - commit-push-pr
allowed-tools: Bash, Read, Glob
model: opus
user-invocable: true
argument-hint: "[type] [message]"
---

# Commit Workflow

## Working Tree
!`git status --short 2>/dev/null`
!`git diff --stat HEAD 2>/dev/null | tail -5`
!`git log --oneline -5 2>/dev/null`

## Quick Commit

```bash
# 1. Check what changed
git status --short
git diff --stat

# 2. Stage specific files (never git add -A blindly)
git add src/components/new-feature.tsx src/lib/utils.ts

# 3. Commit with conventional format
git commit -m "feat: add playlist drag-drop reorder"
```

## Conventional Commits (Required)

```
<type>: <short description>

[optional body]
```

| Type | When |
|------|------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructure, no behavior change |
| `chore` | Dependencies, config, tooling |
| `docs` | Documentation only |
| `test` | Add or update tests |
| `perf` | Performance improvement |

**Rules:**
- Subject line < 70 chars
- Imperative mood: "add" not "added"
- No period at end
- Body explains WHY, not WHAT

## Commit + Push

```bash
git add <files>
git commit -m "feat: description"
git push origin HEAD
```

## Full PR Flow (commit-push-pr)

```bash
# 1. Create branch if on main
git checkout -b feat/playlist-ui

# 2. Stage and commit
git add <files>
git commit -m "feat: add playlist UI with drag-drop"

# 3. Push
git push -u origin feat/playlist-ui

# 4. Create PR
gh pr create --title "Add playlist UI" --body "## Summary
- Drag-drop playlist reorder
- Play queue integration
- Uses existing API routes

## Test plan
- [ ] Create playlist
- [ ] Reorder songs
- [ ] Play from playlist"
```

## Safety Checks

**Before committing (if ANY fail, fix before proceeding):**
- [ ] `npm run typecheck` passes
- [ ] `npm run build` passes
- [ ] No `.env` files staged — unstage if found
- [ ] No `console.log` in staged files — remove if found
- [ ] No hardcoded secrets — remove if found

**Before pushing:**
- [ ] Branch is correct (not pushing to main accidentally)
- [ ] Commit messages are clean

If issues found: fix them, re-stage, re-run checks, THEN commit.

## Version Sync Check (claude-auto-dev repo only)

When committing to this repo, check for stale version strings before staging:

```bash
# Read current version
VERSION=$(cat VERSION 2>/dev/null)

# Grep for previous version references (skip CHANGELOG.md - it's historical)
grep -rn "4\.9\.4\|v4\.9" --include="*.md" --include="*.json" --include="*.ps1" --include="*.sh" . \
  | grep -v CHANGELOG.md | grep -v node_modules | grep -v .git
```

If stale versions found: **fix them before committing.**

Files to check: VERSION, package.json, manifest.json, README.md badge, commands.md, install.sh fallback, install.ps1 fallback.

The current version is: !`cat VERSION 2>/dev/null`

## Batch Commit (During Auto Mode)

During `auto`, commit every 3 tasks:
```bash
git add -A -- ':!.env*' ':!*.pem' ':!*.key' ':!*.secret'
git commit -m "feat: complete S9-1 through S9-3

- S9-1: Playlist UI with drag-drop
- S9-2: Song extend from timestamp
- S9-3: Onboarding wizard"
```

## Amend Last Commit

Only if not pushed yet:
```bash
git add <missed-files>
git commit --amend --no-edit
```

## Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```
