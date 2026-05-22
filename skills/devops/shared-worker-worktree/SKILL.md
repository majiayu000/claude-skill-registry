---
name: shared-worker-worktree
description: Git worktree setup and management for parallel agent development. Use proactively when setting up parallel development between Developer and Tech Artist agents, or when navigating between worktree and master branches.
category: infrastructure
tags: [git, worktree, parallel, coordination]
dependencies: [shared-ralph-core, shared-file-permissions]
---

# Worker Worktree

> "Parallel development without conflicts – each agent works in their own worktree."

## When to Use This Skill

Use **when**:
- Setting up parallel development (Developer + Tech Artist)
- Navigating between worktree and master branches
- Merging changes after QA validation
- Resolving worktree conflicts

Use **proactively**:
- Before starting any work in your worktree
- When merging main branch changes
- Before committing worktree changes

---

## Quick Start

<examples>
Example 1: Initial worktree setup
```bash
# Check if worktree exists
git worktree list

# Create if not exists
git worktree add ../developer-worktree -b developer-worktree

# Navigate and start
cd ../developer-worktree
```

Example 2: Daily workflow
```bash
# Navigate to worktree
cd ../developer-worktree

# Merge latest from main
git fetch origin main
git merge origin/main

# Work happens here...
# ...

# Commit and push
git commit -m "feat: my changes"
git push origin developer-worktree
```

Example 3: QA merge after validation passes
```bash
# QA (on main branch):
git checkout main
git fetch origin developer-worktree
git merge origin/developer-worktree
git push origin main
```
</examples>

---

## Worktree Convention

**MUST follow:** `{agent}-worktree`

| Agent | Worktree Path | Branch Name |
|-------|---------------|------------|
| Developer | `../developer-worktree` | `developer-worktree` |
| Tech Artist | `../techartist-worktree` | `techartist-worktree` |
| QA | Uses main worktree | `main` |

---

## Daily Workflow

### Before Starting Work

```bash
# 1. Navigate to your worktree
cd ../{agent}-worktree

# 2. Merge latest from main
git fetch origin main
git merge origin/main

# 3. Resolve conflicts if any
git status

# 4. Start working
```

### After Committing

```bash
# Push to worktree branch
git push origin {agent}-worktree
```

---

## QA Merge Protocol

**QA Agent ONLY:**

### When Validation PASSES

```bash
# 1. Switch to main
git checkout main

# 2. Fetch and merge
git fetch origin {agent}-worktree
git merge origin/{agent}-worktree

# 3. Push merged
git push origin main
```

### When Validation Fails

```bash
# DO NOT MERGE
# Send bug report to agent
# Agent fixes in their worktree
```

---

## Master Branch Coordination (CRITICAL)

**THE GOLDEN RULE:** Worktrees are for CODE/ASSETS ONLY. All coordination happens in master.

| Operation | Location | Why |
|-----------|----------|-----|
| PRD updates | Master branch | PM needs to see status immediately |
| Messages | Master branch | Watchdog only watches master |
| Heartbeat | Master branch | Watchdog monitors master PRD |
| Code commits | Worktree branch | Isolated development, QA validates |

---

## File Conflict Prevention

| Developer Works In | Tech Artist Works In |
|-------------------|----------------------|
| `src/components/` (logic) | `src/components/` (materials only) |
| `src/hooks/` | `src/assets/` |
| `src/stores/` | `src/styles/` |
| `src/server/` | `src/vfx/` |
| `src/utils/` | `public/textures/` |
| Test files | Visual test files |

**If both need same file:** PM assigns sequentially, not parallel.

---

## Best Practices

✅ **DO:**
- Always merge main before starting work
- Commit frequently in your worktree
- Push worktree branch after each commit
- Resolve merge conflicts promptly

❌ **DON'T:**
- Create worktree if one already exists
- Work in main directory (use your worktree)
- Merge to main yourself (QA does this after validation)
- Delete worktree without QA approval

---

## Quick Reference Commands

| Action | Command |
|--------|----------|
| List worktrees | `git worktree list` |
| Create worktree | `git worktree add ../{agent}-worktree -b {agent}-worktree` |
| Remove worktree | `git worktree remove ../{agent}-worktree` |
| Navigate to worktree | `cd ../{agent}-worktree` |
| Merge main | `git fetch origin main && git merge origin/main` |
| Push worktree | `git push origin {agent}-worktree` |
| Check current branch | `git branch --show-current` |

---

## Troubleshooting

### Worktree Already Exists

```bash
git worktree list
# If listed, just navigate:
cd ../{agent}-worktree
```

### Merge Conflicts

```bash
cd ../{agent}-worktree
git fetch origin main
git merge origin/main
# Resolve conflicts, then:
git add .
git commit -m "Merge main into {agent}-worktree"
```

### Worktree Path Issues

```bash
# Remove and recreate
git worktree remove ../{agent}-worktree
git worktree add ../{agent}-worktree -b {agent}-worktree
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-core` | Session structure, status values |
| `shared-file-permissions` | Permissions matrix |
| `shared-atomic-updates` | File update atomicity |
