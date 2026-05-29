---
name: dev-design
description: This skill should be used when the user asks to "propose architecture", "design implementation approach", "choose between approaches", or in Phase 4 of /dev workflow after exploration is complete. Proposes 2-3 architecture approaches with clear trade-offs, decomposes features into independent tasks, and obtains explicit user approval before implementation begins.
version: 0.1.0
---

**Announce:** "Using dev-design (Phase 4) to propose implementation approaches and obtain user approval."

## Contents

- [The Iron Law of Design](#the-iron-law-of-design)
- [What Design Does](#what-design-does)
- [Process](#process)
- [Approach Categories](#approach-categories)
- [PLAN.md Format](#planmd-format)
- [Red Flags](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Architecture Design with User Gate

Propose implementation approaches, explain trade-offs, get user approval.
**Prerequisites:** SPEC.md finalized, exploration complete, clarifications resolved.

<EXTREMELY-IMPORTANT>
## The Iron Law of Design

**YOU MUST GET USER APPROVAL BEFORE IMPLEMENTATION. This is not negotiable.**

After presenting approaches:
1. Show 2-3 options with trade-offs
2. Lead with your recommendation
3. **Ask user which approach**
4. **Wait for explicit approval**

Implementation CANNOT start without user saying "Yes" or choosing an approach.

**STOP - you're about to implement without user approval.**
</EXTREMELY-IMPORTANT>

## What Design Does

| DO | DON'T |
|----|-------|
| Propose 2-3 approaches | Implement anything |
| Explain trade-offs clearly | Make the choice for user |
| Lead with recommendation | Present without opinion |
| Get explicit approval | Assume approval |
| Write PLAN.md | Skip the user gate |

**Design answers: HOW to build it and WHY this approach**
**Implement executes: the approved approach** (next phase, after gate)

## Process

### 1. Review Inputs

Before designing, ensure the following exist:
- `.claude/SPEC.md` - final requirements
- Exploration findings - key files, patterns
- Clarified decisions - edge cases, integrations

### 2. Propose 2-3 Approaches

Each approach should address the same requirements differently:

**Approach A: Minimal Changes**
- Smallest diff, maximum reuse
- Trade-off: May be less clean, tech debt

**Approach B: Clean Architecture**
- Best patterns, maintainability
- Trade-off: More changes, longer implementation

**Approach C: Pragmatic Balance**
- Balance of speed and quality
- Trade-off: Compromise on both

### 3. Present with Trade-offs

Use the AskUserQuestion tool to present approaches:

```python
# AskUserQuestion: Present 2-3 architecture approaches with trade-offs for user selection
AskUserQuestion(questions=[{
  "question": "Which architecture approach should we use?",
  "header": "Architecture",
  "options": [
    {
      "label": "Pragmatic Balance (Recommended)",
      "description": "Extend existing AuthService with new method. ~150 lines changed. Balances reuse with clean separation."
    },
    {
      "label": "Minimal Changes",
      "description": "Add logic to existing endpoint. ~50 lines changed. Fast but increases coupling."
    },
    {
      "label": "Clean Architecture",
      "description": "New service with full abstraction. ~300 lines. Most maintainable but longest to build."
    }
  ],
  "multiSelect": false
}])
```

**Key principles:**
- Lead with recommendation (first option + "Recommended")
- Concrete numbers (lines changed, files affected)
- Clear trade-offs for each
- Reference specific files from exploration

### 4. Feature Decomposition Check

**CRITICAL:** Before writing PLAN.md, check if this is actually multiple features.

Review the scope and ask:

```python
# AskUserQuestion: Determine if feature should be split into independent tasks
AskUserQuestion(questions=[{
  "question": "Is this one cohesive feature or multiple independent features?",
  "header": "Scope",
  "options": [
    {
      "label": "One feature",
      "description": "Implement everything together in one branch/worktree"
    },
    {
      "label": "Multiple features",
      "description": "Break into separate features, each with own branch/worktree/PR"
    }
  ],
  "multiSelect": false
}])
```

**If "Multiple features":**

1. **List the independent features** identified from SPEC.md:
   ```
   Based on the requirements, this breaks into:
   1. Theme infrastructure (color system, theme provider)
   2. Settings UI (theme selector component)
   3. Component updates (update 20+ components to use theme)
   4. Persistence layer (save user preference)

   Each can be implemented and PR'd independently.
   ```

2. **Ask which to tackle first:**
   ```python
   # AskUserQuestion: Prioritize which feature to implement first
   AskUserQuestion(questions=[{
     "question": "Which feature should we implement first?",
     "header": "Priority",
     "options": [
       {"label": "Theme infrastructure (Recommended)", "description": "Foundation that others depend on"},
       {"label": "Settings UI", "description": "UI for theme selection"},
       {"label": "Component updates", "description": "Apply themes to components"},
       {"label": "Persistence layer", "description": "Save user preference"}
     ],
     "multiSelect": false
   }])
   ```

3. **Write PLAN.md for ONLY the chosen feature**

4. **Document remaining features** in `.claude/BACKLOG.md`:
   ```markdown
   # Feature Backlog

   ## Dark Mode Implementation

   ### Completed
   - [ ] None yet

   ### Next Up
   - [ ] Theme infrastructure
   - [ ] Settings UI
   - [ ] Component updates
   - [ ] Persistence layer

   **Current Focus:** Theme infrastructure
   ```

**If "One feature":**

Proceed to write PLAN.md for the entire scope (step 5 below).

**Why this matters:**

- Multiple features in one branch = massive PR, review hell, merge conflicts
- Separate features = clean PRs, incremental progress, easier reviews
- After first feature PR merges, come back and tackle next feature

### 5. Write PLAN.md

After user chooses approach AND confirms scope, write `.claude/PLAN.md`:

```markdown
# Implementation Plan: [Feature]

> **For Claude:** REQUIRED SUB-SKILL: Invoke `Skill(skill="workflows:dev-implement")` to implement this plan.
>
> **Per-Task Ralph Loops:** Assign each task its OWN ralph loop. Do NOT combine multiple tasks into one loop.
>
> **Delegation:** Main chat orchestrates, Task agents implement. Use `Skill(skill="workflows:dev-delegate")` for subagent templates.

## Chosen Approach
[Name]: [Brief description]

## Rationale
- [Why this approach fits]
- [Trade-offs accepted]

## Files to Modify
| File | Change |
|------|--------|
| `src/auth/service.ts` | Add `validateSession()` method |
| `src/routes/api.ts` | Add new endpoint |

## New Files
| File | Purpose |
|------|---------|
| `src/auth/types.ts` | Session type definitions |

## Implementation Order (with Per-Task Ralph Loops)

> **For Claude:** Each task = one ralph loop. Complete task N before starting task N+1.
>
> Pattern: `Skill(skill="ralph-loop:ralph-loop", args="Task N: [name] --max-iterations 10 --completion-promise TASKN_DONE")`

| Task | Ralph Loop | Core Test (MUST EXECUTE CODE) | Verify Command |
|------|------------|-------------------------------|----------------|
| 1. Add types | `"Task 1: Add types" → TASK1_DONE` | N/A (types only) | `tsc --noEmit` |
| 2. Service method | `"Task 2: Service method" → TASK2_DONE` | `test_validate_session()` calls method, checks return | `pytest tests/test_auth.py -v` |
| 3. Route handler | `"Task 3: Route handler" → TASK3_DONE` | Integration test hits endpoint, checks response | `pytest tests/test_api.py -v` |

### What Counts as a REAL Test

| ✅ REAL (execute + verify) | ❌ NOT A TEST (never do this) |
|----------------------------|-------------------------------|
| pytest calls function | grep for function exists |
| Playwright clicks button | ast-grep finds pattern |
| API request checks response | Log says "success" |
| Screenshot comparison | "Code looks correct" |

**Every task MUST have a test that EXECUTES the code and VERIFIES behavior.**
```

### 6. User Gate - Final Approval

After writing PLAN.md, get explicit approval:

```
AskUserQuestion(questions=[{
  "question": "Ready to start implementation?",
  "header": "Approval",
  "options": [
    {"label": "Yes, proceed", "description": "Start implementation with TDD"},
    {"label": "No, discuss changes", "description": "Modify the plan first"}
  ],
  "multiSelect": false
}])
```

**If "No":** Wait for user feedback, modify plan, ask again.

**If "Yes":** Proceed to workspace setup question in Step 7 below.

### 7. Workspace Setup Question

After user approves implementation, ask about worktree isolation:

```
AskUserQuestion(questions=[{
  "question": "Create isolated worktree for this feature?",
  "header": "Workspace",
  "options": [
    {"label": "Yes (Recommended)", "description": "Work in isolated .worktrees/ directory - keeps main workspace clean"},
    {"label": "No", "description": "Work in current directory"}
  ],
  "multiSelect": false
}])
```

**If "Yes (Recommended)":**

Invoke the dev-worktree skill:
```bash
# dev-worktree: Create isolated git worktree for feature development
Skill(skill="workflows:dev-worktree")
```

Then after worktree is created, invoke dev-implement.

**If "No":**

Directly invoke dev-implement in current directory without worktree isolation.

## Approach Categories

| Category | When to Use | Trade-off |
|----------|-------------|-----------|
| Minimal | Bug fixes, small features | Speed vs cleanliness |
| Clean | New systems, core features | Quality vs time |
| Pragmatic | Most features | Balance |

## PLAN.md Format

Required sections:
- **Chosen Approach** - What was selected and why
- **Files to Modify** - Specific paths with change descriptions
- **New Files** - If any, with purposes
- **Implementation Order** - Ordered task list with dependencies
- **Testing Strategy** - How to verify

## The Gate Function

Complete all steps before starting implementation:

```
1. REVIEW → Read SPEC.md and exploration findings
2. PROPOSE → Present 2-3 approaches with trade-offs
3. ASK → Use AskUserQuestion with clear options
4. DECOMPOSE → Ask "One feature or multiple?" (CRITICAL)
   └─ If multiple → List features, ask which first, write BACKLOG.md
5. WAIT → Do NOT proceed until user responds
6. DOCUMENT → Write chosen approach to PLAN.md (for chosen feature only if decomposed)
7. CONFIRM → Ask "Ready to proceed?"
8. WORKSPACE → Ask "Create worktree?" (Yes recommended / No)
9. SETUP → If worktree Yes, invoke dev-worktree
10. GATE → Only start /dev-implement after all approvals
```

**Mandatory steps (NEVER skip):** DECOMPOSE, WAIT, WORKSPACE, and GATE.

## Rationalization Prevention

Recognize these thoughts as red flags—they signal attempts to bypass the user gate:

| Thought | Reality |
|---------|---------|
| "User will approve this" | Your assumption ≠ approval. Ask and wait. |
| "It's the obvious choice" | User decides what's obvious. Present options. |
| "Let me just start" | NO. Gate exists for a reason. Wait. |
| "User said they trust me" | Trust doesn't mean skip approval. Ask. |
| "Time pressure" | You'll waste more time with the wrong approach. Wait for approval. |
| "Only one viable option" | Present it anyway. User may see alternatives. |
| "Ask forgiveness later" | No. Ask permission now. |

## Red Flags - STOP If You're About To:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Present only one approach | You're removing user choice | Always show 2-3 options |
| Skip trade-offs | You're making decision for user | Explain pros/cons clearly |
| Start implementing | You don't have approval yet | Wait for explicit "Yes" |
| Assume recommendation accepted | You're guessing at user preference | Ask and wait for answer |

## Output

Design complete when:
- 2-3 approaches presented with trade-offs
- User chose an approach
- `.claude/PLAN.md` written with chosen approach
- **User explicitly approved** ("Yes, proceed")

## Phase Complete

**After user approves ("Yes, proceed"):**

1. **Ask about worktree** (Step 7 above)
2. **If worktree chosen:**
   - Invoke `Skill(skill="workflows:dev-worktree")`
   - After worktree created, invoke `Skill(skill="workflows:dev-implement")`
3. **If no worktree:**
   - Directly invoke `Skill(skill="workflows:dev-implement")`

**Required before proceeding:**
- Explicit user approval for implementation
- Feature scope decision (one feature vs multiple)
- User choice on worktree (Yes/No)

**After this feature is implemented and PR'd:**

If multiple features were identified in step 4, check `.claude/BACKLOG.md` for remaining features:
1. View remaining features in BACKLOG.md
2. Invoke `/dev` again to tackle the next feature
3. Repeat until all features are complete

This enables incremental development: one feature → PR → merge → next feature.
