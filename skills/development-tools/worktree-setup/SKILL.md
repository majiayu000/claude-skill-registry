---
description: Create and manage git worktrees for parallel project development
tags: [git, worktree, project-setup, operations]
techStack: [git, powershell]
appliesTo: ["new project", "parallel development", "multi-computer workflow"]
alwaysApply: false
---

# Worktree Setup

> **Category**: Operations
> **Last Updated**: January 2026

---

## Purpose

Manage git worktrees for parallel project development. Worktrees allow multiple working directories from the same repository, each on a different branch, without cloning multiple times.

**Benefits:**
- Work on multiple projects simultaneously
- Each VS Code window has isolated branch state
- No stash juggling when switching projects
- Shared git history across all worktrees

---

## Applies When

- Starting a new project that needs isolation
- Setting up existing project on a new computer
- Cleaning up completed project worktrees
- **Reusing an existing worktree** for a new project (after PR merge)
- Resetting a worktree to start fresh
- **Trigger phrases**: "create worktree", "setup worktree", "new project worktree", "worktree for project", "reuse worktree", "reset worktree"

---

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Worktree folder | `spaarke-wt-{project-name}` | `spaarke-wt-email-automation` |
| Branch name | `work/{project-name}` | `work/email-automation` |
| Location | `C:\code_files\` (sibling to main repo) | `C:\code_files\spaarke-wt-email-automation` |

---

## Workflows

### Workflow A: Create New Project Worktree

**When**: Starting a brand new project

#### Step 1: Gather Information

**ASK user:**
```
What is the project name? (use kebab-case, e.g., "email-automation")
```

Store as: `{project-name}`

#### Step 2: Sync Master (Can Run From Any Location)

**This step ensures master is up-to-date before creating the worktree.**

```powershell
# Navigate to main spaarke repo
cd C:\code_files\spaarke

# Fetch latest from origin
git fetch origin master

# Check if master needs updating
git log master..origin/master --oneline
```

**Decision tree:**
```
IF commits exist (master is behind):
  → Update master:
    git checkout master
    git pull origin master
  → CONFIRM: "Master updated to {commit}"

IF no commits (already up to date):
  → CONFIRM: "Master is already up to date"
```

**If running from a worktree** (e.g., `spaarke-wt-project-planning-and-documentation`):
```powershell
# You can update master without switching to it
cd C:\code_files\spaarke
git fetch origin master:master
```
This fetches and fast-forwards master without needing to checkout.

#### Step 3: Verify Main Repo

```powershell
# Confirm we're in main repo
cd C:\code_files\spaarke
git rev-parse --git-dir
# Should return ".git" (not a path to another repo)
```

**Decision tree:**
```
IF git-dir is not ".git":
  → ERROR: "You're in a worktree, not the main repo"
  → STOP

IF directory doesn't exist:
  → ERROR: "Main repo not found at C:\code_files\spaarke"
  → STOP
```

#### Step 4: Check for Existing Worktree/Branch

```powershell
# List existing worktrees
git worktree list

# Check if branch already exists
git branch --list "work/{project-name}"
git branch -r --list "origin/work/{project-name}"
```

**Decision tree:**
```
IF worktree already exists for this project:
  → WARN: "Worktree already exists at {path}"
  → ASK: "Open existing worktree? (y/n)"
  → If yes: Skip to Step 6

IF branch exists locally or remotely:
  → WARN: "Branch work/{project-name} already exists"
  → ASK: "Use existing branch? (y/n)"
  → If yes: Use `git worktree add` without `-b` flag
  → If no: ASK for different project name
```

#### Step 5: Create Worktree

```powershell
# Create worktree with new branch
git worktree add ..\spaarke-wt-{project-name} -b work/{project-name}
```

**Expected output:**
```
Preparing worktree (new branch 'work/{project-name}')
HEAD is now at {commit} {message}
```

#### Step 6: Provide Next Steps

**Output to user:**
```
✅ Worktree created successfully!

📁 Location: C:\code_files\spaarke-wt-{project-name}
🌿 Branch: work/{project-name}

Next steps:
1. Open in VS Code:
   code -n C:\code_files\spaarke-wt-{project-name}

2. After making changes, push branch to GitHub:
   cd C:\code_files\spaarke-wt-{project-name}
   git add .
   git commit -m "Initial project setup"
   git push -u origin work/{project-name}

3. To start project pipeline:
   /project-pipeline projects/{project-name}
