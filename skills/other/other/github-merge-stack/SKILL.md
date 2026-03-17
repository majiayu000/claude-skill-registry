---
name: github-merge-stack
description: Merge stacked feature branches from Ralph into main, preserving full feature history. Handles PR base updates, sequential squash merges, and branch cleanup.
argument-hint: "[--dry-run] [--no-cleanup]"
allowed-tools: Bash, Read
---

## Purpose

After Ralph completes with `RALPH_CREATE_PR=true`, merge all stacked PRs into main while preserving visibility of when and why each feature was implemented.

## Arguments

- `--dry-run` — Show what would be merged without making changes
- `--no-cleanup` — Skip local branch cleanup after merging

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- On a branch in the repo with open PRs
- PRs created by Ralph with stacked branches

## Template

The merge logic is implemented in `templates/merge-stack.sh`. This script can be:
1. Run directly from the skill's templates folder
2. Copied to a project's `scripts/` directory for convenience

## Workflow

### 1. Copy Script to Project (Optional)

```bash
cp /path/to/skills/shared/github-merge-stack/templates/github-merge-stack.sh scripts/
chmod +x scripts/github-merge-stack.sh
```

### 2. Run the Script

```bash
# Preview what will happen
./scripts/github-merge-stack.sh --dry-run

# Execute merges
./scripts/github-merge-stack.sh

# Execute without local cleanup
./scripts/github-merge-stack.sh --no-cleanup
```

### What the Script Does

1. **Checks prerequisites** — Verifies `gh` CLI is authenticated
2. **Lists open PRs** — Sorted by number (oldest first = merge order)
3. **Dry run** (if `--dry-run`) — Shows plan without executing
4. **Merges PRs sequentially** — For each PR:
   - Updates base to `main` (previous base may be deleted)
   - Squash merges with `gh pr merge --squash --delete-branch`
5. **Syncs local** — Pulls main, prunes remote refs
6. **Cleans up** (unless `--no-cleanup`) — Deletes local `feat/*` branches
7. **Reports results** — Shows merged commits and any remaining branches

## Understanding the Stack

Ralph creates stacked branches where each PR's base is the previous feature branch:

```
main
 └── feat/story-001  →  PR #1 (base: main)
      └── feat/story-002  →  PR #2 (base: feat/story-001)
           └── feat/story-003  →  PR #3 (base: feat/story-002)
```

## Why Squash Merge

- **One commit per feature** — Clean main history
- **Full context preserved** — Ralph's detailed commit messages (description, acceptance criteria, files) become the squash commit body
- **Traceability** — `git blame` traces to originating story, `git log --grep` finds features

## Output

The script reports:
- Number of PRs merged
- Commits now in main (with hashes and titles)
- Branches cleaned up
- Any failed PRs (conflicts to resolve manually)
- Commands for viewing history

## Viewing History Later

```bash
# See all features
git log --oneline

# Full details of a feature  
git show <commit-hash>

# Find specific story
git log --grep="story-003"

# Why was this line changed?
git blame path/to/file.ts
```

## Error Handling

- **PR has conflicts:** Skipped, reported at end for manual resolution
- **gh not authenticated:** Exits with instructions to run `gh auth login`
- **No open PRs:** Reports nothing to merge
- **Branch delete fails:** Continues, reports at end

## Reference

See `reference/github-merge-stack-reference.md` for troubleshooting and manual procedures.
