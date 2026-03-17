---
description: Start task or begin project with lock acquisition and branch setup
triggers:
  - start task
  - begin task
  - start project
  - begin project
  - new task
---

# Start Task Skill

Use this skill when beginning any assigned task that involves modifying code.

## 🚨 Read Critical Guidelines First

**Before starting, read:** `claude/developer/guides/CRITICAL-BEFORE-CODE.md`

This checklist covers:
- Lock file verification and acquisition
- Branch creation best practices
- Agent usage requirements (never use direct commands)
- Using inav-architecture before searching

**Read it now using the Read tool, then proceed with the steps below.**

---

## Pre-Work Checklist

Before writing any code, complete ALL of these steps in order:

### 1. Identify the Repository

Determine which repo(s) your task requires:
- `inav/` - Firmware (C code)
- `inav-configurator/` - Configurator (JavaScript/Electron)

### 2. Check for Existing Lock

```bash
# For firmware work
cat claude/locks/inav.lock 2>/dev/null && echo "LOCKED - STOP" || echo "Available"

# For configurator work
cat claude/locks/inav-configurator.lock 2>/dev/null && echo "LOCKED - STOP" || echo "Available"
```

**If locked:** STOP. Report to manager that the repo is locked. Do not proceed.

### 3. Verify Clean Working Directory

```bash
# For firmware
cd inav && git status --porcelain

# For configurator
cd inav-configurator && git status --porcelain
```

**If output is not empty:** STOP. There are uncommitted changes. Either:
- Commit them if they belong to a previous task
- Stash them: `git stash`
- Or report to manager for guidance

### 4. Check Out the Correct Branch

Check if a branch is specified in the task assignment.

**If branch exists:**
```bash
git checkout <branch-name>
git pull origin <branch-name> 2>/dev/null || true  # Pull if remote exists
```

**If branch doesn't exist - CREATE FROM CORRECT BASE:**

⚠️ **CRITICAL:** You MUST specify the base branch when creating a new branch.

**See `.claude/skills/git-workflow/SKILL.md` for complete branching instructions.**

**Quick reference:**

```bash
# For INAV/inav-configurator (most common - maintains backward compatibility)
git checkout -b <new-branch-name> upstream/maintenance-9.x

# For PrivacyLRS
git checkout -b <new-branch-name> secure_01

# For INAV breaking changes (MSP protocol, settings structure, etc.)
git checkout -b <new-branch-name> upstream/maintenance-10.x
```

**❌ NEVER use `git checkout -b <branch-name>` without specifying base branch** - this creates the branch from your current HEAD, which may include unrelated changes.

**Branch naming conventions:**
- **PrivacyLRS:** No slashes (e.g., `fix-counter-sync`, `encryption-tests`)
- **INAV:** Kebab-case (e.g., `fix-telemetry-bug`, `feature-battery-limit`)

### 5. Acquire the Lock

```bash
# For firmware
cat > claude/locks/inav.lock << EOF
LOCKED_BY: Developer
TASK: <task-name-from-assignment>
LOCKED_AT: $(date '+%Y-%m-%d %H:%M')
BRANCH: <branch-name>
EOF

# For configurator
cat > claude/locks/inav-configurator.lock << EOF
LOCKED_BY: Developer
TASK: <task-name-from-assignment>
LOCKED_AT: $(date '+%Y-%m-%d %H:%M')
BRANCH: <branch-name>
EOF
```

### 6. Create Workspace Directory

Create a workspace directory for task-related files:

```bash
mkdir -p claude/developer/workspace/<task-name>
```

This is your scratch space for notes, test scripts, and data. See `claude/developer/INDEX.md` for what goes here vs. in `claude/projects/`.

### 7. Confirm Ready

Verify:
```bash
# Show lock contents
cat claude/locks/*.lock 2>/dev/null

# Show current branch
git branch --show-current

# Confirm clean
git status --porcelain
```

## Now Begin Work

Only after completing ALL steps above should you begin implementing the task.

## Example: Starting a Configurator Task

```bash
# 1. Check lock
cat claude/locks/inav-configurator.lock 2>/dev/null || echo "Available"

# 2. Check clean
cd inav-configurator
git status --porcelain

# 3. Checkout branch (existing)
git checkout transpiler_clean_copy

# 4. Acquire lock
cat > claude/locks/inav-configurator.lock << EOF
LOCKED_BY: Developer
TASK: fix-decompiler-condition-numbers
LOCKED_AT: $(date '+%Y-%m-%d %H:%M')
BRANCH: transpiler_clean_copy
EOF

# 5. Create workspace
mkdir -p claude/developer/workspace/fix-decompiler-condition-numbers

# 6. Ready to work!
```

## When Task is Complete

Remember to release the lock:
```bash
rm claude/locks/inav.lock
# or
rm claude/locks/inav-configurator.lock
```

Include in your completion report: "Released <repo>.lock"

---

## For Managers: Creating a New Project

When creating a new project to assign to a developer:

### 1. Create Project Directory

```bash
mkdir -p claude/projects/active/<project-name>
```

### 2. Create Project Files

- `summary.md` - Project overview, objectives, approach (use template from `claude/projects/README.md`)
- `todo.md` - Task breakdown (use template from `claude/projects/README.md`)

### 3. Add to INDEX.md

Add concise entry (10-15 lines max):
- Status, type, priority, dates
- One-sentence summary
- Directory: `active/<project-name>/`
- Assignment email path

### 4. Send Assignment Email

Create in `claude/manager/email/sent/` and copy to `claude/developer/email/inbox/`

---

## Related Skills

- **finish-task** - Complete tasks and release locks
- **git-workflow** - Create branches and manage git state
- **create-pr** - Create pull request after completing task