```

---

### Workflow B: Resume Project on Another Computer

**When**: You have a worktree on Computer A and want to work on Computer B

#### Step 1: Gather Information

**ASK user:**
```
What is the project name? (the branch is work/{project-name})
```

#### Step 2: Verify Main Repo Exists

```powershell
cd C:\code_files\spaarke
git status
```

**Decision tree:**
```
IF directory doesn't exist:
  → "Main repo not found. Clone it first:"
  → git clone https://github.com/spaarke-dev/spaarke.git C:\code_files\spaarke
  → THEN continue

IF not a git repo:
  → ERROR: "C:\code_files\spaarke exists but is not a git repo"
  → STOP
```

#### Step 3: Fetch All Branches

```powershell
git fetch --all
```

#### Step 4: Check Branch Exists on Remote

```powershell
git branch -r --list "origin/work/{project-name}"
```

**Decision tree:**
```
IF branch not found:
  → ERROR: "Branch work/{project-name} not found on remote"
  → "Did you push from Computer A? Run: git push -u origin work/{project-name}"
  → STOP
```

#### Step 5: Create Worktree from Existing Branch

```powershell
# Note: NO -b flag - uses existing remote branch
git worktree add ..\spaarke-wt-{project-name} work/{project-name}
```

#### Step 6: Verify Setup

```powershell
cd C:\code_files\spaarke-wt-{project-name}
git status
git log -1 --oneline
```

**Output to user:**
```
✅ Worktree created from existing branch!

📁 Location: C:\code_files\spaarke-wt-{project-name}
🌿 Branch: work/{project-name}
📝 Latest commit: {commit hash} {message}

Open in VS Code:
   code -n C:\code_files\spaarke-wt-{project-name}
```

---

### Workflow C: List Worktrees

**When**: User wants to see all active worktrees

```powershell
cd C:\code_files\spaarke
git worktree list
```

**Format output:**
```
Active Worktrees:
─────────────────
📁 C:/code_files/spaarke                           [master]
📁 C:/code_files/spaarke-wt-project-planning       [work/project-planning-and-documentation]
📁 C:/code_files/spaarke-wt-email-automation       [work/email-automation]
```

---

### Workflow D: Remove Completed Project Worktree

**When**: Project is merged and worktree no longer needed

#### Step 1: Verify Project is Merged

```powershell
cd C:\code_files\spaarke
git fetch origin

# Check if branch is merged to master
git branch --merged master | grep "work/{project-name}"
```

**Decision tree:**
```
IF branch NOT merged:
  → WARN: "Branch work/{project-name} is NOT merged to master"
  → ASK: "Force remove anyway? (y/n)"
  → If no: STOP

IF branch merged:
  → CONFIRM: "Branch is merged. Safe to remove."
```

#### Step 2: Remove Worktree

```powershell
# Remove the worktree
git worktree remove ..\spaarke-wt-{project-name}
```

**If worktree has uncommitted changes:**
```powershell
# Force remove (use with caution)
git worktree remove --force ..\spaarke-wt-{project-name}
```

#### Step 3: Delete Local Branch (Optional)

```powershell
# Delete local branch (safe - only works if merged)
git branch -d work/{project-name}

# Force delete (use if branch wasn't merged)
git branch -D work/{project-name}
```

#### Step 4: Confirm Cleanup

```powershell
# Verify worktree is gone
git worktree list

# Prune any stale worktree references
git worktree prune
```

**Output to user:**
```
✅ Worktree removed successfully!

Cleaned up:
  ❌ Folder: C:\code_files\spaarke-wt-{project-name}
  ❌ Local branch: work/{project-name}

Remote branch still exists (delete via GitHub PR or manually):
  git push origin --delete work/{project-name}
```

---

### Workflow E: Reuse Existing Worktree for New Project

**When**: A worktree exists from a completed/merged project and you want to reuse it for new work

#### Step 1: List Available Worktrees

```powershell
cd C:\code_files\spaarke
git worktree list
```

**ASK user:**
```
Which worktree do you want to reuse?
(e.g., spaarke-wt-email-automation)
```

Store as: `{old-worktree-name}`

#### Step 2: Check Worktree Status

```powershell
cd C:\code_files\{old-worktree-name}

# Get current branch name
git branch --show-current

# Check for uncommitted changes
git status --short

