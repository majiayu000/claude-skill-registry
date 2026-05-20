---
name: update
description: "Morning update routine: merge Renovate PRs, rebase local work, apply chezmoi changes"
argument-hint: "[--push | --dry-run]"
context: default
allowed-tools:
  - Bash(gh pr list:*)
  - Bash(gh pr checks:*)
  - Bash(gh pr diff:*)
  - Bash(gh run view:*)
  - Bash(git fetch:*)
  - Bash(git status:*)
  - Bash(git stash:*)
  - Bash(git add:*)
  - Bash(chezmoi diff:*)
  - Bash(test -f:*)
  - Read
  # NOTE: These require user approval for safety:
  # - gh pr merge (modifies remote state)
  # - git rebase (can rewrite history)
  # - git push (publishes to remote)
  # - chezmoi apply (installs tools, modifies files)
  # - Edit (for conflict resolution)
---

# Update: Morning Maintenance

Merge Renovate PRs, rebase local work on updated main, resolve conflicts intelligently, and apply chezmoi changes.

## Arguments

```
$ARGUMENTS
```

Options:
- `--push` - Also push rebased commits to origin
- `--dry-run` - Show what would be done without making changes

## Instructions

### 0. Check AGENTS.local.md Freshness

```bash
test -f AGENTS.local.md && echo "exists" || echo "missing"
```

If the file exists, read it and check the `Generated:` date line.

- **Missing:** suggest "Run `/agents-local-md` to generate machine-specific context"
- **Older than 7 days:** suggest "Run `/agents-local-md --force` to refresh machine context"
- **Fresh:** no action needed

This is **advisory only** — continue the update regardless.

### 1. Check for Uncommitted Work

```bash
git status --short
```

If tracked files are modified:
- Stash them: `git stash push -u -m "update skill: stashing before merge"`
- Remember to pop later

### 2. List and Evaluate Renovate PRs

```bash
gh pr list --author "app/renovate" --json number,title,headRefName,statusCheckRollup
```

For each PR:
- Check CI status with `gh pr checks <number>`
- If all critical checks pass (tests, not claude-review), prepare to merge
- If `--dry-run`, just show what would be merged

**Edge case:** `claude-review` failing on its own update PR is fine—it's reviewing itself with an old version

### 3. Merge Passing PRs

For each green PR:
```bash
gh pr merge <number> --squash --delete-branch
```

Collect merged PRs for summary:
- PR number
- Package change (extract from title or diff)

### 4. Fetch and Rebase

```bash
git fetch origin
git rebase origin/main
```

**When conflicts occur:**

1. Read the conflicted file
2. Understand both sides:
   - Incoming (Renovate/main): Usually version bumps
   - Local: New packages, config changes
3. Resolution strategy:
   - **Version conflicts**: Take newer version
   - **New additions on both sides**: Keep both
   - **Structural conflicts**: Favor incoming (Renovate) unless it breaks local additions
4. Edit the file to resolve
5. Stage and continue: `git add <file> && git rebase --continue`

### 5. Handle Feature Branches

If not on main:
```bash
git rebase main
```

Resolve conflicts same as above.

### 6. Pop Stash

If stashed earlier:
```bash
git stash pop
```

Resolve any conflicts using same strategy.

### 7. Push (if requested)

If `--push` in arguments:
```bash
git push origin <current-branch>
```

### 8. Preview Chezmoi Changes

```bash
chezmoi diff
```

Show a summary of what will change (not the full diff if huge).

### 9. Apply Chezmoi

```bash
chezmoi apply
```

If mise tools are updated, they'll be installed automatically.

### 10. Summary

Present a table:

| Action | Details |
|--------|---------|
| PRs merged | #121 (claude-code-action), #122 (codex 0.95.0) |
| Conflicts resolved | Python 3.14.2→3.14.3 + added rust 1.87.0 |
| Chezmoi applied | Python 3.14.3, codex 0.95.0 installed |
| Status | 1 commit ahead of origin/main |

## Examples

```
/update                    → Merge PRs, rebase, apply (no push)
/update --push             → Full update and push to origin
/update --dry-run          → Preview what would happen
```

## Edge Cases

- **No Renovate PRs**: Skip merge step, just rebase/apply
- **All PRs failing**: Don't merge any, report to user
- **Detached HEAD**: Abort with error message
- **Catastrophic conflicts**: If unable to resolve after analysis, abort rebase and report
- **Chezmoi template warning**: Normal after config changes, not an error
- **Mise tool download failures**: Retry or report, but don't block rest of workflow

## Philosophy

This is a single-player repository. Conflicts are rare and changes are easily revertable. The skill prioritizes automation over caution—intelligent resolution beats manual review for routine updates.
