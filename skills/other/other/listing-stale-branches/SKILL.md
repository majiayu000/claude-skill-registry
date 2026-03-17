---
name: listing-stale-branches
description: Lists local and remote git branches that are candidates for cleanup — merged but not deleted, and inactive branches with no commits in a configurable period (default 3 months). Use when user mentions "stale branches", "old branches", "branch cleanup", "prune branches", "dead branches", "unused branches", "inactive branches", "branch hygiene", or asks to "list branches to delete", "find stale branches", or runs /stale-branches command.
model: haiku
---

# Stale Branch Detection

Identify git branches that are candidates for cleanup: merged-but-not-deleted and inactive branches with no recent commits.

## Auto-Invoke Triggers

This skill automatically activates when:

1. **Keywords**: "stale branches", "old branches", "branch cleanup", "prune branches", "dead branches", "unused branches", "inactive branches", "branch hygiene"
2. **Actions**: "list branches to delete", "find stale branches", "clean up branches"

## Arguments

- `--threshold <months>` — Inactivity threshold in months (default: 3)
- `--base <branch>` — Base branch for merge check (default: main)
- `--remote` — Include remote branch analysis

## Workflow

Execute each step below using the Bash tool. This is a **read-only** skill — never delete branches, only report findings.

### Step 1: Validate Git Repository

```bash
git rev-parse --is-inside-work-tree 2>/dev/null || echo "NOT_A_GIT_REPO"
```

If not a git repo, stop and inform the user.

### Step 2: Parse Arguments

Parse `$ARGUMENTS` for:
- `--threshold N` → set THRESHOLD_MONTHS=N (default: 3)
- `--base BRANCH` → set BASE_BRANCH=BRANCH (default: main)
- `--remote` → set INCLUDE_REMOTE=true (default: false)

Verify the base branch exists:

```bash
git rev-parse --verify "$BASE_BRANCH" 2>/dev/null || echo "BASE_BRANCH_NOT_FOUND"
```

If the base branch doesn't exist, try `master` as fallback. If neither exists, stop and inform the user.

### Step 3: Calculate Inactivity Threshold

Cross-platform threshold date (epoch seconds):

```bash
# macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
  threshold=$(date -v-${THRESHOLD_MONTHS}m +%s)
else
  # Linux
  threshold=$(date -d "${THRESHOLD_MONTHS} months ago" +%s)
fi
echo "Threshold date (epoch): $threshold"
```

### Step 4: List Merged Branches

Find local branches already merged into the base branch (safe to delete):

```bash
echo "=== MERGED BRANCHES (safe to delete) ==="
merged_count=$(git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | wc -l | tr -d ' ')
git branch --merged "$BASE_BRANCH" | grep -v "^\*" | grep -vw "$BASE_BRANCH" | while IFS= read -r branch; do
  branch="${branch## }"
  last_commit_date=$(git log -1 --format='%ci' "$branch" 2>/dev/null | cut -d' ' -f1)
  echo "  $branch  (last commit: ${last_commit_date:-unknown})"
done
if [ "$merged_count" -eq 0 ]; then
  echo "  (none)"
fi
echo "Total merged: $merged_count"
```

### Step 5: List Inactive Unmerged Branches

Find local branches NOT merged into base with no commits within the threshold period. Include ahead/behind counts:

```bash
echo "=== INACTIVE UNMERGED BRANCHES (review before delete) ==="
git for-each-ref --sort=committerdate --format='%(refname:short) %(committerdate:unix) %(committerdate:relative)' refs/heads/ | while IFS= read -r line; do
  branch=$(echo "$line" | awk '{print $1}')
  timestamp=$(echo "$line" | awk '{print $2}')
  relative=$(echo "$line" | cut -d' ' -f3-)

  # Skip base branch and current branch
  [ "$branch" = "$BASE_BRANCH" ] && continue

  # Check if branch is inactive (older than threshold)
  if [[ "$timestamp" =~ ^[0-9]+$ ]] && [ "$timestamp" -lt "$threshold" ]; then
    # Check if NOT merged
    merged=$(git branch --merged "$BASE_BRANCH" | grep -w "$branch" | wc -l | tr -d ' ')
    if [ "$merged" -eq 0 ]; then
      # Get ahead/behind counts relative to base
      counts=$(git rev-list --left-right --count "$BASE_BRANCH"..."$branch" 2>/dev/null)
      behind=$(echo "$counts" | awk '{print $1}')
      ahead=$(echo "$counts" | awk '{print $2}')
      echo "  $branch ($relative) [ahead $ahead, behind $behind]"
    fi
  fi
done
```