# Check if current branch is merged to master
cd C:\code_files\spaarke
git fetch origin
git branch --merged origin/master | grep "$(cd C:\code_files\{old-worktree-name} && git branch --show-current)"
```

**Decision tree:**
```
IF uncommitted changes exist:
  → WARN: "Worktree has uncommitted changes"
  → ASK: "Discard changes? (y/n)"
  → If no: STOP
  → If yes: Continue (will reset in Step 5)

IF branch NOT merged to master:
  → WARN: "Branch {branch} is NOT merged to master"
  → ASK: "Proceed anyway? You will lose unmerged commits. (y/n)"
  → If no: STOP
```

#### Step 3: Get New Project Name

**ASK user:**
```
What is the new project name? (use kebab-case, e.g., "playbook-builder")
```

Store as: `{new-project-name}`

#### Step 4: Sync Master

```powershell
cd C:\code_files\spaarke
git fetch origin master:master
```

#### Step 5: Create New Branch in Worktree

```powershell
cd C:\code_files\{old-worktree-name}

# Discard any local changes
git reset --hard

# Checkout new branch based on latest master
git checkout -b work/{new-project-name} origin/master
```

**Expected output:**
```
Switched to a new branch 'work/{new-project-name}'
```

#### Step 6: Delete Old Local Branch (Optional Cleanup)

```powershell
# From main repo, delete old merged branch
cd C:\code_files\spaarke
git branch -d work/{old-project-name}
```

**Note:** Skip if the old branch isn't merged or you want to keep it.

#### Step 7: Rename Worktree Folder (Optional)

If you want the folder name to match the new project:

```powershell
# This requires removing and re-adding the worktree
cd C:\code_files\spaarke

# Remove worktree reference (keeps the branch)
git worktree remove ../{old-worktree-name}

# Re-add with new folder name
git worktree add ../spaarke-wt-{new-project-name} work/{new-project-name}
```

**Decision tree:**
```
ASK: "Rename worktree folder to match new project? (y/n)"

IF yes:
  → Execute rename steps above
  → New location: C:\code_files\spaarke-wt-{new-project-name}

IF no:
  → Keep existing folder name
  → Folder stays at: C:\code_files\{old-worktree-name}
```

#### Step 8: Provide Next Steps

**Output to user:**
```
✅ Worktree reused successfully!

📁 Location: C:\code_files\{final-worktree-folder}
🌿 New Branch: work/{new-project-name}
♻️ Old Branch: work/{old-project-name} (deleted/kept)

Next steps:
1. Open in VS Code:
   code -n C:\code_files\{final-worktree-folder}

2. After making changes, push branch to GitHub:
   git add .
   git commit -m "Initial project setup"
   git push -u origin work/{new-project-name}

3. To start project pipeline:
   /project-pipeline projects/{new-project-name}
```

---

### Workflow F: Quick Reset Worktree to Master

**When**: You want to quickly reset a worktree to start fresh without changing branch names

#### Step 1: Navigate to Worktree

```powershell
cd C:\code_files\{worktree-name}
```

#### Step 2: Reset to Latest Master

```powershell
# Fetch latest
git fetch origin master

# Hard reset to master (DESTROYS local changes and commits)
git reset --hard origin/master
```

**⚠️ WARNING:** This destroys all uncommitted changes and unpushed commits!

#### Step 3: Confirm

```powershell
git log -1 --oneline
# Should show latest master commit
```

**Output to user:**
```
✅ Worktree reset to master!

