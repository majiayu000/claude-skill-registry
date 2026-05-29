---
name: plan-archive
description: Use when a plan is abandoned, obsolete, or superseded and should be archived
---

# Plan Archive

## Overview

Move an abandoned or obsolete plan to `archive/` with context on why it was archived.

**Core principle:** Don't delete plans - archive them with context so you can learn from them later.

**Announce at start:** "I'm using the plan-archive skill to archive this plan."

## The Process

### Step 1: Confirm Archive Intent

Ask: "Why is this plan being archived?"

Options:
- **Abandoned** - Started but won't be finished
- **Obsolete** - Requirements changed, no longer relevant
- **Superseded** - Replaced by a different plan
- **Other** - Capture the reason

### Step 2: Add Archive Notes

Create `plans/{active|complete}/{plan-name}/archive.md`:

```markdown
# Archive Notes

**Archived:** YYYY-MM-DD

**Reason:** [abandoned|obsolete|superseded|other]

**Context:** [Why this plan is being archived]

**Superseded by:** [Link to new plan if applicable]

**Partial work:**
- [Any commits/PRs that were done before archiving]

**Lessons learned:**
- [What can we learn from this?]
```

### Step 3: Move to Archive

```bash
# Move from active or complete
mv plans/active/{plan-name} plans/archive/{plan-name}
# OR
mv plans/complete/{plan-name} plans/archive/{plan-name}

# Commit the move
git add -A
git commit -m "docs: archive {plan-name} plan - {reason}"
```

### Step 4: Report

```
Plan '{plan-name}' archived.

Reason: {reason}
Location: plans/archive/{plan-name}/
```

## Quick Reference

| Source | Typical Reason |
|--------|----------------|
| `active/` | Abandoned, obsolete, superseded |
| `complete/` | Superseded by better approach, historical cleanup |

## When to Use

- Plan started but won't be finished
- Requirements changed significantly
- Better approach found (new plan created)
- Cleaning up old completed plans that are no longer relevant

## Common Mistakes

**Archiving without context**
- **Problem:** No record of why plan was abandoned
- **Fix:** Always capture the reason in archive.md

**Deleting instead of archiving**
- **Problem:** Lose historical context and learnings
- **Fix:** Archive preserves history for future reference
