---
name: finish
description: Use when the user indicates a session is ending, says 'done' or 'wrap up', asks for a summary of completed work, or wants handoff notes for the next session.
invocation: agent
---

# Finish

Produce a session summary covering completed work, verification status, git state, and outstanding items.

## Instructions

### Step 1: Gather Session State

Read from `.arc/config.json` if present:
- User preferences (worktree root, baseline, provider mode)

Read from `.arc/state.json` if present:
- Current tier and phase
- Active plan and spec paths
- Bead completion status

Read from `.arc/team-ledger.json` if present:
- Team member activity
- Task completion records

### Step 2: Check Git Status

```bash
git status --short
git log --oneline -5
git diff --stat
```

### Step 3: Check Verification Results

Look for recent verification output:
- Pre-verification results
- Post-verification results
- Any outstanding findings

### Step 4: Generate Summary

```
## Session Summary

### Completed Work
- [List of completed beads/tasks with status]

### Verification Status
- Pre-verify: [PASS/FAIL/NOT RUN]
- Post-verify: [PASS/FAIL/NOT RUN]
- Outstanding findings: [count]

### Git Status
- Branch: <current branch>
- Uncommitted changes: [count]
- Unpushed commits: [count]

### Outstanding Items
- [Items that remain incomplete]

### Handoff Notes
- [Context for the next session or developer]
- [Key decisions made and rationale]
- [Known issues or risks]
```

### Step 5: Cleanup Recommendation

If `.arc/state.json` shows completed workflow:
- Suggest `/arc:utility:reset` if beads state should be cleared
- Suggest committing outstanding changes
- Suggest pushing if commits are local-only
