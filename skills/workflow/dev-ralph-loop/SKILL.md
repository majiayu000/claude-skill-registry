---
name: dev-ralph-loop
description: "Per-task ralph loop pattern for implementation and debugging. One loop per task, not one loop per feature."
---

**Announce:** "I'm using dev-ralph-loop to set up verification loops."

<EXTREMELY-IMPORTANT>
## Load TDD Enforcement (REQUIRED)

Before starting ANY ralph loop, you MUST load the TDD skill to remember the testing gates and task reframing:

```
Skill(skill="workflows:dev-tdd")
```

This loads:
- Task reframing (your job is writing tests, not features)
- The Execution Gate (6 mandatory gates before E2E testing)
- GATE 5: READ LOGS (mandatory - cannot skip)
- The Iron Law of TDD (test-first approach)

**Read dev-tdd skill content now before proceeding with ralph loops.**
</EXTREMELY-IMPORTANT>

## Contents

- [The Iron Law](#the-iron-law-of-ralph-loops)
- [Per-Task Pattern](#the-per-task-pattern)
- [Starting a Loop](#starting-a-loop)
- [Inside the Loop](#inside-the-loop)
- [Completing a Loop](#completing-a-loop)
- [Example: Multi-Task Feature](#example-multi-task-feature)
- [Rationalizations](#rationalization-prevention)

# Ralph Loop Pattern

<EXTREMELY-IMPORTANT>
## The Iron Law of Ralph Loops

**ONE LOOP PER TASK. NOT ONE LOOP PER FEATURE. This is not negotiable.**

A single feature-level loop provides ZERO per-task enforcement. You can just move to the next task without the loop actually gating anything.

Each task in PLAN.md gets its own ralph loop with its own completion promise.
</EXTREMELY-IMPORTANT>

## The Per-Task Pattern

```
For task N in PLAN.md (1, 2, 3, ...):
    1. Start ralph loop for task N
    2. Inside loop: spawn Task agents, iterate until done
    3. Output promise → loop ends
    4. Move to task N+1, start NEW ralph loop
```

**Why per-task loops?**
- Feature loops don't enforce task completion
- Without a loop per task, you can just... move on
- Each task needs its own completion gate
- The promise is your proof that the task is done

## Starting a Loop

**IMPORTANT:** Avoid parentheses `()` in the prompt - they break zsh argument parsing.
Use dashes or brackets instead.

### For Implementation Tasks

```
Skill(skill="ralph-loop:ralph-loop", args="Task N: [TASK NAME] --max-iterations 10 --completion-promise TASKN_DONE")
```

### For Debug Tasks

```
Skill(skill="ralph-loop:ralph-loop", args="Debug: [SYMPTOM] --max-iterations 15 --completion-promise FIXED")
```

### Parameters

| Parameter | Purpose | Recommendation |
|-----------|---------|----------------|
| Prompt | What this loop is for | Be specific: "Task 2: Add auth service" |
| `--max-iterations` | Safety limit | 10 for implementation, 15 for debugging |
| `--completion-promise` | The completion gate | Unique per task: TASK1_DONE, TASK2_DONE, etc. |

## Inside the Loop

Each iteration follows this pattern:

### 1. Spawn Task Agent

```
Task(subagent_type="general-purpose", prompt="""
[TASK-SPECIFIC INSTRUCTIONS]

Context:
- Read .claude/LEARNINGS.md for prior attempts
- Read .claude/SPEC.md for requirements
- Read .claude/PLAN.md for approach

Report back: what was done, results, any blockers.
""")
```

### 2. Verify Results

After Task agent returns:
- Check if the work is actually complete
- Verify tests pass (for implementation)
- Verify bug is fixed (for debugging)

### 3. Decide: Promise or Iterate

**If complete:** Output the promise
```
<promise>TASKN_DONE</promise>
```

**If incomplete:** Do NOT output promise. Spawn another Task agent to continue.

<EXTREMELY-IMPORTANT>
## Promise Rules

**You may ONLY output the promise when the statement is COMPLETELY AND UNEQUIVOCALLY TRUE.**

The promise is a claim that:
- For implementation: "This task's tests pass. The implementation is complete."
- For debugging: "The bug is fixed. Regression test passes."

You may NOT output the promise to:
- "Move on" to the next task
- "Try something else"
- Skip verification

**If the promise isn't true, don't output it. Keep iterating.**
</EXTREMELY-IMPORTANT>

## Completing a Loop

When you output the promise, the ralph loop ends. Then:

1. Document completion in LEARNINGS.md
2. Move to the next task
3. Start a NEW ralph loop for that task

## Example: Multi-Task Feature

```
## Task 1: Create types
Skill(skill="ralph-loop:ralph-loop", args="Task 1: Create types --max-iterations 5 --completion-promise TASK1_DONE")

[Spawn Task agent → implements types]
[Verify: tsc --noEmit passes]

<promise>TASK1_DONE</promise>

## Task 2: Add service method
Skill(skill="ralph-loop:ralph-loop", args="Task 2: Add service method --max-iterations 10 --completion-promise TASK2_DONE")

[Spawn Task agent → implements method]
[Verify: tests fail → iterate]
[Spawn Task agent → fixes tests]
[Verify: tests pass]

<promise>TASK2_DONE</promise>

## Task 3: Add route handler
Skill(skill="ralph-loop:ralph-loop", args="Task 3: Add route handler --max-iterations 10 --completion-promise TASK3_DONE")

[Spawn Task agent → implements route]
[Verify: integration test passes]

<promise>TASK3_DONE</promise>

## All tasks complete
```

## Rationalization Prevention

These thoughts mean STOP—you're about to skip enforcement:

| Thought | Reality |
|---------|---------|
| "One loop for the whole feature" | NO. One loop PER TASK. Feature loops don't enforce. |
| "I'll just move to the next task" | Did the current task's loop complete? If no loop, no gate. |
| "Per-task loops are overhead" | Per-task loops are the ONLY enforcement. |
| "Ralph is for hard problems" | Ralph is for ALL tasks. Simple tasks need gates too. |
| "I'll iterate without the loop" | Without ralph, you'll declare done prematurely. |
| "The ceremony isn't worth it" | The ceremony IS the value. It prevents shortcuts. |
| "I'll cherry-pick the parts I need" | Skills are protocols, not menus. Follow all of it. |
| "Tests passed on first try, skip loop" | Still need the loop structure. Lucky ≠ verified. |
| "Task done, let me check in" | NO. Start next task's loop immediately. |
| "User might want to review" | User wants ALL tasks done. Keep going. |
| "Natural pause point" | Only pause when ALL tasks complete. |

**Each task needs its own ralph loop. One feature loop provides ZERO per-task enforcement.**

**After outputting a promise, IMMEDIATELY start the next task's loop. Do NOT pause for user review.**

## When NOT to Use Ralph Loops

Ralph loops are for:
- Implementation tasks (dev-implement)
- Bug fixes (dev-debug)

Ralph loops are NOT for:
- Exploration (dev-explore)
- Design (dev-design)
- Data science (ds uses output-first verification instead)
- Review phases (dev-review, ds-review)

## Integration

This skill is invoked by:
- `dev-implement` - for implementation tasks
- `dev-debug` - for bug investigation and fixes

After all tasks complete, proceed to the next phase of the parent workflow.
