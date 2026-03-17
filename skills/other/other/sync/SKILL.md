---
name: "sync"
description: "Merge main, commit changes, and push"
argument-hint: "[message]"
---

Merges from origin/main, commits any local changes with professional message generation, and pushes to remote. This ensures the current branch is always ahead of (or equal to) origin/main, never behind or diverged.

**Goal**: Current branch HEAD >= origin/main (no divergence, no outdated commits)

**What this means**:
- "Ahead" = local branch has commits that origin/main doesn't have yet
- "Equal" = local branch is at the same commit as origin/main
- "Behind/Diverged" = ❌ Never allowed - always merge first to stay current

## Optional commit message hint from user input (can be empty string)
"$ARGUMENTS"

## Process

### Step 1: Fetch and Merge from Origin/Main

#### 1.1: Fetch and Check State
```bash
git fetch origin
bash $HOME/.claude/scripts/git_branch_state.sh
```

Parse the JSON output. If `behind_main` is 0 and `diverged` is false, skip directly to Step 2 (no merge needed).

If `behind_main` > 0 or `diverged` is true, proceed with merge:

#### 1.2: Execute Merge
```bash
git merge origin/main
```

#### 1.3: Solve Conflicts (if any)
Git merge automatically:
- **Takes all non-conflicting changes from origin/main** (newer code, new files, etc.)
- **Only creates conflicts** where both branches modified the same lines

For conflicts, resolve by preferring current branch changes.

If conflicts occur:
- Resolve them systematically
- Stage the resolved files
- Continue with the commit process

#### 1.4: Merge Summary
After merge completes, provide brief summary:
- **What was merged**: Source branch and commit range
- **Files added/modified/deleted**: List key changes with file counts
- **Conflicts resolved**: Detail any conflicts encountered and how they were resolved
- **Merge result**: Success status

**Result**: Current branch now includes all commits from origin/main. The branch is either:
- **Equal** to origin/main (if no local commits existed)
- **Ahead** of origin/main (if local commits existed before merge)

This ensures we're never behind or diverged from origin/main.

### Step 2: Analyze Changes for Commit Message
Review staged/unstaged changes to understand:
- Type of change (add, fix, update, refactor)
- Scope and impact
- Key components modified
Do this using git diff. Stage all unstaged changes.

**Important**: If changes exist, committing them (Step 6) will make the current branch ahead of origin/main. If no changes exist, skip to Step 8 - we're already synced.

### Step 3: Check Plan Progress
If `plan_*.md` exists, review current phase status:
- Identify which phase is being completed
- Check if this represents a major milestone
- Note any phase transitions

### Step 4: Generate Professional Commit Message
Create structured commit message:

**Format**:
```
Brief description (50 chars max)

- Detailed bullet points of key changes
- Focus on WHY not just WHAT
- Reference phase completion if applicable
```

### Step 5: Update Plan Status (if applicable)
If `plan_*.md` exists and phase completed:
- Mark completed phase with ✓
- Update status documentation

### Step 6: Execute Commit
```bash
git commit -m "$(cat <<'EOF'
[Generated commit message]
EOF
)"
```

### Step 7: Push to Remote
Push changes to remote repository:
```bash
git push
```

If this is the first push and the branch doesn't exist on remote yet:
```bash
git push -u origin HEAD
```

**Result**: After pushing, the current branch remains ahead of (or equal to) origin/main with all changes safely on remote.

### Step 8: Verify Final State
```bash
bash $HOME/.claude/scripts/git_branch_state.sh
```

Parse the JSON output. Verify `behind_main` is 0 and `diverged` is false. If either check fails, report the issue to the user.

### Step 9: Confirmation
Report commit hash, push status, and summary to user.

**Final State**: ✓ Current branch >= origin/main (ahead or equal, never behind or diverged)
