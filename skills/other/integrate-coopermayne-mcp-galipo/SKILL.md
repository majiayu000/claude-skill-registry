---
name: integrate
description: Integrate remote feature branches into main
---

# Remote Branch Integration

Integrates remote feature branches into main, one at a time. Works entirely from remote state — no scanning of local folders or sibling repo copies.

## Prerequisites

- You must be in the galipo repo
- Feature branches must be pushed to origin
- Local working directory should be clean (or on main)

## Procedure

### Step 1: Fetch and List Remote Feature Branches

```bash
git fetch origin --prune

echo "=== Remote Feature Branches ==="
echo ""

for branch in $(git branch -r | grep -v 'HEAD' | grep -v 'origin/main' | sed 's|origin/||' | tr -d ' '); do
    COMMITS=$(git rev-list --count origin/main..origin/$branch 2>/dev/null || echo "?")
    FILES=$(git diff --name-only origin/main...origin/$branch 2>/dev/null | wc -l | tr -d ' ')
    echo "  $branch  ($COMMITS commits, $FILES files changed)"
done
```

If there are no remote feature branches, tell the user and stop.

### Step 2: Present Branches and Suggest Order

Show the branches sorted by size (fewest commits/files first) and explain:

> **Recommended merge order: smallest first, largest last.**
> Smaller branches merge cleanly and get out of the way. The largest branch goes last so it absorbs any conflicts from the updated main — you only deal with conflicts once, in one place.
> If any branch is foundational (other branches depend on it), it should go first regardless of size.

**Ask the user: "Which branches do you want to merge, and in what order?"**

Do NOT proceed until the user explicitly confirms which branches to merge. Never assume — only integrate branches the user asks for.

### Step 3: Verify Clean Local State

Before starting, make sure the local repo is clean:

```bash
STATUS=$(git status --porcelain)
if [ -n "$STATUS" ]; then
    echo "WARNING: You have uncommitted local changes:"
    echo "$STATUS"
fi
```

If there are uncommitted changes, stop and ask the user to commit or stash them first.

### Step 4: Merge Each Branch (One at a Time)

For each feature branch the user selected, in the order they chose:

#### 4a. Checkout the branch locally and rebase onto latest main:

```bash
git fetch origin
git checkout $FEATURE_BRANCH
git rebase origin/main
```

If there are conflicts:
- Stop and report: "Conflicts detected while rebasing `$FEATURE_BRANCH`. Please resolve manually, then run `/integrate` again."
- Show the conflicting files: `git diff --name-only --diff-filter=U`
- Do NOT continue to the next branch.

If rebase succeeds, push the rebased branch:
```bash
git push --force-with-lease origin $FEATURE_BRANCH
```

#### 4b. Merge into main:

```bash
git checkout main
git pull origin main
git merge origin/$FEATURE_BRANCH --no-ff -m "Merge branch '$FEATURE_BRANCH'"
```

**DO NOT PUSH.** Tell the user:
> Merged `$FEATURE_BRANCH` into main locally. Review in lazygit and push when ready.

**Wait for the user to confirm they've pushed before proceeding to the next branch.** The next branch needs to rebase onto the updated remote main.

#### 4c. Clean up (after user pushes):

```bash
# Delete the remote feature branch
git push origin --delete $FEATURE_BRANCH

# Delete the local feature branch
git branch -d $FEATURE_BRANCH
```

Ask the user before deleting — some people prefer to keep branches around.

Then proceed to the next branch (back to step 4a).

### Step 5: Final Status

After all selected branches are merged:

```bash
git fetch origin --prune

echo "=== Remaining Remote Feature Branches ==="
REMAINING=$(git branch -r | grep -v 'HEAD' | grep -v 'origin/main' | tr -d ' ')
if [ -z "$REMAINING" ]; then
    echo "  None — all feature branches merged."
else
    echo "$REMAINING"
fi

echo ""
echo "=== Local main status ==="
git log --oneline -5
```

Remind the user to update main in their other repo copies if they use them:
```bash
# In each other repo copy:
git checkout main && git pull origin main
```

## Important Notes

- **Remote-only discovery**: Branch discovery uses `git branch -r`, not local folder scanning. If a branch isn't pushed, it won't show up.
- **Explicit selection only**: Never merge a branch the user didn't ask for.
- **No auto-push**: Never pushes main. The user reviews in lazygit and pushes manually.
- **Conflicts stop everything**: If a rebase has conflicts, stop. Don't skip to the next branch.
- **One at a time**: Each branch must be fully merged and pushed before starting the next, so subsequent rebases are against the updated main.
- **Smallest first**: Default recommendation is smallest branches first, largest last. But user's choice overrides.

## Troubleshooting

### Rebase Conflicts
```bash
# See conflicting files
git diff --name-only --diff-filter=U

# After resolving
git add <resolved-files>
git rebase --continue

# Or abort and try a different order
git rebase --abort
```

### Merge Conflicts
```bash
# See conflicts
git diff --name-only --diff-filter=U

# After resolving
git add <resolved-files>
git commit

# Or abort
git merge --abort
```

### Reset Local Main to Remote
```bash
git checkout main
git fetch origin
git reset --hard origin/main
```
