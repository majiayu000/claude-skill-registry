---
name: skill-gate
description: |
  Before starting any significant task, force explicit evaluation of available
  skills. For each potentially relevant skill, state YES/NO with reasoning.
  Only proceed to implementation after skills have been consciously evaluated
  and activated. Prevents the ~50% "coin flip" activation rate that occurs
  when skills are passively available but not deliberately considered.
allowed-tools: |
  bash: ls, cat
  file: read
---

# Skill Gate

<purpose>
Skills don't help if they're not activated. Research shows passive skill
availability leads to ~50% activation (coin flip). Forced evaluation achieves
80-84% activation. This skill is the gate: no significant work begins until
skills have been explicitly evaluated and relevant ones activated.
</purpose>

## When To Activate

Trigger at the START of:

- Any task that will take more than a few minutes
- Any task involving architecture, refactoring, or significant decisions
- Any task where mistakes would be costly
- When user asks for help with a non-trivial problem
- Before writing any significant amount of code

Do NOT trigger for:

- Quick questions or explanations
- Trivial edits (typo fixes, small changes)
- When user explicitly says "just do it" or "skip the process"

## Instructions

### Step 1: Identify the Task Type

Categorize the incoming task:

```
Task: [Brief description]
Type: [Planning | Debugging | Implementation | Refactoring | Decision | Review | Other]
Complexity: [Trivial | Standard | Significant | Critical]
```

If Trivial, skip the gate. Otherwise, proceed.

### Step 2: Scan Available Skills

List potentially relevant skills for this task type:

```
Potentially relevant skills for [task type]:

| Skill | Relevant? | Reason |
|-------|-----------|--------|
| [skill-name] | YES/NO | [One sentence why] |
| [skill-name] | YES/NO | [One sentence why] |
| ... | ... | ... |
```

### Step 3: Activate Relevant Skills

For each YES skill, explicitly activate:

```
Activating skills:
1. [skill-name] - [what it will help with]
2. [skill-name] - [what it will help with]
```

### Step 4: Proceed with Task

Only NOW begin the actual work, with activated skills guiding the approach.

## Skill Categories Reference

<skill-categories>
**Planning & Risk**
- battle-plan: Complete planning ritual for significant tasks
- pre-mortem: Anticipate failure modes before starting
- you-sure: Pause before destructive actions
- split-decision: Multi-option analysis for decisions

**Debugging & Problem Solving**
- rubber-duck: Structured problem articulation
- zero-in: Scoped codebase searching
- debug-to-fix: Full debug cycle (elixir)

**Quality & Verification**
- prove-it: Verify outcomes, don't assume
- loose-ends: Check for cruft before committing
- trace-it: Map dependencies before modifying shared code

**Code Discipline**
- stay-in-lane: Match changes to request, prevent scope creep
- sanity-check: Validate assumptions before building on them
- keep-it-simple: Resist over-engineering

**Context & Learning**
- dont-be-greedy: Manage context window carefully
- breadcrumbs: Leave notes for future sessions
- learn-from-this: Extract learnings from failures
- skill-forge: Create new skills from discoveries

**Safety & Refactoring**
- safe-refactor: Refactoring with guardrails (elixir)
- careful-delete: Destruction with ceremony (elixir)
</skill-categories>

## Quick Reference: Task → Skills

<quick-reference>
| Task Type | Consider These Skills |
|-----------|----------------------|
| Debugging | rubber-duck, zero-in, debug-to-fix, prove-it |
| New Feature | battle-plan, pre-mortem, stay-in-lane, prove-it |
| Refactoring | trace-it, safe-refactor, pre-mortem, loose-ends |
| Architecture Decision | split-decision, pre-mortem, sanity-check |
| Deleting/Removing | careful-delete, you-sure, trace-it |
| Code Review | prove-it, loose-ends, sanity-check |
| Exploring Codebase | zero-in, dont-be-greedy, breadcrumbs |
| After Failure | learn-from-this, retrospective, skill-forge |
</quick-reference>

## NEVER

- Skip evaluation on significant tasks
- Rubber-stamp all skills as "not relevant" without real consideration
- Activate skills you won't actually use (noise)
- Let this become a slow ritual - be brisk and decisive
- Gate trivial tasks (wastes time, annoys user)

## ALWAYS

- Evaluate skills at task START, not midway
- Give real YES/NO reasoning, not perfunctory
- Actually follow activated skills' guidance
- Note when a skill SHOULD have been activated but wasn't (feedback loop)
- Be honest about task complexity

## Examples

### Example 1: Feature Request

User: "Add user authentication to the API"

```
Task: Add user authentication to API
Type: Implementation
Complexity: Significant

Potentially relevant skills:

| Skill | Relevant? | Reason |
|-------|-----------|--------|
| battle-plan | YES | Significant feature, needs planning |
| pre-mortem | YES | Auth has many failure modes |
| split-decision | YES | Multiple auth approaches exist |
| stay-in-lane | YES | Easy to over-scope auth |
| prove-it | YES | Must verify auth actually works |
| trace-it | NO | Not modifying existing shared code |
| rubber-duck | NO | Requirements seem clear |

Activating skills:
1. battle-plan - Plan before coding
2. pre-mortem - Anticipate auth failure modes (token expiry, etc.)
3. split-decision - JWT vs session vs OAuth decision
4. stay-in-lane - Only what's requested, not full RBAC
5. prove-it - Verify auth works end-to-end

Proceeding with battle-plan first...
```

### Example 2: Bug Fix

User: "The login page is broken, users can't sign in"

```
Task: Fix broken login
Type: Debugging
Complexity: Standard

Potentially relevant skills:

| Skill | Relevant? | Reason |
|-------|-----------|--------|
| rubber-duck | YES | Need to understand the actual problem |
| zero-in | YES | Need to find where the bug is |
| debug-to-fix | YES | Full debug cycle appropriate |
| prove-it | YES | Must verify fix actually works |
| pre-mortem | NO | Not planning, fixing |
| split-decision | NO | Need to find bug first, not choose approach |

Activating skills:
1. rubber-duck - Clarify expected vs actual behaviour
2. debug-to-fix - Systematic debug cycle
3. prove-it - Verify the fix

Starting with rubber-duck: What exactly happens when users try to sign in?
```

### Example 3: Trivial Task (Skip Gate)

User: "Fix the typo in the README - it says 'teh' instead of 'the'"

```
Task: Fix typo
Type: Implementation
Complexity: Trivial

[Gate skipped - trivial task]

Fixing typo...
```

## The 80/20 Rule

You don't need to evaluate every skill every time. Focus on:

1. The 3-4 most likely relevant skills for this task type
2. Any skill that addresses a known weakness (e.g., scope creep → stay-in-lane)
3. Quality gates (prove-it, loose-ends) for any code-producing task

Speed matters. Be decisive. The goal is conscious consideration, not bureaucracy.

## Why This Skill Exists

Claude has access to powerful skills but often forgets to use them. Not from
inability - from not pausing to consider. This gate creates that pause.

The difference between 50% and 80% activation is the difference between skills
being occasionally helpful and being reliably transformative.

Gate your work. Activate what matters. Then execute.
