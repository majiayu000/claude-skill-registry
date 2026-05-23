---
name: clean-branches
user_invocable: true
description: |
  Clean up git branches by analyzing merged/unmerged status, archiving completed work,
  and organizing active branches. This skill should be used when the user wants to clean
  up branches, organize their git repository, or review branch status.
  Triggered by "/clean-branches", "/branches", "clean branches", "check branches", "check branch", or "branches".
---

# Branch Cleanup Skill

This skill provides an iterative workflow for cleaning up git branches by analyzing their merge status and organizing them into appropriate namespaces.

## Quick Start - Run Analysis Script

**ALWAYS run this script first to save tokens:**

```bash
python .claude/skills/clean-branches/analyze_branches.py
```

This script:
- Fetches all branches and analyzes merge/containment status
- Outputs a formatted markdown report
- Identifies branches needing action with recommendations

After reviewing the output, proceed with user approval for any actions (delete, move, archive).

## Branch Organization Schema

| Namespace | Purpose | Example |
|-----------|---------|---------|
| `archive/completed/<name>` | Merged branches (work completed) | `archive/completed/feature-login` |
| `archive/stopped/<name>` | Unmerged branches (abandoned work) | `archive/stopped/experiment-x` |
| `wip/<name>` | Work in progress (active development) | `wip/new-feature` |
| (root) | Keep as-is | `feature-y` |

## Workflow

### Step 1: Identify Default Branch

Query GitHub to determine the default branch:

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

### Step 2: Fetch All Remote Branches

```bash
git fetch --all --prune
```

### Step 3: List All Branches

Get all local and remote branches:

```bash
# Local branches
git branch --list

# Remote branches (excluding HEAD)
git branch -r | grep -v HEAD
```

### Step 4: Analyze Local Branches

For each LOCAL branch (excluding the default branch and already-archived branches):

1. **Check if merged** into default branch:
   ```bash
   git branch --merged <default-branch> | grep -q <branch-name>
   ```

2. **Get last commit info**:
   ```bash
   git log -1 --format="%h %s (%cr by %an)" <branch-name>
   ```

3. **Check if remote exists**:
   ```bash
   git ls-remote --heads origin <branch-name>
   ```

4. **CRITICAL: For local-only branches, check if contained in other branches**:

   If a branch has no remote, check if its commits are already contained in main or any archived branch:

   ```bash
   # Check if branch is ancestor of (contained in) main
   git merge-base --is-ancestor <branch> main && echo "Contained in main"

   # Check if branch is ancestor of any archived branch
   for archived in $(git branch -r | grep "origin/archive/"); do
     git merge-base --is-ancestor <branch> $archived 2>/dev/null && echo "Contained in $archived"
   done

   # Alternative: show all branches that contain this branch's HEAD
   git branch -a --contains <branch>
   ```

   **Interpretation:**
   - If contained in `main` → Work was merged, safe to delete local branch
   - If contained in `archive/completed/*` → Work was completed, safe to delete local branch
   - If contained in `archive/stopped/*` → Work was archived, safe to delete local branch
   - If NOT contained anywhere → Work may be lost if deleted, ask user carefully

### Step 5: Analyze Remote-Only Branches (CRITICAL!)

**This step is often missed!** Check remote branches that have NO local copy and are NOT already archived:

```bash
# List remote branches not merged into default branch
git branch -r --no-merged main | grep -v HEAD | grep -v "archive/" | grep -v "wip/"
```

For each remote-only branch found:

1. **Get last commit info**:
   ```bash
   git log -1 --format="%h %s (%cr by %an)" origin/<branch-name>
   ```

2. **Check if contained in default branch or other branches**:
   ```bash
   # Check what branches contain this remote branch
   git branch -a --contains origin/<branch-name>
   ```

3. **Check merge status**:
   ```bash
   # Is it merged into main?
   git merge-base --is-ancestor origin/<branch-name> main && echo "Merged into main"

   # Is it merged into the current working branch?
   git merge-base --is-ancestor origin/<branch-name> HEAD && echo "Merged into HEAD"
   ```

**Actions for remote-only branches:**
- If contained in `main` → Move to `archive/completed/` (work was merged)
- If contained in current branch but not main → Ask user (might be pending merge)
- If NOT contained anywhere → Ask user: archive/stopped or keep for future work

```bash
# Move remote branch to archive/completed (if merged)
git push origin origin/<branch>:refs/heads/archive/completed/<branch>
git push origin --delete <branch>

# Move remote branch to archive/stopped (if abandoned)
git push origin origin/<branch>:refs/heads/archive/stopped/<branch>
git push origin --delete <branch>
```

### Step 6: Generate Report

Present a summary table to the user:

