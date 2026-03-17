---
name: cleaning-up-branches
description: Deletes merged git branches (local and remote) and flags stale unmerged branches for manual review. Use when user mentions "cleanup branches", "delete merged branches", "prune old branches", "remove stale branches", "branch cleanup", or runs /cleanup-branches command.
model: haiku
---

# Branch Cleanup

Delete merged branches (local and optionally remote) with explicit user confirmation, and flag stale unmerged branches for manual review.

## Auto-Invoke Triggers

This skill activates when:

1. **Keywords**: "cleanup branches", "delete merged branches", "prune old branches", "remove stale branches", "branch cleanup", "remove dead branches"
2. **Command**: `/cleanup-branches`

## Arguments

- `--base <branch>` — Base branch for merge check (default: main)
- `--threshold <months>` — Inactivity threshold for stale detection (default: 3)
- `--remote` — Include remote branch deletion
- `--dry-run` — Show what would be deleted without acting

## Safety Model

- **Merged branches**: Deletable after explicit user confirmation
- **Unmerged branches**: Never auto-deleted — reported with manual commands only
- **Dry-run**: Available via `--dry-run` flag to preview actions
- **Confirmation**: Before each destructive step, list branches and ask the user

## Workflow

Execute each step below using the Bash tool.

### Step 1: Validate Git Repository

```bash
git rev-parse --is-inside-work-tree 2>/dev/null || echo "NOT_A_GIT_REPO"
```

If not a git repo, stop and inform the user.

### Step 2: Parse Arguments

Parse `$ARGUMENTS` for:
- `--base BRANCH` → set BASE_BRANCH=BRANCH (default: main)
- `--threshold N` → set THRESHOLD_MONTHS=N (default: 3)
- `--remote` → set INCLUDE_REMOTE=true (default: false)
- `--dry-run` → set DRY_RUN=true (default: false)

Verify the base branch exists:

```bash
git rev-parse --verify "$BASE_BRANCH" 2>/dev/null || echo "BASE_BRANCH_NOT_FOUND"
```

If the base branch doesn't exist, try `master` as fallback. If neither exists, stop and inform the user.

### Step 3: Fetch Latest Remote State

```bash
if ! git fetch --prune 2>/dev/null; then
  echo "Warning: Could not reach remote. Remote branch data may be stale."
fi
```

### Step 4: Display Branch Status Summary

```bash
current_branch=$(git branch --show-current)
total_local=$(git branch | wc -l | tr -d ' ')
total_remote=$(git branch -r | grep -v HEAD | wc -l | tr -d ' ')
remote=$(git config --get "branch.$BASE_BRANCH.remote" 2>/dev/null || echo "origin")
merged_local=$(git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | wc -l | tr -d ' ')
merged_remote=$(git branch -r --merged "$remote/$BASE_BRANCH" | grep -v "$remote/$BASE_BRANCH" | grep -v "$remote/HEAD" | wc -l | tr -d ' ')

echo "=== BRANCH STATUS ==="
echo "Current branch: $current_branch"
echo "Base branch: $BASE_BRANCH"
echo "Local branches: $total_local ($merged_local merged into $BASE_BRANCH)"
echo "Remote branches: $total_remote ($merged_remote merged into $BASE_BRANCH)"
```

Present this summary to the user.

### Step 5: Local Merged Branch Cleanup

List local branches merged into base (excluding base and current branch):

```bash
git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | while IFS= read -r branch; do
  branch="${branch## }"
  last_commit=$(git log -1 --format='%ci' "$branch" 2>/dev/null | cut -d' ' -f1)
  echo "  $branch  (last commit: ${last_commit:-unknown})"
done
```

Count:

```bash
merged_count=$(git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | wc -l | tr -d ' ')
if [ "$merged_count" -eq 0 ]; then
  echo "  (none)"
fi
echo "Found $merged_count local merged branch(es)"
```

**If merged branches exist and not `--dry-run`:**

Ask the user for confirmation using natural conversation: _"These N branches are merged into BASE_BRANCH. Delete them?"_

If confirmed, delete each branch:

```bash
git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | while IFS= read -r branch; do
  branch="${branch## }"
  git branch -d "$branch"
done
```

**If `--dry-run`:** Display what would be deleted but skip the deletion.

