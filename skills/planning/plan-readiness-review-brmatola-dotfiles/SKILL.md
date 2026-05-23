---
name: plan-readiness-review
description: Use when you have a plan and want to verify it's ready for implementation - catches structural gaps, feasibility issues, and scope problems
---

# Plan Readiness Review

## Overview

Pressure test whether a plan is ready for implementation. Catches structural gaps, feasibility issues, and scope problems before committing to build.

**Core principle:** Find problems before implementation, not during.

**Announce at start:** "I'm using the plan-readiness-review skill to evaluate this plan."

**Plan location:** `plans/active/{plan-name}/`

## The Process

### Step 1: Load Plan

1. Read all files from `plans/active/{plan-name}/design/`
2. Read all files from `plans/active/{plan-name}/implementation/` (if exists)
3. Note: Plan must be committed to repo before worktree creation

### Step 2: Evaluate Against Criteria

**Structure:**
- [ ] All required sections present (problem, solution, tasks)?
- [ ] Steps specific enough to execute without interpretation?
- [ ] Success criteria defined?
- [ ] Dependencies between tasks identified?

**Feasibility:**
- [ ] Technical approach sound?
- [ ] Required APIs/libraries exist?
- [ ] No impossible constraints?

**Scope:**
- [ ] Right-sized for one branch?
- [ ] Should it be split into multiple plans?
- [ ] Over-engineered for the problem?
- [ ] Missing obvious requirements?

**Clarity:**
- [ ] Would a fresh agent understand every instruction?
- [ ] Any ambiguous instructions?
- [ ] Missing context that implementer would need?

### Step 3: Cross-Reference Codebase

Check if plan accounts for:
- Existing patterns in the codebase
- Files that will be affected
- Test patterns to follow
- Related code that might need updates

### Step 4: Produce Verdict

Output this format:

```
## Plan Readiness Review: {plan-name}

### Verdict: READY | NEEDS WORK | SPLIT RECOMMENDED

### Strengths
- [What's solid about this plan]

### Issues Found
- **[Category]**: [Issue description]
  - Suggested fix: [How to address]

### Questions to Resolve
- [Anything ambiguous that needs human input]

### Recommendation
[1-2 sentence summary of what to do next]
```

## Verdict Meanings

| Verdict | Meaning | Next Step |
|---------|---------|-----------|
| **READY** | Plan is executable as-is | Proceed to implementation |
| **NEEDS WORK** | Fixable issues found | Address issues, re-review |
| **SPLIT RECOMMENDED** | Too large for one branch | Create multiple plans |

## Red Flags

**Never:**
- Rubber-stamp a plan without thorough review
- Skip codebase cross-reference
- Approve plans with ambiguous instructions

**Always:**
- Check every evaluation criterion
- Verify file paths exist or make sense
- Flag anything a fresh agent might misinterpret

## Integration

**Invoked by:**
- **gremlins:worktree-workflow** (start phase) - First gate in workflow
- Standalone when reviewing any plan

**Pairs with:**
- **gremlins:writing-plans** - Reviews output of that skill
- **gremlins:executing-plans** - Feeds into that skill when READY
