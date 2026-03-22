---
name: cleanup
description: "Use when cleaning up the repository: safe migration to default branch, branch cleanup with merged/stale detection, and rich per-branch status report."
effort: medium
argument-hint: "--branches|--sync|--all"
tags: [git, branch, cleanup, hygiene, status, delivery]
requires:
  bins:
  - git
---



# Repository Cleanup

Full repository hygiene: safely migrate to the default branch, delete merged and squash-merged branches, and produce a per-branch status report. No destructive operations without confirmation.

## When to Use

- Session start, after merging PRs, between tasks, before `/ai-brainstorm`.
- NOT for committing -- use `/ai-commit`.

## Process

### Phase 0: Safe Migration (`--sync` or `--all`)

1. **Detect default branch** -- `git symbolic-ref refs/remotes/origin/HEAD` (main or master).
2. **Record current branch** for the report.
3. **Auto-stash if dirty** -- `git stash push -m "cleanup-auto-stash-$(date +%s)"`.
4. **Switch to default** -- `git checkout <default>`.
5. **Pull latest** -- `git pull --ff-only origin <default>`. If ff-only fails: WARN and STOP.
6. **Restore stash** -- `git stash pop`. If conflict: WARN, leave stash, continue cleanup.

### Phase 1: Branch Analysis (`--branches` or `--all`)

7. **Fetch and prune** -- `git fetch --prune origin`.
8. **Enumerate** all local branches (excluding `main`, `master`).
9. **Classify each branch**:

| Category | Criteria | Action |
|----------|----------|--------|
| Merged | In `git branch --merged <default>` | Delete (`git branch -d`) |
| Squash-merged | Not in `--merged` but `git diff <default>..<branch>` is empty | Delete (`git branch -D`) |
| Gone (safe) | Tracking ref `[gone]` AND no content diff | Delete (`git branch -D`) |
| Gone (has dev) | Tracking ref `[gone]` BUT has content diff | KEEP |
| Active | Has remote tracking, not merged | KEEP |
| Local only | No remote, has commits ahead | KEEP |

10. **Delete eligible** -- merged with `-d`, squash-merged and gone-safe with `-D`.

### Phase 2: Status Report

11. **Build per-branch table**:

```markdown
## Repository Cleanup Report

**Default branch**: `main` (up to date)
**Previous branch**: `feat/old-feature`
**Working tree**: clean | stash restored | stash pending

| Branch | Action | Reason | Remote | Ahead/Behind |
|--------|--------|--------|--------|--------------|
| `feat/done` | DELETED | Merged | -- | -- |
| `feat/squashed` | DELETED | Squash-merged | -- | -- |
| `feat/active` | KEPT | Unmerged (5 commits) | origin/feat/active | +5/-2 |
```

## Quick Reference

```
/ai-cleanup              # full: sync + branch cleanup + report
/ai-cleanup --sync       # sync to default branch only
/ai-cleanup --branches   # branch cleanup only (no migration)
/ai-cleanup --all        # explicit full cleanup
```

## Common Mistakes

- Force-pulling when ff-only fails -- STOP and resolve manually.
- Deleting branches with unmerged local work -- always check content diff.
- Running on `main` -- migration is a no-op but branch cleanup still runs.

## Integration

- Run before `/ai-brainstorm` to start clean.
- Composes with session start protocol.
- Protected branches (`main`, `master`) are never deleted.

## References

- `.ai-engineering/manifest.yml` -- protected branch rules.
- `.agents/skills/brainstorm/SKILL.md` -- spec creation composes cleanup.
$ARGUMENTS