### Step 6: Remote Merged Branch Cleanup (if --remote)

Only execute if `--remote` flag was provided.

List remote branches merged into base:

```bash
git branch -r --merged "$remote/$BASE_BRANCH" | grep -v "$remote/$BASE_BRANCH" | grep -v "$remote/HEAD" | while IFS= read -r branch; do
  branch="${branch## }"
  short_name="${branch#$remote/}"
  last_commit=$(git log -1 --format='%ci' "$branch" 2>/dev/null | cut -d' ' -f1)
  echo "  $short_name  (last commit: ${last_commit:-unknown})"
done
```

Count:

```bash
remote_merged=$(git branch -r --merged "$remote/$BASE_BRANCH" | grep -v "$remote/$BASE_BRANCH" | grep -v "$remote/HEAD" | wc -l | tr -d ' ')
if [ "$remote_merged" -eq 0 ]; then
  echo "  (none)"
fi
echo "Found $remote_merged remote merged branch(es)"
```

**If remote merged branches exist and not `--dry-run`:**

Ask the user for confirmation: _"These N remote branches are merged. Delete them from $remote?"_

If confirmed, delete each remote branch:

```bash
git branch -r --merged "$remote/$BASE_BRANCH" | grep -v "$remote/$BASE_BRANCH" | grep -v "$remote/HEAD" | while IFS= read -r branch; do
  branch="${branch## }"
  short_name="${branch#$remote/}"
  git push "$remote" --delete "$short_name"
done
```

**If `--dry-run`:** Display what would be deleted but skip the deletion.

### Step 7: Stale Unmerged Branch Report

List inactive unmerged branches (past threshold) with ahead/behind counts. **Never delete these** — only display them.

Calculate threshold:

```bash
if [[ "$OSTYPE" == "darwin"* ]]; then
  threshold=$(date -v-${THRESHOLD_MONTHS}m +%s)
else
  threshold=$(date -d "${THRESHOLD_MONTHS} months ago" +%s)
fi
```

Scan for stale unmerged branches:

```bash
echo "=== STALE UNMERGED BRANCHES (manual review required) ==="
git for-each-ref --sort=committerdate --format='%(refname:short) %(committerdate:unix) %(committerdate:relative)' refs/heads/ | while IFS= read -r line; do
  branch=$(echo "$line" | awk '{print $1}')
  timestamp=$(echo "$line" | awk '{print $2}')
  relative=$(echo "$line" | cut -d' ' -f3-)

  [ "$branch" = "$BASE_BRANCH" ] && continue

  if [[ "$timestamp" =~ ^[0-9]+$ ]] && [ "$timestamp" -lt "$threshold" ]; then
    merged=$(git branch --merged "$BASE_BRANCH" | grep -w "$branch" | wc -l | tr -d ' ')
    if [ "$merged" -eq 0 ]; then
      counts=$(git rev-list --left-right --count "$BASE_BRANCH"..."$branch" 2>/dev/null)
      behind=$(echo "$counts" | awk '{print $1}')
      ahead=$(echo "$counts" | awk '{print $2}')
      echo "  $branch ($relative) [ahead $ahead, behind $behind]"
    fi
  fi
done
```

After listing, suggest manual deletion commands (but never execute them):

```
To delete these branches manually:
  Local:   git branch -D <branch>
  Remote:  git push origin --delete <branch>
```

### Step 8: Summary Report

Present a summary of all actions taken:

```
=== CLEANUP SUMMARY ===
Local merged branches deleted: N
Remote merged branches deleted: N (or "skipped — use --remote")
Stale unmerged branches flagged: N (manual review)
```

## Important Caveats

- **Squash merges**: Branches merged via squash-and-merge on GitHub will NOT appear as "merged" in `git branch --merged`. They show as unmerged even though their changes are in the base branch. Check stale unmerged branches carefully.
- **Current branch**: The current branch is never deleted, even if merged.
- **Protected branches**: `main`, `master`, and the base branch are always excluded from deletion.
- **Remote permissions**: Deleting remote branches requires push access to the remote.

## Progressive Disclosure

For more details, see:
- [WORKFLOW.md](WORKFLOW.md) — Detailed 5-phase methodology
- [EXAMPLES.md](EXAMPLES.md) — Usage scenarios with sample output
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and solutions

## Version

1.0.0