📁 Location: C:\code_files\{worktree-name}
🌿 Branch: {branch-name} (now at master's HEAD)
📝 Latest commit: {commit hash} {message}

The branch still has its original name but now contains master's code.
To rename: git branch -m work/{new-name}
```

---

## Multi-Computer Workflow Summary

```
Computer A (create)              GitHub                Computer B (resume)
─────────────────               ──────                ─────────────────
git worktree add ... -b         ←──────────────────── git fetch --all
  ↓                                                     ↓
Work on files                                        git worktree add ...
  ↓                                                   (no -b flag)
git push -u origin work/...     ──────────────────→    ↓
                                                     git pull
                                                       ↓
                                                     Work on files
                                                       ↓
git pull                        ←────────────────── git push
```

---

## Isolation Rules

| Rule | Why |
|------|-----|
| **One worktree per branch** | Git enforces - can't checkout same branch twice |
| **One Claude Code session per worktree** | Avoids conflicting edits |
| **Merge via PR, not local checkout** | Master is "locked" to main worktree |
| **Don't edit shared root files in parallel** | `*.sln`, `Directory.*`, root `package.json` |
| **Use different ports if running locally** | Avoid port conflicts between worktrees |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "fatal: '{branch}' is already checked out" | Branch is in another worktree; use that worktree or remove it first |
| "fatal: '{path}' already exists" | Folder exists; remove it or use different name |
| Worktree folder deleted manually | Run `git worktree prune` to clean up references |
| Can't checkout master | Master is in main worktree; work from there or use PR to merge |
| Stale worktree reference | `git worktree prune` cleans up |

---

## Parallel Claude Code Sessions

Running multiple Claude Code sessions simultaneously requires careful coordination to avoid merge conflicts.

### Setup for Parallel Sessions

```powershell
# From main repo, create worktrees for each parallel session
cd C:\code_files\spaarke

# Session 1: Feature A
git worktree add ../spaarke-wt-feature-a -b feature/feature-a

# Session 2: Feature B
git worktree add ../spaarke-wt-feature-b -b feature/feature-b

# Session 3: Feature C
git worktree add ../spaarke-wt-feature-c -b feature/feature-c

# Result: 4 independent directories
# C:\code_files\spaarke/              ← Main repo (master)
# C:\code_files\spaarke-wt-feature-a/ ← Session 1
# C:\code_files\spaarke-wt-feature-b/ ← Session 2
# C:\code_files\spaarke-wt-feature-c/ ← Session 3
```

### Commit → Push → PR → Merge Flow

| Concept | What It Does | When |
|---------|--------------|------|
| **Commit** | Save snapshot locally | After each task or logical unit |
| **Push** | Upload to GitHub | After every commit |
| **PR** | Proposed merge (reviewable) | Create draft after first push |
| **Merge** | Actually combine into master | When PR approved |

### Conflict Prevention Rules

| Rule | Description |
|------|-------------|
| **Scope isolation** | Each session works on different files/areas |
| **Frequent commits** | Commit after each task completion |
| **Push after commit** | Keep remote in sync |
| **Draft PR early** | Create after first push for visibility |
| **Rebase before merge** | Always sync with master first |
| **Sequential merge** | Merge one PR at a time |

### When to Rebase

```
Another PR merged to master?
│
├─ YES → Do I touch the same files?
│   │
│   ├─ YES → Rebase NOW
│   │   git fetch origin master
│   │   git rebase origin/master
│   │   git push --force-with-lease
│   │
│   └─ NO → Am I almost done?
│       ├─ YES → Rebase NOW (easier while fresh)
│       └─ NO → Continue, rebase before PR ready
│
└─ NO → Continue working normally
```

### End-of-Task Workflow

After completing each task:

```powershell
# 1. Commit changes
git add .
git commit -m "feat(scope): description"

# 2. Check for master updates
git fetch origin master
git log HEAD..origin/master --oneline

# 3. If master has changes to your files: rebase
git rebase origin/master
git push --force-with-lease

# 4. If no conflicts: push normally
git push origin HEAD
```

### Conflict Detection Commands

```powershell
# See what files other PRs are changing
gh pr list --json number,title,files

# See detailed files for specific PR
gh pr view 101 --json files --jq '.files[].path'

# Compare your changes with master
git diff --name-only HEAD origin/master

# Check overlap with another branch
git diff --name-only HEAD origin/feature/other-project
```

### Handling Same-File Work

When two sessions MUST touch the same files:

| Strategy | When to Use |
|----------|-------------|
| **Sequential** | Safest - Session A merges first, Session B rebases |
| **File ownership** | Each session owns specific directories |
| **Frequent sync** | Both work, rebase every 2-3 tasks |

### Full Parallel Timeline Example

```
TIME    SESSION 1          SESSION 2          MASTER
────    ─────────          ─────────          ──────
T1      commit 1           commit 1
T2      push → PR #101     push → PR #102
T3      commit 2           commit 2
T4      push               push
T5      ✅ DONE            ──working──
T6      rebase             ──working──
T7      PR Ready → Merge                      ← PR #101
T8                         rebase master
T9                         push --force
T10                        commit 3
T11                        push
T12                        ✅ DONE
T13                        PR Ready → Merge   ← PR #102
```

### Run Conflict Check

Use `/conflict-check` skill to detect file overlap with active PRs before starting work or before merging.

---

## Related Skills

- `project-pipeline` - Run after creating worktree to initialize project
- `push-to-github` - For pushing worktree changes
- `pull-from-github` - For syncing worktree across computers
- `repo-cleanup` - Run before removing worktree to validate state
- `conflict-check` - Detect file overlap with active PRs

---

*Last updated: January 2026*
