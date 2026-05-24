---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# Subagent-Driven Development

Execute plan by dispatching fresh context per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh context per task + two-stage review = high quality, fast iteration

## When to Use

- Have implementation plan? ✓
- Tasks mostly independent? ✓
- Want fast iteration? ✓

## The Process

```
┌─────────────────────────────────────────────────────────────┐
│                    Per Task Cycle                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. Read task from plan                                    │
│   2. Execute task (implement, test, commit)                 │
│   3. Self-review for spec compliance                        │
│   4. Review for code quality                                │
│   5. Fix any issues found                                   │
│   6. Re-review until approved                               │
│   7. Move to next task                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Two-Stage Review

### Stage 1: Spec Compliance Review

Questions to answer:
- Does the implementation match the spec?
- Are all requirements addressed?
- Did the task do what it was supposed to do?

**Must pass before Stage 2.**

### Stage 2: Code Quality Review

Questions to answer:
- Is the code clean and readable?
- Are there any bugs or edge cases?
- Does it follow project conventions?
- Are tests comprehensive?

## Task Execution Flow

For each task in plan:

1. **Announce:** "Starting Task N: [description]"
2. **Execute:** Follow TDD (write test, watch fail, implement, watch pass)
3. **Commit:** `git commit -m "feat: [task description]"`
4. **Self-Review Stage 1:** Check spec compliance
5. **Self-Review Stage 2:** Check code quality
6. **Report:** "Task N complete. Summary: [what was done]"

## Common Mistakes

- Skipping the spec compliance review
- Starting code quality review before spec compliance passes
- Moving to next task with open issues
- Skipping the TDD cycle
- Not committing after each task

## Integration

**Required skills:**
- `test-driven-development` — Follow TDD for each task
- `writing-plans` — Creates the plan this skill executes
- `requesting-code-review` — Template for review process
