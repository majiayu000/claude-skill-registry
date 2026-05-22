---
name: aico-subagent-driven
description: |
  Execute implementation plan by dispatching fresh subagent per task. Each task gets: Implementer → Spec Review → Quality Review. Two-stage review ensures both correctness and quality.

  Use this skill when:
  - Have implementation plan with multiple independent tasks
  - Want automated execution with quality gates after each task
  - Tasks are mostly independent (not tightly coupled)
  - User asks to "execute the plan", "run the tasks", "auto implement"

  Prerequisites: Must have plan from aico-*-plan or aico-*-task-breakdown skill.
  Process: For each task: Dispatch Implementer → Spec Review (passes?) → Quality Review (passes?) → Next task
  Review order: ALWAYS spec compliance first, THEN code quality.
---

# Subagent-Driven Development

## Process

```
1. Read plan, extract all tasks
      ↓
2. Create TodoWrite with all tasks
      ↓
3. For each task:
   a. Dispatch Implementer Subagent
   b. Implementer: implement, test, commit
   c. Dispatch Spec Reviewer (matches spec?)
   d. Spec issues? → Implementer fixes → re-review
   e. Dispatch Quality Reviewer (code quality?)
   f. Quality issues? → Implementer fixes → re-review
   g. Mark task complete
      ↓
4. All tasks complete → Final review → Done
```

## Review Order is Critical

```
Spec Compliance Review FIRST
        ↓
    ✅ Passes
        ↓
Code Quality Review SECOND
```

**Why:** No point reviewing code quality if it doesn't meet spec.

## Subagent Prompts

### Implementer

- Provide FULL task text (don't make subagent read file)
- Provide context (where task fits in plan)
- Require TDD and self-review

### Spec Reviewer

- Check: Does implementation match spec exactly?
- Missing anything? Added anything extra?

### Quality Reviewer

- Check: Tests, readability, error handling, performance, security
- Rate issues as Critical/Important/Minor

## Key Rules

- ALWAYS run both reviews (spec AND quality)
- MUST fix issues before proceeding to next task
- NEVER dispatch multiple implementers in parallel
- ALWAYS provide full task text to subagent
- Spec review FIRST, then quality review

## Red Flags

**Never:**

- Skip any review
- Proceed with unfixed issues
- Start quality review before spec passes
- Move to next task with open issues

**If issues found:**

- Same implementer fixes them
- Reviewer reviews again
- Repeat until approved

## Common Mistakes

- ❌ Skip spec review → ✅ Always verify spec first
- ❌ Skip quality review → ✅ Always check quality
- ❌ Wrong review order → ✅ Spec first, then quality
- ❌ Provide partial task text → ✅ Give full text