### Step 6: Remote Branch Analysis (if --remote)

Only execute this step if `--remote` flag was provided.

Detect the remote for the base branch and fetch:

```bash
remote=$(git config --get "branch.$BASE_BRANCH.remote" 2>/dev/null || echo "origin")
if ! git fetch --prune 2>/dev/null; then
  echo "Warning: Could not reach remote. Skipping remote analysis."
fi
```

If the fetch warning was shown, skip the rest of Step 6. Otherwise, continue:

List remote merged branches:

```bash
echo "=== REMOTE MERGED BRANCHES ==="
remote_merged_count=$(git branch -r --merged "$BASE_BRANCH" | grep -v "HEAD" | grep -vw "$BASE_BRANCH" | wc -l | tr -d ' ')
git branch -r --merged "$BASE_BRANCH" | grep -v "HEAD" | grep -vw "$BASE_BRANCH" | while IFS= read -r branch; do
  branch="${branch## }"
  last_commit_date=$(git log -1 --format='%ci' "$branch" 2>/dev/null | cut -d' ' -f1)
  echo "  $branch  (last commit: ${last_commit_date:-unknown})"
done
if [ "$remote_merged_count" -eq 0 ]; then
  echo "  (none)"
fi
```

List remote inactive unmerged branches:

```bash
echo "=== REMOTE INACTIVE UNMERGED BRANCHES ==="
git for-each-ref --sort=committerdate --format='%(refname:short) %(committerdate:unix) %(committerdate:relative)' "refs/remotes/$remote/" | grep -v "HEAD" | grep -vw "$BASE_BRANCH" | while IFS= read -r line; do
  branch=$(echo "$line" | awk '{print $1}')
  timestamp=$(echo "$line" | awk '{print $2}')
  relative=$(echo "$line" | cut -d' ' -f3-)

  if [[ "$timestamp" =~ ^[0-9]+$ ]] && [ "$timestamp" -lt "$threshold" ]; then
    merged=$(git branch -r --merged "$BASE_BRANCH" | grep -w "$branch" | wc -l | tr -d ' ')
    if [ "$merged" -eq 0 ]; then
      echo "  $branch ($relative)"
    fi
  fi
done
```

### Step 7: Summary

Present a summary report:

```bash
current_branch=$(git branch --show-current)
total_local=$(git branch | wc -l | tr -d ' ')
merged_into_base=$(git branch --merged "$BASE_BRANCH" | grep -vw "$BASE_BRANCH" | wc -l | tr -d ' ')

echo "=== SUMMARY ==="
echo "Current branch: $current_branch"
echo "Base branch: $BASE_BRANCH"
echo "Inactivity threshold: $THRESHOLD_MONTHS months"
echo "Total local branches: $total_local"
echo "Merged into $BASE_BRANCH: $merged_into_base"
```

After the summary, suggest cleanup commands (but **never execute them**):

```
Cleanup commands (run manually):
  Delete merged local:   git branch -d <branch>
  Delete unmerged local:  git branch -D <branch>
  Delete remote:          git push origin --delete <branch>
  Delete all merged:      git branch --merged main | grep -v main | xargs git branch -d
```

## Important Caveats

- **Squash merges**: Branches merged via squash-and-merge on GitHub will NOT appear as "merged" in `git branch --merged`. They show as unmerged even though their changes are in the base branch. Review inactive unmerged branches carefully.
- **Read-only**: This skill never deletes branches. Deletion commands are shown as suggestions only.
- **Remote analysis**: The `--remote` flag runs `git fetch --prune` which contacts the remote. This requires network access.

## Progressive Disclosure

For more details, see:
- [WORKFLOW.md](WORKFLOW.md) — Detailed 5-phase methodology
- [EXAMPLES.md](EXAMPLES.md) — Usage scenarios with sample output
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and solutions

## Version

1.0.0
