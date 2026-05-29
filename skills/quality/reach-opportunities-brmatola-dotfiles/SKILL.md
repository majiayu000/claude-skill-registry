---
name: reach-opportunities
description: Use after implementation passes review to identify low-hanging enhancements - quick wins only, not scope creep
---

# Reach Opportunities

## Overview

Identify low-hanging enhancements aligned with the plan's goals. Quick wins only, not scope creep.

**Core principle:** Opportunistic polish while context is fresh.

**Announce at start:** "I'm using the reach-opportunities skill to identify potential quick wins."

**Plan location:** `plans/active/{plan-name}/`

## The Process

### Step 1: Load Context

1. Read original plan from `plans/active/{plan-name}/`
2. Understand the goals and scope
3. Review what was implemented (git diff from base)

```bash
git diff --stat $(git merge-base HEAD main)..HEAD
```

### Step 2: Identify Opportunities

Look for these categories:

| Category | What to Look For |
|----------|------------------|
| **Adjacent improvements** | Related functionality that complements what was built |
| **Obvious gaps** | Edge cases or error paths not covered |
| **Polish** | Loading states, better messages, UX improvements |
| **Documentation** | Patterns worth capturing in CLAUDE.md |
| **Test coverage** | Edge cases worth testing while context is fresh |

### Step 3: Evaluate Complexity

Rate each opportunity:

| Tier | Meaning | Scope |
|------|---------|-------|
| **trivial** | Few lines of code | Single function change |
| **small** | Single file change | One component/module |
| **medium** | Multiple files, bounded | Clear scope, no cascading changes |
| **too big** | Spin off to new plan | Needs own design phase |

### Step 4: Apply Constraints

Each opportunity MUST:
- Relate to the plan's original goals (no random tangents)
- Be trivial, small, or medium complexity
- Not introduce new dependencies
- Not require design decisions

If bigger → recommend spinning off to new plan.

### Step 5: Produce Output

```
## Reach Opportunities: {plan-name}

### Context
[Brief summary of what was built and why these opportunities exist]

### Opportunities Found

#### 1. [Opportunity Name]
- **Complexity:** trivial | small | medium
- **Value:** [Why it's worth doing]
- **Implementation:** [Brief description of what to do]

#### 2. [Opportunity Name]
- **Complexity:** trivial | small | medium
- **Value:** [Why it's worth doing]
- **Implementation:** [Brief description of what to do]

#### 3. [Too Big - Spin Off]
- **Why it's related:** [Connection to plan goals]
- **Why spin off:** [What makes it too complex]
- **Suggested plan name:** `{new-plan-name}`

### Recommendation
[Which to tackle now vs defer. Usually: do trivial ones, consider small ones, defer medium unless high value.]
```

## Complexity Examples

**Trivial:**
- Add a missing error message
- Add a null check
- Fix a typo in output
- Add a log statement

**Small:**
- Add input validation to a function
- Add a new test case
- Improve an error message with more context
- Add a keyboard shortcut

**Medium:**
- Add a new related function with tests
- Refactor for consistency across 2-3 files
- Add a configuration option
- Improve error handling across a module

**Too Big (Spin Off):**
- Add a new feature area
- Significant refactoring
- Changes requiring design decisions
- Anything with unclear scope

## Red Flags

**Never:**
- Suggest unrelated improvements
- Recommend anything that needs design work
- Let "while we're here" thinking cause scope creep
- Include anything that might break existing functionality

**Always:**
- Tie opportunities to plan goals
- Be honest about complexity
- Recommend spinning off bigger ideas
- Present as opt-in, not obligations

## Integration

**Invoked by:**
- **gremlins:worktree-workflow** (reach phase) - Opt-in after audit passes
- Standalone after any implementation

**Follows:**
- **gremlins:implementation-review** - Only run after audit passes

**Leads to:**
- Back to **gremlins:implementation-review** - After implementing selected items
- **gremlins:finishing-a-development-branch** - When declining all opportunities
