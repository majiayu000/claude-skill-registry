---
name: loom-merge-queue-worker
description: Process merge queue items as a Loom merge worker - claim, merge, mark done, handle no-op merges, and resolve compound block conflicts correctly.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T10:47:09.586Z"
  updated_at: "2026-01-29T10:47:09.586Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Process merge queue items for a Loom team's merge worker role.

# When To Use
- You are configured as a merge worker (ROLE: merge, WORKTREE: team/merge-queue)
- Running `loom team wait` wakes you with queue items

# Constraints
- Do NOT implement features; ship only manager-approved branches
- You do NOT ship to main. You only merge into the merge-queue branch shown above
- If your merge worktree is wedged, ask the manager to run: `loom team spawn-merge <TEAM> --force`
- Use `loom team merge` commands for deterministic queue operations

# Procedure

## 1. Claim next item
```
loom team merge <TEAM> next --claim-by merge
```

## 2. Ensure merge-queue is current
```bash
git fetch origin
git merge origin/main --ff-only
```

## 3. Stash any local changes
If `git status` shows unstaged changes, stash them first:
```bash
git stash push -m "Merge preparation for <ticket_id>"
```

## 4. Merge the feature branch
```bash
git merge <branch> --no-ff -m "Merge <branch> into merge-queue (ticket: <ticket_id>)"
```

### Handle Merge Conflicts
If merge fails with conflicts:

#### For compound-managed files (AGENTS.md, LOOM_ROADMAP.md, etc.)
```bash
git checkout --theirs AGENTS.md LOOM_ROADMAP.md
git add AGENTS.md LOOM_ROADMAP.md
```
Rationale: Compound blocks are auto-generated; accept incoming version.

#### For dependency files (pyproject.toml, uv.lock, egg-info/)
```bash
git checkout --theirs pyproject.toml uv.lock
git checkout --theirs src/vibe_piper.egg-info/PKG-INFO
git checkout --theirs src/vibe_piper.egg-info/requires.txt
git add -f pyproject.toml uv.lock src/vibe_piper.egg-info/
```
Rationale: Accept incoming dependencies; newer branches add new optional deps.

#### Complete the merge
```bash
git commit -m "Merge <branch> into merge-queue (ticket: <ticket_id>)"
```

## 5. Mark as done
```bash
loom team merge <TEAM> done <ITEM_ID> --result merged|blocked --note "..."
```
Use one of:
- `--result merged` for successful merges
- `--result blocked` for unresolvable merge conflicts

# Handling No-Op Merges

## When `git merge` returns "Already up to date"

This means commits are already in merge-queue history, even if Loom reports them as "NOT in merge-queue".

### Verify first-parent history
```bash
git log --oneline --first-parent team/merge-queue | grep <commit_hash>
```

If not in the first-parent chain, it's a no-op due to a prior main → merge-queue sync.

### Mark as done with an explanatory note
```bash
loom team merge <TEAM> done <ITEM_ID> --result merged --note "Branch already merged (commits already in merge-queue). Merge was a no-op as expected."
```

## Why this happens
- The feature branch was merged into main
- Main was merged into merge-queue
- When merging the feature branch again, it's a no-op
- The commits are in the full history, just not in the merge commit chain

# Queue Ops Reference
- Claim next: `loom team merge <TEAM> next --claim-by <worker>`
- Mark done: `loom team merge <TEAM> done <ITEM_ID> --result merged|blocked --note "..."`
- Manager ships: `loom team ship <TEAM> --push`
- List queue: `loom team merge <TEAM> list`

# Idling
If no work, run `loom team wait 10m` and stop output.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
