---
name: release
description: "Full release workflow including milestone validation, squash, rebase, push, merge to main, and GitHub release creation. Triggers on keywords: release, create release, publish release, tag release"
project-agnostic: true
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - Write
  - AskUserQuestion
  - Skill
---

# Release Command

Full release workflow: validate changelog, squash commits, create tag, rebase, push, and merge to main.

**No arguments required** - all values auto-detected.

## Context Awareness

**INVOKE** `git-safe` skill to gain context about safe history rewriting patterns.

## Phase 1: Invoke /milestone (No Args)

**INVOKE** `/milestone` with no arguments.

This will:
1. Auto-detect base branch (origin/main)
2. Auto-detect version (patch bump from VERSION file or latest tag)
3. Validate CHANGELOG [Unreleased] section
4. Squash commits into single commit
5. Create annotated version tag

**IMPORTANT**: When /milestone prompts "Proceed with push? (yes/no)", answer **"no"**.

We will push after rebase to ensure clean history.

**Capture** from /milestone output:
- `VERSION`: The version tag created (e.g., `v1.2.3`)
- `BRANCH`: Current branch name
- `SQUASH_SHA`: The squashed commit SHA

If /milestone fails: **STOP** - show error, do not proceed.

## Phase 2: Rebase onto origin/main

After successful /milestone (declined push):

### 2.1 Fetch Latest
```bash
git fetch origin main
```

### 2.2 Check Rebase Needed
```bash
git rev-list HEAD..origin/main --count
```

If count > 0 (main has new commits), rebase is needed.

### 2.3 Perform Rebase
```bash
git rebase origin/main
```

If rebase conflicts:
1. Show conflicting files: `git status`
2. Provide resolution guidance
3. Wait for user to resolve manually
4. After resolution: `git rebase --continue`
5. If user wants to abort: `git rebase --abort`
   - Note: Tag {VERSION} still points to pre-rebase commit

## Phase 3: Re-create Tag (if rebase changed SHA)

### 3.1 Check if Tag Needs Update
```bash
TAG_SHA=$(git rev-list -n1 {VERSION} 2>/dev/null)
HEAD_SHA=$(git rev-parse HEAD)
```

If `TAG_SHA != HEAD_SHA`:

### 3.2 Delete Old Tag
```bash
git tag -d {VERSION}
```

### 3.3 Create New Tag on Rebased Commit
```bash
git tag -a {VERSION} -m "Release {VERSION}"
```

## Phase 4: Push Branch and Tag

### 4.1 Force Push Branch
```bash
git push --force-with-lease origin {BRANCH}
```

Due to squash + rebase, force push is required.

### 4.2 Push Tag
```bash
git push origin {VERSION}
```

If tag already exists on remote (from failed previous attempt):
```bash
git push --delete origin {VERSION}
git push origin {VERSION}
```

## Phase 5: Merge to Main

### 5.1 Confirmation Gate

**STOP HERE** and show:

```
Ready to merge to main:
- Branch: {BRANCH}
- Version: {VERSION}
- Commit: {HEAD_SHA short}

This will:
1. Checkout main
2. Pull latest
3. Fast-forward merge from {BRANCH}
4. Push main

Proceed with merge to main? (yes/no)
```

**Wait for explicit "yes"**. Any other response = abort merge (release still valid).

### 5.2 Execute Merge (on "yes")

```bash
git checkout main
git pull origin main
git merge --ff-only {BRANCH}
```

If fast-forward fails:
```
Fast-forward merge failed. This means main has diverged.

Options:
(A) Force merge (creates merge commit)
(B) Abort - investigate manually

Choose (A/B):
```

**On "A":**
```bash
git merge {BRANCH} -m "chore(release): merge {BRANCH} for {VERSION}"
```

**On "B":** STOP - checkout back to {BRANCH}.

### 5.3 Push Main
```bash
git push origin main
```

## Phase 6: Final Report

Display summary:

```
## Release Complete

### Version Released
- Tag: {VERSION}
- Commit: {FINAL_SHA}
- Message: {commit message first line}

### Commits Included
{list from squash - from /milestone output}

### Branch Status
- Feature branch: {BRANCH} (pushed)
- Main branch: merged and pushed
- Tag: {VERSION} (pushed)

### Remote URLs
- Branch: {remote URL for branch}
- Main: {remote URL for main}
- Release: {remote URL for tag}

### Cleanup (optional)
To delete feature branch:
  git branch -d {BRANCH}
  git push origin --delete {BRANCH}
```

## Abort Conditions

| Condition | Action |
|-----------|--------|
| /milestone fails | STOP: Show /milestone error |
| Rebase conflicts unresolved | STOP: Provide manual resolution steps |
| Push fails | STOP: Show error, suggest manual push |
| Fast-forward merge fails | Offer force merge or abort |
| User declines merge | Release is valid, just not merged to main |

## Usage

```bash
# Full auto - no arguments needed
/release
```

The command will:
1. Run /milestone (no args) - validates, squashes, tags
2. Rebase onto origin/main
3. Re-tag if needed
4. Push branch and tag
5. Merge to main (with confirmation)
6. Report results
