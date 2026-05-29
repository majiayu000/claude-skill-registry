---
name: understanding-cross-phase-stacking
description: Use before starting any new phase - explains how sequential and parallel phases automatically chain together through base branch inheritance (main worktree tracks progress, parallel phases inherit from current branch, no manual intervention needed)
---

# Understanding Cross-Phase Stacking

## Overview

**Phases automatically build on each other's completed work.** Understanding how phases chain together is essential for correct execution.

This is a **reference skill** - read it to understand cross-phase dependencies, not to execute a workflow.

## When to Use

Use this skill when:
- Starting a new phase (need to understand what base to build from)
- Debugging stack relationships across phase boundaries
- Verifying phases are chaining correctly
- Understanding why parallel worktrees use specific base branches

**Mental model check:** If you're thinking "create worktrees from `{runid}-main` branch", you need this skill.

## The Cross-Phase Inheritance Principle

```
MAIN WORKTREE CURRENT BRANCH = LATEST COMPLETED WORK
```

**Key insight:**
- Sequential phases leave main worktree **on their last task's branch**
- Parallel phases leave main worktree **on their last stacked branch**
- Next phase (sequential or parallel) inherits from **current branch**, not original base

**This creates automatic linear chaining across all phases.**

## Example: Sequential → Parallel → Sequential

### Phase 1 (Sequential) - Database Setup

```bash
# Working in: .worktrees/{runid}-main
# Starting from: {runid}-main (base branch)

# Task 1: Database schema
gs branch create {runid}-task-1-1-database-schema
# Creates branch, commits work
# Main worktree now on: {runid}-task-1-1-database-schema ← KEY STATE
```

**Phase 1 result:**
- Branch created: `{runid}-task-1-1-database-schema`
- Main worktree current branch: `{runid}-task-1-1-database-schema`
- **This branch becomes Phase 2's base**

### Phase 2 (Parallel) - Three Feature Implementations

```bash
# Base detection (CRITICAL):
BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
# Returns: {runid}-task-1-1-database-schema ← Inherits from Phase 1

# Create parallel worktrees FROM Phase 1's completed branch
git worktree add .worktrees/{runid}-task-2-1 --detach "$BASE_BRANCH"
git worktree add .worktrees/{runid}-task-2-2 --detach "$BASE_BRANCH"
git worktree add .worktrees/{runid}-task-2-3 --detach "$BASE_BRANCH"

# All 3 parallel tasks build on Phase 1's database schema
```

**After parallel tasks complete and stack:**

```bash
# In main worktree (.worktrees/{runid}-main):
# Branch 1: {runid}-task-2-1-user-service → tracked
# Branch 2: {runid}-task-2-2-product-service → tracked, upstacked onto Branch 1
# Branch 3: {runid}-task-2-3-order-service → tracked, upstacked onto Branch 2

# Main worktree now on: {runid}-task-2-3-order-service ← KEY STATE
```

**Phase 2 result:**
- Linear stack: database-schema → user-service → product-service → order-service
- Main worktree current branch: `{runid}-task-2-3-order-service`
- **This branch becomes Phase 3's base**

### Phase 3 (Sequential) - Integration Tests

```bash
# Working in: .worktrees/{runid}-main (reused from Phase 1)
# Current branch: {runid}-task-2-3-order-service (from Phase 2)

# Task 1: Integration tests
gs branch create {runid}-task-3-1-integration-tests
# Automatically stacks on Phase 2's last task via natural stacking
```

**Phase 3 result:**
- Linear chain: Phase 1 → Phase 2 tasks → Phase 3
- Complete stack shows all work in order

## Verification Between Phases

**Before starting parallel phase (check inheritance):**

```bash
# Verify base branch before creating worktrees
BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
echo "Starting parallel phase from: $BASE_BRANCH"
# Should show previous phase's completed branch, NOT {runid}-main
```

**Before starting sequential phase (check current state):**

```bash
# Verify starting point
CURRENT_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
echo "Starting sequential phase from: $CURRENT_BRANCH"
# Should show previous phase's last stacked branch
```

**After phase completes (verify stack):**

```bash
cd .worktrees/{runid}-main
gs log short
# Should show linear chain including all previous phases
```

## Key Principles

1. **Main worktree tracks progress**
   - Current branch = latest completed work
   - Not static - changes as phases complete

2. **Parallel phases inherit from current**
   - Use `git -C .worktrees/{runid}-main branch --show-current` as base
   - NOT `{runid}-main` (that's the original starting point)

3. **Parallel stacking preserves continuity**
   - Last stacked branch becomes next phase's base
   - Checkout last branch after stacking completes

4. **Sequential phases extend naturally**
   - `gs branch create` stacks on current HEAD
   - No manual base specification needed

5. **No manual intervention needed**
   - Cross-phase chaining is automatic
   - Following per-phase patterns creates correct chain

## Common Mistake: Creating From Wrong Base

### ❌ Wrong: Creating parallel worktrees from original base

```bash
# DON'T DO THIS:
git worktree add .worktrees/{runid}-task-2-1 --detach {runid}-main
```

**Why wrong:** Ignores Phase 1's completed work. Phase 2 won't have database schema from Phase 1.

**Result:** Broken dependency chain. Phase 2 builds on stale base instead of Phase 1's changes.

### ✅ Correct: Creating parallel worktrees from current branch

```bash
# DO THIS:
BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
git worktree add .worktrees/{runid}-task-2-1 --detach "$BASE_BRANCH"
```

**Why correct:** Inherits all previous work. Phase 2 builds on Phase 1's completed branch.

**Result:** Linear chain across all phases.

## Mental Model Check

**If you're thinking:**
- "Create worktrees from `{runid}-main`" → WRONG. Use current branch.
- "Parallel tasks should start fresh" → WRONG. They inherit previous work.
- "Phase boundaries break the stack" → WRONG. Stack is continuous across phases.

**Correct mental model:**
- Main worktree is a **moving cursor** pointing to latest work
- Each phase **extends** the cursor position, doesn't reset it
- Stack is **one continuous chain**, not per-phase segments

## Quick Reference

**Starting parallel phase:**
```bash
BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
# Use $BASE_BRANCH for all worktree creation
```

**Starting sequential phase:**
```bash
# Already on correct branch - just create next branch
gs branch create {runid}-task-{phase}-{task}-{name}
# Automatically stacks on current HEAD
```

**Verifying cross-phase chain:**
```bash
cd .worktrees/{runid}-main
gs log short
# Should show linear progression through all phases
```

## The Bottom Line

**Phases chain automatically through main worktree's current branch.**

If you're manually specifying base branches or creating worktrees from `{runid}-main`, you're breaking the automatic inheritance system.

Trust the pattern: main worktree tracks progress, new phases build from current state.
