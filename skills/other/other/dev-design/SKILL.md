---
name: dev-design
description: "Propose architecture, design implementation approach, or choose between approaches."
user-invocable: false
disable-model-invocation: true
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

## Prerequisite: dev-clarify Must Be Complete

**dev-design REQUIRES dev-clarify to be complete. This is not optional.**

Before writing PLAN.md, verify these clarify gates passed:
- [ ] Testing approach documented (unit/integration/E2E)
- [ ] Test framework specified
- [ ] First test described
- [ ] Test command documented
- [ ] User workflow confirmed

**If ANY gate is unchecked → DO NOT START DESIGN. Return to dev-clarify.**

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

### Drive-Aligned Framing

**Proposing an architecture without reading the codebase is NOT HELPFUL — the user trusts your proposal reflects reality, and you're wasting their approval on fiction.**

Design without exploration is not "efficiency" — it is fabricating an approach from imagination. The user trusts your proposal reflects the actual codebase. If it doesn't, you wasted their approval on fiction.

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
- `.planning/SPEC.md` - final requirements
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

4. **Document remaining features** in `.planning/BACKLOG.md`:
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

After user chooses approach AND confirms scope, write `.planning/PLAN.md`:

### PLAN.md Template

Use the template from `references/plan-template.md` for the PLAN.md structure. Load it before writing the plan:

Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-design/references/plan-template.md` and follow its instructions.

### 6. User Gate - Final Approval

**Checkpoint type:** decision (user chooses architecture — cannot auto-advance)

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

**Checkpoint type:** decision (user chooses workspace setup — cannot auto-advance)

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
- **Testing Strategy** - Framework, command, first test, location, skill
- **REAL Test Criteria** - User workflow, protocol, UI elements, what user sees
- **Files to Modify** - Specific paths with change descriptions
- **New Files** - If any, with purposes
- **Implementation Order** - Ordered task list with dependencies and `implements` column mapping tasks to requirement IDs from SPEC.md

## The Gate Function

Complete all steps before starting implementation:

```
1. REVIEW → Read SPEC.md and exploration findings
2. VERIFY TESTING → Check SPEC.md has automated testing strategy
   └─ If missing → STOP. Go back to clarify phase.
3. PROPOSE → Present 2-3 approaches with trade-offs
4. ASK → Use AskUserQuestion with clear options
5. DECOMPOSE → Ask "One feature or multiple?" (CRITICAL)
   └─ If multiple → List features, ask which first, write BACKLOG.md
6. WAIT → Do NOT proceed until user responds
7. DOCUMENT → Write PLAN.md with Testing Strategy section FILLED
8. VERIFY PLAN → Check PLAN.md Testing Strategy table has all boxes checked
   └─ If any unchecked → STOP. Fill them before proceeding.
9. CONFIRM → Ask "Ready to proceed?"
10. WORKSPACE → Ask "Create worktree?" (Yes recommended / No)
11. SETUP → If worktree Yes, invoke dev-worktree
12. GATE → Only start /dev-implement after all approvals
```

**Mandatory steps (NEVER skip):** VERIFY TESTING, DECOMPOSE, VERIFY PLAN, WAIT, WORKSPACE, and GATE.

### Testing Strategy Verification (Step 2 & 8)

Before proceeding past step 2, verify SPEC.md contains:
```
[ ] Testing approach (unit/integration/E2E)
[ ] Test framework (pytest/jest/playwright)
[ ] Test command (how to run)
[ ] Testing skill specified (dev-test-electron/playwright/etc.)
```

Before proceeding past step 8, verify PLAN.md Testing Strategy table:
```
[ ] Framework filled
[ ] Test Command filled
[ ] First Failing Test described
[ ] Test File Location specified
[ ] Testing Skill specified
```

**If any box is unchecked → STOP. Do not proceed.**

### REAL Test Verification (Step 8 - CRITICAL)

Before proceeding past step 8, verify PLAN.md REAL Test Criteria table:

```
[ ] User workflow documented (exact steps user takes)
[ ] Protocol matches production (WebSocket/HTTP/IPC/etc.)
[ ] UI elements identified (what user interacts with)
[ ] User-visible output documented (what user sees)
[ ] Code path specified (same path as production)
```

**If any box is unchecked → You WILL write fake tests. Fix now.**

### Fake Test Prevention Check (Step 8)

Ask yourself before proceeding:
1. Will the test use the SAME protocol as production? (Not a substitute)
2. Will the test follow the EXACT user workflow? (Not shortcuts)
3. Will the test use the SPECIFIED testing skill? (Not your own approach)
4. Will the test verify what the USER sees? (Not internal state)

If ANY answer is "no" → STOP. Fix the REAL Test Criteria section.

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

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "I'll pick the best approach for them" | User had context you lacked — your choice was wrong | **Anti-helpful** |
| **Competence** | "Only one viable option, no need to ask" | User sees alternatives you missed — your confidence was arrogance | **Incompetent** |
| **Efficiency** | "Skip user approval to move faster" | Wrong approach means full rework | **Inefficient** |

**The protocol is not overhead you pay. It is the service you provide.**

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
- `.planning/PLAN.md` written with chosen approach
- **User explicitly approved** ("Yes, proceed")

## Phase Complete

**After user approves ("Yes, proceed"):**

1. **Plan Review Gate (MANDATORY):**
   Discover and read the plan reviewer skill:Read `${CLAUDE_PLUGIN_ROOT}/skills/dev-plan-reviewer/SKILL.md` and follow its instructions.
   Follow the plan reviewer's instructions:
   - If >15 tasks → chunk the plan first, review per-chunk
   - Dispatch reviewer subagent
   - If ISSUES_FOUND → fix PLAN.md → re-dispatch (max 5 iterations)
   - If APPROVED → proceed to worktree question

2. **Ask about worktree** (Step 7 above)
3. **If worktree chosen:**
   - Invoke `Skill(skill="workflows:dev-worktree")`
   - After worktree created, discover and read `skills/dev-implement/SKILL.md` via cache lookup, then invoke with `Read()`
4. **If no worktree:**
   - Directly discover and read `skills/dev-implement/SKILL.md` via cache lookup, then invoke with `Read()`

**Required before proceeding:**
- Explicit user approval for implementation
- Feature scope decision (one feature vs multiple)
- User choice on worktree (Yes/No)

**After this feature is implemented and PR'd:**

If multiple features were identified in step 4, check `.planning/BACKLOG.md` for remaining features:
1. View remaining features in BACKLOG.md
2. Invoke `/dev` again to tackle the next feature
3. Repeat until all features are complete

This enables incremental development: one feature → PR → merge → next feature.
