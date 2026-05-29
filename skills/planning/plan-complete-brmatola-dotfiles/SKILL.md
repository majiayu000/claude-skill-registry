---
name: plan-complete
description: Use when a plan's implementation is finished and all work has been merged or shipped
---

# Plan Complete

## Overview

Move a completed plan from `active/` to `complete/` and capture completion context.

**Core principle:** Plans that are done should be marked done, with context on what was accomplished.

**Announce at start:** "I'm using the plan-complete skill to mark this plan as complete."

## The Process

### Step 1: Verify Completion

Before marking complete, verify:

```bash
# Check plan exists in active
ls plans/active/{plan-name}/

# Verify no outstanding work
git status
```

**Ask:** "Is all work from this plan merged/shipped? Any outstanding items?"

If work remains, don't proceed. Help finish the work first.

### Step 2: Add Completion Notes (Optional)

If the user wants to capture completion context:

Create `plans/active/{plan-name}/completion.md`:

```markdown
# Completion Notes

**Completed:** YYYY-MM-DD

**Summary:** [1-2 sentences on what was accomplished]

**Key commits/PRs:**
- [commit/PR references]

**Deviations from plan:**
- [Any significant changes from original design]

**Lessons learned:**
- [Optional: anything worth remembering]
```

### Step 3: Move to Complete

```bash
# Move the entire plan directory
mv plans/active/{plan-name} plans/complete/{plan-name}

# Commit the move
git add -A
git commit -m "docs: mark {plan-name} plan as complete"
```

### Step 4: Report

```
Plan '{plan-name}' marked complete.

Location: plans/complete/{plan-name}/
```

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Verify all work is done |
| 2 | Add completion notes (optional) |
| 3 | Move to `plans/complete/` |
| 4 | Commit and report |

## When NOT to Use

- Work is still in progress
- Plan was abandoned (use `gremlins:plan-archive` instead)
- Plan is obsolete or superseded (use `gremlins:plan-archive` instead)

## Common Mistakes

**Moving incomplete plans**
- **Problem:** Plan marked complete but work isn't done
- **Fix:** Always verify with user before moving

**Skipping completion notes**
- **Problem:** Context lost about what was accomplished
- **Fix:** At minimum capture completion date and summary