| Branch | Status | Last Commit | Age | Remote | Contained In | Recommendation |
|--------|--------|-------------|-----|--------|--------------|----------------|
| feature-x | Merged | abc123 Fix bug | 2 weeks | Yes | main | → delete local (work in main) |
| experiment-y | Unmerged | def456 WIP | 3 months | No | archive/stopped/exp-y | → delete local (already archived) |
| new-feature | Unmerged | ghi789 Add X | 1 day | No | (none) | → ask user: WIP/stop/keep |

**Key insight:** If "Contained In" shows another branch, the work is NOT lost - it's safe to delete the local branch.

### Step 7: Delete Contained Local-Only Branches

For local branches that have no remote but ARE contained in another branch (main or archive/*), the work is already preserved elsewhere. These can be safely deleted:

```bash
# Delete local branch that's already contained in main or archive
git branch -d <branch>
```

**Note:** Use `-d` (not `-D`) which will fail if the branch isn't actually merged/contained - this is a safety check.

### Step 8: Process Merged Branches (with remotes)

For branches that have remotes and are confirmed as merged, offer these options:

**Options (in order of preference):**
1. **Archive remote + delete local** (Recommended) - Move remote to archive, delete local copy
2. **Delete both** - Delete both local and remote (work already in target branch)
3. **Keep** - Leave as-is

**Archive remote + delete local** (best option - preserves history on remote):
```bash
# Move remote branch to archive
git push origin origin/<branch>:refs/heads/archive/completed/<branch>

# Delete old remote branch
git push origin --delete <branch>

# Delete local branch
git branch -D <branch>
```

**Delete both** (when you don't need the branch history):
```bash
# Delete remote
git push origin --delete <branch>

# Delete local
git branch -D <branch>
```

### Step 9: Handle Truly Unmerged Branches

For each unmerged branch, ask the user using AskUserQuestion:

- **Keep**: Leave branch as-is
- **WIP**: Move to `wip/<branch-name>`
- **Stop**: Move to `archive/stopped/<branch-name>`

Then execute the chosen action:

```bash
# For WIP
git branch -m <branch> wip/<branch>
git push origin wip/<branch>
git push origin --delete <branch>

# For Stop
git branch -m <branch> archive/stopped/<branch>
git push origin archive/stopped/<branch>
git push origin --delete <branch>
```

### Step 10: Clean Up Synced Archive Branches

Local archive branches that are synced with remote are redundant - they're safely backed up. Offer to delete them:

1. **Identify synced archive branches**:
   ```bash
   # Find local archive branches that have matching remote
   for branch in $(git branch --list 'archive/*'); do
     branch_name=$(echo "$branch" | sed 's/^[* ]*//')
     if git ls-remote --heads origin "$branch_name" | grep -q .; then
       echo "$branch_name"  # Has remote backup, safe to delete locally
     fi
   done
   ```

2. **Present to user**:
   | Local Archive Branch | Remote Status | Recommendation |
   |---------------------|---------------|----------------|
   | archive/completed/feature-x | ✅ Synced | Delete local (backed up) |
   | archive/image-bug | ✅ Synced | Delete local (backed up) |

3. **Offer bulk deletion**:
   Ask using AskUserQuestion:
   - **Delete all synced**: Remove all local archive branches that have remote backups
   - **Review each**: Go through them one by one
   - **Keep all**: Leave local copies

4. **Execute deletion**:
   ```bash
   git branch -D <archive-branch>  # Safe - remote copy exists
   ```

### Step 11: Iterate

After processing, show updated branch list and ask if further cleanup is needed. Repeat until the user is satisfied.

## Important Notes

- **CRITICAL: EVERY action with side effects (delete, rename, move, push) MUST be approved by the user using AskUserQuestion BEFORE execution**
- Query/read operations (git log, git branch --list, git branch --contains, etc.) do NOT require approval
- Never batch multiple branch operations - ask for approval for each branch individually or show a clear list and get explicit confirmation
- Even if analysis shows a branch is "safe to delete", still ask the user first
- Skip branches that are already in `archive/` or `wip/` namespaces (no action needed)
- **Archive branches**: When analyzing, distinguish between:
  - Local-only archives: May want to push to remote first or delete
  - Synced archives: Safe to delete locally (backed up on remote)
  - Remote-only archives: No action needed (already clean locally)
- Handle branches that only exist locally or only on remote
- If a branch has no remote tracking, note this in the report
- Preserve the current checked-out branch (cannot delete/rename it while on it)

### User Approval Flow

1. **Present the analysis** - Show the full report with recommendations
2. **Ask for approval** - Use AskUserQuestion for each branch or group of branches
3. **Execute only after approval** - Never assume user consent
4. **Report results** - Show what was done after each action

Example:
```
Analysis shows: branch-x is contained in main, safe to delete

[AskUserQuestion]: "Delete local branch `branch-x`? (already in main)"
  - Yes, delete
  - No, keep

[Only proceed if user selects "Yes"]
```
